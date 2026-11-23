# Protocolo RS-485 v2 — Painel de Sinalização de 4 Salas

Referência: Especificação Rev. 5.0 (23/11/2026), seção 6. Implementado em
`firmware/master_mega/master_mega.ino` (Sala 1, mestre) e
`firmware/slave_uno/slave_uno.ino` (Salas 2, 3 e 4, escravos).

## 1. Camada física

| Item | Valor |
|---|---|
| Meio | RS-485 half-duplex, 1 par trançado (A/B) + malha (SH, referência) |
| Transceptor | MAX485 TTL em cada sala; DE e /RE jumpeados num único pino |
| Pino de direção | Mega **D2** · Uno **D4** (HIGH = transmite, LOW = ouve) |
| Serial | Mega **Serial1** (D18 TX1 / D19 RX1) · Uno **Serial** (D0 RX / D1 TX) |
| Formato | **9600 bps, 8N1** (1 byte = 10 bits ≈ 1,04 ms) |
| Topologia | Linha: S1 → S2 → S3 → S4; 120 Ω só na S1 e na S4; polarização 560 Ω só na S1 |
| Endereços | Mestre = Sala 1 (não tem ID). Escravos: **2, 3, 4** (`#define SLAVE_ID`) |

## 2. Quadros (sempre 6 bytes)

**Pedido (mestre → escravo)**

| Byte | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Campo | `0xA5` | ID (2–4) | SEQ | MASK_H | MASK_L | CRC8 |

**Resposta (escravo → mestre)**

| Byte | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Campo | `0x5A` | ID (2–4) | SEQ (o mesmo do pedido) | ESTADO_H | ESTADO_L | CRC8 |

- `MASK` (16 bits, `MASK_H` = byte alto): bit *i* = 1 → posição local *i* habilitada (*i* = 0…10). Bits 11–15 = 0.
- `ESTADO`: bit *i* = 1 → posição livre (vermelho); 0 → ocupada (verde). O escravo sempre manda 0 nas posições desabilitadas.
- `SEQ`: contador de 0 a 255 do mestre, incrementado a **cada pedido** (255 → 0). O escravo devolve o mesmo valor; o mestre descarta resposta com SEQ diferente (resposta atrasada).
- A máscara vai em **todo** pedido: se qualquer placa religar, em no máximo 300 ms tudo volta a ficar coerente.
- Posição local *i* da sala com ID *k* = posição global **P(15 + (k−2)×11 + i)**; no painel central é o LED de índice **14 + (k−2)×11 + i** (LED *n* = P(*n*+1)).

| Sala | ID | Posições | LEDs centrais (índice) |
|---|---|---|---|
| 2 | 2 | P15–P25 | 14–24 |
| 3 | 3 | P26–P36 | 25–35 |
| 4 | 4 | P37–P47 | 36–46 |

### CRC-8

- Polinômio **0x07** (x⁸ + x² + x + 1), valor inicial **0x00**, sem reflexão de entrada/saída, sem XOR final (CRC-8 "SMBus").
- Calculado sobre os **5 primeiros bytes**; o resultado é o 6º byte.
- Valor de conferência: CRC-8 de `"123456789"` (ASCII) = **0xF4**.
- Truque de conferência: o CRC dos **6** bytes de um quadro correto dá **0x00**.

```c
uint8_t crc8(const uint8_t *dados, uint8_t tamanho) {
  uint8_t crc = 0x00;
  for (uint8_t i = 0; i < tamanho; i++) {
    crc ^= dados[i];
    for (uint8_t b = 0; b < 8; b++) {
      if (crc & 0x80) crc = (uint8_t)((crc << 1) ^ 0x07);
      else            crc = (uint8_t)(crc << 1);
    }
  }
  return crc;
}
```

## 3. Exemplos (CRC conferido com script Python)

| Situação | Quadro (hex) |
|---|---|
| Pedido à Sala 2, SEQ 0x01, todas as 11 habilitadas (`0x07FF`) | `A5 02 01 07 FF C1` |
| Resposta da Sala 2, SEQ 0x01, posições 0 e 2 livres (P15 e P17 vermelhas) | `5A 02 01 00 05 7B` |
| Pedido à Sala 3, SEQ 0x2A, preset TÍPICO 35 (7 primeiras: `0x007F`) | `A5 03 2A 00 7F 9A` |
| Resposta da Sala 3, SEQ 0x2A, todas ocupadas | `5A 03 2A 00 00 D9` |
| Pedido à Sala 4, SEQ 0xFF, preset PLANTÃO 20 (4 primeiras: `0x000F`) | `A5 04 FF 00 0F 40` |
| Resposta da Sala 4, SEQ 0xFF, posição 3 livre (P40 vermelha) | `5A 04 FF 00 08 6C` |

## 4. Tempos

| Evento | Tempo |
|---|---|
| Duração de um quadro (6 bytes a 9600 bps) | ≈ 6,25 ms |
| Intervalo entre pedidos do mestre | **100 ms** (ordem S2 → S3 → S4; ciclo completo **300 ms**) |
| Atraso do escravo antes de responder | **~1 ms** após o último byte do pedido |
| Espera máxima do mestre pela resposta | **25 ms** (resposta normal chega em ≈ 7,5 ms) |
| Pausa máxima entre bytes do mesmo quadro (escravo) | **5 ms**; passou disso, o quadro é descartado |
| Sala considerada offline (mestre) | **2000 ms** sem resposta válida |
| Escravo considera central ausente | **3000 ms** sem pedido válido para o seu ID |

Sequência de um pedido no mestre (polling síncrono):
1. Joga fora bytes antigos do buffer de recepção.
2. D2 = HIGH, envia 6 bytes, `Serial1.flush()` (espera o último bit sair), D2 = LOW.
3. Espera até 25 ms pela resposta; **durante a espera não chama `strip.show()`** (o envio para os WS2812B desliga as interrupções e faria perder bytes).
4. Resposta válida (início `0x5A`, CRC, ID e SEQ corretos) → atualiza o estado; só então redesenha os LEDs.

No escravo: recepção byte a byte por máquina de estados (espera `0xA5`, junta 6 bytes); CRC errado ou ID de outra sala → silêncio total (nunca responde); quadro válido → aplica a máscara, aguarda ~1 ms, liga D4, envia a resposta, `Serial.flush()`, desliga D4.

## 5. Comportamento em falha

| Situação | O que acontece |
|---|---|
| Quadro com CRC errado | Descartado em silêncio (mestre e escravo). |
| Resposta com SEQ diferente | Descartada pelo mestre (resposta atrasada). |
| Escravo não responde por 2 s | As 11 posições da sala piscam **âmbar a 4 Hz** no painel central; buzzer dá **2 bipes curtos a cada 5 s** enquanto houver sala offline; LCD (MONITOR) mostra `DESAB:xx REDE:FALHA` alternando com `REDE: FALHA S3` (lista das salas). |
| Escravo volta a responder | Tudo volta ao normal sozinho na primeira resposta válida. |
| Escravo sem pedido válido por 3 s | Os 11 LEDs locais piscam âmbar 4 Hz. Botões continuam funcionando; o estado é enviado assim que a comunicação volta. |
| Escravo religado | Começa com todas as posições habilitadas e verdes; recebe a máscara correta no próximo pedido (≤ 300 ms). |
| Central religada | Restaura a máscara da EEPROM; todas as posições começam verdes; os escravos recebem a máscara no primeiro ciclo. |
| Posição desabilitada pela central | O escravo zera o bit "livre" dela (volta a ocupada) e ignora o botão; a central faz o mesmo. |

## 6. Como depurar

1. **LED da placa (D13)** — no Uno pisca a cada pedido válido recebido para o seu ID; no Mega pisca a cada resposta válida. Uno apagado = não está recebendo pedidos válidos (fiação A/B, ID errado, RO/DI soltos).
2. **Monitor Serial do Mega** (USB, **115200 bps**, `#define DEPURACAO 1`): mostra `Sala N ONLINE/OFFLINE` e, a cada 10 s, uma linha por sala:
   `S3 pedidos=100 ok=98 sem_resp=2 invalidas=0 ONLINE`
   - `sem_resp` alto → escravo desligado, ID errado, A/B invertidos ou DE/RE do escravo sem controle.
   - `invalidas` alto → ruído, terminação/polarização erradas, malha (SH) sem ligação, dois escravos com o mesmo ID.
3. **Multímetro** (tudo desligado): A–B ≈ 60 Ω (duas terminações de 120 Ω). Com a S1 ligada e o barramento em repouso: V(A−B) ≈ +250 mV ou mais.
4. **Escuta com adaptador USB-RS485** no PC (ligar só A, B e GND; sem terminador): terminal em modo hexadecimal, 9600 8N1. Deve aparecer a cada 100 ms um pedido `A5 …` seguido da resposta `5A …` com o mesmo ID e SEQ. Para conferir um CRC à mão, calcule o CRC-8 dos 6 bytes: tem que dar `00`.
5. **Problemas típicos**
   - Uno não grava → RO/DI do MAX485 ainda ligados em D0/D1.
   - Todas as salas offline → A/B invertidos na S1, D2 do Mega preso em HIGH, falta de polarização.
   - Só uma sala offline → `SLAVE_ID` errado naquela placa, emenda no Wago, R7 não removido em S2/S3 (sobrecarga de terminação).

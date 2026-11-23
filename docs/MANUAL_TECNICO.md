# Manual técnico — Painel de Sinalização de Posições em 4 Salas

Revisão 5.0 — 23/11/2026

Sistema de sinalização de ocupação de 47 posições distribuídas em 4 salas, com uma central (Arduino Mega 2560) e três estações remotas (Arduino Uno R3) ligadas por barramento RS-485, e LEDs RGB endereçáveis WS2812B.

Documentos relacionados:

- [Montagem e conexões](MONTAGEM_E_CONEXOES.md) — como soldar, crimpar e ligar cada ponto com confiabilidade
- [Lista de materiais](LISTA_DE_MATERIAIS.md) — itens, quantidades e preços de referência
- [Protocolo RS-485](PROTOCOLO_RS485.md) — quadros, CRC e tempos em detalhe

---

## Sumário

1. Visão geral e histórico
2. Arquitetura e topologia
3. Alimentação
4. Cabo entre salas
5. Terminação e polarização do barramento
6. Pinagem
7. Cores e estados
8. Operação
9. Protocolo (resumo)
10. Montagem (resumo)
11. Comissionamento
12. Manutenção
13. Solução de problemas
14. Dados de referência

---

## 1. Visão geral e histórico

### 1.1 O sistema antigo (110 V)

O sistema anterior funcionava em 110 V AC: em cada sala, o operador acionava um interruptor ou botão que ligava, por um fio dedicado, uma lâmpada correspondente no painel de madeira da Sala 1. Para as 47 posições havia perto de 50 condutores de 110 V percorrendo os eletrodutos entre as salas.

Problemas observados:

- **Segurança:** condutores e lâmpadas de 110 V montados em painéis e caixas de madeira, sem barreira de isolação adequada.
- **Ambiguidade:** lâmpada apagada podia significar posição livre, lâmpada queimada ou fio rompido.
- **Manutenção:** queima frequente de lâmpadas e grande quantidade de fios para inspecionar.
- **Sem flexibilidade:** não havia como desabilitar no dia as posições que não seriam usadas.

### 1.2 O sistema novo

- Toda a sinalização passa a operar em **5 V DC** (extrabaixa tensão), com fonte própria em cada sala.
- Entre as salas trafegam **apenas dados**, por um único cabo blindado de 2 vias (RS-485).
- Cada posição tem um **LED RGB WS2812B** com cores distintas para ocupada, livre, desabilitada e falha de comunicação.
- A central permite **habilitar ou desabilitar posições** no dia, com presets e memória (EEPROM).
- Falhas de comunicação são **detectadas e sinalizadas** (cor âmbar piscando, alarme sonoro e mensagem no LCD).

A desmontagem da fiação de 110 V deve ser feita por profissional habilitado, com os circuitos desligados e bloqueados, e os condutores antigos removidos ou isolados nas duas pontas.

---

## 2. Arquitetura e topologia

### 2.1 Salas, posições e placas

| Sala | Função | Placa | ID no barramento | Posições | LEDs |
|---|---|---|---|---|---|
| 1 | Central (mestre) | Arduino Mega 2560 R3 | 1 (mestre) | P01–P14 (14) | 47 (painel geral) |
| 2 | Estação remota | Arduino Uno R3 | 2 | P15–P25 (11) | 11 locais |
| 3 | Estação remota | Arduino Uno R3 | 3 | P26–P36 (11) | 11 locais |
| 4 | Estação remota | Arduino Uno R3 | 4 | P37–P47 (11) | 11 locais |

Total: 47 posições e 80 LEDs (47 na central + 3 × 11 nas remotas).

A Sala 1 tem, além disso: display LCD 20x2 com interface I²C, dois botões de configuração (NAV e HAB) e um buzzer.

### 2.2 Topologia

Barramento RS-485 half-duplex em linha (daisy-chain), 9600 bps 8N1. O cabo passa por todas as salas em sequência; não há derivações longas nem estrela.

```
  SALA 1 (central)           SALA 2              SALA 3              SALA 4
 +------------------+     +-------------+     +-------------+     +-------------+
 | Mega 2560        |     | Uno  ID 2   |     | Uno  ID 3   |     | Uno  ID 4   |
 | MAX485 + R7 120R |     | MAX485      |     | MAX485      |     | MAX485      |
 | 560R A->+5V      |     | (sem R7)    |     | (sem R7)    |     | + R7 120R   |
 | 560R B->GND      |     |             |     |             |     |             |
 | LCD, NAV, HAB    |     | 11 botões   |     | 11 botões   |     | 11 botões   |
 | buzzer, 14 botões|     | 11 LEDs     |     | 11 LEDs     |     | 11 LEDs     |
 | 47 LEDs          |     |             |     |             |     |             |
 | fonte 5V 3A      |     | fonte 5V 2A |     | fonte 5V 2A |     | fonte 5V 2A |
 +--------+---------+     +--+-------+--+     +--+-------+--+     +------+------+
          |                  |       |           |       |               |
          +==== 15 m ========+       +=== 12 m ==+       +==== 18 m =====+
            cabo blindado 2 vias: A, B + malha (SH)

  SH: direto ao GND na Sala 1; via 100 R ao GND nas Salas 2, 3 e 4
  Terminação 120 R só nas pontas (Salas 1 e 4)
```

Comprimento total do barramento: 15 + 12 + 18 = **45 m** (comprar 60 m). Para 9600 bps o RS-485 suporta mais de 1000 m; a distância aqui não é um limite.

### 2.3 Divisão de funções

- **Mestre (Sala 1):** guarda a máscara de habilitação das 47 posições, interroga uma remota a cada 100 ms, mostra o estado de todas as posições nos 47 LEDs, opera as 14 posições locais, a IHM (LCD + NAV + HAB) e o alarme.
- **Escravos (Salas 2, 3, 4):** leem os 11 botões locais, mantêm o estado (livre/ocupada) das suas posições, acendem os 11 LEDs locais conforme estado e máscara e respondem ao mestre quando interrogados.

---

## 3. Alimentação

### 3.1 Decisão: uma fonte em cada painel

- Sala 1: fonte 5 V **3 A** regulada.
- Salas 2, 3 e 4: fonte 5 V **2 A** regulada (tipo carregador ou colmeia).
- A fonte entra no **borne 5V/GND do shield** (pino 5V do Arduino, que é a linha regulada da placa). Não usar o jack P4 nem o VIN.
- Os LEDs WS2812B são alimentados **direto da fonte** (por um Wago de distribuição), não pelas trilhas do Arduino.
- **Nunca interligar o +5 V de salas diferentes.**
- O cabo entre salas **não leva energia**, só dados (A, B) e a referência (malha).

### 3.2 Por que não alimentar tudo a partir da Sala 1

Cálculo de verificação, considerando o cenário mais favorável que existia na versão antiga: cabo com **2 fios de 24 AWG por polo** (+5 V e GND) e **0,2 A por sala remota**.

Dados:

- Resistência de um fio 24 AWG: cerca de 0,0842 Ω/m.
- Dois fios em paralelo por polo: 0,0421 Ω/m. Ida (+5 V) e volta (GND): **0,0842 Ω por metro de percurso** (resistência de laço).
- Tensão na saída da fonte da Sala 1: 5,10 V.
- Corrente em cada trecho: o trecho 1 leva a corrente das três remotas, o trecho 2 a das Salas 3 e 4, o trecho 3 só a da Sala 4.

| Trecho | Comprimento | Corrente | Resistência de laço | Queda |
|---|---|---|---|---|
| Sala 1 → Sala 2 | 15 m | 0,6 A | 15 × 0,0842 = 1,263 Ω | 0,758 V |
| Sala 2 → Sala 3 | 12 m | 0,4 A | 12 × 0,0842 = 1,010 Ω | 0,404 V |
| Sala 3 → Sala 4 | 18 m | 0,2 A | 18 × 0,0842 = 1,516 Ω | 0,303 V |
| **Total** | 45 m | | | **1,465 V** |

Tensão que chegaria em cada sala:

| Ponto | Tensão |
|---|---|
| Fonte (Sala 1) | 5,10 V |
| Sala 2 | 5,10 − 0,758 = 4,34 V |
| Sala 3 | 4,34 − 0,404 = 3,94 V |
| Sala 4 | 3,94 − 0,303 = **3,64 V (≈ 3,6 V)** |

Com 3,6 V a Sala 4 fica muito abaixo do mínimo para operação confiável do ATmega328P a 16 MHz e dos WS2812B (cerca de 4,5 V). Mesmo a Sala 2 já ficaria abaixo de 4,5 V. Com um único fio por polo (cabo de 2 vias levando energia), as quedas dobrariam. Por isso cada sala tem fonte própria e o cabo leva só dados.

Também não se deve "equalizar" fontes ligando o +5 V de uma sala na outra: fontes em paralelo por um cabo longo trocam corrente entre si, e qualquer diferença de tensão vira corrente de laço no cabo.

### 3.3 Consumo estimado

Estimativas com brilho de 40% (`setBrightness(100)`) e uma cor por LED:

| Sala | Carga | Corrente típica | Fonte |
|---|---|---|---|
| 1 | Mega + LCD + MAX485 + buzzer + 47 LEDs | 0,6 a 0,8 A | 3 A |
| 2, 3, 4 | Uno + MAX485 + 11 LEDs | 0,15 a 0,2 A | 2 A |

As fontes têm folga grande. Mesmo numa falha de firmware que acendesse todos os LEDs em branco a 100% (cerca de 60 mA por LED), a central consumiria perto de 2,9 A e cada remota perto de 0,75 A — dentro da capacidade das fontes.

### 3.4 Desacoplamento

- 1000 µF/16 V + 100 nF na entrada de alimentação dos LEDs da Sala 1.
- 470 µF/16 V + 100 nF na entrada de alimentação dos LEDs de cada remota.
- 330 Ω em série no sinal de dados (DIN) do primeiro LED.

### 3.5 Gravação pelo USB

Com a fonte externa no pino 5V e o USB conectado ao mesmo tempo, as duas alimentações ficam em paralelo. Procedimento padrão: **desligar a fonte da sala, gravar pelo USB, desconectar o USB, religar a fonte**. Detalhes em [Montagem e conexões](MONTAGEM_E_CONEXOES.md#124-gravação-pelo-usb-com-a-fonte-ligada).

---

## 4. Cabo entre salas

### 4.1 Especificação

**Cabo blindado de 2 vias, par trançado, 24 AWG (0,20–0,30 mm²), com malha** — tipo cabo de microfone balanceado ou cabo RS-485 de 1 par.

| Condutor | Função |
|---|---|
| Via 1 | **A (+)** |
| Via 2 | **B (−)** |
| Malha | **SH** — referência comum (GND) e blindagem |

Anote a cor de cada via e use a mesma correspondência nas quatro salas.

### 4.2 Ligação da malha

| Sala | Ligação da malha (SH) |
|---|---|
| 1 | **Direto ao GND** |
| 2, 3, 4 | Ao GND **através de resistor de 100 Ω 1/4 W** |

O resistor de 100 Ω nas remotas limita a corrente que circularia pela malha se houver diferença de potencial entre os terras das salas (laço de terra), seguindo a recomendação usual de notas de aplicação de RS-485. Para o sinal de referência, 100 Ω é desprezível: as correntes de modo comum dos receptores são de microampères a poucos miliampères.

### 4.3 Por que usar a malha como referência

O RS-485 é diferencial, mas **não é isolado**: os transceptores só funcionam se a tensão de cada linha (A e B), medida em relação ao GND local, ficar dentro da faixa de modo comum de **−7 V a +12 V**. Isso exige uma referência comum entre as salas.

- Com fontes do tipo carregador (saída isolada da rede), o sistema **costuma** funcionar só com A e B, porque os GNDs "flutuam" e acabam se acomodando pelos próprios circuitos. Mas é exatamente esse tipo de instalação que apresenta falhas intermitentes (ruído de partida de motores, descarga eletrostática, fonte com fuga capacitiva).
- Usando a malha como referência, todos os GNDs ficam amarrados, a faixa de modo comum é garantida e o par fica blindado contra ruído — sem precisar de uma "terceira via".

### 4.4 Alternativa: UTP Cat5e

Aceita como alternativa mais barata por metro: **par azul** (branco-azul = A, azul = B) + **fio verde** como referência GND (mesma regra da malha: direto na Sala 1, via 100 Ω nas remotas). Os demais fios ficam sem uso. O cliente optou pelo cabo de 2 vias com malha.

### 4.5 Conexão nas caixas

- **Sem RJ45.** O cabo entra por **prensa-cabo PG7** e termina em **conectores de alavanca Wago 221-413** (um para A, um para B, um para SH), com ilhós nas pontas.
- Nas Salas 2 e 3, cada Wago junta: cabo que chega + cabo que sai + derivação curta até o MAX485 (≤ 30 cm).
- Nas Salas 1 e 4, só um cabo.

### 4.6 Lançamento

- Use eletroduto ou canaleta **exclusiva** para o cabo de dados; os eletrodutos da antiga fiação de 110 V, depois de esvaziados, podem ser reaproveitados.
- Não lance junto de circuitos de força. Se tiver de cruzar, cruze a 90°.
- Raio de curvatura de pelo menos 5 vezes o diâmetro do cabo; não tracione o cabo pelas vias, puxe pela capa.
- Deixe pelo menos 30 cm de sobra em cada ponta para preparação e laço de folga.

---

## 5. Terminação e polarização do barramento

### 5.1 Terminação

- Resistor de **120 Ω entre A e B só nas pontas da linha: Sala 1 e Sala 4.**
- Usa-se o resistor **R7 de 120 Ω que já vem no módulo MAX485.**
- **Remover (ou cortar) o R7 nos módulos das Salas 2 e 3.**

A 9600 bps e 45 m, o tempo de um bit (104 µs) é muito maior que o tempo de propagação no cabo (cerca de 0,25 µs), então reflexões não são críticas. Mesmo assim, a terminação nas pontas é a prática correta: reduz ruído, amortece transitórios e, junto com a polarização, define o nível de repouso da linha.

### 5.2 Polarização fail-safe (só na Sala 1)

Quando nenhum transceptor está transmitindo, a linha fica "solta". Sem polarização, ruído pode ser lido como bits falsos. Na Sala 1:

- **560 Ω de A para +5 V**
- **560 Ω de B para GND**

Tensão diferencial em repouso, com as duas terminações (120 Ω ∥ 120 Ω = 60 Ω):

```
  V(A-B) = 5 V × 60 / (560 + 60 + 560) = 5 × 60 / 1180 ≈ 0,254 V  (≈ +250 mV)
```

Os receptores do MAX485 garantem nível lógico 1 com V(A−B) ≥ +200 mV, então a linha em repouso é lida como "1" (estado de repouso da UART), sem bytes falsos.

Opcional: muitos módulos MAX485 já trazem resistores de polarização de alto valor (dezenas de kΩ) em A e B. Eles podem permanecer; o efeito sobre o cálculo acima é pequeno.

### 5.3 Conferência com o multímetro

Com **todas as fontes desligadas**, medir a resistência entre A e B em qualquer ponto da linha:

| Leitura A–B | Interpretação |
|---|---|
| **≈ 60 Ω** (54 a 64 Ω) | Correto: duas terminações (Salas 1 e 4) |
| ≈ 120 Ω | Só uma terminação: falta R7 numa ponta ou o cabo está interrompido entre o ponto de medição e uma das pontas |
| ≈ 40 Ω | Três terminações: R7 não foi retirado na Sala 2 ou na Sala 3 |
| ≈ 30 Ω | Quatro terminações: R7 presente em todas as salas |
| ≈ 0 Ω | Curto entre A e B (fiozinho da malha, Wago trocado) |
| Muito alto / aberto | Nenhuma terminação alcançada: cabo aberto perto do ponto de medição |

A rede de polarização e os circuitos sem alimentação podem baixar um pouco a leitura em relação aos 60 Ω teóricos.

---

## 6. Pinagem

### 6.1 Arduino Mega 2560 (Sala 1)

| Pino | Ligação |
|---|---|
| 5V / GND | Fonte 5 V 3 A (via borne do proto shield) |
| D18 TX1 | MAX485 DI |
| D19 RX1 | MAX485 RO |
| D2 | MAX485 DE + /RE (jumpeados) |
| D20 SDA / D21 SCL | LCD 20x2 I²C (PCF8574, endereço 0x27; alternativo 0x3F) |
| D4 | Botão NAV (N.A. para GND, INPUT_PULLUP) |
| D5 | Botão HAB (N.A. para GND, INPUT_PULLUP) |
| D6 | DIN do painel de 47 WS2812B, via resistor 330 Ω |
| D7 | Buzzer ativo 5 V (≤ 30 mA) |
| D22 … D35 | Botões P01 … P14 (N.A. para GND, INPUT_PULLUP) |

Correspondência dos botões locais: D22 = P01, D23 = P02, D24 = P03, ..., D35 = P14.

Ordem dos 47 LEDs da central: LED 1 = P01 ... LED 14 = P14 (Sala 1); LED 15 a 25 = P15 a P25 (Sala 2); LED 26 a 36 = P26 a P36 (Sala 3); LED 37 a 47 = P37 a P47 (Sala 4).

### 6.2 Arduino Uno R3 (Salas 2, 3 e 4)

| Pino | Ligação |
|---|---|
| 5V / GND | Fonte local 5 V 2 A (via borne do screw shield) |
| D0 RX | MAX485 RO (desconectar ao gravar via USB) |
| D1 TX | MAX485 DI (desconectar ao gravar via USB) |
| D4 | MAX485 DE + /RE |
| D5 | DIN dos 11 WS2812B locais, via 330 Ω |
| D6 … D12 | Posições 01 … 07 |
| A0 … A3 (D14 … D17) | Posições 08 … 11 |

Todos os botões: N.A. para GND, com INPUT_PULLUP.

| Posição local | Pino | Sala 2 | Sala 3 | Sala 4 |
|---|---|---|---|---|
| 01 | D6 | P15 | P26 | P37 |
| 02 | D7 | P16 | P27 | P38 |
| 03 | D8 | P17 | P28 | P39 |
| 04 | D9 | P18 | P29 | P40 |
| 05 | D10 | P19 | P30 | P41 |
| 06 | D11 | P20 | P31 | P42 |
| 07 | D12 | P21 | P32 | P43 |
| 08 | A0 | P22 | P33 | P44 |
| 09 | A1 | P23 | P34 | P45 |
| 10 | A2 | P24 | P35 | P46 |
| 11 | A3 | P25 | P36 | P47 |

### 6.3 Módulo MAX485 (todas as salas)

| Pino do módulo | Mega (Sala 1) | Uno (Salas 2–4) |
|---|---|---|
| RO | D19 (RX1) | D0 (RX) |
| DI | D18 (TX1) | D1 (TX) |
| DE + /RE | D2 | D4 |
| VCC | +5 V | +5 V |
| GND | GND | GND |
| A, B | Wago A, B | Wago A, B |
| R7 (120 Ω) | mantido | removido nas Salas 2 e 3, mantido na Sala 4 |

---

## 7. Cores e estados

Brilho de 40% (`setBrightness(100)`).

| Estado | Cor | RGB |
|---|---|---|
| Desabilitada no dia | azul escuro | (0, 0, 40) |
| Ocupada / em atendimento | verde | (0, 255, 0) |
| Livre | vermelho | (255, 0, 0) |
| Falha de comunicação | âmbar piscando 4 Hz | (255, 140, 0) |

Regras:

- Ao ligar, todas as posições habilitadas começam **verdes (ocupadas)**.
- Cada toque no botão da posição alterna **verde ↔ vermelho**.
- Posição desabilitada (azul): o botão é **ignorado**.
- Quando uma posição é desabilitada, seu estado volta a "ocupada" (ao ser reabilitada, aparece verde).

---

## 8. Operação

### 8.1 Central (Sala 1)

A central tem LCD 20x2 e dois botões: **NAV** e **HAB**. São três modos:

**MONITOR** (modo normal):

```
+--------------------+
|OCUP:32 LIVRE:10    |
|DESAB:05 REDE:OK    |
+--------------------+
```

Mostra quantas posições estão ocupadas, livres e desabilitadas, e o estado da rede. Em falha, o LCD indica a sala sem comunicação, por exemplo `REDE: FALHA S3`.

**SETUP** (habilitar/desabilitar posição por posição):

```
+--------------------+
|S2 P18 [HABILITADA] |
|NAV:prox HAB:muda   |
+--------------------+
```

- NAV: vai para a próxima posição (segurar = avança rápido).
- HAB: habilita/desabilita a posição mostrada.

**PRESETS** (configurações prontas):

```
+--------------------+
|PRESET: TIPICO 35   |
|NAV:gira HAB:aplica |
+--------------------+
```

- NAV: próximo preset.
- HAB: aplica e salva.

Mudança de modo:

| Ação | Resultado |
|---|---|
| NAV + HAB juntos por 1 s | Passa para o próximo modo (MONITOR → SETUP → PRESETS → MONITOR), com bipe |
| Um toque em NAV no MONITOR | Entra no SETUP |
| 60 s sem tocar em nenhum botão | Volta ao MONITOR |

Presets:

| Nº | Nome | Posições habilitadas | Total |
|---|---|---|---|
| 0 | 100% ATIVO | todas | 47 |
| 1 | TÍPICO 35 | Sala 1: as 14; cada remota: as 7 primeiras | 14 + 3 × 7 = 35 |
| 2 | PLANTÃO 20 | Sala 1: as 8 primeiras; cada remota: as 4 primeiras | 8 + 3 × 4 = 20 |
| 3 | ÚLTIMA CONFIGURAÇÃO | última configuração feita à mão no SETUP (área própria da EEPROM, não é sobrescrita pelos presets 0–2) | — |

Memória (EEPROM):

- A máscara de habilitação é gravada a cada mudança (gravação só dos bytes que mudaram, `EEPROM.update`).
- A gravação inclui um byte mágico e a versão do formato; ao ligar, a central restaura a última máscara.
- EEPROM virgem (placa nova) → 100% ativo.

Botões da Sala 1 (P01–P14): funcionam como os das remotas — cada toque alterna verde ↔ vermelho, se a posição estiver habilitada.

Todos os botões têm filtro de repique (debounce) de 40 ms, feito por software sem travar o programa.

### 8.2 Salas remotas

Cada sala tem 11 botões e 11 LEDs, um por posição:

1. **Posição em atendimento:** LED verde.
2. **Ao liberar a posição:** um toque no botão → LED vermelho (livre). Em até cerca de 0,3 s a central também mostra vermelho.
3. **Ao ocupar novamente:** outro toque → verde.
4. **LED azul escuro:** posição desabilitada pela central; o botão não faz nada.
5. **Todos os LEDs locais piscando âmbar:** a remota está há mais de 3 s sem receber pedido válido da central. Os botões continuam funcionando; o estado é enviado à central quando a comunicação voltar.

### 8.3 Comportamento em falhas

| Situação | Na central | Na sala remota |
|---|---|---|
| Remota sem resposta válida por 2 s | Posições daquela sala piscam âmbar 4 Hz; LCD `REDE: FALHA Sx`; buzzer 2 bipes curtos a cada 5 s enquanto houver sala offline | (se ela não recebe pedidos) LEDs locais piscam âmbar após 3 s |
| Comunicação volta | Volta sozinha ao normal | Volta sozinha ao normal |
| Remota é desligada e religada | Recebe de novo a máscara no próximo pedido (a máscara vai em todo pedido) | Volta com as posições habilitadas em verde (os estados "livre" anteriores se perdem) |
| Central é desligada e religada | Restaura a máscara da EEPROM; posições da Sala 1 voltam verdes | Continua com seu estado; recebe a máscara no próximo pedido |

---

## 9. Protocolo (resumo)

Detalhes completos em [Protocolo RS-485](PROTOCOLO_RS485.md).

- 9600 bps, 8N1, half-duplex. O mestre pergunta um escravo por vez; escravo só fala quando perguntado.

**Pedido (mestre → escravo), 6 bytes:**

```
[0xA5] [ID] [SEQ] [MASK_H] [MASK_L] [CRC8]
```

**Resposta (escravo → mestre), 6 bytes:**

```
[0x5A] [ID] [SEQ] [ESTADO_H] [ESTADO_L] [CRC8]
```

| Campo | Significado |
|---|---|
| ID | 2, 3 ou 4 (sala) |
| SEQ | Contador 0–255 do mestre; o escravo devolve o mesmo valor (o mestre descarta respostas atrasadas) |
| MASK | Bit i = 1 → posição local i habilitada (i = 0…10) |
| ESTADO | Bit i = 1 → posição livre (vermelho); 0 → ocupada (verde) |
| CRC8 | Polinômio 0x07, valor inicial 0x00, sem reflexão, sobre os 5 primeiros bytes |

Exemplo (preset TÍPICO 35 para a Sala 3, só as 7 primeiras posições habilitadas, SEQ = 0x2A):

```
Pedido:   A5 03 2A 00 7F 9A
Resposta: 5A 03 2A 00 05 C2   -> bits 0 e 2 = livres: P26 e P28 vermelhas
```

Tempos:

| Parâmetro | Valor |
|---|---|
| Intervalo entre pedidos do mestre | 100 ms (ciclo completo das 3 salas: 300 ms) |
| Espera máxima pela resposta | 25 ms |
| Intervalo máximo entre bytes do quadro (escravo) | 5 ms (acima disso o quadro é descartado) |
| Atraso do escravo antes de responder | ~1 ms |
| Sala considerada offline (mestre) | 2000 ms sem resposta válida |
| Escravo sinaliza falta de pedidos | 3000 ms sem pedido válido |

O mestre liga DE/RE em nível alto só para transmitir, espera o fim da transmissão (`Serial1.flush()`) e volta a nível baixo. A máscara vai em **todo** pedido: o sistema se corrige sozinho depois que qualquer placa é religada.

---

## 10. Montagem (resumo)

O passo a passo completo está em [Montagem e conexões](MONTAGEM_E_CONEXOES.md). Pontos principais:

- **Proibido** jumper Dupont e protoboard na instalação final.
- **Uno:** screw shield (bornes de parafuso) encaixado e travado com espaçador de nylon M3 + abraçadeira.
- **Mega:** Mega Proto Shield com barras de pinos, bornes KRE 5,08 mm e parte fixa dos plugáveis soldados.
- **Fios internos:** cabinho flexível de cobre estanhado 0,5 mm².
- **Todo fio em borne de parafuso ou Wago recebe ilhós crimpado** com alicate próprio. Nunca estanhar a ponta que vai sob parafuso.
- **Solda só em placa** (shield, pads dos pixels, módulo MAX485, adaptador do LCD), com termo-retrátil e limpeza do fluxo.
- **Botões de 22 mm:** terminal garfo + arruela de pressão (ou ilhós, se o contato tiver plaqueta).
- **Pixels:** fio 26 AWG soldado, termo-retrátil, alívio de tração com cola quente ou silicone neutro.
- **Chicote da porta:** borne plugável 5,08 mm com parafusos de trava (KF2EDG).
- **Alívio de tração:** PG7 na entrada, abraçadeira a cada 10–15 cm, laço de folga de 10 cm.
- **Placas** sobre espaçadores de nylon, nunca encostadas na madeira.
- **Anti-oxidação:** fio estanhado, verniz acrílico após os testes (com mascaramento), caixa fechada, sílica se úmido.
- **Anilha** numerada em todo fio.

---

## 11. Comissionamento

Execute depois do checklist de montagem (seção 16 de [Montagem e conexões](MONTAGEM_E_CONEXOES.md)). Instrumento: multímetro digital, salvo indicação. Recomenda-se fazer primeiro em bancada (todas as placas numa mesa, com pedaços curtos de cabo) e repetir no local.

| Item | Verificação | Como fazer | Critério de aceitação | OK |
|---|---|---|---|---|
| CK-01 | Isolação da rede antiga de 110 V | Com os circuitos antigos desligados e removidos, medir em escala AC entre os condutores remanescentes, botões, caixas e o terra | 0 V AC; nenhum condutor antigo conectado aos painéis | [ ] |
| CK-02 | Resistência do barramento | Todas as fontes desligadas; medir entre A e B (Wago da Sala 1 ou da Sala 4) | ≈ 60 Ω (54 a 64 Ω). Ver tabela da seção 5.3 se diferente | [ ] |
| CK-03 | Tensão das fontes em vazio | Cada fonte sozinha, sem carga, nos seus terminais de saída | 5,05 a 5,20 V DC | [ ] |
| CK-04 | Tensão em cada placa com carga | Sistema ligado, todas as posições habilitadas e acesas; medir no borne 5V/GND do shield em cada sala, com a fonte local daquela sala | ≥ 4,85 V DC em cada placa | [ ] |
| CK-05 | Polarização fail-safe | Sistema ligado; segurar o botão RESET do Mega (mestre para de transmitir) e medir V(A−B) em DC | ≈ +0,25 V (≥ +0,20 V). Se der ~+2 V ou mais, o transmissor da Sala 1 ficou habilitado durante o reset (DE/RE flutuando): repetir com DE/RE ligado provisoriamente ao GND | [ ] |
| CK-06 | Botões e repique | 10 toques rápidos em cada botão de cada sala | Cada toque alterna uma única vez, sem repique; LED local e LED da central mudam juntos | [ ] |
| CK-07 | Detecção de falha de rede | Soltar dos Wago as derivações A e B do MAX485 da Sala 3 e cronometrar | Em 2 s (±0,3 s): posições P26–P36 piscam âmbar na central, LCD `REDE: FALHA S3`, buzzer com 2 bipes a cada 5 s; após ~3 s os LEDs locais da Sala 3 piscam âmbar; Salas 2 e 4 continuam normais | [ ] |
| CK-08 | Recuperação automática | Recolocar as derivações sem reiniciar nenhuma placa; depois desligar e religar a fonte da Sala 2 | Retorno ao normal em menos de 0,5 s após reconectar; Sala 2 volta com a máscara correta sem intervenção | [ ] |
| CK-09 | Temperatura dos LEDs | Após 2 h de operação contínua, medir os pixels (termômetro infravermelho ou de contato) | ≤ temperatura ambiente + 10 °C | [ ] |
| CK-10 | Memória da configuração (EEPROM) | Aplicar um preset ou uma configuração personalizada; desligar a fonte da Sala 1 por 5 min; religar | A mesma máscara é restaurada (mesmas posições em azul) | [ ] |
| CK-11 | Tração e aperto | Puxar cada fio com ~2 kgf junto a cada borne, Wago, plugável e ilhós; reapertar todos os bornes de parafuso | Nenhum fio sai ou se move; nenhum parafuso folgado | [ ] |
| CK-12 | Inspeção visual | Inspecionar com lupa todas as soldas (shield, pixels, MAX485, LCD) e todos os ilhós | Soldas brilhantes em cone, sem ponte nem trinca; ilhós com crimpagem quadrada, sem fio para fora | [ ] |

Registre data, responsável e leituras medidas (não apenas "OK") para servir de referência em manutenções futuras.

---

## 12. Manutenção

### 12.1 Preventiva

| Quando | O quê |
|---|---|
| 30 dias após a instalação | Reapertar todos os bornes de parafuso (shield, KRE, plugáveis, botões). Repetir CK-11. |
| A cada 6 meses | Inspeção visual (fios, prensa-cabos, sinais de aquecimento ou oxidação), teste rápido de todos os botões (CK-06), conferência da tensão nas placas (CK-04). |
| A cada 12 meses | Reaperto geral, medição A–B com tudo desligado (CK-02), troca da sílica se houver. |

### 12.2 Troca de placa

**Uno de uma sala remota:**

1. Desligue a fonte da sala.
2. Solte o plugue da porta e, no screw shield, desaperte e retire os fios (as anilhas indicam o borne de cada um).
3. Retire a abraçadeira de travamento, o shield e o Uno.
4. Grave o firmware no Uno novo **com o `SLAVE_ID` da sala** (ver 12.3).
5. Monte o shield no Uno novo, recoloque os fios conforme as anilhas e a tabela, trave e religue.
6. Confira CK-06 naquela sala e veja no LCD da central se a rede está OK.

**Mega da Sala 1:** como o proto shield concentra as soldas, basta tirar o shield do Mega antigo, gravar o firmware no Mega novo e encaixar o shield. Na primeira partida a EEPROM do Mega novo está virgem: todas as posições ficam ativas; refaça a configuração ou aplique um preset.

**Módulo MAX485:** confira o R7 do módulo novo — **retire-o se for para a Sala 2 ou 3**. Marque o módulo.

**Pixel WS2812B queimado:** um pixel com defeito costuma apagar ou deixar com cores erradas todos os pixels **depois** dele. Troque o pixel por outro cortado da sobra da fita, respeitando a seta DIN → DOUT, e refaça termo-retrátil e alívio de tração.

### 12.3 Como regravar o firmware

1. Desligue a fonte da sala.
2. **Uno:** solte do screw shield os fios `RO` (D0) e `DI` (D1). **Mega:** não é preciso soltar nada (usa Serial1).
3. Conecte o USB, abra o firmware na Arduino IDE (`firmware/master_mega/master_mega.ino` ou `firmware/slave_uno/slave_uno.ino`), confira o `SLAVE_ID` (2, 3 ou 4) no caso do Uno, selecione a placa e a porta, e grave.
4. Desconecte o USB, recoloque `RO` e `DI` (Uno), religue a fonte.
5. Atualize a etiqueta da placa (sala, ID, data).

O passo a passo completo da Arduino IDE está no [README](../README.md).

---

## 13. Solução de problemas

| Sintoma | Causa provável | Ação |
|---|---|---|
| Posições de uma sala piscando âmbar na central; LCD `REDE: FALHA Sx` | Fonte da sala desligada; derivação A/B solta; A e B invertidos naquela sala; `SLAVE_ID` errado; RO/DI não recolocados após gravação | Verificar se a sala está ligada (LEDs locais acesos); conferir Wago e derivação; conferir cores A/B; conferir etiqueta/ID; conferir fios em D0/D1 |
| Todas as remotas offline | Cabo interrompido logo após a Sala 1; problema no MAX485 ou na ligação DE/RE da Sala 1; A/B invertidos na Sala 1; malha desligada; Mega travado | Medir A–B com tudo desligado (CK-02); conferir J2 e Wago da Sala 1; reiniciar o Mega; conferir D2, D18, D19 |
| Salas 3 e 4 offline, Sala 2 normal | Cabo interrompido entre as Salas 2 e 3, ou um dos Wago da Sala 2 com o cabo de saída solto | Conferir os Wago da Sala 2 (cabo que sai); medir continuidade do trecho |
| Comunicação intermitente (salas caem e voltam) | Malha não ligada (falta referência comum); R7 não retirado na Sala 2/3; mau contato em Wago ou ilhós; cabo junto de circuito de força | CK-02 (60 Ω?); conferir SH em todas as salas (direto na 1, 100 Ω nas outras); refazer ilhós suspeitos; afastar o cabo da fiação de força |
| Uma sala sempre offline (com LEDs locais âmbar) e outra intermitente | Duas placas gravadas com o mesmo `SLAVE_ID`: as duas respondem ao mesmo pedido e as respostas colidem | Conferir a etiqueta de cada placa; regravar a placa errada com o ID da sala |
| LED errado acende (posição trocada) | Ordem dos pixels diferente da ordem das posições; fio de botão no borne errado | Conferir a ordem física dos pixels (seção 6.1) e as anilhas contra a tabela de pinagem |
| A partir de um LED, os seguintes ficam apagados ou com cor aleatória | Pixel com defeito ou solda ruim no DOUT/DIN; pixel ligado ao contrário (seta invertida) | Inspecionar o último pixel que funciona e o primeiro que falha; refazer solda ou trocar o pixel |
| Nenhum LED acende | Falta 5 V nos LEDs; resistor 330 Ω aberto; primeiro pixel ao contrário; DIN no pino errado | Medir 5 V no pixel 1; conferir continuidade do DIN (D6 no Mega, D5 no Uno); conferir a seta |
| LEDs com cores erradas ou "tremidas" | GND dos LEDs não comum com o Arduino; falta o 330 Ω; tensão baixa no fim da fileira | Conferir GND comum; conferir resistor; injetar 5 V no fim (Sala 1) |
| LCD aceso mas sem texto (só retângulos ou nada) | Contraste desajustado | Girar o trimpot azul do adaptador I²C com chave pequena até aparecer o texto |
| LCD sem texto, mesmo ajustando o contraste | Endereço I²C diferente do firmware (0x27 x 0x3F); SDA/SCL invertidos; fio solto | Conferir o chip do adaptador (PCF8574 = 0x27, PCF8574A = 0x3F) e ajustar no firmware; conferir D20 = SDA, D21 = SCL |
| LCD totalmente apagado (sem luz de fundo) | Falta de 5 V/GND no LCD; jumper de luz de fundo do adaptador retirado | Medir 5 V no adaptador; recolocar o jumper "LED" |
| Botão não responde | Posição desabilitada (azul, comportamento normal); fio solto; contato N.F. usado no lugar do N.A.; retorno GND aberto | Verificar a cor do LED; testar o botão com multímetro; conferir garfo/ilhós e a ponte de GND |
| Botão alterna duas vezes ou sozinho | Contato do botão gasto; fio de botão passando junto de circuito de força | Trocar o bloco de contato; afastar a fiação; se persistir, 100 nF entre o pino e o GND junto ao borne |
| Uno não grava ("not in sync", tempo esgotado) | RO/DI ainda ligados em D0/D1; porta errada; driver CH340 ausente | Soltar RO e DI; escolher a porta certa; instalar o driver CH340 |
| Placa reinicia quando muitos LEDs acendem | Fonte fraca ou cabo da fonte fino; falta capacitor | Medir tensão no borne com carga (CK-04); trocar fonte/cabo; conferir 470/1000 µF |
| Buzzer não toca | Buzzer passivo em vez de ativo; polaridade invertida | Usar buzzer ativo 5 V; inverter os fios |
| Sistema volta sem a configuração do dia | EEPROM virgem (Mega trocado) ou gravação desativada | Aplicar o preset e conferir CK-10 |

---

## 14. Dados de referência

| Parâmetro | Valor |
|---|---|
| Posições | 47 (14 + 11 + 11 + 11) |
| LEDs | 80 WS2812B (47 + 33), brilho 40% |
| Barramento | RS-485 half-duplex, 9600 bps 8N1, daisy-chain |
| Comprimento | 15 + 12 + 18 = 45 m (comprar 60 m) |
| Cabo | Blindado 2 vias, par trançado, 24 AWG, malha |
| Terminação | 120 Ω (R7 do módulo) nas Salas 1 e 4 |
| Polarização | 560 Ω A→+5 V e 560 Ω B→GND na Sala 1; V(A−B) ≈ +250 mV |
| A–B desligado | ≈ 60 Ω |
| Malha | Direto ao GND na Sala 1; 100 Ω 1/4 W ao GND nas Salas 2, 3 e 4 |
| Fontes | 5 V 3 A (Sala 1); 5 V 2 A (Salas 2, 3, 4) |
| Tensão mínima na placa | 4,85 V |
| Bibliotecas | Mestre: Wire, EEPROM, LiquidCrystal_I2C (Frank de Brabander), Adafruit_NeoPixel. Escravo: Adafruit_NeoPixel |

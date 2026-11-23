# painel-salas-sinalizacao

Sistema de sinalização de ocupação de **47 posições em 4 salas**, com uma central (Arduino Mega 2560) e três estações remotas (Arduino Uno R3) ligadas por **RS-485** em um único cabo blindado de 2 vias. Cada posição tem um LED RGB **WS2812B** que indica se está ocupada, livre, desabilitada no dia ou sem comunicação.

Revisão 5.0 — 23/11/2026.

---

## Sumário

- [Problema e solução](#problema-e-solução)
- [Cores e estados](#cores-e-estados)
- [Arquitetura](#arquitetura)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Como gravar os firmwares](#como-gravar-os-firmwares)
- [Página interativa](#página-interativa)
- [Lista de materiais (resumo)](#lista-de-materiais-resumo)
- [Montagem (resumo)](#montagem-resumo)
- [Comissionamento (resumo)](#comissionamento-resumo)
- [Como regenerar a página](#como-regenerar-a-página)
- [Status e pendências](#status-e-pendências)
- [Licença](#licença)

---

## Problema e solução

**Sistema antigo.** A sinalização funcionava em 110 V AC: em cada sala, um interruptor ligava, por fio dedicado, uma lâmpada no painel de madeira da Sala 1. Eram perto de 50 condutores de 110 V entre as salas, lâmpadas queimando com frequência, e uma lâmpada apagada podia ser "posição livre", "lâmpada queimada" ou "fio rompido". Também não havia como desabilitar posições que não seriam usadas no dia.

**Sistema novo.**

- Tudo em **5 V DC**, com uma **fonte local em cada painel**.
- Entre as salas trafegam **só dados**, em um cabo blindado de 2 vias (par trançado + malha), barramento RS-485 a 9600 bps.
- LEDs RGB com quatro estados bem distintos, inclusive **falha de comunicação**, que é detectada e sinalizada automaticamente.
- Na central, um LCD 20x2 e dois botões permitem **habilitar ou desabilitar posições** no dia, com presets e memória em EEPROM.

---

## Cores e estados

| Estado | Cor | RGB |
|---|---|---|
| Desabilitada no dia | azul escuro | (0, 0, 40) |
| Ocupada / em atendimento | verde | (0, 255, 0) |
| Livre | vermelho | (255, 0, 0) |
| Falha de comunicação | âmbar piscando 4 Hz | (255, 140, 0) |

- Ao ligar, todas as posições habilitadas começam **verdes**.
- Cada toque no botão da posição alterna **verde ↔ vermelho**.
- Posição desabilitada (azul): o botão é ignorado.
- Brilho fixo em 40% (`setBrightness(100)`).

---

## Arquitetura

| Sala | Placa | ID | Posições |
|---|---|---|---|
| 1 (central) | Arduino Mega 2560 R3 + LCD 20x2 I²C + NAV/HAB + buzzer | mestre | P01–P14, e painel com os 47 LEDs |
| 2 | Arduino Uno R3 | 2 | P15–P25 |
| 3 | Arduino Uno R3 | 3 | P26–P36 |
| 4 | Arduino Uno R3 | 4 | P37–P47 |

```
   SALA 1                      SALA 2               SALA 3               SALA 4
 +----------------+          +-----------+        +-----------+        +-----------+
 | Arduino Mega   |          | Uno ID 2  |        | Uno ID 3  |        | Uno ID 4  |
 | MAX485         |  15 m    | MAX485    |  12 m  | MAX485    |  18 m  | MAX485    |
 | [120R] R7      |==========| (sem R7)  |========| (sem R7)  |========| [120R] R7 |
 | 560R A->+5V    | A, B, SH |           |        |           |        |           |
 | 560R B->GND    |          | SH-100R-GND        | SH-100R-GND        | SH-100R-GND
 | SH direto GND  |          |           |        |           |        |           |
 | fonte 5V 3A    |          | fonte 5V 2A        | fonte 5V 2A        | fonte 5V 2A
 +----------------+          +-----------+        +-----------+        +-----------+
   terminação                                                            terminação

   ===  cabo blindado 2 vias, par trançado 24 AWG: via 1 = A, via 2 = B, malha = SH
        (o cabo NÃO leva +5 V; cada sala tem sua própria fonte)
```

- RS-485 half-duplex, 9600 bps 8N1, em linha (daisy-chain), 45 m no total.
- Terminação de 120 Ω só nas pontas (Salas 1 e 4), usando o R7 do próprio módulo MAX485; **retirar o R7 nas Salas 2 e 3**.
- Polarização fail-safe na Sala 1 (V(A−B) ≈ +250 mV em repouso).
- O mestre interroga uma sala a cada 100 ms; sem resposta por 2 s, as posições daquela sala piscam âmbar na central, o LCD mostra a falha e o buzzer avisa.

Detalhes no [Manual técnico](docs/MANUAL_TECNICO.md) e no [Protocolo RS-485](docs/PROTOCOLO_RS485.md).

---

## Estrutura do repositório

```
README.md
.gitignore
index.html                                # redireciona para web/index.html (GitHub Pages)
firmware/master_mega/master_mega.ino      # Sala 1 (Mega 2560)
firmware/slave_uno/slave_uno.ino          # Salas 2, 3, 4 (Uno R3) — mudar SLAVE_ID
docs/MANUAL_TECNICO.md                    # manual completo (também embutido na página)
docs/MONTAGEM_E_CONEXOES.md               # solda, bornes, ilhós, confiabilidade
docs/LISTA_DE_MATERIAIS.md                # BOM com preços de referência
docs/PROTOCOLO_RS485.md                   # quadros, CRC, tempos
web/index.html                            # página interativa (gerada)
tools/build_unified_app.py                # gera web/index.html
tools/pe_tab.py                           # aba Projeto Elétrico (desenhos SVG)
tools/validate_app.js                     # validação da página
```

---

## Como gravar os firmwares

### 1. Preparar a Arduino IDE

1. Instale a **Arduino IDE 2.x** (arduino.cc → Software).
2. Baixe este repositório: botão **Code → Download ZIP** no GitHub e descompacte (ou `git clone`).
3. Instale as bibliotecas: menu **Ferramentas → Gerenciar bibliotecas...** (ou o ícone de livros na barra lateral), pesquise e instale:
   - **Adafruit NeoPixel** (autor: Adafruit) — usada no Mega e nos Uno;
   - **LiquidCrystal I2C** (autor: Frank de Brabander) — usada só no Mega.

   `Wire` e `EEPROM` já vêm com a IDE.
4. Placas Uno compatíveis com conversor **CH340** podem exigir o driver CH340 no Windows (se a porta COM não aparecer ao conectar a placa).

### 2. Gravar o Mega (Sala 1)

1. **Desligue a fonte do painel** da tomada (o USB alimenta a placa durante a gravação).
2. Conecte o Mega ao computador pelo USB.
3. Abra `firmware/master_mega/master_mega.ino`.
4. **Ferramentas → Placa → Arduino AVR Boards → Arduino Mega or Mega 2560**; **Processador: ATmega2560**.
5. **Ferramentas → Porta:** escolha a COM que apareceu ao conectar a placa.
6. Clique em **Verificar** (✓) e depois em **Carregar** (→). Aguarde "Carregamento concluído".
7. Desconecte o USB e religue a fonte.

No Mega não é preciso desligar o MAX485: ele usa a Serial1 (D18/D19), separada da USB.

Se o LCD não mostrar texto, ajuste o contraste (trimpot do adaptador I²C) e confira o endereço do LCD no firmware: **0x27** (PCF8574) ou **0x3F** (PCF8574A).

### 3. Gravar os Uno (Salas 2, 3 e 4)

O mesmo arquivo serve para as três salas; muda só o número da sala.

1. **Desligue a fonte do painel** da tomada.
2. **Solte do screw shield os dois fios do MAX485: D0 (fio `RO`) e D1 (fio `DI`).** No Uno, a USB e o MAX485 usam a mesma serial (D0/D1); com o MAX485 ligado a gravação falha ("not in sync" / tempo esgotado).
3. Conecte o Uno pelo USB.
4. Abra `firmware/slave_uno/slave_uno.ino`.
5. No início do arquivo, altere o identificador para a sala que vai receber a placa:

   ```cpp
   #define SLAVE_ID 2   // Sala 2 = 2, Sala 3 = 3, Sala 4 = 4
   ```

6. **Ferramentas → Placa → Arduino AVR Boards → Arduino Uno**; escolha a **Porta**.
7. **Verificar** (✓) e **Carregar** (→).
8. Desconecte o USB, **recoloque os fios RO (D0) e DI (D1)** e religue a fonte.
9. Etiquete a placa com a sala, o ID e a data. Duas placas com o mesmo ID derrubam a comunicação das duas salas.

---

## Página interativa

`web/index.html` é uma página única, autossuficiente, com o simulador do sistema, o projeto elétrico e o manual técnico embutido.

**Abrir localmente:** dê dois cliques em `web/index.html` (ou arraste-o para o navegador). Não precisa de servidor.

**Publicar com GitHub Pages.** O GitHub Pages, no modo "Deploy from a branch", só permite escolher a raiz (`/`) ou a pasta `/docs` — não a pasta `/web`. Duas formas de publicar:

**Opção A — publicar a raiz e acessar a subpasta (mais simples):**

1. No repositório: **Settings → Pages**.
2. **Source:** *Deploy from a branch*. **Branch:** `main`, pasta **`/ (root)`**. **Save**.
3. Aguarde alguns minutos. A página fica em:
   `https://marceloasl99.github.io/painel-salas-sinalizacao/web/`
   (o `index.html` da raiz do repositório redireciona para `web/`, então o endereço sem `/web/` também abre a página)

**Opção B — publicar só a pasta `/web` com GitHub Actions:**

1. Crie no repositório o arquivo `.github/workflows/pages.yml` com o conteúdo:

   ```yaml
   name: Publicar pagina
   on:
     push:
       branches: [main]
     workflow_dispatch:
   permissions:
     contents: read
     pages: write
     id-token: write
   concurrency:
     group: pages
     cancel-in-progress: true
   jobs:
     deploy:
       runs-on: ubuntu-latest
       environment:
         name: github-pages
       steps:
         - uses: actions/checkout@v4
         - uses: actions/configure-pages@v5
         - uses: actions/upload-pages-artifact@v3
           with:
             path: web
         - uses: actions/deploy-pages@v4
   ```

2. Em **Settings → Pages → Source**, escolha **GitHub Actions**.
3. Faça um commit na `main` (ou rode o workflow manualmente em **Actions**). A página fica em:
   `https://marceloasl99.github.io/painel-salas-sinalizacao/`

(As versões das actions indicadas eram as correntes na data desta revisão; se o GitHub avisar de versão obsoleta, atualize o número.)

---

## Lista de materiais (resumo)

Preços de **referência** de mercado (nov/2026). **Cote antes de comprar.**

| Cenário | Descrição | Subtotal | Reserva 15% | Total |
|---|---|---:|---:|---:|
| **A — Recomendado** | Uno nas 3 remotas, cabo 2 vias blindado, shields de borne, ilhós, Wago, plugáveis, verniz | R$ 979,00 | R$ 146,85 | **R$ 1.125,85** |
| **B — Econômico** | Mesma eletrônica; cabo UTP Cat5e (1 par + 1 fio), proto shield simples no lugar dos screw shields, sem plugáveis, sem verniz, 6 Wago | R$ 797,00 | R$ 119,55 | **R$ 916,55** |
| C — Industrial | Referência: entradas optoisoladas 24 V, botões novos, fontes DIN, cabo Belden | R$ 3.528,76 | R$ 529,31 | R$ 4.058,07 |

O cliente já possui o Mega 2560, um Uno R3 (Sala 2) e o LCD 20x2. Lista completa, totais por grupo e dicas de compra: [docs/LISTA_DE_MATERIAIS.md](docs/LISTA_DE_MATERIAIS.md).

---

## Montagem (resumo)

O guia completo — com passo a passo, tabelas de ligação e diagramas — está em [docs/MONTAGEM_E_CONEXOES.md](docs/MONTAGEM_E_CONEXOES.md). Regras principais:

- **Nada de jumper Dupont ou protoboard** na instalação final.
- **Uno:** screw shield (bornes de parafuso), travado com espaçador e abraçadeira. **Mega:** Mega Proto Shield com bornes KRE e plugáveis soldados.
- **Toda ponta de fio em borne ou Wago leva ilhós crimpado** com alicate próprio. **Nunca estanhar** a ponta que vai sob parafuso.
- **Solda só em placa** (shield, pixels, MAX485, LCD), com termo-retrátil e limpeza do fluxo com álcool isopropílico.
- Cabo entre salas entra por **prensa-cabo PG7** e termina em **Wago 221-413** (A, B, SH). Malha **direto ao GND na Sala 1** e **via 100 Ω** nas outras.
- **R7 (120 Ω) do MAX485:** manter nas Salas 1 e 4, **retirar nas Salas 2 e 3**.
- Fonte no **borne 5V/GND do shield**; LEDs alimentados direto da fonte; **nunca ligar o +5 V de uma sala na outra**.
- Chicote da porta em **borne plugável com parafusos de trava**; anilha em todo fio; placas sobre espaçadores; verniz depois dos testes.

---

## Comissionamento (resumo)

Lista completa (CK-01 a CK-12) no [Manual técnico](docs/MANUAL_TECNICO.md#11-comissionamento). Faça primeiro em bancada e depois no local.

| Item | Verificação | Critério |
|---|---|---|
| CK-01 | Rede antiga de 110 V | 0 V AC, nada antigo conectado |
| CK-02 | A–B com tudo desligado | ≈ 60 Ω |
| CK-03 | Fontes em vazio | 5,05 a 5,20 V |
| CK-04 | Cada placa com carga, fonte local | ≥ 4,85 V |
| CK-05 | Polarização (V(A−B) em repouso) | ≈ +250 mV (≥ +200 mV) |
| CK-06 | Botões (10 toques cada) | Alterna uma vez por toque |
| CK-07 | Falha de rede (soltar A/B da Sala 3) | Âmbar na central em 2 s, LCD e buzzer |
| CK-08 | Recuperação | Volta sozinho em menos de 0,5 s |
| CK-09 | Temperatura dos LEDs após 2 h | ≤ ambiente + 10 °C |
| CK-10 | EEPROM (desligar 5 min) | Configuração restaurada |
| CK-11 | Tração (~2 kgf) e reaperto | Nenhum fio sai |
| CK-12 | Inspeção com lupa | Soldas e ilhós aprovados |

---

## Como regenerar a página

A página `web/index.html` é **gerada**: não edite o HTML à mão. Altere os arquivos de origem (por exemplo, `docs/MANUAL_TECNICO.md`, `tools/build_unified_app.py`, `tools/pe_tab.py`) e rode, na raiz do repositório:

```bash
python tools/build_unified_app.py
node tools/validate_app.js
```

Requisitos: Python 3 e Node.js. O primeiro comando gera `web/index.html`; o segundo verifica a página gerada. Faça commit do `web/index.html` atualizado junto com as alterações de origem.

---

## Status e pendências

- **Preços são de referência** (nov/2026). Cotar com fornecedores antes de comprar.
- **Testar em bancada antes da instalação:** montar as 4 placas numa mesa, com pedaços curtos de cabo, e executar o comissionamento completo antes de levar para as salas.
- Conferir no local o comprimento real de cada trecho de cabo e o espaço disponível nos painéis e caixas existentes.
- Conferir o endereço I²C do LCD (0x27 ou 0x3F) na primeira gravação.
- Após a instalação, reapertar os bornes de parafuso em 30 dias.

---

## Licença

A definir pelo autor.

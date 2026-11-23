# Montagem e conexões — guia prático

Revisão 5.0 — 23/11/2026

Este guia explica **como fazer as ligações nos Arduinos e nos demais componentes** de forma que o painel funcione por anos sem fio solto, sem oxidação e sem mau contato. Ele complementa o [Manual técnico](MANUAL_TECNICO.md) (que explica o funcionamento) e a [Lista de materiais](LISTA_DE_MATERIAIS.md) (que diz o que comprar).

Público: técnico em eletrônica ou eletricista com prática de bancada. Nada aqui exige equipamento especial além de ferro de solda, alicate crimpador de ilhós e multímetro.

---

## Sumário

1. [Princípios](#1-princípios)
2. [Materiais e ferramentas](#2-materiais-e-ferramentas)
3. [Regra de ouro: o que solda, o que vai em borne, o que vai em conector](#3-regra-de-ouro-o-que-solda-o-que-vai-em-borne-o-que-vai-em-conector)
4. [Cores e identificação dos fios](#4-cores-e-identificação-dos-fios)
5. [Técnicas básicas: ilhós, solda e termo-retrátil](#5-técnicas-básicas-ilhós-solda-e-termo-retrátil)
6. [Salas 2, 3 e 4: Arduino Uno com screw shield](#6-salas-2-3-e-4-arduino-uno-com-screw-shield)
7. [Sala 1: Arduino Mega com proto shield](#7-sala-1-arduino-mega-com-proto-shield)
8. [Módulo MAX485](#8-módulo-max485)
9. [Cabo de 2 vias com malha e conectores Wago](#9-cabo-de-2-vias-com-malha-e-conectores-wago)
10. [Botões](#10-botões)
11. [Pixels WS2812B](#11-pixels-ws2812b)
12. [Alimentação](#12-alimentação)
13. [Chicote da porta com borne plugável](#13-chicote-da-porta-com-borne-plugável)
14. [Organização e fixação](#14-organização-e-fixação)
15. [Proteção contra oxidação](#15-proteção-contra-oxidação)
16. [Checklist final de montagem](#16-checklist-final-de-montagem)
17. [O que NÃO fazer](#17-o-que-não-fazer)

---

## 1. Princípios

Quase toda falha de campo em painéis como este é **mecânica**, não eletrônica: um fio que escapa do borne, uma emenda torcida que oxida, um jumper que se solta com a batida da porta, uma solda fria que trinca. Por isso a montagem segue quatro princípios:

1. **Cada ponto de ligação é feito do jeito certo para aquele tipo de ponto** (solda em placa, ilhós em borne, garfo em parafuso de botão). Não se improvisa.
2. **Nenhum fio trabalha à tração.** Todo cabo é preso antes de chegar ao ponto de ligação (prensa-cabo, abraçadeira, laço de folga).
3. **Tudo é identificado.** Anilha numerada em todo fio, igual às tabelas deste guia.
4. **Tudo é testado antes de fechar a caixa.** Continuidade, tensão, puxão de 2 kgf em cada fio e inspeção com lupa.

**Proibido na instalação final:** jumper Dupont, protoboard, emenda torcida com fita isolante e solda na ponta de fio que vai sob parafuso.

---

## 2. Materiais e ferramentas

### Materiais (todos constam da [Lista de materiais](LISTA_DE_MATERIAIS.md))

| Material | Onde é usado |
|---|---|
| Screw shield para Uno (3) | Salas 2, 3 e 4 — todos os fios do Uno chegam em borne de parafuso |
| Mega Proto Shield (1) + bornes KRE 5,08 mm | Sala 1 — bornes e plugáveis soldados no shield |
| Borne plugável 5,08 mm KF2EDG com parafusos de trava | Chicote entre a porta (botões, LEDs, LCD) e a placa |
| Wago 221-413 | Junção do cabo entre salas (A, B, SH) e distribuição de 5 V/GND |
| Cabinho flexível estanhado 0,5 mm² | Toda a fiação interna (alimentação e sinais) |
| Fio flexível 26 AWG, 3 cores | Ligação entre pixels WS2812B |
| Terminal tubular (ilhós) isolado | Toda ponta de fio que vai em borne de parafuso, Wago ou plugável |
| Terminal garfo pré-isolado | Contatos de parafuso dos botões de 22 mm |
| Termo-retrátil | Toda emenda soldada e todo pino soldado exposto |
| Espaçadores de nylon M3 | Fixação das placas na placa de montagem |
| Abraçadeiras, bases adesivas, anilhas | Organização, alívio de tração e identificação |
| Prensa-cabo PG7 | Toda entrada de cabo na caixa |
| Verniz acrílico (conformal coating) | Proteção das placas depois de testadas |

**Item extra recomendado (barato, não está na lista):** um pacote de ilhós **0,25 mm²** para as vias de 24 AWG do cabo entre salas (o kit da lista começa em 0,5 mm²). Ver [seção 9.2](#92-pontas-de-24-awg-ilhós-certo).

### Ferramentas

| Ferramenta | Observação |
|---|---|
| Alicate crimpador de ilhós autoajustável | Perfil quadrado (4 faces). Não use alicate universal para crimpar. |
| Ferro de solda 40–60 W com controle de temperatura | Ponta chanfrada (2–3 mm) para pads e pinos; ponta cônica fina ajuda no MAX485. |
| Solda 63/37 ou 60/40 com fluxo (0,5–0,8 mm) | Fio fino dá mais controle. |
| Fluxo em pasta ou caneta de fluxo | Para pads da fita e retrabalho. |
| Álcool isopropílico + escova antiestática (ou de dente, macia) | Limpeza do fluxo. |
| Alicate desencapador | Regule para não ferir os fios de cobre. |
| Alicate de corte rente | Corte de terminais e abraçadeiras. |
| Chaves de fenda 2,5 mm e 3,0 mm | Bornes do shield e KRE. |
| Multímetro com bipe de continuidade | Testes de continuidade, curto e tensão. |
| Lupa (5× a 10×) | Inspeção de soldas e ilhós. |
| Soprador térmico ou isqueiro de bancada | Termo-retrátil (soprador é melhor; chama queima a capa). |
| Dinamômetro de mão ou balança de bagagem (opcional) | Para calibrar a mão no teste de puxão de ~2 kgf. |

---

## 3. Regra de ouro: o que solda, o que vai em borne, o que vai em conector

| Tipo de ponto | Como ligar | Exemplos neste projeto |
|---|---|---|
| **Pad ou furo de placa** | **Solda** + termo-retrátil sobre o pino/emenda | Barras de pinos e bornes no proto shield do Mega; pads dos pixels WS2812B; pinos do módulo MAX485; pinos do adaptador I²C do LCD; resistores 560 Ω, 330 Ω e 100 Ω |
| **Borne de parafuso** (screw shield, KRE, plugável) | **Ilhós crimpado**. Nunca ponta estanhada, nunca fio nu torcido | Todos os pinos do Uno; bornes KRE do Mega; plugáveis da porta; borne A/B do MAX485 |
| **Conector de alavanca Wago 221** | **Ilhós crimpado** (fio flexível) | Junção A, B e SH do cabo entre salas; distribuição de 5 V e GND |
| **Parafuso de botão com arruela** | **Terminal garfo pré-isolado** + arruela de pressão (ou ilhós se o contato tiver plaqueta de pressão) | Blocos de contato dos botões de 22 mm |
| **Desconexão frequente** | **Borne plugável** com parafusos de trava | Chicote entre porta e placa |

Em resumo: **solda só em placa; parafuso e alavanca só com ilhós; nada de emenda solta no ar.** A única emenda em linha permitida é a do resistor de 100 Ω da malha (seção 9.5), soldada e coberta com termo-retrátil duplo.

---

## 4. Cores e identificação dos fios

Escolha um padrão e use-o **igual nas quatro salas**. Sugestão:

| Função | Cor do cabinho 0,5 mm² | Cor do 26 AWG (pixels) |
|---|---|---|
| +5 V | Vermelho | Vermelho |
| GND (0 V) | Preto | Preto |
| Dados dos LEDs (DIN) | Amarelo | Amarelo ou branco |
| RS-485 A | Laranja (ou a cor da via 1 do cabo) | — |
| RS-485 B | Azul (ou a cor da via 2 do cabo) | — |
| Botões, LCD, buzzer, DE/RE, RO, DI | Qualquer outra cor (branco, cinza, verde...) | — |

Se o rolo de 0,5 mm² for de cor única, identifique +5 V e GND com um anel de termo-retrátil vermelho e preto nas duas pontas, além da anilha.

**Anilhas:** toda ponta de fio recebe anilha com o mesmo nome usado nas tabelas das seções 6 e 7 (ex.: `RO`, `DE/RE`, `DIN`, `01`…`11`, `P01`…`P14`, `+5V`, `GND`, `A`, `B`, `SH`). Coloque a anilha **antes** de crimpar o ilhós, com a leitura voltada para quem abre a caixa.

**Cabo entre salas:** anote qual cor de via é A e qual é B (por exemplo, vermelho = A, branco = B) e mantenha a mesma escolha nas quatro salas. Inverter A e B numa sala derruba a comunicação daquela sala.

---

## 5. Técnicas básicas: ilhós, solda e termo-retrátil

### 5.1 Como crimpar ilhós corretamente

O ilhós (terminal tubular) mantém os fios finos do cabinho juntos sob o parafuso. Sem ele, o parafuso corta e espalha os fios, o contato fica só em alguns fios e afrouxa com o tempo.

```
  Fio desencapado no comprimento do tubo      Ilhós inserido até o colarinho
  ==========[||||||||]                        ==========[colar|=========]
            |<- L ->|                                         |<- L ->|
  L = comprimento do tubo metálico (ex.: 8 mm)

  Depois da crimpagem (perfil quadrado):
  ==========[colar|#########]     <- nenhum fio para fora, ponta rente ou até 0,5 mm
```

Passo a passo:

1. **Escolha o ilhós da seção do fio.** Cabinho 0,5 mm² → ilhós 0,5 mm². Fio de 24 AWG (0,2 mm²) → ilhós 0,25 mm². Ilhós grande demais fica frouxo mesmo crimpado.
2. **Coloque a anilha** no fio.
3. **Desencape no comprimento do tubo metálico** (normalmente 8 mm; meça o seu). Use o desencapador regulado: nenhum fio de cobre pode ser cortado ou ferido.
4. **Torça levemente** os fios (meia volta a uma volta), só para alinhar. Não estanhe.
5. **Insira até o colarinho**: a isolação do fio deve entrar no colarinho plástico e encostar no início do tubo. Confira que nenhum fio ficou para fora (dobrado no colarinho).
6. **Crimpe com o alicate próprio**, no meio do tubo, até o alicate liberar sozinho (autoajustável) ou até o fim do curso (catraca).
7. **Confira:** a ponta do cobre fica rente ao fim do tubo ou sobra até 0,5 mm; o tubo fica com seção quadrada uniforme, sem rachaduras.
8. **Teste de puxão:** segure o ilhós com um alicate e puxe o fio com ~2 kgf (o peso de uma garrafa de 2 litros). Não pode escorregar. Se escorregou, corte e refaça.

Ao apertar no borne: introduza o ilhós até o colarinho encostar no corpo do borne, aperte firme (sem espanar) e **puxe o fio** para confirmar.

### 5.2 Por que não estanhar a ponta do fio que vai sob parafuso

É um erro comum "estanhar a pontinha para ficar firme". Não faça isso em borne de parafuso, plugável ou Wago:

- A solda (liga de estanho e chumbo) é **mole e escoa sob pressão constante** (fluência a frio). Em semanas ou meses ela "afunda" sob o parafuso, o aperto cai e o contato fica frouxo.
- Contato frouxo tem resistência maior, esquenta, oxida, esquenta mais — e o defeito aparece como falha intermitente, a mais difícil de achar.
- A ponta estanhada também fica rígida e quebra logo atrás da solda quando o fio vibra.

O ilhós de cobre estanhado resolve as duas coisas: não escoa e distribui a força do parafuso em todos os fios.

**Estanhar é correto** quando o fio vai ser **soldado** num pad ou pino (pré-estanhar facilita a solda). O problema é só sob parafuso ou alavanca.

### 5.3 Como soldar bem

Configuração:

- Solda 63/37 (funde a 183 °C, solidifica de uma vez — mais fácil para quem tem pouca prática) ou 60/40, com fluxo no núcleo.
- Ferro a **350 °C** para pinos, bornes e fios de 0,5 mm². Para os pads da fita WS2812B, 320–350 °C e contato rápido (2 a 3 s) — a fita é flexível e o pad descola com calor prolongado.
- Ponta limpa e estanhada (passe na esponja úmida ou na palha de latão a cada 2 ou 3 soldas).

Procedimento para pino em placa (barra de pinos, borne KRE):

1. Aqueça **ao mesmo tempo o pad e o pino** com a ponta do ferro (1 a 2 s).
2. Encoste a solda **no lado oposto ao ferro** (no pad/pino, não na ponta do ferro). A solda deve escorrer e envolver o pino.
3. Retire a solda e, logo depois, o ferro. Não mexa na peça por 2 a 3 s.

Procedimento para fio em pad (pixel, MAX485, LCD):

1. Pré-estanhe o pad (pouca solda) e a ponta do fio (2 a 3 mm desencapados).
2. Encoste o fio estanhado no pad e aqueça os dois juntos até a solda fundir e unir. Sem fio de cobre aparecendo para fora da solda.

Como reconhecer:

```
  JUNTA BOA                       JUNTA FRIA / RUIM
     |  pino                          |  pino
    /|\                              (●)   <- bola, opaca, granulada,
   / | \   <- cone côncavo,           |       não "molha" o pad
  /__|__\     brilhante, liso       __|__
  ======== pad                      ======== pad (anel sem solda ou trincado)
```

| Junta boa | Junta ruim |
|---|---|
| Brilhante (63/37) ou acetinada uniforme | Opaca, cinza, granulada (fria) |
| Forma de cone ou "vulcão" côncavo | Forma de bola sobre o pino |
| Cobre todo o anel do pad | Anel do pad aparecendo, solda só de um lado |
| Contorno do pino visível sob a solda | Excesso escorrendo para o pad vizinho (ponte) |

Depois de soldar uma placa inteira:

- **Limpe o fluxo** com álcool isopropílico e escova macia. Resíduo de fluxo absorve umidade e pode causar fuga entre pinos ao longo do tempo, além de impedir a aderência do verniz.
- **Inspecione com lupa** todas as juntas.
- **Teste curto** entre pinos vizinhos com o multímetro (bipe).

Segurança: solde em local ventilado, não respire a fumaça do fluxo e lave as mãos depois de manusear solda com chumbo.

### 5.4 Termo-retrátil

- Coloque o tubo no fio **antes** de soldar (é o esquecimento mais comum).
- Escolha um diâmetro que passe folgado sobre a junta e, encolhido, aperte o fio (razão 2:1 ou 3:1).
- Cubra toda a parte metálica e mais 5 mm de isolação de cada lado.
- Encolha com soprador térmico, girando, sem queimar a capa.
- Em emendas em linha (resistor de 100 Ω da malha), use **duas camadas**: uma fina sobre a junta e outra maior sobre tudo.
- Em pinos soldados do MAX485 e do LCD, um pedaço curto de termo-retrátil sobre cada pino + fio evita curto entre pinos vizinhos e dá apoio mecânico à solda.

---

## 6. Salas 2, 3 e 4: Arduino Uno com screw shield

O screw shield é uma placa que encaixa sobre o Uno e leva cada pino para um borne de parafuso. Nenhum fio é soldado no Uno: a placa pode ser trocada em minutos.

### 6.1 Preparação, encaixe e travamento

1. **Teste o Uno sozinho antes** (grave o firmware pelo USB — ver [README](../README.md)) e confira que liga. Assim você não procura defeito de placa depois de tudo ligado.
2. **Fixe o Uno na placa de montagem** (MDF ou PVC) com espaçadores de nylon M3 de 10 a 15 mm. Use pelo menos 2 furos (3 se der; um dos furos do Uno fica muito perto da barra de pinos). A placa **nunca** encosta na madeira nem no fundo da caixa.
3. **Encaixe o screw shield** alinhando todas as barras de pinos (confira que nenhum pino ficou fora do soquete ou dobrado). Empurre por igual até o fim.
4. **Trave o shield:**
   - se os furos do shield coincidirem com os do Uno, use espaçadores M3 entre as duas placas (altura igual à da junção dos conectores, normalmente 11 a 13 mm) e parafuse;
   - em qualquer caso, passe **uma abraçadeira** pelos furos da placa de montagem, envolvendo Uno e shield juntos, sem apertar componentes (passe a fita entre os conectores, sobre a área sem peças). Isso impede que o shield se solte com vibração ou ao apertar bornes.
5. **Nunca use** o jack P4 nem o pino VIN: a alimentação entra pelo borne 5V/GND do shield.

### 6.2 Ordem de ligação

Ligue na ordem abaixo. Ela evita ter que passar fio por cima de fio já preso e deixa a alimentação por último (com fonte desligada da tomada durante toda a montagem).

1. Fixar na placa de montagem: Uno + shield, módulo MAX485, Wago (A, B, SH, +5V, GND) e o lado da placa do borne plugável.
2. Ligações do MAX485 ao shield (RO, DI, DE/RE, 5V, GND).
3. Fios de sinal do plugável ao shield (posições 01–11, DIN, GND dos botões).
4. Derivação do barramento (Wago → MAX485 A/B; Wago SH → 100 Ω → GND).
5. Alimentação (fonte → Wago → shield e LEDs).
6. Testes de continuidade e de curto **sem fonte**; só então energizar.

### 6.3 Tabela de ligação do Uno (borne → fio → anilha → destino)

| Borne do screw shield | Fio | Anilha | Destino |
|---|---|---|---|
| 5V | 0,5 mm² vermelho | `+5V` | Wago +5 V (saída da fonte) |
| GND | 0,5 mm² preto | `GND` | Wago GND (saída da fonte) |
| 5V (2º borne, ou ilhós duplo) | 0,5 mm² vermelho | `+5V-485` | MAX485 VCC (soldado no pino) |
| GND (2º borne) | 0,5 mm² preto | `GND-485` | MAX485 GND (soldado no pino) |
| GND (3º borne) | 0,5 mm² preto | `GND-SH` | Resistor 100 Ω em linha → Wago SH |
| D0 (RX) | 0,5 mm² cor de sinal | `RO` | MAX485 RO — **soltar ao gravar via USB** |
| D1 (TX) | 0,5 mm² cor de sinal | `DI` | MAX485 DI — **soltar ao gravar via USB** |
| D4 | 0,5 mm² cor de sinal | `DE/RE` | MAX485 DE e /RE (jumpeados no módulo) |
| D5 | 0,5 mm² amarelo | `DIN` | Plugável → 330 Ω no pad DIN do pixel 1 |
| D6 | 0,5 mm² | `01` | Plugável → botão da posição 01 |
| D7 | 0,5 mm² | `02` | Plugável → botão da posição 02 |
| D8 | 0,5 mm² | `03` | Plugável → botão da posição 03 |
| D9 | 0,5 mm² | `04` | Plugável → botão da posição 04 |
| D10 | 0,5 mm² | `05` | Plugável → botão da posição 05 |
| D11 | 0,5 mm² | `06` | Plugável → botão da posição 06 |
| D12 | 0,5 mm² | `07` | Plugável → botão da posição 07 |
| A0 (D14) | 0,5 mm² | `08` | Plugável → botão da posição 08 |
| A1 (D15) | 0,5 mm² | `09` | Plugável → botão da posição 09 |
| A2 (D16) | 0,5 mm² | `10` | Plugável → botão da posição 10 |
| A3 (D17) | 0,5 mm² | `11` | Plugável → botão da posição 11 |
| GND (4º borne) | 0,5 mm² preto | `GND-BT` | Plugável → comum dos botões |

Correspondência com as posições globais: Sala 2 → 01 a 11 = P15 a P25; Sala 3 → P26 a P36; Sala 4 → P37 a P47. Se quiser, use na anilha o número global (`P15`...), mas mantenha o mesmo critério nas três salas.

**Poucos bornes de 5V/GND no shield?** Muitos screw shields têm só 1 borne de 5 V e 2 ou 3 de GND. Não coloque dois fios soltos sob o mesmo parafuso. Opções corretas:

- ilhós **duplo** (próprio para 2 fios de 0,5 mm²) num único borne;
- levar o fio extra a partir do Wago de distribuição (ex.: VCC do MAX485 saindo do Wago +5 V), se houver entrada livre.

Os bornes D2, D3 e D13 ficam livres. Não ligue nada em AREF, IOREF, VIN e RESET.

### 6.4 Diagrama da sala remota

```
                        CAIXA DA SALA REMOTA (2, 3 ou 4)

   cabo que chega  ===[PG7]==+                        +==[PG7]=== cabo que sai
   (A, B, malha)             |                        |           (não existe na Sala 4)
                         +---+------------------------+---+
                         |  WAGO A   WAGO B   WAGO SH      |
                         +----+--------+--------+---------+
                              |        |        |
                   derivação  |        |       [100 Ω] (emenda soldada,
                   ≤ 30 cm    |        |        |       termo-retrátil duplo)
                   (A e B     |        |        |
                   torcidos)  v        v        +------------------------+
                        +------------------+                             |
                        | MAX485  A  B     |  (R7 de 120 Ω REMOVIDO     |
                        |  RO DI DE /RE VCC GND  nas Salas 2 e 3;      |
                        +--+--+--+--+---+---+    mantido na Sala 4)    |
                           |  |  +--+   |   |                          |
                           |  |    |    |   |                          |
      +--------------------+--+----+----+---+--------------------------+-----+
      | SCREW SHIELD   D0 D1   D4    5V GND                      GND (SH)    |
      | sobre o UNO                                                         |
      |   D5 (DIN)  D6..D12, A0..A3 (posições 01..11)   GND-BT   5V   GND   |
      +-----+------------------+------------------------+--------+-----+----+
            |                  |                        |        |     |
            |                  |                        |        |     |
      +-----+------------------+------------------------+--+     |     |
      |  BORNE PLUGÁVEL (lado da placa)  -> porta          |     |     |
      |  DIN | 01..11 | GND-BT | LED+5V | LED GND          |     |     |
      +---------------------------------------^------^-----+     |     |
                                              |      |           |     |
                         +----------+         |      |      +----+-----+--+
   tomada ---[fonte 5V 2A]-+5V------+---------|------+------+ WAGO +5V    |
                          -GND------+---------+-------------+ WAGO GND    |
                                                            +-------------+
```

---

## 7. Sala 1: Arduino Mega com proto shield

No Mega não há screw shield comercial com bornes para todos os pinos usados (D18–D21, D22–D35 na barra dupla). A solução é o **Mega Proto Shield**: uma placa perfurada no formato do Mega, onde se soldam barras de pinos, bornes KRE e a parte fixa dos bornes plugáveis. Tudo o que é solda fica no shield; o Mega continua sem nenhuma solda e pode ser trocado.

### 7.1 Soldar as barras de pinos

1. Separe as barras macho (ou as barras "empilháveis" de pino longo, se o shield vier com elas) para todos os conectores do Mega, **incluindo a barra dupla do fim (D22–D53)**.
2. Use o **próprio Mega como gabarito**: encaixe as barras no Mega, apoie o shield por cima e solde **um pino de cada barra** só. Confira o alinhamento e o esquadro. Então solde o resto.
3. Retire o shield do Mega, limpe o fluxo e inspecione com lupa. Confira com o multímetro que não há ponte entre pinos vizinhos.

### 7.2 Plano de ocupação do shield

Desenhe numa folha (ou fotografe e anote) a posição dos bornes antes de soldar. Sugestão de blocos:

| Bloco | Tipo | Vias | Função |
|---|---|---|---|
| J1 | KRE 2 vias | +5V, GND | Entrada de alimentação (do Wago de distribuição) |
| J2 | KRE 3 vias | A, B, SH | Barramento RS-485 (para o Wago do cabo) |
| J3 | Plugável (parte de placa) | P01–P14, NAV, HAB, GND, GND (18 vias) | Botões da porta |
| J4 | Plugável (parte de placa) | LCD +5V, LCD GND, SDA, SCL, BUZ+, BUZ−, DIN, GND (8 vias) | LCD, buzzer e dados dos LEDs |
| — | Módulo MAX485 | — | No shield ou ao lado, ver 7.4 |

Um plugável de 18 vias pode ser formado por blocos menores lado a lado (ex.: 10 + 8). Use blocos de **número de vias diferente** para J3 e J4 ou marque-os com etiqueta: assim não há como trocar um plugue pelo outro.

A alimentação dos 47 LEDs **não passa pelo shield**: vai do Wago direto à porta por um plugável fio-fio de 2 vias (`LED+5V`, `LED GND`) — ver seção 12.

O passo dos bornes KRE e KF2EDG é 5,08 mm = exatamente 2 furos da placa perfurada (2,54 mm). Confira antes se o pino do borne entra no furo; se estiver justo, não force (o anel metalizado pode soltar) — prefira outro modelo de borne.

### 7.3 Rota das ligações no verso

```
   VISTA DO VERSO DO PROTO SHIELD (exemplo de organização)

   barra de pinos D22..D35 (barra dupla)
   o o o o o o o o o o o o o o
   | | | | | | | | | | | | | |       fios isolados finos, em feixe,
   | | | | | | | | | | | | | |       paralelos à grade, sem cruzar pads
   +-+-+-+-+-+-+-+-+-+-+-+-+-+---->  J3 (plugável dos botões)

   ====================================  trilha de GND (fio nu estanhado
   ====================================  trilha de +5V  ou barra de solda)
```

Regras:

- **+5 V e GND:** uma "trilha" contínua de fio de cobre nu estanhado (pode ser um condutor rígido de 0,5 mm² desencapado) soldada ponto a ponto ao longo dos furos, ligada ao pino 5V e a **dois** pinos GND do Mega.
- **Sinais:** fio isolado fino (0,25–0,5 mm², ou fio de wire-wrap), cada um saindo do pad do pino e indo ao pad do borne pelo caminho mais curto, em feixe e rente à placa.
- Fio rígido é aceitável **aqui** porque fica totalmente apoiado e soldado na placa, sem vibrar.
- Nenhum fio passa sobre pad de outro pino; nenhuma ponta de cobre fica sobrando (corte rente depois de soldar).
- Anote cada ligação na sua folha de plano conforme for soldando.

### 7.4 Circuito RS-485 da Sala 1

Na Sala 1 o barramento recebe, além do módulo MAX485:

- **Terminação 120 Ω**: o próprio R7 do módulo (mantido).
- **Polarização fail-safe**: 560 Ω de A para +5 V e 560 Ω de B para GND, soldados no shield junto ao J2.
- **Malha (SH) ligada direto ao GND** no J2.

```
                 +5V
                  |
                [560 Ω]
                  |
  MAX485 A -------+-------------------- J2-A ---> Wago A ---> cabo via 1
                  |
               [R7 120 Ω] (no módulo, mantido na Sala 1)
                  |
  MAX485 B -------+-------------------- J2-B ---> Wago B ---> cabo via 2
                  |
                [560 Ω]
                  |
  GND ------------+-------------------- J2-SH --> Wago SH --> malha
                                       (direto, sem resistor)

  MAX485 RO  ---- D19 (RX1)
  MAX485 DI  ---- D18 (TX1)
  MAX485 DE + /RE (jumpeados) ---- D2
  MAX485 VCC ---- +5V      MAX485 GND ---- GND
```

O módulo MAX485 pode:

- ficar **sobre o proto shield**, com os 8 pinos soldados na área perfurada, se o espaçamento entre as duas barras do módulo coincidir com a grade de 2,54 mm; ou
- ficar **ao lado**, fixado na placa de montagem, com fios soldados nos seus pinos e no shield (os dois lados são placa — solda permitida), cada pino coberto com termo-retrátil.

Em ambos os casos os fios A e B vão do módulo ao J2 pelo shield; o pequeno borne A/B do módulo fica sem uso na Sala 1.

### 7.5 Tabela de ligação do Mega

| Pino do Mega | Ponto no shield | Fio / anilha | Destino |
|---|---|---|---|
| 5V | J1-+5V | `+5V` (0,5 mm² vermelho) | Wago +5 V (fonte 5 V 3 A) |
| GND | J1-GND | `GND` (0,5 mm² preto) | Wago GND |
| D18 TX1 | trilha | — | MAX485 DI |
| D19 RX1 | trilha | — | MAX485 RO |
| D2 | trilha | — | MAX485 DE + /RE |
| D20 SDA | J4-SDA | `SDA` | LCD (adaptador I²C) SDA |
| D21 SCL | J4-SCL | `SCL` | LCD SCL |
| 5V / GND | J4-LCD+5V / J4-LCD GND | `LCD+5V`, `LCD GND` | LCD VCC / GND |
| D4 | J3-NAV | `NAV` | Botão NAV (16 mm) |
| D5 | J3-HAB | `HAB` | Botão HAB (16 mm) |
| D6 | 330 Ω → J4-DIN | `DIN` | DIN do pixel 1 (P01) do painel de 47 |
| D7 | J4-BUZ+ | `BUZ+` | Buzzer + (o − vai ao J4-BUZ− = GND) |
| D22 … D35 | J3-P01 … J3-P14 | `P01` … `P14` | Botões P01 … P14 |
| GND | J3-GND (2 vias) | `GND-BT` | Comum dos botões |
| — | J2-A, J2-B, J2-SH | `A`, `B`, `SH` | Wago do cabo entre salas |

O resistor de 330 Ω do DIN pode ficar no shield (entre D6 e J4-DIN) porque o fio até o primeiro pixel é curto (até ~1 m). Nas salas remotas ele fica no pixel (seção 11).

### 7.6 Teste de continuidade antes de encaixar no Mega

Com o shield **fora** do Mega e sem nada ligado nos bornes:

1. **Curto entre alimentação:** +5 V × GND → **sem continuidade** (aberto). Se bipar, procure a ponte antes de qualquer outra coisa.
2. **Cada ligação:** ponta do multímetro no pino da barra (lado de baixo) e outra no parafuso do borne correspondente → bipe. Siga a tabela 7.5 linha a linha e marque.
3. **Vizinhos:** cada borne contra o borne ao lado → sem bipe.
4. **RS-485:** J2-A × J2-B → ~120 Ω (R7 do módulo; com os 560 Ω e o MAX485 sem alimentação a leitura pode ficar um pouco abaixo, 100–120 Ω). J2-SH × GND → 0 Ω.
5. Só depois encaixe no Mega, ligue **só pelo USB** e meça 5 V em J1. Então grave o firmware e prossiga.

---

## 8. Módulo MAX485

O módulo comum (placa azul) tem 4 pinos de um lado (`RO`, `RE`, `DE`, `DI`), 4 do outro (`VCC`, `B`, `A`, `GND`) e um borne de 2 vias para A e B.

### 8.1 Como ligar os pinos

Os pinos do módulo são barras macho para jumper Dupont — **que não pode ser usado**. Duas formas corretas:

- **Soldar o fio no pino:** desencape 3 mm, estanhe, enrole meia volta na base do pino e solde. Coloque um pedaço de termo-retrátil cobrindo pino e solda. Faça isso em todos os pinos usados.
- **Retirar a barra de pinos** (dessoldar) e soldar os fios direto nos furos — mais trabalhoso, resultado mais baixo e firme.

Para **A e B**: nas Salas 2, 3 e 4 use o borne de parafuso do próprio módulo com **ilhós** nos fios de derivação. Na Sala 1, A e B saem soldados para o shield (seção 7.4).

### 8.2 DE e /RE jumpeados

Una os pinos `DE` e `RE` com um pedacinho de fio soldado (ou uma ponte de solda entre os dois pinos, se estiverem lado a lado) e leve **um** fio até o pino de controle (D2 no Mega, D4 no Uno).

Opcional recomendado: um resistor de 10 kΩ entre DE/RE e GND mantém o módulo em recepção enquanto o Arduino está em reset ou sendo gravado (não está no kit; não é obrigatório).

### 8.3 Terminação R7: manter ou remover

| Sala | R7 (120 Ω) | Observação |
|---|---|---|
| 1 | **Manter** | Ponta da linha |
| 2 | **Remover** | Meio da linha |
| 3 | **Remover** | Meio da linha |
| 4 | **Manter** | Ponta da linha |

Para identificar o R7: com o módulo desligado, meça entre A e B. ~120 Ω = terminador presente. Na placa ele costuma estar marcado `121` (12 × 10¹ Ω). Para remover: aqueça os dois lados com o ferro e retire com a pinça, ou corte-o ao meio com alicate de corte rente. Confira depois: A–B deve ficar na casa de dezenas de kΩ (resistores de polarização do próprio módulo) ou aberto. **Marque o módulo** com caneta ("SEM R7") para não trocar de sala por engano.

### 8.4 Derivação curta

Nas Salas 2 e 3 o cabo chega e sai pelos Wago; o MAX485 é ligado por uma **derivação de no máximo 30 cm**. Derivação longa cria um "toco" que reflete sinal. Torça A e B da derivação entre si (uma volta a cada 2–3 cm).

### 8.5 Fixação do módulo

Se o módulo tiver furos, use espaçador M3. Se não tiver, fixe-o sobre um pedaço de placa perfurada presa com espaçadores, ou com fita dupla-face espumada de boa qualidade **mais** uma abraçadeira. Ele não pode ficar pendurado pelos fios.

---

## 9. Cabo de 2 vias com malha e conectores Wago

### 9.1 Entrada na caixa

1. Passe o cabo pelo **prensa-cabo PG7** antes de preparar a ponta.
2. Deixe dentro da caixa comprimento suficiente para chegar ao Wago **mais um laço de folga de 10 cm**.
3. Aperte o PG7 sobre a capa externa do cabo. Ele é o alívio de tração: puxar o cabo do lado de fora não pode mover nada lá dentro.
4. Prenda o cabo com abraçadeira em base adesiva a 5–10 cm do PG7.

### 9.2 Pontas de 24 AWG: ilhós certo

As vias A e B têm 24 AWG (cerca de 0,2 mm²). O ilhós de 0,5 mm² fica frouxo nelas. Use uma das opções:

- **ilhós de 0,25 mm²** (recomendado; o crimpador autoajustável aceita);
- se não tiver: desencape o dobro do comprimento, **dobre a ponta de cobre ao meio** (fica com ~0,4 mm²), torça levemente e use o ilhós de 0,5 mm².

### 9.3 Preparar a malha

```
   capa externa     malha torcida (rabicho)          par trançado
  ===============##########~~~~~~~~~~~~~~~~ SH (termo-retrátil + ilhós)
                 \
                  \=================== via 1 (A) + ilhós
                   \================== via 2 (B) + ilhós
                 ^
                 termo-retrátil cobrindo o ponto onde a capa foi aberta
```

1. Retire 60 a 80 mm da capa externa (ou o necessário para chegar ao Wago), sem cortar a malha.
2. **Malha trançada:** empurre-a para trás (ela "abre"), faça uma janela com uma ponta (agulha ou chave fina) e puxe o par trançado por essa janela. Torça a malha formando um rabicho. **Malha em espiral:** junte os fios e torça. **Fita metálica com fio dreno:** retire a fita e use o dreno como SH.
3. Corte fios soltos da malha: nenhum fiozinho pode ficar solto (é a causa clássica de curto com A ou B).
4. **Encape o rabicho** com termo-retrátil, deixando só a ponta para o ilhós. Coloque também um termo-retrátil maior no ponto onde a capa foi aberta, segurando malha e par juntos.
5. Mantenha A e B torcidos até o mais perto possível do Wago.
6. Coloque anilhas `A`, `B`, `SH` e crimpe os ilhós.

### 9.4 Ligação nos Wago 221-413

| Sala | Wago A | Wago B | Wago SH |
|---|---|---|---|
| 1 | cabo A + derivação ao J2-A | cabo B + derivação ao J2-B | cabo SH + derivação ao J2-SH (**direto ao GND**) |
| 2 e 3 | A que chega + A que sai + derivação ao MAX485 A | idem para B | SH que chega + SH que sai + derivação **via 100 Ω** ao GND |
| 4 | cabo A + derivação ao MAX485 A | cabo B + derivação ao MAX485 B | cabo SH + derivação **via 100 Ω** ao GND |

Como usar o Wago 221: levante a alavanca, insira o ilhós até o fim (dá para ver pela janela transparente), abaixe a alavanca, puxe o fio. Prenda o conjunto de Wagos na placa de montagem (abraçadeira em base adesiva com parafuso, ou suporte próprio para Wago 221); eles não podem ficar soltos dentro da caixa.

Na Sala 1 e na Sala 4 sobra uma entrada em cada Wago: ela serve de ponto de medição (encoste a ponta do multímetro na janela de teste ou insira um fio de teste).

### 9.5 Resistor de 100 Ω da malha (Salas 2, 3 e 4)

A malha é a referência comum do barramento. Na Sala 1 ela vai direto ao GND. Nas remotas ela vai ao GND **através de 100 Ω 1/4 W**, que limita a corrente caso haja diferença de potencial entre os terras das salas (laço de terra), sem perder a função de referência.

Montagem:

```
  Wago SH ---[ilhós]--- fio 0,5 mm² (5 cm) ---(solda)[100 Ω](solda)--- fio 0,5 mm² ---[ilhós]--- borne GND do shield
                                               \____________________/
                                       termo-retrátil fino + termo-retrátil maior
                                       por cima de tudo; anilha "SH-100R"
```

- Solde o resistor em linha entre dois pedaços de fio, como emenda: enrole cada terminal do resistor no fio, solde, corte o excesso.
- Duas camadas de termo-retrátil.
- Prenda a emenda com abraçadeira na placa de montagem para que ela não flexione.

### 9.6 Alternativa: UTP Cat5e

Aceito como alternativa (Cenário B da [Lista de materiais](LISTA_DE_MATERIAIS.md)): **par azul** = A (branco-azul) e B (azul), **fio verde** = referência GND (no lugar da malha, com a mesma regra: direto na Sala 1, via 100 Ω nas outras). Os demais fios ficam sem uso, cortados e isolados. O condutor do Cat5e é rígido: entra **sem ilhós** no Wago e o cabo deve ser bem preso logo após o PG7.

---

## 10. Botões

### 10.1 Botões antigos de 22 mm (posições)

Os botões de 22 mm reaproveitados têm blocos de contato com parafuso.

1. **Retire toda a fiação antiga de 110 V** e lâmpadas ou blocos de lâmpada. Nenhum fio antigo fica conectado.
2. Identifique o contato **N.A.** (normalmente aberto; marcação 13–14, 3–4 ou "NO"). Confira com o multímetro: solto = aberto; apertado = 0 Ω.
3. Crimpe **terminal garfo pré-isolado** no fio (desencape no comprimento do cano do terminal, normalmente 5 a 6 mm; insira até a isolação encostar; crimpe no cano metálico com a cavidade da cor do terminal).
4. Monte: parafuso → **arruela de pressão** → (arruela lisa, se houver) → garfo, com a abertura do garfo voltada no sentido de aperto do parafuso (assim ele "puxa" o garfo para dentro ao apertar).
5. Se o contato tiver **plaqueta de pressão** (o fio entra sob uma plaquinha), use **ilhós** em vez de garfo.

### 10.2 Retorno GND comum

Um lado de cada botão vai ao seu pino; o outro lado vai ao GND comum. Duas formas corretas:

**a) Ponte de botão a botão, em anel (recomendada para a porta):**

```
  plugável GND-1 ---[B01]---[B02]---[B03]--- ... ---[B11]--- plugável GND-2
                     |       |       |                |
                   sinal   sinal   sinal            sinal
                   "01"    "02"    "03"             "11"
```

- Cada parafuso recebe no máximo **dois** garfos (o que chega e o que sai), montados costas com costas sob a mesma arruela.
- O anel começa num polo GND do plugável e termina em outro polo GND. Se uma ponte se soltar, todos os botões continuam com retorno.

**b) Barramento:** cada botão tem seu fio de retorno até um ponto comum (Wago 221-415, barra de bornes ou régua de KRE em ponte), e o barramento vai ao GND do plugável.

### 10.3 Botões NAV e HAB (16 mm, Sala 1)

Conforme o terminal do botão comprado:

- **terminal de solda:** solde o fio e cubra com termo-retrátil;
- **parafuso:** garfo ou ilhós, como nos de 22 mm;
- **faston:** terminal faston fêmea isolado, crimpado.

Ligue-os ao J3 (`NAV`, `HAB`) e ao GND comum da mesma forma que os demais.

---

## 11. Pixels WS2812B

Cada posição tem um pixel WS2812B cortado da fita, ligado ao seguinte por fio 26 AWG.

### 11.1 Sentido dos dados

Cada pixel tem uma seta impressa: os dados entram em **DIN** e saem em **DOUT** (às vezes "DI"/"DO"). O DOUT de um pixel vai ao DIN do próximo. Ligar ao contrário é o erro mais comum: nada acende daquele ponto em diante.

```
  Arduino            pixel 1              pixel 2              pixel 3
  D5/D6 --[330 Ω]--> DIN  ->  DOUT -----> DIN  ->  DOUT -----> DIN  -> ...
  +5V -------------> 5V        5V ------> 5V        5V ------> 5V
  GND -------------> GND      GND ------> GND      GND ------> GND
                    (seta ->)            (seta ->)            (seta ->)
```

Ordem dos pixels:

- **Sala 1 (47 pixels):** pixel 1 = P01, ..., pixel 14 = P14, pixel 15 = P15, ..., pixel 47 = P47 (S1, depois S2, S3 e S4).
- **Salas 2, 3 e 4 (11 pixels):** pixel 1 = posição 01, ..., pixel 11 = posição 11.

### 11.2 Corte e solda

1. Corte a fita **sobre a linha de corte** (no meio dos pads de cobre), deixando meio pad de cada lado.
2. Limpe os pads com álcool isopropílico.
3. Pré-estanhe os pads (rápido: 2 s) e as pontas dos fios 26 AWG (2 mm desencapados).
4. Solde cada fio no seu pad, sem encostar no pad vizinho. Confira com lupa: sem pontes entre 5V, DIN e GND.
5. Coloque **termo-retrátil transparente** (10–12 mm) envolvendo o pixel e o início dos fios; a luz passa pelo tubo transparente. Se usar tubo colorido, deixe o LED descoberto.
6. **Alívio de tração:** um ponto de cola quente ou **silicone neutro** sobre os fios logo atrás do pixel, colando fio e pixel no suporte. Assim, quem trabalha é a cola, não a solda. Silicone **acético** (cheiro de vinagre) é proibido: corrói o cobre.
7. Deixe folga entre pixels (os fios não podem ficar esticados quando a porta abre e fecha).

### 11.3 Resistor de 330 Ω e capacitores

- **330 Ω em série no DIN do pixel 1.** Nas remotas, solde o resistor no pad DIN do pixel 1 e o fio de dados na outra ponta do resistor, tudo coberto com termo-retrátil. Na Sala 1 ele fica no proto shield (seção 7.5).
- **Capacitor eletrolítico na entrada de alimentação dos LEDs:** 1000 µF/16 V na Sala 1, 470 µF/16 V nas remotas, com um **100 nF** em paralelo. Solde-os nos pads 5V/GND do pixel 1 (ou numa plaquinha perfurada colada ao lado), **respeitando a polaridade** (faixa do eletrolítico = negativo = GND), e fixe o corpo com silicone neutro.

### 11.4 Injeção de 5 V

O fio 26 AWG é fino. Na Sala 1, com 47 pixels, alimente os LEDs **no início (pixel 1) e no fim (pixel 47)** com cabinho 0,5 mm² vindo do Wago de distribuição; se as fileiras forem longas, injete também no começo de cada fileira. Nas remotas (11 pixels) basta alimentar no pixel 1.

Na injeção liga-se **só +5 V e GND**. O fio de dados segue apenas a corrente DOUT → DIN.

---

## 12. Alimentação

### 12.1 Regras

- **Cada sala tem sua fonte.** O cabo entre salas não leva energia.
- **Nunca interligue o +5 V de salas diferentes.**
- A fonte entra no **borne 5V/GND do shield** (pino 5V do Arduino). Não use o jack P4 nem o VIN.
- Os **LEDs são alimentados direto da fonte**, pelo Wago de distribuição — não pelas trilhas do Arduino.
- O GND é comum: fonte, Arduino, MAX485 e LEDs da mesma sala no mesmo GND.

### 12.2 Distribuição com Wago

```
                           WAGO +5V (221-413)              WAGO GND (221-413)
  fonte +5V  ------------> [1] entrada        fonte GND -> [1] entrada
                           [2] -> borne 5V do shield       [2] -> borne GND do shield
                           [3] -> LEDs (+5V, plugável)     [3] -> LEDs (GND, plugável)
```

Na Sala 1, se precisar de mais saídas (injeção no início e no fim dos 47 LEDs), use um Wago 221-415 (5 entradas) ou dois 221-413 unidos por um pedaço de fio com ilhós.

### 12.3 Fonte tipo carregador ou colmeia

- **Carregador (plug na tomada):** corte o conector, identifique + e − com o multímetro, isole fios que não forem usados (em cabo USB, os de dados). Atenção: cabos de carregador baratos têm fios muito finos; meça a tensão no borne do shield com os LEDs acesos (deve ficar ≥ 4,85 V). Se ficar abaixo, encurte o cabo ou troque por fonte com cabo mais grosso.
- **Colmeia (bornes):** a ligação na rede (fase, neutro, terra de proteção) deve ser feita por profissional habilitado, com cabo próprio entrando por prensa-cabo, ilhós nos fios e **proteção sobre os bornes de 127/220 V**. Ajuste o trimpot para **5,10 V** em vazio.
- Deixe a parte de rede (AC) **separada** da parte de 5 V e sinais dentro da caixa, a pelo menos 5 cm; se tiverem de se cruzar, cruzem a 90°.

### 12.4 Gravação pelo USB com a fonte ligada

O conector USB também alimenta o 5 V da placa. Com a fonte externa ligada no pino 5V **e** o USB conectado, as duas fontes ficam em paralelo (a fonte pode empurrar corrente para a porta USB do computador).

- **Procedimento padrão:** desligue a fonte da sala da tomada, conecte o USB, grave, desconecte o USB, religue a fonte. Os LEDs ficam apagados durante a gravação — é normal.
- No **Uno**, solte também os fios `RO` (D0) e `DI` (D1) antes de gravar e recoloque depois (o MAX485 ocupa a mesma serial do USB).
- Se for indispensável manter o painel ligado com o USB conectado (por exemplo, para acompanhar o Monitor Serial do Mega), use um cabo USB **com a via +5 V interrompida** (cabo "só dados") ou um isolador USB.

---

## 13. Chicote da porta com borne plugável

Botões, LEDs e LCD ficam na porta (ou tampa) do painel; a placa fica no fundo. O chicote entre os dois termina em **borne plugável 5,08 mm (KF2EDG) com parafusos de trava**: para tirar a porta, solta-se dois parafusos e puxa-se o plugue, sem desparafusar fio a fio.

| Sala | Plugável | Vias |
|---|---|---|
| 1 | J3 (no shield) | P01–P14, NAV, HAB, GND, GND |
| 1 | J4 (no shield) | LCD +5V, LCD GND, SDA, SCL, BUZ+, BUZ−, DIN, GND |
| 1 | J5 (fio-fio, do Wago) | LED +5V, LED GND |
| 2, 3, 4 | J1 (fio-fio) | 01–11, GND-BT, GND-BT, DIN, LED +5V, LED GND |

- Na Sala 1, a parte fixa é **soldada no proto shield**. Nas remotas, usa-se a versão **fio-fio** (as duas metades com parafuso), presa na placa de montagem com abraçadeira em base adesiva.
- Todos os fios entram no plugável com **ilhós** e anilha.
- Aperte os **parafusos de trava** do plugue (flange); sem eles o plugue pode sair com a vibração da porta.
- **LCD:** o adaptador I²C vem com pinos para jumper Dupont — solde os fios direto nos pinos (com termo-retrátil) ou retire a barra e solde nos furos. Mantenha o cabo do LCD com até ~1 m.
- **Na dobradiça:** o chicote passa em laço, paralelo ao eixo da dobradiça, de forma que a porta **torça** o feixe em vez de dobrá-lo. Use fio flexível (nunca rígido) e, se possível, espiral organizadora. Abraçadeira com base adesiva dos dois lados da dobradiça.

```
   PORTA (botões, LEDs, LCD)                 FUNDO (placa)
   ------------------------+     dobradiça   +------------------------
          feixe preso      |       ||        |     feixe preso
   ==abraçadeira=====\     |       ||        |   /=====abraçadeira==
                      \____|_______||________|__/
                        laço de folga ao longo do eixo
```

---

## 14. Organização e fixação

- **Placa de montagem:** MDF ou PVC de 3 a 6 mm, fixada no fundo da caixa. Todas as placas sobre **espaçadores de nylon M3** — nunca encostadas na madeira (umidade, fuga, aquecimento).
- **Abraçadeira com base adesiva a cada 10–15 cm** em todos os feixes. Bases com furo para parafuso são mais firmes; só adesivo descola com o calor.
- **Laço de folga (service loop) de 10 cm** antes de cada placa: permite refazer um ilhós sem precisar de fio novo.
- **Feixes por função:** alimentação, RS-485, botões, LEDs. RS-485 longe da rede AC.
- **Anilhas** em todos os fios, legíveis com a caixa aberta.
- **Etiqueta** em cada placa: sala, ID (`SLAVE_ID`), data da gravação do firmware, "COM R7" ou "SEM R7".
- **Uma cópia impressa** das tabelas de ligação (seções 6.3 e 7.5) dentro da tampa da caixa, em saco plástico.

---

## 15. Proteção contra oxidação

| Medida | Como fazer |
|---|---|
| Fio estanhado | Cabinho e 26 AWG de cobre estanhado: o cobre nu escurece (oxida) e piora o contato e a solda. |
| Ilhós estanhado | Contato metal-metal estável sob o parafuso. |
| Conectores com contato estanhado ou dourado | Plugáveis, bornes e Wago de boa procedência. |
| Limpeza do fluxo | Álcool isopropílico logo após soldar. Fluxo velho atrai umidade. |
| Verniz acrílico (conformal coating) | **Depois de testar tudo.** Mascare com fita crepe: bornes, plugáveis, Wago, barras de pinos entre Uno e shield, conector USB, botão de reset, trimpot do LCD. Aplique 2 demãos finas a 20–30 cm, em local ventilado, com intervalo indicado pelo fabricante. Retire a fita antes de secar totalmente. |
| Caixa fechada | Tampa no lugar, prensa-cabos apertados, furos sem uso tampados. |
| Sachê de sílica | Em locais úmidos, um sachê dentro da caixa; troque ou regenere quando mudar de cor. |
| Silicone neutro | Nunca acético (cheiro de vinagre). |

---

## 16. Checklist final de montagem

Faça com a caixa aberta, **fonte desligada** nos itens 1 a 14.

| Nº | Verificação | OK |
|---|---|---|
| 1 | Nenhum jumper Dupont, protoboard ou emenda com fita isolante | [ ] |
| 2 | Toda ponta em borne/Wago/plugável tem ilhós do tamanho certo, sem fio para fora | [ ] |
| 3 | Nenhuma ponta estanhada sob parafuso | [ ] |
| 4 | Toda solda inspecionada com lupa: brilhante, em cone, sem ponte | [ ] |
| 5 | Fluxo limpo com álcool isopropílico | [ ] |
| 6 | Termo-retrátil em toda emenda e pino soldado exposto | [ ] |
| 7 | Anilha em todo fio, conferida com a tabela | [ ] |
| 8 | Teste de puxão (~2 kgf) em cada fio: nenhum saiu | [ ] |
| 9 | Placas em espaçadores, sem contato com a madeira; shield travado | [ ] |
| 10 | Cabo entre salas preso no PG7, com laço de folga; malha encapada, sem fios soltos | [ ] |
| 11 | R7: mantido nas Salas 1 e 4, removido nas Salas 2 e 3 (módulo marcado) | [ ] |
| 12 | Resistor 100 Ω da malha nas Salas 2, 3 e 4; malha direta ao GND na Sala 1; 560 Ω de polarização na Sala 1 | [ ] |
| 13 | +5 V × GND sem curto (multímetro) em cada sala | [ ] |
| 14 | Nenhum fio de +5 V saindo da caixa para outra sala | [ ] |
| 15 | Fonte ligada: 5,05–5,20 V em vazio; ≥ 4,85 V no borne do shield com LEDs acesos | [ ] |
| 16 | Pixels na ordem correta, todos acendendo | [ ] |
| 17 | Plugáveis encaixados e com parafusos de trava apertados | [ ] |
| 18 | Chicote da porta com laço na dobradiça; porta abre e fecha sem esticar fios | [ ] |
| 19 | Parte AC separada e protegida (se houver fonte colmeia) | [ ] |
| 20 | Verniz aplicado após os testes, com mascaramento | [ ] |
| 21 | Etiqueta na placa (sala, ID, R7, data) e tabela de ligação na tampa | [ ] |
| 22 | Reaperto de bornes de parafuso agendado para 30 dias após a instalação | [ ] |

Depois desta lista, execute o comissionamento CK-01 a CK-12 do [Manual técnico](MANUAL_TECNICO.md#11-comissionamento).

---

## 17. O que NÃO fazer

| Não faça | Por quê | Faça assim |
|---|---|---|
| Jumper Dupont ou protoboard na instalação | Contato por pressão fraca; solta com vibração e oxida | Screw shield (Uno), proto shield soldado (Mega), solda nos módulos |
| Emenda torcida com fita isolante | A fita descola com calor; a emenda oxida e aumenta a resistência | Wago com ilhós ou emenda soldada com termo-retrátil |
| Estanhar ponta de fio sob parafuso | A solda escoa, o parafuso afrouxa, mau contato intermitente | Ilhós crimpado |
| Fio nu torcido no borne | Fios cortados e espalhados pelo parafuso | Ilhós crimpado |
| Crimpar ilhós com alicate universal | Crimpagem fraca e irregular, solta no puxão | Alicate crimpador próprio |
| Ilhós maior que o fio | Fica frouxo mesmo crimpado | Ilhós da seção do fio (0,25 mm² para 24 AWG) |
| Dois fios soltos sob o mesmo parafuso | Um deles fica sem pressão | Ilhós duplo ou Wago |
| Fio rígido em ponto que vibra ou dobra (porta, dobradiça) | O cobre rígido quebra por fadiga | Cabinho flexível |
| Cola quente sobre conector, borne ou plugável | Impede manutenção e pode entrar no contato | Cola só sobre fios e pixels, longe de contatos |
| Silicone acético (cheiro de vinagre) | Libera ácido que corrói o cobre | Silicone neutro |
| Ligar o +5 V de uma sala com o de outra | Fontes em paralelo, correntes de laço, risco de queima | Cada sala com sua fonte; cabo só com A, B e malha |
| Deixar o R7 nas Salas 2 e 3 | 3 ou 4 terminadores carregam demais a linha (A–B ≈ 40 Ω ou 30 Ω) | Remover R7 nas Salas 2 e 3 |
| Derivação longa até o MAX485 | Toco de linha, reflexões | Derivação ≤ 30 cm |
| Malha desencapada solta na caixa | Fiozinho da malha encosta em A, B ou 5 V | Malha torcida, encapada com termo-retrátil, ilhós |
| Alimentar os LEDs pelo pino 5V do Arduino | Corrente dos LEDs passa pelas trilhas da placa | LEDs direto do Wago de distribuição |
| Gravar o Uno com RO/DI ligados em D0/D1 | Conflito com a serial do USB; gravação falha | Soltar RO e DI, gravar, recolocar |
| Placa encostada na madeira | Umidade, fuga, aquecimento | Espaçadores de nylon M3 |
| Cabo do barramento junto com circuito de força no mesmo eletroduto | Ruído induzido e risco em caso de falha de isolação | Eletroduto ou canaleta exclusiva; cruzar a 90° |
| Verniz sobre borne, plugável ou barra de pinos | Isola o contato | Mascarar antes de aplicar |
| Fechar a caixa sem teste de puxão e sem lupa | Defeito aparece semanas depois, em campo | Checklist da seção 16 completo |

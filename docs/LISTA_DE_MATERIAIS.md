# Lista de materiais — Painel de Sinalização de 4 Salas

Revisão 5.0 — 23/11/2026

> **Preços de referência.** Os valores abaixo são preços médios de referência do mercado brasileiro (lojas de eletrônica e marketplaces), levantados em **novembro de 2026**. Eles servem para estimar o orçamento, **não são cotação**. Antes de comprar, cote com pelo menos dois fornecedores e confira a especificação de cada item com as dicas da seção [O que observar ao comprar](#o-que-observar-ao-comprar).

Documentos relacionados:

- [Manual técnico](MANUAL_TECNICO.md)
- [Montagem e conexões](MONTAGEM_E_CONEXOES.md) — como usar cada item desta lista na montagem
- [Protocolo RS-485](PROTOCOLO_RS485.md)

---

## Resumo dos cenários

| Cenário | Descrição | Subtotal (R$) | Reserva 15% (R$) | Total (R$) |
|---|---|---:|---:|---:|
| **A — Recomendado** | Uno nas 3 salas remotas, cabo 2 vias blindado, conexões confiáveis | 979,00 | 146,85 | **1.125,85** |
| **B — Econômico** | Mesma eletrônica, menos acessórios | 797,00 | 119,55 | **916,55** |
| **C — Industrial** | Referência para comparação (não recomendado para este caso) | 3.528,76 | 529,31 | **4.058,07** |

A reserva de 15% cobre variação de preço, frete e pequenas perdas (fio, termo-retrátil, um LED danificado na solda etc.).

---

## Cenário A — Recomendado

Arduino Uno nas 3 salas remotas, cabo de 2 vias blindado entre salas e todos os acessórios necessários para uma montagem sem jumpers e sem emendas improvisadas.

| # | Item | Especificação | Qtd | Unit. (R$) | Subtotal (R$) | Grupo |
|---|---|---|---|---:|---:|---|
| 1 | Arduino Mega 2560 R3 | Sala 1 (cliente já possui) | 1 | 0,00 | 0,00 | Controladores |
| 2 | Arduino Uno R3 | Sala 2 (cliente já possui) | 1 | 0,00 | 0,00 | Controladores |
| 3 | Arduino Uno R3 compatível | Salas 3 e 4 (ATmega328P, CH340) | 2 | 55,00 | 110,00 | Controladores |
| 4 | Display LCD 20x2 I²C | cliente já possui | 1 | 0,00 | 0,00 | Controladores |
| 5 | Módulo MAX485 TTL | um por sala | 4 | 8,00 | 32,00 | Comunicação |
| 6 | Fita LED WS2812B 5 V 60 LED/m IP20 | 80 LEDs (47 central + 33 locais) | 2 m | 38,00 | 76,00 | Sinalização |
| 7 | Buzzer ativo 5 V | alarme da central | 1 | 4,00 | 4,00 | Sinalização |
| 8 | Botão pulsador N.A. 16 mm | NAV e HAB | 2 | 8,00 | 16,00 | Sinalização |
| 9 | Kit resistores e capacitores | 120 Ω, 560 Ω, 100 Ω, 330 Ω, 1000 µF/16 V, 470 µF/16 V, 100 nF | 1 | 25,00 | 25,00 | Componentes |
| 10 | Fonte 5 V 3 A regulada | Sala 1 | 1 | 35,00 | 35,00 | Alimentação |
| 11 | Fonte 5 V 2 A regulada | Salas 2, 3 e 4 | 3 | 25,00 | 75,00 | Alimentação |
| 12 | Cabo blindado 2 vias par trançado 24 AWG | barramento RS-485 (45 m + folga) | 60 m | 2,50 | 150,00 | Cabeamento |
| 13 | Cabinho flexível estanhado 0,5 mm² | fiação interna (rolo 100 m) | 1 | 70,00 | 70,00 | Cabeamento |
| 14 | Fio flexível 26 AWG (3 cores) | ligação entre pixels | 1 | 20,00 | 20,00 | Cabeamento |
| 15 | Prensa-cabo PG7 | entradas de cabo | 10 | 2,00 | 20,00 | Cabeamento |
| 16 | Shield de bornes (screw shield) p/ Uno | Salas 2, 3 e 4 | 3 | 30,00 | 90,00 | Conexões |
| 17 | Mega Proto Shield | Sala 1 (bornes soldados) | 1 | 35,00 | 35,00 | Conexões |
| 18 | Bornes KRE 5,08 mm 2 e 3 vias | kit 40 peças | 1 | 20,00 | 20,00 | Conexões |
| 19 | Borne plugável 5,08 mm (KF2EDG) | chicote da porta, kit 10 pares | 1 | 30,00 | 30,00 | Conexões |
| 20 | Conector Wago 221-413 | A, B, SH e distribuição 5 V | 12 | 3,00 | 36,00 | Conexões |
| 21 | Terminal tubular (ilhós) | kit 400 peças 0,25–1,5 mm² (inclui 0,25 mm² para as vias do cabo) | 1 | 25,00 | 25,00 | Conexões |
| 22 | Terminal garfo pré-isolado | botões 22 mm, 100 peças | 1 | 15,00 | 15,00 | Conexões |
| 23 | Termo-retrátil | kit sortido | 1 | 20,00 | 20,00 | Conexões |
| 24 | Espaçadores nylon M3 + parafusos | kit | 1 | 15,00 | 15,00 | Conexões |
| 25 | Abraçadeiras, bases adesivas, anilhas | kit | 1 | 25,00 | 25,00 | Conexões |
| 26 | Verniz isolante (conformal coating) | spray 300 ml | 1 | 35,00 | 35,00 | Conexões |

- **Subtotal A: R$ 979,00**
- Reserva técnica 15%: R$ 146,85
- **Total A: R$ 1.125,85**

### Totais por grupo (Cenário A)

| Grupo | Itens | Subtotal (R$) |
|---|---|---:|
| Controladores | 1 a 4 | 110,00 |
| Comunicação | 5 | 32,00 |
| Sinalização | 6 a 8 | 96,00 |
| Componentes | 9 | 25,00 |
| Alimentação | 10 e 11 | 110,00 |
| Cabeamento | 12 a 15 | 260,00 |
| Conexões | 16 a 26 | 346,00 |
| **Total** | | **979,00** |

Conferência: 110 + 32 + 96 + 25 + 110 + 260 + 346 = 979,00. Reserva: 979,00 × 0,15 = 146,85.

### Ferramentas (não somadas ao orçamento)

| Ferramenta | Observação |
|---|---|
| Alicate crimpador de ilhós (~R$ 60) | Tipo autoajustável, perfil quadrado, faixa 0,25–6 mm² ou 0,25–10 mm² |
| Ferro de solda 40–60 W | De preferência com controle de temperatura e ponta chanfrada de 2 a 3 mm |
| Multímetro | Escalas de tensão DC/AC, resistência e continuidade com bipe |
| Testador de continuidade | Pode ser o próprio multímetro; um testador de cabos com bipe agiliza a conferência dos 45 m |

Também ajudam (não fazem parte da lista da especificação): alicate desencapador automático, alicate de corte rente, lupa ou lupa de bancada, suporte "terceira mão", malha dessoldadora, pistola de ar quente ou isqueiro de bancada para termo-retrátil, chaves de fenda 2,5 mm e 3,0 mm para os bornes, e álcool isopropílico.

---

## Cenário B — Econômico

Mesma eletrônica do Cenário A (Mega, Uno, MAX485, LEDs, fontes). A economia vem do cabo e dos acessórios de conexão.

| Mudança em relação ao Cenário A | Cálculo | Diferença (R$) |
|---|---|---:|
| Cabo 2 vias blindado (item 12) trocado por **UTP Cat5e**, usando 1 par + 1 fio | 60 m × R$ 1,60 = R$ 96,00 (antes R$ 150,00) | −54,00 |
| 3 screw shields (item 16) trocados por **proto shield simples com bornes KRE soldados** | 3 × R$ 15,00 = R$ 45,00 (antes R$ 90,00) | −45,00 |
| Sem bornes plugáveis (item 19) | | −30,00 |
| Sem verniz isolante (item 26) | | −35,00 |
| 6 conectores Wago em vez de 12 (item 20) | 6 × R$ 3,00 = R$ 18,00 (antes R$ 36,00) | −18,00 |
| **Total das reduções** | | **−182,00** |

- **Subtotal B: R$ 797,00** (979,00 − 182,00)
- Reserva técnica 15%: R$ 119,55
- **Total B: R$ 916,55**

Totais por grupo no Cenário B: Controladores 110,00 · Comunicação 32,00 · Sinalização 96,00 · Componentes 25,00 · Alimentação 110,00 · Cabeamento 206,00 · Conexões 218,00 = 797,00.

**O que se perde no Cenário B:**

- Sem bornes plugáveis, para retirar o painel da porta é preciso soltar fio a fio (anote tudo e use anilhas).
- Sem verniz, as placas ficam mais expostas a umidade e poeira; compense com caixa bem fechada e sachê de sílica.
- Com 6 Wago, use-os nas Salas 2 e 3 (onde o cabo chega e sai). Na Sala 1 e na Sala 4, o cabo entra direto em borne KRE de 3 vias (A, B, SH) com ilhós; a distribuição de 5 V é feita nos próprios bornes.
- O proto shield simples exige soldar barras de pinos e bornes no Uno, como no Mega (ver [Montagem e conexões](MONTAGEM_E_CONEXOES.md)).
- No Cat5e, use o par azul (branco-azul = A, azul = B) e o fio verde como referência GND. Os demais fios ficam sem uso, cortados e isolados. **Nunca use pares sobrando para levar +5 V entre salas.**
- O Cat5e comum tem condutor **rígido** (sólido): ele entra direto no Wago ou no borne, **sem ilhós** (ilhós é para fio flexível). Prenda o cabo com abraçadeira logo após o prensa-cabo para que o condutor rígido não fique balançando e quebre na entrada do borne.

---

## Cenário C — Industrial (referência)

Entradas optoisoladas 24 V, botões 22 mm novos, fontes para trilho DIN e cabo RS-485 de marca (tipo Belden):

- Subtotal: **R$ 3.528,76**
- Com reserva de 15%: **R$ 4.058,07**

Mantido apenas como comparação. Para 4 salas, 47 posições e 45 m de cabo, o Cenário A atende com folga; o Cenário C faz sentido apenas se o ambiente tiver ruído elétrico severo ou se houver exigência de padrão industrial.

---

## O que observar ao comprar

| # | Item | O que conferir |
|---|---|---|
| 3 | Arduino Uno R3 compatível | Microcontrolador **ATmega328P** (DIP ou SMD). Conversor USB **CH340** é aceito; no Windows pode ser necessário instalar o driver CH340. Evite placas "Uno" com outros microcontroladores (LGT8F328P, por exemplo) — o firmware não foi testado nelas. Confira se vem com barras fêmea soldadas e furos de fixação. |
| 4 | LCD 20x2 I²C | Já existente. Confira se o módulo adaptador traseiro é PCF8574 (endereço 0x27) ou PCF8574A (0x3F). |
| 5 | MAX485 TTL | Módulo de 5 V com CI MAX485 (ou equivalente) e borne de 2 vias para A/B. Confira que tem o resistor **R7 de 120 Ω** entre A e B (marcação "121"); ele será retirado nos módulos das Salas 2 e 3. Compre 1 de reserva se possível. |
| 6 | Fita WS2812B | Tem de ser **WS2812B 5 V**, com 3 pads (5V, DIN/DO, GND). **Não** comprar WS2811 12 V (1 CI para 3 LEDs, alimentação 12 V), nem SK6812 RGBW, nem fita "5050 RGB" comum de 4 pads (+12V, R, G, B). Densidade 60 LED/m facilita cortar um pixel por posição. IP20 (sem silicone) é mais fácil de soldar. Prefira cobre "puro" na fita (pads largos e PCB mais grossa). |
| 7 | Buzzer ativo 5 V | "Ativo" = já tem oscilador interno, toca com tensão contínua. Corrente ≤ 30 mA a 5 V (ver ficha técnica). Buzzer passivo não serve. |
| 8 | Botão 16 mm N.A. | Contato normalmente aberto, pulsador (retorno por mola, não trava). Confira o tipo de terminal (solda, parafuso ou faston) para preparar o acabamento. |
| 9 | Kit resistores/capacitores | Resistores de 1/4 W, filme metálico (1%) de preferência. Eletrolíticos de **16 V ou mais** (1000 µF e 470 µF), de marca reconhecida; 100 nF cerâmico multicamada. Quantidades mínimas: 560 Ω × 2, 100 Ω × 3, 330 Ω × 4, 1000 µF × 1, 470 µF × 3, 100 nF × 4; o 120 Ω fica de reserva (o terminador já vem no MAX485). |
| 10, 11 | Fontes 5 V | Fonte **regulada** (chaveada), com saída estável entre 5,0 e 5,2 V. Tipo carregador de parede com certificação **INMETRO** ou fonte "colmeia" de marca com trimpot de ajuste. Evite fontes sem marca, muito leves, ou "carregador rápido" de procedência duvidosa. Fonte colmeia exige ligação na rede (fase, neutro, terra) feita por eletricista e tampa protetora nos bornes de entrada. |
| 12 | Cabo blindado 2 vias | **Par trançado** (as duas vias torcidas entre si) e **malha** (trançada ou espiral) envolvendo o par. Condutores de cobre (não CCA — alumínio cobreado), 24 AWG (0,20–0,30 mm²). Cabo de microfone balanceado de boa qualidade ou cabo próprio para RS-485 de 1 par. Diâmetro externo compatível com o PG7 (3 a 6,5 mm). |
| 13 | Cabinho 0,5 mm² | Cobre **estanhado** (fios prateados), flexível (classe 5), isolação para 300 V ou mais. Se possível, compre em 3 ou 4 cores (vermelho = +5 V, preto = GND, outras para sinais) em rolos menores, mantendo o total. |
| 14 | Fio 26 AWG | Flexível, cobre estanhado, 3 cores (sugestão: vermelho = 5 V, preto = GND, amarelo ou branco = dados). Isolação de PVC ou silicone; silicone aguenta melhor o calor da solda. |
| 15 | Prensa-cabo PG7 | Faixa de aperto que cubra o diâmetro real do cabo (tipicamente 3–6,5 mm). Nylon com contraporca. |
| 16 | Screw shield para Uno | Bornes de parafuso para **todos** os pinos, incluindo 5V e GND (de preferência mais de um GND). Confira se as barras de pinos encaixam firme no Uno e se o shield tem furos de fixação. |
| 17 | Mega Proto Shield | Versão com área perfurada grande e barras de pinos para todos os conectores do Mega, incluindo a barra dupla D22–D53. Furos metalizados. |
| 18 | Bornes KRE 5,08 mm | Corpo com parafuso e placa de pressão (não "mola de lâmina" barata). Confira se os pinos entram nos furos do proto shield. |
| 19 | Borne plugável KF2EDG | Passo 5,08 mm, **com flange e parafusos de trava**. Para o Mega: parte fixa de placa (para soldar) + plugue. Para os Uno: versão fio-fio (as duas metades com parafuso). Confira número de vias de cada par. |
| 20 | Wago 221-413 | Original Wago (série 221, alavanca laranja, 3 entradas). Cópias genéricas costumam ter mola fraca. Quantidade: as 12 unidades cobrem a junção A, B e SH nas 4 salas (4 × 3). Se a distribuição de +5 V e GND também for feita em Wago em todas as salas (2 por sala), serão necessárias até 8 unidades a mais — confira na cotação. |
| 21 | Ilhós | Isolados (com colarinho plástico), cobre estanhado. O kit 0,5–1,5 mm² atende o cabinho de 0,5 mm². Para as vias de 24 AWG do cabo de rede, compre também um pacote de ilhós **0,25 mm²** (ou 0,34 mm²) — ver [Montagem e conexões](MONTAGEM_E_CONEXOES.md). O tamanho do ilhós tem de corresponder à seção do fio. |
| 22 | Terminal garfo | Pré-isolado, para fio 0,5–1,5 mm² (faixa "vermelha"), furo para parafuso M3 ou M3,5 (confira o parafuso dos blocos de contato dos botões). |
| 23 | Termo-retrátil | Razão de contração 2:1 ou 3:1. Diâmetros de 1,5 a 10 mm. Um pedaço com cola interna (adesivo) ajuda nas emendas sujeitas a umidade. |
| 24 | Espaçadores M3 | Nylon, macho-fêmea e fêmea-fêmea, alturas de 6 a 15 mm. Os furos do Uno e do Mega são de 3,2 mm. |
| 25 | Abraçadeiras e anilhas | Abraçadeiras de nylon 2,5 × 100 mm e 3,6 × 150 mm; bases adesivas com furo para parafuso (mais firmes que só adesivo); anilhas numeradas 0–9 tipo "argola" para fio de 0,5 mm². |
| 26 | Verniz isolante | Verniz **acrílico** próprio para placas eletrônicas (conformal coating). Não use verniz de móveis, esmalte ou spray de tinta. |

---

## Por que mudou em relação à versão anterior (R$ 211,50)

- A lista antiga não incluía shields de borne, ilhós, Wago, prensa-cabos, fio interno, termo-retrátil, espaçadores nem verniz — sem eles a montagem fica com jumpers e emendas que soltam e oxidam.
- Uno R3 em vez de Nano (escolha do cliente) custa mais por placa.
- Fontes e fita foram atualizadas para preços realistas de mercado.
- O cabo deixou de ser Cat5e de 4 pares (energia não trafega mais) e passou a ser 2 vias blindado.

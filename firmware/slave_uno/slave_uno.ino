/*
 * ============================================================================
 *  PAINEL DE SINALIZAÇÃO DE 4 SALAS — FIRMWARE DAS SALAS REMOTAS (ESCRAVO)
 * ============================================================================
 *  Arquivo   : slave_uno.ino
 *  Placa     : Arduino Uno R3 (Salas 2, 3 e 4 — o MESMO programa nas três)
 *  Versão    : 2.0 — conforme ESPECIFICAÇÃO REV. 5.0 (23/11/2026)
 *  Protocolo : RS-485 v2 (quadros de 6 bytes, CRC-8 polinômio 0x07, início 0x00)
 *
 *  O QUE ESTE PROGRAMA FAZ
 *  - Lê os 11 botões das posições da sala; cada toque alterna verde <-> vermelho.
 *  - Acende os 11 LEDs WS2812B locais com a cor de cada posição.
 *  - Ouve o barramento RS-485 e responde SOMENTE aos pedidos com o seu ID
 *    (SLAVE_ID) e CRC correto, devolvendo o estado das 11 posições.
 *  - Recebe da central, em todo pedido, a máscara de posições habilitadas.
 *    Posição desabilitada fica azul, ignora o botão e volta a "ocupada".
 *  - Se ficar 3 s sem receber pedido válido, os 11 LEDs piscam âmbar (4 Hz),
 *    para o operador saber que a central não está ouvindo. Os botões continuam
 *    funcionando e o estado é enviado quando a comunicação voltar.
 *
 *  POSIÇÕES DE CADA SALA
 *  - SLAVE_ID 2 = Sala 2 = P15 a P25
 *  - SLAVE_ID 3 = Sala 3 = P26 a P36
 *  - SLAVE_ID 4 = Sala 4 = P37 a P47
 *
 *  PINAGEM (Arduino Uno R3)
 *  - 5V / GND .......... fonte local 5 V 2 A (borne do screw shield)
 *  - D0 (RX) ........... MAX485 RO   (DESCONECTAR ao gravar pela USB)
 *  - D1 (TX) ........... MAX485 DI   (DESCONECTAR ao gravar pela USB)
 *  - D4 ................ MAX485 DE e /RE (jumpeados juntos)
 *  - D5 ................ DIN dos 11 WS2812B locais (via resistor 330 ohms)
 *  - D6 ... D12 ........ botões das posições 01 a 07 da sala (N.A. para GND)
 *  - A0 ... A3 ......... botões das posições 08 a 11 da sala (N.A. para GND)
 *  - D13 (LED da placa)  pisca a cada pedido válido recebido (diagnóstico)
 *
 *  BIBLIOTECA (Arduino IDE > Ferramentas > Gerenciar Bibliotecas...)
 *  - "Adafruit NeoPixel"   (autor: Adafruit)
 *
 *  COMO GRAVAR (leia com atenção)
 *  1. TROQUE O SLAVE_ID logo abaixo: 2 na Sala 2, 3 na Sala 3, 4 na Sala 4.
 *  2. DESCONECTE os fios RO e DI do MAX485 (D0 e D1) ou tire o módulo antes de
 *     gravar. O Uno usa os mesmos pinos D0/D1 para a USB; com o MAX485 ligado a
 *     gravação falha ("not in sync" / "programmer is not responding").
 *  3. Ferramentas > Placa > "Arduino Uno"; escolha a porta COM; Carregar.
 *  4. Religue RO em D0 e DI em D1. Pronto.
 *  5. Etiquete a placa com o número da sala (ID 2, 3 ou 4). Dois escravos com o
 *     mesmo ID no barramento causam colisão e falhas nas duas salas.
 * ============================================================================
 */

#include <Adafruit_NeoPixel.h>   // Biblioteca que controla os LEDs WS2812B

// ############################################################################
// ####                                                                    ####
// ####   >>>>>>>>   TROQUE AQUI O NÚMERO DA SALA DESTA PLACA   <<<<<<<<   ####
// ####                                                                    ####
// ####          Sala 2 -> 2        Sala 3 -> 3        Sala 4 -> 4          ####
// ####                                                                    ####
// ############################################################################
#define SLAVE_ID 2               // <<<<<< ID DESTA SALA NO BARRAMENTO (2, 3 ou 4)
// ############################################################################

#if (SLAVE_ID < 2) || (SLAVE_ID > 4)                    // Confere o ID na compilação
#error "SLAVE_ID precisa ser 2, 3 ou 4"                 // Para a compilação se o ID estiver errado
#endif                                                  // Fim da conferência

// ============================================================================
// PINOS (números físicos da placa Uno)
// ============================================================================
constexpr uint8_t PINO_RX = 0;           // D0: recebe do RO do MAX485
constexpr uint8_t PINO_RS485_DIR = 4;    // DE+/RE do MAX485: HIGH = transmitir, LOW = ouvir
constexpr uint8_t PINO_LEDS = 5;         // Saída de dados para os 11 LEDs WS2812B
constexpr uint8_t PINO_LED_PLACA = 13;   // LED soldado na placa (diagnóstico)

constexpr uint8_t NUM_POSICOES = 11;     // 11 posições por sala remota
constexpr uint8_t PINOS_BOTOES[NUM_POSICOES] = {  // Pino de cada botão (posição 01 a 11 da sala)
  6, 7, 8, 9, 10, 11, 12,               // Posições 01 a 07 nos pinos D6 a D12
  A0, A1, A2, A3                        // Posições 08 a 11 nos pinos A0 a A3 (D14 a D17)
};                                      // Fim da tabela de pinos

// ============================================================================
// CORES DOS LEDS (0xRRGGBB = vermelho, verde, azul em hexadecimal)
// ============================================================================
constexpr uint8_t BRILHO_LEDS = 100;              // 100 de 255 = cerca de 40% de brilho
constexpr uint32_t COR_DESABILITADA = 0x000028;   // Azul escuro (0, 0, 40): posição sem uso no dia
constexpr uint32_t COR_OCUPADA = 0x00FF00;        // Verde (0, 255, 0): ocupada / em atendimento
constexpr uint32_t COR_LIVRE = 0xFF0000;          // Vermelho (255, 0, 0): livre
constexpr uint32_t COR_FALHA = 0xFF8C00;          // Âmbar (255, 140, 0): central não está ouvindo
constexpr uint32_t COR_APAGADA = 0x000000;        // Apagado (fase "desligada" do pisca)

// ============================================================================
// PROTOCOLO RS-485 v2 (igual ao do mestre)
// ============================================================================
constexpr uint32_t RS485_BAUD = 9600;        // Velocidade do barramento: 9600 bps, 8N1
constexpr uint8_t INICIO_PEDIDO = 0xA5;      // Primeiro byte de todo pedido (mestre -> escravo)
constexpr uint8_t INICIO_RESPOSTA = 0x5A;    // Primeiro byte de toda resposta (escravo -> mestre)
constexpr uint8_t TAMANHO_QUADRO = 6;        // Todo quadro tem exatamente 6 bytes
constexpr uint8_t BYTES_COM_CRC = 5;         // O CRC é calculado sobre os 5 primeiros bytes
constexpr uint16_t MASCARA_11_BITS = 0x07FF; // Só os bits 0 a 10 têm significado

// ============================================================================
// TEMPOS
// ============================================================================
constexpr uint32_t TIMEOUT_ENTRE_BYTES_US = 5000;  // Mais de 5 ms entre bytes = quadro descartado
constexpr uint32_t ATRASO_RESPOSTA_US = 1000;      // Espera ~1 ms antes de responder
constexpr uint32_t SEM_PEDIDO_MS = 3000;           // 3 s sem pedido válido = pisca âmbar
constexpr uint32_t DEBOUNCE_MS = 40;               // Botão precisa ficar 40 ms estável
constexpr uint32_t MEIO_PISCA_MS = 125;            // Troca aceso/apagado a cada 125 ms = 4 Hz
constexpr uint32_t LED_PLACA_MS = 15;              // Tempo que o LED D13 fica aceso por pedido

// ============================================================================
// TIPOS DE DADOS
// ============================================================================
struct Botao {                // Guarda tudo sobre um botão para o anti-repique sem delay()
  uint8_t pino;               // Número do pino do botão
  bool pressionado;           // Estado já confirmado (true = apertado)
  bool leituraAnterior;       // Última leitura bruta do pino
  uint32_t tMudanca;          // Momento (millis) em que a leitura bruta mudou
};                            // Fim da estrutura Botao

// ============================================================================
// OBJETOS E VARIÁVEIS
// ============================================================================
Adafruit_NeoPixel fita(NUM_POSICOES, PINO_LEDS, NEO_GRB + NEO_KHZ800);  // 11 LEDs WS2812B

Botao botoes[NUM_POSICOES];              // Os 11 botões (preenchidos no setup)
uint16_t mascara = MASCARA_11_BITS;      // Bit i = 1: posição i habilitada (até a central mandar, todas)
uint16_t estadoLivre = 0;                // Bit i = 1: posição i livre (vermelho); 0 = ocupada (verde)

uint8_t quadroRx[TAMANHO_QUADRO];        // Bytes do pedido sendo recebido
uint8_t posRx = 0;                       // Quantos bytes do pedido já chegaram
uint32_t tUltimoByteUs = 0;              // Momento (micros) do último byte recebido

bool respostaPendente = false;           // true = recebeu pedido e precisa responder
uint8_t seqPendente = 0;                 // SEQ do pedido a ser devolvido na resposta
uint32_t tPedidoUs = 0;                  // Momento (micros) em que o pedido terminou de chegar

bool comunicacaoOk = true;               // false = 3 s sem pedido válido (pisca âmbar)
uint32_t tUltimoPedidoValido = 0;        // Momento (millis) do último pedido válido

bool ledsSujos = true;                   // true = algo mudou e os LEDs precisam ser redesenhados
bool fasePisca = false;                  // Fase do pisca âmbar (true = aceso)
uint32_t tPisca = 0;                     // Momento da última troca de fase do pisca
uint32_t tLedPlaca = 0;                  // Momento em que o LED D13 foi aceso

// ============================================================================
// CRC-8 (polinômio 0x07, valor inicial 0x00, sem reflexão) — IGUAL NO MESTRE
// ============================================================================
uint8_t crc8(const uint8_t *dados, uint8_t tamanho) {     // Calcula o CRC de "tamanho" bytes
  uint8_t crc = 0x00;                                     // Valor inicial do CRC
  for (uint8_t i = 0; i < tamanho; i++) {                 // Passa por cada byte
    crc ^= dados[i];                                      // Mistura o byte no CRC
    for (uint8_t b = 0; b < 8; b++) {                     // Processa os 8 bits do byte
      if (crc & 0x80) {                                   // Se o bit mais alto é 1...
        crc = (uint8_t)((crc << 1) ^ 0x07);               // ...desloca e aplica o polinômio 0x07
      } else {                                            // Se o bit mais alto é 0...
        crc = (uint8_t)(crc << 1);                        // ...só desloca
      }                                                   // Fim do teste do bit alto
    }                                                     // Fim dos 8 bits
  }                                                       // Fim dos bytes
  return crc;                                             // Devolve o CRC calculado
}                                                         // Fim de crc8()

// ============================================================================
// BOTÕES COM ANTI-REPIQUE (debounce) SEM delay()
// ============================================================================
bool atualizarBotao(Botao &b, uint32_t agora) {           // Devolve true quando o estado confirmado muda
  bool leitura = (digitalRead(b.pino) == LOW);            // Botão para GND: LOW = apertado
  if (leitura != b.leituraAnterior) {                     // A leitura bruta mudou?
    b.leituraAnterior = leitura;                          // Guarda a nova leitura
    b.tMudanca = agora;                                   // Reinicia a contagem dos 40 ms
  }                                                       // Fim do teste de mudança
  if (leitura != b.pressionado && (agora - b.tMudanca) >= DEBOUNCE_MS) {  // Ficou estável 40 ms?
    b.pressionado = leitura;                              // Confirma o novo estado
    return true;                                          // Avisa que mudou
  }                                                       // Fim do teste de estabilidade
  return false;                                           // Nada mudou
}                                                         // Fim de atualizarBotao()

void lerBotoes(uint32_t agora) {                          // Trata os 11 botões da sala
  for (uint8_t i = 0; i < NUM_POSICOES; i++) {            // Para cada botão
    if (!atualizarBotao(botoes[i], agora)) continue;      // Sem mudança: próximo botão
    if (!botoes[i].pressionado) continue;                 // Só age no aperto, não na soltura
    if (!bitRead(mascara, i)) continue;                   // Posição desabilitada (azul): ignora
    estadoLivre ^= (uint16_t)(1u << i);                   // Alterna verde <-> vermelho
    ledsSujos = true;                                     // Pede redesenho dos LEDs
  }                                                       // Fim do laço
}                                                         // Fim de lerBotoes()

// ============================================================================
// COMUNICAÇÃO RS-485
// ============================================================================
void aplicarMascara(uint16_t nova) {                      // Usa a máscara recebida da central
  nova &= MASCARA_11_BITS;                                // Ignora bits que não existem
  if (nova == mascara) return;                            // Igual à atual: nada muda
  mascara = nova;                                         // Guarda a nova máscara
  estadoLivre &= mascara;                                 // Desabilitada volta a "ocupada" (bit livre = 0)
  ledsSujos = true;                                       // Redesenha (azul nas desabilitadas)
}                                                         // Fim de aplicarMascara()

void processarPedido() {                                  // Chamada quando chegam 6 bytes
  if (crc8(quadroRx, BYTES_COM_CRC) != quadroRx[5]) return;  // CRC errado: ignora em silêncio
  if (quadroRx[1] != SLAVE_ID) return;                    // Pedido para outra sala: ignora
  aplicarMascara(((uint16_t)quadroRx[3] << 8) | quadroRx[4]);  // MASK_H e MASK_L
  seqPendente = quadroRx[2];                              // Guarda o SEQ para devolver igual
  respostaPendente = true;                                // Agenda a resposta
  tPedidoUs = micros();                                   // Marca o fim do pedido (conta ~1 ms)
  tUltimoPedidoValido = millis();                         // Central está ouvindo
  tLedPlaca = tUltimoPedidoValido;                        // Marca para piscar o LED D13
  digitalWrite(PINO_LED_PLACA, HIGH);                     // Acende o LED D13
  if (comunicacaoOk) return;                              // Já estava tudo bem: pronto
  comunicacaoOk = true;                                   // Comunicação voltou
  ledsSujos = true;                                       // Tira o âmbar dos LEDs
}                                                         // Fim de processarPedido()

void receberBytes() {                                     // Máquina de estados da recepção
  while (Serial.available() > 0) {                        // Enquanto houver bytes chegando
    uint8_t b = (uint8_t)Serial.read();                   // Lê um byte
    uint32_t agoraUs = micros();                          // Hora da leitura (microssegundos)
    if (posRx > 0 && (agoraUs - tUltimoByteUs) > TIMEOUT_ENTRE_BYTES_US) posRx = 0;  // > 5 ms: descarta
    tUltimoByteUs = agoraUs;                              // Guarda a hora deste byte
    if (posRx == 0 && b != INICIO_PEDIDO) continue;       // Espera o 0xA5 para começar um quadro
    quadroRx[posRx++] = b;                                // Guarda o byte
    if (posRx < TAMANHO_QUADRO) continue;                 // Ainda faltam bytes
    posRx = 0;                                            // Quadro completo: prepara o próximo
    processarPedido();                                    // Confere CRC/ID e agenda resposta
  }                                                       // Fim do laço de recepção
}                                                         // Fim de receberBytes()

void enviarResposta() {                                   // Manda o quadro de resposta
  uint8_t q[TAMANHO_QUADRO];                              // Espaço para os 6 bytes
  q[0] = INICIO_RESPOSTA;                                 // Byte 0: 0x5A (início de resposta)
  q[1] = SLAVE_ID;                                        // Byte 1: ID desta sala
  q[2] = seqPendente;                                     // Byte 2: o mesmo SEQ do pedido
  q[3] = highByte(estadoLivre);                           // Byte 3: parte alta do estado
  q[4] = lowByte(estadoLivre);                            // Byte 4: parte baixa do estado
  q[5] = crc8(q, BYTES_COM_CRC);                          // Byte 5: CRC dos 5 primeiros
  digitalWrite(PINO_RS485_DIR, HIGH);                     // MAX485 em modo transmitir
  Serial.write(q, TAMANHO_QUADRO);                        // Envia os 6 bytes
  Serial.flush();                                         // Espera o último bit sair de verdade
  digitalWrite(PINO_RS485_DIR, LOW);                      // Volta a ouvir (libera o barramento)
  respostaPendente = false;                               // Resposta entregue
}                                                         // Fim de enviarResposta()

void tratarResposta() {                                   // Responde ~1 ms depois do pedido
  if (!respostaPendente) return;                          // Nada a responder
  if ((micros() - tPedidoUs) < ATRASO_RESPOSTA_US) return;  // Ainda não passou 1 ms
  enviarResposta();                                       // Responde agora
}                                                         // Fim de tratarResposta()

void verificarComunicacao(uint32_t agora) {               // 3 s sem pedido = alerta local
  if (!comunicacaoOk) return;                             // Já está em alerta
  if (agora - tUltimoPedidoValido < SEM_PEDIDO_MS) return;  // Recebeu pedido há pouco: OK
  comunicacaoOk = false;                                  // Central não está ouvindo
  ledsSujos = true;                                       // Começa a piscar âmbar
}                                                         // Fim de verificarComunicacao()

// ============================================================================
// LEDS LOCAIS
// ============================================================================
uint32_t corDaPosicao(uint8_t i) {                        // Decide a cor do LED da posição i
  if (!comunicacaoOk) return fasePisca ? COR_FALHA : COR_APAGADA;  // Sem central: pisca âmbar
  if (!bitRead(mascara, i)) return COR_DESABILITADA;      // Desabilitada: azul escuro
  if (bitRead(estadoLivre, i)) return COR_LIVRE;          // Livre: vermelho
  return COR_OCUPADA;                                     // Ocupada: verde
}                                                         // Fim de corDaPosicao()

void atualizarLeds(uint32_t agora) {                      // Redesenha os LEDs só quando precisa
  if (!comunicacaoOk && (agora - tPisca) >= MEIO_PISCA_MS) {  // Hora de trocar a fase do pisca?
    tPisca = agora;                                       // Marca a troca
    fasePisca = !fasePisca;                               // Inverte aceso/apagado
    ledsSujos = true;                                     // Precisa redesenhar
  }                                                       // Fim do tique do pisca
  if (!ledsSujos) return;                                 // Nada mudou: não chama show()
  if (respostaPendente) return;                           // Responde primeiro, desenha depois
  for (uint8_t i = 0; i < NUM_POSICOES; i++) {            // Para cada LED
    fita.setPixelColor(i, corDaPosicao(i));               // Define a cor
  }                                                       // Fim do laço
  fita.show();                                            // Envia para os LEDs (~0,35 ms)
  ledsSujos = false;                                      // LEDs em dia
}                                                         // Fim de atualizarLeds()

void atualizarLedPlaca(uint32_t agora) {                  // Apaga o LED D13 depois de 15 ms
  if (agora - tLedPlaca >= LED_PLACA_MS) digitalWrite(PINO_LED_PLACA, LOW);  // Tempo esgotado: apaga
}                                                         // Fim de atualizarLedPlaca()

// ============================================================================
// SETUP: roda uma vez ao ligar
// ============================================================================
void configurarPinos() {                                  // Configura entradas e saídas
  pinMode(PINO_RS485_DIR, OUTPUT);                        // Pino de direção do MAX485 é saída
  digitalWrite(PINO_RS485_DIR, LOW);                      // Começa ouvindo (nunca prende o barramento)
  pinMode(PINO_RX, INPUT_PULLUP);                         // Pull-up no RX: evita lixo com o RO solto
  pinMode(PINO_LED_PLACA, OUTPUT);                        // LED D13 é saída
  digitalWrite(PINO_LED_PLACA, LOW);                      // LED D13 apagado
  for (uint8_t i = 0; i < NUM_POSICOES; i++) {            // Para cada botão
    botoes[i] = {PINOS_BOTOES[i], false, false, 0};       // Prepara a estrutura do botão
    pinMode(PINOS_BOTOES[i], INPUT_PULLUP);               // Resistor interno para 5 V
  }                                                       // Fim do laço
}                                                         // Fim de configurarPinos()

void setup() {                                            // Início do programa
  configurarPinos();                                      // Pinos primeiro (MAX485 em recepção)
  fita.begin();                                           // Prepara o pino dos LEDs
  fita.setBrightness(BRILHO_LEDS);                        // Brilho de 40%
  fita.clear();                                           // Apaga todos
  fita.show();                                            // Envia "apagado"
  Serial.begin(RS485_BAUD);                               // Serial D0/D1 do RS-485: 9600 8N1
  tUltimoPedidoValido = millis();                         // Dá 3 s para o primeiro pedido chegar
  ledsSujos = true;                                       // Todas começam verdes (ocupadas)
}                                                         // Fim de setup()

// ============================================================================
// LOOP: roda sem parar (nada de delay())
// ============================================================================
void loop() {                                             // Laço principal
  receberBytes();                                         // Lê o barramento (pedidos da central)
  tratarResposta();                                       // Responde se for a hora
  uint32_t agora = millis();                              // Hora atual (lida DEPOIS da recepção)
  lerBotoes(agora);                                       // Botões das 11 posições
  verificarComunicacao(agora);                            // 3 s sem pedido?
  atualizarLeds(agora);                                   // Atualiza os LEDs locais
  atualizarLedPlaca(agora);                               // Apaga o LED D13
}                                                         // Fim de loop()

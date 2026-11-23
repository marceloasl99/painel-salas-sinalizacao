/*
 * ============================================================================
 *  PAINEL DE SINALIZAÇÃO DE 4 SALAS — FIRMWARE DA CENTRAL (SALA 1, MESTRE)
 * ============================================================================
 *  Arquivo   : master_mega.ino
 *  Placa     : Arduino Mega 2560 R3
 *  Versão    : 2.0 — conforme ESPECIFICAÇÃO REV. 5.0 (23/11/2026)
 *  Protocolo : RS-485 v2 (quadros de 6 bytes, CRC-8 polinômio 0x07, início 0x00)
 *
 *  O QUE ESTE PROGRAMA FAZ
 *  - Controla o painel central com 47 LEDs WS2812B (P01 a P47, um por posição).
 *  - Lê os 14 botões das posições da Sala 1 (P01 a P14).
 *  - Pergunta, uma de cada vez, às Salas 2, 3 e 4 (escravos 2, 3 e 4) o estado
 *    das posições delas, pelo barramento RS-485 (um pedido a cada 100 ms).
 *  - Envia em todo pedido a "máscara" (quais posições estão habilitadas no dia).
 *  - Detecta sala sem comunicação (2 s sem resposta válida): as posições dela
 *    piscam âmbar no painel, o buzzer dá 2 bipes a cada 5 s e o LCD avisa.
 *  - IHM com LCD 20x2 e 2 botões (NAV e HAB): modos MONITOR, SETUP e PRESETS.
 *  - Guarda a configuração do dia na EEPROM (memória que não apaga ao desligar).
 *
 *  CORES (brilho 40%)
 *  - Azul escuro (0,0,40)  = posição desabilitada no dia
 *  - Verde (0,255,0)       = ocupada / em atendimento
 *  - Vermelho (255,0,0)    = livre
 *  - Âmbar (255,140,0) piscando 4 Hz = sala sem comunicação
 *
 *  PINAGEM (Arduino Mega 2560)
 *  - 5V / GND .......... fonte 5 V 3 A (borne do proto shield)
 *  - D18 (TX1) ......... MAX485 DI
 *  - D19 (RX1) ......... MAX485 RO
 *  - D2 ................ MAX485 DE e /RE (jumpeados juntos)
 *  - D20 SDA / D21 SCL . LCD 20x2 I2C (PCF8574, endereço 0x27; alternativo 0x3F)
 *  - D4 ................ botão NAV (N.A. para GND)
 *  - D5 ................ botão HAB (N.A. para GND)
 *  - D6 ................ DIN do painel de 47 WS2812B (via resistor 330 ohms)
 *  - D7 ................ buzzer ativo 5 V (no máximo 30 mA)
 *  - D22 ... D35 ....... botões P01 ... P14 (N.A. para GND)
 *  - D13 (LED da placa)  pisca a cada resposta válida recebida (diagnóstico)
 *
 *  BIBLIOTECAS (Arduino IDE > Ferramentas > Gerenciar Bibliotecas...)
 *  - "Adafruit NeoPixel"   (autor: Adafruit)
 *  - "LiquidCrystal I2C"   (autor: Frank de Brabander) — usa lcd.init()
 *  - Wire e EEPROM já vêm com a IDE (não precisa instalar).
 *
 *  COMO GRAVAR
 *  1. Ferramentas > Placa > "Arduino Mega or Mega 2560"; Processador "ATmega2560".
 *  2. Escolha a porta COM do Mega e clique em Carregar.
 *  3. No Mega NÃO é preciso desligar o MAX485: ele usa a Serial1 (D18/D19) e a
 *     gravação usa a Serial0 (USB).
 *  4. Se o LCD acender mas não mostrar texto, troque LCD_ENDERECO para 0x3F e
 *     ajuste o trimpot de contraste atrás do LCD.
 *  5. Monitor Serial (USB) a 115200 bps mostra mensagens de diagnóstico.
 * ============================================================================
 */

#include <Wire.h>               // Biblioteca do barramento I2C (fios SDA/SCL do LCD)
#include <EEPROM.h>             // Biblioteca da memória EEPROM (guarda a configuração)
#include <LiquidCrystal_I2C.h>  // Biblioteca do LCD com módulo I2C (Frank de Brabander)
#include <Adafruit_NeoPixel.h>  // Biblioteca que controla os LEDs WS2812B

// ============================================================================
// CONFIGURAÇÕES QUE O TÉCNICO PODE PRECISAR TROCAR
// ============================================================================
#define LCD_ENDERECO 0x27       // Endereço I2C do LCD; se não funcionar, use 0x3F
#define DEPURACAO 1             // 1 = manda mensagens de diagnóstico pela USB; 0 = desliga

// ============================================================================
// PINOS (números físicos da placa Mega)
// ============================================================================
constexpr uint8_t PINO_RS485_DIR = 2;   // DE+/RE do MAX485: HIGH = transmitir, LOW = ouvir
constexpr uint8_t PINO_RX1 = 19;        // Pino RX1 (recebe do RO do MAX485)
constexpr uint8_t PINO_NAV = 4;         // Botão NAV (navegar)
constexpr uint8_t PINO_HAB = 5;         // Botão HAB (habilitar/aplicar)
constexpr uint8_t PINO_LEDS = 6;        // Saída de dados para os 47 LEDs WS2812B
constexpr uint8_t PINO_BUZZER = 7;      // Buzzer ativo (HIGH = apita)
constexpr uint8_t PINO_LED_PLACA = 13;  // LED soldado na placa (diagnóstico)

constexpr uint8_t POSICOES_SALA1 = 14;  // Sala 1 tem 14 posições (P01 a P14)
constexpr uint8_t PINOS_BOTOES_S1[POSICOES_SALA1] = {  // Pino de cada botão da Sala 1
  22, 23, 24, 25, 26, 27, 28,   // P01 a P07 nos pinos D22 a D28
  29, 30, 31, 32, 33, 34, 35    // P08 a P14 nos pinos D29 a D35
};                              // Fim da tabela de pinos dos botões

// ============================================================================
// QUANTIDADES DO SISTEMA
// ============================================================================
constexpr uint8_t TOTAL_POSICOES = 47;      // 47 posições no total (P01 a P47)
constexpr uint8_t POSICOES_REMOTA = 11;     // Cada sala remota tem 11 posições
constexpr uint8_t NUM_REMOTAS = 3;          // Salas remotas: 2, 3 e 4
constexpr uint8_t PRIMEIRO_ID_REMOTO = 2;   // ID da primeira sala remota (Sala 2)

// ============================================================================
// CORES DOS LEDS (vermelho, verde, azul de 0 a 255)
// ============================================================================
constexpr uint8_t BRILHO_LEDS = 100;        // 100 de 255 = cerca de 40% de brilho

// Cada cor é escrita como 0xRRGGBB (vermelho, verde, azul em hexadecimal), formato da NeoPixel
constexpr uint32_t COR_DESABILITADA = 0x000028;   // Azul escuro (0, 0, 40): posição sem uso no dia
constexpr uint32_t COR_OCUPADA = 0x00FF00;        // Verde (0, 255, 0): ocupada / em atendimento
constexpr uint32_t COR_LIVRE = 0xFF0000;          // Vermelho (255, 0, 0): livre
constexpr uint32_t COR_FALHA = 0xFF8C00;          // Âmbar (255, 140, 0): sala sem comunicação
constexpr uint32_t COR_APAGADA = 0x000000;        // Apagado (fase "desligada" do pisca)

// ============================================================================
// PROTOCOLO RS-485 v2 (igual ao do escravo)
// ============================================================================
constexpr uint32_t RS485_BAUD = 9600;       // Velocidade do barramento: 9600 bps, 8N1
constexpr uint8_t INICIO_PEDIDO = 0xA5;     // Primeiro byte de todo pedido (mestre -> escravo)
constexpr uint8_t INICIO_RESPOSTA = 0x5A;   // Primeiro byte de toda resposta (escravo -> mestre)
constexpr uint8_t TAMANHO_QUADRO = 6;       // Todo quadro tem exatamente 6 bytes
constexpr uint8_t BYTES_COM_CRC = 5;        // O CRC é calculado sobre os 5 primeiros bytes

// ============================================================================
// TEMPOS (em milissegundos)
// ============================================================================
constexpr uint32_t INTERVALO_PEDIDO_MS = 100;   // Um pedido a cada 100 ms (ciclo de 3 salas = 300 ms)
constexpr uint32_t ESPERA_RESPOSTA_MS = 25;     // Espera no máximo 25 ms pela resposta
constexpr uint32_t SALA_OFFLINE_MS = 2000;      // 2 s sem resposta válida = sala offline
constexpr uint32_t DEBOUNCE_MS = 40;            // Botão precisa ficar 40 ms estável (anti-repique)
constexpr uint32_t COMBO_MS = 1000;             // NAV+HAB juntos por 1 s = troca de modo
constexpr uint32_t INATIVIDADE_MS = 60000;      // 60 s sem tocar em NAV/HAB = volta ao MONITOR
constexpr uint32_t MEIO_PISCA_MS = 125;         // Troca aceso/apagado a cada 125 ms = 4 Hz
constexpr uint32_t ALARME_REPETE_MS = 5000;     // Repete os 2 bipes de falha a cada 5 s
constexpr uint32_t BIPE_LIGADO_MS = 60;         // Duração de cada bipe
constexpr uint32_t BIPE_PAUSA_MS = 120;         // Silêncio entre dois bipes
constexpr uint32_t REPETE_ATRASO_MS = 600;      // NAV segurado 0,6 s começa a avançar sozinho
constexpr uint32_t REPETE_PASSO_MS = 150;       // Depois avança uma posição a cada 150 ms
constexpr uint32_t LCD_ATUALIZA_MS = 200;       // Redesenha o LCD no máximo 5 vezes por segundo
constexpr uint32_t LCD_ALTERNA_MS = 2000;       // Em falha, linha 2 alterna a cada 2 s
constexpr uint32_t MENSAGEM_MS = 1500;          // Tempo da mensagem "APLICADO E SALVO"
constexpr uint32_t LED_PLACA_MS = 15;           // Tempo que o LED D13 fica aceso por resposta
constexpr uint32_t ESTATISTICA_MS = 10000;      // Diagnóstico USB a cada 10 s

// ============================================================================
// EEPROM (endereços dos bytes gravados)
// ============================================================================
constexpr uint16_t EE_END_MAGICO = 0;          // Byte 0: "byte mágico" (indica memória já usada)
constexpr uint16_t EE_END_VERSAO = 1;          // Byte 1: versão do formato
constexpr uint16_t EE_END_MASCARA = 2;         // Bytes 2 a 7: máscara atual (47 bits)
constexpr uint16_t EE_END_PERSONALIZADA = 8;   // Bytes 8 a 13: última configuração feita no SETUP
constexpr uint8_t EE_MAGICO = 0xA7;            // Valor do byte mágico (EEPROM virgem vale 0xFF)
constexpr uint8_t EE_VERSAO = 1;               // Versão 1 do formato
constexpr uint8_t EE_BYTES_MASCARA = 6;        // 6 bytes = 48 bits (47 usados)

// ============================================================================
// PRESETS
// ============================================================================
constexpr uint8_t PRESET_100_ATIVO = 0;        // Todas as 47 posições
constexpr uint8_t PRESET_TIPICO_35 = 1;        // Sala 1 inteira + 7 primeiras de cada remota
constexpr uint8_t PRESET_PLANTAO_20 = 2;       // 8 primeiras da Sala 1 + 4 primeiras de cada remota
constexpr uint8_t PRESET_ULTIMA = 3;           // Última configuração feita à mão no SETUP
constexpr uint8_t NUM_PRESETS = 4;             // Quantidade de presets
const char *const NOMES_PRESETS[NUM_PRESETS] = {  // Nomes que aparecem no LCD (sem acento)
  "100% ATIVO",                                // Preset 0
  "TIPICO 35",                                 // Preset 1
  "PLANTAO 20",                                // Preset 2
  "ULTIMA CONF."                               // Preset 3
};                                             // Fim da tabela de nomes

// ============================================================================
// TIPOS DE DADOS
// ============================================================================
struct Botao {                // Guarda tudo sobre um botão para o anti-repique sem delay()
  uint8_t pino;               // Número do pino do botão
  bool pressionado;           // Estado já confirmado (true = apertado)
  bool leituraAnterior;       // Última leitura bruta do pino
  uint32_t tMudanca;          // Momento (millis) em que a leitura bruta mudou
};                            // Fim da estrutura Botao

enum Modo : uint8_t {         // Telas da IHM
  MODO_MONITOR,               // Resumo de ocupação e estado da rede
  MODO_SETUP,                 // Habilita/desabilita posição por posição
  MODO_PRESETS                // Escolhe e aplica uma configuração pronta
};                            // Fim da lista de modos

enum Resultado : uint8_t {    // Resultado de uma consulta a um escravo
  RES_OK,                     // Resposta válida recebida
  RES_SEM_RESPOSTA,           // Nada chegou em 25 ms
  RES_INVALIDA                // Chegou algo, mas com CRC/ID/SEQ errado ou incompleto
};                            // Fim da lista de resultados

// ============================================================================
// OBJETOS DAS BIBLIOTECAS
// ============================================================================
LiquidCrystal_I2C lcd(LCD_ENDERECO, 20, 2);                          // LCD de 20 colunas e 2 linhas
Adafruit_NeoPixel fita(TOTAL_POSICOES, PINO_LEDS, NEO_GRB + NEO_KHZ800);  // 47 LEDs WS2812B

// ============================================================================
// VARIÁVEIS DE ESTADO
// ============================================================================
bool habilitada[TOTAL_POSICOES];         // true = posição habilitada no dia (índice 0 = P01)
bool livre[TOTAL_POSICOES];              // true = posição livre (vermelho); false = ocupada (verde)
bool salaOnline[NUM_REMOTAS];            // true = sala remota respondendo (índice 0 = Sala 2)
uint32_t tUltimaResposta[NUM_REMOTAS];   // Momento da última resposta válida de cada sala
uint8_t proximaRemota = 0;               // Qual sala será consultada no próximo pedido (0 = Sala 2)
uint8_t numeroSeq = 0;                   // Contador SEQ (0 a 255, volta a 0 sozinho)
uint32_t tUltimoPedido = 0;              // Momento do último pedido enviado

bool ledsSujos = true;                   // true = algo mudou e os LEDs precisam ser redesenhados
bool fasePisca = false;                  // Fase do pisca âmbar (true = aceso)
uint32_t tPisca = 0;                     // Momento da última troca de fase do pisca
uint32_t tLedPlaca = 0;                  // Momento em que o LED D13 foi aceso

uint8_t bipesPendentes = 0;              // Quantos bipes ainda faltam tocar
bool buzzerLigado = false;               // true = buzzer apitando agora
uint32_t tBuzzer = 0;                    // Momento da última troca liga/desliga do buzzer
bool alarmeAtivo = false;                // true = já existe sala offline sendo alarmada
uint32_t tAlarme = 0;                    // Momento dos últimos 2 bipes de falha

Modo modo = MODO_MONITOR;                // Modo atual da IHM (começa no MONITOR)
uint8_t cursorSetup = 0;                 // Posição mostrada no SETUP (0 = P01)
uint8_t presetEscolhido = 0;             // Preset mostrado no modo PRESETS
Botao botaoNav = {PINO_NAV, false, false, 0};   // Botão NAV
Botao botaoHab = {PINO_HAB, false, false, 0};   // Botão HAB
Botao botoesS1[POSICOES_SALA1];          // Botões P01 a P14 (preenchidos no setup)
bool comboEmCurso = false;               // true = NAV e HAB foram apertados juntos
bool comboDisparado = false;             // true = a troca de modo desse combo já aconteceu
bool navRepetiu = false;                 // true = NAV segurado já avançou sozinho
uint32_t tInicioCombo = 0;               // Momento em que NAV e HAB ficaram juntos
uint32_t tNavApertado = 0;               // Momento em que NAV foi apertado
uint32_t tUltimaRepeticao = 0;           // Momento do último avanço automático
uint32_t tUltimaTecla = 0;               // Momento do último toque em NAV ou HAB

char lcdTela[2][21];                     // O que está escrito no LCD agora (evita reescrever igual)
uint32_t tLcd = 0;                       // Momento da última atualização do LCD
uint32_t tMensagem = 0;                  // Momento em que a mensagem "APLICADO" apareceu
bool mensagemAtiva = false;              // true = mostrando "APLICADO E SALVO"

uint32_t contPedidos[NUM_REMOTAS];       // Diagnóstico: pedidos enviados por sala
uint32_t contOk[NUM_REMOTAS];            // Diagnóstico: respostas válidas por sala
uint32_t contSemResposta[NUM_REMOTAS];   // Diagnóstico: pedidos sem nenhuma resposta
uint32_t contInvalidas[NUM_REMOTAS];     // Diagnóstico: respostas com erro
uint32_t tEstatistica = 0;               // Momento do último relatório de diagnóstico

// ============================================================================
// CRC-8 (polinômio 0x07, valor inicial 0x00, sem reflexão) — IGUAL NO ESCRAVO
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
// FUNÇÕES DE POSIÇÃO (traduzem número de posição <-> sala)
// ============================================================================
uint8_t salaDaPosicao(uint8_t g) {                        // g = índice global 0..46
  if (g < POSICOES_SALA1) return 1;                       // 0..13 pertencem à Sala 1
  return PRIMEIRO_ID_REMOTO + (g - POSICOES_SALA1) / POSICOES_REMOTA;  // 14..24 = S2, 25..35 = S3, 36..46 = S4
}                                                         // Fim de salaDaPosicao()

uint8_t indiceLocal(uint8_t g) {                          // Posição dentro da própria sala (0 = primeira)
  if (g < POSICOES_SALA1) return g;                       // Na Sala 1 é o próprio índice
  return (g - POSICOES_SALA1) % POSICOES_REMOTA;          // Nas remotas: 0..10
}                                                         // Fim de indiceLocal()

uint8_t baseDaRemota(uint8_t r) {                         // r = 0 (Sala 2), 1 (Sala 3), 2 (Sala 4)
  return POSICOES_SALA1 + r * POSICOES_REMOTA;            // 14 + (ID-2) x 11
}                                                         // Fim de baseDaRemota()

bool haSalaOffline() {                                    // Existe alguma sala sem comunicação?
  for (uint8_t r = 0; r < NUM_REMOTAS; r++) {             // Verifica as 3 remotas
    if (!salaOnline[r]) return true;                      // Achou uma offline
  }                                                       // Fim do laço das remotas
  return false;                                           // Todas respondendo
}                                                         // Fim de haSalaOffline()

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

void lerBotoesSala1(uint32_t agora) {                     // Trata os botões P01 a P14
  for (uint8_t i = 0; i < POSICOES_SALA1; i++) {          // Para cada botão
    if (!atualizarBotao(botoesS1[i], agora)) continue;    // Sem mudança: próximo botão
    if (!botoesS1[i].pressionado) continue;               // Só age no aperto, não na soltura
    if (!habilitada[i]) continue;                         // Posição desabilitada (azul): ignora
    livre[i] = !livre[i];                                 // Alterna verde <-> vermelho
    ledsSujos = true;                                     // Pede redesenho dos LEDs
  }                                                       // Fim do laço dos botões
}                                                         // Fim de lerBotoesSala1()

// ============================================================================
// EEPROM
// ============================================================================
void gravarMascara(uint16_t endereco) {                   // Grava as 47 habilitações em 6 bytes
  for (uint8_t j = 0; j < EE_BYTES_MASCARA; j++) {        // Para cada um dos 6 bytes
    uint8_t valor = 0;                                    // Começa com todos os bits em 0
    for (uint8_t b = 0; b < 8; b++) {                     // Para cada bit do byte
      uint8_t g = j * 8 + b;                              // Posição correspondente (bit 0 do byte 0 = P01)
      if (g < TOTAL_POSICOES && habilitada[g]) bitSet(valor, b);  // Bit 1 = habilitada
    }                                                     // Fim dos bits
    EEPROM.update(endereco + j, valor);                   // update() só grava se mudou (poupa a EEPROM)
  }                                                       // Fim dos bytes
}                                                         // Fim de gravarMascara()

void lerMascara(uint16_t endereco) {                      // Lê 6 bytes da EEPROM para habilitada[]
  for (uint8_t g = 0; g < TOTAL_POSICOES; g++) {          // Para cada posição
    uint8_t valor = EEPROM.read(endereco + g / 8);        // Byte onde está o bit da posição
    habilitada[g] = bitRead(valor, g % 8);                // Bit 1 = habilitada
  }                                                       // Fim do laço das posições
}                                                         // Fim de lerMascara()

void carregarConfiguracao() {                             // Chamada ao ligar
  bool valida = (EEPROM.read(EE_END_MAGICO) == EE_MAGICO) &&     // Byte mágico confere?
                (EEPROM.read(EE_END_VERSAO) == EE_VERSAO);       // Versão confere?
  if (valida) {                                           // Já existe configuração gravada
    lerMascara(EE_END_MASCARA);                           // Restaura a última máscara
    return;                                               // Pronto
  }                                                       // Fim do caso "memória válida"
  for (uint8_t g = 0; g < TOTAL_POSICOES; g++) habilitada[g] = true;  // EEPROM virgem: 100% ativo
  gravarMascara(EE_END_MASCARA);                          // Grava a máscara inicial
  gravarMascara(EE_END_PERSONALIZADA);                    // A "última configuração" também começa 100%
  EEPROM.update(EE_END_VERSAO, EE_VERSAO);                // Grava a versão
  EEPROM.update(EE_END_MAGICO, EE_MAGICO);                // Grava o mágico por último (confirma tudo)
}                                                         // Fim de carregarConfiguracao()

// ============================================================================
// BUZZER (bipes sem delay())
// ============================================================================
void pedirBipes(uint8_t quantidade) {                     // Agenda "quantidade" bipes
  if (bipesPendentes < quantidade) bipesPendentes = quantidade;  // Não acumula pedidos repetidos
}                                                         // Fim de pedirBipes()

void atualizarBuzzer(uint32_t agora) {                    // Liga/desliga o buzzer no tempo certo
  if (buzzerLigado) {                                     // Está apitando?
    if (agora - tBuzzer < BIPE_LIGADO_MS) return;         // Ainda não deu o tempo do bipe
    digitalWrite(PINO_BUZZER, LOW);                       // Desliga o buzzer
    buzzerLigado = false;                                 // Marca como desligado
    tBuzzer = agora;                                      // Começa a contar a pausa
    return;                                               // Pronto por agora
  }                                                       // Fim do caso "apitando"
  if (bipesPendentes == 0) return;                        // Nada para tocar
  if (agora - tBuzzer < BIPE_PAUSA_MS) return;            // Ainda na pausa entre bipes
  digitalWrite(PINO_BUZZER, HIGH);                        // Liga o buzzer
  buzzerLigado = true;                                    // Marca como ligado
  bipesPendentes--;                                       // Um bipe a menos na fila
  tBuzzer = agora;                                        // Começa a contar a duração
}                                                         // Fim de atualizarBuzzer()

void atualizarAlarme(uint32_t agora) {                    // 2 bipes a cada 5 s com sala offline
  if (!haSalaOffline()) {                                 // Todas as salas respondendo?
    alarmeAtivo = false;                                  // Encerra o alarme
    return;                                               // Nada a fazer
  }                                                       // Fim do caso "rede OK"
  if (alarmeAtivo && (agora - tAlarme) < ALARME_REPETE_MS) return;  // Ainda não passaram 5 s
  alarmeAtivo = true;                                     // Alarme em andamento
  tAlarme = agora;                                        // Marca quando bipou
  pedirBipes(2);                                          // 2 bipes curtos
}                                                         // Fim de atualizarAlarme()

// ============================================================================
// COMUNICAÇÃO RS-485 (polling síncrono)
// ============================================================================
uint16_t mascaraDaRemota(uint8_t r) {                     // Monta os 11 bits de habilitação da sala
  uint16_t mascara = 0;                                   // Começa tudo desabilitado
  uint8_t base = baseDaRemota(r);                         // Índice global da 1ª posição da sala
  for (uint8_t i = 0; i < POSICOES_REMOTA; i++) {         // Para cada posição da sala
    if (habilitada[base + i]) bitSet(mascara, i);         // Bit i = 1 se habilitada
  }                                                       // Fim do laço
  return mascara;                                         // Devolve a máscara
}                                                         // Fim de mascaraDaRemota()

void enviarPedido(uint8_t id, uint8_t seq, uint16_t mascara) {  // Manda o quadro de pedido
  uint8_t q[TAMANHO_QUADRO];                              // Espaço para os 6 bytes
  q[0] = INICIO_PEDIDO;                                   // Byte 0: 0xA5 (início de pedido)
  q[1] = id;                                              // Byte 1: ID da sala (2, 3 ou 4)
  q[2] = seq;                                             // Byte 2: número de sequência
  q[3] = highByte(mascara);                               // Byte 3: parte alta da máscara
  q[4] = lowByte(mascara);                                // Byte 4: parte baixa da máscara
  q[5] = crc8(q, BYTES_COM_CRC);                          // Byte 5: CRC dos 5 primeiros
  while (Serial1.available() > 0) Serial1.read();         // Joga fora qualquer lixo antigo recebido
  digitalWrite(PINO_RS485_DIR, HIGH);                     // MAX485 em modo transmitir
  Serial1.write(q, TAMANHO_QUADRO);                       // Envia os 6 bytes
  Serial1.flush();                                        // Espera o último bit sair de verdade
  digitalWrite(PINO_RS485_DIR, LOW);                      // Volta a ouvir o barramento
}                                                         // Fim de enviarPedido()

bool respostaValida(const uint8_t *q, uint8_t id, uint8_t seq) {  // Confere um quadro de resposta
  if (q[0] != INICIO_RESPOSTA) return false;              // Tem que começar com 0x5A
  if (crc8(q, BYTES_COM_CRC) != q[5]) return false;       // CRC tem que bater
  if (q[1] != id) return false;                           // Tem que ser da sala perguntada
  return q[2] == seq;                                     // SEQ diferente = resposta atrasada, descarta
}                                                         // Fim de respostaValida()

Resultado aguardarResposta(uint8_t id, uint8_t seq, uint8_t *q) {  // Espera até 25 ms pela resposta
  uint8_t pos = 0;                                        // Quantos bytes do quadro já chegaram
  bool houveErro = false;                                 // true = chegou quadro com defeito
  uint32_t inicio = millis();                             // Marca o começo da espera
  while ((millis() - inicio) < ESPERA_RESPOSTA_MS) {      // Enquanto não passar 25 ms (LEDs parados!)
    if (Serial1.available() == 0) continue;               // Nada chegou ainda: continua esperando
    uint8_t b = (uint8_t)Serial1.read();                  // Lê um byte
    if (pos == 0 && b != INICIO_RESPOSTA) continue;       // Ignora bytes soltos até achar 0x5A
    q[pos++] = b;                                         // Guarda o byte no quadro
    if (pos < TAMANHO_QUADRO) continue;                   // Ainda faltam bytes
    pos = 0;                                              // Quadro completo: prepara para o próximo
    if (respostaValida(q, id, seq)) return RES_OK;        // Tudo certo: devolve sucesso
    houveErro = true;                                     // Quadro ruim: anota e continua esperando
  }                                                       // Fim da espera
  if (pos > 0) houveErro = true;                          // Quadro pela metade também é erro
  return houveErro ? RES_INVALIDA : RES_SEM_RESPOSTA;     // Informa o tipo de falha
}                                                         // Fim de aguardarResposta()

void aplicarResposta(uint8_t r, const uint8_t *q) {       // Copia o estado recebido para o painel
  uint16_t estado = ((uint16_t)q[3] << 8) | q[4];         // Junta ESTADO_H e ESTADO_L
  uint8_t base = baseDaRemota(r);                         // 1ª posição global da sala
  for (uint8_t i = 0; i < POSICOES_REMOTA; i++) {         // Para cada posição da sala
    bool novo = bitRead(estado, i) && habilitada[base + i];   // Livre só se também habilitada
    if (livre[base + i] == novo) continue;                // Não mudou: próxima
    livre[base + i] = novo;                               // Atualiza o estado
    ledsSujos = true;                                     // Pede redesenho dos LEDs
  }                                                       // Fim do laço
  tUltimaResposta[r] = millis();                          // Marca a hora da resposta válida
  if (salaOnline[r]) return;                              // Já estava online: pronto
  salaOnline[r] = true;                                   // Sala voltou
  ledsSujos = true;                                       // Tira o âmbar dos LEDs
#if DEPURACAO                                             // Só se o diagnóstico estiver ligado
  Serial.print(F("Sala "));                               // Mensagem pela USB
  Serial.print(r + PRIMEIRO_ID_REMOTO);                   // Número da sala
  Serial.println(F(" ONLINE"));                           // Avisa que voltou
#endif                                                    // Fim do bloco de diagnóstico
}                                                         // Fim de aplicarResposta()

void consultarProximaRemota() {                           // Faz um ciclo pedido -> resposta
  uint8_t r = proximaRemota;                              // Sala da vez (0 = Sala 2)
  proximaRemota = (proximaRemota + 1) % NUM_REMOTAS;      // Na próxima vez, a sala seguinte
  uint8_t id = r + PRIMEIRO_ID_REMOTO;                    // ID no barramento (2, 3 ou 4)
  numeroSeq++;                                            // Novo SEQ a cada pedido (255 -> 0)
  enviarPedido(id, numeroSeq, mascaraDaRemota(r));        // Envia o pedido com a máscara
  contPedidos[r]++;                                       // Diagnóstico: conta pedido
  uint8_t q[TAMANHO_QUADRO];                              // Espaço para a resposta
  Resultado res = aguardarResposta(id, numeroSeq, q);     // Espera até 25 ms (sem mexer nos LEDs)
  if (res == RES_SEM_RESPOSTA) contSemResposta[r]++;      // Diagnóstico: silêncio
  if (res == RES_INVALIDA) contInvalidas[r]++;            // Diagnóstico: erro de quadro
  if (res != RES_OK) return;                              // Falhou: fica com o estado anterior
  contOk[r]++;                                            // Diagnóstico: sucesso
  tLedPlaca = millis();                                   // Marca para piscar o LED D13
  digitalWrite(PINO_LED_PLACA, HIGH);                     // Acende o LED D13
  aplicarResposta(r, q);                                  // Atualiza o painel com o estado recebido
}                                                         // Fim de consultarProximaRemota()

void verificarSalasOffline(uint32_t agora) {              // Marca sala offline após 2 s sem resposta
  for (uint8_t r = 0; r < NUM_REMOTAS; r++) {             // Para cada sala remota
    if (!salaOnline[r]) continue;                         // Já está offline: nada a fazer
    if (agora - tUltimaResposta[r] < SALA_OFFLINE_MS) continue;  // Respondeu há pouco: OK
    salaOnline[r] = false;                                // Declara offline
    ledsSujos = true;                                     // Começa a piscar âmbar
#if DEPURACAO                                             // Só se o diagnóstico estiver ligado
    Serial.print(F("Sala "));                             // Mensagem pela USB
    Serial.print(r + PRIMEIRO_ID_REMOTO);                 // Número da sala
    Serial.println(F(" OFFLINE (2 s sem resposta)"));     // Avisa a falha
#endif                                                    // Fim do bloco de diagnóstico
  }                                                       // Fim do laço
}                                                         // Fim de verificarSalasOffline()

// ============================================================================
// LEDS DO PAINEL
// ============================================================================
uint32_t corDaPosicao(uint8_t g) {                        // Decide a cor do LED da posição g
  uint8_t sala = salaDaPosicao(g);                        // Sala dona da posição
  if (sala >= PRIMEIRO_ID_REMOTO && !salaOnline[sala - PRIMEIRO_ID_REMOTO]) {  // Sala offline?
    return fasePisca ? COR_FALHA : COR_APAGADA;           // Pisca âmbar
  }                                                       // Fim do caso offline
  if (!habilitada[g]) return COR_DESABILITADA;            // Desabilitada: azul escuro
  if (livre[g]) return COR_LIVRE;                         // Livre: vermelho
  return COR_OCUPADA;                                     // Ocupada: verde
}                                                         // Fim de corDaPosicao()

void atualizarLeds(uint32_t agora) {                      // Redesenha o painel só quando precisa
  if (haSalaOffline() && (agora - tPisca) >= MEIO_PISCA_MS) {  // Hora de trocar a fase do pisca?
    tPisca = agora;                                       // Marca a troca
    fasePisca = !fasePisca;                               // Inverte aceso/apagado
    ledsSujos = true;                                     // Precisa redesenhar
  }                                                       // Fim do tique do pisca
  if (!ledsSujos) return;                                 // Nada mudou: não chama show()
  for (uint8_t g = 0; g < TOTAL_POSICOES; g++) {          // Para cada LED (LED i = posição P(i+1))
    fita.setPixelColor(g, corDaPosicao(g));               // Define a cor
  }                                                       // Fim do laço
  fita.show();                                            // Envia para os LEDs (fora da espera RS-485)
  ledsSujos = false;                                      // Painel em dia
}                                                         // Fim de atualizarLeds()

void atualizarLedPlaca(uint32_t agora) {                  // Apaga o LED D13 depois de 15 ms
  if (agora - tLedPlaca >= LED_PLACA_MS) digitalWrite(PINO_LED_PLACA, LOW);  // Tempo esgotado: apaga
}                                                         // Fim de atualizarLedPlaca()

// ============================================================================
// AÇÕES DA IHM (o que NAV e HAB fazem em cada modo)
// ============================================================================
void entrarModo(Modo novo) {                              // Troca de modo
  modo = novo;                                            // Guarda o novo modo
  mensagemAtiva = false;                                  // Apaga mensagem antiga
}                                                         // Fim de entrarModo()

void proximoModo() {                                      // MONITOR -> SETUP -> PRESETS -> MONITOR
  if (modo == MODO_MONITOR) entrarModo(MODO_SETUP);       // Do MONITOR vai para o SETUP
  else if (modo == MODO_SETUP) entrarModo(MODO_PRESETS);  // Do SETUP vai para os PRESETS
  else entrarModo(MODO_MONITOR);                          // Dos PRESETS volta ao MONITOR
  pedirBipes(1);                                          // Bipe de confirmação
}                                                         // Fim de proximoModo()

void aplicarPreset(uint8_t p) {                           // Aplica e salva um preset
  for (uint8_t g = 0; g < TOTAL_POSICOES; g++) {          // Para cada posição
    bool central = (g < POSICOES_SALA1);                  // É da Sala 1?
    uint8_t local = indiceLocal(g);                       // Posição dentro da sala (0 = primeira)
    if (p == PRESET_100_ATIVO) habilitada[g] = true;      // 100%: todas
    if (p == PRESET_TIPICO_35) habilitada[g] = central || local < 7;   // S1 inteira + 7 por remota
    if (p == PRESET_PLANTAO_20) habilitada[g] = central ? (local < 8) : (local < 4);  // 8 + 4 por remota
  }                                                       // Fim do laço
  if (p == PRESET_ULTIMA) lerMascara(EE_END_PERSONALIZADA);  // Recupera a última configuração do SETUP
  for (uint8_t g = 0; g < TOTAL_POSICOES; g++) {          // Para cada posição
    if (!habilitada[g]) livre[g] = false;                 // Desabilitada volta a "ocupada"
  }                                                       // Fim do laço
  gravarMascara(EE_END_MASCARA);                          // Salva na EEPROM
  ledsSujos = true;                                       // Redesenha o painel
  mensagemAtiva = true;                                   // Mostra "APLICADO E SALVO"
  tMensagem = millis();                                   // Marca o início da mensagem
  pedirBipes(1);                                          // Bipe de confirmação
}                                                         // Fim de aplicarPreset()

void alternarHabilitacao() {                              // HAB no SETUP: liga/desliga a posição
  uint8_t g = cursorSetup;                                // Posição mostrada no LCD
  habilitada[g] = !habilitada[g];                         // Inverte habilitada/desabilitada
  if (!habilitada[g]) livre[g] = false;                   // Desabilitou: volta a "ocupada"
  gravarMascara(EE_END_MASCARA);                          // Salva a máscara atual
  gravarMascara(EE_END_PERSONALIZADA);                    // E guarda como "última configuração"
  ledsSujos = true;                                       // Redesenha o painel
}                                                         // Fim de alternarHabilitacao()

void acaoNav() {                                          // Toque curto em NAV
  if (modo == MODO_MONITOR) entrarModo(MODO_SETUP);       // No MONITOR: entra no SETUP
  else if (modo == MODO_SETUP) cursorSetup = (cursorSetup + 1) % TOTAL_POSICOES;  // Próxima posição
  else presetEscolhido = (presetEscolhido + 1) % NUM_PRESETS;   // Próximo preset
  mensagemAtiva = false;                                  // Some com mensagem antiga
}                                                         // Fim de acaoNav()

void acaoHab() {                                          // Toque curto em HAB
  if (modo == MODO_SETUP) alternarHabilitacao();          // No SETUP: habilita/desabilita
  if (modo == MODO_PRESETS) aplicarPreset(presetEscolhido);  // Nos PRESETS: aplica e salva
}                                                         // Fim de acaoHab() (no MONITOR não faz nada)

void tratarCombo(uint32_t agora) {                        // NAV + HAB juntos por 1 s
  if (!(botaoNav.pressionado && botaoHab.pressionado)) return;  // Os dois não estão apertados
  if (!comboEmCurso) {                                    // Acabaram de ficar juntos?
    comboEmCurso = true;                                  // Marca o combo (cancela ações simples)
    tInicioCombo = agora;                                 // Começa a contar 1 s
    return;                                               // Espera o tempo
  }                                                       // Fim do início do combo
  if (comboDisparado || (agora - tInicioCombo) < COMBO_MS) return;  // Já trocou ou falta tempo
  comboDisparado = true;                                  // Só uma troca por combo
  proximoModo();                                          // Troca o modo (com bipe)
}                                                         // Fim de tratarCombo()

void tratarRepeticaoNav(uint32_t agora) {                 // Segurar NAV no SETUP = avanço rápido
  if (modo != MODO_SETUP || !botaoNav.pressionado) return;  // Só no SETUP com NAV apertado
  if (botaoHab.pressionado || comboEmCurso) return;       // Com HAB junto é combo, não repetição
  if (!navRepetiu && (agora - tNavApertado) < REPETE_ATRASO_MS) return;  // Ainda não segurou 0,6 s
  if (navRepetiu && (agora - tUltimaRepeticao) < REPETE_PASSO_MS) return;  // Espera o passo de 150 ms
  navRepetiu = true;                                      // Marca que já repetiu (soltar não avança de novo)
  tUltimaRepeticao = agora;                               // Marca o avanço
  tUltimaTecla = agora;                                   // Segurar conta como uso (não volta ao MONITOR)
  acaoNav();                                              // Avança uma posição
}                                                         // Fim de tratarRepeticaoNav()

void tratarIhm(uint32_t agora) {                          // Lê NAV/HAB e decide o que fazer
  bool navMudou = atualizarBotao(botaoNav, agora);        // Anti-repique do NAV
  bool habMudou = atualizarBotao(botaoHab, agora);        // Anti-repique do HAB
  if (navMudou || habMudou) tUltimaTecla = agora;         // Qualquer toque reinicia os 60 s
  if (navMudou && botaoNav.pressionado) {                 // NAV acabou de ser apertado
    tNavApertado = agora;                                 // Marca para a repetição
    navRepetiu = false;                                   // Ainda não repetiu
  }                                                       // Fim do aperto do NAV
  tratarCombo(agora);                                     // Verifica NAV+HAB juntos
  if (navMudou && !botaoNav.pressionado && !comboEmCurso && !navRepetiu) acaoNav();  // Soltou NAV: ação
  if (habMudou && !botaoHab.pressionado && !comboEmCurso) acaoHab();   // Soltou HAB: ação
  tratarRepeticaoNav(agora);                              // Avanço rápido do NAV
  if (!botaoNav.pressionado && !botaoHab.pressionado) {   // Os dois soltos?
    comboEmCurso = false;                                 // Encerra o combo
    comboDisparado = false;                               // Libera para o próximo combo
  }                                                       // Fim da liberação
  if (modo != MODO_MONITOR && (agora - tUltimaTecla) >= INATIVIDADE_MS) entrarModo(MODO_MONITOR);  // 60 s parado
}                                                         // Fim de tratarIhm()

// ============================================================================
// LCD 20x2
// ============================================================================
void escreverLinha(uint8_t linha, const char *texto) {    // Escreve uma linha só se mudou
  char buf[21];                                           // 20 caracteres + terminador
  snprintf(buf, sizeof(buf), "%-20s", texto);             // Completa com espaços até 20 colunas
  if (strcmp(buf, lcdTela[linha]) == 0) return;           // Igual ao que já está na tela: não mexe
  strcpy(lcdTela[linha], buf);                            // Lembra o novo conteúdo
  lcd.setCursor(0, linha);                                // Vai para o começo da linha
  lcd.print(buf);                                         // Escreve no LCD
}                                                         // Fim de escreverLinha()

void montarListaFalhas(char *buf, uint8_t tamanho) {      // Monta "REDE: FALHA S2 S3 S4"
  strncpy(buf, "REDE: FALHA", tamanho);                   // Começo do texto
  buf[tamanho - 1] = '\0';                                // Garante o fim do texto
  for (uint8_t r = 0; r < NUM_REMOTAS; r++) {             // Para cada sala remota
    if (salaOnline[r]) continue;                          // Respondendo: não lista
    char sala[4];                                         // Espaço para " S3"
    snprintf(sala, sizeof(sala), " S%u", (unsigned)(r + PRIMEIRO_ID_REMOTO));  // Ex.: " S3"
    strncat(buf, sala, tamanho - strlen(buf) - 1);        // Acrescenta sem estourar o espaço
  }                                                       // Fim do laço
}                                                         // Fim de montarListaFalhas()

void telaMonitor(uint32_t agora) {                        // Tela de resumo
  uint8_t ocup = 0, livres = 0, desab = 0;                // Contadores
  for (uint8_t g = 0; g < TOTAL_POSICOES; g++) {          // Conta cada posição
    if (!habilitada[g]) desab++;                          // Desabilitada
    else if (livre[g]) livres++;                          // Livre
    else ocup++;                                          // Ocupada
  }                                                       // Fim da contagem
  char l1[21], l2[21];                                    // Textos das duas linhas
  snprintf(l1, sizeof(l1), "OCUP:%02u LIVRE:%02u", (unsigned)ocup, (unsigned)livres);  // Linha 1
  bool falha = haSalaOffline();                           // Alguma sala sem rede?
  if (falha && ((agora / LCD_ALTERNA_MS) % 2) == 1) {     // Em falha, a cada 2 s mostra quais salas
    montarListaFalhas(l2, sizeof(l2));                    // Ex.: "REDE: FALHA S3"
  } else {                                                // Senão, mostra o resumo
    snprintf(l2, sizeof(l2), "DESAB:%02u REDE:%s", (unsigned)desab, falha ? "FALHA" : "OK");  // Linha 2
  }                                                       // Fim da escolha da linha 2
  escreverLinha(0, l1);                                   // Escreve a linha 1
  escreverLinha(1, l2);                                   // Escreve a linha 2
}                                                         // Fim de telaMonitor()

void telaSetup() {                                        // Tela de habilitação posição a posição
  uint8_t g = cursorSetup;                                // Posição mostrada
  char l1[21];                                            // Texto da linha 1
  snprintf(l1, sizeof(l1), "S%u P%02u [%s]", (unsigned)salaDaPosicao(g), (unsigned)(g + 1),  // Ex.: "S2 P18"
           habilitada[g] ? "HABILITADA" : "DESABILIT.");  // Estado (abreviado para caber em 20)
  escreverLinha(0, l1);                                   // Escreve a linha 1
  escreverLinha(1, "NAV:prox HAB:muda");                  // Ajuda na linha 2
}                                                         // Fim de telaSetup()

void telaPresets(uint32_t agora) {                        // Tela de presets
  char l1[21];                                            // Texto da linha 1
  snprintf(l1, sizeof(l1), "PRESET: %s", NOMES_PRESETS[presetEscolhido]);  // Ex.: "PRESET: TIPICO 35"
  escreverLinha(0, l1);                                   // Escreve a linha 1
  if (mensagemAtiva && (agora - tMensagem) >= MENSAGEM_MS) mensagemAtiva = false;  // Mensagem expirou
  escreverLinha(1, mensagemAtiva ? "APLICADO E SALVO" : "NAV:gira HAB:aplica");  // Linha 2
}                                                         // Fim de telaPresets()

void atualizarLcd(uint32_t agora) {                       // Redesenha o LCD de tempos em tempos
  if (agora - tLcd < LCD_ATUALIZA_MS) return;             // Ainda não é hora
  tLcd = agora;                                           // Marca a atualização
  if (modo == MODO_MONITOR) telaMonitor(agora);           // Tela do MONITOR
  else if (modo == MODO_SETUP) telaSetup();               // Tela do SETUP
  else telaPresets(agora);                                // Tela dos PRESETS
}                                                         // Fim de atualizarLcd()

// ============================================================================
// DIAGNÓSTICO PELA USB (Monitor Serial a 115200 bps)
// ============================================================================
void imprimirEstatisticas(uint32_t agora) {               // Relatório a cada 10 s
#if DEPURACAO                                             // Só se o diagnóstico estiver ligado
  if (agora - tEstatistica < ESTATISTICA_MS) return;      // Ainda não é hora
  tEstatistica = agora;                                   // Marca o relatório
  for (uint8_t r = 0; r < NUM_REMOTAS; r++) {             // Uma linha por sala
    Serial.print(F("S"));                                 // Prefixo
    Serial.print(r + PRIMEIRO_ID_REMOTO);                 // Número da sala
    Serial.print(F(" pedidos=")); Serial.print(contPedidos[r]);       // Pedidos enviados
    Serial.print(F(" ok=")); Serial.print(contOk[r]);                 // Respostas válidas
    Serial.print(F(" sem_resp=")); Serial.print(contSemResposta[r]);  // Silêncios
    Serial.print(F(" invalidas=")); Serial.print(contInvalidas[r]);   // Erros de CRC/ID/SEQ
    Serial.println(salaOnline[r] ? F(" ONLINE") : F(" OFFLINE"));     // Situação atual
  }                                                       // Fim do laço
#else                                                     // Diagnóstico desligado
  (void)agora;                                            // Evita aviso de variável não usada
#endif                                                    // Fim do bloco de diagnóstico
}                                                         // Fim de imprimirEstatisticas()

// ============================================================================
// SETUP: roda uma vez ao ligar
// ============================================================================
void configurarPinos() {                                  // Configura entradas e saídas
  pinMode(PINO_RS485_DIR, OUTPUT);                        // Pino de direção do MAX485 é saída
  digitalWrite(PINO_RS485_DIR, LOW);                      // Começa ouvindo (nunca prende o barramento)
  pinMode(PINO_RX1, INPUT_PULLUP);                        // Pull-up no RX1: evita lixo quando o RO fica solto
  pinMode(PINO_BUZZER, OUTPUT);                           // Buzzer é saída
  digitalWrite(PINO_BUZZER, LOW);                         // Buzzer desligado
  pinMode(PINO_LED_PLACA, OUTPUT);                        // LED D13 é saída
  digitalWrite(PINO_LED_PLACA, LOW);                      // LED D13 apagado
  pinMode(PINO_NAV, INPUT_PULLUP);                        // NAV com resistor interno para 5 V
  pinMode(PINO_HAB, INPUT_PULLUP);                        // HAB com resistor interno para 5 V
  for (uint8_t i = 0; i < POSICOES_SALA1; i++) {          // Para cada botão P01 a P14
    botoesS1[i] = {PINOS_BOTOES_S1[i], false, false, 0};  // Prepara a estrutura do botão
    pinMode(PINOS_BOTOES_S1[i], INPUT_PULLUP);            // Resistor interno para 5 V
  }                                                       // Fim do laço
}                                                         // Fim de configurarPinos()

void setup() {                                            // Início do programa
  configurarPinos();                                      // Pinos primeiro (MAX485 em recepção)
#if DEPURACAO                                             // Só se o diagnóstico estiver ligado
  Serial.begin(115200);                                   // USB para o Monitor Serial
  Serial.println(F("Central Sala 1 - protocolo RS-485 v2"));  // Mensagem de partida
#endif                                                    // Fim do bloco de diagnóstico
  carregarConfiguracao();                                 // Restaura a máscara da EEPROM
  for (uint8_t g = 0; g < TOTAL_POSICOES; g++) livre[g] = false;  // Tudo começa "ocupado" (verde)
  fita.begin();                                           // Prepara o pino dos LEDs
  fita.setBrightness(BRILHO_LEDS);                        // Brilho de 40%
  fita.clear();                                           // Apaga todos
  fita.show();                                            // Envia "apagado"
  lcd.init();                                             // Inicia o LCD (Frank de Brabander)
  lcd.backlight();                                        // Liga a luz de fundo
  lcd.clear();                                            // Limpa a tela
  lcdTela[0][0] = '\0';                                   // Memória da linha 1 vazia
  lcdTela[1][0] = '\0';                                   // Memória da linha 2 vazia
  Serial1.begin(RS485_BAUD);                              // Serial1 do RS-485: 9600 8N1
  uint32_t agora = millis();                              // Hora atual
  for (uint8_t r = 0; r < NUM_REMOTAS; r++) {             // Para cada sala remota
    salaOnline[r] = true;                                 // Considera online até provar o contrário
    tUltimaResposta[r] = agora;                           // Dá 2 s para a primeira resposta
  }                                                       // Fim do laço
  tUltimaTecla = agora;                                   // Começa a contar a inatividade
  tUltimoPedido = agora;                                  // Primeiro pedido em 100 ms
  ledsSujos = true;                                       // Desenha o painel na primeira volta
}                                                         // Fim de setup()

// ============================================================================
// LOOP: roda sem parar (nada de delay())
// ============================================================================
void loop() {                                             // Laço principal
  uint32_t agora = millis();                              // Hora atual
  lerBotoesSala1(agora);                                  // Botões P01 a P14
  tratarIhm(agora);                                       // Botões NAV e HAB
  if (agora - tUltimoPedido >= INTERVALO_PEDIDO_MS) {     // Passaram 100 ms?
    tUltimoPedido = agora;                                // Marca o pedido
    consultarProximaRemota();                             // Pergunta e espera a resposta (até 25 ms)
  }                                                       // Fim do pedido
  agora = millis();                                       // Hora nova: nenhuma marca de tempo fica "no futuro"
  verificarSalasOffline(agora);                           // Sala sem resposta há 2 s?
  atualizarAlarme(agora);                                 // Bipes de falha
  atualizarBuzzer(agora);                                 // Liga/desliga o buzzer
  atualizarLeds(agora);                                   // show() só aqui, nunca durante a espera
  atualizarLedPlaca(agora);                               // Apaga o LED D13
  atualizarLcd(agora);                                    // Atualiza o LCD
  imprimirEstatisticas(agora);                            // Diagnóstico pela USB
}                                                         // Fim de loop()

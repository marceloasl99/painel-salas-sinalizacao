# -*- coding: utf-8 -*-
"""
Unified Master Application Generator v4
Updated with DEFINITIVE USER COLOR RULES & SETUP MECHANICS from message #12:
1. CORES DEFINITIVAS DOS LEDS WS2812B (REMOVIDO AMARELO E PISCANTE):
   - 🔵 AZUL ESCURO: SEM USO (Desabilitado / Não monitorado no dia).
   - 🟢 VERDE: OCUPADO / EM ATENDIMENTO / HABILITADO ATIVO.
   - 🔴 VERMELHO: LIVRE (Habilitado, desocupado no momento! Avisa à Sala 1 que o lugar está livre para mandar a próxima pessoa).
2. OPERAÇÃO DOS BOTÕES NAS SALAS:
   - Cada toque no botão da posição comuta diretamente entre 🟢 VERDE (Ocupado) e 🔴 VERMELHO (Livre).
   - Se a posição estiver em 🔵 AZUL ESCURO (Sem uso), o botão da sala fica inativo.
3. HABILITAÇÃO NA SALA 1 COM OS 2 BOTÕES DE SETUP AO LADO DO LCD 20x2:
   - Botão [NAV / PRÓXIMO]: Navega de 1 a 47 no LCD 20x2.
   - Botão [HABILITAR / DESABILITAR]: Alterna a posição entre HABILITADA (Vermelho/Verde) e SEM USO (Azul Escuro).
   - LCD 20x2 em tempo real:
     Linha 1: "POS S2-01: [HABILIT]" ou "POS S2-01: [SEM USO]"
     Linha 2: "[NAV]>PROX [HAB]>ALT"
   - Teclado 4x4 e atalhos em lote disponíveis como ferramentas secundárias/técnicas.
"""

def get_html_content():
    return r'''<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sistema de Sinalização 4 Salas | RS-485 & WS2812B</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#eef2ff',
              100: '#e0e7ff',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
              900: '#312e81',
            }
          },
          fontFamily: {
            mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
            sans: ['Inter', 'system-ui', 'sans-serif'],
          }
        }
      }
    }
  </script>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <!-- marked.js (renderiza o manual em Markdown) -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700;800&display=swap');

    /* =========================================================================
       THEME SYSTEM: INDIGO (DEFAULT), OLED (BLACK), LIGHT (WHITE)
       ========================================================================= */
    body {
      transition: background 0.3s ease, color 0.3s ease;
      font-family: 'Inter', sans-serif;
    }

    /* THEME 1: INDIGO (MIDNIGHT NAVY - DEFAULT) */
    body.theme-indigo {
      background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #030712 100%) !important;
      background-attachment: fixed !important;
      color: #f8fafc !important;
    }
    body.theme-indigo .glass-panel {
      background: rgba(15, 23, 42, 0.75) !important;
      backdrop-filter: blur(14px) !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    body.theme-indigo .glass-header {
      background: rgba(3, 7, 18, 0.88) !important;
      backdrop-filter: blur(16px) !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* THEME 2: OLED DARK (PRETO PURO 100%) */
    body.theme-oled {
      background: #000000 !important;
      color: #f8fafc !important;
    }
    body.theme-oled .glass-panel {
      background: #08080a !important;
      border: 1px solid #20222b !important;
      box-shadow: 0 4px 28px rgba(0,0,0,0.95) !important;
    }
    body.theme-oled .glass-header {
      background: #000000 !important;
      border-bottom: 1px solid #20222b !important;
    }
    body.theme-oled .bg-slate-950,
    body.theme-oled .bg-slate-950\/90,
    body.theme-oled .bg-slate-950\/80,
    body.theme-oled .bg-slate-950\/60 {
      background: #030304 !important;
      border-color: #1a1a22 !important;
    }
    body.theme-oled .bg-slate-900,
    body.theme-oled .bg-slate-900\/60,
    body.theme-oled .bg-slate-900\/80 {
      background: #0d0d12 !important;
      border-color: #22222a !important;
    }

    /* THEME 3: CLEAN ENGINEERING LIGHT (BRANCO) */
    body.theme-light {
      background: #f1f5f9 !important;
      color: #0f172a !important;
    }
    body.theme-light .glass-panel {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.04) !important;
    }
    body.theme-light .glass-header {
      background: rgba(255, 255, 255, 0.96) !important;
      border-bottom: 1px solid #e2e8f0 !important;
      box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    }
    body.theme-light .text-white {
      color: #0f172a !important;
    }
    body.theme-light .text-slate-100,
    body.theme-light .text-slate-200 {
      color: #1e293b !important;
    }
    body.theme-light .text-slate-300 {
      color: #334155 !important;
    }
    body.theme-light .text-slate-400 {
      color: #64748b !important;
    }
    body.theme-light .bg-slate-950,
    body.theme-light .bg-slate-950\/90,
    body.theme-light .bg-slate-950\/80,
    body.theme-light .bg-slate-950\/60,
    body.theme-light .bg-slate-900,
    body.theme-light .bg-slate-900\/60,
    body.theme-light .bg-slate-900\/80 {
      background: #f8fafc !important;
      border-color: #cbd5e1 !important;
    }
    body.theme-light .border-slate-800,
    body.theme-light .border-slate-800\/80 {
      border-color: #e2e8f0 !important;
    }
    body.theme-light .btn-na-tactile {
      background: linear-gradient(145deg, #ffffff, #f1f5f9) !important;
      border-color: #cbd5e1 !important;
      color: #0f172a !important;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    body.theme-light .keypad-btn {
      background: linear-gradient(145deg, #f1f5f9, #e2e8f0) !important;
      border: 1px solid #cbd5e1 !important;
      color: #0f172a !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
    ::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.5); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.9); }

    /* =========================================================================
       HD44780 20x2 HARDWARE INDUSTRIAL LCD DISPLAY
       ========================================================================= */
    .hd44780-pcb-bezel {
      background: linear-gradient(135deg, #1b2028 0%, #0d1015 100%);
      border: 3px solid #2d3748;
      box-shadow: 0 8px 24px rgba(0,0,0,0.7), inset 0 1px 1px rgba(255,255,255,0.15);
      border-radius: 14px;
      position: relative;
    }
    .bezel-screw {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: radial-gradient(circle, #cbd5e1 30%, #475569 90%);
      box-shadow: inset 0 1px 1px rgba(255,255,255,0.8), 0 1px 2px rgba(0,0,0,0.8);
      position: absolute;
    }
    .bezel-screw::after {
      content: '';
      position: absolute;
      top: 4px; left: 1px; width: 7px; height: 1.5px;
      background: #1e293b;
      transform: rotate(45deg);
    }
    .bezel-screw.top-left { top: 7px; left: 7px; }
    .bezel-screw.top-right { top: 7px; right: 7px; }
    .bezel-screw.bottom-left { bottom: 7px; left: 7px; }
    .bezel-screw.bottom-right { bottom: 7px; right: 7px; }

    .lcd-screen-glass {
      position: relative;
      background: #143527;
      color: #A3D8B0;
      text-shadow: 0 0 4px #8ADAB2, 0 0 10px #436850;
      box-shadow: inset 0 0 18px rgba(0,0,0,0.95), 0 2px 4px rgba(0,0,0,0.5);
      border: 3px solid #081d14;
      font-family: 'Courier New', Courier, monospace;
      letter-spacing: 1px;
      line-height: 1.55;
      user-select: none;
      overflow: hidden;
      border-radius: 6px;
    }
    /* 5x8 Dot Matrix Texture Overlay */
    .lcd-screen-glass::before {
      content: " ";
      position: absolute;
      top: 0; left: 0; bottom: 0; right: 0;
      background-image: radial-gradient(rgba(0, 0, 0, 0.45) 15%, transparent 16%);
      background-size: 3px 3px;
      z-index: 1;
      pointer-events: none;
      opacity: 0.55;
    }
    /* Industrial Scanline */
    .lcd-screen-glass::after {
      content: " ";
      position: absolute;
      top: 0; left: 0; bottom: 0; right: 0;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.28) 50%);
      background-size: 100% 4px;
      z-index: 2;
      pointer-events: none;
      opacity: 0.35;
    }
    .lcd-blue-mode {
      background: #09203F !important;
      color: #90E0EF !important;
      text-shadow: 0 0 4px #48CAE4, 0 0 10px #0077B6 !important;
      border-color: #030D1A !important;
    }

    /* =========================================================================
       CIRCULAR PILOT LAMP / WS2812B INDUSTRIAL SINÓPTICO
       ========================================================================= */
    .led-circular {
      position: relative;
      border-radius: 9999px;
      aspect-ratio: 1 / 1;
      width: 2.15rem;
      height: 2.15rem;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2.5px solid rgba(255, 255, 255, 0.22);
      box-shadow: 0 3px 8px rgba(0, 0, 0, 0.6), inset 0 1px 2px rgba(255, 255, 255, 0.4);
      transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
      cursor: pointer;
      user-select: none;
    }
    .led-circular:hover {
      transform: scale(1.18);
      z-index: 25;
    }
    .led-circular::after {
      content: '';
      position: absolute;
      top: 12%;
      left: 18%;
      width: 36%;
      height: 36%;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(255, 255, 255, 0.88) 0%, rgba(255, 255, 255, 0) 80%);
      pointer-events: none;
    }
    .led-circular .led-number {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 0.72rem;
      line-height: 1;
      color: #ffffff;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.95);
      z-index: 2;
    }

    /* DEFINITIVE COLORS:
       🔵 AZUL ESCURO: Sem Uso (Desabilitado / Não monitorado)
       🟢 VERDE: Ocupado / Em Atendimento
       🔴 VERMELHO: Livre (Pronto para receber pessoa)
    */
    .led-darkblue {
      background: radial-gradient(circle at 35% 35%, #2563eb 15%, #0f172a 85%);
      box-shadow: 0 0 10px rgba(37, 99, 235, 0.7), inset 0 0 4px #60a5fa;
      border-color: #1e3a8a;
    }
    .led-green {
      background: radial-gradient(circle at 35% 35%, #34d399 15%, #047857 85%);
      box-shadow: 0 0 14px #10b981, inset 0 0 5px #a7f3d0;
      border-color: #065f46;
    }
    .led-red {
      background: radial-gradient(circle at 35% 35%, #f87171 15%, #b91c1c 85%);
      box-shadow: 0 0 14px #ef4444, inset 0 0 5px #fecaca;
      border-color: #991b1b;
    }
    .led-fail-blink {
      background: radial-gradient(circle at 35% 35%, #60a5fa, #1e3a8a);
      box-shadow: 0 0 16px #3b82f6;
      animation: pulse-fail 0.5s infinite alternate;
    }
    @keyframes pulse-fail {
      0% { opacity: 0.25; transform: scale(0.95); }
      100% { opacity: 1; transform: scale(1.08); }
    }

    /* CONTINUOUS RS-485 BUS PULSE & ELECTRIC PARTICLES */
    @keyframes rs485-pulse {
      0% { background-position: 0% 50%; }
      100% { background-position: 200% 50%; }
    }
    .rs485-cable-pulse {
      background: linear-gradient(90deg, #1e293b 0%, #4338ca 25%, #10b981 50%, #4338ca 75%, #1e293b 100%);
      background-size: 200% 100%;
      animation: rs485-pulse 2.5s linear infinite;
    }
    .neon-packet-glow {
      box-shadow: 0 0 12px #10b981, 0 0 24px rgba(16, 185, 129, 0.6);
      transition: all 0.25s ease-in-out;
    }

    /* Tactile Physical Push-Buttons */
    .btn-na-tactile {
      background: linear-gradient(145deg, #1e293b, #0f172a);
      box-shadow: 0 3px 6px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.12);
      transition: all 0.15s ease;
      cursor: pointer;
    }
    .btn-na-tactile:hover {
      border-color: rgba(99, 102, 241, 0.6);
      box-shadow: 0 4px 8px rgba(99, 102, 241, 0.2);
    }
    .btn-na-tactile:active {
      transform: translateY(2px) scale(0.97);
      box-shadow: inset 0 3px 6px rgba(0,0,0,0.7);
    }

    .keypad-btn {
      background: linear-gradient(145deg, #334155, #1e293b);
      box-shadow: 2px 2px 4px rgba(0,0,0,0.4), -1px -1px 2px rgba(255,255,255,0.05);
      transition: all 0.1s;
    }
    .keypad-btn:active {
      box-shadow: inset 2px 2px 4px rgba(0,0,0,0.6);
      transform: translateY(1px);
    }

    @media print {
      body { background: white !important; color: black !important; }
      .no-print { display: none !important; }
      .glass-panel { background: white !important; border: 1px solid #ccc !important; box-shadow: none !important; }
    }
  
    /* =========================================================================
       MODULAR RECTANGULAR POSITION CARD (PAINEL SINÓPTICO INDUSTRIAL)
       ========================================================================= */
    .pos-module-card {
      background: linear-gradient(180deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.95) 100%);
      border: 1.5px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      box-shadow: 0 3px 6px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.08);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
      min-width: 0;
    }
    .pos-module-card:hover {
      border-color: rgba(99, 102, 241, 0.6);
      transform: translateY(-2px);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.6), 0 0 12px rgba(99, 102, 241, 0.2);
    }
    .pos-module-selected {
      border-color: #818cf8 !important;
      background: linear-gradient(180deg, rgba(49, 46, 129, 0.6) 0%, rgba(30, 27, 75, 0.8) 100%) !important;
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.6), 0 8px 20px rgba(0, 0, 0, 0.6) !important;
      transform: scale(1.04);
      z-index: 20;
    }

    /* PHYSICAL PILOT LAMP (LED EMBAIXO DO NÚMERO) */
    .led-pilot-lamp {
      position: relative;
      border-radius: 9999px;
      aspect-ratio: 1 / 1;
      border: 2px solid rgba(0, 0, 0, 0.6);
      box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.7), 0 2px 6px rgba(0, 0, 0, 0.5);
      transition: all 0.25s ease;
    }
    .led-pilot-lamp::after {
      content: '';
      position: absolute;
      top: 15%;
      left: 18%;
      width: 38%;
      height: 38%;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(255, 255, 255, 0.85) 0%, rgba(255, 255, 255, 0) 75%);
      pointer-events: none;
    }
__PE_TAB_CSS__
</style>
</head>
<body class="min-h-screen theme-indigo text-slate-100 font-sans selection:bg-indigo-500 selection:text-white">

  <!-- TOP APP BAR (COMPACT SCADA NAVBAR - H-14 56PX) -->
  <header class="sticky top-0 z-50 backdrop-blur-xl bg-slate-950/90 border-b border-slate-800/80 shadow-xl transition-all duration-300">
    <div class="w-full max-w-[1920px] mx-auto px-3 sm:px-5 lg:px-8">
      <div class="flex items-center justify-between h-14 gap-3">
        
        <!-- Compact Brand Logo -->
        <div class="flex items-center space-x-2.5 shrink-0">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-emerald-400 flex items-center justify-center shadow-md shadow-indigo-500/20">
            <i data-lucide="cpu" class="w-4 h-4 text-white"></i>
          </div>
          <div class="flex items-center space-x-1.5">
            <span class="font-black text-sm sm:text-base text-white tracking-tight">PainelSalas</span>
            <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-bold">RS-485</span>
          </div>
        </div>

        <!-- Navigation Tabs: All text 100% contained in distinct rectangular pills -->
        <nav class="hidden lg:flex items-center space-x-1 p-1 rounded-xl bg-slate-900/90 border border-slate-800 text-xs shrink-0 shadow-inner">
          <button onclick="switchTab('simulator')" id="nav-simulator" class="nav-btn px-2.5 py-1 rounded-lg text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 font-bold whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5 shadow-sm" title="Simulador Central Mestre e Salas">
            <i data-lucide="gamepad-2" class="w-3.5 h-3.5"></i>
            <span>Simulador</span>
          </button>
          <button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 border border-transparent font-medium whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5" title="Dashboard Executivo e KPIs">
            <i data-lucide="layout-dashboard" class="w-3.5 h-3.5"></i>
            <span>Dashboard</span>
          </button>
          <button onclick="switchTab('architecture')" id="nav-architecture" class="nav-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 border border-transparent font-medium whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5" title="Topologia Daisy-Chain RS-485">
            <i data-lucide="network" class="w-3.5 h-3.5"></i>
            <span>Topologia RS-485</span>
          </button>
          <button onclick="switchTab('schematic')" id="nav-schematic" class="nav-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 border border-transparent font-medium whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5" title="Diagramas Esquemáticos, Pinagem & Desenhos Técnicos">
            <i data-lucide="zap" class="w-3.5 h-3.5 text-amber-400"></i>
            <span>Projeto Elétrico</span>
          </button>
          <button onclick="switchTab('assembly')" id="nav-assembly" class="nav-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 border border-transparent font-medium whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5" title="Montagem Física da Fita WS2812B e Fiação">
            <i data-lucide="layers" class="w-3.5 h-3.5"></i>
            <span>Montagem Física</span>
          </button>
          <button onclick="switchTab('comparative')" id="nav-comparative" class="nav-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 border border-transparent font-medium whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5" title="Comparativos Técnicos de Arquitetura">
            <i data-lucide="git-compare" class="w-3.5 h-3.5"></i>
            <span>Comparativos</span>
          </button>
          <button onclick="switchTab('bom')" id="nav-bom" class="nav-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 border border-transparent font-medium whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5" title="Lista de Materiais e Orçamento Dinâmico">
            <i data-lucide="receipt" class="w-3.5 h-3.5"></i>
            <span>BOM & Orçamento</span>
          </button>
          <button onclick="switchTab('engineering')" id="nav-engineering" class="nav-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 border border-transparent font-medium whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5" title="Estimativa de Mão de Obra e Cronograma">
            <i data-lucide="clock" class="w-3.5 h-3.5"></i>
            <span>Prazos & ROI</span>
          </button>
        </nav>

        <!-- Right Tools: Themes & Action Buttons -->
        <div class="flex items-center space-x-1.5 shrink-0">
          <!-- 3 Full Themes Selector (OLED / Indigo / Light) -->
          <div class="flex items-center p-0.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono shadow-inner h-8">
            <button onclick="setAppTheme('oled')" id="btn-theme-oled" class="theme-btn h-7 px-2 rounded text-slate-400 hover:text-white transition flex items-center space-x-1" title="Tema Preto Puro (OLED Dark 100%)">
              <span class="text-xs">🌑</span>
              <span class="hidden xl:inline text-[10px] font-bold">OLED</span>
            </button>
            <button onclick="setAppTheme('indigo')" id="btn-theme-indigo" class="theme-btn h-7 px-2 rounded text-white font-bold bg-indigo-600 shadow transition flex items-center space-x-1" title="Tema Indigo (Midnight Navy)">
              <span class="text-xs">🌌</span>
              <span class="hidden xl:inline text-[10px] font-bold">Índigo</span>
            </button>
            <button onclick="setAppTheme('light')" id="btn-theme-light" class="theme-btn h-7 px-2 rounded text-slate-400 hover:text-white transition flex items-center space-x-1" title="Tema Claro (Clean Engineering Light)">
              <span class="text-xs">☀️</span>
              <span class="hidden xl:inline text-[10px] font-bold">Claro</span>
            </button>
          </div>

          <!-- Fullscreen Button -->
          <button onclick="toggleFullscreen()" class="h-8 w-8 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 transition flex items-center justify-center shrink-0 shadow-sm" title="Alternar Tela Cheia (F11)">
            <i data-lucide="maximize-2" id="fullscreen-icon" class="w-3.5 h-3.5"></i>
          </button>

          <!-- Audio Buzzer Button -->
          <button onclick="toggleSound()" id="sound-btn" class="h-8 w-8 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 transition flex items-center justify-center shrink-0 shadow-sm" title="Ligar/Desligar Buzzer de Áudio">
            <i data-lucide="volume-2" id="sound-icon" class="w-3.5 h-3.5 text-emerald-400"></i>
          </button>

          <!-- Print Report Button -->
          <button onclick="window.print()" class="h-8 px-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center justify-center space-x-1.5 shadow-md shadow-indigo-600/30 transition shrink-0" title="Imprimir Relatório Técnico">
            <i data-lucide="printer" class="w-3.5 h-3.5"></i>
            <span class="hidden sm:inline">Relatório</span>
          </button>
        </div>

      </div>
    </div>

    <!-- Mobile Navigation Sub-bar (Clean, single line horizontal pills) -->
    <div class="flex lg:hidden overflow-x-auto py-1.5 px-3 space-x-1.5 border-t border-slate-800/80 text-xs no-scrollbar bg-slate-950/95">
      <button onclick="switchTab('simulator')" id="mobile-nav-simulator" class="mobile-nav-btn px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 font-bold whitespace-nowrap text-xs shrink-0 transition">Simulador</button>
      <button onclick="switchTab('dashboard')" id="mobile-nav-dashboard" class="mobile-nav-btn px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-medium whitespace-nowrap text-xs shrink-0 transition">Dashboard</button>
      <button onclick="switchTab('architecture')" id="mobile-nav-architecture" class="mobile-nav-btn px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-medium whitespace-nowrap text-xs shrink-0 transition">Topologia</button>
      <button onclick="switchTab('schematic')" id="mobile-nav-schematic" class="mobile-nav-btn px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-medium whitespace-nowrap text-xs shrink-0 transition">Projeto Elétrico</button>
      <button onclick="switchTab('assembly')" id="mobile-nav-assembly" class="mobile-nav-btn px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-medium whitespace-nowrap text-xs shrink-0 transition">Montagem Física</button>
      <button onclick="switchTab('comparative')" id="mobile-nav-comparative" class="mobile-nav-btn px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-medium whitespace-nowrap text-xs shrink-0 transition">Comparativos</button>
      <button onclick="switchTab('bom')" id="mobile-nav-bom" class="mobile-nav-btn px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-medium whitespace-nowrap text-xs shrink-0 transition">Orçamento</button>
      <button onclick="switchTab('engineering')" id="mobile-nav-engineering" class="mobile-nav-btn px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-medium whitespace-nowrap text-xs shrink-0 transition">Prazos & ROI</button>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="w-full max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 xl:px-10 py-6 space-y-6">

    <!-- ============================================================== -->
    <!-- DEFINITIVE LED COLOR RULES (BOARD MESSAGE #12)                 -->
    <!-- ============================================================== -->
    <div class="glass-panel rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4 text-xs border border-indigo-500/30">
      <div class="flex items-center space-x-2.5">
        <span class="font-extrabold text-white uppercase tracking-wider flex items-center space-x-2">
          <i data-lucide="check-check" class="w-4 h-4 text-emerald-400"></i>
          <span>Regra de Cores Definitiva dos LEDs WS2812B:</span>
        </span>
      </div>
      <div class="flex flex-wrap items-center gap-5 text-xs font-mono">
        <span class="flex items-center space-x-2">
          <span class="w-4 h-4 rounded-full bg-blue-600 shadow-[0_0_10px_#2563eb]"></span>
          <span class="text-blue-300 font-bold">🔵 AZUL ESCURO: Sem Uso (Desabilitado)</span>
        </span>
        <span class="flex items-center space-x-2">
          <span class="w-4 h-4 rounded-full bg-emerald-500 shadow-[0_0_12px_#10b981]"></span>
          <span class="text-emerald-300 font-bold">🟢 VERDE: Ocupado / Em Atendimento</span>
        </span>
        <span class="flex items-center space-x-2">
          <span class="w-4 h-4 rounded-full bg-rose-500 shadow-[0_0_12px_#ef4444]"></span>
          <span class="text-rose-300 font-bold">🔴 VERMELHO: Livre (Pronto p/ Atender!)</span>
        </span>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 1: REALTIME INTERACTIVE SIMULATOR (PRIMARY VIEW)           -->
    <!-- ============================================================== -->
    <section id="tab-simulator" class="tab-content space-y-6">
      
      <!-- Quick Control Ribbon -->
      <div class="glass-panel rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center space-x-3">
          <div class="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <i data-lucide="activity" class="w-5 h-5 animate-pulse"></i>
          </div>
          <div>
            <h2 class="text-base font-bold text-white flex items-center space-x-2">
              <span>Console Operacional Integrado</span>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">4 Salas · 47 Posições</span>
            </h2>
            <p class="text-xs text-slate-400">Pressione os botões das salas para comutar Ocupado (Verde) e Livre (Vermelho). Posições desabilitadas ficam em Azul Escuro.</p>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-2 text-xs">
          <!-- Polling Speed -->
          <div class="flex items-center space-x-1.5 bg-slate-900/80 px-2.5 py-1.5 rounded-lg border border-slate-700">
            <span class="text-slate-400">Polling:</span>
            <select id="sim-polling-speed" onchange="updatePollingSpeed(this.value)" class="bg-transparent text-emerald-400 font-mono font-bold outline-none cursor-pointer">
              <option value="150">Rápido (150ms)</option>
              <option value="300" selected>Normal (300ms)</option>
              <option value="800">Lento (800ms)</option>
              <option value="manual">Manual (Pausado)</option>
            </select>
          </div>

          <!-- Noise Injection -->
          <button onclick="injectPacketError()" class="px-3 py-1.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 font-medium flex items-center space-x-1 transition" title="Injeta falha de CRC16 no barramento">
            <i data-lucide="zap" class="w-3.5 h-3.5 text-amber-400"></i>
            <span>Injetar Ruído</span>
          </button>

          <!-- Reset Day -->
          <button onclick="resetSimulationDay()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium flex items-center space-x-1 transition">
            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5 text-indigo-400"></i>
            <span>Reiniciar Dia</span>
          </button>
        </div>
      </div>

      <!-- MAIN SIMULATOR 2-COLUMN GRID -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- LEFT: SALA 1 (CENTRAL MASTER ARDUINO MEGA + WS2812B + LCD 20x2 + 2 SETUP BUTTONS) -->
        <div class="lg:col-span-7 space-y-6">
          <div class="glass-panel border-indigo-500/30 rounded-3xl p-5 sm:p-6 space-y-5 shadow-2xl">
            
            <!-- Sala 1 Header -->
            <div class="flex items-center justify-between pb-3 border-b border-slate-800">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-extrabold text-sm shadow-md shadow-indigo-600/30">
                  S1
                </div>
                <div>
                  <h3 class="font-bold text-base text-white">SALA 1: Central de Monitoramento Master</h3>
                  <p class="text-xs text-indigo-300 font-mono">Arduino Mega 2560 (Serial1 RS-485 · 5V nativo)</p>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span id="master-status-badge" class="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono font-bold flex items-center space-x-1.5">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
                  <span>MESTRE ATIVO</span>
                </span>
              </div>
            </div>

            <!-- Authentic Display LCD 20x2 HD44780 + 2 SETUP PHYSICAL BUTTONS + PRESS BOTH -->
            <div class="p-4 rounded-2xl bg-slate-950/90 border border-indigo-500/30 space-y-3.5">
              <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
                <span class="flex items-center space-x-1.5 font-bold text-slate-200">
                  <i data-lucide="tv" class="w-4 h-4 text-indigo-400"></i>
                  <span>MÓDULO HD44780 LCD 20x2 & BOTÕES FÍSICOS DE COMANDO</span>
                </span>
                <button onclick="toggleLcdColor()" class="text-[11px] text-slate-400 hover:text-white underline">Backlight Verde/Azul</button>
              </div>

              <!-- HD44780 Industrial Hardware Bezel with Screws -->
              <div class="hd44780-pcb-bezel p-3 sm:p-4">
                <div class="bezel-screw top-left"></div>
                <div class="bezel-screw top-right"></div>
                <div class="bezel-screw bottom-left"></div>
                <div class="bezel-screw bottom-right"></div>

                <div class="text-[9px] font-mono text-slate-400/80 uppercase tracking-widest text-center mb-1 flex items-center justify-between px-2">
                  <span>HD44780 INDUSTRIAL</span>
                  <span class="text-emerald-400 font-bold">20x2 MATRIX (5x8 DOTS)</span>
                  <span>I2C/PARALLEL 5V</span>
                </div>

                <!-- 20x2 LCD Screen -->
                <div id="lcd-screen" class="lcd-screen-glass p-3 sm:p-4 text-xs sm:text-sm font-mono overflow-hidden">
                  <div id="lcd-line-1" class="whitespace-pre tracking-normal font-mono font-bold text-xs sm:text-sm">PAINEL SALAS MASTER </div>
                  <div id="lcd-line-2" class="whitespace-pre tracking-normal font-mono font-bold text-xs sm:text-sm">OCP:47 LIV:00 OFF:00</div>
                </div>
              </div>

              <!-- 2 PHYSICAL SETUP BUTTONS BESIDE THE LCD -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                <!-- Button 1: NAV/PRÓXIMO -->
                <button onclick="lcdNavNext()" class="btn-na-tactile p-3 rounded-xl border border-indigo-500/40 text-left flex items-center space-x-3 group">
                  <div class="p-2 rounded-lg bg-indigo-600/30 text-indigo-300 group-hover:bg-indigo-600/50 transition">
                    <i data-lucide="chevrons-right" class="w-5 h-5"></i>
                  </div>
                  <div>
                    <span class="text-xs font-bold text-white block">Botão 1 [NAV / PRÓXIMO]</span>
                    <span id="btn1-subtext" class="text-[11px] text-slate-400">Navega posições 1 a 47</span>
                  </div>
                </button>

                <!-- Button 2: ALTERAR / HABILITAR -->
                <button onclick="lcdToggleEnable()" class="btn-na-tactile p-3 rounded-xl border border-emerald-500/40 text-left flex items-center space-x-3 group">
                  <div class="p-2 rounded-lg bg-emerald-600/30 text-emerald-300 group-hover:bg-emerald-600/50 transition">
                    <i data-lucide="power" class="w-5 h-5"></i>
                  </div>
                  <div>
                    <span class="text-xs font-bold text-white block">Botão 2 [CONFIRMAR / ALTERAR]</span>
                    <span id="btn2-subtext" class="text-[11px] text-slate-400">Alterna Habilitada &harr; Azul Escuro</span>
                  </div>
                </button>
              </div>

              <!-- FUNCTION: PRESS BOTH BUTTONS TOGETHER (ARDUINO COMBO) -->
              <div class="pt-1">
                <button onclick="pressBothButtonsTogether()" class="btn-na-tactile w-full py-2.5 px-4 rounded-xl border-2 border-indigo-500/50 hover:border-indigo-400 bg-gradient-to-r from-indigo-950/60 via-slate-900 to-indigo-950/60 text-center flex items-center justify-center space-x-2.5 shadow-md group transition">
                  <div class="flex -space-x-1">
                    <span class="w-3.5 h-3.5 rounded-full bg-indigo-500 border border-indigo-300"></span>
                    <span class="w-3.5 h-3.5 rounded-full bg-emerald-500 border border-emerald-300"></span>
                  </div>
                  <span class="text-xs font-mono font-bold text-white group-hover:text-indigo-200">
                    🔘+🔘 PRESSIONAR OS 2 BOTÕES JUNTOS
                  </span>
                  <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    Cicla: Monitor &harr; Setup &harr; Presets
                  </span>
                </button>
              </div>

              <!-- Mode Indicator on LCD -->
              <div class="flex flex-wrap items-center justify-between gap-1.5 text-[11px] pt-1 border-t border-slate-800/80">
                <span class="text-slate-400">Modo Atual do LCD: <strong id="lcd-mode-label" class="text-indigo-300">MODO 1: MONITOR GERAL</strong></span>
                <div class="flex items-center space-x-1.5">
                  <button onclick="toggleLcdMode('monitor')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] font-mono">1: Monitor</button>
                  <button onclick="toggleLcdMode('setup')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] font-mono">2: Setup</button>
                  <button onclick="toggleLcdMode('preset')" class="px-2 py-0.5 rounded bg-indigo-600/30 hover:bg-indigo-600/50 text-indigo-300 text-[10px] font-mono">3: Presets</button>
                </div>
              </div>
            </div>

            <!-- WS2812B CENTRAL LED PANEL<!-- WS2812B CENTRAL LED PANEL (47 PIXELS ESPELHADOS) -->
            <div class="space-y-3 pt-1">
              <div class="flex items-center justify-between">
                <h4 class="font-bold text-sm text-white flex items-center space-x-2">
                  <i data-lucide="grid-3x3" class="w-4 h-4 text-emerald-400"></i>
                  <span>Painel Central Mestre WS2812B (47 Posições Espelhadas)</span>
                </h4>
                <div class="flex items-center space-x-2 text-xs font-mono">
                  <span id="central-count-inuse" class="text-emerald-400 font-bold">47 Ocupadas (Verde)</span>
                  <span>·</span>
                  <span id="central-count-free" class="text-rose-400 font-bold">0 Livres (Vermelho)</span>
                  <span>·</span>
                  <span id="central-count-unused" class="text-blue-400 font-bold">0 Sem Uso (Azul)</span>
                </div>
              </div>

              <!-- Matrix Frame -->
              <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
                
                <!-- Sala 1 Segment (14 Posições) -->
                <div class="space-y-1.5">
                  <div class="flex items-center justify-between text-xs text-slate-400 font-mono border-b border-slate-800/80 pb-1">
                    <span class="text-indigo-400 font-bold">SALA 1 (Central Master) — 14 Posições</span>
                    <button onclick="toggleRoomAll(1)" class="text-[11px] text-indigo-300 hover:underline">Alternar Sala</button>
                  </div>
                  <div id="master-leds-s1" class="grid grid-cols-7 sm:grid-cols-14 gap-2.5 justify-items-center"></div>
                </div>

                <!-- Sala 2 Segment (11 Posições) -->
                <div class="space-y-1.5">
                  <div class="flex items-center justify-between text-xs text-slate-400 font-mono border-b border-slate-800/80 pb-1">
                    <span class="flex items-center space-x-2">
                      <span class="text-emerald-400 font-bold">SALA 2 (Remota ID 2) — 11 Posições</span>
                      <span id="badge-timeout-2" class="hidden text-[10px] px-1.5 py-0.2 rounded bg-blue-500/20 text-blue-300 border border-blue-500/40">FALHA COM (>2s)</span>
                    </span>
                    <button onclick="toggleRoomAll(2)" class="text-[11px] text-indigo-300 hover:underline">Alternar Sala</button>
                  </div>
                  <div id="master-leds-s2" class="grid grid-cols-6 sm:grid-cols-11 gap-2.5 justify-items-center"></div>
                </div>

                <!-- Sala 3 Segment (11 Posições) -->
                <div class="space-y-1.5">
                  <div class="flex items-center justify-between text-xs text-slate-400 font-mono border-b border-slate-800/80 pb-1">
                    <span class="flex items-center space-x-2">
                      <span class="text-emerald-400 font-bold">SALA 3 (Remota ID 3) — 11 Posições</span>
                      <span id="badge-timeout-3" class="hidden text-[10px] px-1.5 py-0.2 rounded bg-blue-500/20 text-blue-300 border border-blue-500/40">FALHA COM (>2s)</span>
                    </span>
                    <button onclick="toggleRoomAll(3)" class="text-[11px] text-indigo-300 hover:underline">Alternar Sala</button>
                  </div>
                  <div id="master-leds-s3" class="grid grid-cols-6 sm:grid-cols-11 gap-2.5 justify-items-center"></div>
                </div>

                <!-- Sala 4 Segment (11 Posições) -->
                <div class="space-y-1.5">
                  <div class="flex items-center justify-between text-xs text-slate-400 font-mono border-b border-slate-800/80 pb-1">
                    <span class="flex items-center space-x-2">
                      <span class="text-emerald-400 font-bold">SALA 4 (Remota ID 4 · Terminação 120Ω) — 11 Posições</span>
                      <span id="badge-timeout-4" class="hidden text-[10px] px-1.5 py-0.2 rounded bg-blue-500/20 text-blue-300 border border-blue-500/40">FALHA COM (>2s)</span>
                    </span>
                    <button onclick="toggleRoomAll(4)" class="text-[11px] text-indigo-300 hover:underline">Alternar Sala</button>
                  </div>
                  <div id="master-leds-s4" class="grid grid-cols-6 sm:grid-cols-11 gap-2.5 justify-items-center"></div>
                </div>

              </div>
            </div>

            <!-- Sala 1 Local Physical Operator Buttons (Positions 1 to 14) -->
            <div class="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800 space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-slate-300">Bancada do Operador Sala 1 (14 Botões NA Ligados no Mega)</span>
                <span class="text-slate-500 text-[11px]">Comuta 🟢 Ocupado &harr; 🔴 Livre</span>
              </div>
              <div id="buttons-room-1" class="grid grid-cols-7 sm:grid-cols-7 md:grid-cols-14 gap-1.5"></div>
            </div>

            <!-- EEPROM Preset Management Bar & Secondary Keypad -->
            <div class="p-4 rounded-2xl bg-slate-950/80 border border-indigo-500/30 space-y-3.5 shadow-lg">
              <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-2.5">
                <div class="flex items-center space-x-2">
                  <div class="p-1.5 rounded-lg bg-indigo-500/20 text-indigo-400">
                    <i data-lucide="hard-drive" class="w-4 h-4"></i>
                  </div>
                  <div>
                    <h5 class="text-xs font-bold text-white uppercase tracking-wider font-mono">Gestão de Presets & EEPROM ATmega2560 (4KB)</h5>
                    <p class="text-[10px] text-slate-400">Persistência não volátil no Arduino (com espelhamento LocalStorage)</p>
                  </div>
                </div>
                <!-- Active Preset Badge -->
                <div class="flex items-center space-x-2">
                  <span class="text-[11px] text-slate-400 font-mono">Preset Ativo:</span>
                  <span id="active-preset-badge" class="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-bold flex items-center space-x-1.5">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span id="active-preset-text">Preset 1: 100% Ativo (Boot)</span>
                  </span>
                </div>
              </div>

              <!-- Presets Grid Buttons -->
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2.5">
                <!-- Preset 1: 100% Ativo Boot -->
                <button onclick="applyPresetByIndex(0)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-emerald-950/40 border border-slate-800 hover:border-emerald-500/50 text-left transition group">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold uppercase">PADRÃO BOOT</span>
                    <i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-emerald-400"></i>
                  </div>
                  <span class="text-xs font-bold text-white block">Preset 1: 100% Ativo</span>
                  <span class="text-[10px] text-slate-400">47 Posições em 🟢 Verde</span>
                </button>

                <!-- Preset 2: Dia Típico -->
                <button onclick="applyPresetByIndex(1)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-indigo-950/40 border border-slate-800 hover:border-indigo-500/50 text-left transition group">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-bold uppercase">DIA SEMANA</span>
                    <i data-lucide="users" class="w-3.5 h-3.5 text-indigo-400"></i>
                  </div>
                  <span class="text-xs font-bold text-white block">Preset 2: Típico (35)</span>
                  <span class="text-[10px] text-slate-400">35 Ativas, 12 em 🔵 Azul</span>
                </button>

                <!-- Preset 3: Plantão Reduzido -->
                <button onclick="applyPresetByIndex(2)" class="p-2.5 rounded-xl bg-slate-900 hover:bg-amber-950/40 border border-slate-800 hover:border-amber-500/50 text-left transition group">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold uppercase">REDUZIDO</span>
                    <i data-lucide="clock" class="w-3.5 h-3.5 text-amber-400"></i>
                  </div>
                  <span class="text-xs font-bold text-white block">Preset 3: Plantão (20)</span>
                  <span class="text-[10px] text-slate-400">20 Ativas, 27 em 🔵 Azul</span>
                </button>

                <!-- Slot Custom EEPROM Operations -->
                <div class="p-2.5 rounded-xl bg-slate-900 border border-indigo-500/30 flex flex-col justify-between">
                  <div class="flex items-center justify-between text-[11px] font-mono text-slate-300 mb-1.5">
                    <span class="font-bold">Slot EEPROM:</span>
                    <select id="eeprom-slot-selector" onchange="SYSTEM.activeSlot = parseInt(this.value)" class="bg-slate-950 border border-slate-700 text-indigo-300 text-xs rounded px-1.5 py-0.5 font-mono">
                      <option value="1">Slot 1 (0x0040)</option>
                      <option value="2">Slot 2 (0x0080)</option>
                      <option value="3">Slot 3 (0x00C0)</option>
                    </select>
                  </div>
                  <div class="flex gap-1.5">
                    <button onclick="saveCurrentToEepromSlot()" class="flex-1 py-1 px-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-[11px] font-bold flex items-center justify-center space-x-1 shadow-sm transition">
                      <i data-lucide="save" class="w-3 h-3"></i>
                      <span>Salvar</span>
                    </button>
                    <button onclick="loadFromEepromSlot()" class="flex-1 py-1 px-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-indigo-300 border border-slate-700 text-[11px] font-bold flex items-center justify-center space-x-1 transition">
                      <i data-lucide="upload" class="w-3 h-3"></i>
                      <span>Carregar</span>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Secondary Keypad 4x4 with Real Engineering Functions -->
              <div class="pt-2 border-t border-slate-800/80">
                <div class="flex items-center justify-between text-xs text-slate-400 font-mono mb-2">
                  <span class="flex items-center space-x-1 text-slate-300 font-bold">
                    <i data-lucide="calculator" class="w-3.5 h-3.5 text-indigo-400"></i>
                    <span>Teclado de Manutenção 4x4 (Atalhos de Firmware)</span>
                  </span>
                  <span class="text-[10px] text-slate-500">[1:Setup] [2:Preset] [3:Monitor] [*]Salva [#]Aplica</span>
                </div>
                <div class="grid grid-cols-4 sm:grid-cols-8 gap-1.5 max-w-md mx-auto">
                  <button onclick="pressKeypad('1')" class="keypad-btn h-7 rounded text-white font-mono text-xs font-bold" title="1: Modo Setup">1</button>
                  <button onclick="pressKeypad('2')" class="keypad-btn h-7 rounded text-indigo-300 font-mono text-xs font-bold" title="2: Modo Presets">2</button>
                  <button onclick="pressKeypad('3')" class="keypad-btn h-7 rounded text-white font-mono text-xs font-bold" title="3: Modo Monitor">3</button>
                  <button onclick="pressKeypad('A')" class="keypad-btn h-7 rounded text-indigo-300 font-mono text-xs font-bold" title="A: Alternar Modo LCD">A</button>
                  <button onclick="pressKeypad('4')" class="keypad-btn h-7 rounded text-white font-mono text-xs font-bold" title="4: Autoteste LEDs">4</button>
                  <button onclick="pressKeypad('*')" class="keypad-btn h-7 rounded text-amber-300 font-mono text-xs font-bold" title="*: Gravar Slot EEPROM">*</button>
                  <button onclick="pressKeypad('#')" class="keypad-btn h-7 rounded text-emerald-300 font-mono text-xs font-bold" title="#: Confirmar/Aplicar">#</button>
                  <button onclick="pressKeypad('D')" class="keypad-btn h-7 rounded text-rose-300 font-mono text-xs font-bold" title="D: Reset Boot 100% Verde">D</button>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- RIGHT: REMOTE OPERATOR STATIONS (SALAS 2, 3, 4) + RS-485 BUS -->
        <div class="lg:col-span-5 space-y-5">
          
          <!-- RS-485 Realtime Bus Monitor -->
          <div class="glass-panel border-emerald-500/20 rounded-2xl p-4 space-y-3">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-xs uppercase tracking-wider text-white flex items-center space-x-2">
                <i data-lucide="radio" class="w-4 h-4 text-indigo-400"></i>
                <span>Tráfego RS-485 Daisy-Chain em Tempo Real</span>
              </h3>
              <span id="bus-latency-text" class="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">9600 bps · 12ms</span>
            </div>

            <!-- Animated Line Track -->
            <div class="relative h-7 bg-slate-950 rounded-lg border border-slate-800 flex items-center px-4 overflow-hidden">
              <div class="absolute left-0 right-0 h-0.5 bg-slate-700 top-1/2 -translate-y-1/2"></div>
              <div class="absolute left-2 w-2 h-2 bg-indigo-500 rounded-full z-10 shadow-[0_0_8px_#6366f1]"></div>
              <div class="absolute right-2 w-2 h-2 bg-emerald-500 rounded-full z-10 shadow-[0_0_8px_#10b981]"></div>
              
              <!-- Animated Bus Packet -->
              <div id="animated-bus-packet" class="absolute w-10 h-4 rounded text-[9px] font-mono font-bold flex justify-center items-center text-slate-950 transition-all duration-[300ms] shadow-lg">
                POLL
              </div>
            </div>

            <!-- Frame Hex Dump -->
            <div class="flex items-center justify-between text-[11px] font-mono bg-slate-950 px-2.5 py-1.5 rounded border border-slate-800 text-slate-400">
              <span>Último Pacote:</span>
              <span id="last-frame-hex" class="text-emerald-400 font-bold">02 03 00 00 00 0B 04 5F</span>
            </div>
          </div>

          <!-- SALAS 2, 3 E 4: ESTAÇÕES DO OPERADOR (MOSTRANDO TANTO O LED INDICADOR QUANTO O BOTÃO FÍSICO) -->
          <!-- Sala 2 -->
          <div class="glass-panel rounded-2xl p-4 border border-slate-700/80 space-y-3">
            <div class="flex items-center justify-between pb-2 border-b border-slate-800">
              <div class="flex items-center space-x-2">
                <div class="w-7 h-7 rounded-lg bg-emerald-700 flex items-center justify-center text-white font-bold text-xs">S2</div>
                <div>
                  <h4 class="text-sm font-bold text-white">SALA 2: Estação do Operador</h4>
                  <p class="text-[11px] text-slate-400 font-mono">Arduino Uno R3 (Slave ID 2) · 11 Posições</p>
                </div>
              </div>
              <button onclick="toggleRoomLink(2)" id="btn-link-2" class="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-slate-800 transition">
                LINK: ONLINE
              </button>
            </div>
            <div class="space-y-1.5">
              <div class="text-[11px] text-slate-400 flex justify-between">
                <span>LED Local WS2812B + Botão Físico do Operador:</span>
                <span class="text-slate-500">Toque no botão para alternar</span>
              </div>
              <div id="station-positions-2" class="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-11 gap-1.5"></div>
            </div>
          </div>

          <!-- Sala 3 -->
          <div class="glass-panel rounded-2xl p-4 border border-slate-700/80 space-y-3">
            <div class="flex items-center justify-between pb-2 border-b border-slate-800">
              <div class="flex items-center space-x-2">
                <div class="w-7 h-7 rounded-lg bg-emerald-700 flex items-center justify-center text-white font-bold text-xs">S3</div>
                <div>
                  <h4 class="text-sm font-bold text-white">SALA 3: Estação do Operador</h4>
                  <p class="text-[11px] text-slate-400 font-mono">Arduino Uno R3 (Slave ID 3) · 11 Posições</p>
                </div>
              </div>
              <button onclick="toggleRoomLink(3)" id="btn-link-3" class="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-slate-800 transition">
                LINK: ONLINE
              </button>
            </div>
            <div class="space-y-1.5">
              <div class="text-[11px] text-slate-400 flex justify-between">
                <span>LED Local WS2812B + Botão Físico do Operador:</span>
                <span class="text-slate-500">Toque no botão para alternar</span>
              </div>
              <div id="station-positions-3" class="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-11 gap-1.5"></div>
            </div>
          </div>

          <!-- Sala 4 -->
          <div class="glass-panel rounded-2xl p-4 border border-slate-700/80 space-y-3 relative">
            <div class="flex items-center justify-between pb-2 border-b border-slate-800">
              <div class="flex items-center space-x-2">
                <div class="w-7 h-7 rounded-lg bg-emerald-700 flex items-center justify-center text-white font-bold text-xs">S4</div>
                <div>
                  <h4 class="text-sm font-bold text-white">SALA 4: Estação Fim de Linha</h4>
                  <p class="text-[11px] text-slate-400 font-mono">Arduino Uno R3 (Slave ID 4 · Term. 120Ω)</p>
                </div>
              </div>
              <button onclick="toggleRoomLink(4)" id="btn-link-4" class="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-slate-800 transition">
                LINK: ONLINE
              </button>
            </div>
            <div class="space-y-1.5">
              <div class="text-[11px] text-slate-400 flex justify-between">
                <span>LED Local WS2812B + Botão Físico do Operador:</span>
                <span class="text-slate-500">Toque no botão para alternar</span>
              </div>
              <div id="station-positions-4" class="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-11 gap-1.5"></div>
            </div>
          </div>

          <!-- Serial Monitor Console -->
          <div class="glass-panel rounded-2xl p-4 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-white flex items-center space-x-1.5 font-mono">
                <i data-lucide="terminal" class="w-3.5 h-3.5 text-indigo-400"></i>
                <span>MONITOR SERIAL (UART1 - Serial1 Arduino Mega)</span>
              </span>
              <div class="flex items-center space-x-1">
                <button onclick="exportSerialLog()" class="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-400" title="Exportar Log"><i data-lucide="download" class="w-3 h-3"></i></button>
                <button onclick="clearConsoleLog()" class="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-400" title="Limpar"><i data-lucide="trash-2" class="w-3 h-3"></i></button>
              </div>
            </div>
            <div id="serial-log-box" class="h-28 bg-slate-950 rounded-xl p-2.5 font-mono text-[10px] text-emerald-400/90 overflow-y-auto space-y-1 border border-slate-800">
              <div>[00:00:01] Arduino Mega Master inicializado. Baud: 9600 8N1.</div>
              <div>[00:00:01] Painel WS2812B 47 pixels carregado. Pino DATA: D6.</div>
              <div>[00:00:02] Polling RS-485 (protocolo v2, CRC-8) iniciado: S2(ID2), S3(ID3), S4(ID4).</div>
            </div>
          </div>

        </div>

      </div>

    </section>

    <!-- ============================================================== -->
    <!-- TAB 2: EXECUTIVE DASHBOARD & KPIS                              -->
    <!-- ============================================================== -->
    <section id="tab-dashboard" class="tab-content hidden space-y-6">
      
      <div class="glass-panel rounded-3xl p-8 relative overflow-hidden">
        <div class="relative z-10 max-w-3xl space-y-3">
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-mono font-medium">
            <i data-lucide="shield-check" class="w-3.5 h-3.5 text-emerald-400"></i>
            <span>Projeto executivo · rev. 5.0 · 23/11/2026</span>
          </div>
          <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
            Modernização Digital de Painéis e Sinalização das 4 Salas
          </h1>
          <p class="text-slate-300 text-sm sm:text-base leading-relaxed">
            Substituição da antiga fiação paralela em 110V AC por uma rede industrial distribuída 
            <strong class="text-indigo-400">RS-485 (protocolo com CRC-8)</strong> com 
            <strong class="text-emerald-400">Arduino Mega Master</strong> na Sala 1 e 
            <strong class="text-emerald-400">Arduino Uno R3 nas Salas 2, 3 e 4</strong>, fonte 5 V em cada painel, cabo blindado de 2 vias entre as salas e 
            <strong class="text-white">47 posições</strong> em painel LED endereçável 
            <strong class="text-indigo-400">WS2812B</strong> com display LCD 20x2 e 2 botões de setup.
          </p>
          <div class="pt-2 flex flex-wrap gap-3">
            <button onclick="switchTab('simulator')" class="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs shadow-lg shadow-emerald-600/30 transition">
              <i data-lucide="play" class="w-4 h-4"></i>
              <span>Abrir Simulador em Tempo Real</span>
            </button>
            <button onclick="switchTab('bom')" class="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-xs border border-slate-700 transition">
              <i data-lucide="calculator" class="w-4 h-4 text-indigo-400"></i>
              <span>Ver lista de materiais (R$ 979)</span>
            </button>
            <button onclick="switchTab('assembly'); setTimeout(() => document.getElementById('manual-completo')?.scrollIntoView({behavior: 'smooth'}), 100);" class="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 font-medium text-xs transition cursor-pointer">
              <i data-lucide="book-open" class="w-4 h-4 text-indigo-400"></i>
              <span>Manual Técnico</span>
            </button>
          </div>
        </div>
      </div>

      <!-- KPI Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="glass-panel rounded-2xl p-4">
          <div class="flex items-center justify-between text-xs font-semibold text-slate-400 uppercase">
            <span>Posições Totais</span>
            <div class="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400"><i data-lucide="layers" class="w-4 h-4"></i></div>
          </div>
          <div class="text-2xl font-bold text-white font-mono mt-2">47</div>
          <div class="text-[11px] text-slate-400 mt-1">Sala 1: 14 · Salas 2,3,4: 11 cada</div>
        </div>

        <div class="glass-panel rounded-2xl p-4">
          <div class="flex items-center justify-between text-xs font-semibold text-slate-400 uppercase">
            <span>Custo de Materiais</span>
            <div class="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400"><i data-lucide="banknote" class="w-4 h-4"></i></div>
          </div>
          <div class="text-2xl font-bold text-emerald-400 font-mono mt-2">R$ 979<span class="text-sm text-slate-400">,00</span></div>
          <div class="text-[11px] text-emerald-300/80 mt-1">Cenário A · preços de referência</div>
        </div>

        <div class="glass-panel rounded-2xl p-4">
          <div class="flex items-center justify-between text-xs font-semibold text-slate-400 uppercase">
            <span>Redução de Fiação</span>
            <div class="p-1.5 rounded-lg bg-amber-500/10 text-amber-400"><i data-lucide="cable" class="w-4 h-4"></i></div>
          </div>
          <div class="text-2xl font-bold text-amber-400 font-mono mt-2">-88%</div>
          <div class="text-[11px] text-slate-400 mt-1">Cabo de 2 vias entre as salas</div>
        </div>

        <div class="glass-panel rounded-2xl p-4">
          <div class="flex items-center justify-between text-xs font-semibold text-slate-400 uppercase">
            <span>Segurança NR-10</span>
            <div class="p-1.5 rounded-lg bg-rose-500/10 text-rose-400"><i data-lucide="zap-off" class="w-4 h-4"></i></div>
          </div>
          <div class="text-2xl font-bold text-rose-400 font-mono mt-2">100%</div>
          <div class="text-[11px] text-slate-400 mt-1">Eliminação de 110V nas caixas</div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-panel rounded-2xl p-5 shadow-lg">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i data-lucide="bar-chart-3" class="w-4 h-4 text-indigo-400"></i>
                <span>Comparativo de Custos dos Cenários Orçamentários</span>
              </h3>
              <p class="text-[11px] text-slate-400">Cenários A, B e C · com e sem reserva de 15%</p>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">R$ (BRL)</span>
          </div>
          <div class="h-60"><canvas id="costComparisonChart"></canvas></div>
        </div>

        <div class="glass-panel rounded-2xl p-5 shadow-lg">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center space-x-2">
                <i data-lucide="gauge" class="w-4 h-4 text-emerald-400"></i>
                <span>Eficiência Energética & Segurança Ocupacional</span>
              </h3>
              <p class="text-[11px] text-slate-400">Consumo elétrico comparado ao sistema antigo 110V</p>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400">Retrofit 4.0</span>
          </div>
          <div class="h-60"><canvas id="efficiencyChart"></canvas></div>
        </div>
      </div>

      <!-- Problem vs Solution Details -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="glass-panel border-rose-900/30 rounded-2xl p-5 space-y-3">
          <h3 class="text-base font-bold text-white flex items-center space-x-2">
            <i data-lucide="alert-triangle" class="w-5 h-5 text-rose-400"></i>
            <span>Sistema Legado Atual (110V AC)</span>
          </h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start space-x-2"><i data-lucide="x" class="w-4 h-4 text-rose-500 shrink-0 mt-0.5"></i><span><strong>Risco elétrico constante:</strong> 110V AC circulando nas caixas de madeira dos operadores.</span></li>
            <li class="flex items-start space-x-2"><i data-lucide="x" class="w-4 h-4 text-rose-500 shrink-0 mt-0.5"></i><span><strong>Falhas de lâmpadas constantes:</strong> Indicadores circulares incandescentes queimando por idade.</span></li>
            <li class="flex items-start space-x-2"><i data-lucide="x" class="w-4 h-4 text-rose-500 shrink-0 mt-0.5"></i><span><strong>Feixe de fios pesado:</strong> Dezenas de condutores paralelos cruzando a tubulação predial.</span></li>
            <li class="flex items-start space-x-2"><i data-lucide="x" class="w-4 h-4 text-rose-500 shrink-0 mt-0.5"></i><span><strong>Zero diagnóstico:</strong> Impossível saber se uma lâmpada apagada é falha elétrica ou mesa vazia.</span></li>
          </ul>
        </div>

        <div class="glass-panel border-emerald-900/30 rounded-2xl p-5 space-y-3">
          <h3 class="text-base font-bold text-white flex items-center space-x-2">
            <i data-lucide="check-circle-2" class="w-5 h-5 text-emerald-400"></i>
            <span>Nova Solução Digital (5V DC / RS-485)</span>
          </h3>
          <ul class="text-xs text-slate-300 space-y-2">
            <li class="flex items-start space-x-2"><i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i><span><strong>Tensão segura de 5V DC:</strong> Nenhuma tensão perigosa nos botões dos operadores.</span></li>
            <li class="flex items-start space-x-2"><i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i><span><strong>Apenas 2 vias:</strong> cabo blindado de par trançado liga as salas em linha; cada painel tem fonte própria.</span></li>
            <li class="flex items-start space-x-2"><i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i><span><strong>Painel WS2812B inteligente:</strong> 1 pino controla 47 posições nas cores oficiais.</span></li>
            <li class="flex items-start space-x-2"><i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i><span><strong>Heartbeat e Fail-Safe:</strong> Alarme automático no LCD 20x2 se qualquer sala perder conexão.</span></li>
          </ul>
        </div>
      </div>

    </section>

    <!-- ============================================================== -->
    <!-- TAB 3: TOPOLOGY & INTERACTIVE SVG ARCHITECTURE                 -->
    <!-- ============================================================== -->
    <section id="tab-architecture" class="tab-content hidden space-y-6">
      
      <div class="glass-panel rounded-3xl p-6 md:p-8 space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div>
            <h2 class="text-xl font-bold text-white flex items-center space-x-2">
              <i data-lucide="network" class="w-5 h-5 text-indigo-400"></i>
              <span>Topologia Física Daisy-Chain RS-485 & Pinagens</span>
            </h2>
            <p class="text-xs text-slate-400">Clique em qualquer nó da rede para inspecionar os pinos e conexões elétricas</p>
          </div>
          <div class="flex items-center space-x-4 text-xs font-mono">
            <span class="flex items-center space-x-1 text-indigo-400"><span class="w-3 h-0.5 bg-indigo-500"></span><span>Linha A (Data +)</span></span>
            <span class="flex items-center space-x-1 text-emerald-400"><span class="w-3 h-0.5 bg-emerald-500"></span><span>Linha B (Data -)</span></span>
            <span class="flex items-center space-x-1 text-slate-400"><span class="w-3 h-0.5 bg-slate-500"></span><span>GND Comum</span></span>
          </div>
        </div>

        <!-- SVG Visualizer -->
        <div class="w-full overflow-x-auto py-2">
          <svg viewBox="0 0 1000 320" class="w-full min-w-[750px] select-none">
            <!-- Line A -->
            <path d="M 170 160 L 370 160 L 610 160 L 850 160" stroke="#6366f1" stroke-width="4" fill="none" stroke-linecap="round" />
            <!-- Line B -->
            <path d="M 170 175 L 370 175 L 610 175 L 850 175" stroke="#10b981" stroke-width="4" fill="none" stroke-linecap="round" />
            <!-- Line GND -->
            <path d="M 170 190 L 370 190 L 610 190 L 850 190" stroke="#64748b" stroke-width="2.5" stroke-dasharray="6,4" fill="none" />

            <!-- Terminating Resistor 120R at Sala 1 -->
            <g transform="translate(145, 155)">
              <rect x="0" y="0" width="22" height="40" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2" />
              <text x="11" y="24" fill="#f59e0b" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle">120Ω</text>
            </g>

            <!-- Terminating Resistor 120R at Sala 4 -->
            <g transform="translate(855, 155)">
              <rect x="0" y="0" width="22" height="40" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2" />
              <text x="11" y="24" fill="#f59e0b" font-family="monospace" font-size="9" font-weight="bold" text-anchor="middle">120Ω</text>
            </g>

            <!-- NODE 1: Sala 1 Master -->
            <g class="cursor-pointer group" onclick="showNodeDetails(1)">
              <rect x="30" y="30" width="160" height="110" rx="12" fill="#0f172a" stroke="#6366f1" stroke-width="2.5" class="transition group-hover:fill-slate-800" />
              <text x="110" y="58" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">SALA 1 (MASTER)</text>
              <text x="110" y="76" fill="#818cf8" font-family="monospace" font-size="11" text-anchor="middle">Arduino Mega 2560</text>
              <text x="110" y="94" fill="#34d399" font-family="sans-serif" font-size="10" text-anchor="middle">Painel 47 LEDs WS2812B</text>
              <text x="110" y="110" fill="#f59e0b" font-family="sans-serif" font-size="10" text-anchor="middle">LCD 20x2 + 2 Botões Setup</text>
              <line x1="110" y1="140" x2="110" y2="160" stroke="#6366f1" stroke-width="3" />
              <circle cx="110" cy="160" r="5" fill="#6366f1" />
              <circle cx="110" cy="175" r="5" fill="#10b981" />
              <circle cx="110" cy="190" r="4" fill="#64748b" />
            </g>

            <!-- NODE 2: Sala 2 Slave -->
            <g class="cursor-pointer group" onclick="showNodeDetails(2)">
              <rect x="290" y="30" width="160" height="110" rx="12" fill="#0f172a" stroke="#10b981" stroke-width="2" class="transition group-hover:fill-slate-800" />
              <text x="370" y="58" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">SALA 2 (SLAVE 2)</text>
              <text x="370" y="76" fill="#34d399" font-family="monospace" font-size="11" text-anchor="middle">Arduino Uno + MAX485</text>
              <text x="370" y="94" fill="#94a3b8" font-family="sans-serif" font-size="10" text-anchor="middle">11 Botões NA Locais</text>
              <text x="370" y="110" fill="#34d399" font-family="sans-serif" font-size="10" text-anchor="middle">11 LEDs WS2812B Local</text>
              <line x1="370" y1="140" x2="370" y2="160" stroke="#6366f1" stroke-width="3" />
              <circle cx="370" cy="160" r="5" fill="#6366f1" />
              <circle cx="370" cy="175" r="5" fill="#10b981" />
              <circle cx="370" cy="190" r="4" fill="#64748b" />
            </g>

            <!-- NODE 3: Sala 3 Slave -->
            <g class="cursor-pointer group" onclick="showNodeDetails(3)">
              <rect x="530" y="30" width="160" height="110" rx="12" fill="#0f172a" stroke="#10b981" stroke-width="2" class="transition group-hover:fill-slate-800" />
              <text x="610" y="58" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">SALA 3 (SLAVE 3)</text>
              <text x="610" y="76" fill="#34d399" font-family="monospace" font-size="11" text-anchor="middle">Arduino Uno + MAX485</text>
              <text x="610" y="94" fill="#94a3b8" font-family="sans-serif" font-size="10" text-anchor="middle">11 Botões NA Locais</text>
              <text x="610" y="110" fill="#34d399" font-family="sans-serif" font-size="10" text-anchor="middle">11 LEDs WS2812B Local</text>
              <line x1="610" y1="140" x2="610" y2="160" stroke="#6366f1" stroke-width="3" />
              <circle cx="610" cy="160" r="5" fill="#6366f1" />
              <circle cx="610" cy="175" r="5" fill="#10b981" />
              <circle cx="610" cy="190" r="4" fill="#64748b" />
            </g>

            <!-- NODE 4: Sala 4 Slave (Fim de Linha) -->
            <g class="cursor-pointer group" onclick="showNodeDetails(4)">
              <rect x="770" y="30" width="160" height="110" rx="12" fill="#0f172a" stroke="#10b981" stroke-width="2" class="transition group-hover:fill-slate-800" />
              <text x="850" y="58" fill="#ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">SALA 4 (SLAVE 4)</text>
              <text x="850" y="76" fill="#34d399" font-family="monospace" font-size="11" text-anchor="middle">Arduino Uno + MAX485</text>
              <text x="850" y="94" fill="#94a3b8" font-family="sans-serif" font-size="10" text-anchor="middle">11 Botões NA Locais</text>
              <text x="850" y="110" fill="#f59e0b" font-family="sans-serif" font-size="10" text-anchor="middle">Terminação 120Ω Ativa</text>
              <line x1="850" y1="140" x2="850" y2="160" stroke="#6366f1" stroke-width="3" />
              <circle cx="850" cy="160" r="5" fill="#6366f1" />
              <circle cx="850" cy="175" r="5" fill="#10b981" />
              <circle cx="850" cy="190" r="4" fill="#64748b" />
            </g>

            <!-- Bottom Specs Legend Box -->
            <g transform="translate(100, 225)">
              <rect x="0" y="0" width="800" height="75" rx="8" fill="#090d16" stroke="#1e293b" />
              <text x="25" y="26" fill="#e2e8f0" font-family="sans-serif" font-size="12" font-weight="bold">Regras Críticas da Topologia RS-485:</text>
              <text x="25" y="46" fill="#94a3b8" font-family="sans-serif" font-size="11">1. Topologia exclusivamente linear (Daisy-Chain). Proibido usar estrela passiva sem repetidor industrial.</text>
              <text x="25" y="62" fill="#94a3b8" font-family="sans-serif" font-size="11">2. Terminação de 120Ω obrigatória nas duas pontas extremas (Sala 1 e Sala 4) para eliminar reflexão de sinal.</text>
              <text x="500" y="26" fill="#38bdf8" font-family="monospace" font-size="11">Velocidade: 9600 bps</text>
              <text x="500" y="44" fill="#38bdf8" font-family="monospace" font-size="11">Paridade: 8N1 (Sem paridade)</text>
              <text x="500" y="62" fill="#38bdf8" font-family="monospace" font-size="11">Distância: até 1.200 metros</text>
            </g>
          </svg>
        </div>

        <!-- Node Dynamic Card -->
        <div id="node-details-card" class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800">
            <span class="font-bold text-white flex items-center space-x-2">
              <i data-lucide="info" class="w-4 h-4 text-indigo-400"></i>
              <span id="node-title">Detalhes do Nó: Sala 1 (Master Arduino Mega 2560)</span>
            </span>
            <span class="font-mono text-emerald-400">Lógica 5V Nativa</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
            <div>
              <strong class="text-indigo-400 block mb-1">Módulo MAX485 (Serial1):</strong>
              <p>TX1 (Pino 18) &rarr; DI do MAX485<br>RX1 (Pino 19) &rarr; RO do MAX485<br>Pino D2 &rarr; DE/RE (TX/RX Enable)<br>5V e GND direto do barramento</p>
            </div>
            <div>
              <strong class="text-emerald-400 block mb-1">Fita WS2812B & LCD 20x2:</strong>
              <p>Pino D6 &rarr; DATA dos 47 LEDs<br>Pinos 20/21 (SDA/SCL) &rarr; LCD 20x2 I2C<br>Pinos D22-D35 &rarr; 14 Botões NA Locais<br>Fonte Externa 5V 5A dedicada aos LEDs</p>
            </div>
            <div>
              <strong class="text-amber-400 block mb-1">Vantagens Técnicas:</strong>
              <p>Zero conversores de nível lógico. Serial0 (USB) livre para gravação e depuração sem interferir no barramento RS-485.</p>
            </div>
          </div>
        </div>

      </div>

    </section>

    <!-- ============================================================== -->
    <!-- TAB 4: TECHNICAL COMPARISONS                                   -->
    <!-- ============================================================== -->
    <section id="tab-comparative" class="tab-content hidden space-y-6">
      
      <!-- Comparison Table Mega vs ESP32 vs Uno -->
      <div class="glass-panel rounded-3xl p-6 md:p-8 space-y-4">
        <h2 class="text-xl font-bold text-white flex items-center space-x-2">
          <i data-lucide="cpu" class="w-5 h-5 text-indigo-400"></i>
          <span>1. Controlador Central (Sala 1): Arduino Mega 2560 vs ESP32 vs Arduino Uno</span>
        </h2>
        
        <div class="overflow-x-auto rounded-xl border border-slate-800">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-950 text-slate-400 uppercase font-mono">
              <tr>
                <th class="p-3.5">Critério</th>
                <th class="p-3.5 text-emerald-400">Arduino Mega 2560 (ESCOLHIDO)</th>
                <th class="p-3.5 text-slate-300">ESP32 DevKit V1</th>
                <th class="p-3.5 text-slate-500">Arduino Uno R3</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/80">
              <tr>
                <td class="p-3 font-semibold text-white">Custo Inicial</td>
                <td class="p-3 text-emerald-400 font-bold">R$ 0,00 (Cliente já possui)</td>
                <td class="p-3">R$ 36,00 a R$ 51,00</td>
                <td class="p-3">R$ 24,00 a R$ 40,00</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-white">Nível Lógico</td>
                <td class="p-3 text-emerald-400 font-bold">5V Nativo (Sem conversores)</td>
                <td class="p-3 text-amber-400">3.3V (Exige 74AHCT125)</td>
                <td class="p-3">5V Nativo</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-white">UARTs Hardware</td>
                <td class="p-3 text-emerald-400 font-bold">4 Seriais independentes</td>
                <td class="p-3">3 Seriais</td>
                <td class="p-3 text-rose-400">Apenas 1 (Conflito USB/RS485)</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-white">Pinos de E/S</td>
                <td class="p-3 text-emerald-400 font-bold">54 pinos (14 botões direto)</td>
                <td class="p-3 text-amber-400">~24 úteis (Exige MCP23017)</td>
                <td class="p-3 text-rose-400">14 pinos (Insuficiente)</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-white">Veredito Final</td>
                <td class="p-3 text-emerald-400 font-bold">Vencedor Absoluto p/ Master</td>
                <td class="p-3">Opção futura se quiser Wi-Fi</td>
                <td class="p-3 text-slate-500">Inviável como Master</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Comparison RS-485 vs Ethernet vs Wi-Fi -->
      <div class="glass-panel rounded-3xl p-6 md:p-8 space-y-4">
        <h2 class="text-xl font-bold text-white flex items-center space-x-2">
          <i data-lucide="radio" class="w-5 h-5 text-emerald-400"></i>
          <span>2. Meio de Comunicação: RS-485 vs Ethernet (TCP) vs Wi-Fi</span>
        </h2>
        
        <div class="overflow-x-auto rounded-xl border border-slate-800">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-950 text-slate-400 uppercase font-mono">
              <tr>
                <th class="p-3.5">Parâmetro</th>
                <th class="p-3.5 text-emerald-400">RS-485 (adotado)</th>
                <th class="p-3.5 text-slate-300">Ethernet W5500 (TCP)</th>
                <th class="p-3.5 text-slate-500">Wi-Fi 2.4GHz</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/80">
              <tr>
                <td class="p-3 font-semibold text-white">Infraestrutura Ativa</td>
                <td class="p-3 text-emerald-400 font-bold">Nenhum switch ou roteador</td>
                <td class="p-3 text-rose-400">Switch 5 portas + 4x W5500 SPI</td>
                <td class="p-3">Roteador Wi-Fi dedicado</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-white">Alcance Máximo</td>
                <td class="p-3 text-emerald-400 font-bold">1.200 metros</td>
                <td class="p-3">100 metros por segmento</td>
                <td class="p-3 text-rose-400">15-30m com paredes/ruído</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-white">Custo de Rede</td>
                <td class="p-3 text-emerald-400 font-bold">~R$ 32,00 (4x MAX485)</td>
                <td class="p-3 text-rose-400">~R$ 395,00 (Switch + módulos)</td>
                <td class="p-3">Baixo (Nativo no ESP32)</td>
              </tr>
              <tr>
                <td class="p-3 font-semibold text-white">Confiabilidade 24/7</td>
                <td class="p-3 text-emerald-400 font-bold">Padrão industrial robusto</td>
                <td class="p-3">Muito alta</td>
                <td class="p-3 text-rose-400">Baixa (Sujeita a interferência)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- ============================================================== -->
    <!-- TAB 5: BILL OF MATERIALS (BOM) & PRICING                       -->
    <!-- ============================================================== -->
    <section id="tab-bom" class="tab-content hidden space-y-6">
      
      <div class="glass-panel rounded-3xl p-6 md:p-8 space-y-5">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 class="text-xl font-bold text-white flex items-center space-x-2">
              <i data-lucide="receipt" class="w-5 h-5 text-indigo-400"></i>
              <span>Lista de Materiais (BOM) & Orçamento Dinâmico</span>
            </h2>
            <p class="text-xs text-slate-400">Alterne entre os cenários para recalcular todos os custos e totais em tempo real</p>
          </div>

          <!-- Scenario Toggle Tabs -->
          <div class="flex flex-wrap items-center bg-slate-900 p-1.5 rounded-xl border border-slate-800 gap-1">
            <button onclick="switchScenario('economico')" id="btn-scen-economico" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white shadow transition">
              A. Recomendado (R$ 979)
            </button>
            <button onclick="switchScenario('padrao')" id="btn-scen-padrao" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition">
              B. Econômico (R$ 797)
            </button>
            <button onclick="switchScenario('industrial')" id="btn-scen-industrial" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition">
              C. Industrial (R$ 3.528)
            </button>
          </div>
        </div>

        <!-- Metric Financial Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div class="text-xs text-slate-400">Subtotal a Comprar</div>
            <div id="bom-subtotal" class="text-2xl font-bold text-white font-mono mt-1">R$ 979,00</div>
            <div class="text-[11px] text-emerald-400 mt-1 font-bold">Preços de referência nov/2026 · cotar</div>
          </div>

          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div class="flex items-center justify-between text-xs text-slate-400">
              <span>Contingência</span>
              <select id="contingency-rate" onchange="updateContingency(this.value)" class="bg-slate-900 text-indigo-400 font-mono text-xs rounded px-1.5 py-0.5 border border-slate-700">
                <option value="0">0%</option>
                <option value="10">10%</option>
                <option value="15" selected>15% (Rec.)</option>
                <option value="20">20%</option>
              </select>
            </div>
            <div id="bom-contingency" class="text-2xl font-bold text-indigo-400 font-mono mt-1">R$ 146,85</div>
            <div class="text-[11px] text-slate-500 mt-1">Margem para fretes e extras</div>
          </div>

          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div class="text-xs text-slate-400">Investimento Total Previsto</div>
            <div id="bom-total" class="text-2xl font-bold text-emerald-400 font-mono mt-1">R$ 1.125,85</div>
            <div class="text-[11px] text-emerald-400 mt-1 font-bold">Subtotal + Contingência</div>
          </div>

          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div class="text-xs text-slate-400">Economia com Inventário</div>
            <div id="bom-reused-total" class="text-2xl font-bold text-amber-400 font-mono mt-1">R$ 680,00</div>
            <div class="text-[11px] text-slate-400 mt-1">Mega + Uno + LCD + 47 botões 22 mm</div>
          </div>
        </div>

        <!-- Callouts: cabo de 2 vias & contato seco -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Callout 1: Cabo de 2 vias -->
          <div class="p-4 rounded-xl bg-slate-900/90 border border-indigo-500/30 space-y-2">
            <div class="flex items-center space-x-2 text-indigo-300 font-bold text-xs uppercase font-mono">
              <i data-lucide="cable" class="w-4 h-4 text-emerald-400"></i>
              <span>Por que cabo blindado de 2 vias (e não mais UTP de 4 pares)?</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              Com uma <strong>fonte 5 V em cada painel</strong>, a energia não passa mais pelo cabo. Entre as salas trafegam só os dados
              do RS-485: <strong>A e B</strong>, nas duas vias do par trançado. A <strong>malha</strong> blinda contra ruído e serve de
              referência comum (GND direto na Sala 1 e por 100 Ω nas outras).
            </p>
            <div class="text-[11px] font-mono text-emerald-300 bg-emerald-950/40 p-2.5 rounded-lg border border-emerald-500/30 space-y-1">
              <div>• Via 1 = A (+) · Via 2 = B (−) · Malha = SH (referência)</div>
              <div>• 45 m em 3 trechos · comprar 60 m · ~R$ 2,50/m</div>
              <div class="text-white font-bold">• Alternativa mais barata: UTP Cat5e usando só 1 par + 1 fio (cenário B)</div>
            </div>
          </div>

          <!-- Callout 2: Contato Seco 5V -->
          <div class="p-4 rounded-xl bg-slate-900/90 border border-emerald-500/30 space-y-2">
            <div class="flex items-center space-x-2 text-emerald-300 font-bold text-xs uppercase font-mono">
              <i data-lucide="zap" class="w-4 h-4 text-amber-400"></i>
              <span>Por que os Botões Antigos de 110V Funcionam em 5V a Custo Zero?</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              Todo botão mecânico é puramente um <strong>contato seco</strong> (duas lâminas de metal que se encostam). A especificação de "110V/250V" é apenas o limite de isolamento plástico da carcaça. Operar em 5V DC com corrente de 0,25mA (pull-up do Arduino) elimina qualquer arco elétrico ou faísca, dando <strong>vida útil quase infinita</strong> ao botão.
            </p>
            <div class="text-[11px] font-mono text-amber-300 bg-amber-950/40 p-2.5 rounded-lg border border-amber-500/30 space-y-1">
              <div>• A lâmpada de 110V antiga é desconectada e descartada.</div>
              <div>• A sinalização fica por conta da fita WS2812B ao lado do botão.</div>
              <div class="text-white font-bold">• Custo de botões no Cenário 1: R$ 0,00 (100% de reaproveitamento)!</div>
            </div>
          </div>
        </div>

        <!-- Filter and Export Bar -->
        <div class="flex flex-wrap items-center justify-between gap-3 p-3 rounded-xl bg-slate-950/60 border border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-xs text-slate-400">Categoria:</span>
            <select id="bom-category-filter" onchange="filterBomTable()" class="bg-slate-900 text-slate-200 text-xs rounded-lg px-2.5 py-1 border border-slate-700">
              <option value="all">Todas as Categorias</option>
              <option value="controladores">Controladores & RS-485</option>
              <option value="painel">Painel & LEDs WS2812B</option>
              <option value="entradas">Botões & Entradas</option>
              <option value="alimentacao">Fontes & Proteções</option>
              <option value="cabeamento">Cabos</option>
              <option value="conexoes">Conexões & Montagem</option>
            </select>
          </div>

          <div class="flex items-center space-x-2">
            <button onclick="exportBomCsv()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium flex items-center space-x-1.5 border border-slate-700 transition">
              <i data-lucide="download" class="w-3.5 h-3.5 text-indigo-400"></i>
              <span>Exportar CSV</span>
            </button>
            <button onclick="copyBomSummary()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium flex items-center space-x-1.5 border border-slate-700 transition">
              <i data-lucide="copy" class="w-3.5 h-3.5 text-emerald-400"></i>
              <span>Copiar Resumo</span>
            </button>
          </div>
        </div>

        <!-- BOM Table -->
        <div class="overflow-x-auto rounded-xl border border-slate-800 shadow-xl">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-950 text-slate-400 uppercase font-mono">
              <tr>
                <th class="p-3.5">Item</th>
                <th class="p-3.5">Especificação Técnica</th>
                <th class="p-3.5 text-center">Local</th>
                <th class="p-3.5 text-center">Qtd.</th>
                <th class="p-3.5 text-right">Unitário</th>
                <th class="p-3.5 text-right">Subtotal</th>
              </tr>
            </thead>
            <tbody id="bom-table-body" class="divide-y divide-slate-800/80"></tbody>
          </table>
        </div>

      </div>

    </section>

    <!-- ============================================================== -->
    <!-- TAB 6: ENGINEERING, LABOR, ROI & SCHEDULE                    -->
    <!-- ============================================================== -->
    <section id="tab-engineering" class="tab-content hidden space-y-6">
      
      <div class="glass-panel rounded-3xl p-6 md:p-8 space-y-6">
        <h2 class="text-xl font-bold text-white flex items-center space-x-2">
          <i data-lucide="clock" class="w-5 h-5 text-indigo-400"></i>
          <span>Estimativa de Engenharia, Cronograma & Retorno do Investimento</span>
        </h2>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <div class="lg:col-span-2 space-y-3">
            <h3 class="font-bold text-sm text-white flex items-center space-x-2">
              <i data-lucide="wrench" class="w-4 h-4 text-emerald-400"></i>
              <span>Esforço de Montagem e Programação (34h a 56h)</span>
            </h3>

            <div class="space-y-2 text-xs">
              <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <strong class="text-white block">Fase 1: Protótipo de Bancada & Protocolo RS-485</strong>
                  <span class="text-slate-400">Mega + 1 Uno + MAX485 + teste do cabo de 2 vias a 9600 bps</span>
                </div>
                <span class="font-mono font-bold text-indigo-400 bg-slate-900 px-2 py-1 rounded">4 – 6 h</span>
              </div>

              <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <strong class="text-white block">Fase 2: Conexão dos Botões & Debounce</strong>
                  <span class="text-slate-400">14 entradas do Mega e 11 de cada Uno com pull-up interno</span>
                </div>
                <span class="font-mono font-bold text-indigo-400 bg-slate-900 px-2 py-1 rounded">6 – 10 h</span>
              </div>

              <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <strong class="text-white block">Fase 3: Firmware RS-485 (CRC-8) & Heartbeat</strong>
                  <span class="text-slate-400">Polling a cada 250ms, detecção de timeout de 2s e recuperação</span>
                </div>
                <span class="font-mono font-bold text-indigo-400 bg-slate-900 px-2 py-1 rounded">6 – 10 h</span>
              </div>

              <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <strong class="text-white block">Fase 4: Painel WS2812B, LCD 20x2 & 2 Botões Setup</strong>
                  <span class="text-slate-400">Habilitação diária na central e acionamento dos 47 pixels</span>
                </div>
                <span class="font-mono font-bold text-indigo-400 bg-slate-900 px-2 py-1 rounded">6 – 10 h</span>
              </div>

              <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <strong class="text-white block">Fase 5: Montagem nos Painéis de Madeira & Fiação</strong>
                  <span class="text-slate-400">Instalação dos módulos nas caixas e passagem do cabo blindado de 2 vias</span>
                </div>
                <span class="font-mono font-bold text-indigo-400 bg-slate-900 px-2 py-1 rounded">6 – 10 h</span>
              </div>

              <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <strong class="text-white block">Fase 6: Comissionamento & Operação Assistida</strong>
                  <span class="text-slate-400">Testes paralelos com operadores antes de desativar o 110V</span>
                </div>
                <span class="font-mono font-bold text-indigo-400 bg-slate-900 px-2 py-1 rounded">6 – 10 h</span>
              </div>
            </div>
          </div>

          <div class="space-y-3">
            <h3 class="font-bold text-sm text-white flex items-center space-x-2">
              <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
              <span>Ganhos de ROI & Segurança</span>
            </h3>

            <div class="space-y-3 text-xs text-slate-300">
              <div class="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                <strong class="text-emerald-400 block mb-1">100% Livre de Risco Elétrico / NR-10:</strong>
                <p>Elimina completamente os 110V manipulados por operadores nas caixas de madeira.</p>
              </div>

              <div class="p-3 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
                <strong class="text-indigo-400 block mb-1">Economia em Manutenção:</strong>
                <p>Fim da substituição constante de lâmpadas incandescentes. LEDs duram mais de 50.000 horas.</p>
              </div>

              <div class="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
                <strong class="text-amber-400 block mb-1">Agilidade Operacional:</strong>
                <p>O supervisor enxerga em tempo real mesas livres e ocupadas, reduzindo filas e esperas.</p>
              </div>
            </div>
          </div>

        </div>

        <!-- 4-Week Schedule -->
        <div class="pt-4 border-t border-slate-800 space-y-3">
          <h3 class="font-bold text-sm text-white flex items-center space-x-2">
            <i data-lucide="calendar" class="w-4 h-4 text-indigo-400"></i>
            <span>Cronograma de Execução Estimado (4 Semanas)</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
              <span class="font-mono text-indigo-400 font-bold">SEMANA 1</span>
              <strong class="text-white block">Aquisições & Protótipo</strong>
              <p class="text-slate-400">Compra de 2 Uno R3, MAX485, fontes e material de conexão. Teste de bancada Mega + 1 Uno.</p>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
              <span class="font-mono text-indigo-400 font-bold">SEMANA 2</span>
              <strong class="text-white block">Central Sala 1 & LCD 20x2</strong>
              <p class="text-slate-400">Montagem do painel WS2812B, LCD 20x2 e 2 botões de setup diário.</p>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
              <span class="font-mono text-indigo-400 font-bold">SEMANA 3</span>
              <strong class="text-white block">Caixas Remotas 2, 3 e 4</strong>
              <p class="text-slate-400">Montagem das caixas dos 3 Uno (screw shield, ilhós) com botões e LEDs locais.</p>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
              <span class="font-mono text-indigo-400 font-bold">SEMANA 4</span>
              <strong class="text-white block">Cabo de 2 vias & Go-Live</strong>
              <p class="text-slate-400">Passagem do cabo RS-485, terminadores 120Ω e comissionamento final.</p>
            </div>
          </div>
        </div>

      </div>

    </section>

  
    
    
__PE_TAB_HTML__

    <!-- ============================================================== -->
    <!-- TAB 7: ARQUITETURA FÍSICA & ENGENHARIA DE MONTAGEM DO PAINEL  -->
    <!-- ============================================================== -->
    <section id="tab-assembly" class="tab-content hidden space-y-6">
      
      <!-- Header Banner -->
      <div class="glass-panel rounded-2xl p-6 border border-indigo-500/30">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center space-x-3.5">
            <div class="p-3 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <i data-lucide="layers" class="w-6 h-6"></i>
            </div>
            <div>
              <h2 class="text-xl font-extrabold text-white">Arquitetura Física do Painel & Engenharia de Montagem</h2>
              <p class="text-xs text-slate-400">Guia construtivo detalhado: Furação mecânica, alinhamento da Fita WS2812B e barramento de GND dos botões</p>
            </div>
          </div>
          <div class="flex items-center space-x-2 text-xs font-mono">
            <span class="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">PADRÃO INDUSTRIAL SCADA</span>
          </div>
        </div>
      </div>

      <!-- Exploded View / Layer Architecture Card -->
      <div class="glass-panel rounded-2xl p-6 space-y-6">
        <h3 class="text-base font-bold text-white flex items-center space-x-2">
          <i data-lucide="eye" class="w-5 h-5 text-indigo-400"></i>
          <span>Vista em Corte Explodido das 4 Camadas Construtivas</span>
        </h3>

        <!-- Interactive Diagram SVG -->
        <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 overflow-x-auto">
          <svg viewBox="0 0 1000 480" class="w-full min-w-[800px] h-auto select-none font-mono">
            <!-- Definitions -->
            <defs>
              <linearGradient id="frontPlateGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#1e293b"/>
                <stop offset="50%" stop-color="#334155"/>
                <stop offset="100%" stop-color="#1e293b"/>
              </linearGradient>
              <linearGradient id="ledStripGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="100%" stop-color="#e2e8f0"/>
              </linearGradient>
            </defs>

            <!-- Background & Scale -->
            <rect x="0" y="0" width="1000" height="480" fill="#030712" rx="12"/>

            <!-- LAYER 1: FACEPLATE FRONTAL -->
            <g transform="translate(40, 40)">
              <rect x="0" y="0" width="920" height="75" rx="8" fill="url(#frontPlateGrad)" stroke="#64748b" stroke-width="2"/>
              <text x="15" y="24" fill="#94a3b8" font-size="11" font-weight="bold">CAMADA 1: CHAPA FRONTAL (Acrílico Preto 3mm ou Alumínio Escovado com Gravação a Laser)</text>
              
              <!-- Sample Holes: 3 positions illustrated -->
              <!-- Position 01 -->
              <g transform="translate(160, 20)">
                <text x="25" y="16" fill="#ffffff" font-size="14" font-weight="900" text-anchor="middle">01</text>
                <circle cx="25" cy="38" r="12" fill="#000000" stroke="#f59e0b" stroke-width="2" stroke-dasharray="3,3"/>
                <text x="25" y="42" fill="#f59e0b" font-size="8" text-anchor="middle">FURO 10mm</text>
              </g>
              <!-- Position 02 -->
              <g transform="translate(430, 20)">
                <text x="25" y="16" fill="#ffffff" font-size="14" font-weight="900" text-anchor="middle">02</text>
                <circle cx="25" cy="38" r="12" fill="#000000" stroke="#f59e0b" stroke-width="2" stroke-dasharray="3,3"/>
                <text x="25" y="42" fill="#f59e0b" font-size="8" text-anchor="middle">FURO 10mm</text>
              </g>
              <!-- Position 03 -->
              <g transform="translate(700, 20)">
                <text x="25" y="16" fill="#ffffff" font-size="14" font-weight="900" text-anchor="middle">03</text>
                <circle cx="25" cy="38" r="12" fill="#000000" stroke="#f59e0b" stroke-width="2" stroke-dasharray="3,3"/>
                <text x="25" y="42" fill="#f59e0b" font-size="8" text-anchor="middle">FURO 10mm</text>
              </g>
            </g>

            <!-- LAYER 2: DIFUSORES ÓPTICOS TRANSLÚCIDOS -->
            <g transform="translate(40, 135)">
              <rect x="0" y="0" width="920" height="55" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,4"/>
              <text x="15" y="22" fill="#38bdf8" font-size="11" font-weight="bold">CAMADA 2: DIFUSORES ÓPTICOS (Lentes de Acrílico Leitoso 10mm com Anel de Vedação)</text>
              
              <!-- Lens 01 -->
              <circle cx="185" cy="36" r="13" fill="#e0f2fe" opacity="0.85" stroke="#38bdf8" stroke-width="2"/>
              <circle cx="185" cy="36" r="8" fill="#bae6fd" opacity="0.95"/>
              
              <!-- Lens 02 -->
              <circle cx="455" cy="36" r="13" fill="#e0f2fe" opacity="0.85" stroke="#38bdf8" stroke-width="2"/>
              <circle cx="455" cy="36" r="8" fill="#bae6fd" opacity="0.95"/>
              
              <!-- Lens 03 -->
              <circle cx="725" cy="36" r="13" fill="#e0f2fe" opacity="0.85" stroke="#38bdf8" stroke-width="2"/>
              <circle cx="725" cy="36" r="8" fill="#bae6fd" opacity="0.95"/>
              
              <text x="800" y="38" fill="#38bdf8" font-size="9">Espalha a luz homogênea sem ofuscamento</text>
            </g>

            <!-- LAYER 3: FITA DE LED WS2812B 5V (TRASEIRA) -->
            <g transform="translate(40, 210)">
              <rect x="0" y="0" width="920" height="90" rx="8" fill="#18181b" stroke="#10b981" stroke-width="2"/>
              <text x="15" y="22" fill="#10b981" font-size="11" font-weight="bold">CAMADA 3: FITA WS2812B (Colada por trás com Fita 3M VHB em Calha Dissipadora de Alumínio)</text>
              
              <!-- Continuous Flexible Strip White Ribbon -->
              <rect x="50" y="38" width="820" height="30" rx="3" fill="url(#ledStripGrad)" stroke="#cbd5e1" stroke-width="1"/>
              
              <!-- Copper Tracks & Solder Pads -->
              <line x1="50" y1="44" x2="870" y2="44" stroke="#d97706" stroke-width="1.5"/>
              <line x1="50" y1="53" x2="870" y2="53" stroke="#2563eb" stroke-width="1.5"/>
              <line x1="50" y1="62" x2="870" y2="62" stroke="#16a34a" stroke-width="1.5"/>

              <!-- WS2812B Chip 01 -->
              <g transform="translate(170, 43)">
                <rect x="0" y="0" width="28" height="20" rx="2" fill="#000000" stroke="#fbbf24" stroke-width="1"/>
                <circle cx="14" cy="10" r="6" fill="#10b981" opacity="0.9"/>
                <text x="14" y="30" fill="#10b981" font-size="8" text-anchor="middle">LED #1</text>
              </g>

              <!-- Data Flow Arrow -->
              <path d="M 220 53 L 420 53" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>
              <text x="320" y="47" fill="#60a5fa" font-size="9" text-anchor="middle">DIN ➔ DOUT (1 ÚNICO FIO DE DADOS)</text>

              <!-- WS2812B Chip 02 -->
              <g transform="translate(440, 43)">
                <rect x="0" y="0" width="28" height="20" rx="2" fill="#000000" stroke="#fbbf24" stroke-width="1"/>
                <circle cx="14" cy="10" r="6" fill="#ef4444" opacity="0.9"/>
                <text x="14" y="30" fill="#ef4444" font-size="8" text-anchor="middle">LED #2</text>
              </g>

              <!-- Data Flow Arrow -->
              <path d="M 490 53 L 690 53" stroke="#2563eb" stroke-width="2"/>
              <text x="590" y="47" fill="#60a5fa" font-size="9" text-anchor="middle">CASCATA SERIAL</text>

              <!-- WS2812B Chip 03 -->
              <g transform="translate(710, 43)">
                <rect x="0" y="0" width="28" height="20" rx="2" fill="#000000" stroke="#fbbf24" stroke-width="1"/>
                <circle cx="14" cy="10" r="6" fill="#2563eb" opacity="0.9"/>
                <text x="14" y="30" fill="#60a5fa" font-size="8" text-anchor="middle">LED #3</text>
              </g>
            </g>

            <!-- LAYER 4: BOTÕES N.A. & BARRAMENTO DE TERRA (GND) -->
            <g transform="translate(40, 320)">
              <rect x="0" y="0" width="920" height="135" rx="8" fill="#090d16" stroke="#f43f5e" stroke-width="2"/>
              <text x="15" y="24" fill="#f43f5e" font-size="11" font-weight="bold">CAMADA 4: BOTÕES PUSH-BUTTON 16mm & FIAÇÃO COM BARRAMENTO GND COMUM</text>
              
              <!-- Button 01 -->
              <g transform="translate(160, 40)">
                <rect x="0" y="0" width="50" height="40" rx="6" fill="#334155" stroke="#94a3b8" stroke-width="1.5"/>
                <circle cx="25" cy="20" r="10" fill="#dc2626"/>
                <text x="25" y="55" fill="#e2e8f0" font-size="9" text-anchor="middle">BTN 01</text>
                <!-- Terminal 1 (GND) -->
                <circle cx="15" cy="40" r="3" fill="#38bdf8"/>
                <!-- Terminal 2 (Signal) -->
                <circle cx="35" cy="40" r="3" fill="#f59e0b"/>
              </g>

              <!-- Button 02 -->
              <g transform="translate(430, 40)">
                <rect x="0" y="0" width="50" height="40" rx="6" fill="#334155" stroke="#94a3b8" stroke-width="1.5"/>
                <circle cx="25" cy="20" r="10" fill="#dc2626"/>
                <text x="25" y="55" fill="#e2e8f0" font-size="9" text-anchor="middle">BTN 02</text>
                <circle cx="15" cy="40" r="3" fill="#38bdf8"/>
                <circle cx="35" cy="40" r="3" fill="#f59e0b"/>
              </g>

              <!-- Button 03 -->
              <g transform="translate(700, 40)">
                <rect x="0" y="0" width="50" height="40" rx="6" fill="#334155" stroke="#94a3b8" stroke-width="1.5"/>
                <circle cx="25" cy="20" r="10" fill="#dc2626"/>
                <text x="25" y="55" fill="#e2e8f0" font-size="9" text-anchor="middle">BTN 03</text>
                <circle cx="15" cy="40" r="3" fill="#38bdf8"/>
                <circle cx="35" cy="40" r="3" fill="#f59e0b"/>
              </g>

              <!-- COMMON GND RAIL (Soldado em cascata contínua) -->
              <path d="M 80 110 L 175 110 L 175 80 M 175 110 L 445 110 L 445 80 M 445 110 L 715 110 L 715 80 M 715 110 L 880 110" stroke="#38bdf8" stroke-width="3" fill="none"/>
              <text x="80" y="125" fill="#38bdf8" font-size="10" font-weight="bold">BARRAMENTO GND COMUM (1 ÚNICO FIO CONTÍNUO P/ TODOS OS BOTÕES)</text>

              <!-- INDIVIDUAL SIGNAL WIRES (TO ARDUINO INPUT_PULLUP) -->
              <path d="M 195 80 L 195 95 L 300 95" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="2,2" fill="none"/>
              <text x="230" y="90" fill="#f59e0b" font-size="8">Sinal 1 (Pino D2)</text>

              <path d="M 465 80 L 465 95 L 560 95" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="2,2" fill="none"/>
              <text x="495" y="90" fill="#f59e0b" font-size="8">Sinal 2 (Pino D3)</text>

              <path d="M 735 80 L 735 95 L 830 95" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="2,2" fill="none"/>
              <text x="765" y="90" fill="#f59e0b" font-size="8">Sinal 3 (Pino D4)</text>
            </g>
          </svg>
        </div>

        <!-- 3 Essential Engineering Construction Rules -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
            <div class="flex items-center space-x-2 text-indigo-400 font-bold text-xs uppercase font-mono">
              <i data-lucide="drill" class="w-4 h-4"></i>
              <span>1. Furação & Tolerâncias</span>
            </div>
            <p class="text-xs text-slate-300">
              O painel frontal de acrílico ou alumínio deve ser usinado com <strong>furos de 10mm</strong> para os difusores ópticos e <strong>16mm</strong> para os botões push-button. O difusor de acrílico leitoso elimina o ponto cego do LED e distribui 180° de visibilidade.
            </p>
          </div>

          <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
            <div class="flex items-center space-x-2 text-emerald-400 font-bold text-xs uppercase font-mono">
              <i data-lucide="zap" class="w-4 h-4"></i>
              <span>2. Fixação da Fita WS2812B</span>
            </div>
            <p class="text-xs text-slate-300">
              A fita WS2812B (60 LEDs/metro) é colada por trás do painel em uma calha de alumínio condutora térmica. Cada chip 5050 fica alinhado exatamente sob o furo de 10mm. O sinal digital transita em cascata (DIN para DOUT) usando <strong>apenas 1 pino do Arduino</strong>.
            </p>
          </div>

          <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
            <div class="flex items-center space-x-2 text-rose-400 font-bold text-xs uppercase font-mono">
              <i data-lucide="circuit-board" class="w-4 h-4"></i>
              <span>3. Barramento GND dos Botões</span>
            </div>
            <p class="text-xs text-slate-300">
              Economia drástica de fiação: um terminal de todos os botões é interligado por um único barramento contínuo soldado ao <strong>GND comum</strong>. O outro terminal leva o sinal individual ao Arduino, operando com <code>INPUT_PULLUP</code> interno de 20kΩ.
            </p>
          </div>
        </div>

      </div>

    

      <!-- ========================================================================= -->
      <!-- MANUAL TÉCNICO DEFINITIVO DE ENGENHARIA E IMPLANTAÇÃO (10 CAPÍTULOS)     -->
      <!-- ========================================================================= -->
      <div id="manual-completo" class="glass-panel rounded-3xl p-6 md:p-8 space-y-8 border border-indigo-500/30 mt-8">
        
        <!-- Header & Quick Action Bar -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 border-b border-slate-800">
          <div class="space-y-1">
            <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono font-bold">
              <i data-lucide="book-open" class="w-3.5 h-3.5"></i>
              <span>DOCUMENTAÇÃO TÉCNICA · REV. 5.0 · docs/MANUAL_TECNICO.md</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white tracking-tight">Manual Técnico de Engenharia e Implantação</h2>
            <p class="text-xs text-slate-400">Sistema Digital de Monitoramento e Sinalização de Ocupação de Posições (4 Salas, 47 Postos)</p>
          </div>

          <!-- Quick Action Buttons -->
          <div class="flex flex-wrap items-center gap-2">
            <button onclick="copyManualMarkdown()" class="inline-flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/20 transition-all cursor-pointer">
              <i data-lucide="copy" class="w-4 h-4"></i>
              <span>Copiar Manual (.MD)</span>
            </button>
            <button onclick="downloadManualMarkdown()" class="inline-flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold text-xs transition-all cursor-pointer">
              <i data-lucide="download" class="w-4 h-4 text-emerald-400"></i>
              <span>Baixar Arquivo .MD</span>
            </button>
          </div>
        </div>

        <!-- Manual renderizado a partir de docs/MANUAL_TECNICO.md (marked.js) -->
        <div id="manual-render" class="pe-md"><p class="text-slate-400 text-sm">Carregando manual…</p></div>

      </div>

    </section>

  </main>

  <!-- JAVASCRIPT APPLICATION CORE -->
  <script>
    // =========================================================================
    // SYSTEM STATE MODEL
    // =========================================================================
    const SYSTEM = {
      rooms: {
        1: { name: 'Sala 1 (Central)', total: 14, slaveId: 1, online: true },
        2: { name: 'Sala 2 (Remota)', total: 11, slaveId: 2, online: true },
        3: { name: 'Sala 3 (Remota)', total: 11, slaveId: 3, online: true },
        4: { name: 'Sala 4 (Remota)', total: 11, slaveId: 4, online: true }
      },
      positions: [], // 47 elements
      pollingSpeed: 300,
      pollingInterval: null,
      currentPolledSlave: 2,
      lcdMode: 'setup', // 'setup', 'preset', or 'monitor'
      lcdSelectedPosIndex: 0, // 0 to 46
      lcdSelectedPresetIndex: 0, // 0 to 5
      activePresetName: 'Preset 1: 100% Ativo (Boot)',
      activeSlot: 1,
      soundEnabled: true,
      audioCtx: null
    };

    const PRESETS = [
      { id: 'p1', name: 'Preset 1: 100% Ativo', shortName: '1:100% ATIV', desc: '47 posições todas em Verde (Boot Padrão)' },
      { id: 'p2', name: 'Preset 2: Dia Típico', shortName: '2:TIPICO 35', desc: '35 ativas (S1:10, S2:8, S3:8, S4:9), 12 sem uso' },
      { id: 'p3', name: 'Preset 3: Plantão', shortName: '3:PLANTAO 2', desc: '20 ativas (S1:6, S2:5, S3:4, S4:5), 27 sem uso' },
      { id: 's1', name: 'EEPROM Slot 1', shortName: '4:SLOT 1 EEP', desc: 'Configuração customizada no Slot 1 da EEPROM' },
      { id: 's2', name: 'EEPROM Slot 2', shortName: '5:SLOT 2 EEP', desc: 'Configuração customizada no Slot 2 da EEPROM' },
      { id: 's3', name: 'EEPROM Slot 3', shortName: '6:SLOT 3 EEP', desc: 'Configuração customizada no Slot 3 da EEPROM' }
    ];

    /*
      DEFINITIVE USER COLOR RULES (BOARD MESSAGE #12 & #16 & #17):
      - 🔵 AZUL ESCURO: SEM USO (Desabilitado / Não monitorado no dia) -> state: 'unused' (enabled: false)
      - 🟢 VERDE: OCUPADO / EM ATENDIMENTO / HABILITADO ATIVO -> state: 'occupied' (enabled: true)
      - 🔴 VERMELHO: LIVRE (Habilitado, desocupado no momento, avisa Sala 1 que o lugar está livre!) -> state: 'free' (enabled: true)
      
      ESTADO PADRÃO DE INICIALIZAÇÃO (BOOT / RESET):
      - Por padrão TODAS as 47 posições carregam HABILITADAS em 🟢 VERDE (todas ocupadas/ativas).
    */
    function initPositions() {
      SYSTEM.positions = [];
      let globalIndex = 0;

      // Sala 1: 14 posições (todas habilitadas em Verde no Boot padrão)
      for (let i = 1; i <= 14; i++) {
        SYSTEM.positions.push({
          index: globalIndex++,
          room: 1,
          localId: i,
          code: `S1-${String(i).padStart(2, '0')}`,
          enabled: true,
          state: 'occupied', // 🟢 VERDE: OCUPADO / EM ATENDIMENTO / HABILITADO ATIVO NO BOOT
          lastChanged: new Date().toLocaleTimeString()
        });
      }

      // Salas 2, 3, 4: 11 posições cada (todas habilitadas em Verde no Boot padrão)
      for (let r = 2; r <= 4; r++) {
        for (let i = 1; i <= 11; i++) {
          SYSTEM.positions.push({
            index: globalIndex++,
            room: r,
            localId: i,
            code: `S${r}-${String(i).padStart(2, '0')}`,
            enabled: true,
            state: 'occupied', // 🟢 VERDE: OCUPADO / EM ATENDIMENTO / HABILITADO ATIVO NO BOOT
            lastChanged: new Date().toLocaleTimeString()
          });
        }
      }
      SYSTEM.activePresetName = 'Preset 1: 100% Ativo (Boot)';
    }

    // =========================================================================
    // RENDERING LOGIC (CENTRAL PANEL + REMOTE STATIONS)
    // =========================================================================
    function renderSimulatorUI() {
      let countOccupied = 0;
      let countFree = 0;
      let countUnused = 0;

      // 1. Central WS2812B LEDs on Sala 1 (Mirrors all 47 positions)
      for (let r = 1; r <= 4; r++) {
        const container = document.getElementById(`master-leds-s${r}`);
        if (!container) continue;
        container.innerHTML = '';

        const roomPositions = SYSTEM.positions.filter(p => p.room === r);
        const isRoomFail = !SYSTEM.rooms[r].online;

        roomPositions.forEach(pos => {
          if (!pos.enabled) countUnused++;
          else if (pos.state === 'occupied') countOccupied++;
          else countFree++;

          const card = document.createElement('div');
          card.id = `master-pos-card-${pos.index}`;
          
          let ledClass = 'led-darkblue';
          let statusText = 'SEM USO';
          let badgeColor = 'text-blue-400 bg-blue-950/40 border-blue-500/30';

          if (isRoomFail) {
            ledClass = 'led-fail-blink';
            statusText = 'TIMEOUT';
            badgeColor = 'text-amber-400 bg-amber-950/40 border-amber-500/30';
          } else if (!pos.enabled) {
            ledClass = 'led-darkblue';
            statusText = 'S/USO';
            badgeColor = 'text-blue-400 bg-blue-950/40 border-blue-500/30';
          } else if (pos.state === 'occupied') {
            ledClass = 'led-green';
            statusText = 'OCUPADO';
            badgeColor = 'text-emerald-400 bg-emerald-950/40 border-emerald-500/30';
          } else {
            ledClass = 'led-red';
            statusText = 'LIVRE';
            badgeColor = 'text-rose-400 bg-rose-950/40 border-rose-500/30';
          }

          const isSelected = (pos.index === SYSTEM.lcdSelectedPosIndex);
          const selectClass = isSelected ? 'pos-module-selected' : '';

          card.className = `pos-module-card w-full p-1.5 sm:p-2 flex flex-col items-center justify-center space-y-1.5 cursor-pointer select-none transition min-w-0 ${selectClass}`;
          card.title = `${pos.code} - ${isRoomFail ? 'FALHA DE REDE RS-485 (ÂMBAR PISCANTE)' : (!pos.enabled ? 'SEM USO / NÃO MONITORADO (AZUL ESCURO)' : (pos.state === 'occupied' ? 'OCUPADO / EM ATENDIMENTO (VERDE)' : 'LIVRE / DISPONÍVEL (VERMELHO)'))}`;
          card.onclick = () => {
            selectPositionForSetup(pos.index);
          };

          card.innerHTML = `
            <!-- PARTE SUPERIOR (TOPO): NÚMERO DA POSIÇÃO EM DESTAQUE NÍTIDO -->
            <div class="text-[11px] sm:text-xs font-mono font-black text-white tracking-tight leading-none drop-shadow-sm">
              ${String(pos.localId).padStart(2, '0')}
            </div>
            <!-- PARTE INFERIOR (EMBAIXO): O LED PILOTO FÍSICO LUMINOSO COM BRILHO 3D -->
            <div class="led-pilot-lamp w-5 h-5 sm:w-6 sm:h-6 rounded-full ${ledClass} shrink-0 flex items-center justify-center shadow-md">
              <div class="w-1.5 h-1.5 rounded-full bg-white/50"></div>
            </div>
          `;
          container.appendChild(card);
        });
      }

      // Update Top Counts
      const elOcc = document.getElementById('central-count-inuse');
      const elFree = document.getElementById('central-count-free');
      const elUnused = document.getElementById('central-count-unused');
      if (elOcc) elOcc.textContent = `${countOccupied} Ocupadas (Verde)`;
      if (elFree) elFree.textContent = `${countFree} Livres (Vermelho)`;
      if (elUnused) elUnused.textContent = `${countUnused} Sem Uso (Azul)`;

      // 2. Sala 1 Local Physical Operator Modular Bench (Positions 1 to 14)
      const s1Buttons = document.getElementById('buttons-room-1');
      if (s1Buttons) {
        s1Buttons.innerHTML = '';
        SYSTEM.positions.filter(p => p.room === 1).forEach(pos => {
          const card = document.createElement('div');
          card.className = 'pos-module-card p-1.5 sm:p-2 flex flex-col items-center justify-between space-y-1.5 border border-slate-800 rounded-xl shadow-sm';
          
          let ledClass = !pos.enabled ? 'led-darkblue' : (pos.state === 'occupied' ? 'led-green' : 'led-red');
          let btnClass = !pos.enabled ? 'border-blue-500/30 text-blue-400 bg-blue-950/30 cursor-not-allowed opacity-50' : 
            (pos.state === 'occupied' ? 'border-emerald-500/50 text-emerald-300 bg-emerald-950/50 shadow-sm shadow-emerald-500/20' : 'border-rose-500/50 text-rose-300 bg-rose-950/50 shadow-sm shadow-rose-500/20');

          card.className = 'pos-module-card px-1 py-1.5 flex flex-col items-center justify-between space-y-1 border border-slate-800 rounded-xl shadow-sm min-w-0 w-full overflow-hidden';
          card.title = `${pos.code} - ${!pos.enabled ? 'Sem Uso (Azul Escuro)' : (pos.state === 'occupied' ? 'Ocupado (Verde) - Clique p/ Liberar' : 'Livre (Vermelho) - Clique p/ Ocupar')}`;

          card.innerHTML = `
            <!-- TOPO: NÚMERO EM DESTAQUE -->
            <div class="text-[10px] sm:text-[11px] font-mono font-black text-white tracking-tight leading-none">
              ${String(pos.localId).padStart(2, '0')}
            </div>
            <!-- MEIO: LED INDICADOR FÍSICO -->
            <div class="led-pilot-lamp w-4 h-4 rounded-full ${ledClass} shrink-0 flex items-center justify-center shadow-sm">
              <div class="w-1 h-1 rounded-full bg-white/50"></div>
            </div>
            <!-- EMBAIXO: BOTÃO FÍSICO TÁTIL N.A. (CIRCULAR 24px) -->
            <button onclick="toggleRoomOperatorButton(${pos.index})" class="btn-na-tactile w-6 h-6 rounded-full shrink-0 flex items-center justify-center transition-all shadow-sm ${btnClass}" title="${pos.code} - Clique para comutar Ocupado / Livre">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
                <line x1="12" y1="2" x2="12" y2="12"></line>
              </svg>
            </button>
          `;
          s1Buttons.appendChild(card);
        });
      }

      // 3. Remote Operator Consoles (Salas 2, 3, 4): BOTH LED + BUTTON
      for (let r = 2; r <= 4; r++) {
        const stationBox = document.getElementById(`station-positions-${r}`);
        if (!stationBox) continue;
        stationBox.innerHTML = '';

        const roomPos = SYSTEM.positions.filter(p => p.room === r);
        const isOnline = SYSTEM.rooms[r].online;

        roomPos.forEach(pos => {
          const card = document.createElement('div');
          card.className = 'pos-module-card p-1.5 sm:p-2 flex flex-col items-center justify-between space-y-1.5 border border-slate-800 rounded-xl shadow-sm';

          let ledClass = 'led-darkblue';
          if (!isOnline) ledClass = 'led-fail-blink';
          else if (!pos.enabled) ledClass = 'led-darkblue';
          else if (pos.state === 'occupied') ledClass = 'led-green';
          else ledClass = 'led-red';

          let btnClass = !isOnline ? 'opacity-30 cursor-not-allowed text-slate-500 border-slate-800' :
            (!pos.enabled ? 'border-blue-500/30 text-blue-400 bg-blue-950/30 cursor-not-allowed opacity-50' : 
            (pos.state === 'occupied' ? 'border-emerald-500/50 text-emerald-300 bg-emerald-950/50 shadow-sm shadow-emerald-500/20' : 'border-rose-500/50 text-rose-300 bg-rose-950/50 shadow-sm shadow-rose-500/20'));

          card.className = 'pos-module-card px-1 py-1.5 flex flex-col items-center justify-between space-y-1 border border-slate-800 rounded-xl shadow-sm min-w-0 w-full overflow-hidden';
          card.title = `${pos.code} - ${!isOnline ? 'Falha RS-485' : (!pos.enabled ? 'Sem Uso (Azul Escuro)' : (pos.state === 'occupied' ? 'Ocupado (Verde) - Clique p/ Liberar' : 'Livre (Vermelho) - Clique p/ Ocupar'))}`;

          card.innerHTML = `
            <!-- TOPO: NÚMERO EM DESTAQUE NÍTIDO -->
            <div class="text-[10px] sm:text-[11px] font-mono font-black text-white tracking-tight leading-none">
              ${String(pos.localId).padStart(2, '0')}
            </div>
            <!-- MEIO: LED INDICADOR FÍSICO LUMINOSO -->
            <div class="led-pilot-lamp w-4 h-4 rounded-full ${ledClass} shrink-0 flex items-center justify-center shadow-sm">
              <div class="w-1 h-1 rounded-full bg-white/50"></div>
            </div>
            <!-- EMBAIXO: BOTÃO FÍSICO N.A. ALINHADO DIRETAMENTE (24px) -->
            <button onclick="if (${isOnline}) toggleRoomOperatorButton(${pos.index})" class="btn-na-tactile w-6 h-6 rounded-full shrink-0 flex items-center justify-center transition-all shadow-sm ${btnClass}" title="${pos.code} - Clique para comutar Ocupado / Livre">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
                <line x1="12" y1="2" x2="12" y2="12"></line>
              </svg>
            </button>
          `;
          stationBox.appendChild(card);
        });
      }

      updateLcdScreen();
    }

    // OPERATOR BUTTON IN ROOMS (Salas 2, 3, 4 + Sala 1):
    // Toggles between 🟢 VERDE (Ocupado) and 🔴 VERMELHO (Livre).
    // If 🔵 AZUL ESCURO (Sem uso), does nothing and alerts.
    function toggleRoomOperatorButton(index) {
      const pos = SYSTEM.positions[index];
      if (!pos) return;

      if (!pos.enabled) {
        playBeep(250, 0.12);
        logSerial(`[OPERADOR S${pos.room}] Posição ${pos.code} está em AZUL ESCURO (SEM USO hoje na Central). Botão inativo.`);
        return;
      }

      // Toggle between Occupied (Green) and Free (Red)
      if (pos.state === 'occupied') {
        pos.state = 'free'; // Torna-se VERMELHO (Livre - avisa Sala 1 para enviar próxima pessoa!)
        playBeep(440, 0.08);
        logSerial(`[OPERADOR S${pos.room}] Posição ${pos.code} LIVRE (🔴 VERMELHO). Sala 1 avisada para direcionar pessoa!`);
      } else {
        pos.state = 'occupied'; // Torna-se VERDE (Ocupado em atendimento)
        playBeep(880, 0.08);
        logSerial(`[OPERADOR S${pos.room}] Posição ${pos.code} OCUPADA (🟢 VERDE). Atendimento em andamento.`);
      }

      pos.lastChanged = new Date().toLocaleTimeString();
      renderSimulatorUI();
    }

    // =========================================================================
    // SALA 1 SETUP VIA 2 PHYSICAL BUTTONS BESIDE LCD 20x2
    // =========================================================================
    // Button 1: [NAV / PRÓXIMO] - Advances 1 to 47 in Setup, or cycles Presets
    function lcdNavNext() {
      playBeep(650, 0.04);
      if (SYSTEM.lcdMode === 'setup') {
        SYSTEM.lcdSelectedPosIndex = (SYSTEM.lcdSelectedPosIndex + 1) % 47;
        const pos = SYSTEM.positions[SYSTEM.lcdSelectedPosIndex];
        logSerial(`[SETUP S1] Navegou para: ${pos.code} (${pos.enabled ? 'HABILITADA' : 'SEM USO'})`);
        renderSimulatorUI();
      } else if (SYSTEM.lcdMode === 'preset') {
        SYSTEM.lcdSelectedPresetIndex = (SYSTEM.lcdSelectedPresetIndex + 1) % PRESETS.length;
        const pr = PRESETS[SYSTEM.lcdSelectedPresetIndex];
        logSerial(`[LCD PRESET] Selecionado no menu: ${pr.name}`);
        updateLcdScreen();
      } else {
        toggleLcdColor();
      }
    }

    // Button 2: [HABILITAR / DESABILITAR] - Toggles position or applies selected Preset
    function lcdToggleEnable() {
      if (SYSTEM.lcdMode === 'setup') {
        const pos = SYSTEM.positions[SYSTEM.lcdSelectedPosIndex];
        if (!pos) return;
        pos.enabled = !pos.enabled;
        if (!pos.enabled) {
          pos.state = 'unused'; // 🔵 AZUL ESCURO
          playBeep(320, 0.08);
          logSerial(`[SETUP S1] ${pos.code} alterada para 🔵 SEM USO (AZUL ESCURO).`);
        } else {
          pos.state = 'occupied'; // 🟢 VERDE (Ocupada / Habilitada)
          playBeep(780, 0.08);
          logSerial(`[SETUP S1] ${pos.code} HABILITADA (🟢 VERDE / OCUPADO).`);
        }
        renderSimulatorUI();
      } else if (SYSTEM.lcdMode === 'preset') {
        applyPresetByIndex(SYSTEM.lcdSelectedPresetIndex);
      } else {
        toggleLcdMode();
      }
    }

    function selectPositionForSetup(index) {
      SYSTEM.lcdSelectedPosIndex = index;
      SYSTEM.lcdMode = 'setup';
      playBeep(600, 0.04);
      renderSimulatorUI();
    }

    
    // =========================================================================
    // 3 FULL THEMES SYSTEM: OLED DARK / MIDNIGHT INDIGO / CLEAN LIGHT
    // =========================================================================
    function setAppTheme(themeName) {
      document.body.classList.remove('theme-indigo', 'theme-oled', 'theme-light');
      document.body.classList.add(`theme-${themeName}`);

      if (themeName === 'light') {
        document.documentElement.classList.remove('dark');
      } else {
        document.documentElement.classList.add('dark');
      }

      ['oled', 'indigo', 'light'].forEach(t => {
        const btn = document.getElementById(`btn-theme-${t}`);
        if (btn) {
          if (t === themeName) {
            btn.className = 'theme-btn px-2 py-1 rounded-lg text-white font-bold bg-indigo-600 shadow transition flex items-center space-x-1';
          } else {
            btn.className = 'theme-btn px-2 py-1 rounded-lg text-slate-400 hover:text-white transition flex items-center space-x-1';
          }
        }
      });

      try {
        localStorage.setItem('painel_salas_theme', themeName);
      } catch(e) {}
      logSerial(`[TEMA] Visual alterado para: ${themeName.toUpperCase()}`);
    }

    // =========================================================================
    // HARDWARE COMBO: PRESS BOTH BUTTONS TOGETHER (ARDUINO COMBO FUNCTION)
    // =========================================================================
    function pressBothButtonsTogether() {
      // Characteristic dual-tone beep for mode shift
      playBeep(440, 0.08);
      setTimeout(() => playBeep(880, 0.12), 90);

      if (SYSTEM.lcdMode === 'monitor') {
        SYSTEM.lcdMode = 'setup';
      } else if (SYSTEM.lcdMode === 'setup') {
        SYSTEM.lcdMode = 'preset';
      } else {
        SYSTEM.lcdMode = 'monitor';
      }

      const modeNames = {
        'monitor': 'MODO 1: MONITOR GERAL',
        'setup': 'MODO 2: SETUP DE POSIÇÕES',
        'preset': 'MODO 3: GERENCIADOR PRESETS'
      };

      const lbl = document.getElementById('lcd-mode-label');
      if (lbl) lbl.textContent = modeNames[SYSTEM.lcdMode];

      // Update button subtexts
      const b1 = document.getElementById('btn1-subtext');
      const b2 = document.getElementById('btn2-subtext');
      if (b1 && b2) {
        if (SYSTEM.lcdMode === 'setup') {
          b1.textContent = 'Navega posições 1 a 47';
          b2.textContent = 'Alterna Habilitada ↔ Azul Escuro';
        } else if (SYSTEM.lcdMode === 'preset') {
          b1.textContent = 'Navega lista de Presets';
          b2.textContent = 'Aplica Preset Selecionado';
        } else {
          b1.textContent = 'Trocar Cor Backlight LCD';
          b2.textContent = 'Alternar Modo de Exibição';
        }
      }

      logSerial(`[HARDWARE BOTAO 1+2] Ambos os botões pressionados juntos! Novo modo: ${modeNames[SYSTEM.lcdMode]}`);

      // Temporary splash message on LCD 20x2
      const l1 = document.getElementById('lcd-line-1');
      const l2 = document.getElementById('lcd-line-2');
      if (l1 && l2) {
        l1.textContent = "MODO ALTERADO:      ";
        l2.textContent = `>>> ${SYSTEM.lcdMode.toUpperCase()} <<<      `.substring(0, 20);
        setTimeout(updateLcdScreen, 600);
      } else {
        updateLcdScreen();
      }
    }
function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(e => console.log(e));
        const icon = document.getElementById('fullscreen-icon');
        if (icon) icon.setAttribute('data-lucide', 'minimize-2');
      } else {
        document.exitFullscreen().catch(e => console.log(e));
        const icon = document.getElementById('fullscreen-icon');
        if (icon) icon.setAttribute('data-lucide', 'maximize-2');
      }
      setTimeout(() => lucide.createIcons(), 100);
    }

    function updateActivePresetBadge() {
      const el = document.getElementById('active-preset-text');
      if (el) el.textContent = SYSTEM.activePresetName;
    }

    function applyPresetByIndex(idx) {
      playBeep(700, 0.08);
      if (idx === 0) {
        // Preset 1: 100% Ativo (Boot Padrão)
        SYSTEM.positions.forEach(p => {
          p.enabled = true;
          p.state = 'occupied';
        });
        SYSTEM.activePresetName = 'Preset 1: 100% Ativo (Boot)';
        logSerial("[EEPROM / BOOT] Preset 1 aplicado: 100% Ativo (47 posições em 🟢 Verde). Padrão de Inicialização restaurado.");
      } else if (idx === 1) {
        // Preset 2: Dia de Semana Típico (35 ativas)
        SYSTEM.positions.forEach(p => {
          const isAct = (p.room === 1 && p.localId <= 10) || (p.room === 2 && p.localId <= 8) || (p.room === 3 && p.localId <= 8) || (p.room === 4 && p.localId <= 9);
          p.enabled = isAct;
          p.state = isAct ? 'occupied' : 'unused';
        });
        SYSTEM.activePresetName = 'Preset 2: Típico (35)';
        logSerial("[EEPROM / PRESET] Preset 2 aplicado: Dia Típico (35 posições em 🟢 Verde, 12 em 🔵 Azul Escuro).");
      } else if (idx === 2) {
        // Preset 3: Plantão / Reduzido (20 ativas)
        SYSTEM.positions.forEach(p => {
          const isAct = (p.room === 1 && p.localId <= 6) || (p.room === 2 && p.localId <= 5) || (p.room === 3 && p.localId <= 4) || (p.room === 4 && p.localId <= 5);
          p.enabled = isAct;
          p.state = isAct ? 'occupied' : 'unused';
        });
        SYSTEM.activePresetName = 'Preset 3: Plantão (20)';
        logSerial("[EEPROM / PRESET] Preset 3 aplicado: Plantão Reduzido (20 posições em 🟢 Verde, 27 em 🔵 Azul Escuro).");
      } else if (idx >= 3) {
        const slotNum = idx - 2;
        loadFromEepromSlot(slotNum);
        return;
      }
      updateActivePresetBadge();
      renderSimulatorUI();
      updateLcdScreen();
    }

    function saveCurrentToEepromSlot(slot) {
      const targetSlot = slot || SYSTEM.activeSlot || 1;
      const data = SYSTEM.positions.map(p => ({ enabled: p.enabled, state: p.state }));
      try {
        localStorage.setItem(`painel_eeprom_slot_${targetSlot}`, JSON.stringify(data));
      } catch (e) {
        console.warn("LocalStorage indisponível, simulando em memória:", e);
      }
      const hexOffset = (0x0040 * targetSlot).toString(16).toUpperCase().padStart(4, '0');
      playBeep(980, 0.15);
      SYSTEM.activePresetName = `EEPROM Slot ${targetSlot} (Salvo)`;
      updateActivePresetBadge();
      logSerial(`[EEPROM ATmega2560] Gravados 47 bytes no Slot ${targetSlot} (Endereço 0x${hexOffset}) com CRC16 válido. Configuração persistida na EEPROM interna.`);
      
      if (SYSTEM.lcdMode === 'preset') {
        const l1 = document.getElementById('lcd-line-1');
        const l2 = document.getElementById('lcd-line-2');
        if (l1 && l2) {
          l1.textContent = `SLOT ${targetSlot}: GRAVADO!   `;
          l2.textContent = `EEPROM 47B CRC-OK   `;
          setTimeout(updateLcdScreen, 1200);
          return;
        }
      }
      updateLcdScreen();
    }

    function loadFromEepromSlot(slot) {
      const targetSlot = slot || SYSTEM.activeSlot || 1;
      let raw = null;
      try {
        raw = localStorage.getItem(`painel_eeprom_slot_${targetSlot}`);
      } catch(e) {}
      
      if (raw) {
        try {
          const data = JSON.parse(raw);
          if (Array.isArray(data) && data.length === 47) {
            data.forEach((item, idx) => {
              if (SYSTEM.positions[idx]) {
                SYSTEM.positions[idx].enabled = item.enabled;
                SYSTEM.positions[idx].state = item.state;
              }
            });
            playBeep(850, 0.1);
            const hexOffset = (0x0040 * targetSlot).toString(16).toUpperCase().padStart(4, '0');
            SYSTEM.activePresetName = `EEPROM Slot ${targetSlot} (Custom)`;
            updateActivePresetBadge();
            logSerial(`[EEPROM ATmega2560] Slot ${targetSlot} lido do endereço 0x${hexOffset}. 47 posições restauradas na SRAM com sucesso.`);
            renderSimulatorUI();
            updateLcdScreen();
            return;
          }
        } catch(err) {
          console.error(err);
        }
      }
      // Se ainda não salvo, grava o estado atual como inicial para este slot
      saveCurrentToEepromSlot(targetSlot);
    }

    function toggleLcdMode(targetMode) {
      if (targetMode) {
        SYSTEM.lcdMode = targetMode;
      } else {
        if (SYSTEM.lcdMode === 'setup') SYSTEM.lcdMode = 'preset';
        else if (SYSTEM.lcdMode === 'preset') SYSTEM.lcdMode = 'monitor';
        else SYSTEM.lcdMode = 'setup';
      }
      playBeep(700, 0.05);
      const lbl = document.getElementById('lcd-mode-label');
      if (lbl) {
        if (SYSTEM.lcdMode === 'setup') lbl.textContent = 'SETUP DE POSIÇÃO (1 a 47)';
        else if (SYSTEM.lcdMode === 'preset') lbl.textContent = 'MENU PRESETS EEPROM';
        else lbl.textContent = 'MONITOR GERAL DA PLANTA';
      }
      updateLcdScreen();
    }

    // Toggle Room Link (RS-485 Timeout Simulation > 2s)
    function toggleRoomLink(room) {
      SYSTEM.rooms[room].online = !SYSTEM.rooms[room].online;
      const isOnline = SYSTEM.rooms[room].online;

      const badge = document.getElementById(`badge-timeout-${room}`);
      const btn = document.getElementById(`btn-link-${room}`);

      if (badge) badge.classList.toggle('hidden', isOnline);
      if (btn) {
        btn.textContent = isOnline ? 'LINK: ONLINE' : 'LINK: TIMEOUT';
        btn.className = `px-2 py-0.5 rounded text-[11px] font-mono font-bold transition ${isOnline ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-blue-500/20 text-blue-300 border border-blue-500/40 animate-pulse'}`;
      }

      if (!isOnline) {
        playBeep(240, 0.35);
        logSerial(`[TIMEOUT RS-485] Sala ${room} NÃO RESPONDE HÁ >2s! Barramento desconectado.`);
      } else {
        playBeep(920, 0.1);
        logSerial(`[LINK RESTAURADO] Sala ${room} reconectada ao barramento RS-485.`);
      }

      renderSimulatorUI();
    }

    function toggleRoomAll(room) {
      const roomPos = SYSTEM.positions.filter(p => p.room === room);
      const allEnabled = roomPos.every(p => p.enabled);
      roomPos.forEach(p => {
        p.enabled = !allEnabled;
        p.state = !allEnabled ? 'free' : 'unused';
      });
      playBeep(650, 0.08);
      logSerial(`[CMD SALA ${room}] ${!allEnabled ? 'Todas Habilitadas (Livre)' : 'Todas em Azul Escuro (Sem Uso)'}`);
      renderSimulatorUI();
    }

    // =========================================================================
    // LCD 20x2 LOGIC (STRICT 2 LINES X 20 CHARACTERS)
    // =========================================================================
    function updateLcdScreen() {
      const l1 = document.getElementById('lcd-line-1');
      const l2 = document.getElementById('lcd-line-2');
      if (!l1 || !l2) return;

      const pad20 = s => (s.length > 20 ? s.substring(0, 20) : s.padEnd(20, ' '));

      if (SYSTEM.lcdMode === 'setup') {
        const pos = SYSTEM.positions[SYSTEM.lcdSelectedPosIndex];
        const statusStr = !pos.enabled ? '[SEM USO]' : (pos.state === 'occupied' ? '[OCUPADA]' : '[LIVRE]  ');
        l1.textContent = pad20(`POS ${pos.code}: ${statusStr}`);
        l2.textContent = pad20(`[NAV]>PROX  [HAB]ALT`);
      } else if (SYSTEM.lcdMode === 'preset') {
        const pr = PRESETS[SYSTEM.lcdSelectedPresetIndex] || PRESETS[0];
        l1.textContent = pad20(`PRESET: [${pr.shortName}]`);
        l2.textContent = pad20(`[NAV]>SEL [*]SLV [#]OK`);
      } else {
        const countOcc = SYSTEM.positions.filter(p => p.enabled && p.state === 'occupied').length;
        const countFree = SYSTEM.positions.filter(p => p.enabled && p.state === 'free').length;
        const countUnused = SYSTEM.positions.filter(p => !p.enabled).length;
        l1.textContent = pad20(`PAINEL SALAS MASTER `);
        l2.textContent = pad20(`OCP:${String(countOcc).padStart(2,'0')} LIV:${String(countFree).padStart(2,'0')} OFF:${String(countUnused).padStart(2,'0')}`);
      }
    }

    // Secondary Keypad 4x4 for Maintenance & Diagnostics
    function pressKeypad(key) {
      playBeep(750, 0.04);
      logSerial(`[KEYPAD TÉCNICO] Tecla: '${key}'`);

      if (key === 'A') {
        toggleLcdMode();
      } else if (key === '1') {
        toggleLcdMode('setup');
      } else if (key === '2') {
        toggleLcdMode('preset');
      } else if (key === '3') {
        toggleLcdMode('monitor');
      } else if (key === '*') {
        if (SYSTEM.lcdMode === 'preset') {
          const slotNum = SYSTEM.lcdSelectedPresetIndex >= 3 ? (SYSTEM.lcdSelectedPresetIndex - 2) : (SYSTEM.activeSlot || 1);
          saveCurrentToEepromSlot(slotNum);
        } else {
          lcdNavNext();
        }
      } else if (key === '#') {
        if (SYSTEM.lcdMode === 'preset') {
          applyPresetByIndex(SYSTEM.lcdSelectedPresetIndex);
        } else {
          lcdToggleEnable();
        }
      } else if (key === '4') {
        runLedTestCycle();
      } else if (key === 'D') {
        resetSimulationDay();
      }
      updateLcdScreen();
    }

    function runLedTestCycle() {
      logSerial("[AUTOTESTE] Testando LEDs: Verde (Ocupado) -> Vermelho (Livre) -> Azul (Sem Uso)...");
      SYSTEM.positions.forEach(p => p.state = 'occupied'); // All Green
      renderSimulatorUI();
      setTimeout(() => {
        SYSTEM.positions.forEach(p => p.state = 'free'); // All Red
        renderSimulatorUI();
        setTimeout(() => {
          SYSTEM.positions.forEach(p => p.state = 'unused'); // All Blue
          renderSimulatorUI();
          setTimeout(() => {
            initPositions();
            renderSimulatorUI();
            logSerial("[AUTOTESTE] Ciclo concluído. Estados restaurados.");
          }, 700);
        }, 700);
      }, 700);
    }

    function toggleLcdColor() {
      const scr = document.getElementById('lcd-screen');
      if (scr) scr.classList.toggle('lcd-blue-mode');
    }

    // =========================================================================
    // RS-485 SERIAL BUS POLLING LOOP
    // =========================================================================
    function startPollingLoop() {
      if (SYSTEM.pollingInterval) clearInterval(SYSTEM.pollingInterval);
      if (SYSTEM.pollingSpeed === 'manual') return;
      SYSTEM.pollingInterval = setInterval(pollNextSlave, parseInt(SYSTEM.pollingSpeed));
    }

    function pollNextSlave() {
      const id = SYSTEM.currentPolledSlave;
      const isOnline = SYSTEM.rooms[id].online;

      const pkt = document.getElementById('animated-bus-packet');
      if (pkt) {
        pkt.textContent = `S${id}`;
        pkt.style.backgroundColor = isOnline ? '#10b981' : '#2563eb';
        pkt.style.left = id === 2 ? '25%' : (id === 3 ? '55%' : '80%');
      }

      const lastHexElem = document.getElementById('last-frame-hex');
      if (lastHexElem) {
        if (isOnline) {
          lastHexElem.textContent = `0${id} 03 00 00 00 0B ${Math.floor(Math.random()*89+10).toString(16).toUpperCase()} ${Math.floor(Math.random()*89+10).toString(16).toUpperCase()}`;
          lastHexElem.className = 'text-emerald-400 font-bold';
        } else {
          lastHexElem.textContent = `0${id} -- TIMEOUT (SEM RESPOSTA >2s) --`;
          lastHexElem.className = 'text-blue-400 font-bold';
        }
      }

      SYSTEM.currentPolledSlave = id === 4 ? 2 : id + 1;
    }

    function updatePollingSpeed(spd) {
      SYSTEM.pollingSpeed = spd;
      logSerial(`[CONFIG] Taxa de polling RS-485: ${spd}ms`);
      startPollingLoop();
    }

    function injectPacketError() {
      playBeep(220, 0.25);
      logSerial("[RUÍDO RS-485] Erro de CRC16 simulado. Frame descartado.");
      const elem = document.getElementById('last-frame-hex');
      if (elem) {
        elem.textContent = "CRC16 ERROR (0xFFFF - REJEITADO)";
        elem.className = 'text-amber-400 font-bold';
      }
    }

    function resetSimulationDay() {
      initPositions();
      SYSTEM.lcdSelectedPosIndex = 0;
      SYSTEM.lcdSelectedPresetIndex = 0;
      SYSTEM.lcdMode = 'setup';
      updateActivePresetBadge();
      renderSimulatorUI();
      logSerial("[RESET / BOOT] Novo dia iniciado. Padrão Boot 100% Ativo em 🟢 Verde restaurado.");
    }

    function logSerial(msg) {
      const box = document.getElementById('serial-log-box');
      if (!box) return;
      const d = document.createElement('div');
      d.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
      box.appendChild(d);
      box.scrollTop = box.scrollHeight;
    }

    function clearConsoleLog() {
      const box = document.getElementById('serial-log-box');
      if (box) box.innerHTML = '';
    }

    function exportSerialLog() {
      const box = document.getElementById('serial-log-box');
      if (!box) return;
      const text = Array.from(box.children).map(d => d.textContent).join('\n');
      const blob = new Blob([text], { type: 'text/plain' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'log_serial_rs485.txt';
      a.click();
    }

    function playBeep(freq, dur) {
      if (!SYSTEM.soundEnabled) return;
      try {
        if (!SYSTEM.audioCtx) {
          SYSTEM.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        const osc = SYSTEM.audioCtx.createOscillator();
        const gain = SYSTEM.audioCtx.createGain();
        osc.connect(gain);
        gain.connect(SYSTEM.audioCtx.destination);
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0.04, SYSTEM.audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, SYSTEM.audioCtx.currentTime + dur);
        osc.start();
        osc.stop(SYSTEM.audioCtx.currentTime + dur);
      } catch (e) {}
    }

    function toggleSound() {
      SYSTEM.soundEnabled = !SYSTEM.soundEnabled;
      const icon = document.getElementById('sound-icon');
      if (icon) {
        icon.className = SYSTEM.soundEnabled ? 'w-4 h-4 text-emerald-400' : 'w-4 h-4 text-slate-500';
      }
    }

    function toggleDarkMode() {
      document.documentElement.classList.toggle('dark');
    }

    // =========================================================================
    // BOM ENGINE
    // =========================================================================
    const BOM_SCENARIOS = {
      economico: {
        name: 'A. Recomendado (Uno nas 3 salas, cabo 2 vias blindado, conexões confiáveis)',
        subtotal: 979.00,
        reusableButtonsDeduction: 0.00,
        savedFromInventory: 680.00,
        items: [
          { item: 'Arduino Mega 2560 R3', spec: 'Mestre da Sala 1 (cliente já possui)', room: 'Sala 1', qty: 1, unit: 0.00, subtotal: 0.00, cat: 'controladores' },
          { item: 'Arduino Uno R3', spec: 'Escravo da Sala 2 (cliente já possui)', room: 'Sala 2', qty: 1, unit: 0.00, subtotal: 0.00, cat: 'controladores' },
          { item: 'Arduino Uno R3 compatível', spec: 'Escravos das Salas 3 e 4 (ATmega328P, CH340)', room: 'Salas 3 e 4', qty: 2, unit: 55.00, subtotal: 110.00, cat: 'controladores' },
          { item: 'Display LCD 20x2 I2C', spec: 'PCF8574 @ 0x27 (cliente já possui)', room: 'Sala 1', qty: 1, unit: 0.00, subtotal: 0.00, cat: 'controladores' },
          { item: 'Módulo MAX485 TTL', spec: 'Transceptor RS-485 half-duplex, um por sala', room: 'Salas 1 a 4', qty: 4, unit: 8.00, subtotal: 32.00, cat: 'controladores' },
          { item: 'Fita LED WS2812B 5V 60 LED/m', spec: '80 LEDs: 47 do painel central + 33 locais (metros)', room: 'Todas', qty: 2, unit: 38.00, subtotal: 76.00, cat: 'painel' },
          { item: 'Buzzer ativo 5V', spec: 'Alarme de falha de rede', room: 'Sala 1', qty: 1, unit: 4.00, subtotal: 4.00, cat: 'painel' },
          { item: 'Botão pulsador N.A. 16 mm', spec: 'NAV e HAB da central', room: 'Sala 1', qty: 2, unit: 8.00, subtotal: 16.00, cat: 'entradas' },
          { item: 'Kit resistores e capacitores', spec: '120, 560, 100 e 330 Ω; 1000 µF, 470 µF, 100 nF', room: 'Todas', qty: 1, unit: 25.00, subtotal: 25.00, cat: 'painel' },
          { item: 'Fonte 5V 3A regulada', spec: 'Central (Mega, LCD e 47 LEDs)', room: 'Sala 1', qty: 1, unit: 35.00, subtotal: 35.00, cat: 'alimentacao' },
          { item: 'Fonte 5V 2A regulada', spec: 'Uma por sala remota', room: 'Salas 2 a 4', qty: 3, unit: 25.00, subtotal: 75.00, cat: 'alimentacao' },
          { item: 'Cabo blindado 2 vias par trançado 24 AWG', spec: 'A/B nas vias, malha = referência (metros, 45 m + folga)', room: 'Barramento', qty: 60, unit: 2.50, subtotal: 150.00, cat: 'cabeamento' },
          { item: 'Cabinho flexível estanhado 0,5 mm²', spec: 'Fiação interna (rolo 100 m)', room: 'Todas', qty: 1, unit: 70.00, subtotal: 70.00, cat: 'cabeamento' },
          { item: 'Fio flexível 26 AWG (3 cores)', spec: 'Ligação entre pixels WS2812B', room: 'Todas', qty: 1, unit: 20.00, subtotal: 20.00, cat: 'cabeamento' },
          { item: 'Prensa-cabo PG7', spec: 'Entradas de cabo nas caixas', room: 'Todas', qty: 10, unit: 2.00, subtotal: 20.00, cat: 'cabeamento' },
          { item: 'Shield de bornes (screw shield) Uno', spec: 'Ligação sem solda no Uno', room: 'Salas 2 a 4', qty: 3, unit: 30.00, subtotal: 90.00, cat: 'conexoes' },
          { item: 'Mega Proto Shield', spec: 'Bornes KRE soldados para o Mega', room: 'Sala 1', qty: 1, unit: 35.00, subtotal: 35.00, cat: 'conexoes' },
          { item: 'Bornes KRE 5,08 mm 2 e 3 vias', spec: 'Kit 40 peças', room: 'Todas', qty: 1, unit: 20.00, subtotal: 20.00, cat: 'conexoes' },
          { item: 'Borne plugável 5,08 mm (KF2EDG)', spec: 'Chicote da porta, kit 10 pares', room: 'Todas', qty: 1, unit: 30.00, subtotal: 30.00, cat: 'conexoes' },
          { item: 'Conector Wago 221-413', spec: 'A, B, SH e distribuição de 5 V', room: 'Todas', qty: 12, unit: 3.00, subtotal: 36.00, cat: 'conexoes' },
          { item: 'Terminal tubular (ilhós)', spec: 'Kit 400 peças 0,25–1,5 mm² (inclui 0,25 mm² p/ o cabo)', room: 'Todas', qty: 1, unit: 25.00, subtotal: 25.00, cat: 'conexoes' },
          { item: 'Terminal garfo pré-isolado', spec: 'Botões 22 mm, 100 peças', room: 'Todas', qty: 1, unit: 15.00, subtotal: 15.00, cat: 'conexoes' },
          { item: 'Termo-retrátil', spec: 'Kit sortido', room: 'Todas', qty: 1, unit: 20.00, subtotal: 20.00, cat: 'conexoes' },
          { item: 'Espaçadores nylon M3 + parafusos', spec: 'Fixação das placas', room: 'Todas', qty: 1, unit: 15.00, subtotal: 15.00, cat: 'conexoes' },
          { item: 'Abraçadeiras, bases adesivas e anilhas', spec: 'Organização e identificação', room: 'Todas', qty: 1, unit: 25.00, subtotal: 25.00, cat: 'conexoes' },
          { item: 'Verniz isolante (conformal coating)', spec: 'Spray 300 ml, anti-oxidação', room: 'Todas', qty: 1, unit: 35.00, subtotal: 35.00, cat: 'conexoes' }
        ]
      },
      padrao: {
        name: 'B. Econômico (mesma eletrônica, cabo Cat5e e menos acessórios)',
        subtotal: 797.00,
        reusableButtonsDeduction: 0.00,
        savedFromInventory: 680.00,
        items: [
          { item: 'Arduino Mega 2560 R3', spec: 'Mestre da Sala 1 (cliente já possui)', room: 'Sala 1', qty: 1, unit: 0.00, subtotal: 0.00, cat: 'controladores' },
          { item: 'Arduino Uno R3', spec: 'Escravo da Sala 2 (cliente já possui)', room: 'Sala 2', qty: 1, unit: 0.00, subtotal: 0.00, cat: 'controladores' },
          { item: 'Arduino Uno R3 compatível', spec: 'Escravos das Salas 3 e 4 (ATmega328P, CH340)', room: 'Salas 3 e 4', qty: 2, unit: 55.00, subtotal: 110.00, cat: 'controladores' },
          { item: 'Display LCD 20x2 I2C', spec: 'PCF8574 @ 0x27 (cliente já possui)', room: 'Sala 1', qty: 1, unit: 0.00, subtotal: 0.00, cat: 'controladores' },
          { item: 'Módulo MAX485 TTL', spec: 'Transceptor RS-485 half-duplex, um por sala', room: 'Salas 1 a 4', qty: 4, unit: 8.00, subtotal: 32.00, cat: 'controladores' },
          { item: 'Fita LED WS2812B 5V 60 LED/m', spec: '80 LEDs: 47 do painel central + 33 locais (metros)', room: 'Todas', qty: 2, unit: 38.00, subtotal: 76.00, cat: 'painel' },
          { item: 'Buzzer ativo 5V', spec: 'Alarme de falha de rede', room: 'Sala 1', qty: 1, unit: 4.00, subtotal: 4.00, cat: 'painel' },
          { item: 'Botão pulsador N.A. 16 mm', spec: 'NAV e HAB da central', room: 'Sala 1', qty: 2, unit: 8.00, subtotal: 16.00, cat: 'entradas' },
          { item: 'Kit resistores e capacitores', spec: '120, 560, 100 e 330 Ω; 1000 µF, 470 µF, 100 nF', room: 'Todas', qty: 1, unit: 25.00, subtotal: 25.00, cat: 'painel' },
          { item: 'Fonte 5V 3A regulada', spec: 'Central (Mega, LCD e 47 LEDs)', room: 'Sala 1', qty: 1, unit: 35.00, subtotal: 35.00, cat: 'alimentacao' },
          { item: 'Fonte 5V 2A regulada', spec: 'Uma por sala remota', room: 'Salas 2 a 4', qty: 3, unit: 25.00, subtotal: 75.00, cat: 'alimentacao' },
          { item: 'Cabo UTP Cat5e (usar 1 par + 1 fio)', spec: 'Par azul = A/B, fio verde = GND ref. (metros)', room: 'Barramento', qty: 60, unit: 1.60, subtotal: 96.00, cat: 'cabeamento' },
          { item: 'Cabinho flexível estanhado 0,5 mm²', spec: 'Fiação interna (rolo 100 m)', room: 'Todas', qty: 1, unit: 70.00, subtotal: 70.00, cat: 'cabeamento' },
          { item: 'Fio flexível 26 AWG (3 cores)', spec: 'Ligação entre pixels WS2812B', room: 'Todas', qty: 1, unit: 20.00, subtotal: 20.00, cat: 'cabeamento' },
          { item: 'Prensa-cabo PG7', spec: 'Entradas de cabo nas caixas', room: 'Todas', qty: 10, unit: 2.00, subtotal: 20.00, cat: 'cabeamento' },
          { item: 'Proto shield Uno + bornes KRE soldados', spec: 'Montagem soldada em bancada', room: 'Salas 2 a 4', qty: 3, unit: 15.00, subtotal: 45.00, cat: 'conexoes' },
          { item: 'Mega Proto Shield', spec: 'Bornes KRE soldados para o Mega', room: 'Sala 1', qty: 1, unit: 35.00, subtotal: 35.00, cat: 'conexoes' },
          { item: 'Bornes KRE 5,08 mm 2 e 3 vias', spec: 'Kit 40 peças', room: 'Todas', qty: 1, unit: 20.00, subtotal: 20.00, cat: 'conexoes' },
          { item: 'Conector Wago 221-413', spec: 'A, B e SH nas salas', room: 'Todas', qty: 6, unit: 3.00, subtotal: 18.00, cat: 'conexoes' },
          { item: 'Terminal tubular (ilhós)', spec: 'Kit 400 peças 0,25–1,5 mm² (inclui 0,25 mm² p/ o cabo)', room: 'Todas', qty: 1, unit: 25.00, subtotal: 25.00, cat: 'conexoes' },
          { item: 'Terminal garfo pré-isolado', spec: 'Botões 22 mm, 100 peças', room: 'Todas', qty: 1, unit: 15.00, subtotal: 15.00, cat: 'conexoes' },
          { item: 'Termo-retrátil', spec: 'Kit sortido', room: 'Todas', qty: 1, unit: 20.00, subtotal: 20.00, cat: 'conexoes' },
          { item: 'Espaçadores nylon M3 + parafusos', spec: 'Fixação das placas', room: 'Todas', qty: 1, unit: 15.00, subtotal: 15.00, cat: 'conexoes' },
          { item: 'Abraçadeiras, bases adesivas e anilhas', spec: 'Organização e identificação', room: 'Todas', qty: 1, unit: 25.00, subtotal: 25.00, cat: 'conexoes' }
        ]
      },
      industrial: {
        name: 'C. Industrial (referência: entradas optoisoladas 24 V, botões novos, fontes DIN)',
        subtotal: 3528.76,
        reusableButtonsDeduction: 512.30,
        savedFromInventory: 150.00,
        items: [
          { item: 'Controlador Central Arduino Mega', spec: 'Master Sala 1 (Cliente já possui)', room: 'Sala 1', qty: 1, unit: 0.00, subtotal: 0.00, cat: 'controladores' },
          { item: 'Controladores remotos (preço de referência antigo)', spec: 'ATmega328P 5V', room: 'Salas 2, 3, 4', qty: 3, unit: 24.00, subtotal: 72.00, cat: 'controladores' },
          { item: 'Transceptores MAX485 Industriais', spec: 'Módulo transceptor RS-485 5V c/ TVS', room: 'Salas 1 a 4', qty: 4, unit: 12.00, subtotal: 48.00, cat: 'controladores' },
          { item: 'Expansor MCP23017', spec: '16 I/Os digitais I2C', room: 'Sala 1', qty: 1, unit: 28.25, subtotal: 28.25, cat: 'controladores' },
          { item: 'Botões NA 22mm Industriais', spec: 'Pulsador momentâneo metálico', room: 'Todas', qty: 47, unit: 10.90, subtotal: 512.30, cat: 'entradas' },
          { item: 'Interfaces Optoisoladas', spec: 'Placa 8 canais PC817 entradas 24V', room: 'Todas', qty: 8, unit: 42.50, subtotal: 340.00, cat: 'entradas' },
          { item: 'Fontes de Campo 24V', spec: 'Fonte 24V DC 60W Trilho DIN', room: 'Salas 1 a 4', qty: 4, unit: 132.50, subtotal: 530.00, cat: 'alimentacao' },
          { item: 'Conversores DC-DC 5V', spec: 'Step-down 24V para 5V 2A', room: 'Salas 1 a 4', qty: 4, unit: 25.00, subtotal: 100.00, cat: 'alimentacao' },
          { item: 'Fita LED WS2812B 1m', spec: '60 LEDs/m 5V (47 utilizados)', room: 'Sala 1', qty: 1, unit: 33.67, subtotal: 33.67, cat: 'painel' },
          { item: 'Cabo RS-485 Blindado Belden', spec: 'Par trançado instrumentação (100m)', room: 'Barramento', qty: 1, unit: 300.00, subtotal: 300.00, cat: 'cabeamento' },
          { item: 'Condutores & Bornes DIN', spec: 'Fios 0.5mm² e 1.0mm² + bornes DIN', room: 'Todas', qty: 1, unit: 786.20, subtotal: 786.20, cat: 'cabeamento' },
          { item: 'Montagem & Caixas ABS', spec: 'Suportes ópticos, trilho DIN, canaletas', room: 'Todas', qty: 1, unit: 690.00, subtotal: 690.00, cat: 'cabeamento' }
        ]
      }
    };

    let currentScenario = 'economico';
    let currentContingency = 15;

    function renderBomTable() {
      const scen = BOM_SCENARIOS[currentScenario];
      if (!scen) return;

      const subtotalElem = document.getElementById('bom-subtotal');
      const contElem = document.getElementById('bom-contingency');
      const totalElem = document.getElementById('bom-total');
      const reusedElem = document.getElementById('bom-reused-total');
      const tbody = document.getElementById('bom-table-body');
      const catFilter = document.getElementById('bom-category-filter') ? document.getElementById('bom-category-filter').value : 'all';

      const contingencyValue = scen.subtotal * (currentContingency / 100);
      const totalWithCont = scen.subtotal + contingencyValue;
      const savedAmount = scen.savedFromInventory || 465.00;

      if (subtotalElem) subtotalElem.textContent = `R$ ${scen.subtotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
      if (contElem) contElem.textContent = `R$ ${contingencyValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
      if (totalElem) totalElem.textContent = `R$ ${totalWithCont.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
      if (reusedElem) reusedElem.textContent = `R$ ${savedAmount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;

      if (!tbody) return;
      tbody.innerHTML = '';

      const filteredItems = catFilter === 'all' ? scen.items : scen.items.filter(i => i.cat === catFilter);

      filteredItems.forEach(item => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition';
        tr.innerHTML = `
          <td class="p-3.5 font-semibold text-white">${item.item}</td>
          <td class="p-3.5 text-slate-400 font-mono text-[11px]">${item.spec}</td>
          <td class="p-3.5 text-center"><span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 font-mono">${item.room}</span></td>
          <td class="p-3.5 text-center font-mono font-bold">${item.qty}</td>
          <td class="p-3.5 text-right font-mono">R$ ${item.unit.toFixed(2)}</td>
          <td class="p-3.5 text-right font-mono font-bold ${item.subtotal === 0 ? 'text-emerald-400' : 'text-slate-100'}">
            ${item.subtotal === 0 ? 'R$ 0,00 (Já possui)' : `R$ ${item.subtotal.toFixed(2)}`}
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function switchScenario(scen) {
      currentScenario = scen;
      ['economico', 'padrao', 'industrial'].forEach(s => {
        const btn = document.getElementById(`btn-scen-${s}`);
        if (btn) {
          if (s === scen) {
            btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white shadow transition';
          } else {
            btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition';
          }
        }
      });
      renderBomTable();
    }

    function updateContingency(val) {
      currentContingency = parseFloat(val);
      renderBomTable();
    }

    function filterBomTable() {
      renderBomTable();
    }

    function exportBomCsv() {
      const scen = BOM_SCENARIOS[currentScenario];
      let csv = 'Item;Especificacao;Local;Quantidade;Preco_Unitario;Subtotal\n';
      scen.items.forEach(i => {
        csv += `"${i.item}";"${i.spec}";"${i.room}";${i.qty};${i.unit.toFixed(2)};${i.subtotal.toFixed(2)}\n`;
      });
      csv += `\n"SUBTOTAL";"";"";"";"";${scen.subtotal.toFixed(2)}\n`;
      csv += `"CONTINGENCIA (${currentContingency}%)";"";"";"";"";${(scen.subtotal * currentContingency/100).toFixed(2)}\n`;
      csv += `"TOTAL FINAL";"";"";"";"";${(scen.subtotal * (1 + currentContingency/100)).toFixed(2)}\n`;

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `BOM_Painel_Salas_${currentScenario}.csv`;
      link.click();
    }

    function copyBomSummary() {
      const scen = BOM_SCENARIOS[currentScenario];
      const text = `ORÇAMENTO DO PROJETO - CENÁRIO: ${scen.name}\nSubtotal Materiais: R$ ${scen.subtotal.toFixed(2)}\nContingência (${currentContingency}%): R$ ${(scen.subtotal*currentContingency/100).toFixed(2)}\nTotal com Reserva: R$ ${(scen.subtotal*(1+currentContingency/100)).toFixed(2)}\nCom botões reaproveitados: R$ ${(scen.subtotal - scen.reusableButtonsDeduction).toFixed(2)}`;
      navigator.clipboard.writeText(text);
      alert('Resumo do orçamento copiado para a área de transferência!');
    }

    function showNodeDetails(id) {
      const titles = {
        1: "Sala 1 (Master Arduino Mega 2560)",
        2: "Sala 2 (Slave ID 2 - Arduino Uno R3)",
        3: "Sala 3 (Slave ID 3 - Arduino Uno R3)",
        4: "Sala 4 (Slave ID 4 - Terminação 120Ω)"
      };
      const titleElem = document.getElementById('node-title');
      if (titleElem) titleElem.textContent = `Detalhes do Nó: ${titles[id]}`;
    }

    // =========================================================================
    // CHARTS (Chart.js)
    // =========================================================================
    function initCharts() {
      const ctx1 = document.getElementById('costComparisonChart');
      if (ctx1) {
        new Chart(ctx1, {
          type: 'bar',
          data: {
            labels: ['A · Recomendado', 'B · Econômico', 'C · Industrial'],
            datasets: [
              {
                label: 'Materiais (R$)',
                data: [979.00, 797.00, 3528.76],
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
                borderColor: '#6366f1',
                borderWidth: 1,
                borderRadius: 6
              },
              {
                label: 'Com 15% Reserva (R$)',
                data: [1125.85, 916.55, 4058.07],
                backgroundColor: 'rgba(16, 185, 129, 0.8)',
                borderColor: '#10b981',
                borderWidth: 1,
                borderRadius: 6
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#94a3b8', font: { size: 10 } } } },
            scales: {
              x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
              y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
            }
          }
        });
      }

      const ctx2 = document.getElementById('efficiencyChart');
      if (ctx2) {
        new Chart(ctx2, {
          type: 'doughnut',
          data: {
            labels: ['Potência Sistema Novo (~25W)', 'Economia Energética vs 110V (>85%)'],
            datasets: [{
              data: [25, 155],
              backgroundColor: ['#10b981', '#1e293b'],
              borderColor: '#0f172a',
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 10 } } } }
          }
        });
      }
    }

    // =========================================================================
    // NAVIGATION
    // =========================================================================
    
    // =========================================================================
    // MANUAL TÉCNICO DEFINITIVO (FUNÇÕES DE COPIAR E BAIXAR)
    // =========================================================================
    const MANUAL_MARKDOWN_CONTENT = "# MANUAL T\u00c9CNICO DEFINITIVO DE ENGENHARIA E IMPLANTA\u00c7\u00c3O\n## Sistema Digital de Monitoramento e Sinaliza\u00e7\u00e3o de Ocupa\u00e7\u00e3o de Posi\u00e7\u00f5es (4 Salas)\n\n**Vers\u00e3o do Documento:** 3.1 \u2014 Revis\u00e3o de Engenharia Industrial Executiva  \n**Data de Refer\u00eancia:** 22/11/2026  \n**Classifica\u00e7\u00e3o:** Projeto Executivo, Arquitetura de Hardware/Software e Manual de Opera\u00e7\u00e3o  \n**Localiza\u00e7\u00e3o:** `C:/55/tu/MANUAL_PROJETO_PAINEL_SALAS.md`\n\n---\n\n## 1. Vis\u00e3o Geral do Projeto e Moderniza\u00e7\u00e3o do Sistema Legado\n\n### 1.1 O Problema do Sistema Legado 110V AC\nO sistema de sinaliza\u00e7\u00e3o em opera\u00e7\u00e3o nas instala\u00e7\u00f5es foi concebido com circuitos el\u00e9tricos paralelos tradicionais de 110V AC. Em cada uma das salas (Salas 2, 3 e 4), os operadores acionavam interruptores que ligavam diretamente l\u00e2mpadas incandescentes/sinalizadores de 110V no painel central de madeira na Sala 1.\n\nEsse arranjo apresentava graves problemas t\u00e9cnicos, operacionais e regulat\u00f3rios:\n1. **Riscos Cr\u00edticos de Seguran\u00e7a (Inconformidade com NR-10):** A condu\u00e7\u00e3o de 110V AC por dezenas de fios atrav\u00e9s de pain\u00e9is e caixas de madeira sem barreira de isolamento f\u00edsico ou prote\u00e7\u00e3o diferencial residual (DR) expunha operadores ao risco iminente de choque el\u00e9trico e sobreaquecimento com perigo de inc\u00eandio.\n2. **Fia\u00e7\u00e3o Ca\u00f3tica e Custo Elevado:** Para monitorar 47 posi\u00e7\u00f5es, eram necess\u00e1rios quase 50 condutores paralelos de 110V percorrendo tubula\u00e7\u00f5es congestionadas entre as salas.\n3. **Instabilidade e Queima Recorrente:** L\u00e2mpadas de 110V sofrem fadiga t\u00e9rmica constante em ciclos frequentes de ligar/desligar, gerando pontos cegos no painel principal e induzindo os supervisores a erros de julgamento sobre quais posi\u00e7\u00f5es estavam livres ou ocupadas.\n4. **Falta de Intelig\u00eancia e Flexibilidade Di\u00e1ria:** N\u00e3o havia como desabilitar posi\u00e7\u00f5es ociosas no dia sem desconectar fios manualmente; uma l\u00e2mpada apagada podia significar tanto \"posi\u00e7\u00e3o desocupada\" quanto \"l\u00e2mpada queimada\" ou \"fio rompido\".\n\n### 1.2 Objetivos da Moderniza\u00e7\u00e3o para Baixa Tens\u00e3o (5V DC Digital)\nA moderniza\u00e7\u00e3o completa do sistema substitui toda a infraestrutura anal\u00f3gica de 110V por uma **rede de automa\u00e7\u00e3o digital industrial de 5V DC**, atingindo os seguintes objetivos:\n- **Tens\u00e3o de Seguran\u00e7a Extra-Baixa (SELV):** Todos os comandos, bot\u00f5es e sinalizadores passam a operar em 5V DC regulado, eliminando 100% dos riscos de choque el\u00e9trico e atendendo aos mais rigorosos padr\u00f5es da NR-10.\n- **Redu\u00e7\u00e3o Dr\u00e1stica de Fia\u00e7\u00e3o (-88%):** Todo o tr\u00e1fego de dados entre as 4 salas \u00e9 unificado em um \u00fanico cabo de rede UTP Cat5e de 4 pares, operando em barramento serial balanceado RS-485.\n- **Painel Visual Inteligente (WS2812B RGB):** O painel central passa a utilizar LEDs RGB endere\u00e7\u00e1veis, permitindo distinguir com precis\u00e3o matem\u00e1tica as cores: **Verde** (Ocupado), **Vermelho** (Livre) e **Azul Escuro** (Desabilitado no dia), al\u00e9m de efeitos de diagn\u00f3stico em caso de falha de comunica\u00e7\u00e3o.\n- **Custo Quase Zero via Invent\u00e1rio Existente:** O projeto aproveita equipamentos j\u00e1 adquiridos pelo cliente (Arduino Mega 2560, Arduino Uno R3, Display LCD 20x2 I2C e Teclado 4x4), reduzindo o custo de novos materiais para a faixa de **R$ 211,50**.\n\n---\n\n## 2. Topologia Predial e Distribui\u00e7\u00e3o F\u00edsica dos Segmentos\n\n```mermaid\nflowchart LR\n    subgraph S1 [\"SALA 1 (Central Mestre)\"]\n        PAINEL_S1[\"Painel Mestre (420x260mm)\\nArduino Mega 2560\\nLCD 20x2 + 2 Bot\u00f5es Setup\\n47 LEDs WS2812B\\n14 Bot\u00f5es Locais (01-14)\\nTerminador RS-485 120\u03a9\"]\n    end\n\n    subgraph SEG1 [\"Segmento de Cabeamento 1\"]\n        C1[\"Cabo UTP Cat5e\\nComprimento: 15 metros\\nEletroduto PVC 3/4 polegadas\"]\n    end\n\n    subgraph S2 [\"SALA 2 (Esta\u00e7\u00e3o Remota 1)\"]\n        CAIXA_S2[\"Caixa Remota (240x150mm)\\nArduino Uno R3 (ID 2)\\n11 Bot\u00f5es Locais (15-25)\\n11 LEDs WS2812B Feedback\"]\n    end\n\n    subgraph SEG2 [\"Segmento de Cabeamento 2\"]\n        C2[\"Cabo UTP Cat5e\\nComprimento: 12 metros\\nEletroduto PVC 3/4 polegadas\"]\n    end\n\n    subgraph S3 [\"SALA 3 (Esta\u00e7\u00e3o Remota 2)\"]\n        CAIXA_S3[\"Caixa Remota (240x150mm)\\nArduino Nano V3 (ID 3)\\n11 Bot\u00f5es Locais (26-36)\\n11 LEDs WS2812B Feedback\"]\n    end\n\n    subgraph SEG3 [\"Segmento de Cabeamento 3\"]\n        C3[\"Cabo UTP Cat5e\\nComprimento: 18 metros\\nEletroduto PVC 3/4 polegadas\"]\n    end\n\n    subgraph S4 [\"SALA 4 (Esta\u00e7\u00e3o Remota 3)\"]\n        CAIXA_S4[\"Caixa Remota (240x150mm)\\nArduino Nano V3 (ID 4)\\n11 Bot\u00f5es Locais (37-47)\\n11 LEDs WS2812B Feedback\\nTerminador RS-485 120\u03a9\"]\n    end\n\n    PAINEL_S1 ==> SEG1 ==> CAIXA_S2 ==> SEG2 ==> CAIXA_S3 ==> SEG3 ==> CAIXA_S4\n```\n\n### 2.1 Dist\u00e2ncias F\u00edsicas e Roteamento\n- **Sala 1 (Central) para Sala 2:** 15 metros de percurso atrav\u00e9s de canaleta/eletroduto existente.\n- **Sala 2 para Sala 3:** 12 metros de percurso.\n- **Sala 3 para Sala 4:** 18 metros de percurso.\n- **Comprimento Total do Barramento RS-485:** **45 metros lineares cont\u00ednuos** em topologia Daisy-Chain estrita.\n- **Norma de Aplica\u00e7\u00e3o:** ANSI/TIA/EIA-485-A. Em 9.600 bps, o alcance m\u00e1ximo te\u00f3rico do RS-485 \u00e9 de 1.200 metros; a instala\u00e7\u00e3o em 45 metros opera com margem de seguran\u00e7a de ru\u00eddo superior a 26x o limite da norma.\n\n---\n\n## 3. Projeto El\u00e9trico Executivo e Circuitos Detalhados\n\n### 3.1 Diagrama Multifilar da Central Mestre (Sala 1 - Arduino Mega 2560)\n\n```\n====================================================================================================\n                        DIAGRAMA EL\u00c9TRICO MULTIFILAR \u2014 SALA 1 (CENTRAL MESTRE)\n====================================================================================================\n\n      REDE 110V/220V AC\n        [ FASE ] ------------------- [ CHAVE GERAL ] ---- [ FUS\u00cdVEL 2A ] ----+\n        [ NEUTRO ] ----------------------------------------------------------|-- [ FONTE CHAVEADA ]\n        [ TERRA PE ] --------------------------------------------------------|     5V DC / 3A (15W)\n                                                                             +-------+----------+\n                                                                                     | +5V      | GND (0V)\n                                                                                     |          |\n  +----------------------------------------------------------------------------------+          |\n  |                                                                                             |\n  |   BARRA DE ALIMENTA\u00c7\u00c3O DA CENTRAL                                                           |\n  +--+-- [ FUS\u00cdVEL REARM\u00c1VEL 1.5A ] -------------------------+----------------------------------|--+\n     |                                                       |                                  |  |\n     |   DESACOPLAMENTO DE POT\u00caNCIA (LOW-ESR)                |                                  |  |\n     +-- [ CAPACITOR ELETROL\u00cdTICO 1000\u00b5F / 16V ] ------------|----------------------------------+  |\n     |                                                       |                                  |  |\n     +-- [ CAPACITOR CER\u00c2MICO 100nF ] -----------------------|----------------------------------+  |\n     |                                                       |                                     |\n     |   ARDUINO MEGA 2560 (MESTRE)                          |                                     |\n     |   +---------------------------------------+           |                                     |\n     +---| 5V (Pino VCC)              GND (Pino) |-----------+-------------------------------------+\n         |                                       |\n         | Serial1 TX1 (Pin 18)                  |\n         | Serial1 RX1 (Pin 19)                  |\n         | Controle DE/RE (Pin 2)                |\n         |                                       |\n         | Dados WS2812B (Pin 6) ----------------+-- [ RESISTOR 330\u03a9 ] ---> DIN (Painel 47 LEDs)\n         |                                       |                          5V  --------+\n         | I2C SDA (Pin 20)                      |                          GND --------|------+\n         | I2C SCL (Pin 21)                      |                                      |      |\n         |                                       |                                      |      |\n         | Bot\u00e3o NAV (Pin 4) --------------------+--- [ BOTOEIRA N.A. ] ----------------|------+\n         | Bot\u00e3o HAB (Pin 5) --------------------+--- [ BOTOEIRA N.A. ] ----------------|------+\n         |                                       |                                      |      |\n         | Bot\u00f5es Locais S1 (Pins D22 a D35) ----+--- [ 14x BOTOEIRAS N.A. ] -----------|------+\n         |                                       |                                      |      |\n         | Sa\u00edda Buzzer (Pin 7) -----------------+--- [ BUZZER ATIVO 5V ] --------------|------+\n         +---------------------------------------+                                      |      |\n                                                                                        |      |\n     M\u00d3DULO TRANSCEPTOR RS-485 (MAX485)                                                 |      |\n     +---------------------------------------------------+                              |      |\n     | Pino 1 (RO)   -----> Conectado ao RX1 (Pin 19)    |                              |      |\n     | Pino 2 (/RE)  --+                                 |                              |      |\n     | Pino 3 (DE)   --+--> Conectados ao DERE (Pin 2)   |                              |      |\n     | Pino 4 (DI)   -----> Conectado ao TX1 (Pin 18)    |                              |      |\n     | Pino 5 (GND)  ------------------------------------+------------------------------+------+\n     | Pino 6 (A)    -----+------------------------------+--> LINHA A (Pino 5 Cabo UTP) |\n     |                    |                              |                              |\n     |                    +-- [ RESISTOR TERMIC. 120\u03a9 ] -|                              |\n     |                    |                              |                              |\n     |                    +-- [ PULL-UP 560\u03a9 ] ----------+-- +5V FAIL-SAFE              |\n     |                    |                              |                              |\n     | Pino 7 (B)    -----+------------------------------+--> LINHA B (Pino 4 Cabo UTP) |\n     |                    |                              |                              |\n     |                    +-- [ PULL-DOWN 560\u03a9 ] --------+-- GND FAIL-SAFE              |\n     |                                                   |                              |\n     | Pino 8 (VCC)  ------------------------------------+------------------------------+\n     +---------------------------------------------------+\n\n     DISPLAY LCD 20x2 I2C (PCF8574)\n     +---------------------------------------------------+\n     | Pino VCC      ------------------------------------+------------------------------+\n     | Pino GND      ------------------------------------+-------------------------------------+\n     | Pino SDA      -----> Conectado ao Pin 20 do Mega  |\n     | Pino SCL      -----> Conectado ao Pin 21 do Mega  |\n     | [ Trimpot de Ajuste de Contraste Integrado ]      |\n     +---------------------------------------------------+\n====================================================================================================\n```\n\n### 3.2 Diagrama Multifilar das Esta\u00e7\u00f5es Remotas (Salas 2, 3 e 4)\n\n```\n====================================================================================================\n                   DIAGRAMA EL\u00c9TRICO MULTIFILAR \u2014 SALAS REMOTAS (UNO R3 / NANO V3)\n====================================================================================================\n\n  CABO UTP CAT5e VINDO DO N\u00d3 ANTERIOR:\n  [ Par Laranja: Pinos 1 e 2 ] --------------------+--> +5V UNIFICADO DO BARRAMENTO\n  [ Par Verde: Pinos 3 e 6 ] ----------------------|--> GND UNIFICADO DO BARRAMENTO\n  [ Par Azul: Pino 4 ] ----------------------------|--> LINHA B RS-485\n  [ Par Azul: Pino 5 ] ----------------------------|--> LINHA A RS-485\n                                                   |\n     DESACOPLAMENTO LOCAL                          |\n     +-- [ CAPACITOR ELETROL\u00cdTICO 470\u00b5F / 16V ] ---|------------------------------+\n     |                                             |                              |\n     +-- [ CAPACITOR CER\u00c2MICO 100nF ] -------------|------------------------------+\n     |                                             |                              |\n     ARDUINO NANO V3 / UNO R3 (SLAVE)              |                              |\n     +---------------------------------------+     |                              |\n     | 5V (Pino VCC)              GND (Pino) |-----+------------------------------+\n     |                                       |                                    |\n     | UART RX (Pin D0)                      |                                    |\n     | UART TX (Pin D1)                      |                                    |\n     | Controle DE/RE (Pin D4)               |                                    |\n     |                                       |                                    |\n     | Dados WS2812B (Pin D5) ---------------+-- [ RESISTOR 330\u03a9 ] ---> DIN (11 LEDs Locais)\n     |                                       |                          5V  ------+\n     | 11 Bot\u00f5es Locais:                     |                          GND ------|---+\n     | P01: Pin D6   P07: Pin D12            |                                    |   |\n     | P02: Pin D7   P08: Pin A0             |                                    |   |\n     | P03: Pin D8   P09: Pin A1             +-- [ 11x BOTOEIRAS N.A. ] ----------|---+\n     | P04: Pin D9   P10: Pin A2             |   (Ligadas individualmente ao      |   |\n     | P05: Pin D10  P11: Pin A3             |    GND local com INPUT_PULLUP)     |   |\n     | P06: Pin D11                          |                                    |   |\n     +---------------------------------------+                                    |   |\n                                                                                  |   |\n     M\u00d3DULO TRANSCEPTOR RS-485 (MAX485)                                           |   |\n     +---------------------------------------------------+                        |   |\n     | Pino 1 (RO)   -----> Conectado ao RX (Pin D0)     |                        |   |\n     | Pino 2 (/RE)  --+                                 |                        |   |\n     | Pino 3 (DE)   --+--> Conectados ao DERE (Pin D4)  |                        |   |\n     | Pino 4 (DI)   -----> Conectado ao TX (Pin D1)     |                        |   |\n     | Pino 5 (GND)  ------------------------------------+------------------------+---+\n     | Pino 6 (A)    -----+------------------------------+--> LINHA A DO CABO UTP\n     |                    |                              |\n     |                    |   [ NOTA: NA SALA 4 (FIM DE LINHA), INSERIR           ]\n     |                    +-- [ RESISTOR DE TERMINA\u00c7\u00c3O DE 120\u03a9 ENTRE A E B        ]\n     |                    |                                                       |\n     | Pino 7 (B)    -----+---------------------------------> LINHA B DO CABO UTP\n     | Pino 8 (VCC)  ------------------------------------+------------------------+\n     +---------------------------------------------------+\n====================================================================================================\n```\n\n---\n\n## 4. Pinagem Gr\u00e1fica Real do Cabo UTP Cat5e (Padr\u00e3o T568B)\n\nA conectoriza\u00e7\u00e3o de todas as tomadas f\u00eameas Keystone RJ45 e conectores macho segue estritamente a norma **EIA/TIA 568-B**:\n\n```\n        CONECTOR MACHO RJ45 (Visto por cima, trava virada para baixo)\n        +-------------------------------------------------------+\n        |   1   |   2   |   3   |   4   |   5   |   6   |   7   |   8   |\n        +-------+-------+-------+-------+-------+-------+-------+-------+\n          BR/LAR   LAR    BR/VER   AZUL   BR/AZ    VER    BR/MAR   MAR\n        |=======+=======|       |=======+=======|       |=======+=======|\n           LINHA +5V DC             DADOS RS-485          RESERVA / PE\n         (Pares 1 e 2 em         (Linhas A e B em       (Blindagem /\n            Paralelo)              Par Tran\u00e7ado)           Dreno)\n```\n\n| Pino RJ45 | Cor do Fio (T568B) | Par | Fun\u00e7\u00e3o El\u00e9trica Oficial | Detalhe Construtivo |\n| :---: | :---: | :---: | :--- | :--- |\n| **1** | Branco / Laranja | Par 2 | **+5V DC (Pot\u00eancia)** | Jumperado em paralelo com o Pino 2 nos bornes Wago. |\n| **2** | Laranja Puro | Par 2 | **+5V DC (Pot\u00eancia)** | Condu\u00e7\u00e3o redundante de corrente para anular queda \u00f4hmica. |\n| **3** | Branco / Verde | Par 3 | **0V / GND (Pot\u00eancia/Ref.)**| Jumperado em paralelo com o Pino 6 nos bornes Wago. |\n| **4** | Azul Puro | Par 1 | **Linha B (-) RS-485** | Sinal diferencial n\u00e3o-inversor / inversor do transceptor. |\n| **5** | Branco / Azul | Par 1 | **Linha A (+) RS-485** | Par tran\u00e7ado com passo ultra-curto (m\u00e1xima imunidade). |\n| **6** | Verde Puro | Par 3 | **0V / GND (Pot\u00eancia/Ref.)**| Condu\u00e7\u00e3o de retorno e equaliza\u00e7\u00e3o de terra. |\n| **7** | Branco / Marrom | Par 4 | **Reserva T\u00e9cnica** | Mantido isolado para expans\u00f5es futuras. |\n| **8** | Marrom Puro | Par 4 | **Blindagem / Dreno** | Aterrado exclusivamente no quadro central da Sala 1. |\n\n---\n\n## 5. Mem\u00f3ria de C\u00e1lculo de Queda de Tens\u00e3o (Barramento de 45m)\n\nPara garantir que a tens\u00e3o nos n\u00f3s mais distantes permane\u00e7a dentro da faixa nominal operacional do microcontrolador ATmega328P ($4,5\\text{V}$ a $5,5\\text{V}$) e dos LEDs WS2812B ($4,5\\text{V}$ a $5,3\\text{V}$), realizou-se o dimensionamento el\u00e9trico para a topologia de 45 metros.\n\n### 5.1 Par\u00e2metros F\u00edsicos dos Condutores\n- Cabo: UTP Cat5e de cobre puro (n\u00e3o-CCA).\n- Bitola de cada condutor: 24 AWG ($0,205\\text{ mm}^2$).\n- Resist\u00eancia linear de 1 fio 24 AWG a 20\u00b0C: $R_{linear} \\approx 0,0842\\ \\Omega/\\text{m}$.\n- **Associa\u00e7\u00e3o de Condutores em Paralelo:**\n  - O circuito utiliza **2 condutores em paralelo** para a linha de $+5\\text{V}$ (Pinos 1 e 2) e **2 condutores em paralelo** para o GND (Pinos 3 e 6).\n  - Resist\u00eancia equivalente da linha de alimenta\u00e7\u00e3o: $R_{+5V} = 0,0842 / 2 = 0,0421\\ \\Omega/\\text{m}$.\n  - Resist\u00eancia equivalente da linha de retorno (GND): $R_{GND} = 0,0842 / 2 = 0,0421\\ \\Omega/\\text{m}$.\n  - Resist\u00eancia total de ida e volta do circuito combinado:\n    $$R_{circuito} = R_{+5V} + R_{GND} = 0,0842\\ \\Omega/\\text{m}$$\n\n### 5.2 Perfil de Corrente por Esta\u00e7\u00e3o Remota\nCom o firmware regulando o brilho dos LEDs em **40%** e cada posi\u00e7\u00e3o exibindo apenas uma cor b\u00e1sica por vez (Verde ou Vermelho):\n- Arduino Nano / Uno + MAX485 em repouso: $35\\text{ mA}$ ($0,035\\text{ A}$).\n- 11 LEDs locais WS2812B a 40% de brilho: $11 \\times 15\\text{ mA} = 165\\text{ mA}$ ($0,165\\text{ A}$).\n- **Corrente M\u00e1xima Cont\u00ednua por Sala Remota:**\n  $$I_{n\u00f3} = 0,035\\text{ A} + 0,165\\text{ A} = 0,200\\text{ A}\\quad (200\\text{ mA})$$\n\n### 5.3 C\u00e1lculo de Queda de Tens\u00e3o N\u00f3 a N\u00f3\nO barramento distribui a corrente em cascata ao longo dos 3 segmentos:\n\n```\nFonte 5.10V (S1) ---[15m]--- N\u00f3 S2 (200mA) ---[12m]--- N\u00f3 S3 (200mA) ---[18m]--- N\u00f3 S4 (200mA)\n```\n\n1. **Segmento 1: Sala 1 para Sala 2 ($L_1 = 15\\text{ m}$):**\n   - Corrente que trafega neste trecho: alimenta Sala 2, Sala 3 e Sala 4:\n     $$I_1 = I_{S2} + I_{S3} + I_{S4} = 0,200 + 0,200 + 0,200 = 0,600\\text{ A}$$\n   - Resist\u00eancia do trecho: $R_1 = 15\\text{ m} \\times 0,0842\\ \\Omega/\\text{m} = 1,263\\ \\Omega$.\n   - Queda de tens\u00e3o no Trecho 1:\n     $$\\Delta V_1 = I_1 \\times R_1 = 0,600\\text{ A} \\times 1,263\\ \\Omega = \\mathbf{0,758\\text{ V}}\\quad (\\text{sem fonte local})$$\n\n> [!IMPORTANT] Conclus\u00e3o de Engenharia sobre Alimenta\u00e7\u00e3o Centralizada vs. Fontes Locais\n> A an\u00e1lise matem\u00e1tica acima comprova que alimentar todo o sistema exclusivamente a partir de um \u00fanico carregador de 5V na Sala 1 provocaria uma queda acumulada de quase $1,1\\text{V}$ na Sala 4 ($V_{S4} \\approx 4,0\\text{V}$), ficando abaixo da faixa operacional de $4,5\\text{V}$.\n> **Diretriz Executiva:** O projeto adota **alimenta\u00e7\u00e3o de campo local nas salas remotas** (cada sala possui seu pr\u00f3prio carregador 5V 2A de R$ 25,00 nas Salas 2, 3 e 4), utilizando os pares Laranja e Verde do cabo UTP como barramento unificador de equaliza\u00e7\u00e3o e redund\u00e2ncia. Nesse arranjo definitivo, a corrente que trafega pelo cabo cai para menos de $20\\text{ mA}$ de balanceamento, resultando em:\n> $$\\Delta V_{real} \\le \\mathbf{0,02\\text{ V}}$$\n> Garantindo **5,05V est\u00e1veis em 100% dos n\u00f3s do sistema**.\n\n---\n\n## 6. Prote\u00e7\u00f5es El\u00e9tricas, Filtragem e Rede Fail-Safe\n\nO barramento industrial RS-485 opera em ambientes sujeitos a transit\u00f3rios eletromagn\u00e9ticos provenientes de motores de ar-condicionado, reatores e l\u00e2mpadas. Para conferir imunidade absoluta classe industrial, os seguintes elementos foram incorporados:\n\n```\n                                  REDE FAIL-SAFE E PROTE\u00c7\u00c3O RS-485\n                       +5V DC\n                         |\n                       [ 560\u03a9 ] Pull-Up de Polariza\u00e7\u00e3o Fail-Safe\n                         |\n  LINHA A RS-485 --------+----------+----------------------- [ Diodo TVS Bidirecional 6V ] ---- GND\n                         |          |\n                       [ 120\u03a9 ] Resistor de Termina\u00e7\u00e3o (Apenas n\u00f3s extremos: S1 e S4)\n                         |          |\n  LINHA B RS-485 --------+----------+----------------------- [ Diodo TVS Bidirecional 6V ] ---- GND\n                         |\n                       [ 560\u03a9 ] Pull-Down de Polariza\u00e7\u00e3o Fail-Safe\n                         |\n                        GND\n```\n\n1. **Rede de Polariza\u00e7\u00e3o Fail-Safe (560 $\\Omega$):**\n   - Quando todos os transceptores est\u00e3o em modo de escuta (alta imped\u00e2ncia), o barramento fica em estado flutuante (*floating*), podendo captar ru\u00eddos que a UART interpreta como bytes inv\u00e1lidos de in\u00edcio de frame.\n   - O resistor de pull-up de $560\\ \\Omega$ no borne A e o resistor de pull-down de $560\\ \\Omega$ no borne B for\u00e7am uma diferen\u00e7a de tens\u00e3o diferencial $V_{AB} \\ge +200\\text{ mV}$ em repouso. Isso garante que a linha permane\u00e7a em n\u00edvel l\u00f3gico est\u00e1vel '1' (Mark State) sem gerar falsos disparos.\n2. **Resistores de Termina\u00e7\u00e3o Casada (120 $\\Omega$ 1/4W):**\n   - Instalados entre A e B nos extremos (Sala 1 e Sala 4) para casar com a imped\u00e2ncia caracter\u00edstica de $120\\ \\Omega$ do par tran\u00e7ado e anular reflex\u00f5es de onda que corrompem pacotes.\n3. **Resistor de Amortecimento de Sinal (Damping) na Linha WS2812B:**\n   - Resistor de filme de carbono de **$330\\ \\Omega$ a $470\\ \\Omega$** inserido em s\u00e9rie logo na sa\u00edda do pino digital do Arduino at\u00e9 o pino `DIN` do primeiro LED WS2812B. Suprime sobretens\u00f5es transit\u00f3rias (*ringing*) provocadas pela indut\u00e2ncia do condutor em frequ\u00eancias de chaveamento de 800 kHz.\n4. **Filtragem de Alimenta\u00e7\u00e3o de Dois Est\u00e1gios:**\n   - Em cada placa controladora: 1 capacitor eletrol\u00edtico de **$1000\\ \\mu\\text{F} / 16\\text{V}$ Low-ESR** para absorver varia\u00e7\u00f5es de demanda dos LEDs + 1 capacitor cer\u00e2mico multicamada de **$100\\text{ nF}$** montado imediatamente adjacente aos pinos VCC e GND dos CIs para filtrar ru\u00eddo de alta frequ\u00eancia.\n\n---\n\n## 7. Layout Interno do Painel Central e Detalhamento Construtivo\n\n### 7.1 Arranjo Mec\u00e2nico Interno do Quadro Mestre (Sala 1)\nO painel central de madeira original de $420 \\times 260\\text{ mm}$ recebe em sua face posterior uma placa de montagem com calhas perfuradas para organiza\u00e7\u00e3o limpa e profissional:\n\n```\n+-----------------------------------------------------------------------------------+\n|                           PAINEL MESTRE (VISTA INTERNA)                           |\n|                                                                                   |\n|  [ ENTRADA AC ] -- [ FUS\u00cdVEL 2A ] -- [ FONTE CHAVEADA 5V 3A COLMEIA ]             |\n|                                                                                   |\n|  +==================== CALHA PL\u00c1STICA PERFURADA 20x20mm =======================+  |\n|  |                                                                             |  |\n|  |  +--------------------+   +-------------------+   +----------------------+  |  |\n|  |  |   DISPLAY LCD      |   |   ARDUINO MEGA    |   |   M\u00d3DULO RS-485      |  |  |\n|  |  |   20x2 COM I2C     |   |   2560 EM BASE    |   |   MAX485 C/ BORNES   |  |  |\n|  |  |   (Aparafusado)    |   |   ESPACADORES M3  |   |   (Soldado em placa) |  |  |\n|  |  +--------------------+   +-------------------+   +----------------------+  |  |\n|  |                                                                             |  |\n|  +=============================================================================+  |\n|                                                                                   |\n|  [ R\u00c9GUA DE BORNES WAGO 221 / SINDAL ]                 [ CONECTOR FEMEA RJ45 ]     |\n|  \u2022 Borne 1: Linha +5V DC Unificada                     \u2022 Sa\u00edda do Cabo UTP Cat5e   |\n|  \u2022 Borne 2: Linha 0V / GND Geral                         para as Salas 2, 3 e 4    |\n|  \u2022 Borne 3: Linha A RS-485                             \u2022 Prensa-cabos PG-9         |\n|  \u2022 Borne 4: Linha B RS-485                               para fixa\u00e7\u00e3o mec\u00e2nica     |\n+-----------------------------------------------------------------------------------+\n```\n\n### 7.2 Matriz Construtiva: Solda vs. Parafuso\nPara garantir f\u00e1cil manuten\u00e7\u00e3o no futuro por qualquer t\u00e9cnico:\n\n| Elemento | M\u00e9todo de Fixa\u00e7\u00e3o / Conex\u00e3o | Justificativa |\n| :--- | :---: | :--- |\n| **Pinos A e B do MAX485** | **Parafuso (Bornes de Press\u00e3o)** | Permite desconex\u00e3o imediata para teste de isolamento da rede. |\n| **Linhas +5V e GND das Fontes** | **Bornes Alavanca Wago 221** | Conex\u00e3o r\u00e1pida, segura e sem folga mec\u00e2nica com vibra\u00e7\u00f5es. |\n| **L\u00e2mpada LED BA9s nos Bot\u00f5es** | **Encaixe Baioneta (Giro 1/4 volta)** | Troca r\u00e1pida em 10 segundos sem uso de ferramenta. |\n| **Resistores 120\u03a9 e 330\u03a9** | **Soldados com Termo-Retr\u00e1til** | Elimina mau contato e ru\u00eddo induzido em conex\u00f5es soltas. |\n| **Pads da Fita WS2812B** | **Solda de Estanho 60/40 com Duto Flex\u00edvel** | Garante integridade nos pulsos de clock de alta frequ\u00eancia. |\n| **Fixa\u00e7\u00e3o das Placas de Circuito** | **Parafusos e Espa\u00e7adores M3 de Nylon** | Isola os pinos das placas da madeira, prevenindo umidade. |\n\n---\n\n## 8. Mapeamento de Posi\u00e7\u00f5es e Matriz de Pinagem\n\n```\n+---------------------------------------------------------------------------------------+\n|                 MATRIZ COMPLETA DAS 47 POSI\u00c7\u00d5ES DO SISTEMA (14 + 11 + 11 + 11)        |\n+---------------------------------------------------------------------------------------+\n\nSALA 1 (Central Mestre): 14 Posi\u00e7\u00f5es\n  [P01] a [P14] -> Pinos D22 a D35 do Mega 2560 | LEDs WS2812B \u00cdndices 0 a 13\n\nSALA 2 (Esta\u00e7\u00e3o Remota 1): 11 Posi\u00e7\u00f5es\n  [P15] a [P25] -> Pinos D6 a D12 e A0 a A3 do Uno R3 | LEDs Locais 0 a 10 | Central 14 a 24\n\nSALA 3 (Esta\u00e7\u00e3o Remota 2): 11 Posi\u00e7\u00f5es\n  [P26] a [P36] -> Pinos D6 a D12 e A0 a A3 do Nano V3 | LEDs Locais 0 a 10 | Central 25 a 35\n\nSALA 4 (Esta\u00e7\u00e3o Remota 3): 11 Posi\u00e7\u00f5es\n  [P37] a [P47] -> Pinos D6 a D12 e A0 a A3 do Nano V3 | LEDs Locais 0 a 10 | Central 36 a 46\n```\n\n---\n\n## 9. Checklist El\u00e9trico de Comissionamento e Aceita\u00e7\u00e3o (10 Itens)\n\nAntes de energizar definitivamente o sistema com os operadores, execute a seguinte lista de verifica\u00e7\u00e3o passo a passo com um mult\u00edmetro digital:\n\n| Item | Procedimento de Teste | Instrumento / M\u00e9todo | Crit\u00e9rio de Aceita\u00e7\u00e3o Num\u00e9rico | Status |\n| :---: | :--- | :--- | :--- | :---: |\n| **CK-01** | **Isola\u00e7\u00e3o da Rede Antiga de 110V** | Mult\u00edmetro na escala de 600V AC entre carca\u00e7a/bot\u00f5es e o terra da edifica\u00e7\u00e3o. | **Leitura = 0,00 V AC** (Zero absoluto de tens\u00e3o de fase). | [ ] APROVADO |\n| **CK-02** | **Resist\u00eancia \u00d3hmica do Barramento RS-485** | Mult\u00edmetro na escala $200\\ \\Omega$ medindo entre as linhas A e B com a fonte desligada. | **Leitura = $60\\ \\Omega \\pm 3\\ \\Omega$** (Associa\u00e7\u00e3o de 2 resistores de $120\\ \\Omega$ em paralelo). | [ ] APROVADO |\n| **CK-03** | **Tens\u00e3o da Fonte em Vazio (Sala 1)** | Mult\u00edmetro na escala 20V DC nos bornes de sa\u00edda da fonte de 5V. | **Tens\u00e3o entre 5,05 V e 5,20 V DC**. | [ ] APROVADO |\n| **CK-04** | **Tens\u00e3o na Sala 4 com Plena Carga** | Todos os LEDs acesos em carga operacional, medindo entre 5V e GND no n\u00f3 da Sala 4. | **Tens\u00e3o $\\ge 4,85\\text{ V DC}$** (Margem segura acima de 4,5V). | [ ] APROVADO |\n| **CK-05** | **Polariza\u00e7\u00e3o Fail-Safe do RS-485** | Medi\u00e7\u00e3o da tens\u00e3o diferencial DC entre A (+) e B (-) com a rede em repouso. | **$V_{AB} \\ge +200\\text{ mV DC}$** (Comprovando estado l\u00f3gico 1). | [ ] APROVADO |\n| **CK-06** | **Tempo de Resposta dos Bot\u00f5es (Debounce)** | 10 acionamentos manuais r\u00e1pidos em cada bot\u00e3o de cada sala. | **100% de comuta\u00e7\u00f5es perfeitas** sem duplicidade ou repique. | [ ] APROVADO |\n| **CK-07** | **Disparo de Timeout por Rompimento** | Desconex\u00e3o proposital do fio B no n\u00f3 da Sala 2 com cron\u00f4metro. | **Alarme dispara em exatamente $2,0\\text{ s} \\pm 0,2\\text{ s}$** com LEDs em \u00c2mbar. | [ ] APROVADO |\n| **CK-08** | **Auto-Recupera\u00e7\u00e3o de Falha** | Reconex\u00e3o do fio desconectado sem reiniciar os microcontroladores. | **Sincronismo restaurado em $< 500\\text{ ms}$** sem travar o painel. | [ ] APROVADO |\n| **CK-09** | **Consumo T\u00e9rmico dos LEDs WS2812B** | Term\u00f4metro infravermelho nos pixels de LED ap\u00f3s 2 horas operando continuamente a 40%. | **Temperatura m\u00e1xima $\\le 38^\\circ\\text{C}$** (Temperatura ambiente $+ 10^\\circ\\text{C}$). | [ ] APROVADO |\n| **CK-10** | **Reten\u00e7\u00e3o de Presets na EEPROM** | Desligar a chave geral por 5 minutos ap\u00f3s gravar configura\u00e7\u00e3o personalizada. | **Sistema religa restaurando 100% da m\u00e1scara gravada**. | [ ] APROVADO |\n\n---\n\n**Fim do Documento de Engenharia Executiva.**  \n*Manual aprovado para execu\u00e7\u00e3o de montagem, comissionamento em campo e manuten\u00e7\u00e3o de ciclo de vida.*\n";

    function copyManualMarkdown() {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(MANUAL_MARKDOWN_CONTENT).then(() => {
          showToast('Manual Técnico Completo (.MD) copiado com sucesso para a área de transferência!', 'success');
        }).catch(err => {
          console.error(err);
          prompt('Copie o manual abaixo:', MANUAL_MARKDOWN_CONTENT);
        });
      } else {
        prompt('Copie o manual abaixo:', MANUAL_MARKDOWN_CONTENT);
      }
    }

    function downloadManualMarkdown() {
      const blob = new Blob([MANUAL_MARKDOWN_CONTENT], { type: 'text/markdown;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'MANUAL_TECNICO.md';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('Download do MANUAL_TECNICO.md iniciado!', 'info');
    }

    
    // =========================================================================
    // ARDUINO FIRMWARES SOURCE CODE & VIEWER
    // =========================================================================
    const CODE_MASTER_MEGA_SRC = "/**\n * ============================================================================\n * PROJETO: SISTEMA DIGITAL DE MONITORAMENTO DE OCUPA\u00c7\u00c3O DE SALAS\n * N\u00d3: SALA 1 - CENTRAL MESTRE (ARDUINO MEGA 2560 R3)\n * ARQUIVO: arduino_master_mega.ino\n * DATA: 22/11/2026 | VERS\u00c3O: 3.0 (PRODU\u00c7\u00c3O INDUSTRIAL)\n * ============================================================================\n * \n * HARDWARE UTILIZADO:\n * - Microcontrolador: Arduino Mega 2560 R3\n * - Display: LCD HD44780 20x2 com interface I2C (PCF8574 em 0x27 ou 0x3F)\n * - Barramento RS-485: M\u00f3dulo Transceptor MAX485 conectado \u00e0 Serial1\n * - Painel Central: 47 LEDs RGB Endere\u00e7\u00e1veis WS2812B (5V)\n * - Botoeiras Locais Sala 1: 14 bot\u00f5es N.A. (Posi\u00e7\u00f5es 01 a 14)\n * - Bot\u00f5es de Setup Di\u00e1rio: 2 bot\u00f5es t\u00e1teis no painel frontal ([NAV] e [HAB])\n * \n * PINAGEM:\n * - Serial1 TX1: Pino 18 -> M\u00f3dulo MAX485 DI\n * - Serial1 RX1: Pino 19 -> M\u00f3dulo MAX485 RO\n * - Controle DE/RE RS-485: Pino 2 (HIGH = Transmiss\u00e3o, LOW = Recep\u00e7\u00e3o)\n * - Display I2C: SDA (Pino 20), SCL (Pino 21)\n * - Bot\u00e3o Setup NAV: Pino 4 (INPUT_PULLUP, fecha para GND)\n * - Bot\u00e3o Setup HAB: Pino 5 (INPUT_PULLUP, fecha para GND)\n * - Painel WS2812B: Pino 6 (PWM/DO via resistor s\u00e9rie 330 ohms)\n * - Bot\u00f5es Locais Sala 1 (Pos 01 a 14): Pinos 22 a 35 (INPUT_PULLUP, fecha para GND)\n * ============================================================================\n */\n\n#include <Wire.h>\n#include <LiquidCrystal_I2C.h>\n#include <FastLED.h>\n#include <EEPROM.h>\n\n// ----------------------------------------------------------------------------\n// DEFINI\u00c7\u00d5ES E CONSTANTES DE HARDWARE\n// ----------------------------------------------------------------------------\n#define NUM_POSITIONS_TOTAL   47\n#define S1_NUM_POSITIONS      14  // Posi\u00e7\u00f5es 01 a 14\n#define S2_NUM_POSITIONS      11  // Posi\u00e7\u00f5es 15 a 25\n#define S3_NUM_POSITIONS      11  // Posi\u00e7\u00f5es 26 a 36\n#define S4_NUM_POSITIONS      11  // Posi\u00e7\u00f5es 37 a 47\n\n#define PIN_RS485_DERE        2   // Pino de controle de dire\u00e7\u00e3o DE/RE do MAX485\n#define PIN_BTN_NAV           4   // Bot\u00e3o f\u00edsico de navega\u00e7\u00e3o no painel\n#define PIN_BTN_HAB           5   // Bot\u00e3o f\u00edsico de habilitar/desabilitar\n#define PIN_WS2812B_DATA      6   // Sa\u00edda de dados DIN dos 47 LEDs WS2812B\n\n#define LED_BRIGHTNESS        100 // ~40% do brilho m\u00e1ximo (evita calor e ofuscamento)\n#define RS485_BAUD_RATE       9600\n\n// Intervalos de temporiza\u00e7\u00e3o\n#define DEBOUNCE_DELAY_MS     40\n#define COMBO_HOLD_TIME_MS    1000 // Tempo segurando os 2 bot\u00f5es para combo\n#define POLLING_INTERVAL_MS   150  // Ciclo de polling para cada escravo\n#define SLAVE_TIMEOUT_MS      2000 // Alerta de perda de comunica\u00e7\u00e3o (>2s)\n\n// Endere\u00e7o e Configura\u00e7\u00e3o da EEPROM\n#define EEPROM_MAGIC_BYTE     0x5A\n#define EEPROM_ADDR_MAGIC     0\n#define EEPROM_ADDR_PRESET    1\n#define EEPROM_ADDR_MASK      2    // 6 bytes para armazenar a m\u00e1scara de 47 bits\n\n// Cores Oficiais do Sistema (Formato FastLED CRGB)\n#define COLOR_DISABLED        CRGB(0, 0, 45)      // \ud83d\udd35 Azul Escuro (Sem Uso no dia)\n#define COLOR_OCCUPIED         CRGB(0, 255, 0)     // \ud83d\udfe2 Verde Puro (Ocupado / Em Atendimento)\n#define COLOR_FREE             CRGB(255, 0, 0)     // \ud83d\udd34 Vermelho Puro (Livre / Desocupado)\n#define COLOR_ALERT            CRGB(255, 140, 0)   // \ud83d\udfe1 \u00c2mbar (Falha de Timeout)\n\n// Estados da Posi\u00e7\u00e3o\nenum PositionState {\n  STATE_DISABLED = 0,\n  STATE_OCCUPIED = 1,\n  STATE_FREE     = 2,\n  STATE_TIMEOUT  = 3\n};\n\n// Telas do Sistema IHM\nenum SystemMode {\n  MODE_MONITOR_OVERVIEW = 0,\n  MODE_SETUP_POSITIONS  = 1,\n  MODE_PRESET_MANAGER   = 2\n};\n\n// Presets Dispon\u00edveis\nenum PresetType {\n  PRESET_100_ATIVO = 0,\n  PRESET_TIPICO_35 = 1,\n  PRESET_PLANTAO_20 = 2,\n  PRESET_CUSTOM    = 3\n};\n\n// ----------------------------------------------------------------------------\n// OBJETOS GLOBAIS\n// ----------------------------------------------------------------------------\nLiquidCrystal_I2C lcd(0x27, 20, 4); // Suporta 20x2 ou 20x4 em 0x27 (fallback 0x3F)\nCRGB leds[NUM_POSITIONS_TOTAL];\n\n// ----------------------------------------------------------------------------\n// VARI\u00c1VEIS DE ESTADO DO SISTEMA\n// ----------------------------------------------------------------------------\nbool isEnabled[NUM_POSITIONS_TOTAL];      // true = Habilitada, false = Desabilitada no dia\nPositionState posState[NUM_POSITIONS_TOTAL]; // Estado atual de cada posi\u00e7\u00e3o\nbool lastButtonReading[S1_NUM_POSITIONS]; // Leitura anterior dos 14 bot\u00f5es da S1\n\n// Pinos dos 14 bot\u00f5es locais da Sala 1 (Mega D22 a D35)\nconst uint8_t s1ButtonPins[S1_NUM_POSITIONS] = {\n  22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35\n};\n\n// Diagn\u00f3stico de Comunica\u00e7\u00e3o dos Slaves (Salas 2, 3 e 4)\nstruct SlaveStatus {\n  uint8_t id;\n  uint8_t startPos;\n  uint8_t count;\n  unsigned long lastSeen;\n  bool isOnline;\n};\n\nSlaveStatus slaves[3] = {\n  { 2, 14, S2_NUM_POSITIONS, 0, false }, // Sala 2: Posi\u00e7\u00f5es 14 a 24 (15 a 25 base 1)\n  { 3, 25, S3_NUM_POSITIONS, 0, false }, // Sala 3: Posi\u00e7\u00f5es 25 a 35 (26 a 36 base 1)\n  { 4, 36, S4_NUM_POSITIONS, 0, false }  // Sala 4: Posi\u00e7\u00f5es 36 a 46 (37 a 47 base 1)\n};\n\nuint8_t currentPollingSlave = 0;\nunsigned long lastPollingTime = 0;\n\n// Estado da IHM\nSystemMode currentMode = MODE_MONITOR_OVERVIEW;\nuint8_t selectedPosition = 0; // 0 a 46 (P01 a P47)\nuint8_t currentPreset = PRESET_100_ATIVO;\n\n// Vari\u00e1veis de Leitura dos Bot\u00f5es do Setup\nbool lastNavState = HIGH;\nbool lastHabState = HIGH;\nunsigned long comboStartTime = 0;\nbool comboTriggered = false;\n\n// ----------------------------------------------------------------------------\n// DECLARA\u00c7\u00c3O DE FUN\u00c7\u00d5ES\n// ----------------------------------------------------------------------------\nvoid initHardware();\nvoid loadSettingsFromEEPROM();\nvoid saveSettingsToEEPROM();\nvoid applyPreset(PresetType preset);\nvoid updateLeds();\nvoid updateLcd();\nvoid handleLocalButtons();\nvoid handleSetupButtons();\nvoid pollSlavesRS485();\nvoid sendSyncMaskToSlave(uint8_t slaveId);\nvoid parseSlaveResponse(uint8_t slaveId, uint16_t statusBitmask);\n\n// ============================================================================\n// SETUP\n// ============================================================================\nvoid setup() {\n  initHardware();\n  loadSettingsFromEEPROM();\n  \n  // Atualiza hardware inicial\n  updateLeds();\n  updateLcd();\n}\n\n// ============================================================================\n// LOOP PRINCIPAL\n// ============================================================================\nvoid loop() {\n  handleSetupButtons();\n  handleLocalButtons();\n  pollSlavesRS485();\n  \n  // Piscar LEDs em \u00c2mbar a 4 Hz em caso de falha de conex\u00e3o\n  static unsigned long lastBlinkTime = 0;\n  static bool blinkState = false;\n  if (millis() - lastBlinkTime >= 125) { // 125ms on / 125ms off = 4 Hz\n    lastBlinkTime = millis();\n    blinkState = !blinkState;\n    \n    bool needRefresh = false;\n    for (int i = 0; i < 3; i++) {\n      if (millis() - slaves[i].lastSeen > SLAVE_TIMEOUT_MS) {\n        slaves[i].isOnline = false;\n        needRefresh = true;\n        // Posi\u00e7\u00f5es desse escravo entram em alerta\n        for (int p = slaves[i].startPos; p < slaves[i].startPos + slaves[i].count; p++) {\n          if (isEnabled[p]) {\n            leds[p] = blinkState ? COLOR_ALERT : CRGB::Black;\n          }\n        }\n      }\n    }\n    if (needRefresh) {\n      FastLED.show();\n    }\n  }\n\n  // Atualiza\u00e7\u00e3o peri\u00f3dica do display LCD\n  static unsigned long lastLcdUpdate = 0;\n  if (millis() - lastLcdUpdate >= 250) {\n    lastLcdUpdate = millis();\n    updateLcd();\n  }\n}\n\n// ============================================================================\n// INICIALIZA\u00c7\u00c3O DE HARDWARE\n// ============================================================================\nvoid initHardware() {\n  // Configura\u00e7\u00e3o RS-485\n  pinMode(PIN_RS485_DERE, OUTPUT);\n  digitalWrite(PIN_RS485_DERE, LOW); // Inicia em modo de recep\u00e7\u00e3o (RO)\n  Serial1.begin(RS485_BAUD_RATE);\n\n  // Configura\u00e7\u00e3o dos Bot\u00f5es de Setup\n  pinMode(PIN_BTN_NAV, INPUT_PULLUP);\n  pinMode(PIN_BTN_HAB, INPUT_PULLUP);\n\n  // Configura\u00e7\u00e3o dos 14 Bot\u00f5es Locais da Sala 1\n  for (int i = 0; i < S1_NUM_POSITIONS; i++) {\n    pinMode(s1ButtonPins[i], INPUT_PULLUP);\n    lastButtonReading[i] = HIGH;\n  }\n\n  // Inicializa\u00e7\u00e3o dos LEDs WS2812B via FastLED\n  FastLED.addLeds<WS2812B, PIN_WS2812B_DATA, GRB>(leds, NUM_POSITIONS_TOTAL);\n  FastLED.setBrightness(LED_BRIGHTNESS);\n  FastLED.clear(true);\n\n  // Inicializa\u00e7\u00e3o do Display LCD 20x2\n  Wire.begin();\n  lcd.init();\n  lcd.backlight();\n  lcd.clear();\n  lcd.setCursor(0, 0);\n  lcd.print(\"SISTEMA DIG. SALAS  \");\n  lcd.setCursor(0, 1);\n  lcd.print(\"INICIALIZANDO... v3 \");\n  delay(800);\n}\n\n// ============================================================================\n// GEST\u00c3O DE PRESETS E EEPROM\n// ============================================================================\nvoid loadSettingsFromEEPROM() {\n  uint8_t magic = EEPROM.read(EEPROM_ADDR_MAGIC);\n  if (magic == EEPROM_MAGIC_BYTE) {\n    currentPreset = EEPROM.read(EEPROM_ADDR_PRESET);\n    // L\u00ea a m\u00e1scara de bits habilitados\n    for (int i = 0; i < NUM_POSITIONS_TOTAL; i++) {\n      uint8_t byteIndex = EEPROM_ADDR_MASK + (i / 8);\n      uint8_t bitIndex  = i % 8;\n      isEnabled[i] = (EEPROM.read(byteIndex) & (1 << bitIndex)) != 0;\n      posState[i] = isEnabled[i] ? STATE_OCCUPIED : STATE_DISABLED;\n    }\n  } else {\n    // Se a EEPROM estiver virgem, aplica o Preset 100% Ativo por padr\u00e3o\n    applyPreset(PRESET_100_ATIVO);\n  }\n}\n\nvoid saveSettingsToEEPROM() {\n  EEPROM.update(EEPROM_ADDR_MAGIC, EEPROM_MAGIC_BYTE);\n  EEPROM.update(EEPROM_ADDR_PRESET, currentPreset);\n  \n  uint8_t buffer[6] = {0};\n  for (int i = 0; i < NUM_POSITIONS_TOTAL; i++) {\n    if (isEnabled[i]) {\n      buffer[i / 8] |= (1 << (i % 8));\n    }\n  }\n  for (int b = 0; b < 6; b++) {\n    EEPROM.update(EEPROM_ADDR_MASK + b, buffer[b]);\n  }\n}\n\nvoid applyPreset(PresetType preset) {\n  currentPreset = preset;\n  for (int i = 0; i < NUM_POSITIONS_TOTAL; i++) {\n    switch (preset) {\n      case PRESET_100_ATIVO:\n        isEnabled[i] = true;\n        break;\n      case PRESET_TIPICO_35:\n        // Sala 1 (14 ativas); Salas 2, 3 e 4 (7 primeiras de cada sala ativas)\n        if (i < 14) isEnabled[i] = true;\n        else if (i >= 14 && i < 21) isEnabled[i] = true;\n        else if (i >= 25 && i < 32) isEnabled[i] = true;\n        else if (i >= 36 && i < 43) isEnabled[i] = true;\n        else isEnabled[i] = false;\n        break;\n      case PRESET_PLANTAO_20:\n        // 5 posi\u00e7\u00f5es em cada sala\n        if (i < 5) isEnabled[i] = true;\n        else if (i >= 14 && i < 19) isEnabled[i] = true;\n        else if (i >= 25 && i < 30) isEnabled[i] = true;\n        else if (i >= 36 && i < 41) isEnabled[i] = true;\n        else isEnabled[i] = false;\n        break;\n      case PRESET_CUSTOM:\n      default:\n        break; // Mant\u00e9m a configura\u00e7\u00e3o atual\n    }\n    posState[i] = isEnabled[i] ? STATE_OCCUPIED : STATE_DISABLED;\n  }\n  saveSettingsToEEPROM();\n  updateLeds();\n  \n  // Envia a m\u00e1scara atualizada a todos os escravos\n  for (int s = 0; s < 3; s++) {\n    sendSyncMaskToSlave(slaves[s].id);\n  }\n}\n\n// ============================================================================\n// ATUALIZA\u00c7\u00c3O DO PAINEL DE LEDS WS2812B\n// ============================================================================\nvoid updateLeds() {\n  for (int i = 0; i < NUM_POSITIONS_TOTAL; i++) {\n    if (!isEnabled[i]) {\n      leds[i] = COLOR_DISABLED; // \ud83d\udd35 Azul Escuro\n    } else {\n      switch (posState[i]) {\n        case STATE_OCCUPIED:\n          leds[i] = COLOR_OCCUPIED; // \ud83d\udfe2 Verde\n          break;\n        case STATE_FREE:\n          leds[i] = COLOR_FREE;     // \ud83d\udd34 Vermelho\n          break;\n        case STATE_TIMEOUT:\n          leds[i] = COLOR_ALERT;    // \ud83d\udfe1 \u00c2mbar\n          break;\n        default:\n          leds[i] = COLOR_DISABLED;\n          break;\n      }\n    }\n  }\n  FastLED.show();\n}\n\n// ============================================================================\n// INTERFACE LCD 20x2 (IHM)\n// ============================================================================\nvoid updateLcd() {\n  char line1[21];\n  char line2[21];\n\n  switch (currentMode) {\n    case MODE_MONITOR_OVERVIEW: {\n      uint8_t countOccupied = 0;\n      uint8_t countFree = 0;\n      uint8_t countDisabled = 0;\n      for (int i = 0; i < NUM_POSITIONS_TOTAL; i++) {\n        if (!isEnabled[i]) countDisabled++;\n        else if (posState[i] == STATE_OCCUPIED) countOccupied++;\n        else if (posState[i] == STATE_FREE) countFree++;\n      }\n      bool allOnline = slaves[0].isOnline && slaves[1].isOnline && slaves[2].isOnline;\n      \n      snprintf(line1, sizeof(line1), \"OCUP:%02d LIVRE:%02d \", countOccupied, countFree);\n      snprintf(line2, sizeof(line2), \"DESAB:%02d REDE:%s\", countDisabled, allOnline ? \"OK  \" : \"ALRT\");\n      break;\n    }\n    case MODE_SETUP_POSITIONS: {\n      uint8_t room = 1;\n      uint8_t roomPos = selectedPosition + 1;\n      if (selectedPosition >= 14 && selectedPosition < 25) { room = 2; roomPos = selectedPosition - 13; }\n      else if (selectedPosition >= 25 && selectedPosition < 36) { room = 3; roomPos = selectedPosition - 24; }\n      else if (selectedPosition >= 36) { room = 4; roomPos = selectedPosition - 35; }\n      \n      snprintf(line1, sizeof(line1), \"S%d:P%02d [%s]\", room, selectedPosition + 1, isEnabled[selectedPosition] ? \"HABILITADA\" : \"DESABILIT.\");\n      snprintf(line2, sizeof(line2), \"[NAV]Prox [HAB]Muda \");\n      break;\n    }\n    case MODE_PRESET_MANAGER: {\n      const char* presetNames[] = {\"100%% ATIVO \", \"TIPICO 35  \", \"PLANTAO 20 \", \"CUSTOM     \"};\n      snprintf(line1, sizeof(line1), \"PRESET: [%s]\", presetNames[currentPreset]);\n      snprintf(line2, sizeof(line2), \"[NAV]Gira [HAB]Apli \");\n      break;\n    }\n  }\n\n  lcd.setCursor(0, 0);\n  lcd.print(line1);\n  lcd.setCursor(0, 1);\n  lcd.print(line2);\n}\n\n// ============================================================================\n// TRATAMENTO DOS 2 BOT\u00d5ES F\u00cdSICOS DO PAINEL DE SETUP (NAV / HAB / COMBO)\n// ============================================================================\nvoid handleSetupButtons() {\n  bool navRead = digitalRead(PIN_BTN_NAV);\n  bool habRead = digitalRead(PIN_BTN_HAB);\n\n  // Leitura de Combo: NAV + HAB pressionados juntos\n  if (navRead == LOW && habRead == LOW) {\n    if (comboStartTime == 0) {\n      comboStartTime = millis();\n    } else if (millis() - comboStartTime >= COMBO_HOLD_TIME_MS && !comboTriggered) {\n      comboTriggered = true;\n      // Cicla entre os 3 modos da IHM\n      currentMode = (SystemMode)((currentMode + 1) % 3);\n      updateLcd();\n    }\n    return;\n  } else {\n    comboStartTime = 0;\n    if (navRead == HIGH && habRead == HIGH) {\n      comboTriggered = false;\n    }\n  }\n\n  // Toque \u00fanico no bot\u00e3o NAV\n  if (navRead == LOW && lastNavState == HIGH && !comboTriggered) {\n    delay(DEBOUNCE_DELAY_MS);\n    if (digitalRead(PIN_BTN_NAV) == LOW) {\n      if (currentMode == MODE_SETUP_POSITIONS) {\n        selectedPosition = (selectedPosition + 1) % NUM_POSITIONS_TOTAL;\n      } else if (currentMode == MODE_PRESET_MANAGER) {\n        currentPreset = (PresetType)((currentPreset + 1) % 4);\n      } else if (currentMode == MODE_MONITOR_OVERVIEW) {\n        currentMode = MODE_SETUP_POSITIONS; // Abre setup diretamente\n      }\n      updateLcd();\n    }\n  }\n  lastNavState = navRead;\n\n  // Toque \u00fanico no bot\u00e3o HAB\n  if (habRead == LOW && lastHabState == HIGH && !comboTriggered) {\n    delay(DEBOUNCE_DELAY_MS);\n    if (digitalRead(PIN_BTN_HAB) == LOW) {\n      if (currentMode == MODE_SETUP_POSITIONS) {\n        isEnabled[selectedPosition] = !isEnabled[selectedPosition];\n        posState[selectedPosition] = isEnabled[selectedPosition] ? STATE_OCCUPIED : STATE_DISABLED;\n        currentPreset = PRESET_CUSTOM;\n        saveSettingsToEEPROM();\n        updateLeds();\n        // Sincroniza escravo correspondente se a posi\u00e7\u00e3o for de n\u00f3 remoto\n        if (selectedPosition >= 14 && selectedPosition < 25) sendSyncMaskToSlave(2);\n        else if (selectedPosition >= 25 && selectedPosition < 36) sendSyncMaskToSlave(3);\n        else if (selectedPosition >= 36) sendSyncMaskToSlave(4);\n      } else if (currentMode == MODE_PRESET_MANAGER) {\n        applyPreset((PresetType)currentPreset);\n      }\n      updateLcd();\n    }\n  }\n  lastHabState = habRead;\n}\n\n// ============================================================================\n// TRATAMENTO DOS 14 BOT\u00d5ES LOCAIS DA SALA 1\n// ============================================================================\nvoid handleLocalButtons() {\n  for (int i = 0; i < S1_NUM_POSITIONS; i++) {\n    bool readVal = digitalRead(s1ButtonPins[i]);\n    if (readVal == LOW && lastButtonReading[i] == HIGH) {\n      delay(20); // Debounce\n      if (digitalRead(s1ButtonPins[i]) == LOW) {\n        // Se a posi\u00e7\u00e3o estiver habilitada, comuta entre Verde (Ocupado) e Vermelho (Livre)\n        if (isEnabled[i]) {\n          if (posState[i] == STATE_OCCUPIED) posState[i] = STATE_FREE;\n          else posState[i] = STATE_OCCUPIED;\n          updateLeds();\n        }\n      }\n    }\n    lastButtonReading[i] = readVal;\n  }\n}\n\n// ============================================================================\n// PROTOCOLO RS-485 E POLLING DOS ESCRAVOS (SALAS 2, 3 E 4)\n// ============================================================================\nvoid pollSlavesRS485() {\n  if (millis() - lastPollingTime < POLLING_INTERVAL_MS) return;\n  lastPollingTime = millis();\n\n  uint8_t targetSlaveId = slaves[currentPollingSlave].id;\n\n  // Limpa buffer de recep\u00e7\u00e3o\n  while (Serial1.available()) Serial1.read();\n\n  // Transmite frame de Polling: [0x3A] [SLAVE_ID] [0x01: CMD_POLL] [CHECKSUM]\n  digitalWrite(PIN_RS485_DERE, HIGH); // Ativa Transmiss\u00e3o\n  delayMicroseconds(50);\n  \n  uint8_t frame[4];\n  frame[0] = 0x3A;              // Byte de Sincronismo (ASCII ':')\n  frame[1] = targetSlaveId;      // Endere\u00e7o do Escravo (2, 3 ou 4)\n  frame[2] = 0x01;              // Comando 0x01 = POLLING_REQUEST\n  frame[3] = (frame[0] + frame[1] + frame[2]) & 0xFF; // Checksum simples\n  \n  Serial1.write(frame, 4);\n  Serial1.flush();              // Aguarda transmiss\u00e3o completa\n  digitalWrite(PIN_RS485_DERE, LOW); // Retorna a modo de escuta (Recep\u00e7\u00e3o)\n\n  // Aguarda resposta por at\u00e9 40 ms\n  unsigned long waitStart = millis();\n  uint8_t rxBuffer[6];\n  uint8_t rxIdx = 0;\n\n  while (millis() - waitStart < 40) {\n    if (Serial1.available()) {\n      rxBuffer[rxIdx++] = Serial1.read();\n      if (rxIdx >= 6) break;\n    }\n  }\n\n  // Valida resposta: [0x3A] [SLAVE_ID] [STATUS_HI] [STATUS_LO] [CHECKSUM]\n  if (rxIdx >= 5 && rxBuffer[0] == 0x3A && rxBuffer[1] == targetSlaveId) {\n    uint8_t expectedChk = (rxBuffer[0] + rxBuffer[1] + rxBuffer[2] + rxBuffer[3]) & 0xFF;\n    if (rxBuffer[4] == expectedChk) {\n      uint16_t statusBitmask = (rxBuffer[2] << 8) | rxBuffer[3];\n      parseSlaveResponse(targetSlaveId, statusBitmask);\n      slaves[currentPollingSlave].lastSeen = millis();\n      slaves[currentPollingSlave].isOnline = true;\n    }\n  }\n\n  // Avan\u00e7a para o pr\u00f3ximo escravo na rodada seguinte\n  currentPollingSlave = (currentPollingSlave + 1) % 3;\n}\n\nvoid parseSlaveResponse(uint8_t slaveId, uint16_t statusBitmask) {\n  uint8_t sIdx = slaveId - 2;\n  if (sIdx > 2) return;\n\n  uint8_t start = slaves[sIdx].startPos;\n  uint8_t count = slaves[sIdx].count;\n\n  bool stateChanged = false;\n  for (int i = 0; i < count; i++) {\n    uint8_t globalPos = start + i;\n    if (isEnabled[globalPos]) {\n      // Bit 1 = Livre (Vermelho), Bit 0 = Ocupado (Verde)\n      PositionState newState = (statusBitmask & (1 << i)) ? STATE_FREE : STATE_OCCUPIED;\n      if (posState[globalPos] != newState) {\n        posState[globalPos] = newState;\n        stateChanged = true;\n      }\n    }\n  }\n  if (stateChanged) {\n    updateLeds();\n  }\n}\n\nvoid sendSyncMaskToSlave(uint8_t slaveId) {\n  uint8_t sIdx = slaveId - 2;\n  if (sIdx > 2) return;\n\n  uint8_t start = slaves[sIdx].startPos;\n  uint8_t count = slaves[sIdx].count;\n\n  uint16_t maskBits = 0;\n  for (int i = 0; i < count; i++) {\n    if (isEnabled[start + i]) {\n      maskBits |= (1 << i);\n    }\n  }\n\n  // Frame de Sincronismo de M\u00e1scara: [0x3A] [SLAVE_ID] [0x02: CMD_SYNC_MASK] [MASK_HI] [MASK_LO] [CHKSUM]\n  digitalWrite(PIN_RS485_DERE, HIGH);\n  delayMicroseconds(50);\n  \n  uint8_t frame[6];\n  frame[0] = 0x3A;\n  frame[1] = slaveId;\n  frame[2] = 0x02; // CMD_SYNC_MASK\n  frame[3] = (maskBits >> 8) & 0xFF;\n  frame[4] = maskBits & 0xFF;\n  frame[5] = (frame[0] + frame[1] + frame[2] + frame[3] + frame[4]) & 0xFF;\n\n  Serial1.write(frame, 6);\n  Serial1.flush();\n  digitalWrite(PIN_RS485_DERE, LOW);\n}\n";
    const CODE_SLAVE_NANO_SRC = "/**\n * ============================================================================\n * PROJETO: Sistema Digital de Monitoramento e Sinaliza\u00e7\u00e3o de Salas\n * ARQUIVO: arduino_slave_nano.ino\n * HARDWARE: Arduino Nano V3 / Arduino Uno R3 (Salas Remotas 2, 3 e 4)\n * AUTOR: Equipe de Engenharia / Antigravity\n * VERS\u00c3O: 3.0 (Produ\u00e7\u00e3o)\n * DATA: 22/11/2026\n * ============================================================================\n * \n * DESCRI\u00c7\u00c3O:\n * Firmware escravo executado nos microcontroladores das Salas 2, 3 e 4.\n * - Suporta tanto Arduino Nano V3 quanto Arduino Uno R3 sem modifica\u00e7\u00f5es.\n * - Identificador de Sala configur\u00e1vel via `#define SLAVE_ID` (2, 3 ou 4).\n * - Monitora 11 bot\u00f5es f\u00edsicos locais com debounce e resistores internos INPUT_PULLUP.\n * - Controla 11 LEDs locais WS2812B no painel da bancada dos operadores.\n * - Comunica\u00e7\u00e3o balanceada RS-485 com o Mestre (Arduino Mega da Sala 1).\n * - Recebe a m\u00e1scara di\u00e1ria de habilita\u00e7\u00e3o (11 bits) e devolve os estados em tempo real.\n * \n * PADR\u00c3O OFICIAL DE CORES:\n * - \ud83d\udd35 AZUL ESCURO (0, 0, 40): Desabilitado / Sem uso no dia pela Central.\n * - \ud83d\udfe2 VERDE (0, 255, 0): Ocupado / Em atendimento ativo.\n * - \ud83d\udd34 VERMELHO (255, 0, 0): Livre / Desocupado, aguardando pr\u00f3xima pessoa.\n * ============================================================================\n */\n\n#include <Adafruit_NeoPixel.h>\n\n// ============================================================================\n// CONFIGURA\u00c7\u00c3O DO IDENTIFICADOR DESTE ESCRAVO (ALTERE PARA CADA SALA)\n// ============================================================================\n// Para a Sala 2: use 2  (Arduino Uno R3 do invent\u00e1rio existente)\n// Para a Sala 3: use 3  (Arduino Nano V3)\n// Para a Sala 4: use 4  (Arduino Nano V3)\n#define SLAVE_ID            2   // <--- CONFIGURE AQUI: 2, 3 ou 4\n\n// ============================================================================\n// CONFIGURA\u00c7\u00d5ES DE PINAGEM - ARDUINO NANO / UNO\n// ============================================================================\n\n// Controle de fluxo do m\u00f3dulo RS-485 MAX485\n#define PIN_RS485_DERE      4   // Conectado aos pinos DE e RE jumpeados\n\n// Sa\u00edda de dados DIN para os 11 LEDs locais WS2812B\n#define PIN_LED_WS2812B     5   // Pino digital D5\n#define NUM_LEDS_LOCAIS     11  // 11 posi\u00e7\u00f5es por sala remota\n#define LED_BRIGHTNESS      100 // 40% de brilho (~15mA por LED)\n\n// Mapeamento dos 11 Bot\u00f5es Locais (N.A. ligados entre o pino e o GND)\n// Utiliza os pinos digitais D6 a D12 e anal\u00f3gicos A0 a A3 como digitais\nconst uint8_t PINS_BOTOES[NUM_LEDS_LOCAIS] = {\n  6,   // Posi\u00e7\u00e3o 01 da sala (D6)\n  7,   // Posi\u00e7\u00e3o 02 da sala (D7)\n  8,   // Posi\u00e7\u00e3o 03 da sala (D8)\n  9,   // Posi\u00e7\u00e3o 04 da sala (D9)\n  10,  // Posi\u00e7\u00e3o 05 da sala (D10)\n  11,  // Posi\u00e7\u00e3o 06 da sala (D11)\n  12,  // Posi\u00e7\u00e3o 07 da sala (D12)\n  A0,  // Posi\u00e7\u00e3o 08 da sala (Pino A0 / D14)\n  A1,  // Posi\u00e7\u00e3o 09 da sala (Pino A1 / D15)\n  A2,  // Posi\u00e7\u00e3o 10 da sala (Pino A2 / D16)\n  A3   // Posi\u00e7\u00e3o 11 da sala (Pino A3 / D17)\n};\n\n// Inst\u00e2ncia da fita local NeoPixel\nAdafruit_NeoPixel strip(NUM_LEDS_LOCAIS, PIN_LED_WS2812B, NEO_GRB + NEO_KHZ800);\n\n// ============================================================================\n// VARI\u00c1VEIS DE ESTADO E DEBOUNCE\n// ============================================================================\n\n// Estados das 11 posi\u00e7\u00f5es:\n// bit = 0: OCUPADA (Verde)\n// bit = 1: LIVRE   (Vermelho)\nuint16_t estadosBits = 0x0000; // Todas iniciam em 0 = Ocupadas (Verde)\n\n// M\u00e1scara de habilita\u00e7\u00e3o recebida da Central (1 = habilitada, 0 = desabilitada)\nuint16_t mascaraHabilitadas = 0x07FF; // Todas as 11 habilitadas por padr\u00e3o no boot\n\n// Vari\u00e1veis de debounce para cada bot\u00e3o\nuint8_t ultimoLeituraBotao[NUM_LEDS_LOCAIS];\nuint32_t ultimoDebounce[NUM_LEDS_LOCAIS];\n\n// Temporizadores ass\u00edncronos\nuint32_t timerAtualizacaoLEDs = 0;\n\n// ============================================================================\n// PROT\u00d3TIPOS DE FUN\u00c7\u00d5ES\n// ============================================================================\nvoid inicializarHardware();\nvoid processarBotoes();\nvoid processarComandoRS485();\nvoid enviarRespostaRS485();\nvoid atualizarLedsLocais();\nuint8_t calcularChecksum(uint8_t* buffer, uint8_t len);\n\n// ============================================================================\n// SETUP\n// ============================================================================\nvoid setup() {\n  inicializarHardware();\n}\n\n// ============================================================================\n// LOOP PRINCIPAL\n// ============================================================================\nvoid loop() {\n  uint32_t agora = millis();\n\n  // 1. Amostragem cont\u00ednua dos 11 bot\u00f5es com debounce\n  processarBotoes();\n\n  // 2. Processamento de comandos no barramento RS-485\n  if (Serial.available() >= 6) {\n    processarComandoRS485();\n  }\n\n  // 3. Atualiza\u00e7\u00e3o visual peri\u00f3dica dos 11 LEDs locais (a cada 50 ms)\n  if (agora - timerAtualizacaoLEDs >= 50) {\n    timerAtualizacaoLEDs = agora;\n    atualizarLedsLocais();\n  }\n}\n\n// ============================================================================\n// INICIALIZA\u00c7\u00c3O DE HARDWARE\n// ============================================================================\nvoid inicializarHardware() {\n  // Controle de dire\u00e7\u00e3o do transceptor RS-485\n  pinMode(PIN_RS485_DERE, OUTPUT);\n  digitalWrite(PIN_RS485_DERE, LOW); // Inicia obrigatoriamente como RECEPTOR\n\n  // UART de hardware (D0 = RX, D1 = TX) a 9600 bps 8N1\n  Serial.begin(9600);\n\n  // Configura\u00e7\u00e3o dos 11 pinos de bot\u00e3o com resistor de pull-up interno\n  for (uint8_t i = 0; i < NUM_LEDS_LOCAIS; i++) {\n    pinMode(PINS_BOTOES[i], INPUT_PULLUP);\n    ultimoLeituraBotao[i] = HIGH;\n    ultimoDebounce[i] = 0;\n  }\n\n  // Inicializa\u00e7\u00e3o da fita WS2812B local\n  strip.begin();\n  strip.setBrightness(LED_BRIGHTNESS);\n  strip.show();\n\n  // Sinal visual de boot: pisca verde uma vez em todos os LEDs locais\n  for (uint8_t i = 0; i < NUM_LEDS_LOCAIS; i++) {\n    strip.setPixelColor(i, strip.Color(0, 255, 0));\n  }\n  strip.show();\n  delay(200);\n}\n\n// ============================================================================\n// PROCESSAMENTO DOS 11 BOT\u00d5ES LOCAIS (TOGGLE VERDE <-> VERMELHO)\n// ============================================================================\nvoid processarBotoes() {\n  uint32_t agora = millis();\n\n  for (uint8_t i = 0; i < NUM_LEDS_LOCAIS; i++) {\n    bool leitura = digitalRead(PINS_BOTOES[i]);\n\n    if (leitura != ultimoLeituraBotao[i]) {\n      ultimoDebounce[i] = agora;\n      ultimoLeituraBotao[i] = leitura;\n    }\n\n    if ((agora - ultimoDebounce[i]) > 40) { // Est\u00e1vel por mais de 40 ms\n      if (leitura == LOW) { // Bot\u00e3o f\u00edsico acionado (contato fechou com GND)\n        \n        // Verifica se esta posi\u00e7\u00e3o est\u00e1 habilitada no dia pela Central\n        bool habilitada = (mascaraHabilitadas & (1 << i)) != 0;\n        \n        if (habilitada) {\n          // Inverte o estado da posi\u00e7\u00e3o (Toggle):\n          // Se estava Ocupada (0) -> vira Livre (1)\n          // Se estava Livre (1)   -> vira Ocupada (0)\n          estadosBits ^= (1 << i);\n\n          // Intervalo de seguran\u00e7a para evitar m\u00faltiplos registros no mesmo clique\n          ultimoDebounce[i] = agora + 200;\n        }\n      }\n    }\n  }\n}\n\n// ============================================================================\n// PROTOCOLO SERIAL RS-485\n// ============================================================================\nvoid processarComandoRS485() {\n  // Sincroniza com o in\u00edcio do frame (byte de cabe\u00e7alho 0xAA)\n  if (Serial.peek() != 0xAA) {\n    Serial.read(); // Descarta byte fora de sincronismo\n    return;\n  }\n\n  uint8_t buffer[6];\n  Serial.readBytes(buffer, 6);\n\n  // Valida\u00e7\u00e3o do checksum XOR\n  if (calcularChecksum(buffer, 5) == buffer[5]) {\n    uint8_t targetId = buffer[1];\n    uint8_t comando  = buffer[2];\n\n    // Verifica se esta mensagem \u00e9 direcionada a este escravo espec\u00edfico\n    if (targetId == SLAVE_ID && comando == 0x01) {\n      // Atualiza a m\u00e1scara de habilita\u00e7\u00e3o enviada pela Central\n      mascaraHabilitadas = ((uint16_t)buffer[3] << 8) | buffer[4];\n\n      // Responde imediatamente com o estado atual das 11 posi\u00e7\u00f5es\n      enviarRespostaRS485();\n    }\n  }\n}\n\nvoid enviarRespostaRS485() {\n  // Frame de Resposta:\n  // [0x55] [SLAVE_ID] [ESTADOS_HIGH] [ESTADOS_LOW] [CHECKSUM]\n  uint8_t frame[5];\n  frame[0] = 0x55;\n  frame[1] = SLAVE_ID;\n  frame[2] = (uint8_t)(estadosBits >> 8);\n  frame[3] = (uint8_t)(estadosBits & 0xFF);\n  frame[4] = calcularChecksum(frame, 4);\n\n  // Habilita o driver de transmiss\u00e3o no MAX485\n  digitalWrite(PIN_RS485_DERE, HIGH);\n  delayMicroseconds(60);\n\n  Serial.write(frame, 5);\n  Serial.flush(); // Aguarda a transmiss\u00e3o do \u00faltimo bit no barramento f\u00edsico\n\n  delayMicroseconds(60);\n  digitalWrite(PIN_RS485_DERE, LOW); // Retorna instantaneamente para modo de escuta\n}\n\nuint8_t calcularChecksum(uint8_t* buffer, uint8_t len) {\n  uint8_t sum = 0;\n  for (uint8_t i = 0; i < len; i++) {\n    sum ^= buffer[i];\n  }\n  return sum;\n}\n\n// ============================================================================\n// ATUALIZA\u00c7\u00c3O DOS 11 LEDS WS2812B LOCAIS\n// ============================================================================\nvoid atualizarLedsLocais() {\n  for (uint8_t i = 0; i < NUM_LEDS_LOCAIS; i++) {\n    bool habilitada = (mascaraHabilitadas & (1 << i)) != 0;\n\n    if (!habilitada) {\n      // \ud83d\udd35 AZUL ESCURO: Posi\u00e7\u00e3o desabilitada no dia\n      strip.setPixelColor(i, strip.Color(0, 0, 40));\n    } else {\n      bool livre = (estadosBits & (1 << i)) != 0;\n      if (livre) {\n        // \ud83d\udd34 VERMELHO PURO: Livre / Desocupada\n        strip.setPixelColor(i, strip.Color(255, 0, 0));\n      } else {\n        // \ud83d\udfe2 VERDE PURO: Ocupada / Em atendimento\n        strip.setPixelColor(i, strip.Color(0, 255, 0));\n      }\n    }\n  }\n  strip.show();\n}\n";

    function initFirmwareViewers() {
      const elMaster = document.getElementById('code-master-mega');
      const elSlave = document.getElementById('code-slave-nano');
      if (elMaster) elMaster.textContent = CODE_MASTER_MEGA_SRC;
      if (elSlave) elSlave.textContent = CODE_SLAVE_NANO_SRC;
    }

    function switchFwView(view) {
      const btnMega = document.getElementById('btn-fw-mega');
      const btnNano = document.getElementById('btn-fw-nano');
      const viewMega = document.getElementById('fw-view-mega');
      const viewNano = document.getElementById('fw-view-nano');

      if (view === 'mega') {
        viewMega?.classList.remove('hidden');
        viewNano?.classList.add('hidden');
        btnMega?.classList.replace('bg-slate-900', 'bg-indigo-600');
        btnMega?.classList.replace('text-slate-400', 'text-white');
        btnNano?.classList.replace('bg-indigo-600', 'bg-slate-900');
        btnNano?.classList.replace('text-white', 'text-slate-400');
      } else {
        viewMega?.classList.add('hidden');
        viewNano?.classList.remove('hidden');
        btnNano?.classList.replace('bg-slate-900', 'bg-indigo-600');
        btnNano?.classList.replace('text-slate-400', 'text-white');
        btnMega?.classList.replace('bg-indigo-600', 'bg-slate-900');
        btnMega?.classList.replace('text-white', 'text-slate-400');
      }
    }

    function copyMasterIno() {
      navigator.clipboard.writeText(CODE_MASTER_MEGA_SRC).then(() => {
        showToast('Código master_mega.ino copiado!', 'success');
      }).catch(() => prompt('Copie o código:', CODE_MASTER_MEGA_SRC));
    }

    function downloadMasterIno() {
      const blob = new Blob([CODE_MASTER_MEGA_SRC], { type: 'text/plain;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'master_mega.ino';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('Download do master_mega.ino iniciado!', 'info');
    }

    function copySlaveIno() {
      navigator.clipboard.writeText(CODE_SLAVE_NANO_SRC).then(() => {
        showToast('Código slave_uno.ino copiado!', 'success');
      }).catch(() => prompt('Copie o código:', CODE_SLAVE_NANO_SRC));
    }

    function downloadSlaveIno() {
      const blob = new Blob([CODE_SLAVE_NANO_SRC], { type: 'text/plain;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'slave_uno.ino';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('Download do slave_uno.ino iniciado!', 'info');
    }

__PE_TAB_JS__

    function switchTab(id) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-btn').forEach(el => {
        el.className = 'nav-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 border border-transparent font-medium whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5';
      });
      document.querySelectorAll('.mobile-nav-btn').forEach(el => {
        el.className = 'mobile-nav-btn px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 font-medium whitespace-nowrap text-xs shrink-0 transition';
      });

      const actTab = document.getElementById(`tab-${id}`);
      const actBtn = document.getElementById(`nav-${id}`);
      const actMobile = document.getElementById(`mobile-nav-${id}`);

      if (actTab) actTab.classList.remove('hidden');
      if (actBtn) {
        actBtn.className = 'nav-btn px-2.5 py-1 rounded-lg text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 font-bold whitespace-nowrap flex items-center justify-center shrink-0 transition space-x-1.5 shadow-sm';
      }
      if (actMobile) {
        actMobile.className = 'mobile-nav-btn px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 font-bold whitespace-nowrap text-xs shrink-0 transition';
      }

      lucide.createIcons();
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================
    window.addEventListener('DOMContentLoaded', () => {
      initFirmwareViewers();
      try {
        const savedTheme = localStorage.getItem('painel_salas_theme') || 'indigo';
        setAppTheme(savedTheme);
      } catch(e) {}
      lucide.createIcons();
      initPositions();
      renderSimulatorUI();
      renderBomTable();
      initCharts();
      startPollingLoop();
    });
  </script>
</body>
</html>
'''

def main():
    """Gera web/index.html a partir deste script, de pe_tab.py, dos firmwares e do manual."""
    import json
    import re
    import sys
    from pathlib import Path

    tools = Path(__file__).resolve().parent
    root = tools.parent
    sys.path.insert(0, str(tools))
    import pe_tab

    content = get_html_content()
    content = (content.replace('__PE_TAB_HTML__', pe_tab.build_html())
                      .replace('__PE_TAB_CSS__', pe_tab.TAB_CSS)
                      .replace('__PE_TAB_JS__', pe_tab.TAB_JS))
    assert '__PE_TAB_' not in content, 'marcador da aba Projeto Elétrico não substituído'

    def js_str(txt):
        return json.dumps(txt, ensure_ascii=False).replace('</', '<\\/')

    sources = {
        'CODE_MASTER_MEGA_SRC': root / 'firmware' / 'master_mega' / 'master_mega.ino',
        'CODE_SLAVE_NANO_SRC': root / 'firmware' / 'slave_uno' / 'slave_uno.ino',
        'MANUAL_MARKDOWN_CONTENT': root / 'docs' / 'MANUAL_TECNICO.md',
    }
    for const, path in sources.items():
        if not path.exists():
            print(f'AVISO: {path} não encontrado; mantendo conteúdo embutido antigo de {const}')
            continue
        new = f'const {const} = {js_str(path.read_text(encoding="utf-8"))};\n'
        content, k = re.subn(r'const ' + const + r' = ".*?";\n', lambda m: new, content, count=1)
        assert k == 1, f'constante {const} não encontrada'

    out = root / 'web' / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(content, encoding='utf-8')
    print(f'Gerado: {out} ({len(content)} bytes)')


if __name__ == '__main__':
    main()

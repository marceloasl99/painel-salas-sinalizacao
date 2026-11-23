# -*- coding: utf-8 -*-
"""
pe_tab.py - Aba "Projeto Eletrico" (rev. 4.1) do PainelSalas.

Gera HTML + CSS + JS que o build_unified_app.py injeta nos marcadores
__PE_TAB_HTML__, __PE_TAB_CSS__ e __PE_TAB_JS__.

Os desenhos sao SVG gerados por codigo (fios reais, simbolos IEC, juncoes,
bornes numerados e carimbo), entao ficam consistentes e faceis de manter.
"""
from html import escape as _escape


def esc(s):
    return _escape(str(s), quote=False)


def n(v):
    """Formata numero sem '.0' desnecessario."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, float):
        return f'{v:.2f}'.rstrip('0').rstrip('.')
    return str(v)


# ----------------------------------------------------------------------------
# REDES (cores dos fios) - usadas nos desenhos, na legenda e no destaque
# ----------------------------------------------------------------------------
NETS = {
    'v5':  ('#f43f5e', '+5V DC'),
    'gnd': ('#94a3b8', 'GND / 0 V'),
    'sh':  ('#d6b98c', 'Malha do cabo (SH) · referência'),
    'ac':  ('#e2e8f0', 'Rede AC 127/220 V'),
    'pe':  ('#a3e635', 'Terra de proteção PE'),
    'a':   ('#38bdf8', 'RS-485 A (+)'),
    'b':   ('#818cf8', 'RS-485 B (−)'),
    'tx':  ('#facc15', 'UART TX'),
    'rx':  ('#fb923c', 'UART RX'),
    'de':  ('#f472b6', 'DE/RE (direção)'),
    'i2c': ('#c084fc', 'I²C SDA/SCL'),
    'led': ('#22c55e', 'Dados WS2812B'),
    'io':  ('#2dd4bf', 'E/S digitais (botões, buzzer)'),
}
DASH = {'ac': '7 4', 'pe': '3 3', 'sh': '6 3'}

INK = '#e2e8f0'      # traço de componentes
MUTED = '#94a3b8'
DIM = '#64748b'
BG = '#0b1120'


# ----------------------------------------------------------------------------
# PRIMITIVAS SVG
# ----------------------------------------------------------------------------
def text(x, y, s, size=11, fill='#cbd5e1', anchor='start', weight='400', extra=''):
    ex = f' {extra}' if extra else ''
    return (f'<text x="{n(x)}" y="{n(y)}" font-size="{n(size)}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{ex}>{esc(s)}</text>')


def rect(x, y, w, h, fill='none', stroke=None, rx=6, sw=1.5, dash=None, extra=''):
    st = f' stroke="{stroke}" stroke-width="{n(sw)}"' if stroke else ''
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    ex = f' {extra}' if extra else ''
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" fill="{fill}"{st}{ds}{ex}/>'


def line(x1, y1, x2, y2, stroke=INK, sw=1.6, dash=None, extra=''):
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    ex = f' {extra}' if extra else ''
    return (f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" stroke="{stroke}" '
            f'stroke-width="{n(sw)}" stroke-linecap="round"{ds}{ex}/>')


def circle(cx, cy, r, fill='none', stroke=None, sw=1.5, extra=''):
    st = f' stroke="{stroke}" stroke-width="{n(sw)}"' if stroke else ''
    ex = f' {extra}' if extra else ''
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"{st}{ex}/>'


def wire(pts, net, title=None, width=2.2, dash=None):
    c = NETS[net][0]
    d = dash or DASH.get(net)
    ds = f' stroke-dasharray="{d}"' if d else ''
    p = ' '.join(f'{n(x)},{n(y)}' for x, y in pts)
    t = f'<title>{esc(title)}</title>' if title else ''
    return (f'<polyline class="net n-{net}" points="{p}" fill="none" stroke="{c}" '
            f'stroke-width="{n(width)}" stroke-linecap="round" stroke-linejoin="round"{ds}>{t}</polyline>')


def pwire(d, net, title=None, width=2.2):
    c = NETS[net][0]
    t = f'<title>{esc(title)}</title>' if title else ''
    return (f'<path class="net n-{net}" d="{d}" fill="none" stroke="{c}" stroke-width="{n(width)}" '
            f'stroke-linecap="round" stroke-linejoin="round">{t}</path>')


def dot(x, y, net):
    return f'<circle class="net n-{net}" cx="{n(x)}" cy="{n(y)}" r="3.8" fill="{NETS[net][0]}"/>'


def vcc(x, y, net='v5', label='+5V'):
    c = NETS[net][0]
    return (f'<g class="net n-{net}"><title>{esc(NETS[net][1])}</title>'
            + line(x, y, x, y - 12, c, 2.2) + line(x - 9, y - 12, x + 9, y - 12, c, 2.6)
            + text(x, y - 17, label, 10, c, 'middle', '800') + '</g>')


def gnd(x, y):
    c = NETS['gnd'][0]
    return (f'<g class="net n-gnd"><title>GND / 0 V</title>'
            + line(x, y, x, y + 10, c, 2.2) + line(x - 10, y + 10, x + 10, y + 10, c, 2.4)
            + line(x - 6, y + 14.5, x + 6, y + 14.5, c, 2.2) + line(x - 2.5, y + 19, x + 2.5, y + 19, c, 2)
            + '</g>')


def tag(x, y, label, net):
    """Rótulo de rede em forma de bandeira, a partir da ponta de um fio (aponta p/ direita)."""
    c = NETS[net][0]
    w = 10 + 6.4 * len(label)
    pts = f'{n(x)},{n(y)} {n(x+7)},{n(y-9)} {n(x+7+w)},{n(y-9)} {n(x+7+w)},{n(y+9)} {n(x+7)},{n(y+9)}'
    return (f'<g class="net n-{net}"><polygon points="{pts}" fill="{BG}" stroke="{c}" stroke-width="1.6"/>'
            + text(x + 7 + w / 2, y + 3.5, label, 9.5, c, 'middle', '800') + '</g>')


def res_h(x1, x2, y, net, ref, val, lab='above'):
    cx = (x1 + x2) / 2
    bw = min(30, (x2 - x1) - 10)
    o = wire([(x1, y), (cx - bw / 2, y)], net) + wire([(cx + bw / 2, y), (x2, y)], net)
    o += rect(cx - bw / 2, y - 5.5, bw, 11, BG, INK, 1.5, 1.6)
    o += text(cx, y - 10 if lab == 'above' else y + 19, f'{ref} {val}', 9, INK, 'middle', '700')
    return o


def res_v(x, y1, y2, n1, n2, ref, val, side='right', bh=22):
    cy = (y1 + y2) / 2
    bh = min(bh, (y2 - y1) - 8)
    o = wire([(x, y1), (x, cy - bh / 2)], n1) + wire([(x, cy + bh / 2), (x, y2)], n2)
    o += rect(x - 5.5, cy - bh / 2, 11, bh, BG, INK, 1.5, 1.6)
    if side == 'right':
        o += text(x + 10, cy - 2, ref, 9, INK, 'start', '700') + text(x + 10, cy + 10, val, 9, MUTED)
    elif side == 'left':
        o += text(x - 10, cy - 2, ref, 9, INK, 'end', '700') + text(x - 10, cy + 10, val, 9, MUTED, 'end')
    return o


def cap_v(x, y1, y2, ref, val, polar=False, side='right'):
    cy = (y1 + y2) / 2
    o = wire([(x, y1), (x, cy - 4)], 'v5') + wire([(x, cy + 4), (x, y2)], 'gnd')
    o += line(x - 10, cy - 4, x + 10, cy - 4, INK, 2.4)
    if polar:
        o += (f'<path d="M{n(x-10)} {n(cy+7)} Q{n(x)} {n(cy+1)} {n(x+10)} {n(cy+7)}" fill="none" '
              f'stroke="{INK}" stroke-width="2.4"/>')
        o += text(x - 14, cy - 6, '+', 10, INK, 'middle', '800')
    else:
        o += line(x - 10, cy + 4, x + 10, cy + 4, INK, 2.4)
    if side == 'right':
        o += text(x + 14, cy - 2, ref, 9, INK, 'start', '700') + text(x + 14, cy + 10, val, 9, MUTED)
    elif side == 'left':
        o += text(x - 14, cy - 2, ref, 9, INK, 'end', '700') + text(x - 14, cy + 10, val, 9, MUTED, 'end')
    return o


def button_h(x1, x2, y, net_in, label):
    """Botão pulsador N.A. (IEC) entre x1 e x2; lado direito vai ao GND."""
    xa, xb = x1 + 16, x2 - 16
    m = (xa + xb) / 2
    o = wire([(x1, y), (xa - 3, y)], net_in) + wire([(xb + 3, y), (x2, y)], 'gnd')
    o += circle(xa, y, 3, BG, INK, 1.6) + circle(xb, y, 3, BG, INK, 1.6)
    o += line(xa - 4, y - 9, xb + 4, y - 9, INK, 2.2)
    o += line(m, y - 9, m, y - 17, INK, 1.6) + line(m - 6, y - 17, m + 6, y - 17, INK, 2.2)
    o += text(m, y - 23, label, 9, '#cbd5e1', 'middle', '700')
    return o


def fuse_h(x1, x2, y, net, label):
    cx = (x1 + x2) / 2
    o = wire([(x1, y), (cx - 15, y)], net) + wire([(cx + 15, y), (x2, y)], net)
    o += rect(cx - 15, y - 6, 30, 12, BG, '#fbbf24', 1.5, 1.6) + line(cx - 15, y, cx + 15, y, '#fbbf24', 1.2)
    o += text(cx, y - 11, label, 9, '#fbbf24', 'middle', '700')
    return o


def switch_h(x1, x2, y, net, label):
    xa, xb = x1 + 12, x2 - 12
    o = wire([(x1, y), (xa, y)], net) + wire([(xb, y), (x2, y)], net)
    o += circle(xa, y, 2.6, INK) + circle(xb, y, 2.6, BG, INK, 1.4)
    o += line(xa, y, xb - 2, y - 13, INK, 2)
    o += text((x1 + x2) / 2, y - 17, label, 9, '#cbd5e1', 'middle', '700')
    return o


def buzzer(x1, x2, y, label):
    cx = (x1 + x2) / 2
    o = wire([(x1, y), (cx - 12, y)], 'io') + wire([(cx + 12, y), (x2, y)], 'gnd')
    o += circle(cx, y, 12, '#111827', INK, 1.6) + text(cx, y + 3.5, 'BZ', 8.5, INK, 'middle', '800')
    o += text(cx - 16, y - 6, '+', 10, INK, 'middle', '800')
    o += text(cx, y - 19, label, 9, '#cbd5e1', 'middle', '700')
    return o


def ws_led(x, y, label, color):
    o = rect(x, y, 44, 44, '#111827', '#475569', 5, 1.4)
    o += rect(x + 11, y + 6, 22, 22, '#1f2937', '#94a3b8', 2, 1)
    o += circle(x + 22, y + 17, 11, color, extra='opacity="0.25"')
    o += circle(x + 22, y + 17, 6, color)
    o += text(x + 22, y + 40, label, 7.5, MUTED, 'middle', '700')
    return o


def chip(x, y, w, h, title, sub, color, pins, stub=14):
    """Bloco de CI/módulo com cabeçalho e pinos. pins: (lado 'L'/'R', y, rótulo, rede)."""
    o = [rect(x, y, w, h, '#0f172a', color, 10, 2)]
    o.append(f'<path d="M{n(x)} {n(y+40)} V{n(y+10)} a10 10 0 0 1 10 -10 H{n(x+w-10)} '
             f'a10 10 0 0 1 10 10 V{n(y+40)} Z" fill="{color}" fill-opacity="0.16"/>')
    o.append(line(x, y + 40, x + w, y + 40, color, 1, extra='stroke-opacity="0.5"'))
    o.append(text(x + w / 2, y + 18, title, 11.5, color, 'middle', '800'))
    if sub:
        o.append(text(x + w / 2, y + 33, sub, 9, MUTED, 'middle', '600'))
    for side, py, lbl, net in pins:
        c = NETS[net][0]
        if side == 'L':
            o.append(f'<g class="net n-{net}">' + line(x - stub, py, x, py, c, 2.2)
                     + circle(x - stub, py, 2.4, c) + '</g>')
            o.append(text(x + 8, py + 3.5, lbl, 10, INK, 'start', '700'))
        else:
            o.append(f'<g class="net n-{net}">' + line(x + w, py, x + w + stub, py, c, 2.2)
                     + circle(x + w + stub, py, 2.4, c) + '</g>')
            o.append(text(x + w - 8, py + 3.5, lbl, 10, INK, 'end', '700'))
    return ''.join(o)


def title_block(x, y, code, title, w=265, h=78):
    o = rect(x, y, w, h, '#0f172a', '#475569', 4, 1.2)
    o += line(x, y + 24, x + w, y + 24, '#475569', 1) + line(x, y + 56, x + w, y + 56, '#475569', 1)
    o += line(x + 70, y + 24, x + 70, y + 56, '#475569', 1)
    o += text(x + 8, y + 16, 'SINALIZAÇÃO 4 SALAS · RS-485 / WS2812B', 8.5, MUTED, 'start', '700')
    o += text(x + 35, y + 46, code, 15, '#fbbf24', 'middle', '800')
    o += text(x + 78, y + 44, title, 9.5, INK, 'start', '700')
    o += text(x + 8, y + 70, 'Rev. 5.0 · 23/11/2026 · sem escala', 8, DIM)
    return o


def dim_h(sid, x1, x2, y, label, size=10):
    return (f'<line x1="{n(x1)}" y1="{n(y)}" x2="{n(x2)}" y2="{n(y)}" stroke="{MUTED}" stroke-width="1.2" '
            f'marker-start="url(#{sid}-arr)" marker-end="url(#{sid}-arr)"/>'
            + text((x1 + x2) / 2, y - 6, label, size, INK, 'middle', '700'))


def dim_v(sid, x, y1, y2, label):
    cy = (y1 + y2) / 2
    return (f'<line x1="{n(x)}" y1="{n(y1)}" x2="{n(x)}" y2="{n(y2)}" stroke="{MUTED}" stroke-width="1.2" '
            f'marker-start="url(#{sid}-arr)" marker-end="url(#{sid}-arr)"/>'
            + text(x - 6, cy, label, 10, INK, 'middle', '700', f'transform="rotate(-90 {n(x-6)} {n(cy)})"'))


def balloon(x, y, num):
    return (circle(x, y, 9, '#fbbf24', '#0b1120', 1.5)
            + text(x, y + 3.5, str(num), 9.5, '#0b1120', 'middle', '800'))


def svg_open(sid, w, h, label, extra_defs=''):
    return (f'<svg id="{sid}" class="pe-svg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{esc(label)}" '
            f'style="font-family:\'JetBrains Mono\',ui-monospace,Consolas,monospace">'
            f'<defs><pattern id="{sid}-grid" width="20" height="20" patternUnits="userSpaceOnUse">'
            f'<path d="M20 0H0V20" fill="none" stroke="#18233a" stroke-width="0.7"/></pattern>'
            f'<marker id="{sid}-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto-start-reverse"><path d="M0 1L10 5L0 9z" fill="{MUTED}"/></marker>{extra_defs}</defs>'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#{sid}-grid)"/>'
            f'<rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none" stroke="#334155" stroke-width="1"/>')


# ============================================================================
# DESENHO PE-01 · TOPOLOGIA PREDIAL
# ============================================================================
def diagram_topology():
    sid = 'pe-svg-topo'
    W, H = 1200, 420
    o = [svg_open(sid, W, H, 'PE-01 Topologia predial do barramento RS-485')]
    rooms = [
        (20, 'SALA 1', 'CENTRAL · MESTRE', '#818cf8', 'MESTRE',
         ['Arduino Mega 2560', 'LCD 20×2 · NAV/HAB · buzzer', 'Painel central 47× WS2812B',
          '14 botões locais · P01–P14', 'Fonte 5V 3A']),
        (316, 'SALA 2', 'ESTAÇÃO REMOTA', '#34d399', 'ID 2',
         ['Arduino Uno R3 (existente)', '11 botões · P15–P25', '11× WS2812B locais', 'Fonte local 5V 2A']),
        (612, 'SALA 3', 'ESTAÇÃO REMOTA', '#38bdf8', 'ID 3',
         ['Arduino Uno R3 (comprar)', '11 botões · P26–P36', '11× WS2812B locais', 'Fonte local 5V 2A']),
        (908, 'SALA 4', 'FIM DE LINHA', '#c084fc', 'ID 4',
         ['Arduino Uno R3 (comprar)', '11 botões · P37–P47', '11× WS2812B locais', 'Fonte local 5V 2A']),
    ]
    YA, YB, YG = 244, 270, 296
    # salas
    for x, name, sub, col, badge, lines_ in rooms:
        o.append(rect(x, 28, 272, 290, col, col, 14, 1.4, '8 6', 'fill-opacity="0.05" stroke-opacity="0.55"'))
        o.append(text(x + 18, 56, name, 16, col, 'start', '800'))
        o.append(text(x + 18, 73, sub, 9.5, MUTED, 'start', '700'))
        o.append(rect(x + 272 - 78, 41, 62, 20, col, col, 10, 1, extra='fill-opacity="0.15"'))
        o.append(text(x + 272 - 47, 55, badge, 9.5, col, 'middle', '800'))
        o.append(rect(x + 18, 86, 236, 126, '#0f172a', col, 10, 1.6))
        for i, s in enumerate(lines_):
            o.append(text(x + 32, 108 + i * 18, ('▸ ' if i == 0 else '· ') + s, 10,
                          INK if i == 0 else '#cbd5e1', 'start', '700' if i == 0 else '400'))
        o.append(rect(x + 190, 188, 56, 17, '#1e1b4b', '#818cf8', 4, 1))
        o.append(text(x + 218, 200, 'MAX485', 8.5, '#c7d2fe', 'middle', '800'))
    # eletrodutos entre salas
    for gx in (292, 588, 884):
        o.append(rect(gx - 6, 232, 36, 76, '#1e293b', '#475569', 4, 1))
        o.append(text(gx + 12, 226, '¾″', 9, MUTED, 'middle', '700'))
    # barramento
    o.append(wire([(44, YA), (1156, YA)], 'a', 'Linha A (+) · via 1 do cabo blindado', 2.6))
    o.append(wire([(44, YB), (1156, YB)], 'b', 'Linha B (−) · via 2 do cabo blindado', 2.6))
    o.append(wire([(64, YG), (1136, YG)], 'sh', 'Malha (SH): blindagem e referência comum', 2.6))
    o.append(text(70, YA - 6, 'A', 9, NETS['a'][0], 'start', '800'))
    o.append(text(70, YB - 6, 'B', 9, NETS['b'][0], 'start', '800'))
    o.append(text(76, YG - 6, 'SH (malha)', 9, NETS['sh'][0], 'start', '800'))
    # terminações nas pontas
    o.append(res_v(44, YA, YB, 'a', 'b', '', '', side='none'))
    o.append(res_v(1156, YA, YB, 'a', 'b', '', '', side='none'))
    o.append(text(30, 314, 'RT 120 Ω (R7) + bias 560 Ω · SH→GND', 8.5, '#fbbf24', 'start', '700'))
    o.append(text(1170, 314, 'RT 120 Ω (R7 mantido)', 8.5, '#fbbf24', 'end', '700'))
    # derivações (taps) com pontes nos cruzamentos
    taps = []
    for x, *_ in rooms:
        cx = x + 136
        taps.append(cx)
        o.append(wire([(cx - 14, 212), (cx - 14, YA)], 'a') + dot(cx - 14, YA, 'a'))
        o.append(pwire(f'M{cx} 212 V{YA-6} A6 6 0 0 1 {cx} {YA+6} V{YB}', 'b') + dot(cx, YB, 'b'))
        o.append(pwire(f'M{cx+14} 212 V{YA-6} A6 6 0 0 1 {cx+14} {YA+6} V{YB-6} '
                       f'A6 6 0 0 1 {cx+14} {YB+6} V{YG}', 'sh') + dot(cx + 14, YG, 'sh'))
    # cotas
    for cx in taps:
        o.append(line(cx, 304, cx, 360, DIM, 1, '4 3'))
    segs = [('15 m', 'trecho 1'), ('12 m', 'trecho 2'), ('18 m', 'trecho 3')]
    for i, (lbl, tr) in enumerate(segs):
        o.append(dim_h(sid, taps[i], taps[i + 1], 352, f'{lbl} · {tr}'))
    o.append(line(taps[0], 360, taps[0], 396, DIM, 1, '4 3') + line(taps[3], 360, taps[3], 396, DIM, 1, '4 3'))
    o.append(dim_h(sid, taps[0], taps[3], 392,
                   '45 m de cabo blindado 2 vias (par trançado + malha) — em linha, sem T ou estrela'))
    o.append(text(1188, 24, 'PE-01 · sem escala', 9, DIM, 'end', '700'))
    o.append('</svg>')
    return ''.join(o)


# ============================================================================
# DESENHO PE-02 · ESQUEMA DA CENTRAL (SALA 1)
# ============================================================================
def diagram_master():
    sid = 'pe-svg-master'
    W, H = 1240, 800
    o = [svg_open(sid, W, H, 'PE-02 Esquema elétrico da central Sala 1')]

    # ---------------- Alimentação ----------------
    o.append(text(24, 38, 'ALIMENTAÇÃO', 10.5, MUTED, 'start', '800'))
    o.append(rect(24, 54, 34, 78, '#111827', '#475569', 4, 1.4))
    for lbl, yy in (('L', 72), ('N', 94), ('PE', 116)):
        o.append(text(41, yy + 3.5, lbl, 9, INK, 'middle', '800'))
    o.append(text(41, 148, 'X0', 9, DIM, 'middle', '700'))
    o.append(wire([(58, 72), (80, 72)], 'ac'))
    o.append(fuse_h(80, 130, 72, 'ac', 'F1 2A'))
    o.append(wire([(130, 72), (150, 72)], 'ac'))
    o.append(switch_h(150, 200, 72, 'ac', 'S0'))
    o.append(wire([(200, 72), (250, 72)], 'ac', 'Fase L → fonte U1'))
    o.append(wire([(58, 94), (250, 94)], 'ac', 'Neutro N → fonte U1'))
    o.append(wire([(58, 116), (250, 116)], 'pe', 'Terra PE → carcaça da fonte'))
    o.append(rect(250, 50, 120, 82, '#052e2b', '#14b8a6', 8, 1.8))
    o.append(text(316, 70, 'U1 · FONTE', 10.5, '#5eead4', 'middle', '800'))
    o.append(text(316, 84, '5V 3A chaveada', 9, '#99f6e4', 'middle', '600'))
    o.append(text(316, 98, 'SELV', 9, '#99f6e4', 'middle', '600'))
    o.append(text(256, 75, 'L', 8, MUTED) + text(256, 97, 'N', 8, MUTED) + text(256, 119, '⏚', 9, MUTED))
    o.append(text(275, 127, '−V', 8.5, MUTED, 'middle', '700') + text(345, 127, '+V', 8.5, '#fda4af', 'middle', '700'))
    o.append(wire([(345, 132), (345, 160), (486, 160)], 'v5', 'Barra +5V → Mega 5V'))
    o.append(wire([(275, 132), (275, 200), (486, 200)], 'gnd', 'Barra GND → Mega GND'))
    o.append(cap_v(395, 160, 200, 'C1', '1000µF', polar=True))
    o.append(cap_v(455, 160, 200, 'C2', '100nF'))
    for xx in (395, 455):
        o.append(dot(xx, 160, 'v5') + dot(xx, 200, 'gnd'))
    o.append(text(360, 154, '+5V', 9, NETS['v5'][0], 'middle', '800'))
    o.append(text(300, 214, 'GND', 9, NETS['gnd'][0], 'middle', '800'))

    # ---------------- Rede RS-485 (início de linha) ----------------
    o.append(text(24, 246, 'RS-485 · INÍCIO DE LINHA (CABO 2 VIAS)', 10.5, MUTED, 'start', '800'))
    o.append(chip(250, 228, 130, 227, 'MAX485', 'U2 · módulo TTL', '#818cf8', [
        ('L', 280, 'VCC', 'v5'), ('L', 330, 'A', 'a'), ('L', 380, 'B', 'b'), ('L', 430, 'GND', 'gnd'),
        ('R', 280, 'RO', 'rx'), ('R', 330, '/RE', 'de'), ('R', 380, 'DE', 'de'), ('R', 430, 'DI', 'tx')]))
    o.append(text(315, 358, 'half-duplex', 8.5, DIM, 'middle'))
    o.append(wire([(236, 280), (222, 280)], 'v5') + vcc(222, 280))
    o.append(wire([(236, 430), (222, 430)], 'gnd') + gnd(222, 430))
    o.append(wire([(236, 330), (80, 330)], 'a', 'Linha A (+) → via 1 do cabo'))
    o.append(wire([(236, 380), (80, 380)], 'b', 'Linha B (−) → via 2 do cabo'))
    o.append(res_v(190, 330, 380, 'a', 'b', 'RT R7', '120Ω', side='left'))
    o.append(res_v(130, 282, 330, 'v5', 'a', 'RB1', '560Ω', side='right') + vcc(130, 282))
    o.append(res_v(130, 380, 428, 'b', 'gnd', 'RB2', '560Ω', side='right') + gnd(130, 428))
    for xx in (130, 190):
        o.append(dot(xx, 330, 'a') + dot(xx, 380, 'b'))
    o.append(rect(24, 300, 56, 165, '#111827', '#d6b98c', 6, 1.6))
    o.append(text(52, 316, 'X3', 10, '#e7d3b0', 'middle', '800') + text(52, 328, 'Wago 221', 8, MUTED, 'middle'))
    o.append(text(76, 345, 'A', 9.5, NETS['a'][0], 'end', '800'))
    o.append(text(76, 395, 'B', 9.5, NETS['b'][0], 'end', '800'))
    o.append(text(76, 445, 'SH', 9.5, NETS['sh'][0], 'end', '800'))
    o.append(text(52, 459, 'PG7', 7.5, DIM, 'middle'))
    o.append(wire([(80, 430), (104, 430)], 'sh', 'Malha do cabo → GND direto (só na Sala 1)') + gnd(104, 430))
    o.append(text(52, 484, '→ Sala 2 · 15 m', 9, '#38bdf8', 'middle', '700'))
    o.append(text(52, 497, '2 vias + malha', 8, DIM, 'middle'))

    # ---------------- LCD ----------------
    o.append(chip(200, 556, 180, 160, 'LCD 20×2 I²C', 'U3 · PCF8574 @ 0x27', '#c084fc', [
        ('R', 600, 'SDA', 'i2c'), ('R', 640, 'SCL', 'i2c'), ('R', 670, 'VCC', 'v5'), ('R', 700, 'GND', 'gnd')]))
    o.append(rect(210, 606, 118, 44, '#14532d', '#166534', 3, 1.2))
    o.append(text(216, 623, 'OCUP:32 LIVRE:10', 8, '#bbf7d0', 'start', '700'))
    o.append(text(216, 639, 'DESAB:05 REDE:OK', 8, '#bbf7d0', 'start', '700'))
    o.append(text(210, 670, 'trimpot = contraste', 8, DIM))
    o.append(text(210, 684, 'pull-up 4,7 kΩ no módulo', 8, DIM))
    o.append(wire([(394, 600), (486, 600)], 'i2c', 'D20/SDA ↔ SDA do LCD'))
    o.append(wire([(394, 640), (486, 640)], 'i2c', 'D21/SCL → SCL do LCD'))
    o.append(wire([(394, 670), (410, 670)], 'v5') + tag(410, 670, '+5V', 'v5'))
    o.append(wire([(394, 700), (410, 700)], 'gnd') + gnd(410, 700))

    # ---------------- Arduino Mega ----------------
    o.append(chip(500, 100, 240, 640, 'ARDUINO MEGA 2560 R3', 'U4 · MESTRE · proto shield c/ bornes', '#38bdf8', [
        ('L', 160, '5V', 'v5'), ('L', 200, 'GND', 'gnd'), ('L', 280, 'D19 · RX1', 'rx'),
        ('L', 355, 'D2 · DE/RE', 'de'), ('L', 430, 'D18 · TX1', 'tx'),
        ('L', 600, 'D20 · SDA', 'i2c'), ('L', 640, 'D21 · SCL', 'i2c'),
        ('R', 160, 'D4 · NAV', 'io'), ('R', 205, 'D5 · HAB', 'io'), ('R', 255, 'D7 · BUZZER', 'io'),
        ('R', 350, 'D6 · DATA', 'led'), ('R', 460, 'D22 · P01', 'io'), ('R', 505, 'D23 · P02', 'io'),
        ('R', 550, 'D24 · P03', 'io'), ('R', 635, 'D35 · P14', 'io')]))
    o.append(rect(545, 470, 120, 100, '#111827', '#334155', 6, 1.2))
    o.append(text(605, 500, 'ATmega2560', 10.5, INK, 'middle', '800'))
    o.append(text(605, 517, '16 MHz · 5 V', 9, MUTED, 'middle'))
    o.append(text(605, 533, 'Flash 256 KB', 9, MUTED, 'middle'))
    o.append(text(605, 549, 'EEPROM 4 KB', 9, MUTED, 'middle'))
    o.append(text(726, 594, 'D25…D34', 10, DIM, 'end', '700'))
    o.append(text(620, 690, 'USB-B: gravação / diagnóstico', 9, DIM, 'middle'))
    o.append(text(620, 706, 'firmware/master_mega.ino', 9, '#7dd3fc', 'middle', '700'))
    o.append(wire([(394, 280), (486, 280)], 'rx', 'RO (U2) → D19/RX1'))
    o.append(wire([(394, 330), (420, 330), (420, 380), (394, 380)], 'de', '/RE + DE jumpeados'))
    o.append(wire([(420, 355), (486, 355)], 'de', 'D2 → DE e /RE (HIGH = transmite)') + dot(420, 355, 'de'))
    o.append(wire([(394, 430), (486, 430)], 'tx', 'D18/TX1 → DI (U2)'))
    o.append(text(440, 272, 'Serial1 9600 8N1', 8.5, DIM, 'middle'))

    # ---------------- Lado direito: IHM ----------------
    o.append(wire([(754, 160), (790, 160)], 'io', 'D4 ← SW1 NAV') + button_h(790, 850, 160, 'io', 'SW1 · NAV'))
    o.append(wire([(850, 160), (880, 160)], 'gnd') + gnd(880, 160))
    o.append(wire([(754, 205), (790, 205)], 'io', 'D5 ← SW2 HAB') + button_h(790, 850, 205, 'io', 'SW2 · HAB'))
    o.append(wire([(850, 205), (880, 205)], 'gnd') + gnd(880, 205))
    o.append(wire([(754, 255), (800, 255)], 'io', 'D7 → buzzer') + buzzer(800, 840, 255, 'BZ1 · buzzer ativo 5V'))
    o.append(wire([(840, 255), (880, 255)], 'gnd') + gnd(880, 255))

    # ---------------- Painel WS2812B ----------------
    o.append(text(905, 302, 'PAINEL CENTRAL · 47× WS2812B (GRB)', 10.5, '#4ade80', 'start', '800'))
    o.append(wire([(754, 350), (775, 350)], 'led') + res_h(775, 835, 350, 'led', 'R1', '330Ω'))
    o.append(wire([(835, 350), (905, 350)], 'led', 'D6 → R1 → DIN do LED #0'))
    o.append(wire([(880, 318), (1180, 318)], 'v5', 'Barra +5V dos LEDs') + vcc(880, 318))
    o.append(wire([(880, 384), (1180, 384)], 'gnd', 'Barra GND dos LEDs') + gnd(880, 384))
    leds = [(905, '#0 · P01', '#22c55e'), (965, '#1 · P02', '#ef4444'), (1025, '#2 · P03', '#22c55e'),
            (1115, '#46 · P47', '#3b82f6')]
    for x, lbl, col in leds:
        o.append(ws_led(x, 328, lbl, col))
        o.append(wire([(x + 22, 328), (x + 22, 318)], 'v5') + dot(x + 22, 318, 'v5'))
        o.append(wire([(x + 22, 372), (x + 22, 384)], 'gnd') + dot(x + 22, 384, 'gnd'))
    o.append(wire([(949, 350), (965, 350)], 'led', 'DOUT #0 → DIN #1'))
    o.append(wire([(1009, 350), (1025, 350)], 'led', 'DOUT #1 → DIN #2'))
    o.append(wire([(1069, 350), (1115, 350)], 'led', 'LEDs #3 … #45', dash='4 4'))
    o.append(cap_v(1180, 318, 384, 'C3', '1000µF', polar=True))
    o.append(text(905, 404, 'injeção de 5V nas 2 pontas · brilho 40% ≈ 15 mA/LED', 9, DIM))

    # ---------------- Botoeiras P01..P14 ----------------
    rows = [(460, 'P01'), (505, 'P02'), (550, 'P03'), (635, 'P14')]
    for y, lbl in rows:
        o.append(wire([(754, y), (800, y)], 'io', f'Botão {lbl} → Mega'))
        o.append(button_h(800, 860, y, 'io', lbl))
        o.append(wire([(860, y), (940, y)], 'gnd'))
    o.append(wire([(940, 460), (940, 660)], 'gnd', 'Retorno comum dos botões (GND)'))
    for y in (505, 550, 635):
        o.append(dot(940, y, 'gnd'))
    o.append(gnd(940, 660))
    o.append(text(830, 600, '⋮', 18, DIM, 'middle', '800'))
    o.append(text(962, 474, 'BOTOEIRAS DE MESA · SALA 1', 10, '#5eead4', 'start', '800'))
    for i, s in enumerate(['14× contato seco N.A.', 'P01…P14 → D22…D35', 'INPUT_PULLUP (fecha p/ GND)',
                           'debounce por software']):
        o.append(text(962, 492 + i * 16, s, 9.5, '#cbd5e1'))

    o.append(title_block(960, 700, 'PE-02', 'Central · Sala 1 (Mega 2560)'))
    o.append('</svg>')
    return ''.join(o)


# ============================================================================
# DESENHO PE-03 · ESQUEMA DOS ESCRAVOS (SALAS 2, 3, 4)
# ============================================================================
def diagram_slave():
    sid = 'pe-svg-slave'
    W, H = 1240, 740
    o = [svg_open(sid, W, H, 'PE-03 Esquema elétrico dos nós escravos')]

    # ---------------- Alimentação local ----------------
    o.append(text(214, 34, 'ALIMENTAÇÃO LOCAL', 10.5, MUTED, 'start', '800'))
    o.append(wire([(214, 62), (270, 62)], 'ac', 'Fase') + wire([(214, 84), (270, 84)], 'ac', 'Neutro'))
    o.append(text(208, 77, '127/220 V~', 9, INK, 'end', '700'))
    o.append(rect(270, 44, 120, 70, '#052e2b', '#14b8a6', 8, 1.8))
    o.append(text(330, 64, 'U1 · FONTE 5V 2A', 10, '#5eead4', 'middle', '800'))
    o.append(text(330, 79, 'regulada', 8.5, '#99f6e4', 'middle'))
    o.append(text(295, 109, '−V', 8.5, MUTED, 'middle', '700') + text(365, 109, '+V', 8.5, '#fda4af', 'middle', '700'))
    o.append(wire([(365, 114), (365, 130), (546, 130)], 'v5', 'Barra +5V local'))
    o.append(wire([(295, 114), (295, 170), (546, 170)], 'gnd', 'Barra GND local'))
    o.append(cap_v(430, 130, 170, 'C1', '470µF', polar=True))
    o.append(cap_v(490, 130, 170, 'C2', '100nF'))
    for xx in (430, 490):
        o.append(dot(xx, 130, 'v5') + dot(xx, 170, 'gnd'))
    o.append(text(385, 124, '+5V', 9, NETS['v5'][0], 'middle', '800'))
    o.append(text(320, 186, 'GND', 9, NETS['gnd'][0], 'middle', '800'))

    # ---------------- Barramento (entra/sai) ----------------
    o.append(text(24, 160, 'RS-485 · CABO 2 VIAS + MALHA', 10.5, MUTED, 'start', '800'))
    o.append(rect(24, 180, 56, 100, '#111827', '#d6b98c', 6, 1.6))
    o.append(text(52, 196, 'CABO IN', 8.5, '#e7d3b0', 'middle', '800'))
    o.append(text(76, 228.5, 'A', 9.5, NETS['a'][0], 'end', '800'))
    o.append(text(76, 248.5, 'B', 9.5, NETS['b'][0], 'end', '800'))
    o.append(text(76, 268.5, 'SH', 9, NETS['sh'][0], 'end', '800'))
    o.append(text(52, 296, '← sala anterior', 8.5, '#38bdf8', 'middle', '700'))
    o.append(rect(24, 466, 56, 100, '#111827', '#d6b98c', 6, 1.6))
    o.append(text(76, 485.5, 'SH', 9, NETS['sh'][0], 'end', '800'))
    o.append(text(76, 505.5, 'B', 9.5, NETS['b'][0], 'end', '800'))
    o.append(text(76, 525.5, 'A', 9.5, NETS['a'][0], 'end', '800'))
    o.append(text(52, 556, 'CABO OUT', 8.5, '#e7d3b0', 'middle', '800'))
    o.append(text(52, 584, '→ próxima sala', 8.5, '#38bdf8', 'middle', '700'))
    o.append(text(52, 597, '(Sala 4: sem cabo)', 8, DIM, 'middle'))
    o.append(wire([(80, 225), (190, 225), (190, 522), (80, 522)], 'a', 'Linha A: entra e sai pelo mesmo Wago 221-413'))
    o.append(wire([(80, 245), (170, 245), (170, 502), (80, 502)], 'b', 'Linha B: entra e sai pelo mesmo Wago 221-413'))
    o.append(wire([(80, 265), (150, 265), (150, 482), (80, 482)], 'sh', 'Malha SH: entra e sai pelo mesmo Wago 221-413'))
    o.append(wire([(150, 440), (130, 440)], 'sh') + dot(150, 440, 'sh'))
    o.append(res_h(84, 130, 440, 'sh', 'RS', '100Ω'))
    o.append(gnd(84, 440))
    o.append(text(104, 418, 'SH→GND', 8, NETS['sh'][0], 'middle', '700'))
    # derivações para o MAX485
    o.append(wire([(190, 330), (286, 330)], 'a', 'A → MAX485') + dot(190, 330, 'a'))
    o.append(pwire('M170 380 H184 A6 6 0 0 1 196 380 H286', 'b', 'B → MAX485') + dot(170, 380, 'b'))
    # terminação J3 + RT
    o.append(wire([(245, 330), (245, 337)], 'a'))
    o.append(rect(241, 337, 8, 6, '#fbbf24', None, 1) + rect(241, 349, 8, 6, '#fbbf24', None, 1))
    o.append(wire([(245, 355), (245, 358)], 'b'))
    o.append(rect(239.5, 358, 11, 16, BG, INK, 1.5, 1.6))
    o.append(wire([(245, 374), (245, 380)], 'b'))
    o.append(dot(245, 330, 'a') + dot(245, 380, 'b'))
    o.append(text(236, 348, 'R7', 9, '#fbbf24', 'end', '800'))
    o.append(text(236, 371, '120Ω', 9, INK, 'end', '700'))

    # ---------------- MAX485 ----------------
    o.append(chip(300, 228, 130, 227, 'MAX485', 'U2 · módulo TTL', '#818cf8', [
        ('L', 280, 'VCC', 'v5'), ('L', 330, 'A', 'a'), ('L', 380, 'B', 'b'), ('L', 430, 'GND', 'gnd'),
        ('R', 280, 'RO', 'rx'), ('R', 330, '/RE', 'de'), ('R', 380, 'DE', 'de'), ('R', 430, 'DI', 'tx')]))
    o.append(text(365, 358, 'half-duplex', 8.5, DIM, 'middle'))
    o.append(wire([(286, 280), (266, 280)], 'v5') + vcc(266, 280))
    o.append(wire([(286, 430), (266, 430)], 'gnd') + gnd(266, 430))
    o.append(wire([(444, 280), (546, 280)], 'rx', 'RO → D0/RX'))
    o.append(wire([(444, 330), (470, 330), (470, 380), (444, 380)], 'de', '/RE + DE jumpeados'))
    o.append(wire([(470, 355), (546, 355)], 'de', 'D4 → DE e /RE') + dot(470, 355, 'de'))
    o.append(wire([(444, 430), (546, 430)], 'tx', 'D1/TX → DI'))
    o.append(text(495, 272, 'Serial 9600 8N1', 8.5, DIM, 'middle'))
    o.append(text(300, 478, '⚠ D0/D1 = USB: soltar RO/DI ao gravar', 9, '#fbbf24', 'start', '700'))

    # ---------------- Arduino Nano/Uno ----------------
    o.append(chip(560, 80, 230, 540, 'ARDUINO UNO R3', 'U3 · ESCRAVO ID 2|3|4 · screw shield', '#34d399', [
        ('L', 130, '5V', 'v5'), ('L', 170, 'GND', 'gnd'), ('L', 280, 'D0 · RX', 'rx'),
        ('L', 355, 'D4 · DE/RE', 'de'), ('L', 430, 'D1 · TX', 'tx'),
        ('R', 140, 'D5 · DATA', 'led'), ('R', 300, 'D6 · P01', 'io'), ('R', 345, 'D7 · P02', 'io'),
        ('R', 390, 'D8 · P03', 'io'), ('R', 475, 'A3 · P11', 'io')]))
    o.append(rect(615, 185, 110, 80, '#111827', '#334155', 6, 1.2))
    o.append(text(670, 214, 'ATmega328P', 10.5, INK, 'middle', '800'))
    o.append(text(670, 230, '16 MHz · 5 V', 9, MUTED, 'middle'))
    o.append(text(670, 246, 'EEPROM 1 KB', 9, MUTED, 'middle'))
    o.append(text(782, 434, 'D9…D12 · A0…A2', 9.5, DIM, 'end', '700'))
    for i, s in enumerate(['#define SLAVE_ID por sala:', 'Sala 2 → Uno R3 (existente) · 2', 'Sala 3 → Uno R3 · ID 3',
                           'Sala 4 → Uno R3 · ID 4']):
        o.append(text(675, 530 + i * 16, s, 9, '#a7f3d0' if i else '#6ee7b7', 'middle', '700' if i == 0 else '400'))
    o.append(text(675, 604, 'firmware/slave_uno.ino', 9, '#6ee7b7', 'middle', '700'))

    # ---------------- LEDs locais ----------------
    o.append(text(925, 92, '11× WS2812B · FEEDBACK DO OPERADOR', 10.5, '#4ade80', 'start', '800'))
    o.append(wire([(804, 140), (822, 140)], 'led') + res_h(822, 878, 140, 'led', 'R1', '330Ω'))
    o.append(wire([(878, 140), (925, 140)], 'led', 'D5 → R1 → DIN do LED local #0'))
    o.append(wire([(900, 108), (1195, 108)], 'v5') + vcc(900, 108))
    o.append(wire([(900, 174), (1195, 174)], 'gnd') + gnd(900, 174))
    for x, lbl, col in [(925, '#0 · Pos01', '#22c55e'), (985, '#1 · Pos02', '#ef4444'),
                        (1045, '#2 · Pos03', '#3b82f6'), (1135, '#10 · Pos11', '#22c55e')]:
        o.append(ws_led(x, 118, lbl, col))
        o.append(wire([(x + 22, 118), (x + 22, 108)], 'v5') + dot(x + 22, 108, 'v5'))
        o.append(wire([(x + 22, 162), (x + 22, 174)], 'gnd') + dot(x + 22, 174, 'gnd'))
    o.append(wire([(969, 140), (985, 140)], 'led') + wire([(1029, 140), (1045, 140)], 'led'))
    o.append(wire([(1089, 140), (1135, 140)], 'led', 'LEDs #3 … #9', dash='4 4'))
    o.append(cap_v(1195, 108, 174, '', '', polar=True, side='none'))
    o.append(text(1195, 200, 'C3 470µF', 8.5, INK, 'middle', '700'))
    o.append(text(925, 200, 'LED local #0…#10 = Pos 01…11', 9, DIM))

    # ---------------- Botoeiras ----------------
    rows = [(300, 'Pos 01'), (345, 'Pos 02'), (390, 'Pos 03'), (475, 'Pos 11')]
    for y, lbl in rows:
        o.append(wire([(804, y), (845, y)], 'io', f'{lbl} → Arduino'))
        o.append(button_h(845, 905, y, 'io', lbl))
        o.append(wire([(905, y), (985, y)], 'gnd'))
    o.append(wire([(985, 300), (985, 500)], 'gnd', 'Retorno comum dos botões (GND)'))
    for y in (345, 390, 475):
        o.append(dot(985, y, 'gnd'))
    o.append(gnd(985, 500))
    o.append(text(875, 440, '⋮', 18, DIM, 'middle', '800'))
    o.append(text(1005, 310, 'BOTOEIRAS DA SALA', 10, '#5eead4', 'start', '800'))
    for i, s in enumerate(['11× contato seco N.A.', '(botões 22 mm existentes)', 'INPUT_PULLUP · debounce 40 ms',
                           'travado se DESABILITADA']):
        o.append(text(1005, 328 + i * 16, s, 9.5, '#cbd5e1'))

    # ---------------- Notas de terminação ----------------
    o.append(rect(24, 618, 520, 98, '#111827', '#fbbf24', 8, 1.2, extra='stroke-opacity="0.6"'))
    o.append(text(40, 640, 'TERMINAÇÃO E MALHA', 10, '#fbbf24', 'start', '800'))
    for i, s in enumerate(['• Salas 2 e 3 (meio da linha): REMOVER o R7 (120 Ω) do módulo',
                           '• Sala 4 (fim de linha): MANTER o R7 → 120 Ω entre A e B',
                           '• Malha SH → GND por RS 100 Ω (na Sala 1: direto ao GND)',
                           '• Conferência: A–B com tudo desligado ≈ 60 Ω (CK-02)']):
        o.append(text(40, 660 + i * 15, s, 9.5, '#cbd5e1'))

    o.append(title_block(960, 640, 'PE-03', 'Nós escravos · Salas 2–4'))
    o.append('</svg>')
    return ''.join(o)


# ============================================================================
# DESENHO PE-04 · CONECTOR RJ45 T568B
# ============================================================================
def diagram_cable():
    sid = 'pe-svg-cabo'
    W, H = 560, 440
    o = [svg_open(sid, W, H, 'PE-04 Cabo blindado de 2 vias')]
    o.append(text(280, 30, 'CABO BLINDADO 2 VIAS · PAR TRANÇADO 24 AWG', 11.5, INK, 'middle', '800'))
    # corte transversal
    cx, cy = 140, 150
    o.append(circle(cx, cy, 74, '#1f2937', '#475569', 2))
    o.append(circle(cx, cy, 62, 'none', NETS['sh'][0], 7, extra='stroke-dasharray="2 2"'))
    o.append(circle(cx, cy, 56, '#334155'))
    o.append(circle(cx - 24, cy, 21, '#f8fafc', '#cbd5e1', 1.4) + circle(cx - 24, cy, 9, '#d97706'))
    o.append(circle(cx + 24, cy, 21, '#2563eb', '#1e40af', 1.4) + circle(cx + 24, cy, 9, '#d97706'))
    o.append(text(cx, 248, 'corte transversal', 9, DIM, 'middle'))

    def lead(px, py, tx, ty, lbl, col):
        return line(px, py, tx - 4, ty - 3, DIM, 1) + circle(px, py, 2.4, DIM) + text(tx, ty, lbl, 9.5, col, 'start', '700')
    o.append(lead(cx + 52, cy - 52, 250, 70, 'Capa PVC', MUTED))
    o.append(lead(cx + 44, cy - 38, 250, 92, 'Malha (SH) → referência GND', NETS['sh'][0]))
    o.append(lead(cx - 24, cy - 12, 250, 128, 'Via 1 (clara) → A (+)', NETS['a'][0]))
    o.append(lead(cx + 30, cy + 8, 250, 164, 'Via 2 (colorida) → B (−)', NETS['b'][0]))
    o.append(text(250, 188, 'anote as cores com anilha: iguais', 8.5, DIM))
    o.append(text(250, 201, 'nas 4 salas', 8.5, DIM))
    # preparo da ponta
    y = 300
    o.append(text(24, 278, 'PREPARO DA PONTA', 10, '#fbbf24', 'start', '800'))
    o.append(rect(24, y - 12, 150, 24, '#1f2937', '#475569', 6, 1.4))
    o.append(text(99, y + 4, 'cabo', 9, MUTED, 'middle'))
    o.append(pwire(f'M174 {y-5} C 220 {y-5} 230 {y-40} 290 {y-40}', 'a', width=4))
    o.append(pwire(f'M174 {y+1} C 220 {y+1} 240 {y} 290 {y}', 'b', width=4))
    o.append(pwire(f'M174 {y+8} C 210 {y+30} 230 {y+44} 290 {y+44}', 'sh', width=4))
    for yy, col in ((y - 40, '#38bdf8'), (y, '#818cf8')):
        o.append(rect(290, yy - 6, 18, 12, col, None, 2) + rect(308, yy - 4, 26, 8, '#cbd5e1', '#94a3b8', 1, 1))
    o.append(rect(290, y + 38, 40, 12, '#111827', NETS['sh'][0], 3, 1.2))
    o.append(text(342, y - 37, 'ilhós 0,25 mm² crimpado', 9, INK))
    o.append(text(342, y + 3, 'ilhós 0,25 mm² crimpado', 9, INK))
    o.append(text(342, y + 47, 'malha torcida + termo-retrátil', 9, NETS['sh'][0]))
    o.append(line(174, y + 24, 174, y + 64, DIM, 1) + line(24, y + 24, 24, y + 64, DIM, 1))
    o.append(dim_h(sid, 24, 174, y + 58, 'capa: retirar 40 mm', 9))
    o.append(text(24, 400, 'Tranças cancelam o ruído; a malha blinda e serve de', 9, '#cbd5e1'))
    o.append(text(24, 414, 'referência comum. Alternativa: UTP Cat5e usando só o', 9, '#cbd5e1'))
    o.append(text(24, 428, 'par azul (A/B) + 1 fio verde (GND ref.).', 9, '#cbd5e1'))
    o.append('</svg>')
    return ''.join(o)


# ============================================================================
# DESENHO PE-05 · LAYOUT DO QUADRO DA SALA 1
# ============================================================================
def diagram_panel():
    sid = 'pe-svg-quadro'
    W, H = 1200, 470
    s = 1.25
    defs = (f'<pattern id="{sid}-wood" width="40" height="12" patternUnits="userSpaceOnUse">'
            f'<rect width="40" height="12" fill="#2a1a10"/><path d="M0 6 Q10 3 20 6 T40 6" fill="none" '
            f'stroke="#3b2516" stroke-width="1"/></pattern>'
            f'<pattern id="{sid}-slot" width="8" height="10" patternUnits="userSpaceOnUse">'
            f'<rect width="8" height="10" fill="#334155"/><rect x="3" y="2" width="2" height="6" fill="#1e293b"/></pattern>')
    o = [svg_open(sid, W, H, 'PE-05 Layout do quadro da Sala 1', defs)]

    # ---------------- A · Vista frontal ----------------
    FX, FY = 60, 70

    def F(x, y):
        return FX + x * s, FY + y * s

    o.append(text(FX, 50, 'A · VISTA FRONTAL — PAINEL 420 × 260 mm', 11, INK, 'start', '800'))
    o.append(rect(FX, FY, 420 * s, 260 * s, f'url(#{sid}-wood)', '#78350f', 8, 2))
    lx, ly = F(20, 12)
    o.append(rect(lx - 4, ly - 4, 108, 53, '#111827', '#475569', 4, 1.2))
    o.append(rect(lx, ly, 100, 45, '#14532d', '#166534', 2, 1))
    o.append(text(lx + 6, ly + 18, 'OCUP:32 LIVRE:10', 8.5, '#bbf7d0', 'start', '700'))
    o.append(text(lx + 6, ly + 34, 'DESAB:05 REDE:OK', 8.5, '#bbf7d0', 'start', '700'))
    o.append(text(lx + 112, ly + 26, 'LCD 20×2', 8.5, '#d6d3d1', 'start', '700'))
    for xm, lbl, r in ((250, 'NAV', 10), (320, 'HAB', 10), (385, 'BUZZER', 7)):
        cx, cy = F(xm, 30)
        o.append(circle(cx, cy, r, '#1e293b', '#94a3b8', 1.6) + circle(cx, cy, r - 3.5, '#334155'))
        o.append(text(cx, cy + r + 13, lbl, 8.5, '#e7e5e4', 'middle', '800'))
    red = {5, 12, 18, 23, 31, 40, 44}
    blue = {9, 10, 24, 25, 36, 46, 47}
    rows = [('S1', 14, 1, 62, True), ('S2', 11, 15, 106, False), ('S3', 11, 26, 150, False),
            ('S4', 11, 37, 194, False)]
    for lbl, cnt, start, ym, has_btn in rows:
        rx_, ry_ = F(15, ym + 20)
        o.append(text(rx_, ry_ + 4, lbl, 10, '#fde68a', 'middle', '800'))
        for i in range(cnt):
            p = start + i
            x0, y0 = F(30 + i * 26 + 1, ym)
            col = '#ef4444' if p in red else ('#3b82f6' if p in blue else '#22c55e')
            o.append(rect(x0, y0, 30, 50, '#1c1917', '#57534e', 3, 1))
            o.append(circle(x0 + 15, y0 + 11, 9, col, extra='opacity="0.25"') + circle(x0 + 15, y0 + 11, 5, col))
            o.append(text(x0 + 15, y0 + 28, f'{p:02d}', 8.5, '#f5f5f4', 'middle', '800'))
            if has_btn:
                o.append(circle(x0 + 15, y0 + 40, 7.5, '#0f172a', '#a8a29e', 1.2))
    o.append(line(FX, FY + 330, FX, FY + 362, DIM, 1) + line(FX + 525, FY + 330, FX + 525, FY + 362, DIM, 1))
    o.append(dim_h(sid, FX, FX + 525, FY + 356, '420 mm'))
    o.append(line(FX - 6, FY, FX - 38, FY, DIM, 1) + line(FX - 6, FY + 325, FX - 38, FY + 325, DIM, 1))
    o.append(dim_v(sid, FX - 30, FY, FY + 325, '260 mm'))
    o.append(text(FX + 262, FY + 386 - 4, 'célula 26 × 44 mm · LED Ø10 mm · S1 com botão 22 mm', 9, DIM, 'middle'))

    # ---------------- B · Vista interna ----------------
    IX, IY = 640, 70

    def I(x, y):
        return IX + x * s, IY + y * s

    o.append(text(IX, 50, 'B · VISTA INTERNA — PLACA DE MONTAGEM', 11, INK, 'start', '800'))
    o.append(rect(IX, IY, 525, 325, '#1f2937', '#64748b', 8, 2))
    x, y = I(10, 8)
    o.append(rect(x, y, 400 * s, 16 * s, f'url(#{sid}-slot)', '#64748b', 2, 1))
    x, y = I(10, 52)
    o.append(rect(x, y, 400 * s, 7.5 * s, '#9ca3af', '#6b7280', 1, 1))
    # componentes no trilho
    comps = [
        ((14, 34, 70, 58), '#052e2b', '#14b8a6', ['FONTE U1', '5V 3A DIN'], '#5eead4'),
        ((88, 40, 14, 46), '#1e293b', '#f59e0b', ['F1'], '#fbbf24'),
        ((194, 38, 60, 50), '#1e1b4b', '#818cf8', ['MAX485', 'R7+bias'], '#c7d2fe'),
    ]
    for (xm, ym, wm, hm), fill, stroke, labels, tc in comps:
        x, y = I(xm, ym)
        o.append(rect(x, y, wm * s, hm * s, fill, stroke, 4, 1.6))
        for k, lb in enumerate(labels):
            o.append(text(x + wm * s / 2, y + hm * s / 2 - (len(labels) - 1) * 6 + k * 13 + 3, lb, 8.5, tc, 'middle', '800'))
    # bornes Wago
    for k, (lb, col) in enumerate((('+5V', NETS['v5'][0]), ('GND', NETS['gnd'][0]), ('A', NETS['a'][0]),
                                    ('B', NETS['b'][0]))):
        x, y = I(108 + k * 20, 40)
        o.append(rect(x, y, 19 * s, 46 * s, '#e5e7eb', '#9ca3af', 2, 1))
        o.append(rect(x + 3, y + 4, 19 * s - 6, 8, col, None, 1))
        o.append(text(x + 19 * s / 2, y + 46 * s - 8, lb, 8, '#111827', 'middle', '800'))
    x, y = I(108, 88)
    o.append(text(x + 50 * s, y + 9, 'X1 · Wago 221', 8, MUTED, 'middle', '700'))
    x, y = I(260, 40)
    o.append(rect(x, y, 70 * s, 46 * s, 'none', '#475569', 4, 1.2, '5 4'))
    o.append(text(x + 35 * s, y + 31, 'reserva', 8.5, DIM, 'middle'))
    # conectores do cabo de 2 vias (Wago 221-413: A, B, SH) + prensa-cabo PG7
    for k, (lb, col) in enumerate((('A', NETS['a'][0]), ('B', NETS['b'][0]), ('SH', NETS['sh'][0]))):
        x, y = I(342 + k * 14, 38)
        o.append(rect(x, y, 13 * s, 28 * s, '#e5e7eb', '#9ca3af', 2, 1))
        o.append(rect(x + 2, y + 3, 13 * s - 4, 9, '#f97316', None, 1))
        o.append(text(x + 6.5 * s, y + 28 * s - 6, lb, 7.5, '#111827', 'middle', '800'))
    x, y = I(342, 68)
    o.append(text(x + 21 * s, y + 9, 'X3 · cabo 2 vias', 8, MUTED, 'middle', '700'))
    cx, cy = I(398, 51)
    o.append(circle(cx, cy, 9, '#334155', '#94a3b8', 1.6) + circle(cx, cy, 3.5, NETS['sh'][0]))
    o.append(wire([(cx + 9, cy), (IX + 525 + 18, cy)], 'sh', 'Cabo blindado 2 vias → Sala 2'))
    o.append(text(1192, cy - 14, '→ Sala 2', 8.5, '#38bdf8', 'end', '700'))
    x, y = I(10, 100)
    o.append(rect(x, y, 400 * s, 14 * s, f'url(#{sid}-slot)', '#64748b', 2, 1))
    # entrada AC
    cx, cy = I(6, 72)
    o.append(wire([(IX - 26, cy), (cx - 6, cy)], 'ac', 'Entrada AC 127/220 V') + circle(cx, cy, 7, '#334155', '#94a3b8', 1.4))
    o.append(text(IX - 28, cy - 8, 'AC', 8.5, INK, 'end', '800'))
    # parte inferior: Mega e X2
    x, y = I(14, 124)
    o.append(rect(x, y, 102 * s, 54 * s, '#0c4a6e', '#38bdf8', 4, 1.6))
    for dx, dy in ((4, 4), (98, 4), (4, 50), (98, 50)):
        o.append(circle(x + dx * s, y + dy * s, 3.2, '#e5e7eb'))
    o.append(text(x + 51 * s, y + 30, 'ARDUINO MEGA 2560', 9, '#e0f2fe', 'middle', '800'))
    o.append(text(x + 51 * s, y + 45, 'proto shield · M3 nylon', 8, '#bae6fd', 'middle'))
    x, y = I(132, 128)
    for k in range(24):
        o.append(rect(x + k * 8.2, y, 7.6, 30, '#475569', '#1f2937', 1, 0.8))
    o.append(text(x, y - 6, 'X2 · chicote p/ porta: 14 botões, NAV/HAB, BZ, LCD, LED', 8, MUTED, 'start', '700'))
    o.append(pwire(f'M{n(x+24*8.2)} {n(y+15)} C {n(x+24*8.2+60)} {n(y+15)} {n(IX+470)} {n(y+70)} {n(IX+520)} {n(y+70)}',
                   'io', 'Chicote flexível para o painel frontal (porta)'))
    o.append(text(IX + 515, y + 86, 'chicote flexível → porta', 8, MUTED, 'end', '700'))
    cx, cy = I(395, 238)
    o.append(circle(cx, cy, 7, '#365314', NETS['pe'][0], 1.6) + text(cx - 12, cy + 4, 'PE', 8.5, NETS['pe'][0], 'end', '800'))
    # balões
    for num, (xm, ym) in enumerate([(22, 16), (338, 56), (18, 38), (95, 42), (116, 42), (200, 42),
                                    (360, 34), (22, 107), (20, 128), (138, 122), (6, 64), (395, 228)], start=1):
        bx, by = I(xm, ym)
        o.append(balloon(bx, by, num))
    o.append(text(1190, 24, 'PE-05 · escala ≈ 1:4', 9, DIM, 'end', '700'))
    o.append('</svg>')
    return ''.join(o)


# ============================================================================
# DESENHO PE-06 · DETALHE DAS POSIÇÕES (BOTÃO + LED)
# ============================================================================
def diagram_buttons():
    sid = 'pe-svg-botoes'
    W, H = 1200, 400
    defs = (f'<pattern id="{sid}-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="6" height="6" fill="#78350f"/><line x1="0" y1="0" x2="0" y2="6" stroke="#451a03" stroke-width="2"/></pattern>')
    o = [svg_open(sid, W, H, 'PE-06 Detalhe construtivo de uma posição', defs)]

    def leader(px, py, tx, ty, label, col='#cbd5e1'):
        return (line(px, py, tx - 4, ty - 3, DIM, 1) + circle(px, py, 2.2, DIM)
                + text(tx, ty, label, 9.5, col, 'start', '600'))

    # ---- Painel 1: WS2812B + difusor ----
    o.append(rect(20, 20, 380, 360, '#0f172a', '#22c55e', 12, 1.4, extra='stroke-opacity="0.6"'))
    o.append(text(36, 44, 'OPÇÃO 1 · PIXEL WS2812B + DIFUSOR', 11, '#4ade80', 'start', '800'))
    o.append(rect(36, 54, 150, 18, '#14532d', '#22c55e', 9, 1) + text(111, 67, 'RECOMENDADA · RGB', 8.5, '#bbf7d0', 'middle', '800'))
    o.append(rect(70, 84, 22, 240, f'url(#{sid}-hatch)', '#451a03', 1, 1))
    o.append(rect(70, 116, 22, 24, '#e0f2fe', None, 1, extra='opacity="0.9"'))
    o.append(circle(64, 128, 14, '#22c55e', extra='opacity="0.35"'))
    o.append(rect(94, 106, 7, 44, '#14532d', '#22c55e', 1, 1) + rect(92, 120, 4, 16, '#f8fafc', None, 0.5))
    for k, (net, lb) in enumerate((('v5', '+5V'), ('led', 'DIN ←'), ('led', 'DOUT →'), ('gnd', 'GND'))):
        yy = 110 + k * 11
        o.append(wire([(101, yy), (138, yy)], net, width=1.6) + text(142, yy + 3, lb, 8, NETS[net][0], 'start', '700'))
    o.append(rect(52, 220, 18, 60, '#991b1b', '#7f1d1d', 5, 1))
    o.append(rect(70, 228, 22, 44, '#475569', '#334155', 1, 1) + rect(92, 222, 6, 56, '#94a3b8', None, 1))
    o.append(rect(98, 230, 40, 40, '#1e1b4b', '#818cf8', 3, 1.2) + text(118, 254, 'N.A.', 8.5, '#c7d2fe', 'middle', '800'))
    o.append(wire([(138, 240), (170, 240)], 'io', width=1.6) + text(174, 243, 'pino Dx', 8, NETS['io'][0], 'start', '700'))
    o.append(wire([(138, 260), (170, 260)], 'gnd', width=1.6) + text(174, 263, 'GND', 8, MUTED, 'start', '700'))
    o.append(leader(81, 116, 214, 80, 'Difusor leitoso Ø10 mm'))
    o.append(leader(98, 150, 214, 172, 'Pixel cortado da fita'))
    o.append(leader(81, 200, 214, 204, 'Madeira 15 mm'))
    o.append(leader(60, 278, 214, 300, 'Botão 22 mm existente'))
    for i, s_ in enumerate(['✓ mostra verde / vermelho / azul / âmbar', '✓ 1 fio de dados para 11 posições',
                            '✓ fita de R$ 45 atende o projeto todo']):
        o.append(text(36, 334 + i * 15, s_, 9.5, '#bbf7d0'))

    # ---- Painel 2: BA9s ----
    o.append(rect(410, 20, 380, 360, '#0f172a', '#f59e0b', 12, 1.4, extra='stroke-opacity="0.6"'))
    o.append(text(426, 44, 'OPÇÃO 2 · LÂMPADA LED BA9s 5 V', 11, '#fbbf24', 'start', '800'))
    o.append(rect(426, 54, 120, 18, '#451a03', '#f59e0b', 9, 1) + text(486, 67, 'SÓ 1 COR', 8.5, '#fde68a', 'middle', '800'))
    o.append(rect(470, 84, 22, 240, f'url(#{sid}-hatch)', '#451a03', 1, 1))
    o.append(rect(448, 140, 22, 80, '#dc2626', '#7f1d1d', 5, 1, extra='opacity="0.85"'))
    o.append(rect(470, 148, 22, 64, '#475569', '#334155', 1, 1))
    o.append(rect(492, 146, 44, 68, '#0f172a', '#f59e0b', 3, 1.2))
    o.append(circle(514, 180, 13, '#fde68a', extra='opacity="0.9"') + text(514, 183, 'LED', 7.5, '#78350f', 'middle', '800'))
    o.append(rect(536, 150, 38, 60, '#1e1b4b', '#818cf8', 3, 1.2) + text(555, 184, 'N.A.', 8.5, '#c7d2fe', 'middle', '800'))
    o.append(leader(459, 150, 600, 110, 'Lente colorida (cor fixa)'))
    o.append(leader(514, 146, 600, 132, 'Soquete BA9s (¼ de volta)'))
    o.append(leader(526, 190, 600, 196, 'Lâmpada LED 5 V'))
    o.append(leader(570, 210, 600, 230, 'Bloco N.A. → Dx / GND'))
    for i, s_ in enumerate(['⚠ não mostra verde/vermelho/azul', '⚠ 1 transistor por posição (sem WS2812B)',
                            '→ só se o feedback local for liga/desliga']):
        o.append(text(426, 334 + i * 15, s_, 9.5, '#fde68a'))

    # ---- Painel 3: ligação de uma posição ----
    o.append(rect(800, 20, 380, 360, '#0f172a', '#38bdf8', 12, 1.4, extra='stroke-opacity="0.6"'))
    o.append(text(816, 44, 'LIGAÇÃO DE UMA POSIÇÃO (SALA REMOTA)', 11, '#7dd3fc', 'start', '800'))
    o.append(chip(816, 70, 70, 230, 'UNO', '', '#34d399', [
        ('R', 150, 'D5', 'led'), ('R', 250, 'D6', 'io')]))
    o.append(res_h(900, 950, 150, 'led', 'R', '330Ω'))
    o.append(wire([(950, 150), (980, 150)], 'led'))
    o.append(wire([(960, 110), (1160, 110)], 'v5') + vcc(960, 110))
    o.append(wire([(960, 190), (1160, 190)], 'gnd') + gnd(960, 190))
    for x, lbl, col in ((980, '#0', '#22c55e'), (1060, '#1', '#ef4444')):
        o.append(ws_led(x, 128, lbl, col))
        o.append(wire([(x + 22, 128), (x + 22, 110)], 'v5') + dot(x + 22, 110, 'v5'))
        o.append(wire([(x + 22, 172), (x + 22, 190)], 'gnd') + dot(x + 22, 190, 'gnd'))
    o.append(wire([(1024, 150), (1060, 150)], 'led', 'DOUT → DIN (≤ 30 cm)'))
    o.append(wire([(1104, 150), (1150, 150)], 'led', '→ #2 … #10', dash='4 4'))
    o.append(text(1042, 166, '≤30cm', 7.5, DIM, 'middle'))
    o.append(button_h(900, 960, 250, 'io', 'Pos 01'))
    o.append(wire([(960, 250), (990, 250)], 'gnd') + gnd(990, 250))
    for i, s_ in enumerate(['Repouso: pino em 1 (pull-up interno)', 'Botão apertado: pino vai a 0 (GND)',
                            'Pixel: +5V · GND · DIN entra · DOUT sai', 'Fio 26 AWG entre pixels; GND comum']):
        o.append(text(816, 318 + i * 15, s_, 9.5, '#cbd5e1'))
    o.append(text(1188, 392, 'PE-06 · sem escala', 9, DIM, 'end', '700'))
    o.append('</svg>')
    return ''.join(o)


# ============================================================================
# DESENHO PE-07 · LIGAÇÃO NOS ARDUINOS (CONEXÕES CONFIÁVEIS)
# ============================================================================
def diagram_assembly():
    sid = 'pe-svg-montagem'
    W, H = 1200, 430
    o = [svg_open(sid, W, H, 'PE-07 Ligação nos Arduinos')]

    # ---- Painel A: Uno + screw shield (vista lateral) ----
    o.append(rect(20, 20, 380, 390, '#0f172a', '#34d399', 12, 1.4, extra='stroke-opacity="0.6"'))
    o.append(text(36, 44, 'A · UNO + SHIELD DE BORNES', 11, '#6ee7b7', 'start', '800'))
    o.append(text(36, 60, 'vista lateral', 9, DIM))
    o.append('<g transform="translate(0,-70)">')
    o.append(rect(40, 300, 340, 14, '#334155', '#475569', 2, 1))
    o.append(text(210, 330, 'placa de montagem (MDF / PVC)', 8.5, DIM, 'middle'))
    for x in (66, 340):
        o.append(rect(x, 266, 10, 34, '#e5e7eb', '#9ca3af', 1, 1))
    o.append(rect(50, 256, 320, 10, '#0e7490', '#155e75', 2, 1))
    o.append(text(210, 286, 'Arduino Uno R3', 9, '#a5f3fc', 'middle', '700'))
    o.append(rect(96, 240, 96, 16, '#111827', '#334155', 1, 1) + rect(222, 240, 120, 16, '#111827', '#334155', 1, 1))
    for x in range(102, 342, 12):
        if 192 < x < 222:
            continue
        o.append(line(x, 230, x, 248, '#eab308', 1.4))
    o.append(rect(50, 220, 320, 10, '#1d4ed8', '#1e3a8a', 2, 1))
    o.append(text(230, 184, 'shield de bornes (screw shield)', 8.5, '#93c5fd', 'middle', '700'))
    for k in range(10):
        x = 62 + k * 30
        o.append(rect(x, 194, 26, 26, '#2563eb', '#1e40af', 2, 1) + circle(x + 13, 201, 4, '#cbd5e1', '#64748b', 1))
    o.append(pwire('M30 150 C 50 150 52 207 66 207', 'io', 'fio com ilhós entrando no borne', 3))
    o.append(rect(56, 203, 12, 8, '#cbd5e1', '#64748b', 1, 1))
    o.append(pwire('M30 170 C 70 170 82 207 96 207', 'gnd', None, 3))
    o.append(rect(86, 203, 12, 8, '#cbd5e1', '#64748b', 1, 1))
    o.append(rect(348, 214, 10, 60, 'none', '#fbbf24', 3, 1.4, '3 2'))
    o.append(text(364, 196, 'abraçadeira', 8.5, '#fbbf24', 'end', '700'))
    o.append(text(78, 296, 'M3', 8, '#e5e7eb'))
    o.append('</g>')
    for i, t in enumerate(['1. Shield encaixado em todos os pinos', '2. Espaçador M3 + abraçadeira: não sai',
                           '   com vibração nem com puxão no fio', '3. Todo fio com ilhós; aperto firme',
                           '4. Puxão de teste ~2 kgf em cada fio']):
        o.append(text(36, 300 + i * 16, t, 9.5, '#cbd5e1'))

    # ---- Painel B: ilhós passo a passo ----
    o.append(rect(410, 20, 380, 390, '#0f172a', '#fbbf24', 12, 1.4, extra='stroke-opacity="0.6"'))
    o.append(text(426, 44, 'B · TERMINAL TUBULAR (ILHÓS)', 11, '#fcd34d', 'start', '800'))
    steps = [(426, 78, '1 · descascar 8 mm'), (610, 78, '2 · torcer os fios'),
             (426, 198, '3 · inserir até o colarinho'), (610, 198, '4 · crimpar e apertar')]
    for x, y, t in steps:
        o.append(rect(x, y, 168, 104, '#111827', '#334155', 8, 1))
        o.append(text(x + 10, y + 18, t, 9.5, INK, 'start', '700'))
    # 1
    o.append(rect(436, 128, 80, 14, '#14b8a6', None, 3))
    for k in range(5):
        o.append(line(516, 130 + k * 2.6, 548, 130 + k * 2.6, '#d97706', 1.2))
    o.append(dim_h(sid, 516, 548, 162, '8 mm', 8.5))
    # 2
    o.append(rect(620, 128, 80, 14, '#14b8a6', None, 3))
    o.append(pwire('M700 135 q4 -6 8 0 t8 0 t8 0 t8 0', 'rx', None, 3))
    # 3
    o.append(rect(436, 248, 70, 14, '#14b8a6', None, 3))
    o.append(rect(506, 244, 18, 22, '#ef4444', '#991b1b', 3, 1) + rect(524, 248, 34, 14, '#cbd5e1', '#94a3b8', 1, 1))
    o.append(text(541, 282, 'colarinho encosta na capa', 8, DIM, 'middle'))
    # 4
    o.append(rect(620, 248, 50, 14, '#14b8a6', None, 3))
    o.append(rect(670, 244, 18, 22, '#ef4444', '#991b1b', 3, 1) + rect(688, 250, 30, 10, '#94a3b8', '#64748b', 1, 1))
    o.append(rect(716, 236, 56, 38, '#2563eb', '#1e40af', 3, 1) + circle(744, 244, 5, '#cbd5e1', '#64748b', 1))
    o.append(text(744, 290, 'borne apertado', 8, DIM, 'middle'))
    for i, (t, c) in enumerate([('✓ alicate quadrado (crimpa 4 lados)', '#bbf7d0'),
                                ('✓ ilhós do tamanho do fio (0,5 mm² = branco/laranja)', '#bbf7d0'),
                                ('✗ nunca estanhar com solda a ponta que vai', '#fecaca'),
                                ('   sob parafuso: a solda escoa e afrouxa', '#fecaca')]):
        o.append(text(426, 330 + i * 15, t, 9.5, c))

    # ---- Painel C: certo x errado ----
    o.append(rect(800, 20, 380, 390, '#0f172a', '#38bdf8', 12, 1.4, extra='stroke-opacity="0.6"'))
    o.append(text(816, 44, 'C · CERTO × ERRADO', 11, '#7dd3fc', 'start', '800'))
    # juntas de solda
    for x0, ok in ((830, True), (1010, False)):
        o.append(rect(x0, 98, 70, 8, '#b45309', None, 1))
        o.append(line(x0 + 35, 60, x0 + 35, 104, '#cbd5e1', 2.4))
        if ok:
            o.append(f'<path d="M{x0+16} 98 Q{x0+30} 94 {x0+33} 72 L{x0+37} 72 Q{x0+40} 94 {x0+54} 98 Z" fill="#e5e7eb" stroke="#f8fafc" stroke-width="1"/>')
            o.append(text(x0 + 35, 124, '✓ cone brilhante', 9, '#bbf7d0', 'middle', '700'))
        else:
            o.append(circle(x0 + 35, 88, 14, '#6b7280', '#4b5563', 1))
            o.append(text(x0 + 35, 124, '✗ bola opaca (fria)', 9, '#fecaca', 'middle', '700'))
    rows = [('Ilhós no borne de parafuso', 'Ponta estanhada sob parafuso'),
            ('Wago 221 para juntar fios', 'Emenda torcida + fita isolante'),
            ('Borne plugável com trava', 'Jumper Dupont / protoboard'),
            ('Cabinho flexível estanhado', 'Fio rígido em ponto que mexe'),
            ('Prensa-cabo + abraçadeira', 'Cabo pendurado no borne'),
            ('Termo-retrátil em toda emenda', 'Solda exposta / sem isolação'),
            ('Verniz depois de testar', 'Cola quente sobre conector')]
    for i, (good, bad) in enumerate(rows):
        y = 156 + i * 34
        o.append(rect(816, y - 14, 170, 26, '#052e16', '#166534', 6, 1) + text(824, y + 3, '✓ ' + good, 8.5, '#bbf7d0', 'start', '600'))
        o.append(rect(994, y - 14, 172, 26, '#450a0a', '#7f1d1d', 6, 1) + text(1002, y + 3, '✗ ' + bad, 8.5, '#fecaca', 'start', '600'))
    o.append(text(1188, 424, 'PE-07 · sem escala', 9, DIM, 'end', '700'))
    o.append('</svg>')
    return ''.join(o)


# ============================================================================
# HTML DA ABA
# ============================================================================
def figure(fig_id, svg, minw, filename, caption):
    return f'''
        <figure class="pe-figure" id="{fig_id}">
          <div class="pe-fig-toolbar">
            <span class="pe-fig-caption"><i data-lucide="file-text" class="w-3.5 h-3.5"></i><span>{caption}</span></span>
            <div class="pe-fig-actions">
              <button type="button" onclick="peZoom('{fig_id}',-0.25)" title="Diminuir zoom"><i data-lucide="zoom-out" class="w-3.5 h-3.5"></i></button>
              <span class="pe-zoom-val" data-zoom-label>100%</span>
              <button type="button" onclick="peZoom('{fig_id}',0.25)" title="Aumentar zoom (ou Ctrl + roda do mouse)"><i data-lucide="zoom-in" class="w-3.5 h-3.5"></i></button>
              <button type="button" onclick="peZoom('{fig_id}',0)" title="Ajustar à largura"><i data-lucide="scan" class="w-3.5 h-3.5"></i></button>
              <button type="button" onclick="peFullscreen('{fig_id}')" title="Tela cheia"><i data-lucide="maximize" class="w-3.5 h-3.5"></i></button>
              <button type="button" onclick="peDownloadSvg('{fig_id}','{filename}')" title="Baixar desenho vetorial"><i data-lucide="download" class="w-3.5 h-3.5"></i><span class="hidden sm:inline">SVG</span></button>
            </div>
          </div>
          <div class="pe-canvas" data-minw="{minw}">{svg}</div>
        </figure>'''


def head(num, title, sub, code=None, tags=()):
    tg = ''.join(f'<span class="pe-tag pe-tag-{c}">{t}</span>' for t, c in tags)
    cd = f'<span class="pe-code">{code}</span>' if code else ''
    return f'''
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800">
          <div class="flex items-start gap-3">
            <div class="pe-num">{num:02d}</div>
            <div>
              <h2 class="text-lg md:text-xl font-bold text-white leading-tight">{title}</h2>
              <p class="text-xs md:text-sm text-slate-400 mt-0.5">{sub}</p>
            </div>
          </div>
          <div class="flex flex-wrap items-center gap-1.5">{cd}{tg}</div>
        </div>'''


def notes(items, cols='xl:grid-cols-4'):
    cards = ''.join(f'''
          <div class="pe-note pe-note-{c}">
            <div class="pe-note-ic"><i data-lucide="{ic}" class="w-4 h-4"></i></div>
            <div><div class="pe-note-t">{t}</div><div class="pe-note-d">{d}</div></div>
          </div>''' for ic, c, t, d in items)
    return f'<div class="grid grid-cols-1 md:grid-cols-2 {cols} gap-3">{cards}\n        </div>'


def net_chip(net):
    c, lb = NETS[net]
    return f'<span class="pe-netchip"><span style="background:{c}"></span>{esc(lb)}</span>'


def pin_table(tid, cols, rows):
    th = ''.join(f'<th>{c}</th>' for c in cols)
    trs = []
    for r in rows:
        cells = list(r)
        net = cells.pop(3)
        tds = (f'<td class="pe-pin">{cells[0]}</td><td>{cells[1]}</td><td>{cells[2]}</td>'
               f'<td>{net_chip(net)}</td><td class="pe-fn">{cells[3]}</td>')
        trs.append(f'<tr>{tds}</tr>')
    return f'''<div class="pe-table-wrap"><table id="{tid}" class="pe-table"><thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table></div>'''


MASTER_ROWS = [
    ('5V / GND', 'Fonte U1 5V 3A', 'Borne 5V/GND do proto shield (X1)', 'v5', 'Alimentação pelo pino 5V (regulado) — não usar Vin'),
    ('D18 · TX1', 'MAX485 U2', 'DI', 'tx', 'Transmissão Serial1 · 9600 8N1'),
    ('D19 · RX1', 'MAX485 U2', 'RO', 'rx', 'Recepção Serial1'),
    ('D2', 'MAX485 U2', 'DE + /RE (jumpeados)', 'de', 'HIGH = transmite · LOW = escuta'),
    ('D20 · SDA', 'LCD U3 (PCF8574)', 'SDA', 'i2c', 'I²C dados · endereço 0x27 (ou 0x3F)'),
    ('D21 · SCL', 'LCD U3 (PCF8574)', 'SCL', 'i2c', 'I²C clock'),
    ('D4', 'SW1 · NAV', 'Contato N.A. → GND', 'io', 'INPUT_PULLUP · navega / próximo'),
    ('D5', 'SW2 · HAB', 'Contato N.A. → GND', 'io', 'INPUT_PULLUP · habilita / desabilita'),
    ('D7', 'BZ1 buzzer ativo', '+ do buzzer', 'io', 'Alarme de falha de rede (≤ 30 mA)'),
    ('D6', 'Painel 47× WS2812B', 'DIN do LED #0 via R1 330 Ω', 'led', 'Dados 800 kHz · LED #0…#46 = P01…P47'),
    ('D22 … D35', 'Botões P01 … P14', 'Contato N.A. → GND', 'io', 'INPUT_PULLUP · 14 entradas'),
]
SLAVE_ROWS = [
    ('5V / GND', 'Fonte local 5V 2A', 'Borne 5V/GND do screw shield', 'v5', 'Cada sala tem a sua fonte; nunca ligar +5V entre salas'),
    ('D0 · RX', 'MAX485 U2', 'RO', 'rx', 'Recebe o polling · soltar ao gravar via USB'),
    ('D1 · TX', 'MAX485 U2', 'DI', 'tx', 'Responde o estado das 11 posições'),
    ('D4', 'MAX485 U2', 'DE + /RE (jumpeados)', 'de', 'HIGH só durante a resposta'),
    ('D5', '11× WS2812B locais', 'DIN do LED #0 via 330 Ω', 'led', 'Feedback do operador'),
    ('D6 … D12', 'Pos 01 … 07', 'Contato N.A. → GND', 'io', 'INPUT_PULLUP · debounce 40 ms'),
    ('A0 … A3 (D14 … D17)', 'Pos 08 … 11', 'Contato N.A. → GND', 'io', 'Analógicas usadas como digitais'),
]


def build_html():
    legend = ''.join(
        f'<button type="button" class="pe-legend-chip" data-pe-net="{k}" onclick="peFocusNet(\'{k}\')">'
        f'<span style="background:{c}"></span>{esc(lb)}</button>'
        for k, (c, lb) in NETS.items())

    pills = [('sec-topologia-predial', '01 Topologia'), ('sec-esquematico-master', '02 Central S1'),
             ('sec-esquematico-slaves', '03 Escravos S2–S4'), ('sec-utp-queda', '04 Cabo & queda'),
             ('sec-layout-quadro', '05 Quadro'), ('sec-corte-botoes', '06 Posições'),
             ('sec-montagem', '07 Ligações'), ('sec-pinagem', '08 Pinagem'),
             ('sec-comissionamento', '09 Comissionamento'), ('sec-firmwares', '10 Firmwares')]
    pills_html = ''.join(f'<a href="#{a}" class="pe-pill">{b}</a>' for a, b in pills)

    kpis = [('zap', 'Tensão', '5 V DC', 'SELV · sem 110 V nas salas', 'amber'),
            ('radio', 'Barramento', 'RS-485', '9600 bps · 8N1 · half-duplex', 'sky'),
            ('cable', 'Cabo', '45 m', '2 vias blindado + malha', 'indigo'),
            ('cpu', 'Nós', '4', '1 mestre + 3 escravos', 'emerald'),
            ('layout-grid', 'Posições', '47', '14 + 11 + 11 + 11', 'violet'),
            ('gauge', 'Consumo', '≈ 7,5 W', 'sistema completo', 'rose')]
    kpi_html = ''.join(f'''
            <div class="pe-kpi pe-kpi-{c}">
              <div class="flex items-center justify-between"><span class="pe-kpi-l">{l}</span><i data-lucide="{ic}" class="w-4 h-4"></i></div>
              <div class="pe-kpi-v">{v}</div><div class="pe-kpi-s">{s}</div>
            </div>''' for ic, l, v, s, c in kpis)

    balloons = ['Canaleta perfurada 20×20 mm (superior)', 'Trilho DIN 35 mm', 'Fonte U1 5V 3A (DIN)',
                'Porta-fusível F1 2 A', 'Bornes Wago 221: +5V · GND · A · B (X1)',
                'Módulo MAX485 (R7 120 Ω) + bias 560 Ω', 'Wago 221-413 (A, B, SH) + prensa-cabo PG7 → Sala 2',
                'Canaleta intermediária (separa AC do sinal)', 'Arduino Mega em espaçadores M3 de nylon',
                'Régua X2: bornes plugáveis do chicote da porta', 'Entrada AC 127/220 V com prensa-cabo',
                'Parafuso de aterramento PE da carcaça']
    balloons_html = ''.join(f'<li><span class="pe-ball">{i}</span>{t}</li>' for i, t in enumerate(balloons, 1))

    H = []
    H.append('''
    <!-- ============================================================== -->
    <!-- TAB: PROJETO ELÉTRICO (gerado por pe_tab.py)                    -->
    <!-- ============================================================== -->
    <section id="tab-schematic" class="tab-content hidden space-y-6">

      <!-- CABEÇALHO -->
      <div class="glass-panel rounded-3xl p-6 md:p-8 border border-indigo-500/30 relative overflow-hidden">
        <div class="absolute -right-24 -top-24 w-80 h-80 rounded-full bg-indigo-500/10 blur-3xl pointer-events-none"></div>
        <div class="absolute -left-24 -bottom-32 w-80 h-80 rounded-full bg-emerald-500/5 blur-3xl pointer-events-none"></div>
        <div class="relative flex flex-col xl:flex-row xl:items-end justify-between gap-6">
          <div class="space-y-3 max-w-3xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[11px] font-mono font-bold">
              <i data-lucide="zap" class="w-3.5 h-3.5"></i><span>PROJETO ELÉTRICO EXECUTIVO · REV. 5.0 · 7 PRANCHAS</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Projeto Elétrico — 47 posições em 4 salas</h1>
            <p class="text-sm text-slate-300 leading-relaxed">
              Esquemas com fios, bornes e pinos reais da central (Mega 2560) e das estações remotas (Arduino Uno R3),
              topologia do barramento RS-485 em cabo blindado de 2 vias, alimentação local em cada painel, layout do quadro,
              detalhe das posições, <b>como fazer as ligações sem mau contato</b>, pinagem, comissionamento e firmwares.
            </p>
            <p class="text-xs text-slate-400 flex items-center gap-1.5"><i data-lucide="mouse-pointer-click" class="w-3.5 h-3.5 text-indigo-400"></i>
              Passe o mouse sobre um fio para destacar o circuito inteiro · use zoom, tela cheia e exportação SVG em cada prancha.</p>
          </div>
          <div class="flex flex-wrap gap-2 pe-noprint">
            <button onclick="downloadMasterIno()" class="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/20 transition"><i data-lucide="download" class="w-4 h-4"></i>master_mega.ino</button>
            <button onclick="downloadSlaveIno()" class="pe-btn-ghost pe-btn-lg"><i data-lucide="download" class="w-4 h-4 text-emerald-400"></i>slave_uno.ino</button>
            <button onclick="window.print()" class="pe-btn-ghost pe-btn-lg"><i data-lucide="printer" class="w-4 h-4 text-amber-400"></i>Imprimir</button>
          </div>
        </div>
        <div class="relative grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-3 mt-6">%%KPIS%%
        </div>
      </div>

      <!-- NAVEGAÇÃO FIXA + LEGENDA -->
      <nav id="pe-subnav" class="pe-subnav pe-noprint">
        <div class="pe-subnav-inner">
          <div id="pe-pills" class="pe-pills">%%PILLS%%</div>
          <button type="button" class="pe-legend-toggle" onclick="document.getElementById('pe-legend-row').classList.toggle('hidden')">
            <i data-lucide="palette" class="w-3.5 h-3.5"></i><span>Cores dos fios</span>
          </button>
        </div>
        <div id="pe-legend-row" class="pe-legend-row hidden">
          <span class="text-[11px] text-slate-400 font-mono mr-1">Clique para destacar:</span>%%LEGEND%%
          <button type="button" class="pe-legend-clear" onclick="peFocusNet(null)">limpar</button>
        </div>
      </nav>
''')

    # ---- 01 Topologia
    H.append(f'''
      <div id="sec-topologia-predial" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(1, 'Topologia predial do barramento', 'Ligação em linha (daisy-chain) entre as 4 salas, com terminação nas duas pontas', 'PE-01', [('45 m', 'sky'), ('RS-485', 'indigo')])}
        {figure('fig-topo', diagram_topology(), 900, 'PE-01_topologia.svg', 'PE-01 · Topologia predial · sem escala')}
        <div class="pe-table-wrap">
          <table class="pe-table">
            <thead><tr><th>Trecho</th><th>De → Para</th><th>Comprimento</th><th>Cabo / eletroduto</th><th>Observação</th></tr></thead>
            <tbody>
              <tr><td class="pe-pin">T1</td><td>Sala 1 → Sala 2</td><td class="pe-pin">15 m</td><td>2 vias blindado · ¾″</td><td class="pe-fn">sai do X3 da central (PG7), chega nos Wago da Sala 2</td></tr>
              <tr><td class="pe-pin">T2</td><td>Sala 2 → Sala 3</td><td class="pe-pin">12 m</td><td>2 vias blindado · ¾″</td><td class="pe-fn">sai dos mesmos Wago da Sala 2, chega na Sala 3</td></tr>
              <tr><td class="pe-pin">T3</td><td>Sala 3 → Sala 4</td><td class="pe-pin">18 m</td><td>2 vias blindado · ¾″</td><td class="pe-fn">sai da Sala 3, termina na Sala 4 (fim de linha)</td></tr>
              <tr class="pe-total"><td class="pe-pin">Σ</td><td>Total</td><td class="pe-pin">45 m</td><td>compre 60 m (folga)</td><td class="pe-fn">limite da norma em 9600 bps: 1200 m</td></tr>
            </tbody>
          </table>
        </div>
        {notes([
            ('git-commit-horizontal', 'sky', 'Só em linha', 'O cabo entra e sai de cada caixa. Nada de &ldquo;T&rdquo;, estrela ou emenda no meio do caminho.'),
            ('circle-slash', 'amber', 'Terminação nas pontas', '120 Ω apenas na Sala 1 e na Sala 4. Com tudo desligado, A–B deve medir ≈ 60 Ω.'),
            ('shield-check', 'emerald', 'Polarização fail-safe', '560 Ω (A→+5V e B→GND) só na Sala 1: mantém A–B ≥ +200 mV com a linha ociosa.'),
            ('plug-zap', 'rose', 'Fonte em cada painel', 'Energia não passa pelo cabo: ele leva só A e B (2 vias) e a malha serve de referência. Nunca ligue o +5V de salas diferentes.'),
        ])}
      </div>
''')

    # ---- 02 Mestre
    H.append(f'''
      <div id="sec-esquematico-master" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(2, 'Esquema elétrico da central — Sala 1', 'Arduino Mega 2560, fonte, MAX485 com terminação/polarização, LCD, IHM, painel de 47 LEDs e 14 botões', 'PE-02', [('Mega 2560', 'sky'), ('Mestre', 'indigo')])}
        {figure('fig-master', diagram_master(), 980, 'PE-02_central_sala1.svg', 'PE-02 · Central Sala 1 · Arduino Mega 2560')}
        {notes([
            ('battery-charging', 'rose', 'Alimentação', 'Fonte 5 V no pino <b>5V</b> do Mega (não no Vin). C1 1000 µF segura os picos dos LEDs; C2 100 nF filtra ruído.'),
            ('arrow-left-right', 'indigo', 'Direção do MAX485', 'DE e /RE ligados juntos no <b>D2</b>: HIGH transmite, LOW escuta. Serial1 = D18/D19.'),
            ('mouse-pointer-2', 'emerald', 'Botões', 'Todos fecham para GND com <b>INPUT_PULLUP</b>. No contato circulam 5 V e ~0,1 mA: sem risco e sem faísca.'),
            ('lightbulb', 'amber', 'Linha dos LEDs', 'R1 330 Ω perto do Mega, GND comum entre fonte, Mega e fita, e 5 V injetado nas duas pontas.'),
        ])}
      </div>
''')

    # ---- 03 Escravos
    H.append(f'''
      <div id="sec-esquematico-slaves" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(3, 'Esquema elétrico das estações remotas — Salas 2, 3 e 4', 'Mesmo circuito nas três salas: muda só o SLAVE_ID e o resistor de terminação R7 do módulo', 'PE-03', [('Uno R3', 'emerald'), ('ID 2 · 3 · 4', 'indigo')])}
        {figure('fig-slave', diagram_slave(), 980, 'PE-03_escravos.svg', 'PE-03 · Nós escravos · Salas 2, 3 e 4')}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="pe-room pe-room-emerald"><div class="pe-room-h">Sala 2 · ID 2</div><div>Arduino <b>Uno R3</b> (já existe)</div><div>Posições P15–P25 · cabo entra e sai</div><div>R7 <b>removido</b> · malha via 100 Ω</div></div>
          <div class="pe-room pe-room-sky"><div class="pe-room-h">Sala 3 · ID 3</div><div>Arduino <b>Uno R3</b> (comprar)</div><div>Posições P26–P36 · cabo entra e sai</div><div>R7 <b>removido</b> · malha via 100 Ω</div></div>
          <div class="pe-room pe-room-violet"><div class="pe-room-h">Sala 4 · ID 4</div><div>Arduino <b>Uno R3</b> (comprar)</div><div>Posições P37–P47 · só cabo de entrada</div><div>R7 <b>mantido</b> (fim de linha) · malha via 100 Ω</div></div>
        </div>
        {notes([
            ('repeat', 'sky', 'Entra e sai no mesmo Wago', 'Cada linha (A, B, SH) usa um Wago 221-413: cabo que chega + cabo que sai + fio curto até o MAX485.'),
            ('hash', 'indigo', 'Identificação', 'Antes de gravar, ajuste <code>#define SLAVE_ID</code> para 2, 3 ou 4.'),
            ('usb', 'amber', 'Gravação via USB', 'D0/D1 são a mesma serial da USB: solte RO/DI do MAX485 enquanto grava.'),
            ('lock', 'rose', 'Posição desabilitada', 'Com a posição em azul (sem uso no dia), o botão é ignorado pelo firmware.'),
        ])}
      </div>
''')

    # ---- 04 Cabo e queda de tensão
    H.append(f'''
      <div id="sec-utp-queda" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(4, 'Cabo de 2 vias e alimentação local', 'Cabo blindado de par trançado entre as salas e a calculadora que mostra por que a fonte fica em cada painel', 'PE-04', [('2 vias + malha', 'sky'), ('24 AWG', 'amber')])}
        <div class="grid grid-cols-1 xl:grid-cols-5 gap-5">
          <div class="xl:col-span-2 space-y-3">
            {figure('fig-cabo', diagram_cable(), 460, 'PE-04_cabo_2_vias.svg', 'PE-04 · Cabo blindado 2 vias')}
            <div class="pe-callout pe-callout-sky">
              <i data-lucide="info" class="w-4 h-4 shrink-0 mt-0.5"></i>
              <div>Use a <b>mesma cor para A e para B nas 4 salas</b> e teste cada trecho com multímetro antes de ligar: continuidade A–A, B–B e malha, e nenhum curto entre eles.</div>
            </div>
          </div>

          <div class="xl:col-span-3 pe-calc space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <h3 class="text-sm font-bold text-white flex items-center gap-2"><i data-lucide="calculator" class="w-4 h-4 text-amber-400"></i>Calculadora de queda de tensão</h3>
              <div class="pe-seg" role="radiogroup">
                <label><input type="radio" name="pe-mode" value="local" checked onchange="peCalc()"><span>Fontes locais (projeto)</span></label>
                <label><input type="radio" name="pe-mode" value="central" onchange="peCalc()"><span>Tudo pela Sala 1 (cabo de 4 vias)</span></label>
              </div>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5">
              <label class="pe-field"><span>Tensão da fonte (V)</span><input id="pe-v" type="number" step="0.05" value="5.10" oninput="peCalc()"></label>
              <label class="pe-field"><span>Corrente por sala (A)</span><input id="pe-i" type="number" step="0.01" value="0.20" oninput="peCalc()"></label>
              <label class="pe-field"><span>Fios por polo</span><select id="pe-n" onchange="peCalc()"><option value="1">1 fio</option><option value="2" selected>2 fios (par)</option><option value="4">4 fios</option></select></label>
              <label class="pe-field"><span>Ω/m por fio (24 AWG)</span><input id="pe-rho" type="number" step="0.001" value="0.0842" oninput="peCalc()"></label>
              <label class="pe-field"><span>Trecho 1 S1→S2 (m)</span><input id="pe-l1" type="number" value="15" oninput="peCalc()"></label>
              <label class="pe-field"><span>Trecho 2 S2→S3 (m)</span><input id="pe-l2" type="number" value="12" oninput="peCalc()"></label>
              <label class="pe-field"><span>Trecho 3 S3→S4 (m)</span><input id="pe-l3" type="number" value="18" oninput="peCalc()"></label>
              <div class="pe-field pe-field-ro"><span>Resistência do laço</span><b id="pe-rloop">—</b></div>
            </div>
            <div id="pe-calc-nodes" class="grid grid-cols-2 md:grid-cols-4 gap-2.5"></div>
            <div id="pe-calc-verdict"></div>
            <div class="pe-formula">ΔV<sub>trecho</sub> = I<sub>trecho</sub> × L × (2 × ρ ÷ fios por polo) &nbsp;·&nbsp; I<sub>T1</sub> = 3·I, I<sub>T2</sub> = 2·I, I<sub>T3</sub> = I</div>
          </div>
        </div>
      </div>
''')

    # ---- 05 Quadro
    H.append(f'''
      <div id="sec-layout-quadro" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(5, 'Layout do quadro da Sala 1', 'Frente do painel (o que o supervisor vê) e placa de montagem interna (o que o eletricista monta)', 'PE-05', [('420 × 260 mm', 'amber'), ('Trilho DIN', 'indigo')])}
        {figure('fig-quadro', diagram_panel(), 980, 'PE-05_quadro_sala1.svg', 'PE-05 · Quadro da Sala 1 · vistas frontal e interna')}
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div class="lg:col-span-2 pe-list-card">
            <div class="pe-list-h"><i data-lucide="list-ordered" class="w-4 h-4 text-amber-400"></i>Itens da vista interna (balões)</div>
            <ol class="pe-balloons">{balloons_html}</ol>
          </div>
          {notes([
              ('separator-horizontal', 'amber', 'Separação AC × sinal', 'A canaleta do meio separa a entrada 127/220 V dos fios de 5 V e RS-485.'),
              ('wrench', 'emerald', 'Manutenção', 'Bornes de alavanca e conectores: dá para trocar Mega, fonte ou módulo sem solda.'),
          ], cols='lg:grid-cols-1')}
        </div>
      </div>
''')

    # ---- 06 Posições
    H.append(f'''
      <div id="sec-corte-botoes" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(6, 'Detalhe construtivo de uma posição', 'Como montar o LED e o botão em cada posição e como ligar no Arduino', 'PE-06', [('Botão 22 mm', 'amber'), ('WS2812B', 'emerald')])}
        {figure('fig-botoes', diagram_buttons(), 980, 'PE-06_detalhe_posicao.svg', 'PE-06 · Detalhe de montagem de uma posição')}
        <div class="pe-callout pe-callout-amber">
          <i data-lucide="alert-triangle" class="w-4 h-4 shrink-0 mt-0.5"></i>
          <div><b>Atenção:</b> a lâmpada BA9s é de uma cor só e não consegue mostrar verde/vermelho/azul. Para as cores do projeto,
          use o <b>pixel WS2812B</b> (Opção 1). A BA9s só serve se o retorno local puder ser apenas aceso/apagado.</div>
        </div>
      </div>
''')

    # ---- 07 Montagem e ligações
    H.append(f'''
      <div id="sec-montagem" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(7, 'Como fazer as ligações nos Arduinos', 'Solda, bornes e conectores: o que usar em cada ponto para não soltar, não oxidar e não dar mau contato', 'PE-07', [('Ilhós', 'amber'), ('Screw shield', 'emerald')])}
        {figure('fig-montagem', diagram_assembly(), 980, 'PE-07_ligacoes_arduino.svg', 'PE-07 · Ligações confiáveis nos Arduinos')}
        <div class="pe-table-wrap">
          <table class="pe-table">
            <thead><tr><th>Ponto de ligação</th><th>Método</th><th>Por quê</th></tr></thead>
            <tbody>
              <tr><td class="pe-pin">Pinos do Uno (Salas 2–4)</td><td><b>Shield de bornes</b> (screw shield) encaixado + espaçador M3 + abraçadeira</td><td class="pe-fn">nada de solda no Arduino; trocar a placa leva 5 minutos</td></tr>
              <tr><td class="pe-pin">Pinos do Mega (Sala 1)</td><td><b>Mega Proto Shield</b> com barras de pinos e bornes KRE 5,08 mm soldados</td><td class="pe-fn">solda feita uma vez, em bancada; o Mega fica intacto</td></tr>
              <tr><td class="pe-pin">Fio em qualquer borne</td><td><b>Terminal tubular (ilhós)</b> crimpado com alicate quadrado</td><td class="pe-fn">os fios finos não se espalham e o aperto não afrouxa</td></tr>
              <tr><td class="pe-pin">Cabo entre salas (A, B, SH)</td><td><b>Wago 221-413</b> com ilhós + prensa-cabo PG7</td><td class="pe-fn">junta 3 fios por linha sem emenda; mola não afrouxa com o tempo</td></tr>
              <tr><td class="pe-pin">Módulo MAX485</td><td>fios <b>soldados</b> nos furos do módulo + termo-retrátil (ou borne do módulo com ilhós)</td><td class="pe-fn">pinos de módulo com Dupont soltam com vibração</td></tr>
              <tr><td class="pe-pin">Pixels WS2812B</td><td>fio 26 AWG <b>soldado</b> nos pads + termo-retrátil + alívio com silicone neutro</td><td class="pe-fn">os pads são pequenos; o alívio impede que o puxão arranque o pad</td></tr>
              <tr><td class="pe-pin">Botões 22 mm antigos</td><td><b>Terminal garfo</b> pré-isolado + arruela de pressão</td><td class="pe-fn">o garfo fica preso pelo parafuso mesmo se afrouxar um pouco</td></tr>
              <tr><td class="pe-pin">Chicote da porta</td><td><b>Borne plugável 5,08 mm com trava</b> (KF2EDG)</td><td class="pe-fn">permite tirar o painel sem desparafusar fio a fio</td></tr>
              <tr><td class="pe-pin">Fonte 5 V</td><td>borne 5V/GND do shield + <b>Wago</b> de distribuição para os LEDs</td><td class="pe-fn">a corrente dos LEDs não passa pelas trilhas do Arduino</td></tr>
            </tbody>
          </table>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div class="pe-list-card">
            <div class="pe-list-h"><i data-lucide="list-ordered" class="w-4 h-4 text-emerald-400"></i>Passo a passo · Uno (Salas 2, 3 e 4)</div>
            <ol class="pe-steps">
              <li>Grave o firmware com o Uno <b>sozinho</b> no USB (sem o MAX485 em D0/D1) e com o <code>SLAVE_ID</code> da sala.</li>
              <li>Encaixe o shield de bornes em todos os pinos; prenda o conjunto na placa de montagem com espaçadores M3 de nylon e trave com uma abraçadeira.</li>
              <li>Crimpe ilhós em todos os fios. Ligue primeiro a fonte (5V/GND), confira 5,0 V no borne, depois o MAX485 (RO→D0, DI→D1, DE+/RE→D4).</li>
              <li>Ligue o DIN dos LEDs no D5 passando pelo resistor de 330 Ω (soldado e encapado) e os 11 botões em D6…D12 e A0…A3, com retorno comum ao GND.</li>
              <li>Coloque anilha em cada fio, amarre o chicote a cada 10–15 cm e deixe 10 cm de folga perto da placa.</li>
              <li>Puxe cada fio com cerca de 2 kgf. Depois do teste geral, aplique verniz isolante na placa (com fita nos bornes e conectores).</li>
            </ol>
          </div>
          <div class="pe-list-card">
            <div class="pe-list-h"><i data-lucide="list-ordered" class="w-4 h-4 text-sky-400"></i>Passo a passo · Mega (Sala 1)</div>
            <ol class="pe-steps">
              <li>Na bancada, solde no Mega Proto Shield as barras de pinos e os bornes KRE (5V, GND, D2, D4–D7, D18–D21, D22–D35).</li>
              <li>Ferro a ~350 °C, solda com fluxo: junta em forma de cone e brilhante. Limpe o fluxo com álcool isopropílico.</li>
              <li>Antes de encaixar no Mega, teste continuidade borne → pino e ausência de curto entre vizinhos com o multímetro.</li>
              <li>Monte os resistores de polarização (560 Ω A→5V e B→GND) no shield ou no borne do MAX485; mantenha o R7 (120 Ω) do módulo.</li>
              <li>Ligue o cabo da Sala 2 nos Wago X3 (A, B e malha); a malha vai direto ao GND só nesta sala.</li>
              <li>Chicote da porta (14 botões, NAV/HAB, buzzer, LCD, LEDs) em bornes plugáveis com trava.</li>
            </ol>
          </div>
        </div>
        <div class="pe-callout pe-callout-sky">
          <i data-lucide="book-open" class="w-4 h-4 shrink-0 mt-0.5"></i>
          <div>O guia completo, com ferramentas, fotos de referência descritas e a lista de verificação de montagem, está em <code>docs/MONTAGEM_E_CONEXOES.md</code> no repositório.</div>
        </div>
      </div>
''')

    # ---- 08 Pinagem
    H.append(f'''
      <div id="sec-pinagem" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(8, 'Pinagem e mapa das 47 posições', 'Tabelas pino a pino para montagem e um mapa completo posição → sala → pino → LED', 'PE-07', [('Busca', 'indigo')])}
        <div class="grid grid-cols-1 2xl:grid-cols-2 gap-5">
          <div class="space-y-2.5">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <h3 class="pe-h3"><i data-lucide="cpu" class="w-4 h-4 text-sky-400"></i>Central · Arduino Mega 2560 (Sala 1)</h3>
              <input class="pe-search" placeholder="Filtrar pinos…" oninput="peFilterTable(this,'pe-tbl-master')">
            </div>
            {pin_table('pe-tbl-master', ['Pino', 'Destino', 'Terminal', 'Rede', 'Função'], MASTER_ROWS)}
          </div>
          <div class="space-y-2.5">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <h3 class="pe-h3"><i data-lucide="radio" class="w-4 h-4 text-emerald-400"></i>Remotas · Arduino Uno R3 (Salas 2, 3 e 4)</h3>
              <input class="pe-search" placeholder="Filtrar pinos…" oninput="peFilterTable(this,'pe-tbl-slave')">
            </div>
            {pin_table('pe-tbl-slave', ['Pino', 'Destino', 'Terminal', 'Rede', 'Função'], SLAVE_ROWS)}
          </div>
        </div>

        <div class="space-y-2.5 pt-2">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <h3 class="pe-h3"><i data-lucide="map" class="w-4 h-4 text-amber-400"></i>Mapa das 47 posições</h3>
            <div class="flex flex-wrap items-center gap-2">
              <div id="pe-pos-filter" class="pe-seg pe-seg-sm">
                <button type="button" data-room="0" class="active" onclick="peSetRoom(0)">Todas</button>
                <button type="button" data-room="1" onclick="peSetRoom(1)">S1</button>
                <button type="button" data-room="2" onclick="peSetRoom(2)">S2</button>
                <button type="button" data-room="3" onclick="peSetRoom(3)">S3</button>
                <button type="button" data-room="4" onclick="peSetRoom(4)">S4</button>
              </div>
              <input id="pe-pos-q" class="pe-search" placeholder="Ex.: P23, A2, D9…" oninput="peRenderPositions()">
            </div>
          </div>
          <div class="pe-table-wrap pe-table-scroll">
            <table class="pe-table" id="pe-tbl-pos">
              <thead><tr><th>Posição</th><th>Sala</th><th>Pos. na sala</th><th>Controlador</th><th>Pino de entrada</th><th>LED central</th><th>LED local</th><th>Bit no quadro</th></tr></thead>
              <tbody></tbody>
            </table>
          </div>
          <div id="pe-pos-count" class="text-[11px] text-slate-500 font-mono"></div>
        </div>
      </div>
''')

    # ---- 08 Comissionamento
    H.append(f'''
      <div id="sec-comissionamento" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(9, 'Checklist de comissionamento', 'Marque cada teste conforme for aprovado; o progresso fica salvo neste navegador', 'CK-01…12', [('Multímetro', 'amber')])}
        <div class="flex flex-wrap items-center gap-3">
          <div class="flex-1 min-w-[220px]">
            <div class="flex justify-between text-xs font-mono text-slate-400 mb-1"><span>Progresso</span><span id="pe-ck-label">0 / 12</span></div>
            <div class="pe-progress"><div id="pe-ck-bar"></div></div>
          </div>
          <button type="button" onclick="peResetChecklist()" class="pe-btn-ghost pe-noprint"><i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>Limpar</button>
        </div>
        <div id="pe-checklist" class="grid grid-cols-1 lg:grid-cols-2 gap-3"></div>
      </div>
''')

    # ---- 09 Firmwares
    H.append(f'''
      <div id="sec-firmwares" class="pe-section glass-panel rounded-3xl p-5 md:p-7 space-y-5">
        {head(10, 'Firmwares (.ino)', 'Código-fonte comentado linha a linha, para gravar pela Arduino IDE', None, [('Protocolo v2', 'emerald'), ('C++', 'sky')])}
        <div class="pe-callout pe-callout-sky">
          <i data-lucide="info" class="w-4 h-4 shrink-0 mt-0.5"></i>
          <div><b>Protocolo RS-485 v2 unificado:</b> pedido do mestre <code>A5 ID SEQ MASK_H MASK_L CRC8</code> e resposta do escravo
          <code>5A ID SEQ EST_H EST_L CRC8</code> (CRC-8, polinômio 0x07). Arquivos no repositório:
          <code>firmware/master_mega/master_mega.ino</code> (Sala 1) e <code>firmware/slave_uno/slave_uno.ino</code> (Salas 2–4 — mude
          <code>SLAVE_ID</code> para 2, 3 ou 4). Bibliotecas: <b>Adafruit NeoPixel</b> e <b>LiquidCrystal I2C</b>.</div>
        </div>
        <div class="flex flex-wrap items-center gap-2 border-b border-slate-800 pb-3">
          <button id="btn-fw-mega" onclick="switchFwView('mega')" class="px-4 py-2 rounded-xl bg-indigo-600 text-white font-bold text-xs shadow-lg shadow-indigo-600/20 transition cursor-pointer flex items-center gap-2 border border-transparent">
            <i data-lucide="cpu" class="w-4 h-4"></i><span>master_mega.ino · Sala 1</span>
          </button>
          <button id="btn-fw-nano" onclick="switchFwView('nano')" class="px-4 py-2 rounded-xl bg-slate-900 text-slate-400 hover:text-white font-bold text-xs border border-slate-800 transition cursor-pointer flex items-center gap-2">
            <i data-lucide="radio" class="w-4 h-4 text-emerald-400"></i><span>slave_uno.ino · Salas 2–4</span>
          </button>
        </div>
        <div id="fw-view-mega" class="space-y-3">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div class="text-xs text-slate-400 font-mono">Arquivo <strong class="text-indigo-400">firmware/master_mega/master_mega.ino</strong> · Mega 2560 · <span id="pe-fw-mega-meta"></span></div>
            <div class="flex items-center gap-2">
              <button onclick="copyMasterIno()" class="pe-btn-ghost"><i data-lucide="copy" class="w-3.5 h-3.5"></i>Copiar</button>
              <button onclick="downloadMasterIno()" class="pe-btn-ghost"><i data-lucide="download" class="w-3.5 h-3.5 text-emerald-400"></i>Baixar .ino</button>
            </div>
          </div>
          <pre class="pe-code-view"><code id="code-master-mega">Carregando master_mega.ino...</code></pre>
        </div>
        <div id="fw-view-nano" class="hidden space-y-3">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div class="text-xs text-slate-400 font-mono">Arquivo <strong class="text-emerald-400">firmware/slave_uno/slave_uno.ino</strong> · Uno R3 · <span id="pe-fw-nano-meta"></span></div>
            <div class="flex items-center gap-2">
              <button onclick="copySlaveIno()" class="pe-btn-ghost"><i data-lucide="copy" class="w-3.5 h-3.5"></i>Copiar</button>
              <button onclick="downloadSlaveIno()" class="pe-btn-ghost"><i data-lucide="download" class="w-3.5 h-3.5 text-emerald-400"></i>Baixar .ino</button>
            </div>
          </div>
          <pre class="pe-code-view"><code id="code-slave-nano">Carregando slave_uno.ino...</code></pre>
        </div>
      </div>

    </section>
''')
    html = ''.join(H)
    return (html.replace('%%KPIS%%', kpi_html).replace('%%PILLS%%', pills_html)
                .replace('%%LEGEND%%', legend))


# ============================================================================
# CSS
# ============================================================================
TAB_CSS = r'''
    /* =========================================================================
       ABA PROJETO ELÉTRICO (pe_tab.py)
       ========================================================================= */
    #tab-schematic .grid > *, #tab-schematic .flex > * { min-width: 0; }
    .pe-figure { max-width: 100%; }
    .pe-section { scroll-margin-top: 128px; }
    @media (max-width: 1023px) { .pe-section { scroll-margin-top: 168px; } }
    .pe-subnav { position: sticky; top: 56px; z-index: 40; border-radius: 16px; border: 1px solid rgba(99,102,241,.25);
      background: rgba(3,7,18,.88); backdrop-filter: blur(14px); box-shadow: 0 10px 30px rgba(0,0,0,.35); }
    @media (max-width: 1023px) { .pe-subnav { top: 96px; } }
    .pe-subnav-inner { display: flex; align-items: center; gap: 8px; padding: 8px; }
    .pe-pills { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; flex: 1; scroll-behavior: smooth; }
    .pe-pills::-webkit-scrollbar { display: none; }
    .pe-pill { white-space: nowrap; font: 600 11px 'JetBrains Mono', monospace; color: #94a3b8; padding: 6px 11px; border-radius: 10px;
      border: 1px solid transparent; transition: all .15s; }
    .pe-pill:hover { color: #fff; background: rgba(30,41,59,.8); }
    .pe-pill.active { color: #fff; background: rgba(99,102,241,.22); border-color: rgba(129,140,248,.55); }
    .pe-legend-toggle, .pe-legend-clear, .pe-btn-ghost { display: inline-flex; align-items: center; gap: 6px; white-space: nowrap;
      font: 700 11px 'JetBrains Mono', monospace; color: #cbd5e1; padding: 6px 10px; border-radius: 10px; border: 1px solid #1e293b;
      background: #0f172a; cursor: pointer; transition: all .15s; }
    .pe-legend-toggle:hover, .pe-legend-clear:hover, .pe-btn-ghost:hover { border-color: #6366f1; color: #fff; }
    .pe-btn-lg { padding: 8px 14px; border-radius: 12px; font-size: 12px; }
    .pe-legend-row { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; padding: 0 10px 10px; }
    .pe-legend-row.hidden { display: none; }
    .pe-legend-chip { display: inline-flex; align-items: center; gap: 6px; font: 600 11px Inter, sans-serif; color: #cbd5e1;
      padding: 4px 9px; border-radius: 999px; border: 1px solid #1e293b; background: #0b1120; cursor: pointer; transition: all .15s; }
    .pe-legend-chip span, .pe-netchip span { width: 14px; height: 4px; border-radius: 2px; display: inline-block; }
    .pe-legend-chip:hover { border-color: #475569; color: #fff; }
    .pe-legend-chip.active { border-color: #a5b4fc; color: #fff; background: rgba(99,102,241,.2); }

    .pe-kpi { border-radius: 16px; padding: 12px 14px; border: 1px solid rgba(148,163,184,.14); background: rgba(2,6,23,.55); }
    .pe-kpi-l { font: 700 10px 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: .08em; color: #94a3b8; }
    .pe-kpi-v { font: 800 22px 'JetBrains Mono', monospace; color: #fff; margin-top: 4px; }
    .pe-kpi-s { font-size: 11px; color: #94a3b8; }
    .pe-kpi-amber i { color: #fbbf24; } .pe-kpi-sky i { color: #38bdf8; } .pe-kpi-indigo i { color: #818cf8; }
    .pe-kpi-emerald i { color: #34d399; } .pe-kpi-violet i { color: #c084fc; } .pe-kpi-rose i { color: #fb7185; }

    .pe-num { width: 40px; height: 40px; flex-shrink: 0; border-radius: 12px; display: flex; align-items: center; justify-content: center;
      font: 800 14px 'JetBrains Mono', monospace; color: #c7d2fe; background: linear-gradient(135deg, rgba(99,102,241,.35), rgba(16,185,129,.15));
      border: 1px solid rgba(129,140,248,.4); }
    .pe-code { font: 800 11px 'JetBrains Mono', monospace; color: #fbbf24; padding: 3px 9px; border-radius: 8px;
      border: 1px solid rgba(251,191,36,.35); background: rgba(251,191,36,.08); }
    .pe-tag { font: 700 10px 'JetBrains Mono', monospace; padding: 3px 9px; border-radius: 999px; border: 1px solid; }
    .pe-tag-sky { color: #7dd3fc; border-color: rgba(56,189,248,.35); background: rgba(56,189,248,.08); }
    .pe-tag-indigo { color: #a5b4fc; border-color: rgba(129,140,248,.35); background: rgba(129,140,248,.08); }
    .pe-tag-emerald { color: #6ee7b7; border-color: rgba(52,211,153,.35); background: rgba(52,211,153,.08); }
    .pe-tag-amber { color: #fcd34d; border-color: rgba(251,191,36,.35); background: rgba(251,191,36,.08); }

    .pe-figure { margin: 0; border: 1px solid #1e293b; border-radius: 16px; overflow: hidden; background: #0b1120; }
    .pe-fig-toolbar { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px; padding: 7px 10px;
      background: #0f172a; border-bottom: 1px solid #1e293b; font: 600 11px 'JetBrains Mono', monospace; color: #94a3b8; }
    .pe-fig-caption { display: inline-flex; align-items: center; gap: 6px; }
    .pe-fig-actions { display: flex; align-items: center; gap: 4px; }
    .pe-fig-actions button { display: inline-flex; align-items: center; gap: 4px; height: 26px; padding: 0 8px; border-radius: 8px;
      border: 1px solid #1e293b; background: #111827; color: #cbd5e1; cursor: pointer; font: 700 11px 'JetBrains Mono', monospace; }
    .pe-fig-actions button:hover { border-color: #6366f1; color: #fff; }
    .pe-zoom-val { min-width: 44px; text-align: center; color: #cbd5e1; }
    .pe-canvas { overflow: auto; max-height: 80vh; cursor: grab; }
    .pe-canvas.dragging { cursor: grabbing; user-select: none; }
    .pe-canvas svg { display: block; width: 100%; height: auto; }
    .pe-figure:fullscreen { border-radius: 0; display: flex; flex-direction: column; background: #020617; }
    .pe-figure:fullscreen .pe-canvas { flex: 1; max-height: none; }
    .pe-svg .net { transition: opacity .18s ease; }
    .pe-svg .net.pe-dim { opacity: .09; }
    .pe-svg .net.pe-hl { filter: drop-shadow(0 0 3px rgba(255,255,255,.55)); }

    .pe-note { display: flex; gap: 10px; padding: 12px; border-radius: 14px; border: 1px solid rgba(148,163,184,.14); background: rgba(2,6,23,.45); }
    .pe-note-ic { width: 30px; height: 30px; border-radius: 9px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
    .pe-note-t { font-size: 12.5px; font-weight: 700; color: #f1f5f9; }
    .pe-note-d { font-size: 12px; color: #94a3b8; line-height: 1.5; margin-top: 2px; }
    .pe-note-d b { color: #e2e8f0; } .pe-note-d code { font-size: 11px; color: #fcd34d; }
    .pe-note-sky .pe-note-ic { background: rgba(56,189,248,.12); color: #38bdf8; }
    .pe-note-amber .pe-note-ic { background: rgba(251,191,36,.12); color: #fbbf24; }
    .pe-note-emerald .pe-note-ic { background: rgba(52,211,153,.12); color: #34d399; }
    .pe-note-rose .pe-note-ic { background: rgba(251,113,133,.12); color: #fb7185; }
    .pe-note-indigo .pe-note-ic { background: rgba(129,140,248,.12); color: #818cf8; }

    .pe-callout { display: flex; gap: 10px; padding: 12px 14px; border-radius: 14px; font-size: 12.5px; line-height: 1.55; border: 1px solid; }
    .pe-callout code { font-size: 11.5px; }
    .pe-callout-sky { color: #bae6fd; border-color: rgba(56,189,248,.3); background: rgba(56,189,248,.07); }
    .pe-callout-amber { color: #fde68a; border-color: rgba(251,191,36,.35); background: rgba(251,191,36,.07); }
    .pe-callout-rose { color: #fecdd3; border-color: rgba(251,113,133,.35); background: rgba(251,113,133,.07); }

    .pe-room { padding: 12px 14px; border-radius: 14px; border: 1px solid; font-size: 12px; color: #cbd5e1; line-height: 1.7; background: rgba(2,6,23,.45); }
    .pe-room b { color: #fff; }
    .pe-room-h { font: 800 12px 'JetBrains Mono', monospace; margin-bottom: 2px; }
    .pe-room-emerald { border-color: rgba(52,211,153,.35); } .pe-room-emerald .pe-room-h { color: #34d399; }
    .pe-room-sky { border-color: rgba(56,189,248,.35); } .pe-room-sky .pe-room-h { color: #38bdf8; }
    .pe-room-violet { border-color: rgba(192,132,252,.35); } .pe-room-violet .pe-room-h { color: #c084fc; }

    .pe-table-wrap { overflow-x: auto; border-radius: 14px; border: 1px solid #1e293b; }
    .pe-table-scroll { max-height: 440px; overflow-y: auto; }
    .pe-table { width: 100%; border-collapse: collapse; font-size: 12px; color: #cbd5e1; }
    .pe-table thead th { position: sticky; top: 0; background: #0f172a; color: #94a3b8; font: 700 10.5px 'JetBrains Mono', monospace;
      text-transform: uppercase; letter-spacing: .05em; text-align: left; padding: 10px 12px; border-bottom: 1px solid #1e293b; white-space: nowrap; }
    .pe-table td { padding: 8px 12px; border-bottom: 1px solid rgba(30,41,59,.7); vertical-align: middle; }
    .pe-table td { white-space: nowrap; } .pe-table td.pe-fn { white-space: normal; min-width: 220px; }
    .pe-table tbody tr:hover { background: rgba(99,102,241,.06); }
    .pe-table .pe-pin { font: 800 11.5px 'JetBrains Mono', monospace; color: #e2e8f0; white-space: nowrap; }
    .pe-table .pe-fn { color: #94a3b8; }
    .pe-table .pe-total td { background: rgba(99,102,241,.07); font-weight: 700; }
    .pe-netchip { display: inline-flex; align-items: center; gap: 6px; font: 600 11px Inter, sans-serif; white-space: nowrap; }
    .pe-h3 { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 700; color: #fff; }
    .pe-search { background: #0b1120; border: 1px solid #1e293b; color: #e2e8f0; border-radius: 10px; padding: 6px 10px;
      font: 500 12px 'JetBrains Mono', monospace; outline: none; min-width: 180px; }
    .pe-search:focus { border-color: #6366f1; }
    .pe-room-badge { font: 800 10px 'JetBrains Mono', monospace; padding: 2px 7px; border-radius: 6px; }

    .pe-calc { padding: 16px; border-radius: 16px; border: 1px solid #1e293b; background: rgba(2,6,23,.55); }
    .pe-seg { display: inline-flex; padding: 3px; border-radius: 11px; background: #0b1120; border: 1px solid #1e293b; gap: 2px; }
    .pe-seg label { cursor: pointer; }
    .pe-seg input { display: none; }
    .pe-seg span, .pe-seg button { display: inline-block; padding: 5px 10px; border-radius: 8px; font: 700 11px 'JetBrains Mono', monospace;
      color: #94a3b8; cursor: pointer; border: 0; background: transparent; }
    .pe-seg input:checked + span, .pe-seg button.active { background: #4f46e5; color: #fff; }
    .pe-field { display: flex; flex-direction: column; gap: 4px; font: 600 10.5px 'JetBrains Mono', monospace; color: #94a3b8; }
    .pe-field input, .pe-field select { background: #0b1120; border: 1px solid #1e293b; color: #f1f5f9; border-radius: 9px;
      padding: 7px 9px; font: 700 13px 'JetBrains Mono', monospace; outline: none; width: 100%; }
    .pe-field input:focus, .pe-field select:focus { border-color: #6366f1; }
    .pe-field-ro b { padding: 7px 9px; border-radius: 9px; border: 1px dashed #1e293b; color: #fcd34d; font: 800 13px 'JetBrains Mono', monospace; }
    .pe-node { padding: 12px; border-radius: 14px; border: 1px solid #1e293b; background: #0b1120; }
    .pe-node-n { font: 700 11px 'JetBrains Mono', monospace; color: #94a3b8; display: flex; justify-content: space-between; }
    .pe-node-v { font: 800 24px 'JetBrains Mono', monospace; margin: 4px 0; }
    .pe-node-bar { height: 6px; border-radius: 99px; background: #1e293b; overflow: hidden; }
    .pe-node-bar div { height: 100%; border-radius: 99px; transition: width .3s; }
    .pe-node-s { font-size: 11px; color: #94a3b8; margin-top: 6px; }
    .pe-ok { color: #34d399; } .pe-warn { color: #fbbf24; } .pe-bad { color: #fb7185; }
    .pe-formula { font: 600 11.5px 'JetBrains Mono', monospace; color: #94a3b8; padding: 10px 12px; border-radius: 10px;
      background: #0b1120; border: 1px dashed #1e293b; }

    .pe-list-card { padding: 16px; border-radius: 16px; border: 1px solid #1e293b; background: rgba(2,6,23,.45); }
    .pe-list-h { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 700; color: #fff; margin-bottom: 10px; }
    .pe-balloons { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 6px 16px; font-size: 12px; color: #cbd5e1; }
    .pe-balloons li { display: flex; align-items: center; gap: 8px; }
    .pe-ball { width: 20px; height: 20px; border-radius: 50%; background: #fbbf24; color: #0b1120; font: 800 10.5px 'JetBrains Mono', monospace;
      display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; }

    .pe-steps { list-style: decimal; padding-left: 20px; display: flex; flex-direction: column; gap: 8px; font-size: 12.5px; color: #cbd5e1; line-height: 1.55; }
    .pe-steps b { color: #fff; } .pe-steps code { font-size: 11.5px; color: #fcd34d; }
    body.theme-light .pe-steps { color: #334155; } body.theme-light .pe-steps b { color: #0f172a; } body.theme-light .pe-steps code { color: #b45309; }
    .pe-progress { height: 8px; border-radius: 99px; background: #1e293b; overflow: hidden; }
    .pe-progress div { height: 100%; width: 0; border-radius: 99px; background: linear-gradient(90deg, #6366f1, #10b981); transition: width .3s; }
    .pe-ck { display: flex; gap: 12px; padding: 12px 14px; border-radius: 14px; border: 1px solid #1e293b; background: rgba(2,6,23,.45);
      cursor: pointer; transition: all .15s; }
    .pe-ck:hover { border-color: #334155; }
    .pe-ck input { width: 18px; height: 18px; margin-top: 2px; accent-color: #10b981; flex-shrink: 0; cursor: pointer; }
    .pe-ck.done { border-color: rgba(16,185,129,.45); background: rgba(16,185,129,.06); }
    .pe-ck-id { font: 800 11px 'JetBrains Mono', monospace; color: #fbbf24; }
    .pe-ck-t { font-size: 13px; font-weight: 700; color: #f1f5f9; }
    .pe-ck-d { font-size: 12px; color: #94a3b8; margin-top: 2px; }
    .pe-ck-c { font: 700 11.5px 'JetBrains Mono', monospace; color: #6ee7b7; margin-top: 4px; }

    .pe-code-view { padding: 16px; border-radius: 16px; background: #020617; border: 1px solid #1e293b; color: #cbd5e1;
      font: 12px/1.6 'JetBrains Mono', monospace; overflow: auto; max-height: 520px; tab-size: 2; }

    .pe-toast { transition: opacity .3s, transform .3s; }

    /* Manual renderizado (docs/MANUAL_TECNICO.md) */
    .pe-md { font-size: 14px; line-height: 1.7; color: #cbd5e1; max-width: 1100px; }
    .pe-md h1 { font-size: 26px; font-weight: 800; color: #fff; margin: 8px 0 14px; }
    .pe-md h2 { font-size: 20px; font-weight: 800; color: #fff; margin: 34px 0 12px; padding-bottom: 8px; border-bottom: 1px solid #1e293b; }
    .pe-md h3 { font-size: 16px; font-weight: 700; color: #e2e8f0; margin: 24px 0 8px; }
    .pe-md h4 { font-size: 14px; font-weight: 700; color: #e2e8f0; margin: 18px 0 6px; }
    .pe-md p { margin: 10px 0; }
    .pe-md ul, .pe-md ol { margin: 8px 0 12px; padding-left: 22px; }
    .pe-md ul { list-style: disc; } .pe-md ol { list-style: decimal; }
    .pe-md li { margin: 4px 0; }
    .pe-md strong { color: #fff; }
    .pe-md a { color: #818cf8; text-decoration: underline; }
    .pe-md code { font: 12.5px 'JetBrains Mono', monospace; color: #fcd34d; background: rgba(15,23,42,.8); padding: 1px 5px; border-radius: 5px; }
    .pe-md pre { background: #020617; border: 1px solid #1e293b; border-radius: 12px; padding: 14px; overflow-x: auto; margin: 12px 0; }
    .pe-md pre code { background: none; padding: 0; color: #cbd5e1; font-size: 12px; line-height: 1.5; }
    .pe-md table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; display: block; overflow-x: auto; }
    .pe-md th { background: #0f172a; color: #94a3b8; text-align: left; padding: 8px 10px; border: 1px solid #1e293b; white-space: nowrap; }
    .pe-md td { padding: 7px 10px; border: 1px solid #1e293b; vertical-align: top; }
    .pe-md blockquote { border-left: 3px solid #6366f1; padding: 6px 14px; margin: 12px 0; background: rgba(99,102,241,.07); border-radius: 0 10px 10px 0; color: #c7d2fe; }
    .pe-md hr { border: 0; border-top: 1px solid #1e293b; margin: 24px 0; }
    body.theme-light .pe-md { color: #334155; }
    body.theme-light .pe-md h1, body.theme-light .pe-md h2, body.theme-light .pe-md h3, body.theme-light .pe-md h4, body.theme-light .pe-md strong { color: #0f172a; }
    body.theme-light .pe-md h2, body.theme-light .pe-md th, body.theme-light .pe-md td, body.theme-light .pe-md hr { border-color: #e2e8f0; }
    body.theme-light .pe-md th { background: #f1f5f9; color: #475569; }
    body.theme-light .pe-md code { background: #f1f5f9; color: #b45309; }
    body.theme-light .pe-md pre { background: #0f172a; }

    /* Tema claro */
    body.theme-light .pe-subnav { background: rgba(255,255,255,.95); border-color: #e2e8f0; box-shadow: 0 6px 20px rgba(15,23,42,.08); }
    body.theme-light .pe-pill { color: #475569; }
    body.theme-light .pe-pill:hover { background: #f1f5f9; color: #0f172a; }
    body.theme-light .pe-pill.active { background: #eef2ff; color: #3730a3; border-color: #c7d2fe; }
    body.theme-light .pe-legend-toggle, body.theme-light .pe-legend-clear, body.theme-light .pe-btn-ghost,
    body.theme-light .pe-legend-chip, body.theme-light .pe-search, body.theme-light .pe-field input,
    body.theme-light .pe-field select, body.theme-light .pe-seg { background: #fff; border-color: #cbd5e1; color: #0f172a; }
    body.theme-light .pe-kpi, body.theme-light .pe-note, body.theme-light .pe-room, body.theme-light .pe-calc,
    body.theme-light .pe-list-card, body.theme-light .pe-ck, body.theme-light .pe-node, body.theme-light .pe-formula { background: #f8fafc; border-color: #e2e8f0; }
    body.theme-light .pe-kpi-v, body.theme-light .pe-note-t, body.theme-light .pe-ck-t, body.theme-light .pe-h3,
    body.theme-light .pe-list-h, body.theme-light .pe-room b, body.theme-light .pe-note-d b { color: #0f172a; }
    body.theme-light .pe-note-d, body.theme-light .pe-room, body.theme-light .pe-balloons, body.theme-light .pe-ck-d { color: #475569; }
    body.theme-light .pe-table { color: #334155; }
    body.theme-light .pe-table-wrap { border-color: #e2e8f0; }
    body.theme-light .pe-table thead th { background: #f1f5f9; color: #475569; border-color: #e2e8f0; }
    body.theme-light .pe-table td { border-color: #eef2f7; }
    body.theme-light .pe-table .pe-pin { color: #0f172a; }
    body.theme-light .pe-callout-sky { color: #075985; } body.theme-light .pe-callout-amber { color: #92400e; }
    body.theme-light .pe-callout-rose { color: #9f1239; }
    body.theme-light .pe-num { color: #3730a3; background: #eef2ff; border-color: #c7d2fe; }
    body.theme-light .pe-code, body.theme-light .pe-field-ro b, body.theme-light .pe-note-d code,
    body.theme-light .pe-ck-id { color: #b45309; }
    body.theme-light .pe-tag-sky { color: #0369a1; } body.theme-light .pe-tag-indigo { color: #4338ca; }
    body.theme-light .pe-tag-emerald { color: #047857; } body.theme-light .pe-tag-amber { color: #b45309; }
    body.theme-light .pe-ck-c { color: #047857; }

    @media print {
      .pe-noprint, .pe-fig-actions { display: none !important; }
      .pe-canvas { max-height: none !important; overflow: visible !important; }
      .pe-canvas svg { width: 100% !important; min-width: 0 !important; }
      .pe-figure, .pe-section { break-inside: avoid; }
      .pe-table-scroll { max-height: none !important; }
    }
'''


# ============================================================================
# JS
# ============================================================================
TAB_JS = r'''
    // =========================================================================
    // ABA PROJETO ELÉTRICO (pe_tab.py)
    // =========================================================================
    if (typeof window.showToast !== 'function') {
      window.showToast = function (msg, type) {
        let box = document.getElementById('pe-toast-box');
        if (!box) {
          box = document.createElement('div');
          box.id = 'pe-toast-box';
          box.style.cssText = 'position:fixed;right:16px;bottom:16px;z-index:9999;display:flex;flex-direction:column;gap:8px;align-items:flex-end;pointer-events:none';
          document.body.appendChild(box);
        }
        const colors = { success: '#059669', info: '#4f46e5', warn: '#d97706', error: '#e11d48' };
        const t = document.createElement('div');
        t.className = 'pe-toast';
        t.style.cssText = 'padding:10px 16px;border-radius:12px;color:#fff;font:600 12px Inter,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.4);background:' + (colors[type] || colors.info);
        t.textContent = msg;
        box.appendChild(t);
        setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateY(6px)'; }, 2400);
        setTimeout(() => t.remove(), 2900);
      };
    }

    const PE_ZOOM = {};
    function peApplyZoom(figId) {
      const fig = document.getElementById(figId);
      if (!fig) return;
      const canvas = fig.querySelector('.pe-canvas');
      const svg = canvas && canvas.querySelector('svg');
      if (!svg) return;
      const z = PE_ZOOM[figId] || 1;
      const minw = parseFloat(canvas.dataset.minw) || 800;
      svg.style.width = (z * 100) + '%';
      svg.style.minWidth = Math.round(minw * z) + 'px';
      const lbl = fig.querySelector('[data-zoom-label]');
      if (lbl) lbl.textContent = Math.round(z * 100) + '%';
    }
    function peZoom(figId, delta) {
      let z = PE_ZOOM[figId] || 1;
      z = delta === 0 ? 1 : Math.min(3, Math.max(0.5, +(z + delta).toFixed(2)));
      PE_ZOOM[figId] = z;
      peApplyZoom(figId);
    }
    function peFullscreen(figId) {
      const fig = document.getElementById(figId);
      if (!fig) return;
      if (document.fullscreenElement) { document.exitFullscreen(); return; }
      const fn = fig.requestFullscreen || fig.webkitRequestFullscreen;
      if (fn) fn.call(fig);
    }
    function peDownloadSvg(figId, filename) {
      const svg = document.querySelector('#' + figId + ' svg');
      if (!svg) return;
      const clone = svg.cloneNode(true);
      clone.querySelectorAll('.pe-dim, .pe-hl').forEach(e => e.classList.remove('pe-dim', 'pe-hl'));
      clone.style.width = ''; clone.style.minWidth = '';
      const vb = svg.viewBox.baseVal;
      clone.setAttribute('width', vb.width); clone.setAttribute('height', vb.height);
      const data = '<?xml version="1.0" encoding="UTF-8"?>\n' + new XMLSerializer().serializeToString(clone);
      const url = URL.createObjectURL(new Blob([data], { type: 'image/svg+xml;charset=utf-8' }));
      const a = document.createElement('a');
      a.href = url; a.download = filename;
      document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(url);
      showToast('Prancha ' + filename + ' exportada em SVG (vetorial).', 'success');
    }

    // ---------- destaque de circuitos ----------
    let PE_NET_LOCK = null, PE_NET_SHOWN = undefined;
    function peSetFocus(net) {
      if (net === PE_NET_SHOWN) return;
      PE_NET_SHOWN = net;
      document.querySelectorAll('.pe-svg .net').forEach(el => {
        const on = !net || el.classList.contains('n-' + net);
        el.classList.toggle('pe-dim', !!net && !on);
        el.classList.toggle('pe-hl', !!net && on);
      });
      document.querySelectorAll('[data-pe-net]').forEach(b => b.classList.toggle('active', b.dataset.peNet === net));
    }
    function peFocusNet(net) {
      PE_NET_LOCK = (net && PE_NET_LOCK !== net) ? net : null;
      peSetFocus(PE_NET_LOCK);
    }
    function peBindSvgHover(svg) {
      svg.addEventListener('mouseover', e => {
        const el = e.target.closest('.net');
        if (!el) { peSetFocus(PE_NET_LOCK); return; }
        const cls = [...el.classList].find(c => c.startsWith('n-'));
        if (cls) peSetFocus(cls.slice(2));
      });
      svg.addEventListener('mouseleave', () => peSetFocus(PE_NET_LOCK));
    }

    // ---------- arrastar / zoom com roda ----------
    function peEnablePan(canvas, figId) {
      let down = false, sx = 0, sy = 0, sl = 0, st = 0;
      canvas.addEventListener('pointerdown', e => {
        if (e.pointerType !== 'mouse' || e.button !== 0) return;
        if (canvas.scrollWidth <= canvas.clientWidth && canvas.scrollHeight <= canvas.clientHeight) return;
        down = true; sx = e.clientX; sy = e.clientY; sl = canvas.scrollLeft; st = canvas.scrollTop;
        canvas.classList.add('dragging');
      });
      window.addEventListener('pointermove', e => {
        if (!down) return;
        canvas.scrollLeft = sl - (e.clientX - sx);
        canvas.scrollTop = st - (e.clientY - sy);
      });
      window.addEventListener('pointerup', () => { down = false; canvas.classList.remove('dragging'); });
      canvas.addEventListener('wheel', e => {
        if (!e.ctrlKey) return;
        e.preventDefault();
        peZoom(figId, e.deltaY < 0 ? 0.1 : -0.1);
      }, { passive: false });
    }

    // ---------- navegação com seção ativa ----------
    function peInitScrollSpy() {
      const pills = [...document.querySelectorAll('#pe-pills a')];
      if (!pills.length || !('IntersectionObserver' in window)) return;
      const box = document.getElementById('pe-pills');
      const map = new Map(pills.map(p => [p.getAttribute('href').slice(1), p]));
      const obs = new IntersectionObserver(entries => {
        entries.forEach(en => {
          if (!en.isIntersecting) return;
          pills.forEach(p => p.classList.remove('active'));
          const p = map.get(en.target.id);
          if (p) { p.classList.add('active'); box.scrollTo({ left: p.offsetLeft - box.clientWidth / 2 + p.clientWidth / 2 }); }
        });
      }, { rootMargin: '-40% 0px -55% 0px' });
      map.forEach((p, id) => { const s = document.getElementById(id); if (s) obs.observe(s); });
    }

    // ---------- calculadora de queda de tensão ----------
    function peNum(id, def) { const v = parseFloat(document.getElementById(id)?.value); return isFinite(v) ? v : def; }
    function peFmt(v, d) { return v.toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d }); }
    function peCalc() {
      const host = document.getElementById('pe-calc-nodes');
      if (!host) return;
      const mode = document.querySelector('input[name="pe-mode"]:checked')?.value || 'local';
      const V = peNum('pe-v', 5.1), I = peNum('pe-i', 0.2), nf = peNum('pe-n', 2), rho = peNum('pe-rho', 0.0842);
      const L = [peNum('pe-l1', 15), peNum('pe-l2', 12), peNum('pe-l3', 18)];
      const rloop = 2 * rho / nf;
      document.getElementById('pe-rloop').textContent = peFmt(rloop, 4) + ' Ω/m';
      const nodes = [{ name: 'Sala 1', v: V, info: 'fonte da central' }];
      let v = V, total = 0;
      const segI = [3 * I, 2 * I, I];
      for (let i = 0; i < 3; i++) {
        if (mode === 'central') {
          const dv = segI[i] * L[i] * rloop;
          total += dv; v -= dv;
          nodes.push({ name: 'Sala ' + (i + 2), v, info: 'T' + (i + 1) + ': ' + peFmt(segI[i], 2) + ' A · −' + peFmt(dv, 3) + ' V' });
        } else {
          nodes.push({ name: 'Sala ' + (i + 2), v: V, info: 'fonte local · cabo só com A/B' });
        }
      }
      host.innerHTML = nodes.map(nd => {
        const st = nd.v >= 4.75 ? ['pe-ok', '#10b981', 'OK'] : nd.v >= 4.5 ? ['pe-warn', '#f59e0b', 'LIMITE'] : ['pe-bad', '#f43f5e', 'FALHA'];
        const pct = Math.max(0, Math.min(100, (nd.v - 3) / (5.5 - 3) * 100));
        return '<div class="pe-node"><div class="pe-node-n"><span>' + nd.name + '</span><span class="' + st[0] + '">' + st[2] + '</span></div>' +
          '<div class="pe-node-v ' + st[0] + '">' + peFmt(nd.v, 2) + ' V</div>' +
          '<div class="pe-node-bar"><div style="width:' + pct + '%;background:' + st[1] + '"></div></div>' +
          '<div class="pe-node-s">' + nd.info + '</div></div>';
      }).join('');
      const vmin = Math.min(...nodes.map(x => x.v));
      const verdict = document.getElementById('pe-calc-verdict');
      let cls, msg;
      if (mode === 'local') {
        cls = 'pe-callout-sky';
        msg = '<b>Projeto adotado:</b> cada painel tem fonte 5 V própria, então o cabo entre salas precisa de <b>só 2 vias</b> (A e B) — a malha serve de referência. Corrente no cabo: poucos mA, queda desprezível. <b>Não interligue o +5V de fontes diferentes.</b>';
      } else if (vmin < 4.5) {
        cls = 'pe-callout-rose';
        msg = '<b>Inviável:</b> a Sala 4 recebe ' + peFmt(vmin, 2) + ' V (queda total de ' + peFmt(total, 2) + ' V, ' + peFmt(total / V * 100, 1) + '%). Abaixo de 4,5 V o ATmega328P e os WS2812B ficam instáveis. Use fontes locais.';
      } else if (vmin < 4.75) {
        cls = 'pe-callout-amber';
        msg = '<b>No limite:</b> Sala 4 com ' + peFmt(vmin, 2) + ' V (queda de ' + peFmt(total, 2) + ' V). Funciona em bancada, mas sem margem. Prefira fontes locais.';
      } else {
        cls = 'pe-callout-sky';
        msg = '<b>Aceitável:</b> menor tensão ' + peFmt(vmin, 2) + ' V (queda de ' + peFmt(total, 2) + ' V).';
      }
      verdict.innerHTML = '<div class="pe-callout ' + cls + '"><i data-lucide="info" class="w-4 h-4 shrink-0 mt-0.5"></i><div>' + msg + '</div></div>';
      if (window.lucide) lucide.createIcons();
    }

    // ---------- mapa das 47 posições ----------
    const PE_PIN11 = ['D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'A0 (D14)', 'A1 (D15)', 'A2 (D16)', 'A3 (D17)'];
    const PE_ROOM_COL = { 1: '#818cf8', 2: '#34d399', 3: '#38bdf8', 4: '#c084fc' };
    let PE_ROOM = 0;
    function peBuildPositions() {
      const rows = [];
      for (let i = 0; i < 14; i++) rows.push({ p: i + 1, sala: 1, local: i + 1, ctrl: 'Mega 2560 · mestre', pin: 'D' + (22 + i), led: i, ledLocal: '—', bit: '— (local)' });
      [['Uno R3 · ID 2', 2], ['Uno R3 · ID 3', 3], ['Uno R3 · ID 4', 4]].forEach(([ctrl, sala], k) => {
        for (let i = 0; i < 11; i++) {
          const p = 15 + k * 11 + i;
          rows.push({ p, sala, local: i + 1, ctrl, pin: PE_PIN11[i], led: p - 1, ledLocal: '#' + i, bit: 'bit ' + i });
        }
      });
      return rows;
    }
    const PE_POS = peBuildPositions();
    function peSetRoom(r) {
      PE_ROOM = r;
      document.querySelectorAll('#pe-pos-filter button').forEach(b => b.classList.toggle('active', +b.dataset.room === r));
      peRenderPositions();
    }
    function peRenderPositions() {
      const tb = document.querySelector('#pe-tbl-pos tbody');
      if (!tb) return;
      const q = (document.getElementById('pe-pos-q')?.value || '').trim().toLowerCase();
      const list = PE_POS.filter(r => (!PE_ROOM || r.sala === PE_ROOM) &&
        (!q || ('p' + String(r.p).padStart(2, '0') + ' sala ' + r.sala + ' ' + r.ctrl + ' ' + r.pin + ' #' + r.led).toLowerCase().includes(q)));
      tb.innerHTML = list.map(r => {
        const c = PE_ROOM_COL[r.sala];
        return '<tr><td class="pe-pin">P' + String(r.p).padStart(2, '0') + '</td>' +
          '<td><span class="pe-room-badge" style="color:' + c + ';background:' + c + '1f;border:1px solid ' + c + '55">S' + r.sala + '</span></td>' +
          '<td class="pe-pin">' + String(r.local).padStart(2, '0') + '</td><td>' + r.ctrl + '</td>' +
          '<td class="pe-pin" style="color:#5eead4">' + r.pin + '</td><td class="pe-pin" style="color:#4ade80">#' + r.led + '</td>' +
          '<td class="pe-pin">' + r.ledLocal + '</td><td class="pe-fn">' + r.bit + '</td></tr>';
      }).join('') || '<tr><td colspan="8" class="pe-fn" style="text-align:center;padding:18px">Nenhuma posição encontrada.</td></tr>';
      const cnt = document.getElementById('pe-pos-count');
      if (cnt) cnt.textContent = list.length + ' de 47 posições';
    }
    function peFilterTable(input, tableId) {
      const q = input.value.trim().toLowerCase();
      document.querySelectorAll('#' + tableId + ' tbody tr').forEach(tr => {
        tr.style.display = !q || tr.textContent.toLowerCase().includes(q) ? '' : 'none';
      });
    }

    // ---------- checklist de comissionamento ----------
    const PE_CHECKS = [
      ['CK-01', 'Rede antiga de 110 V isolada', 'Multímetro em 600 V~ entre botões/carcaça e terra.', '0,00 V~ em todos os pontos'],
      ['CK-02', 'Resistência do barramento A–B', 'Tudo desligado, multímetro em 200 Ω entre A e B.', '60 Ω ± 3 Ω (duas terminações)'],
      ['CK-03', 'Tensão das fontes em vazio', 'Medir +V/−V de cada fonte (S1 a S4).', '5,05 V a 5,20 V DC'],
      ['CK-04', 'Tensão com carga plena', 'Todos os LEDs acesos; medir 5V–GND em cada placa (fonte local).', '≥ 4,85 V DC em todas as salas'],
      ['CK-05', 'Polarização fail-safe', 'Rede em repouso; medir V entre A (+) e B (−).', 'V(A–B) ≥ +200 mV'],
      ['CK-06', 'Botões e debounce', '10 toques rápidos em cada botão de cada sala.', '100% das trocas, sem repique'],
      ['CK-07', 'Alarme de falha de rede', 'Soltar o fio B na Sala 2 e cronometrar.', 'Âmbar + buzzer em 2,0 s ± 0,2 s'],
      ['CK-08', 'Recuperação automática', 'Religar o fio sem reiniciar as placas.', 'Volta ao normal em < 0,5 s'],
      ['CK-09', 'Temperatura dos LEDs', 'Termômetro IR após 2 h de operação a 40%.', '≤ 38 °C'],
      ['CK-10', 'Presets na EEPROM', 'Gravar preset, desligar 5 min e religar.', 'Máscara restaurada 100%'],
      ['CK-11', 'Tração e aperto', 'Puxar cada fio com ~2 kgf; reapertar bornes de parafuso.', 'Nenhum fio solta ou gira no borne'],
      ['CK-12', 'Inspeção de soldas e ilhós', 'Lupa em todas as soldas, ilhós e termo-retráteis.', 'Juntas brilhantes, sem cobre exposto'],
    ];
    const PE_CK_KEY = 'pe_checklist_v1';
    function peLoadChecks() { try { return JSON.parse(localStorage.getItem(PE_CK_KEY) || '{}'); } catch (e) { return {}; } }
    function peRenderChecklist() {
      const host = document.getElementById('pe-checklist');
      if (!host) return;
      const st = peLoadChecks();
      host.innerHTML = PE_CHECKS.map(([id, t, d, c]) =>
        '<label class="pe-ck' + (st[id] ? ' done' : '') + '"><input type="checkbox" ' + (st[id] ? 'checked' : '') +
        ' onchange="peToggleCheck(\'' + id + '\', this.checked)"><div><div class="flex items-center gap-2"><span class="pe-ck-id">' + id +
        '</span><span class="pe-ck-t">' + t + '</span></div><div class="pe-ck-d">' + d + '</div><div class="pe-ck-c">✓ ' + c + '</div></div></label>'
      ).join('');
      const done = PE_CHECKS.filter(([id]) => st[id]).length;
      document.getElementById('pe-ck-label').textContent = done + ' / ' + PE_CHECKS.length + (done === PE_CHECKS.length ? ' · sistema aceito' : '');
      document.getElementById('pe-ck-bar').style.width = (done / PE_CHECKS.length * 100) + '%';
    }
    function peToggleCheck(id, on) {
      const st = peLoadChecks();
      if (on) st[id] = new Date().toISOString(); else delete st[id];
      try { localStorage.setItem(PE_CK_KEY, JSON.stringify(st)); } catch (e) {}
      peRenderChecklist();
    }
    function peResetChecklist() {
      try { localStorage.removeItem(PE_CK_KEY); } catch (e) {}
      peRenderChecklist();
      showToast('Checklist de comissionamento limpo.', 'info');
    }

    function peRenderManual() {
      const el = document.getElementById('manual-render');
      if (!el || typeof MANUAL_MARKDOWN_CONTENT === 'undefined') return;
      if (window.marked && typeof marked.parse === 'function') {
        el.innerHTML = marked.parse(MANUAL_MARKDOWN_CONTENT);
      } else {
        const pre = document.createElement('pre');
        pre.textContent = MANUAL_MARKDOWN_CONTENT;
        el.innerHTML = '';
        el.appendChild(pre);
      }
    }

    function peInit() {
      document.querySelectorAll('.pe-figure').forEach(f => {
        peApplyZoom(f.id);
        const c = f.querySelector('.pe-canvas');
        if (c) peEnablePan(c, f.id);
      });
      document.querySelectorAll('.pe-svg').forEach(peBindSvgHover);
      peInitScrollSpy();
      peCalc();
      peRenderPositions();
      peRenderChecklist();
      peRenderManual();
      try {
        const m = document.getElementById('pe-fw-mega-meta'), s = document.getElementById('pe-fw-nano-meta');
        if (m) m.textContent = CODE_MASTER_MEGA_SRC.split('\n').length + ' linhas';
        if (s) s.textContent = CODE_SLAVE_NANO_SRC.split('\n').length + ' linhas';
      } catch (e) {}
    }
    window.addEventListener('DOMContentLoaded', peInit);
'''


if __name__ == '__main__':
    html = build_html()
    print(f'HTML da aba: {len(html)} bytes')

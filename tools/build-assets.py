#!/usr/bin/env python3
"""Builds the animated SVG assets for the profile README.

    python tools/build-assets.py

Everything is pure SVG (SMIL + CSS), no scripts, no external fonts or images,
so it renders inside GitHub's camo <img> proxy. Run it after editing and commit
the generated files in assets/.
"""
from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

SANS = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif"
MONO = "'Cascadia Code', 'Fira Code', Consolas, 'SF Mono', Menlo, monospace"

PALETTES = {
    "dark": dict(
        bg0="#0b1220", bg1="#101a30", bg2="#0c1626",
        grid="#58a6ff", star="#cfe3ff",
        text="#f0f6fc", sub="#9ecbff", muted="#8b98a9", mono="#7ee787",
        blue="#58a6ff", green="#7ee787", orange="#f78166", yellow="#e3b341",
        card="#0f1a2e", cardStroke="#243352", cardTitle="#c9d1d9", cardText="#8b98a9",
        edge="#2f4470", pill="#162238", pillStroke="#2a3c5e",
        tokenA="#58a6ff", tokenB="#7ee787", tokenC="#b083f0",
        hairline="url(#accent)",
    ),
    "light": dict(
        bg0="#f6f8fa", bg1="#eef3fb", bg2="#f3f6fb",
        grid="#0969da", star="#0969da",
        text="#0f172a", sub="#0550ae", muted="#57606a", mono="#1a7f37",
        blue="#0969da", green="#1a7f37", orange="#cf222e", yellow="#9a6700",
        card="#ffffff", cardStroke="#d0d7de", cardTitle="#1f2328", cardText="#57606a",
        edge="#afb8c1", pill="#ffffff", pillStroke="#d0d7de",
        tokenA="#0969da", tokenB="#1a7f37", tokenC="#8250df",
        hairline="url(#accent)",
    ),
}

T = 14.0  # master loop seconds


def kt(t: float) -> str:
    """seconds -> keyTimes fraction string"""
    return f"{max(0.0, min(1.0, t / T)):.4f}"


def discrete(attr: str, steps: list[tuple[float, str]], *, extra: str = "") -> str:
    """SMIL discrete animation over the master loop.

    steps: list of (time_seconds, value); value holds until the next step.
    Always pads so keyTimes start at 0 and end at 1.
    """
    steps = sorted(steps, key=lambda s: s[0])
    if steps[0][0] > 0:
        steps = [(0.0, steps[0][1])] + steps  # hold first value from 0
    vals = [v for _, v in steps] + [steps[-1][1]]
    times = [kt(t) for t, _ in steps] + ["1"]
    return (f'<animate attributeName="{attr}" values="{";".join(vals)}" '
            f'keyTimes="{";".join(times)}" calcMode="discrete" dur="{T}s" '
            f'repeatCount="indefinite" {extra}/>')


def typewriter_steps(start: float, n_chars: float, cps: float, cw: float,
                     hold_until: float | None, erase_cps: float | None,
                     end_val: float = 0.0) -> list[tuple[float, float]]:
    """Discrete width steps for a clip rect: type, hold, (erase)."""
    steps: list[tuple[float, float]] = [(0.0, 0.0)]
    n = int(n_chars)
    for i in range(1, n + 1):
        steps.append((start + i / cps, round(i * cw, 2)))
    if erase_cps is not None and hold_until is not None:
        for i in range(n - 1, -1, -1):
            steps.append((hold_until + (n - i) / erase_cps, round(i * cw, 2)))
    return steps


def fmt_steps(steps: list[tuple[float, float]]) -> list[tuple[float, str]]:
    return [(t, f"{v:g}") for t, v in steps]


# --------------------------------------------------------------------------- #
# Banner
# --------------------------------------------------------------------------- #

def banner(theme: str) -> str:
    P = PALETTES[theme]
    rnd = random.Random(97)
    W, H = 1200, 380
    out: list[str] = []
    a = out.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
    a('<title id="t">Joel Stephen — Full-Stack &amp; AI Engineer</title>')
    a('<desc id="d">Animated banner: a terminal types whoami, the name Joel Stephen appears with rotating roles, and on the right a request travels from a UI card through an API card to a model card that streams tokens back.</desc>')
    a('<defs>')
    a(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{P["bg0"]}"/><stop offset=".55" stop-color="{P["bg1"]}"/><stop offset="1" stop-color="{P["bg2"]}"/></linearGradient>')
    a(f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P["blue"]}"/><stop offset="1" stop-color="{P["green"]}"/></linearGradient>')
    # shimmer gradient for the name (userSpaceOnUse so we can slide it)
    a(f'<linearGradient id="shimmer" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="320" y2="0">'
      f'<stop offset="0" stop-color="{P["blue"]}"/><stop offset=".45" stop-color="{P["text"]}"/><stop offset=".55" stop-color="{P["text"]}"/><stop offset="1" stop-color="{P["green"]}"/>'
      f'<animateTransform attributeName="gradientTransform" type="translate" from="-520 0" to="900 0" dur="{T}s" repeatCount="indefinite"/>'
      f'</linearGradient>')
    ga, gb = (".30", ".22") if theme == "dark" else (".16", ".08")
    a(f'<radialGradient id="glowA" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{P["blue"]}" stop-opacity="{ga}"/><stop offset="1" stop-color="{P["blue"]}" stop-opacity="0"/></radialGradient>')
    a(f'<radialGradient id="glowB" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{P["orange"]}" stop-opacity="{gb}"/><stop offset="1" stop-color="{P["orange"]}" stop-opacity="0"/></radialGradient>')
    a(f'<linearGradient id="fadeUp" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{P["bg0"]}" stop-opacity="0"/><stop offset="1" stop-color="{P["bg0"]}" stop-opacity="1"/></linearGradient>')
    a(f'<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    # typewriter clips
    a('<clipPath id="clipWho"><rect x="0" y="0" height="40" width="0">'
      + discrete("width", fmt_steps(typewriter_steps(0.3, 11, 14, 9.6, None, None)),
                 extra='fill="freeze"') + '</rect></clipPath>')
    roles = ["Full-Stack Engineer", "AI Engineer", "ships on-device ML in the browser", "React · Vue · FastAPI · LLM pipelines"]
    cw_role = 13.2  # ~0.6em at 22px mono
    slot = T / len(roles)  # 3.5 s each
    for i, r in enumerate(roles):
        start = i * slot
        n = len(r)
        type_cps = max(18.0, n / 1.3)
        hold_until = start + n / type_cps + 1.1
        steps = typewriter_steps(start, n, type_cps, cw_role, hold_until, erase_cps=max(30.0, n / 0.55))
        a(f'<clipPath id="clipRole{i}"><rect x="0" y="0" height="40" width="0">'
          + discrete("width", fmt_steps(steps)) + '</rect></clipPath>')
    # UI input typewriter (in card coords)
    a('<clipPath id="clipInput"><rect x="0" y="0" height="20" width="0">'
      + discrete("width", fmt_steps(typewriter_steps(0.2, 15, 11, 5.7, None, None) + [(12.9, 0.0)])) + '</rect></clipPath>')
    a('</defs>')

    a('<style>'
      f'.name{{font:700 60px {SANS};letter-spacing:-.5px}}'
      f'.role{{font:500 22px {MONO};fill:{P["sub"]}}}'
      f'.who{{font:500 16px {MONO};fill:{P["mono"]}}}'
      f'.pill{{font:500 13px {SANS};fill:{P["muted"]}}}'
      f'.tick{{font:500 13px {MONO};fill:{P["muted"]}}}'
      f'.ct{{font:600 12px {SANS};fill:{P["cardTitle"]}}}'
      f'.cs{{font:500 10px {MONO};fill:{P["cardText"]}}}'
      f'.log{{font:500 10px {MONO};fill:{P["cardText"]}}}'
      f'.input{{font:500 9.5px {MONO};fill:{P["cardTitle"]}}}'
      '.ticker{animation:tick 42s linear infinite}'
      '@keyframes tick{to{transform:translateX(-1100px)}}'
      '.cursor{animation:blink 1s steps(1) infinite}'
      '@keyframes blink{50%{opacity:0}}'
      '.shield{animation:shine 2.4s ease-in-out infinite}'
      '@keyframes shine{0%,100%{opacity:.55}50%{opacity:1}}'
      '.orbit{animation:spin 60s linear infinite;transform-origin:910px 188px}'
      '@keyframes spin{to{transform:rotate(360deg)}}'
      '@media (prefers-reduced-motion:reduce){.ticker,.cursor,.shield,.orbit{animation:none}}'
      '</style>')

    a('<g clip-path="url(#card)">')
    a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

    # stars (subtle in light theme)
    star_op = 0.9 if theme == "dark" else 0.35
    for _ in range(70):
        x = rnd.uniform(8, W - 8); y = rnd.uniform(8, H - 60)
        r = rnd.choice([0.7, 0.9, 1.1, 1.4])
        dur = rnd.uniform(2.2, 6.0); beg = -rnd.uniform(0, 6)
        lo = rnd.uniform(0.1, 0.35)
        a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{P["star"]}" opacity="{lo:.2f}">'
          f'<animate attributeName="opacity" values="{lo:.2f};{star_op:.2f};{lo:.2f}" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite"/></circle>')

    # perspective floor grid (bottom), faded
    a(f'<g stroke="{P["grid"]}" stroke-opacity="{0.13 if theme == "dark" else 0.10}" stroke-width="1">')
    for i in range(-6, 19):
        x0 = 600 + i * 140
        a(f'<line x1="{x0}" y1="{H}" x2="{600 + (x0 - 600) * 0.18:.0f}" y2="250"/>')
    for k, yy in enumerate([262, 276, 293, 313, 337, 365]):
        a(f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" stroke-opacity="{0.05 + k * 0.02:.2f}"/>')
    a('</g>')
    a(f'<rect x="0" y="230" width="{W}" height="90" fill="url(#fadeUp)" opacity=".9"/>')
    a(f'<circle cx="960" cy="40" r="300" fill="url(#glowA)"/>')
    a(f'<circle cx="110" cy="{H}" r="240" fill="url(#glowB)"/>')

    # ---------------- left: identity ----------------
    # whoami line
    a('<g transform="translate(64,78)">')
    a('<g clip-path="url(#clipWho)"><text class="who" x="0" y="18">~ $ whoami</text></g>')
    # cursor follows typing then parks
    a(f'<rect class="cursor" y="4" width="9" height="18" fill="{P["mono"]}" opacity=".9">'
      + discrete("x", fmt_steps(typewriter_steps(0.3, 11, 14, 9.6, None, None)), extra='fill="freeze"')
      + '</rect>')
    a('</g>')

    # name
    a('<g opacity="0" transform="translate(64,150)">'
      '<animate attributeName="opacity" from="0" to="1" dur=".7s" begin="1.2s" fill="freeze"/>'
      '<animateTransform attributeName="transform" type="translate" from="64 164" to="64 150" dur=".7s" begin="1.2s" fill="freeze"/>'
      f'<text class="name" x="0" y="0" fill="url(#shimmer)">Joel Stephen</text>'
      '</g>')

    # roles (typewriter rotation)
    a('<g transform="translate(66,176)">')
    for i, r in enumerate(roles):
        a(f'<g clip-path="url(#clipRole{i})"><text class="role" x="0" y="22">{r}</text></g>')
    # one shared cursor: x follows whichever role is active (sum of clip widths; only one non-zero at a time)
    cursor_steps: list[tuple[float, float]] = [(0.0, 0.0)]
    for i, r in enumerate(roles):
        start = i * slot; n = len(r)
        type_cps = max(18.0, n / 1.3)
        hold_until = start + n / type_cps + 1.1
        cursor_steps += typewriter_steps(start, n, type_cps, cw_role, hold_until, erase_cps=max(30.0, n / 0.55))[1:]
    a(f'<rect class="cursor" y="6" width="11" height="22" fill="{P["sub"]}" opacity=".9">'
      + discrete("x", fmt_steps(cursor_steps)) + '</rect>')
    a('</g>')

    # location pill + small facts
    a('<g transform="translate(66,222)">')
    a(f'<rect x="0" y="0" width="128" height="26" rx="13" fill="{P["pill"]}" stroke="{P["pillStroke"]}"/>')
    a(f'<path transform="translate(11,5)" d="M7 0a5.2 5.2 0 0 0-5.2 5.2C1.8 9 7 16 7 16s5.2-7 5.2-10.8A5.2 5.2 0 0 0 7 0zm0 7.4a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4z" fill="{P["orange"]}"/>')
    a('<text class="pill" x="30" y="17">Abu Dhabi, UAE</text>')
    a(f'<rect x="138" y="0" width="150" height="26" rx="13" fill="{P["pill"]}" stroke="{P["pillStroke"]}"/>')
    a(f'<circle cx="153" cy="13" r="4" fill="{P["green"]}"><animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>')
    a('<text class="pill" x="164" y="17">5+ yrs shipping</text>')
    a(f'<rect x="296" y="0" width="196" height="26" rx="13" fill="{P["pill"]}" stroke="{P["pillStroke"]}"/>')
    a(f'<path transform="translate(307,6)" d="M7 0 13 2.4v4.1c0 3.6-2.6 6.2-6 7.5-3.4-1.3-6-3.9-6-7.5V2.4L7 0z" fill="{P["green"]}" class="shield"/>')
    a('<text class="pill" x="326" y="17">on-device ML, by default</text>')
    a('</g>')

    # ticker (bottom-left). Two copies, each forced to 640px with textLength so the loop is seamless.
    ticker = "react  ·  vue  ·  typescript  ·  python  ·  fastapi  ·  django  ·  postgres  ·  llm pipelines  ·  yjs / crdt  ·  mv3 extensions  ·  on-device ml  ·  "
    a('<g transform="translate(64,300)">')
    a(f'<rect x="-10" y="-14" width="520" height="26" fill="none"/>')
    a('<clipPath id="tclip"><rect x="-2" y="-16" width="508" height="30"/></clipPath>')
    a('<g clip-path="url(#tclip)"><g class="ticker">')
    a(f'<text class="tick" x="0" y="4" textLength="1100" lengthAdjust="spacing">{ticker}</text>')
    a(f'<text class="tick" x="1100" y="4" textLength="1100" lengthAdjust="spacing">{ticker}</text>')
    a('</g></g>')
    a('</g>')

    # ---------------- right: request lifecycle ----------------
    # faint orbit ring behind the cards
    a(f'<circle class="orbit" cx="910" cy="188" r="150" fill="none" stroke="{P["blue"]}" stroke-opacity=".12" stroke-dasharray="3 9"/>')

    cards = {  # x, y, w, h
        "ui": (612, 96, 176, 184),
        "api": (826, 118, 160, 140),
        "model": (1024, 96, 156, 184),
    }

    def card(name: str, title: str, subtitle: str) -> None:
        x, y, w, h = cards[name]
        a(f'<g transform="translate({x},{y})">')
        a(f'<rect width="{w}" height="{h}" rx="12" fill="{P["card"]}" stroke="{P["cardStroke"]}"/>')
        a(f'<rect x="0" y="0" width="{w}" height="26" rx="12" fill="{P["cardStroke"]}" opacity=".35"/>')
        a(f'<circle cx="14" cy="13" r="3.2" fill="{P["orange"]}"/><circle cx="24" cy="13" r="3.2" fill="{P["yellow"]}"/><circle cx="34" cy="13" r="3.2" fill="{P["green"]}"/>')
        a(f'<text class="ct" x="48" y="17">{title}</text>')
        a(f'<text class="cs" x="{w - 8}" y="17" text-anchor="end">{subtitle}</text>')
        a('</g>')

    # timing (seconds within loop)
    t_send = 2.2
    t_api = 3.0
    t_model = 5.2
    t_tokens = 6.0
    t_resp = 9.0
    t_ui_resp = 10.6
    t_reset = 12.9

    # ---- UI card
    card("ui", "UI", "react · vue")
    x, y, w, h = cards["ui"]
    a(f'<g transform="translate({x},{y})">')
    # wireframe rows
    a(f'<rect x="12" y="38" width="96" height="8" rx="4" fill="{P["cardStroke"]}"/>')
    a(f'<rect x="12" y="52" width="140" height="6" rx="3" fill="{P["cardStroke"]}" opacity=".7"/>')
    a(f'<rect x="12" y="63" width="118" height="6" rx="3" fill="{P["cardStroke"]}" opacity=".5"/>')
    # shield chip
    a(f'<g transform="translate({w - 30},36)" class="shield"><path d="M9 0 17 3v5c0 4.6-3.4 8-8 9.6C4.4 16 1 12.6 1 8V3L9 0z" fill="{P["green"]}" opacity=".9"/><path d="M5.5 8.2 8 10.6l4.5-5" stroke="{P["card"]}" stroke-width="1.6" fill="none" stroke-linecap="round"/></g>')
    # input box
    a(f'<rect x="12" y="84" width="{w - 58}" height="24" rx="7" fill="{P["bg0"] if theme == "dark" else "#f6f8fa"}" stroke="{P["cardStroke"]}"/>')
    a(f'<g transform="translate(19,88)"><g clip-path="url(#clipInput)"><text class="input" x="0" y="12">summarise this…</text></g></g>')
    # send button pulses at t_send
    a(f'<g transform="translate({w - 40},89)"><rect width="26" height="14" rx="4" fill="{P["blue"]}">'
      + discrete("opacity", [(0, ".55"), (t_send, "1"), (t_send + .5, ".55")]) + '</rect>'
      f'<path d="M8 7h10M14 4l3 3-3 3" stroke="{P["card"]}" stroke-width="1.4" fill="none" stroke-linecap="round"/></g>')
    # reply bubble lines after t_ui_resp
    a(f'<rect x="12" y="118" width="{w - 24}" height="54" rx="8" fill="{P["green"]}" opacity="0">'
      + discrete("opacity", [(0, "0"), (t_ui_resp, ".10"), (t_reset, "0")]) + '</rect>')
    for i, lw in enumerate([118, 132, 92]):
        a(f'<rect x="20" y="{126 + i * 14}" width="{lw}" height="6" rx="3" fill="{P["green"]}" opacity="0">'
          + discrete("opacity", [(0, "0"), (t_ui_resp + .3 + i * .45, ".85"), (t_reset, "0")]) + '</rect>')
    a('</g>')

    # ---- API card
    card("api", "API", "fastapi")
    x, y, w, h = cards["api"]
    a(f'<g transform="translate({x},{y})">')
    logs = ["POST /workflows", "→ anthropic.messages", "200 · 41 ms"]
    for i, line in enumerate(logs):
        col = P["green"] if i == 2 else P["cardText"]
        a(f'<text class="log" x="12" y="{46 + i * 16}" fill="{col}" opacity="0">'
          + discrete("opacity", [(0, "0"), (t_api + i * .45, "1"), (t_reset, "0")]) + f'{line}</text>')
    # progress bar
    a(f'<rect x="12" y="100" width="{w - 24}" height="6" rx="3" fill="{P["cardStroke"]}"/>')
    a(f'<rect x="12" y="100" width="0" height="6" rx="3" fill="url(#accent)">'
      f'<animate attributeName="width" values="0;0;{w - 24};{w - 24};0;0" keyTimes="0;{kt(t_api)};{kt(t_model)};{kt(t_reset)};{kt(t_reset + .01)};1" dur="{T}s" repeatCount="indefinite"/></rect>')
    a(f'<text class="cs" x="12" y="124">pydantic · sse stream</text>')
    a('</g>')

    # ---- Model card
    card("model", "Model", "llm")
    x, y, w, h = cards["model"]
    a(f'<g transform="translate({x},{y})">')
    # thinking dots between t_model and t_tokens
    for i in range(3):
        a(f'<circle cx="{22 + i * 12}" cy="46" r="3.5" fill="{P["blue"]}" opacity="0">'
          f'<animate attributeName="opacity" values="0;0;.3;1;.3;.3;1;.3;0;0" keyTimes="0;{kt(t_model)};{kt(t_model + .05 + i * .1)};{kt(t_model + .25 + i * .1)};{kt(t_model + .45 + i * .1)};{kt(t_model + .5 + i * .1)};{kt(t_model + .65 + i * .1)};{kt(t_tokens - .05)};{kt(t_tokens)};1" dur="{T}s" repeatCount="indefinite"/></circle>')
    a(f'<text class="cs" x="12" y="36">thinking</text>')
    # token stream: rows of rounded rects
    tok_colors = [P["tokenA"], P["tokenB"], P["tokenC"]]
    ti = 0
    for row in range(5):
        xx = 12
        while xx < w - 24:
            tw = rnd.choice([10, 14, 18, 22, 26])
            if xx + tw > w - 12:
                break
            col = tok_colors[ti % 3] if rnd.random() < .35 else P["cardStroke"]
            t_on = t_tokens + ti * 0.085
            a(f'<rect x="{xx}" y="{62 + row * 16}" width="{tw}" height="8" rx="3" fill="{col}" opacity="0">'
              + discrete("opacity", [(0, "0"), (t_on, ".95"), (t_reset, "0")]) + '</rect>')
            xx += tw + 5
            ti += 1
    a(f'<text class="cs" x="12" y="{h - 14}">tokens streaming</text>')
    a('</g>')

    # ---- edges + pulses
    ux, uy, uw, uh = cards["ui"]; ax, ay, aw, ah = cards["api"]; mx, my, mw, mh = cards["model"]
    y_mid = 188
    p1 = f"M{ux + uw} {y_mid} L{ax} {y_mid}"
    p2 = f"M{ax + aw} {y_mid} L{mx} {y_mid}"
    a(f'<g stroke="{P["edge"]}" stroke-width="2" fill="none"><path d="{p1}"/><path d="{p2}"/></g>')
    a(f'<g fill="{P["edge"]}"><path d="M{ax - 7} {y_mid - 4} l7 4 -7 4z"/><path d="M{mx - 7} {y_mid - 4} l7 4 -7 4z"/></g>')

    def pulse(path: str, t0: float, t1: float, color: str, reverse: bool = False) -> None:
        kp = "1;1;0;0" if reverse else "0;0;1;1"
        a(f'<circle r="5" fill="{color}" opacity="0">'
          f'<animateMotion path="{path}" keyPoints="{kp}" keyTimes="0;{kt(t0)};{kt(t1)};1" calcMode="linear" dur="{T}s" repeatCount="indefinite"/>'
          + discrete("opacity", [(0, "0"), (t0, "1"), (t1, "0")]) + '</circle>')
        a(f'<circle r="10" fill="{color}" opacity="0">'
          f'<animateMotion path="{path}" keyPoints="{kp}" keyTimes="0;{kt(t0)};{kt(t1)};1" calcMode="linear" dur="{T}s" repeatCount="indefinite"/>'
          + discrete("opacity", [(0, "0"), (t0, ".25"), (t1, "0")]) + '</circle>')

    pulse(p1, t_send, t_api, P["blue"])
    pulse(p2, t_model - .8, t_model, P["blue"])
    pulse(p2, t_resp, t_resp + .8, P["green"], reverse=True)
    pulse(p1, t_resp + .8, t_ui_resp, P["green"], reverse=True)

    # labels under the edges
    a(f'<text class="cs" x="{(ux + uw + ax) / 2}" y="{y_mid + 18}" text-anchor="middle">request</text>')
    a(f'<text class="cs" x="{(ax + aw + mx) / 2}" y="{y_mid + 18}" text-anchor="middle">tool calls</text>')

    # bottom hairline
    a(f'<rect x="0" y="{H - 4}" width="{W}" height="4" fill="url(#accent)" opacity=".9"/>')
    a('</g>')
    a('</svg>')
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# ScamShield demo
# --------------------------------------------------------------------------- #

def scamshield_demo() -> str:
    W, H = 640, 400
    D = 11.0  # loop seconds
    url = "https://paypa1-secure-verify.com/login"
    red = "#d1242f"; green = "#1a7f37"; blue = "#0969da"
    out: list[str] = []
    a = out.append

    def k(t: float) -> str:
        return f"{max(0.0, min(1.0, t / D)):.4f}"

    def disc(attr: str, steps: list[tuple[float, str]], extra: str = "") -> str:
        steps = sorted(steps, key=lambda s: s[0])
        if steps[0][0] > 0:
            steps = [(0.0, steps[0][1])] + steps
        vals = [v for _, v in steps] + [steps[-1][1]]
        times = [k(t) for t, _ in steps] + ["1"]
        return (f'<animate attributeName="{attr}" values="{";".join(vals)}" keyTimes="{";".join(times)}" '
                f'calcMode="discrete" dur="{D}s" repeatCount="indefinite" {extra}/>')

    def lin(attr: str, values: str, times: list[float], extra: str = "") -> str:
        return (f'<animate attributeName="{attr}" values="{values}" keyTimes="{";".join(k(t) for t in times)}" '
                f'dur="{D}s" repeatCount="indefinite" {extra}/>')

    t_type0, t_type1 = 0.4, 2.6        # url typing
    t_page = 3.0                        # page paints
    t_verdict = 4.6                     # banner slides in
    t_out = 10.2                        # fade everything

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
    a('<title id="t">ScamShield catching a phishing page</title>')
    a('<desc id="d">A browser window loads a fake PayPal login on a look-alike domain; ScamShield flags it as a dangerous page and offers a one-click link to the real site.</desc>')
    a('<defs>')
    a(f'<clipPath id="win"><rect width="{W}" height="{H}" rx="14"/></clipPath>')
    a(f'<clipPath id="page"><rect x="0" y="76" width="{W}" height="{H - 76}"/></clipPath>')
    # url typewriter clip
    n = len(url); cw = 7.2
    steps = [(0.0, "0")] + [(t_type0 + i * (t_type1 - t_type0) / n, f"{i * cw:.1f}") for i in range(1, n + 1)] + [(t_out + .4, "0")]
    a('<clipPath id="urlclip"><rect x="0" y="0" width="0" height="20">' + disc("width", steps) + '</rect></clipPath>')
    a(f'<linearGradient id="red" x1="0" x2="1"><stop offset="0" stop-color="#cf222e"/><stop offset="1" stop-color="#a40e26"/></linearGradient>')
    a('</defs>')
    a('<style>'
      f'.t{{font:500 12px {MONO};fill:#24292f}}'
      f'.h{{font:700 15px {SANS};fill:#ffffff}}'
      f'.b{{font:500 12px {SANS};fill:#ffffff}}'
      f'.lbl{{font:500 11px {SANS};fill:#57606a}}'
      f'.btn{{font:600 12px {SANS};fill:#ffffff}}'
      f'.logo{{font:800 18px {SANS};fill:#ffffff;letter-spacing:-.3px}}'
      f'.small{{font:500 10px {SANS};fill:#57606a}}'
      '.cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}'
      '.pulse{animation:pp 1.6s ease-in-out infinite}@keyframes pp{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}'
      '@media (prefers-reduced-motion:reduce){.cur,.pulse{animation:none}}'
      '</style>')

    a('<g clip-path="url(#win)">')
    a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    # browser chrome
    a(f'<rect width="{W}" height="76" fill="#eef1f4"/>')
    a('<circle cx="18" cy="18" r="5" fill="#ff5f57"/><circle cx="36" cy="18" r="5" fill="#febc2e"/><circle cx="54" cy="18" r="5" fill="#28c840"/>')
    # tab
    a('<rect x="78" y="6" width="190" height="28" rx="8" fill="#ffffff"/>')
    a('<text class="small" x="92" y="24">Log in to your account</text>')
    # url bar
    a(f'<rect x="16" y="42" width="{W - 90}" height="26" rx="13" fill="#ffffff" stroke="#d0d7de"/>')
    a('<g transform="translate(30,45)"><g clip-path="url(#urlclip)"><text class="t" x="0" y="15">' + url + '</text></g>')
    a('<rect class="cur" y="3" width="7" height="15" fill="#24292f">' + disc("x", steps) + '</rect></g>')
    # toolbar extension icon with badge
    a(f'<g transform="translate({W - 60},43)">')
    a(f'<path d="M12 2 21 5.5v6c0 5.4-3.8 9.7-9 11.5-5.2-1.8-9-6.1-9-11.5v-6L12 2z" fill="{green}">' + disc("fill", [(0, green), (t_verdict, red), (t_out + .4, green)]) + '</path>')
    a(f'<circle cx="21" cy="5" r="6" fill="{red}" opacity="0">' + disc("opacity", [(0, "0"), (t_verdict, "1"), (t_out + .4, "0")]) + '</circle>')
    a('<text x="21" y="8.5" text-anchor="middle" font-family="Arial" font-weight="700" font-size="9" fill="#fff" opacity="0">!' + disc("opacity", [(0, "0"), (t_verdict, "1"), (t_out + .4, "0")]) + '</text>')
    a('</g>')

    # ---- page content (fake PayPal-ish login) appears at t_page
    a('<g opacity="0">' + disc("opacity", [(0, "0"), (t_page, "1"), (t_out, "0")]))
    a(f'<rect x="0" y="76" width="{W}" height="56" fill="#003087"/>')
    a('<text class="logo" x="24" y="112">PayPaI</text>')
    a(f'<rect x="{W/2 - 150}" y="160" width="300" height="200" rx="10" fill="#ffffff" stroke="#d0d7de"/>')
    a(f'<text class="lbl" x="{W/2 - 130}" y="192">Email or mobile number</text>')
    a(f'<rect x="{W/2 - 130}" y="200" width="260" height="30" rx="6" fill="#f6f8fa" stroke="#d0d7de"/>')
    a(f'<text class="lbl" x="{W/2 - 130}" y="254">Password</text>')
    a(f'<rect x="{W/2 - 130}" y="262" width="260" height="30" rx="6" fill="#f6f8fa" stroke="#d0d7de"/>')
    a(f'<rect x="{W/2 - 130}" y="308" width="260" height="32" rx="16" fill="#0070ba"/>')
    a(f'<text class="btn" x="{W/2}" y="329" text-anchor="middle">Log In</text>')
    a('</g>')

    # greyed overlay once flagged
    a(f'<rect x="0" y="76" width="{W}" height="{H - 76}" fill="#0b1220" opacity="0">' + disc("opacity", [(0, "0"), (t_verdict, ".45"), (t_out, "0")]) + '</rect>')

    # ---- ScamShield banner slides down from under the chrome
    a('<g clip-path="url(#page)">')
    a(f'<g transform="translate(0,-90)">'
      f'<animateTransform attributeName="transform" type="translate" values="0 -90;0 -90;0 76;0 76;0 -90;0 -90" keyTimes="0;{k(t_verdict)};{k(t_verdict + .45)};{k(t_out)};{k(t_out + .3)};1" calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1;0 0 1 1;.4 0 1 1;0 0 1 1" dur="{D}s" repeatCount="indefinite"/>')
    a(f'<rect x="0" y="0" width="{W}" height="84" fill="url(#red)"/>')
    # shield icon
    a('<g transform="translate(20,22)"><path d="M20 2 36 8v10c0 9-6.4 16.3-16 19.6C10.4 34.3 4 27 4 18V8l16-6z" fill="#fff" opacity=".95"/><path d="M20 12v9M20 26.5v1" stroke="#cf222e" stroke-width="3.2" stroke-linecap="round"/></g>')
    a('<text class="h" x="70" y="32">Dangerous page</text>')
    a('<text class="b" x="70" y="52">Looks like PayPal, but this is not paypal.com.</text>')
    # rescue button
    a(f'<g transform="translate({W - 196},22)"><g class="pulse" style="transform-box:fill-box;transform-origin:center">'
      '<rect width="176" height="34" rx="17" fill="#ffffff"/>'
      f'<text class="btn" x="88" y="22" text-anchor="middle" style="fill:#cf222e">Take me to the real site →</text></g></g>')
    a('</g></g>')

    # footer caption
    a(f'<text class="small" x="{W/2}" y="{H - 10}" text-anchor="middle" opacity="0">on-device verdict · nothing sent anywhere' + disc("opacity", [(0, "0"), (t_verdict + .6, "1"), (t_out, "0")]) + '</text>')
    a('</g>')
    a(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="#30363d" stroke-opacity=".35"/>')
    a('</svg>')
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Career timeline
# --------------------------------------------------------------------------- #

def timeline(theme: str) -> str:
    P = PALETTES[theme]
    W, H = 1200, 170
    out: list[str] = []
    a = out.append
    x0, x1 = 70, 1130
    y = 96
    years = list(range(2015, 2027))

    def X(year: float) -> float:
        return x0 + (year - 2015) / (2026.6 - 2015) * (x1 - x0)

    nodes = [
        (2015.6, 2019.6, "BITS Pilani Dubai", "B.E. Computer Science (Hons)", P["muted"], "above"),
        (2019.0, 2019.5, "Alucor", "SDE intern · Django", P["blue"], "below"),
        (2019.7, 2023.1, "RIOT", "Junior SWE · payments, migrations, Python automation", P["blue"], "above"),
        (2023.7, 2025.1, "Otani Trading", "SWE → Senior SWE · Vue, FastAPI, GraphQL, YOLOv5", P["blue"], "below"),
        (2025.45, 2026.6, "AppliedAI", "SWE on Opus · React, Yjs, LLM pipelines", P["green"], "above"),
    ]
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">')
    a('<title id="t">Career timeline 2015 to 2026: BITS Pilani Dubai, Alucor, RIOT, Otani Trading, AppliedAI</title>')
    a('<defs>'
      f'<linearGradient id="accent" x1="0" x2="1"><stop offset="0" stop-color="{P["blue"]}"/><stop offset="1" stop-color="{P["green"]}"/></linearGradient>'
      '</defs>')
    a('<style>'
      f'.yr{{font:500 11px {MONO};fill:{P["muted"]}}}'
      f'.nm{{font:700 13px {SANS};fill:{P["text"]}}}'
      f'.ds{{font:400 11px {SANS};fill:{P["muted"]}}}'
      '.draw{stroke-dasharray:1100;stroke-dashoffset:1100;animation:draw 2.2s ease-out forwards}'
      '@keyframes draw{to{stroke-dashoffset:0}}'
      '.fade{opacity:0;animation:fade .6s ease-out forwards}'
      '@keyframes fade{to{opacity:1}}'
      '.now{animation:now 2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}'
      '@keyframes now{0%,100%{transform:scale(1);opacity:.35}50%{transform:scale(1.9);opacity:0}}'
      '@media (prefers-reduced-motion:reduce){.draw{animation:none;stroke-dashoffset:0}.fade{animation:none;opacity:1}.now{animation:none}}'
      '</style>')
    a(f'<rect width="{W}" height="{H}" fill="none"/>')
    # base track
    a(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{P["cardStroke"]}" stroke-width="2"/>')
    a(f'<line class="draw" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#accent)" stroke-width="2"/>')
    # year ticks
    for yr in years:
        xx = X(yr)
        a(f'<line x1="{xx:.1f}" y1="{y - 4}" x2="{xx:.1f}" y2="{y + 4}" stroke="{P["cardStroke"]}"/>')
        a(f'<text class="yr" x="{xx:.1f}" y="{y + 22}" text-anchor="middle">{yr}</text>')
    # spans + nodes
    for i, (s, e, name, desc, col, side) in enumerate(nodes):
        xs, xe = X(s), X(e)
        delay = 0.3 + i * 0.35
        a(f'<g class="fade" style="animation-delay:{delay:.2f}s">')
        a(f'<rect x="{xs:.1f}" y="{y - 5}" width="{max(6, xe - xs):.1f}" height="10" rx="5" fill="{col}" opacity=".28"/>')
        a(f'<circle cx="{xs:.1f}" cy="{y}" r="6" fill="{P["bg0"]}" stroke="{col}" stroke-width="2.5"/>')
        ly = y - 30 if side == "above" else y + 50
        ty = y - 16 if side == "above" else y + 36
        a(f'<line x1="{xs:.1f}" y1="{y - 6 if side == "above" else y + 6}" x2="{xs:.1f}" y2="{ty:.1f}" stroke="{col}" stroke-opacity=".5"/>')
        anchor = "end" if name == "AppliedAI" else "start"
        tx = xe + 4 if anchor == "end" else xs - 4
        a(f'<text class="nm" x="{tx:.1f}" y="{ly - 4:.1f}" text-anchor="{anchor}">{name}</text>')
        a(f'<text class="ds" x="{tx:.1f}" y="{ly + 12:.1f}" text-anchor="{anchor}">{desc}</text>')
        if name == "AppliedAI":
            a(f'<circle class="now" cx="{xe:.1f}" cy="{y}" r="7" fill="{P["green"]}"/>')
            a(f'<circle cx="{xe:.1f}" cy="{y}" r="5" fill="{P["green"]}"/>')
            a(f'<text class="yr" x="{xe + 13:.1f}" y="{y + 4}" text-anchor="start" fill="{P["green"]}">now</text>')
        a('</g>')
    a('</svg>')
    return "\n".join(out)


def write(name: str, svg: str) -> None:
    p = ASSETS / name
    p.write_text(svg, encoding="utf-8", newline="\n")
    import xml.dom.minidom as m
    m.parseString(svg.encode("utf-8"))  # validates XML
    print(f"{name:28s} {p.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    write("header-dark.svg", banner("dark"))
    write("header-light.svg", banner("light"))
    write("scamshield-demo.svg", scamshield_demo())
    write("timeline-dark.svg", timeline("dark"))
    write("timeline-light.svg", timeline("light"))

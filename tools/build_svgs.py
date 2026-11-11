# สร้างภาพ SVG ขยับได้ สำหรับหน้าโปรไฟล์ GitHub (ธีม terminal + pixel game)
import pathlib, sys

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BG, PANEL, LINE = "#0D1117", "#161B22", "#30363D"
TXT, MUTED = "#C9D1D9", "#8B949E"
GREEN, BLUE, AMBER, PINK, RED = "#3FB950", "#58A6FF", "#F2CC60", "#F778BA", "#F85149"
MONO = "Consolas, 'DejaVu Sans Mono', 'Courier New', monospace"
CW = 0.55  # ความกว้างตัวอักษร monospace ต่อ font-size โดยประมาณ


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sprite(x, y, px=6, cls=""):
    # ตัวละครพิกเซล 8x8 (หุ่นยนต์ตัวเล็ก ออกแบบเอง)
    grid = ["..AAAA..",
            ".A....A.",
            ".A.G.GA.",
            ".A....A.",
            "..AAAA..",
            ".BBBBBB.",
            ".B.BB.B.",
            "..B..B.."]
    col = {"A": AMBER, "G": GREEN, "B": BLUE}
    r = [f'<rect x="{x+i*px}" y="{y+j*px}" width="{px}" height="{px}" fill="{col[c]}"/>'
         for j, row in enumerate(grid) for i, c in enumerate(row) if c != "."]
    return f'<g class="{cls}">' + "".join(r) + "</g>"


def typed_line(x, y, text, color, size, start, dur, prompt=False):
    """บรรทัดที่พิมพ์ทีละตัว: ใช้แผ่นปิดที่หดแบบ steps"""
    n = max(len(text), 1)
    w = n * size * CW + 4
    pre = ""
    if prompt:
        pre = f'<text x="{x}" y="{y}" fill="{GREEN}" font-size="{size}">$</text>'
        x += size * CW * 2
    # แผ่นสีพื้นหลังปิดข้อความ แล้วหดจากซ้ายไปขวาทีละตัวอักษร = เหมือนพิมพ์
    return (f'{pre}<text x="{x}" y="{y}" fill="{color}" font-size="{size}">{esc(text)}</text>'
            f'<rect x="{x-1}" y="{y-size}" height="{size*1.4}" width="{w+2}" fill="{BG}" '
            f'style="transform-box:fill-box;transform-origin:right;'
            f'animation:wipe {dur}s steps({n}) {start}s forwards"/>')


STYLE = f"""<style>
@keyframes wipe {{ to {{ transform: scaleX(0); }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
@keyframes fadein {{ to {{ opacity: 1; }} }}
@keyframes bob {{ 50% {{ transform: translateY(-6px); }} }}
@keyframes fill {{ to {{ transform: scaleX(1); }} }}
@keyframes dash {{ to {{ stroke-dashoffset: -40; }} }}
@keyframes pulse {{ 50% {{ opacity: .35; }} }}
.cur {{ animation: blink 1s steps(1) infinite; }}
.bob {{ animation: bob 1.2s ease-in-out infinite; }}
.late {{ opacity: 0; }}
.pulse {{ animation: pulse 1.4s ease-in-out infinite; }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; opacity: 1 !important; transform: none !important; }} }}
</style>"""


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{MONO}" role="img"><title>{esc(title)}</title>{STYLE}{body}</svg>')


# ---------- 1. Hero: หน้าต่าง terminal ----------
def hero():
    W, H = 1200, 430
    b = [f'<rect width="{W}" height="{H}" rx="14" fill="{BG}" stroke="{LINE}"/>',
         f'<path d="M0 14 a14 14 0 0 1 14 -14 h{W-28} a14 14 0 0 1 14 14 v30 h-{W} z" fill="{PANEL}"/>',
         f'<circle cx="28" cy="22" r="7" fill="{RED}"/><circle cx="52" cy="22" r="7" fill="{AMBER}"/>'
         f'<circle cx="76" cy="22" r="7" fill="{GREEN}"/>',
         f'<text x="{W/2}" y="27" fill="{MUTED}" font-size="15" text-anchor="middle">thinnaphat@ict-mahidol: ~</text>']
    lines = [
        ("whoami", None),
        ("Thinnaphat  ·  Digital Science & Technology, ICT Mahidol  ·  Year 2", TXT),
        ("cat interests.txt", None),
        ("AI apps  ·  networking  ·  software that helps real people", BLUE),
        ("ls ~/projects", None),
        ("laan-chuay-aan/   trading-cooldown/   study-sites/", AMBER),
        ("./start_adventure.sh", None),
    ]
    t, y = 0.4, 80
    for text, color in lines:
        size = 22
        d = max(0.8, len(text) * 0.06)
        if color is None:
            b.append(typed_line(40, y, text, TXT, size, t, d, prompt=True))
        else:
            b.append(f'<g class="late" style="animation:fadein .01s {t}s forwards">'
                     f'<text x="40" y="{y}" fill="{color}" font-size="{size}">{esc(text)}</text></g>')
            d = 0.2
        t += d + 0.25
        y += 40
    # แถบโหลดแบบพิกเซล
    b.append(f'<g class="late" style="animation:fadein .01s {t}s forwards">'
             f'<text x="40" y="{y}" fill="{GREEN}" font-size="20">LOADING ROADMAP</text>'
             f'<rect x="270" y="{y-18}" width="300" height="22" fill="none" stroke="{GREEN}" stroke-width="2"/>'
             f'<rect x="274" y="{y-14}" width="292" height="14" fill="{GREEN}" '
             f'style="transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:fill 1.6s steps(10) {t}s forwards"/>'
             f'<rect x="590" y="{y-18}" width="12" height="22" fill="{TXT}" class="cur"/></g>')
    # ตัวละครพิกเซลด้านขวา
    b.append(f'<g transform="translate(985 150)">{sprite(0, 0, 18, "bob")}</g>')
    b.append(f'<text x="1057" y="350" fill="{MUTED}" font-size="15" text-anchor="middle">PLAYER 1</text>')
    b.append(f'<text x="1057" y="374" fill="{AMBER}" font-size="15" text-anchor="middle">LV.2</text>')
    return svg(W, H, "".join(b), "Terminal: Thinnaphat, Digital Science & Technology, ICT Mahidol")


# ---------- 2. หัวข้อแต่ละส่วน ----------
def section(cmd, comment):
    W, H = 1200, 64
    b = [f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{LINE}"/>',
         typed_line(24, 41, cmd, TXT, 24, 0.2, max(0.4, len(cmd) * 0.04), prompt=True)]
    x = 24 + (len(cmd) + 3) * 24 * CW
    b.append(f'<g class="late" style="animation:fadein .01s {0.3+len(cmd)*0.04}s forwards">'
             f'<text x="{x}" y="41" fill="{MUTED}" font-size="18"># {esc(comment)}</text></g>')
    b.append(f'<rect x="{W-40}" y="20" width="14" height="26" fill="{GREEN}" class="cur"/>')
    return svg(W, H, "".join(b), f"{cmd} — {comment}")


# ---------- 3. Roadmap แบบด่านเกม ----------
def roadmap():
    W, H = 1200, 720
    b = [f'<rect width="{W}" height="{H}" rx="14" fill="{BG}" stroke="{LINE}"/>']
    for gx in range(30, W, 30):  # จุดกริดพื้นหลัง
        for gy in range(30, H, 30):
            b.append(f'<rect x="{gx}" y="{gy}" width="2" height="2" fill="{LINE}"/>')
    b.append(f'<text x="40" y="58" fill="{AMBER}" font-size="26">▶ WORLD 1 — CAREER ROADMAP</text>')
    b.append(f'<text x="{W-40}" y="58" fill="{MUTED}" font-size="18" text-anchor="end">MAIN QUEST: AI / BACKEND</text>')
    # สถานะ: clear = ผ่านแล้ว, next = ด่านถัดไป, locked = ยังไม่ถึง, goal = เป้าหมาย, side = ทางแยกที่ยังไม่ตัดสินใจ
    stages = [  # (x, y, ชื่อ, รายละเอียด, สี, สถานะ)
        (130, 190, "START", "Joined ICT Mahidol · 2025", GREEN, "clear"),
        (410, 190, "STUDY SITES ×7", "Exam guides for classmates", BLUE, "clear"),
        (690, 190, "TRADING COOLDOWN", "Minecraft data pack", BLUE, "clear"),
        (970, 190, "LAAN CHUAY AAN", "AI LINE bot (Gemini)", PINK, "clear"),
        (970, 420, "INTERNSHIP", "Backend / AI · Year 2", AMBER, "next"),
        (690, 420, "LEVEL UP", "SQL · Java · Python APIs", MUTED, "locked"),
        (410, 420, "CO-OP", "4 months · Year 4", MUTED, "locked"),
        (130, 420, "JUNIOR ENGINEER", "AI / Backend", AMBER, "goal"),
        (970, 610, "SIDE QUEST: ???", "Cybersecurity · try CTFs", PINK, "side"),
    ]
    tags = {"clear": ("CLEAR", GREEN), "next": ("NEXT ▶", AMBER), "locked": ("LOCKED", MUTED),
            "goal": ("GOAL ★", AMBER), "side": ("???", PINK)}
    done = "M130 190 H1080 V420 H970"
    for d, col in (("M970 420 H130", MUTED), ("M1080 420 V610 H970", PINK)):
        b.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="10"/>'
                 f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="6 10"/>')
    b.append(f'<path d="{done}" fill="none" stroke="{LINE}" stroke-width="10"/>'
             f'<path d="{done}" fill="none" stroke="{GREEN}" stroke-width="4" stroke-dasharray="14 6" '
             f'style="animation:dash 1s linear infinite"/>')
    for x, y, name, sub, col, state in stages:
        cls = ' class="pulse"' if state in ("next", "side") else ""
        inner = "" if state == "locked" else f'<rect x="{x-14}" y="{y-14}" width="28" height="28" fill="{col}"/>'
        b.append(f'<g{cls}><rect x="{x-26}" y="{y-26}" width="52" height="52" fill="{PANEL}" stroke="{col}" stroke-width="4"/>{inner}</g>')
        b.append(f'<text x="{x}" y="{y+58}" fill="{col if state != "locked" else TXT}" font-size="19" text-anchor="middle">{esc(name)}</text>')
        b.append(f'<text x="{x}" y="{y+82}" fill="{MUTED}" font-size="15" text-anchor="middle">{esc(sub)}</text>')
        tag, tcol = tags[state]
        b.append(f'<rect x="{x-34}" y="{y-52}" width="68" height="18" fill="{BG}"/>'
                 f'<text x="{x}" y="{y-38}" fill="{tcol}" font-size="13" text-anchor="middle">{tag}</text>')
    # ตัวละครเดินจาก START มาหยุดที่ด่านถัดไป (ฝึกงาน) แล้ววนใหม่
    b.append(f'<g>{sprite(-24, -112, 6)}<animateMotion dur="8s" repeatCount="indefinite" path="{done}" '
             f'keyPoints="0;0;1;1" keyTimes="0;0.08;0.85;1" calcMode="linear"/></g>')
    return svg(W, H, "".join(b), "Career roadmap: cleared Start 2025, study sites, Trading Cooldown, Laan Chuay Aan; "
                                 "next internship (Backend/AI), then level up, co-op, goal Junior AI/Backend Engineer; side quest cybersecurity")


# ---------- 4. การ์ดผลงานแบบไอเทมเกม ----------
def card(name, rarity, rcol, lines, tags):
    W, H = 580, 300
    b = [f'<rect x="6" y="6" width="{W-12}" height="{H-12}" fill="{BG}" stroke="{rcol}" stroke-width="4" '
         f'stroke-dasharray="20 8" style="animation:dash 1.5s linear infinite"/>',
         f'<rect x="20" y="20" width="{W-40}" height="44" fill="{PANEL}"/>',
         f'<text x="36" y="50" fill="{TXT}" font-size="22">{esc(name)}</text>',
         f'<text x="{W-36}" y="50" fill="{rcol}" font-size="15" text-anchor="end" class="pulse">★ {rarity}</text>']
    y = 104
    for i, ln in enumerate(lines):
        b.append(f'<g class="late" style="animation:fadein .01s {0.3+i*0.35}s forwards">'
                 f'<text x="36" y="{y}" fill="{GREEN}" font-size="17">&gt;</text>'
                 f'<text x="58" y="{y}" fill="{TXT}" font-size="17">{esc(ln)}</text></g>')
        y += 32
    x = 36
    for t in tags:
        w = len(t) * 15 * CW + 20
        b.append(f'<rect x="{x}" y="{H-62}" width="{w}" height="28" fill="none" stroke="{LINE}"/>'
                 f'<text x="{x+w/2}" y="{H-43}" fill="{BLUE}" font-size="15" text-anchor="middle">{esc(t)}</text>')
        x += w + 10
    b.append(f'<text x="{W-36}" y="{H-43}" fill="{AMBER}" font-size="15" text-anchor="end">OPEN ▶</text>')
    return svg(W, H, "".join(b), name)


files = {
    "hero.svg": hero(),
    "roadmap.svg": roadmap(),
    "card-laan.svg": card("Laan Chuay Aan", "LEGENDARY", PINK,
                          ["Photo of a Thai letter in, plain summary out", "Flags letters that look like scams", "51 automated tests passing"],
                          ["Python", "FastAPI", "Gemini", "LINE"]),
    "card-cooldown.svg": card("Trading Cooldown", "EPIC", BLUE,
                              ["Countdown above sold-out villagers", "Reads vanilla restock mechanics", "No mods required"],
                              ["Minecraft", "mcfunction", "v0.2.0"]),
    "sec-roadmap.svg": section("./roadmap --world 1", "where I've been, where I'm heading"),
    "sec-projects.svg": section("ls ~/projects --featured", "things I shipped"),
    "sec-study.svg": section("open ./study-sites", "free exam prep for ICT courses"),
    "sec-stack.svg": section("cat stack.txt", "tools I use"),
    "sec-stats.svg": section("git log --stats", "auto-updated daily"),
}
for name, s in files.items():
    (OUT / name).write_text(s, encoding="utf-8")
print("wrote", len(files), "files to", OUT)

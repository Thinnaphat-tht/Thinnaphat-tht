# สร้างภาพ SVG ขยับได้ สำหรับหน้าโปรไฟล์ GitHub (ธีม terminal + pixel game)
import base64, pathlib, sys

HERE = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BG, PANEL, LINE = "#0D1117", "#161B22", "#30363D"
TXT, MUTED = "#C9D1D9", "#8B949E"
GREEN, BLUE, AMBER, PINK, RED = "#3FB950", "#58A6FF", "#F2CC60", "#F778BA", "#F85149"
MONO = "Consolas, 'DejaVu Sans Mono', 'Courier New', monospace"
CW = 0.55  # ความกว้างตัวอักษร monospace ต่อ font-size โดยประมาณ


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mascot(name, x, y, w, h, cls=""):
    # CREAMY.exe มาสคอตของเจ้าของ ตัดจาก D:\Portfolio\CREAMY.exe Character Concept Sheet.png
    # ฝังเป็น base64 เพราะ GitHub ไม่โหลดรูปภายนอกที่อยู่ใน SVG
    data = base64.b64encode((HERE / f"creamy-{name}.png").read_bytes()).decode()
    return (f'<g class="{cls}"><image x="{x}" y="{y}" width="{w}" height="{h}" '
            f'style="image-rendering:pixelated" href="data:image/png;base64,{data}"/></g>')


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
    b.append(mascot("coding", 890, 70, 290, 279, "bob"))
    b.append(f'<text x="1035" y="378" fill="{MUTED}" font-size="15" text-anchor="middle">PLAYER 1: CREAMY.exe</text>')
    b.append(f'<text x="1035" y="402" fill="{AMBER}" font-size="15" text-anchor="middle">LV.2</text>')
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
    # เส้นทางกระโดดเป็นโค้งระหว่างเกาะ (จุดยอดสูงกว่าเกาะ 70px)
    def hops(*pts):
        d = f"M{pts[0][0]} {pts[0][1]}"
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 == x1:  # ลงแถวล่าง: โค้งออกด้านขวา
                d += f" Q{x0+120} {(y0+y1)/2} {x1} {y1}"
            else:
                d += f" Q{(x0+x1)/2} {min(y0, y1)-70} {x1} {y1}"
        return d
    done = hops((130, 190), (410, 190), (690, 190), (970, 190), (970, 420))
    for d, col in ((hops((970, 420), (690, 420), (410, 420), (130, 420)), MUTED),
                   (hops((970, 420), (970, 610)), PINK)):
        b.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round" opacity=".7"/>')
    b.append(f'<path d="{done}" fill="none" stroke="{GREEN}" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round" '
             f'style="animation:dash 1.2s linear infinite"/>')
    for i, (x, y, name, sub, col, state) in enumerate(stages):
        dim = state == "locked"
        grass = MUTED if dim else col
        dirt, dark = ("#30363D", "#21262D") if dim else ("#6E4A2E", "#4A3326")
        # เกาะลอยฟ้าแบบพิกเซล: หญ้า 2 ชั้น ดิน 3 ชั้นเรียวลง ลอยขึ้นลงคนละจังหวะ
        isle = (f'<rect x="{x-50}" y="{y-8}" width="100" height="10" fill="{grass}"/>'
                f'<rect x="{x-50}" y="{y+2}" width="100" height="4" fill="{grass}" opacity=".6"/>'
                f'<rect x="{x-42}" y="{y+6}" width="84" height="12" fill="{dirt}"/>'
                f'<rect x="{x-28}" y="{y+18}" width="56" height="10" fill="{dark}"/>'
                f'<rect x="{x-12}" y="{y+28}" width="24" height="8" fill="{dark}"/>')
        if state == "goal":  # ธงบนเกาะเป้าหมาย
            isle += (f'<rect x="{x+26}" y="{y-58}" width="4" height="50" fill="{TXT}"/>'
                     f'<rect x="{x+30}" y="{y-58}" width="26" height="16" fill="{AMBER}"/>')
        if state == "side":
            isle += f'<text x="{x}" y="{y-16}" fill="{PINK}" font-size="30" text-anchor="middle">?</text>'
        cls = "pulse" if state in ("next", "side") else ""
        b.append(f'<g class="{cls}" style="opacity:{0.55 if dim else 1}"><g style="animation:bob {2+i%3*0.4}s ease-in-out {i*0.3}s infinite">{isle}</g></g>')
        b.append(f'<text x="{x}" y="{y+64}" fill="{TXT if dim else col}" font-size="19" text-anchor="middle">{esc(name)}</text>')
        b.append(f'<text x="{x}" y="{y+88}" fill="{MUTED}" font-size="15" text-anchor="middle">{esc(sub)}</text>')
        tag, tcol = tags[state]
        b.append(f'<text x="{x-58}" y="{y+5}" fill="{tcol}" font-size="13" text-anchor="end">{tag}</text>')
    # CREAMY กระโดดข้ามเกาะจาก START มาหยุดที่ด่านถัดไป (ฝึกงาน) แล้ววนใหม่
    b.append(f'<g>{mascot("front", -30, -76, 60, 69)}<animateMotion dur="8s" repeatCount="indefinite" path="{done}" '
             f'keyPoints="0;0;1;1" keyTimes="0;0.08;0.85;1" calcMode="linear"/></g>')
    return svg(W, H, "".join(b), "Career roadmap: cleared Start 2025, study sites, Trading Cooldown, Laan Chuay Aan; "
                                 "next internship (Backend/AI), then level up, co-op, goal Junior AI/Backend Engineer; side quest cybersecurity")


# ---------- 4. การ์ดผลงานแบบหน้าต่าง terminal ----------
def card(name, repo, rcol, cmd, lines, tags):
    W, H = 580, 300
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{BG}" stroke="{LINE}" stroke-width="2"/>',
         f'<path d="M1 13 a12 12 0 0 1 12 -12 h{W-26} a12 12 0 0 1 12 12 v31 h-{W-2} z" fill="{PANEL}"/>',
         f'<rect x="1" y="44" width="{W-2}" height="3" fill="{rcol}"/>',
         f'<circle cx="24" cy="23" r="6" fill="{RED}"/><circle cx="44" cy="23" r="6" fill="{AMBER}"/>'
         f'<circle cx="64" cy="23" r="6" fill="{GREEN}"/>',
         f'<text x="{W/2}" y="28" fill="{MUTED}" font-size="14" text-anchor="middle">~/{esc(repo)}</text>',
         typed_line(26, 84, cmd, TXT, 18, 0.3, max(0.6, len(cmd) * 0.05), prompt=True),
         f'<text x="26" y="120" fill="{rcol}" font-size="22">{esc(name)}</text>']
    t, y = 0.6 + len(cmd) * 0.05, 154
    for ln in lines:
        b.append(f'<g class="late" style="animation:fadein .01s {t}s forwards">'
                 f'<text x="26" y="{y}" fill="{TXT}" font-size="16">{esc(ln)}</text></g>')
        t += 0.3
        y += 28
    b.append(f'<text x="26" y="{H-26}" fill="{BLUE}" font-size="14">{esc("  ".join("[" + x + "]" for x in tags))}</text>')
    b.append(f'<text x="{W-26}" y="{H-26}" fill="{AMBER}" font-size="14" text-anchor="end">OPEN ▶</text>')
    b.append(f'<rect x="{26 + (len(cmd) + 3) * 18 * CW}" y="70" width="10" height="18" fill="{TXT}" class="cur"/>')
    return svg(W, H, "".join(b), name)


files = {
    "hero.svg": hero(),
    "roadmap.svg": roadmap(),
    "card-laan.svg": card("Laan Chuay Aan", "laan-chuay-aan", PINK, "cat about.txt",
                          ["Photo of a Thai letter in, plain summary out", "Flags letters that look like scams", "51 automated tests passing"],
                          ["Python", "FastAPI", "Gemini", "LINE"]),
    "card-cooldown.svg": card("Trading Cooldown", "trading-cooldown", BLUE, "cat about.txt",
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

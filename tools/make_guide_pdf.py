"""Generate the lead-magnet PDF (pure stdlib, minimal PDF writer).

Output: site/assets/princeton-wealth-diagnostic-guide.pdf
Content adapted from blog draft 10 (5 questions), compliance-safe.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "princeton-wealth-diagnostic-guide.pdf"
OUT.parent.mkdir(exist_ok=True)

NAVY = "0.106 0.165 0.290"   # #1B2A4A
BRASS = "0.663 0.557 0.290"  # #A98E4A
INK = "0.078 0.094 0.114"    # #14181D
GREY = "0.42 0.44 0.47"

def esc(t):
    return t.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

class Page:
    def __init__(self):
        self.ops = []
        self.y = 742
    def text(self, x, size, s, font="F1", color=INK, leading=None):
        self.ops.append(f"BT /{font} {size} Tf {color} rg 1 0 0 1 {x} {self.y} Tm ({esc(s)}) Tj ET")
        self.y -= leading or (size * 1.45)
    def para(self, x, size, s, width, font="F1", color=INK):
        for ln in wrap(s, width):
            self.text(x, size, ln, font, color)
        self.y -= size * 0.6
    def rule(self, x1, x2, color=BRASS, w=1.2):
        self.ops.append(f"{color} RG {w} w {x1} {self.y} m {x2} {self.y} l S")
        self.y -= 18
    def gap(self, n): self.y -= n

p1, p2 = Page(), Page()

# ---- Page 1 ----
p1.text(57, 10, "PRINCETON ASSET MANAGEMENT", "F2", BRASS, 26)
p1.text(57, 26, "The Wealth Diagnostic:", "F2", NAVY, 32)
p1.text(57, 26, "5 Questions to Ask Any Advisor", "F2", NAVY, 30)
p1.text(57, 26, "Managing Over $1 Million", "F2", NAVY, 30)
p1.gap(6); p1.rule(57, 250)
p1.para(57, 11, "At $1 million and above, the advisory industry competes for you in earnest. The pitches sound alike and the offices look alike - but the structures behind them are very different. These five questions reveal how any advisor is really paid, regulated, and organized. Ask them plainly, and insist on plain answers.", 92)
p1.gap(8)

QS = [
    ("1. \"Are you a fiduciary at all times, on every account, in writing?\"",
     "Some advisors are fiduciaries in every interaction. Others switch between a fiduciary standard and a sales standard within the same relationship. Do not accept \"yes, I'm a fiduciary.\" Ask: at all times? On every account? Will you confirm it in writing?"),
    ("2. \"How, exactly, are you paid - and by whom?\"",
     "Fee-only means paid solely by you. Commission-based means paid by product providers. Fee-based means both - fees plus commissions. Each model shapes the advice you receive. You should know which one you are in before you wire the first dollar."),
    ("3. \"Who holds my assets?\"",
     "Your assets should sit at an independent custodian - in your name, visible to you daily, movable only where you direct. If the firm holding your money is the same firm advising you, ask why."),
    ("4. \"Who actually manages my portfolio?\"",
     "A named person with credentials - or a model, a call center, and \"the team\"? Ask who makes the decisions, what their qualifications are, and how many clients they are responsible for."),
    ("5. \"What happens when we disagree?\"",
     "Markets will test the relationship. Ask how the advisor handles a client who wants to sell at the bottom - the answer tells you whether you are buying discipline or just agreement."),
]
for q, a in QS:
    p1_or_p2 = p1 if p1.y > 150 else p2
    p1_or_p2.text(57, 13, q, "F2", NAVY, 20)
    p1_or_p2.para(57, 10.5, a, 96, color=INK)

# ---- Page 2 footer content ----
p2.gap(10); p2.rule(57, 538)
p2.text(57, 13, "The standard to measure any firm against - including ours", "F2", NAVY, 20)
p2.para(57, 10.5, "An advisor who is a fiduciary at all times, paid only by you, using an independent custodian, with named and credentialed people managing the portfolio, has removed most structural conflicts before the first recommendation is made. That is the standard independent, fee-only registered investment advisers are built around.", 96)
p2.gap(14)
p2.text(57, 12, "Talk it through with a fiduciary.", "F2", BRASS, 18)
p2.para(57, 10.5, "Princeton Asset Management is an independent, fee-only fiduciary founded in 2008. Principals are CFA Charterholders; client assets are custodied at Fidelity Investments. A complimentary 15-minute wealth diagnostic comes with no obligation - and you'll leave with something actionable either way.", 96)
p2.text(57, 10.5, "Schedule: princetonam.com/schedule  |  561-800-4100  |  clientservices@princetonam.com", "F2", NAVY, 22)
p2.gap(10)
p2.para(57, 8, "Princeton Asset Management is an independent registered investment adviser. This guide is general education, not individualized investment, tax, or legal advice. Consult your own advisors regarding your situation.", 128, color=GREY)

def content_stream(page):
    return "\n".join(page.ops)

streams = [content_stream(p1), content_stream(p2)]
objs = []
objs.append("<< /Type /Catalog /Pages 2 0 R >>")                                   # 1
objs.append("<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>")                     # 2
page_tmpl = ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
             "/Resources << /Font << /F1 {f1} 0 R /F2 {f2} 0 R >> >> /Contents {c} 0 R >>")
objs.append(page_tmpl.format(f1=5, f2=6, c=7))                                      # 3
objs.append(page_tmpl.format(f1=5, f2=6, c=8))                                      # 4
objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")               # 5
objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")          # 6
for s in streams:
    objs.append(f"<< /Length {len(s.encode('latin-1', 'replace'))} >>\nstream\n{s}\nendstream")  # 7, 8

out, offsets = ["%PDF-1.4"], []
pos = len(out[0]) + 1
for i, o in enumerate(objs, 1):
    offsets.append(pos)
    block = f"{i} 0 obj\n{o}\nendobj"
    out.append(block)
    pos += len(block.encode("latin-1", "replace")) + 1
xref_pos = pos
xref = ["xref", f"0 {len(objs)+1}", "0000000000 65535 f "]
xref += [f"{off:010d} 00000 n " for off in offsets]
trailer = f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF"
OUT.write_bytes(("\n".join(out) + "\n" + "\n".join(xref) + "\n" + trailer).encode("latin-1", "replace"))
print("wrote", OUT, OUT.stat().st_size, "bytes")

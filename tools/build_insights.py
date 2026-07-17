"""Build insights/*.html + insights.html from ../blog-drafts/*.md (stdlib only).

Usage:  python build_insights.py
Re-run any time a draft changes.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # site/
DRAFTS = ROOT.parent / "blog-drafts"                    # WebSiteRebuilt/blog-drafts
OUT = ROOT / "insights"
OUT.mkdir(exist_ok=True)

# file-number -> category (addendum §5: segment categories for related-insight blocks)
CATEGORIES = {
    "01": "Retirees", "02": "Retirees", "03": "Retirees", "04": "Investing",
    "05": "Retirees", "06": "Business Owners", "07": "Professionals",
    "08": "Investing", "09": "Professionals", "10": "Investing",
    "11": "Retirees", "12": "Investing",
}
# addendum §5 suggested publishing order (index display order)
ORDER = ["10", "01", "06", "02", "09", "05", "11", "03", "04", "08", "12", "07"]

# post number -> (image file in assets/img/, alt text); chosen so adjacent index
# cards never repeat an image
IMAGES = {
    "01": ("blog-porch-couple.jpg", "A retired couple relaxing on their porch with their dogs"),
    "02": ("blog-tax-planning.jpg", "A couple reviewing tax documents at their kitchen table"),
    "03": ("family-hug.jpg", "A multigenerational family embracing outdoors"),
    "04": ("dunes-horizon.jpg", "A couple on open dunes under a wide sky"),
    "05": ("couple-home.jpg", "A couple arriving at their new home"),
    "06": ("blog-workshop-owner.jpg", "A business owner working on a laptop in his workshop"),
    "07": ("blog-surgeons.jpg", "Surgeons at work in an operating room"),
    "08": ("blog-facade-sky.jpg", "A modern building facade against a bright blue sky"),
    "09": ("blog-market-screen.jpg", "A stock market chart on a trading screen"),
    "10": ("blog-advisor-consult.jpg", "A couple reviewing documents with an advisor"),
    "11": ("blog-autumn-walk.jpg", "A senior couple walking arm in arm through an autumn park"),
    "12": ("blog-desk-charts.jpg", "A laptop showing market charts on a sunlit desk"),
}

def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def inline(t: str) -> str:
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a class="textlink" href="\2">\1</a>', t)
    # bare [Schedule ...] CTA bracket -> link
    t = re.sub(r"\[(Schedule[^\]]*)\]", r'<a class="btn" href="../schedule.html">\1</a>', t)
    return t

def md_to_html(body: str) -> str:
    lines = body.split("\n")
    html, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1; continue
        if s.startswith("### "):
            html.append(f"<h3>{inline(s[4:])}</h3>"); i += 1; continue
        if s.startswith("## "):
            html.append(f"<h2>{inline(s[3:])}</h2>"); i += 1; continue
        if s in ("---", "***"):
            html.append("<hr>"); i += 1; continue
        if s.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            if len(rows) >= 2 and set("".join(rows[1])) <= set("-: "):
                head, data = rows[0], rows[2:]
            else:
                head, data = rows[0], rows[1:]
            t = ['<div class="table-scroll"><table>', "<thead><tr>"]
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in data:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            html.append("".join(t)); continue
        if s.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            text = " ".join(b for b in block if b)
            if "[Schedule" in text or "wealth diagnostic</a>" in text:
                html.append(f'<div class="article-cta"><p>{inline(text)}</p></div>')
            elif text.startswith("*") and text.endswith("*"):
                html.append(f'<p class="article-disclosure">{inline(text.strip("*"))}</p>')
            else:
                html.append(f"<blockquote>{inline(text)}</blockquote>")
            continue
        if re.match(r"^[-*] ", s):
            html.append("<ul>")
            while i < n and re.match(r"^[-*] ", lines[i].strip()):
                html.append(f"<li>{inline(lines[i].strip()[2:])}</li>"); i += 1
            html.append("</ul>"); continue
        if re.match(r"^\d+\. ", s):
            html.append("<ol>")
            while i < n and re.match(r"^\d+\. ", lines[i].strip()):
                html.append(f"<li>{inline(re.sub(r'^\\d+\\. ', '', lines[i].strip()))}</li>"); i += 1
            html.append("</ol>"); continue
        # paragraph: join soft-wrapped lines
        para = [s]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{2,3} |[-*] |\d+\. |>|\||---)", lines[i].strip()):
            para.append(lines[i].strip()); i += 1
        html.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(html)

def shell(title, desc, body, canonical_slug):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Princeton Asset Management</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/site.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap nav-bar">
    <a class="brand" href="../index.html">Princeton <span>Asset Management</span></a>
    <nav aria-label="Primary"><ul class="nav-links">
      <li><a href="../services.html">Services</a></li>
      <li><a href="../families.html">Who We Serve</a></li>
      <li><a href="../approach.html">How We Invest</a></li>
      <li><a href="../team.html">Team</a></li>
      <li><a href="../fees.html">Fees</a></li>
      <li><a href="../insights.html" aria-current="page">Insights</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a class="login-link" href="../login.html" rel="noopener">Client Login</a>
      <a class="btn" href="../schedule.html">Schedule a Call</a>
    </div>
    <button class="nav-toggle" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  <div class="mobile-menu wrap"><ul>
    <li><a href="../services.html">Services</a></li>
    <li><a href="../families.html">Who We Serve</a></li>
    <li><a href="../approach.html">How We Invest</a></li>
    <li><a href="../team.html">Team</a></li>
    <li><a href="../fees.html">Fees</a></li>
    <li><a href="../insights.html">Insights</a></li>
    <li><a href="../schedule.html">Schedule a Call</a></li>
  </ul></div>
</header>
<main id="main">
  <article class="article">
    <div class="wrap"><div class="article-body">
{body}
      <p class="mt-4"><a class="textlink" href="../insights.html">← All insights</a></p>
    </div></div>
  </article>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-legal">
      <p>Princeton Asset Management is an independent registered investment adviser. This article is general education, not individualized investment, tax, or legal advice.</p>
      <p><a href="#">Form CRS</a> · <a href="#">Form ADV Part 2</a> · <a href="#">Privacy Policy</a> · <a href="#">Terms of Use</a></p>
      <p>© 2026 Princeton Asset Management. All rights reserved.</p>
    </div>
  </div>
</footer>
<div class="mobile-cta"><a class="btn" href="../schedule.html">Schedule Your Wealth Diagnostic</a></div>
<script src="../js/site.js"></script>
</body>
</html>"""

posts = {}
for f in sorted(DRAFTS.glob("[0-9][0-9]-*.md")):
    num = f.name[:2]
    raw = f.read_text(encoding="utf-8")
    title_m = re.search(r"^# (.+)$", raw, re.M)
    title = title_m.group(1).strip()
    desc_m = re.search(r"\*\*Meta description:\*\*\s*(.+)", raw)
    desc = desc_m.group(1).strip() if desc_m else ""
    slug_m = re.search(r"\*\*Suggested URL slug:\*\*\s*(.+)", raw)
    slug = slug_m.group(1).strip().strip("/").split("/")[-1] if slug_m else f.stem
    # Body = everything after the "# Title" line (frontmatter lines may sit
    # before OR after the title depending on the draft). Strip any remaining
    # frontmatter lines and a leading "---" separator; keep later "---" hrs.
    body_md = raw[title_m.end():]
    body_md = re.sub(r"^\*\*(SEO title|Meta description|Suggested URL slug):\*\*.*$",
                     "", body_md, flags=re.M)
    body_md = re.sub(r"^\s*---\s*\n", "", body_md.lstrip("\n"), count=1)
    img, alt = IMAGES.get(num, ("family-dinner.jpg", "Princeton Asset Management"))
    hero_img = (f'<div class="img-frame wide" style="margin-bottom: 40px;">'
                f'<img src="../assets/img/{img}" alt="{esc(alt)}" loading="eager"></div>')
    body = (f"<h1>{esc(title)}</h1>\n"
            f"<p class=\"meta\">{CATEGORIES.get(num,'Investing')} · Princeton Asset Management</p>\n"
            f"{hero_img}\n" + md_to_html(body_md))
    (OUT / f"{slug}.html").write_text(shell(title, desc, body, slug), encoding="utf-8")
    posts[num] = {"title": title, "desc": desc, "slug": slug, "cat": CATEGORIES.get(num, "Investing")}
    print(f"built insights/{slug}.html")

# ---------- index ----------
cards = []
for num in ORDER:
    p = posts[num]
    img, alt = IMAGES.get(num, ("family-dinner.jpg", ""))
    cards.append(f"""        <a class="card post-card reveal" href="insights/{p['slug']}.html">
          <div class="card-media">
            <img src="assets/img/{img}" alt="{esc(alt)}" loading="lazy">
          </div>
          <span class="card-kicker">{esc(p['cat'])}</span>
          <h3>{esc(p['title'])}</h3>
          <p>{esc(p['desc'])}</p>
          <span class="card-more">Read →</span>
        </a>""")

index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Insights — Princeton Asset Management</title>
<meta name="description" content="Plain-English thinking on retirement, taxes, business exits, and investing for families with $1 million or more — from an independent fiduciary.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap nav-bar">
    <a class="brand" href="index.html">Princeton <span>Asset Management</span></a>
    <nav aria-label="Primary"><ul class="nav-links">
      <li><a href="services.html">Services</a></li>
      <li><a href="families.html">Who We Serve</a></li>
      <li><a href="approach.html">How We Invest</a></li>
      <li><a href="team.html">Team</a></li>
      <li><a href="fees.html">Fees</a></li>
      <li><a href="insights.html" aria-current="page">Insights</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a class="login-link" href="login.html" rel="noopener">Client Login</a>
      <a class="btn" href="schedule.html">Schedule a Call</a>
    </div>
    <button class="nav-toggle" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  <div class="mobile-menu wrap"><ul>
    <li><a href="services.html">Services</a></li>
    <li><a href="families.html">Who We Serve</a></li>
    <li><a href="approach.html">How We Invest</a></li>
    <li><a href="team.html">Team</a></li>
    <li><a href="fees.html">Fees</a></li>
    <li><a href="insights.html">Insights</a></li>
    <li><a href="schedule.html">Schedule a Call</a></li>
  </ul></div>
</header>
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <span class="label">Insights</span>
      <h1>Thinking you can act on.</h1>
      <p class="lede">Plain-English analysis of the decisions that matter above $1 million — retirement income, taxes, business exits, and what the industry won't tell you. No jargon, no hype, no predictions.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="grid grid-3">
{chr(10).join(cards)}
      </div>
    </div>
  </section>
  <section class="cta-band">
    <div class="wrap reveal">
      <h2>The first conversation costs nothing — and clarifies everything.</h2>
      <p>Fifteen minutes. Our honest read on your positioning, and the two or three decisions likely to matter most.</p>
      <a class="btn" href="schedule.html">Schedule Your Wealth Diagnostic</a>
      <p class="btn-note">Complimentary · Fiduciary from the first minute · No obligation to proceed</p>
    </div>
  </section>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-legal">
      <p>Princeton Asset Management is an independent registered investment adviser. Articles are general education, not individualized investment, tax, or legal advice.</p>
      <p><a href="#">Form CRS</a> · <a href="#">Form ADV Part 2</a> · <a href="#">Privacy Policy</a> · <a href="#">Terms of Use</a></p>
      <p>© 2026 Princeton Asset Management. All rights reserved.</p>
    </div>
  </div>
</footer>
<div class="mobile-cta"><a class="btn" href="schedule.html">Schedule Your Wealth Diagnostic</a></div>
<script src="js/site.js"></script>
</body>
</html>"""
(ROOT / "insights.html").write_text(index, encoding="utf-8")
print("built insights.html")
print(f"done: {len(posts)} posts")

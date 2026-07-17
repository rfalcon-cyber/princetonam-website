"""Build interior pages from a shared shell (stdlib only).

Usage: python build_pages.py    — regenerates the 9 interior pages.
Edit page content in the PAGES dict below.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # site/

NAV = [("services.html", "Services"), ("families.html", "Who We Serve"),
       ("approach.html", "How We Invest"), ("team.html", "Team"),
       ("fees.html", "Fees"), ("insights.html", "Insights")]

WHO_WE_SERVE_SUBITEMS = [
    ("families.html", "Families"),
    ("professionals.html", "Professionals"),
    ("retirees.html", "Retirees"),
    ("business-owners.html", "Business Owners"),
    ("foundations-endowments.html", "Foundations &amp; Endowments"),
    ("professionals.html", "Executives"),
    ("institutional.html", "Institutions"),
]

def shell(fname, title, desc, main):
    def nav_item(h, t):
        current = ' aria-current="page"' if h == fname else ""
        if h == "families.html" and t == "Who We Serve":
            sub = "\n".join(f'          <li><a href="{sh}">{st}</a></li>' for sh, st in WHO_WE_SERVE_SUBITEMS)
            return (f'      <li class="has-dropdown"><a href="{h}"{current}>{t}</a>\n'
                    f'        <ul class="nav-dropdown">\n{sub}\n        </ul>\n'
                    f'      </li>')
        return f'      <li><a href="{h}"{current}>{t}</a></li>'

    def mnav_item(h, t):
        if h == "families.html" and t == "Who We Serve":
            sub = "\n".join(f'    <li class="mobile-submenu"><a href="{sh}">{st}</a></li>' for sh, st in WHO_WE_SERVE_SUBITEMS)
            return f'    <li><a href="{h}">{t}</a></li>\n{sub}'
        return f'    <li><a href="{h}">{t}</a></li>'

    links = "\n".join(nav_item(h, t) for h, t in NAV)
    mlinks = "\n".join(mnav_item(h, t) for h, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Princeton Asset Management</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap nav-bar">
    <a class="brand" href="home.html">Princeton <span>Asset Management</span></a>
    <nav aria-label="Primary"><ul class="nav-links">
{links}
    </ul></nav>
    <div class="nav-cta">
      <a class="login-link" href="login.html" rel="noopener">Client Login</a>
      <a class="btn" href="schedule.html">Schedule a Call</a>
    </div>
    <button class="nav-toggle" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  <div class="mobile-menu wrap"><ul>
{mlinks}
    <li><a href="schedule.html">Schedule a Call</a></li>
    <li><a class="login-link" href="login.html" rel="noopener">Client Login</a></li>
  </ul></div>
</header>
<main id="main">
{main}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="home.html">Princeton <span>Asset Management</span></a>
        <p class="mt-3" style="max-width: 34ch;">Independent, fee-only fiduciary wealth management. Founded 2008. Women- and minority-owned.</p>
      </div>
      <div>
        <h4>Firm</h4>
        <ul>
          <li><a href="families.html">Who We Serve</a></li>
          <li><a href="approach.html">How We Invest</a></li>
          <li><a href="team.html">Our Team</a></li>
          <li><a href="fees.html">Fees &amp; Fiduciary Standard</a></li>
          <li><a href="institutional.html">Institutional</a></li>
        </ul>
      </div>
      <div>
        <h4>Resources</h4>
        <ul>
          <li><a href="insights.html">Insights</a></li>
          <li><a href="schedule.html">Schedule a Call</a></li>
          <li><a href="login.html" rel="noopener">Client Login</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:+15618004100">561-800-4100</a></li>
          <li><a href="mailto:clientservices@princetonam.com">clientservices@princetonam.com</a></li>
          <li>One Park Place<br>621 NW 53rd St., Ste 240<br>Boca Raton, FL 33487</li>
        </ul>
      </div>
    </div>
    <div class="footer-legal">
      <p>Princeton Asset Management is an independent registered investment adviser. Registration does not imply a certain level of skill or training. This website is for informational purposes only and does not constitute investment, tax, or legal advice, nor an offer to buy or sell any security.</p>
      <p><a href="#">Form CRS</a> · <a href="#">Form ADV Part 2</a> · <a href="#">Privacy Policy</a> · <a href="#">Terms of Use</a></p>
      <p>© 2026 Princeton Asset Management. All rights reserved.</p>
    </div>
  </div>
</footer>
<div class="mobile-cta"><a class="btn" href="schedule.html">Schedule Your Wealth Diagnostic</a></div>
<script src="js/site.js"></script>
</body>
</html>"""

CTA_BAND = """  <section class="cta-band">
    <div class="wrap reveal">
      <h2>The first conversation costs nothing — and clarifies everything.</h2>
      <p>Fifteen minutes. Our honest read on your positioning, and the two or three decisions likely to matter most.</p>
      <a class="btn" href="schedule.html">Schedule Your Wealth Diagnostic</a>
      <p class="btn-note">Complimentary · Fiduciary from the first minute · No obligation to proceed</p>
    </div>
  </section>"""

LEAD_MAGNET = """  <section class="section">
    <div class="wrap">
      <div class="lead-magnet reveal">
        <div class="lm-copy">
          <span class="label">Free Guide</span>
          <h2>The Wealth Diagnostic: 5 questions to ask any advisor managing over $1M.</h2>
          <p class="mt-2">A two-page guide to how any advisory firm is really paid, regulated, and structured — before you move a dollar.</p>
          <ul>
            <li>The one question that exposes part-time fiduciaries</li>
            <li>Fee-only vs. fee-based — and why the single letter matters</li>
            <li>The custody question that protects you from the worst outcomes</li>
          </ul>
        </div>
        <div class="lm-form">
          <!-- PRODUCTION: set data-endpoint to your form service (e.g. Formspree/ConvertKit URL)
               or replace this block with a Squarespace form + automated download email. -->
          <form class="lead-form" novalidate data-endpoint="">
            <div>
              <label for="lm-name">Name</label>
              <input id="lm-name" name="name" type="text" autocomplete="name" required>
              <p class="field-error">Please enter your name.</p>
            </div>
            <div>
              <label for="lm-email">Email</label>
              <input id="lm-email" name="email" type="email" autocomplete="email" required>
              <p class="field-error">Please enter a valid email address.</p>
            </div>
            <input class="honeypot" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
            <button class="btn" type="submit">Get the Guide (PDF)</button>
            <p class="lm-fineprint">We'll send occasional insights for families with $1M+. No spam, unsubscribe anytime. We never share your information.</p>
          </form>
          <div class="lm-success" role="status">
            <h3>Your guide is ready.</h3>
            <p>We've also noted your interest — if you asked a question, a principal (not a sales team) will reply.</p>
            <a class="btn" href="assets/princeton-wealth-diagnostic-guide.pdf" download>Download the PDF</a>
          </div>
        </div>
      </div>
    </div>
  </section>"""

PAGES = {}

# ---------------- SERVICES (family-office approach) ----------------
PAGES["services.html"] = ("Services — A Family-Office Approach", "Investment management, retirement planning, trust and estate investments, and multi-asset alternatives — one team coordinating your family's full financial life.", f"""
  <section class="page-hero-split">
    <div class="wrap grid grid-7-5">
      <div>
        <span class="label">Services</span>
        <h1>A family-office approach for complex capital.</h1>
        <p class="lede">A discreet, highly personalized relationship for families and individuals who expect strategic coordination, thoughtful stewardship, and a single trusted advisor.</p>
      </div>
      <div class="img-frame tall reveal">
        <img src="assets/img/retirees-travel.jpg" alt="A couple enjoying the freedom of well-planned wealth" loading="eager">
      </div>
    </div>
  </section>

  <section class="section" style="padding-top: 0;">
    <div class="wrap">
      <div class="stat-strip reveal">
        <div class="stat"><b>2008</b><span>Independent since</span></div>
        <div class="stat"><b>CFA®</b><span>Charterholder principals</span></div>
        <div class="stat"><b>GIPS®</b><span>Firm-wide compliance</span></div>
        <div class="stat"><b>100%</b><span>Fee-only. Nothing sold, ever</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="reveal">
        <span class="label">What We Do</span>
        <h2 style="max-width: 22ch;">Four disciplines. One coordinated engagement.</h2>
      </div>
      <div class="mt-6">
        <div class="service-row reveal">
          <div class="service-num">01</div>
          <div>
            <h3>Investment Management</h3>
            <p>High-conviction, actively managed portfolios built for changing interest-rate and market environments — each one customized to your objectives, never pulled from a model shelf.</p>
          </div>
          <div class="service-meta"><strong>In practice</strong>Security-level credit research, custom fixed income, disciplined rebalancing, tax-aware implementation.</div>
        </div>
        <div class="service-row reveal">
          <div class="service-num">02</div>
          <div>
            <h3>Retirement Planning</h3>
            <p>Comprehensive strategies that balance income needs, tax efficiency, and capital preservation across your full financial picture — engineered year by year, not projected on an average.</p>
          </div>
          <div class="service-meta"><strong>In practice</strong>Withdrawal sequencing, Roth conversion windows, Social Security timing, bracket and IRMAA management.</div>
        </div>
        <div class="service-row reveal">
          <div class="service-num">03</div>
          <div>
            <h3>Trust &amp; Estate Investments</h3>
            <p>Stewardship of trust assets and intergenerational wealth with discretion and a fiduciary mindset — invested to honor both the document and the family behind it.</p>
          </div>
          <div class="service-meta"><strong>In practice</strong>Trustee coordination, distribution planning, exemption-aware gifting, next-generation onboarding.</div>
        </div>
        <div class="service-row reveal">
          <div class="service-num">04</div>
          <div>
            <h3>Multi-Asset &amp; Alternatives</h3>
            <p>Access across public equities, fixed income, and vetted private markets — private equity, infrastructure, real estate, and private credit — with independent diligence and zero placement fees.</p>
          </div>
          <div class="service-meta"><strong>In practice</strong>Liquidity-matched allocations, manager diligence, capital-call planning, consolidated reporting.</div>
        </div>
      </div>
    </div>
  </section>

  <section class="quote-band">
    <div class="wrap reveal">
      <span class="label">On the Same Wavelength</span>
      <p class="big-quote">One team, quarterbacking your family's <em>entire</em> financial life.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-5-7">
      <div class="img-frame reveal">
        <img src="assets/img/advisor-meeting.jpg" alt="A principal in conversation with a client family" loading="lazy">
      </div>
      <div class="reveal">
        <span class="label">Integrated Family Services</span>
        <h2>Strategy is only half the job. Coordination is the other half.</h2>
        <p class="mt-3" style="color: var(--ink-soft);">Most families with real complexity have five advisors and no coordinator: a CPA who sees the taxes, an attorney who sees the documents, an insurance agent who sees a sale, and a broker who sees a fee. Nobody sees the whole field.</p>
        <p class="mt-3" style="color: var(--ink-soft);">We take that seat. One team with a complete view — investments, taxes, estate, philanthropy, the 401(k) nobody looks at — coordinating your existing professionals and telling you plainly when something doesn't fit. That's the family-office approach: not another product, but a single point of accountability.</p>
        <p class="mt-3"><a class="textlink" href="approach.html">How we invest →</a></p>
      </div>
    </div>
  </section>
{LEAD_MAGNET}
{CTA_BAND}""")

# ---------------- WHO WE SERVE ----------------
PAGES["families.html"] = ("Who We Serve", "Princeton Asset Management serves business owners, professionals, and retirees with $1 million or more — plus foundations, trusts, and family offices.", f"""
  <section class="page-hero">
    <div class="wrap">
      <span class="label">Who We Serve</span>
      <h1>Wealth is personal. So is the way we manage it.</h1>
      <p class="lede">No models, no tiers, no "you'll be assigned an advisor." We work with a deliberately limited number of families — because customization doesn't scale, and we refuse to pretend it does.</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="img-frame wide reveal">
        <img src="assets/img/passingItOn.png" alt="Three generations of a family at dinner together — passing it on" loading="eager">
      </div>
      <p class="img-caption">Three generations, one balance sheet — the situation we're built for.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="reveal">
        <span class="label">Start With What Matters to You</span>
        <h2 style="max-width: 24ch;">The questions we actually work on.</h2>
      </div>
      <dl class="mt-6">
        <div class="fact-row reveal">
          <dt>"Can I actually afford to retire?"</dt>
          <dd>We turn the portfolio into a paycheck plan: withdrawal order, tax brackets year by year, and what happens in the bad decade — not just an average return assumption.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>"What happens when I sell the business?"</dt>
          <dd>Exit modeling before the letter of intent — entity structure, QSBS eligibility, installment treatment, and what the after-tax number really funds.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>"Am I paying more tax than I need to?"</dt>
          <dd>Roth conversion windows, gain harvesting, asset location, charitable structure — coordinated with your CPA, not in competition with them.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>"Is my family protected if something happens to me?"</dt>
          <dd>Estate structure, beneficiary hygiene, and a written continuity plan your spouse can actually follow — reviewed against current exemption law.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>"Is anyone actually watching all of this together?"</dt>
          <dd>Investments, taxes, estate, insurance, and the 401(k) nobody looks at — one coordinated view, reported through institutional-grade Black Diamond reporting.</dd>
        </div>
      </dl>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="center reveal">
        <span class="label">Three Kinds of Complexity</span>
        <h2>Find your situation.</h2>
      </div>
      <div class="grid grid-3 mt-6">
        <a class="card reveal" href="business-owners.html">
          <span class="card-kicker">Business Owners</span>
          <h3>Your largest asset deserves a plan.</h3>
          <p>Most owners hold 60–80% of their net worth in the company. The exit is the financial event of your life — and most of its tax outcome is decided before the LOI.</p>
          <span class="card-more">For business owners →</span>
        </a>
        <a class="card reveal" href="professionals.html">
          <span class="card-kicker">Physicians, Attorneys &amp; Executives</span>
          <h3>High income deserves more than a high tax bill.</h3>
          <p>Concentrated stock, deferred compensation, K-1s, RSUs vesting into a 37% bracket. Earning well and being positioned well are different skills.</p>
          <span class="card-more">For professionals →</span>
        </a>
        <a class="card reveal" href="retirees.html">
          <span class="card-kicker">Retirees &amp; Pre-Retirees</span>
          <h3>A paycheck from the portfolio — that lasts.</h3>
          <p>Sequence risk, Social Security timing, the tax window between 62 and 65 — retirement income is an engineering problem. We engineer it.</p>
          <span class="card-more">For retirees →</span>
        </a>
      </div>
      <p class="center mt-4 reveal" style="color: var(--ink-muted); font-size: 0.92rem;">We also serve foundations, dynasty trusts, and family offices — <a class="textlink" href="institutional.html">Institutional</a>.</p>
    </div>
  </section>
{CTA_BAND}""")

# ---------------- BUSINESS OWNERS ----------------
PAGES["business-owners.html"] = ("For Business Owners", "Exit modeling, pre-sale tax planning, and post-sale wealth management for business owners — from an independent fiduciary with nothing to sell you.", f"""
  <section class="page-hero-split">
    <div class="wrap grid grid-7-5">
      <div>
        <span class="label">Business Owners</span>
        <h1>Your largest asset deserves a plan.</h1>
        <p class="lede">For most owners, 60–80% of net worth sits in one company. Everything — retirement, the family's security, what you pass on — depends on decisions made in an 18-month window around the exit. We model those decisions before you sign anything.</p>
      </div>
      <div class="img-frame reveal">
        <img src="assets/img/executive-tower.jpg" alt="A business owner taking a call in a modern office tower" loading="eager">
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-5-7">
      <div class="reveal">
        <span class="label">Before the Sale</span>
        <h2>Most of the tax outcome is decided before the LOI.</h2>
      </div>
      <div class="reveal">
        <p style="color: var(--ink-soft);">Entity structure, QSBS eligibility, charitable vehicles, installment treatment, state residency — the levers that change your after-tax proceeds by seven figures close quietly, months before the deal team shows up. We work alongside your CPA and deal counsel to model the exit while the choices are still open.</p>
        <p class="mt-3" style="color: var(--ink-soft);">Then we answer the question that actually keeps owners up at night: <strong>what does the after-tax number really fund?</strong> Not as a projection with a smooth 7% line — as a plan that survives bad markets, inflation, and a 35-year retirement.</p>
        <p class="mt-3"><a class="textlink" href="insights/selling-your-business-tax-moves-before-the-sale.html">Read: the tax moves that must happen before the LOI →</a></p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="reveal"><span class="label">After the Sale</span>
      <h2 style="max-width: 22ch;">From one concentrated asset to a portfolio that pays you.</h2></div>
      <div class="grid grid-3 mt-6">
        <div class="card reveal">
          <h3>Liquidity, staged</h3>
          <p>Proceeds don't need to be invested in a week. We build a staged deployment plan so you're never forced to buy a market top with your life's work.</p>
        </div>
        <div class="card reveal">
          <h3>Income replacement</h3>
          <p>The business paid you a salary and distributions. The portfolio must now do that job — reliably, tax-intelligently, across public and private markets.</p>
        </div>
        <div class="card reveal">
          <h3>Passing it on</h3>
          <p>Estate exemptions are generous today and legislated to change. We structure gifts and trusts while the window is open — with your attorney, on your timeline.</p>
        </div>
      </div>
    </div>
  </section>
{CTA_BAND}""")

# ---------------- PROFESSIONALS ----------------
PAGES["professionals.html"] = ("For Physicians, Attorneys & Executives", "Tax-first wealth management for physicians, attorneys, CPAs, and executives — concentrated stock, deferred compensation, and equity comp handled by an independent fiduciary.", f"""
  <section class="page-hero-split">
    <div class="wrap grid grid-7-5">
      <div>
        <span class="label">Physicians, Attorneys &amp; Executives</span>
        <h1>High income deserves more than a high tax bill.</h1>
        <p class="lede">You earn in the top brackets, your equity vests whether the timing suits you or not, and every "advisor" you meet wants to sell you insurance. What you actually need is positioning: tax, concentration, and time — managed together.</p>
      </div>
      <div class="img-frame reveal">
        <img src="assets/img/physician.jpg" alt="A physician at work" loading="eager">
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <dl>
        <div class="fact-row reveal">
          <dt>Concentrated stock</dt>
          <dd>There are four exits from a concentrated position besides selling it outright — exchange funds, collars, staged 10b5-1 plans, and charitable structures. Which one fits depends on your basis, your restrictions, and your intentions. <a class="textlink" href="insights/concentrated-stock-4-exits-besides-selling.html">Read the four exits →</a></dd>
        </div>
        <div class="fact-row reveal">
          <dt>Equity &amp; deferred compensation</dt>
          <dd>RSU vesting schedules, options, 409A deferrals, and partnership distributions — sequenced against your bracket, not against the calendar.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>Tax drag on the portfolio itself</dt>
          <dd>At your bracket, the difference between a tax-aware portfolio and an ordinary one compounds meaningfully. Direct indexing, asset location, and loss harvesting are tools — when they fit. <a class="textlink" href="insights/direct-indexing-vs-etfs-high-earners-tax-alpha.html">Direct indexing vs. ETFs →</a></dd>
        </div>
        <div class="fact-row reveal">
          <dt>Time</dt>
          <dd>You bill hours or run a P&amp;L. The plan has to run without weekly homework from you — one coordinated view, principals who answer the phone, meetings that respect your calendar.</dd>
        </div>
      </dl>
      <p class="mt-4 reveal"><a class="textlink" href="insights/case-study-physician-couple-4m-lifetime-tax.html">Case study: a physician couple's lifetime-tax plan (hypothetical) →</a></p>
    </div>
  </section>
{CTA_BAND}""")

# ---------------- RETIREES ----------------
PAGES["retirees.html"] = ("For Retirees & Pre-Retirees", "Retirement income engineering — withdrawal order, Roth conversions, Social Security timing, and sequence risk — from an independent fiduciary founded 2008.", f"""
  <section class="page-hero-split">
    <div class="wrap grid grid-7-5">
      <div>
        <span class="label">Retirees &amp; Pre-Retirees</span>
        <h1>A paycheck from the portfolio — that lasts.</h1>
        <p class="lede">The question isn't whether you've saved enough. It's whether the portfolio can pay you reliably, tax-intelligently, through every market you'll live through — including the bad decade nobody plans for.</p>
      </div>
      <div class="img-frame reveal">
        <img src="assets/img/retirees-golf.jpg" alt="A retired couple on the golf course at sunset" loading="eager">
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-5-7">
      <div class="reveal">
        <span class="label">The Engineering Problem</span>
        <h2>Retirement income is a sequencing problem.</h2>
      </div>
      <div class="reveal">
        <p style="color: var(--ink-soft);">Which account do you draw first — taxable, IRA, or Roth? When do you convert, and how much, before RMDs and Medicare surcharges lock in? When does each spouse claim Social Security? The same portfolio can fund very different retirements depending on the order of operations.</p>
        <p class="mt-3" style="color: var(--ink-soft);">We build the year-by-year plan: withdrawal order, conversion windows, bracket management, and a fixed-income allocation designed by specialists — because a retiree's bond portfolio is not a place for guesswork.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="reveal"><span class="label">From the Insights Library</span>
      <h2>Start with the decisions that matter most.</h2></div>
      <div class="grid grid-3 mt-6">
        <a class="card post-card reveal" href="insights/retiring-with-3-million-annual-spending.html">
          <span class="card-kicker">Retirees</span>
          <h3>Retiring With $3 Million: What Actually Changes</h3>
          <span class="card-more">Read →</span>
        </a>
        <a class="card post-card reveal" href="insights/tax-window-62-to-65-roth-conversions-aca.html">
          <span class="card-kicker">Retirees</span>
          <h3>The Tax Window Between 62 and 65</h3>
          <span class="card-more">Read →</span>
        </a>
        <a class="card post-card reveal" href="insights/social-security-2-million-net-worth.html">
          <span class="card-kicker">Retirees</span>
          <h3>Social Security With a $2M+ Net Worth</h3>
          <span class="card-more">Read →</span>
        </a>
      </div>
    </div>
  </section>
{CTA_BAND}""")

# ---------------- HOW WE INVEST ----------------
PAGES["approach.html"] = ("How We Invest", "Capital preservation first. Fixed income and credit specialization, custom portfolios across public and private markets, GIPS-aligned reporting via Black Diamond.", f"""
  <section class="page-hero">
    <div class="wrap">
      <span class="label">How We Invest</span>
      <h1>Portfolios that don't require prediction to survive.</h1>
      <p class="lede">Capital preservation first. Specialization in fixed income and credit. Custom portfolios — never models — across public and private markets. That's the whole philosophy, and we're happy to defend every word of it.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-5-7">
      <div class="reveal">
        <span class="label">1 — Every Asset Class</span>
        <h2>In-house where we're specialists. Vetted partners where we're not.</h2>
        <div class="img-frame mt-4">
          <img src="assets/img/blog-tax-planning.jpg" alt="A couple reviewing their financial plan together" loading="eager">
        </div>
      </div>
      <div class="reveal">
        <p style="color: var(--ink-soft);"><strong>Fixed income and credit are managed in-house</strong> — security by security, with direct credit research. It's the firm's founding specialization and where our CFA training does its heaviest work.</p>
        <p class="mt-3" style="color: var(--ink-soft);"><strong>Equities</strong> are built as customized allocations — direct positions, index vehicles, or both — shaped by your tax situation, not a model's convenience.</p>
        <p class="mt-3" style="color: var(--ink-soft);"><strong>Private markets and alternatives</strong> enter a portfolio only after independent diligence, only where the client's liquidity genuinely permits, and never with a product we're paid to place. <a class="textlink" href="insights/public-and-private-markets-what-advisors-wont-tell-you.html">What advisors won't tell you about private markets →</a></p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-5-7">
      <div class="reveal">
        <span class="label">2 — The Process</span>
        <h2>Four stages. No shortcuts.</h2>
      </div>
      <div class="steps reveal">
        <div class="step"><h3>Understand</h3><p>Your balance sheet, tax picture, obligations, and what the money is actually for. We don't recommend anything in the first meeting — we can't, honestly.</p></div>
        <div class="step"><h3>Customize</h3><p>A written portfolio design and plan built for you — asset allocation, tax placement, income plan, and the reasoning behind each choice, in plain English.</p></div>
        <div class="step"><h3>Implement</h3><p>Staged and tax-aware. Existing positions with embedded gains are transitioned deliberately, not liquidated on day one.</p></div>
        <div class="step"><h3>Monitor</h3><p>Continuous oversight with disciplined rebalancing bands — so changes happen when positioning drifts, not when headlines shout.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-5-7">
      <div class="reveal">
        <span class="label">3 — Principles</span>
        <h2>Cycles are survived, not predicted.</h2>
        <p class="mt-3" style="color: var(--ink-soft);">Markets and economies move in cycles that are obvious in hindsight and unknowable in advance. We don't position portfolios on forecasts. We position them so that no single environment — inflation, recession, a credit crunch — can do permanent damage.</p>
        <p class="mt-3" style="color: var(--ink-soft);">The discipline that makes this work is unglamorous: rebalancing into weakness, harvesting losses when they appear, and declining to act on excitement. Founded in 2008, this firm learned that lesson in its first year of existence.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-5-7">
      <div class="reveal">
        <span class="label">4 — Transparency</span>
        <h2>You can verify everything. That's the point.</h2>
      </div>
      <div class="reveal">
        <p style="color: var(--ink-soft);">Client assets are custodied at <strong>Fidelity Investments' institutional platform</strong> — held in your name, visible to you daily, movable only where you direct.</p>
        <p class="mt-3" style="color: var(--ink-soft);">Reporting runs on <strong>Black Diamond</strong>, the institutional reporting platform, with a client portal showing positions, performance, and fees. The firm maintains <strong>GIPS® compliance</strong> — the institutional standard for how investment results are calculated and presented.</p>
      </div>
    </div>
  </section>
{CTA_BAND}""")

# ---------------- TEAM ----------------
PAGES["team.html"] = ("Our Team", "Rui Guo, CFA and Adam Falcon, CFA, JD — the principals of Princeton Asset Management, an independent fiduciary founded in 2008.", f"""
  <section class="page-hero">
    <div class="wrap">
      <span class="label">Our Team</span>
      <h1>The people you meet are the people who manage your money.</h1>
      <p class="lede">No handoffs, no relationship managers, no call center. Two principals — both CFA® Charterholders — who built the firm in 2008 and still answer the phone.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-2">
      <div class="card reveal">
        <div class="photo-ph" style="min-height: 300px;" role="img" aria-label="Placeholder for Rui Guo photograph">Professional photo — unified color grade with Adam's so the two read as one system.</div>
        <h3 class="mt-3">Rui Guo, CFA</h3>
        <p class="card-kicker">Founder</p>
        <p>Rui founded Princeton Asset Management in 2008 with a conviction the industry still resists: that families deserve institutional-quality credit research without institutional conflicts of interest. Trained at the University of Chicago Booth School of Business, she leads the firm's investment strategy and its fixed income and credit specialization.</p>
      </div>
      <div class="card reveal">
        <div class="photo-ph" style="min-height: 300px;" role="img" aria-label="Placeholder for Adam Falcon photograph">Professional photo — unified color grade with Rui's so the two read as one system.</div>
        <h3 class="mt-3">Adam Falcon, CFA, JD</h3>
        <p class="card-kicker">Chief Investment Officer</p>
        <p>Adam brings the uncommon combination of a law degree and the CFA charter to portfolio oversight — credit analysis with a lawyer's eye for what's actually in the covenants. He directs portfolio construction, risk management, and the firm's research process.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-5-7">
      <div class="reveal">
        <span class="label">Since 2008</span>
        <h2>A boutique by conviction, not by circumstance.</h2>
      </div>
      <div class="reveal">
        <p style="color: var(--ink-soft);">Princeton Asset Management is a women- and minority-owned investment firm founded in Boca Raton, Florida in 2008 — the year that tested every assumption the industry held. The firms that survived it either got bigger or got better. We chose better: a deliberately limited client base, custom portfolios, and a fiduciary standard in every engagement.</p>
        <p class="mt-3" style="color: var(--ink-soft);">Behind the two principals sits an institutional infrastructure most boutiques can't offer: Fidelity institutional custody, Black Diamond reporting, GIPS® compliance, and a network of vetted specialists — estate attorneys, CPAs, insurance analysts — coordinated on your behalf, paid nothing by us and owing us nothing.</p>
      </div>
    </div>
  </section>
{CTA_BAND}""")

# ---------------- FEES ----------------
PAGES["fees.html"] = ("Fees & Fiduciary Standard", "One transparent fee, no commissions, no products. What Princeton Asset Management charges, how we're paid, and what fiduciary actually means.", f"""
  <section class="page-hero">
    <div class="wrap">
      <span class="label">Fees &amp; Fiduciary Standard</span>
      <h1>The page most firms hope you won't ask about.</h1>
      <p class="lede">We charge a single, transparent fee: a percentage of the assets we manage for you. It declines as assets grow. No commissions, no product markups, no hidden charges — and because we sell no annuities, insurance, or proprietary products, our fee is the only way we're paid.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <dl>
        <div class="fact-row reveal">
          <dt>What "fiduciary" means</dt>
          <dd>A fiduciary is legally required to put your interests ahead of the firm's — on every account, every recommendation, at all times. We are fiduciaries in every engagement, and we'll confirm it in writing.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>How you'll see the fee</dt>
          <dd>Plainly, in your agreement, and on every statement. You'll never need to reverse-engineer what you're paying from a prospectus footnote.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>What we will never charge you</dt>
          <dd>Commissions. Product markups. Revenue sharing. 12b-1 fees. Placement fees from fund sponsors. Surrender charges. If a product pays the advisor, we don't sell it — full stop.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>What the fee covers</dt>
          <dd>Portfolio management across public and private markets, the planning work — retirement income, tax coordination, estate structure review — and direct access to the principals. One fee, the whole engagement.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>Why we publish this page</dt>
          <dd>Because hiding fees is the number-one reason wealthy families silently disqualify advisory firms. If our structure doesn't make sense for your situation, we'd rather you know in fifteen minutes than after three meetings.</dd>
        </div>
      </dl>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="reveal"><span class="label">The Comparison Worth Making</span>
      <h2 style="max-width: 22ch;">Ask any firm these questions. Including us.</h2></div>
      <div class="table-scroll mt-6 reveal">
        <table class="compare-table">
          <thead><tr><th scope="col">Question</th><th scope="col">Typical brokerage answer</th><th scope="col">Princeton Asset Management</th></tr></thead>
          <tbody>
            <tr><td>Fiduciary at all times, in writing?</td><td>"It depends on the account."</td><td>Yes — every account, every recommendation, in writing.</td></tr>
            <tr><td>How are you paid?</td><td>Fees plus commissions, revenue sharing, product payments.</td><td>One fee, paid only by you. Nothing else, from anyone.</td></tr>
            <tr><td>Who holds my assets?</td><td>Often the firm's own platform.</td><td>Fidelity Investments — independent custody, in your name.</td></tr>
            <tr><td>Who manages my portfolio?</td><td>A model, a call center, or "the team."</td><td>The firm's principals — both CFA® Charterholders.</td></tr>
            <tr><td>Will you sell me insurance or annuities?</td><td>Frequently.</td><td>Never. We hold no insurance licenses on purpose.</td></tr>
          </tbody>
        </table>
      </div>
      <p class="mt-4 reveal"><a class="textlink" href="insights/5-questions-advisor-over-1-million.html">The full five questions to ask any advisor →</a></p>
    </div>
  </section>
{CTA_BAND}""")

# ---------------- SCHEDULE ----------------
PAGES["schedule.html"] = ("Schedule a Call", "Schedule a complimentary 15-minute wealth diagnostic with Princeton Asset Management — no obligation, and you'll leave with something actionable either way.", """
  <section class="page-hero">
    <div class="wrap">
      <span class="label">Schedule a Call</span>
      <h1>Fifteen minutes. Something actionable either way.</h1>
      <p class="lede">The complimentary wealth diagnostic is a short call, not a sales meeting. You talk, we listen, and you leave with our honest read — including "you're in good shape" if that's the truth.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid grid-7-5">
      <div class="reveal">
        <!-- SCHEDULER EMBED: replace this block with the Calendly / Squarespace Scheduling embed.
             Blueprint addendum open item #4 — either tool works; native integrates cleaner. -->
        <div class="photo-ph" style="min-height: 480px;" role="img" aria-label="Scheduler placeholder">
          Scheduler embed goes here (Calendly or Squarespace Scheduling).<br>
          Real availability · booking takes under 60 seconds.
        </div>
      </div>
      <div class="reveal">
        <span class="label">What to Expect</span>
        <ul style="list-style: none; display: flex; flex-direction: column; gap: 22px;">
          <li><strong>You talk first.</strong> Your situation, your questions, what prompted the call. No forms to fill out beforehand.</li>
          <li><strong>We give you our honest read.</strong> The two or three decisions likely to matter most in your position — whether or not they involve us.</li>
          <li><strong>Nothing to buy, no follow-up pressure.</strong> If there's a fit, we'll describe the next step. If not, we'll say that plainly.</li>
        </ul>
        <div class="mt-6">
          <span class="label">Prefer Direct?</span>
          <p style="color: var(--ink-soft);">
            <a class="textlink" href="tel:+15618004100">561-800-4100</a><br>
            <a class="textlink" href="mailto:clientservices@princetonam.com">clientservices@princetonam.com</a><br><br>
            One Park Place<br>621 NW 53rd St., Ste 240<br>Boca Raton, FL 33487
          </p>
        </div>
      </div>
    </div>
  </section>""")

# ---------------- INSTITUTIONAL ----------------
PAGES["institutional.html"] = ("Institutional", "Princeton Asset Management manages fixed income and credit strategies for foundations, trusts, and institutional allocators. Women- and minority-owned, GIPS compliant, founded 2008.", f"""
  <section class="page-hero">
    <div class="wrap">
      <span class="label">Institutional</span>
      <h1>Fixed income and credit, managed with conviction.</h1>
      <p class="lede">Princeton Asset Management is a women- and minority-owned investment firm managing fixed income and credit strategies for foundations, trusts, family offices, and institutional allocators since 2008.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <dl>
        <div class="fact-row reveal">
          <dt>Princeton Opportunistic Credit Strategy</dt>
          <dd>An actively managed credit strategy built on direct, security-level research — identifying credits where the market's price and the covenant reality disagree. Strategy materials and composite presentations are available to qualified allocators on request.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>Core fixed income</dt>
          <dd>Customized investment-grade portfolios managed against client-specific objectives — liability schedules, income targets, or policy benchmarks — rather than one-size-fits-all duration.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>Standards</dt>
          <dd>Firm-wide GIPS® compliance. Composite performance, Form ADV, and due-diligence materials provided to qualified institutions on request. Principals are CFA® Charterholders, University of Chicago Booth-trained.</dd>
        </div>
        <div class="fact-row reveal">
          <dt>Diverse-manager mandates</dt>
          <dd>As a women- and minority-owned firm with an eighteen-year operating history, we welcome inquiries from allocators with emerging- and diverse-manager programs.</dd>
        </div>
      </dl>
      <p class="mt-6 reveal">Allocator inquiries: <a class="textlink" href="mailto:clientservices@princetonam.com">clientservices@princetonam.com</a> · <a class="textlink" href="tel:+15618004100">561-800-4100</a></p>
    </div>
  </section>""")

for fname, (title, desc, main) in PAGES.items():
    (ROOT / fname).write_text(shell(fname, title, desc, main), encoding="utf-8")
    print("built", fname)
print("done:", len(PAGES), "pages")

"""Builds the site's HTML pages from shared pieces (head, header, footer, concept panel).

Edit the page bodies or shared pieces here, then run:  python3 scripts/build.py
Output is plain static HTML in the repo root, so Cloudflare Pages needs no build step.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGO = "d6231e_9077a0dc3d96405ca1bae4d9ad1a346c~mv2.png"

NAV = [
    ("index.html", "Home"),
    ("flavors.html", "Flavors"),
    ("pop-ups.html", "Pop-ups"),
    ("our-story.html", "Our story"),
    ("experiences.html", "Experiences"),
    ("locations.html", "Locations"),
]


SITE = "https://cloudy-donut.pages.dev"

def head(title, desc, fname="index.html"):
    slug = fname[:-5]
    url = SITE + ("/" if slug == "index" else "/" + slug)
    og = f"{SITE}/og/{slug}.jpg"
    full = "Cloudy Donut Co." if slug == "index" else f"{title} | Cloudy Donut Co."
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#141312">
  <title>{title} | Cloudy Donut Co. Concept by Siani Creates</title>
  <meta name="description" content="{desc}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Cloudy Donut Co.">
  <meta property="og:title" content="{full}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Cloudy Donut Co. logo with Donut stop believing! and Where Dreams Crumb True">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{full}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Caudex:ital,wght@0,400;0,700;1,400;1,700&family=Figtree:wght@400;500;700;800;900&family=Montserrat:wght@800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>"""


# Splash: line-drawn clouds in the style of the Cloudy logo. Small clouds drift; the
# hero cloud draws itself, the donut lands in its top-right bump, then the real logo resolves.

_dsb_n = [0]
def dsb(extra=""):
    """Their box and window lockup: DONUT stop BELIEVING!, with a donut for the O."""
    _dsb_n[0] += 1
    m = f"dsbm{_dsb_n[0]}"
    sprinkles = "".join(f'<path d="{d}"/>' for d in ["M30 26l6 3", "M52 18l1 7", "M70 27l-5 4", "M80 47l-7 1", "M72 70l-4-5", "M50 82l1-7", "M28 72l5-4", "M20 50l7 1"])
    o = (f'<span class="dsb-o" aria-hidden="true"><svg viewBox="0 0 100 100"><defs><mask id="{m}"><rect width="100" height="100" fill="#fff"/>'
         f'<circle cx="50" cy="50" r="15" fill="#000"/><g stroke="#000" stroke-width="5" stroke-linecap="round">{sprinkles}</g></mask></defs>'
         f'<circle cx="50" cy="50" r="48" fill="currentColor" mask="url(#{m})"/></svg></span>')
    return (f'<span class="dsb{extra}" role="img" aria-label="Donut stop believing!"><span class="dsb-l1" aria-hidden="true"><span>D</span>{o}<span>NUT</span>'
            f'<span class="dsb-stop">STOP</span></span><span class="dsb-l2" aria-hidden="true">BELIEVING!</span></span>')

CLOUD_SMALL = "M18 70 C4 70 2 50 20 47 C18 33 34 25 48 33 C54 15 82 10 94 27 C104 13 128 15 132 33 C146 31 156 44 150 56 C162 58 162 70 150 70 Z"
SVG_DEFS = f"""
<script>try{{if(sessionStorage.getItem("cd-intro")==="1"||matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("intro-seen")}}catch(e){{}}</script>
<div class="intro" id="intro" aria-hidden="true">
  <svg class="drift" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">
    <defs><path id="cl" d="{CLOUD_SMALL}"/></defs>
    <g class="dc d1"><use href="#cl" transform="translate(120 140) scale(1.5)"/></g>
    <g class="dc d2"><use href="#cl" transform="translate(1180 110) scale(1.15)"/></g>
    <g class="dc d3"><use href="#cl" transform="translate(1290 600) scale(1.7)"/></g>
    <g class="dc d4"><use href="#cl" transform="translate(180 640) scale(1.05)"/></g>
    <g class="dc d5"><use href="#cl" transform="translate(760 760) scale(.8)"/></g>
    <g class="dc d6"><use href="#cl" transform="translate(640 60) scale(.7)"/></g>
  </svg>
  <div class="intro-mark">
    <div class="mark-wrap">
      <!-- The real logo, revealed by a pen that traces its own cloud outline, then the lettering fills in -->
      <svg class="trace" viewBox="0 0 1200 581" aria-hidden="true">
        <defs>
          <filter id="logo-white"><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0"/></filter>
          <mask id="logo-pen" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="581">
            <path d="M 245 553 L 30 553 C 0 553 -5 470 40 445 C 70 405 140 400 160 400 L 165 340 C 170 300 200 310 250 305 C 245 250 290 175 380 170 C 420 168 450 175 470 180 C 490 160 510 140 540 130 C 590 50 650 5 760 3 C 860 0 930 60 960 110 C 990 160 990 230 990 310 C 1060 300 1130 330 1165 400 C 1195 460 1190 520 1185 565" fill="none" stroke="#fff" stroke-width="74" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1">
              <animate attributeName="stroke-dashoffset" from="1" to="0" begin=".3s" dur="1.35s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".55 .05 .3 1"/>
            </path>
            <rect width="1200" height="581" fill="#fff" opacity="0">
              <animate attributeName="opacity" from="0" to="1" begin="1.5s" dur=".5s" fill="freeze"/>
            </rect>
          </mask>
        </defs>
        <image href="https://static.wixstatic.com/media/{LOGO}/v1/fit/w_900,h_900,q_90,enc_auto/{LOGO}" width="1200" height="581" filter="url(#logo-white)" mask="url(#logo-pen)"/>
      </svg>
    </div>
    <div class="intro-dsb">{dsb()}<p class="intro-line">Where Dreams Crumb True</p></div>
  </div>
  <button class="intro-skip" type="button">Skip</button>
</div>
"""


def header(active, overlay):
    links = "\n    ".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>' for href, label in NAV[1:]
    )
    return f"""
<div class="grain" aria-hidden="true"></div>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header{' overlay' if overlay else ''}" id="top">
  <a class="brand" href="index.html" aria-label="Cloudy Donut Co. home">
    <img class="wix" data-wix="{LOGO}" data-w="320" alt="Cloudy Donut Co.">
  </a>
  <button class="search-open search-mobile" type="button" aria-label="Search the site" aria-haspopup="dialog"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav"><span></span><span></span><span class="visually-hidden">Menu</span></button>
  <nav id="nav" class="nav" aria-label="Main">
    {links}
    <button class="search-open" type="button" aria-label="Search the site" aria-haspopup="dialog"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg><span class="search-label">Search</span></button>
    <a class="btn btn-mint btn-small" href="locations.html" data-order>Order ahead</a>
  </nav>
</header>
"""


FOOTER = f"""
<footer class="site-footer">
  <div class="wrap foot">
    <img class="wix logo-cream foot-logo" data-wix="{LOGO}" data-w="400" alt="Cloudy Donut Co.">
    <p class="foot-tag">Where Dreams Crumb True</p>
    <nav class="foot-links" aria-label="Footer">
      {"".join(f'<a href="{h}">{l}</a>' for h, l in NAV[1:])}
    </nav>
    <div class="foot-links foot-social">
      <a href="https://www.instagram.com/cloudydonuts/" target="_blank" rel="noopener">Instagram</a>
      <a href="https://www.facebook.com/CloudyDonutCo" target="_blank" rel="noopener">Facebook</a>
      <a href="https://www.thesevenstreams.com" target="_blank" rel="noopener">7Streams</a>
      <a href="tel:+13474639628">347.463.9628</a>
      <a href="mailto:info@cloudydonut.com">info@cloudydonut.com</a>
    </div>
    <p class="concept-line">Concept site prepared by Siani Creates for Cloudy Donut Co. Not the official website. Content, logo and photos belong to Cloudy Donut Co.</p>
  </div>
</footer>

__BTS__

<dialog class="terms-dlg" id="terms-dlg" aria-labelledby="terms-h">
  <h2 id="terms-h">Email terms</h2>
  <ul>
    <li>The weekly flavor lineup, pop-up dates and the occasional note from Cloudy Donut Co., about once a week.</li>
    <li>Your email, and your city or state if you add one, is used only to send these emails. It's never sold or shared.</li>
    <li>Every email has an unsubscribe link. You can also write to <a href="mailto:info@cloudydonut.com">info@cloudydonut.com</a>.</li>
  </ul>
  <p class="fine">Draft for Cloudy Donut Co. to confirm before launch.</p>
  <form method="dialog"><button class="btn btn-ink" type="submit">Got it</button></form>
</dialog>

<dialog class="ig-dlg" id="ig-dlg" aria-label="Instagram post">
  <div class="ig-dlg-bar"><a id="ig-dlg-open" href="https://www.instagram.com/cloudydonuts/" target="_blank" rel="noopener">Open on Instagram</a><button type="button" class="ig-dlg-x" aria-label="Close">×</button></div>
  <div class="ig-dlg-body" id="ig-dlg-body"></div>
</dialog>

<dialog class="search-dialog" id="search-dialog" aria-label="Search Cloudy Donut">
  <div class="search-box">
    <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>
    <input id="site-search" type="search" aria-label="Search flavors, shops and pop-ups" placeholder="Search Cloudy" autocomplete="off" role="combobox" aria-expanded="true" aria-controls="search-results" aria-autocomplete="list">
    <button class="search-close" type="button">Esc</button>
  </div>
  <div class="search-results" id="search-results" role="listbox" aria-label="Results"></div>
  <button class="sr-more" id="sr-more" type="button" tabindex="-1" aria-hidden="true" hidden><svg viewBox="0 0 24 24" width="18" height="18"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg><span>More</span></button>
</dialog>

<svg class="defs" aria-hidden="true" focusable="false">
  <filter id="crinkle" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".008 .014" numOctaves="4" seed="21" result="n"/>
    <feDiffuseLighting in="n" lighting-color="#fff" surfaceScale="2.4" result="l"><feDistantLight azimuth="225" elevation="60"/></feDiffuseLighting>
    <feColorMatrix in="l" type="matrix" values="0 0 0 0 .3  0 0 0 0 .27  0 0 0 0 .2  -1.6 0 0 0 1.32"/>
  </filter>
</svg>
<dialog class="paper-dialog" id="flavor-dialog" aria-labelledby="fd-name">
  <div class="sheet" id="fd-sheet">
    <div class="paper" id="fd-paper">
      <div class="pp-tone" aria-hidden="true"></div>
      <div class="pp-print" id="fd-print" aria-hidden="true"></div>
      <div class="pp-crinkle" aria-hidden="true"></div>
      <div class="pp-crease c1" aria-hidden="true"></div><div class="pp-crease c2" aria-hidden="true"></div><div class="pp-crease c3" aria-hidden="true"></div><div class="pp-crease c4" aria-hidden="true"></div>
      <div class="pp-sheen" aria-hidden="true"></div>
      <form method="dialog"><button class="pp-close" aria-label="Close">×</button></form>
      <p class="pp-sticker" id="fd-badge" hidden><span>On this week's<br>lineup</span></p>
      <div class="pp-donut"><img id="fd-img" alt=""></div>
      <div class="pp-text">
        <h3 id="fd-name"></h3>
        <p class="pp-desc" id="fd-desc"></p>
        <p class="pp-contains" id="fd-contains"></p>
      </div>
    </div>
  </div>
</dialog>

<script src="data/fallback.js" defer></script>
<script src="app.js" defer></script>
</body>
</html>
"""


def page_hero(kicker, title, sub, img=None, cta=""):
    photo = f'<img class="wix ph-photo" data-wix="{img}" data-w="1600" alt="">' if img else ""
    return f"""
  <section class="page-hero{' has-photo' if img else ''}">
    {photo}
    <div class="wrap">
      <p class="kicker">{kicker}</p>
      <h1 class="display-lg">{title}</h1>
      {f'<p class="page-sub">{sub}</p>' if sub else ''}
      {cta}
    </div>
  </section>"""


# ---------- Reusable sections ----------

LINEUP = """
  <section class="cream lineup" id="lineup" aria-labelledby="lineup-h">
    <div class="wrap">
      <div class="head-row">
        <div>
          <p class="kicker dark">Fri · Sat · Sun</p>
          <h2 class="display-md" id="lineup-h">This Week's Lineup</h2>
        </div>
        <p class="head-note" id="lineup-sub">Six to eight flavors a weekend, in small batches. When it's gone, it's gone until it rotates back.</p>
      </div>
      <div class="box-wrap">
        <div class="cbox" id="cbox" data-state="closed">
          <div class="cbox-stage">
            <div class="cbox-body" id="cbox-body" inert>
              <span class="wall w-back" aria-hidden="true"></span><span class="wall w-left" aria-hidden="true"></span><span class="wall w-right" aria-hidden="true"></span><span class="wall w-front" aria-hidden="true"></span>
              <div class="cbox-well">
                <div class="cbox-liner" aria-hidden="true"><div class="cbox-print" id="cbox-print"></div></div>
                <div class="donut-box" id="donut-box" role="tablist" aria-label="This week's flavors"></div>
              </div>
            </div>
            <div class="cbox-lid" aria-hidden="true">
              <div class="lid-face lid-out"><img class="wix lid-logo" data-wix="d6231e_9077a0dc3d96405ca1bae4d9ad1a346c~mv2.png" data-w="420" alt=""></div>
              <div class="lid-face lid-inn"><div class="lid-pat" id="lid-pat-in"></div><div class="lid-inn-mark"><img class="wix" data-wix="d6231e_9077a0dc3d96405ca1bae4d9ad1a346c~mv2.png" data-w="420" alt=""></div><span class="tuck" aria-hidden="true"></span></div>
            </div>
          </div>
          <div class="cbox-front"><span class="notch" aria-hidden="true"></span>__DSB__</div>
          <button class="seal" id="cbox-seal" type="button" aria-controls="cbox-body" aria-expanded="false"><span>Where<br>Dreams<br>Crumb<br>True</span><span class="visually-hidden">Open this week's box</span></button>
        </div>
        <div class="bd-wrap">
        <div class="bd-dots" id="bd-dots" role="group" aria-label="Flavors in this week's box" hidden></div>
        <div class="box-detail" id="box-detail" role="tabpanel" aria-live="polite">
          <p class="bd-num">8 flavors inside</p>
          <h3 class="bd-name">Tap The Seal.</h3>
          <p class="bd-desc">This week's box is packed and sealed. Break the seal to see what's inside.</p>
        </div>
        </div>
      </div>
      <div class="lineup-foot">
        <p class="lineup-also" id="lineup-also"></p>
        <div class="price-strip" id="price-strip" aria-label="Prices"></div>
      </div>
      <div class="lineup-actions">
        <form class="inline-signup light" data-form="newsletter" novalidate>
          <label for="nl-email">Get the lineup every week</label>
          <div class="inline-row">
            <input id="nl-email" name="email" type="email" autocomplete="email" placeholder="Email" required>
            <button class="btn btn-ink" type="submit">Subscribe</button>
          </div>
          <div class="consent"><input id="nl-consent" name="consent" type="checkbox" required><label for="nl-consent">I agree to the <button type="button" class="terms-link" data-terms>email terms</button></label></div>
          <p class="form-msg" role="status"></p>
        </form>
        __MORE__
      </div>
    </div>
  </section>""".replace("__DSB__", dsb())

FLYER = """
  <section class="popups" id="popups" aria-labelledby="popups-h">
    <div class="flyer" id="flyer">
      <div class="flyer-top"><span>Cloudy Donut</span><span>Presents</span></div>
      <h2 class="flyer-city" id="popups-h">On Tour</h2>
      <div class="flyer-bottom" id="flyer-bottom"></div>
      <p class="flyer-count" id="flyer-count" aria-live="polite"></p>
    </div>
    <div class="tour-side">
      <p class="kicker">The tour</p>
      <ol class="tour-list" id="tour-list"></ol>
      <p class="fine">Dates drop on Instagram first. Pop-ups sell out.</p>
      __TOURMORE__
    </div>
  </section>"""

TOUR_FORM = """
      <form class="inline-signup" data-form="tour_alert" novalidate>
        <label for="tour-email">Bring Cloudy to my city</label>
        <div class="inline-row">
          <input id="tour-email" name="email" type="email" autocomplete="email" placeholder="Email" required>
          <input name="city" type="text" autocomplete="address-level2" placeholder="City" aria-label="City" required>
          <button class="btn btn-mint" type="submit">Notify me</button>
        </div>
        <div class="consent"><input id="tour-consent" name="consent" type="checkbox" required><label for="tour-consent">I agree to the <button type="button" class="terms-link" data-terms>email terms</button></label></div>
        <p class="form-msg" role="status"></p>
      </form>"""

CAMPAIGN = """
  <section class="campaign" aria-label="Cloudy Donut campaign photos">
    <img class="wix" data-wix="d6231e_c4aef1bd70ef4c6490281833541a53d2~mv2.jpg" data-w="700" alt="A woman holding a stack of glazed donuts">
    <img class="wix" data-wix="d6231e_c435e945d8b64cdf875b33d92d335df8~mv2.jpg" data-w="700" alt="A toddler in overalls holding a Cookie Monster donut">
    <img class="wix" data-wix="d6231e_097b0864e2334f8bbd01dcdba05a012e~mv2.jpg" data-w="700" alt="A stack of chocolate donuts">
    <img class="wix" data-wix="d6231e_19d4b6ff15bc42a184856f8caf1816f4~mv2.jpg" data-w="700" alt="A child taking a bite of a sprinkled donut">
    <img class="wix" data-wix="d6231e_2ddfd7964b1f4e089573e576a08eb5e0~mv2.jpg" data-w="700" alt="A woman holding a donut up to her face">
  </section>"""

LOCATIONS = """
  <section class="cream locations" id="locations" aria-labelledby="loc-h">
    <div class="wrap">
      <div class="head-row">
        <div>
          <p class="kicker dark">Come early</p>
          <h2 class="display-md" id="loc-h">Where To Find Us</h2>
        </div>
        <p class="head-note">Weekends only, and the good ones go fast. Order ahead for pickup.</p>
      </div>
      <ul class="loc-grid" id="loc-grid" role="list"></ul>
    </div>
  </section>"""

# Their "Our Story" copy, verbatim from cloudydonut.com (Nov 2026).
STORY_COPY = """
        <p>Considered amongst many, as some of "the best pastries in the world," this gourmet vegan patisserie first made headlines with its strong social impact and outstanding products to back its mission, most famous for its pillowy soft cloud like donuts. Cloudy Donut Co. is a brand of many first, it is NYC's first 100% vegan donut store and the first Black Owned food and beverage business in Brooklyn Heights and Nolita.</p>
        <p>With over 50 flavors this outpost is a tourist haven known for its brown butter chocolate chip donuts, apple pie cinnamon rolls and sweet potato pound cake; for which all desserts are small-batched and hand crafted.</p>
        <p>Known for limited quantity with an emphasis on storytelling, beginning with the design of the spaces to the curation of the music, merchandise and weekly flavor profile; everything is created with intention.</p>
        <p>These experiences provide the consumer with a boutique feel, curated by Founder, Derrick Faulcon, along with Zewiditu Jewel, Leaders of The Brown Collective, which builds each space in a luxurious and harmonious way. Collectively, the two have created Worlds of Black luxury, which can only be told in a way that Black people themselves can articulate.</p>"""

FIRSTS = """
      <ul class="firsts" role="list">
        <li><span class="big">1st</span><span>100% vegan donut store in NYC</span></li>
        <li><span class="big">1st</span><span>Black Owned food and beverage business in Brooklyn Heights</span></li>
        <li><span class="big">1st</span><span>Black Owned food and beverage business in Nolita</span></li>
        <li><span class="big">50+</span><span>Flavors, small-batched and hand crafted</span></li>
      </ul>"""

PRESS = """
  <section class="press" aria-labelledby="press-h">
    <div class="wrap">
      <h2 class="kicker" id="press-h">As seen in</h2>
      <ul class="press-list" role="list">
        <li><a href="https://www.forbes.com/sites/chrissytracey/2026/08/31/how-cloudy-donuts-became-jay-zs-favorite-donut-shop/" target="_blank" rel="noopener"><span class="outlet">Forbes</span><span class="headline">How Cloudy Donuts Became Jay-Z's Favorite Donut Shop</span></a></li>
        <li><a href="https://www.okayplayer.com/cloudy-donut-brooklyn-heights" target="_blank" rel="noopener"><span class="outlet">Okayplayer</span><span class="headline">Cloudy With A Chance Of Progress</span></a></li>
        <li><a href="https://abc7ny.com/videoClip/15696668/" target="_blank" rel="noopener"><span class="outlet">ABC7 New York</span><span class="headline">Cloudy Donut is a ray of sunshine for creators of color</span></a></li>
        <li><a href="https://timeout.com/newyork/news/this-tiktok-famous-vegan-donut-company-just-opened-a-store-in-brooklyn-110122" target="_blank" rel="noopener"><span class="outlet">Time Out New York</span><span class="headline">This TikTok-famous vegan donut company just opened in Brooklyn</span></a></li>
        <li><a href="https://thegrio.com/2023/06/01/blackmade-derrick-faulcon-on-cloudy-donut-co-entrepreneurship/" target="_blank" rel="noopener"><span class="outlet">theGrio</span><span class="headline">BlackMade: Derrick Faulcon on Cloudy Donut Co.</span></a></li>
        <li><a href="https://blackenterprise.com/cloudy-donut-co-first-black-owned-business-in-brooklyn-heights-will-have-you-on-cloud-nine/" target="_blank" rel="noopener"><span class="outlet">Black Enterprise</span><span class="headline">First Black-owned business in Brooklyn Heights will have your tastebuds on cloud nine</span></a></li>
      </ul>
    </div>
  </section>"""

FAQ = """
  <section class="faq" id="faq" aria-labelledby="faq-h">
    <div class="wrap faq-wrap">
      <h2 class="display-md" id="faq-h">Good To Know</h2>
      <div class="faq-list">
        <details><summary>Where are you all located?</summary><p>We have two shops in NYC: 14 Columbia Pl., Brooklyn, NY 11201 and 209 Mott Street, New York, NY 10012. Our Lauraville home in Baltimore hosts pop-ups. See <a href="locations.html">hours and maps</a>.</p></details>
        <details><summary>What oils are your donuts made in?</summary><p>All our donuts are fried in liquid vegetable shortening.</p></details>
        <details><summary>What substitutes do you use to make the donuts vegan?</summary><p>Applesauce, coconut milk and shortening are used in place of animal products.</p></details>
        <details><summary>Are your donuts gluten free?</summary><p>Our donuts are 100% vegan, but they are not gluten free.</p></details>
        <details><summary>Which donuts have nuts in them?</summary><p>Some of our donuts contain nuts. Every flavor with nuts is marked on the <a href="flavors.html?filter=nutfree">flavors page</a>, and you can filter to nut-free flavors.</p></details>
        <details><summary>How long can I store the donuts for?</summary><p>Our donuts do not contain preservatives, so we do not recommend holding them longer than 13 hours at room temperature. Our cinnamon rolls and pound cakes have a shelf life of 2–3 days.</p></details>
        <details><summary>What happens if I place a preorder and forget to pick it up?</summary><p>Contact the company where you placed your order, like DoorDash or Grubhub, to sort it out. If you ordered directly from us, give us a call at <a href="tel:+13474639628">347.463.9628</a> and we will do our best to accommodate you.</p></details>
        <details><summary>Do you cater or do large orders?</summary><p>Yes. Tell us about your event on the <a href="experiences.html">Experiences page</a>, or call <a href="tel:+13474639628">347.463.9628</a> to place a large order.</p></details>
        <details><summary>Do you all do custom or special order donuts?</summary><p>We have special holiday and occasion packages, but we do not make custom order donuts at this time.</p></details>
        <details><summary>Do you all ship?</summary><p>Due to the short shelf life of our vegan donuts, we do not ship them. Pound cakes are coming next year, and the <a href="experiences.html#ship">waitlist</a> hears first.</p></details>
        <details><summary>Do you all wholesale the donuts?</summary><p>We do not wholesale our donuts at this time, but call <a href="tel:+13474639628">347.463.9628</a> to learn how we can help with your program or event.</p></details>
        <details><summary>Do you sell gift cards?</summary><p>Gift cards are available in store at our Brooklyn Heights location.</p></details>
        <details><summary>Do you all sell merchandise?</summary><p>Call <a href="tel:+13474639628">347.463.9628</a> or DM <a href="https://www.instagram.com/cloudydonuts/" target="_blank" rel="noopener">@cloudydonuts</a> to ask what merch is in stock.</p></details>
        <details><summary>How can I apply for a job?</summary><p>Email us at <a href="mailto:info@cloudydonut.com">info@cloudydonut.com</a>. We are always open to new talent with an interest in baking.</p></details>
        <details><summary>Something for the dog?</summary><p>Yes. Lil Bow Wow and the Snoop Doggy Donut are <a href="flavors.html?filter=pups">made for pups</a>.</p></details>
      </div>
    </div>
  </section>"""

CATERING_FORM = """
      <form class="cat-form" data-form="catering" novalidate>
        <div class="row2">
          <label>First name<input name="first_name" autocomplete="given-name" required></label>
          <label>Last name<input name="last_name" autocomplete="family-name" required></label>
        </div>
        <div class="row2">
          <label>Email<input name="email" type="email" autocomplete="email" required></label>
          <label>Phone<input name="phone" type="tel" autocomplete="tel"></label>
        </div>
        <div class="row2">
          <label>Date of event<input name="event_date" type="date" required id="event-date"></label>
          <label>Time<input name="event_time" type="time"></label>
        </div>
        <fieldset class="seg">
          <legend>Pick up or delivery</legend>
          <label><input type="radio" name="fulfillment" value="Pick up" checked> Pick up</label>
          <label><input type="radio" name="fulfillment" value="Delivery"> Delivery</label>
        </fieldset>
        <label>Event address<input name="address" autocomplete="street-address" placeholder="Street, city, state, zip"></label>
        <label>Setup
          <select name="package" required>
            <option value="">Choose one</option>
            <option>Minis, passed</option>
            <option>Minis, display</option>
            <option>Not sure yet</option>
          </select>
        </label>
        <label>Dietary restrictions<input name="dietary" placeholder="Nut allergies, etc."></label>
        <label>Tell us about it<textarea name="notes" rows="3" placeholder="Guest count, the occasion, flavors you love"></textarea></label>
        <button class="btn btn-mint" type="submit">Send request</button>
        <p class="form-msg" role="status"></p>
      </form>"""

SHIP = """
  <section class="ship" id="ship" aria-labelledby="ship-h">
    <div class="wrap ship-card">
      <div>
        <p class="kicker dark">Coming next year</p>
        <h2 class="display-md" id="ship-h">Cloudy, Shipped.</h2>
        <p>Donuts are best within hours, so they stay in the shop. Pound cakes keep for days, and they're the first thing we'll ship. The waitlist hears first.</p>
      </div>
      <form class="stack-form" data-form="ship_waitlist" novalidate>
        <label>Email<input name="email" type="email" autocomplete="email" required></label>
        <label>State<input name="state" type="text" autocomplete="address-level1" required></label>
        <div class="consent"><input id="ship-consent" name="consent" type="checkbox" required><label for="ship-consent">I agree to the <button type="button" class="terms-link" data-terms>email terms</button></label></div>
        <button class="btn btn-ink" type="submit">Join the waitlist</button>
        <p class="form-msg" role="status"></p>
      </form>
    </div>
  </section>"""

# ---------- Pages ----------

HOME = f"""
<main id="main">
  <section class="hero-c">
    <div class="collage" aria-hidden="true">
      <img class="wix donut c1" data-wix="d6231e_39a567b0401142f38f3bb70722d23bd7~mv2.png" data-w="520" alt="">
      <img class="wix donut c2" data-wix="d6231e_878a5cb4cd0040ee9b069858b056b9ce~mv2.png" data-w="520" alt="">
      <img class="wix donut c3" data-wix="d6231e_48a7f829a25342a3b7de68e11918e842~mv2.png" data-w="520" alt="">
      <img class="wix donut c4" data-wix="d6231e_0e703767089a4b95ac748491648171fb~mv2.png" data-w="520" alt="">
      <img class="wix donut c5" data-wix="d6231e_b202da8be46549e2a211a2375810af61~mv2.png" data-w="520" alt="">
      <img class="wix donut c6" data-wix="d6231e_2e57026f214c4280912f3a4219fbfcdc~mv2.png" data-w="520" alt="">
      <img class="wix donut c7" data-wix="d6231e_2798173fb08a42d5bb2fd8f6fce66871~mv2.png" data-w="520" alt="">
      <img class="wix donut c8" data-wix="d6231e_f4941503cbda409ab0b4afdcdd330e17~mv2.png" data-w="520" alt="">
      <img class="wix donut c9" data-wix="d6231e_6d8ec40113d84019ac84756b68370d22~mv2.png" data-w="520" alt="">
    </div>
    <div class="hero-card">
      <p class="kicker dark">Luxury Dessert Experiences</p>
      <h1 class="display">Where Dreams<br>Crumb True.</h1>
      <p class="hero-sub">100% vegan. Small batch. Hand crafted in Brooklyn Heights, NoLita and Baltimore, and on the road.</p>
      <div class="hero-actions">
        <a class="btn btn-ink" href="#lineup">This week's lineup</a>
        <a class="btn btn-line-ink" href="pop-ups.html" id="hero-popup">Pop-up tour</a>
      </div>
      <p class="open-now" id="hero-status" aria-live="polite"></p>
    </div>
  </section>

  <section class="tiles" aria-label="Explore">
    <a class="tile tile-mint" href="flavors.html"><span class="ring" aria-hidden="true"></span><span class="tile-k">100%</span><span class="tile-t">Vegan</span><span class="tile-go">Our flavors →</span></a>
    <a class="tile tile-char" href="pop-ups.html"><span class="ring" aria-hidden="true"></span><span class="tile-k">On</span><span class="tile-t">Tour</span><span class="tile-go">Pop-ups →</span></a>
    <a class="tile tile-photo" href="experiences.html"><img class="wix" data-wix="d6231e_53d7df9586bb4bcfa7d31a527d4cfe90~mv2.jpg" data-w="900" alt="A box of assorted Cloudy donuts"><span class="tile-k">Luxury</span><span class="tile-t">Experiences</span><span class="tile-go">Catering &amp; events →</span></a>
  </section>

  <div class="marquee" aria-hidden="true"><div class="marquee-track" id="marquee"></div></div>
{LINEUP.replace("__MORE__", '<div class="more-links"><a class="link-arrow" href="flavors.html#picker">Not sure? Find your flavor</a><a class="link-arrow" href="flavors.html">See all 40+ flavors</a></div>')}
{CAMPAIGN}
{FLYER.replace("__TOURMORE__", '<a class="btn btn-line" href="pop-ups.html">Full tour</a>')}

  <section class="story-teaser" aria-labelledby="st-h">
    <div class="wrap st-grid">
      <div>
        <p class="kicker">Our story</p>
        <h2 class="display-md" id="st-h">Everything Is Created With Intention.</h2>
      </div>
      <div>
        <p class="st-lede">Cloudy Donut Co. is a brand of many first, it is NYC's first 100% vegan donut store and the first Black Owned food and beverage business in Brooklyn Heights and Nolita.</p>
        <a class="btn btn-line" href="our-story.html">Read our story</a>
      </div>
    </div>
  </section>

  <section class="exp-teaser" aria-labelledby="et-h">
    <div class="wrap et-grid">
      <img class="wix et-photo" data-wix="d6231e_de85e764a62b4080bf6cb8aab7b5ee25~mv2.png" data-w="600" alt="Raspberry Rosé donuts">
      <div>
        <p class="kicker dark">Luxury dessert experiences</p>
        <h2 class="display-md" id="et-h">Bring Cloudy To The Party.</h2>
        <p>Cloudy Donut Minis, passed on trays or styled as a display, with the flavors you pick.</p>
        <a class="btn btn-ink" href="experiences.html">Plan an experience</a>
      </div>
    </div>
  </section>
{LOCATIONS}
</main>"""

FLAVORS = f"""
<main id="main">
{page_hero("The full rotation", "Every Flavor<br>We Make.", "Six to eight of these hit the case each weekend. All 100% vegan, small-batched and hand crafted. Tap a donut for the details and allergens.", "d6231e_53d7df9586bb4bcfa7d31a527d4cfe90~mv2.jpg", cta='<div class="hero-cta"><a class="btn btn-mint" href="#picker">Find your flavor <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M12 4v15m-6-6 6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a><span>Four questions, three donuts.</span></div>')}
  <section class="cream flavors" id="flavors" aria-label="Flavor library">
    <div class="wrap">
      <div class="flavor-tools">
        <div class="chips" role="group" aria-label="Filter flavors" id="chips"></div>
        <label class="search">
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
          <span class="visually-hidden">Search flavors</span>
          <input type="search" id="flavor-search" placeholder="Find a flavor">
        </label>
      </div>
      <div class="flavor-meta">
        <p class="flavor-count" id="flavor-count" aria-live="polite"></p>
        <div class="price-strip" id="price-strip" aria-label="Prices"></div>
      </div>
      <ul class="flavor-grid" id="flavor-grid" role="list"></ul>
      <p class="fine">Every donut is 100% vegan. They are not gluten free.</p>
    </div>
  </section>
  <section class="picker" id="picker" aria-labelledby="picker-h">
    <div class="wrap picker-grid">
      <div>
        <p class="kicker dark">Not sure?</p>
        <h2 class="display-md" id="picker-h">Find Your Flavor.</h2>
        <p class="picker-sub">Tell us your mood and we'll pull three for you.</p>
      </div>
      <div class="picker-qs">
        <div class="pq" role="group" aria-label="Flavor mood">
          <span class="pq-label">I'm in the mood for</span>
          <div class="pq-opts"><button type="button" data-pick="mood:fruity" aria-pressed="false">Fruity</button><button type="button" data-pick="mood:rich" aria-pressed="false">Rich</button><button type="button" data-pick="mood:spiced" aria-pressed="false">Spiced</button><button type="button" data-pick="mood:fresh" aria-pressed="false">Zesty</button></div>
        </div>
        <div class="pq" role="group" aria-label="Style">
          <span class="pq-label">Done up</span>
          <div class="pq-opts"><button type="button" data-pick="style:any" aria-pressed="true">Any way</button><button type="button" data-pick="style:glazed" aria-pressed="false">Glazed</button><button type="button" data-pick="style:sugar" aria-pressed="false">Sugar-tossed</button><button type="button" data-pick="style:filled" aria-pressed="false">Filled</button></div>
        </div>
        <div class="pq" role="group" aria-label="Texture">
          <span class="pq-label">On top</span>
          <div class="pq-opts"><button type="button" data-pick="texture:any" aria-pressed="true">Either</button><button type="button" data-pick="texture:crunchy" aria-pressed="false">Crunch</button><button type="button" data-pick="texture:smooth" aria-pressed="false">Smooth</button></div>
        </div>
        <div class="pq" role="group" aria-label="Booze">
          <span class="pq-label">A splash of booze</span>
          <div class="pq-opts"><button type="button" data-pick="boozy:any" aria-pressed="true">Either</button><button type="button" data-pick="boozy:yes" aria-pressed="false">Yes</button><button type="button" data-pick="boozy:no" aria-pressed="false">No</button></div>
        </div>
        <div class="pq-foot">
          <label class="pq-check"><input type="checkbox" id="pick-nonuts"> No nuts, please</label>
          <div class="scope" role="radiogroup" aria-label="Which flavors">
            <button type="button" role="radio" data-scope="week" aria-checked="true">In the case this week</button>
            <button type="button" role="radio" data-scope="all" aria-checked="false">Any flavor</button>
          </div>
        </div>
      </div>
    </div>
    <div class="wrap picker-out" id="picker-out" hidden>
      <p class="kicker dark">Your three</p>
      <p class="picker-note" id="picker-note" aria-live="polite"></p>
      <div class="picker-results" id="picker-results" aria-live="polite"></div>
      <button class="link-arrow picker-more" id="picker-more" type="button">Show three more</button>
    </div>
  </section>
{CAMPAIGN}
</main>"""

POPUPS = f"""
<main id="main" class="pad-top">
{FLYER.replace("__TOURMORE__", TOUR_FORM).replace('<h2 class="flyer-city" id="popups-h">On Tour</h2>', '<h1 class="flyer-city" id="popups-h">On Tour</h1>')}
  <section class="cream tour-notes" aria-labelledby="tn-h">
    <div class="wrap tn-grid">
      <h2 class="display-md" id="tn-h">How Pop-ups Work</h2>
      <ol class="tn-list">
        <li><span class="donut-num g1" aria-hidden="true"><b>1</b></span><p>Dates and addresses drop on Instagram first, then here.</p></li>
        <li><span class="donut-num g2" aria-hidden="true"><b>2</b></span><p>Get there early. Quantities are limited and pop-ups sell out.</p></li>
        <li><span class="donut-num g3" aria-hidden="true"><b>3</b></span><p>Want Cloudy in your city? Add it above, and you'll hear first if the tour comes your way.</p></li>
      </ol>
    </div>
  </section>
  <section class="ig" aria-labelledby="ig-h">
    <div class="wrap ig-head">
      <div>
        <p class="kicker">@cloudydonuts</p>
        <h2 class="display-md" id="ig-h">Straight From The Feed</h2>
        <p class="ig-sub">Every stop drops here first. Swipe for the latest.</p>
      </div>
      <div class="ig-ctrl">
        <button type="button" class="ig-arrow" id="ig-prev" aria-label="Previous posts"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <button type="button" class="ig-arrow" id="ig-next" aria-label="Next posts"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <a class="btn btn-mint" href="https://www.instagram.com/cloudydonuts/" target="_blank" rel="noopener">Follow @cloudydonuts</a>
      </div>
    </div>
    <ul class="ig-row" id="ig-row" role="list" aria-label="Latest Instagram posts"></ul>
  </section>
</main>"""

STORY = f"""
<main id="main">
{page_hero("Our story", "Everything Is<br>Created With<br>Intention.", "", "d6231e_c89404741c31438ebe480745bb432652~mv2.jpg")}
  <section class="story" aria-label="Our story">
    <div class="wrap story-grid">
      <div class="story-copy">{STORY_COPY}
      </div>
      <aside class="story-side">
        <p class="kicker">Collectively</p>
        <p class="pull">Worlds of Black luxury.</p>
        <img class="wix side-donut" data-wix="d6231e_862492948fe948f98140a59edb4a546c~mv2.png" data-w="500" alt="Brown Butter Chocolate Chip donut">
        <a class="founder-link" href="https://www.thesevenstreams.com" target="_blank" rel="noopener">7Streams <span aria-hidden="true">↗</span></a>
      </aside>
    </div>
    <div class="wrap">{FIRSTS}
    </div>
  </section>
  <section class="photo-pair" aria-label="Cloudy Donut photos">
    <img class="wix" data-wix="d6231e_a9fcfc976a4c48ffaec94304ac9051bb~mv2.jpg" data-w="1100" alt="The Cloudy Donut display case">
    <img class="wix" data-wix="d6231e_c4aef1bd70ef4c6490281833541a53d2~mv2.jpg" data-w="900" alt="A woman holding a stack of glazed donuts">
  </section>
{PRESS}
</main>"""

EXPERIENCES = f"""
<main id="main">
{page_hero("Luxury dessert experiences", "Bring Cloudy<br>To The Party.", "Weddings, launches, showers, office days. Cloudy Donut Minis turn any event into a Cloudy experience.", "d6231e_2ddfd7964b1f4e089573e576a08eb5e0~mv2.jpg")}
  <section class="experiences" id="experiences" aria-labelledby="exp-h">
    <div class="wrap exp-grid">
      <div class="exp-copy">
        <p class="kicker">Cloudy Donut Minis</p>
        <h2 class="display-md" id="exp-h">Two To Four Bites. All Cloudy.</h2>
        <p>Minis are passed on trays or styled as a display. You pick the flavors. We come back with menu options built around your event.</p>
        <p class="note">Book at least 14 days ahead.</p>
        <img class="wix exp-photo" data-wix="d6231e_de85e764a62b4080bf6cb8aab7b5ee25~mv2.png" data-w="600" alt="Raspberry Rosé donuts">
      </div>{CATERING_FORM}
    </div>
  </section>
  <section class="banner-photo" aria-hidden="true"><img class="wix" data-wix="d6231e_53d7df9586bb4bcfa7d31a527d4cfe90~mv2.jpg" data-w="1800" alt=""></section>
{SHIP}
</main>"""

LOCS = f"""
<main id="main">
{page_hero("Come early", "Where To<br>Find Us.", "Weekends only. Order ahead for pickup and skip the line.", "d6231e_a9fcfc976a4c48ffaec94304ac9051bb~mv2.jpg")}
{LOCATIONS.replace('<div class="head-row">', '<div class="head-row visually-hidden">').replace('Where To Find Us</h2>', 'Shops and hours</h2>').replace('<ul class="loc-grid" id="loc-grid" role="list"></ul>', '<ul class="loc-grid" id="loc-grid" role="list"></ul>\n      <p class="tour-line" id="tour-line" hidden></p>')}
{CAMPAIGN}
{FAQ}
</main>"""

COMPARE_PAGES = {
    "index.html": ("Home",
        ["This week's lineup sits behind a button, inside a pop-up.",
         "The email signup asks you to accept terms and conditions, but there are no terms to read.",
         "Lineup photos are described to screen readers by file name, like \"raspberry lemonade.png\".",
         "The page's main heading reads \"100% Vegan\"."],
        ["This week's lineup opens on the page, in a sealed box. Tap the seal.",
         "Every signup links to short, plain email terms.",
         "Every donut photo is named for the donut.",
         "Each shop shows open or closed on New York time, plus the next tour stop with a countdown."]),
    "flavors.html": ("Flavors",
        ["Every flavor sits in one long scroll.",
         "Nut warnings live inside the descriptions, with no way to filter."],
        ["40+ flavors, filterable by nut-free, boozy and made for pups.",
         "Tap any donut for its deli-paper card with allergens.",
         "Find your flavor: four questions, this week's box or every flavor."]),
    "pop-ups.html": ("Pop-ups",
        ["There's no tour page. Stops are announced on Instagram.",
         "The pop-up ordering page reads \"No items to show yet.\""],
        ["A tour page with a flyer built from the tour list. Next stop: Newark, Nov 14.",
         "\"Bring Cloudy to my city\" signups show where demand is.",
         "A swipeable row of the latest @cloudydonuts posts. Once Cloudy connects Instagram, new posts appear on their own and each card shows the post's cover photo."]),
    "our-story.html": ("Our story",
        ["\"Our Story\" in the menu links back to the home page."],
        ["Its own page, with the story copy word for word.",
         "Firsts and press coverage, each press item linked to the source."]),
    "experiences.html": ("Experiences",
        ["Catering notice reads 14 days in one place and 7 in another."],
        ["One number, 14 days, in the event form.",
         "Event requests and the cake waitlist land in one place, connected to the tools Cloudy already uses or a standard free or low-cost one."]),
    "locations.html": ("Locations",
        ["Hours are listed with no open or closed status, no map and no directions link.",
         "The FAQ sends merch shoppers to a Federal Hill shop this page doesn't list."],
        ["Maps with donut pins, plus Google Maps, Apple Maps and Waze links.",
         "Open now, by shop, and tap to call.",
         "Only the three shops on the current site, and all 14 FAQ answers."]),
}

# Each pair lines up: the live issue, then the demo fix, in the same order.
EVERY_PAGE = [
    ("Mint text on cream measures about 1.5:1. WCAG AA asks for 4.5:1.",
     "Text contrast meets WCAG AA on every page."),
    ("Photos are described to screen readers by file name.",
     "Photos carry real descriptions, or stay silent when the donut's name sits beside them."),
    ("Flavors and Locations have no H1. Contact and FAQ jump from H1 to H3.",
     "One H1 per page, no skipped heading levels."),
    ("Instagram and Facebook open new tabs without saying so.",
     "Links that open a new tab tell screen readers first."),
    ("No phone number on the site can be tapped to call.",
     "Every phone number calls on tap."),
    ("The email address appears only on Contact.",
     "Email sits in the footer of every page."),
    ("Log In and a cart sit in every header. Nothing is sold online.",
     "No login or cart until there's something to sell."),
    ("Six leftover Wix template posts, on fintech and earbuds, are indexed by Google under the Cloudy name.",
     "Only Cloudy pages exist to be indexed."),
]

LIVE = {  # what cloudydonut.com has for each page, checked Nov 10, 2026
    "index.html": ("cloudydonut.com", "100% Vegan"),
    "flavors.html": ("cloudydonut.com/our-flavors", None),
    "pop-ups.html": ("No tour page today", None),
    "our-story.html": ("Menu link goes to the home page", None),
    "experiences.html": ("cloudydonut.com/event-packages", "Event & Catering Packages"),
    "locations.html": ("cloudydonut.com/order-online-locations", None),
}
SAME = {
    "index.html": ["Logo, cream, mint and sage, and the Caudex type", "Photos from cloudydonut.com", "This week's lineup", "The box: mint, white logo and DONUT stop BELIEVING! on the side"],
    "flavors.html": ["Flavor names, descriptions and photos", "Nut notes from each description"],
    "pop-ups.html": ["The \"Cloudy Donut Presents\" flyer style from Instagram", "The Newark stop, as announced on Instagram"],
    "our-story.html": ["The Our Story copy, word for word"],
    "experiences.html": ["Event and catering packages"],
    "locations.html": ["The three shops, with addresses, hours and phone", "All 14 FAQ answers"],
}
BUILD = [
    ("The lineup updates itself", "Flavors, shop hours and pop-up dates live in one simple list. Change it there and every page follows. It can run on the tools Cloudy already uses, or a standard free or low-cost one."),
    ("Every pop-up gets a flyer", "Add a city and date, and the site builds the \"Cloudy Donut Presents\" flyer with a live countdown."),
    ("Demand, mapped", "\"Bring Cloudy to my city\" signups show where the next tour stop should go."),
    ("Shipping, ready before launch", "The cake waitlist builds now, so the first day of shipping already has buyers."),
    ("One inbox for every form", "Experiences, newsletter, tour alerts and the waitlist land in one inbox, connected to what Cloudy uses now or a standard free or low-cost tool."),
    ("Owned by Cloudy", "Custom code in Cloudy's own GitHub and Cloudflare accounts. No platform subscription."),
]

WIX_IMG = "https://static.wixstatic.com/media/{0}/v1/fill/w_600,h_315,al_c,q_80,enc_auto/{0}"
LIVE_SHARE = {  # cloudydonut.com titles, descriptions and share images, checked Nov 12, 2026
    "index.html": ("cloudydonut.com", "HOME | Cloudy Donut", "Cloudy Donut Co., located in Brooklyn and Manhattan is a vegan gourmet bakery known for its mouthwatering donuts, pound cakes, and cinnamon rolls.", "d6231e_53d7df9586bb4bcfa7d31a527d4cfe90~mv2.jpg", None),
    "flavors.html": ("cloudydonut.com › our-flavors", "OUR FLAVORS | Cloudy Donut", None, "d6231e_9077a0dc3d96405ca1bae4d9ad1a346c~mv2.png", "The share image is the logo file on a see-through background, so apps show it on a plain white or black box."),
    "pop-ups.html": (None, None, None, None, "There's no pop-ups page to share or find in search."),
    "our-story.html": ("cloudydonut.com", "HOME | Cloudy Donut", "Cloudy Donut Co., located in Brooklyn and Manhattan is a vegan gourmet bakery known for its mouthwatering donuts, pound cakes, and cinnamon rolls.", "d6231e_53d7df9586bb4bcfa7d31a527d4cfe90~mv2.jpg", "There's no story page. Sharing Our Story shares the home page."),
    "experiences.html": ("cloudydonut.com › event-packages", "CATERING & EVENTS | Cloudy Donut", "Cloudy Donut is a 100% vegan, small-batched, gourmet donut shop located in Baltimore, MD and Brooklyn Heights, NY.", "d6231e_53d7df9586bb4bcfa7d31a527d4cfe90~mv2.jpg", "The description leaves out NoLita, and the image is the same one most pages use."),
    "locations.html": ("cloudydonut.com › order-online-locations", "LOCATIONS | Cloudy Donut", None, "d6231e_53d7df9586bb4bcfa7d31a527d4cfe90~mv2.jpg", None),
}

def share_block(fname):
    url, title, desc, img, note = LIVE_SHARE[fname]
    p_title, p_desc = PAGES[fname][0], PAGES[fname][1]
    slug = fname[:-5]
    new_title = "Cloudy Donut Co." if slug == "index" else f"{p_title} | Cloudy Donut Co."
    new_url = "cloudydonut.com" + ("" if slug == "index" else f" › {slug}")
    def card(cls, label, im, u, ti, de):
        img_html = (f'<img class="{"contain" if im and ".png" in im else ""}" src="{im}" alt="" loading="lazy" width="600" height="315">' if im else '<div class="sc-none">No page</div>')
        lbl = f'<span class="bts-lbl {"old" if cls == "today" else "new"}">{label}</span>'
        if not ti:
            return f'<div class="share-card {cls}">{lbl}{img_html}</div>'
        d = f'<p class="g-desc">{de}</p>' if de else '<p class="g-desc g-miss">No description set, so Google fills this line with whatever text it finds on the page.</p>'
        return f'<div class="share-card {cls}">{lbl}{img_html}<div class="g-snip"><p class="g-url">{u}</p><p class="g-title">{ti}</p>{d}</div></div>'
    live_img = None if not img else (f"https://static.wixstatic.com/media/{img}/v1/fit/w_600,h_315,q_80/{img}" if img.endswith(".png") else WIX_IMG.format(img))
    today = card("today", "Today", live_img, url, title, desc)
    new = card("new", "New", f"og/{slug}.jpg", new_url, new_title, p_desc)
    note_html = f'<p class="bts-sub share-note">{note}</p>' if note else ""
    return f"""<h3>Shared and searched</h3>
      <p class="bts-sub">The image people see when this page is texted or posted, and how it reads in a Google result.</p>
      <div class="share-grid">{today}{new}</div>
      {note_html}"""

def bts_block(fname):
    name, live, demo = COMPARE_PAGES[fname]
    url, h1 = LIVE[fname]
    ul = lambda cls, xs: f'<ul class="{cls}">' + "".join(f"<li><span>{x}</span></li>" for x in xs) + "</ul>"
    h1_live = f'"{h1}"' if h1 else '<span class="bad">None</span>'
    tel_live = '<span class="bad">0</span>'
    pairs = "".join(f'<li><span class="bts-lbl old">Today</span><p>{a}</p><span class="bts-lbl new">New</span><p>{b}</p></li>' for a, b in EVERY_PAGE)
    build = "".join(f"<li><h4>{t}</h4><p>{d}</p></li>" for t, d in BUILD)
    return f"""<aside class="badge" aria-label="Demo controls">
  <img class="badge-logo" src="assets/siani-creates-logo.png" alt="Demo by Siani Creates" width="265" height="130">
  <button type="button" id="mode-btn"></button>
  <button type="button" id="bts-btn" aria-expanded="false" aria-controls="bts">Behind the scenes</button>
  <p class="visually-hidden" id="mode-live" aria-live="polite"></p>
</aside>
<div class="mode-toast" id="mode-toast" aria-hidden="true"></div>
<aside class="bts" id="bts" aria-label="Behind the scenes" hidden>
  <div class="bts-h"><h2>Behind the scenes</h2><button class="bts-x" type="button" aria-label="Close behind the scenes">×</button></div>
  <div class="bts-tabs" role="tablist" aria-label="Behind the scenes">
    <button role="tab" id="bt-page" aria-controls="bp-page" aria-selected="true">This page</button>
    <button role="tab" id="bt-a11y" aria-controls="bp-a11y" aria-selected="false" tabindex="-1">Accessibility</button>
    <button role="tab" id="bt-build" aria-controls="bp-build" aria-selected="false" tabindex="-1">The build</button>
  </div>
  <div class="bts-body">
    <section role="tabpanel" id="bp-page" aria-labelledby="bt-page" tabindex="0">
      <p class="bts-path">{url}</p>
      <h3>At a glance</h3>
      <table class="snap"><thead><tr><th scope="col"><span class="visually-hidden">Check</span></th><th scope="col">Today</th><th scope="col">New</th></tr></thead><tbody>
        <tr><th scope="row">Main headline</th><td>{h1_live}</td><td class="good" data-snap="h1"></td></tr>
        <tr><th scope="row">Phone numbers you can tap</th><td>{tel_live}</td><td class="good" data-snap="tel"></td></tr>
        <tr><th scope="row">Email link</th><td>Contact page only</td><td class="good">Every page</td></tr>
        <tr><th scope="row">Login and cart</th><td>In the header, nothing to buy</td><td class="good">Gone until there's a store</td></tr>
      </tbody></table>
      {share_block(fname)}
      <h3>Same as the live site</h3>{ul("samel", SAME[fname])}
      <h3>New in this demo</h3>{ul("checkl", demo)}
      <h3>On the live site today, fixed here</h3>{ul("issl", live)}
      <h3>Switch the clock</h3>
      <p class="bts-sub">Cloudy opens Friday to Sunday. The button at the bottom left steps the site through a Saturday morning and a Tuesday, so you can watch open and closed update whatever day you visit.</p>
      <div class="bts-note">Live site details come from cloudydonut.com, checked November 10, 2026.</div>
    </section>
    <section role="tabpanel" id="bp-a11y" aria-labelledby="bt-a11y" tabindex="0" hidden>
      <p class="bts-sub">What changes for people using screen readers, keyboards or a phone, on every page.</p>
      <ol class="pairs">{pairs}</ol>
      <div class="bts-note">Automated scan with axe-core against WCAG 2.1 AA, the standard used in ADA website claims: 0 issues on all six pages, with search, the flavor cards and this panel open.</div>
    </section>
    <section role="tabpanel" id="bp-build" aria-labelledby="bt-build" tabindex="0" hidden>
      <h3>Yours to run, yours to keep</h3>
      <ol class="buildl">{build}</ol>
      <div class="bts-note">Forms in this demo are not connected. Nothing you type is saved.</div>
      <p class="bts-cta">Like what you see? Reply to Siani's message with the best email, and the full proposal follows.</p>
    </section>
  </div>
</aside>"""

PAGES = {
    "index.html": ("Home", "Luxury dessert experiences. 100% vegan, small batch and hand crafted in Brooklyn Heights, NoLita and Baltimore. See this week's lineup.", HOME, True),
    "flavors.html": ("Flavors", "40+ Cloudy Donut flavors, with allergens, this week's lineup and a four-question flavor finder.", FLAVORS, False),
    "pop-ups.html": ("Pop-ups", "The Cloudy Donut pop-up tour: the next stop, dates, and a signup to bring Cloudy to your city.", POPUPS, False),
    "our-story.html": ("Our story", "How Cloudy Donut Co. became NYC's first 100% vegan donut shop, and the first Black-owned food and beverage business in Brooklyn Heights and NoLita.", STORY, False),
    "experiences.html": ("Experiences", "Cloudy Donut Minis for weddings, offices and events, plus the waitlist for pound cakes by mail.", EXPERIENCES, False),
    "locations.html": ("Locations", "Cloudy Donut shops in Brooklyn Heights, NoLita and Baltimore, with hours, maps, directions and FAQ.", LOCS, False),
}

for fname, (title, desc, body, is_home) in PAGES.items():
    html = head(title, desc, fname) + f'\n<body class="page-{fname[:-5]}">\n' + (SVG_DEFS if is_home else "") + header(fname, True) + body + FOOTER.replace("__BTS__", bts_block(fname))
    (ROOT / fname).write_text(html)
    print("wrote", fname)

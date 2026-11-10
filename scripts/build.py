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


def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#141312">
  <title>{title} | Cloudy Donut Co. Concept by Siani Creates</title>
  <meta name="description" content="{desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Caudex:ital,wght@0,400;0,700;1,400;1,700&family=Figtree:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>"""


SVG_DEFS = """
<svg class="defs" aria-hidden="true" focusable="false">
  <filter id="cloud-back" x="-50%" y="-50%" width="200%" height="200%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" seed="7"/>
    <feDisplacementMap in="SourceGraphic" scale="170"/>
  </filter>
  <filter id="cloud-mid" x="-50%" y="-50%" width="200%" height="200%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="7"/>
    <feDisplacementMap in="SourceGraphic" scale="150"/>
  </filter>
  <filter id="cloud-front" x="-50%" y="-50%" width="200%" height="200%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="2" seed="7"/>
    <feDisplacementMap in="SourceGraphic" scale="100"/>
  </filter>
</svg>

<div class="intro" id="intro" aria-hidden="true">
  <div class="sky">""" + "".join(
    f'\n    <div class="cloud cl-{c}"><div class="back"></div><div class="mid"></div><div class="front"></div></div>' for c in "abcde"
) + f"""
  </div>
  <div class="intro-mark">
    <img class="wix" data-wix="{LOGO}" data-w="600" alt="">
    <p class="intro-line">Where Dreams Crumb True</p>
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
    </div>
    <p class="concept-line">Concept site prepared by Siani Creates for Cloudy Donut Co. Not the official website. Content, logo and photos belong to Cloudy Donut Co.</p>
  </div>
</footer>

<button class="concept-pill" type="button" aria-controls="concept" aria-expanded="false">Concept by Siani Creates</button>
<aside class="concept-panel" id="concept" hidden aria-label="About this concept">
  <button class="concept-close" type="button" aria-label="Close">×</button>
  <p class="kicker dark">What this build does</p>
  <h2>Yours to run, yours to keep</h2>
  <ol>
    <li><h3>The lineup updates itself</h3><p>Flavors, shop hours and pop-up dates live in one Airtable base. Change it there and every page follows.</p></li>
    <li><h3>Every pop-up gets a flyer</h3><p>Add a city and date, and the site builds the "Cloudy Donut Presents" flyer with a live countdown.</p></li>
    <li><h3>Demand, mapped</h3><p>"Bring Cloudy to my city" signups show where the next tour stop should go.</p></li>
    <li><h3>Shipping, ready before launch</h3><p>The cake waitlist builds now, so the first day of shipping already has buyers.</p></li>
    <li><h3>One inbox for every form</h3><p>Experiences, newsletter, tour alerts and the waitlist land in Airtable and email.</p></li>
    <li><h3>Owned by Cloudy</h3><p>Custom code in Cloudy's own GitHub and Cloudflare accounts. No platform subscription.</p></li>
  </ol>
  <p class="fine">Forms in this concept are not connected. Nothing you type is saved.</p>
</aside>

<dialog class="search-dialog" id="search-dialog" aria-label="Search Cloudy Donut">
  <div class="search-box">
    <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>
    <input id="site-search" type="search" placeholder="Search flavors, shops, pop-ups, questions" autocomplete="off" role="combobox" aria-expanded="true" aria-controls="search-results" aria-autocomplete="list">
    <button class="search-close" type="button">Esc</button>
  </div>
  <div class="search-results" id="search-results" role="listbox" aria-label="Results"></div>
  <p class="search-hint" id="search-hint">Try "pistachio", "nut free", "Brooklyn", "Newark" or "gluten".</p>
</dialog>

<dialog class="flavor-dialog" id="flavor-dialog" aria-labelledby="fd-name">
  <form method="dialog"><button class="dialog-close" aria-label="Close">×</button></form>
  <img id="fd-img" alt="">
  <div class="fd-body">
    <p class="fd-badge" id="fd-badge" hidden>On this week's lineup</p>
    <h3 id="fd-name"></h3>
    <p id="fd-desc"></p>
    <p class="fd-contains" id="fd-contains"></p>
  </div>
</dialog>

<script src="data/fallback.js" defer></script>
<script src="app.js" defer></script>
</body>
</html>
"""


def page_hero(kicker, title, sub, img=None):
    photo = f'<img class="wix ph-photo" data-wix="{img}" data-w="1600" alt="">' if img else ""
    return f"""
  <section class="page-hero{' has-photo' if img else ''}">
    {photo}
    <div class="wrap">
      <p class="kicker">{kicker}</p>
      <h1 class="display-lg">{title}</h1>
      {f'<p class="page-sub">{sub}</p>' if sub else ''}
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
      <ol class="lineup-grid" id="lineup-grid"></ol>
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
          <p class="form-msg" role="status"></p>
        </form>
        __MORE__
      </div>
    </div>
  </section>"""

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
        <li><span class="outlet">Forbes</span><span class="headline">How Cloudy Donuts Became Jay-Z's Favorite Donut Shop</span></li>
        <li><a href="https://www.okayplayer.com/cloudy-donut-brooklyn-heights" target="_blank" rel="noopener"><span class="outlet">Okayplayer</span><span class="headline">Cloudy With A Chance Of Progress</span></a></li>
        <li><a href="https://abc7ny.com/videoClip/15696668/" target="_blank" rel="noopener"><span class="outlet">ABC7 New York</span><span class="headline">Cloudy Donut is a ray of sunshine for creators of color</span></a></li>
        <li><a href="https://timeout.com/newyork/news/this-tiktok-famous-vegan-donut-company-just-opened-a-store-in-brooklyn-110122" target="_blank" rel="noopener"><span class="outlet">Time Out New York</span><span class="headline">This TikTok-famous vegan donut company just opened in Brooklyn</span></a></li>
        <li><a href="https://thegrio.com/2023/04/25/blackmade-derrick-faulcon-on-cloudy-donut-co-entrepreneurship" target="_blank" rel="noopener"><span class="outlet">theGrio</span><span class="headline">BlackMade: Derrick Faulcon on Cloudy Donut Co.</span></a></li>
        <li><a href="https://blackenterprise.com/ex-convict-opens-vegan-donut-shop-first-ever-black-owned-business-in-brooklyn-heights-nyc/" target="_blank" rel="noopener"><span class="outlet">Black Enterprise</span><span class="headline">First ever Black-owned business in Brooklyn Heights</span></a></li>
      </ul>
    </div>
  </section>"""

FAQ = """
  <section class="faq" id="faq" aria-labelledby="faq-h">
    <div class="wrap faq-wrap">
      <h2 class="display-md" id="faq-h">Good To Know</h2>
      <div class="faq-list">
        <details><summary>Are your donuts gluten free?</summary><p>Our donuts are 100% vegan, but they are not gluten free.</p></details>
        <details><summary>Which donuts have nuts?</summary><p>Every flavor with nuts is marked on the <a href="flavors.html">flavors page</a>.</p></details>
        <details><summary>What replaces eggs and dairy?</summary><p>Applesauce, coconut milk and shortening. All donuts are fried in liquid vegetable shortening.</p></details>
        <details><summary>How long do they keep?</summary><p>No preservatives, so eat donuts within 13 hours at room temperature. Cinnamon rolls and pound cakes keep for 2–3 days.</p></details>
        <details><summary>What if I forget to pick up a preorder?</summary><p>If you ordered through a delivery app, contact that app. If you ordered directly from us, give us a call and we'll do our best to help.</p></details>
        <details><summary>Do you ship?</summary><p>Not donuts. Pound cakes are coming next year, and the <a href="experiences.html#ship">waitlist</a> hears first.</p></details>
        <details><summary>Do you make custom donuts?</summary><p>We have special holiday and occasion packages, but no custom orders at this time.</p></details>
        <details><summary>Something for the dog?</summary><p>Lil Bow Wow and the Snoop Doggy Donut are made for pups.</p></details>
        <details><summary>Gift cards?</summary><p>Available in store at Brooklyn Heights.</p></details>
        <details><summary>How can I apply for a job?</summary><p>Send us an email. We're always open to new talent with an interest in baking.</p></details>
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
{LINEUP.replace("__MORE__", '<a class="btn btn-line-ink" href="flavors.html">See all 44 flavors</a>')}
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
{page_hero("The full rotation", "Every Flavor<br>We Make.", "Six to eight of these hit the case each weekend. All 100% vegan, small-batched and hand crafted. Tap a donut for the details and allergens.", "d6231e_53d7df9586bb4bcfa7d31a527d4cfe90~mv2.jpg")}
  <section class="cream flavors" id="flavors" aria-label="Flavor library">
    <div class="wrap">
      <div class="flavor-tools">
        <div class="chips" role="group" aria-label="Filter flavors" id="chips"></div>
        <label class="search">
          <span class="visually-hidden">Search flavors</span>
          <input type="search" id="flavor-search" placeholder="Search flavors">
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
{CAMPAIGN}
</main>"""

POPUPS = f"""
<main id="main" class="pad-top">
{FLYER.replace("__TOURMORE__", TOUR_FORM)}
  <section class="cream tour-notes" aria-labelledby="tn-h">
    <div class="wrap tn-grid">
      <h2 class="display-md" id="tn-h">How Pop-ups Work</h2>
      <ol class="tn-list">
        <li><span class="big">01</span><p>Dates and addresses drop on Instagram first, then here.</p></li>
        <li><span class="big">02</span><p>Get there early. Quantities are limited and pop-ups sell out.</p></li>
        <li><span class="big">03</span><p>Want Cloudy in your city? Add it above. Signups show where the tour goes next.</p></li>
      </ol>
    </div>
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
{LOCATIONS.replace('<div class="head-row">', '<div class="head-row" hidden>')}
{CAMPAIGN}
{FAQ}
</main>"""

PAGES = {
    "index.html": ("Home", "Luxury dessert experiences. 100% vegan, small batch, hand crafted.", HOME, True),
    "flavors.html": ("Flavors", "Every Cloudy Donut flavor, with allergens and this week's lineup.", FLAVORS, False),
    "pop-ups.html": ("Pop-ups", "The Cloudy Donut pop-up tour: next stop, dates and city signups.", POPUPS, False),
    "our-story.html": ("Our story", "The story of Cloudy Donut Co.", STORY, False),
    "experiences.html": ("Experiences", "Cloudy Donut Minis for events, plus the cake shipping waitlist.", EXPERIENCES, False),
    "locations.html": ("Locations", "Cloudy Donut shops, hours and FAQ.", LOCS, False),
}

for fname, (title, desc, body, is_home) in PAGES.items():
    html = head(title, desc) + f'\n<body class="page-{fname[:-5]}">\n' + (SVG_DEFS if is_home else "") + header(fname, True) + body + FOOTER
    (ROOT / fname).write_text(html)
    print("wrote", fname)

#!/usr/bin/env python3
"""Builds index.html, services.html and thanks.html from one source.

Edit the settings and copy below, then run:  python3 build.py
Do not hand-edit the generated HTML; it is overwritten on every build.
"""
from html import escape
from pathlib import Path

# ---------------------------------------------------------------- settings
BUSINESS = "Hot Water Today"
OWNER = "Kyle Cadotte"
PHONE = "(781) 204-3247"
PHONE_TEL = "+17812043247"
PUBLIC_EMAIL = "info@hotwatertodaycorp.com"   # shown on the site
SITE_URL = "https://www.hotwatertodaycorp.com"

# Lead form (FormSubmit). LIVE: leads go to Ryan, cc Kyle (info@).
# To go live: FORM_TO = "info@hotwatertodaycorp.com", drop "TEST " from the
# subject, rebuild, then submit once and click FormSubmit's activation email.
FORM_TO = "rcummins1025@gmail.com"
FORM_SUBJECT = "New Hot Water Today lead"
# Copies of every lead (comma-separated). Kyle gets each lead; FORM_TO stays
# Ryan's activated address so no new FormSubmit activation is needed.
FORM_CC = "info@hotwatertodaycorp.com"
# Where FormSubmit sends visitors who submit without JavaScript. Use the
# GitHub Pages address until the domain points here, then switch to SITE_URL.
NEXT_URL = "https://www.hotwatertodaycorp.com/thanks.html"

# Massachusetts plumbing license number. Leave "" to hide it.
LICENSE_NO = ""

TOWNS = [
    "Andover", "Arlington", "Bedford", "Belmont", "Billerica", "Brighton",
    "Brookline", "Burlington", "Cambridge", "Chelsea", "Chelmsford", "Dracut",
    "Everett", "Haverhill", "Lawrence", "Lexington", "Lowell", "Lynnfield",
    "Malden", "Medford", "Melrose", "Methuen", "Newton", "North Andover",
    "North Reading", "Reading", "Revere", "Saugus", "Somerville", "Stoneham",
    "Tewksbury", "Tyngsborough", "Wakefield", "Waltham", "Wilmington", "Woburn",
]
N_TOWNS = len(TOWNS)

# Photos in assets/img/<name>-<width>.webp and .jpg (made by tools/images.py).
IMAGES = {
    "heater": {
        "alt": "Copper water lines, a red-handled ball valve and a flue on top of a gas water heater against a dark stone wall",
        "pos": "62% 38%", "w": 2400, "h": 1500, "widths": [640, 1024, 1600, 2400],
    },
    "utility": {
        "alt": "A white tank water heater in a drain pan with copper piping and an expansion tank, next to a wall-hung boiler",
        "pos": "62% 45%", "w": 1800, "h": 1200, "widths": [640, 1024, 1600],
    },
    "van": {
        "alt": "A white cargo van with a roof ladder rack parked on a wet, leaf-covered street in front of clapboard houses",
        "pos": "50% 55%", "w": 1800, "h": 1200, "widths": [640, 1024, 1600],
    },
}

ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>'


def picture(name, sizes, cls="", eager=False):
    im = IMAGES[name]
    ws = im["widths"]
    webp = ", ".join(f"assets/img/{name}-{w}.webp {w}w" for w in ws)
    jpg = ", ".join(f"assets/img/{name}-{w}.jpg {w}w" for w in ws)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'
            f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="assets/img/{name}-{ws[1]}.jpg" srcset="{jpg}" sizes="{sizes}" '
            f'width="{im["w"]}" height="{im["h"]}" alt="{escape(im["alt"])}" '
            f'style="object-position:{im["pos"]}" {load}></picture>')


def head(title, description, path, preload_img=None):
    areas = ", ".join(f'{{"@type":"City","name":"{t}, MA"}}' for t in TOWNS)
    pre = ""
    if preload_img:
        im = IMAGES[preload_img]
        srcset = ", ".join(f"assets/img/{preload_img}-{w}.webp {w}w" for w in im["widths"])
        pre = f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset}" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE_URL}/{path}">
<meta name="theme-color" content="#0B1F3A">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE_URL}/assets/og.jpg">
<link rel="preload" href="assets/fonts/league-gothic.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Plumber","name":"{BUSINESS}","founder":{{"@type":"Person","name":"{OWNER}"}},"telephone":"{PHONE_TEL}","email":"{PUBLIC_EMAIL}","url":"{SITE_URL}/","image":"{SITE_URL}/assets/og.jpg","areaServed":[{areas}]}}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active):
    def cur(name):
        return ' aria-current="page"' if name == active else ""
    home = "" if active == "home" else "index.html"
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="{BUSINESS} home"><img src="assets/logo.svg" alt="{BUSINESS}" width="852" height="132"></a>
    <nav class="nav" aria-label="Main">
      <a class="wide" href="index.html"{cur("home")}>Home</a>
      <a href="services.html"{cur("services")}>Services</a>
      <a class="wide" href="{home}#towns">Towns</a>
      <a class="wide" href="{home}#quote">Get a quote</a>
      <a class="btn btn-amber" href="tel:{PHONE_TEL}">{ICON_PHONE}{PHONE}</a>
    </nav>
  </div>
</header>
"""


def proof():
    lic = f" Lic. #{LICENSE_NO}." if LICENSE_NO else ""
    return f"""<section class="proof" aria-label="Service area, availability and license">
  <div class="wrap proof-grid">
    <a class="proof-item" href="#towns"><strong>{N_TOWNS} towns</strong><span>North and west of Boston, up to the New Hampshire line. Every one is listed below.</span></a>
    <div class="proof-item"><strong>Same-day service</strong><span>Call early. We’ll tell you straight when we can get there.</span></div>
    <div class="proof-item"><strong>Licensed in MA</strong><span>Massachusetts licensed plumber.{lic}</span></div>
  </div>
</section>
"""


def towns_section():
    items = "".join(f"<li>{t.replace(chr(32), chr(38) + 'nbsp;')}</li>" for t in TOWNS)
    return f"""<section class="towns" id="towns" aria-labelledby="towns-h">
  <div class="towns-photo">{picture("van", "100vw")}</div>
  <div class="wrap towns-inner">
    <p class="label">Service area</p>
    <h2 id="towns-h">On the road in<br>{N_TOWNS} towns.</h2>
    <ul class="town-list">{items}</ul>
    <p class="towns-note">Not on the list? Call anyway: <a href="tel:{PHONE_TEL}">{PHONE}</a>. If we can’t get there, we’ll say so.</p>
  </div>
</section>
"""


def opts(name, values, required=True):
    req = " required" if required else ""
    return "\n".join(
        f'          <label class="opt"><input type="radio" name="{name}" value="{escape(v)}"{req}><span>{escape(label)}</span></label>'
        for v, label in values)


def quote_section():
    issue = [("No hot water", "No hot water"), ("Leaking tank", "Leaking tank"),
             ("Runs out fast or not hot enough", "Runs out fast / not hot enough"),
             ("Replace an old heater", "Replace an old heater"),
             ("Maintenance or flush", "Maintenance or flush"),
             ("Boiler or other plumbing", "Boiler or other plumbing")]
    heater = [("Gas tank", "Gas tank"), ("Electric tank", "Electric tank"),
              ("Tankless", "Tankless"), ("Not sure", "Not sure")]
    soon = [("Today, it's urgent", "Today. It’s urgent"), ("This week", "This week"),
            ("Just getting a quote", "Just getting a quote")]
    towns = "\n".join(f"            <option>{t}</option>" for t in TOWNS)
    return f"""<section class="section mist" id="quote" aria-labelledby="quote-h">
  <div class="wrap quote-grid">
    <div class="quote-intro">
      <p class="label">Get a quote</p>
      <h2 id="quote-h">A few taps.<br>Then we call.</h2>
      <p>Tell us what’s going on and where you are. We’ll call you back.</p>
      <p>Rather talk now? <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
    </div>
    <form class="lead-form" id="lead-form" action="https://formsubmit.co/{FORM_TO}" method="POST">
      <input type="hidden" name="_subject" value="{escape(FORM_SUBJECT)}">
      <input type="hidden" name="_cc" value="{escape(FORM_CC)}">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" value="{NEXT_URL}">
      <div class="hp" aria-hidden="true"><input type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
      <div class="lead-progress" aria-hidden="true"><span class="lead-bar"><span></span></span><span class="lead-count">Step 1 of 5</span></div>
      <fieldset class="step">
        <legend>What’s going on?</legend>
        <div class="opts">
{opts("Issue", issue)}
        </div>
        <button class="btn btn-navy next" type="button" hidden>Next</button>
      </fieldset>
      <fieldset class="step" data-skip-unless-heater>
        <legend>What kind of heater?</legend>
        <div class="opts">
{opts("Heater type", heater, required=False)}
        </div>
        <button class="btn btn-navy next" type="button" hidden>Next</button>
      </fieldset>
      <fieldset class="step">
        <legend>How soon?</legend>
        <div class="opts">
{opts("How soon", soon)}
        </div>
        <button class="btn btn-navy next" type="button" hidden>Next</button>
      </fieldset>
      <fieldset class="step step-town">
        <legend>Which town?</legend>
        <div class="field">
          <label for="lead-town">Your town</label>
          <select id="lead-town" name="Town" required>
            <option value="">Choose your town</option>
{towns}
            <option value="Other">Somewhere else</option>
          </select>
        </div>
        <div class="field">
          <label for="lead-town-other">Not on the list? Type your town</label>
          <input id="lead-town-other" name="Other town" type="text" autocomplete="address-level2">
        </div>
        <p class="field-err" id="town-err" aria-live="polite"></p>
        <button class="btn btn-navy next" type="button">Next</button>
      </fieldset>
      <fieldset class="step">
        <legend>Who should we call?</legend>
        <div class="field">
          <label for="lead-name">Name</label>
          <input id="lead-name" name="Name" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="lead-phone">Phone</label>
          <input id="lead-phone" name="Phone" type="tel" autocomplete="tel" inputmode="tel" required>
        </div>
        <div class="field">
          <label for="lead-note">Anything else? <small>(optional)</small></label>
          <textarea id="lead-note" name="Note" placeholder="Age of the heater, where it is, what you’re seeing"></textarea>
        </div>
        <p class="field-err" id="lead-err" aria-live="polite"></p>
        <div class="lead-actions">
          <button class="btn btn-amber" type="submit">Send request</button>
        </div>
        <p class="lead-status" role="status" aria-live="polite"></p>
        <p class="lead-note">Leaking right now? Don’t wait on the form. Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
      </fieldset>
      <button class="back" type="button" hidden>&larr; Back</button>
    </form>
  </div>
</section>
"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <img src="assets/logo-white.svg" alt="{BUSINESS}" width="852" height="132">
        <a class="foot-phone" href="tel:{PHONE_TEL}">{PHONE}</a>
        <p>{OWNER}, owner<br><a href="mailto:{PUBLIC_EMAIL}">{PUBLIC_EMAIL}</a></p>
      </div>
      <div>
        <h2>Pages</h2>
        <ul><li><a href="index.html">Home</a></li><li><a href="services.html">Services</a></li><li><a href="index.html#towns">Towns</a></li><li><a href="index.html#quote">Get a quote</a></li></ul>
      </div>
      <div>
        <h2>Work</h2>
        <ul><li>Water heater replacement</li><li>Water heater repair</li><li>Tankless</li><li>Boilers</li><li>Plumbing</li></ul>
      </div>
    </div>
    <div class="legal"><span>&copy; <span class="yr">2026</span> {BUSINESS}</span><span>Water heaters, boilers and plumbing in {N_TOWNS} Massachusetts towns</span></div>
  </div>
</footer>
<nav class="call-bar" aria-label="Call or get a quote">
  <a class="call" href="tel:{PHONE_TEL}">{ICON_PHONE}{PHONE}</a>
  <a class="quote" href="#quote">Quote</a>
</nav>
<script src="assets/site.js" defer></script>
<script>document.querySelectorAll('.yr').forEach(function(e){{e.textContent=new Date().getFullYear()}});</script>
</body>
</html>
"""


TIPS = f"""<section class="section mist" aria-label="Before you call">
  <div class="wrap tips">
    <div class="tip">
      <h3>Leaking right now?</h3>
      <p>Close the cold-water valve on the pipe going into the top of the tank. That stops the tank from refilling. Then call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
    </div>
    <div class="tip">
      <h3>Read us the label</h3>
      <p>The sticker on the side of the tank lists the model, size and fuel type. Have it handy when you call and we can tell you a lot before we even get there.</p>
    </div>
  </div>
</section>
"""

HOME = head(
    f"{BUSINESS} | Water Heater Repair & Replacement | {OWNER}",
    f"Water heater repair and replacement by {OWNER}. Gas, electric and tankless, plus boilers and plumbing, in {N_TOWNS} towns north and west of Boston. Call {PHONE}.",
    "", preload_img="heater",
) + header("home") + f"""<main id="main">
<section class="hero" aria-labelledby="hero-h">
  {picture("heater", "100vw", "hero-img", eager=True)}
  <div class="wrap hero-inner">
    <p class="kicker">Water heaters · Boilers · Plumbing</p>
    <h1 id="hero-h">No hot water?<br><span class="hot">Not for long.</span></h1>
    <p class="lead">{BUSINESS} repairs and replaces water heaters. Gas, electric and tankless, done right the first time.</p>
    <div class="hero-cta">
      <a class="btn btn-amber" href="tel:{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
      <a class="btn btn-ghost" href="#quote">Get a quote</a>
    </div>
  </div>
</section>
{proof()}
<section class="section" id="services" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="section-head">
      <p class="label">What we do</p>
      <h2 id="svc-h">Water heaters first.</h2>
      <p class="lead">It’s most of what we do, every day. Boilers and plumbing too.</p>
    </div>
    <div class="svc-feature">
      <figure class="svc-photo">{picture("utility", "(min-width: 960px) 45vw, 100vw")}</figure>
      <div class="svc-list">
        <article class="svc">
          <h3>Replacement &amp; install</h3>
          <p>Tank leaking or worn out? We pull the old one, haul it away and put in the right size for your house.</p>
          <ul class="ticks"><li>Gas and electric tanks</li><li>Tankless, on-demand</li><li>Expansion tanks and relief valves</li><li>Venting and gas hookups</li></ul>
        </article>
        <article class="svc">
          <h3>Repair &amp; maintenance</h3>
          <p>Pilot won’t stay lit. Hot water runs out fast. Tank is rumbling. We find the problem and tell you if it’s worth fixing.</p>
          <ul class="ticks"><li>Pilot, igniter, gas valve</li><li>Elements and thermostats</li><li>Flush and anode rod</li><li>Tankless descaling</li></ul>
        </article>
      </div>
    </div>
    <div class="svc-more">
      <div><h3>Boilers</h3><p>Boiler replacement and installs for home heating.</p></div>
      <div><h3>Plumbing</h3><p>Leaks, fixtures, valves, disposals. The everyday stuff.</p></div>
      <div><h3>Everything else</h3><p>Commercial and other residential plumbing. Call and ask.</p></div>
    </div>
    <a class="text-link" href="services.html">All services <span aria-hidden="true">&rarr;</span></a>
  </div>
</section>
{TIPS}{towns_section()}{quote_section()}</main>
""" + footer()


def svc_detail(anchor, label, title, lead, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"""    <article class="svc-detail" id="{anchor}">
      <div><p class="label">{label}</p><h2>{title}</h2></div>
      <div class="svc-body">
        <p class="lead">{lead}</p>
        <ul class="ticks">{lis}</ul>
      </div>
    </article>
"""


SERVICES_PAGE = head(
    f"Services | {BUSINESS} | Water Heaters, Boilers & Plumbing",
    f"Water heater replacement and repair (gas, electric, tankless), boiler installs and residential and commercial plumbing in {N_TOWNS} Massachusetts towns. Call {PHONE}.",
    "services.html", preload_img="utility",
) + header("services") + f"""<main id="main">
<section class="hero compact" aria-labelledby="hero-h">
  {picture("utility", "100vw", "hero-img", eager=True)}
  <div class="wrap hero-inner">
    <p class="kicker">Services</p>
    <h1 id="hero-h">Water heaters.<br>Boilers. <span class="hot">Plumbing.</span></h1>
    <p class="lead">Mostly water heaters. If your job isn’t listed here, call and ask.</p>
    <div class="hero-cta">
      <a class="btn btn-amber" href="tel:{PHONE_TEL}">{ICON_PHONE}Call {PHONE}</a>
      <a class="btn btn-ghost" href="#quote">Get a quote</a>
    </div>
  </div>
</section>
{proof().replace('href="#towns"', 'href="index.html#towns"').replace("Every one is listed below.", "Every one is listed on the home page.")}
<section class="section">
  <div class="wrap">
{svc_detail("replacement", "Main work", "Water heater replacement",
    "When a tank is leaking or worn out, it gets replaced. We size the new one to your house, hook it up right and take the old one away.",
    ["Gas tank water heaters", "Electric tank water heaters", "Tankless, on-demand units", "Power-vent and direct-vent models",
     "Expansion tanks and relief valves", "Shutoffs, gas lines and venting", "Haul-away of the old tank", "Moving to a bigger or smaller tank"])}
{svc_detail("repair", "Main work", "Repair &amp; maintenance",
    "A lot of problems are one part, not the whole heater. We find the cause and tell you straight if a repair makes sense.",
    ["No hot water", "Pilot or igniter trouble", "Gas valve and thermocouple", "Elements and thermostats",
     "Dripping relief valve", "Rumbling, sediment, flushing", "Anode rod replacement", "Tankless descaling and service"])}
{svc_detail("boilers", "Heating", "Boilers",
    "Boiler replacement and new installs for home heating. We look at the house, the old system and the piping before we recommend anything.",
    ["Boiler replacement", "New boiler installs", "Near-boiler piping", "Indirect water heaters"])}
{svc_detail("plumbing", "Everything else", "Plumbing",
    "Everyday residential plumbing, plus commercial work. If it’s plumbing and it’s not listed, ask.",
    ["Leaks and pipe repair", "Faucets, toilets, sinks", "Shutoff and main valves", "Garbage disposals", "Commercial plumbing"])}
    <div class="callout">
      <h3>Repair or replace?</h3>
      <p>If the tank itself is leaking, it’s done. Tanks can’t be patched. If it’s a part, like an igniter, thermocouple, element or valve, it can usually be fixed. Either way we’ll explain what we found and give you the options before any work starts.</p>
    </div>
  </div>
</section>
{TIPS}{quote_section()}</main>
""" + footer()


THANKS = head(
    f"Request sent | {BUSINESS}",
    f"Thanks for contacting {BUSINESS}.",
    "thanks.html",
).replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"') + header("") + f"""<main id="main">
<section class="thanks-band">
  <div class="wrap thanks">
    <p class="label">Request sent</p>
    <h1>Got it.<br><span class="hot">We’ll call you.</span></h1>
    <p class="lead">Your request is in. Keep your phone handy.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="callout">
      <h2>Leaking right now?</h2>
      <p>Close the cold-water valve on the pipe going into the top of the tank, then call <a href="tel:{PHONE_TEL}">{PHONE}</a>. Don’t wait on us to call you.</p>
    </div>
    <p><a class="text-link" href="index.html"><span aria-hidden="true">&larr;</span> Back to home</a></p>
  </div>
</section>
</main>
""" + footer()


if __name__ == "__main__":
    here = Path(__file__).parent
    (here / "index.html").write_text(HOME)
    (here / "services.html").write_text(SERVICES_PAGE)
    # Call bar "Quote" on the thanks page has no form below it: send it home.
    (here / "thanks.html").write_text(THANKS.replace('<a class="quote" href="#quote">', '<a class="quote" href="index.html#quote">'))
    print("Built index.html, services.html, thanks.html")

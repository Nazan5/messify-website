#!/usr/bin/env python3
"""Builds the Messify static site into ./dist. Run: python3 build.py"""
import json, os, html
from urllib.parse import quote
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
BASE = 'https://www.messify.me'
TODAY = '2026-10-11'
UPDATED_LABEL = 'October 2026'

PHONE_DISPLAY = '+971 50 251 3033'
PHONE_TEL = '+971502513033'
EMAIL = 'info@messify.me'
WA = 'https://wa.me/971502513033'
IG = 'https://www.instagram.com/messify.me/'
APP_STORE = 'https://apps.apple.com/ae/app/my-messify/id6749799177'
GOOGLE_PLAY = 'https://play.google.com/store/apps/details?id=com.messifyfzc.messify'
HOURS_LABEL = 'Daily, 8 AM to 11 PM'
HOURS_SPEC = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '08:00', 'closes': '23:00'}]
OG_IMAGE = BASE + '/assets/img/og-messify.jpg'
GA_ID = 'G-KNKHKG7LR2'  # Google Analytics 4
LOGO = BASE + '/assets/img/messify-logo.png'

ONE_LINER = ('Messify is a Dubai meal-plan and catering company. Its meals are cooked fresh every day in a partner kitchen in International City '
             'and delivers breakfast, lunch and dinner together each morning across Dubai Academic City, Dubai Silicon Oasis '
             'and International City, from AED 25.63 a meal. It also caters corporate events, parties, university events '
             'and weddings across Dubai, Sharjah, Ajman and Abu Dhabi.')

PLANS = [  # meals a day, length, tokens, price
    (1, 'weekly', 7, 215), (2, 'weekly', 14, 415), (3, 'weekly', 21, 610),
    (1, 'monthly', 26, 715), (2, 'monthly', 52, 1400), (3, 'monthly', 78, 1999),
]
def per(price, tokens): return f'{price / tokens:.2f}'
def aed(n): return f'AED {n:,}'
def mlabel(m): return f'{m} meal{"s" if m > 1 else ""} a day'

PLACES = {
    'academic-city': 'Dubai International Academic City',
    'silicon-oasis': 'Dubai Silicon Oasis',
    'international-city': 'International City, Dubai',
}

esc = html.escape

# ---------------------------------------------------------------- icons
I = {
 'arrow': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'back': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
 'tick': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12 4 4 10-10"/></svg>',
 'phone': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
 'mail': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
 'insta': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
 'wa': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5Z"/></svg>',
 'cap': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/></svg>',
 'home': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
 'office': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/></svg>',
 'pin': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'case': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/></svg>',
 'party': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20 9 6l9 9-14 5Z"/><path d="M14 4v2M19 9h2M17 3l-1 2M20 6l-2 1"/></svg>',
 'rings': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="14" r="5"/><circle cx="15" cy="14" r="5"/><path d="m10 6 2-3 2 3"/></svg>',
 'box': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7l9-4 9 4-9 4-9-4Z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/></svg>',
 'shield': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg>',
 'snow': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v20M3.3 7l17.4 10M3.3 17 20.7 7"/></svg>',
 'lock': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
 'bag': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 8h12l-1 13H7L6 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
 'phonedl': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/></svg>',
 'clock': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 'serve': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 18h18M5 18a7 7 0 0 1 14 0M12 8V6M10 6h4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 'play': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5v17l14-8.5-14-8.5Z"/></svg>',
}
def ticklist(items, cls='plan__list'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{I["tick"]}<span>{x}</span></li>' for x in items) + '</ul>'

# ---------------------------------------------------------------- shared blocks
def json_ld(graph):
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    return '<script type="application/ld+json">\n' + data.replace('</', '<\\/') + '\n</script>'

ORG = {'@type': 'Organization', '@id': BASE + '/#organization', 'name': 'Messify', 'legalName': 'Messify FZC', 'url': BASE + '/',
       'logo': LOGO, 'email': EMAIL, 'telephone': PHONE_TEL, 'sameAs': [IG, APP_STORE, GOOGLE_PLAY], 'description': ONE_LINER}
BUSINESS = {
    '@type': 'FoodEstablishment', '@id': BASE + '/#business', 'name': 'Messify', 'url': BASE + '/',
    'image': OG_IMAGE, 'logo': LOGO, 'telephone': PHONE_TEL, 'email': EMAIL,
    'description': ONE_LINER, 'priceRange': 'AED 25.63–30.71 per meal',
    'address': {'@type': 'PostalAddress', 'addressLocality': 'International City', 'addressRegion': 'Dubai', 'addressCountry': 'AE'},
    'areaServed': [{'@type': 'Place', 'name': n} for n in PLACES.values()] + [{'@type': 'City', 'name': c} for c in ('Dubai', 'Sharjah', 'Ajman', 'Abu Dhabi')],
    'openingHoursSpecification': HOURS_SPEC,
    'sameAs': [IG, APP_STORE, GOOGLE_PLAY],
}
WEBSITE = {'@type': 'WebSite', '@id': BASE + '/#website', 'url': BASE + '/', 'name': 'Messify', 'inLanguage': 'en-AE', 'publisher': {'@id': BASE + '/#organization'}}

def offer_catalog():
    return {'@type': 'OfferCatalog', 'name': 'Messify meal plans', 'itemListElement': [
        {'@type': 'Offer', 'name': f'{mlabel(m)}, {ln}', 'price': str(p), 'priceCurrency': 'AED',
         'description': f'{t} meals (tokens): {7 if ln == "weekly" else 26} days of meals to use within {9 if ln == "weekly" else 30} days. AED {per(p, t)} per meal.',
         'url': BASE + '/meal-plans/#plans'} for m, ln, t, p in PLANS]}

def faq_schema(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}

def crumbs(items):
    """items: list of (name, path). Last item is the current page."""
    lis = []
    for i, (n, p) in enumerate(items):
        if i == len(items) - 1: lis.append(f'<li aria-current="page">{n}</li>')
        else: lis.append(f'<li><a href="{p}">{n}</a></li>')
    htmlc = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + ''.join(lis) + '</ol></nav>'
    schema = {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + p} for i, (n, p) in enumerate(items)]}
    return htmlc, schema

def faq_html(faqs, open_first=True):
    out = []
    for i, (q, a) in enumerate(faqs):
        out.append(f'<details{" open" if (i == 0 and open_first) else ""}><summary><h3>{esc(q)}</h3></summary><p>{esc(a)}</p></details>')
    return '<div class="faq">' + ''.join(out) + '</div>'

def contact_lines():
    return f'''<div class="contact-lines">
  <div><span class="ci">{I["phone"]}</span><small>Phone &amp; WhatsApp</small><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div>
  <div><span class="ci">{I["mail"]}</span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  <div><span class="ci">{I["clock"]}</span><small>Open</small><b>{HOURS_LABEL}</b></div>
</div>'''

def ver(rel):
    """Short content hash so browsers fetch a changed stylesheet or script straight away."""
    import hashlib
    return hashlib.md5(open(os.path.join(DIST, rel.lstrip('/')), 'rb').read()).hexdigest()[:8]

def head(page):
    url = BASE + page['path']
    robots = '<meta name="robots" content="noindex, follow">' if page.get('noindex') else '<meta name="robots" content="index, follow, max-image-preview:large">'
    theme = '#120F0D' if page['mode'] == 'catering' else '#FAF6EE'
    preload = page.get('preload', '')
    links = '' if page.get('file') else f'<link rel="canonical" href="{url}">\n<link rel="alternate" hreflang="en-AE" href="{url}">\n<link rel="alternate" hreflang="x-default" href="{url}">'
    return f'''<!doctype html>
<html lang="en-AE" data-mode="{page['mode']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['desc'])}">
{links}
{robots}
<meta name="theme-color" content="{theme}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Messify">
<meta property="og:locale" content="en_AE">
<meta property="og:title" content="{esc(page.get('og_title', page['title']))}">
<meta property="og:description" content="{esc(page['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Two Messify meal bowls in a branded Messify delivery bag">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page.get('og_title', page['title']))}">
<meta name="twitter:description" content="{esc(page['desc'])}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&amp;family=Poppins:wght@400;500;600;700&amp;display=swap">
{preload}<link rel="stylesheet" href="/assets/css/site.css?v={ver('/assets/css/site.css')}">
{json_ld(page['schema'])}
</head>'''

def header(page):
    mode = page['mode']
    cur = page.get('nav')  # 'meals' | 'catering' | None
    def a(href, label, key):
        attr = ''
        if cur == key and page.get('exact'): attr = ' aria-current="page"'
        elif mode == ('catering' if key == 'catering' else 'meals'): attr = ' class="is-on"'
        return f'<a href="{href}"{attr}>{label}</a>'
    cta = page.get('cta', ('/start/', 'Start my plan', 'Start'))
    return f'''<header class="bar">
  <div class="wrap bar__in">
    <a class="bar__logo" href="/" aria-label="Messify home"><span class="mark"></span></a>
    <nav class="switch" aria-label="Services">
      <span class="switch__thumb" aria-hidden="true"></span>
      {a('/meal-plans/', 'Meal plans', 'meals')}{a('/catering/', 'Catering', 'catering')}
    </nav>
    <div class="bar__end"><a class="btn btn--sm" href="{cta[0]}"{f' data-messibot="{page["cta_bot"]}"' if page.get("cta_bot") else ''}><span class="cta-long">{cta[1]}</span><span class="cta-short">{cta[2]}</span></a></div>
  </div>
</header>'''

FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div><span class="mark" role="img" aria-label="Messify"></span><p>Daily meal plans and event catering in Dubai. Cooked fresh every day in International City.</p></div>
      <div><h2>Meal plans</h2><ul>
        <li><a href="/meal-plans/">Meal plans &amp; prices</a></li>
        <li><a href="/meal-plans/academic-city/">Academic City</a></li>
        <li><a href="/meal-plans/silicon-oasis/">Silicon Oasis</a></li>
        <li><a href="/meal-plans/international-city/">International City</a></li>
      </ul></div>
      <div><h2>Catering</h2><ul>
        <li><a href="/catering/">Catering services</a></li>
        <li><a href="/catering/#menu-builder">Build your menu</a></li>
        <li><a href="/catering/#quote">Get a quote</a></li>
      </ul></div>
      <div><h2>Company</h2><ul>
        <li><a href="/about/">About Messify</a></li>
        <li><a href="/meal-plans/#contact">Contact us</a></li>
        <li><a href="/terms/">Terms &amp; conditions</a></li>
        <li><a href="/privacy/">Privacy</a></li>
      </ul></div>
      <div><h2>Contact</h2><ul>
        <li><a class="with-ico" href="tel:{PHONE_TEL}">{I["phone"]}{PHONE_DISPLAY}</a></li>
        <li><a class="with-ico" href="mailto:{EMAIL}">{I["mail"]}{EMAIL}</a></li>
        <li><a class="with-ico" href="{IG}" target="_blank" rel="noopener" aria-label="Messify on Instagram, @messify.me">{I["insta"]}@messify.me</a></li>
        <li><span class="with-ico">{I["clock"]}{HOURS_LABEL}</span></li>
      </ul></div>
    </div>
    <div class="foot__base"><span>© <span data-year>2026</span> Messify. International City, Dubai, UAE.</span><span><a href="{APP_STORE}" target="_blank" rel="noopener">App Store</a> · <a href="{GOOGLE_PLAY}" target="_blank" rel="noopener">Google Play</a></span></div>
  </div>
</footer>'''

def render(page, body):
    out = head(page) + f'''
<body class="{page.get('body_class', '')}">
<a class="skip" href="#content">Skip to content</a>
{page.get('pre', '')}
{header(page)}
<main id="content">
{body}
</main>
{FOOTER}
<script src="/assets/js/site.js?v={ver('/assets/js/site.js')}" defer></script>
<script src="/assets/js/messibot.js?v={ver('/assets/js/messibot.js')}" defer></script>
</body>
</html>
'''
    path = os.path.join(DIST, page['path'].strip('/'), 'index.html') if page['path'] != '/' else os.path.join(DIST, 'index.html')
    if page.get('file'): path = os.path.join(DIST, page['file'])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: f.write(out)
    print('wrote', os.path.relpath(path, DIST))

# ---------------------------------------------------------------- reusable sections
def plan_cards():
    cards = [
        (1, False, 'AED 715', 'AED 27.50 per meal', '26 tokens · 26 days of meals, use within 30 days', ['Lunch only, or any meal you pick', 'Skip a day, have it later in your plan']),
        (2, True,  'AED 1,400', 'AED 26.92 per meal', '52 tokens · 26 days of meals, use within 30 days', ['Lunch and dinner, sorted', 'Skip a day, have it later in your plan']),
        (3, False, 'AED 1,999', 'AED 25.63 per meal', '78 tokens · 26 days of meals, use within 30 days', ['Breakfast, lunch and dinner in one bag', 'Best price per meal']),
    ]
    out = []
    for m, pop, price, perm, tok, extra in cards:
        coins = ''.join('<img src="/assets/img/coin.webp" alt="" width="42" height="39">' for _ in range(m))
        badge = '<span class="plan__badge">Most popular</span>' if pop else ''
        items = ''.join(f'<li>{I["tick"]}<span>{x}</span></li>' for x in extra)
        out.append(f'''<article class="plan{' plan--pop' if pop else ''}" data-plan="{m}">
  {badge}<div class="coins">{coins}</div>
  <h3 class="plan__name">{mlabel(m)}</h3>
  <div class="plan__price"><b data-price>{price}</b><span data-unit>/ month</span></div>
  <p class="plan__per" data-per>{perm}</p>
  <ul class="plan__list"><li>{I["tick"]}<span data-tokens>{tok}</span></li>{items}</ul>
  <a class="btn" href="/start/?meals={m}&amp;duration=monthly" data-start-meals="{m}">Start with {m} meal{'s' if m > 1 else ''}</a>
</article>''')
    return '<div class="plans">' + ''.join(out) + '</div>'

def plans_table(caption='All Messify meal plans and prices'):
    rows = ''.join(f'<tr><th scope="row">{mlabel(m)}</th><td>{ln.capitalize()}</td><td class="num">{t}</td><td class="num">{aed(p)}</td><td class="num">AED {per(p, t)}</td></tr>' for m, ln, t, p in PLANS)
    return f'''<div class="table-wrap"><table class="ptable">
  <caption>{caption}</caption>
  <thead><tr><th scope="col">Plan</th><th scope="col">Length</th><th scope="col" class="num">Meals</th><th scope="col" class="num">Price</th><th scope="col" class="num">Per meal</th></tr></thead>
  <tbody>{rows}</tbody>
</table></div>'''

def plans_section(title='Pick a plan in ten seconds.', with_table=True):
    table = f'<details class="more"><summary>Compare all six plans</summary>{plans_table()}</details>' if with_table else ''
    return f'''<section class="sec sec--tint" id="plans" aria-labelledby="plans-title">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Plans &amp; prices</p>
      <h2 class="h2" id="plans-title">{title}</h2>
      <p class="lede">Every meal on your plan is one token. Use them for breakfast, lunch or dinner, any way you like. Try us out on a weekly meal plan, or go monthly for the best price per meal.</p>
    </div>
    <div class="toggle" role="group" aria-label="Plan length">
      <button type="button" data-dur="weekly" aria-pressed="false">Weekly</button>
      <button type="button" data-dur="monthly" aria-pressed="true">Monthly <span class="save">Best value</span></button>
    </div>
    {plan_cards()}
    <p class="fine">Prices in AED. Monthly plans are 26 days of meals to use within 30 days. Weekly plans are 7 days of meals to use within 9 days. Price per meal = plan price ÷ tokens.</p>
    {table}
  </div>
</section>'''

def meal_form(area_default='', heading='Talk to us.', lede="Have a question before you start? Tell us which plan you're considering and we'll get back to you, usually on WhatsApp.", tint=True):
    areas = ['Dubai Academic City', 'Dubai Silicon Oasis', 'International City', 'Somewhere else (join the waitlist)']
    opts = ''.join(f'<option{" selected" if a == area_default else ""}>{a}</option>' for a in areas)
    return f'''<section class="sec{' sec--tint' if tint else ''}" id="contact" aria-labelledby="contact-title">
  <div class="wrap form-grid">
    <div>
      <p class="eyebrow">Contact us</p>
      <h2 class="h2" id="contact-title">{heading}</h2>
      <p class="lede">{lede}</p>
      {contact_lines()}
    </div>
    <div>
      <form class="form" data-form="meal" data-done="contactDone" data-wa-intro="Hi Messify, I have a question about meal plans." novalidate>
        <input type="hidden" name="_subject" value="New meal plan enquiry from messify.me">
        <div class="row">
          <div class="field"><label for="c-name">Your name</label><input id="c-name" name="name" data-label="Name" autocomplete="name" placeholder="Sara Khan" required><span class="err" aria-live="polite"></span></div>
          <div class="field"><label for="c-phone">Phone number (WhatsApp)</label><input id="c-phone" name="phone" data-label="Phone (WhatsApp)" type="tel" inputmode="tel" autocomplete="tel" placeholder="+971 50 000 0000" required><span class="err" aria-live="polite"></span></div>
        </div>
        <fieldset class="field">
          <legend>Meals a day</legend>
          <div class="seg seg--3">
            <label><input type="radio" name="meals" data-label="Meals a day" value="1 meal a day" id="c-m1"><span>1 meal</span></label>
            <label><input type="radio" name="meals" data-label="Meals a day" value="2 meals a day" id="c-m2" checked><span>2 meals</span></label>
            <label><input type="radio" name="meals" data-label="Meals a day" value="3 meals a day" id="c-m3"><span>3 meals</span></label>
          </div>
        </fieldset>
        <fieldset class="field">
          <legend>Plan length</legend>
          <div class="seg">
            <label><input type="radio" name="length" data-label="Plan length" value="Weekly" id="c-weekly"><span>Weekly</span></label>
            <label><input type="radio" name="length" data-label="Plan length" value="Monthly" id="c-monthly" checked><span>Monthly</span></label>
          </div>
        </fieldset>
        <div class="field"><label for="c-area">Your area</label><select id="c-area" name="area" data-label="Area">{opts}</select></div>
        <div class="field"><label for="c-note">Note <span class="opt-tag">(optional)</span></label><textarea id="c-note" name="note" data-label="Note" placeholder="Your building, start date or any questions"></textarea></div>
        <div class="hp" aria-hidden="true"><label for="c-web">Leave this empty</label><input id="c-web" name="website" tabindex="-1" autocomplete="off"></div>
        <button class="btn" type="submit">Send message</button>
        <p class="form-status" role="alert"></p>
      </form>
      <div class="form form-done" id="contactDone" tabindex="-1" hidden>
        <span class="tick">{I["tick"]}</span>
        <h3 data-done-title>Thanks, we've got it.</h3>
        <p>We'll get back to you on WhatsApp or by phone shortly.</p>
        <a class="btn btn--ghost" data-done-wa href="{WA}" target="_blank" rel="noopener">Want a faster reply? Message us on WhatsApp</a>
      </div>
    </div>
  </div>
</section>'''

QUOTES = [
    ("The food was better than expected and the quantity was perfect, enough to fully satisfy my hunger. Thank you!", 'Yasir Ahmed'),
    ("I got the chicken biryani and loved it. The taste was perfect, and it was the right level of spiciness.", 'Charles Wiley'),
    ("Loved the food. Surprisingly, the box was completely full, and I'm full from the crazy quantity. Thank you.", 'Sara Fatima'),
]
def quotes_block(heading_tag='h2', title='Straight from our WhatsApp chats.'):
    items = ''.join(f'<figure class="quote"><blockquote><p>{esc(q)}</p></blockquote><figcaption><b>{who}</b><span>Meal plan customer · via WhatsApp</span></figcaption></figure>' for q, who in QUOTES)
    return f'''<div class="quotes-head"><p class="eyebrow">From our customers</p><{heading_tag} class="h2" id="quotes-title">{title}</{heading_tag}></div>
    <div class="quotes">{items}</div>'''

def band(title='You planned it right.', text='Tomorrow\'s meals are one tap away. Plans from AED 25 a meal.'):
    return f'''<section class="sec">
  <div class="wrap">
    <div class="band band--sky">
      <div><h2 class="h2">{title}</h2><p class="lede">{text}</p></div>
      <div class="actions" style="margin-top:0">
        <a class="btn" href="/start/">Start my plan</a>
        <a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp us</a>
      </div>
    </div>
  </div>
</section>'''

def areas_cards(exclude=None, heading_level='h3'):
    data = [
        ('academic-city', 'Dubai International Academic City', 'Academic City', 'Universities and student residences, including KSK Homes and The Myriad.'),
        ('silicon-oasis', 'Dubai Silicon Oasis', 'Silicon Oasis', 'Offices, residents, RIT Dubai and DSOA University Residence.'),
        ('international-city', 'Home of our partner kitchen', 'International City', 'Every cluster, minutes from where your meals are cooked.'),
    ]
    out = ''.join(f'<a class="area" href="/meal-plans/{s}/"><small>{small}</small><b>Meal plans in {name}</b><span>{line}</span><span class="link-arrow">See the area {I["arrow"]}</span></a>'
                  for s, small, name, line in data if s != exclude)
    return f'<div class="areas">{out}</div>'

FAQ_PRICE = ('How much does a meal plan cost in Dubai with Messify?',
             'Weekly plans cost AED 215, 415 or 610 for 1, 2 or 3 meals a day. Monthly plans cost AED 715, 1,400 or 1,999. That works out to AED 25.63 to 30.71 per meal.')
FAQ_AREAS = ('Which areas do you deliver meal plans to?',
             'We deliver meal plans every morning to three areas: Dubai Academic City, Dubai Silicon Oasis and International City. Message us on WhatsApp to check your building.')
FAQ_START = ('How do I start a meal plan?',
             'Download the Messify app, pick your plan and pay in the app. Prefer to talk first? Message us on WhatsApp at +971 50 251 3033.')
FAQ_SKIP = ('Can I skip a day?', 'Yes. Skip a day in the app and use that token on another day of your plan.')

# ================================================================= PAGES
def page_home():
    faqs = [FAQ_PRICE, FAQ_AREAS,
            ('Do you cater parties and events?', 'Yes. We cater corporate events, office lunches, parties and home events, university events, weddings and bulk orders across Dubai, Sharjah, Ajman and Abu Dhabi. Every menu is custom and priced by headcount.'),
            FAQ_START]
    page = {
        'path': '/', 'mode': 'meals', 'nav': None, 'body_class': 'has-gate',
        'title': 'Messify | Meal Plans & Catering in Dubai',
        'og_title': 'Messify | Daily meal plans and catering in Dubai',
        'desc': 'Daily meal plans in Dubai from AED 25 a meal, delivered every morning in one chilled bag. Plus custom catering across Dubai, Sharjah and Abu Dhabi.',
        'preload': '<link rel="preload" as="image" href="/assets/img/bag-bowls-640.webp" imagesrcset="/assets/img/bag-bowls-640.webp 640w, /assets/img/bag-bowls.webp 1100w" imagesizes="(min-width: 900px) 50vw, 100vw">\n',
        'schema': [ORG, WEBSITE, BUSINESS, faq_schema(faqs)],
    }
    page['pre'] = f'''<section class="gate" aria-label="Choose meal plans or catering">
  <div class="gate__inner">
    <a class="door door--meals" href="/meal-plans/">
      <img src="/assets/img/bag-bowls-640.webp" srcset="/assets/img/bag-bowls-640.webp 640w, /assets/img/bag-bowls.webp 1100w" sizes="(min-width: 900px) 50vw, 100vw" alt="Messify delivery bag holding two kebab rice bowls, with branded Messify boxes behind" width="1100" height="1650" fetchpriority="high">
      <div class="door__shade"></div>
      <div class="door__copy">
        <div class="door__tag">For every day</div>
        <p class="door__title">Meal plans</p>
        <p class="door__text">Breakfast, lunch and dinner delivered together every morning. From AED 25 a meal.</p>
        <span class="door__cta">Explore meal plans {I["arrow"]}</span>
      </div>
    </a>
    <a class="door door--catering" href="/catering/">
      <img src="/assets/img/cat-chef-640.webp" srcset="/assets/img/cat-chef-640.webp 640w, /assets/img/cat-chef.webp 1024w" sizes="(min-width: 900px) 50vw, 100vw" alt="A chef carving at a buffet station while guests serve themselves at an evening event" width="1024" height="1024">
      <div class="door__shade"></div>
      <div class="door__copy">
        <div class="door__tag">For events</div>
        <p class="door__title">Catering</p>
        <p class="door__text">Corporate, party, university and wedding catering across Dubai, Sharjah, Ajman and Abu Dhabi.</p>
        <span class="door__cta">Explore catering {I["arrow"]}</span>
      </div>
    </a>
    <div class="gate__seam" aria-hidden="true"></div>
    <div class="gate__brand"><span class="mark" role="img" aria-label="Messify"></span><p>Daily meals simplified</p></div>
    <div class="gate__cue" aria-hidden="true">Scroll<span></span></div>
  </div>
</section>'''
    body = f'''<section class="sec">
  <div class="wrap">
    <div class="sec-head" style="max-width:820px">
      <p class="eyebrow">Messify · Dubai</p>
      <h1 class="h2">Meal plans and catering in Dubai.</h1>
      <p class="lede">Fresh, balanced meals are cooked every day in our partner kitchen in International City. With daily meal delivery, subscribers get breakfast, lunch and dinner together each morning across Dubai Academic City, Silicon Oasis and International City. For events, we cater anything from a house party to a wedding across Dubai, Sharjah, Ajman and Abu Dhabi.</p>
    </div>
    <div class="duo">
      <a class="card-link" href="/meal-plans/">
        <div class="photo"><img src="/assets/img/bag-sofa-640.webp" srcset="/assets/img/bag-sofa-640.webp 640w, /assets/img/bag-sofa.webp 900w" sizes="(min-width: 860px) 50vw, 100vw" alt="A steaming meal bowl beside a Messify bag and a Certified Chill ice pack" width="900" height="1350" loading="lazy" style="object-position:50% 62%"></div>
        <div class="card-link__body">
          <p class="eyebrow" style="margin:0">Meal plans</p>
          <h3 class="h3">Your meals, handled.</h3>
          {ticklist(['From AED 25 a meal, weekly or monthly', 'New menu every day, see it a day ahead', 'Skip a day, have it later in your plan'], 'x')}
          <span class="link-arrow">Explore meal plans {I["arrow"]}</span>
        </div>
      </a>
      <a class="card-link card-link--dark" href="/catering/">
        <div class="photo"><img src="/assets/img/cat-serving-640.webp" srcset="/assets/img/cat-serving-640.webp 640w, /assets/img/cat-serving.webp 1100w" sizes="(min-width: 860px) 50vw, 100vw" alt="A gloved server lifting the lid of a chafing dish at a catered buffet" width="1100" height="1375" loading="lazy"></div>
        <div class="card-link__body">
          <p class="eyebrow" style="margin:0;color:#D8B48A">Catering</p>
          <h3 class="h3">Your event, fed properly.</h3>
          {ticklist(['Corporate, parties, university events, weddings', 'Fully customisable menus, quoted by headcount', 'Dubai, Sharjah, Ajman and Abu Dhabi'], 'x')}
          <span class="link-arrow">Explore catering {I["arrow"]}</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="areas-title">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Where we deliver</p>
      <h2 class="h2" id="areas-title">Meal plans delivered every morning, close to where they're cooked.</h2>
    </div>
    {areas_cards()}
  </div>
</section>

<section class="sec" aria-labelledby="glance-title">
  <div class="wrap split split--top">
    <div class="sec-head">
      <p class="eyebrow">At a glance</p>
      <h2 class="h2" id="glance-title">What is Messify?</h2>
    </div>
    <div class="answer">
      <p class="answer__label">Quick answer</p>
      <p class="answer__lead">{ONE_LINER}</p>
      <table class="facts-table">
        <tr><th scope="row">Meal plan prices</th><td>AED 215–610 a week or AED 715–1,999 a month (AED 25.63–30.71 per meal)</td></tr>
        <tr><th scope="row">Delivery</th><td>Every morning, all the day's meals in one chilled bag</td></tr>
        <tr><th scope="row">Food</th><td>Balanced and 100% halal, with a new menu every day</td></tr>
        <tr><th scope="row">Vegetarian</th><td>A vegetarian option every day, for every meal</td></tr>
        <tr><th scope="row">Flexibility</th><td>1 meal = 1 token. Skip a day and use the token later in your plan.</td></tr>
        <tr><th scope="row">Meal plan areas</th><td>Dubai Academic City, Dubai Silicon Oasis, International City</td></tr>
        <tr><th scope="row">Catering areas</th><td>Dubai, Sharjah, Ajman and Abu Dhabi</td></tr>
      </table>
      <a class="link-arrow" href="/about/">More about Messify {I["arrow"]}</a>
    </div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="quotes-title">
  <div class="wrap">{quotes_block()}</div>
</section>

<section class="sec" aria-labelledby="faq-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-title">Good to know.</h2></div>
    {faq_html(faqs)}
  </div>
</section>
{band()}'''
    render(page, body)

def page_meal_plans():
    faqs = [FAQ_PRICE,
            ("What's the difference between weekly and monthly plans?", 'Monthly plans are 26 days of meals to use within 30 days, and save you more on every meal. Weekly plans are 7 days of meals to use within 9 days, the easy way to try us out first.'),
            FAQ_SKIP,
            ('Can I order extra meals?', 'Yes. Two lunches in one day, or a friend coming over? Spend an extra token.'),
            ('When do meals arrive?', "Every morning, all together in one Messify bag with an ice pack. Meals are blast-chilled, so you reheat them when you're ready to eat."),
            ('Can I see the menu in advance?', "Yes. The menu changes every day, and tomorrow's menu is in the app the day before. Choose your meals by 6 PM for next-morning delivery."),
            ('Is Messify food halal?', 'Yes. All Messify meals are 100% halal.'),
            ('Do you have vegetarian meals?', 'Yes. There is a vegetarian option every day, for every meal: breakfast, lunch and dinner.'),
            FAQ_AREAS, FAQ_START]
    cr, crs = crumbs([('Home', '/'), ('Meal plans', '/meal-plans/')])
    service = {'@type': 'Service', '@id': BASE + '/meal-plans/#service', 'name': 'Messify meal plans', 'serviceType': 'Meal plan delivery',
               'description': 'Daily meal plans in Dubai: 1, 2 or 3 fresh meals a day, delivered together every morning, weekly or monthly.',
               'provider': {'@id': BASE + '/#business'}, 'areaServed': [{'@type': 'Place', 'name': n} for n in PLACES.values()],
               'hasOfferCatalog': offer_catalog()}
    page = {
        'path': '/meal-plans/', 'mode': 'meals', 'nav': 'meals', 'exact': True,
        'title': 'Meal Plans in Dubai, Weekly & Monthly | Messify',
        'desc': 'Affordable weekly and monthly meal plans in Dubai. 1, 2 or 3 meals a day from AED 715 a month, delivered every morning. Skip a day, have it later.',
        'preload': '<link rel="preload" as="image" href="/assets/img/bag-sofa-640.webp" imagesrcset="/assets/img/bag-sofa-640.webp 640w, /assets/img/bag-sofa.webp 900w" imagesizes="(min-width: 900px) 45vw, 100vw">\n',
        'schema': [ORG, BUSINESS, service, faq_schema(faqs), crs],
    }
    body = f'''<section class="sec sec--first">
  <div class="wrap split">
    <div>
      {cr}
      <h1 class="h2 rise"><span class="kicker">Meal plans in Dubai</span> Your meals, handled.</h1>
      <p class="lede rise">Fresh, balanced, 100% halal meals cooked daily in our partner kitchen in International City and delivered together each morning in one chilled Messify bag. Skip a day and have it later in your plan.</p>
      <div class="actions">
        <a class="btn" href="#plans">See plans &amp; prices</a>
        <a class="btn btn--ghost" href="#how">How it works</a>
      </div>
      <div class="facts">
        <div><b>From AED 25</b><span>per meal</span></div>
        <div><b>Every morning</b><span>all your meals in one bag</span></div>
        <div><b>Daily</b><span>new menu, see it a day ahead</span></div>
      </div>
    </div>
    <div class="photo photo--tall">
      <img src="/assets/img/bag-sofa-640.webp" srcset="/assets/img/bag-sofa-640.webp 640w, /assets/img/bag-sofa.webp 900w" sizes="(min-width: 900px) 45vw, 100vw" alt="A steaming meal bowl beside a Messify bag and a Certified Chill ice pack on a coffee table" width="900" height="1350" fetchpriority="high">
    </div>
  </div>
</section>

{plans_section()}

<section class="sec sec--tight" aria-label="Quick answer">
  <div class="wrap">
    <div class="answer">
      <p class="answer__label">Quick answer</p>
      <p class="answer__lead">Messify is an affordable meal subscription in Dubai. Plans cost AED 215–610 a week or AED 715–1,999 a month for 1 to 3 meals a day, which works out to AED 25.63–30.71 per meal. All of the day's meals arrive together every morning, and you can skip a day and use that meal later in your plan.</p>
    </div>
  </div>
</section>

<section class="sec" id="how" aria-labelledby="how-title">
  <div class="wrap split split--rev">
    <div class="photo photo--tall">
      <img src="/assets/img/one-less-thing.webp" alt="Messify poster reading One less thing to think about, your meals handled, with a chicken and vegetable rice bowl beside a laptop" width="900" height="1125" loading="lazy">
    </div>
    <div>
      <div class="sec-head"><p class="eyebrow">How it works</p><h2 class="h2" id="how-title">Your mornings, sorted in four steps.</h2></div>
      <ol class="steps">
        <li><div><h3>Pick your plan</h3><p>1, 2 or 3 meals a day, weekly or monthly.</p></div></li>
        <li><div><h3>Check tomorrow's menu</h3><p>The menu changes every day. See it in the app and choose your meals by 6 PM.</p></div></li>
        <li><div><h3>Get your bag</h3><p>All your meals arrive together each morning, packed with an ice pack.</p></div></li>
        <li><div><h3>Heat and eat</h3><p>Meals are blast-chilled after cooking. A few minutes to reheat and you're done.</p></div></li>
      </ol>
    </div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="tokens-title">
  <div class="wrap token-grid">
    <div>
      <div class="sec-head"><p class="eyebrow">The token system</p><h2 class="h2" id="tokens-title">Plans change. Your meals don't go to waste.</h2></div>
      <div class="token-cards">
        <div class="tcard"><img src="/assets/img/coin.webp" alt="" width="52" height="48" loading="lazy"><div><h3>1 meal = 1 token</h3><p>Your plan fills your wallet: 7, 14 or 21 tokens a week, or 26, 52 or 78 a month.</p></div></div>
        <div class="tcard"><img src="/assets/img/coin.webp" alt="" width="52" height="48" loading="lazy"><div><h3>Skip a day, eat it later</h3><p>Travelling or eating out? Skip in the app and use that token on another day of your plan.</p></div></div>
        <div class="tcard"><img src="/assets/img/coin.webp" alt="" width="52" height="48" loading="lazy"><div><h3>Double up when you need to</h3><p>Two lunches today, or a friend coming over? Spend an extra token.</p></div></div>
      </div>
    </div>
    <div class="ledger" role="group" aria-label="Example token wallet">
      <div class="ledger__head"><b>Example wallet</b><span>2 meals a day · monthly</span></div>
      <table>
        <tbody>
          <tr><td>Plan starts</td><td class="plus">+52</td><td>52</td></tr>
          <tr><td>Mon<span class="note">Lunch and dinner</span></td><td>−2</td><td>50</td></tr>
          <tr><td>Tue<span class="note">Skipped, out of town</span></td><td class="zero">0</td><td>50</td></tr>
          <tr><td>Wed<span class="note">Lunch, dinner, one for a friend</span></td><td>−3</td><td>47</td></tr>
        </tbody>
        <tfoot><tr><td>Tokens left</td><td></td><td>47</td></tr></tfoot>
      </table>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="menu-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">On the menu</p><h2 class="h2" id="menu-title">A new menu every day. <span class="sample">Sample dishes</span></h2><p class="lede">Healthy, balanced home-style meals, with a different menu every day so the week never gets repetitive. There's a vegetarian option every day, for every meal.</p></div>
    <div class="dishes">
      <article class="dish"><div class="photo"><img src="/assets/img/biryani.webp" alt="Paneer makhani with saffron rice" width="1600" height="1181" loading="lazy"></div><div class="dish__body"><span class="dish__tag">Indian</span><h3>Paneer makhani with saffron rice</h3><p>Soft paneer in a rich tomato gravy.</p></div></article>
      <article class="dish"><div class="photo"><img src="/assets/img/stroganoff.webp" alt="Creamy chicken with peppers and herb rice" width="1200" height="885" loading="lazy"></div><div class="dish__body"><span class="dish__tag">Continental</span><h3>Creamy chicken with herb rice</h3><p>Peppers and mushrooms in a light cream sauce.</p></div></article>
      <article class="dish"><div class="photo"><img src="/assets/img/pasta-dish.webp" alt="Grilled chicken over creamy penne with parmesan" width="780" height="585" loading="lazy"></div><div class="dish__body"><span class="dish__tag">Continental</span><h3>Grilled chicken penne</h3><p>Finished with parmesan and parsley.</p></div></article>
      <article class="dish"><div class="photo"><img src="/assets/img/wrap.webp" alt="A fresh garden wrap with roast potatoes" width="900" height="1380" loading="lazy" style="object-position:50% 60%"></div><div class="dish__body"><span class="dish__tag">Wraps</span><h3>Garden wrap with roast potatoes</h3><p>Crisp lettuce, tomato and cucumber.</p></div></article>
    </div>
    {quotes_block('h3', 'What customers say.')}
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="chill-title">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Certified Chill.</p>
      <h2 class="h2" id="chill-title">Made fresh. Kept cold. Delivered safe.</h2>
      <ul class="ticks">
        <li><span class="ico-wrap">{I["shield"]}</span><div><b>Prepared with gloved hands</b><span>Every meal is plated by the kitchen team.</span></div></li>
        <li><span class="ico-wrap">{I["snow"]}</span><div><b>Blast-chilled after cooking</b><span>Locks in freshness until you reheat.</span></div></li>
        <li><span class="ico-wrap">{I["lock"]}</span><div><b>Sealed in kraft bowls</b><span>Closed at the kitchen, opened by you.</span></div></li>
        <li><span class="ico-wrap">{I["bag"]}</span><div><b>Packed cold</b><span>A Certified Chill. ice pack goes in every bag.</span></div></li>
      </ul>
    </div>
    <div class="photo" style="aspect-ratio:1000/844"><img src="/assets/img/fresh-chill.webp" alt="A chicken and vegetable bowl on a desk next to a laptop, a coffee and a blue Certified Chill ice pack" width="1000" height="844" loading="lazy"></div>
  </div>
</section>

<section class="sec" aria-labelledby="where-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Where we deliver</p><h2 class="h2" id="where-title">Delivered every morning, close to where it's cooked.</h2>
      <p class="lede">Daily meal delivery to three areas: Academic City, Silicon Oasis and International City. Meals are cooked in International City and arrive every morning.</p></div>
    {areas_cards()}
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="faq-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-title">Good to know.</h2>
      <a class="link-arrow" href="#contact" data-messibot="meals" style="margin-top:18px">Ask a question {I["arrow"]}</a></div>
    {faq_html(faqs)}
  </div>
</section>

{meal_form(tint=False)}
{band()}'''
    render(page, body)

# ---------------------------------------------------------------- area pages
AREAS = {
 'academic-city': {
  'name': 'Academic City', 'place': 'Dubai International Academic City', 'kicker': 'Dubai International Academic City (DIAC)',
  'title': 'Meal Plans in Dubai Academic City (DIAC) | Messify',
  'desc': 'Student meal plans delivered every morning to universities and residences in Dubai Academic City, including KSK Homes and The Myriad. From AED 25 a meal.',
  'h1': 'Meal plans in Academic City.',
  'lede': 'Student meal plans and fresh daily meals for staff across Dubai International Academic City, delivered every morning to your residence or campus. Cooked daily in our partner kitchen in nearby International City.',
  'facts': [('From AED 25', 'per meal'), ('Every morning', 'to your residence or campus'), ('Skip a day', 'have it later in your plan')],
  'img': ('bag-bowls-640.webp', 'bag-bowls.webp', 1100, 1650, 'A Messify bag holding two kebab rice bowls, ready for delivery', '50% 40%'),
  'where_title': 'Where we deliver in Academic City.',
  'groups': [
    ('cap', 'Universities', ['University of Birmingham Dubai', 'Manipal Academy of Higher Education, Dubai', 'BITS Pilani, Dubai Campus', 'Amity University Dubai', 'Middlesex University Dubai, Academic City campus', 'Curtin University Dubai'], 'And other campuses across DIAC'),
    ('home', 'Student accommodation', ['KSK Homes', 'The Myriad'], 'And other student residences in Academic City'),
  ],
  'why_title': 'Why students in Academic City choose Messify.',
  'reasons': [
    ('Priced for students', 'Monthly plans start at AED 715 for a meal a day, and the 3-meal plan works out to AED 25.63 a meal, with nothing to decide each day.'),
    ('Built around the semester', 'Exam week or a long weekend? Skip a day in the app and use that token on another day. Weekly plans fit neatly around trips home.'),
    ('One bag, the whole day', 'Breakfast, lunch and dinner arrive together each morning. No waiting for delivery riders between lectures.'),
  ],
  'faqs': [
    ('Do you deliver to KSK Homes and The Myriad?', 'Yes. We deliver every morning to KSK Homes, The Myriad and other student residences in Dubai International Academic City.'),
    ('Can you deliver to my university in Academic City?', 'Yes. We deliver across DIAC, including University of Birmingham Dubai, Middlesex University Dubai, Manipal Academy of Higher Education, BITS Pilani Dubai Campus and Amity University Dubai. Message us with your building and we will confirm the drop-off point.'),
    ('What happens during exams or semester breaks?', "Skip busy days in the app and use those tokens on other days of your plan. Heading home for the break? Choose a weekly plan, or start your monthly plan when you're back."),
    ('How much is a meal plan for students in Academic City?', 'Weekly plans cost AED 215, 415 or 610 for 1, 2 or 3 meals a day. Monthly plans cost AED 715, 1,400 or 1,999, which is AED 25.63 to 30.71 per meal.'),
  ],
  'form_area': 'Dubai Academic City',
 },
 'silicon-oasis': {
  'name': 'Silicon Oasis', 'place': 'Dubai Silicon Oasis', 'kicker': 'Dubai Silicon Oasis (DSO)',
  'title': 'Meal Plans in Dubai Silicon Oasis (DSO) | Messify',
  'desc': 'Daily meal plans and office lunch delivery in Dubai Silicon Oasis, for teams, residents and RIT Dubai students. From AED 25 a meal.',
  'h1': 'Meal plans in Silicon Oasis.',
  'lede': 'Office lunch delivery, dinner for home and breakfast for the morning rush. We deliver every morning across Dubai Silicon Oasis, from RIT Dubai and DSOA University Residence to the offices and towers around DSO.',
  'facts': [('From AED 25', 'per meal'), ('Every morning', 'to your office or home'), ('Team plans', 'for offices in DSO')],
  'img': ('fresh-chill.webp', 'fresh-chill.webp', 1000, 844, 'A chicken and vegetable bowl on an office desk beside a laptop, coffee and a Certified Chill ice pack', '50% 50%'),
  'where_title': 'Where we deliver in Silicon Oasis.',
  'groups': [
    ('office', 'Offices and residences', ['Offices and business centres across DSO', 'Residential towers and villas in Silicon Oasis'], 'Message us your building to confirm'),
    ('cap', 'Students', ['RIT Dubai', 'DSOA University Residence'], 'And other student housing in DSO'),
  ],
  'why_title': 'Why people in Silicon Oasis choose Messify.',
  'reasons': [
    ('Lunch sorted before work starts', 'Lunch delivery that beats the rush: your meals arrive together every morning, so lunch is handled before the workday gets busy. No more 1 pm delivery queues.'),
    ('Plans for whole teams', 'Feed your office on one monthly plan, with one delivery for everyone. Each person still chooses their meals in the app.'),
    ('Flexible for students', 'RIT Dubai students can skip busy days and use those tokens later in the plan. Weekly plans fit neatly around breaks.'),
  ],
  'faqs': [
    ('Do you deliver to offices in Dubai Silicon Oasis?', 'Yes. We deliver every morning to offices and business centres across DSO, so lunch is sorted before the workday starts.'),
    ('Do you deliver to RIT Dubai and DSOA University Residence?', 'Yes. We deliver every morning to RIT Dubai students, including DSOA University Residence and other student housing in Silicon Oasis.'),
    ('Can our team get a meal plan together?', 'Yes. We offer monthly office meal plans for teams. Message us on WhatsApp with your team size and office location.'),
    ('How much is a meal plan in Silicon Oasis?', 'Weekly plans cost AED 215, 415 or 610 for 1, 2 or 3 meals a day. Monthly plans cost AED 715, 1,400 or 1,999, which is AED 25.63 to 30.71 per meal.'),
  ],
  'form_area': 'Dubai Silicon Oasis',
 },
 'international-city': {
  'name': 'International City', 'place': 'International City, Dubai', 'kicker': 'International City, Dubai',
  'title': 'Meal Plans in International City, Dubai | Messify',
  'desc': 'Cooked in our partner kitchen in International City. Fresh daily meal plans delivered every morning across the clusters, from AED 25 a meal.',
  'h1': 'Cooked right here in International City.',
  'lede': "Messify meals are cooked in our partner kitchen in International City, so they travel the shortest distance of all. Fresh, balanced meals delivered every morning across the clusters.",
  'facts': [('From AED 25', 'per meal'), ('Every morning', 'to every cluster'), ('Cooked here', 'in International City')],
  'img': ('biryani.webp', 'biryani.webp', 1600, 1181, 'Paneer makhani with saffron rice', '50% 50%'),
  'where_title': 'Where we deliver in International City.',
  'groups': [
    ('pin', 'Clusters', ['China and England clusters', 'France, Italy and Greece clusters', 'Russia, Persia and Morocco clusters', 'Spain and Emirates clusters'], 'Message us your cluster and building to confirm'),
    ('home', 'Nearby', ['Dubai Silicon Oasis', 'Dubai Academic City'], 'Both a short drive from International City'),
  ],
  'why_title': 'Why International City chooses Messify.',
  'reasons': [
    ('Cooked next door', 'Your meals are cooked in International City and reach you minutes later, packed cold with an ice pack.'),
    ('Simple monthly budgeting', 'One plan, one price. The 3-meal monthly plan works out to AED 25.63 a meal, with breakfast, lunch and dinner covered.'),
    ('Skip when life happens', 'Away for a day or two? Skip in the app and use those tokens later in your plan.'),
  ],
  'faqs': [
    ('Where are Messify meals cooked?', 'In our partner kitchen in International City, Dubai. Meals are cooked every day and delivered from here each morning.'),
    ('Do you deliver to every cluster in International City?', 'Yes. We deliver across the International City clusters. Message us your cluster and building and we will confirm.'),
    ('Do you also deliver to Silicon Oasis and Academic City?', 'Yes. Both are a short drive from International City and we deliver there every morning.'),
    ('How much is a meal plan in International City?', 'Weekly plans cost AED 215, 415 or 610 for 1, 2 or 3 meals a day. Monthly plans cost AED 715, 1,400 or 1,999, which is AED 25.63 to 30.71 per meal.'),
  ],
  'form_area': 'International City',
 },
}

def page_area(slug):
    a = AREAS[slug]
    path = f'/meal-plans/{slug}/'
    cr, crs = crumbs([('Home', '/'), ('Meal plans', '/meal-plans/'), (a['name'], path)])
    service = {'@type': 'Service', '@id': BASE + path + '#service', 'name': f'Messify meal plans in {a["place"]}',
               'serviceType': 'Meal plan delivery', 'provider': {'@id': BASE + '/#business'},
               'areaServed': {'@type': 'Place', 'name': a['place'], 'containedInPlace': {'@type': 'City', 'name': 'Dubai'}},
               'description': a['desc'], 'hasOfferCatalog': offer_catalog()}
    schema = [ORG, BUSINESS, service, faq_schema(a['faqs']), crs]
    page = {'path': path, 'mode': 'meals', 'nav': 'meals', 'title': a['title'], 'desc': a['desc'], 'schema': schema}
    small, big, w, h, alt, pos = a['img']
    srcset = f' srcset="/assets/img/{small} 640w, /assets/img/{big} {w}w" sizes="(min-width: 900px) 45vw, 100vw"' if small != big else ''
    facts = ''.join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in a['facts'])
    groups = ''
    for ico, title, items, more in a['groups']:
        lis = ''.join(f'<li>{I["tick"]}<span>{x}</span></li>' for x in items) + f'<li class="more">{I["pin"]}<span>{more}</span></li>'
        groups += f'<div class="place-group"><h3>{I[ico]}{title}</h3><ul>{lis}</ul></div>'
    reasons = ''.join(f'<div class="reason"><h3>{t}</h3><p>{d}</p></div>' for t, d in a['reasons'])
    body = f'''<section class="sec sec--first">
  <div class="wrap split">
    <div>
      {cr}
      <h1 class="h2 rise"><span class="kicker">{a['kicker']}</span> {a['h1']}</h1>
      <p class="lede rise">{a['lede']}</p>
      <div class="actions">
        <a class="btn" href="#plans">See plans &amp; prices</a>
        <a class="btn btn--ghost" href="{WA}?text={quote(f"Hi Messify, I'm in {a['name']} and I'd like to know more about your meal plans.")}" target="_blank" rel="noopener">WhatsApp us</a>
      </div>
      <div class="facts">{facts}</div>
    </div>
    <div class="photo photo--tall"><img src="/assets/img/{small}"{srcset} alt="{alt}" width="{w}" height="{h}" fetchpriority="high" style="object-position:{pos}"></div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="where-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Delivery in {a['name']}</p><h2 class="h2" id="where-title">{a['where_title']}</h2>
      <p class="lede">All of the day's meals arrive together every morning in one chilled Messify bag.</p></div>
    <div class="places">{groups}</div>
    <p class="disclaim">Names of universities, residences and buildings are used only to describe where we deliver. Messify is not affiliated with them.</p>
  </div>
</section>

<section class="sec" aria-labelledby="why-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Why Messify</p><h2 class="h2" id="why-title">{a['why_title']}</h2></div>
    <div class="reasons">{reasons}</div>
  </div>
</section>

{plans_section('Meal plans and prices in ' + a['name'] + '.')}

<section class="sec" aria-labelledby="faq-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-title">Good to know.</h2></div>
    {faq_html(a['faqs'])}
  </div>
</section>

<section class="sec sec--tint sec--tight" aria-labelledby="nearby-title">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:28px"><p class="eyebrow">Nearby</p><h2 class="h3" id="nearby-title" style="font-size:1.4rem">We also deliver to</h2></div>
    {areas_cards(exclude=slug)}
  </div>
</section>

{meal_form(area_default=a['form_area'], tint=False, lede=f"Live or work in {a['name']}? Tell us which plan you're considering and we'll get back to you, usually on WhatsApp.")}
{band()}'''
    render(page, body)

# ---------------------------------------------------------------- start
def page_start():
    page = {'path': '/start/', 'mode': 'meals', 'nav': 'meals', 'noindex': True,
            'title': 'Start Your Meal Plan | Messify',
            'desc': 'Start your Messify meal plan in the app, or talk to our team on WhatsApp first.',
            'cta': ('#start-app', 'Get the app', 'App'),
            'schema': [ORG]}
    body = f'''<div data-start-page>
<section class="sec sec--first">
  <div class="wrap">
    <a class="back" href="/meal-plans/#plans">{I["back"]}Back to plans</a>
    <div class="start-hero">
      <div>
        <p class="eyebrow rise">Almost there</p>
        <h1 class="h2 rise">Your bag is almost packed.</h1>
        <p class="lede rise">You've picked your plan. Now choose how you'd like to begin: straight from the Messify app, or with a quick chat with our team on WhatsApp.</p>
      </div>
      <div class="summary" aria-live="polite">
        <div class="summary__top"><small>Your plan</small><div class="coins" data-s-coins></div></div>
        <div>
          <p class="summary__name" data-s-name>2 meals a day · Monthly</p>
          <div class="summary__price"><b data-s-price>AED 1,400</b><span data-s-unit>/ month</span></div>
          <p class="summary__meta" data-s-meta>AED 26.92 per meal · 52 tokens · 26 days of meals, use within 30 days</p>
        </div>
        <div class="summary__edit">
          <fieldset class="mini"><legend>Meals a day</legend>
            <div class="chips" data-s="meals">
              <button type="button" class="chip" data-value="1" aria-pressed="false">1</button>
              <button type="button" class="chip" data-value="2" aria-pressed="true">2</button>
              <button type="button" class="chip" data-value="3" aria-pressed="false">3</button>
            </div>
          </fieldset>
          <fieldset class="mini"><legend>Plan length</legend>
            <div class="chips" data-s="dur">
              <button type="button" class="chip" data-value="weekly" aria-pressed="false">Weekly</button>
              <button type="button" class="chip" data-value="monthly" aria-pressed="true">Monthly</button>
            </div>
          </fieldset>
        </div>
      </div>
    </div>
    <div class="two-ways"><span class="line" aria-hidden="true"></span>Two ways to start</div>
  </div>
</section>

<section class="sec sec--tint" id="start-app" style="padding-top:clamp(56px,7vw,96px)">
  <div class="wrap way way--rev">
    <div>
      <p class="eyebrow way__num"><i>1</i>The Messify app</p>
      <h2 class="h2">Your tokens are waiting in the app.</h2>
      <p class="lede">Download Messify, confirm your plan and pay securely. Your tokens land in your wallet, ready for tomorrow's menu. Skip a day or double up any time, right from your phone.</p>
      <div class="stores">
        <a class="store" href="{APP_STORE}" target="_blank" rel="noopener">{I["phonedl"]}<span><small>Download on the</small><b>App Store</b></span></a>
        <a class="store" href="{GOOGLE_PLAY}" target="_blank" rel="noopener">{I["play"]}<span><small>Get it on</small><b>Google Play</b></span></a>
      </div>
      <p class="plan-line" data-s-appline>You'll confirm <b>2 meals a day, monthly</b> in the app.</p>
    </div>
    <div class="stage" data-stage aria-hidden="true">
      <div class="coin-pop" style="--x:-140%;--y:-120%;--s:17%;--d:.15s;--depth:26;--rot:-14"><img src="/assets/img/coin.webp" alt=""></div>
      <div class="coin-pop" style="--x:150%;--y:-150%;--s:14%;--d:.22s;--depth:40;--rot:18"><img src="/assets/img/coin.webp" alt=""></div>
      <div class="coin-pop" style="--x:190%;--y:20%;--s:19%;--d:.3s;--depth:18;--rot:10"><img src="/assets/img/coin.webp" alt=""></div>
      <div class="coin-pop" style="--x:-185%;--y:55%;--s:13%;--d:.36s;--depth:34;--rot:-20"><img src="/assets/img/coin.webp" alt=""></div>
      <div class="coin-pop" style="--x:20%;--y:-215%;--s:11%;--d:.42s;--depth:48;--rot:24"><img src="/assets/img/coin.webp" alt=""></div>
      <div class="app-icon"><span class="mark"></span></div>
      <div class="wallet"><img src="/assets/img/coin.webp" alt=""><b data-s-count>+52</b><span>tokens added to your wallet</span></div>
    </div>
  </div>
</section>

<section class="sec" id="start-chat">
  <div class="wrap way">
    <div>
      <p class="eyebrow way__num"><i>2</i>Talk to our team</p>
      <h2 class="h2">Rather talk it through first?</h2>
      <p class="lede">Not sure which plan fits, or whether we deliver to your building? Message us on WhatsApp. A real person on our team will help you choose before you commit.</p>
      <div class="actions"><a class="btn wa-btn" href="{WA}" target="_blank" rel="noopener" data-s-wa>{I["wa"]}Chat with us on WhatsApp</a></div>
      <p class="plan-line">We'll see the plan you picked, so you won't need to explain it twice.</p>
    </div>
    <div class="chat" data-chat>
      <div class="chat__head"><span class="chat__avatar"><span class="mark"></span></span><div><b>Messify</b><small>WhatsApp</small></div><span class="chat__tag">Example chat</span></div>
      <div class="chat__body">
        <div class="bubble me"><span class="txt" data-s-chat1>Hi Messify! I'm interested in the 2 meals a day monthly plan.</span></div>
        <div class="bubble them"><span class="dots"><i></i><i></i><i></i></span><span class="txt">Hi! Great choice. Which building should we deliver to?</span></div>
        <div class="bubble me"><span class="txt">KSK Homes in Academic City. Can I see tomorrow's menu?</span></div>
        <div class="bubble them"><span class="dots"><i></i><i></i><i></i></span><span class="txt">Sending it now. Start whenever you're ready and your first bag arrives the next morning.</span></div>
      </div>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(56px,7vw,96px)">
    <div class="start-end"><p>You planned it right.</p><a class="btn btn--ghost" href="/meal-plans/#plans">Back to plans</a></div>
  </div>
</section>
</div>'''
    render(page, body)

# ---------------------------------------------------------------- catering
def page_catering():
    faqs = [
        ('What events do you cater?', 'Corporate events and office lunches, parties and home events, university events, weddings, buffet setups and bulk orders.'),
        ('Do you cater small parties at home?', "Yes. Birthdays, family gatherings and house parties are welcome. Tell us your headcount and we'll build a menu to fit."),
        ('Which areas do you cater in?', 'We cater across Dubai, Sharjah, Ajman and Abu Dhabi.'),
        ('How is catering priced?', 'Every quote is custom, based on your headcount and the menu you choose.'),
        ('Do you do buffet setups?', 'Yes. We set up full buffets at your venue, from office lunches and house parties to weddings, with the menu built around your headcount.'),
        ('Is your catering halal?', 'Yes. All our catering menus are 100% halal.'),
        ('Can we choose our own menu?', 'Yes. Pick any mix of appetisers, main courses, salads, desserts and beverages, in Indian, Arabic, Continental, Italian, Chinese or other flavours.'),
        ('How do I get a catering quote?', 'Fill in the form on this page, or message us on WhatsApp at +971 50 251 3033 with your date, location and headcount.'),
    ]
    cr, crs = crumbs([('Home', '/'), ('Catering', '/catering/')])
    service = {'@type': 'Service', '@id': BASE + '/catering/#service', 'name': 'Messify Catering', 'serviceType': 'Catering',
               'description': 'Custom catering and buffet setups for corporate events, office lunches, parties and home events, university events, weddings and bulk orders. Quoted by headcount.',
               'provider': {'@id': BASE + '/#business'},
               'areaServed': [{'@type': 'City', 'name': c} for c in ('Dubai', 'Sharjah', 'Ajman', 'Abu Dhabi')],
               'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Catering services', 'itemListElement': [
                   {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for n in
                   ('Corporate and office catering', 'Party and home event catering', 'University event catering', 'Wedding catering', 'Buffet catering', 'Bulk catering')]}}
    page = {'path': '/catering/', 'mode': 'catering', 'nav': 'catering', 'exact': True,
            'title': 'Catering Services Dubai, Sharjah & Abu Dhabi | Messify',
            'desc': 'Custom catering and buffet setups for corporate events, parties, university events and weddings across Dubai, Sharjah, Ajman and Abu Dhabi.',
            'cta': ('#quote', 'Get a quote', 'Quote'), 'cta_bot': 'catering',
            'preload': '<link rel="preload" as="image" href="/assets/img/cat-serving-640.webp" imagesrcset="/assets/img/cat-serving-640.webp 640w, /assets/img/cat-serving.webp 1100w" imagesizes="(min-width: 900px) 45vw, 100vw">\n',
            'schema': [ORG, BUSINESS, service, faq_schema(faqs), crs]}
    events = [
        ('case', 'Corporate &amp; office', 'Corporate and office catering for team lunches, meetings and company events, delivered on time.'),
        ('party', 'Parties &amp; home events', 'Party catering for birthdays, family gatherings and house parties, at home.'),
        ('cap', 'University events', 'Orientation days, society nights and campus functions.'),
        ('rings', 'Weddings', 'Wedding catering with generous menus built around your guest list.'),
        ('serve', 'Buffet setups', 'Full buffets set up at your venue, from office lunches to weddings.'),
        ('box', 'Bulk catering', 'Large daily volumes for sites, institutions and events.'),
    ]
    ev = ''.join(f'<div class="event">{I[i]}<h3 class="h3">{t}</h3><p>{d}</p></div>' for i, t, d in events)
    def chips(group, items, on, multi=True):
        return f'<div class="chips" data-group="{group}"{" data-multi" if multi else ""}>' + ''.join(
            f'<button type="button" class="chip" aria-pressed="{"true" if x in on else "false"}" data-value="{x}">{x}</button>' for x in items) + '</div>'
    body = f'''<section class="sec sec--first">
  <div class="wrap split">
    <div>
      {cr}
      <h1 class="h2 rise"><span class="kicker">Catering in Dubai, Sharjah &amp; Abu Dhabi</span> Your event, <em class="it">fed properly.</em></h1>
      <p class="lede rise">Catering services and buffet setups for corporate events, parties, university events and weddings across Dubai, Sharjah, Ajman and Abu Dhabi. Every menu is built around your event and quoted by headcount.</p>
      <div class="actions">
        <a class="btn" href="#quote" data-messibot="catering">Get a quote</a>
        <a class="btn btn--ghost" href="{WA}?text=Hi%20Messify%2C%20I%27d%20like%20a%20catering%20quote." target="_blank" rel="noopener">WhatsApp us</a>
      </div>
      <div class="facts">
        <div><b>5,000+</b><span>meals a day of kitchen capacity</span></div>
        <div><b>4</b><span>emirates covered</span></div>
        <div><b>100%</b><span>customisable menus</span></div>
      </div>
    </div>
    <div class="photo photo--tall"><img src="/assets/img/cat-serving-640.webp" srcset="/assets/img/cat-serving-640.webp 640w, /assets/img/cat-serving.webp 1100w" sizes="(min-width: 900px) 45vw, 100vw" alt="A gloved server lifting the lid of a gold chafing dish at a catered buffet" width="1100" height="1375" fetchpriority="high"></div>
  </div>
</section>

<section class="sec" style="padding-top:0" aria-labelledby="events-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">What we cater</p><h2 class="h2" id="events-title">From house parties to wedding halls.</h2></div>
    <div class="events">{ev}</div>
  </div>
</section>

<section class="sec sec--tint" id="menu-builder" aria-labelledby="builder-title">
  <div class="wrap builder">
    <div>
      <p class="eyebrow">Fully customisable</p>
      <h2 class="h2" id="builder-title">Your menu, built around your event.</h2>
      <p class="lede">No fixed packages. Pick the courses, the flavours and your headcount, and we'll build the menu to fit.</p>
      <div class="composer">
        <fieldset class="opt"><legend>Courses <span>(pick any)</span></legend>{chips('course', ['Appetisers', 'Main course', 'Salads', 'Desserts', 'Beverages'], ['Main course', 'Desserts'])}</fieldset>
        <fieldset class="opt"><legend>Flavours <span>(pick any)</span></legend>{chips('flavour', ['Indian', 'Arabic', 'Continental', 'Italian', 'Chinese', 'Other'], ['Indian', 'Arabic'])}</fieldset>
        <div class="opt"><label for="b-guests">Guests</label><div class="guests"><input id="b-guests" type="range" min="20" max="2000" step="10" value="150"><output for="b-guests" id="b-guests-out">150</output></div></div>
        <fieldset class="opt"><legend>Where</legend>{chips('emirate', ['Dubai', 'Sharjah', 'Ajman', 'Abu Dhabi'], ['Dubai'], multi=False)}</fieldset>
        <div class="brief">
          <small>Your brief</small>
          <p id="briefText">Main course and desserts in <em>Indian and Arabic flavours</em>, for <em>150 guests</em> in Dubai.</p>
          <a class="btn" href="#quote" id="useBrief">Request this menu</a>
        </div>
      </div>
    </div>
    <div class="mosaic">
      <figure class="m1"><img src="/assets/img/cat-canapes.webp" alt="Trays of canapés on slate boards at a catered event" width="900" height="1200" loading="lazy"></figure>
      <figure class="m2"><img src="/assets/img/cat-buffet.webp" alt="A buffet table set with tartlets, skewers and desserts" width="736" height="981" loading="lazy"></figure>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="why-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Why Messify</p><h2 class="h2" id="why-title">Built to feed hundreds, consistently.</h2><p class="lede">What sets us apart from other catering companies in Dubai.</p></div>
    <ul class="why">
      <li><b>Scalable production</b><span>Up to <em>5,000+ meals per day</em> from our partner kitchen operation.</span></li>
      <li><b>Centralised kitchen</b><span>Standardised quality control on every batch.</span></li>
      <li><b>Transparent pricing</b><span>Custom quotes based on your headcount.</span></li>
      <li><b>Reliable logistics</b><span>On-time bulk delivery across the four emirates.</span></li>
      <li><b>Your menu, your way</b><span>From a single main course to a full spread, built around your guests.</span></li>
    </ul>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="uae-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Where we cater</p><h2 class="h2" id="uae-title">Catering across the UAE.</h2></div>
    <div class="emirates">
      <div class="emirate"><h3 class="h3">Catering in Dubai</h3><p>Our meals are cooked in International City, so Dubai events get the shortest journey: office lunches, parties at home and large events across the city.</p></div>
      <div class="emirate"><h3 class="h3">Catering in Sharjah</h3><p>Catering services in Sharjah for corporate events, family occasions and parties, delivered on time from Dubai.</p></div>
      <div class="emirate"><h3 class="h3">Catering in Abu Dhabi</h3><p>Catering in Abu Dhabi for corporate events, weddings and large gatherings. Share your date early and we'll plan delivery around your event.</p></div>
      <div class="emirate"><h3 class="h3">Catering in Ajman</h3><p>Party and event catering in Ajman, from family gatherings to bulk orders.</p></div>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="steps-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">How it works</p><h2 class="h2" id="steps-title">From enquiry to plated, in four steps.</h2></div>
    <ol class="steps" style="max-width:820px">
      <li><div><h3>Tell us about your event</h3><p>Date, location, headcount and what you'd like on the menu.</p></div></li>
      <li><div><h3>Get a custom quote</h3><p>Priced by headcount and the menu you choose.</p></div></li>
      <li><div><h3>Finalise the menu</h3><p>We adjust dishes and quantities until it fits.</p></div></li>
      <li><div><h3>Delivered on time</h3><p>Our team brings everything to your venue.</p></div></li>
    </ol>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="faq-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-title">Good to know.</h2></div>
    {faq_html(faqs)}
  </div>
</section>

<section class="sec" id="quote" aria-labelledby="quote-title">
  <div class="wrap form-grid">
    <div>
      <p class="eyebrow">Get a quote</p>
      <h2 class="h2" id="quote-title">Let's build your next event.</h2>
      <p class="lede">Send the details and we'll come back with a menu and price for your headcount.</p>
      {contact_lines()}
    </div>
    <div>
      <form class="form" data-form="catering" data-done="quoteDone" data-wa-intro="Hi Messify, I'd like a catering quote." novalidate>
        <input type="hidden" name="_subject" value="New catering enquiry from messify.me">
        <div class="row">
          <div class="field"><label for="q-name">Your name</label><input id="q-name" name="name" data-label="Name" autocomplete="name" placeholder="Sara Khan" required><span class="err" aria-live="polite"></span></div>
          <div class="field"><label for="q-phone">Phone number (WhatsApp)</label><input id="q-phone" name="phone" data-label="Phone (WhatsApp)" type="tel" inputmode="tel" autocomplete="tel" placeholder="+971 50 000 0000" required><span class="err" aria-live="polite"></span></div>
        </div>
        <div class="row">
          <div class="field"><label for="q-type">Event type</label><select id="q-type" name="type" data-label="Event type"><option>Corporate &amp; office</option><option>Party or home event</option><option>University event</option><option>Wedding</option><option>Buffet setup</option><option>Bulk catering</option><option>Other</option></select></div>
          <div class="field"><label for="q-emirate">Emirate</label><select id="q-emirate" name="emirate" data-label="Emirate"><option>Dubai</option><option>Sharjah</option><option>Ajman</option><option>Abu Dhabi</option></select></div>
        </div>
        <div class="row">
          <div class="field"><label for="q-date">Event date</label><input id="q-date" name="date" data-label="Event date" type="date"></div>
          <div class="field"><label for="q-guests">Headcount</label><input id="q-guests" name="guests" data-label="Headcount" type="number" inputmode="numeric" min="1" placeholder="150" required><span class="err" aria-live="polite"></span></div>
        </div>
        <div class="field"><label for="q-location">Location <span class="opt-tag">(optional)</span></label><input id="q-location" name="location" data-label="Location" autocomplete="street-address" placeholder="Venue or area, e.g. Business Bay"></div>
        <div class="field"><label for="q-notes">Anything else?</label><textarea id="q-notes" name="notes" data-label="Notes" placeholder="Menu ideas, dietary needs, timings"></textarea></div>
        <div class="hp" aria-hidden="true"><label for="q-web">Leave this empty</label><input id="q-web" name="website" tabindex="-1" autocomplete="off"></div>
        <button class="btn" type="submit">Send enquiry</button>
        <p class="form-status" role="alert"></p>
      </form>
      <div class="form form-done" id="quoteDone" tabindex="-1" hidden>
        <span class="tick">{I["tick"]}</span>
        <h3 data-done-title>Enquiry received.</h3>
        <p>We'll come back with a menu and price for your headcount.</p>
        <a class="btn btn--ghost" data-done-wa href="{WA}" target="_blank" rel="noopener">Prefer WhatsApp? Send it there</a>
      </div>
    </div>
  </div>
</section>'''
    render(page, body)

# ---------------------------------------------------------------- about, privacy, 404
def page_about():
    cr, crs = crumbs([('Home', '/'), ('About Messify', '/about/')])
    plans = '; '.join(f'{mlabel(m)} {ln}: {aed(p)} ({t} meals, AED {per(p, t)} each)' for m, ln, t, p in PLANS)
    rows = [
        ('What Messify does', 'Daily meal plans and event catering in Dubai and the UAE.'),
        ('Where meals are cooked', 'Partner kitchen in International City, Dubai'),
        ('Meal plan delivery areas', 'Dubai International Academic City, Dubai Silicon Oasis and International City only'),
        ('Who it serves', 'Students, working professionals, office teams and residents'),
        ('Meal plan options', '1, 2 or 3 meals a day. Monthly: 26 days of meals to use within 30 days. Weekly: 7 days of meals to use within 9 days.'),
        ('Meal plan prices', plans),
        ('Price per meal', 'AED 25.63 to AED 30.71'),
        ('Token system', '1 meal = 1 token. Skip a day and use the token later in your plan. Spend extra tokens to double up.'),
        ('Delivery', "Every morning. All of the day's meals arrive together in one chilled Messify bag with an ice pack."),
        ('Menu', "Changes every day. Tomorrow's menu is visible in the app the day before; choose your meals by 6 PM for next-morning delivery."),
        ('Halal', 'All meals are 100% halal'),
        ('Vegetarian', 'A vegetarian option every day, for every meal'),
        ('Food safety', 'Prepared with gloved hands, blast-chilled after cooking, sealed in kraft bowls, packed cold.'),
        ('Catering', 'Corporate and office, parties and home events, university events, weddings, buffet setups and bulk catering. Fully customisable menus, quoted by headcount.'),
        ('Catering areas', 'Dubai, Sharjah, Ajman and Abu Dhabi'),
        ('How to order', 'Messify app (App Store and Google Play) or WhatsApp'),
        ('Opening hours', 'Every day, 8 AM to 11 PM'),
        ('Contact', f'{PHONE_DISPLAY} (phone and WhatsApp), {EMAIL}'),
        ('Instagram', '@messify.me'),
    ]
    trs = ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows)
    page = {'path': '/about/', 'mode': 'meals', 'nav': None, 'title': 'About Messify | Meal Plans & Catering in Dubai',
            'desc': 'Messify is a Dubai meal-plan and catering company. Meals are cooked fresh daily in International City. Prices, delivery areas and contact details.',
            'schema': [ORG, BUSINESS, {'@type': 'AboutPage', '@id': BASE + '/about/#page', 'url': BASE + '/about/', 'name': 'About Messify',
                                        'mainEntity': {'@id': BASE + '/#organization'}, 'dateModified': TODAY}, crs]}
    body = f'''<section class="sec sec--first">
  <div class="wrap">
    {cr}
    <div class="sec-head" style="max-width:820px">
      <h1 class="h2"><span class="kicker">About us</span> Messify at a glance.</h1>
      <p class="lede">{ONE_LINER}</p>
    </div>
    <div class="answer">
      <p class="answer__label">Key facts</p>
      <table class="facts-table">{trs}</table>
      <p class="updated">Last updated: {UPDATED_LABEL}</p>
    </div>
  </div>
</section>
<section class="sec sec--tint" aria-labelledby="diff-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">What makes us different</p><h2 class="h2" id="diff-title">One less thing to think about.</h2></div>
    <div class="reasons">
      <div class="reason"><h3>The whole day in one bag</h3><p>Breakfast, lunch and dinner arrive together every morning, so there's nothing to wait for later.</p></div>
      <div class="reason"><h3>Tokens, not rigid plans</h3><p>Skip a day and eat it later, or double up when you need to. Your plan bends around your week.</p></div>
      <div class="reason"><h3>Priced for everyday eating</h3><p>From AED 25.63 a meal on the 3-meal monthly plan, with a new menu every day.</p></div>
    </div>
  </div>
</section>
{band()}'''
    render(page, body)

# Terms text supplied by Messify (26 September 2025). Spelling and punctuation tidied; 'Partner Restaurant' renamed 'Partner Kitchen'
# token validity (weekly 9 days, monthly 30 days) and the 6:00 PM meal-selection cut-off updated on Aman's instruction, 11 October 2026.
TERMS = [
 ('introduction', 'Introduction', [
  'These Terms and Conditions ("Terms") govern your use of the Messify platform, our mobile application and website, operated by Messify FZC in the United Arab Emirates (UAE). By accessing or using the Platform, you agree to these Terms. If you do not accept these Terms, discontinue use immediately.']),
 ('definitions', 'Definitions', [('dl', [
  ('Messify / Platform', 'The Messify mobile app, website and related services.'),
  ('User', 'Any individual who registers, accesses or uses the Platform.'),
  ('Partner Kitchen', 'Third-party kitchens that prepare meals ordered through Messify.'),
  ('Token', 'A digital unit that represents one standard meal.'),
  ('Subscription Plan', 'A prepaid package of Tokens for a defined period.')])]),
 ('eligibility', 'Eligibility and account registration', [
  'You must be 18 years or older to create an account, or use the Platform under the supervision of a legal guardian. Provide accurate information at registration and keep it updated. One user = one account. You are solely responsible for securing your login credentials; Messify is not liable for unauthorized access resulting from your failure to safeguard your account.']),
 ('service', 'Service overview', [
  'Messify offers affordable, customizable meal subscription plans fulfilled by Partner Kitchens. Key features include app-based meal scheduling and selection, a redeemable Token system, and scheduled deliveries.',
  'Important: during the first app version, service is limited to selected delivery zones as listed in-app. Photos shown for meals are illustrative and may not be exact replicas; images are chosen to best represent each dish.']),
 ('payment', 'Subscription plans and payment terms', [
  'All plans are prepaid. Pricing is displayed in-app and on the site and may vary by plan. We accept debit and credit cards and approved wallets (e.g. Apple Pay and Google Pay) via secure third-party gateways; Messify does not store card data. VAT is included unless stated otherwise. Cash on Delivery (COD) is not supported.']),
 ('tokens', 'Tokens and meal redemption', [
  'Each Token equals one standard meal (breakfast, lunch or dinner). Some premium upgrades may require additional Tokens. Subscription Tokens are valid from the Start Date specified in the app for 9 days on weekly plans and 30 days on monthly plans; unused Tokens do not carry forward after plan expiry. Extra Tokens purchased outside a subscription have no expiry and remain on your account until used. To ensure next-day delivery of all three meals, you must update your selections in the app by 6:00 PM each day. Redemption is subject to meal availability and kitchen operating hours.']),
 ('cancellation', 'Cancellation, refund and transfer policy', [
  ('b', 'Cancellation:', 'You may cancel within 24 hours of purchase for a full refund if no Tokens have been used. Beyond 24 hours, a cancellation may be granted at Messify’s discretion. In such case, (i) the value of all Tokens already used will be deducted, and (ii) a 25% cancellation fee will be applied on the remaining refundable balance.'),
  ('b', 'Refunds:', 'Refunds may also be issued where: (a) payment is complete but Tokens are not provisioned within 48 hours; (b) meals are undelivered due to a verified Messify system fault; or (c) duplicate charges occur due to a payment gateway error. Refunds are not granted for user unavailability, change of mind or taste preferences unless food is proven unsafe or spoiled. Processing time is typically 7 to 14 business days.'),
  ('b', 'Non-transferable:', 'Plans and Tokens are non-transferable and may not be resold, shared or gifted.')]),
 ('delivery', 'Delivery policy', [
  'Deliveries are executed by Partner Kitchens or approved logistics providers within the selected time slots. You must ensure the typed address exactly matches the map pin location selected in the app; discrepancies are the user’s responsibility. If the courier arrives and you do not answer calls or collect the order within 10 minutes, the order may be left at the doorstep or, for student accommodation and hostels, at the lobby with a package code or your phone number noted on the label. Reattempted delivery is not guaranteed. Tokens may still be deducted where delivery failure is due to user error, inaccessibility or unresponsiveness.']),
 ('availability', 'Service limitations and availability', [
  'Service operates only in selected UAE areas listed in-app. Platform performance depends on connectivity, device compatibility and app version. Maintenance or temporary outages may occur; where feasible, advance notice will be provided.']),
 ('responsibilities', 'User responsibilities', [
  'You agree to use the Platform lawfully, provide accurate delivery and contact information, keep your phone reachable during delivery windows, and refrain from exploiting promotions or system loopholes. Treat Partner Kitchen staff and couriers with respect. Violations may result in suspension or permanent account termination.']),
 ('partners', 'Kitchen partners', [
  'Messify works with verified Partner Kitchens. The Partner Kitchen is fully responsible for food preparation and any health-related issues, including food poisoning. Messify conducts periodic checks and monitors quality to the maximum of our capabilities; however, the final responsibility for food safety rests with the Partner Kitchen. Issues must be reported within 4 hours of delivery to be eligible for review and potential Token adjustments.']),
 ('allergies', 'Allergies and health disclaimers', [
  'Meals are not guaranteed allergen-free unless explicitly labeled. Users must check ingredients and disclose allergies when choosing meals. Messify is not liable for allergic reactions or dietary complications unless due to proven negligence.']),
 ('promotions', 'Promotions, discounts and referrals', [
  'Promotions and referral programs may change or be withdrawn without notice. Abuse, such as self-referrals, fake accounts or manipulation, will void rewards. Only one promo code per order unless otherwise stated.']),
 ('ip', 'Intellectual property', [
  'All content on the Platform (logos, brand identity, UI, copy, images, designs) is owned by Messify FZC. Reproduction, distribution or commercial use without written consent is prohibited.']),
 ('liability', 'Limitation of liability', [
  'To the fullest extent permitted by law, Messify is not liable for indirect, incidental, punitive or consequential damages. Messify is not liable for delivery delays, user health complications or food quality issues attributable to Partner Kitchens. Total Messify liability is limited to the value of the last paid subscription by the user.']),
 ('indemnity', 'Indemnity', [
  'You agree to indemnify and hold harmless Messify, its directors, employees, partners and affiliates from claims, liabilities or expenses arising out of your use of the Platform, your breach of these Terms, or violations of applicable law.']),
 ('termination', 'Termination of account', [
  'Messify may suspend or terminate accounts for breaches, fraud, abuse, or conduct that harms the Platform, Partner Kitchens or other users.']),
 ('changes', 'Modifications to terms', [
  'Messify may update these Terms at any time. Continued use after updates constitutes acceptance of the revised Terms.']),
 ('law', 'Governing law and jurisdiction', [
  'These Terms are governed by the laws of the United Arab Emirates, with exclusive jurisdiction vested in the courts of Dubai, UAE.']),
 ('contact', 'Contact information', [
  'For questions, feedback or complaints, please contact:',
  ('dl', [('Email', '<a href="mailto:info@messify.me">info@messify.me</a>'), ('Phone', '<a href="tel:+971502513033">+971 50 251 3033</a>'), ('Office', 'P.O. Box 932, Ajman, United Arab Emirates')])]),
 ('disputes', 'Issue resolution and management review', [
  'All complaints and disputes must be submitted via the official channels listed above. Messify management will review all material facts and make a final decision (subject to applicable law). Third-party mediation or arbitration will not be entertained without prior written consent.']),
]

def page_terms():
    cr, crs = crumbs([('Home', '/'), ('Terms & conditions', '/terms/')])
    page = {'path': '/terms/', 'mode': 'meals', 'nav': None, 'title': 'Terms & Conditions | Messify',
            'desc': 'Terms and conditions for the Messify app, website and meal plans: subscriptions, tokens, payments, delivery, cancellations and refunds.',
            'schema': [ORG, {'@type': 'WebPage', '@id': BASE + '/terms/#page', 'url': BASE + '/terms/', 'name': 'Messify terms and conditions',
                             'datePublished': '2025-09-26', 'dateModified': '2026-10-11', 'publisher': {'@id': BASE + '/#organization'}}, crs]}
    toc = ''.join(f'<li><a href="#{k}">{t}</a></li>' for k, t, _ in TERMS)
    secs = []
    for i, (k, t, blocks) in enumerate(TERMS, 1):
        out = []
        for b in blocks:
            if isinstance(b, str): out.append(f'<p>{esc(b)}</p>')
            elif b[0] == 'dl': out.append('<dl class="terms-dl">' + ''.join(f'<div><dt>{dt}</dt><dd>{dd}</dd></div>' for dt, dd in b[1]) + '</dl>')
            elif b[0] == 'b': out.append(f'<p><b>{b[1]}</b> {esc(b[2])}</p>')
        secs.append(f'<section class="terms-sec" id="{k}"><h2><span>{i}.</span> {t}</h2>{"".join(out)}</section>')
    body = f'''<section class="sec sec--first">
  <div class="wrap">
    {cr}
    <div class="terms">
      <header class="terms-head">
        <h1 class="h2"><span class="kicker">Messify FZC</span> Terms &amp; conditions</h1>
        <p class="lede">Last updated 11 October 2026. Effective until the next software update.</p>
      </header>
      <nav class="toc" aria-label="Contents"><p class="answer__label">Contents</p><ol>{toc}</ol></nav>
      <div class="doc terms-body">{"".join(secs)}</div>
    </div>
  </div>
</section>'''
    render(page, body)

def page_privacy():
    page = {'path': '/privacy/', 'mode': 'meals', 'nav': None, 'title': 'Privacy Notice | Messify',
            'desc': 'How Messify handles the details you send through the forms on messify.me, and how we use website analytics.', 'schema': [ORG]}
    body = f'''<section class="sec sec--first">
  <div class="wrap doc">
    <h1 class="h2">Privacy notice</h1>
    <p class="lede">This notice explains how Messify handles the information you send through this website. Using the Messify app and our meal plans is covered by our <a href="/terms/">terms and conditions</a>.</p>
    <h2>What we collect</h2>
    <p>When you fill in a form on messify.me, we receive your name, phone number and the details you choose to share, such as your plan preference, area, event date, headcount, location and notes.</p>
    <p>If you use Messibot, the chat assistant on this website, the answers you give it (such as your name, area, plan or event details) are sent to us as a summary when you reach the end of the chat, so our team can follow up. Messibot is a scripted assistant and does not use AI.</p>
    <h2>How we use it</h2>
    <p>We use these details only to reply to your enquiry, prepare a quote or help you start a meal plan. We may contact you by phone, WhatsApp or email.</p>
    <h2>Website analytics</h2>
    <p>We use Google Analytics to understand how people use this website, such as which pages are visited, the type of device and the approximate city. It uses cookies and does not give us your name or contact details. You can block cookies in your browser settings or install Google's Analytics opt-out add-on.</p>
    <h2>How it reaches us</h2>
    <p>Form submissions and Messibot summaries are delivered to our inbox at {EMAIL} through FormSubmit, an email forwarding service. We do not sell or rent your details to anyone.</p>
    <h2>How long we keep it</h2>
    <p>We keep enquiry details for as long as we need them to serve you, and delete them on request.</p>
    <h2>Your choices</h2>
    <p>To see, correct or delete the details you sent us, email {EMAIL} or message us on WhatsApp at {PHONE_DISPLAY}.</p>
    <p class="updated" style="margin-top:32px">Last updated: {UPDATED_LABEL}</p>
  </div>
</section>'''
    render(page, body)

def page_404():
    page = {'path': '/404/', 'file': '404.html', 'mode': 'meals', 'nav': None, 'noindex': True,
            'title': 'Page Not Found | Messify', 'desc': 'This page could not be found.', 'schema': [ORG]}
    body = f'''<section class="sec sec--first notfound">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1 class="h2">This page skipped a day.</h1>
    <p class="lede">Don't worry, you can have it later. Try one of these instead.</p>
    <div class="actions"><a class="btn" href="/">Go home</a><a class="btn btn--ghost" href="/meal-plans/">Meal plans</a><a class="btn btn--ghost" href="/catering/">Catering</a></div>
  </div>
</section>'''
    render(page, body)

# ---------------------------------------------------------------- technical files
def tech_files():
    urls = [('/', '1.0'), ('/meal-plans/', '0.9'), ('/meal-plans/academic-city/', '0.9'), ('/meal-plans/silicon-oasis/', '0.9'),
            ('/meal-plans/international-city/', '0.8'), ('/catering/', '0.9'), ('/about/', '0.6'), ('/terms/', '0.2'), ('/privacy/', '0.2')]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n' for u, p in urls) + '</urlset>\n'
    open(os.path.join(DIST, 'sitemap.xml'), 'w').write(sm)
    robots = f'''# Messify: search engines and AI assistants are welcome.
User-agent: *
Allow: /

# AI search and assistant crawlers (explicitly allowed)
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Applebot
User-agent: Applebot-Extended
User-agent: Bingbot
User-agent: meta-externalagent
User-agent: meta-externalfetcher
Allow: /

Sitemap: {BASE}/sitemap.xml
'''
    open(os.path.join(DIST, 'robots.txt'), 'w').write(robots)
    plan_lines = '\n'.join(f'- {mlabel(m)}, {ln}: {aed(p)} ({t} meals, AED {per(p, t)} per meal)' for m, ln, t, p in PLANS)
    llms = f'''# Messify

> {ONE_LINER}

Messify sells daily meal plans through the Messify app. Each meal on a plan is a token: customers can skip a day and use the token later in their plan, or spend extra tokens to double up. All of the day's meals are delivered together every morning in one chilled bag. The menu changes daily, all meals are 100% halal, and there is a vegetarian option every day, for every meal. Monthly plans are 26 days of meals to use within 30 days; weekly plans are 7 days of meals to use within 9 days. Meal plan delivery covers Dubai Academic City, Dubai Silicon Oasis and International City only.

## Meal plan prices (AED)
{plan_lines}

## Key pages
- [Meal plans and prices]({BASE}/meal-plans/): plans, the token system, delivery and FAQs
- [Meal plans in Dubai Academic City]({BASE}/meal-plans/academic-city/): delivery to universities and student residences in DIAC, including KSK Homes and The Myriad
- [Meal plans in Dubai Silicon Oasis]({BASE}/meal-plans/silicon-oasis/): delivery to offices, residents, RIT Dubai and DSOA University Residence
- [Meal plans in International City]({BASE}/meal-plans/international-city/): where Messify meals are cooked
- [Catering]({BASE}/catering/): corporate, party and home events, university events, weddings, buffet setups and bulk catering across Dubai, Sharjah, Ajman and Abu Dhabi
- [About Messify]({BASE}/about/): key facts in one table

## Contact
- Phone and WhatsApp: {PHONE_DISPLAY}
- Email: {EMAIL}
- Instagram: @messify.me
- Opening hours: every day, 8 AM to 11 PM (Gulf Standard Time)
- App Store: {APP_STORE}
- Google Play: {GOOGLE_PLAY}
'''
    open(os.path.join(DIST, 'llms.txt'), 'w').write(llms)
    # Netlify redirects: old Wix addresses keep working (and keep their Google ranking) after the move.
    redirects = '''/terms-and-conditions   /terms/          301
/terms-and-conditions/  /terms/          301
/privacy-policy         /privacy/        301
/privacy-policy/        /privacy/        301
/about-us               /about/          301
/about-us/              /about/          301
/faqs                   /meal-plans/     301
/faqs/                  /meal-plans/     301
'''
    open(os.path.join(DIST, '_redirects'), 'w').write(redirects)
    manifest = {'name': 'Messify', 'short_name': 'Messify', 'description': 'Daily meal plans and catering in Dubai.', 'start_url': '/',
                'display': 'browser', 'background_color': '#FAF6EE', 'theme_color': '#38B6FF',
                'icons': [{'src': '/assets/img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                          {'src': '/assets/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}
    open(os.path.join(DIST, 'site.webmanifest'), 'w').write(json.dumps(manifest, indent=1))
    print('wrote sitemap.xml robots.txt llms.txt site.webmanifest')

def sync_js_prices():
    """Prices live only in PLANS above; this copies them into site.js so the page and script never disagree."""
    import re
    js_path = os.path.join(DIST, 'assets', 'js', 'site.js')
    js = open(js_path).read()
    rows = []
    for m in (1, 2, 3):
        w = next(p for p in PLANS if p[0] == m and p[1] == 'weekly')
        mo = next(p for p in PLANS if p[0] == m and p[1] == 'monthly')
        rows.append(f"    {m}: {{ weekly: {{ price: {w[3]}, tokens: {w[2]} }}, monthly: {{ price: {mo[3]}, tokens: {mo[2]} }} }}")
    block = 'var PLANS = {\n' + ',\n'.join(rows) + '\n  };'
    js, n = re.subn(r'var PLANS = \{.*?\n  \};', lambda _: block, js, count=1, flags=re.S)
    assert n == 1, 'PLANS block not found in site.js'
    open(js_path, 'w').write(js)

if __name__ == '__main__':
    sync_js_prices()
    page_home(); page_meal_plans()
    for s in AREAS: page_area(s)
    page_start(); page_catering(); page_about(); page_terms(); page_privacy(); page_404(); tech_files()

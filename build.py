#!/usr/bin/env python3
"""Builds the Messify static site into ./dist. Run: python3 build.py"""
import json, os, html
from urllib.parse import quote
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
BASE = 'https://www.messify.me'
TODAY = '2026-10-23'
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
             'and delivers breakfast, lunch and dinner together each morning across Dubai Academic City, Dubai Silicon Oasis, '
             'International City and Dubai Festival City (DFC), from AED 25.63 a meal. It also caters corporate events, parties, university events '
             'and weddings across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain.')

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
    'festival-city': 'Dubai Festival City',
}
CATER_EMIRATES = ['Dubai', 'Sharjah', 'Ajman', 'Abu Dhabi', 'Ras Al Khaimah', 'Umm Al Quwain']
CATER_TXT = 'Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain'
GMAPS = 'https://maps.google.com/maps?cid=12829665698799731370'  # Messify on Google Maps (reviews)
RATING = '4.9'  # Google rating. Never show the number of reviews.

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
    'areaServed': [{'@type': 'Place', 'name': n} for n in PLACES.values()] + [{'@type': 'AdministrativeArea', 'name': c} for c in CATER_EMIRATES],
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

def rating_badge():
    return (f'<a class="gbadge" href="{GMAPS}" target="_blank" rel="noopener" aria-label="Rated {RATING} out of 5 on Google reviews">'
            f'<span class="gbadge__stars" aria-hidden="true">★★★★★</span><b>{RATING}</b><span>on Google reviews</span></a>')

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
        <li><a href="/meal-plans/">Meal plans in Dubai</a></li>
        <li><a href="/meal-plans/academic-city/">Academic City</a></li>
        <li><a href="/meal-plans/silicon-oasis/">Silicon Oasis</a></li>
        <li><a href="/meal-plans/international-city/">International City</a></li>
        <li><a href="/meal-plans/festival-city/">Dubai Festival City</a></li>
      </ul></div>
      <div><h2>Catering</h2><ul>
        <li><a href="/catering/">Catering services</a></li>
        <li><a href="/catering/corporate-events/">Corporate catering</a></li>
        <li><a href="/catering/weddings/">Wedding catering</a></li>
        <li><a href="/catering/iftar/">Iftar catering</a></li>
        <li><a href="/catering/dubai/">Catering in Dubai</a></li>
        <li><a href="/catering/sharjah/">Catering in Sharjah</a></li>
        <li><a href="/guides/#catering-guides">Catering guides</a></li>
        <li><a href="/catering/#quote">Get a quote</a></li>
      </ul></div>
      <div><h2>Company</h2><ul>
        <li><a href="/about/">About Messify</a></li>
        <li><a href="/guides/">Guides</a></li>
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
    <p class="fine">Prices in AED. Monthly plans are 26 days of meals to use within 30 days. Weekly plans are 7 days of meals to use within 9 days. Price per meal = plan price ÷ tokens. <a href="/guides/meal-plan-cost-dubai/#calculator">Compare with ordering in</a>.</p>
    {table}
  </div>
</section>'''

def meal_form(area_default='', heading='Talk to us.', lede="Have a question before you start? Tell us which plan you're considering and we'll get back to you, usually on WhatsApp.", tint=True):
    areas = ['Dubai Academic City', 'Dubai Silicon Oasis', 'International City', 'Dubai Festival City (DFC)', 'Somewhere else (join the waitlist)']
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
    return f'''<div class="quotes-head"><p class="eyebrow">From our customers</p><{heading_tag} class="h2" id="quotes-title">{title}</{heading_tag}>{rating_badge()}</div>
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
        ('festival-city', 'Dubai Festival City (DFC)', 'Festival City', 'Homes in Al Badia and offices across DFC.'),
    ]
    out = ''.join(f'<a class="area" href="/meal-plans/{s}/"><small>{small}</small><b>Meal plans in {name}</b><span>{line}</span><span class="link-arrow">See the area {I["arrow"]}</span></a>'
                  for s, small, name, line in data if s != exclude)
    return f'<div class="areas">{out}</div>'

FAQ_PRICE = ('How much does a meal plan cost in Dubai with Messify?',
             'Weekly plans cost AED 215, 415 or 610 for 1, 2 or 3 meals a day. Monthly plans cost AED 715, 1,400 or 1,999. That works out to AED 25.63 to 30.71 per meal.')
FAQ_AREAS = ('Which areas do you deliver meal plans to?',
             'We deliver meal plans every morning to four areas: Dubai Academic City, Dubai Silicon Oasis, International City and Dubai Festival City (DFC). Message us on WhatsApp to check your building.')
FAQ_START = ('How do I start a meal plan?',
             'Download the Messify app, pick your plan and pay in the app. Prefer to talk first? Message us on WhatsApp at +971 50 251 3033.')
FAQ_SKIP = ('Can I skip a day?', 'Yes. Skip a day in the app and use that token on another day of your plan.')

# ================================================================= PAGES
def page_home():
    faqs = [FAQ_PRICE, FAQ_AREAS,
            ('Do you cater parties and events?', 'Yes. We cater corporate events, office lunches, parties and home events, university events, weddings and bulk orders across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain. Every menu is custom and priced by headcount.'),
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
        <p class="door__text">Corporate, party, university and wedding catering across six emirates, from Dubai and Sharjah to Abu Dhabi.</p>
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
      <p class="lede">Fresh, balanced meals are cooked every day in our partner kitchen in International City. With daily meal delivery, subscribers get breakfast, lunch and dinner together each morning across Dubai Academic City, Silicon Oasis, International City and Dubai Festival City. For events, we cater anything from a house party to a wedding across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain.</p>
    </div>
    <div class="duo">
      <a class="card-link" href="/meal-plans/">
        <div class="photo"><img src="/assets/img/bag-sofa-640.webp" srcset="/assets/img/bag-sofa-640.webp 640w, /assets/img/bag-sofa.webp 900w" sizes="(min-width: 860px) 50vw, 100vw" alt="A steaming meal bowl beside a Messify bag and a Certified Chill ice pack" width="900" height="1350" loading="lazy" style="object-position:50% 62%"></div>
        <div class="card-link__body">
          <p class="eyebrow" style="margin:0">Meal plans</p>
          <h3 class="h3">Your meals, handled.</h3>
          {ticklist(['From AED 25 a meal, weekly or monthly', 'New menu every day, see it a day ahead', 'Skip a day, have it later in your plan'], 'x')}
          <span class="link-arrow">Explore meal plans in Dubai {I["arrow"]}</span>
        </div>
      </a>
      <a class="card-link card-link--dark" href="/catering/">
        <div class="photo"><img src="/assets/img/cat-serving-640.webp" srcset="/assets/img/cat-serving-640.webp 640w, /assets/img/cat-serving.webp 1100w" sizes="(min-width: 860px) 50vw, 100vw" alt="A gloved server lifting the lid of a chafing dish at a catered buffet" width="1100" height="1375" loading="lazy"></div>
        <div class="card-link__body">
          <p class="eyebrow" style="margin:0;color:#D8B48A">Catering</p>
          <h3 class="h3">Your event, fed properly.</h3>
          {ticklist(['Corporate, parties, weddings and buffet setups', 'Fully customisable menus, quoted by headcount', 'Six emirates, including Dubai, Sharjah and Abu Dhabi'], 'x')}
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
        <tr><th scope="row">Meal plan areas</th><td>Dubai Academic City, Dubai Silicon Oasis, International City, Dubai Festival City (DFC)</td></tr>
        <tr><th scope="row">Catering areas</th><td>Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain</td></tr>
        <tr><th scope="row">Google rating</th><td><a href="{GMAPS}" target="_blank" rel="noopener">{RATING} out of 5 on Google reviews</a></td></tr>
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
        'desc': 'Affordable weekly and monthly meal plans in Dubai from AED 25 a meal. 1, 2 or 3 fresh, 100% halal meals a day, delivered together every morning.',
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
      {rating_badge()}
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

{plans_section('Meal plans in Dubai, priced per meal.')}

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
      <p class="lede">Daily meal delivery to four areas: Academic City, Silicon Oasis, International City and Dubai Festival City (DFC). Meals are cooked in International City and arrive every morning.</p></div>
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
  'guide': ('/guides/student-meal-plans-dubai/', 'Read our guide to student meal plans in Dubai'),
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
  'guide': ('/guides/office-lunch-delivery-silicon-oasis/', 'Read our guide to office lunch delivery in Silicon Oasis'),
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
 'festival-city': {
  'name': 'Festival City', 'place': 'Dubai Festival City', 'kicker': 'Dubai Festival City (DFC)',
  'title': 'Meal Plans in Dubai Festival City (DFC) | Messify',
  'desc': 'Daily meal plans delivered every morning in Dubai Festival City (DFC), to homes in Al Badia and offices across DFC. 100% halal, from AED 25 a meal.',
  'h1': 'Meal plans in Dubai Festival City.',
  'lede': "Breakfast, lunch and dinner for DFC, delivered together every morning. Fresh, 100% halal meals cooked daily in our partner kitchen in International City and brought to your home in Al Badia or your office in Dubai Festival City.",
  'facts': [('From AED 25', 'per meal'), ('Every morning', 'to your home or office'), ('Skip a day', 'have it later in your plan')],
  'img': ('bag-sofa-640.webp', 'bag-sofa.webp', 900, 1350, 'A steaming meal bowl beside a Messify bag and a Certified Chill ice pack', '50% 62%'),
  'where_title': 'Where we deliver in Dubai Festival City.',
  'groups': [
    ('home', 'Homes', ['Al Badia Residences', 'Al Badia Hillside Village', 'Villas and apartments across DFC'], 'Message us your building to confirm'),
    ('office', 'Offices', ['Offices and business centres across Dubai Festival City', 'Office towers around Festival City Mall'], 'Lunch arrives before your workday starts'),
  ],
  'why_title': 'Why people in Dubai Festival City choose Messify.',
  'guide': ('/guides/meal-delivery-dubai-festival-city/', 'Read our guide to daily meal delivery in Dubai Festival City'),
  'reasons': [
    ('One bag, the whole day', "All of the day's meals arrive together every morning in one chilled bag. No waiting on delivery riders at lunch or dinner."),
    ('Lunch sorted for work', 'Working in DFC? Your lunch is at your desk before the lunchtime rush, and dinner is ready to reheat when you get home.'),
    ('Skip when life happens', 'Away for the weekend or out for dinner? Skip a day in the app and use that token later in your plan.'),
  ],
  'faqs': [
    ('Do you deliver meal plans in Dubai Festival City?', "Yes. We deliver every morning to homes and offices across Dubai Festival City (DFC), including Al Badia. All of the day's meals arrive together in one chilled bag."),
    ('Do you deliver to Al Badia Residences and Al Badia Hillside Village?', 'Yes. Message us on WhatsApp with your building and we will confirm the drop-off point.'),
    ('Can I get lunch delivered to my office in DFC?', 'Yes. Your meals arrive every morning, so lunch is sorted before the workday starts. Teams can also share one monthly plan with one delivery for everyone.'),
    ('How much is a meal plan in Dubai Festival City?', 'Weekly plans cost AED 215, 415 or 610 for 1, 2 or 3 meals a day. Monthly plans cost AED 715, 1,400 or 1,999, which is AED 25.63 to 30.71 per meal.'),
  ],
  'form_area': 'Dubai Festival City (DFC)',
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
      {rating_badge()}
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
    <a class="link-arrow" style="margin-top:28px" href="{a.get('guide', GUIDES[1])[0]}">{a.get('guide', GUIDES[1])[1]} {I["arrow"]}</a>
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
<section class="sec sec--first start-top">
  <div class="wrap">
    <a class="back" href="/meal-plans/#plans">{I["back"]}Back to plans</a>
    <div class="start-hero start-hero--compact">
      <div>
        <p class="eyebrow rise">Almost there</p>
        <h1 class="h2 rise">Two ways to start your plan.</h1>
        <p class="lede rise">Orders aren't taken on this website. Download the Messify app and start your plan there, or talk to us on WhatsApp and we'll get you started.</p>
      </div>
      <div class="summary summary--compact" aria-live="polite">
        <div class="summary__row">
          <div><small class="summary__label">Your plan</small><p class="summary__name" data-s-name>2 meals a day · Monthly</p></div>
          <div class="summary__price"><b data-s-price>AED 1,400</b><span data-s-unit>/ month</span></div>
        </div>
        <p class="summary__meta" data-s-meta>AED 26.92 per meal · 52 tokens · 26 days of meals, use within 30 days</p>
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
        <div class="coins" data-s-coins hidden></div>
      </div>
    </div>
    <div class="start-ways" id="start-app">
      <div class="start-way">
        <p class="eyebrow way__num"><i>1</i>Download the app</p>
        <h2 class="h3">Start in the Messify app</h2>
        <p>Pick your plan, pay securely and choose tomorrow's meals.</p>
        <div class="stores stores--tight">
          <a class="store" href="{APP_STORE}" target="_blank" rel="noopener">{I["phonedl"]}<span><small>Download on the</small><b>App Store</b></span></a>
          <a class="store" href="{GOOGLE_PLAY}" target="_blank" rel="noopener">{I["play"]}<span><small>Get it on</small><b>Google Play</b></span></a>
        </div>
      </div>
      <div class="start-way">
        <p class="eyebrow way__num"><i>2</i>Talk to us</p>
        <h2 class="h3">Start on WhatsApp</h2>
        <p>A real person helps you choose, checks your building and gets you started.</p>
        <div class="actions"><a class="btn wa-btn" href="{WA}" target="_blank" rel="noopener" data-s-wa>{I["wa"]}Chat on WhatsApp</a></div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--tint" id="app-more">
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
        ('Which areas do you cater in?', 'We cater across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain. Events further from Dubai need a little more notice, so share your date early.'),
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
               'areaServed': [{'@type': 'AdministrativeArea', 'name': c} for c in CATER_EMIRATES],
               'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Catering services', 'itemListElement': [
                   {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for n in
                   ('Corporate and office catering', 'Party and home event catering', 'University event catering', 'Wedding catering', 'Buffet catering', 'Bulk catering')]}}
    page = {'path': '/catering/', 'mode': 'catering', 'nav': 'catering', 'exact': True,
            'title': 'Catering Services in Dubai & the UAE | Messify',
            'desc': 'Custom halal catering and buffet setups for corporate events, parties, university events and weddings in Dubai, Sharjah, Abu Dhabi and across the UAE.',
            'cta': ('#quote', 'Get a quote', 'Quote'), 'cta_bot': 'catering',
            'preload': '<link rel="preload" as="image" href="/assets/img/cat-serving-640.webp" imagesrcset="/assets/img/cat-serving-640.webp 640w, /assets/img/cat-serving.webp 1100w" imagesizes="(min-width: 900px) 45vw, 100vw">\n',
            'schema': [ORG, BUSINESS, service, faq_schema(faqs), crs]}
    ev = event_tiles(CATER_EVENTS)
    def chips(group, items, on, multi=True):
        return f'<div class="chips" data-group="{group}"{" data-multi" if multi else ""}>' + ''.join(
            f'<button type="button" class="chip" aria-pressed="{"true" if x in on else "false"}" data-value="{x}">{x}</button>' for x in items) + '</div>'
    body = f'''<section class="sec sec--first">
  <div class="wrap split">
    <div>
      {cr}
      <h1 class="h2 rise"><span class="kicker">Catering in Dubai &amp; across the UAE</span> Your event, <em class="it">fed properly.</em></h1>
      <p class="lede rise">Catering services and buffet setups for corporate events, parties, university events and weddings across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain. Every menu is built around your event and quoted by headcount.</p>
      <div class="actions">
        <a class="btn" href="#quote" data-messibot="catering">Get a quote</a>
        <a class="btn btn--ghost" href="{WA}?text=Hi%20Messify%2C%20I%27d%20like%20a%20catering%20quote." target="_blank" rel="noopener">WhatsApp us</a>
      </div>
      {rating_badge()}
      <div class="facts">
        <div><b>5,000+</b><span>meals a day of kitchen capacity</span></div>
        <div><b>6</b><span>emirates covered</span></div>
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
        <fieldset class="opt"><legend>Where</legend>{chips('emirate', CATER_EMIRATES, ['Dubai'], multi=False)}</fieldset>
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
      <li><b>Reliable logistics</b><span>On-time bulk delivery across six emirates.</span></li>
      <li><b>Your menu, your way</b><span>From a single main course to a full spread, built around your guests.</span></li>
    </ul>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="occasions-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Every occasion</p><h2 class="h2" id="occasions-title">Catering for every kind of event.</h2></div>
    {type_cards('event')}
    <div class="sec-head" style="margin:56px 0 28px"><p class="eyebrow">Seasonal and festive</p><h2 class="h3" id="season-title" style="font-size:1.6rem">Ramadan, Eid, Diwali, National Day and the festive season.</h2></div>
    {type_cards('occasion')}
  </div>
</section>

<section class="sec" aria-labelledby="uae-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Where we cater</p><h2 class="h2" id="uae-title">Catering across the UAE.</h2></div>
    {emirate_cards()}
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="steps-title">
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

<section class="sec" aria-labelledby="faq-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-title">Good to know.</h2></div>
    {faq_html(faqs)}
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="cguides-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Planning help</p><h2 class="h2" id="cguides-title">Catering guides.</h2><p class="lede">How much food to order, how catering is priced and what to sort before the day.</p></div>
    {guide_cards(CATERING_GUIDES)}
  </div>
</section>

{catering_form(tint=False)}'''
    render(page, body)

def catering_form(emirate='Dubai', title="Let's build your next event.", tint=True, event=None):
    opts = ''.join(f'<option{" selected" if e == emirate else ""}>{e}</option>' for e in CATER_EMIRATES)
    topts = ''.join(f'<option{" selected" if e == event else ""}>{e}</option>' for e in FORM_TYPES)
    return f'''<section class="sec{' sec--tint' if tint else ''}" id="quote" aria-labelledby="quote-title">
  <div class="wrap form-grid">
    <div>
      <p class="eyebrow">Get a quote</p>
      <h2 class="h2" id="quote-title">{title}</h2>
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
          <div class="field"><label for="q-type">Event type</label><select id="q-type" name="type" data-label="Event type">{topts}</select></div>
          <div class="field"><label for="q-emirate">Emirate</label><select id="q-emirate" name="emirate" data-label="Emirate">{opts}</select></div>
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

def emirate_cards(exclude=None):
    out = ''.join(f'<a class="emirate" href="/catering/{slug}/"><h3 class="h3">Catering in {c["name"]}</h3><p>{c["card"]}</p><span class="link-arrow">See catering in {c["short"]} {I["arrow"]}</span></a>'
                  for slug, c in CATER_AREAS.items() if slug != exclude)
    return f'<div class="emirates">{out}</div>'

# ---------------------------------------------------------------- about, privacy, 404
def page_about():
    cr, crs = crumbs([('Home', '/'), ('About Messify', '/about/')])
    plans = '; '.join(f'{mlabel(m)} {ln}: {aed(p)} ({t} meals, AED {per(p, t)} each)' for m, ln, t, p in PLANS)
    rows = [
        ('What Messify does', 'Daily meal plans and event catering in Dubai and the UAE.'),
        ('Where meals are cooked', 'Partner kitchen in International City, Dubai'),
        ('Meal plan delivery areas', 'Dubai International Academic City, Dubai Silicon Oasis, International City and Dubai Festival City (DFC) only'),
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
        ('Catering areas', 'Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain'),
        ('Google rating', f'{RATING} out of 5 on Google reviews'),
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

# ---------------------------------------------------------------- guides (content pages for search)
GUIDES = [
    ('/guides/best-meal-plans-dubai/', 'The best meal plans in Dubai, compared',
     'Messify, Right Bite, Calo, Kcal, VMeals and Meals On Me side by side, with published prices and who each one suits.'),
    ('/guides/affordable-meal-plans-dubai/', 'Affordable meal plans in Dubai',
     'How to keep a meal plan affordable: price per meal, which plan costs least, using every meal, and a comparison with ordering in.'),
    ('/guides/meal-plan-cost-dubai/', 'How much does a meal plan cost in Dubai?',
     'What you actually pay per meal, what pushes the price up, and a calculator to compare a meal plan with ordering in.'),
    ('/guides/student-meal-plans-dubai/', 'Student meal plans in Dubai',
     'Budgets, exam weeks, residences in Academic City and Silicon Oasis, and how to pick a plan that fits a semester.'),
    ('/guides/weekly-vs-monthly-meal-plan/', 'Weekly or monthly meal plan: which is better?',
     'The real difference in price per meal and flexibility, and who should start with which.'),
    ('/guides/office-lunch-delivery-silicon-oasis/', 'Office lunch delivery in Dubai Silicon Oasis',
     'Lunch on your desk before the 1 PM rush: how morning delivery works, prices, team plans and work-from-home days.'),
    ('/guides/meal-delivery-dubai-festival-city/', 'Daily meal delivery in Dubai Festival City',
     'Meal plans for Al Badia homes and offices in DFC: how morning delivery works, prices and how to start.'),
]

def article_schema(path, headline, desc, published='2026-10-13'):
    return {'@type': 'Article', '@id': BASE + path + '#article', 'headline': headline, 'description': desc,
            'url': BASE + path, 'mainEntityOfPage': BASE + path, 'inLanguage': 'en-AE', 'image': OG_IMAGE,
            'datePublished': published, 'dateModified': TODAY,
            'author': {'@id': BASE + '/#organization'}, 'publisher': {'@id': BASE + '/#organization'}}

def guide_cards(guides, exclude=None, tag='h3'):
    items = ''.join(f'<a class="reason guide-card" href="{p}"><{tag}>{t}</{tag}><p>{d}</p><span class="link-arrow">Read the guide {I["arrow"]}</span></a>'
                    for p, t, d in guides if p != exclude)
    return f'<div class="reasons">{items}</div>'

def guide_more(exclude, guides=None):
    return f'''<section class="sec sec--tint sec--tight" aria-labelledby="more-guides">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:28px"><p class="eyebrow">Guides</p><h2 class="h3" id="more-guides" style="font-size:1.4rem">Keep reading</h2></div>
    {guide_cards([g for g in (guides or GUIDES) if g[0] != exclude][:6])}
  </div>
</section>'''

def band_catering(title='Planning an event?', text="Send your date, location and headcount, and we'll come back with a menu and a price."):
    return f'''<section class="sec">
  <div class="wrap">
    <div class="band band--walnut">
      <div><h2 class="h2">{title}</h2><p class="lede">{text}</p></div>
      <div class="actions" style="margin-top:0">
        <a class="btn" href="/catering/#quote" data-messibot="catering">Get a quote</a>
        <a class="btn btn--ghost" href="{WA}?text={quote("Hi Messify, I'd like a catering quote.")}" target="_blank" rel="noopener">WhatsApp us</a>
      </div>
    </div>
  </div>
</section>'''

def read_time(htmltext):
    import re
    words = len(re.sub(r'<[^>]+>', ' ', htmltext).split())
    return max(3, round(words / 200))

def article_page(path, crumb, title, desc, h1, kicker, quick, sections, faqs, extra_after='', kind='meals', published='2026-10-13'):
    cr, crs = crumbs([('Home', '/'), ('Guides', '/guides/'), (crumb, path)])
    page = {'path': path, 'mode': kind, 'nav': kind, 'title': title, 'desc': desc,
            'schema': [ORG, BUSINESS, article_schema(path, h1, desc, published), faq_schema(faqs), crs]}
    if kind == 'catering':
        page.update({'cta': ('/catering/#quote', 'Get a quote', 'Quote'), 'cta_bot': 'catering'})
    mins = read_time(quick + sections + ''.join(q + a for q, a in faqs))
    body = f'''<section class="sec sec--first">
  <div class="wrap article">
    {cr}
    <h1 class="h2"><span class="kicker">{kicker}</span> {h1}</h1>
    <p class="byline">By the Messify team · Updated {UPDATED_LABEL} · {mins} min read</p>
    <div class="answer">
      <p class="answer__label">Quick answer</p>
      <p class="answer__lead">{quick}</p>
    </div>
    {sections}
    <h2 id="faq">Questions people ask</h2>
    {faq_html(faqs, open_first=False)}
  </div>
</section>
{extra_after}
{guide_more(path, CATERING_GUIDES if kind == 'catering' else GUIDES)}
{band_catering() if kind == 'catering' else band()}'''
    render(page, body)

def calculator():
    return f'''<div class="calc" data-calc id="calculator">
      <p class="answer__label">Calculator</p>
      <h3 class="calc__title">Meal plan vs ordering in</h3>
      <fieldset class="field">
        <legend>Meals a day</legend>
        <div class="seg seg--3">
          <label><input type="radio" name="calc-meals" value="1"><span>1 meal</span></label>
          <label><input type="radio" name="calc-meals" value="2" checked><span>2 meals</span></label>
          <label><input type="radio" name="calc-meals" value="3"><span>3 meals</span></label>
        </div>
      </fieldset>
      <div class="field"><label for="calc-spend">What you usually spend per delivery order (AED, including fees)</label>
        <input id="calc-spend" type="number" inputmode="decimal" min="10" max="300" step="1" value="45"></div>
      <div class="calc__out" aria-live="polite">
        <div><small>Ordering in, 26 days</small><b data-calc-order>AED 2,340</b></div>
        <div><small>Messify monthly plan</small><b data-calc-plan>AED 1,400</b></div>
        <div class="calc__diff"><small>Difference a month</small><b data-calc-diff>AED 940</b></div>
      </div>
      <p class="fine">AED 45 is only a starting example. Change it to what you really spend, including delivery and service fees. Messify figures use the monthly plan: 26 days of meals to use within 30 days.</p>
    </div>'''

def page_guides():
    cr, crs = crumbs([('Home', '/'), ('Guides', '/guides/')])
    page = {'path': '/guides/', 'mode': 'meals', 'nav': 'meals', 'title': 'Meal Plan & Catering Guides for Dubai | Messify',
            'desc': 'Straight answers about meal plans and catering in Dubai: costs, student plans, food per guest, catering prices and event checklists.',
            'schema': [ORG, {'@type': 'CollectionPage', '@id': BASE + '/guides/#page', 'url': BASE + '/guides/', 'name': 'Messify guides',
                             'hasPart': [{'@id': BASE + p + '#article'} for p, _, _ in GUIDES + CATERING_GUIDES]}, crs]}
    body = f'''<section class="sec sec--first">
  <div class="wrap">
    {cr}
    <div class="sec-head" style="max-width:760px">
      <h1 class="h2"><span class="kicker">Guides</span> Meal plans and catering in Dubai, explained.</h1>
      <p class="lede">Straight answers to the questions we get every day on WhatsApp, with real prices.</p>
    </div>
    <h2 class="h3" id="meal-plan-guides" style="margin:0 0 20px">Meal plan guides</h2>
    {guide_cards(GUIDES, tag='h3')}
  </div>
</section>
<section class="sec sec--tint" aria-labelledby="catering-guides">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Planning an event</p><h2 class="h2" id="catering-guides">Catering guides.</h2>
      <p class="lede">How much food to order, how catering is priced and what to sort before the day. See <a href="/catering/">our catering</a>.</p></div>
    {guide_cards(CATERING_GUIDES, tag='h3')}
  </div>
</section>
{band()}'''
    render(page, body)

def page_guide_cost():
    p = {m: {ln: (t, pr) for mm, ln, t, pr in PLANS if mm == m} for m in (1, 2, 3)}
    sections = f'''
    <h2>The number that matters: price per meal</h2>
    <p>Meal plans in Dubai are sold in very different ways: by the week, by the month, by calories or by number of meals. The only fair way to compare them is the price of one meal: <b>plan price ÷ number of meals</b>. Then check what that price includes, because delivery fees, VAT and how many days you get to use your meals change the real cost.</p>
    <p>Broadly, Dubai meal plans fall into two groups. <b>Diet and fitness plans</b> (calorie-counted, macro-tracked, often with snacks and juices) cost the most per meal. <b>Everyday meal plans</b>, which replace ordering in or cooking, cost less and are built around normal home-style meals. Messify is an everyday meal plan. See how Dubai's meal plans <a href="/guides/best-meal-plans-dubai/">compare side by side</a>.</p>

    <h2>What a Messify meal plan costs</h2>
    <p>Every price below is for the whole plan. Each meal is one token you can use for breakfast, lunch or dinner.</p>
    {plans_table('Messify meal plan prices in Dubai (AED)')}
    <p>The cheapest price per meal is the 3-meal monthly plan at <b>AED {per(p[3]['monthly'][1], p[3]['monthly'][0])}</b>. The lowest total price is the 1-meal weekly plan at <b>AED {p[1]['weekly'][1]}</b>, which is the easiest way to try us. Monthly plans are 26 days of meals to use within 30 days; weekly plans are 7 days of meals to use within 9 days. Prices include VAT unless stated otherwise.</p>

    <h2>Meal plan vs ordering in: run your own numbers</h2>
    <p>Most people who start a meal plan were ordering in before. Put in what you usually spend on one delivery order, including delivery and service fees, and compare it with a month of Messify.</p>
    {calculator()}

    <h2>Five things that change the real price</h2>
    <ol>
      <li><b>Meals you actually eat.</b> A cheap plan you can't fully use is expensive. Check how long you have to use your meals and whether you can skip days. With Messify you skip a day in the app and use that meal later in your plan.</li>
      <li><b>Delivery.</b> Some services charge per delivery or per drop. Messify delivers all of the day's meals together every morning in one chilled bag.</li>
      <li><b>Menu variety.</b> If you get bored by week two, you'll go back to ordering in. Messify's menu changes every day and you pick tomorrow's meals in the app by 6 PM.</li>
      <li><b>Dietary fit.</b> Every Messify meal is 100% halal and there's a vegetarian option every day, for every meal.</li>
      <li><b>Where you live.</b> Plans only help if they deliver to you. Messify meal plans deliver to Dubai Academic City, Dubai Silicon Oasis, International City and Dubai Festival City.</li>
    </ol>

    <h2>Is a meal plan worth it?</h2>
    <p>If you mostly order in, a meal plan usually costs less per meal and removes the daily decision of what to eat. If you cook most of your meals and enjoy it, cooking is cheaper on ingredients. Many students and professionals in Dubai sit in between: no time or kitchen to cook properly, and tired of delivery apps. That's who an everyday meal plan is for.</p>
    <p>See every plan on our <a href="/meal-plans/">meal plans in Dubai</a> page, or check delivery in <a href="/meal-plans/academic-city/">Academic City</a>, <a href="/meal-plans/silicon-oasis/">Silicon Oasis</a>, <a href="/meal-plans/international-city/">International City</a> and <a href="/meal-plans/festival-city/">Dubai Festival City</a>.</p>'''
    faqs = [
        ('How much is a meal plan in Dubai per month?', f"It depends on the type of plan. Messify monthly plans cost AED {p[1]['monthly'][1]:,} for 1 meal a day, AED {p[2]['monthly'][1]:,} for 2 and AED {p[3]['monthly'][1]:,} for 3, which works out to AED 25.63 to 27.50 per meal. Diet and fitness plans with calorie tracking usually cost more per meal."),
        ('What is the cheapest way to get a meal plan in Dubai?', 'Compare the price per meal, not the plan price. With Messify, the 3-meal monthly plan has the lowest price per meal, at AED 25.63. The 1-meal weekly plan, at AED 215, is the cheapest way to try it.'),
        ('Is a weekly meal plan more expensive than a monthly one?', f"Per meal, yes. A Messify weekly plan costs AED {per(p[1]['weekly'][1], p[1]['weekly'][0])} to {per(p[3]['weekly'][1], p[3]['weekly'][0])} per meal, while monthly plans cost AED 25.63 to 27.50. Weekly plans are the easy way to try us first."),
        ('Do Messify prices include VAT?', 'Yes. Prices include VAT unless stated otherwise.'),
        ('Can I skip days on a meal plan?', 'With Messify, yes. Skip a day in the app and use that meal on another day of your plan. Monthly plans give you 30 days to use 26 days of meals; weekly plans give you 9 days to use 7.'),
    ]
    article_page('/guides/meal-plan-cost-dubai/', 'Meal plan cost', 'How Much Does a Meal Plan Cost in Dubai? (2026) | Messify',
                 'What meal plans in Dubai really cost per meal, what changes the price, and a calculator to compare a meal plan with ordering in.',
                 'How much does a meal plan cost in Dubai?', 'Meal plan prices · 2026',
                 f"Compare meal plans by price per meal. Messify meal plans in Dubai cost AED 25.63 to 30.71 per meal: AED 215–610 a week or AED 715–1,999 a month for 1 to 3 meals a day. Diet and fitness plans with calorie tracking usually cost more per meal.",
                 sections, faqs)

def page_guide_students():
    sections = f'''
    <h2>Why students in Dubai use meal plans</h2>
    <p>Student life in Dubai makes eating well harder than it should be. Residences often have small or shared kitchens, lectures and labs run through lunch, and delivery apps add up fast. A meal plan fixes the daily question of what to eat and puts a ceiling on what you spend on food each month.</p>

    <h2>What a student meal plan costs</h2>
    <p>Messify plans start from AED 25 a meal. Most students pick one of these:</p>
    <ul>
      <li><b>1 meal a day, monthly: AED 715.</b> Lunch or dinner sorted, AED 27.50 a meal.</li>
      <li><b>2 meals a day, monthly: AED 1,400.</b> Lunch and dinner, AED 26.92 a meal.</li>
      <li><b>1 meal a day, weekly: AED 215.</b> The easiest way to try it before committing to a month.</li>
    </ul>
    <p>Monthly plans are 26 days of meals to use within 30 days, and weekly plans are 7 days of meals to use within 9 days. Compare it with your delivery spending in our <a href="/guides/meal-plan-cost-dubai/#calculator">meal plan vs ordering in calculator</a>.</p>

    <h2>Where we deliver for students</h2>
    <p>Messify meals are cooked daily in our partner kitchen in International City and delivered every morning to:</p>
    <ul>
      <li><a href="/meal-plans/academic-city/">Dubai Academic City (DIAC)</a>: University of Birmingham Dubai, Middlesex University Dubai, Manipal Academy of Higher Education, BITS Pilani Dubai Campus, Amity University Dubai, Curtin University Dubai, plus residences such as KSK Homes and The Myriad.</li>
      <li><a href="/meal-plans/silicon-oasis/">Dubai Silicon Oasis (DSO)</a>: RIT Dubai and DSOA University Residence.</li>
      <li><a href="/meal-plans/international-city/">International City</a>: every cluster.</li>
    </ul>
    <p class="disclaim">Universities and residences are named only to describe where we deliver. Messify is not affiliated with them.</p>

    <h2>Exams, trips home and long weekends</h2>
    <p>Your week won't always be the same, and your plan shouldn't punish you for it. With Messify, every meal is a token: skip a busy day in the app and use that meal on another day of your plan, or double up when a friend comes over. Going home for the break? Start a weekly plan, or start your monthly plan when you're back.</p>

    <h2>Halal, vegetarian and variety</h2>
    <p>Every Messify meal is 100% halal, and there's a vegetarian option every day, for every meal. The menu changes daily, so you won't be eating the same thing all week. You see tomorrow's menu in the app and choose your meals by 6 PM.</p>

    <h2>How to choose a student meal plan</h2>
    <ol>
      <li><b>Check delivery to your exact building</b> before paying.</li>
      <li><b>Compare price per meal</b>, not the plan price.</li>
      <li><b>Check how long you have to use your meals</b> and whether you can skip days.</li>
      <li><b>Look at the menu</b>: does it change often enough that you'll keep eating it?</li>
      <li><b>Start small.</b> A weekly plan is a cheap way to test the food and the delivery.</li>
    </ol>
    <p>Ready? See all <a href="/meal-plans/">meal plans in Dubai</a> or <a href="/start/">start your plan</a> in the Messify app.</p>'''
    faqs = [
        ('What is the best meal plan for students in Dubai?', 'The best student meal plan is one that delivers to your building, fits your budget per meal and lets you skip busy days. Messify delivers to Academic City, Silicon Oasis and International City from AED 25 a meal, and every meal is a token you can use on another day of your plan.'),
        ('How much should a student spend on food in Dubai?', 'It varies widely. A useful benchmark: a Messify 2-meal monthly plan is AED 1,400, or AED 26.92 a meal. Use our calculator to compare that with what you spend ordering in.'),
        ('Do you deliver to KSK Homes, The Myriad and DSOA University Residence?', 'Yes. We deliver every morning to KSK Homes and The Myriad in Academic City, and to DSOA University Residence in Silicon Oasis.'),
        ('Can I pause my meal plan during exams?', 'You can skip days in the app and use those meals on other days of your plan. Monthly plans give you 30 days to use 26 days of meals; weekly plans give you 9 days to use 7.'),
        ('Is the food halal?', 'Yes. Every Messify meal is 100% halal, with a vegetarian option every day, for every meal.'),
    ]
    article_page('/guides/student-meal-plans-dubai/', 'Student meal plans', 'Student Meal Plans in Dubai: Prices & Delivery | Messify',
                 'A practical guide to student meal plans in Dubai: costs per meal, delivery to Academic City and Silicon Oasis residences, exams and halal food.',
                 'Student meal plans in Dubai', 'For students · 2026',
                 'Student meal plans in Dubai with Messify start from AED 25 a meal, delivered every morning to Dubai Academic City, Silicon Oasis and International City. A 2-meal monthly plan costs AED 1,400 (AED 26.92 a meal), and you can skip busy days and use those meals later in your plan.',
                 sections, faqs)

def page_guide_weekly_monthly():
    rows = ''.join(
        f'<tr><th scope="row">{mlabel(m)}</th>'
        + ''.join(f'<td class="num">{aed(pr)}<br><small>AED {per(pr, t)} a meal</small></td>' for mm, ln, t, pr in PLANS if mm == m and ln == 'weekly')
        + ''.join(f'<td class="num">{aed(pr)}<br><small>AED {per(pr, t)} a meal</small></td>' for mm, ln, t, pr in PLANS if mm == m and ln == 'monthly')
        + '</tr>' for m in (1, 2, 3))
    table = f'''<div class="table-wrap"><table class="ptable">
  <caption>Messify weekly vs monthly meal plans (AED)</caption>
  <thead><tr><th scope="col">Meals a day</th><th scope="col" class="num">Weekly (7 days of meals)</th><th scope="col" class="num">Monthly (26 days of meals)</th></tr></thead>
  <tbody>{rows}</tbody></table></div>'''
    sections = f'''
    <h2>The short version</h2>
    <ul>
      <li><b>Choose weekly</b> if you're trying a meal plan for the first time, your schedule is unpredictable, or you're only in Dubai for part of the month.</li>
      <li><b>Choose monthly</b> once you know you like the food: it gives you the best price per meal and covers your whole month.</li>
    </ul>

    <h2>Price per meal, side by side</h2>
    {table}
    <p>On every plan size, monthly costs less per meal. On the 2-meal plan, for example, you pay AED 26.92 a meal monthly against AED 29.64 weekly.</p>

    <h2>Flexibility</h2>
    <p>Both plans work the same way: every meal is a token you can use for breakfast, lunch or dinner, and you can skip a day and have that meal later in your plan. Weekly plans are 7 days of meals to use within 9 days. Monthly plans are 26 days of meals to use within 30 days, which leaves room for weekends away and busy days.</p>

    <h2>Who usually picks which</h2>
    <ul>
      <li><b>First-time customers:</b> weekly, then switch to monthly.</li>
      <li><b>Students during term:</b> monthly. Around exams and trips home, weekly.</li>
      <li><b>Office workers in Silicon Oasis:</b> monthly, often 1 or 2 meals a day for workday lunches and dinners.</li>
      <li><b>Teams:</b> monthly office plans with one morning delivery for everyone.</li>
    </ul>
    <p>See every option on our <a href="/meal-plans/">meal plans in Dubai</a> page, or read <a href="/guides/meal-plan-cost-dubai/">how much a meal plan costs in Dubai</a>.</p>'''
    faqs = [
        ('Is a monthly meal plan cheaper than a weekly one?', 'Per meal, yes. Messify monthly plans cost AED 25.63 to 27.50 a meal; weekly plans cost AED 29.05 to 30.71 a meal.'),
        ('How long do I have to use a weekly or monthly plan?', 'Weekly plans are 7 days of meals to use within 9 days. Monthly plans are 26 days of meals to use within 30 days.'),
        ('Can I switch from weekly to monthly?', 'Yes. Most people start with a week to try the food, then choose a monthly plan in the app.'),
        ('Which plan is best for students?', 'Monthly during term for the best price per meal; weekly around exams, trips home or if you are trying Messify for the first time.'),
    ]
    article_page('/guides/weekly-vs-monthly-meal-plan/', 'Weekly vs monthly', 'Weekly vs Monthly Meal Plans in Dubai | Messify',
                 'Weekly or monthly meal plan? Compare the price per meal, flexibility and who each plan suits, with real Messify prices in Dubai.',
                 'Weekly or monthly meal plan: which is better?', 'Choosing a plan · 2026',
                 'Monthly meal plans cost less per meal: Messify monthly plans are AED 25.63 to 27.50 a meal against AED 29.05 to 30.71 on weekly plans. Start weekly if you want to try the food first, then switch to monthly.',
                 sections, faqs)

def page_guide_best():
    checked = '13 October 2026'
    providers = [
        # name, type, published price, what stands out, source url
        ('Messify', 'Everyday meal plan', 'AED 25.63–30.71 a meal (AED 215 a week, AED 715 a month and up)',
         'Breakfast, lunch and dinner delivered together each morning; skip a day and use the meal later; 100% halal with a vegetarian option every meal',
         '/meal-plans/'),
        ('Right Bite', 'Diet & nutrition plans', 'From AED 22 a meal (Essentials); goal-based plans from AED 25–42 a meal',
         'Wide range of goal plans, including weight loss, diabetic and GLP-1 support', 'https://rightbite.com/en-ae/subscribe-to-a-plan'),
        ('Calo', 'Diet & nutrition plans', 'From AED 46.88 a day (minimum 2 meals a day)',
         'Personalised plans such as balanced, custom macros, low-carb, high-protein and vegetarian; weekly, monthly or 3-month payment', 'https://calo.app/en-ae/plans-and-packages'),
        ('Kcal', 'Diet & nutrition plans', 'Offer from AED 2,116 a month on an 8-week plan',
         'Large rotating menu of portion-controlled meals; offers built around 4, 8 and 12-week plans', 'https://kcallife.com/get-started/'),
        ('VMeals', 'Diet plans', 'From AED 81 a day (vegetarian); other diets from AED 88–111 a day',
         'Diet-specific plans including Indian fusion, keto, and gluten and dairy free', 'https://vmeals.ae/'),
        ('Meals On Me', 'Calorie-counted plans', 'Prices on request',
         'Goal-based plans plus lunch and dinner plans in Arabic, Indian, keto and vegetarian styles', 'https://hellomealsonme.com/'),
    ]
    def link(name, url):
        return f'<a href="{url}">{name}</a>' if url.startswith('/') else f'<a href="{url}" target="_blank" rel="nofollow noopener">{name}</a>'
    rows = ''.join(f'<tr><th scope="row">{link(n, u)}</th><td data-label="Type">{t}</td><td data-label="Published price">{p}</td></tr>' for n, t, p, s, u in providers)
    table = f'''<div class="table-wrap"><table class="ptable ptable--wrap">
  <caption>Dubai meal plans compared: published starting prices, checked {checked}</caption>
  <thead><tr><th scope="col">Company</th><th scope="col">Type</th><th scope="col">Published price</th></tr></thead>
  <tbody>{rows}</tbody></table></div>'''
    profiles = ''.join(f'<h3>{n}</h3><p><b>{t}.</b> {s}. Published price: {p if p.startswith('AED') else p[0].lower() + p[1:]}. {"See <a href=\"/meal-plans/\">Messify meal plans</a>." if u.startswith("/") else f"Source: {link(n + chr(39) + "s website", u)}."}</p>' for n, t, p, s, u in providers)
    sections = f'''
    <p>We're Messify, so we're not neutral. To keep this useful, we've stuck to what each company publishes on its own website, linked every source, and listed prices exactly as shown on {checked}. Prices and offers change often, so check the latest before you buy.</p>

    <h2>Dubai meal plans at a glance</h2>
    {table}
    <p>Plans are priced in different ways (per meal, per day or per month), so compare carefully. Our <a href="/guides/meal-plan-cost-dubai/">meal plan cost guide</a> explains how to work out the price per meal.</p>

    <h2>Two kinds of meal plan</h2>
    <p><b>Diet and nutrition plans</b> are built around a goal: weight loss, muscle gain, calorie targets or a specific diet such as keto. Most of the well-known names in Dubai, including Calo, Right Bite, Kcal and VMeals, are in this group.</p>
    <p><b>Everyday meal plans</b> replace ordering in or cooking. They focus on normal, balanced, home-style food at a predictable price, without calorie tracking. Messify is an everyday meal plan.</p>

    <h2>The companies, one by one</h2>
    {profiles}

    <h2>Which meal plan is best for you?</h2>
    <ul>
      <li><b>You want to lose weight or hit macros:</b> a diet plan such as Calo, Right Bite, Kcal or VMeals, which are built for calorie and macro targets.</li>
      <li><b>You want the lowest published price per meal:</b> Right Bite lists its Essentials plan from AED 22 a meal; Messify's 3-meal monthly plan is AED 25.63 a meal. Check what each price includes and how many days you get to use your meals.</li>
      <li><b>You live, work or study in Academic City, Silicon Oasis, International City or Dubai Festival City and just want your everyday meals sorted:</b> Messify, from AED 25 a meal, with the whole day's meals delivered every morning.</li>
      <li><b>You need vegetarian food:</b> Messify has a vegetarian option every day, for every meal; Calo, VMeals and Meals On Me also list vegetarian plans.</li>
      <li><b>Your schedule changes week to week:</b> look for plans that let you skip days. With Messify, every meal is a token you can use later in your plan.</li>
    </ul>

    <h2>How to choose: a 5-point checklist</h2>
    <ol>
      <li><b>Delivery to your exact building.</b> Coverage varies a lot between companies.</li>
      <li><b>Price per meal</b>, not the headline plan price.</li>
      <li><b>Days to use your meals</b>, and whether you can skip or pause.</li>
      <li><b>Menu variety</b>, so you keep eating it after week two.</li>
      <li><b>Dietary needs:</b> halal, vegetarian, allergies or a specific diet.</li>
    </ol>'''
    faqs = [
        ('What is the best meal plan in Dubai?', 'It depends on your goal. For weight loss or calorie targets, diet plans such as Calo, Right Bite, Kcal and VMeals are built for that. For everyday meals at a predictable price in Academic City, Silicon Oasis, International City or Dubai Festival City, Messify starts from AED 25 a meal.'),
        ('What is the cheapest meal plan in Dubai?', f'Of the published prices we checked on {checked}, Right Bite listed its Essentials plan from AED 22 a meal, and Messify\'s 3-meal monthly plan is AED 25.63 a meal. Compare what each price includes, delivery coverage and how long you have to use your meals.'),
        ('Are Dubai meal plans halal?', 'Every Messify meal is 100% halal. Check each company\'s website for its own policy.'),
        ('Which Dubai meal plans have vegetarian options?', 'Messify has a vegetarian option every day, for every meal. Calo, VMeals and Meals On Me also list vegetarian plans.'),
        ('Can I skip days on a meal plan?', 'With Messify, yes: skip a day in the app and use that meal later in your plan. Monthly plans give you 30 days to use 26 days of meals, and weekly plans give you 9 days to use 7.'),
    ]
    article_page('/guides/best-meal-plans-dubai/', 'Best meal plans in Dubai', 'Best Meal Plans in Dubai 2026: Prices Compared | Messify',
                 'Dubai meal plans compared with published prices: Messify, Right Bite, Calo, Kcal, VMeals and Meals On Me. What each costs and who it suits.',
                 'The best meal plans in Dubai, compared', 'Updated October 2026',
                 f'The best meal plan in Dubai depends on your goal. For weight loss and macros, diet plans like Calo, Right Bite, Kcal and VMeals lead. For everyday meals, Messify costs AED 25.63–30.71 a meal and delivers all the day\'s meals every morning in Academic City, Silicon Oasis, International City and Dubai Festival City. Prices below are as published on {checked}.',
                 sections, faqs)

def page_guide_office_dso():
    sections = f'''
    <h2>The lunch problem in Silicon Oasis</h2>
    <p>Dubai Silicon Oasis is full of offices, business centres and tech companies, and most of them hit the same wall around 1 PM. Everyone orders at once, riders queue at the same buildings, and lunch turns up late, or not until after the next meeting. Then it happens again tomorrow, with the same daily question of what to order and the same delivery fees.</p>
    <p>There are three common ways to fix it: order in every day, bring food from home, or get lunch delivered before the workday starts. This guide walks through what each one costs you in time and money, and how to set up the third.</p>

    <h2>Three ways to sort office lunch</h2>
    <ul>
      <li><b>Ordering in every day.</b> The most choice, but you decide every day, pay delivery and service fees on each order, and depend on the lunchtime rush.</li>
      <li><b>Bringing lunch from home.</b> Low cost on ingredients, but it needs time to cook and pack, which is exactly what most people working in DSO are short of.</li>
      <li><b>A morning meal plan delivery.</b> Your meals arrive before work, so lunch is already on your desk or in the office fridge when you get hungry. You pay one plan price and choose your meals ahead in an app.</li>
    </ul>

    <h2>How Messify office lunch delivery works</h2>
    <ol>
      <li><b>Pick a plan.</b> 1, 2 or 3 meals a day, weekly or monthly. Many office workers start with 1 meal a day for lunch, or 2 for lunch and dinner.</li>
      <li><b>Choose tomorrow's meals by 6 PM.</b> The menu changes every day, and you see it in the Messify app the day before.</li>
      <li><b>Get your bag every morning.</b> All of the day's meals arrive together in one chilled bag with an ice pack, delivered to your office or your home in Silicon Oasis.</li>
      <li><b>Reheat and eat.</b> Meals are blast-chilled after cooking, so keep lunch cold until you're ready, then reheat it for a few minutes.</li>
    </ol>
    <p>Meals are cooked fresh every day in our partner kitchen in nearby International City. Every meal is 100% halal, and there's a vegetarian option every day, for every meal.</p>

    <h2>What it costs</h2>
    <p>Messify meal plans start from AED 25 a meal. For a working lunch, these are the usual starting points:</p>
    <ul>
      <li><b>1 meal a day, weekly: AED 215.</b> The easiest way to try office lunch delivery for a week.</li>
      <li><b>1 meal a day, monthly: AED 715.</b> 26 days of meals to use within 30 days, AED 27.50 a meal.</li>
      <li><b>2 meals a day, monthly: AED 1,400.</b> Lunch at work and dinner at home, AED 26.92 a meal.</li>
    </ul>
    <p>To see how that compares with what you spend on delivery apps, use our <a href="/guides/meal-plan-cost-dubai/#calculator">meal plan vs ordering in calculator</a>. Every price is on our <a href="/meal-plans/">meal plans in Dubai</a> page.</p>

    <h2>Weekends, leave and days you work from home</h2>
    <p>Office weeks are rarely the same. With Messify, every meal is a token: skip a day in the app and use that meal later in your plan. Weekly plans give you 9 days to use 7 days of meals, and monthly plans give you 30 days to use 26 days of meals, which leaves room for weekends, leave and days at home.</p>

    <h2>Lunch for the whole team</h2>
    <p>If several people in your office want lunch sorted, a team plan keeps it simple: one monthly plan, one morning delivery for everyone, and each person still chooses their own meals in the app. Message us on WhatsApp with your team size and office location and we'll set it up.</p>
    <p>Planning a one-off meeting lunch, a launch or a company event instead? That's catering: custom menus quoted by headcount, with buffet setups if you want them. See <a href="/catering/">corporate catering in Dubai</a>.</p>

    <h2>A quick checklist before you start</h2>
    <ol>
      <li><b>Confirm delivery to your building.</b> Message us your building in DSO and we'll confirm the drop-off point.</li>
      <li><b>Check there's a fridge and a microwave</b> at the office, or a pantry you can use.</li>
      <li><b>Decide on 1 or 2 meals a day:</b> lunch only, or lunch plus dinner at home.</li>
      <li><b>Try a week first</b>, then move to monthly for a lower price per meal.</li>
    </ol>
    <p>Read more about delivery in <a href="/meal-plans/silicon-oasis/">meal plans in Dubai Silicon Oasis</a>, or <a href="/start/">start your plan</a> in the Messify app.</p>'''
    faqs = [
        ('Do you deliver lunch to offices in Dubai Silicon Oasis?', "Yes. Messify delivers every morning to offices and business centres across Dubai Silicon Oasis. All of the day's meals arrive together in one chilled bag, so lunch is sorted before the workday starts."),
        ('How much does office lunch delivery cost in Silicon Oasis?', 'Messify meal plans start from AED 25 a meal. A 1-meal weekly plan costs AED 215, and a 1-meal monthly plan costs AED 715, or AED 27.50 a meal.'),
        ('Can our whole team get lunch delivered together?', 'Yes. Teams can share one monthly plan with one morning delivery for everyone, and each person chooses their own meals in the app. Message us on WhatsApp with your team size and office location.'),
        ('What if I work from home some days?', 'Skip that day in the app and use the meal later in your plan. Monthly plans give you 30 days to use 26 days of meals, and weekly plans give you 9 days to use 7.'),
        ('Is the food halal? Are there vegetarian options?', 'Every Messify meal is 100% halal, and there is a vegetarian option every day, for every meal.'),
    ]
    article_page('/guides/office-lunch-delivery-silicon-oasis/', 'Office lunch in Silicon Oasis',
                 'Office Lunch Delivery in Dubai Silicon Oasis | Messify',
                 'How to sort office lunch in Dubai Silicon Oasis: morning delivery, prices from AED 25 a meal, team plans and what to do on work-from-home days.',
                 'Office lunch delivery in Dubai Silicon Oasis', 'For offices in DSO · 2026',
                 'Messify delivers office lunch in Dubai Silicon Oasis every morning, before the lunchtime rush. All of the day\'s meals arrive together in one chilled bag, from AED 25 a meal (AED 215 for a 1-meal weekly plan). Teams can share one monthly plan with one delivery for everyone.',
                 sections, faqs)

def page_guide_dfc():
    sections = f'''
    <h2>Everyday meals in DFC, without the daily decision</h2>
    <p>Dubai Festival City has no shortage of places to eat. The harder part is the everyday: deciding what to have three times a day, paying delivery and service fees on every order, and waiting on riders when everyone in Al Badia or the office towers orders at the same time. A daily meal plan takes that decision off your plate. You choose your meals ahead in an app, and they arrive every morning.</p>
    <p>Messify now delivers meal plans in Dubai Festival City (DFC), alongside Dubai Academic City, Dubai Silicon Oasis and International City. This guide explains how it works, what it costs and who it suits.</p>

    <h2>How daily meal delivery works in Dubai Festival City</h2>
    <ol>
      <li><b>Pick a plan</b> in the Messify app: 1, 2 or 3 meals a day, weekly or monthly.</li>
      <li><b>Choose tomorrow's meals by 6 PM.</b> The menu changes every day, and you see it in the app the day before.</li>
      <li><b>Get your bag every morning.</b> All of the day's meals arrive together in one chilled bag with an ice pack, at your home or your office in DFC.</li>
      <li><b>Reheat and eat.</b> Meals are blast-chilled after cooking. Keep them cold, then reheat for a few minutes when you're ready.</li>
    </ol>
    <p>Every meal is cooked fresh daily in our partner kitchen in International City and is 100% halal, with a vegetarian option every day, for every meal.</p>

    <h2>What a meal plan costs in DFC</h2>
    <p>Prices are the same in Dubai Festival City as in every Messify area, from AED 25 a meal:</p>
    <ul>
      <li><b>Weekly:</b> AED 215, 415 or 610 for 1, 2 or 3 meals a day (7 days of meals to use within 9 days).</li>
      <li><b>Monthly:</b> AED 715, 1,400 or 1,999 for 1, 2 or 3 meals a day (26 days of meals to use within 30 days).</li>
    </ul>
    <p>The 2-meal monthly plan, lunch and dinner sorted, works out to AED 26.92 a meal. To compare with what you spend on delivery apps now, try our <a href="/guides/meal-plan-cost-dubai/#calculator">meal plan vs ordering in calculator</a>, or see every option on our <a href="/meal-plans/">meal plans in Dubai</a> page.</p>

    <h2>For people living in Al Badia and around DFC</h2>
    <p>If you live in Al Badia Residences, Al Badia Hillside Village or elsewhere in Dubai Festival City, a 2 or 3-meal plan covers most of your day: breakfast before work, lunch to take with you, dinner ready when you get home. Because everything arrives together in the morning, there's no waiting in for a rider at 8 PM.</p>

    <h2>For people working in Dubai Festival City</h2>
    <p>Office lunch is where a meal plan helps most. Your meals are delivered to your office in the morning, so lunch is waiting before the 1 PM rush. Several colleagues interested? Teams can share one monthly plan with one morning delivery for everyone, while each person still chooses their own meals in the app. Planning a meeting lunch or company event instead? See our <a href="/catering/">catering in Dubai</a>.</p>

    <h2>Weekends, travel and nights out</h2>
    <p>Every meal on a Messify plan is a token. Skip a day in the app and use that meal on another day of your plan, or spend extra tokens to double up when a friend comes over. Monthly plans give you 30 days to use 26 days of meals, so a weekend away doesn't cost you anything.</p>

    <h2>How to start in DFC</h2>
    <p>Orders aren't taken on this website. There are two ways to start:</p>
    <ul>
      <li><b>Download the Messify app</b>, choose your plan and pay in the app.</li>
      <li><b>Message us on WhatsApp</b> with your building in Dubai Festival City, and a real person on our team will help you choose and get started.</li>
    </ul>
    <p>Read more on our <a href="/meal-plans/festival-city/">meal plans in Dubai Festival City</a> page, or <a href="/start/">start your plan</a>.</p>'''
    faqs = [
        ('Is there a meal plan that delivers in Dubai Festival City?', "Yes. Messify delivers meal plans every morning across Dubai Festival City (DFC), including Al Badia. All of the day's meals arrive together in one chilled bag, from AED 25 a meal."),
        ('How much does a meal plan cost in DFC?', 'Weekly plans cost AED 215, 415 or 610 and monthly plans AED 715, 1,400 or 1,999 for 1, 2 or 3 meals a day. That is AED 25.63 to 30.71 per meal.'),
        ('Can I get office lunch delivered in Dubai Festival City?', 'Yes. Meals arrive at your office every morning, so lunch is ready before the lunchtime rush. Teams can share one monthly plan with one delivery for everyone.'),
        ('Is the food halal? Is there a vegetarian option?', 'Every Messify meal is 100% halal, and there is a vegetarian option every day, for every meal.'),
        ('Can I order on the website?', 'No. Start in the Messify app, or message us on WhatsApp and our team will help you get started.'),
    ]
    article_page('/guides/meal-delivery-dubai-festival-city/', 'Meal delivery in DFC',
                 'Daily Meal Delivery in Dubai Festival City (DFC) | Messify',
                 'How daily meal plan delivery works in Dubai Festival City: prices from AED 25 a meal, Al Badia homes, office lunch in DFC and how to start.',
                 'Daily meal delivery in Dubai Festival City', 'For DFC · 2026',
                 "Messify delivers daily meal plans in Dubai Festival City (DFC), to homes in Al Badia and offices across DFC. All of the day's meals arrive together every morning in one chilled bag, from AED 25 a meal (AED 215 for a 1-meal weekly plan). Start in the Messify app or on WhatsApp.",
                 sections, faqs)

# ---------------------------------------------------------------- catering guides
CATERING_GUIDES = [
    ('/guides/how-much-food-per-person-catering/', 'How much food per person for catering?',
     'Quantities per guest for rice, mains, sides, bread, desserts and drinks, with a calculator for your headcount.'),
    ('/guides/catering-cost-dubai/', 'How catering is priced in Dubai',
     'What goes into a per-person catering price, what pushes it up, and how to compare quotes fairly.'),
    ('/guides/corporate-event-catering-checklist/', 'Corporate event catering checklist',
     'Headcount, dietary needs, building access, timings and invoices: what to sort before an office event.'),
    ('/guides/party-catering-at-home-dubai/', 'Party catering at home in Dubai',
     'Birthdays and family gatherings at home: how much to order, space for a buffet, timings and food safety.'),
    ('/guides/buffet-vs-plated-catering/', 'Buffet, delivered or plated catering?',
     'The main catering styles compared, and which one suits your event, venue and headcount.'),
    ('/guides/wedding-catering-checklist-uae/', 'Wedding catering checklist for the UAE',
     'Guest numbers, venue rules, separate halls, timings and the questions to ask before you book.'),
]
CG_DATE = '2026-10-23'

# Planning rules of thumb, per adult guest. Used by the table and the calculator (site.js mirrors these numbers).
FOOD_MEAL = [  # item, amount per guest, unit
    ('Rice or biryani (cooked, served with other mains)', 150, 'g'),
    ('Meat, chicken or fish mains (cooked, all dishes together)', 175, 'g'),
    ('Vegetable and lentil dishes', 100, 'g'),
    ('Salads', 75, 'g'),
    ('Bread (naan, roti or rolls)', 1.5, 'pieces'),
    ('Appetisers, alongside a meal', 3, 'pieces'),
    ('Dessert', 1, 'portion'),
    ('Water', 750, 'ml'),
]
FOOD_RECEPTION = [
    ('Savoury bites and canapés', 10, 'pieces'),
    ('Sweet bites', 3, 'pieces'),
    ('Drinks (water, juice, tea or coffee)', 3, 'servings'),
]

UNITS = {'pieces': ('piece', 'pieces'), 'portion': ('portion', 'portions'), 'servings': ('serving', 'servings')}

def fmt_qty(v, unit, guests=1):
    import math
    t = v * guests
    if unit == 'g': return f'{t / 1000:,.2f}'.rstrip('0').rstrip('.') + ' kg' if t >= 1000 else f'{t:,.0f} g'
    if unit == 'ml': return f'{t / 1000:,.2f}'.rstrip('0').rstrip('.') + ' litres' if t >= 1000 else f'{t:,.0f} ml'
    n = t if guests == 1 else math.ceil(t - 1e-9)
    return f'{n:,g} {UNITS[unit][0] if n == 1 else UNITS[unit][1]}'

def food_table(rows, caption):
    trs = ''.join(f'<tr><th scope="row">{n}</th><td data-label="Per guest">{fmt_qty(v, u)}</td><td data-label="50 guests">{fmt_qty(v, u, 50)}</td><td data-label="100 guests">{fmt_qty(v, u, 100)}</td></tr>' for n, v, u in rows)
    return f'''<div class="table-wrap"><table class="ptable ptable--wrap">
  <caption>{caption}</caption>
  <thead><tr><th scope="col">Item</th><th scope="col">Per guest</th><th scope="col">50 guests</th><th scope="col">100 guests</th></tr></thead>
  <tbody>{trs}</tbody></table></div>'''

def food_calculator():
    return f'''<div class="calc" data-qcalc id="calculator">
      <p class="answer__label">Calculator</p>
      <h3 class="calc__title">Catering quantities for your headcount</h3>
      <div class="row">
        <div class="field"><label for="qc-adults">Adults</label><input id="qc-adults" type="number" inputmode="numeric" min="0" max="5000" step="1" value="50"></div>
        <div class="field"><label for="qc-kids">Children under 10</label><input id="qc-kids" type="number" inputmode="numeric" min="0" max="5000" step="1" value="0"></div>
      </div>
      <fieldset class="field">
        <legend>Type of event</legend>
        <div class="seg">
          <label><input type="radio" name="qc-style" value="meal" checked><span>Full meal</span></label>
          <label><input type="radio" name="qc-style" value="reception"><span>Light bites</span></label>
        </div>
      </fieldset>
      <ul class="qcalc__out" aria-live="polite" data-qcalc-out></ul>
      <p class="fine">Rules of thumb for a buffet, with children under 10 counted as half a guest. They don't include a buffer: most hosts add a little extra for a buffet. Your caterer should adjust them to your menu, your guests and the length of your event.</p>
    </div>'''

def page_guide_food_per_person():
    sections = f'''
    <h2>Start with the type of event</h2>
    <p>How much food you need depends first on what your guests expect. A <b>full meal</b> (lunch or dinner, usually served as a buffet) needs a main course with sides, bread, salad and dessert. A <b>light event</b>, such as a networking evening, an open house or a two-hour reception, runs on bites and drinks instead. Mixing the two up is the most common reason for running out, or for throwing half the food away.</p>

    <h2>Full meal: how much food per guest</h2>
    <p>For a buffet lunch or dinner, these are widely used planning amounts per adult guest. The weights are for cooked food, as it is served.</p>
    {food_table(FOOD_MEAL, 'Full meal: food per adult guest, with totals for 50 and 100 guests')}
    <p>Two things that surprise people. First, the meat figure is for <b>all main dishes together</b>: with chicken curry and lamb on the menu, guests take some of each, so 175 g covers both, not each. Second, when <b>biryani is the main dish</b> rather than a side, plan around 300 to 350 g of biryani per guest instead of the rice and meat lines above.</p>

    <h2>Light events: bites and drinks</h2>
    <p>For a two-hour reception, launch or open house with no main meal, plan by pieces instead of weight:</p>
    {food_table(FOOD_RECEPTION, 'Light event of about two hours: per adult guest')}
    <p>If the event runs longer than two hours, or overlaps with lunch or dinner time, guests will treat it as a meal. Either add a main course or plan nearer 14 to 16 bites per guest.</p>

    <h2>Work out your own quantities</h2>
    {food_calculator()}

    <h2>When to order more, and when to order less</h2>
    <ul>
      <li><b>Order more</b> for dinner rather than lunch, for events that run longer than three hours, for buffets where guests serve themselves, and for younger crowds such as university events.</li>
      <li><b>Order less</b> for a short daytime meeting, for an event straight after another meal, or when most of the menu is heavy (biryani, rich curries, grills).</li>
      <li><b>Children:</b> count children under 10 as half a guest. Babies and toddlers rarely need their own portion.</li>
      <li><b>Number of dishes:</b> more dishes doesn't mean more food in total. Guests take smaller servings of each, so split the same total across the dishes.</li>
      <li><b>Buffer:</b> for a buffet, a small buffer covers guests who arrive without an RSVP and second helpings. A plated meal needs much less spare.</li>
    </ul>

    <h2>Headcount: the number that drives everything</h2>
    <p>Quantities are only as good as the guest count behind them. For office events, use confirmed sign-ups. For weddings and family events in the UAE, where extra guests often arrive, ask the host family for their realistic number, not the invitation list. Give your caterer a final number a few days before the event, and tell them if it changes.</p>

    <h2>Don't forget dietary needs</h2>
    <p>Ask about vegetarian, vegan and allergy needs when you collect RSVPs. For a mixed crowd, make sure at least one main dish and one side are vegetarian, so no one is left with only rice and salad. Every Messify catering menu is 100% halal, and vegetarian dishes can be included in any menu.</p>

    <h2>Let the caterer do the maths</h2>
    <p>When you ask for a quote, give the caterer your headcount, the time you want to serve, how long the event runs and whether it is a full meal or a light event. A good caterer will turn that into quantities for your menu. Send us your details for a <a href="/catering/#quote">catering quote</a>, or see <a href="/catering/">catering in Dubai and across the UAE</a>.</p>'''
    faqs = [
        ('How much food do I need per person for a buffet?', 'For a full buffet meal, a widely used rule of thumb is about 150 g of rice, 175 g of meat, chicken or fish across all main dishes, 100 g of vegetable dishes, 75 g of salad, 1 to 2 pieces of bread and one dessert per adult guest.'),
        ('How much biryani per person should I order?', 'If biryani is the main dish, plan around 300 to 350 g of cooked biryani per adult. If it is served alongside other mains, around 150 g is usually enough.'),
        ('How much food for 100 guests?', 'For a full buffet meal for 100 adults: around 15 kg of cooked rice, 17.5 kg of meat, chicken or fish mains, 10 kg of vegetable dishes, 7.5 kg of salad, 150 pieces of bread, 100 desserts and 75 litres of water.'),
        ('How many appetisers per person?', 'About 3 pieces per guest when appetisers come before a meal, and around 10 savoury and 3 sweet pieces per guest for a two-hour event with no main meal.'),
        ('How do I count children for catering?', 'Count children under 10 as half a guest. Babies and toddlers rarely need their own portion.'),
    ]
    article_page('/guides/how-much-food-per-person-catering/', 'Food per person', 'How Much Food Per Person for Catering? | Messify',
                 'How much food to order per guest: rice, biryani, mains, sides, bread, desserts and drinks, with totals for 50 and 100 guests and a calculator.',
                 'How much food per person for catering?', 'Catering guide · 2026',
                 'For a buffet meal, plan about 150 g of cooked rice, 175 g of meat, chicken or fish across all main dishes, 100 g of vegetable dishes, 75 g of salad, 1 to 2 pieces of bread and one dessert per adult guest. For a two-hour event with only bites, plan about 10 savoury and 3 sweet pieces per guest. Count children under 10 as half.',
                 sections, faqs, kind='catering', published=CG_DATE)

def page_guide_catering_cost():
    sections = '''
    <h2>Most catering is priced per person</h2>
    <p>Caterers in the UAE usually quote a <b>price per person</b> (per head) for the food, then add anything that isn't food: staff, equipment, delivery and setup. Some include these in the per-person price; others list them separately. That is why two quotes for the same event can look very different until you put them side by side.</p>
    <p>We don't publish a fixed price list, because every Messify menu is built around the event. What we can do is explain what moves the price, so you can brief a caterer well and compare quotes fairly.</p>

    <h2>What changes the price per person</h2>
    <ol>
      <li><b>The menu.</b> The number of courses and the dishes themselves matter most. Lamb and seafood cost more than chicken; a single main course with sides costs less than a spread with appetisers, two mains, salads and desserts.</li>
      <li><b>Headcount.</b> Larger events usually cost less per person, because cooking, transport and setup are shared across more guests. Very small events often have a minimum order.</li>
      <li><b>Service style.</b> Food delivered ready to serve costs least. A buffet set up at your venue adds equipment and setup time. Served or plated meals need the most staff. See <a href="/guides/buffet-vs-plated-catering/">catering styles compared</a>.</li>
      <li><b>Staff.</b> Servers, buffet attendants and clean-up are usually priced per staff member and per hour.</li>
      <li><b>Equipment.</b> Chafing dishes, serving ware, tables, linen, plates and cutlery. Disposable or reusable makes a difference too.</li>
      <li><b>Location and timing.</b> Events further away cost more to reach. Early morning, late night and peak dates, such as weekends in the cooler months and the days around Eid, can be in higher demand.</li>
      <li><b>Notice.</b> Short-notice orders can limit the menu, and sometimes cost more.</li>
    </ol>

    <h2>What a good catering quote should show</h2>
    <p>Ask for a written quote that lists:</p>
    <ul>
      <li>The full menu, dish by dish, with the quantity or number of portions.</li>
      <li>The price per person and the total, and whether VAT is included.</li>
      <li>What is included: delivery, setup, equipment, serving staff, clean-up and taking equipment back.</li>
      <li>Arrival time, serving time and how long food will be on the buffet.</li>
      <li>The deadline for final numbers, and the cost of adding guests after it.</li>
      <li>Payment terms: deposit, balance and cancellation.</li>
    </ul>
    <p>Companies in the UAE usually need a tax invoice for their accounts, so mention it when you ask for the quote.</p>

    <h2>How to compare two quotes fairly</h2>
    <ol>
      <li><b>Line up the menus.</b> Same number of courses, similar dishes, similar portions.</li>
      <li><b>Add the extras</b> to each per-person price: delivery, setup, staff and equipment.</li>
      <li><b>Check the quantities.</b> A low price with small portions is not cheaper if you run out. Our guide to <a href="/guides/how-much-food-per-person-catering/">how much food per person</a> gives you a benchmark.</li>
      <li><b>Compare the total,</b> including VAT, for your real headcount.</li>
    </ol>

    <h2>How to keep catering costs down</h2>
    <ul>
      <li><b>Get your headcount right.</b> Over-ordering is the most expensive mistake.</li>
      <li><b>Pick fewer dishes, done well.</b> One or two mains with good sides feed people as well as five mains.</li>
      <li><b>Choose delivered catering</b> when you don't need a full setup, for example a team lunch in the office.</li>
      <li><b>Book early,</b> especially for weekends, Eid and the cooler months.</li>
      <li><b>Be clear about timing,</b> so you pay for staff only when you need them.</li>
    </ul>

    <h2>Getting a Messify catering quote</h2>
    <p>Send your date, location, headcount, the time you want to serve and any menu ideas, and we'll come back with a menu and a price for your headcount. Every menu is 100% halal and fully customisable, in Indian, Arabic, Continental, Italian, Chinese or other flavours. <a href="/catering/#quote">Request a catering quote</a>.</p>'''
    faqs = [
        ('How is catering priced in Dubai?', 'Most caterers quote a price per person for the food, then add or include staff, equipment, delivery and setup. The menu, headcount, service style and location move the price the most.'),
        ('Why do catering quotes vary so much?', 'Quotes differ in menu, portion sizes and what is included. Compare them with the same menu, the same headcount and all extras such as staff, setup and delivery added in.'),
        ('Is catering cheaper for more guests?', 'Usually, per person. Cooking, transport and setup are shared across more guests. Very small events often have a minimum order.'),
        ('Does a catering quote include VAT?', 'It depends on the caterer, so ask. Check whether the quote shows prices with or without VAT, and ask for a tax invoice if your company needs one.'),
        ('How much does Messify catering cost?', 'Every Messify catering quote is custom, based on your headcount, the menu you choose and the service style. Send your date, location and headcount for a price.'),
    ]
    article_page('/guides/catering-cost-dubai/', 'Catering prices', 'How Catering Is Priced in Dubai (Per Person) | Messify',
                 'What goes into a catering price per person in Dubai, what pushes it up, what a quote should include and how to compare catering quotes fairly.',
                 'How catering is priced in Dubai', 'Catering guide · 2026',
                 'Most catering in Dubai is priced per person, based on the menu, the headcount and the service style, with staff, equipment, delivery and setup either included or added on. To compare quotes fairly, line up the menus and portions, add every extra and compare the total for your real headcount, including VAT.',
                 sections, faqs, kind='catering', published=CG_DATE)

def page_guide_corporate_checklist():
    sections = '''
    <h2>The short version</h2>
    <p>Most office catering problems come from four things: a wrong headcount, a missed dietary need, food arriving at the wrong time, and a delivery stuck at the building's loading bay. Sort those four and the rest is easy. Use the checklist below, from a few weeks out to the day itself.</p>

    <h2>As soon as the event is confirmed</h2>
    <ul>
      <li><b>Date, start time and serving time.</b> The serving time matters more than the start time: a 10 AM workshop might need coffee at 9:45 and lunch at 1 PM.</li>
      <li><b>Estimated headcount</b>, including speakers, guests and staff working the event.</li>
      <li><b>Type of meal:</b> breakfast, working lunch, full buffet, afternoon break or evening reception.</li>
      <li><b>Budget</b> per person or in total, so the caterer can suggest a menu that fits.</li>
      <li><b>Venue:</b> office, meeting room, hotel, campus or outdoor. Check whether the venue allows outside catering.</li>
    </ul>

    <h2>Two to three weeks before</h2>
    <ul>
      <li><b>Collect dietary needs</b> with RSVPs: vegetarian, vegan, allergies and any medical diets. Make sure at least one main dish is vegetarian.</li>
      <li><b>Choose the service style:</b> delivered and ready to serve, a buffet setup, or served. See <a href="/guides/buffet-vs-plated-catering/">catering styles compared</a>.</li>
      <li><b>Agree the menu</b> and quantities. Our guide to <a href="/guides/how-much-food-per-person-catering/">how much food per person</a> helps you sense-check them.</li>
      <li><b>Get a written quote</b> showing what is included, VAT, payment terms and the deadline for final numbers. Ask for a tax invoice if your finance team needs one.</li>
    </ul>

    <h2>One week before</h2>
    <ul>
      <li><b>Building access.</b> Many Dubai office towers need a delivery pass, a service lift booking or a set loading-bay time slot. Ask your building management what they need and send it to the caterer.</li>
      <li><b>Space and power.</b> Where will the buffet go? Is there a table, enough space for a queue, and a socket nearby if food needs to be kept warm?</li>
      <li><b>Point of contact</b> on the day, with a phone number, who can meet the delivery and sign it off.</li>
      <li><b>Clean-up:</b> who clears the buffet, what happens to equipment, and where rubbish goes.</li>
    </ul>

    <h2>Two to three days before</h2>
    <ul>
      <li><b>Confirm the final headcount</b>, with dietary needs by number (for example, 60 guests including 8 vegetarian and 1 nut allergy).</li>
      <li><b>Reconfirm times:</b> delivery, setup and serving.</li>
      <li><b>Share the agenda</b> if timings could move, so food isn't sitting out while a session overruns.</li>
    </ul>

    <h2>On the day</h2>
    <ul>
      <li>Meet the delivery and check it against the order.</li>
      <li>Label dishes, especially vegetarian and allergen information.</li>
      <li>Keep an eye on timing: hot food is best eaten within two hours of being served.</li>
      <li>Plan for leftovers. Agree with the caterer and venue whether they can be kept, and store them cold straight away.</li>
    </ul>

    <h2>Timing around the UAE calendar</h2>
    <p>During Ramadan, many companies move events to iftar time, and daytime catering in the office needs care. The cooler months from October to April are busy for corporate events, so book early. Around public holidays, confirm your caterer's availability before you announce the date.</p>

    <h2>Office lunch every day, not just for events</h2>
    <p>If your team needs lunch sorted every day rather than for one event, a meal plan is simpler than catering. Messify delivers all of the day's meals every morning in Silicon Oasis, Academic City, International City and Dubai Festival City. See <a href="/guides/office-lunch-delivery-silicon-oasis/">office lunch delivery in Silicon Oasis</a>.</p>
    <p>Planning a one-off event? Send us your date, venue, headcount and serving time for a <a href="/catering/#quote">corporate catering quote</a>.</p>'''
    faqs = [
        ('How far in advance should I book corporate catering?', 'Two to three weeks is comfortable for most office events, and earlier for large events, weekends and the busy months from October to April. Confirm the final headcount two to three days before.'),
        ('What should I ask a corporate caterer?', 'Ask what the quote includes (delivery, setup, staff, equipment and clean-up), whether VAT is included, the deadline for final numbers, payment terms, and whether they can provide a tax invoice.'),
        ('How do I handle dietary requirements at an office event?', 'Collect them with RSVPs, give the caterer numbers for each need, make sure at least one main dish is vegetarian, and label dishes on the day.'),
        ('Do caterers need access passes for Dubai office buildings?', 'Often, yes. Many towers need a delivery pass, a service lift booking or a loading-bay slot. Ask building management early and share the details with your caterer.'),
        ('Does Messify cater corporate events?', 'Yes. We cater team lunches, meetings, launches and company events across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain, with custom 100% halal menus quoted by headcount.'),
    ]
    article_page('/guides/corporate-event-catering-checklist/', 'Corporate catering checklist', 'Corporate Event Catering Checklist (UAE) | Messify',
                 'A step-by-step corporate catering checklist for office events in Dubai and the UAE: headcount, dietary needs, building access, timings and invoices.',
                 'Corporate event catering checklist', 'Catering guide · 2026',
                 'Book corporate catering two to three weeks ahead. Agree the serving time, headcount and dietary needs first, then the menu and service style. A week before, sort building access, space and power for the buffet, and confirm the final numbers two to three days before the event.',
                 sections, faqs, kind='catering', published=CG_DATE)

def page_guide_home_party():
    sections = '''
    <h2>Why cater a party at home</h2>
    <p>Cooking for 30 people at home means two days in the kitchen and no time with your guests. Catering hands over the cooking, and the serving too if you want a buffet setup. This guide covers how to plan it in a Dubai home, from a villa garden to a flat with a lift.</p>

    <h2>1. Get the headcount right</h2>
    <p>Count adults and children separately. For quantities, children under 10 count as about half a guest. For family gatherings, plan for the number you expect to arrive, which is often higher than the number who replied. Our <a href="/guides/how-much-food-per-person-catering/">food per person guide</a> has a calculator for this.</p>

    <h2>2. Pick a menu that suits a home party</h2>
    <ul>
      <li><b>Dishes that hold well:</b> curries, biryani, grills, pasta bakes and rice dishes stay good on a buffet. Fried snacks and delicate dishes lose quality fast.</li>
      <li><b>One or two mains</b> plus rice, bread, a salad and a dessert is enough for most parties.</li>
      <li><b>Something for everyone:</b> a vegetarian main, a milder dish for children and older guests, and clear labels for anything with nuts.</li>
    </ul>

    <h2>3. Plan the space</h2>
    <ul>
      <li><b>Buffet table:</b> a long table against a wall works for smaller parties. For more than about 60 guests, a table guests can reach from both sides keeps the queue moving.</li>
      <li><b>Power:</b> if food is kept warm in electric chafing dishes, you need sockets close to the table. Ask your caterer what they bring.</li>
      <li><b>Plates, cutlery and serving spoons:</b> check whether they are included.</li>
      <li><b>Bins and clean-up:</b> decide who clears the buffet and takes equipment away.</li>
    </ul>

    <h2>4. If you live in a building</h2>
    <p>Tell your building's security or reception about the delivery, and book the service lift if your building requires it. Give the caterer the building name, tower, parking or drop-off point and a phone number for whoever will meet them.</p>

    <h2>5. Timing</h2>
    <p>Tell the caterer when you want to <b>eat</b>, not when guests arrive. Food should arrive shortly before serving, not hours early. For evening parties, many families in the UAE eat late, so be realistic about when dinner will actually be served.</p>

    <h2>6. Outdoor parties in the heat</h2>
    <p>From May to September, garden and rooftop parties need extra care. Keep the buffet in the shade or indoors, keep cold dishes chilled, and serve food in smaller batches instead of putting everything out at once.</p>

    <h2>7. Food safety and leftovers</h2>
    <p>As a general food safety rule, don't leave hot or cold food at room temperature for more than two hours, and no more than one hour on a hot day outdoors. Put leftovers in the fridge promptly, in shallow containers, and reheat them until piping hot.</p>

    <h2>Quick checklist</h2>
    <ol>
      <li>Headcount: adults and children.</li>
      <li>Menu: one or two mains, sides, salad, dessert, a vegetarian option.</li>
      <li>Serving time, not arrival time.</li>
      <li>Buffet table, power and serving ware.</li>
      <li>Building access and a contact number.</li>
      <li>Clean-up and leftovers plan.</li>
    </ol>
    <p>We cater birthdays, family gatherings and house parties at home across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain, with buffet setups if you want one. <a href="/catering/#quote">Get a party catering quote</a>.</p>'''
    faqs = [
        ('How much food do I need for a party at home?', 'For a buffet meal, plan about 150 g of rice, 175 g of meat, chicken or fish across all main dishes, 100 g of vegetable dishes, a salad, 1 to 2 pieces of bread and a dessert per adult, with children under 10 counted as half.'),
        ('Can caterers set up a buffet in a flat?', 'Yes, if there is space for a table and, for heated dishes, power nearby. Tell your building security about the delivery and book the service lift if needed.'),
        ('How long can buffet food sit out?', 'As a general food safety rule, no more than two hours at room temperature, and no more than one hour on a hot day outdoors.'),
        ('When should I book party catering?', 'A week or two ahead is comfortable for most home parties. Book earlier for weekends, Eid and large family gatherings.'),
        ('Does Messify cater parties at home?', 'Yes. We cater birthdays, family gatherings and house parties at home, with custom 100% halal menus quoted by headcount and buffet setups if you want one.'),
    ]
    article_page('/guides/party-catering-at-home-dubai/', 'Party catering at home', 'Party Catering at Home in Dubai: A Guide | Messify',
                 'How to plan party catering at home in Dubai: headcount, menu, space for a buffet, building access, timing, outdoor heat and food safety.',
                 'Party catering at home in Dubai', 'Catering guide · 2026',
                 'For a party at home, give the caterer your headcount (children under 10 count as half), the time you want to eat and the space you have for a buffet table and power. Pick one or two mains that hold well, add a vegetarian dish, tell your building security about the delivery, and keep food out for no more than two hours.',
                 sections, faqs, kind='catering', published=CG_DATE)

def page_guide_styles():
    rows = [
        ('Delivered, ready to serve', 'Lowest', 'Office lunches, meetings, small parties', 'You or your team set out and serve the food'),
        ('Buffet setup', 'Medium', 'Parties, corporate events, weddings', 'Needs space for a table and a queue'),
        ('Served or plated', 'Highest', 'Formal dinners, award nights, VIP events', 'Needs the most staff and a fixed seating plan'),
        ('Family style (shared platters)', 'Medium', 'Family gatherings, team dinners', 'Needs space on each table for platters'),
        ('Live stations', 'Medium to high', 'Weddings, receptions, larger parties', 'Needs chefs on site, space and often power or gas'),
    ]
    trs = ''.join(f'<tr><th scope="row">{a}</th><td data-label="Staff needed">{b}</td><td data-label="Best for">{c}</td><td data-label="Watch out for">{d}</td></tr>' for a, b, c, d in rows)
    table = f'''<div class="table-wrap"><table class="ptable ptable--wrap">
  <caption>Catering styles compared</caption>
  <thead><tr><th scope="col">Style</th><th scope="col">Staff needed</th><th scope="col">Best for</th><th scope="col">Watch out for</th></tr></thead>
  <tbody>{trs}</tbody></table></div>'''
    sections = f'''
    <h2>The main catering styles</h2>
    <p>The service style shapes your budget, the space you need and how the event feels. Here is how the main options compare.</p>
    {table}

    <h2>Delivered catering</h2>
    <p>The food arrives ready to serve, in trays or containers, and you set it out. It is the simplest and usually the lowest-cost option, and it suits office lunches, meetings and small gatherings where someone on your side can manage the table.</p>

    <h2>Buffet setup</h2>
    <p>The caterer sets up a full buffet at your venue, with dishes kept warm and the table arranged for guests to serve themselves. Buffets handle large numbers well, offer variety, and let guests choose what and how much they eat. Plan enough space for a queue: for more than about 60 guests, a table guests can reach from both sides keeps it moving.</p>

    <h2>Served or plated</h2>
    <p>Each guest is served at their seat, course by course. It is the most formal option and gives you full control over timing, but it needs the most staff, a fixed headcount and a seating plan, and it usually costs the most per person.</p>

    <h2>Family style</h2>
    <p>Shared platters go on each table and guests pass them around. It feels generous and social, and suits family gatherings and team dinners, but each table needs room for the platters.</p>

    <h2>Live stations</h2>
    <p>A chef cooks or carves in front of guests: grills, shawarma, pasta or desserts. Stations add a sense of occasion to weddings and receptions, but they need space, time and often power or gas at the venue, so check the venue rules first.</p>

    <h2>Which style suits your event?</h2>
    <ul>
      <li><b>Team lunch or meeting:</b> delivered, or a simple buffet setup for bigger groups.</li>
      <li><b>Birthday or family gathering at home:</b> a buffet setup, or family style for a sit-down meal.</li>
      <li><b>Corporate event or launch:</b> a buffet setup, with live stations if you want a centrepiece.</li>
      <li><b>Wedding:</b> usually a buffet, sometimes with live stations; plated for smaller, formal weddings.</li>
      <li><b>Formal dinner or awards night:</b> served or plated.</li>
    </ul>

    <h2>What Messify offers</h2>
    <p>Messify delivers catering ready to serve and sets up full buffets at your venue, from office lunches and house parties to weddings. Every menu is custom and 100% halal. If you need served or plated service or live stations, mention it in your enquiry and the team will confirm what's possible for your event. <a href="/catering/#quote">Get a catering quote</a>.</p>
    <p>Not sure how much to order? Read <a href="/guides/how-much-food-per-person-catering/">how much food per person for catering</a>.</p>'''
    faqs = [
        ('Is a buffet cheaper than a plated meal?', 'Usually, yes. A buffet needs fewer staff than serving each guest at their seat, so it tends to cost less per person for the same menu.'),
        ('What is the difference between delivered catering and a buffet setup?', 'Delivered catering arrives ready to serve and you set it out. With a buffet setup, the caterer arranges the full buffet at your venue and keeps the food warm.'),
        ('Which catering style is best for a large event?', 'A buffet handles large numbers well and offers variety. For several hundred guests, plan multiple serving points so queues stay short.'),
        ('What are live stations?', 'Stations where a chef cooks or carves in front of guests, such as grills, shawarma, pasta or desserts. They need space, staff and often power or gas at the venue.'),
        ('Does Messify do buffet setups?', 'Yes. We deliver catering ready to serve and set up full buffets at your venue. Ask in your enquiry about other service styles.'),
    ]
    article_page('/guides/buffet-vs-plated-catering/', 'Catering styles', 'Buffet vs Plated vs Delivered Catering | Messify',
                 'Buffet, plated, family style, live stations or delivered catering: how each style works, what it needs and which one suits your event.',
                 'Buffet, delivered or plated catering?', 'Catering guide · 2026',
                 'Delivered catering is the simplest and usually lowest-cost option, best for office lunches and small groups. A buffet setup suits parties, corporate events and weddings and handles large numbers well. Served or plated meals are the most formal and need the most staff. Family style and live stations sit in between.',
                 sections, faqs, kind='catering', published=CG_DATE)

def page_guide_wedding():
    sections = '''
    <h2>Start with the venue's rules</h2>
    <p>Before you talk to any caterer, ask your venue whether outside catering is allowed. Many hotels in the UAE only allow their own kitchens, and some venues charge a fee for outside caterers or require them to use the venue's equipment. Halls, community venues, gardens and family homes usually give you more freedom.</p>

    <h2>Guest numbers, realistically</h2>
    <p>Weddings in the UAE are often large, and the number who arrive can be very different from the invitation list. Ask both families for their realistic number, plan for children separately (under 10s count as about half for food), and agree with the caterer how late you can change the final number.</p>

    <h2>Separate halls, separate plans</h2>
    <p>If your celebration has separate men's and women's halls, or separate family and guest areas, give the caterer a headcount for each, and decide whether each hall gets its own buffet, its own serving time and its own staff. Food quantities and timings are planned per hall, not just for the total.</p>

    <h2>More than one event?</h2>
    <p>Many weddings in the UAE run over several days: a henna or mehndi night, a nikah, a reception, a family lunch. List every event, with its date, venue, headcount and style, so the caterer can quote them together and plan the menus so they don't repeat.</p>

    <h2>The menu</h2>
    <ul>
      <li><b>Choose dishes that hold well</b> on a buffet for the length of your dinner service.</li>
      <li><b>Plan a vegetarian main</b>, a milder option for children and older guests, and clear labels for allergens.</li>
      <li><b>Think about the timeline:</b> welcome drinks and bites while guests arrive, the main meal, then dessert and tea or coffee.</li>
      <li><b>Ask about a tasting</b> and whether it is included in the price.</li>
    </ul>
    <p>Our guide to <a href="/guides/how-much-food-per-person-catering/">how much food per person</a> gives you a benchmark for quantities.</p>

    <h2>Service style</h2>
    <p>Most UAE weddings serve a buffet, sometimes with live stations as a centrepiece. Plated service suits smaller, formal weddings. For several hundred guests, plan more than one buffet line or serving point so no one waits long. See <a href="/guides/buffet-vs-plated-catering/">catering styles compared</a>.</p>

    <h2>Timing on the night</h2>
    <p>Weddings rarely run to schedule. Agree a serving window rather than a fixed minute, tell the caterer who decides when dinner starts, and make sure food can be held safely if the programme runs late.</p>

    <h2>Questions to ask before you book</h2>
    <ol>
      <li>Is the price per person, and what does it include: food, staff, equipment, setup, clean-up, delivery?</li>
      <li>Is VAT included?</li>
      <li>How many serving staff, and for how many hours?</li>
      <li>When is the deadline for final numbers, and what does it cost to add guests after it?</li>
      <li>How will food be kept hot or cold, and for how long?</li>
      <li>What happens to leftovers?</li>
      <li>What are the deposit, payment and cancellation terms?</li>
    </ol>

    <h2>When to book</h2>
    <p>Book the caterer once the venue and date are confirmed, ideally a few months ahead for large weddings, and earlier still for the cooler months from October to April, which are the busiest wedding season. Confirm final numbers about a week before.</p>
    <p>We cater weddings across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain, with custom 100% halal menus built around your guest list and full buffet setups. <a href="/catering/#quote">Get a wedding catering quote</a>.</p>'''
    faqs = [
        ('Can I bring an outside caterer to a hotel wedding in the UAE?', 'Many hotels only allow their own catering, and some charge a fee for outside caterers. Ask your venue before you book a caterer.'),
        ('How far in advance should I book wedding catering?', 'Once your venue and date are confirmed, ideally a few months ahead for a large wedding, and earlier for the busy season from October to April. Confirm final numbers about a week before.'),
        ('How much food per guest for a wedding?', 'For a buffet dinner, plan about 150 g of rice, 175 g of meat, chicken or fish across all main dishes, 100 g of vegetable dishes, a salad, bread and a dessert per adult guest, plus welcome bites if guests arrive well before dinner.'),
        ('How do I plan catering for separate halls?', 'Give the caterer a headcount for each hall and decide whether each gets its own buffet, serving time and staff. Quantities and timings are planned per hall.'),
        ('Does Messify cater weddings?', 'Yes. We cater weddings with custom 100% halal menus built around your guest list, including full buffet setups.'),
    ]
    article_page('/guides/wedding-catering-checklist-uae/', 'Wedding catering checklist', 'Wedding Catering Checklist for the UAE | Messify',
                 'Plan wedding catering in the UAE: venue rules, realistic guest numbers, separate halls, multi-day events, menus, timing and questions to ask.',
                 'Wedding catering checklist for the UAE', 'Catering guide · 2026',
                 'Check first whether your venue allows outside catering. Then agree a realistic guest number (per hall if you have separate halls), list every event if the wedding runs over several days, choose dishes that hold well on a buffet, and get a written quote that shows staff, setup, VAT and the deadline for final numbers.',
                 sections, faqs, kind='catering', published=CG_DATE)

def page_guide_affordable():
    p = {(m, ln): (t, pr) for m, ln, t, pr in PLANS}
    by_per = sorted(PLANS, key=lambda x: x[3] / x[2])
    rows = ''.join(f'<tr><th scope="row">{mlabel(m)}, {ln}</th><td class="num">AED {per(pr, t)}</td><td class="num">{aed(pr)}</td><td class="num">{t}</td></tr>' for m, ln, t, pr in by_per)
    table = f'''<div class="table-wrap"><table class="ptable">
  <caption>Messify meal plans, from the lowest price per meal (AED)</caption>
  <thead><tr><th scope="col">Plan</th><th scope="col" class="num">Per meal</th><th scope="col" class="num">Plan price</th><th scope="col" class="num">Meals</th></tr></thead>
  <tbody>{rows}</tbody></table></div>'''
    t3, pr3 = p[(3, 'monthly')]
    sections = f'''
    <h2>What makes a meal plan affordable</h2>
    <p>An affordable meal plan is not just the one with the lowest headline price. It is the one with a fair <b>price per meal</b>, a total you can fit into your monthly budget, and meals you actually eat. A plan you only use half of costs twice as much per meal as it says on the page.</p>
    <p>So check three things: the price per meal (plan price ÷ number of meals), what that price includes, and how much time you get to use your meals.</p>

    <h2>Messify prices, ranked by price per meal</h2>
    {table}
    <ul>
      <li><b>Lowest price per meal:</b> 3 meals a day, monthly, at AED {per(pr3, t3)} a meal. That is breakfast, lunch and dinner for about AED {pr3 / 26:.2f} a day.</li>
      <li><b>Lowest upfront cost:</b> 1 meal a day, weekly, at AED {p[(1, 'weekly')][1]}. The easiest way to try it.</li>
      <li><b>Most common middle ground:</b> 2 meals a day, monthly, at AED {p[(2, 'monthly')][1]:,}, lunch and dinner for AED {per(p[(2, 'monthly')][1], p[(2, 'monthly')][0])} a meal.</li>
    </ul>
    <p>Monthly plans are 26 days of meals to use within 30 days; weekly plans are 7 days of meals to use within 9 days. Prices include VAT unless stated otherwise.</p>

    <h2>Compare it with what you spend now</h2>
    <p>Most people looking for an affordable meal plan are ordering in. Put in what you usually spend on one delivery order, including fees, and see the difference over a month.</p>
    {calculator()}

    <h2>Six ways to keep your meal plan affordable</h2>
    <ol>
      <li><b>Try a week, then go monthly.</b> Monthly plans cost less per meal on every plan size, so switch once you know you like the food.</li>
      <li><b>Only buy the meals you'll eat.</b> If you eat breakfast at home, a 2-meal plan beats a 3-meal plan you don't finish.</li>
      <li><b>Use every meal.</b> With Messify, skip a busy day in the app and use that meal later in your plan, instead of letting it go to waste.</li>
      <li><b>Compare per meal, including fees.</b> Delivery, service fees and VAT change the real price of ordering in and of some plans.</li>
      <li><b>Skip extras you don't need.</b> Diet and fitness plans with snacks, juices and calorie tracking cost more per meal. If you just want everyday meals sorted, an everyday meal plan costs less.</li>
      <li><b>Check delivery to your building first.</b> Messify delivers in Dubai Academic City, Dubai Silicon Oasis, International City and Dubai Festival City.</li>
    </ol>

    <h2>Affordable, not the cheapest</h2>
    <p>We'd rather be straight with you. Cooking for yourself is cheaper on ingredients, if you have the time and a kitchen. And some companies publish lower starting prices on certain plans: when we last checked, Right Bite listed its Essentials plan from AED 22 a meal. Our <a href="/guides/best-meal-plans-dubai/">comparison of Dubai meal plans</a> shows published prices side by side.</p>
    <p>Where Messify fits is everyday meals at a predictable price: breakfast, lunch and dinner delivered together every morning, a new menu every day, 100% halal, with a vegetarian option every day, for every meal.</p>

    <h2>Who an affordable meal plan suits</h2>
    <ul>
      <li><b>Students</b> in shared residences with small kitchens. See <a href="/guides/student-meal-plans-dubai/">student meal plans in Dubai</a>.</li>
      <li><b>Young professionals</b> who order in most days and want one predictable food bill.</li>
      <li><b>Office workers</b> who want lunch sorted before the workday starts.</li>
    </ul>
    <p>See every plan on our <a href="/meal-plans/">meal plans in Dubai</a> page, or read <a href="/guides/meal-plan-cost-dubai/">how much a meal plan costs in Dubai</a>.</p>'''
    faqs = [
        ('What is the most affordable meal plan in Dubai?', f"Compare the price per meal, not the plan price. Messify's lowest price per meal is the 3-meal monthly plan at AED {per(pr3, t3)}. When we last checked, Right Bite listed its Essentials plan from AED 22 a meal. Check what each price includes and where each company delivers."),
        ('Is a meal plan cheaper than ordering food in Dubai?', 'If you order in most days, a meal plan usually costs less per meal once delivery and service fees are counted. Use the calculator on this page with what you really spend.'),
        ('How much is a monthly meal plan in Dubai?', 'Messify monthly plans cost AED 715, 1,400 or 1,999 for 1, 2 or 3 meals a day, which is AED 25.63 to 27.50 a meal.'),
        ('What is the cheapest way to try a meal plan?', 'Start with a weekly plan. Messify\'s 1-meal weekly plan costs AED 215 for 7 meals.'),
        ('Do I lose meals if I skip a day?', 'With Messify, no. Skip a day in the app and use that meal later in your plan. Monthly plans give you 30 days to use 26 days of meals, and weekly plans give you 9 days to use 7.'),
    ]
    article_page('/guides/affordable-meal-plans-dubai/', 'Affordable meal plans', 'Affordable Meal Plans in Dubai: Real Prices | Messify',
                 'How to find an affordable meal plan in Dubai: price per meal, which plan costs least, how to avoid waste, and a calculator to compare with ordering in.',
                 'Affordable meal plans in Dubai', 'Meal plans on a budget · 2026',
                 f"An affordable meal plan is one with a fair price per meal that you actually use. Messify meal plans in Dubai cost AED 25.63 to 30.71 a meal: from AED 215 a week or AED 715 a month. The 3-meal monthly plan has the lowest price per meal (AED {per(pr3, t3)}), and the 1-meal weekly plan has the lowest upfront cost.",
                 sections, faqs, published=CG_DATE)

# ---------------------------------------------------------------- catering by emirate
CATER_EVENTS = [
    ('case', 'Corporate &amp; office', 'Team lunches, meetings, launches and company events, delivered on time.', '/catering/corporate-events/'),
    ('party', 'Parties &amp; home events', 'Birthdays, family gatherings and house parties, catered at home.', '/catering/family-gatherings/'),
    ('cap', 'University events', 'Orientation days, society nights and campus functions.', '/catering/university-events/'),
    ('rings', 'Weddings', 'Generous menus built around your guest list.', '/catering/weddings/'),
    ('serve', 'Buffet setups', 'Full buffets set up at your venue, from office lunches to weddings.', '/guides/buffet-vs-plated-catering/'),
    ('box', 'Bulk catering', 'Large volumes for sites, institutions and events.', ''),
]

def event_tiles(items):
    return ''.join((f'<a class="event" href="{u}">' if u else '<div class="event">') + f'{I[i]}<h3 class="h3">{t}</h3><p>{d}</p>' + ('</a>' if u else '</div>') for i, t, d, u in items)

def catering_catalog():
    return {'@type': 'OfferCatalog', 'name': 'Catering services', 'itemListElement': [
        {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for n in
        ('Corporate and office catering', 'Party and home event catering', 'University event catering', 'Wedding catering', 'Buffet catering', 'Bulk catering')]}

CATER_AREAS = {
 'dubai': {
  'name': 'Dubai', 'short': 'Dubai',
  'card': 'Our meals are cooked in International City, so Dubai events get the shortest journey: office lunches, parties at home and large events.',
  'title': 'Catering in Dubai: Corporate, Party & Buffet | Messify',
  'desc': 'Catering in Dubai for office lunches, corporate events, parties at home and weddings. Buffet setups and custom halal menus, quoted by headcount.',
  'h1': 'Event catering in Dubai, cooked across town.',
  'lede': "Our meals are cooked in our partner kitchen in International City, so Dubai events get the shortest journey of all. Office lunches in Business Bay, a birthday at home in Mirdif, an orientation day in Academic City: every menu is custom, 100% halal and quoted by headcount.",
  'img': ('cat-serving-640.webp', 'cat-serving.webp', 1100, 1375, 'A gloved server lifting the lid of a chafing dish at a catered buffet'),
  'where_title': 'Across Dubai, from offices to homes.',
  'groups': [
    ('office', 'Offices and business districts', ['Business Bay and Downtown Dubai', 'DIFC', 'Dubai Silicon Oasis', 'JLT, Dubai Internet City and Media City', 'Al Barsha and Al Quoz']),
    ('home', 'Homes and communities', ['Mirdif and Dubai Festival City', 'Arabian Ranches and Dubai Hills', 'Jumeirah and Al Barsha', 'Al Warqa and International City', 'Dubai Marina and JBR']),
    ('cap', 'Campuses and venues', ['Dubai Academic City and Knowledge Park', 'Hotels and event halls', 'Community halls and majlis', 'Outdoor and garden events']),
  ],
  'logistics': "Most of Dubai is a short drive from International City, which keeps hot food hot and cold food cold. For office lunches, tell us the time you want to eat rather than the meeting start time, and check whether your building needs a delivery pass or a service lift booking. For weddings and large events, share your date as early as you can so the menu, staff and setup can be planned.",
  'faqs': [
    ('Do you cater office lunches in Dubai?', 'Yes. We cater team lunches, meetings and company events across Dubai, with menus built around your headcount and delivered for the time you want to eat.'),
    ('Can you cater a party at home in Dubai?', "Yes. Birthdays, family gatherings and house parties are welcome. Tell us your headcount and the space you have, and we'll build a menu and setup to fit."),
    ('Do you set up buffets in Dubai?', 'Yes. We set up full buffets at your venue, from office lunches and house parties to weddings.'),
    ('How much does catering cost in Dubai?', 'Every quote is custom, based on your headcount, the courses you choose and the service style. Send your date, location and headcount for a price.'),
    ('Is your catering halal?', 'Yes. All our catering menus are 100% halal, and vegetarian dishes can be included in any menu.'),
  ],
 },
 'sharjah': {
  'name': 'Sharjah', 'short': 'Sharjah',
  'card': 'Corporate events, family occasions and parties across Sharjah, a short drive from our kitchen in International City.',
  'title': 'Catering in Sharjah: Corporate, Party & Buffet | Messify',
  'desc': 'Catering in Sharjah for corporate events, family gatherings, parties at home, university events and weddings. Custom halal menus and buffet setups.',
  'h1': 'Event catering in Sharjah.',
  'lede': 'Sharjah is a short drive from our partner kitchen in International City. We cater corporate events, family gatherings, parties at home, university events and weddings across Sharjah, with custom 100% halal menus quoted by headcount.',
  'img': ('cat-chef-640.webp', 'cat-chef.webp', 1024, 1024, 'A chef carving at a buffet station while guests serve themselves at an evening event'),
  'where_title': 'Across Sharjah, from Al Majaz to Aljada.',
  'groups': [
    ('office', 'Offices and business areas', ['Al Majaz and Al Taawun', 'Al Khan and Al Nahda', 'Sharjah Industrial Area', 'SAIF Zone and Hamriyah Free Zone']),
    ('home', 'Homes and communities', ['Al Nahda and Al Qasimia', 'Muwaileh', 'Aljada and Al Zahia', 'Al Rahmaniya']),
    ('cap', 'Campuses and venues', ['University City Sharjah', 'Hotels and wedding halls', 'Community halls and majlis', 'Outdoor and garden events']),
  ],
  'logistics': "The roads between Dubai and Sharjah get heavy at rush hour, so we plan departure times around the traffic and your serving time, not the other way round. When you enquire, tell us when you want food served, how long the event runs and whether there is a kitchen or power at the venue for keeping food warm.",
  'faqs': [
    ('Do you deliver catering to Sharjah?', 'Yes. We cater across Sharjah, from offices in Al Majaz and Al Taawun to homes in Al Nahda, Muwaileh and Aljada.'),
    ('Can you cater a family gathering at home in Sharjah?', "Yes. Family gatherings, birthdays and house parties are welcome. Tell us your headcount and we'll build a menu to fit, with a buffet setup if you want one."),
    ('Do you cater university events in Sharjah?', 'Yes. We cater orientation days, society events and campus functions, including in University City Sharjah.'),
    ('How is catering in Sharjah priced?', 'Every quote is custom, based on your headcount, menu and service style. Send your date, location and headcount for a price.'),
    ('Is your catering halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
 },
 'ajman': {
  'name': 'Ajman', 'short': 'Ajman',
  'card': 'Party and event catering in Ajman, from family gatherings at home to office events and bulk orders.',
  'title': 'Catering in Ajman: Parties, Events & Buffets | Messify',
  'desc': 'Party and event catering in Ajman: family gatherings at home, office events, weddings and bulk orders. Custom halal menus, quoted by headcount.',
  'h1': 'Party and event catering in Ajman.',
  'lede': 'From a family gathering at home in Al Nuaimiya to an office event in Ajman Free Zone, we cater events across Ajman with custom 100% halal menus quoted by headcount, and full buffet setups if you want them.',
  'img': ('cat-canapes.webp', 'cat-canapes.webp', 900, 1200, 'Trays of canapés on slate boards at a catered event'),
  'where_title': 'Across Ajman, from the Corniche to Al Jurf.',
  'groups': [
    ('home', 'Homes and communities', ['Al Nuaimiya and Al Rashidiya', 'Al Rawda and Al Mowaihat', 'Al Yasmeen and Al Helio', 'Al Zorah and the Corniche']),
    ('office', 'Offices and business areas', ['Ajman Free Zone', 'Al Jurf and Al Jurf Industrial Area', 'Ajman city centre']),
    ('party', 'Venues', ['Hotels along Ajman Corniche', 'Wedding and event halls', 'Community halls and majlis', 'Outdoor and garden events']),
  ],
  'logistics': "Ajman is reached through Sharjah, so we allow for traffic on the way and time the delivery to when you want to serve. If your event is at home, tell us the space you have for a buffet table and whether there is power nearby for keeping food warm.",
  'faqs': [
    ('Do you cater in Ajman?', 'Yes. We cater parties, family gatherings, office events, weddings and bulk orders across Ajman.'),
    ('Can you cater a party at home in Ajman?', "Yes. Birthdays, family gatherings and house parties are welcome. Tell us your headcount and we'll build the menu and setup around your space."),
    ('Do you do buffet setups in Ajman?', 'Yes. We can set up a full buffet at your home or venue in Ajman.'),
    ('How is catering in Ajman priced?', 'Every quote is custom, based on your headcount, menu and service style. Send your date, location and headcount for a price.'),
    ('Is your catering halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
 },
 'abu-dhabi': {
  'name': 'Abu Dhabi', 'short': 'Abu Dhabi',
  'card': 'Corporate events, weddings and large gatherings in Abu Dhabi. Share your date early and we plan delivery around your event.',
  'title': 'Catering in Abu Dhabi: Corporate & Events | Messify',
  'desc': 'Catering in Abu Dhabi for corporate events, weddings, university events and large gatherings. Custom halal menus and buffet setups, quoted by headcount.',
  'h1': 'Event catering in Abu Dhabi.',
  'lede': 'We cater corporate events, weddings, university events and large gatherings in Abu Dhabi. It is the longest journey from our kitchen in International City, so we plan every Abu Dhabi event around the drive. Share your date early.',
  'img': ('cat-chef-640.webp', 'cat-chef.webp', 1024, 1024, 'A chef carving at a buffet station while guests serve themselves at an evening event'),
  'where_title': 'Across Abu Dhabi, city and islands.',
  'groups': [
    ('office', 'Offices and business areas', ['Abu Dhabi city centre', 'Al Maryah Island and Al Reem Island', 'Mussafah and ICAD', 'KIZAD']),
    ('home', 'Homes and communities', ['Khalifa City', 'Mohammed Bin Zayed City', 'Al Raha and Yas Island', 'Al Reef and Al Shamkha']),
    ('rings', 'Venues', ['Hotels and wedding halls', 'Event venues on Yas and Saadiyat', 'Community halls and majlis', 'Outdoor and garden events']),
  ],
  'logistics': "Abu Dhabi city is around an hour and a half's drive from International City, and longer at peak times. We plan cooking, chilling and transport so food arrives on time and is held at a safe temperature until it is served. The earlier you share your date, headcount and serving time, the easier this is to plan, especially for weddings and events with several hundred guests.",
  'faqs': [
    ('Do you cater in Abu Dhabi?', 'Yes. We cater corporate events, weddings, university events and large gatherings across Abu Dhabi, including Khalifa City, Mussafah, Al Reem and Yas Island.'),
    ('Can you cater a wedding in Abu Dhabi?', "Yes. Share your date, venue and guest numbers early and we'll build a menu and delivery plan around your event. Check first whether your venue allows outside catering."),
    ('How early should I book catering in Abu Dhabi?', 'As early as you can. Abu Dhabi is the longest journey from our kitchen, so earlier notice makes it easier to plan the menu, transport and setup.'),
    ('How is catering in Abu Dhabi priced?', 'Every quote is custom, based on your headcount, menu, service style and location. Send your date, venue and headcount for a price.'),
    ('Is your catering halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
 },
 'ras-al-khaimah': {
  'name': 'Ras Al Khaimah', 'short': 'RAK',
  'card': 'Corporate events, weddings and family gatherings in Ras Al Khaimah, planned around the drive from Dubai.',
  'title': 'Catering in Ras Al Khaimah: Events & Buffets | Messify',
  'desc': 'Catering in Ras Al Khaimah (RAK) for corporate events, weddings, family gatherings and group events. Custom halal menus and buffet setups.',
  'h1': 'Event catering in Ras Al Khaimah.',
  'lede': "We cater corporate events, weddings, family gatherings and group events in Ras Al Khaimah, with custom 100% halal menus quoted by headcount. RAK is a longer drive from our kitchen in Dubai, so share your date early and we'll plan delivery around your event.",
  'img': ('cat-serving-640.webp', 'cat-serving.webp', 1100, 1375, 'A gloved server lifting the lid of a chafing dish at a catered buffet'),
  'where_title': 'Across Ras Al Khaimah, from Al Hamra to the city.',
  'groups': [
    ('home', 'Homes and communities', ['Al Hamra Village', 'Mina Al Arab', 'Al Nakheel and Al Dhait', 'Khuzam and Al Mamourah']),
    ('office', 'Offices and business areas', ['RAK city centre', 'RAKEZ business parks', 'Al Hamra and Al Ghail industrial zones']),
    ('rings', 'Venues', ['Resorts on Al Marjan Island', 'Hotels and wedding halls', 'Community halls and majlis', 'Outdoor and desert events']),
  ],
  'logistics': "Ras Al Khaimah is roughly an hour to an hour and a half's drive from International City, depending on where your event is and the traffic. We plan cooking and transport so food arrives on time and is held safely until it is served. Many resorts and hotels use their own kitchens, so check whether your venue allows outside catering before you book.",
  'faqs': [
    ('Do you cater in Ras Al Khaimah?', 'Yes. We cater corporate events, weddings, family gatherings and group events across Ras Al Khaimah.'),
    ('How early should I book catering in RAK?', 'As early as you can. RAK is a longer drive from our kitchen in Dubai, so earlier notice makes it easier to plan the menu, transport and setup.'),
    ('Can you cater at a resort or hotel in Ras Al Khaimah?', 'Many resorts and hotels only allow their own catering, so check with your venue first. If outside catering is allowed, send us the venue details with your enquiry.'),
    ('How is catering in Ras Al Khaimah priced?', 'Every quote is custom, based on your headcount, menu, service style and location. Send your date, venue and headcount for a price.'),
    ('Is your catering halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
 },
 'umm-al-quwain': {
  'name': 'Umm Al Quwain', 'short': 'UAQ',
  'card': 'Family gatherings, outdoor events and company functions in Umm Al Quwain, with custom halal menus.',
  'title': 'Catering in Umm Al Quwain: Parties & Events | Messify',
  'desc': 'Catering in Umm Al Quwain (UAQ) for family gatherings, parties, outdoor events, company functions and bulk orders. Custom halal menus by headcount.',
  'h1': 'Party and event catering in Umm Al Quwain.',
  'lede': "We cater family gatherings, parties, outdoor events, company functions and bulk orders in Umm Al Quwain, with custom 100% halal menus quoted by headcount. UAQ is about an hour's drive from our kitchen in Dubai, so share your date early.",
  'img': ('cat-canapes.webp', 'cat-canapes.webp', 900, 1200, 'Trays of canapés on slate boards at a catered event'),
  'where_title': 'Across Umm Al Quwain.',
  'groups': [
    ('home', 'Homes and communities', ['Al Salamah and Al Raas', 'Al Ramlah and Al Humrah', 'Al Salam City', 'The Old Town and the Corniche']),
    ('office', 'Offices and business areas', ['Umm Al Quwain Free Trade Zone', 'Industrial areas along Emirates Road']),
    ('party', 'Venues', ['Beach and waterfront venues', 'Hotels and event halls', 'Community halls and majlis', 'Outdoor and farm events']),
  ],
  'logistics': "Umm Al Quwain is about an hour's drive from International City, longer at peak times. For outdoor and beach events, tell us whether there is shade, power and a table for the buffet, because heat changes how long food can safely sit out. We plan delivery so food arrives close to your serving time.",
  'faqs': [
    ('Do you cater in Umm Al Quwain?', 'Yes. We cater family gatherings, parties, outdoor events, company functions and bulk orders across Umm Al Quwain.'),
    ('Can you cater an outdoor or beach event in UAQ?', 'Yes. Tell us about shade, power and space for a buffet table, and we will plan the menu and delivery time around the heat and your serving time.'),
    ('How early should I book catering in Umm Al Quwain?', 'As early as you can. UAQ is about an hour from our kitchen in Dubai, so earlier notice makes planning easier.'),
    ('How is catering in Umm Al Quwain priced?', 'Every quote is custom, based on your headcount, menu, service style and location. Send your date, location and headcount for a price.'),
    ('Is your catering halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
 },
}

def page_cater_area(slug):
    c = CATER_AREAS[slug]
    path = f'/catering/{slug}/'
    cr, crs = crumbs([('Home', '/'), ('Catering', '/catering/'), (f'Catering in {c["name"]}', path)])
    service = {'@type': 'Service', '@id': BASE + path + '#service', 'name': f'Messify catering in {c["name"]}', 'serviceType': 'Catering',
               'description': c['desc'], 'provider': {'@id': BASE + '/#business'},
               'areaServed': {'@type': 'AdministrativeArea', 'name': c['name'], 'containedInPlace': {'@type': 'Country', 'name': 'United Arab Emirates'}},
               'hasOfferCatalog': catering_catalog()}
    page = {'path': path, 'mode': 'catering', 'nav': 'catering', 'title': c['title'], 'desc': c['desc'],
            'cta': ('#quote', 'Get a quote', 'Quote'), 'cta_bot': 'catering',
            'schema': [ORG, BUSINESS, service, faq_schema(c['faqs']), crs]}
    small, big, w, h, alt = c['img']
    srcset = f' srcset="/assets/img/{small} 640w, /assets/img/{big} {w}w" sizes="(min-width: 900px) 45vw, 100vw"' if small != big else ''
    ev = event_tiles(CATER_EVENTS)
    groups = ''.join(f'<div class="place-group"><h3>{I[ico]}{title}</h3><ul>' + ''.join(f'<li>{I["tick"]}<span>{x}</span></li>' for x in items) + '</ul></div>'
                     for ico, title, items in c['groups'])
    wa = f'{WA}?text=' + quote(f"Hi Messify, I'd like a catering quote for an event in {c['name']}.")
    body = f'''<section class="sec sec--first">
  <div class="wrap split">
    <div>
      {cr}
      <h1 class="h2 rise"><span class="kicker">Catering in {c['name']}</span> {c['h1']}</h1>
      <p class="lede rise">{c['lede']}</p>
      <div class="actions">
        <a class="btn" href="#quote" data-messibot="catering">Get a quote</a>
        <a class="btn btn--ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp us</a>
      </div>
      {rating_badge()}
      <div class="facts">
        <div><b>100%</b><span>halal menus</span></div>
        <div><b>Custom</b><span>menus, priced by headcount</span></div>
        <div><b>Buffet</b><span>setups at your venue</span></div>
      </div>
    </div>
    <div class="photo photo--tall"><img src="/assets/img/{small}"{srcset} alt="{alt}" width="{w}" height="{h}" fetchpriority="high"></div>
  </div>
</section>

<section class="sec" style="padding-top:0" aria-labelledby="events-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">What we cater in {c['name']}</p><h2 class="h2" id="events-title">From house parties to wedding halls.</h2></div>
    <div class="events">{ev}</div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="where-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Where we cater</p><h2 class="h2" id="where-title">{c['where_title']}</h2>
      <p class="lede">{c['logistics']}</p></div>
    <div class="places">{groups}</div>
    <p class="disclaim">Areas and venue types are listed to show where we cater. Send us your exact venue and we'll confirm.</p>
  </div>
</section>

<section class="sec" aria-labelledby="steps-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">How it works</p><h2 class="h2" id="steps-title">From enquiry to served, in four steps.</h2></div>
    <ol class="steps" style="max-width:820px">
      <li><div><h3>Tell us about your event</h3><p>Date, venue in {c['name']}, headcount and the time you want to serve.</p></div></li>
      <li><div><h3>Get a custom quote</h3><p>Priced by headcount, the menu you choose and the service style.</p></div></li>
      <li><div><h3>Finalise the menu</h3><p>Pick appetisers, mains, salads, desserts and drinks in the flavours you want.</p></div></li>
      <li><div><h3>Delivered on time</h3><p>Our team brings everything to your venue, with a buffet setup if you want one.</p></div></li>
    </ol>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="faq-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-title">Catering in {c['name']}: good to know.</h2></div>
    {faq_html(c['faqs'])}
  </div>
</section>

<section class="sec" aria-labelledby="cguides-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Planning help</p><h2 class="h2" id="cguides-title">Before you book.</h2></div>
    {guide_cards(CATERING_GUIDES[:3])}
    <a class="link-arrow" style="margin-top:28px" href="/guides/#catering-guides">All catering guides {I["arrow"]}</a>
  </div>
</section>

{catering_form(emirate=c['name'], title=f"Plan your event in {c['name']}.")}

<section class="sec sec--tight" aria-labelledby="other-title">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:28px"><p class="eyebrow">Across the UAE</p><h2 class="h3" id="other-title" style="font-size:1.4rem">We also cater in</h2></div>
    {emirate_cards(exclude=slug)}
  </div>
</section>'''
    render(page, body)

# ---------------------------------------------------------------- occasion guides
CATERING_GUIDES += [
    ('/guides/uae-event-catering-calendar/', 'UAE event catering calendar 2026–27',
     'Halloween, Diwali, Thanksgiving, National Day, Christmas, Ramadan, Eid and graduation season: dates and when to book.'),
    ('/guides/corporate-iftar-planning/', 'How to plan a corporate iftar',
     'Timing around Maghrib, headcount, menu, venue and the details that make a Ramadan iftar for your team work.'),
    ('/guides/diwali-party-food-planning/', 'Planning food for a Diwali party',
     'A vegetarian Diwali menu, how much to order, snacks and sweets, and timing for a party at home or the office.'),
    ('/guides/office-year-end-party-catering/', 'Catering an office year-end party',
     'Dates, budget, menu, dietary needs and logistics for a December office party in the UAE.'),
]
OG_DATE = '2026-10-23'

def page_guide_calendar():
    rows = [
        ('31 October 2026', 'Halloween', 'Kids\' and themed parties at home, school and community events.', '1–2 weeks', '/catering/birthday-parties/'),
        ('8 November 2026', 'Diwali', 'Dhanteras is 6 November and Bhai Dooj 10 November. Parties at home, office celebrations, community events.', '2–3 weeks', '/catering/diwali/'),
        ('26 November 2026', 'Thanksgiving (US)', 'Expat dinners and Friendsgivings, usually on the nearest weekend.', '2 weeks', '/catering/christmas-year-end-parties/'),
        ('2–3 December 2026', 'UAE National Day (Eid Al Etihad)', 'Office celebrations in the days before the holiday, community and family events.', '3–4 weeks', '/catering/national-day/'),
        ('December 2026', 'Year-end and Christmas parties', 'The busiest weeks of the year for office parties. Christmas is 25 December.', '4–6 weeks', '/catering/christmas-year-end-parties/'),
        ('31 December 2026', 'New Year\'s Eve', 'House parties and gatherings; a night in very high demand.', '3–4 weeks', '/catering/christmas-year-end-parties/'),
        ('6 February 2027', 'Chinese New Year', 'Office and community celebrations.', '2 weeks', '/catering/corporate-events/'),
        ('About 8 February to 9 March 2027', 'Ramadan', 'Corporate iftars, family iftars, majlis gatherings, ghabga nights and staff iftars. Expected dates, subject to the moon sighting.', '4–6 weeks', '/catering/iftar/'),
        ('About 9 or 10 March 2027', 'Eid al-Fitr', 'Family lunches, open houses and office Eid celebrations. Expected, subject to the moon sighting.', '3–4 weeks', '/catering/eid/'),
        ('About 16 or 17 May 2027', 'Eid al-Adha', 'Family gatherings and open houses. Expected, subject to the moon sighting.', '3–4 weeks', '/catering/eid/'),
        ('May to June 2027', 'Graduation season', 'Graduation parties for students and families, school and university events.', '2–3 weeks', '/catering/university-events/'),
        ('Late August to September 2027', 'New academic year', 'Orientation days, welcome events and society fairs on campus.', '3–4 weeks', '/catering/university-events/'),
    ]
    trs = ''.join(f'<tr><th scope="row">{o}</th><td data-label="Date">{d}</td><td data-label="What people cater">{w}</td><td data-label="Book ahead">{b}</td></tr>' for d, o, w, b, _ in rows)
    table = f'''<div class="table-wrap"><table class="ptable ptable--wrap">
  <caption>UAE catering calendar, October 2026 to September 2027</caption>
  <thead><tr><th scope="col">Occasion</th><th scope="col">Date</th><th scope="col">What people cater</th><th scope="col">Book ahead</th></tr></thead>
  <tbody>{trs}</tbody></table></div>'''
    sections = f'''
    <h2>Why the calendar matters for catering</h2>
    <p>In the UAE, demand for catering isn't spread evenly through the year. From October to April the weather is cooler and events pile up: Diwali, National Day, year-end parties, Christmas and New Year all land within about eight weeks, followed by Ramadan and Eid. Book late in those weeks and you choose from what's left. This calendar lists the occasions people most often cater for, their dates and how early to book.</p>

    <h2>The calendar at a glance</h2>
    {table}
    <p class="disclaim">Islamic dates depend on the moon sighting and are confirmed close to the day. Book for the expected date and confirm your final numbers once it is announced.</p>

    <h2>October and November: Halloween, Diwali and Thanksgiving</h2>
    <p><b>Halloween</b> (31 October) is mostly children's parties and themed house parties: finger food, mild dishes for children and something proper for the adults. See <a href="/catering/birthday-parties/">party catering</a>.</p>
    <p><b>Diwali</b> falls on Sunday 8 November 2026. Menus are mostly vegetarian, with snacks and sweets to share, and many families host on the weekend around it. See <a href="/catering/diwali/">Diwali catering</a> and our <a href="/guides/diwali-party-food-planning/">Diwali food guide</a>.</p>
    <p><b>Thanksgiving</b> is Thursday 26 November 2026. In the UAE it is usually celebrated by American and other expat families and friends on the nearest weekend, as a roast-style dinner.</p>

    <h2>December: National Day, year-end parties, Christmas and New Year</h2>
    <p>December is the most crowded month. <b>UAE National Day</b> (Eid Al Etihad) is a public holiday on 2 and 3 December 2026, and offices celebrate in the days before it. <b>Year-end office parties</b> cluster in the first three weeks of December, then come <b>Christmas</b> and <b>New Year's Eve</b>. If your company holds a December party, fix the date and book in October or early November. See <a href="/catering/national-day/">National Day catering</a> and <a href="/catering/christmas-year-end-parties/">year-end party catering</a>.</p>

    <h2>February and March: Ramadan and Eid al-Fitr</h2>
    <p><b>Ramadan 2027</b> is expected to begin around 8 February 2027. Iftar catering is in demand every evening of the month, especially at weekends and in the last ten days. Corporate iftars need booking four to six weeks ahead. <b>Eid al-Fitr</b> is expected around 9 or 10 March 2027, when families host lunches and open houses. See <a href="/catering/iftar/">iftar catering</a>, our <a href="/guides/corporate-iftar-planning/">corporate iftar guide</a> and <a href="/catering/eid/">Eid catering</a>.</p>

    <h2>May to September: Eid al-Adha, graduations and the new academic year</h2>
    <p><b>Eid al-Adha</b> is expected around 16 or 17 May 2027. <b>Graduation season</b> runs from May into June. Summer is quieter as many residents travel, then <b>orientation weeks</b> bring campus events from late August. See <a href="/catering/university-events/">university event catering</a>.</p>

    <h2>Events that happen all year</h2>
    <p>Weddings, birthdays, family gatherings, business meetings and corporate events happen in every month, though weddings and outdoor events are concentrated in the cooler months. See <a href="/catering/weddings/">wedding catering</a>, <a href="/catering/family-gatherings/">family gatherings</a>, <a href="/catering/business-meetings/">business meetings</a> and <a href="/catering/corporate-events/">corporate events</a>.</p>

    <h2>How early to book, in short</h2>
    <ul>
      <li><b>Peak dates</b> (December parties, iftars, Eid, New Year's Eve): four to six weeks.</li>
      <li><b>Busy-season weekends</b> (October to April): two to four weeks.</li>
      <li><b>Weekday office lunches and small parties</b>: a few days to a week, if the date is quiet.</li>
    </ul>
    <p>Whatever the occasion, send us your date, location, headcount and serving time for a <a href="/catering/#quote">catering quote</a>.</p>'''
    faqs = [
        ('When is the busiest time for catering in the UAE?', 'The cooler months from October to April, and especially December (National Day, year-end parties, Christmas and New Year) and Ramadan.'),
        ('When is Ramadan 2027?', 'Ramadan 2027 is expected to begin around 8 February 2027 and end around 9 March 2027, subject to the moon sighting.'),
        ('When is Diwali 2026 in the UAE?', 'Diwali falls on Sunday 8 November 2026, with Dhanteras on 6 November and Bhai Dooj on 10 November.'),
        ('When is UAE National Day 2026?', 'The Eid Al Etihad public holiday in 2026 is on 2 and 3 December.'),
        ('How far in advance should I book catering for the festive season?', 'Four to six weeks for December parties, iftars, Eid and New Year\'s Eve; two to four weeks for other busy-season weekends.'),
    ]
    article_page('/guides/uae-event-catering-calendar/', 'Catering calendar', 'UAE Event Catering Calendar 2026–27: Dates | Messify',
                 'Key UAE catering dates for 2026–27: Halloween, Diwali, Thanksgiving, National Day, Christmas, Ramadan, Eid and graduations, and when to book.',
                 'UAE event catering calendar 2026–27', 'Catering guide · 2026–27',
                 'The busiest catering dates in the UAE for 2026–27 are Diwali (8 November 2026), UAE National Day (2–3 December), December year-end parties, Christmas and New Year, then Ramadan (expected from about 8 February 2027) and Eid al-Fitr (about 9–10 March 2027). Book four to six weeks ahead for peak dates.',
                 sections, faqs, kind='catering', published=OG_DATE)

def page_guide_corporate_iftar():
    sections = '''
    <h2>Why a corporate iftar needs more planning than a lunch</h2>
    <p>An iftar has a fixed moment: the call to Maghrib. Food that arrives five minutes late, or is still being set up when guests break their fast, is the one mistake everyone remembers. Add heavy traffic in the hour before iftar, guests arriving straight from work, and a time that moves a little each day, and it pays to plan carefully.</p>

    <h2>1. Pick the date and confirm the iftar time</h2>
    <p>Ramadan 2027 is expected to begin around 8 February 2027, subject to the moon sighting. Maghrib moves a minute or two each day, so check the iftar time for your date and city. Weekday iftars in the first two weeks are usually easier to book than weekends and the last ten days.</p>

    <h2>2. Decide the format</h2>
    <ul>
      <li><b>Iftar at the office:</b> simple to organise, and staff don't need to travel in iftar traffic. Needs space for a buffet and seating.</li>
      <li><b>Iftar at a venue:</b> more of an occasion, especially for clients and partners. Check whether the venue allows outside catering.</li>
      <li><b>Ghabga:</b> a later evening gathering after taraweeh, more relaxed, with lighter food. It suits teams who prefer to break their fast at home.</li>
      <li><b>Iftar meals for staff:</b> individual meals delivered to staff accommodation or sites, often sponsored by the company.</li>
    </ul>

    <h2>3. Headcount and guests</h2>
    <p>Invite non-fasting colleagues too: a corporate iftar is a team occasion. Collect RSVPs early and give the caterer a final number a few days before. Because many guests arrive in the last minutes before Maghrib, make sure people know the start time and where to go.</p>

    <h2>4. Build the menu in stages</h2>
    <ol>
      <li><b>Break the fast:</b> dates, water and laban, ready on the tables before Maghrib.</li>
      <li><b>Light start:</b> lentil soup or harees, samosas or sambousek, and salads such as fattoush.</li>
      <li><b>Main meal:</b> after Maghrib prayer, a rice dish such as biryani, mandi or ouzi, with grills or curries and a vegetarian main.</li>
      <li><b>To finish:</b> luqaimat, kunafa or umm ali, fruit, Arabic coffee and tea.</li>
    </ol>
    <p>For quantities, our <a href="/guides/how-much-food-per-person-catering/">food per person guide</a> applies: iftar guests eat a full meal.</p>

    <h2>5. Set aside space for prayer</h2>
    <p>Many guests will pray Maghrib before the main meal. Set aside a clean, quiet space with prayer mats, and plan the main meal to be served after the prayer.</p>

    <h2>6. Timing on the day</h2>
    <ul>
      <li>Ask the caterer to arrive and set up well before Maghrib, allowing for traffic.</li>
      <li>Have dates and water on the tables, not on the buffet, so guests can break their fast immediately.</li>
      <li>Keep speeches short and after the meal.</li>
    </ul>

    <h2>7. Daytime during Ramadan</h2>
    <p>If you are catering daytime meetings during Ramadan for non-fasting colleagues, serve food discreetly in a private room, out of sight of colleagues who are fasting.</p>

    <h2>Book your corporate iftar</h2>
    <p>We cater corporate iftars, ghabga nights and staff iftar meals across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain, with 100% halal menus planned around Maghrib. See <a href="/catering/iftar/">iftar catering</a> or send your date, venue and headcount for a <a href="/catering/#quote">quote</a>.</p>'''
    faqs = [
        ('How far ahead should I book a corporate iftar?', 'Four to six weeks ahead. Weekends and the last ten days of Ramadan fill up first.'),
        ('What should a corporate iftar menu include?', 'Dates, water and laban to break the fast, then soup and savoury bites, a main course with a rice dish, grills or curries and a vegetarian option, and sweets with Arabic coffee and tea.'),
        ('What is a ghabga?', 'A Ramadan evening gathering held later at night, after taraweeh prayers. It is more relaxed than an iftar, with lighter food.'),
        ('Should non-fasting colleagues be invited to an iftar?', 'Yes. A corporate iftar is a team occasion, and colleagues of every background are usually welcome.'),
        ('When is Ramadan 2027?', 'Ramadan 2027 is expected to begin around 8 February 2027, subject to the moon sighting.'),
    ]
    article_page('/guides/corporate-iftar-planning/', 'Corporate iftar', 'How to Plan a Corporate Iftar in the UAE | Messify',
                 'Plan a corporate iftar in Dubai and the UAE: timing around Maghrib, format, headcount, menu in stages, prayer space and when to book for Ramadan 2027.',
                 'How to plan a corporate iftar', 'Ramadan guide · 2027',
                 'Book a corporate iftar four to six weeks ahead. Confirm the Maghrib time for your date, choose the format (office, venue, ghabga or staff meals), collect RSVPs, have dates and water on the tables before Maghrib, set aside space for prayer, and serve the main meal after the prayer. Ramadan 2027 is expected to begin around 8 February 2027.',
                 sections, faqs, kind='catering', published=OG_DATE)

def page_guide_diwali():
    rows = [('Snacks (samosas, pakoras, dhokla)', '4–6 pieces'), ('Rice, biryani or pulao (cooked)', '150 g'), ('Paneer, dal and vegetable curries (all together)', '250 g'),
            ('Breads (puri, naan or roti)', '2 pieces'), ('Raita and salad', '75 g'), ('Indian sweets and desserts', '2–3 pieces or 1 portion')]
    trs = ''.join(f'<tr><th scope="row">{a}</th><td data-label="Per adult guest">{b}</td></tr>' for a, b in rows)
    table = f'''<div class="table-wrap"><table class="ptable ptable--wrap">
  <caption>Vegetarian Diwali dinner: planning amounts per adult guest</caption>
  <thead><tr><th scope="col">Item</th><th scope="col">Per adult guest</th></tr></thead>
  <tbody>{trs}</tbody></table></div>'''
    sections = f'''
    <h2>Diwali 2026 dates in the UAE</h2>
    <p>Diwali (Lakshmi Puja) falls on <b>Sunday 8 November 2026</b>. Dhanteras is on Friday 6 November and Bhai Dooj on Tuesday 10 November in the UAE. Many families host on the weekend around Diwali, and offices often celebrate in the working days just before or after, so book early.</p>

    <h2>Build a vegetarian menu</h2>
    <p>Most Diwali menus are vegetarian. A balanced spread has four parts:</p>
    <ul>
      <li><b>Snacks</b> for guests as they arrive: samosas, pakoras, dhokla, chaat-style bites.</li>
      <li><b>Two or three curries:</b> one paneer dish, one dal, one vegetable or chole.</li>
      <li><b>Rice and breads:</b> a biryani or pulao, with puri, naan or roti.</li>
      <li><b>Sweets:</b> the heart of Diwali. Gulab jamun, kheer and mithai, plus chai.</li>
    </ul>

    <h2>How much food to order</h2>
    {table}
    <p>Count children under 10 as half a guest. If guests are visiting several homes on the same evening, they will eat less at each, so lean towards snacks and sweets rather than a full dinner.</p>

    <h2>Pure vegetarian and Jain guests</h2>
    <p>Some guests only eat food cooked in a pure-vegetarian kitchen, and Jain guests avoid onion, garlic and root vegetables. Ask your caterer directly whether their kitchen also cooks meat, and whether they can do Jain dishes. Our partner kitchen cooks both vegetarian and non-vegetarian food, so if this matters to your guests, tell us and we will say upfront what we can do.</p>

    <h2>Timing for a Diwali party</h2>
    <ul>
      <li>Serve snacks as guests arrive, and dinner after the puja.</li>
      <li>Tell the caterer when you want to eat, not when guests arrive.</li>
      <li>Keep candles and diyas well away from the buffet table.</li>
    </ul>

    <h2>Office Diwali celebrations</h2>
    <p>For the office, a lunch buffet with two curries, rice, breads and a sweet works well, or snacks and sweets with chai in the afternoon. Make sure non-vegetarian colleagues know the menu is vegetarian, so no one is surprised.</p>

    <h2>Get a Diwali catering quote</h2>
    <p>We cater Diwali parties at home, office celebrations and community gatherings across the UAE. See <a href="/catering/diwali/">Diwali catering</a> or send your date, location and headcount for a <a href="/catering/#quote">quote</a>.</p>'''
    faqs = [
        ('When is Diwali 2026?', 'Diwali (Lakshmi Puja) falls on Sunday 8 November 2026 in the UAE, with Dhanteras on 6 November and Bhai Dooj on 10 November.'),
        ('What food is served at a Diwali party?', 'Usually a vegetarian spread: snacks such as samosas and pakoras, paneer, dal and vegetable curries, biryani or pulao, puri or naan, and Indian sweets with chai.'),
        ('How much food do I need for a Diwali party?', 'Per adult, plan about 4–6 snacks, 150 g of rice or biryani, 250 g of curries and dal, 2 breads, some raita and salad, and 2–3 sweets.'),
        ('Can a caterer provide Jain food?', 'Some can. Ask whether the kitchen can cook without onion, garlic and root vegetables, and whether it also cooks meat.'),
        ('Does Messify cater Diwali?', 'Yes. We cater Diwali parties at home, office celebrations and community gatherings, with vegetarian Indian menus and sweets.'),
    ]
    article_page('/guides/diwali-party-food-planning/', 'Diwali party food', 'Diwali Party Food: Menu & How Much to Order | Messify',
                 'Plan the food for a Diwali party in the UAE: a vegetarian menu, how much to order per guest, snacks and sweets, Jain guests and timing for 2026.',
                 'Planning food for a Diwali party', 'Diwali guide · 2026',
                 'Diwali 2026 is on Sunday 8 November. A Diwali party menu is usually vegetarian: snacks as guests arrive, two or three curries (paneer, dal, vegetables), rice and breads, and Indian sweets with chai. Per adult, plan about 150 g of rice, 250 g of curries, 2 breads and 2–3 sweets.',
                 sections, faqs, kind='catering', published=OG_DATE)

def page_guide_year_end():
    sections = '''
    <h2>Fix the date first</h2>
    <p>December is the busiest month for events in the UAE. UAE National Day is on 2 and 3 December 2026, and most companies hold their year-end party in the first three weeks of December, before people travel. Popular dates go first, so set your date in October or early November and book the caterer straight away.</p>

    <h2>Choose the format</h2>
    <ul>
      <li><b>Lunch at the office:</b> the easiest to organise and the most inclusive, because everyone is already there.</li>
      <li><b>Evening party at the office or a venue:</b> more of an occasion. Check whether the venue allows outside catering.</li>
      <li><b>Bites and drinks:</b> lighter and cheaper than dinner, but if it runs past 8 PM, people expect a proper meal.</li>
    </ul>

    <h2>Set a budget per person</h2>
    <p>Work out the budget per head, then decide what it covers: food, setup, staff and equipment. Catering is usually quoted per person, so a clear headcount and budget lets the caterer suggest a menu that fits. Our guide to <a href="/guides/catering-cost-dubai/">how catering is priced</a> explains what moves the price.</p>

    <h2>A menu for a mixed team</h2>
    <p>UAE teams are international, so the best year-end menus mix cuisines: something festive and Continental, an Indian or Arabic favourite, a vegetarian main and a good dessert. Keep it halal so everyone can eat everything.</p>

    <h2>Dietary needs</h2>
    <p>Collect them with your RSVPs: vegetarian, vegan, allergies and any medical diets. Label dishes on the day.</p>

    <h2>Logistics</h2>
    <ul>
      <li>Confirm building access, a delivery pass and the service lift for office towers.</li>
      <li>Plan space for a buffet table and a queue, and power if food is kept warm.</li>
      <li>Agree serving time, clean-up and what happens to leftovers.</li>
      <li>Confirm the final headcount two to three days before.</li>
    </ul>
    <p>Our <a href="/guides/corporate-event-catering-checklist/">corporate event catering checklist</a> has the full list.</p>

    <h2>Book your year-end party catering</h2>
    <p>We cater office year-end parties, Christmas lunches and New Year gatherings across the UAE, with custom 100% halal menus and buffet setups. See <a href="/catering/christmas-year-end-parties/">Christmas and year-end catering</a> or send your date, venue and headcount for a <a href="/catering/#quote">quote</a>.</p>'''
    faqs = [
        ('When should we book catering for a December office party?', 'In October or early November. The first three weeks of December are the busiest weeks of the year for events in the UAE.'),
        ('What food works for an office year-end party?', 'A mix of cuisines for an international team: a festive Continental dish, an Indian or Arabic favourite, a vegetarian main and a good dessert, all halal.'),
        ('Lunch or evening party?', 'Lunch at the office is the easiest and most inclusive. An evening party feels more like an occasion but needs a venue and more planning.'),
        ('How much food for an office party?', 'For a full buffet, plan about 150 g of rice, 175 g of mains, 100 g of vegetable dishes, a salad and a dessert per guest. For bites only, around 10 to 12 pieces per guest for two hours.'),
        ('Does Messify cater office year-end parties?', 'Yes. We cater year-end parties, Christmas lunches and New Year gatherings with custom 100% halal menus and buffet setups.'),
    ]
    article_page('/guides/office-year-end-party-catering/', 'Year-end party catering', 'Office Year-End Party Catering in the UAE | Messify',
                 'Plan catering for an office year-end party in Dubai and the UAE: when to book in December, format, budget per person, a menu for a mixed team and logistics.',
                 'Catering an office year-end party', 'Catering guide · 2026',
                 'Book December office party catering in October or early November, because the first three weeks of December are the busiest of the year. Decide between an office lunch, an evening party or bites and drinks, set a budget per person, choose a halal menu that mixes cuisines, and collect dietary needs with RSVPs.',
                 sections, faqs, kind='catering', published=OG_DATE)

# ---------------------------------------------------------------- catering by event type and occasion
I.update({
 'moon': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/></svg>',
 'lamp': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 14h18a9 9 0 0 1-18 0Z"/><path d="M12 3c1.6 2 2 3.4 0 6-2-2.6-1.6-4 0-6Z"/><path d="M12 9v5"/></svg>',
 'gift': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v9h14v-9M12 8v13"/><path d="M12 8S10.5 3 8 4s0 4 4 4ZM12 8s1.5-5 4-4 0 4-4 4Z"/></svg>',
 'flag': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V4"/><path d="M5 4h13l-2.5 4.5L18 13H5"/></svg>',
 'cake': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 21h16v-8H4v8Z"/><path d="M4 16c2 1.5 4 1.5 6 0s4-1.5 6 0 3 1 4 0M8 13V9M12 13V9M16 13V9"/><path d="M8 6v1M12 5v2M16 6v1"/></svg>',
 'users': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/></svg>',
 'mic': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>',
 'cup': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V8Z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 3v2M12 3v2"/></svg>',
 'star': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3Z"/></svg>',
})

CATER_IMGS = [
    ('cat-serving-640.webp', 'cat-serving.webp', 1100, 1375, 'A gloved server lifting the lid of a chafing dish at a catered buffet'),
    ('cat-chef-640.webp', 'cat-chef.webp', 1024, 1024, 'A chef carving at a buffet station while guests serve themselves at an evening event'),
    ('cat-canapes.webp', 'cat-canapes.webp', 900, 1200, 'Trays of canapés on slate boards at a catered event'),
]

FORM_TYPES = ['Corporate event', 'Business meeting or office lunch', 'Wedding', 'Family gathering', 'Birthday party', 'University event',
              'Iftar or Ramadan event', 'Eid', 'Diwali', 'Christmas or year-end party', 'National Day', 'Buffet setup', 'Bulk catering', 'Other']

CATER_TYPES = {
 # ------------------------------------------------ by event
 'corporate-events': {
  'kind': 'event', 'name': 'Corporate event catering', 'short': 'Corporate events', 'icon': 'case', 'img': 0, 'form': 'Corporate event',
  'card': 'Conferences, launches, team days, annual parties and award nights.',
  'title': 'Corporate Event Catering in Dubai & the UAE | Messify',
  'desc': 'Corporate event catering in Dubai and the UAE: conferences, launches, team days, annual parties and award nights. Custom halal menus and buffet setups.',
  'kicker': 'Corporate event catering', 'h1': 'Catering for company events, at any scale.',
  'lede': "From a 40-person team day to a conference for several hundred, we cater corporate events across Dubai, Sharjah, Abu Dhabi and the rest of the UAE. Every menu is custom and 100% halal, quoted by headcount, with buffet setups at your venue.",
  'facts': [('5,000+', 'meals a day of kitchen capacity'), ('100%', 'halal, custom menus'), ('Buffet', 'setups at your venue')],
  'offers': [
    ('mic', 'Conferences and seminars', 'Breakfast, breaks and lunch planned around your agenda, not the other way round.'),
    ('star', 'Launches and open days', 'Bites and drinks for guests who arrive in waves, or a full buffet for a seated crowd.'),
    ('users', 'Team days and town halls', 'Generous buffets for the whole company, from one floor to several sites.'),
    ('gift', 'Annual and year-end parties', 'Evening menus with a sense of occasion for your end-of-year celebration.'),
    ('serve', 'Award nights and dinners', 'Buffet dinners with dishes that hold well through speeches and presentations.'),
    ('box', 'Staff and site catering', 'Bulk meals for staff, sites and large teams, delivered on schedule.'),
  ],
  'plan_title': 'What makes corporate catering go smoothly.',
  'plan': '''<p>Corporate events are planned around an agenda, so the food has to be too. Tell us the <b>serving times</b>, not just the start time: a conference might need breakfast at 8:30, a coffee break at 10:45 and lunch at 1 PM. We build the menu and delivery around those times.</p>
<p>Give us a realistic headcount, including speakers, staff and guests, and collect dietary needs with your registrations. Make sure at least one main dish is vegetarian. If your venue is an office tower, check whether it needs a delivery pass, a service lift booking or a loading bay slot.</p>
<p>For a full walkthrough, read our <a href="/guides/corporate-event-catering-checklist/">corporate event catering checklist</a>.</p>''',
  'menu': [('To start', ['Breakfast spreads for early sessions', 'Savoury bites and sandwiches', 'Fresh salads']),
           ('Mains', ['Biryani, curries and grills', 'Pasta bakes and Continental mains', 'Arabic rice and grills', 'A vegetarian main every time']),
           ('To finish', ['Desserts and sweet bites', 'Fruit', 'Tea, coffee and juices'])],
  'faqs': [
    ('Do you cater conferences and large corporate events?', 'Yes. Our partner kitchen can produce 5,000+ meals a day, so we cater events from a few dozen to several hundred guests, with buffet setups at your venue.'),
    ('Can you work around our event agenda?', 'Yes. Send us your serving times for breakfast, breaks and lunch, and we plan the menu and delivery around them.'),
    ('Can you invoice our company?', 'Yes. Share your company details when you request a quote, and tell us if your finance team needs anything specific on the invoice.'),
    ('How far ahead should we book corporate catering?', 'Two to three weeks is comfortable for most events, and earlier for large events and the busy months from October to April.'),
    ('Which emirates do you cover for corporate events?', 'Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain.'),
  ],
  'guides': ['/guides/corporate-event-catering-checklist/', '/guides/how-much-food-per-person-catering/', '/guides/catering-cost-dubai/'],
 },
 'business-meetings': {
  'kind': 'event', 'name': 'Business meeting catering', 'short': 'Business meetings', 'icon': 'cup', 'img': 2, 'form': 'Business meeting or office lunch',
  'card': 'Working lunches, board meetings, workshops and training days.',
  'title': 'Business Meeting & Office Lunch Catering | Messify',
  'desc': 'Catering for business meetings, working lunches, board meetings, workshops and training days in Dubai and the UAE. Custom halal menus by headcount.',
  'kicker': 'Business meeting catering', 'h1': 'Meeting and office lunch catering.',
  'lede': "Working lunches, board meetings, client workshops and training days. We deliver food that is easy to eat around a meeting table, timed to your break, with custom 100% halal menus quoted by headcount.",
  'facts': [('On time', 'for your break, not before'), ('100%', 'halal menus'), ('Custom', 'menus, by headcount')],
  'offers': [
    ('cup', 'Working lunches', 'Food that is easy to eat at the table, so the meeting can keep going.'),
    ('case', 'Board and client meetings', 'A smarter spread when you are hosting clients or the board.'),
    ('mic', 'Workshops and training days', 'Breakfast, a mid-morning break and lunch for full-day sessions.'),
    ('office', 'Office lunches', 'Lunch for the whole team, delivered to your office.'),
    ('users', 'Interviews and assessment days', 'Simple, reliable food for candidates and panels.'),
    ('serve', 'Buffet setups', 'A buffet laid out in your meeting room or pantry.'),
  ],
  'plan_title': 'Meeting food that works around the meeting.',
  'plan': '''<p>Meeting food has one job: keep people going without stopping the meeting. Choose dishes that are easy to eat with a fork or by hand, avoid anything messy for client-facing meetings, and keep heavy dishes for after the session rather than before it.</p>
<p>Tell us the time of the break and the room. We aim to arrive shortly before, so the food is ready when people are, not sitting out through the first agenda item. For full-day workshops, a light breakfast, a mid-morning break and a proper lunch keeps energy up better than one large meal.</p>
<p>If your team needs lunch every day rather than for one meeting, a meal plan is simpler: see <a href="/guides/office-lunch-delivery-silicon-oasis/">office lunch delivery in Silicon Oasis</a>.</p>''',
  'menu': [('Easy to eat', ['Wraps and sandwiches', 'Salads and bowls', 'Savoury bites']),
           ('Hot lunch', ['Rice dishes and curries', 'Grilled chicken and sides', 'Pasta and Continental dishes', 'A vegetarian main every time']),
           ('Breaks', ['Pastries and breakfast items', 'Fruit and sweet bites', 'Tea, coffee and juices'])],
  'faqs': [
    ('Can you deliver lunch for a meeting at our office?', 'Yes. Tell us the time of your break, the room and the headcount, and we deliver lunch timed to your break.'),
    ('What food works best for a working lunch?', 'Dishes that are easy to eat at the table: wraps, salads, bowls and rice dishes, with a vegetarian option. We help you pick.'),
    ('Do you cater full-day workshops and training?', 'Yes. We can plan breakfast, a mid-morning break and lunch around your schedule.'),
    ('Can you set up a buffet in our meeting room?', 'Yes. We can lay out a buffet in your meeting room or pantry if there is space for a table.'),
    ('Is your food halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
  'guides': ['/guides/corporate-event-catering-checklist/', '/guides/how-much-food-per-person-catering/', '/guides/buffet-vs-plated-catering/'],
 },
 'weddings': {
  'kind': 'event', 'name': 'Wedding catering', 'short': 'Weddings', 'icon': 'rings', 'img': 1, 'form': 'Wedding',
  'card': 'Nikah, receptions, walima, mehndi and henna nights, built around your guest list.',
  'title': 'Wedding Catering in Dubai & the UAE | Messify',
  'desc': 'Wedding catering in Dubai and across the UAE: nikah, receptions, walima, mehndi and henna nights. Custom halal menus and full buffet setups.',
  'kicker': 'Wedding catering', 'h1': 'Wedding catering, built around your guest list.',
  'lede': "Nikah, reception, walima, mehndi or henna night: we cater weddings across the UAE with generous, custom menus, 100% halal, and full buffet setups at your venue or home. Every quote is built around your guest numbers.",
  'facts': [('5,000+', 'meals a day of kitchen capacity'), ('100%', 'halal menus'), ('Buffet', 'setups at your venue')],
  'offers': [
    ('rings', 'Nikah and reception', 'The main celebration, with a full buffet sized to your guest list.'),
    ('serve', 'Walima', 'Generous menus for the walima, at a hall, a venue or at home.'),
    ('party', 'Mehndi and henna nights', 'Lively menus for the night before, often for a separate crowd.'),
    ('users', 'Separate halls', 'Separate menus, timings and service for men\'s and women\'s halls.'),
    ('home', 'Weddings at home', 'Buffets set up in villas, gardens and majlis.'),
    ('star', 'Engagements', 'Smaller celebrations with the same care as the big day.'),
  ],
  'plan_title': 'Planning wedding food, without the stress.',
  'plan': '''<p>Start with your venue: many hotels in the UAE only allow their own kitchens, while halls, gardens and family homes usually give you freedom to choose your caterer. Then agree a realistic guest number with both families, because the number who arrive is often different from the invitation list.</p>
<p>If your celebration has separate halls, give us a headcount for each, and decide whether each hall gets its own buffet and serving time. If the wedding runs over several days, list every event so we can plan menus that don't repeat.</p>
<p>Our <a href="/guides/wedding-catering-checklist-uae/">wedding catering checklist for the UAE</a> covers the questions to ask before you book.</p>''',
  'menu': [('Welcome', ['Savoury bites as guests arrive', 'Fresh juices and soft drinks']),
           ('The main spread', ['Biryani, mandi or other rice dishes', 'Curries, grills and roasts', 'Arabic, Indian or Continental mains', 'Vegetarian mains']),
           ('To finish', ['Indian, Arabic and Continental desserts', 'Fruit', 'Tea and coffee'])],
  'faqs': [
    ('Do you cater weddings in Dubai and across the UAE?', 'Yes. We cater weddings in Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain, with custom 100% halal menus and full buffet setups.'),
    ('Can you cater separate men\'s and women\'s halls?', 'Yes. Give us a headcount for each hall and we will plan the quantities, timings and setup for each.'),
    ('Can you cater a wedding at a hotel?', 'Many hotels only allow their own catering, so check with your venue first. Halls, gardens and homes usually allow outside caterers.'),
    ('How early should we book wedding catering?', 'Once your venue and date are confirmed, ideally a few months ahead for a large wedding, and earlier for the busy season from October to April.'),
    ('Do you cater mehndi, henna nights and walima?', 'Yes. Tell us every event in your wedding and we will quote them together.'),
  ],
  'guides': ['/guides/wedding-catering-checklist-uae/', '/guides/how-much-food-per-person-catering/', '/guides/buffet-vs-plated-catering/'],
 },
 'family-gatherings': {
  'kind': 'event', 'name': 'Family gathering catering', 'short': 'Family gatherings', 'icon': 'users', 'img': 0, 'form': 'Family gathering',
  'card': 'Family lunches, reunions, aqiqah, baby showers, engagements and housewarmings.',
  'title': 'Family Gathering Catering in Dubai & the UAE | Messify',
  'desc': 'Catering for family gatherings at home in Dubai and the UAE: family lunches, reunions, aqiqah, baby showers and housewarmings. Halal buffets by headcount.',
  'kicker': 'Family gathering catering', 'h1': 'Family gatherings, catered at home.',
  'lede': "Family lunches, reunions, aqiqah, baby showers, engagements and housewarmings. We cater family gatherings at home across the UAE, with custom 100% halal menus and a buffet setup if you want one, so you get to spend the day with your family instead of in the kitchen.",
  'facts': [('At home', 'villas, flats, gardens and majlis'), ('100%', 'halal menus'), ('Custom', 'menus, by headcount')],
  'offers': [
    ('users', 'Family lunches and reunions', 'Weekend lunches for the whole family, however big it is.'),
    ('home', 'Housewarmings', 'A spread for friends and neighbours in your new home.'),
    ('star', 'Aqiqah', 'Generous menus to share with family and friends.'),
    ('party', 'Baby showers', 'Lighter menus, bites and desserts for an afternoon celebration.'),
    ('rings', 'Engagements', 'A celebration menu for the families meeting.'),
    ('serve', 'Majlis gatherings', 'Buffets and platters for guests at your majlis.'),
  ],
  'plan_title': 'Catering at home, made easy.',
  'plan': '''<p>Count adults and children separately (children under 10 eat about half an adult portion), and plan for the number you expect to arrive, which is often more than the number who replied. Tell us when you want to <b>eat</b>, not when guests arrive.</p>
<p>Think about where the buffet will go: a long table against a wall works for smaller groups, and a table guests can reach from both sides keeps a bigger crowd moving. If you live in a building, let security know about the delivery and book the service lift if needed.</p>
<p>Our <a href="/guides/party-catering-at-home-dubai/">guide to party catering at home</a> covers space, timing, outdoor heat and food safety.</p>''',
  'menu': [('To start', ['Samosas, pastries and savoury bites', 'Hummus, salads and dips']),
           ('Mains', ['Biryani, mandi and rice dishes', 'Curries and grills', 'Pasta bakes for children', 'Vegetarian mains']),
           ('To finish', ['Desserts and Arabic or Indian sweets', 'Fruit', 'Tea, coffee and juices'])],
  'faqs': [
    ('Do you cater family gatherings at home?', 'Yes. We cater family lunches, reunions, aqiqah, baby showers, engagements and housewarmings at home, with a buffet setup if you want one.'),
    ('How do I count children for catering?', 'Children under 10 count as about half a guest. Tell us how many adults and children you expect and we will size the menu.'),
    ('Can you set up a buffet in a flat?', 'Yes, if there is space for a table. Let your building security know about the delivery and book the service lift if needed.'),
    ('Can you include vegetarian dishes?', 'Yes. We can include vegetarian dishes in any menu.'),
    ('Is your food halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
  'guides': ['/guides/party-catering-at-home-dubai/', '/guides/how-much-food-per-person-catering/', '/guides/buffet-vs-plated-catering/'],
 },
 'birthday-parties': {
  'kind': 'event', 'name': 'Birthday party catering', 'short': 'Birthday parties', 'icon': 'cake', 'img': 2, 'form': 'Birthday party',
  'card': 'Kids\' parties, milestone birthdays and themed parties, at home or at a venue.',
  'title': 'Birthday Party Catering in Dubai & the UAE | Messify',
  'desc': 'Birthday party catering in Dubai and the UAE: kids\' parties, milestone birthdays and themed parties at home or a venue. Custom halal menus by headcount.',
  'kicker': 'Birthday party catering', 'h1': 'Birthday party catering, sorted.',
  'lede': "Kids' parties, a 30th, a 50th or a themed party: we cater birthdays at home or at your venue across the UAE, with custom 100% halal menus, food children actually eat, and a buffet setup if you want one.",
  'facts': [('Kids', 'and grown-up menus'), ('100%', 'halal menus'), ('Buffet', 'setups at home or a venue')],
  'offers': [
    ('cake', 'Kids\' birthday parties', 'Simple, child-friendly food, plus something proper for the parents.'),
    ('star', 'Milestone birthdays', 'A celebration menu for a 21st, 30th, 40th, 50th or 60th.'),
    ('party', 'Themed and Halloween parties', 'Bites and buffets for themed parties, from Halloween to costume nights.'),
    ('home', 'Parties at home', 'Buffets set up in villas, flats and gardens.'),
    ('users', 'Surprise parties', 'Delivery timed so the surprise stays a surprise.'),
    ('serve', 'Venue parties', 'Catering for parties at halls and event spaces that allow outside caterers.'),
  ],
  'plan_title': 'Feeding a party crowd.',
  'plan': '''<p>For a kids' party, plan two menus: simple food for the children (pasta, mild chicken, finger food) and a proper meal for the adults who came with them. Children under 10 count as about half a guest. Serve food early in the party, before the games and cake.</p>
<p>For an evening party, decide whether guests expect a full dinner or bites and drinks: the quantities are very different. Our <a href="/guides/how-much-food-per-person-catering/">food per person guide</a> has a calculator for both.</p>
<p>Planning a party at home? Read our <a href="/guides/party-catering-at-home-dubai/">guide to party catering at home in Dubai</a>.</p>''',
  'menu': [('For children', ['Mild pasta and chicken dishes', 'Mini sandwiches and finger food', 'Fruit']),
           ('For adults', ['Biryani, curries and grills', 'Continental and Italian dishes', 'Salads', 'Vegetarian mains']),
           ('Party extras', ['Savoury bites', 'Desserts and sweet bites', 'Juices and soft drinks'])],
  'faqs': [
    ('Do you cater kids\' birthday parties?', 'Yes. We plan simple, child-friendly food for the children and a proper menu for the adults.'),
    ('Do you make birthday cakes?', 'Tell us in your enquiry if you need a cake and the team will confirm what we can provide. Many families order the cake separately.'),
    ('Can you cater a Halloween or themed party?', 'Yes. Tell us the theme and headcount, and we will build a menu of bites or a buffet to fit.'),
    ('How much food do I need for a birthday party?', 'For a full meal, plan about 150 g of rice, 175 g of meat, chicken or fish, 100 g of vegetable dishes, a salad and a dessert per adult, with children under 10 counted as half.'),
    ('Is your food halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
  'guides': ['/guides/party-catering-at-home-dubai/', '/guides/how-much-food-per-person-catering/', '/guides/uae-event-catering-calendar/'],
 },
 'university-events': {
  'kind': 'event', 'name': 'University event catering', 'short': 'University events', 'icon': 'cap', 'img': 0, 'form': 'University event',
  'card': 'Orientation days, society events, career fairs, graduations and campus functions.',
  'title': 'University & Student Event Catering in the UAE | Messify',
  'desc': 'Catering for university events in Dubai and the UAE: orientation days, society events, career fairs, graduations and campus functions. Halal menus.',
  'kicker': 'University event catering', 'h1': 'Catering for campus events.',
  'lede': "Orientation days, society nights, career fairs, guest lectures and graduations. We cater university events across the UAE, including Dubai Academic City, where we deliver meal plans every day, with custom 100% halal menus that feed students properly.",
  'facts': [('Students', 'fed properly'), ('100%', 'halal menus'), ('Custom', 'menus, by headcount')],
  'offers': [
    ('cap', 'Orientation and welcome days', 'Food for new students and families on their first day.'),
    ('users', 'Society events', 'Cultural nights, socials and society iftars.'),
    ('case', 'Career fairs', 'Food for exhibitors, recruiters and students.'),
    ('mic', 'Guest lectures and conferences', 'Breaks and lunches for academic events.'),
    ('star', 'Graduations', 'Celebration menus for graduates and their families.'),
    ('box', 'Bulk student meals', 'Large volumes for residences and campus programmes.'),
  ],
  'plan_title': 'Feeding students well, on a student budget.',
  'plan': '''<p>Student events usually mean big appetites and a fixed budget. Rice dishes, curries and grills feed a crowd better than lots of small bites, and a vegetarian main makes sure everyone eats. Plan for walk-ins: free food at a campus event draws more people than the sign-up list.</p>
<p>Check your campus rules on outside catering and where food can be served, and book early for orientation weeks and graduation season, which are busy.</p>
<p>Students living in Academic City or Silicon Oasis can also get daily meals delivered: see <a href="/guides/student-meal-plans-dubai/">student meal plans in Dubai</a>.</p>''',
  'menu': [('Crowd-pleasers', ['Biryani and rice dishes', 'Curries and grills', 'Pasta bakes', 'Vegetarian mains']),
           ('Light events', ['Sandwiches and wraps', 'Savoury bites', 'Fruit']),
           ('Extras', ['Desserts', 'Tea, coffee and juices'])],
  'faqs': [
    ('Do you cater university events in Dubai Academic City?', 'Yes. We cater orientation days, society events, career fairs and campus functions, including in Dubai Academic City and Silicon Oasis.'),
    ('Can you cater a society iftar?', 'Yes. Tell us your headcount and the time of Maghrib at your campus, and we will plan delivery before iftar.'),
    ('Do you cater graduation parties?', 'Yes. We cater graduation celebrations for graduates and their families, on campus where allowed or at home.'),
    ('How should we plan for walk-ins?', 'Free food draws extra people, so add a buffer above your sign-up number. We can help you size it.'),
    ('Is your food halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
  'guides': ['/guides/how-much-food-per-person-catering/', '/guides/catering-cost-dubai/', '/guides/uae-event-catering-calendar/'],
 },
 # ------------------------------------------------ by occasion
 'iftar': {
  'kind': 'occasion', 'name': 'Iftar catering', 'short': 'Iftar and Ramadan', 'icon': 'moon', 'img': 1, 'form': 'Iftar or Ramadan event',
  'card': 'Corporate iftars, family iftars at home, majlis gatherings and bulk iftar meals.',
  'title': 'Iftar Catering in Dubai & the UAE | Ramadan | Messify',
  'desc': 'Ramadan iftar catering in Dubai and the UAE: corporate iftars, family iftars at home, majlis gatherings, ghabga and bulk iftar meals. 100% halal.',
  'kicker': 'Iftar catering · Ramadan', 'h1': 'Iftar catering, on the table before Maghrib.',
  'lede': "Corporate iftars, family iftars at home, majlis gatherings, ghabga nights and iftar meals for staff and communities. We cater Ramadan across the UAE with 100% halal menus, planned so everything is ready when it is time to break the fast.",
  'facts': [('Before', 'Maghrib, every time'), ('100%', 'halal menus'), ('5,000+', 'meals a day of capacity')],
  'offers': [
    ('case', 'Corporate iftars', 'Iftar for your team, clients or partners, at the office or a venue.'),
    ('home', 'Family iftars at home', 'A full iftar spread for family and friends, with a buffet setup if you want one.'),
    ('serve', 'Majlis gatherings', 'Iftar and evening platters for guests at your majlis.'),
    ('moon', 'Ghabga nights', 'Late-evening Ramadan gatherings for teams and families.'),
    ('box', 'Staff and community iftars', 'Bulk iftar meals for staff, sites and community iftars.'),
    ('cap', 'Society and campus iftars', 'Iftar for student societies and university events.'),
  ],
  'plan_title': 'Timing is everything at iftar.',
  'plan': '''<p>Iftar has a fixed moment, and it moves a minute or two earlier or later every day through Ramadan. Tell us the date and the venue, and we plan delivery so food is set up and ready before Maghrib, never arriving as guests are breaking their fast. Remember that roads are busiest in the hour before iftar.</p>
<p>Start light and build up: dates, water and laban to break the fast, then soup and savoury bites, then the main meal after Maghrib prayer, and sweets with tea and coffee to finish. For corporate iftars, many guests arrive straight from work, so plan for people coming in close to the time.</p>
<p>Ramadan 2027 is expected to begin around 8 February 2027, subject to the moon sighting. The weeks fill up quickly, so book early. Our <a href="/guides/corporate-iftar-planning/">guide to planning a corporate iftar</a> covers the details.</p>''',
  'menu': [('To break the fast', ['Dates, water and laban', 'Lentil soup or harees', 'Samosas, sambousek and savoury bites']),
           ('Main meal', ['Biryani, mandi, ouzi and rice dishes', 'Curries, grills and roasts', 'Salads and fattoush', 'Vegetarian mains']),
           ('To finish', ['Luqaimat, kunafa, umm ali and other sweets', 'Fruit', 'Arabic coffee, tea and juices'])],
  'faqs': [
    ('When should I book iftar catering?', 'As early as you can. Ramadan 2027 is expected to begin around 8 February 2027, subject to the moon sighting, and popular dates fill up quickly.'),
    ('Will the food arrive before iftar?', 'Yes. We plan delivery and setup so food is ready before Maghrib at your venue, allowing for the heavy traffic before iftar.'),
    ('Do you cater corporate iftars?', 'Yes. We cater iftars for teams, clients and partners, at your office or a venue, with buffet setups.'),
    ('Can you provide iftar meals for staff or a community iftar?', 'Yes. Our kitchen can produce 5,000+ meals a day, so we can supply bulk iftar meals. Tell us the headcount, location and dates.'),
    ('Is your food halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
  'guides': ['/guides/corporate-iftar-planning/', '/guides/how-much-food-per-person-catering/', '/guides/uae-event-catering-calendar/'],
 },
 'eid': {
  'kind': 'occasion', 'name': 'Eid catering', 'short': 'Eid', 'icon': 'star', 'img': 0, 'form': 'Eid',
  'card': 'Eid al-Fitr and Eid al-Adha family lunches, open houses and office celebrations.',
  'title': 'Eid Catering in Dubai & the UAE | Messify',
  'desc': 'Eid catering in Dubai and the UAE: Eid al-Fitr and Eid al-Adha family lunches, open houses and office Eid celebrations. 100% halal menus by headcount.',
  'kicker': 'Eid catering', 'h1': 'Eid catering for family, friends and the office.',
  'lede': "Eid al-Fitr or Eid al-Adha, a family lunch, an open house that runs all day, or an Eid celebration at the office. We cater Eid across the UAE with generous, 100% halal menus, so you can spend the day with your guests.",
  'facts': [('Both', 'Eid al-Fitr and Eid al-Adha'), ('100%', 'halal menus'), ('Buffet', 'setups at home or a venue')],
  'offers': [
    ('users', 'Eid family lunches', 'A full spread for the family on the first day of Eid.'),
    ('home', 'Eid open houses', 'Food that holds well while guests come and go all day.'),
    ('case', 'Office Eid celebrations', 'Eid lunches and sweets for your team before or after the holiday.'),
    ('serve', 'Majlis hospitality', 'Platters, sweets and coffee for visitors to your majlis.'),
    ('box', 'Staff Eid meals', 'Bulk festive meals for staff and sites.'),
    ('party', 'Eid parties', 'Evening celebrations for friends and extended family.'),
  ],
  'plan_title': 'Plan Eid early.',
  'plan': '''<p>Eid dates depend on the moon sighting, so families and caterers plan around a likely date and confirm a day or two before. Eid al-Fitr 2027 is expected around 9 or 10 March 2027, and Eid al-Adha 2027 around 16 or 17 May 2027. Because everyone celebrates at the same time, book early and confirm your final numbers as soon as the date is announced.</p>
<p>For an open house where guests come and go, choose dishes that hold well for hours, and plan the food to come out in batches rather than all at once. For a sit-down family lunch, tell us the time you want to eat.</p>
<p>See every key date in our <a href="/guides/uae-event-catering-calendar/">UAE event catering calendar</a>.</p>''',
  'menu': [('To start', ['Savoury bites and pastries', 'Salads, hummus and mezze']),
           ('Mains', ['Mandi, ouzi, biryani and machboos-style rice dishes', 'Grills and roasts', 'Curries', 'Vegetarian mains']),
           ('Sweets and drinks', ['Luqaimat, maamoul and Eid sweets', 'Fruit', 'Arabic coffee, tea and juices'])],
  'faqs': [
    ('When should I book Eid catering?', 'Early. Eid al-Fitr 2027 is expected around 9 or 10 March 2027 and Eid al-Adha 2027 around 16 or 17 May 2027, subject to the moon sighting, and everyone celebrates at once.'),
    ('What if the Eid date changes?', 'Book for the likely date and confirm your final numbers once the date is announced. Talk to us about timing when you book.'),
    ('Do you cater Eid open houses?', 'Yes. We plan dishes that hold well through the day, and can stagger the food so it comes out in batches.'),
    ('Do you cater office Eid celebrations?', 'Yes. We cater Eid lunches and celebrations for teams before or after the holiday.'),
    ('Is your food halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
  'guides': ['/guides/uae-event-catering-calendar/', '/guides/party-catering-at-home-dubai/', '/guides/how-much-food-per-person-catering/'],
 },
 'diwali': {
  'kind': 'occasion', 'name': 'Diwali catering', 'short': 'Diwali', 'icon': 'lamp', 'img': 2, 'form': 'Diwali',
  'card': 'Diwali parties at home, office Diwali celebrations and community gatherings.',
  'title': 'Diwali Catering in Dubai & the UAE | Messify',
  'desc': 'Diwali catering in Dubai and the UAE: Diwali parties at home, office celebrations and community gatherings, with vegetarian Indian menus and sweets.',
  'kicker': 'Diwali catering', 'h1': 'Diwali catering, with vegetarian menus at the centre.',
  'lede': "Diwali parties at home, office celebrations and community gatherings across the UAE. We build Diwali menus around vegetarian Indian dishes, with sweets and snacks to share, quoted by headcount and set up as a buffet if you want one.",
  'facts': [('Veg', 'Indian menus at the centre'), ('Custom', 'menus, by headcount'), ('Buffet', 'setups at home or a venue')],
  'offers': [
    ('lamp', 'Diwali parties at home', 'A full vegetarian spread for family and friends.'),
    ('case', 'Office Diwali celebrations', 'Diwali lunches and sweets for your team.'),
    ('users', 'Community gatherings', 'Larger menus for community and association events.'),
    ('serve', 'Buffet setups', 'Buffets laid out at your home or venue.'),
    ('star', 'Snacks and sweets', 'Savoury snacks and desserts for guests who come and go.'),
    ('party', 'Card parties and get-togethers', 'Evening bites and dinner for Diwali get-togethers.'),
  ],
  'plan_title': 'Planning food for Diwali.',
  'plan': '''<p>Diwali 2026 falls on Sunday 8 November, with Dhanteras on 6 November and Bhai Dooj on 10 November in the UAE. Many families host on the weekend around Diwali, so book as early as you can.</p>
<p>Most Diwali menus are vegetarian. <b>Please note:</b> our partner kitchen cooks both vegetarian and non-vegetarian food. If your guests need food cooked in a pure-vegetarian kitchen, or Jain food without onion and garlic, tell us in your enquiry and we will say upfront what we can and can't do.</p>
<p>Our <a href="/guides/diwali-party-food-planning/">guide to planning food for a Diwali party</a> covers menus, quantities and timing.</p>''',
  'menu': [('Snacks and starters', ['Samosas, pakoras and chaat-style bites', 'Paneer tikka', 'Dhokla and savoury snacks']),
           ('Mains', ['Paneer makhani and dal makhani', 'Chole, mixed vegetable curries', 'Biryani and pulao', 'Puri, naan and roti']),
           ('Sweets', ['Gulab jamun and Indian desserts', 'Kheer', 'Chai, juices and soft drinks'])],
  'faqs': [
    ('When is Diwali 2026 in the UAE?', 'Diwali (Lakshmi Puja) falls on Sunday 8 November 2026, with Dhanteras on 6 November and Bhai Dooj on 10 November in the UAE.'),
    ('Do you cater vegetarian Diwali menus?', 'Yes. We build Diwali menus around vegetarian Indian dishes, snacks and sweets.'),
    ('Is your kitchen pure vegetarian?', 'No. Our partner kitchen cooks both vegetarian and non-vegetarian food. If you need a pure-vegetarian kitchen or Jain food, tell us and we will tell you upfront what we can do.'),
    ('Do you cater office Diwali celebrations?', 'Yes. We cater Diwali lunches and celebrations for teams, with sweets and snacks to share.'),
    ('How much food do I need for a Diwali party?', 'For a full vegetarian meal, plan about 150 g of rice or biryani, 250 g of curries and dal, 2 breads, snacks and a dessert per adult. Our Diwali food guide has more detail.'),
  ],
  'guides': ['/guides/diwali-party-food-planning/', '/guides/how-much-food-per-person-catering/', '/guides/uae-event-catering-calendar/'],
 },
 'christmas-year-end-parties': {
  'kind': 'occasion', 'name': 'Christmas and year-end party catering', 'short': 'Christmas and year-end', 'icon': 'gift', 'img': 1, 'form': 'Christmas or year-end party',
  'card': 'Office year-end parties, Christmas lunches, festive dinners and New Year gatherings.',
  'title': 'Christmas & Year-End Party Catering in Dubai | Messify',
  'desc': 'Christmas and year-end party catering in Dubai and the UAE: office parties, festive lunches, Thanksgiving-style dinners and New Year gatherings. Halal menus.',
  'kicker': 'Christmas and year-end catering', 'h1': 'Year-end parties and festive menus.',
  'lede': "Office year-end parties, Christmas lunches, Thanksgiving-style dinners with friends and New Year gatherings. We cater the festive season across the UAE with custom 100% halal menus and buffet setups, quoted by headcount.",
  'facts': [('Nov–Jan', 'the festive season'), ('100%', 'halal menus'), ('Buffet', 'setups at your venue')],
  'offers': [
    ('gift', 'Office year-end parties', 'A festive buffet to thank your team for the year.'),
    ('home', 'Christmas lunches and dinners', 'Festive menus for family and friends at home.'),
    ('users', 'Thanksgiving and Friendsgiving', 'Roast-style dinners for expat friends and families in late November.'),
    ('star', 'New Year gatherings', 'Bites and buffets for New Year\'s Eve and New Year parties.'),
    ('case', 'Client appreciation events', 'End-of-year events for clients and partners.'),
    ('serve', 'Buffet setups', 'Festive buffets laid out at your office, home or venue.'),
  ],
  'plan_title': 'Book the festive season early.',
  'plan': '''<p>The festive season is the busiest time of year for events in the UAE: the cooler weather, year-end parties, National Day on 2 and 3 December, Christmas and New Year all fall within a few weeks. Office parties tend to cluster in the first three weeks of December, so book as soon as your date is set.</p>
<p>Our menus are 100% halal. For a festive feel, think roasts, Continental and Italian dishes alongside the Indian and Arabic favourites your team already loves, and finish with desserts. If you want a specific dish, such as a roast turkey for a Thanksgiving or Christmas dinner, ask in your enquiry and we will confirm what we can do.</p>
<p>Planning the office party? See our <a href="/guides/office-year-end-party-catering/">guide to catering an office year-end party</a>.</p>''',
  'menu': [('To start', ['Canapés and savoury bites', 'Soups and salads']),
           ('Festive mains', ['Roast chicken and roasts', 'Continental and Italian mains', 'Biryani, grills and curries', 'Vegetarian mains']),
           ('To finish', ['Festive desserts and sweet bites', 'Hot chocolate, tea, coffee and juices'])],
  'faqs': [
    ('When should we book a year-end office party?', 'As soon as your date is set. December is the busiest month for events in the UAE, and the first three weeks fill up first.'),
    ('Is your Christmas menu halal?', 'Yes. All our catering menus are 100% halal.'),
    ('Can you cater a Thanksgiving dinner?', 'Yes, we cater Thanksgiving-style dinners. If you want a specific dish such as roast turkey, ask in your enquiry and we will confirm.'),
    ('Do you cater New Year parties?', 'Yes. We cater New Year gatherings at homes and venues. Tell us your timing early, because the night is in high demand.'),
    ('How much food do we need for an office party?', 'For a full buffet, plan about 150 g of rice, 175 g of mains, 100 g of vegetable dishes, a salad and a dessert per guest. For a drinks-and-bites party, around 10 to 12 bites per guest.'),
  ],
  'guides': ['/guides/office-year-end-party-catering/', '/guides/uae-event-catering-calendar/', '/guides/how-much-food-per-person-catering/'],
 },
 'national-day': {
  'kind': 'occasion', 'name': 'UAE National Day catering', 'short': 'National Day', 'icon': 'flag', 'img': 0, 'form': 'National Day',
  'card': 'Eid Al Etihad celebrations for offices, schools, communities and families.',
  'title': 'UAE National Day Catering (Eid Al Etihad) | Messify',
  'desc': 'UAE National Day (Eid Al Etihad) catering for office celebrations, community events and family gatherings, with Emirati-inspired, 100% halal menus.',
  'kicker': 'UAE National Day catering', 'h1': 'Catering for Eid Al Etihad celebrations.',
  'lede': "Office celebrations, community events and family gatherings for UAE National Day. We cater Eid Al Etihad across the UAE with Arabic and Emirati-inspired menus, 100% halal, quoted by headcount.",
  'facts': [('2–3 Dec', 'Eid Al Etihad 2026 holiday'), ('100%', 'halal menus'), ('Buffet', 'setups at your venue')],
  'offers': [
    ('flag', 'Office celebrations', 'National Day lunches for teams, usually in the days before the holiday.'),
    ('users', 'Community events', 'Food for community and residents\' celebrations.'),
    ('home', 'Family gatherings', 'National Day lunches and dinners at home.'),
    ('cap', 'Campus celebrations', 'Food for university National Day events.'),
    ('serve', 'Majlis hospitality', 'Arabic coffee, dates and platters for guests.'),
    ('box', 'Staff meals', 'Bulk festive meals for staff and sites.'),
  ],
  'plan_title': 'National Day falls in the busiest weeks.',
  'plan': '''<p>The Eid Al Etihad public holiday in 2026 is on 2 and 3 December. Offices usually celebrate in the last working days before the holiday, which overlaps with the start of year-end party season, so book early.</p>
<p>Arabic coffee and dates for guests, a generous rice dish at the centre, grills and salads, and luqaimat to finish make a classic National Day spread. Tell us whether you want an Emirati-inspired menu, a mix of cuisines that reflects your team, or both.</p>
<p>See every key date in our <a href="/guides/uae-event-catering-calendar/">UAE event catering calendar</a>.</p>''',
  'menu': [('Welcome', ['Arabic coffee and dates', 'Savoury bites and sambousek']),
           ('Mains', ['Machboos, mandi and rice dishes', 'Grills and roasts', 'Salads and mezze', 'Vegetarian mains']),
           ('To finish', ['Luqaimat and Arabic sweets', 'Fruit', 'Karak tea, juices and soft drinks'])],
  'faqs': [
    ('When is UAE National Day 2026?', 'The Eid Al Etihad public holiday in 2026 is on 2 and 3 December.'),
    ('When do offices hold National Day celebrations?', 'Usually in the last working days before the holiday. Book early, because those days overlap with year-end party season.'),
    ('Can you cater an Emirati-inspired menu?', 'Yes. We build Arabic and Emirati-inspired menus, and can mix in other cuisines to suit your guests.'),
    ('Do you cater community and school events?', 'We cater community and campus events where outside catering is allowed. Tell us the venue and headcount.'),
    ('Is your food halal?', 'Yes. All our catering menus are 100% halal.'),
  ],
  'guides': ['/guides/uae-event-catering-calendar/', '/guides/corporate-event-catering-checklist/', '/guides/how-much-food-per-person-catering/'],
 },
}

def type_cards(kind=None, exclude=None):
    def label(n):
        return n if n.split()[0] in ('Christmas', 'Eid', 'Diwali', 'UAE') else n[0].lower() + n[1:]
    out = ''.join(f'<a class="emirate" href="/catering/{slug}/"><span class="emirate__ico">{I[t["icon"]]}</span><h3 class="h3">{t["name"]}</h3><p>{t["card"]}</p><span class="link-arrow">See {label(t["name"])} {I["arrow"]}</span></a>'
                  for slug, t in CATER_TYPES.items() if (kind is None or t['kind'] == kind) and slug != exclude)
    if kind == 'occasion' and exclude is None:
        out += f'<a class="emirate" href="/guides/uae-event-catering-calendar/"><span class="emirate__ico">{I["clock"]}</span><h3 class="h3">UAE catering calendar</h3><p>Every key date for 2026–27, from Diwali to Eid al-Adha, and how early to book.</p><span class="link-arrow">See the calendar {I["arrow"]}</span></a>'
    return f'<div class="emirates">{out}</div>'

def page_cater_type(slug):
    t = CATER_TYPES[slug]
    path = f'/catering/{slug}/'
    cr, crs = crumbs([('Home', '/'), ('Catering', '/catering/'), (t['name'], path)])
    service = {'@type': 'Service', '@id': BASE + path + '#service', 'name': f'Messify {t["name"].lower()}', 'serviceType': t['name'],
               'description': t['desc'], 'provider': {'@id': BASE + '/#business'},
               'areaServed': [{'@type': 'AdministrativeArea', 'name': c} for c in CATER_EMIRATES]}
    page = {'path': path, 'mode': 'catering', 'nav': 'catering', 'title': t['title'], 'desc': t['desc'],
            'cta': ('#quote', 'Get a quote', 'Quote'), 'cta_bot': 'catering',
            'schema': [ORG, BUSINESS, service, faq_schema(t['faqs']), crs]}
    small, big, w, h, alt = CATER_IMGS[t['img']]
    srcset = f' srcset="/assets/img/{small} 640w, /assets/img/{big} {w}w" sizes="(min-width: 900px) 45vw, 100vw"' if small != big else ''
    facts = ''.join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in t['facts'])
    offers = ''.join(f'<div class="event">{I[i]}<h3 class="h3">{a}</h3><p>{d}</p></div>' for i, a, d in t['offers'])
    menu = ''.join(f'<div class="place-group"><h3>{g}</h3><ul>' + ''.join(f'<li>{I["tick"]}<span>{x}</span></li>' for x in items) + '</ul></div>' for g, items in t['menu'])
    guides = [g for g in CATERING_GUIDES if g[0] in t['guides']]
    wa = f'{WA}?text=' + quote(f"Hi Messify, I'd like a quote for {t['name'].lower()}.")
    other_kind = 'occasion' if t['kind'] == 'event' else 'event'
    body = f'''<section class="sec sec--first">
  <div class="wrap split">
    <div>
      {cr}
      <h1 class="h2 rise"><span class="kicker">{t['kicker']}</span> {t['h1']}</h1>
      <p class="lede rise">{t['lede']}</p>
      <div class="actions">
        <a class="btn" href="#quote" data-messibot="catering">Get a quote</a>
        <a class="btn btn--ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp us</a>
      </div>
      {rating_badge()}
      <div class="facts">{facts}</div>
    </div>
    <div class="photo photo--tall"><img src="/assets/img/{small}"{srcset} alt="{alt}" width="{w}" height="{h}" fetchpriority="high"></div>
  </div>
</section>

<section class="sec" style="padding-top:0" aria-labelledby="offers-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">What we cater</p><h2 class="h2" id="offers-title">{t['short']}, covered.</h2></div>
    <div class="events">{offers}</div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="plan-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Good to plan</p><h2 class="h2" id="plan-title">{t['plan_title']}</h2></div>
    <div class="prose">{t['plan']}</div>
  </div>
</section>

<section class="sec" aria-labelledby="menu-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Menu ideas</p><h2 class="h2" id="menu-title">Built around your guests.</h2>
      <p class="lede">Every menu is custom and 100% halal. These are starting points: tell us what you'd like and we'll confirm the menu in your quote.</p></div>
    <div class="places">{menu}</div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="faq-title">
  <div class="wrap split split--top">
    <div class="sec-head"><p class="eyebrow">Questions</p><h2 class="h2" id="faq-title">Good to know.</h2></div>
    {faq_html(t['faqs'])}
  </div>
</section>

<section class="sec" aria-labelledby="cguides-title">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Planning help</p><h2 class="h2" id="cguides-title">Before you book.</h2></div>
    {guide_cards(guides)}
  </div>
</section>

{catering_form(title="Tell us about your event.", event=t['form'])}

<section class="sec sec--tight" aria-labelledby="more-title">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:28px"><p class="eyebrow">More catering</p><h2 class="h3" id="more-title" style="font-size:1.4rem">{'Seasonal and festive catering' if other_kind == 'occasion' else 'Catering by event'}</h2></div>
    {type_cards(other_kind)}
    <div class="sec-head" style="margin:48px 0 28px"><p class="eyebrow">Across the UAE</p><h2 class="h3" style="font-size:1.4rem">Where we cater</h2></div>
    {emirate_cards()}
  </div>
</section>'''
    render(page, body)

# ---------------------------------------------------------------- technical files
def tech_files():
    urls = [('/', '1.0'), ('/meal-plans/', '0.9'), ('/meal-plans/academic-city/', '0.9'), ('/meal-plans/silicon-oasis/', '0.9'),
            ('/meal-plans/international-city/', '0.8'), ('/meal-plans/festival-city/', '0.9'), ('/guides/meal-delivery-dubai-festival-city/', '0.7'), ('/catering/', '0.9'), ('/guides/', '0.6'), ('/guides/best-meal-plans-dubai/', '0.8'), ('/guides/meal-plan-cost-dubai/', '0.8'), ('/guides/student-meal-plans-dubai/', '0.8'), ('/guides/weekly-vs-monthly-meal-plan/', '0.7'), ('/guides/office-lunch-delivery-silicon-oasis/', '0.7'), ('/about/', '0.6'), ('/terms/', '0.2'), ('/privacy/', '0.2'),
            ('/guides/affordable-meal-plans-dubai/', '0.7')] + [(f'/catering/{c}/', '0.8') for c in CATER_AREAS] + [(f'/catering/{c}/', '0.8') for c in CATER_TYPES] + [(p, '0.7') for p, _, _ in CATERING_GUIDES]
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
    cater_lines = '\n'.join(f'- [Catering in {c["name"]}]({BASE}/catering/{slug}/): {c["desc"]}' for slug, c in CATER_AREAS.items())
    type_lines = '\n'.join(f'- [{t["name"]}]({BASE}/catering/{slug}/): {t["desc"]}' for slug, t in CATER_TYPES.items())
    cguide_lines = '\n'.join(f'- [{t}]({BASE}{p}): {d}' for p, t, d in CATERING_GUIDES)
    plan_lines = '\n'.join(f'- {mlabel(m)}, {ln}: {aed(p)} ({t} meals, AED {per(p, t)} per meal)' for m, ln, t, p in PLANS)
    llms = f'''# Messify

> {ONE_LINER}

Messify sells daily meal plans through the Messify app. Each meal on a plan is a token: customers can skip a day and use the token later in their plan, or spend extra tokens to double up. All of the day's meals are delivered together every morning in one chilled bag. The menu changes daily, all meals are 100% halal, and there is a vegetarian option every day, for every meal. Monthly plans are 26 days of meals to use within 30 days; weekly plans are 7 days of meals to use within 9 days. Meal plan delivery covers Dubai Academic City, Dubai Silicon Oasis, International City and Dubai Festival City (DFC) only.

## Meal plan prices (AED)
{plan_lines}

## Key pages
- [Meal plans and prices]({BASE}/meal-plans/): plans, the token system, delivery and FAQs
- [Meal plans in Dubai Academic City]({BASE}/meal-plans/academic-city/): delivery to universities and student residences in DIAC, including KSK Homes and The Myriad
- [Meal plans in Dubai Silicon Oasis]({BASE}/meal-plans/silicon-oasis/): delivery to offices, residents, RIT Dubai and DSOA University Residence
- [Meal plans in International City]({BASE}/meal-plans/international-city/): where Messify meals are cooked
- [Meal plans in Dubai Festival City (DFC)]({BASE}/meal-plans/festival-city/): delivery to homes in Al Badia and offices across DFC
- [Catering]({BASE}/catering/): corporate, party and home events, university events, weddings, buffet setups and bulk catering across Dubai, Sharjah, Ajman, Abu Dhabi, Ras Al Khaimah and Umm Al Quwain
- [The best meal plans in Dubai, compared]({BASE}/guides/best-meal-plans-dubai/): Messify, Right Bite, Calo, Kcal, VMeals and Meals On Me with published prices
- [How much does a meal plan cost in Dubai?]({BASE}/guides/meal-plan-cost-dubai/): price per meal explained, with a meal plan vs ordering-in calculator
- [Student meal plans in Dubai]({BASE}/guides/student-meal-plans-dubai/): costs, delivery to Academic City and Silicon Oasis residences, exams
- [Weekly vs monthly meal plans]({BASE}/guides/weekly-vs-monthly-meal-plan/): price per meal and flexibility compared
- [Daily meal delivery in Dubai Festival City]({BASE}/guides/meal-delivery-dubai-festival-city/): meal plans for Al Badia homes and offices in DFC
- [Office lunch delivery in Dubai Silicon Oasis]({BASE}/guides/office-lunch-delivery-silicon-oasis/): morning delivery for offices in DSO, prices, team plans
- [Affordable meal plans in Dubai]({BASE}/guides/affordable-meal-plans-dubai/): price per meal, the lowest-cost plans and how to avoid waste
{cater_lines}
{type_lines}
{cguide_lines}
- [About Messify]({BASE}/about/): key facts in one table

## Contact
- Phone and WhatsApp: {PHONE_DISPLAY}
- Email: {EMAIL}
- Instagram: @messify.me
- Opening hours: every day, 8 AM to 11 PM (Gulf Standard Time)
- Google rating: {RATING} out of 5 on Google reviews ({GMAPS})
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
    page_guides(); page_guide_best(); page_guide_cost(); page_guide_students(); page_guide_weekly_monthly(); page_guide_office_dso(); page_guide_dfc(); page_guide_affordable()
    page_guide_food_per_person(); page_guide_catering_cost(); page_guide_corporate_checklist(); page_guide_home_party(); page_guide_styles(); page_guide_wedding()
    for s in CATER_AREAS: page_cater_area(s)
    page_guide_calendar(); page_guide_corporate_iftar(); page_guide_diwali(); page_guide_year_end()
    for s in CATER_TYPES: page_cater_type(s)
    page_start(); page_catering(); page_about(); page_terms(); page_privacy(); page_404(); tech_files()

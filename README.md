# Messify website

The Messify website (www.messify.me): 10 pages, hosted on Netlify, published automatically from this GitHub repository.

```
build.py                 the generator that writes every page
dist/                    the finished website (this is what Netlify publishes)
  index.html             Home (split meal plans / catering screen)
  meal-plans/            Meal plans and prices
    academic-city/       Meal plans in Dubai Academic City
    silicon-oasis/       Meal plans in Dubai Silicon Oasis
    international-city/  Meal plans in International City
  catering/              Catering (includes party, buffet and home events)
  start/                 Start page: app or WhatsApp (hidden from Google)
  about/                 Messify at a glance (key facts for Google and AI assistants)
  terms/                 Terms and conditions
  privacy/               Privacy notice
  404.html               Page not found
  _redirects             sends the old Wix addresses to the new pages
  sitemap.xml, robots.txt, llms.txt, site.webmanifest
  assets/                styles, script and images
netlify.toml             Netlify settings (publish dist/, caching)
GOOGLE-BUSINESS-PROFILE.md   step-by-step Google Business Profile setup
```

## How changes go live

Every change saved (committed) to the `main` branch of this repository is published by Netlify within about a minute.

- **Easiest:** open Claude, attach this repository and describe the change ("change the monthly 2-meal price to AED 1,450"). Claude edits `build.py`, rebuilds and commits.
- **Small text fix:** edit the HTML file inside `dist/` directly on github.com and commit. Note that the next run of `build.py` overwrites `dist/` pages, so make the same change in `build.py` too (or ask Claude to).
- **Prices** live in one place: the `PLANS` list at the top of `build.py`. Running `python3 build.py` updates every page and the website script.
- **Photos:** replace a file in `dist/assets/img/` with one of the same name and size ratio.

## Messibot (chat assistant)

`dist/assets/js/messibot.js` is a scripted chat assistant (no AI, no server), loaded on every page. Any link or button with `data-messibot="meals"` or `data-messibot="catering"` opens it. Prices, areas and answers live in the `CONFIG` and `FAQ` blocks inside that file. Its lead summaries are emailed to info@messify.me through FormSubmit.

## Contact forms

Both forms (meal plans and catering) email **info@messify.me** through FormSubmit, a free form service.

1. After the site is live, fill in either form once yourself.
2. FormSubmit sends an **activation email** to info@messify.me. Click the link in it.
3. From then on, every enquiry arrives in that inbox.

Until it's activated, or if sending ever fails, the form offers the customer a "Send it on WhatsApp" button with their details already filled in.

## Domain (GoDaddy)

The domain is registered at GoDaddy and email runs on Google Workspace. In GoDaddy DNS only two records point to the website: the **A** record for `@` and the **CNAME** for `www`. Never change the **MX** or **TXT** records: they run email and Google verification.

## Tell Google and Bing about the site

1. **Google Search Console** (search.google.com/search-console): add `https://www.messify.me`, verify with DNS, then submit `sitemap.xml` under **Sitemaps**.
2. **URL Inspection → Request indexing** for `/`, `/meal-plans/`, `/meal-plans/silicon-oasis/`, `/meal-plans/academic-city/`, `/catering/`.
3. **Bing Webmaster Tools**: "Import from Google Search Console". Bing also feeds ChatGPT search and Copilot.
4. Check the structured data at **search.google.com/test/rich-results**.
5. Update the **privacy policy link** in App Store Connect and Google Play Console to `https://www.messify.me/privacy/` (the old Wix address redirects, but the direct link is cleaner).

## What's built in for search and AI assistants

- A page per search target: meal plans Dubai, Academic City, Silicon Oasis, International City, catering (corporate, party, wedding, buffet).
- Real local detail: University of Birmingham Dubai, Middlesex University Dubai, Manipal, BITS Pilani, Amity, Curtin, KSK Homes, The Myriad, RIT Dubai, DSOA University Residence.
- Structured data on every page: business details, opening hours, all six plan prices, FAQs, breadcrumbs, app store links.
- "Quick answer" boxes and an About page with key facts AI assistants can quote.
- `robots.txt` welcomes ChatGPT, Claude, Perplexity, Gemini, Apple, Bing and Meta crawlers; `llms.txt` summarises Messify for AI tools.
- Old Wix addresses (/terms-and-conditions, /privacy-policy, /about-us, /faqs) redirect permanently to the new pages, so existing Google ranking carries over.
- Google Analytics (G-KNKHKG7LR2) with events for WhatsApp, phone, app store and "Start my plan" clicks and form enquiries (`generate_lead`). Mark `generate_lead` and `app_store_click` as key events in Google Analytics.

## Still to do

1. **Replace the catering photos** (cat-chef, cat-serving, cat-canapes, cat-buffet in `dist/assets/img/`) with photos from your own events. They currently look like other caterers' images.
2. **Replace the two AI-made images** (`bag-sofa.webp`, `fresh-chill.webp`) with real shoots.

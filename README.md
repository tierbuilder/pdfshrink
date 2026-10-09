# PDF Shrink — private, in-browser PDF & image tools

A static site (no backend) of PDF and image tools that run **entirely in the browser**: compress PDF (to an exact
size), resize image to KB (with exact dimensions), merge PDF, split PDF, JPG→PDF and PDF→JPG. It costs nothing to run at any traffic
level, because every visitor's own device does the work. The build generates 25 pages targeting specific searches,
with structured data and files for AI crawlers.

The build now generates 42 pages: 6 tools, 7 "resize image to X KB" pages, 11 "compress PDF to X" pages,
use-case, device and guide pages, plus the about, contact and legal pages.

## Quick start

```bash
python3 build.py            # → dist/
python3 -m http.server 8099 --directory dist
```

Set your real domain before deploying (it's used in canonicals, sitemap, OG tags, llms.txt):

```bash
SITE_URL=https://yourdomain.com SITE_NAME="PDF Shrink" CONTACT_EMAIL=hello@yourdomain.com python3 build.py
```

Optional env vars: `PLAUSIBLE_DOMAIN`, `CF_BEACON_TOKEN` (Cloudflare Web Analytics), `GOOGLE_VERIFY`, `BING_VERIFY`.

## Deploy (pick one, ~2 minutes)

| Host | Command / step | Notes |
|---|---|---|
| **Cloudflare Pages** (recommended) | `npx wrangler pages deploy dist --project-name pdfshrink` | Free unlimited bandwidth; reads `dist/_headers` |
| Netlify | drag `dist/` onto app.netlify.com/drop | reads `_headers` |
| Vercel | `cd dist && npx vercel --prod` | reads `vercel.json` |

The site must be served from the domain root (paths like `/vendor/` are absolute).

After deploying:
1. Add the domain to **Google Search Console** and **Bing Webmaster Tools**, then submit `/sitemap.xml`.
   Bing powers ChatGPT search and Copilot, so don't skip it.
2. Turn on **IndexNow** in Cloudflare (Caching → Configuration → Crawler Hints) so Bing and Yandex pick up changes fast.

## Compliance checklist

| Area | What's in place | Before going live |
|---|---|---|
| **Privacy (GDPR / UK GDPR / CCPA / India DPDP 2023)** | Files never leave the device. No cookies. `/privacy/` covers server logs, cookie-less analytics, legal basis, user rights, a grievance contact, children, and ads | Set `CONTACT_EMAIL`. If you enable analytics, use cookie-less Plausible or Cloudflare Web Analytics, so no consent banner is needed |
| **Ads (if added later)** | The policy says no ads and promises an update first | AdSense needs a Google-certified consent platform for EEA/UK/CH visitors. Update `/privacy/` and add the ad domains to the CSP in `build.py` |
| **Terms** | `/terms/`: as-is with no warranty, acceptable use (no forgery or bypassing protection), trademark notice, not affiliated with any government or exam body | — |
| **Open-source licenses** | `/licenses/` plus full texts in `/vendor/licenses/`. pdf.js (Apache-2.0) is unmodified; JSZip is used under MIT | Keep the texts if you upgrade the libraries |
| **Accessibility (WCAG 2.1 AA)** | Skip link, keyboard-operable drop zones, live regions, visible focus, reduced-motion support, AA contrast in both themes. axe-core reports 0 violations on the audited pages. `/accessibility/` statement | Recheck with axe after any design change |
| **Security** | Strict CSP (`default-src 'self'`, no inline scripts), nosniff, referrer policy, no framing. Verified the tools run under the CSP with 0 violations | — |
| **Search engine rules** | Every page has unique content (its own use case, tips and FAQ). No fake reviews or ratings in structured data. Brands are named only to describe compatibility | Don't mass-produce near-duplicate pages. Add pages only when they have something distinct to say |
| **Required site pages (AdSense, app stores)** | `/about/`, `/contact/`, `/privacy/`, `/terms/` | Use a real, monitored contact email |
| **Size accuracy** | Targets count 1 KB as 1000 bytes, so output passes portals that use either 1000 or 1024 | — |

## How compression works

`static/engine.js`:
1. **Cleanup (lossless):** removes XMP metadata, thumbnails and PieceInfo, garbage-collects unreachable objects,
   deflates uncompressed streams, and saves with object streams.
2. **Images:** decodes JPEG and 8-bit RGB/gray Flate images (including ASCII85/Hex chains and PNG predictors),
   downscales them, and re-encodes them as JPEG. Text, fonts, links and forms are left as they are.
3. **Exact size:** binary search over an 8-step quality ladder. If no step fits, it renders the pages with pdf.js
   and searches DPI and quality. It never returns a file bigger than the original.

Test results from local runs: a 2.43 MB photo PDF went to 287 KB on Recommended and to 76 KB with a 100 KB target,
with text still selectable. A 28 KB text PDF went to 3 KB with lossless cleanup.

## Project layout

```
build.py          site generator (templates, JSON-LD, sitemap, robots, llms.txt, PWA, headers, icons)
content.py        all page copy — add pages here
static/engine.js  compression engine
static/app.js     UI
static/style.css  styles (light/dark)
static/vendor/    pdf-lib, pdf.js, pako, jszip (self-hosted, so there's no CDN dependency)
testpdfs/         sample PDFs for manual testing
```

---

## Market research: what competitors do and what they lack

| | iLovePDF / Smallpdf / Adobe (leaders) | What we do |
|---|---|---|
| Upload | Every file goes to their servers | Never uploaded; this is the headline |
| Free limits | Smallpdf: 2 tasks/day; iLovePDF: 25 MB cap and roughly 1 task/hour | Unlimited |
| Exact size ("to 100 KB") | They rank for these pages, but the tool is a fixed preset that often misses the target | Real target search with a hit/miss result |
| Text after compression | Strong modes often turn pages into images | Images only, text kept |
| Batch | Limited or paid | Free batch plus ZIP |
| Offline | No | PWA, installable |
| Ads and pop-ups | Upsell modals and sign-up walls | None |

Newer client-side competitors exist (BentoPDF, MiOffice), so privacy alone isn't enough of a moat. Win on
**exact size + keeps text + speed + content depth**.

## Traffic playbook (in priority order)

1. **Size-specific pages = the biggest search demand.** "compress pdf to 100kb / 200kb / 50kb / 1mb" are huge
   queries, especially in India: government exams, jobs, scholarships, passport and visa forms. 11 are built.
   Next to add: 10kb, 30kb, 40kb, 250kb, 400kb, 3mb, 15mb, 20mb.
2. **Languages.** iLovePDF gets much of its traffic from 25+ languages. Add `/hi/`, `/es/`, `/pt/`, `/id/`, `/fr/`,
   `/de/`, `/ar/` versions of the home page and the top size pages, with `hreflang`. Hindi and Indonesian are
   underserved. (content.py is already a data structure, so this is a loop.)
3. **Sibling tools on the same engine** (each one is a new set of keywords): merge PDF, split PDF, PDF→JPG,
   JPG→PDF, "resize image to 20 KB / 50 KB" (very large demand on the same Indian form portals), and remove PDF
   password (owner password only).
4. **AI assistants (GEO).** Already done: static HTML that crawlers can read without running JS, "Key facts" blocks,
   FAQ/HowTo/WebApplication schema, `llms.txt` + `llms-full.txt`, and a robots.txt that welcomes GPTBot, ClaudeBot,
   PerplexityBot and others. Next: get mentioned on Reddit, Quora and listicles ("best free PDF compressor 2026").
   AI answers draw heavily on those sources.
5. **Launch:** Product Hunt, Hacker News ("Show HN: PDF compressor that never uploads your file"), r/privacy,
   r/selfhosted, r/india, r/IndianStudents, AlternativeTo (list it as an alternative to Smallpdf and iLovePDF).
   These also bring the first backlinks.
6. **Growth loop:** the "Share this free tool" button appears after success. Consider an embeddable widget
   (`<iframe>`) for bloggers. Every embed is a backlink.
7. **Monetize later** with one non-intrusive ad below the tool or a "Pro" desktop app. Keep the tool itself free
   and unlimited, because that's the moat.

Measure with Search Console. Expect size pages to start ranking in 4–12 weeks. Domain age and backlinks are the
bottleneck, not on-page SEO.

## Usage analytics (Cloudflare)

- `worker/index.js` runs only for `/api/*`; every page and file is served straight from `dist/` as a static asset.
- The tools send anonymous events (`compressed`, `image_resized`, `merged`, …) to `POST /api/event`. They go to
  Workers Analytics Engine (dataset `pdfshrink`, kept about 3 months) and to Workers Logs. No files, file
  names or IP addresses are sent. Do-Not-Track and Global Privacy Control are honoured, and nothing is sent from
  localhost.
- To read the stats:
  `CF_ACCOUNT_ID=... CF_API_TOKEN=... python3 scripts/stats.py 7`
  The token needs **Account Analytics: Read**.
- Visit counts come from Cloudflare Web Analytics: Worker → Metrics → enable.

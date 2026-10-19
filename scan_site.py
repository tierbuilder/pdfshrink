"""Standalone "make it look scanned" website, built from the same engine as PDF Shrink.

    python3 build.py --site scan          # → dist-scan/

Env: SCAN_SITE_URL (default https://scan.gumber.ai), SCAN_SITE_NAME (default ScanEffect), CONTACT_EMAIL.
Deployed as a separate Cloudflare Worker: npx wrangler deploy -c wrangler.scan.jsonc
The copy here is deliberately different from PDF Shrink's /make-pdf-look-scanned/ page so search engines
don't treat the two sites as duplicates."""
import hashlib
import html
import json
import os
import shutil
from datetime import date
from pathlib import Path

from tools_html import scan_tool

ROOT = Path(__file__).parent
STATIC = ROOT / "static"
DIST = ROOT / "dist-scan"
SITE_URL = os.environ.get("SCAN_SITE_URL", "https://scan.gumber.ai").rstrip("/")
SITE_NAME = os.environ.get("SCAN_SITE_NAME", "ScanEffect")
SISTER_URL = os.environ.get("SITE_URL", "https://pdfshrink.gumber.ai").rstrip("/")
CONTACT = os.environ.get("CONTACT_EMAIL", "online@gumber.ai")
UPDATED = os.environ.get("UPDATED", date.today().isoformat())
e = html.escape

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#1f5fd1"/>'
        '<rect x="8" y="6" width="16" height="20" rx="2" fill="#fff"/>'
        '<path d="M11 11h10M11 14h10M11 17h7" stroke="#1f5fd1" stroke-width="1.6" stroke-linecap="round"/>'
        '<rect x="4" y="19" width="24" height="3" rx="1.5" fill="#7fb0ff"/></svg>')
# Own accent colour (blue) so it reads as a separate product; contrast-checked like the main site.
BRAND_CSS = """:root{--accent:#1d4fb8;--accent-soft:#e8effc;--accent-glow:rgba(31,95,209,.16);--grad:linear-gradient(135deg,#2563d9 0%,#1a46a8 100%)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--accent:#7fb0ff;--accent-ink:#0b0d12;--accent-soft:#14213a;--accent-glow:rgba(127,176,255,.18);--grad:linear-gradient(135deg,#8ab8ff 0%,#5b97ff 100%)}}
:root[data-theme="dark"]{--accent:#7fb0ff;--accent-ink:#0b0d12;--accent-soft:#14213a;--accent-glow:rgba(127,176,255,.18);--grad:linear-gradient(135deg,#8ab8ff 0%,#5b97ff 100%)}
.brand svg{box-shadow:0 4px 12px -4px rgba(31,95,209,.6)}
.drop-title .link,.btn{box-shadow:0 8px 20px -10px rgba(31,95,209,.8)}
.sister{font-size:14px;font-weight:600;text-decoration:none;color:var(--muted);padding:7px 12px;border-radius:999px}
.sister:hover{color:var(--ink);background:var(--bg-2)}
@media (max-width:600px){.sister{display:none}}
"""

HOME = dict(
    path="", title="Make Documents Look Scanned — Free Scanner Effect for PDF",
    desc="Turn any PDF or photo into a realistic scanned document: paper texture, tilt, grain, grayscale or photocopy look. Live preview, runs in your browser, nothing uploaded.",
    h1="Make any document look scanned",
    lead="No printer, no scanner. Drop a PDF or photos and get a convincing scanned copy in seconds — styled exactly how you want, right in your browser.",
    tool=True,
    body=f"""
<section><h2>Scanner realism, without the scanner</h2>
<div class="grid">
<div class="card"><h3>Every page is different</h3><p>Real scans aren't perfectly straight. Each page gets its own tiny tilt, grain pattern and edge shadow.</p></div>
<div class="card"><h3>Preview = download</h3><p>The preview uses the same random seed as the export, so the file looks exactly like what you approved.</p></div>
<div class="card"><h3>Five looks</h3><p>Natural flatbed, office photocopier, old fax, phone-app scan, or a clean colour scan.</p></div>
<div class="card"><h3>Private by design</h3><p>Pages are rendered and processed on your device. Nothing is uploaded — it even works offline once loaded.</p></div>
</div></section>
<section class="prose"><h2>Common reasons people use it</h2>
<ul><li>A form or office asks for a “scanned copy”, but you signed the document digitally.</li>
<li>You only have the digital original and no scanner nearby.</li>
<li>You want a consistent, print-like look across a bundle of documents and photos.</li></ul>
<h2>Good to know</h2>
<p>A scanned-look PDF is made of page images, so its text can't be selected or searched — keep your original file.
It changes how a document looks, not what it is: please don't use it to misrepresent where a document came from,
and follow the rules of whoever you send it to.</p>
<p>Need to shrink the result, merge it with other files or sign it first? Try the free tools at
<a href="{SISTER_URL}/">PDF Shrink</a>.</p></section>""",
    faqs=[("Is it free?", "Yes — free, no sign-up, no watermark and no page limits."),
          ("Does my file get uploaded?", "No. Everything happens in your browser; the document never leaves your device."),
          ("Which files can I use?", "PDFs and images (JPG, PNG, WebP). Each image becomes one page of the output PDF."),
          ("How do I make it look less perfect?", "Raise Tilt, Grain and Paper texture, or pick the Old fax style. Use 🎲 Re-roll for a different random tilt."),
          ("How big will the file be?", "Roughly 50–250 KB per page at 150 DPI depending on how much is on the page. Choose “Small” file size or 110 DPI for less."),
          ("Does it work on my phone?", "Yes, in any modern mobile browser — no app needed.")],
)
PRIVACY = dict(path="privacy", title="Privacy", desc=f"{SITE_NAME} processes files in your browser and never uploads them.",
               h1="Privacy", lead="Your documents never leave your device.", tool=False, faqs=[],
               body=f"""<section class="prose">
<h2>Files</h2><p>Documents you choose are read and processed entirely inside your browser and offered back to you as a
download. They are never uploaded to us or anyone else. Closing the tab discards them.</p>
<h2>Usage counts</h2><p>We may count anonymous, cookie-less events (for example “a document was converted”, the style
and page count) to improve the tool. No files, file names or IP addresses are stored. Do-Not-Track and Global Privacy
Control are honoured. Our hosting provider (a CDN) processes standard request logs to deliver the site.</p>
<h2>Cookies</h2><p>None. Your light/dark choice is kept in your browser's local storage.</p>
<h2>Your rights</h2><p>For requests under the GDPR, UK GDPR, CCPA/CPRA or India's DPDP Act 2023, contact
<a href="mailto:{e(CONTACT)}">{e(CONTACT)}</a>.</p></section>""")
TERMS = dict(path="terms", title="Terms of use", desc=f"Terms of use for {SITE_NAME}.", h1="Terms of use",
             lead="Plain-language terms. By using the site you agree to them.", tool=False, faqs=[],
             body=f"""<section class="prose" id="disclaimer">
<h2>Hobby project — no warranty</h2><p>{e(SITE_NAME)} is a personal hobby project, provided free and “as is”, without
warranty of any kind, express or implied. You use it at your own risk; always check the result and keep your original
file. To the extent permitted by law, the author is not liable for any loss arising from its use.</p>
<h2>Acceptable use</h2><p>Use the tool only with documents you are entitled to use. Do not use it to forge documents,
to misrepresent a document's origin where that matters, or for any unlawful purpose.</p>
<h2>Open-source software</h2><p>Built with pdf.js (Apache-2.0), pdf-lib (MIT) and pako (MIT); full license texts are in
<a href="/vendor/licenses/">/vendor/licenses/</a>.</p>
<h2>Contact</h2><p><a href="mailto:{e(CONTACT)}">{e(CONTACT)}</a></p></section>""")


def fingerprint(src, name):
    h = hashlib.sha256(src.read_bytes()).hexdigest()[:10]
    stem, ext = name.rsplit(".", 1)
    (DIST / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(src, DIST / "assets" / f"{stem}.{h}.{ext}")
    return f"/assets/{stem}.{h}.{ext}"


def page_html(p, assets):
    url = f"{SITE_URL}/{p['path']}/" if p["path"] else f"{SITE_URL}/"
    graph = [{"@type": "WebPage", "url": url, "name": p["title"], "description": p["desc"], "dateModified": UPDATED}]
    if p["tool"]:
        graph += [{"@type": "WebApplication", "name": SITE_NAME, "url": url, "applicationCategory": "UtilitiesApplication",
                   "operatingSystem": "Any (web browser)", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                   "isAccessibleForFree": True},
                  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                                      for q, a in p["faqs"]]}]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    faqs = ""
    if p["faqs"]:
        faqs = '<section class="faq"><h2>Questions</h2>' + "".join(
            f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faqs"]) + "</section>"
    tool = scan_tool() if p["tool"] else ""
    scripts = (f'<script src="{assets["engine"]}" defer></script><script src="{assets["scan"]}" defer></script>' if p["tool"] else "")
    badges = ('<ul class="badges"><li>🔒 No upload</li><li>👁 Live preview</li><li>🎲 Natural randomness</li><li>✓ Free, no sign-up</li></ul>'
              if p["tool"] else "")
    theme = ('<button type="button" class="theme-btn" id="theme-toggle" data-mode="auto" data-label-auto="Theme: system" '
             'data-label-light="Theme: light" data-label-dark="Theme: dark" aria-label="Theme: system" title="Theme: system">'
             '<svg class="i-auto" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>'
             '<svg class="i-light" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="currentColor"/><path d="M12 1.5v3M12 19.5v3M1.5 12h3M19.5 12h3M4.6 4.6l2.1 2.1M17.3 17.3l2.1 2.1M4.6 19.4l2.1-2.1M17.3 6.7l2.1-2.1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
             '<svg class="i-dark" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11z" fill="currentColor"/></svg>'
             '<span class="theme-text">Theme: system</span></button>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1f5fd1">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(SITE_NAME)}">
<meta property="og:title" content="{e(p["title"])}"><meta property="og:description" content="{e(p["desc"])}"><meta property="og:url" content="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script src="{assets["theme"]}"></script>
<link rel="stylesheet" href="{assets["css"]}">
<link rel="stylesheet" href="{assets["brand"]}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap"><a class="brand" href="/">{LOGO}{e(SITE_NAME)}</a>
<div class="hdr-tools"><a class="sister" href="{SISTER_URL}/">More free PDF tools ↗</a>{theme}</div></div></header>
<main class="wrap" id="main">
<div class="hero"><h1>{e(p["h1"])}</h1><p class="lead">{e(p["lead"])}</p>{badges}</div>
{tool}
{p["body"]}
{faqs}
<p class="updated">Last updated <time datetime="{UPDATED}">{UPDATED}</time></p>
</main>
<footer class="site"><div class="wrap"><div class="cols">
<div><h4>{e(SITE_NAME)}</h4><a href="/">Make it look scanned</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="mailto:{e(CONTACT)}">Contact</a></div>
<div><h4>Free PDF tools</h4><a href="{SISTER_URL}/">Compress PDF</a><a href="{SISTER_URL}/compress-pdf-to-100kb/">PDF to 100 KB</a><a href="{SISTER_URL}/merge-pdf/">Merge PDF</a><a href="{SISTER_URL}/sign-pdf/">Sign PDF</a></div>
</div><p>© {date.today().year} {e(SITE_NAME)} · Runs in your browser — your files never leave your device.</p>
<p class="small"><strong>Disclaimer:</strong> {e(SITE_NAME)} is a personal hobby project, provided free and “as is”, without warranty of any kind. <a href="/terms/#disclaimer" style="display:inline">Terms</a>.</p></div></footer>
<div id="toast" role="status" hidden></div>
{scripts}
</body>
</html>
"""


def build(csp_extra_src="", csp_extra_conn=""):
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    (DIST / "vendor" / "licenses").mkdir(parents=True)
    for f in ("pdf-lib.min.js", "pako.min.js", "pdf.min.js", "pdf.worker.min.js"):
        shutil.copy(STATIC / "vendor" / f, DIST / "vendor" / f)
    for f in ("pdf-lib-LICENSE.txt", "pako-LICENSE.txt", "pdfjs-LICENSE.txt"):
        shutil.copy(STATIC / "vendor" / "licenses" / f, DIST / "vendor" / "licenses" / f)
    (DIST / "vendor" / "licenses" / "index.html").write_text(
        "<!doctype html><meta charset=utf-8><title>Licenses</title><ul>" +
        "".join(f'<li><a href="{f}">{f}</a></li>' for f in ("pdfjs-LICENSE.txt", "pdf-lib-LICENSE.txt", "pako-LICENSE.txt")) + "</ul>")
    brand = DIST / "brand.css"
    brand.write_text(BRAND_CSS)
    assets = {"css": fingerprint(STATIC / "style.css", "style.css"), "theme": fingerprint(STATIC / "theme.js", "theme.js"),
              "engine": fingerprint(STATIC / "engine.js", "engine.js"), "scan": fingerprint(STATIC / "scan.js", "scan.js"),
              "brand": fingerprint(brand, "brand.css")}
    brand.unlink()
    pages = [HOME, PRIVACY, TERMS]
    for p in pages:
        out = DIST / p["path"] / "index.html" if p["path"] else DIST / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page_html(p, assets), encoding="utf-8")
    nf = dict(path="404", title="Page not found", desc="Page not found.", h1="Page not found", lead="That page doesn't exist — but the scanner effect does.",
              tool=False, faqs=[], body='<p class="prose"><a href="/">Make a document look scanned →</a></p>')
    (DIST / "404.html").write_text(page_html(nf, assets).replace('content="index,follow,max-image-preview:large"', 'content="noindex"'))
    (DIST / "favicon.svg").write_text(LOGO.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" '))
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{SITE_URL}/{p['path'] + '/' if p['path'] else ''}</loc><lastmod>{UPDATED}</lastmod></url>\n" for p in pages) + "</urlset>\n")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    (DIST / "llms.txt").write_text(f"# {SITE_NAME}\n\n> {HOME['desc']}\n\n- [{HOME['h1']}]({SITE_URL}/): free, in-browser, no upload.\n"
                                   f"- Sister site with more PDF tools: [PDF Shrink]({SISTER_URL}/)\n")
    csp = ("default-src 'self'; script-src 'self' 'wasm-unsafe-eval' https://static.cloudflareinsights.com" + csp_extra_src +
           "; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; worker-src 'self' blob:; "
           "connect-src 'self' blob: data: https://cloudflareinsights.com" + csp_extra_conn +
           "; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'")
    (DIST / "_headers").write_text(f"/*\n  Content-Security-Policy: {csp}\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
                                   "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/vendor/*\n  Cache-Control: public, max-age=2592000\n")
    (DIST / ".assetsignore").write_text(".assetsignore\n")
    print(f"Built {SITE_NAME}: {len(pages)} pages → {DIST}  (SITE_URL={SITE_URL})")

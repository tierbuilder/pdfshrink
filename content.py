"""All page content. Each page is static HTML at build time so search engines and
AI crawlers (which mostly don't run JavaScript) see the full text."""

# ---------------------------------------------------------------- shared FAQ
FAQ_PRIVACY = ("Are my PDFs uploaded to a server?",
               "No. Compression runs entirely inside your browser using JavaScript and WebAssembly-grade libraries. "
               "Your file never leaves your device, so confidential documents stay private. You can even disconnect "
               "from the internet after the page loads and it keeps working.")
FAQ_LIMITS = ("Is there a file size or daily limit?",
              "No daily limits, no sign-up and no watermark. The only limit is your device's memory — most phones "
              "handle PDFs up to a few hundred MB and computers handle more.")
FAQ_TEXT = ("Will my text stay selectable and searchable?",
            "Yes in the normal modes: we keep text, fonts, links, bookmarks and form fields and only re-encode the "
            "images inside the PDF. Only if you ask for an exact size that cannot be reached that way do we flatten "
            "pages into images — and the tool tells you when that happens.")
FAQ_FREE = ("Is it really free?",
            "Yes. Because your own device does the work there are no server costs per file, so there is no reason "
            "to limit or charge for compression.")
FAQ_QUALITY = ("Will compression reduce quality?",
               "Images are re-encoded at the level you choose. “Recommended” is visually indistinguishable for "
               "most documents on screen and in print. Text and vector graphics are never degraded.")


def kb_label(kb):
    return f"{kb // 1024} MB" if kb >= 1024 and kb % 1024 == 0 else f"{kb} KB"


def kb_slug(kb):
    return f"{kb // 1024}mb" if kb >= 1024 and kb % 1024 == 0 else f"{kb}kb"


# ------------------------------------------------------------ target pages
# Each size gets its own real-world context so pages are genuinely distinct.
TARGETS = {
    20: dict(
        who="Very strict upload fields — signature files, single-page declarations and some legacy government or banking portals.",
        tips=["Text-only one-page PDFs usually fit easily.",
              "A scanned page needs grayscale and low resolution to fit — tick “Grayscale” first.",
              "Crop away blank margins before scanning; white space still costs bytes in a scan."],
        q=("Can a scanned page really fit in 20 KB?",
           "Often, yes, if it is a single page of mostly text: in grayscale at around 60–70 DPI a typical scan lands "
           "between 15 and 30 KB. Photos or colour-heavy pages may not fit while staying readable.")),
    50: dict(
        who="ID proofs, caste/income certificates, marksheets and photo-ID uploads on recruitment and scholarship portals.",
        tips=["One scanned page in grayscale typically fits at good readability.",
              "Colour scans of ID cards fit if you scan only the card, not the full A4 page.",
              "If a form asks for JPG instead of PDF, check the upload instructions before compressing."],
        q=("Why do forms ask for PDFs under 50 KB?",
           "Older application portals were built to store millions of uploads cheaply, so they set tight limits per "
           "document. Compressing images inside the PDF, not shrinking the text, is how you get under them.")),
    100: dict(
        who="Government job and exam applications, university admissions, scholarship forms and KYC uploads — the single most common PDF size limit online.",
        tips=["1–2 scanned pages fit comfortably at readable quality.",
              "Keep text-based PDFs (exported from Word or Google Docs) as they are — they are often already under 100 KB after cleanup.",
              "Need several documents in one file? Merge first, then compress the merged PDF to 100 KB."],
        q=("What if my PDF has many pages and won't go under 100 KB?",
           "The tool will produce the smallest readable version and tell you it couldn't reach the target. For long "
           "scans, split the document and upload only the pages the form asks for, or rescan in grayscale.")),
    150: dict(
        who="Admission documents, experience letters and multi-page certificates on job and education portals.",
        tips=["2–3 scanned pages fit at good quality.",
              "Colour stamps and signatures stay legible at this size.",
              "Choose “Exact size” so the result is guaranteed below 150 KB, not just “smaller”."],
        q=("Is 150 KB the same as 0.15 MB?",
           "Close. Sites count a KB as either 1000 or 1024 bytes. We always aim for 1000 bytes per KB (150 KB = "
           "150,000 bytes), so the file is accepted under either convention.")),
    200: dict(
        who="Visa and passport supporting documents, university applications, bank and insurance forms.",
        tips=["3–4 scanned pages fit; colour photos inside the PDF stay clear.",
              "Text-heavy reports with a few charts usually fit without touching image quality much.",
              "If the portal rejects the file anyway, re-run with a slightly lower target such as 190 KB."],
        q=("Why does my 200 KB file still get rejected?",
           "Some sites count 1 KB as 1000 bytes and others as 1024. We already target 1000-byte KB (200,000 bytes) so "
           "both kinds accept it. If a site still refuses, it may also check pixel dimensions or page count — read its rules.")),
    300: dict(
        who="Resumes with photos, project reports and multi-page application bundles.",
        tips=["4–6 scanned pages or a long text document with images fit well.",
              "Resumes exported from design tools often contain huge images — compressing to 300 KB keeps them crisp.",
              "Check the page count: about 50–70 KB per scanned page is a good budget."],
        q=("How many pages fit in 300 KB?",
           "Roughly 15–30 text-only pages, 4–6 grayscale scanned pages or 1–2 full-colour photo pages. Exact numbers "
           "depend on how much image content each page has.")),
    500: dict(
        who="Job applications, CVs with portfolios, claim forms and many e-government uploads.",
        tips=["Most office documents land well under 500 KB with “Recommended” alone.",
              "Scanned contracts of 6–10 pages fit at sharp quality.",
              "Use batch mode to compress all your application documents to 500 KB at once."],
        q=("Is 500 KB good enough quality for printing?",
           "For text documents and typical scans, yes — text stays vector and images remain around 150 DPI. For "
           "photo-heavy brochures meant for professional print, keep a larger original.")),
    1024: dict(
        who="Applicant tracking systems (job portals), online forms, chat apps and email-friendly sharing.",
        tips=["Presentations exported to PDF commonly drop from 10–30 MB to under 1 MB.",
              "Text, links and bookmarks are preserved — recruiters can still search your CV.",
              "We treat 1 MB as 1,000,000 bytes, so the file passes strict and lenient checks alike."],
        q=("How do I make a PDF under 1 MB for a job application?",
           "Choose “Exact size”, set 1 MB, drop in your CV. We compress the images inside it and keep the text "
           "selectable, which matters because many hiring systems read the text automatically.")),
    2048: dict(
        who="University and visa portals, HR systems, school assignment uploads and e-filing.",
        tips=["Scanned books chapters of 20–30 pages typically fit.",
              "Slide decks with photos stay presentation-quality at 2 MB.",
              "Start with “Recommended” — you may land under 2 MB without forcing a target."],
        q=("What's the best way to get a PDF to 2 MB?",
           "Use “Recommended” first; it keeps quality high and is usually enough. If the file is still larger, switch "
           "to “Exact size” with 2 MB so the tool searches for the highest quality that fits.")),
    5120: dict(
        who="Court and tax e-filing, visa applications, LMS assignment uploads and large reports.",
        tips=["Scans of 50–100 pages often fit after grayscale compression.",
              "Full-colour catalogs and portfolios stay sharp at 5 MB.",
              "Batch-compress several exhibits at once and download them as a ZIP."],
        q=("My scanned PDF is 60 MB — can it get to 5 MB?",
           "Usually. Scanners save images at 300–600 DPI, far more than needed to read on screen. Re-encoding them at "
           "around 150 DPI typically cuts size by 80–95%.")),
    10240: dict(
        who="Email attachments (corporate mail servers often cap at 10 MB), messaging apps and cloud forms.",
        tips=["Large presentations and photo reports fit without visible quality loss.",
              "Remember attachments grow ~33% when emailed (base64), so 10 MB on disk can be ~13 MB in an email.",
              "For Gmail's 25 MB limit see our email guide."],
        q=("Why does a 9 MB PDF bounce from a 10 MB email limit?",
           "Email encodes attachments as base64, adding about a third to their size. Compress to about 7 MB to send "
           "safely through a 10 MB limit.")),
}



# Typical size of one page *after* good compression (KB): (low, typical, high).
PAGE_COST = [
    ("Text-only page (exported from Word, Google Docs, a website)", 5, 15, 25),
    ("Scanned page in grayscale (letters, forms, certificates)", 15, 60, 90),  # 15 KB ≈ one page at ~70 DPI
    ("Scanned page in colour (stamps, photos, coloured backgrounds)", 80, 150, 250),
    ("Full-page colour photo or brochure page", 150, 220, 400),
]


def _fit_range(kb, lo, hi, text=False):
    a, b = int(kb // hi), int(kb // lo)
    if text and a < 1 <= b:  # text is never re-encoded, so short files fit without any quality loss
        return f"1–{b}", "✅ Short documents usually fit, text stays sharp"
    if b < 1:
        return "under 1", "❌ Unlikely — even one page needs heavy quality loss"
    if a < 1:
        return (f"0–{b}", "⚠️ One page at most, at reduced quality" if b == 1 else "⚠️ Only a page or two, at reduced quality")
    rng = f"{a}" if a == b else f"{a}–{b}"
    if a >= 3:
        return rng, "✅ Yes, comfortably"
    return rng, "✅ Yes, if the file has only a few pages"


def realistic_section(kb, L):
    kb_label_in = kb
    kb = kb // 1024 * 1000 if kb >= 1024 and kb % 1024 == 0 else kb  # the tool counts 1 MB = 1000 KB
    rows = ""
    for label, lo, typ, hi in PAGE_COST:
        rng, verdict = _fit_range(kb, lo, hi, text=label.startswith("Text"))
        rows += f"<tr><td>{label}</td><td>{lo}–{hi} KB</td><td>{rng}</td><td>{verdict}</td></tr>"
    nxt = {20: 50, 50: 100, 100: 200, 150: 200, 200: 300, 300: 500, 500: 1024, 1024: 2048, 2048: 5120, 5120: 10240}.get(kb_label_in)
    nxt_link = (f'<li>Check whether your form actually allows more — if so, <a href="/compress-pdf-to-{kb_slug(nxt)}/">compress to {kb_label(nxt)}</a> for better quality.</li>'
                if nxt else "")
    budget = lambda n: f"{kb / n / 1000:g} MB" if kb / n >= 1000 else f"{kb / n:.0f} KB"
    return f"""
<h2>Is {L} realistic for my PDF?</h2>
<p>It depends almost entirely on <strong>what is on the pages and how many pages there are</strong> — not on the tool.
Text is tiny; scanned and photographed pages are images, and every page shares the same {L}. Typical sizes per page
after good compression:</p>
<div class="tablewrap"><table><thead><tr><th>What your PDF contains</th><th>Size per page</th><th>Pages that fit in {L}</th><th>Realistic?</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="muted small">Estimates for typical A4/Letter pages at readable quality; your file may differ. The tool always
tells you whether it reached {L}.</p>
<h3>10-second self-check</h3>
<p>Divide {L} by your number of pages. With 1 page you have {budget(1)} per page, with 2 pages {budget(2)}, with
5 pages {budget(5)}. Then compare: <strong>about 15 KB</strong> per page is enough for text, <strong>about 60 KB</strong>
for a grayscale scan and <strong>about 150–220 KB</strong> for colour scans or photos.{" (We count 1 MB as 1,000 KB, so it also passes stricter checks.)" if kb_label_in >= 1024 else ""}</p>
<h3>If it won't fit</h3>
<ul>
<li>Tick <strong>Grayscale</strong> under “More options” — for scans it often halves the size.</li>
<li>Upload only the pages the form needs: <a href="/delete-pdf-pages/">delete pages</a> or <a href="/split-pdf/">split the PDF</a>.</li>
<li>Re-scan at 150 DPI in grayscale instead of 300 DPI colour, and crop to the paper's edges.</li>
<li>Photos of documents? Crop them first, then use <a href="/jpg-to-pdf/">JPG to PDF</a>.</li>
{nxt_link}
</ul>
"""


def target_page(kb):
    t = TARGETS[kb]
    L, s = kb_label(kb), kb_slug(kb)
    text_pages = max(1, kb // 15)
    gray_pages = max(1, round(kb / 60))
    color_pages = kb / 220
    color_txt = "less than one" if color_pages < 1 else f"about {round(color_pages)}"
    return dict(
        slug=f"compress-pdf-to-{s}",
        title=f"Compress PDF to {L} Online Free — Exact Size, No Upload",
        desc=f"Reduce a PDF to under {L} in seconds. Exact target size, keeps text sharp, works in your browser — no upload, no sign-up, no limits.",
        h1=f"Compress PDF to {L}",
        lead=f"Get any PDF under {L} for online forms and uploads. Set the size, drop the file — done in seconds, right on your device.",
        target_kb=kb,
        crumb=f"PDF to {L}",
        facts=[
            f"Guarantees the output is at or below {L} when possible (counting 1 KB = 1000 bytes, so it passes either convention), and tells you if it isn't.",
            "Text and links stay selectable; only images are re-encoded unless flattening is needed.",
            f"Rough capacity of {L}: ~{text_pages} text-only pages, ~{gray_pages} grayscale scanned page(s), {color_txt} full-colour photo page(s) — see “Is {L} realistic?” below.",
            "Runs in your browser: files are never uploaded. Free, unlimited, no watermark.",
        ],
        steps=[
            "Click “Choose files” or drop your PDF onto the box above.",
            f"The size is already set to {L} — change it if your form needs something else.",
            "Wait a few seconds while the tool finds the best quality that fits.",
            "Click “Download” and upload the compressed PDF to your form.",
        ],
        body=f"""
<h2>Who needs a PDF under {L}?</h2>
<p>{t['who']}</p>
{realistic_section(kb, L)}
<h2>Tips to fit {L} with the best quality</h2>
<ul>{''.join(f'<li>{x}</li>' for x in t['tips'])}</ul>
<h2>How we hit {L} exactly</h2>
<p>Most compressors apply one fixed setting and hope the result is small enough. We search for it: first we remove
waste (duplicate objects, metadata, thumbnails), then re-encode the images at progressively lower resolution
and quality, checking the size after each try and keeping the <strong>highest quality that is still under {L}</strong>.
Only if images alone can't get there do we flatten pages, and we say so on screen.</p>
""",
        faqs=[t['q'], FAQ_PRIVACY, FAQ_TEXT, FAQ_LIMITS],
        group="size",
    )


# ------------------------------------------------------------ other pages
HOME = dict(
    slug="",
    title="Compress PDF Free — Reduce PDF Size Online Without Uploading",
    desc="Free PDF compressor that runs in your browser. Shrink PDFs to an exact size like 100 KB, keep text sharp, batch compress — no upload, no sign-up, no limits.",
    h1="Compress PDF files — privately, for free",
    lead="Shrink PDFs by up to 90% or to an exact size like 100 KB. Everything happens on your device, so nothing is uploaded and there are no limits.",
    crumb="Compress PDF",
    facts=[
        "100% in-browser: your PDF is never uploaded to any server.",
        "No daily limit, no file-size cap, no sign-up, no watermark.",
        "Exact target size mode (e.g. 100 KB, 200 KB, 1 MB) for online forms.",
        "Keeps text selectable, links, bookmarks and form fields — only images are re-encoded.",
        "Batch compress many PDFs and download them as a ZIP. Works offline after the first visit.",
    ],
    steps=[
        "Drop one or more PDFs onto the box, or click to choose them.",
        "Pick a level — Recommended, Strong or Light — or set an exact size.",
        "Download each file, or all of them as a ZIP.",
    ],
    body="""
<h2>Why this PDF compressor is different</h2>
<div class="grid">
<div class="card"><h3>Never uploaded</h3><p>Compression runs in your browser. Bank statements, contracts and IDs never touch a server — not ours, not anyone's.</p></div>
<div class="card"><h3>Exact size targets</h3><p>Need under 100 KB for a form? Set it. We search for the best quality that fits instead of guessing.</p></div>
<div class="card"><h3>Text stays text</h3><p>We re-encode images only, so your PDF stays searchable, copyable and accessible — unlike tools that turn pages into pictures.</p></div>
<div class="card"><h3>No limits</h3><p>No “2 tasks per day”, no 25 MB cap, no account. Your device does the work, so it's free for good.</p></div>
<div class="card"><h3>Batch + ZIP</h3><p>Drop 50 PDFs at once and get them back in one ZIP file.</p></div>
<div class="card"><h3>Works offline</h3><p>After your first visit the app is cached — install it and compress PDFs on a plane.</p></div>
</div>
<h2>How it compares</h2>
<div class="tablewrap"><table>
<thead><tr><th>Feature</th><th>This tool</th><th>Typical online compressors</th></tr></thead>
<tbody>
<tr><td>Files uploaded to a server</td><td class="yes">Never</td><td class="no">Yes</td></tr>
<tr><td>Free daily limit</td><td class="yes">Unlimited</td><td>Often 1–2 tasks per day or per hour</td></tr>
<tr><td>Max file size (free)</td><td class="yes">Your device's memory</td><td>Often 25–100 MB</td></tr>
<tr><td>Account required</td><td class="yes">No</td><td>Often, for more files</td></tr>
<tr><td>Exact target size (100 KB, 1 MB…)</td><td class="yes">Yes, verified</td><td>Rare; fixed presets</td></tr>
<tr><td>Text remains selectable</td><td class="yes">Yes</td><td>Varies</td></tr>
<tr><td>Batch + ZIP download</td><td class="yes">Free</td><td>Often paid</td></tr>
<tr><td>Works offline</td><td class="yes">Yes</td><td class="no">No</td></tr>
</tbody></table></div>
<h2>What makes PDFs large — and what we do about it</h2>
<p>In almost every oversized PDF the culprit is images: scans saved at 300–600 DPI, photos pasted straight from a
phone camera, or slides with full-resolution backgrounds. Text and vector drawings are tiny by comparison. So we
downscale and re-encode the images, deflate any uncompressed data, and delete things nobody sees — editing history,
embedded thumbnails, XMP metadata and orphaned objects left behind by previous edits. Read more in
<a href="/why-is-my-pdf-so-large/">Why is my PDF so large?</a></p>
""",
    faqs=[FAQ_PRIVACY, FAQ_LIMITS, FAQ_TEXT, FAQ_QUALITY, FAQ_FREE,
          ("How much smaller will my PDF get?",
           "Scanned and photo-heavy PDFs typically shrink 60–95%. PDFs that are mostly text are often already compact; "
           "for those we remove hidden waste, which saves 5–40%. If we can't make it smaller we return the original."),
          ("Does it work on iPhone and Android?",
           "Yes. It runs in Safari, Chrome, Firefox and Edge on phones, tablets and computers — no app to install. "
           "You can also add it to your home screen.")],
    group="main",
)

USE_CASES = [
    dict(
        slug="compress-pdf-for-email",
        title="Compress PDF for Email — Fit Gmail & Outlook Limits Free",
        desc="Make PDFs small enough to email. Fit Gmail's 25 MB and Outlook's 20 MB limits, keep text sharp, no upload or sign-up needed.",
        h1="Compress a PDF for email",
        lead="Attachment too big? Shrink it to fit Gmail, Outlook or your company's mail server in seconds — privately, on your device.",
        target_kb=None, mode="recommended", crumb="For email",
        facts=["Gmail and Yahoo Mail allow attachments up to 25 MB; Outlook.com allows 20 MB.",
               "Email adds about 33% (base64 encoding), so aim for roughly 18 MB for Gmail and 14 MB for Outlook.",
               "Company servers often cap at 10 MB — target about 7 MB to be safe.",
               "Files are compressed in your browser, so confidential attachments are never uploaded."],
        steps=["Drop the PDF you want to email.", "Keep “Recommended”, or choose “Exact size” and enter your mail limit.",
               "Download and attach the smaller file."],
        body="""
<h2>Email attachment size limits</h2>
<div class="tablewrap"><table><thead><tr><th>Service</th><th>Attachment limit</th><th>Safe PDF size</th></tr></thead><tbody>
<tr><td>Gmail</td><td>25 MB</td><td>≈ 18 MB</td></tr>
<tr><td>Outlook.com / Hotmail</td><td>20 MB</td><td>≈ 14 MB</td></tr>
<tr><td>Yahoo Mail</td><td>25 MB</td><td>≈ 18 MB</td></tr>
<tr><td>Many company servers</td><td>10 MB</td><td>≈ 7 MB</td></tr>
</tbody></table></div>
<p>Limits change occasionally and some organizations set their own; check with your provider if a message bounces.</p>
<h2>Why send a small PDF instead of a link?</h2>
<p>Attachments open instantly on any device, don't expire, and don't require the recipient to sign in to a cloud
drive. A compressed PDF also downloads faster on mobile data and is less likely to be stripped by spam filters.</p>
""",
        faqs=[("Why does my email say the attachment is too big when the file is smaller than the limit?",
               "Email encodes attachments in base64, which increases their size by about a third. A 20 MB PDF becomes "
               "roughly 27 MB inside the message."), FAQ_PRIVACY, FAQ_TEXT],
        group="use",
    ),
    dict(
        slug="compress-pdf-for-online-forms",
        title="Compress PDF for Online Application Forms — Exam, Job & Govt",
        desc="Reduce certificates, ID proofs and marksheets to the size job, exam, admission and government portals accept (50 KB, 100 KB, 200 KB). Free, no upload.",
        h1="Compress PDFs for online application forms",
        lead="Recruitment, exam, admission, scholarship and government portals often accept only tiny files. Hit their exact limit without making your documents unreadable.",
        target_kb=100, crumb="For online forms",
        facts=["Common portal limits are 50 KB, 100 KB, 200 KB, 500 KB and 1 MB per document.",
               "Set the exact limit and the tool keeps the highest quality that fits.",
               "Certificates, marksheets and ID proofs stay legible — stamps and signatures included.",
               "Your documents are processed on your device — never uploaded, which matters for ID proofs."],
        steps=["Read the size limit in the form's instructions (e.g. “max 100 KB”).",
               "Set that size above and drop all your documents at once.",
               "Download them as a ZIP and upload each to the portal."],
        body="""
<h2>Typical document size limits</h2>
<div class="tablewrap"><table><thead><tr><th>Document</th><th>Common limit</th><th>Tool</th></tr></thead><tbody>
<tr><td>Signature, declaration</td><td>10–50 KB</td><td><a href="/compress-pdf-to-50kb/">PDF to 50 KB</a></td></tr>
<tr><td>ID proof, caste/income certificate</td><td>50–100 KB</td><td><a href="/compress-pdf-to-100kb/">PDF to 100 KB</a></td></tr>
<tr><td>Marksheets, degree certificate</td><td>100–300 KB</td><td><a href="/compress-pdf-to-200kb/">PDF to 200 KB</a></td></tr>
<tr><td>Experience letters, CV</td><td>300 KB–2 MB</td><td><a href="/compress-pdf-to-500kb/">PDF to 500 KB</a></td></tr>
</tbody></table></div>
<p>Always follow the exact limit stated in your form; these are only common patterns.</p>
<h2>Avoiding rejection</h2>
<ul>
<li>Scan in grayscale unless colour is required — it's the biggest single saving.</li>
<li>Scan just the document, not the whole scanner bed; crop margins.</li>
<li>We count 1 KB as 1000 bytes, so files pass sites that use either 1000 or 1024. If a portal still rejects a file, check its dimension, format and page rules.</li>
<li>Don't password-protect the PDF; portals often can't open protected files.</li>
</ul>
""",
        faqs=[("Will a compressed certificate still be accepted?",
               "Yes, as long as it is legible. We keep text and stamps readable and never add a watermark."),
              ("Can I compress all my documents at once?",
               "Yes. Drop them together, set the size once, and download a ZIP."), FAQ_PRIVACY],
        group="use",
    ),
    dict(
        slug="compress-scanned-pdf",
        title="Compress Scanned PDF — Shrink Scans 80–95% Free, No Upload",
        desc="Scanned PDFs are huge because scanners save 300–600 DPI images. Shrink them 80–95% while staying readable. Free, private, in your browser.",
        h1="Compress a scanned PDF",
        lead="Scanners save every page as a high-resolution photo. We bring them down to a sensible resolution so your scan is 5–20× smaller and still crisp.",
        target_kb=None, mode="recommended", crumb="Scanned PDF",
        facts=["Scanned pages are images; a 300 DPI colour A4 page can be 1–5 MB.",
               "Re-encoding at ~150 DPI usually cuts size by 80–95% with no visible loss on screen.",
               "Grayscale halves the size again for black-and-white documents.",
               "Processing happens on your device — scans of IDs and contracts are never uploaded."],
        steps=["Drop your scanned PDF.", "Choose “Recommended”, or “Strong” for very large scans; tick Grayscale for text-only scans.",
               "Download the smaller PDF."],
        body="""
<h2>Why scans are so big</h2>
<p>A scanner doesn't know what text is — it photographs each page. At 300 DPI an A4 page is about 2480 × 3508 pixels,
and phone “scanner” apps often go higher. That's ideal for archives but far beyond what's needed to read on a screen
or print on an office printer.</p>
<h2>Best settings for scans</h2>
<ul><li><strong>Text documents:</strong> Strong + Grayscale — usually 30–80 KB per page.</li>
<li><strong>Documents with colour stamps or photos:</strong> Recommended — usually 100–250 KB per page.</li>
<li><strong>Archive quality:</strong> Light — still 40–70% smaller than most raw scans.</li></ul>
""",
        faqs=[("Can I make a scanned PDF searchable?",
               "This tool reduces size; it doesn't add OCR. Searchable scans that already have an OCR text layer keep it."),
              FAQ_QUALITY, FAQ_PRIVACY],
        group="use",
    ),
    dict(
        slug="compress-pdf-without-losing-quality",
        title="Compress PDF Without Losing Quality — Lossless & Light Modes",
        desc="Reduce PDF size while keeping full quality: lossless cleanup plus gentle image optimization. Text and vectors untouched. Free, in-browser.",
        h1="Compress PDF without losing quality",
        lead="Use lossless cleanup and our Light mode to shrink PDFs while keeping images sharp and text perfect.",
        target_kb=None, mode="light", crumb="Without losing quality",
        facts=["Lossless mode removes metadata, thumbnails, duplicate/orphaned objects and compresses uncompressed streams — pixels are untouched.",
               "Light mode re-encodes only images larger than ~2600 px at high JPEG quality.",
               "Text, fonts and vector graphics are never rasterized in these modes.",
               "If nothing can be saved, you get the original file back — never a worse one."],
        steps=["Drop your PDF.", "Choose “Light”, or open “More options” and tick “Lossless only”.", "Download and compare."],
        body="""
<h2>Lossless vs. visually lossless</h2>
<p><strong>Lossless</strong> means not a single pixel changes: we only restructure the file and remove hidden data.
Typical savings are 5–40%, more for PDFs that were edited many times. <strong>Visually lossless</strong> (Light mode)
also re-encodes oversized images at high quality — at normal zoom you can't tell the difference, and savings are
often 40–70%.</p>
""",
        faqs=[("Which mode should I choose?",
               "For print-ready or archival PDFs use Lossless. For sharing and uploading use Light or Recommended."),
              FAQ_TEXT, FAQ_PRIVACY],
        group="use",
    ),
    dict(
        slug="compress-pdf-without-uploading",
        title="Compress PDF Offline Without Uploading — Private & Secure",
        desc="Compress confidential PDFs with zero upload. Runs locally in your browser, works offline, no account. Ideal for bank statements, contracts and IDs.",
        h1="Compress PDFs without uploading them",
        lead="For confidential files — contracts, bank statements, medical records, IDs — compression should happen on your device. Here it does.",
        target_kb=None, mode="recommended", crumb="Without uploading",
        facts=["All processing uses JavaScript running in your browser tab; no file data is sent over the network.",
               "You can verify it: open your browser's developer tools → Network tab while compressing — no upload requests appear.",
               "Works with Wi-Fi turned off after the page has loaded once (it's an installable offline web app).",
               "No account, no cookies required for compression, no file retention — closing the tab erases everything."],
        steps=["Load this page (optionally, then switch off Wi-Fi).", "Drop your PDF and choose a level.", "Download — the file only ever existed on your device."],
        body="""
<h2>Why uploading matters</h2>
<p>Upload-based tools receive a full copy of your document. Even with good intentions, that copy passes through
servers, logs and backups you don't control, and may be subject to another country's laws. For regulated data
(health, finance, HR, legal) that alone can break company policy. Local processing removes the question entirely.</p>
<h2>How to check for yourself</h2>
<ol><li>Open developer tools (F12, or ⌥⌘I on Mac) and select the <em>Network</em> tab.</li>
<li>Compress a PDF.</li><li>You'll see no request carrying your file — only the app's own scripts, loaded once.</li></ol>
""",
        faqs=[FAQ_PRIVACY, ("Can I use it at work with sensitive files?",
               "Yes — since nothing leaves the device, it fits most data-handling policies. Check your organization's rules on browser tools."),
              ("Do you store anything?", "No file data is stored. Optional anonymous usage counts (e.g. “a file was compressed”) may be collected to improve the tool; they never contain file contents or names.")],
        group="use",
    ),
    dict(
        slug="batch-compress-pdf",
        title="Batch Compress PDF — Compress Multiple PDFs at Once Free",
        desc="Compress dozens of PDFs in one go and download them as a ZIP. Same exact-size or quality setting for all. Free, unlimited, no upload.",
        h1="Batch compress multiple PDFs",
        lead="Drop a whole folder's worth of PDFs, pick one setting, and get them all back in a single ZIP.",
        target_kb=None, mode="recommended", crumb="Batch compress",
        facts=["No limit on the number of files — they're processed one after another on your device.",
               "One setting applies to all: a quality level or an exact size such as 200 KB.",
               "Download each file or everything as one ZIP.",
               "Free batch processing — usually a paid feature elsewhere."],
        steps=["Select or drop multiple PDFs (Ctrl/Cmd-click to multi-select).", "Choose a level or exact size.", "Click “Download all (ZIP)”."],
        body="""
<h2>Great for</h2>
<ul><li>Application packs: certificates, ID proofs, marksheets — all to 100 KB.</li>
<li>Invoices and receipts before archiving or sending to an accountant.</li>
<li>Course material and lecture slides before uploading to an LMS.</li></ul>
""",
        faqs=[("Is there a limit to how many PDFs I can batch compress?",
               "No hard limit. Very large batches just take longer, and your device's memory is the practical ceiling."),
              FAQ_PRIVACY],
        group="use",
    ),
]

DEVICES = [
    dict(
        slug="compress-pdf-on-iphone",
        title="How to Compress a PDF on iPhone & iPad (Free, No App)",
        desc="Reduce PDF size on iPhone or iPad in Safari — no app, no upload. Plus the built-in Files and Shortcuts methods compared.",
        h1="Compress a PDF on iPhone or iPad",
        lead="No app needed: this page works in Safari. Tap the box, pick your PDF from Files, and save the smaller copy back.",
        target_kb=None, mode="recommended", crumb="On iPhone",
        facts=["Works in Safari, Chrome and other iOS browsers — no App Store download.",
               "Pick files from Files, iCloud Drive, Google Drive or Dropbox via the iOS file picker.",
               "Tap “Download”, then share or save to Files.",
               "Add to Home Screen (Share → Add to Home Screen) to use it like an app, even offline."],
        steps=["Tap the upload box and choose “Browse” to pick your PDF from Files.",
               "Choose a level or an exact size.", "Tap “Download” → open the share sheet → Save to Files."],
        body="""
<h2>Other ways on iPhone</h2>
<p><strong>Shortcuts app:</strong> you can build a shortcut with the “Optimize File Size of PDF” action, but it
offers no size control. <strong>Mail:</strong> iOS can't shrink PDF attachments, only images. This page gives you
exact size targets and batch processing without installing anything.</p>
""",
        faqs=[("Where does the compressed PDF go?", "Safari saves it to Downloads in the Files app by default; you can change that in Settings → Apps → Safari → Downloads."),
              FAQ_PRIVACY],
        group="device",
    ),
    dict(
        slug="compress-pdf-on-android",
        title="How to Compress a PDF on Android (Free, No App)",
        desc="Shrink PDFs on any Android phone in Chrome — no app, no upload, exact size like 100 KB. Works offline once loaded.",
        h1="Compress a PDF on Android",
        lead="Open this page in Chrome, tap the box, choose your PDF — get a smaller file in your Downloads folder.",
        target_kb=None, mode="recommended", crumb="On Android",
        facts=["Works in Chrome, Samsung Internet, Firefox and Edge on Android.",
               "Choose PDFs from Files, Downloads, Google Drive or WhatsApp documents.",
               "Compressed files save to Downloads.",
               "Install as an app from Chrome's menu (“Add to Home screen”) for offline use."],
        steps=["Tap the box and choose your PDF.", "Pick a level or exact size such as 100 KB.", "Tap “Download” — find it in Files → Downloads."],
        body="""
<h2>Why not install an app?</h2>
<p>Many PDF compressor apps on app stores upload your file to their servers, show heavy ads or lock features behind
subscriptions. A web app that runs locally avoids all three and takes no storage space.</p>
""",
        faqs=[("Does it work on low-end phones?", "Yes, though big scans take longer. For very large files, use “Strong” to reduce work, or compress on a computer."),
              FAQ_PRIVACY],
        group="device",
    ),
    dict(
        slug="compress-pdf-on-mac",
        title="Compress a PDF on Mac — Better than Preview (Free)",
        desc="Compress PDFs on macOS without Preview's blurry Reduce File Size filter. Exact sizes, keeps text, free, offline-capable, no upload.",
        h1="Compress a PDF on Mac",
        lead="Preview's “Reduce File Size” often makes documents blurry or barely smaller. Here you control the quality — or set an exact size.",
        target_kb=None, mode="recommended", crumb="On Mac",
        facts=["macOS Preview: File → Export → Quartz Filter → Reduce File Size — fixed, aggressive, no size control.",
               "This tool offers Light/Recommended/Strong levels and exact sizes, and keeps text selectable.",
               "Works in Safari, Chrome, Firefox and Edge on macOS.",
               "Install from Chrome/Edge (address bar → Install) to use it offline like a native app."],
        steps=["Drag PDFs from Finder onto the box.", "Choose a level or exact size.", "Download — the file lands in your Downloads folder."],
        body="""
<h2>Preview vs. this tool</h2>
<div class="tablewrap"><table><thead><tr><th></th><th>Preview (Quartz filter)</th><th>This tool</th></tr></thead><tbody>
<tr><td>Quality control</td><td>One fixed setting</td><td>Light / Recommended / Strong / exact size</td></tr>
<tr><td>Typical image result</td><td>Often visibly blurry</td><td>Sharp at Recommended</td></tr>
<tr><td>Batch</td><td>One at a time</td><td>Many + ZIP</td></tr>
<tr><td>Upload</td><td>No</td><td>No</td></tr>
</tbody></table></div>
""",
        faqs=[("Why does Preview sometimes make my PDF bigger?",
               "The Quartz filter re-encodes everything with fixed settings, which can enlarge already-optimized files. We always keep the original if we can't make it smaller."),
              FAQ_PRIVACY],
        group="device",
    ),
    dict(
        slug="compress-pdf-on-windows",
        title="How to Compress a PDF on Windows 10 & 11 (Free, No Software)",
        desc="Reduce PDF size on Windows without installing software or uploading files. Exact size targets, batch ZIP, keeps text. Works in Edge and Chrome.",
        h1="Compress a PDF on Windows",
        lead="Windows has no built-in PDF compressor. This page works in Edge or Chrome without installing anything — and without uploading your file.",
        target_kb=None, mode="recommended", crumb="On Windows",
        facts=["Windows 10/11 can create PDFs (Microsoft Print to PDF) but cannot compress them.",
               "“Print to PDF” on a scanned file usually makes it bigger, not smaller.",
               "This tool runs in Edge, Chrome or Firefox with nothing to install.",
               "Install as an app from Edge (… → Apps → Install) for offline use."],
        steps=["Drag PDFs from File Explorer onto the box.", "Choose a level or an exact size.", "Download single files or a ZIP."],
        body="""
<h2>Desktop alternatives</h2>
<p>Desktop suites can compress PDFs but are paid or require installation and admin rights — often not possible on
office PCs. A local-processing web app gives the same privacy as desktop software without the install.</p>
""",
        faqs=[("Do I need admin rights?", "No. It's a web page; nothing is installed unless you choose to add it as an app."), FAQ_PRIVACY],
        group="device",
    ),
]

GUIDES = [
    dict(
        slug="why-is-my-pdf-so-large",
        title="Why Is My PDF So Large? 7 Causes and How to Fix Each",
        desc="The seven reasons PDFs get huge — high-DPI scans, camera photos, embedded fonts, edit history and more — and how to fix each one for free.",
        h1="Why is my PDF so large?",
        lead="Seven common causes of oversized PDFs, how to spot each one, and how to fix it.",
        target_kb=None, mode="recommended", crumb="Why is my PDF so large", tool=False,
        facts=["Images cause most oversized PDFs — usually scans or phone photos at far higher resolution than needed.",
               "Text is tiny: a page of plain text is typically 2–20 KB.",
               "Repeated editing can leave old versions of content inside the file (incremental saves).",
               "Fonts, embedded attachments, metadata and thumbnails add smaller amounts."],
        steps=None,
        body="""
<h2>1. High-resolution scans</h2>
<p>Scanning at 300–600 DPI in colour produces 1–5 MB per page. For reading and normal printing, 150 DPI is plenty
and grayscale is enough for text. <em>Fix:</em> <a href="/compress-scanned-pdf/">compress the scan</a>.</p>
<h2>2. Photos straight from a phone camera</h2>
<p>A 12–48 MP photo pasted into a document keeps its full resolution even when shown at thumbnail size.
<em>Fix:</em> image re-encoding at Recommended typically saves 80%+.</p>
<h2>3. Slides and designs exported to PDF</h2>
<p>Presentation and design apps often embed every background image at original resolution, sometimes several times.</p>
<h2>4. Incremental saves</h2>
<p>Some editors append changes to the end of the file instead of rewriting it, so deleted pages and replaced images
are still inside. <em>Fix:</em> our lossless cleanup rebuilds the file and drops unreachable objects.</p>
<h2>5. Embedded fonts</h2>
<p>Full font files (especially CJK fonts) can add several MB. Most exporters subset fonts; if yours doesn't, re-export
with “subset fonts” enabled.</p>
<h2>6. Attachments and multimedia</h2>
<p>PDFs can carry attached files, audio or video. Remove them in your PDF editor if they aren't needed.</p>
<h2>7. Metadata, thumbnails and editing data</h2>
<p>XMP metadata, page thumbnails and application-private data (like PieceInfo) are invisible but add up. Our default
cleanup removes them.</p>
""",
        faqs=[("What is a normal size for a PDF page?",
               "Text-only: 2–20 KB. Text with a few graphics: 20–100 KB. Grayscale scan at 150 DPI: 50–150 KB. Colour photo page: 200 KB–1 MB."),
              ("Does converting to PDF/A reduce size?", "No — PDF/A requires embedding all fonts and often increases size.")],
        group="guide",
    ),
    dict(
        slug="how-it-works",
        title="How Our In-Browser PDF Compression Works",
        desc="A technical look at how this PDF compressor shrinks files locally: object cleanup, stream deflation, image re-encoding and target-size search.",
        h1="How the compressor works",
        lead="A plain-English (and a bit technical) explanation of what happens to your PDF — all of it inside your browser.",
        target_kb=None, mode="recommended", crumb="How it works", tool=False,
        facts=["Libraries: pdf-lib (PDF structure), pako (zlib), pdf.js (rendering), all executed locally.",
               "Step 1 — cleanup: remove XMP metadata, thumbnails, PieceInfo, and objects unreachable from the document root.",
               "Step 2 — streams: deflate any uncompressed content streams; save with compressed object streams.",
               "Step 3 — images: decode JPEG and Flate (8-bit RGB/gray) images, downscale, re-encode as JPEG if smaller.",
               "Step 4 — exact size: binary search over quality levels; flatten pages to images only as a last resort."],
        steps=None,
        body="""
<h2>Smart mode (default)</h2>
<p>We parse the PDF into its objects, walk the object graph from the document catalog and drop everything that
isn't reachable — leftovers from previous edits. We remove metadata and embedded page thumbnails, compress any
uncompressed streams with zlib, then look at each image. Supported images (JPEG, and 8-bit RGB or grayscale
Flate images, including PNG-predicted ones) are decoded with the browser's own decoder, resized so the longest
side fits the chosen limit, and re-encoded as JPEG. If the new version isn't smaller, the original image is kept.
CMYK, indexed-colour and masked images are left untouched to avoid colour shifts.</p>
<h2>Exact-size mode</h2>
<p>Given a target like 100 KB, we first try lossless cleanup. If that isn't enough, we binary-search an 8-step
ladder from high quality (JPEG 82%, 2600 px) to low (20%, 620 px), keeping the best result under the target. If
even the lowest step is too large — for example because the PDF contains many vector-heavy pages — we render each
page with pdf.js and binary-search resolution (150 → 44 DPI) and quality. The result tells you which path was used.</p>
<h2>Safety</h2>
<p>We never return a file larger than your original. PDFs with security restrictions are flattened rather than
modified, because rewriting them in place would break their encryption.</p>
""",
        faqs=[("Is the source code available?", "The app is plain HTML and JavaScript; you can read every line in your browser's developer tools."),
              FAQ_PRIVACY],
        group="guide",
    ),
]

PRIVACY_PAGE = dict(
    slug="privacy",
    title="Privacy Policy — Files Never Leave Your Device",
    desc="Privacy policy: PDF files are processed locally in your browser and never uploaded, stored or seen by us.",
    h1="Privacy",
    lead="Short version: your files never leave your device.",
    target_kb=None, crumb="Privacy", tool=False,
    facts=["PDF files are processed entirely in your browser and are never transmitted to us or anyone else.",
           "We don't require accounts and don't store files.",
           "If analytics is enabled, it records only anonymous aggregate events (page views, “file compressed”) — never file names or contents."],
    steps=None,
    body="""
<h2>Files</h2><p>When you select a PDF, it is read into your browser's memory, compressed there, and offered back to
you as a download. Closing or reloading the tab discards it.</p>
<h2>Analytics</h2><p>We may use privacy-friendly, cookie-less analytics to count visits and anonymous events. No
personal data or document information is included.</p>
<h2>Offline cache</h2><p>The app's own code is cached by your browser so it can work offline. It contains no personal data.</p>
""",
    faqs=[], group="legal",
)

SIZES = [20, 50, 100, 150, 200, 300, 500, 1024, 2048, 5120, 10240]


# ================================================================ image tools
FAQ_IMG_PRIVACY = ("Is my photo uploaded anywhere?",
                   "No. The image is resized inside your browser and never leaves your device — important for ID photos and signatures.")
FAQ_IMG_EXIF = ("Does it remove location and camera data (EXIF)?",
                "Yes. The output is a freshly encoded image, so GPS location, camera model and other EXIF metadata from your phone are not carried over.")

IMG_TARGETS = {
    10: dict(who="Signature uploads and thumbnail fields with very tight limits.",
             tips=["Signatures compress best: sign in black ink on plain white paper.",
                   "Crop tightly around the signature before uploading.",
                   "If the form gives dimensions (e.g. 140×60 px), enter them under “Dimensions”."],
             q=("Can a photo be under 10 KB and still look good?",
                "A small passport-style photo (around 200×230 px) usually fits in 8–12 KB at acceptable quality. Larger photos will be scaled down to fit.")),
    20: dict(who="Signatures and passport-style photos on exam, recruitment and scholarship application forms — one of the most common upload limits.",
             tips=["Set the exact pixel dimensions from the form first, then the size limit.",
                   "Use a plain, light background — busy backgrounds take more bytes.",
                   "If the form also has a minimum (e.g. 10–20 KB), enter it under “Min size”."],
             q=("How do I resize a photo to 20 KB for an application form?",
                "Drop your photo, keep the size at 20 KB, and if the form specifies dimensions enter them with “Crop to exact size”. Download the JPG and upload it.")),
    30: dict(who="Application photos where the limit is 30 KB, and signatures with more generous limits.",
             tips=["Face photos look sharp at 30 KB up to about 400×500 px.",
                   "Avoid screenshots of photos — start from the original camera image.",
                   "Check whether the form wants JPG specifically; most do."],
             q=("Why does the website say my 29 KB photo is too large?",
                "Usually it's a different rule you've missed — pixel dimensions, format (JPG vs PNG) or a minimum size. We count 1 KB as 1000 bytes, so our 30 KB output passes both 1000- and 1024-byte checks.")),
    50: dict(who="Photos and ID scans for job portals, admission forms and KYC.",
             tips=["A 600×600 px photo fits easily in 50 KB at high quality.",
                   "For ID cards, crop to the card itself before resizing.",
                   "Batch-resize all your documents to 50 KB at once and download a ZIP."],
             q=("What resolution fits in 50 KB?",
                "Typical portrait photos fit at around 600–900 px on the long side with good quality. Scanned documents with lots of text may need slightly lower resolution.")),
    100: dict(who="Profile pictures, ID document scans and image uploads on forms and marketplaces.",
              tips=["Photos up to about 1000–1200 px stay crisp at 100 KB.",
                    "WebP is ~25% smaller than JPG at the same quality — use it for websites, not for forms.",
                    "Scanned certificates are readable at 100 KB if cropped to the page."],
              q=("Is 100 KB good enough for a profile photo?",
                 "Yes — most sites display profile photos well under 1000 px wide, which fits comfortably in 100 KB.")),
    200: dict(who="Website images, document scans and online listing photos.",
              tips=["Good for blog and product images up to ~1600 px wide.",
                    "Faster pages rank better — 200 KB is a sensible upper bound for web images.",
                    "Choose WebP for your own website if your platform supports it."],
              q=("How small should images be for a website?",
                 "A common rule of thumb is under 200 KB for large hero images and under 100 KB for content images, served at the size they're displayed.")),
    500: dict(who="High-quality photos for email, listings and documents that must stay sharp.",
              tips=["Phone photos (3–10 MB) usually fit at near-original quality around 2000 px.",
                    "Use this before emailing many photos so they don't bounce.",
                    "Great for property, car and marketplace listings that cap file size."],
              q=("Will my phone photo lose quality at 500 KB?",
                 "Hardly noticeably on screens. A 12 MP photo is downscaled to roughly 2000–2500 px, which is still larger than most monitors.")),
}


def img_target_page(kb):
    t = IMG_TARGETS[kb]
    return dict(
        slug=f"resize-image-to-{kb}kb",
        title=f"Resize Image to {kb} KB Online Free — JPG, Exact Size",
        desc=f"Resize or compress a photo or signature to under {kb} KB in one click. Set exact pixel dimensions, keep quality. Free, private — no upload.",
        h1=f"Resize image to {kb} KB",
        lead=f"Make any photo, signature or scan smaller than {kb} KB for online forms — with exact dimensions if you need them. Runs on your device.",
        tool="image", target_kb=kb, crumb=f"Image to {kb} KB",
        facts=[f"Outputs a JPG at or below {kb} KB, using the highest quality that fits.",
               "Optional exact pixel dimensions (e.g. 200×230) with crop-to-fit, and an optional minimum size.",
               "Works with JPG, PNG, WebP and (in Safari) iPhone HEIC photos. Batch + ZIP supported.",
               "Images are processed locally in your browser and never uploaded. EXIF location data is removed."],
        steps=["Choose or drop your photo, signature or scan.",
               f"Keep {kb} KB, or enter the size and dimensions from your form's instructions.",
               "Download the resized JPG and upload it to the form."],
        body=f"""
<h2>Who needs an image under {kb} KB?</h2>
<p>{t['who']}</p>
<h2>Tips for the best result at {kb} KB</h2>
<ul>{''.join(f'<li>{x}</li>' for x in t['tips'])}</ul>
<h2>How it hits {kb} KB</h2>
<p>We binary-search JPEG quality at your chosen dimensions and keep the best quality that is still under {kb} KB. If
even low quality doesn't fit and you haven't fixed the dimensions, we reduce the resolution a step at a time, so you
get a sharper small image rather than a blocky large one.</p>
""",
        faqs=[t["q"], FAQ_IMG_PRIVACY, FAQ_IMG_EXIF,
              ("Is this an official tool for any government or exam portal?",
               "No. It's an independent free tool. Always follow the exact size, dimension and format rules published in your form's instructions.")],
        group="img",
    )


IMG_SIZES = [10, 20, 30, 50, 100, 200, 500]

TOOLS = [
    dict(
        slug="compress-image", tool="image", target_kb=100, crumb="Compress image",
        title="Compress Image to KB Online — Resize JPG, PNG Free",
        desc="Compress JPG, PNG or WebP images to an exact size in KB, with optional pixel dimensions. Batch + ZIP. Free, private, nothing is uploaded.",
        h1="Compress & resize images to any KB",
        lead="Shrink photos, scans and signatures to an exact file size — 20 KB, 50 KB, 100 KB or whatever your form needs.",
        facts=["Exact target size in KB or MB, with an optional minimum.",
               "Optional exact width × height in pixels, with keep-proportions or crop-to-fit.",
               "JPG or WebP output; EXIF location data removed.",
               "Runs locally in the browser — images are never uploaded."],
        steps=["Drop one or more images.", "Set the maximum size (and dimensions if needed).", "Download each image or a ZIP."],
        body="""
<h2>Image size or image dimensions?</h2>
<p><strong>File size</strong> (KB) is how much storage the image takes; <strong>dimensions</strong> (pixels) are its
width and height. Forms often specify both, e.g. “200×230 pixels, 20–50 KB”. Set the dimensions under “Dimensions”
and the size limit at the top — the tool handles both at once.</p>
""",
        faqs=[FAQ_IMG_PRIVACY, FAQ_IMG_EXIF, ("Can I compress PNG screenshots?", "Yes. They're converted to JPG (or WebP), which is far smaller for photos and screenshots. Transparent areas become white.")],
        group="tool",
    ),
    dict(
        slug="merge-pdf", tool="merge", crumb="Merge PDF",
        title="Merge PDF Online Free — No Size Limit, No Upload",
        desc="Combine PDFs into one with no file size or file count limit. Reorder files, keep links and text. Free, runs in your browser — nothing is uploaded.",
        h1="Merge PDF files",
        lead="Combine PDFs into one document in the order you choose — privately, on your device.",
        facts=["Combine any number of PDFs; reorder with the ↑ ↓ buttons or sort by name.",
               "Pages are copied as-is: text, fonts and quality are unchanged.",
               "No file count or size limits beyond your device's memory.",
               "Runs in your browser — files are never uploaded."],
        steps=["Drop the PDFs you want to combine.", "Put them in order with ↑ ↓ (or Sort A→Z).", "Click “Merge PDFs” and download."],
        body="""
<h2>Merge, then compress</h2>
<p>Application portals often want everything in one file under a size limit. Merge your documents here, then use
<a href="/compress-pdf-to-200kb/">Compress PDF to 200 KB</a> (or any size) on the merged file.</p>
""",
        faqs=[("Is there a size limit for merging?", "No fixed limit. Files are merged on your own device, so the only limit is its memory — hundreds of MB work on most computers. Most online mergers cap free files at 25–100 MB because they upload them."),
              ("Will merging reduce quality?", "No. Pages are copied without re-encoding."),
              ("Can I merge password-protected PDFs?", "Not directly — remove the password first in a PDF reader you're authorised to use."), FAQ_PRIVACY],
        group="tool",
    ),
    dict(
        slug="split-pdf", tool="split", crumb="Split PDF",
        title="Split PDF Online Free — Extract Pages, No Upload",
        desc="Extract pages from a PDF or split it into separate files by page or range. Free, unlimited, and private — runs entirely in your browser.",
        h1="Split a PDF or extract pages",
        lead="Pull out just the pages you need, or break a PDF into separate files — without uploading it.",
        facts=["Extract ranges like “1-3, 5, 8-” into a single new PDF.",
               "Or split every page — or every N pages — into separate PDFs, downloaded as a ZIP.",
               "Pages are copied without quality loss.",
               "Runs locally; the PDF is never uploaded."],
        steps=["Drop your PDF.", "Choose “Extract pages” and type the ranges, or choose a split mode.", "Click “Split PDF” and download."],
        body="""
<h2>Useful for</h2>
<ul><li>Uploading only the required pages of a long document to a form.</li>
<li>Getting a long scan under a size limit — split it, then <a href="/">compress</a> each part.</li>
<li>Separating a combined scan of several certificates into individual files.</li></ul>
""",
        faqs=[("How do I write page ranges?", "Use commas and dashes: “1-3, 5, 8-” means pages 1 to 3, page 5, and page 8 to the end."), FAQ_PRIVACY],
        group="tool",
    ),
    dict(
        slug="jpg-to-pdf", tool="img2pdf", crumb="JPG to PDF",
        title="JPG to PDF Converter Free — Unlimited Pages, No Upload",
        desc="Convert JPG, PNG and phone photos into one PDF — 40, 100 or more pages, no limit. A4, Letter or fit-to-image pages. Free, private, in your browser.",
        h1="Convert JPG & images to PDF",
        lead="Turn photos, scans and screenshots into a single, tidy PDF — in your chosen order and page size.",
        facts=["No page limit: combine 40, 100 or more images into one PDF, free.",
               "Supports JPG, PNG, WebP, GIF and iPhone HEIC photos.",
               "A4, US Letter or same-as-image page sizes; landscape images get landscape pages.",
               "Phone photo rotation (EXIF) is applied automatically.",
               "Runs locally; your images are never uploaded."],
        steps=["Drop your images.", "Order them and choose page size, margin and quality.", "Click “Create PDF” and download."],
        body="""
<h2>Photos of documents → one PDF</h2>
<p>Photographed your documents on your phone? Put them into one PDF here, then use
<a href="/compress-pdf-to-100kb/">Compress PDF to 100 KB</a> if a form needs it smaller.</p>
<h2>Need the PDF under a size limit?</h2>
<p>Set “Max PDF size”, or open a ready-made page:
<a href="/jpg-to-pdf-under-20kb/">20 KB</a> · <a href="/jpg-to-pdf-under-40kb/">40 KB</a> · <a href="/jpg-to-pdf-under-50kb/">50 KB</a> ·
<a href="/jpg-to-pdf-under-100kb/">100 KB</a> · <a href="/jpg-to-pdf-under-200kb/">200 KB</a> · <a href="/jpg-to-pdf-under-300kb/">300 KB</a> ·
<a href="/jpg-to-pdf-under-500kb/">500 KB</a> · <a href="/jpg-to-pdf-under-1mb/">1 MB</a>.</p>
""",
        faqs=[("How many images can I convert at once?", "There's no fixed limit — 40, 100 or more images work. Very large batches just take longer and depend on your device's memory."),
              ("Can I make the PDF smaller than a limit?", "Yes. Use JPG to PDF under 50 KB, 100 KB, 200 KB and similar pages, or fill in “Max PDF size”."),
              ("Why is my photo sideways in other converters?", "Phones store rotation as metadata. We apply it before creating the PDF, so pages come out upright."), FAQ_PRIVACY],
        group="tool",
    ),
    dict(
        slug="pdf-to-jpg", tool="pdf2img", crumb="PDF to JPG",
        title="PDF to JPG Converter Free — Every Page as Image, No Upload",
        desc="Convert each PDF page to a JPG or PNG image at 72, 150 or 300 DPI. Download single pages or a ZIP. Free, private, runs in your browser.",
        h1="Convert PDF to JPG images",
        lead="Save every page of a PDF as a high-quality image — for slides, social posts or forms that want JPG.",
        facts=["Choose JPG or lossless PNG.", "72, 150 or 300 DPI output.",
               "Download single pages or all pages as a ZIP.", "Rendered locally with pdf.js — nothing is uploaded."],
        steps=["Drop your PDF.", "Choose format and resolution.", "Click “Convert” and download pages or the ZIP."],
        body="""
<h2>Which resolution should I choose?</h2>
<ul><li><strong>72 DPI</strong> — small files for previews and messaging.</li>
<li><strong>150 DPI</strong> — sharp on screens; good default.</li>
<li><strong>300 DPI</strong> — print quality; large files.</li></ul>
<p>Need the image under a size limit? Run it through <a href="/resize-image-to-50kb/">Resize image to 50 KB</a>.</p>
""",
        faqs=[("Can I convert a password-protected PDF?", "Only PDFs that open without a password."), FAQ_PRIVACY],
        group="tool",
    ),
]

# ================================================================ company / compliance
ABOUT = dict(
    slug="about", tool=False, crumb="About", group="legal",
    title="About — Free, Private PDF & Image Tools",
    desc="Why we build free PDF and image tools that run in your browser instead of on our servers.",
    h1="About", lead="Free document tools that respect your privacy by design.",
    facts=["Independent project; not affiliated with any government, exam body or software company.",
           "Every tool runs locally in your browser — we never receive your files.",
           "Built on open-source libraries: pdf-lib, pdf.js, pako and JSZip."],
    steps=None, faqs=[],
    body="""
<h2>A hobby project</h2>
<p>This site is a personal hobby project — free, with no ads, no accounts and no paid tier. It's offered “as is”,
without any warranty; see the <a href="/terms/#disclaimer">terms</a>.</p>
<h2>Why we built this</h2>
<p>Millions of people every day need to shrink a document or photo to fit an upload limit. The popular tools make
you upload personal documents to a server, then limit you to a couple of files a day. Modern browsers are powerful
enough to do the work themselves — so ours do. That keeps your files private and lets us offer the tools free with
no limits.</p>
<h2>Accuracy</h2>
<p>Size limits on this site are examples. Always follow the instructions published by the organization you're
submitting to. If you spot an error, please <a href="/contact/">tell us</a>.</p>
""",
)
CONTACT = dict(
    slug="contact", tool=False, crumb="Contact", group="legal",
    title="Contact", desc="How to contact us about the tools, privacy, or a problem with a file.",
    h1="Contact", lead="Questions, bug reports, privacy requests or feedback — we read everything.",
    facts=["Email: {{CONTACT}}", "We never ask for your documents by email — please don't send personal files.",
           "Privacy and grievance requests are answered within 30 days."],
    steps=None, faqs=[],
    body="""
<h2>Reporting a problem</h2>
<p>Tell us your browser and device, the tool you used and what happened. If a specific PDF fails, describe it
(page count, how it was created) rather than attaching it — unless it contains nothing personal.</p>
<h2>Grievance officer / privacy contact</h2>
<p>For requests under the GDPR, UK GDPR, CCPA/CPRA or India's Digital Personal Data Protection Act 2023, write to
{{CONTACT}} with the subject “Privacy request”.</p>
""",
)
TERMS = dict(
    slug="terms", tool=False, crumb="Terms", group="legal",
    title="Terms of Use", desc="Terms of use for the free PDF and image tools.",
    h1="Terms of use", lead="Plain-language terms. By using the site you agree to them.",
    facts=["Free to use for personal and commercial purposes.",
           "A personal hobby project, provided free and “as is”, without warranty of any kind — keep your original files.",
           "You are responsible for having the right to process the files you use.",
           "Not affiliated with any government, exam body or third-party brand mentioned."],
    steps=None, faqs=[],
    body="""
<h2>1. The service</h2><p>The tools run in your web browser. We do not receive, store or process the files you
select. Output is generated on your device.</p>
<h2>2. Acceptable use</h2><p>Use the tools only with files you own or are authorised to process. Don't use them to
infringe copyright, to circumvent security measures or access controls you aren't authorised to remove, or to create
forged or fraudulent documents.</p>
<h2 id="disclaimer">3. Hobby project — no warranty</h2>
<p>This site is a <strong>personal hobby project</strong>, built and run in spare time. It is not a commercial service
and comes with no support commitment, uptime guarantee or service-level agreement.</p>
<p>The tools are provided <strong>“as is” and “as available”, without warranty of any kind</strong>, express or implied —
including any warranty of merchantability, fitness for a particular purpose, accuracy, or non-infringement. There is
no guarantee that a tool will work for your file, that the output will meet a form's or authority's requirements, or
that size limits, dimensions and other figures shown on the site are correct for your situation.</p>
<p>Compression and conversion can change how a document looks. Always check the output and keep your original
file. You use the site at your own risk. To the extent permitted by law, the author is not liable for any direct or
indirect loss arising from use of the site — including lost or damaged files, rejected uploads, missed deadlines or
rejected applications.</p>
<h2>4. Third parties and trademarks</h2><p>Names of services such as Gmail, Outlook, iPhone, Android, macOS or
Windows are used only to describe compatibility. They are trademarks of their respective owners, who do not endorse
this site. Size limits mentioned for forms are examples, not official requirements.</p>
<h2>5. Open-source software</h2><p>The site includes open-source components under their own licenses; see
<a href="/licenses/">Open-source licenses</a>.</p>
<h2>6. Changes</h2><p>We may update these terms; the date below shows the latest version.</p>
<h2>7. Contact</h2><p>{{CONTACT}}</p>
""",
)
LICENSES = dict(
    slug="licenses", tool=False, crumb="Open-source licenses", group="legal",
    title="Open-Source Licenses", desc="Open-source software used by this site and its licenses.",
    h1="Open-source licenses", lead="This site is built on excellent open-source projects. Thank you to their authors.",
    facts=["pdf.js — Apache License 2.0 — © Mozilla Foundation and contributors.",
           "pdf-lib — MIT License — © Andrew Dillon.",
           "pako — MIT License (and zlib license for ported code) — © Vitaly Puzrin, Andrei Tuputcyn.",
           "JSZip — used under the MIT License (dual-licensed MIT/GPLv3) — © Stuart Knightley and contributors.",
           "@cantoo/pdf-lib — MIT License — fork of pdf-lib with encryption support (used to unlock PDFs).",
           "libheif-js — LGPL-3.0 — libheif (with libde265) compiled to WebAssembly, used to open iPhone HEIC photos.",
           "UPNG.js — MIT License — © Photopea (Ivan Kutskir).",
           "tesseract.js and tesseract.js-core — Apache License 2.0; Tesseract OCR and the English language data — Apache License 2.0."],
    steps=None, faqs=[],
    body="""
<h2>Full license texts</h2>
<ul>
<li><a href="/vendor/licenses/pdfjs-LICENSE.txt">pdf.js — Apache License 2.0</a> (unmodified distribution build, v4.10.38)</li>
<li><a href="/vendor/licenses/pdf-lib-LICENSE.txt">pdf-lib — MIT License</a> (v1.17.1)</li>
<li><a href="/vendor/licenses/pako-LICENSE.txt">pako — MIT License</a> (v2.1.0)</li>
<li><a href="/vendor/licenses/jszip-LICENSE.txt">JSZip — MIT / GPLv3 dual license</a> (v3.10.1, used under MIT)</li>
<li><a href="/vendor/licenses/pdf-lib-cantoo-LICENSE.txt">@cantoo/pdf-lib — MIT License</a> (v2.11.1)</li>
<li><a href="/vendor/licenses/upng-LICENSE.txt">UPNG.js — MIT License</a> (v2.1.0)</li>
<li><a href="/vendor/licenses/tesseract.js-LICENSE.txt">tesseract.js — Apache License 2.0</a> (v7.0.0, with tesseract.js-core v7.0.0 and Tesseract English data, Apache 2.0)</li>
<li><a href="/vendor/licenses/libheif-js-LICENSE.txt">libheif-js — LGPL-3.0</a> (v1.19.8, WebAssembly bundle)</li>
</ul>
<h2>LGPL components</h2>
<p>libheif-js packages <a href="https://github.com/strukturag/libheif">libheif</a> and
<a href="https://github.com/strukturag/libde265">libde265</a>, licensed under the
<a href="/vendor/licenses/lgpl-3.0.txt">GNU Lesser General Public License v3.0</a> (which incorporates the
<a href="/vendor/licenses/gpl-3.0.txt">GNU GPL v3.0</a>). They are shipped unmodified as a separate file,
<a href="/vendor/libheif-bundle.js">/vendor/libheif-bundle.js</a>, which you may replace with your own build. Their
source code is available from the projects linked above and from the
<a href="https://github.com/catdad-experiments/libheif-js">libheif-js repository</a>.</p>
""",
)
ACCESSIBILITY = dict(
    slug="accessibility", tool=False, crumb="Accessibility", group="legal",
    title="Accessibility Statement", desc="Our commitment to WCAG 2.1 AA accessibility for the PDF and image tools.",
    h1="Accessibility statement", lead="We aim for the tools to be usable by everyone, conforming to WCAG 2.1 level AA.",
    facts=["Everything works with a keyboard: Tab to the upload area and press Enter or Space.",
           "Status updates are announced to screen readers through live regions.",
           "Text and controls meet AA colour-contrast ratios in light and dark mode.",
           "Pages respect reduced-motion and dark-mode system settings and reflow to 320 px wide."],
    steps=None, faqs=[],
    body="""
<h2>Known limitations</h2>
<p>Image previews of converted PDF pages don't include the page text. Compressed PDFs keep the original's tagging,
but flattened pages (used only as a last resort for exact sizes) are images and lose text accessibility — the tool
warns you when this happens.</p>
<h2>Feedback</h2><p>If anything is hard to use, please contact {{CONTACT}}. We aim to respond within 5 working days.</p>
""",
)
PRIVACY_PAGE.update(
    title="Privacy Policy — Files Never Leave Your Device",
    desc="Privacy policy: files are processed locally in your browser and never uploaded. No cookies. GDPR, CCPA and DPDP Act information.",
    facts=["Files you select are processed entirely in your browser and are never transmitted to us or anyone else.",
           "We set no cookies and run no advertising or cross-site tracking.",
           "We count anonymous, cookie-less usage events (e.g. “a PDF was compressed”) — never files, file names or IP addresses. Do-Not-Track and Global Privacy Control are honoured.",
           "Contact for privacy requests: {{CONTACT}}."],
    body="""
<h2>1. Files</h2><p>When you select a file, it is read into your browser's memory, processed there, and offered back
to you as a download. Nothing is uploaded. Closing or reloading the tab discards it. You can verify this in your
browser's developer tools (Network tab).</p>
<h2>2. Data we collect</h2>
<p><strong>Server logs:</strong> our hosting provider (a CDN) processes standard request data such as IP address,
user agent and requested URL to deliver pages and protect against abuse, typically retained for a short period.</p>
<p><strong>Usage events:</strong> when you use a tool, your browser sends an anonymous event to our own endpoint:
the tool used (for example “a PDF was compressed”), the page, the settings chosen (such as the target size), the
outcome (such as percentage saved, whether the target was met, or a short error type) and your approximate country
as determined by our CDN. We do not store IP addresses, files, file names or any identifier, and events cannot be
linked to each other or to you. They are kept for up to about 3 months in Cloudflare Workers Analytics Engine and
briefly in Cloudflare's logs. If your browser sends a Do-Not-Track or Global Privacy Control signal, no events are
sent at all.</p>
<p><strong>Visit statistics (if enabled):</strong> Cloudflare Web Analytics counts page views without cookies or
fingerprinting. No personal profiles are built and no data is sold or shared for advertising.</p>
<h2>3. Cookies and local storage</h2><p>We don't use cookies. The browser caches the app's code (a service worker) so
it works offline; it contains no personal data and can be cleared in your browser settings.</p>
<h2>4. Legal basis and your rights</h2>
<p>Under the GDPR/UK GDPR, minimal server logs and aggregate analytics are processed on the basis of legitimate
interests (running and improving a free service). You have the right to access, rectify, erase, restrict or object
to processing and to complain to your data-protection authority. California residents have rights under the
CCPA/CPRA; we do not sell or share personal information. Users in India have rights under the Digital Personal Data
Protection Act 2023, including the right to grievance redressal. Contact {{CONTACT}}.</p>
<h2>5. Children</h2><p>The site is a general-audience utility and does not knowingly collect data from children.</p>
<h2>6. Advertising</h2><p>The site currently shows no ads. If that changes, this policy will be updated first and,
where required, we will ask for your consent before any advertising cookies are used.</p>
<h2>7. Changes</h2><p>The date below shows the latest version of this policy.</p>
""",
)


def all_pages():
    pages = ([HOME] + TOOLS + [img_target_page(k) for k in IMG_SIZES] + [target_page(k) for k in SIZES] +
             USE_CASES + DEVICES + GUIDES + [ABOUT, CONTACT, PRIVACY_PAGE, TERMS, LICENSES, ACCESSIBILITY])
    for p in pages:
        p.setdefault("tool", "compress")
        if p["tool"] is True:
            p["tool"] = "compress"
        p.setdefault("mode", "target" if p.get("target_kb") else "recommended")
    return pages


# ================================================================ tier 1 + 2 tools
FAQ_FORM_RULES = ("Which size should I choose for my form?",
                  "Always use the exact numbers printed in your application's instructions or official notification — "
                  "pixels or cm, DPI, minimum and maximum KB, and format. The presets here are only common examples.")
FAQ_PDF_PRIVATE = ("Is my PDF uploaded?", "No. The PDF is opened and edited inside your browser; it never leaves your device.")


def _tool(slug, tool, crumb, title, desc, h1, lead, facts, steps, body, faqs, cat, **extra):
    d = dict(slug=slug, tool=tool, crumb=crumb, title=title, desc=desc, h1=h1, lead=lead, facts=facts, steps=steps,
             body=body, faqs=faqs, group="tool", cat=cat)
    d.update(extra)
    return d


NEW_TOOLS = [
    # ---------------------------------------------------------------- tier 1: forms & images
    _tool("photo-signature-resizer", "image", "Photo & signature resizer",
          "Photo & Signature Resizer for Exam Forms — KB, cm, DPI",
          "Resize your photo and signature for online exam and job forms: exact KB, pixel or cm size, DPI, and name & date on the photo. Free, no upload.",
          "Photo & signature resizer for online forms",
          "Get your photo and signature exactly right for exam, job and scholarship applications — file size, dimensions, DPI and format in one step.",
          ["Sets maximum and minimum KB, exact dimensions in px, cm, mm or inches, and DPI together.",
           "Can print your name and the photo date on the photo when a form asks for it.",
           "Outputs JPG by default — the format nearly every application portal accepts.",
           "Runs in your browser: your photo and signature are never uploaded."],
          ["Read the photo and signature rules in your application's instructions.",
           "Drop the photo, set its size limit and dimensions (use a preset as a starting point), download.",
           "Repeat for the signature with its own limits."],
          """
<h2>Why uploads get rejected</h2>
<ul><li><strong>File size</strong> outside the allowed range — too big <em>or</em> too small (many forms have a minimum).</li>
<li><strong>Wrong dimensions</strong> — the form checks pixel width and height, or cm at a stated DPI.</li>
<li><strong>Wrong format</strong> — PNG or HEIC (iPhone) instead of JPG.</li>
<li><strong>Missing name/date</strong> — some recruitment forms require them printed on the photo.</li></ul>
<p>This tool handles all four at once. For signatures, sign in black ink on plain white paper and crop tightly.</p>
""",
          [FAQ_FORM_RULES, ("Can I convert an iPhone (HEIC) photo?", "Yes — HEIC photos are converted automatically and saved as JPG."), FAQ_IMG_PRIVACY],
          "form", target_kb=50, img=dict(presets="exam", open=True)),
    _tool("add-name-and-date-on-photo", "image", "Name & date on photo",
          "Add Name and Date on Photo Online — For Exam Application Forms",
          "Print your name and the photo date at the bottom of your photograph, as some exam and recruitment forms require. Exact KB and size. Free, private.",
          "Add name and date on your photo",
          "Some recruitment and exam applications require the candidate's name and the date the photo was taken printed on the photo. Do it here in seconds.",
          ["Adds a white band at the bottom with your name and date in clear black text.",
           "Choose the date format your form wants (DD-MM-YYYY, DD/MM/YYYY and more).",
           "Keeps the final size within your KB limit and exact dimensions.",
           "Processed on your device — your photo is never uploaded."],
          ["Drop your photo.", "Type your name and pick the photo date and format.", "Set the size limit and dimensions from your form, then download."],
          """
<h2>Tips</h2>
<ul><li>Use the date the photo was <em>taken</em>, and make sure it's recent enough for your form's rules.</li>
<li>Use the same spelling of your name as in your application.</li>
<li>Check the preview: the text must be readable, and your face must still fill most of the photo.</li></ul>
""",
          [FAQ_FORM_RULES, ("Will the text make my face smaller?", "The photo is cropped to fill the area above the band, so your face stays large; choose “Crop to exact size” to keep exact dimensions."), FAQ_IMG_PRIVACY],
          "form", target_kb=50, img=dict(presets="exam", text=True)),
    _tool("resize-image-in-cm", "image", "Resize in cm / mm",
          "Resize Image in cm, mm or Inches (with DPI) — Free Online",
          "Resize a photo to an exact size in centimetres, millimetres or inches at the DPI you need, e.g. 3.5 × 4.5 cm at 200 DPI. Free and private.",
          "Resize an image in cm, mm or inches",
          "Forms and printers often give sizes in cm and DPI instead of pixels. Enter them directly — we do the maths and write the DPI into the file.",
          ["Converts cm/mm/inches to pixels at your DPI (pixels = cm ÷ 2.54 × DPI).",
           "Writes the DPI into the JPG or PNG so print and form checks read the right physical size.",
           "Optional maximum KB at the same time.",
           "Runs locally — nothing is uploaded."],
          ["Drop your image.", "Enter width and height, choose cm/mm/inch and the DPI.", "Download — the file has the exact size and DPI."],
          """
<h2>Quick reference at 200 DPI</h2>
<div class="tablewrap"><table><thead><tr><th>Physical size</th><th>Pixels at 200 DPI</th><th>Pixels at 300 DPI</th></tr></thead><tbody>
<tr><td>3.5 × 4.5 cm</td><td>276 × 354</td><td>413 × 531</td></tr>
<tr><td>2 × 2 in</td><td>400 × 400</td><td>600 × 600</td></tr>
<tr><td>3.5 × 1.5 cm</td><td>276 × 118</td><td>413 × 177</td></tr>
</tbody></table></div>
""",
          [("What DPI should I use?", "Use the DPI stated in your form or by your printer. If none is stated, 200 DPI is common for online forms and 300 DPI for printing."), FAQ_IMG_PRIVACY],
          "form", img=dict(presets="exam", unit="cm")),
    _tool("passport-size-photo-resize", "image", "Passport-size photo",
          "Passport Size Photo Resizer — 3.5×4.5 cm, 2×2 in, Free",
          "Resize a photo to passport size (3.5 × 4.5 cm, 35 × 45 mm or 2 × 2 in) at 300 DPI, with an optional KB limit. Free, private, no upload.",
          "Passport-size photo resizer",
          "Crop and resize your photo to common passport-photo sizes for online applications — in your browser.",
          ["Presets for 3.5 × 4.5 cm, 35 × 45 mm, 2 × 2 in and 51 × 51 mm at 300 DPI.",
           "Crops to the exact shape so nothing is stretched.",
           "Optional maximum KB for online upload limits.",
           "Your photo is never uploaded."],
          ["Drop a well-lit, front-facing photo with a plain background.", "Pick a preset (or enter your size).", "Download the JPG."],
          """
<h2>Passport photo width and height (cm, mm, inches and pixels)</h2>
<div class="tablewrap"><table><thead><tr><th>Size (width × height)</th><th>In inches</th><th>Pixels at 200 DPI</th><th>Pixels at 300 DPI</th><th>Commonly used for</th></tr></thead><tbody>
<tr><td>3.5 × 4.5 cm (35 × 45 mm)</td><td>1.38 × 1.77 in</td><td>276 × 354</td><td>413 × 531</td><td>India, UK, Schengen and many other countries</td></tr>
<tr><td>2 × 2 in (51 × 51 mm)</td><td>2 × 2 in</td><td>400 × 400</td><td>600 × 600</td><td>US passport and visa</td></tr>
<tr><td>3.3 × 4.8 cm (33 × 48 mm)</td><td>1.30 × 1.89 in</td><td>260 × 378</td><td>390 × 567</td><td>China visa</td></tr>
<tr><td>5 × 7 cm</td><td>1.97 × 2.76 in</td><td>394 × 551</td><td>591 × 827</td><td>Some application forms</td></tr>
</tbody></table></div>
<p class="muted small">Pixels = size in inches × DPI (1 inch = 2.54 cm). Rules change — always confirm the size with the
official guidelines for your application.</p>
<h2>Before you start</h2>
<p>Official passport and visa photos have strict rules on background colour, head size, expression and age of the
photo. This tool handles size and file format; check the issuing authority's photo guidelines for everything else,
and use a professional studio where the authority requires one.</p>
""",
          [("What is the width and height of a passport size photo?", "The most common size is 3.5 cm wide × 4.5 cm high (35 × 45 mm), which is 413 × 531 pixels at 300 DPI. The US uses 2 × 2 inches (600 × 600 pixels at 300 DPI)."),
           ("Is this an official passport photo service?", "No. It's an independent resizing tool. Requirements vary by country and application — always follow the official guidelines."), FAQ_IMG_PRIVACY],
          "form", img=dict(presets="passport", unit="cm")),
    _tool("change-image-dpi", "dpi", "Change image DPI",
          "Change Image DPI Online (DPI Changer) — 72, 200, 300 DPI",
          "Set the DPI of a JPG or PNG to 72, 150, 200, 300 or any value without changing its pixels or quality. Free, instant, no upload.",
          "Change image DPI",
          "Set a photo's DPI (dots per inch) to the value a form or printer asks for — without touching a single pixel.",
          ["Changes only the DPI stored in the file (JFIF/EXIF for JPG, pHYs for PNG) — no quality loss.",
           "Pixel dimensions and file size stay the same.",
           "Batch-change many images and download a ZIP.",
           "Processed on your device."],
          ["Drop JPG or PNG images.", "Choose the DPI (e.g. 200 or 300).", "Download — done."],
          """
<h2>What DPI actually changes</h2>
<p>DPI is a label that tells printers and some form checkers how large the image is physically. A 600 × 600 px
photo is 2 × 2 inches at 300 DPI, or about 8.3 × 8.3 inches at 72 DPI — the pixels are identical. If you need a
specific physical size, use <a href="/resize-image-in-cm/">Resize in cm</a> instead, which sets both pixels and DPI.</p>
""",
          [("How do I change the DPI of a photo to 200 or 300?", "Drop the photo, type 200 or 300 (or tap a preset) and download. The DPI is changed instantly without re-saving the image."),
           ("Does changing DPI reduce quality?", "No. Only the stored DPI value changes; the image data is untouched."),
           ("Why does my form say the DPI is wrong?", "Phones usually save photos at 72 DPI. Many forms ask for 200 or 300 DPI — changing it here fixes that. If the form also gives a size in cm, use Resize in cm so the pixels match too."),
           FAQ_IMG_PRIVACY],
          "image"),
    _tool("jpg-to-pdf-under-100kb", "img2pdf", "JPG to PDF under 100 KB",
          "JPG to PDF Under 100 KB — Combine Images, Exact Size",
          "Turn one or more photos or scans into a single PDF under 100 KB for online forms. Order pages, pick A4. Free and private — no upload.",
          "JPG to PDF under 100 KB",
          "Many forms want documents as one PDF under 100 KB. Add your photos or scans and get a PDF that fits — in one step.",
          ["Combines images into one PDF, then compresses it to under 100 KB automatically.",
           "Counts 1 KB as 1000 bytes so the file passes either convention.",
           "A4, Letter or fit-to-image pages; phone photo rotation fixed automatically.",
           "Runs locally — documents are never uploaded."],
          ["Drop your images (certificate pages, ID front and back…).", "Order them; the 100 KB limit is pre-set.", "Click “Create PDF” and download."],
          """
<h2>Tips to fit 100 KB</h2>
<ul><li>Crop photos to the document edges before adding them.</li><li>Use 1–2 pages; each extra page shares the same 100 KB.</li>
<li>Choose “Small file” quality for text documents.</li></ul>
""",
          [("What if it can't reach 100 KB?", "You'll see a message. Use fewer pages, crop the images, or choose “Small file” quality and try again."), FAQ_IMG_PRIVACY],
          "form", pdf_max_kb=100),
    _tool("jpg-to-pdf-under-200kb", "img2pdf", "JPG to PDF under 200 KB",
          "JPG to PDF Under 200 KB — Photos to One Small PDF",
          "Combine photos or scanned pages into one PDF under 200 KB for application uploads. Reorder pages, A4 or Letter. Free, private, in your browser.",
          "JPG to PDF under 200 KB",
          "Merge your document photos into one PDF that's guaranteed under 200 KB when possible — no separate compress step.",
          ["Builds the PDF, then compresses it to fit 200 KB.",
           "3–4 scanned pages typically fit at readable quality.",
           "Rotation from phone cameras is applied automatically.",
           "Your images never leave your device."],
          ["Drop your images.", "Arrange the order; 200 KB is pre-set.", "Create and download the PDF."],
          """
<h2>Good for</h2><ul><li>Marksheets and certificates that must be one PDF.</li><li>ID proof front + back in one file.</li><li>Supporting documents for visa and university forms.</li></ul>
""",
          [("Can I change the limit?", "Yes — edit “Max PDF size” to any value, or clear it for no limit."), FAQ_IMG_PRIVACY],
          "form", pdf_max_kb=200),
    _tool("heic-to-jpg", "image", "HEIC to JPG",
          "HEIC to JPG Converter — iPhone Photos to JPG Free",
          "Convert iPhone HEIC photos to JPG in your browser so forms and Windows can open them. Batch convert, optional size limit. Free, private.",
          "Convert HEIC to JPG",
          "iPhone photos are saved as HEIC, which many websites and forms reject. Convert them to JPG here — without uploading them.",
          ["Converts HEIC/HEIF photos to JPG (or PNG/WebP).",
           "Batch-convert many photos and download a ZIP.",
           "Optional maximum KB and dimensions in the same step.",
           "Location (GPS) data is not carried over to the JPG."],
          ["Drop your HEIC photos.", "Keep JPG and choose quality (or set a KB limit).", "Download the JPGs."],
          """
<h2>Stop your iPhone saving HEIC</h2>
<p>On iPhone go to <em>Settings → Camera → Formats</em> and choose <em>Most Compatible</em> to save new photos as JPG.
Photos shared by AirDrop or email can also be sent as JPG automatically.</p>
""",
          [("Why does conversion take a few seconds?", "HEIC decoding runs in your browser instead of on a server, which keeps your photos private."), FAQ_IMG_PRIVACY],
          "image", img=dict(fmt="jpg", q="0.95")),
    _tool("png-to-jpg", "image", "PNG to JPG",
          "PNG to JPG Converter — Free, Batch, No Upload",
          "Convert PNG images and screenshots to JPG, usually 5–10× smaller. Transparent areas become white. Batch + ZIP. Free and private.",
          "Convert PNG to JPG",
          "Turn PNG screenshots and images into compact JPGs that every form and website accepts.",
          ["PNG photos and screenshots usually shrink 5–10× as JPG.", "Transparent areas are filled with white.",
           "Batch convert and download a ZIP.", "Processed locally in your browser."],
          ["Drop PNG files.", "Choose quality (or a KB limit).", "Download the JPGs."],
          """<h2>When to keep PNG</h2><p>Keep PNG for logos, icons and images that need transparency or crisp flat colours. For photos and screenshots you upload to forms, JPG is smaller and universally accepted.</p>""",
          [("Will text in screenshots stay sharp?", "At “High” quality, yes. Lower settings shrink the file more but can blur small text."), FAQ_IMG_PRIVACY],
          "image", img=dict(fmt="jpg", q="0.95")),
    _tool("webp-to-jpg", "image", "WebP to JPG",
          "WebP to JPG Converter — Free Online, No Upload",
          "Convert WebP images saved from websites into JPG files that open everywhere. Batch convert, optional size limit. Free, private.",
          "Convert WebP to JPG",
          "Images saved from the web are often WebP, which some apps and forms can't open. Convert them to JPG in one click.",
          ["Converts WebP (including transparent WebP) to JPG.", "Batch + ZIP download.", "Optional KB limit and dimensions.", "Runs in your browser."],
          ["Drop WebP images.", "Keep JPG and choose quality.", "Download."],
          """<h2>About WebP</h2><p>WebP is a modern web format that's smaller than JPG, but older software and many upload forms still expect JPG. Converting is quick and keeps the visible quality.</p>""",
          [("Can I convert to PNG instead?", "Yes — change Format to PNG to keep transparency."), FAQ_IMG_PRIVACY],
          "image", img=dict(fmt="jpg", q="0.95")),
    _tool("jpg-to-png", "image", "JPG to PNG",
          "JPG to PNG Converter — Free Online, No Upload",
          "Convert JPG photos to PNG in your browser. Lossless PNG by default, batch + ZIP, optional resizing. Free and private.",
          "Convert JPG to PNG",
          "Need a PNG for a design tool or document? Convert JPG images to PNG without uploading them.",
          ["Lossless PNG output by default.", "Batch convert and download a ZIP.", "Optional resizing and DPI.", "Processed locally."],
          ["Drop JPG files.", "Keep “High / lossless”.", "Download the PNGs."],
          """<h2>Heads-up on file size</h2><p>PNG is lossless, so photos usually get <em>bigger</em> as PNG. If you need a small file for a form, keep JPG and use <a href="/compress-jpeg/">Compress JPEG</a> instead.</p>""",
          [("Does converting to PNG improve quality?", "No — it preserves the JPG exactly as it is; it can't restore detail already lost."), FAQ_IMG_PRIVACY],
          "image", img=dict(fmt="png", q="0.95")),
    _tool("compress-jpeg", "image", "Compress JPEG",
          "Compress JPEG Online — Reduce JPG File Size Free",
          "Reduce JPG file size by 50–90% with adjustable quality or an exact KB target. Batch + ZIP, EXIF location removed. Free, private, no upload.",
          "Compress JPEG images",
          "Shrink photos for email, websites and forms — choose a quality level or an exact size.",
          ["Typical phone photos shrink 70–90% with no visible difference on screen.", "Quality levels or an exact KB/MB target.",
           "Batch + ZIP download; EXIF location data removed.", "Runs in your browser."],
          ["Drop JPG photos.", "Pick a quality level, or enter a maximum size.", "Download."],
          """<h2>Why phone photos are so big</h2><p>Phone cameras save 12–48 megapixel images at very high quality. Websites and forms display them far smaller, so re-encoding at a sensible size and quality saves most of the bytes.</p>""",
          [("What's the best quality setting?", "“Balanced” is visually indistinguishable for most photos. Use “High” for printing and “Small file” for web uploads."), FAQ_IMG_EXIF],
          "image", img=dict(fmt="jpg")),
    _tool("compress-png", "image", "Compress PNG",
          "Compress PNG Online — Smaller PNG, Keeps Transparency",
          "Reduce PNG file size by 50–80% with colour quantisation while keeping transparency. Batch + ZIP. Free, private, runs in your browser.",
          "Compress PNG images",
          "Make PNG screenshots, logos and graphics much smaller while keeping transparency — no upload.",
          ["Smart colour reduction (palette quantisation) — usually 50–80% smaller.", "Transparency is preserved.",
           "Choose a quality level or an exact KB target.", "Processed locally."],
          ["Drop PNG files.", "Pick a quality level (Balanced is a good start).", "Download the smaller PNGs."],
          """<h2>How PNG compression works</h2><p>PNG is lossless, so the big savings come from reducing the number of colours to a smart palette — almost invisible for screenshots, logos and illustrations. For photographs, <a href="/png-to-jpg/">converting to JPG</a> saves even more.</p>""",
          [("Will my transparent background stay?", "Yes — PNG output keeps the alpha channel."), FAQ_IMG_PRIVACY],
          "image", img=dict(fmt="png")),
    # ---------------------------------------------------------------- tier 2: PDF
    _tool("rotate-pdf", "organize", "Rotate PDF",
          "Rotate PDF Pages Online — Free, Permanent, No Upload",
          "Rotate all or individual PDF pages left or right and save the PDF permanently. See page thumbnails. Free, private — runs in your browser.",
          "Rotate PDF pages",
          "Fix sideways or upside-down scans: rotate every page or just the ones that need it, then save.",
          ["Rotate all pages at once or page by page, with thumbnails.", "Rotation is saved in the PDF permanently.",
           "Text, links and quality are untouched.", "Your PDF never leaves your device."],
          ["Drop your PDF.", "Use ⟲ / ⟳ on single pages or “Rotate all”.", "Click “Save PDF” and download."],
          """<h2>Also on this page</h2><p>The same editor lets you <a href="/delete-pdf-pages/">delete pages</a> and <a href="/rearrange-pdf-pages/">reorder pages</a> before saving.</p>""",
          [("Does rotating reduce quality?", "No — only the page's rotation setting changes."), FAQ_PDF_PRIVATE],
          "pdf"),
    _tool("delete-pdf-pages", "organize", "Delete PDF pages",
          "Delete Pages from PDF Online — Free, No Upload",
          "Remove unwanted pages from a PDF by clicking them or typing ranges like 2, 5-7. Thumbnails, undo, instant download. Free and private.",
          "Delete pages from a PDF",
          "Remove blank, duplicate or unwanted pages — click them, or type the page numbers.",
          ["Click ✕ on any page, or type ranges like “2, 5-7”.", "Deleted pages are shown greyed out until you save — click ↺ to restore.",
           "Remaining pages keep their quality, text and links.", "Runs locally."],
          ["Drop your PDF.", "Mark pages to delete.", "Save and download."],
          """<h2>Make it smaller too</h2><p>Removing pages is the fastest way to shrink a PDF. Still too big? Run the result through <a href="/">Compress PDF</a>.</p>""",
          [("Can I undo a deletion?", "Yes — until you save, click ↺ on the page or “Reset”."), FAQ_PDF_PRIVATE],
          "pdf"),
    _tool("rearrange-pdf-pages", "organize", "Rearrange PDF pages",
          "Rearrange PDF Pages — Reorder, Move & Reverse Free",
          "Change the order of pages in a PDF with ← → buttons and thumbnails, or reverse the whole document. Free, private, in your browser.",
          "Rearrange PDF pages",
          "Put scanned pages in the right order, move a page to the end, or reverse the whole file.",
          ["Move pages with ← → and see thumbnails as you go.", "One-click “Reverse order” for back-to-front scans.",
           "Combine with rotate and delete in the same step.", "Your PDF is never uploaded."],
          ["Drop your PDF.", "Move pages into the order you want.", "Save and download."],
          """<h2>Combining several PDFs?</h2><p>Use <a href="/merge-pdf/">Merge PDF</a> first, then reorder the pages of the merged file here.</p>""",
          [("Is drag-and-drop supported?", "Use the ← → buttons on each page — they also work with a keyboard and on phones."), FAQ_PDF_PRIVATE],
          "pdf"),
    _tool("add-page-numbers-to-pdf", "pagenum", "Add page numbers",
          "Add Page Numbers to PDF — Free, Choose Position & Style",
          "Number the pages of a PDF: choose position, format (1, Page 1, 1 / 10, Page 1 of 10), start number and skip the cover. Free, no upload.",
          "Add page numbers to a PDF",
          "Add clean page numbers to reports, theses and applications — positioned exactly where you want them.",
          ["Six positions: top or bottom, left, centre or right.", "Formats: 1 · Page 1 · 1 / N · Page 1 of N.",
           "Start from any number and optionally skip the cover page.", "Rotated pages are numbered the right way up."],
          ["Drop your PDF.", "Choose position, format and start number.", "Add numbers and download."],
          """<h2>Tip</h2><p>Merging documents? <a href="/merge-pdf/">Merge</a> them first so the numbering runs continuously across the whole file.</p>""",
          [("Can I start numbering at page 2?", "Tick “Don't number the first page” — the second page becomes 1 (or your start number)."), FAQ_PDF_PRIVATE],
          "pdf"),
    _tool("watermark-pdf", "watermark", "Watermark PDF",
          "Watermark PDF Online — Add Text Watermark Free",
          "Stamp CONFIDENTIAL, DRAFT, COPY or your own text across every page of a PDF. Choose size, colour, opacity and angle. Free, private.",
          "Add a watermark to a PDF",
          "Mark documents as CONFIDENTIAL, DRAFT or “Copy for KYC only” before you share them.",
          ["Any text, diagonal or horizontal, on every page.", "Choose colour, size and opacity.",
           "Good practice for ID copies: write who it's for and why (e.g. “For XYZ Bank KYC only”).", "Runs locally."],
          ["Drop your PDF.", "Type the watermark text and choose its look.", "Add and download."],
          """<h2>Protect copies of your ID</h2><p>When you share a copy of an ID or bank statement, a watermark stating the purpose and recipient makes misuse much harder. Make the text specific: “Submitted to ABC Ltd for address proof — 10/10/2026”.</p>""",
          [("Can a watermark be removed?", "Someone with PDF editing software can remove a text watermark, so it deters casual misuse rather than guaranteeing security."), FAQ_PDF_PRIVATE],
          "pdf"),
    _tool("sign-pdf", "sign", "Sign PDF",
          "Sign PDF Online Free — Draw, Type or Upload Signature",
          "Add your signature to a PDF: draw it, type it or upload an image, then click to place it on any page. Free, private — never uploaded.",
          "Sign a PDF",
          "Draw, type or upload your signature and place it anywhere on the document — all on your device.",
          ["Draw with a mouse, finger or stylus; type your name; or upload a photo of your signature.",
           "White backgrounds are removed from uploaded signatures automatically.",
           "Place as many signatures as you need, on any pages.", "Your document and signature never leave your device."],
          ["Drop the PDF and create your signature.", "Pick the page and click where the signature goes.", "Save and download the signed PDF."],
          """<h2>Is this a legally binding e-signature?</h2><p>This adds a visual signature image — the same as signing a printout and scanning it. That's accepted for many everyday documents, but some contracts and official filings require a certified digital signature (e.g. DSC or Aadhaar eSign in India). Check what the recipient accepts.</p>""",
          [("Is my signature stored?", "No. It exists only in your browser tab and is discarded when you close it."), FAQ_PDF_PRIVATE],
          "pdf"),
    _tool("unlock-pdf", "unlock", "Unlock PDF",
          "Unlock PDF — Remove PDF Password & Restrictions Free",
          "Remove the password or print/copy/edit restrictions from a PDF you're allowed to open. Keeps text and quality. Free, private, no upload.",
          "Unlock a PDF",
          "Remove the open password or the printing, copying and editing restrictions from your own PDFs — such as bank statements and e-bills.",
          ["Removes restrictions from PDFs that open without a password.", "Removes the open password when you enter it.",
           "Text, links and quality are kept — pages are not turned into images.", "The PDF and password never leave your device."],
          ["Drop the PDF.", "Type its password if it asks for one when opening.", "Download the unlocked copy."],
          """<h2>Only for files you're allowed to open</h2><p>This tool removes protection when you already know the password or the file opens normally. It does not crack unknown passwords. Use it only for documents you own or are authorised to modify.</p>""",
          [("I forgot the password — can you recover it?", "No. Without the password the content can't be decrypted. Bank statements often use a combination like your date of birth or customer ID — check the email that came with it."),
           FAQ_PDF_PRIVATE],
          "pdf"),
    _tool("pdf-to-text", "ocr", "PDF to text (OCR)",
          "PDF to Text — Extract Text from PDF & Scans (OCR) Free",
          "Extract text from any PDF, including scanned pages, with built-in OCR. Copy or download as .txt. Free, private — runs in your browser.",
          "PDF to text with OCR",
          "Copy the text out of any PDF — digital or scanned. Pages without a text layer are recognised with OCR, right on your device.",
          ["Reads the text layer instantly when the PDF has one.", "Scanned pages are recognised with OCR (English).",
           "Copy to clipboard or download a .txt file.", "Nothing is uploaded — OCR runs in your browser."],
          ["Drop your PDF.", "Click “Extract text” (tick “Always use OCR” for messy text layers).", "Copy or download the text."],
          """<h2>How accurate is OCR?</h2><p>Clean, straight scans at 200–300 DPI usually reach very high accuracy. Handwriting, low-resolution photos and complex layouts are harder — always proofread important text.</p>""",
          [("Which languages are supported?", "English for now. Other languages may be added later."), FAQ_PDF_PRIVATE],
          "pdf"),
    _tool("image-to-text", "ocr", "Image to text (OCR)",
          "Image to Text — Extract Text from Photos (OCR) Free",
          "Copy text from photos, screenshots and scans with OCR in your browser. JPG, PNG, WebP, HEIC. Free, private — images are never uploaded.",
          "Image to text (OCR)",
          "Photograph a document or take a screenshot and turn it into editable text — privately, on your device.",
          ["Works with JPG, PNG, WebP and HEIC photos and screenshots.", "Batch: drop several images and get all the text at once.",
           "Copy or download as .txt.", "Runs entirely in your browser."],
          ["Drop your images.", "Click “Extract text”.", "Copy or download."],
          """<h2>Tips for better results</h2><ul><li>Photograph the page flat, in good light, filling the frame.</li><li>Avoid shadows and angles; crop to the text.</li><li>Screenshots work best of all.</li></ul>""",
          [("Can it read handwriting?", "Neat print-style handwriting sometimes works, but OCR is designed for printed text."), FAQ_IMG_PRIVACY],
          "image", ocr_images=True),
]



# ---------------------------------------------------------------- JPG → PDF under X KB
DOC_PHOTO_COST = [  # one A4 page made from a phone photo/scan, after good compression (KB)
    ("Photo of a text document, grayscale", 15, 60),
    ("Photo of a certificate or ID in colour", 40, 120),
    ("Ordinary photo (people, places)", 80, 250),
]
IMG2PDF_WHO = {
    20: "Portals that want a one-page document as a tiny PDF — signatures, declarations or a single ID side.",
    40: "Forms that ask for small PDFs such as one-page certificates or ID proof — a very common limit on application portals.",
    50: "ID proofs, caste and income certificates or a single marksheet uploaded as PDF.",
    300: "Multi-page bundles: marksheets for several semesters, experience letters or a short project.",
    500: "Larger application bundles, claim documents and multi-page scans that must stay sharp.",
    1024: "Job portals, HR systems and email — several pages of photos at good quality.",
}


def img2pdf_page(kb):
    L, s = kb_label(kb), kb_slug(kb)
    eff = kb // 1024 * 1000 if kb >= 1024 and kb % 1024 == 0 else kb
    rows = ""
    for label, lo, hi in DOC_PHOTO_COST:
        rng, verdict = _fit_range(eff, lo, hi)
        rows += f"<tr><td>{label}</td><td>{lo}–{hi} KB</td><td>{rng}</td><td>{verdict}</td></tr>"
    return _tool(
        f"jpg-to-pdf-under-{s}", "img2pdf", f"JPG to PDF under {L}",
        f"JPG to PDF Under {L} — Image to PDF Converter, Exact Size",
        f"Convert photos or scans into one PDF under {L}. Add any number of images, order pages, A4 or Letter. Free and private — nothing is uploaded.",
        f"JPG to PDF under {L}",
        f"Turn your photos or scanned pages into a single PDF that fits {L} — the image-to-PDF and compress steps in one.",
        [f"Combines images into one PDF, then compresses it to fit {L} automatically.",
         "Counts 1 KB as 1000 bytes, so the file passes either convention.",
         "Works with JPG, PNG, WebP and iPhone HEIC photos; rotation is fixed automatically.",
         "Runs in your browser — your documents are never uploaded."],
        ["Drop your images (document pages, ID front and back…).", f"Put them in order; {L} is already set.", "Click “Create PDF” and download."],
        f"""
<h2>Who needs an image PDF under {L}?</h2>
<p>{IMG2PDF_WHO[kb]}</p>
<h2>How many photos fit in {L}?</h2>
<div class="tablewrap"><table><thead><tr><th>Each page is…</th><th>Size per page</th><th>Pages that fit</th><th>Realistic?</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="muted small">Estimates for cropped A4/Letter pages at readable quality. The tool always tells you whether it reached {L}.</p>
<h2>Tips</h2>
<ul><li>Crop each photo to the paper's edges before adding it — background wastes bytes.</li>
<li>Choose “Small file” quality for text documents.</li>
<li>Only include the pages the form asks for; every page shares the same {L}.</li></ul>
""",
        [(f"Can I convert JPG to PDF under {L} for free?", f"Yes — free, no sign-up and no watermark. Add your images, keep {L} as the limit and download."),
         ("What if it can't reach the size?", "You'll see a message. Use fewer pages, crop the photos or choose “Small file” quality and try again."),
         FAQ_IMG_PRIVACY],
        "form", pdf_max_kb=eff, group="img")


IMG2PDF_SIZES = [20, 40, 50, 300, 500, 1024]

_orig_all_pages = all_pages


def all_pages():
    pages = _orig_all_pages()
    i = max(k for k, p in enumerate(pages) if p.get("group") == "tool") + 1
    pages[i:i] = NEW_TOOLS
    j = max(k for k, p in enumerate(pages) if p.get("group") == "img") + 1
    extra = [img2pdf_page(k) for k in IMG2PDF_SIZES]
    pages[j:j] = extra
    for p in NEW_TOOLS + extra:
        p.setdefault("mode", "recommended")
    return pages

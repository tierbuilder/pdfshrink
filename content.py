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
            f"Rough capacity of {L}: ~{text_pages} text-only pages, ~{gray_pages} grayscale scanned page(s), {color_txt} full-colour photo page(s).",
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
        title="Merge PDF Files Online Free — Combine PDFs, No Upload",
        desc="Combine multiple PDFs into one in seconds. Reorder files, keep links and text. Free, unlimited, runs in your browser — nothing is uploaded.",
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
        faqs=[("Will merging reduce quality?", "No. Pages are copied without re-encoding."),
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
        title="JPG to PDF Converter Free — Images to PDF, No Upload",
        desc="Convert JPG, PNG and phone photos into one PDF. A4, Letter or fit-to-image pages, adjustable margins. Free, private, in your browser.",
        h1="Convert JPG & images to PDF",
        lead="Turn photos, scans and screenshots into a single, tidy PDF — in your chosen order and page size.",
        facts=["Supports JPG, PNG, WebP, GIF and (in Safari) HEIC.",
               "A4, US Letter or same-as-image page sizes; landscape images get landscape pages.",
               "Phone photo rotation (EXIF) is applied automatically.",
               "Runs locally; your images are never uploaded."],
        steps=["Drop your images.", "Order them and choose page size, margin and quality.", "Click “Create PDF” and download."],
        body="""
<h2>Photos of documents → one PDF</h2>
<p>Photographed your documents on your phone? Put them into one PDF here, then use
<a href="/compress-pdf-to-100kb/">Compress PDF to 100 KB</a> if a form needs it smaller.</p>
""",
        faqs=[("Why is my photo sideways in other converters?", "Phones store rotation as metadata. We apply it before creating the PDF, so pages come out upright."), FAQ_PRIVACY],
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
           "Provided “as is” without warranty — keep your original files.",
           "You are responsible for having the right to process the files you use.",
           "Not affiliated with any government, exam body or third-party brand mentioned."],
    steps=None, faqs=[],
    body="""
<h2>1. The service</h2><p>The tools run in your web browser. We do not receive, store or process the files you
select. Output is generated on your device.</p>
<h2>2. Acceptable use</h2><p>Use the tools only with files you own or are authorised to process. Don't use them to
infringe copyright, to circumvent security measures or access controls you aren't authorised to remove, or to create
forged or fraudulent documents.</p>
<h2>3. No warranty</h2><p>The tools are provided “as is”. Compression and conversion can change how a document
looks; always check the output and keep your original. To the extent permitted by law, we are not liable for any
loss arising from use of the site, including rejected uploads or missed deadlines.</p>
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
           "JSZip — used under the MIT License (dual-licensed MIT/GPLv3) — © Stuart Knightley and contributors."],
    steps=None, faqs=[],
    body="""
<h2>Full license texts</h2>
<ul>
<li><a href="/vendor/licenses/pdfjs-LICENSE.txt">pdf.js — Apache License 2.0</a> (unmodified distribution build, v4.10.38)</li>
<li><a href="/vendor/licenses/pdf-lib-LICENSE.txt">pdf-lib — MIT License</a> (v1.17.1)</li>
<li><a href="/vendor/licenses/pako-LICENSE.txt">pako — MIT License</a> (v2.1.0)</li>
<li><a href="/vendor/licenses/jszip-LICENSE.txt">JSZip — MIT / GPLv3 dual license</a> (v3.10.1, used under MIT)</li>
</ul>
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

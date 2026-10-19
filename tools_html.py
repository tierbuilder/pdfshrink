"""Markup for the non-compressor tools (wired up by static/tools.js)."""

ICON_UP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
           'stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/>'
           '<path d="M14 3v5h5"/><path d="M12 18v-6m-3 3 3-3 3 3"/></svg>')
ICON_IMG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/>'
            '<circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/></svg>')


def dropzone(accept, multiple, mouse, tap, icon=ICON_UP):
    m = " multiple" if multiple else ""
    return f"""<div class="drop" id="drop" tabindex="0" role="button" aria-label="{tap}">
<input type="file" id="file" accept="{accept}"{m} hidden>
{icon}
<p class="drop-title"><span class="mouse-only">{mouse}</span><span class="tap-only"><span class="link">{tap}</span></span></p>
<p class="drop-sub">🔒 Processed on your device — never uploaded · Free · No sign-up</p>
</div>"""


PRESETS = {
    # label, width, height, unit, dpi, kb — examples only; pages tell users to follow their form's rules.
    "general": [("200×230 px", 200, 230, "px", "", ""), ("300×300 px", 300, 300, "px", "", ""),
                ("600×600 px", 600, 600, "px", "", ""), ("140×60 px", 140, 60, "px", "", "")],
    "exam": [("Photo 3.5×4.5 cm · 200 DPI", 3.5, 4.5, "cm", 200, ""), ("Photo 200×230 px", 200, 230, "px", "", ""),
             ("Signature 140×60 px", 140, 60, "px", "", ""), ("Signature 3.5×1.5 cm · 200 DPI", 3.5, 1.5, "cm", 200, "")],
    "passport": [("3.5×4.5 cm (India, UK, EU)", 3.5, 4.5, "cm", 300, ""), ("35×45 mm", 35, 45, "mm", 300, ""),
                 ("2×2 in (US)", 2, 2, "in", 300, ""), ("51×51 mm", 51, 51, "mm", 300, "")],
}


def image_focus(p):
    """Which controls a page shows by default (Basic); everything else sits under Advanced options."""
    img = p.get("img", {})
    if img.get("focus"):
        return img["focus"]
    if img.get("text"):
        return "text"
    if img.get("unit", "px") != "px":
        return "size"
    if img.get("presets") == "exam":
        return "presets"
    if img.get("fmt"):
        return "convert"
    return "kb"


def image_tool(p):
    target_kb = p.get("target_kb")
    img = p.get("img", {})
    fmt, unit, text = img.get("fmt", "jpg"), img.get("unit", "px"), img.get("text", False)
    presets = PRESETS[img.get("presets", "general")]
    focus = image_focus(p)
    kb_chips = "".join(f'<button type="button" class="chip" data-kb="{k}">{k} KB</button>' for k in (10, 20, 30, 50, 100, 200))
    dim_chips = "".join(f'<button type="button" class="chip" data-w="{w}" data-h="{h}" data-unit="{u}" data-dpi="{d}"'
                        f'{f" data-kb={chr(34)}{kb}{chr(34)}" if kb else ""}>{label}</button>' for label, w, h, u, d, kb in presets)
    sel = lambda cur, val: " selected" if cur == val else ""
    fmts = [("jpg", "JPG (accepted everywhere)"), ("png", "PNG (keeps transparency)"), ("webp", "WebP (smallest, for websites)")]
    fmt_opts = "".join(f'<option value="{v}"{sel(fmt, v)}>{t}</option>' for v, t in fmts)
    unit_opts = "".join(f'<option value="{v}"{sel(unit, v)}>{t}</option>' for v, t in (("px", "px"), ("cm", "cm"), ("mm", "mm"), ("in", "inch")))
    q = img.get("q", "0.8")
    q_opts = "".join(f'<option value="{v}"{sel(q, v)}>{t}</option>' for v, t in (("0.95", "High / lossless PNG"), ("0.8", "Balanced"), ("0.6", "Small file"), ("0.4", "Smallest")))
    checked = " checked" if text else ""
    label = "Photo resizer" if img.get("presets") else "Image resizer"
    dpi_hint = ('<p class="muted small">DPI: 200 by default (presets set their own) — change it under Advanced options.</p>'
                if focus == "size" else "")

    # Every control is rendered exactly once — in Basic or in Advanced — so the script finds it either way.
    block = {
        "kb": f"""<div class="target-row"><label for="tsize">Max size</label>
<input id="tsize" type="number" min="1" step="any" inputmode="decimal" value="{target_kb or ''}" placeholder="optional">
<select id="tunit" aria-label="Unit"><option>KB</option><option>MB</option></select>{kb_chips}</div>""",
        "quality": f"""<div class="target-row" id="quality-row"><label for="quality">Quality</label>
<select id="quality">{q_opts}</select>
<label for="fmt">Format</label><select id="fmt">{fmt_opts}</select></div>""",
        "size": f"""<p class="muted small chips-line" id="dimhelp">Common sizes: {dim_chips}</p>
<div class="target-row"><label for="iw">Width</label><input id="iw" type="number" min="0" step="any" inputmode="decimal" placeholder="auto" aria-describedby="dimhelp">
<label for="ih">Height</label><input id="ih" type="number" min="0" step="any" inputmode="decimal" placeholder="auto">
<select id="unit" aria-label="Size unit">{unit_opts}</select>
<select id="fit" aria-label="Resize mode"><option value="contain">Keep proportions</option><option value="cover">Crop to exact size</option></select></div>
{dpi_hint}""",
        "dpi": f"""<div class="target-row" id="dpi-row"><label for="dpi">DPI</label><input id="dpi" type="number" min="1" max="65535" inputmode="numeric" placeholder="{'200' if unit != 'px' else 'keep'}">
<span class="muted small">Needed for cm/mm/inch sizes (default 200) and written into the file.</span></div>""",
        "min": """<div class="target-row"><label for="tmin">Min size</label><input id="tmin" type="number" min="0" step="any" inputmode="decimal" placeholder="none"> <span class="muted">KB (if your form has a minimum)</span></div>""",
        "text": f"""<label class="check"><input type="checkbox" id="addtext"{checked}> Print name and date at the bottom of the photo</label>
<div class="target-row" id="text-row"><label for="tname">Name</label><input id="tname" type="text" autocomplete="name" style="width:200px" maxlength="60">
<label for="tdate">Date</label><input id="tdate" type="date">
<select id="tdfmt" aria-label="Date format"><option value="dmy">DD-MM-YYYY</option><option value="dmy/">DD/MM/YYYY</option><option value="dmy.">DD.MM.YYYY</option><option value="mdy">MM/DD/YYYY</option><option value="ymd">YYYY-MM-DD</option></select></div>""",
    }
    basic_keys = {"kb": ["kb"], "size": ["size"], "presets": ["size", "kb"], "text": ["text", "kb"],
                  "convert": ["quality"]}[focus]
    order = ["text", "size", "kb", "quality", "dpi", "min"]
    basic = "\n".join(block[k] for k in order if k in basic_keys)
    advanced = "\n".join(block[k] for k in order if k not in basic_keys)
    return f"""<section class="tool" id="tool" data-tool="image" data-focus="{focus}" data-target-kb="{target_kb or ''}" aria-label="{label}">
{dropzone("image/*,.heic,.heif", True, 'Drop images here or <span class="link">choose files</span>', "Tap to choose images", ICON_IMG)}
<div class="opts">
{basic}
<details class="adv adv-remember"><summary>Advanced options</summary>
<div class="adv-body">
{advanced}
<p class="muted small">Always follow the exact numbers in your form's instructions.</p>
</div></details>
</div>
<ul class="files" id="files" aria-live="polite"></ul>
<div class="after"><button type="button" class="btn btn-ghost btn-sm" id="rerun" hidden>Apply new settings</button></div>
<div class="bulk" id="bulk" hidden><button type="button" class="btn" id="zip">Download all (ZIP)</button>
<button type="button" class="btn btn-ghost" id="clear">Clear</button></div>
</section>"""


def dpi_tool():
    chips = "".join(f'<button type="button" class="chip" data-dpi="{d}">{d} DPI</button>' for d in (72, 96, 150, 200, 300, 600))
    return f"""<section class="tool" id="tool" data-tool="dpi" aria-label="Change image DPI">
{dropzone("image/*,.heic,.heif", True, 'Drop images here or <span class="link">choose files</span>', "Tap to choose images", ICON_IMG)}
<div class="opts"><div class="target-row"><label for="dpival">New DPI</label><input id="dpival" type="number" min="1" max="65535" value="300" inputmode="numeric">{chips}</div></div>
<ul class="files" id="files" aria-live="polite"></ul>
<div class="bulk" id="bulk" hidden><button type="button" class="btn" id="zip">Download all (ZIP)</button>
<button type="button" class="btn btn-ghost" id="clear">Clear</button></div>
</section>"""


def merge_tool():
    return f"""<section class="tool" id="tool" data-tool="merge" aria-label="Merge PDF">
{dropzone("application/pdf,.pdf", True, 'Drop PDFs to merge or <span class="link">choose files</span>', "Tap to choose PDFs")}
<ol class="files" id="files" aria-live="polite"></ol>
<div class="bulk" id="go-row" hidden><button type="button" class="btn" id="go" disabled>Merge PDFs</button>
<button type="button" class="btn btn-ghost" id="sort">Sort A→Z</button></div>
<div class="result" id="result" aria-live="polite" hidden></div>
</section>"""


def split_tool():
    return f"""<section class="tool" id="tool" data-tool="split" aria-label="Split PDF">
{dropzone("application/pdf,.pdf", False, 'Drop a PDF here or <span class="link">choose a file</span>', "Tap to choose a PDF")}
<p class="muted" id="doc-info" aria-live="polite"></p>
<div class="opts">
<div class="target-row"><label for="split-mode">Mode</label><select id="split-mode">
<option value="extract">Extract pages into one PDF</option><option value="single">Every page as its own PDF</option>
<option value="every">Split every N pages</option></select></div>
<div class="target-row" id="range-row"><label for="ranges">Pages</label><input id="ranges" type="text" value="1-2" style="width:200px" aria-describedby="rangehelp"><span class="muted small" id="rangehelp">e.g. 1-3, 5, 8-</span></div>
<div class="target-row" id="every-row" hidden><label for="every">Pages per file</label><input id="every" type="number" min="1" value="2"></div>
</div>
<div class="bulk" id="go-row" hidden><button type="button" class="btn" id="go" disabled>Split PDF</button></div>
<div class="result" id="result" aria-live="polite" hidden></div>
</section>"""


def img2pdf_tool(max_kb=""):
    return f"""<section class="tool" id="tool" data-tool="img2pdf" aria-label="Images to PDF">
{dropzone("image/*,.heic,.heif", True, 'Drop images here or <span class="link">choose files</span>', "Tap to choose images", ICON_IMG)}
<div class="opts">
<div class="target-row"><label for="page-size">Page size</label><select id="page-size"><option value="a4">A4</option><option value="letter">US Letter</option><option value="fit">Same as image</option></select>
<label for="margin">Margin</label><select id="margin"><option value="0">None</option><option value="18" selected>Small</option><option value="40">Large</option></select>
<label for="quality">Quality</label><select id="quality"><option value="0.92">High</option><option value="0.8" selected>Medium</option><option value="0.6">Small file</option></select></div>
<div class="target-row"><label for="pdfmax">Max PDF size</label><input id="pdfmax" type="number" min="1" step="any" inputmode="decimal" value="{max_kb}" placeholder="optional"> <span class="muted">KB</span></div>
</div>
<ol class="files" id="files" aria-live="polite"></ol>
<div class="bulk" id="go-row" hidden><button type="button" class="btn" id="go" disabled>Create PDF</button>
<button type="button" class="btn btn-ghost" id="sort">Sort A→Z</button></div>
<div class="result" id="result" aria-live="polite" hidden></div>
</section>"""


def pdf2img_tool():
    return f"""<section class="tool" id="tool" data-tool="pdf2img" aria-label="PDF to images">
{dropzone("application/pdf,.pdf", False, 'Drop a PDF here or <span class="link">choose a file</span>', "Tap to choose a PDF")}
<p class="muted" id="doc-info" aria-live="polite"></p>
<div class="opts"><div class="target-row">
<label for="ifmt">Format</label><select id="ifmt"><option value="jpg">JPG</option><option value="png">PNG (lossless)</option></select>
<label for="dpi">Resolution</label><select id="dpi"><option value="72">72 DPI (small)</option><option value="150" selected>150 DPI (standard)</option><option value="300">300 DPI (print)</option></select>
</div></div>
<div class="bulk" id="go-row" hidden><button type="button" class="btn" id="go" disabled>Convert to images</button></div>
<div class="result" id="result" aria-live="polite" hidden></div>
</section>"""



def pdf_single(kind, label, inner, go_label, extra_after=""):
    return f"""<section class="tool" id="tool" data-tool="{kind}" aria-label="{label}">
{dropzone("application/pdf,.pdf", False, 'Drop a PDF here or <span class="link">choose a file</span>', "Tap to choose a PDF")}
<p class="muted" id="doc-info" aria-live="polite"></p>
{inner}
<div class="bulk" id="go-row" hidden><button type="button" class="btn" id="go" disabled>{go_label}</button></div>
{extra_after}<div class="result" id="result" aria-live="polite" hidden></div>
</section>"""


def organize_tool():
    inner = """<div class="opts" id="org-actions" hidden>
<div class="target-row"><button type="button" class="btn btn-ghost btn-sm" id="rot-all-ccw">⟲ Rotate all left</button>
<button type="button" class="btn btn-ghost btn-sm" id="rot-all-cw">⟳ Rotate all right</button>
<button type="button" class="btn btn-ghost btn-sm" id="reverse">Reverse order</button>
<button type="button" class="btn btn-ghost btn-sm" id="reset">Reset</button></div>
<div class="target-row"><label for="delpages">Delete pages</label><input id="delpages" type="text" placeholder="e.g. 2, 5-7" style="width:160px">
<button type="button" class="btn btn-ghost btn-sm" id="del-range">Mark for deletion</button>
<span class="muted small" id="org-summary" aria-live="polite"></span></div>
</div>
<ol class="pagegrid" id="pages" aria-label="Pages"></ol>"""
    return pdf_single("organize", "Organize PDF pages", inner, "Save PDF")


def pagenum_tool():
    inner = """<div class="opts"><div class="target-row">
<label for="pn-pos">Position</label><select id="pn-pos"><option value="bottom-center">Bottom centre</option><option value="bottom-right">Bottom right</option><option value="bottom-left">Bottom left</option><option value="top-center">Top centre</option><option value="top-right">Top right</option><option value="top-left">Top left</option></select>
<label for="pn-style">Format</label><select id="pn-style"><option value="n">1</option><option value="page">Page 1</option><option value="of">1 / 10</option><option value="pageof">Page 1 of 10</option></select></div>
<div class="target-row"><label for="pn-start">Start at</label><input id="pn-start" type="number" value="1" min="0" style="width:80px">
<label for="pn-size">Size</label><select id="pn-size"><option value="9">Small</option><option value="11" selected>Medium</option><option value="14">Large</option></select>
<label class="check"><input type="checkbox" id="pn-skip"> Don't number the first page (cover)</label></div></div>"""
    return pdf_single("pagenum", "Add page numbers", inner, "Add page numbers")


def watermark_tool():
    inner = """<div class="opts"><div class="target-row"><label for="wm-text">Text</label><input id="wm-text" type="text" value="CONFIDENTIAL" maxlength="60" style="width:220px">
<label for="wm-color">Colour</label><select id="wm-color"><option value="gray">Grey</option><option value="red">Red</option><option value="blue">Blue</option></select></div>
<div class="target-row"><label for="wm-size">Size</label><select id="wm-size"><option value="40">Small</option><option value="70" selected>Medium</option><option value="110">Large</option></select>
<label for="wm-opacity">Opacity</label><select id="wm-opacity"><option value="0.12">Faint</option><option value="0.25" selected>Light</option><option value="0.45">Strong</option></select>
<label for="wm-angle">Angle</label><select id="wm-angle"><option value="45" selected>Diagonal</option><option value="0">Horizontal</option></select></div></div>"""
    return pdf_single("watermark", "Watermark PDF", inner, "Add watermark")


def sign_tool():
    inner = """<div class="opts"><div class="target-row"><label for="sig-mode">Signature</label><select id="sig-mode"><option value="draw">Draw</option><option value="type">Type</option><option value="upload">Upload image</option></select>
<label for="sig-color">Ink</label><select id="sig-color"><option value="#111111">Black</option><option value="#1a3fa8">Blue</option></select></div>
<div id="sig-draw"><canvas id="sigpad" class="sigpad" width="600" height="200" aria-label="Signature drawing area — draw with mouse, finger or stylus"></canvas>
<button type="button" class="btn btn-ghost btn-sm" id="sig-clear">Clear</button></div>
<div class="target-row" id="sig-type" hidden><label for="sig-text">Your name</label><input id="sig-text" type="text" autocomplete="name" maxlength="60" style="width:240px"></div>
<div class="target-row" id="sig-upload" hidden><label for="sig-file">Signature image</label><input id="sig-file" type="file" accept="image/*"></div>
</div>"""
    after = """<div id="place-step" hidden>
<div class="target-row"><label for="sig-page">Page</label><select id="sig-page"></select>
<label for="sig-width">Width</label><select id="sig-width"><option value="15">Small</option><option value="25" selected>Medium</option><option value="35">Large</option></select>
<button type="button" class="btn btn-ghost btn-sm" id="sig-undo">Undo last</button>
<span class="muted small" id="placed" aria-live="polite"></span></div>
<div class="prevwrap" id="prevwrap" tabindex="0" role="button" aria-label="Page preview — click where the signature should go (Enter places it at the bottom right)">
<canvas id="preview"></canvas><div class="overlay" id="overlay"></div></div>
</div>"""
    return pdf_single("sign", "Sign PDF", inner, "Save signed PDF", after)


def unlock_tool():
    inner = """<div class="opts"><div class="target-row"><label for="pw">Password</label>
<input id="pw" type="password" autocomplete="off" style="width:220px" aria-describedby="pwhelp">
<span class="muted small" id="pwhelp">Leave empty if the PDF opens without a password (it only blocks printing, copying or editing).</span></div></div>"""
    return pdf_single("unlock", "Unlock PDF", inner, "Unlock PDF")


def ocr_tool(images=False):
    accept = "image/*,.heic,.heif,application/pdf,.pdf"
    mouse = 'Drop a PDF or images here or <span class="link">choose files</span>'
    return f"""<section class="tool" id="tool" data-tool="ocr" aria-label="Extract text">
{dropzone(accept, True, mouse, "Tap to choose a PDF or images", ICON_IMG if images else ICON_UP)}
<p class="muted" id="doc-info" aria-live="polite"></p>
<div class="opts"><label class="check"><input type="checkbox" id="ocr-force"> Always use OCR (ignore any existing text layer)</label>
<p class="muted small">Language: English. OCR downloads a ~3 MB language file once; it is then cached for offline use.</p></div>
<div class="bulk" id="go-row" hidden><button type="button" class="btn" id="go" disabled>Extract text</button></div>
<div id="ocr-result" hidden><p class="muted" id="ocr-prog" aria-live="polite"></p>
<label for="ocr-out" class="small muted">Extracted text</label>
<textarea id="ocr-out" class="ocr-out" rows="14" spellcheck="false"></textarea>
<div class="bulk"><button type="button" class="btn btn-sm" id="ocr-copy">Copy</button><button type="button" class="btn btn-ghost btn-sm" id="ocr-dl">Download .txt</button></div></div>
</section>"""


def render_tool(p):
    t = p["tool"]
    if t == "image":
        return image_tool(p)
    if t == "img2pdf":
        return img2pdf_tool(p.get("pdf_max_kb", ""))
    if t == "ocr":
        return ocr_tool(p.get("ocr_images", False))
    if t == "scan":
        return scan_tool(p.get("preset", "natural"))
    return {"merge": merge_tool, "split": split_tool, "pdf2img": pdf2img_tool, "dpi": dpi_tool, "organize": organize_tool,
            "pagenum": pagenum_tool, "watermark": watermark_tool, "sign": sign_tool, "unlock": unlock_tool}[t]()


def scan_tool(preset="natural"):
    def rng(id_, label, lo, hi, step, unit=""):
        return (f'<div class="sc-field"><label for="sc-{id_}">{label}</label>'
                f'<input type="range" id="sc-{id_}" min="{lo}" max="{hi}" step="{step}" data-unit="{unit}">'
                f'<output for="sc-{id_}"></output></div>')
    presets = [("natural", "Natural scan"), ("copier", "Office copier"), ("fax", "Old fax"), ("phone", "Phone scan"), ("clean", "Clean colour")]
    pre = "".join(f'<button type="button" role="radio" aria-checked="{str(k == preset).lower()}" data-preset="{k}">{label}</button>'
                  for k, label in presets)
    return f"""<section class="tool" id="tool" data-tool="scan" data-preset="{preset}" aria-label="Make PDF look scanned">
{dropzone("application/pdf,.pdf,image/*", True, 'Drop a PDF or images here or <span class="link">choose files</span>', "Tap to choose a PDF or images")}
<p class="muted" id="sc-status" aria-live="polite" hidden></p>
<div id="sc-work" hidden>
<p class="sc-file"><strong id="sc-file"></strong></p>
<div class="seg sc-presets" role="radiogroup" aria-label="Scan style">{pre}</div>
<div class="sc-layout">
<div class="sc-view">
<div class="sc-viewbar"><label for="sc-page" class="sr-only">Preview page</label><select id="sc-page"></select>
<label class="check sc-inline"><input type="checkbox" id="sc-compare"> Show original</label>
<button type="button" class="btn btn-ghost btn-sm" id="sc-shuffle" title="New random tilt and grain">🎲 Re-roll</button></div>
<div class="sc-canvases"><canvas id="sc-before" hidden aria-label="Original page"></canvas><canvas id="sc-preview" aria-label="Scanned preview"></canvas></div>
</div>
<details class="adv adv-remember sc-adv"><summary>Advanced: fine-tune the look</summary>
<div class="sc-controls">
<div class="sc-field"><label for="sc-color">Colour</label><select id="sc-color"><option value="gray">Grayscale</option><option value="bw">Black &amp; white (photocopy)</option><option value="color">Colour</option></select></div>
{rng("rotate", "Tilt", 0, 3, 0.1, "°")}
{rng("noise", "Grain", 0, 80, 1)}
{rng("blur", "Blur", 0, 2, 0.05)}
{rng("brightness", "Brightness", -40, 40, 1)}
{rng("contrast", "Contrast", -30, 60, 1)}
{rng("yellow", "Paper tone", 0, 100, 1)}
{rng("texture", "Paper texture", 0, 100, 1)}
<label class="check"><input type="checkbox" id="sc-edge"> Scanner edge shadow</label>
<div class="sc-field"><label for="sc-dpi">Resolution</label><select id="sc-dpi"><option value="110">110 DPI (smallest)</option><option value="150">150 DPI (standard)</option><option value="200">200 DPI (sharp)</option><option value="300">300 DPI (print)</option></select></div>
<div class="sc-field"><label for="sc-quality">File size</label><select id="sc-quality"><option value="0.5">Small</option><option value="0.62">Balanced</option><option value="0.8">High quality</option></select></div>
</div></details>
</div>
<div class="bulk"><button type="button" class="btn" id="sc-go">Make it look scanned</button></div>
<div class="result" id="result" aria-live="polite" hidden></div>
</div>
</section>"""

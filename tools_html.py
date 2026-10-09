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


def image_tool(target_kb):
    kb_chips = "".join(f'<button type="button" class="chip" data-kb="{k}">{k} KB</button>' for k in (10, 20, 30, 50, 100, 200))
    dim_chips = "".join(f'<button type="button" class="chip" data-w="{w}" data-h="{h}">{w}×{h}</button>'
                        for w, h in ((200, 230), (300, 300), (600, 600), (140, 60)))
    return f"""<section class="tool" id="tool" data-tool="image" data-target-kb="{target_kb or 50}" aria-label="Image resizer">
{dropzone("image/*,.heic,.heif", True, 'Drop images here or <span class="link">choose files</span>', "Tap to choose images", ICON_IMG)}
<div class="opts">
<div class="target-row"><label for="tsize">Max size</label>
<input id="tsize" type="number" min="1" step="any" inputmode="decimal" value="{target_kb or 50}">
<select id="tunit" aria-label="Unit"><option>KB</option><option>MB</option></select>{kb_chips}</div>
<details class="adv"><summary>Dimensions, minimum size &amp; format</summary>
<div class="target-row"><label for="iw">Width</label><input id="iw" type="number" min="1" inputmode="numeric" placeholder="auto" aria-describedby="dimhelp">
<label for="ih">Height</label><input id="ih" type="number" min="1" inputmode="numeric" placeholder="auto">
<span class="muted">px</span>
<select id="fit" aria-label="Resize mode"><option value="contain">Keep proportions</option><option value="cover">Crop to exact size</option></select></div>
<p class="muted small" id="dimhelp">Examples: {dim_chips} — always use the exact dimensions in your form's instructions.</p>
<div class="target-row"><label for="tmin">Min size</label><input id="tmin" type="number" min="0" step="any" inputmode="decimal" placeholder="none"> <span class="muted">KB (if your form has a minimum)</span></div>
<div class="target-row"><label for="fmt">Format</label><select id="fmt"><option value="jpg">JPG (accepted everywhere)</option><option value="webp">WebP (smaller, for websites)</option></select></div>
</details>
</div>
<ul class="files" id="files" aria-live="polite"></ul>
<div class="after"><button type="button" class="btn btn-ghost btn-sm" id="rerun" hidden>Apply new settings</button></div>
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


def img2pdf_tool():
    return f"""<section class="tool" id="tool" data-tool="img2pdf" aria-label="Images to PDF">
{dropzone("image/*,.heic,.heif", True, 'Drop images here or <span class="link">choose files</span>', "Tap to choose images", ICON_IMG)}
<div class="opts">
<div class="target-row"><label for="page-size">Page size</label><select id="page-size"><option value="a4">A4</option><option value="letter">US Letter</option><option value="fit">Same as image</option></select>
<label for="margin">Margin</label><select id="margin"><option value="0">None</option><option value="18" selected>Small</option><option value="40">Large</option></select>
<label for="quality">Quality</label><select id="quality"><option value="0.92">High</option><option value="0.8" selected>Medium</option><option value="0.6">Small file</option></select></div>
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


def render_tool(p):
    t = p["tool"]
    if t == "image":
        return image_tool(p.get("target_kb"))
    return {"merge": merge_tool, "split": split_tool, "img2pdf": img2pdf_tool, "pdf2img": pdf2img_tool}[t]()

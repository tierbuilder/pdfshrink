/* Image + PDF utility tools: image to exact KB, merge, split, images→PDF, PDF→images.
 * Everything runs locally in the browser; nothing is uploaded. Libraries are loaded
 * on demand through engine.js (PdfShrink.ready / PdfShrink.getPdfjs). */
(function () {
  'use strict';
  const tool = document.getElementById('tool');
  if (!tool) return;
  const kind = tool.dataset.tool;
  const $ = (s, r) => (r || tool).querySelector(s);
  const $$ = (s, r) => Array.from((r || tool).querySelectorAll(s));
  const fmt = (n) => (n >= 1048576 ? (n / 1048576).toFixed(2) + ' MB' : n >= 1024 ? (n / 1024).toFixed(n < 10240 ? 1 : 0) + ' KB' : n + ' B');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const baseName = (n) => n.replace(/\.[^.]+$/, '');
  const tick = () => new Promise((r) => setTimeout(r, 0));
  function beacon(name, props) {
    // First-party, cookie-less usage counts. Skipped for Do-Not-Track / Global Privacy Control and local dev.
    try {
      if (navigator.globalPrivacyControl || navigator.doNotTrack === '1' || /^(localhost|127\.|\[::1\])/.test(location.hostname)) return;
      const body = JSON.stringify({ n: name, u: location.pathname, p: props || {} });
      if (!(navigator.sendBeacon && navigator.sendBeacon('/api/event', body))) {
        fetch('/api/event', { method: 'POST', body, keepalive: true }).catch(() => {});
      }
    } catch (e) { /* analytics is optional */ }
  }
  const track = (name, props) => {
    beacon(name, props);
    try { if (window.plausible) window.plausible(name, { props }); if (window.gtag) window.gtag('event', name, props); } catch (e) { /* optional */ }
  };
  function toast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.hidden = false;
    clearTimeout(toast.t); toast.t = setTimeout(() => (t.hidden = true), 3500);
  }
  function loadScript(src) {
    return new Promise((res, rej) => {
      if (document.querySelector('script[src="' + src + '"]')) return res();
      const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s);
    });
  }
  async function downloadZip(files, zipName) {
    if (!window.JSZip) await loadScript('/vendor/jszip.min.js');
    const zip = new JSZip(), used = new Set();
    for (const f of files) {
      let n = f.name, k = 1;
      while (used.has(n)) n = f.name.replace(/(\.[^.]+)$/, '-' + k++ + '$1');
      used.add(n); zip.file(n, f.blob);
    }
    saveBlob(await zip.generateAsync({ type: 'blob', compression: 'STORE' }), zipName);
  }
  function saveBlob(blob, name) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 60000);
  }
  const isPdf = (f) => f.type === 'application/pdf' || /\.pdf$/i.test(f.name);
  const isImg = (f) => /^image\//.test(f.type) || /\.(jpe?g|png|webp|gif|bmp|avif|heic|heif)$/i.test(f.name);

  // Drop zone shared by all tools.
  const drop = $('#drop'), input = $('#file');
  let onFiles = () => {};
  drop.addEventListener('click', () => input.click());
  drop.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
  input.addEventListener('change', () => { onFiles(Array.from(input.files)); input.value = ''; });
  ['dragenter', 'dragover'].forEach((t) => document.addEventListener(t, (e) => { e.preventDefault(); drop.classList.add('over'); }));
  ['dragleave', 'drop'].forEach((t) => document.addEventListener(t, (e) => { e.preventDefault(); if (t === 'drop' || e.target === document.documentElement) drop.classList.remove('over'); }));
  document.addEventListener('drop', (e) => { if (e.dataTransfer && e.dataTransfer.files.length) onFiles(Array.from(e.dataTransfer.files)); });
  document.addEventListener('paste', (e) => { if (e.clipboardData && e.clipboardData.files.length) onFiles(Array.from(e.clipboardData.files)); });

  // Decode any image the browser supports, honouring EXIF rotation.
  async function decodeImage(file) {
    try { return await createImageBitmap(file, { imageOrientation: 'from-image' }); }
    catch (e) {
      const url = URL.createObjectURL(file);
      try {
        const img = new Image(); img.src = url; await img.decode();
        return img;
      } catch (e2) {
        throw new Error(/hei[cf]/i.test(file.name) ? 'HEIC images are only supported in Safari. Convert to JPG first, or open this page in Safari.' : 'This image format is not supported by your browser.');
      } finally { setTimeout(() => URL.revokeObjectURL(url), 1000); }
    }
  }
  const dimsOf = (src) => ({ w: src.naturalWidth || src.width, h: src.naturalHeight || src.height });

  function drawTo(src, w, h, fit) {
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const g = c.getContext('2d');
    g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); // JPEG has no transparency
    g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
    const { w: sw, h: sh } = dimsOf(src);
    if (fit === 'cover') {
      const s = Math.max(w / sw, h / sh), cw = w / s, ch = h / s;
      g.drawImage(src, (sw - cw) / 2, (sh - ch) / 2, cw, ch, 0, 0, w, h);
    } else g.drawImage(src, 0, 0, w, h);
    return c;
  }
  const toBlob = (c, type, q) => new Promise((r) => c.toBlob(r, type, q));

  // ------------------------------------------------------------------ image to KB
  async function imageToSize(file, o) {
    const src = await decodeImage(file);
    const { w: ow, h: oh } = dimsOf(src);
    // Requested output dimensions.
    let tw = ow, th = oh, fixed = false;
    if (o.width || o.height) {
      fixed = true;
      if (o.fit === 'cover' && o.width && o.height) { tw = o.width; th = o.height; }
      else {
        const s = Math.min(o.width ? o.width / ow : Infinity, o.height ? o.height / oh : Infinity);
        tw = Math.max(1, Math.round(ow * s)); th = Math.max(1, Math.round(oh * s));
      }
    }
    const fit = o.fit === 'cover' && o.width && o.height ? 'cover' : 'contain';
    const type = o.format === 'webp' ? 'image/webp' : 'image/jpeg';
    const maxB = o.maxBytes, minB = o.minBytes || 0, maxLabel = o.maxLabel || fmt(maxB);
    let best = null, smallest = null;
    const consider = (b, w, h, q) => {
      const r = { blob: b, w, h, q };
      if (!smallest || b.size < smallest.blob.size) smallest = r;
      return r;
    };
    if (!maxB) {
      const c = drawTo(src, tw, th, fit);
      const b = await toBlob(c, type, 0.85);
      return { blob: b, w: tw, h: th, hit: true };
    }
    // Shrink resolution until a reasonable quality (≥ 0.5) fits, unless the user fixed the dimensions.
    let scale = 1;
    for (let round = 0; round < 25; round++) {
      const w = Math.max(16, Math.round(tw * scale)), h = Math.max(16, Math.round(th * scale));
      const c = drawTo(src, w, h, fit);
      let lo = 0.05, hi = 0.95, found = null;
      const top = await toBlob(c, type, hi); // hi = 0.95
      consider(top, w, h, hi);
      if (top.size <= maxB) found = { blob: top, w, h, q: hi };
      else {
        for (let i = 0; i < 7; i++) {
          const q = (lo + hi) / 2, b = await toBlob(c, type, q);
          consider(b, w, h, q);
          if (b.size <= maxB) { found = { blob: b, w, h, q }; lo = q; } else hi = q;
        }
      }
      await tick();
      if (found && (found.q >= 0.5 || fixed || w <= 160)) { best = found; break; }
      if (found && !best) best = found; // keep as fallback while trying smaller sizes
      if (fixed && !found) break;
      if (w <= 32 || h <= 32) break;
      scale *= found ? 0.9 : 0.8;
    }
    const r = best || smallest;
    if (src.close) src.close();
    const res = { blob: r.blob, w: r.w, h: r.h, hit: !!best && r.blob.size <= maxB };
    if (res.hit && minB && r.blob.size < minB) res.note = 'Below the ' + o.minLabel + ' minimum — use larger dimensions or a bigger photo.';
    if (!res.hit) res.note = fixed ? 'Could not fit these dimensions under ' + maxLabel + ' — try smaller dimensions.' : 'Could not reach ' + maxLabel + '.';
    return res;
  }

  function initImage() {
    const list = $('#files'), bulk = $('#bulk'), rerun = $('#rerun');
    const tsize = $('#tsize'), tunit = $('#tunit');
    const items = [];
    if (tool.dataset.targetKb) tsize.value = tool.dataset.targetKb;
    $$('.chip[data-kb]').forEach((c) => c.addEventListener('click', () => { tsize.value = c.dataset.kb; tunit.value = 'KB'; stale(); }));
    $$('.chip[data-w]').forEach((c) => c.addEventListener('click', () => { $('#iw').value = c.dataset.w; $('#ih').value = c.dataset.h; $('#fit').value = 'cover'; stale(); }));
    $$('input,select', $('.opts')).forEach((el) => el.addEventListener('change', stale));
    function stale() { if (items.some((i) => i.out)) rerun.hidden = false; }
    function opts() {
      const v = parseFloat(tsize.value), mul = tunit.value === 'MB' ? 1e6 : 1000; // 1000-byte KB passes both conventions
      const mn = parseFloat($('#tmin').value);
      return {
        maxBytes: v > 0 ? Math.floor(v * mul) : 0, minBytes: mn > 0 ? Math.ceil(mn * 1024) : 0,
        width: parseInt($('#iw').value, 10) || 0, height: parseInt($('#ih').value, 10) || 0,
        fit: $('#fit').value, format: $('#fmt').value,
        maxLabel: tsize.value + ' ' + tunit.value, minLabel: (mn || 0) + ' KB',
      };
    }
    onFiles = (files) => {
      const imgs = files.filter(isImg);
      if (!imgs.length) return toast('Please choose image files (JPG, PNG, WebP…).');
      for (const f of imgs) {
        const li = document.createElement('li'); li.className = 'item';
        li.innerHTML = '<div class="item-top"><span class="name">' + esc(f.name) + '</span><span class="sizes">' + fmt(f.size) + '</span></div>' +
          '<div class="bar"><span></span></div><div class="item-bottom"><span class="status">Waiting…</span><span class="actions"></span></div>';
        list.appendChild(li); items.push({ file: f, li });
      }
      track('images_added', { count: imgs.length });
      run(false);
    };
    let busy = false;
    async function run(force) {
      if (busy) return; busy = true; rerun.hidden = true;
      const o = opts();
      for (const it of items) {
        if (it.out && !force) continue;
        const { li, file } = it, st = $('.status', li), bar = $('.bar span', li), actions = $('.actions', li), sizes = $('.sizes', li);
        li.classList.remove('done', 'miss', 'err'); actions.innerHTML = ''; li.querySelector('.note') && li.querySelector('.note').remove();
        if (it.out) URL.revokeObjectURL(it.out.url);
        st.textContent = 'Resizing…'; bar.style.width = '40%';
        try {
          const r = await imageToSize(file, o);
          const ext = o.format === 'webp' ? '.webp' : '.jpg';
          const name = baseName(file.name) + '-' + Math.max(1, Math.round(r.blob.size / 1024)) + 'kb' + ext;
          it.out = { url: URL.createObjectURL(r.blob), name, blob: r.blob };
          bar.style.width = '100%';
          sizes.innerHTML = fmt(file.size) + ' → <b>' + fmt(r.blob.size) + '</b>';
          st.textContent = (o.maxBytes ? (r.hit ? '✓ Under ' : '✗ Above ') + o.maxLabel + ' · ' : '') + r.w + '×' + r.h + ' px';
          li.classList.add(r.hit && !r.note ? 'done' : 'miss');
          actions.innerHTML = '<img class="thumb" alt="Preview of ' + esc(name) + '" src="' + it.out.url + '"><a class="btn btn-sm" download="' + esc(name) + '" href="' + it.out.url + '">Download</a>';
          if (r.note) { const n = document.createElement('p'); n.className = 'note'; n.textContent = r.note; li.appendChild(n); }
          track('image_resized', { hit: r.hit, kb: Math.round(o.maxBytes / 1024) });
        } catch (e) {
          li.classList.add('err'); st.textContent = e.message || 'Could not read this image.';
        }
        await tick();
      }
      busy = false;
      bulk.hidden = items.filter((i) => i.out).length < 2;
    }
    rerun.addEventListener('click', () => run(true));
    $('#zip').addEventListener('click', () => downloadZip(items.filter((i) => i.out).map((i) => i.out), 'resized-images.zip'));
    $('#clear').addEventListener('click', () => { items.forEach((i) => i.out && URL.revokeObjectURL(i.out.url)); items.length = 0; list.innerHTML = ''; bulk.hidden = true; rerun.hidden = true; });
  }

  // ------------------------------------------------------------------ ordered file list (merge, images→PDF)
  function orderedList(accept, label) {
    const list = $('#files'), files = [];
    function render() {
      list.innerHTML = '';
      files.forEach((f, i) => {
        const li = document.createElement('li'); li.className = 'item row';
        li.innerHTML = '<span class="idx">' + (i + 1) + '</span><span class="name">' + esc(f.name) + '</span><span class="sizes">' + fmt(f.size) + '</span>' +
          '<span class="order"><button type="button" class="icon" data-a="up" aria-label="Move ' + esc(f.name) + ' up"' + (i ? '' : ' disabled') + '>↑</button>' +
          '<button type="button" class="icon" data-a="down" aria-label="Move ' + esc(f.name) + ' down"' + (i < files.length - 1 ? '' : ' disabled') + '>↓</button>' +
          '<button type="button" class="icon" data-a="rm" aria-label="Remove ' + esc(f.name) + '">✕</button></span>';
        li.addEventListener('click', (e) => {
          const a = e.target.dataset && e.target.dataset.a; if (!a) return;
          if (a === 'up') files.splice(i - 1, 0, files.splice(i, 1)[0]);
          if (a === 'down') files.splice(i + 1, 0, files.splice(i, 1)[0]);
          if (a === 'rm') files.splice(i, 1);
          render();
        });
        list.appendChild(li);
      });
      $('#go').disabled = !files.length;
      $('#go-row').hidden = !files.length;
    }
    onFiles = (fs) => {
      const ok = fs.filter(accept);
      if (!ok.length) return toast('Please choose ' + label + '.');
      files.push(...ok); render();
    };
    $('#sort') && $('#sort').addEventListener('click', () => { files.sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true })); render(); });
    return files;
  }
  function setBusy(btn, on, text) {
    btn.disabled = on;
    if (on) { btn.dataset.label = btn.textContent; btn.textContent = text; } else btn.textContent = btn.dataset.label || btn.textContent;
  }
  function showResult(html) { const r = $('#result'); r.innerHTML = html; r.hidden = false; }

  function encryptedError(name) { return new Error('“' + name + '” is password-protected or encrypted. Remove the protection first.'); }

  function initMerge() {
    const files = orderedList(isPdf, 'PDF files');
    $('#go').addEventListener('click', async () => {
      const btn = $('#go'); setBusy(btn, true, 'Merging…');
      try {
        await PdfShrink.ready();
        const out = await PDFLib.PDFDocument.create();
        let pages = 0;
        for (const f of files) {
          const src = await PDFLib.PDFDocument.load(await f.arrayBuffer(), { ignoreEncryption: true });
          if (src.isEncrypted) throw encryptedError(f.name);
          const copied = await out.copyPages(src, src.getPageIndices());
          copied.forEach((p) => out.addPage(p)); pages += copied.length;
          await tick();
        }
        const bytes = await out.save({ useObjectStreams: true });
        const blob = new Blob([bytes], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        showResult('<p>✓ Merged ' + files.length + ' files · ' + pages + ' pages · ' + fmt(blob.size) + '</p><a class="btn" download="merged.pdf" href="' + url + '">Download merged PDF</a> <a class="btn btn-ghost" href="/">Compress it →</a>');
        track('merged', { files: files.length, pages });
      } catch (e) { console.error(e); showResult('<p class="error">' + esc(e.message || 'Could not merge these files.') + '</p>'); }
      setBusy(btn, false);
    });
  }

  // Parse "1-3, 5, 8-" into zero-based page indices (in the order given).
  function parseRanges(s, n) {
    const out = [];
    for (const part of s.split(',').map((x) => x.trim()).filter(Boolean)) {
      const m = part.match(/^(\d*)\s*-\s*(\d*)$/);
      let a, b;
      if (m) { a = m[1] ? +m[1] : 1; b = m[2] ? +m[2] : n; } else if (/^\d+$/.test(part)) a = b = +part;
      else throw new Error('Could not understand “' + part + '”. Use a format like 1-3, 5, 8-10.');
      if (a < 1 || b > n || a > b) throw new Error('Page range “' + part + '” is outside 1–' + n + '.');
      for (let i = a; i <= b; i++) out.push(i - 1);
    }
    if (!out.length) throw new Error('Enter at least one page.');
    return out;
  }

  function initSplit() {
    let file = null, doc = null;
    const info = $('#doc-info');
    onFiles = async (fs) => {
      const f = fs.find(isPdf);
      if (!f) return toast('Please choose a PDF file.');
      file = f; info.textContent = 'Reading…'; $('#go-row').hidden = false;
      try {
        await PdfShrink.ready();
        doc = await PDFLib.PDFDocument.load(await f.arrayBuffer(), { ignoreEncryption: true });
        if (doc.isEncrypted) throw encryptedError(f.name);
        info.textContent = f.name + ' · ' + doc.getPageCount() + ' pages · ' + fmt(f.size);
        $('#go').disabled = false;
      } catch (e) { info.textContent = e.message || 'Could not read this PDF.'; doc = null; $('#go').disabled = true; }
    };
    const modeSel = $('#split-mode');
    const sync = () => { $('#range-row').hidden = modeSel.value !== 'extract'; $('#every-row').hidden = modeSel.value !== 'every'; };
    modeSel.addEventListener('change', sync); sync();
    $('#go').addEventListener('click', async () => {
      if (!doc) return;
      const btn = $('#go'); setBusy(btn, true, 'Splitting…');
      try {
        const n = doc.getPageCount(), base = baseName(file.name);
        const groups = [];
        if (modeSel.value === 'extract') groups.push({ idx: parseRanges($('#ranges').value, n), name: base + '-pages.pdf' });
        else {
          const k = modeSel.value === 'every' ? Math.max(1, parseInt($('#every').value, 10) || 1) : 1;
          for (let i = 0; i < n; i += k) {
            const idx = []; for (let j = i; j < Math.min(n, i + k); j++) idx.push(j);
            groups.push({ idx, name: base + '-' + (k === 1 ? 'page-' + (i + 1) : 'pages-' + (i + 1) + '-' + (i + idx.length)) + '.pdf' });
          }
        }
        const outs = [];
        for (const g of groups) {
          const out = await PDFLib.PDFDocument.create();
          (await out.copyPages(doc, g.idx)).forEach((p) => out.addPage(p));
          outs.push({ name: g.name, blob: new Blob([await out.save({ useObjectStreams: true })], { type: 'application/pdf' }) });
          await tick();
        }
        if (outs.length === 1) {
          const url = URL.createObjectURL(outs[0].blob);
          showResult('<p>✓ ' + groups[0].idx.length + ' pages · ' + fmt(outs[0].blob.size) + '</p><a class="btn" download="' + esc(outs[0].name) + '" href="' + url + '">Download PDF</a>');
        } else {
          showResult('<p>✓ Split into ' + outs.length + ' files</p><button type="button" class="btn" id="dlzip">Download all (ZIP)</button>');
          $('#dlzip').addEventListener('click', () => downloadZip(outs, base + '-split.zip'));
        }
        track('split', { mode: modeSel.value, files: outs.length });
      } catch (e) { showResult('<p class="error">' + esc(e.message) + '</p>'); }
      setBusy(btn, false);
    });
  }

  function initImagesToPdf() {
    const files = orderedList(isImg, 'image files (JPG, PNG, WebP…)');
    const SIZES = { a4: [595.28, 841.89], letter: [612, 792] };
    $('#go').addEventListener('click', async () => {
      const btn = $('#go'); setBusy(btn, true, 'Creating PDF…');
      try {
        await PdfShrink.ready();
        const out = await PDFLib.PDFDocument.create();
        const size = $('#page-size').value, margin = +$('#margin').value, q = +$('#quality').value;
        for (const f of files) {
          const src = await decodeImage(f);
          let { w, h } = dimsOf(src);
          const cap = 3000 / Math.max(w, h);
          if (cap < 1) { w = Math.round(w * cap); h = Math.round(h * cap); }
          const c = drawTo(src, w, h, 'contain');
          if (src.close) src.close();
          const img = await out.embedJpg(new Uint8Array(await (await toBlob(c, 'image/jpeg', q)).arrayBuffer()));
          let pw, ph;
          if (size === 'fit') { pw = w * 0.75 + margin * 2; ph = h * 0.75 + margin * 2; } // 96 px → 72 pt
          else { [pw, ph] = SIZES[size]; if (w > h) [pw, ph] = [ph, pw]; }
          const page = out.addPage([pw, ph]);
          const s = Math.min((pw - 2 * margin) / w, (ph - 2 * margin) / h);
          page.drawImage(img, { x: (pw - w * s) / 2, y: (ph - h * s) / 2, width: w * s, height: h * s });
          await tick();
        }
        const blob = new Blob([await out.save({ useObjectStreams: true })], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        showResult('<p>✓ ' + files.length + ' pages · ' + fmt(blob.size) + '</p><a class="btn" download="images.pdf" href="' + url + '">Download PDF</a> <a class="btn btn-ghost" href="/compress-pdf-to-100kb/">Need it smaller? →</a>');
        track('images_to_pdf', { count: files.length });
      } catch (e) { console.error(e); showResult('<p class="error">' + esc(e.message || 'Could not create the PDF.') + '</p>'); }
      setBusy(btn, false);
    });
  }

  function initPdfToImages() {
    let file = null;
    onFiles = (fs) => {
      const f = fs.find(isPdf);
      if (!f) return toast('Please choose a PDF file.');
      file = f; $('#doc-info').textContent = f.name + ' · ' + fmt(f.size); $('#go-row').hidden = false; $('#go').disabled = false;
    };
    $('#go').addEventListener('click', async () => {
      if (!file) return;
      const btn = $('#go'); setBusy(btn, true, 'Converting…');
      const res = $('#result'); res.hidden = false; res.innerHTML = '<p id="prog">Rendering…</p><div class="thumbs" id="thumbs"></div>';
      try {
        const pdfjs = await PdfShrink.getPdfjs();
        const doc = await pdfjs.getDocument({ data: new Uint8Array(await file.arrayBuffer()), isEvalSupported: false }).promise;
        const dpi = +$('#dpi').value, fmtSel = $('#ifmt').value, type = fmtSel === 'png' ? 'image/png' : 'image/jpeg';
        const outs = [], base = baseName(file.name);
        for (let n = 1; n <= doc.numPages; n++) {
          $('#prog').textContent = 'Rendering page ' + n + ' of ' + doc.numPages + '…';
          const page = await doc.getPage(n);
          const vp1 = page.getViewport({ scale: 1 });
          const scale = Math.min(dpi / 72, 8000 / Math.max(vp1.width, vp1.height));
          const vp = page.getViewport({ scale });
          const c = document.createElement('canvas'); c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
          const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
          await page.render({ canvasContext: g, viewport: vp }).promise;
          const blob = await toBlob(c, type, 0.9);
          const name = base + '-page-' + n + (fmtSel === 'png' ? '.png' : '.jpg');
          outs.push({ name, blob });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a'); a.href = url; a.download = name; a.className = 'thumbcard';
          a.innerHTML = '<img alt="Page ' + n + '" src="' + url + '"><span>Page ' + n + ' · ' + fmt(blob.size) + '</span>';
          $('#thumbs').appendChild(a);
          page.cleanup(); c.width = c.height = 0;
          await tick();
        }
        await doc.destroy();
        $('#prog').innerHTML = '✓ ' + outs.length + ' images. Click one to download, or ';
        const zb = document.createElement('button'); zb.type = 'button'; zb.className = 'btn btn-sm'; zb.textContent = 'Download all (ZIP)';
        zb.addEventListener('click', () => downloadZip(outs, base + '-images.zip'));
        $('#prog').appendChild(zb);
        track('pdf_to_images', { pages: outs.length, dpi });
      } catch (e) {
        console.error(e);
        res.innerHTML = '<p class="error">' + esc(/password/i.test(e.message) ? 'This PDF needs a password to open.' : 'Could not read this PDF.') + '</p>';
      }
      setBusy(btn, false);
    });
  }

  ({ image: initImage, merge: initMerge, split: initSplit, img2pdf: initImagesToPdf, pdf2img: initPdfToImages }[kind] || (() => {}))();
  if (kind !== 'image') { const w = () => PdfShrink.ready().catch(() => {}); ('requestIdleCallback' in window) ? requestIdleCallback(w, { timeout: 4000 }) : setTimeout(w, 2500); }
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
  }
})();

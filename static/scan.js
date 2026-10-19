/* "Make PDF look scanned" — renders each page (pdf.js) or image, then applies scanner effects on a
 * canvas: tilt, blur, colour mode, brightness/contrast, paper tone, grain, paper texture and edge
 * shadow; finally rebuilds a PDF of JPEG pages (pdf-lib) at the original page size.
 * Runs entirely in the browser. Uses PdfShrink.ready()/getPdfjs() from engine.js for libraries.
 * Effects use a seeded random generator, so the live preview matches the exported file exactly. */
(function () {
  'use strict';
  const tool = document.getElementById('tool');
  if (!tool || tool.dataset.tool !== 'scan') return;
  const $ = (s) => tool.querySelector(s);
  const t = window.__t || ((s, v) => { if (v) for (const k in v) s = s.split('{' + k + '}').join(v[k]); return s; });
  const fmt = (n) => (n >= 1048576 ? (n / 1048576).toFixed(2) + ' MB' : Math.max(1, Math.round(n / 1024)) + ' KB');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const tick = () => new Promise((r) => setTimeout(r, 0));
  const track = (name, props) => {
    try {
      if (navigator.globalPrivacyControl || navigator.doNotTrack === '1' || /^(localhost|127\.)/.test(location.hostname)) return;
      const body = JSON.stringify({ n: name, u: location.pathname, p: props || {} });
      if (!(navigator.sendBeacon && navigator.sendBeacon('/api/event', body))) fetch('/api/event', { method: 'POST', body, keepalive: true }).catch(() => {});
    } catch (e) { /* optional */ }
  };

  // ------------------------------------------------------------------ presets
  const PRESETS = {
    natural: { color: 'gray', rotate: 1.1, blur: 0.45, noise: 14, brightness: -2, contrast: 14, yellow: 22, texture: 45, edge: true, dpi: 150, quality: 0.62 },
    copier: { color: 'bw', rotate: 0.5, blur: 0.4, noise: 22, brightness: 8, contrast: 35, yellow: 0, texture: 15, edge: true, dpi: 150, quality: 0.62 },
    fax: { color: 'gray', rotate: 1.4, blur: 0.8, noise: 40, brightness: -4, contrast: 20, yellow: 45, texture: 55, edge: true, dpi: 110, quality: 0.5 },
    phone: { color: 'color', rotate: 1.2, blur: 0.5, noise: 14, brightness: -6, contrast: 6, yellow: 18, texture: 30, edge: false, dpi: 150, quality: 0.62 },
    clean: { color: 'color', rotate: 0.3, blur: 0.15, noise: 8, brightness: 2, contrast: 4, yellow: 4, texture: 10, edge: false, dpi: 200, quality: 0.8 },
  };

  // ------------------------------------------------------------------ seeded randomness
  function rng(seed) { // mulberry32
    let a = seed >>> 0;
    return () => {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let x = Math.imul(a ^ (a >>> 15), 1 | a);
      x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ------------------------------------------------------------------ effect pipeline
  // src: canvas with the clean page; scale: pixels per "150-DPI pixel" so preview and export look alike.
  function applyScan(src, o, seed, scale) {
    const W = src.width, H = src.height, rnd = rng(seed);
    const out = document.createElement('canvas'); out.width = W; out.height = H;
    const g = out.getContext('2d', { willReadFrequently: true });
    // scanner lid background + tilt + slight offset
    g.fillStyle = o.color === 'color' ? '#f4f3ef' : '#f2f2f2';
    g.fillRect(0, 0, W, H);
    const angle = ((rnd() * 2 - 1) * o.rotate * Math.PI) / 180;
    const dx = (rnd() * 2 - 1) * W * 0.004, dy = (rnd() * 2 - 1) * H * 0.004;
    g.save(); g.translate(W / 2 + dx, H / 2 + dy); g.rotate(angle);
    // blur via down/up-scaling (works in every browser, unlike ctx.filter)
    const b = o.blur * scale;
    if (b > 0.05) {
      const f = Math.max(0.25, 1 / (1 + b * 0.9));
      const tmp = document.createElement('canvas'); tmp.width = Math.max(1, Math.round(W * f)); tmp.height = Math.max(1, Math.round(H * f));
      const tg = tmp.getContext('2d'); tg.imageSmoothingQuality = 'high'; tg.drawImage(src, 0, 0, tmp.width, tmp.height);
      g.imageSmoothingQuality = 'high'; g.drawImage(tmp, -W / 2, -H / 2, W, H);
    } else g.drawImage(src, -W / 2, -H / 2, W, H);
    g.restore();

    // per-pixel: colour mode, brightness/contrast, paper tone, grain, low-frequency paper texture, edge shadow
    const img = g.getImageData(0, 0, W, H), p = img.data;
    const br = o.brightness * 2.55, ct = (100 + o.contrast * 1.5) / 100;
    const yel = o.yellow / 100, grain = o.noise * 0.55, tex = o.texture / 100;
    // scanner levels: real scans never reach pure white paper or pure black ink
    const lo = o.color === 'bw' ? 10 : 22, hi = o.color === 'bw' ? 250 : 242, lv = (hi - lo) / 255;
    // texture: coarse random grid, bilinearly sampled (cheap "paper fibre" blotches)
    const TS = Math.max(8, Math.round(48 * scale)), tw = Math.ceil(W / TS) + 2, th = Math.ceil(H / TS) + 2;
    const grid = new Float32Array(tw * th);
    for (let i = 0; i < grid.length; i++) grid[i] = rnd() * 2 - 1;
    const edgeW = o.edge ? W * 0.035 : 0, edgeSide = rnd() < 0.5 ? 0 : 1;
    // grain in clusters (~1 px at 150 DPI → 2×2 here): looks like real sensor noise and compresses far better
    const cell = Math.max(2, Math.round(1.6 * scale)), zrow = new Float32Array(Math.ceil(W / cell) + 1);
    for (let y = 0; y < H; y++) {
      const gy = y / TS, y0 = gy | 0, fy = gy - y0;
      if (y % cell === 0) for (let j = 0; j < zrow.length; j++) zrow[j] = (rnd() + rnd() - 1) * grain;
      for (let x = 0; x < W; x++) {
        const i = (y * W + x) * 4;
        let r = p[i], gg = p[i + 1], bb = p[i + 2];
        if (o.color !== 'color') { const l = r * 0.299 + gg * 0.587 + bb * 0.114; r = gg = bb = l; }
        // contrast + brightness
        r = (r - 128) * ct + 128 + br; gg = (gg - 128) * ct + 128 + br; bb = (bb - 128) * ct + 128 + br;
        if (o.color === 'bw') { // photocopy: crush toward black/white with a soft knee
          const l = r, v = l < 110 ? l * 0.35 : l > 170 ? 255 - (255 - l) * 0.25 : l;
          r = gg = bb = v;
        }
        r = lo + r * lv; gg = lo + gg * lv; bb = lo + bb * lv;
        // paper texture (multiplicative, stronger on light paper)
        const gx = x / TS, x0 = gx | 0, fx = gx - x0, k = y0 * tw + x0;
        const n = (grid[k] * (1 - fx) + grid[k + 1] * fx) * (1 - fy) + (grid[k + tw] * (1 - fx) + grid[k + tw + 1] * fx) * fy;
        const m = 1 + n * 0.06 * tex;
        // grain
        const z = zrow[(x / cell) | 0];
        r = r * m + z; gg = gg * m + z; bb = bb * m + z;
        // paper tone toward a warm off-white (only on light areas, so ink stays dark)
        const light = Math.max(0, (r + gg + bb) / 765 - 0.4) / 0.6;
        r -= yel * light * 4; gg -= yel * light * 10; bb -= yel * light * 34;
        // scanner edge shadow on one side
        if (edgeW) {
          const d = edgeSide ? W - 1 - x : x;
          if (d < edgeW) { const s = 1 - (1 - d / edgeW) * 0.22; r *= s; gg *= s; bb *= s; }
        }
        p[i] = r < 0 ? 0 : r > 255 ? 255 : r; p[i + 1] = gg < 0 ? 0 : gg > 255 ? 255 : gg; p[i + 2] = bb < 0 ? 0 : bb > 255 ? 255 : bb;
      }
    }
    g.putImageData(img, 0, 0);
    return out;
  }

  // ------------------------------------------------------------------ sources (PDF pages or images)
  let source = null; // { name, kind:'pdf'|'images', pdf?, files?, count, sizes:[{w,h}] (points) }
  let seed = (Math.random() * 1e9) | 0;
  async function loadFiles(files) {
    const pdfs = files.filter((f) => f.type === 'application/pdf' || /\.pdf$/i.test(f.name));
    const imgs = files.filter((f) => /^image\//.test(f.type) || /\.(jpe?g|png|webp|gif|bmp)$/i.test(f.name));
    if (!pdfs.length && !imgs.length) { status(t('Please choose a PDF or image files.')); return; }
    status(t('Reading…'));
    if (pdfs.length) {
      const pdfjs = await PdfShrink.getPdfjs();
      const data = new Uint8Array(await pdfs[0].arrayBuffer());
      let pdf;
      try { pdf = await pdfjs.getDocument({ data, isEvalSupported: false }).promise; }
      catch (e) { status(/password/i.test(e.message) ? t('This PDF needs a password to open.') : t('Could not read this PDF.')); return; }
      const sizes = [];
      for (let n = 1; n <= pdf.numPages; n++) { const vp = (await pdf.getPage(n)).getViewport({ scale: 1 }); sizes.push({ w: vp.width, h: vp.height }); }
      source = { name: pdfs[0].name, kind: 'pdf', pdf, count: pdf.numPages, sizes };
    } else {
      const sizes = [], bitmaps = [];
      for (const f of imgs) {
        const bm = await createImageBitmap(f, { imageOrientation: 'from-image' });
        bitmaps.push(bm);
        const a4 = bm.width > bm.height ? [841.89, 595.28] : [595.28, 841.89]; // each image on an A4 page
        sizes.push({ w: a4[0], h: a4[1] });
      }
      source = { name: imgs[0].name.replace(/\.[^.]+$/, '') + (imgs.length > 1 ? '-and-more' : '') + '.pdf', kind: 'images', bitmaps, count: imgs.length, sizes };
    }
    const sel = $('#sc-page'); sel.innerHTML = '';
    for (let i = 1; i <= source.count; i++) sel.add(new Option(t('Page {n}', { n: i }), i));
    $('#sc-work').hidden = false; $('#sc-file').textContent = source.name + ' · ' + t(source.count === 1 ? '{n} page' : '{n} pages', { n: source.count });
    status('');
    preview();
  }

  // Render one page (1-based) as a clean canvas at `dpi`.
  async function renderPage(n, dpi) {
    const sz = source.sizes[n - 1];
    const W = Math.round((sz.w / 72) * dpi), H = Math.round((sz.h / 72) * dpi);
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
    if (source.kind === 'pdf') {
      const page = await source.pdf.getPage(n);
      const vp = page.getViewport({ scale: dpi / 72 });
      await page.render({ canvasContext: g, viewport: vp }).promise;
      page.cleanup();
    } else {
      const bm = source.bitmaps[n - 1], margin = W * 0.06;
      const s = Math.min((W - margin * 2) / bm.width, (H - margin * 2) / bm.height);
      g.imageSmoothingQuality = 'high';
      g.drawImage(bm, (W - bm.width * s) / 2, (H - bm.height * s) / 2, bm.width * s, bm.height * s);
    }
    return c;
  }

  // ------------------------------------------------------------------ settings
  const ids = ['color', 'rotate', 'blur', 'noise', 'brightness', 'contrast', 'yellow', 'texture', 'dpi', 'quality'];
  function readOpts() {
    const o = {};
    for (const k of ids) { const el = $('#sc-' + k); o[k] = el.type === 'range' || el.tagName === 'SELECT' && k !== 'color' ? +el.value : el.value; }
    o.edge = $('#sc-edge').checked;
    if (!(o.quality > 0.3)) o.quality = 0.62;
    if (!(o.dpi >= 72)) o.dpi = 150;
    return o;
  }
  function setOpts(o) {
    for (const k of ids) {
      const el = $('#sc-' + k);
      if (!el || o[k] === undefined) continue;
      if (el.tagName === 'SELECT' && k !== 'color') { // snap to the nearest listed value
        const opts = Array.from(el.options).map((x) => +x.value);
        el.value = String(opts.reduce((a, b) => (Math.abs(b - o[k]) < Math.abs(a - o[k]) ? b : a)));
      } else el.value = o[k];
    }
    $('#sc-edge').checked = !!o.edge;
    syncLabels();
  }
  function syncLabels() {
    for (const el of tool.querySelectorAll('input[type=range]')) {
      const out = tool.querySelector('output[for="' + el.id + '"]');
      if (out) out.textContent = el.value + (el.dataset.unit || '');
    }
  }

  // ------------------------------------------------------------------ preview (debounced, WYSIWYG)
  let pvTimer = 0, pvToken = 0;
  function preview() {
    clearTimeout(pvTimer);
    pvTimer = setTimeout(async () => {
      if (!source) return;
      const token = ++pvToken, n = +$('#sc-page').value || 1, o = readOpts();
      const dpi = Math.min(o.dpi, 110); // fast preview; effects are scaled so it matches the export
      const clean = await renderPage(n, dpi);
      if (token !== pvToken) return;
      const out = applyScan(clean, o, seed + n * 7919, dpi / 150);
      if (token !== pvToken) return;
      const cv = $('#sc-preview'); cv.width = out.width; cv.height = out.height;
      cv.getContext('2d').drawImage(out, 0, 0);
      if ($('#sc-compare').checked) { const cc = $('#sc-before'); cc.hidden = false; cc.width = clean.width; cc.height = clean.height; cc.getContext('2d').drawImage(clean, 0, 0); }
      else $('#sc-before').hidden = true;
    }, 120);
  }

  // ------------------------------------------------------------------ export
  async function exportPdf() {
    const btn = $('#sc-go'); btn.disabled = true;
    const o = readOpts(), res = $('#result');
    res.hidden = true;
    try {
      await PdfShrink.ready();
      const out = await PDFLib.PDFDocument.create();
      for (let n = 1; n <= source.count; n++) {
        btn.textContent = t('Scanning page {i} of {n}…', { i: n, n: source.count });
        const clean = await renderPage(n, o.dpi);
        const scanned = applyScan(clean, o, seed + n * 7919, o.dpi / 150);
        const blob = await new Promise((r) => scanned.toBlob(r, 'image/jpeg', o.quality));
        const img = await out.embedJpg(new Uint8Array(await blob.arrayBuffer()));
        const { w, h } = source.sizes[n - 1];
        out.addPage([w, h]).drawImage(img, { x: 0, y: 0, width: w, height: h });
        clean.width = clean.height = scanned.width = scanned.height = 0;
        await tick();
      }
      out.setProducer('Scanner'); out.setCreator('Scanner');
      const bytes = await out.save({ useObjectStreams: true });
      const blob = new Blob([bytes], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob), name = source.name.replace(/\.pdf$/i, '') + '-scanned.pdf';
      res.innerHTML = '<p>✓ ' + esc(t('{n} pages', { n: source.count })) + ' · ' + fmt(blob.size) + '</p><a class="btn" download="' + esc(name) + '" href="' + url + '">' + esc(t('Download scanned PDF')) + '</a>';
      res.hidden = false;
      track('scanned', { pages: source.count, mode: o.color, dpi: o.dpi });
    } catch (e) {
      console.error(e);
      res.innerHTML = '<p class="error">' + esc(t('Could not create the PDF.')) + '</p>'; res.hidden = false;
    }
    btn.disabled = false; btn.textContent = t('Make it look scanned');
  }

  function status(msg) { const s = $('#sc-status'); s.textContent = msg; s.hidden = !msg; }

  // ------------------------------------------------------------------ wiring
  const drop = $('#drop'), input = $('#file');
  drop.addEventListener('click', () => input.click());
  drop.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
  input.addEventListener('change', () => { loadFiles(Array.from(input.files)); input.value = ''; });
  ['dragenter', 'dragover'].forEach((ev) => document.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add('over'); }));
  ['dragleave', 'drop'].forEach((ev) => document.addEventListener(ev, (e) => { e.preventDefault(); if (ev === 'drop' || e.target === document.documentElement) drop.classList.remove('over'); }));
  document.addEventListener('drop', (e) => { if (e.dataTransfer && e.dataTransfer.files.length) loadFiles(Array.from(e.dataTransfer.files)); });

  tool.querySelectorAll('[data-preset]').forEach((b) => b.addEventListener('click', () => {
    tool.querySelectorAll('[data-preset]').forEach((x) => x.setAttribute('aria-checked', String(x === b)));
    setOpts(PRESETS[b.dataset.preset]); preview();
  }));
  tool.querySelectorAll('.sc-controls input, .sc-controls select, #sc-page, #sc-compare').forEach((el) =>
    el.addEventListener(el.type === 'range' ? 'input' : 'change', () => { syncLabels(); preview(); }));
  $('#sc-shuffle').addEventListener('click', () => { seed = (Math.random() * 1e9) | 0; preview(); });
  $('#sc-go').addEventListener('click', exportPdf);
  setOpts(PRESETS[tool.dataset.preset || 'natural']);
  const w = () => PdfShrink.ready().catch(() => {}); ('requestIdleCallback' in window) ? requestIdleCallback(w, { timeout: 4000 }) : setTimeout(w, 2500);
  window.__scanTest = { applyScan, PRESETS, rng }; // used by automated tests
})();

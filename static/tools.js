/* Image + PDF utility tools: image to exact KB/size/DPI (+ name & date band), format conversion,
 * change DPI, merge, split, images→PDF, PDF→images, organize (rotate/delete/reorder), page numbers,
 * watermark, sign, unlock and PDF/image → text (OCR).
 * Everything runs locally in the browser; nothing is uploaded. Libraries are loaded
 * on demand through engine.js (PdfShrink.ready / PdfShrink.getPdfjs) or loadScript(). */
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

  // Decode any image the browser supports, honouring EXIF rotation. HEIC falls back to libheif (WebAssembly).
  const isHeic = (f) => /\.(heic|heif)$/i.test(f.name) || /hei[cf]/i.test(f.type);
  async function decodeImage(file) {
    try { return await createImageBitmap(file, { imageOrientation: 'from-image' }); }
    catch (e) {
      const url = URL.createObjectURL(file);
      try {
        const img = new Image(); img.src = url; await img.decode();
        return img;
      } catch (e2) {
        if (!isHeic(file)) throw new Error('This image format is not supported by your browser.');
      } finally { setTimeout(() => URL.revokeObjectURL(url), 1000); }
      try {
        await loadScript('/vendor/libheif-bundle.js'); // libheif (LGPL-3.0) compiled to WebAssembly
        if (!window.__heif) window.__heif = typeof libheif === 'function' ? libheif() : libheif;
        const imgs = new window.__heif.HeifDecoder().decode(new Uint8Array(await file.arrayBuffer()));
        if (!imgs || !imgs.length) throw new Error('empty');
        const im = imgs[0], w = im.get_width(), h = im.get_height();
        const c = document.createElement('canvas'); c.width = w; c.height = h;
        const g = c.getContext('2d'), id = g.createImageData(w, h);
        await new Promise((res, rej) => im.display(id, (d) => (d ? res() : rej(new Error('decode')))));
        g.putImageData(id, 0, 0);
        imgs.forEach((x) => x.free && x.free());
        return c;
      } catch (e3) { throw new Error('Could not read this HEIC photo. Try exporting it as JPG from your Photos app.'); }
    }
  }
  const dimsOf = (src) => ({ w: src.naturalWidth || src.width, h: src.naturalHeight || src.height });

  // Draw src into a w×h canvas. fit: 'contain' (stretch to w×h after proportional sizing) or 'cover' (crop).
  // opt.alpha keeps transparency (PNG/WebP); opt.lines prints a name/date band at the bottom.
  function drawTo(src, w, h, fit, opt) {
    opt = opt || {};
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const g = c.getContext('2d');
    if (!opt.alpha) { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); }
    g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
    const lines = (opt.lines || []).filter(Boolean);
    const band = lines.length ? Math.round(h * (lines.length > 1 ? 0.2 : 0.12)) : 0;
    const ih = h - band;
    const { w: sw, h: sh } = dimsOf(src);
    if (fit === 'cover' || band) {
      const s = Math.max(w / sw, ih / sh), cw = w / s, ch = ih / s;
      g.drawImage(src, (sw - cw) / 2, (sh - ch) / 2, cw, ch, 0, 0, w, ih);
    } else g.drawImage(src, 0, 0, w, h);
    if (band) {
      g.fillStyle = '#fff'; g.fillRect(0, ih, w, band);
      g.fillStyle = '#000'; g.textAlign = 'center'; g.textBaseline = 'middle';
      const lh = band / lines.length;
      lines.forEach((t, i) => {
        let size = Math.floor(lh * 0.72);
        g.font = '700 ' + size + 'px Arial, Helvetica, sans-serif';
        while (size > 6 && g.measureText(t).width > w * 0.94) { size--; g.font = '700 ' + size + 'px Arial, Helvetica, sans-serif'; }
        g.fillText(t, w / 2, ih + lh * (i + 0.5));
      });
    }
    return c;
  }
  const toBlob = (c, type, q) => new Promise((r) => c.toBlob(r, type, q));

  // Encode a canvas. For PNG, q maps to a colour palette (UPNG quantisation); q ≥ 0.95 is lossless.
  async function encode(c, format, q) {
    if (format !== 'png') return toBlob(c, format === 'webp' ? 'image/webp' : 'image/jpeg', q);
    if (q >= 0.95) return toBlob(c, 'image/png');
    await PdfShrink.ready(); // pako, needed by UPNG
    await loadScript('/vendor/UPNG.js');
    const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
    const colors = Math.max(2, Math.round(2 + q * q * 254));
    return new Blob([UPNG.encode([d.buffer], c.width, c.height, colors)], { type: 'image/png' });
  }

  // ---- DPI metadata (lossless): JPEG JFIF/EXIF density, PNG pHYs.
  async function setDpi(blob, dpi) {
    const b = new Uint8Array(await blob.arrayBuffer());
    if (b[0] === 0xff && b[1] === 0xd8) return new Blob([jpegDpi(b, dpi)], { type: 'image/jpeg' });
    if (b[0] === 0x89 && b[1] === 0x50) return new Blob([pngDpi(b, dpi)], { type: 'image/png' });
    return blob;
  }
  function jpegDpi(b, dpi) {
    const hi = (dpi >> 8) & 255, lo = dpi & 255;
    let hasJfif = false;
    for (let i = 2; i + 4 < b.length && b[i] === 0xff;) {
      const m = b[i + 1], len = (b[i + 2] << 8) | b[i + 3];
      if (m === 0xda) break; // start of scan
      if (m === 0xe0 && String.fromCharCode(b[i + 4], b[i + 5], b[i + 6], b[i + 7]) === 'JFIF') {
        b[i + 11] = 1; b[i + 12] = hi; b[i + 13] = lo; b[i + 14] = hi; b[i + 15] = lo; hasJfif = true;
      }
      if (m === 0xe1 && String.fromCharCode(b[i + 4], b[i + 5], b[i + 6], b[i + 7]) === 'Exif') exifDpi(b, i + 10, dpi);
      i += 2 + len;
    }
    if (hasJfif) return b;
    const app0 = [0xff, 0xe0, 0, 16, 0x4a, 0x46, 0x49, 0x46, 0, 1, 1, 1, hi, lo, hi, lo, 0, 0];
    const out = new Uint8Array(b.length + app0.length);
    out.set(b.subarray(0, 2)); out.set(app0, 2); out.set(b.subarray(2), 2 + app0.length);
    return out;
  }
  function exifDpi(b, t, dpi) { // t = start of TIFF header
    const le = b[t] === 0x49;
    const u16 = (o) => (le ? b[o] | (b[o + 1] << 8) : (b[o] << 8) | b[o + 1]);
    const u32 = (o) => (le ? (b[o] | (b[o + 1] << 8) | (b[o + 2] << 16)) + b[o + 3] * 16777216 : b[o] * 16777216 + ((b[o + 1] << 16) | (b[o + 2] << 8) | b[o + 3]));
    const w32 = (o, v) => { const a = [(v >>> 24) & 255, (v >>> 16) & 255, (v >>> 8) & 255, v & 255]; (le ? a.reverse() : a).forEach((x, k) => (b[o + k] = x)); };
    const ifd = t + u32(t + 4), n = u16(ifd);
    for (let k = 0; k < n; k++) {
      const e = ifd + 2 + k * 12, tag = u16(e);
      if (tag === 0x011a || tag === 0x011b) { const off = t + u32(e + 8); w32(off, dpi); w32(off + 4, 1); }
      if (tag === 0x0128) { if (le) { b[e + 8] = 2; b[e + 9] = 0; } else { b[e + 8] = 0; b[e + 9] = 2; } }
    }
  }
  const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  function crc32(bytes) { let c = 0xffffffff; for (const x of bytes) c = CRC[(c ^ x) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
  function pngDpi(b, dpi) {
    const ppm = Math.round(dpi / 0.0254), parts = [b.subarray(0, 8)];
    const be = (v) => [(v >>> 24) & 255, (v >>> 16) & 255, (v >>> 8) & 255, v & 255];
    for (let i = 8; i < b.length;) {
      const len = (b[i] << 24 >>> 0) + (b[i + 1] << 16) + (b[i + 2] << 8) + b[i + 3], type = String.fromCharCode(b[i + 4], b[i + 5], b[i + 6], b[i + 7]);
      const chunk = b.subarray(i, i + 12 + len);
      if (type !== 'pHYs') parts.push(chunk);
      if (type === 'IHDR') {
        const body = new Uint8Array([0x70, 0x48, 0x59, 0x73, ...be(ppm), ...be(ppm), 1]);
        parts.push(new Uint8Array([0, 0, 0, 9, ...body, ...be(crc32(body))]));
      }
      i += 12 + len;
    }
    const out = new Uint8Array(parts.reduce((a, p) => a + p.length, 0));
    let o = 0; for (const p of parts) { out.set(p, o); o += p.length; }
    return out;
  }

  // Convert a length in the chosen unit to pixels at dpi.
  const toPx = (v, unit, dpi) => Math.round(unit === 'cm' ? (v / 2.54) * dpi : unit === 'mm' ? (v / 25.4) * dpi : unit === 'in' ? v * dpi : v);

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
    const draw = { alpha: o.format !== 'jpg', lines: o.lines };
    const maxB = o.maxBytes, minB = o.minBytes || 0, maxLabel = o.maxLabel || fmt(maxB);
    const finish = async (r) => (o.dpi ? Object.assign(r, { blob: await setDpi(r.blob, o.dpi) }) : r);
    let best = null, smallest = null;
    const consider = (b, w, h, q) => {
      const r = { blob: b, w, h, q };
      if (!smallest || b.size < smallest.blob.size) smallest = r;
      return r;
    };
    if (!maxB) {
      const c = drawTo(src, tw, th, fit, draw);
      if (src.close) src.close();
      return finish({ blob: await encode(c, o.format, o.quality || 0.85), w: tw, h: th, hit: true });
    }
    // Shrink resolution until a reasonable quality (≥ 0.5) fits, unless the user fixed the dimensions.
    let scale = 1;
    for (let round = 0; round < 25; round++) {
      const w = Math.max(16, Math.round(tw * scale)), h = Math.max(16, Math.round(th * scale));
      const c = drawTo(src, w, h, fit, draw);
      let lo = 0.05, hi = 0.95, found = null;
      const top = await encode(c, o.format, hi);
      consider(top, w, h, hi);
      if (top.size <= maxB) found = { blob: top, w, h, q: hi };
      else {
        for (let i = 0; i < 7; i++) {
          const q = (lo + hi) / 2, b = await encode(c, o.format, q);
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
    const res = await finish({ blob: r.blob, w: r.w, h: r.h, hit: !!best && r.blob.size <= maxB });
    if (res.blob.size > maxB) res.hit = false; // DPI metadata adds a few bytes
    if (res.hit && minB && res.blob.size < minB) res.note = 'Below the ' + o.minLabel + ' minimum — use larger dimensions or a bigger photo.';
    if (!res.hit) res.note = fixed ? 'Could not fit these dimensions under ' + maxLabel + ' — try smaller dimensions.' : 'Could not reach ' + maxLabel + '.';
    return res;
  }

  const EXT = { jpg: '.jpg', png: '.png', webp: '.webp' };
  function fmtDate(iso, style) {
    if (!iso) return '';
    const [y, m, d] = iso.split('-');
    return { dmy: d + '-' + m + '-' + y, 'dmy/': d + '/' + m + '/' + y, 'dmy.': d + '.' + m + '.' + y, mdy: m + '/' + d + '/' + y, ymd: y + '-' + m + '-' + d }[style] || d + '-' + m + '-' + y;
  }

  function initImage() {
    const list = $('#files'), bulk = $('#bulk'), rerun = $('#rerun');
    const tsize = $('#tsize'), tunit = $('#tunit');
    const items = [];
    tsize.value = tool.dataset.targetKb || '';
    const now = new Date(), pad2 = (n) => String(n).padStart(2, '0'); // local date, not UTC
    $('#tdate').value = now.getFullYear() + '-' + pad2(now.getMonth() + 1) + '-' + pad2(now.getDate());
    $$('.chip[data-kb]').forEach((c) => c.addEventListener('click', () => { tsize.value = c.dataset.kb; tunit.value = 'KB'; stale(); }));
    $$('.chip[data-w]').forEach((c) => c.addEventListener('click', () => {
      $('#iw').value = c.dataset.w; $('#ih').value = c.dataset.h; $('#unit').value = c.dataset.unit || 'px';
      if (c.dataset.dpi) $('#dpi').value = c.dataset.dpi;
      $('#fit').value = 'cover'; if (c.dataset.kb) tsize.value = c.dataset.kb; syncUnit(); stale();
    }));
    const syncUnit = () => { $('#dpi').placeholder = $('#unit').value === 'px' ? 'keep' : '200'; };
    $('#unit').addEventListener('change', syncUnit); syncUnit();
    const syncText = () => { $('#text-row').hidden = !$('#addtext').checked; };
    $('#addtext').addEventListener('change', syncText); syncText();
    const syncFmt = () => { $('#quality-row').hidden = !!parseFloat(tsize.value); };
    tsize.addEventListener('input', syncFmt); syncFmt();
    $$('input,select', $('.opts')).forEach((el) => el.addEventListener('change', stale));
    function stale() { if (items.some((i) => i.out)) rerun.hidden = false; }
    function opts() {
      const v = parseFloat(tsize.value), mul = tunit.value === 'MB' ? 1e6 : 1000; // 1000-byte KB passes both conventions
      const mn = parseFloat($('#tmin').value);
      const unit = $('#unit').value, dpi = parseInt($('#dpi').value, 10) || (unit !== 'px' ? 200 : 0); // physical sizes need a DPI
      const pxDpi = dpi || 96;
      const iw = parseFloat($('#iw').value) || 0, ih = parseFloat($('#ih').value) || 0;
      const lines = $('#addtext').checked ? [$('#tname').value.trim(), fmtDate($('#tdate').value, $('#tdfmt').value)] : [];
      return {
        maxBytes: v > 0 ? Math.floor(v * mul) : 0, minBytes: mn > 0 ? Math.ceil(mn * 1024) : 0,
        width: iw ? toPx(iw, unit, pxDpi) : 0, height: ih ? toPx(ih, unit, pxDpi) : 0,
        fit: $('#fit').value, format: $('#fmt').value, quality: +$('#quality').value, dpi,
        lines, maxLabel: tsize.value + ' ' + tunit.value, minLabel: (mn || 0) + ' KB',
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
        st.textContent = 'Processing…'; bar.style.width = '40%';
        try {
          const r = await imageToSize(file, o);
          const ext = EXT[o.format] || '.jpg';
          const name = baseName(file.name) + (o.maxBytes ? '-' + Math.max(1, Math.round(r.blob.size / 1024)) + 'kb' : '') + ext;
          it.out = { url: URL.createObjectURL(r.blob), name, blob: r.blob };
          bar.style.width = '100%';
          sizes.innerHTML = fmt(file.size) + ' → <b>' + fmt(r.blob.size) + '</b>';
          st.textContent = (o.maxBytes ? (r.hit ? '✓ Under ' : '✗ Above ') + o.maxLabel + ' · ' : '✓ ') + r.w + '×' + r.h + ' px' + (o.dpi ? ' · ' + o.dpi + ' DPI' : '');
          li.classList.add(r.hit && !r.note ? 'done' : 'miss');
          actions.innerHTML = '<img class="thumb" alt="Preview of ' + esc(name) + '" src="' + it.out.url + '"><a class="btn btn-sm" download="' + esc(name) + '" href="' + it.out.url + '">Download</a>';
          if (r.note) { const n = document.createElement('p'); n.className = 'note'; n.textContent = r.note; li.appendChild(n); }
          track('image_resized', { hit: r.hit, kb: Math.round(o.maxBytes / 1000), mode: o.format + (o.lines.length ? '+text' : '') + (o.dpi ? '+dpi' : '') });
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
        let bytes = await out.save({ useObjectStreams: true }), note = '';
        const maxKb = parseFloat(($('#pdfmax') || {}).value);
        if (maxKb > 0 && bytes.length > maxKb * 1000) {
          btn.textContent = 'Fitting under ' + maxKb + ' KB…';
          const r = await PdfShrink.compress(bytes, { targetBytes: Math.floor(maxKb * 1000) });
          bytes = r.bytes;
          note = r.hit ? ' · ✓ under ' + maxKb + ' KB' : ' · ✗ could not reach ' + maxKb + ' KB — try fewer images or “Small file” quality';
        }
        const blob = new Blob([bytes], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        showResult('<p>✓ ' + files.length + ' pages · ' + fmt(blob.size) + esc(note) + '</p><a class="btn" download="images.pdf" href="' + url + '">Download PDF</a>' + (maxKb > 0 ? '' : ' <a class="btn btn-ghost" href="/compress-pdf-to-100kb/">Need it smaller? →</a>'));
        track('images_to_pdf', { count: files.length, kb: maxKb || 0 });
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


  // ------------------------------------------------------------------ change DPI (lossless metadata)
  function initDpi() {
    const list = $('#files'), bulk = $('#bulk'), items = [];
    $$('.chip[data-dpi]').forEach((c) => c.addEventListener('click', () => { $('#dpival').value = c.dataset.dpi; if (items.length) run(); }));
    $('#dpival').addEventListener('change', () => items.length && run());
    onFiles = (fs) => {
      const imgs = fs.filter(isImg);
      if (!imgs.length) return toast('Please choose JPG or PNG images.');
      imgs.forEach((f) => items.push({ file: f }));
      run();
    };
    async function run() {
      const dpi = Math.max(1, Math.min(65535, parseInt($('#dpival').value, 10) || 300));
      list.innerHTML = '';
      for (const it of items) {
        const li = document.createElement('li'); li.className = 'item';
        list.appendChild(li);
        try {
          let blob = it.file, converted = false;
          if (!/^image\/(jpeg|png)$/.test(it.file.type) && !/\.(jpe?g|png)$/i.test(it.file.name)) {
            const src = await decodeImage(it.file), d = dimsOf(src);
            const c = drawTo(src, d.w, d.h, 'contain');
            blob = await toBlob(c, 'image/jpeg', 0.92); converted = true;
          }
          const out = await setDpi(blob, dpi);
          const name = baseName(it.file.name) + '-' + dpi + 'dpi' + (/png/.test(out.type) ? '.png' : '.jpg');
          if (it.url) URL.revokeObjectURL(it.url);
          it.url = URL.createObjectURL(out); it.out = { name, blob: out };
          li.classList.add('done');
          li.innerHTML = '<div class="item-top"><span class="name">' + esc(it.file.name) + '</span><span class="sizes">' + fmt(out.size) + '</span></div>' +
            '<div class="item-bottom"><span class="status">✓ ' + dpi + ' DPI' + (converted ? ' · converted to JPG' : ' · pixels unchanged') + '</span>' +
            '<span class="actions"><a class="btn btn-sm" download="' + esc(name) + '" href="' + it.url + '">Download</a></span></div>';
        } catch (e) {
          li.classList.add('err'); li.innerHTML = '<span class="name">' + esc(it.file.name) + '</span> <span class="status">' + esc(e.message) + '</span>';
        }
      }
      bulk.hidden = items.length < 2;
      track('dpi_changed', { dpi, count: items.length });
    }
    $('#zip').addEventListener('click', () => downloadZip(items.filter((i) => i.out).map((i) => i.out), 'dpi-images.zip'));
    $('#clear').addEventListener('click', () => { items.length = 0; list.innerHTML = ''; bulk.hidden = true; });
  }

  // ------------------------------------------------------------------ shared: load one PDF (decrypting restriction-only files)
  let cantooP;
  function loadCantoo() {
    if (!cantooP) {
      cantooP = (async () => {
        await PdfShrink.ready();
        const orig = window.PDFLib;
        await loadScript('/vendor/pdf-lib-cantoo.min.js');
        const lib = window.PDFLib; window.PDFLib = orig; // keep the main pdf-lib global intact
        return lib;
      })();
    }
    return cantooP;
  }
  async function decryptBytes(bytes, password) {
    const C = await loadCantoo();
    const d = await C.PDFDocument.load(bytes, { password: password || '', ignoreEncryption: false });
    return new Uint8Array(await d.save({ useObjectStreams: true }));
  }
  async function openPdf(file) {
    await PdfShrink.ready();
    let bytes = new Uint8Array(await file.arrayBuffer());
    let doc = await PDFLib.PDFDocument.load(bytes, { ignoreEncryption: true });
    if (doc.isEncrypted) {
      try { bytes = await decryptBytes(bytes, ''); doc = await PDFLib.PDFDocument.load(bytes); }
      catch (e) { throw new Error('This PDF needs a password. Unlock it first with the Unlock PDF tool.'); }
    }
    return { doc, bytes };
  }
  function pickPdf(cb) {
    onFiles = async (fs) => {
      const f = fs.find(isPdf);
      if (!f) return toast('Please choose a PDF file.');
      $('#doc-info').textContent = 'Reading ' + f.name + '…';
      try { const r = await openPdf(f); $('#doc-info').textContent = f.name + ' · ' + r.doc.getPageCount() + ' pages · ' + fmt(f.size); await cb(f, r.doc, r.bytes); }
      catch (e) { console.error(e); $('#doc-info').textContent = e.message || 'Could not read this PDF.'; }
    };
  }
  async function deliverPdf(doc, name, msg, event, props) {
    const blob = new Blob([await doc.save({ useObjectStreams: true })], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    showResult('<p>✓ ' + esc(msg) + ' · ' + fmt(blob.size) + '</p><a class="btn" download="' + esc(name) + '" href="' + url + '">Download PDF</a>');
    track(event, props || {});
  }
  // Map a point in the page's *visual* coordinates (origin bottom-left, as displayed) to PDF user space.
  function visual(page) {
    const r = ((page.getRotation().angle % 360) + 360) % 360;
    const box = page.getCropBox ? page.getCropBox() : page.getMediaBox();
    const w = box.width, h = box.height, ox = box.x, oy = box.y;
    const vw = r % 180 ? h : w, vh = r % 180 ? w : h;
    const map = (vx, vy) => {
      if (r === 90) return { x: ox + w - vy, y: oy + vx };
      if (r === 180) return { x: ox + w - vx, y: oy + h - vy };
      if (r === 270) return { x: ox + vy, y: oy + h - vx };
      return { x: ox + vx, y: oy + vy };
    };
    return { r, vw, vh, map };
  }

  // ------------------------------------------------------------------ organize: rotate / delete / reorder
  function initOrganize() {
    let file = null, srcDoc = null, pages = [];
    const grid = $('#pages');
    pickPdf(async (f, doc, bytes) => {
      file = f; srcDoc = doc;
      pages = doc.getPages().map((p, i) => ({ i, rot: 0, del: false }));
      $('#go-row').hidden = false; $('#go').disabled = false; $('#org-actions').hidden = false;
      render();
      // Thumbnails (best effort; editing works without them).
      try {
        const pdfjs = await PdfShrink.getPdfjs();
        const pd = await pdfjs.getDocument({ data: bytes.slice(), isEvalSupported: false }).promise;
        for (let n = 1; n <= pd.numPages; n++) {
          const pg = await pd.getPage(n), vp1 = pg.getViewport({ scale: 1 }), vp = pg.getViewport({ scale: 150 / Math.max(vp1.width, vp1.height) });
          const c = document.createElement('canvas'); c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
          const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
          await pg.render({ canvasContext: g, viewport: vp }).promise;
          pages[n - 1].thumb = c.toDataURL('image/jpeg', 0.7);
          const img = grid.querySelector('[data-src="' + (n - 1) + '"] img'); if (img) img.src = pages[n - 1].thumb;
          await tick();
        }
        await pd.destroy();
      } catch (e) { console.warn('thumbnails unavailable', e); }
    });
    function render() {
      grid.innerHTML = '';
      pages.forEach((p, k) => {
        const li = document.createElement('li');
        li.className = 'pagecard' + (p.del ? ' deleted' : ''); li.dataset.src = p.i;
        li.innerHTML = '<div class="pthumb"><img alt="Page ' + (p.i + 1) + '" src="' + (p.thumb || 'data:image/gif;base64,R0lGODlhAQABAAAAACw=') + '" style="transform:rotate(' + p.rot + 'deg)"></div>' +
          '<span class="pnum">' + (p.i + 1) + (p.del ? ' · deleted' : p.rot ? ' · ' + p.rot + '°' : '') + '</span><span class="pbtns">' +
          '<button type="button" class="icon" data-a="left" aria-label="Move page ' + (p.i + 1) + ' earlier"' + (k ? '' : ' disabled') + '>←</button>' +
          '<button type="button" class="icon" data-a="ccw" aria-label="Rotate page ' + (p.i + 1) + ' left">⟲</button>' +
          '<button type="button" class="icon" data-a="cw" aria-label="Rotate page ' + (p.i + 1) + ' right">⟳</button>' +
          '<button type="button" class="icon" data-a="del" aria-pressed="' + p.del + '" aria-label="' + (p.del ? 'Restore' : 'Delete') + ' page ' + (p.i + 1) + '">' + (p.del ? '↺' : '✕') + '</button>' +
          '<button type="button" class="icon" data-a="right" aria-label="Move page ' + (p.i + 1) + ' later"' + (k < pages.length - 1 ? '' : ' disabled') + '>→</button></span>';
        li.addEventListener('click', (e) => {
          const a = e.target.dataset && e.target.dataset.a; if (!a) return;
          if (a === 'cw') p.rot = (p.rot + 90) % 360;
          if (a === 'ccw') p.rot = (p.rot + 270) % 360;
          if (a === 'del') p.del = !p.del;
          if (a === 'left') pages.splice(k - 1, 0, pages.splice(k, 1)[0]);
          if (a === 'right') pages.splice(k + 1, 0, pages.splice(k, 1)[0]);
          render();
          const btn = grid.querySelector('[data-src="' + p.i + '"] [data-a="' + a + '"]'); if (btn && !btn.disabled) btn.focus();
        });
        grid.appendChild(li);
      });
      const kept = pages.filter((p) => !p.del).length;
      $('#org-summary').textContent = kept + ' of ' + pages.length + ' pages will be kept';
    }
    $('#rot-all-cw').addEventListener('click', () => { pages.forEach((p) => (p.rot = (p.rot + 90) % 360)); render(); });
    $('#rot-all-ccw').addEventListener('click', () => { pages.forEach((p) => (p.rot = (p.rot + 270) % 360)); render(); });
    $('#del-range').addEventListener('click', () => {
      try { const idx = new Set(parseRanges($('#delpages').value, pages.length)); pages.forEach((p) => { if (idx.has(p.i)) p.del = true; }); render(); }
      catch (e) { toast(e.message); }
    });
    $('#reverse').addEventListener('click', () => { pages.reverse(); render(); });
    $('#reset').addEventListener('click', () => { pages.sort((a, b) => a.i - b.i).forEach((p) => { p.rot = 0; p.del = false; }); render(); });
    $('#go').addEventListener('click', async () => {
      const keep = pages.filter((p) => !p.del);
      if (!keep.length) return toast('You deleted every page — keep at least one.');
      const btn = $('#go'); setBusy(btn, true, 'Saving…');
      try {
        const out = await PDFLib.PDFDocument.create();
        const copied = await out.copyPages(srcDoc, keep.map((p) => p.i));
        copied.forEach((pg, k) => {
          if (keep[k].rot) pg.setRotation(PDFLib.degrees((pg.getRotation().angle + keep[k].rot) % 360));
          out.addPage(pg);
        });
        const changes = { rotated: keep.filter((p) => p.rot).length, deleted: pages.length - keep.length };
        await deliverPdf(out, baseName(file.name) + '-edited.pdf', keep.length + ' pages' + (changes.deleted ? ' · ' + changes.deleted + ' deleted' : '') + (changes.rotated ? ' · ' + changes.rotated + ' rotated' : ''), 'organized', { pages: keep.length, files: changes.deleted, count: changes.rotated });
      } catch (e) { console.error(e); showResult('<p class="error">' + esc(e.message) + '</p>'); }
      setBusy(btn, false);
    });
  }

  // ------------------------------------------------------------------ page numbers
  function initPageNumbers() {
    let file = null, doc = null;
    pickPdf((f, d) => { file = f; doc = d; $('#go-row').hidden = false; $('#go').disabled = false; });
    $('#go').addEventListener('click', async () => {
      if (!doc) return;
      const btn = $('#go'); setBusy(btn, true, 'Numbering…');
      try {
        const work = await PDFLib.PDFDocument.load(await doc.save());
        const font = await work.embedFont(PDFLib.StandardFonts.Helvetica);
        const pos = $('#pn-pos').value, style = $('#pn-style').value, size = +$('#pn-size').value, start = parseInt($('#pn-start').value, 10) || 1;
        const skipFirst = $('#pn-skip').checked, all = work.getPages(), total = all.length - (skipFirst ? 1 : 0), m = 28;
        all.forEach((page, k) => {
          if (skipFirst && k === 0) return;
          const n = start + k - (skipFirst ? 1 : 0), last = start + total - 1;
          const text = { n: String(n), page: 'Page ' + n, of: n + ' / ' + last, pageof: 'Page ' + n + ' of ' + last }[style];
          const v = visual(page), tw = font.widthOfTextAtSize(text, size);
          const vx = pos.endsWith('left') ? m : pos.endsWith('right') ? v.vw - m - tw : (v.vw - tw) / 2;
          const vy = pos.startsWith('top') ? v.vh - m - size : m;
          const p = v.map(vx, vy);
          page.drawText(text, { x: p.x, y: p.y, size, font, color: PDFLib.rgb(0, 0, 0), rotate: PDFLib.degrees(v.r) });
        });
        await deliverPdf(work, baseName(file.name) + '-numbered.pdf', 'Numbered ' + total + ' pages', 'page_numbers', { pages: total, mode: style });
      } catch (e) { console.error(e); showResult('<p class="error">' + esc(e.message) + '</p>'); }
      setBusy(btn, false);
    });
  }

  // ------------------------------------------------------------------ watermark
  function initWatermark() {
    let file = null, doc = null;
    pickPdf((f, d) => { file = f; doc = d; $('#go-row').hidden = false; $('#go').disabled = false; });
    $('#go').addEventListener('click', async () => {
      if (!doc) return;
      const text = $('#wm-text').value.trim();
      if (!text) return toast('Type the watermark text first.');
      const btn = $('#go'); setBusy(btn, true, 'Adding watermark…');
      try {
        const work = await PDFLib.PDFDocument.load(await doc.save());
        const font = await work.embedFont(PDFLib.StandardFonts.HelveticaBold);
        const opacity = +$('#wm-opacity').value, angle = +$('#wm-angle').value;
        const col = { gray: [0.5, 0.5, 0.5], red: [0.8, 0.1, 0.1], blue: [0.1, 0.3, 0.8] }[$('#wm-color').value];
        work.getPages().forEach((page) => {
          const v = visual(page);
          const size = Math.min(+$('#wm-size').value, (Math.hypot(v.vw, v.vh) * 0.8) / Math.max(1, font.widthOfTextAtSize(text, 1)));
          const tw = font.widthOfTextAtSize(text, size), th = font.heightAtSize(size, { descender: false });
          const a = (angle * Math.PI) / 180;
          // start point so the text's centre sits at the visual centre
          const vx = v.vw / 2 - (Math.cos(a) * tw) / 2 + (Math.sin(a) * th) / 2;
          const vy = v.vh / 2 - (Math.sin(a) * tw) / 2 - (Math.cos(a) * th) / 2;
          const p = v.map(vx, vy);
          page.drawText(text, { x: p.x, y: p.y, size, font, color: PDFLib.rgb(...col), opacity, rotate: PDFLib.degrees(v.r + angle) });
        });
        await deliverPdf(work, baseName(file.name) + '-watermarked.pdf', 'Watermark added to ' + work.getPageCount() + ' pages', 'watermarked', { pages: work.getPageCount() });
      } catch (e) { console.error(e); showResult('<p class="error">' + esc(e.message) + '</p>'); }
      setBusy(btn, false);
    });
  }

  // ------------------------------------------------------------------ sign PDF
  function initSign() {
    let file = null, doc = null, pdfjsDoc = null, sig = null, placements = [];
    const pad = $('#sigpad'), pg = pad.getContext('2d');
    const prev = $('#preview'), overlay = $('#overlay');
    // --- signature pad
    function resetPad() { pg.clearRect(0, 0, pad.width, pad.height); pg.lineWidth = 3; pg.lineCap = pg.lineJoin = 'round'; pg.strokeStyle = $('#sig-color').value; drawn = false; }
    let drawing = false, drawn = false;
    const pt = (e) => { const r = pad.getBoundingClientRect(); return [((e.clientX - r.left) * pad.width) / r.width, ((e.clientY - r.top) * pad.height) / r.height]; };
    pad.addEventListener('pointerdown', (e) => { drawing = true; pad.setPointerCapture(e.pointerId); pg.beginPath(); pg.moveTo(...pt(e)); });
    pad.addEventListener('pointermove', (e) => { if (!drawing) return; pg.lineTo(...pt(e)); pg.stroke(); drawn = true; });
    ['pointerup', 'pointercancel'].forEach((t) => pad.addEventListener(t, () => { drawing = false; }));
    resetPad();
    $('#sig-clear').addEventListener('click', resetPad);
    $('#sig-color').addEventListener('change', () => { pg.strokeStyle = $('#sig-color').value; });
    const modeSel = $('#sig-mode');
    const syncMode = () => { $('#sig-draw').hidden = modeSel.value !== 'draw'; $('#sig-type').hidden = modeSel.value !== 'type'; $('#sig-upload').hidden = modeSel.value !== 'upload'; };
    modeSel.addEventListener('change', syncMode); syncMode();
    let uploaded = null;
    $('#sig-file').addEventListener('change', async () => { const f = $('#sig-file').files[0]; if (f) uploaded = await decodeImage(f); });
    // Crop transparent/white margins and return a PNG canvas of the signature.
    function makeSignature() {
      let c;
      if (modeSel.value === 'draw') { if (!drawn) throw new Error('Draw your signature in the box first.'); c = pad; }
      else if (modeSel.value === 'type') {
        const t = $('#sig-text').value.trim(); if (!t) throw new Error('Type your name first.');
        c = document.createElement('canvas'); c.width = 900; c.height = 260;
        const g = c.getContext('2d'); g.fillStyle = $('#sig-color').value; g.textBaseline = 'middle';
        g.font = 'italic 120px "Segoe Script", "Brush Script MT", "Snell Roundhand", cursive';
        g.fillText(t, 20, 130, 860);
      } else {
        if (!uploaded) throw new Error('Choose a signature image first.');
        const d = dimsOf(uploaded); c = document.createElement('canvas'); c.width = d.w; c.height = d.h;
        const g = c.getContext('2d'); g.drawImage(uploaded, 0, 0);
        const id = g.getImageData(0, 0, d.w, d.h), px = id.data; // make near-white transparent
        for (let i = 0; i < px.length; i += 4) if (px[i] > 230 && px[i + 1] > 230 && px[i + 2] > 230) px[i + 3] = 0;
        g.putImageData(id, 0, 0);
      }
      const g = c.getContext('2d'), { width: W, height: H } = c, d = g.getImageData(0, 0, W, H).data;
      let x0 = W, y0 = H, x1 = 0, y1 = 0;
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (d[(y * W + x) * 4 + 3] > 10) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      if (x1 <= x0) throw new Error('The signature is empty.');
      const out = document.createElement('canvas'); out.width = x1 - x0 + 9; out.height = y1 - y0 + 9;
      out.getContext('2d').drawImage(c, x0 - 4, y0 - 4, out.width, out.height, 0, 0, out.width, out.height);
      return out;
    }
    // --- PDF preview + placement
    pickPdf(async (f, d, bytes) => {
      file = f; doc = d; placements = [];
      const pdfjs = await PdfShrink.getPdfjs();
      pdfjsDoc = await pdfjs.getDocument({ data: bytes.slice(), isEvalSupported: false }).promise;
      const sel = $('#sig-page'); sel.innerHTML = '';
      for (let n = 1; n <= pdfjsDoc.numPages; n++) sel.add(new Option('Page ' + n, n));
      sel.value = String(pdfjsDoc.numPages);
      $('#place-step').hidden = false; $('#go-row').hidden = false;
      await showPage();
    });
    $('#sig-page').addEventListener('change', showPage);
    async function showPage() {
      const n = +$('#sig-page').value, page = await pdfjsDoc.getPage(n);
      const vp1 = page.getViewport({ scale: 1 }), vp = page.getViewport({ scale: Math.min(2, 900 / vp1.width) });
      prev.width = Math.ceil(vp.width); prev.height = Math.ceil(vp.height);
      const g = prev.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, prev.width, prev.height);
      await page.render({ canvasContext: g, viewport: vp }).promise;
      drawPlacements();
    }
    function drawPlacements() {
      overlay.innerHTML = '';
      const n = +$('#sig-page').value;
      placements.filter((p) => p.page === n).forEach((p) => {
        const im = document.createElement('img'); im.src = p.sig.toDataURL(); im.alt = 'Placed signature';
        im.style.cssText = 'left:' + p.fx * 100 + '%;top:' + p.fy * 100 + '%;width:' + p.fw * 100 + '%';
        overlay.appendChild(im);
      });
      $('#placed').textContent = placements.length ? placements.length + ' signature(s) placed' : 'Click on the page where the signature should go.';
      $('#go').disabled = !placements.length;
    }
    function place(fx, fy) {
      try { sig = makeSignature(); } catch (e) { return toast(e.message); }
      const fw = +$('#sig-width').value / 100;
      const fh = (fw * prev.width * (sig.height / sig.width)) / prev.height;
      placements.push({ page: +$('#sig-page').value, fx: Math.max(0, Math.min(1 - fw, fx - fw / 2)), fy: Math.max(0, Math.min(1 - fh, fy - fh / 2)), fw, fh, sig });
      drawPlacements();
    }
    $('#prevwrap').addEventListener('click', (e) => {
      const r = prev.getBoundingClientRect();
      place((e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height);
    });
    $('#prevwrap').addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); place(0.75, 0.88); } });
    $('#sig-undo').addEventListener('click', () => { placements.pop(); drawPlacements(); });
    $('#go').addEventListener('click', async () => {
      const btn = $('#go'); setBusy(btn, true, 'Signing…');
      try {
        const work = await PDFLib.PDFDocument.load(await doc.save());
        const pagesArr = work.getPages();
        for (const p of placements) {
          const png = await work.embedPng(new Uint8Array(await (await toBlob(p.sig, 'image/png')).arrayBuffer()));
          const page = pagesArr[p.page - 1], v = visual(page);
          const w = p.fw * v.vw, h = p.fh * v.vh;
          const pt0 = v.map(p.fx * v.vw, v.vh - (p.fy * v.vh + h)); // bottom-left of the box, in visual coords
          page.drawImage(png, { x: pt0.x, y: pt0.y, width: w, height: h, rotate: PDFLib.degrees(v.r) });
        }
        await deliverPdf(work, baseName(file.name) + '-signed.pdf', 'Signed (' + placements.length + ' signature' + (placements.length > 1 ? 's' : '') + ')', 'signed', { count: placements.length, mode: modeSel.value });
      } catch (e) { console.error(e); showResult('<p class="error">' + esc(e.message) + '</p>'); }
      setBusy(btn, false);
    });
  }

  // ------------------------------------------------------------------ unlock PDF
  function initUnlock() {
    let file = null;
    onFiles = async (fs) => {
      const f = fs.find(isPdf);
      if (!f) return toast('Please choose a PDF file.');
      file = f; $('#doc-info').textContent = f.name + ' · ' + fmt(f.size); $('#go-row').hidden = false; $('#go').disabled = false;
      $('#result').hidden = true;
    };
    $('#go').addEventListener('click', async () => {
      if (!file) return;
      const btn = $('#go'); setBusy(btn, true, 'Unlocking…');
      try {
        await PdfShrink.ready();
        const bytes = new Uint8Array(await file.arrayBuffer());
        const probe = await PDFLib.PDFDocument.load(bytes, { ignoreEncryption: true });
        if (!probe.isEncrypted) { showResult('<p>This PDF isn’t protected — there’s nothing to unlock.</p>'); setBusy(btn, false); return; }
        let out;
        try { out = await decryptBytes(bytes, $('#pw').value); }
        catch (e) {
          if (/password/i.test(e.message)) throw new Error($('#pw').value ? 'That password is incorrect.' : 'This PDF needs its open password. Type it above and try again.');
          throw e;
        }
        const blob = new Blob([out], { type: 'application/pdf' }), url = URL.createObjectURL(blob);
        showResult('<p>✓ Unlocked — no password or restrictions · ' + fmt(blob.size) + '</p><a class="btn" download="' + esc(baseName(file.name)) + '-unlocked.pdf" href="' + url + '">Download unlocked PDF</a>');
        track('unlocked', { hit: true });
      } catch (e) { console.error(e); showResult('<p class="error">' + esc(e.message || 'Could not unlock this PDF.') + '</p>'); track('unlocked', { hit: false }); }
      setBusy(btn, false);
    });
  }

  // ------------------------------------------------------------------ PDF / image → text (OCR)
  let ocrWorkerP;
  function getOcr(progress) {
    if (!ocrWorkerP) {
      ocrWorkerP = (async () => {
        await loadScript('/vendor/tesseract/tesseract.min.js');
        // Pick the core build ourselves (SIMD where supported) so only two variants need hosting.
        const simd = WebAssembly.validate(new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 123, 3, 2, 1, 0, 10, 10, 1, 8, 0, 65, 0, 253, 15, 253, 98, 11]));
        return Tesseract.createWorker('eng', 1, {
          workerPath: '/vendor/tesseract/worker.min.js', langPath: '/vendor/tesseract',
          corePath: '/vendor/tesseract/tesseract-core-' + (simd ? 'simd-' : '') + 'lstm.wasm.js',
          workerBlobURL: false, logger: (m) => progress.fn && progress.fn(m),
        });
      })();
      ocrWorkerP.catch(() => { ocrWorkerP = null; });
    }
    return ocrWorkerP;
  }
  function initOcr() {
    let files = [];
    const out = $('#ocr-out'), prog = $('#ocr-prog'), progress = { fn: null };
    onFiles = (fs) => {
      files = fs.filter((f) => isPdf(f) || isImg(f));
      if (!files.length) return toast('Please choose a PDF or image files.');
      $('#doc-info').textContent = files.map((f) => f.name).join(', ');
      $('#go-row').hidden = false; $('#go').disabled = false;
    };
    async function ocrCanvas(c, label) {
      progress.fn = (m) => { if (m.status === 'recognizing text') prog.textContent = label + ' — recognising ' + Math.round(m.progress * 100) + '%'; else if (m.status) prog.textContent = label + ' — ' + m.status + '…'; };
      const w = await getOcr(progress);
      const r = await w.recognize(c);
      return r.data.text.trim();
    }
    $('#go').addEventListener('click', async () => {
      const btn = $('#go'); setBusy(btn, true, 'Extracting…');
      out.value = ''; $('#ocr-result').hidden = false;
      const force = $('#ocr-force').checked, parts = [];
      let ocrPages = 0, textPages = 0;
      try {
        for (const f of files) {
          if (isPdf(f)) {
            const { bytes } = await openPdf(f);
            const pdfjs = await PdfShrink.getPdfjs();
            const pd = await pdfjs.getDocument({ data: bytes.slice(), isEvalSupported: false }).promise;
            for (let n = 1; n <= pd.numPages; n++) {
              const page = await pd.getPage(n);
              let text = '';
              if (!force) {
                const tc = await page.getTextContent();
                text = tc.items.map((it) => it.str + (it.hasEOL ? '\n' : '')).join('').replace(/[ \t]+\n/g, '\n').trim();
              }
              if (text.length < 20) {
                const vp = page.getViewport({ scale: 2.2 });
                const c = document.createElement('canvas'); c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
                const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
                await page.render({ canvasContext: g, viewport: vp }).promise;
                text = await ocrCanvas(c, f.name + ' · page ' + n + '/' + pd.numPages); ocrPages++;
                c.width = c.height = 0;
              } else { textPages++; prog.textContent = f.name + ' · page ' + n + '/' + pd.numPages + ' — text layer found'; }
              parts.push((files.length > 1 || pd.numPages > 1 ? '--- ' + f.name + ' · page ' + n + ' ---\n' : '') + text);
              out.value = parts.join('\n\n');
              page.cleanup(); await tick();
            }
            await pd.destroy();
          } else {
            const src = await decodeImage(f), d = dimsOf(src);
            const s = Math.min(1, 4000 / Math.max(d.w, d.h));
            const text = await ocrCanvas(drawTo(src, Math.round(d.w * s), Math.round(d.h * s), 'contain'), f.name); ocrPages++;
            parts.push((files.length > 1 ? '--- ' + f.name + ' ---\n' : '') + text);
            out.value = parts.join('\n\n');
          }
        }
        prog.textContent = '✓ Done · ' + (textPages ? textPages + ' page(s) read from the text layer' : '') + (textPages && ocrPages ? ', ' : '') + (ocrPages ? ocrPages + ' page(s)/image(s) recognised with OCR' : '');
        track('ocr', { pages: textPages + ocrPages, count: ocrPages });
      } catch (e) { console.error(e); prog.textContent = e.message || 'Could not extract text.'; }
      setBusy(btn, false);
    });
    $('#ocr-copy').addEventListener('click', async () => { try { await navigator.clipboard.writeText(out.value); toast('Copied to clipboard'); } catch (e) { out.select(); } });
    $('#ocr-dl').addEventListener('click', () => saveBlob(new Blob([out.value], { type: 'text/plain;charset=utf-8' }), (files[0] ? baseName(files[0].name) : 'text') + '.txt'));
  }

  ({
    image: initImage, merge: initMerge, split: initSplit, img2pdf: initImagesToPdf, pdf2img: initPdfToImages, dpi: initDpi,
    organize: initOrganize, pagenum: initPageNumbers, watermark: initWatermark, sign: initSign, unlock: initUnlock, ocr: initOcr,
  }[kind] || (() => {}))();
  if (kind !== 'image' && kind !== 'dpi') { const w = () => PdfShrink.ready().catch(() => {}); ('requestIdleCallback' in window) ? requestIdleCallback(w, { timeout: 4000 }) : setTimeout(w, 2500); }
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
  }
})();

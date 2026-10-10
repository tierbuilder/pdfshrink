/* UI for the compressor. All processing is delegated to engine.js (in-browser). */
(function () {
  'use strict';
  const tool = document.getElementById('tool');
  if (!tool) return;
  const $ = (s, r) => (r || tool).querySelector(s);
  const $$ = (s, r) => Array.from((r || tool).querySelectorAll(s));
  const input = $('#file'), drop = $('#drop'), list = $('#files'), bulk = $('#bulk');
  const tsize = $('#tsize'), tunit = $('#tunit'), targetRow = $('#target-row'), rerun = $('#rerun');
  const items = [];
  let mode = tool.dataset.mode || 'recommended';
  let busy = false;

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
    try {
      if (window.plausible) window.plausible(name, { props });
      if (window.gtag) window.gtag('event', name, props);
    } catch (e) { /* analytics is optional */ }
  };
  const fmt = (n) => (n >= 1048576 ? (n / 1048576).toFixed(2) + ' MB' : n >= 1024 ? Math.round(n / 1024) + ' KB' : n + ' B');
  const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // Preset target from the landing page (e.g. /compress-pdf-to-100kb/).
  if (tool.dataset.targetKb) {
    const kb = +tool.dataset.targetKb;
    if (kb >= 1024 && kb % 1024 === 0) { tsize.value = kb / 1024; tunit.value = 'MB'; } else { tsize.value = kb; tunit.value = 'KB'; }
    mode = 'target';
  }
  function setMode(m) {
    mode = m;
    $$('.seg button').forEach((b) => b.setAttribute('aria-checked', String(b.dataset.mode === m)));
    targetRow.hidden = m !== 'target';
    markStale();
  }
  setMode(mode);
  $$('.seg button').forEach((b) => b.addEventListener('click', () => setMode(b.dataset.mode)));
  $$('.chip[data-kb]').forEach((c) => c.addEventListener('click', () => {
    const kb = +c.dataset.kb;
    if (kb >= 1024) { tsize.value = kb / 1024; tunit.value = 'MB'; } else { tsize.value = kb; tunit.value = 'KB'; }
    setMode('target');
  }));
  [tsize, tunit, $('#opt-gray'), $('#opt-meta'), $('#opt-flatten'), $('#opt-lossless')].forEach((el) => el && el.addEventListener('change', markStale));

  function options() {
    const o = { preset: mode, gray: $('#opt-gray').checked, stripMeta: $('#opt-meta').checked, allowFlatten: $('#opt-flatten').checked };
    if ($('#opt-lossless').checked && mode !== 'target') o.preset = 'lossless';
    if (mode === 'target') {
      const v = parseFloat(tsize.value);
      if (v > 0) o.targetBytes = Math.floor(v * (tunit.value === 'MB' ? 1e6 : 1000)); // 1000-byte KB passes both conventions
      else o.preset = 'recommended';
    }
    return o;
  }
  function markStale() {
    if (items.some((it) => it.result)) rerun.hidden = false;
  }

  // Warm up the libraries once the page is idle so the first file starts instantly.
  const warm = () => window.PdfShrink && window.PdfShrink.ready().catch(() => {});
  if ('requestIdleCallback' in window) requestIdleCallback(warm, { timeout: 4000 }); else setTimeout(warm, 2500);

  drop.addEventListener('click', () => input.click());
  drop.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
  input.addEventListener('change', () => { addFiles(input.files); input.value = ''; });
  ['dragenter', 'dragover'].forEach((t) => document.addEventListener(t, (e) => { e.preventDefault(); drop.classList.add('over'); }));
  ['dragleave', 'drop'].forEach((t) => document.addEventListener(t, (e) => { e.preventDefault(); if (t === 'drop' || e.target === document.documentElement) drop.classList.remove('over'); }));
  document.addEventListener('drop', (e) => { if (e.dataTransfer && e.dataTransfer.files.length) addFiles(e.dataTransfer.files); });
  document.addEventListener('paste', (e) => { if (e.clipboardData && e.clipboardData.files.length) addFiles(e.clipboardData.files); });

  function addFiles(fileList) {
    const files = Array.from(fileList).filter((f) => f.type === 'application/pdf' || /\.pdf$/i.test(f.name));
    if (!files.length) { flash('Please choose PDF files.'); return; }
    for (const f of files) {
      const li = document.createElement('li');
      li.className = 'item';
      li.innerHTML =
        '<div class="item-top"><span class="name">' + esc(f.name) + '</span><span class="sizes">' + fmt(f.size) + '</span></div>' +
        '<div class="bar"><span></span></div><div class="item-bottom"><span class="status">Waiting…</span><span class="actions"></span></div>';
      list.appendChild(li);
      items.push({ file: f, li, result: null });
    }
    track('files_added', { count: files.length });
    run();
  }

  async function run(force) {
    if (busy) return;
    busy = true;
    rerun.hidden = true;
    for (const it of items) {
      if (it.result && !force) continue;
      await processItem(it);
    }
    busy = false;
    const ok = items.filter((i) => i.result && i.result.url);
    bulk.hidden = ok.length < 2;
    if (ok.length) $('#share').hidden = false;
  }
  rerun.addEventListener('click', () => run(true));

  async function processItem(it) {
    const { li, file } = it;
    const bar = $('.bar span', li), st = $('.status', li), sizes = $('.sizes', li), actions = $('.actions', li);
    li.classList.remove('done', 'err', 'miss');
    actions.innerHTML = '';
    if (it.result && it.result.url) URL.revokeObjectURL(it.result.url);
    it.result = null;
    const opts = options();
    const t0 = performance.now();
    try {
      const buf = it.buf || (it.buf = new Uint8Array(await file.arrayBuffer()));
      const r = await window.PdfShrink.compress(buf, opts, (msg, f) => {
        st.textContent = msg;
        if (f != null) bar.style.width = Math.max(4, Math.min(100, f * 100)) + '%';
      });
      bar.style.width = '100%';
      const blob = new Blob([r.bytes], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      const outName = file.name.replace(/\.pdf$/i, '') + '-compressed.pdf';
      it.result = { url, name: outName, blob, size: r.bytes.length };
      const saved = Math.max(0, Math.round((1 - r.bytes.length / file.size) * 100));
      sizes.innerHTML = fmt(file.size) + ' → <b>' + fmt(r.bytes.length) + '</b>' + (saved ? ' <em class="save">−' + saved + '%</em>' : '');
      let msg = r.locked ? '🔒 Password-protected' : r.method === 'original' ? 'Kept original' : r.method === 'flatten' ? 'Done (pages flattened)' : 'Done — text & links kept';
      if (opts.targetBytes) msg = (r.hit ? '✓ Under ' : '✗ Above ') + tsize.value + ' ' + tunit.value + ' · ' + msg;
      st.textContent = msg + ' · ' + ((performance.now() - t0) / 1000).toFixed(1) + 's';
      if (r.note) st.title = r.note;
      li.classList.add(r.locked || (opts.targetBytes && !r.hit) ? 'miss' : 'done');
      actions.innerHTML = '<a class="btn btn-sm" download="' + esc(outName) + '" href="' + url + '">Download</a>';
      if (r.note) {
        const n = document.createElement('p'); n.className = 'note'; n.textContent = r.note; li.appendChild(n);
        if (r.locked) { const l = document.createElement('a'); l.href = '/unlock-pdf/'; l.textContent = ' Open Unlock PDF →'; n.appendChild(l); }
      }
      track('compressed', { mode: opts.targetBytes ? 'target' : opts.preset, method: r.method, saved, hit: r.hit !== false });
    } catch (e) {
      console.error(e);
      li.classList.add('err');
      st.textContent = 'Could not read this PDF. It may be damaged or password-protected (open password).';
      track('error', { msg: String(e && e.message).slice(0, 80) });
    }
  }

  $('#zip').addEventListener('click', async () => {
    const btn = $('#zip'); btn.disabled = true; btn.textContent = 'Zipping…';
    try {
      if (!window.JSZip) await new Promise((res, rej) => { const s = document.createElement('script'); s.src = '/vendor/jszip.min.js'; s.onload = res; s.onerror = rej; document.head.appendChild(s); });
      const zip = new JSZip(), used = new Set();
      for (const it of items) {
        if (!it.result) continue;
        let n = it.result.name, k = 1;
        while (used.has(n)) n = it.result.name.replace(/\.pdf$/, '') + '-' + k++ + '.pdf';
        used.add(n); zip.file(n, it.result.blob);
      }
      const blob = await zip.generateAsync({ type: 'blob', compression: 'STORE' });
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'compressed-pdfs.zip'; a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 60000);
      track('zip_download', { count: used.size });
    } finally { btn.disabled = false; btn.textContent = 'Download all (ZIP)'; }
  });
  $('#clear').addEventListener('click', () => {
    items.forEach((it) => it.result && it.result.url && URL.revokeObjectURL(it.result.url));
    items.length = 0; list.innerHTML = ''; bulk.hidden = true; rerun.hidden = true;
  });
  $('#share').addEventListener('click', async () => {
    const data = { title: document.title, text: 'Free PDF compressor that never uploads your files', url: location.origin + location.pathname };
    try {
      if (navigator.share) await navigator.share(data);
      else { await navigator.clipboard.writeText(data.url); flash('Link copied — thanks for sharing!'); }
      track('share');
    } catch (e) { /* user cancelled */ }
  });
  function flash(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.hidden = false;
    clearTimeout(flash.t); flash.t = setTimeout(() => (t.hidden = true), 3000);
  }

  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
  }
})();

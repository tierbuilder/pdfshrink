/* PDF compression engine — runs 100% in the browser. Nothing is uploaded.
 *
 * Two strategies:
 *  1. smart   — keeps text, links, forms and vectors. Strips junk (metadata,
 *               thumbnails, orphaned objects), deflates uncompressed streams and
 *               re-encodes embedded images as downscaled JPEG.
 *  2. flatten — renders every page to a JPEG (pdf.js) and rebuilds the PDF.
 *               Text stops being selectable, but it can hit any size target.
 *
 * compressToTarget() walks a quality ladder (binary search) using smart first
 * and flatten only if smart can't reach the target.
 */
(function () {
  'use strict';
  const VENDOR = '/vendor/';
  const loaded = {};
  function loadScript(src) {
    if (!loaded[src]) {
      loaded[src] = new Promise((res, rej) => {
        const s = document.createElement('script');
        s.src = src; s.async = true; s.onload = res;
        s.onerror = () => rej(new Error('Failed to load ' + src));
        document.head.appendChild(s);
      });
    }
    return loaded[src];
  }
  let pdfjsP;
  function getPdfjs() {
    if (!pdfjsP) {
      pdfjsP = import(VENDOR + 'pdf.min.js').then((m) => {
        m.GlobalWorkerOptions.workerSrc = VENDOR + 'pdf.worker.min.js';
        return m;
      });
    }
    return pdfjsP;
  }
  const ready = () => Promise.all([loadScript(VENDOR + 'pdf-lib.min.js'), loadScript(VENDOR + 'pako.min.js')]);
  const tick = () => new Promise((r) => setTimeout(r, 0));

  // Smart-mode quality ladder: best quality first.
  const SMART_LADDER = [
    { quality: 0.82, maxDim: 2600 },
    { quality: 0.72, maxDim: 2000 },
    { quality: 0.62, maxDim: 1700 },
    { quality: 0.52, maxDim: 1400 },
    { quality: 0.42, maxDim: 1150 },
    { quality: 0.34, maxDim: 950 },
    { quality: 0.26, maxDim: 780 },
    { quality: 0.2, maxDim: 620 },
  ];
  const FLATTEN_LADDER = [
    { dpi: 150, quality: 0.72 },
    { dpi: 130, quality: 0.62 },
    { dpi: 110, quality: 0.55 },
    { dpi: 96, quality: 0.48 },
    { dpi: 84, quality: 0.42 },
    { dpi: 72, quality: 0.36 },
    { dpi: 62, quality: 0.3 },
    { dpi: 52, quality: 0.25 },
    { dpi: 44, quality: 0.2, gray: true },
  ];
  const PRESETS = {
    light: { quality: 0.82, maxDim: 2600 },
    recommended: { quality: 0.62, maxDim: 1700 },
    strong: { quality: 0.4, maxDim: 1100 },
  };

  function makeCanvas(w, h) {
    if (typeof OffscreenCanvas !== 'undefined') return new OffscreenCanvas(w, h);
    const c = document.createElement('canvas'); c.width = w; c.height = h; return c;
  }
  async function canvasToJpeg(c, quality) {
    const blob = c.convertToBlob
      ? await c.convertToBlob({ type: 'image/jpeg', quality })
      : await new Promise((r) => c.toBlob(r, 'image/jpeg', quality));
    return new Uint8Array(await blob.arrayBuffer());
  }
  function toGray(ctx2d, w, h) {
    const id = ctx2d.getImageData(0, 0, w, h), p = id.data;
    for (let i = 0; i < p.length; i += 4) {
      const y = (p[i] * 299 + p[i + 1] * 587 + p[i + 2] * 114) / 1000;
      p[i] = p[i + 1] = p[i + 2] = y;
    }
    ctx2d.putImageData(id, 0, 0);
  }

  // PNG predictor (Predictor >= 10) un-filtering for Flate image streams.
  function unPredict(data, colors, columns) {
    const bpp = colors, row = colors * columns, out = new Uint8Array(row * Math.floor(data.length / (row + 1)));
    let prev = new Uint8Array(row);
    for (let r = 0, src = 0, dst = 0; dst < out.length; r++) {
      const type = data[src++];
      for (let i = 0; i < row; i++) {
        const raw = data[src++], left = i >= bpp ? out[dst + i - bpp] : 0, up = prev[i], ul = i >= bpp ? prev[i - bpp] : 0;
        let v;
        switch (type) {
          case 1: v = raw + left; break;
          case 2: v = raw + up; break;
          case 3: v = raw + ((left + up) >> 1); break;
          case 4: {
            const pa = Math.abs(up - ul), pb = Math.abs(left - ul), pc = Math.abs(left + up - 2 * ul);
            v = raw + (pa <= pb && pa <= pc ? left : pb <= pc ? up : ul); break;
          }
          default: v = raw;
        }
        out[dst + i] = v & 255;
      }
      prev = out.subarray(dst, dst + row);
      dst += row;
    }
    return out;
  }

  // Decode one image XObject to something drawable, or null if unsupported.
  async function decodeImage(ctx, stream) {
    const { PDFName, PDFArray, PDFBool } = PDFLib;
    const d = stream.dict;
    const get = (k) => ctx.lookup(d.get(PDFName.of(k)));
    const nm = (x) => (x instanceof PDFName ? x.decodeText() : null);
    const im = get('ImageMask');
    if (im instanceof PDFBool && im.asBoolean()) return null;
    if (d.get(PDFName.of('Decode'))) return null;
    const w = get('Width') && get('Width').asNumber(), h = get('Height') && get('Height').asNumber();
    if (!w || !h || w * h < 10000) return null;

    let f = get('Filter');
    const filters = f instanceof PDFArray ? f.asArray().map((x) => nm(ctx.lookup(x))) : f ? [nm(f)] : [];
    const cs = get('ColorSpace');
    let ncomp = 0;
    if (cs instanceof PDFName) ncomp = { DeviceRGB: 3, DeviceGray: 1, CalRGB: 3, CalGray: 1 }[nm(cs)] || 0;
    else if (cs instanceof PDFArray) {
      const kind = nm(ctx.lookup(cs.get(0)));
      if (kind === 'ICCBased') {
        const icc = ctx.lookup(cs.get(1));
        const n = icc && icc.dict && ctx.lookup(icc.dict.get(PDFName.of('N')));
        ncomp = n ? n.asNumber() : 0;
      } else if (kind === 'CalRGB') ncomp = 3;
      else if (kind === 'CalGray') ncomp = 1;
    }
    if (ncomp !== 1 && ncomp !== 3) return null; // CMYK, Indexed, Lab, Separation… left alone

    // Undo generic encoding filters (ASCII85, ASCIIHex, Flate) so we reach either JPEG data or raw pixels.
    const parmsObj = get('DecodeParms');
    const parmsList = parmsObj instanceof PDFArray ? parmsObj.asArray().map((x) => ctx.lookup(x)) : filters.map(() => parmsObj);
    let data = stream.contents, predictor = 1;
    for (let i = 0; i < filters.length; i++) {
      const fl = filters[i], last = i === filters.length - 1;
      if (fl === 'DCTDecode' && last) break;
      try {
        if (fl === 'ASCII85Decode' || fl === 'A85') data = a85(data);
        else if (fl === 'ASCIIHexDecode' || fl === 'AHx') data = ahx(data);
        else if (fl === 'FlateDecode' || fl === 'Fl') {
          data = pako.inflate(data);
          const pr = parmsList[i] && parmsList[i].get && ctx.lookup(parmsList[i].get(PDFName.of('Predictor')));
          predictor = pr ? pr.asNumber() : 1;
        } else return null; // LZW, CCITT, JBIG2, JPX, RunLength… left alone
      } catch (e) { return null; }
    }

    if (filters[filters.length - 1] === 'DCTDecode') {
      const blob = new Blob([data], { type: 'image/jpeg' });
      let bmp;
      try { bmp = await createImageBitmap(blob, { imageOrientation: 'none' }); }
      catch (e) { try { bmp = await createImageBitmap(blob); } catch (e2) { return null; } }
      if (bmp.width !== w || bmp.height !== h) { bmp.close && bmp.close(); return null; }
      return { source: bmp, w, h, ncomp };
    }
    const bpc = get('BitsPerComponent');
    if (!bpc || bpc.asNumber() !== 8) return null;
    let raw = data;
    if (predictor >= 10) raw = unPredict(raw, ncomp, w);
    else if (predictor !== 1) return null;
    if (raw.length < w * h * ncomp) return null;
    const rgba = new Uint8ClampedArray(w * h * 4);
    for (let i = 0, j = 0; i < w * h; i++, j += ncomp) {
      const o = i * 4;
      if (ncomp === 3) { rgba[o] = raw[j]; rgba[o + 1] = raw[j + 1]; rgba[o + 2] = raw[j + 2]; }
      else rgba[o] = rgba[o + 1] = rgba[o + 2] = raw[j];
      rgba[o + 3] = 255;
    }
    const c = makeCanvas(w, h);
    c.getContext('2d').putImageData(new ImageData(rgba, w, h), 0, 0);
    return { source: c, w, h, ncomp };
  }

  function a85(src) {
    const out = [];
    let tuple = 0, n = 0;
    for (let i = 0; i < src.length; i++) {
      const ch = src[i];
      if (ch === 0x7e) break; // '~>' end marker
      if (ch <= 0x20) continue;
      if (ch === 0x7a && n === 0) { out.push(0, 0, 0, 0); continue; } // 'z'
      tuple = tuple * 85 + (ch - 33); n++;
      if (n === 5) { out.push((tuple >>> 24) & 255, (tuple >>> 16) & 255, (tuple >>> 8) & 255, tuple & 255); tuple = 0; n = 0; }
    }
    if (n > 1) {
      for (let k = n; k < 5; k++) tuple = tuple * 85 + 84;
      const b = [(tuple >>> 24) & 255, (tuple >>> 16) & 255, (tuple >>> 8) & 255, tuple & 255];
      for (let k = 0; k < n - 1; k++) out.push(b[k]);
    }
    return new Uint8Array(out);
  }
  function ahx(src) {
    const hex = new TextDecoder('latin1').decode(src).replace(/>.*$/s, '').replace(/[^0-9a-fA-F]/g, '');
    const out = new Uint8Array(Math.ceil(hex.length / 2));
    for (let i = 0; i < out.length; i++) out[i] = parseInt((hex.substr(i * 2, 2) + '0').slice(0, 2), 16);
    return out;
  }

  async function recompressImage(ctx, stream, opt) {
    const { PDFName, PDFRawStream } = PDFLib;
    const img = await decodeImage(ctx, stream);
    if (!img) return null;
    const scale = Math.min(1, opt.maxDim / Math.max(img.w, img.h));
    const nw = Math.max(1, Math.round(img.w * scale)), nh = Math.max(1, Math.round(img.h * scale));
    const c = makeCanvas(nw, nh), g = c.getContext('2d');
    g.fillStyle = '#fff'; g.fillRect(0, 0, nw, nh);
    g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
    g.drawImage(img.source, 0, 0, nw, nh);
    if (img.source.close) img.source.close();
    if (opt.gray && img.ncomp === 3) toGray(g, nw, nh);
    const jpg = await canvasToJpeg(c, opt.quality);
    if (jpg.length >= stream.contents.length * 0.97) return null;
    const nd = ctx.obj({
      Type: 'XObject', Subtype: 'Image', Width: nw, Height: nh,
      ColorSpace: 'DeviceRGB', BitsPerComponent: 8, Filter: 'DCTDecode', Length: jpg.length,
    });
    for (const k of ['SMask', 'Interpolate', 'Intent']) {
      const v = stream.dict.get(PDFName.of(k));
      if (v) nd.set(PDFName.of(k), v);
    }
    return PDFRawStream.of(nd, jpg);
  }

  // Drop every object not reachable from the trailer (old revisions, orphans).
  function garbageCollect(ctx) {
    const { PDFRef, PDFDict, PDFArray, PDFStream } = PDFLib;
    const seen = new Set();
    const stack = [ctx.trailerInfo.Root, ctx.trailerInfo.Info].filter(Boolean);
    while (stack.length) {
      const o = stack.pop();
      if (o instanceof PDFRef) {
        if (seen.has(o.tag)) continue;
        seen.add(o.tag);
        const t = ctx.lookup(o);
        if (t) stack.push(t);
      } else if (o instanceof PDFDict) { for (const [, v] of o.entries()) stack.push(v); }
      else if (o instanceof PDFArray) { for (const v of o.asArray()) stack.push(v); }
      else if (o instanceof PDFStream) stack.push(o.dict);
    }
    let removed = 0;
    for (const [ref] of ctx.enumerateIndirectObjects()) if (!seen.has(ref.tag)) { ctx.delete(ref); removed++; }
    return removed;
  }

  function isEncrypted(bytes) {
    // Cheap check on the trailer region; pdf-lib drops /Encrypt on save, so we must never smart-save these.
    const tail = new TextDecoder('latin1').decode(bytes.subarray(Math.max(0, bytes.length - 4096)));
    const head = new TextDecoder('latin1').decode(bytes.subarray(0, Math.min(bytes.length, 4096)));
    return /\/Encrypt\s/.test(tail) || /\/Encrypt\s/.test(head);
  }

  async function smartCompress(bytes, opt, onProgress) {
    await ready();
    const { PDFDocument, PDFName, PDFNumber, PDFRawStream } = PDFLib;
    const doc = await PDFDocument.load(bytes, { updateMetadata: false, ignoreEncryption: true });
    if (doc.isEncrypted || isEncrypted(bytes)) throw new Error('ENCRYPTED');
    const ctx = doc.context;
    if (opt.stripMeta !== false) {
      doc.catalog.delete(PDFName.of('Metadata'));
      doc.catalog.delete(PDFName.of('PieceInfo'));
      for (const p of doc.getPages()) { p.node.delete(PDFName.of('Thumb')); p.node.delete(PDFName.of('PieceInfo')); }
      ctx.trailerInfo.Info = ctx.obj({ Producer: 'PDF compressed in-browser' });
    }
    garbageCollect(ctx);
    const objs = ctx.enumerateIndirectObjects();
    const IMAGE = PDFName.of('Image'), SUBTYPE = PDFName.of('Subtype'), FILTER = PDFName.of('Filter'), TYPE = PDFName.of('Type');
    const SKIP_TYPES = new Set(['XRef', 'ObjStm', 'Metadata']);
    let images = 0, done = 0;
    for (let i = 0; i < objs.length; i++) {
      const [ref, obj] = objs[i];
      if (!(obj instanceof PDFRawStream)) continue;
      const d = obj.dict;
      if (d.get(SUBTYPE) === IMAGE) {
        if (opt.images === false) continue;
        images++;
        try {
          const ns = await recompressImage(ctx, obj, opt);
          if (ns) { ctx.assign(ref, ns); done++; }
        } catch (e) { /* leave this image as-is */ }
        onProgress && onProgress(i / objs.length);
        await tick();
      } else if (!d.get(FILTER) && obj.contents.length > 128) {
        const t = d.get(TYPE);
        if (t && SKIP_TYPES.has(t.decodeText ? t.decodeText() : '')) continue;
        const z = pako.deflate(obj.contents, { level: 9 });
        if (z.length < obj.contents.length) {
          const nd = d.clone(ctx);
          nd.set(FILTER, PDFName.of('FlateDecode'));
          nd.set(PDFName.of('Length'), PDFNumber.of(z.length));
          ctx.assign(ref, PDFRawStream.of(nd, z));
        }
      }
      if (i % 50 === 0) { onProgress && onProgress(i / objs.length); await tick(); }
    }
    const out = await doc.save({ useObjectStreams: true, addDefaultPage: false, objectsPerTick: 200 });
    return { bytes: out, method: 'smart', images, recompressed: done };
  }

  async function flattenCompress(bytes, opt, onProgress) {
    await ready();
    const pdfjs = await getPdfjs();
    const src = await pdfjs.getDocument({ data: bytes.slice(), isEvalSupported: false }).promise;
    const out = await PDFLib.PDFDocument.create();
    for (let n = 1; n <= src.numPages; n++) {
      const page = await src.getPage(n);
      const vp1 = page.getViewport({ scale: 1 });
      let scale = opt.dpi / 72;
      // Keep canvases sane on huge pages (browser canvas limits ~16k px / 268M px²).
      const maxSide = 6000;
      scale = Math.min(scale, maxSide / Math.max(vp1.width, vp1.height));
      const vp = page.getViewport({ scale });
      const c = document.createElement('canvas');
      c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
      const g = c.getContext('2d');
      g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
      await page.render({ canvasContext: g, viewport: vp }).promise;
      if (opt.gray) toGray(g, c.width, c.height);
      const jpg = await canvasToJpeg(c, opt.quality);
      const img = await out.embedJpg(jpg);
      const p = out.addPage([vp1.width, vp1.height]);
      p.drawImage(img, { x: 0, y: 0, width: vp1.width, height: vp1.height });
      page.cleanup();
      c.width = c.height = 0;
      onProgress && onProgress(n / src.numPages);
      await tick();
    }
    await src.destroy();
    const outBytes = await out.save({ useObjectStreams: true });
    return { bytes: outBytes, method: 'flatten', pages: src.numPages };
  }

  // Binary-search the smallest ladder index whose result fits.
  async function searchLadder(ladder, run, target, onStep) {
    let lo = 0, hi = ladder.length - 1, best = null, smallest = null;
    while (lo <= hi) {
      const mid = (lo + hi) >> 1;
      onStep && onStep(mid);
      let r;
      try { r = await run(ladder[mid]); } catch (e) { break; } // unparseable for this strategy

      if (!smallest || r.bytes.length < smallest.bytes.length) smallest = r;
      if (r.bytes.length <= target) { best = r; hi = mid - 1; } else lo = mid + 1;
    }
    return { best, smallest };
  }

  /**
   * compress(bytes, options, onStatus) → { bytes, method, hit, note }
   * options: { preset: 'light'|'recommended'|'strong'|'lossless', targetBytes?, gray, stripMeta, allowFlatten }
   */
  // Remove encryption from PDFs that open without a password (permission-restricted files),
  // using the @cantoo pdf-lib fork, so they can be optimised without flattening.
  async function decryptIfRestricted(bytes) {
    if (!isEncrypted(bytes)) return bytes;
    try {
      await ready();
      const orig = window.PDFLib;
      await loadScript(VENDOR + 'pdf-lib-cantoo.min.js');
      const C = window.PDFLib; window.PDFLib = orig;
      const d = await C.PDFDocument.load(bytes, { password: '', ignoreEncryption: false });
      return new Uint8Array(await d.save({ useObjectStreams: false }));
    } catch (e) { return bytes; } // needs a real password: fall back to flattening
  }

  async function compress(input, options, onStatus) {
    const original = input instanceof Uint8Array ? input : new Uint8Array(input);
    const bytes = await decryptIfRestricted(original);
    const status = (msg, frac) => onStatus && onStatus(msg, frac);
    if (isEncrypted(bytes)) {
      return { bytes: original, method: 'original', hit: false, locked: true,
        note: 'This PDF needs a password to open. Unlock it first (Unlock PDF tool), then compress the unlocked copy.' };
    }
    const base = { gray: !!options.gray, stripMeta: options.stripMeta !== false };
    let encrypted = false;
    const tryRun = async (fn) => {
      try { return await fn(); }
      catch (e) { if (e.message === 'ENCRYPTED') encrypted = true; return { error: e }; }
    };
    const pick = (r, extra) => {
      if (!r || r.error || r.bytes.length >= original.length) {
        return Object.assign({ bytes: original, method: 'original', note: 'This PDF is already well optimized — we kept the original.' }, extra);
      }
      return Object.assign(r, extra);
    };

    if (!options.targetBytes) {
      if (options.preset === 'flatten') {
        status('Flattening pages…', 0);
        const r = await tryRun(() => flattenCompress(bytes, Object.assign({ dpi: 110, quality: 0.55 }, base), (f) => status('Flattening pages…', f)));
        return pick(r);
      }
      const p = options.preset === 'lossless' ? { images: false } : PRESETS[options.preset] || PRESETS.recommended;
      status('Optimizing…', 0);
      const r = await tryRun(() => smartCompress(bytes, Object.assign({}, base, p), (f) => status('Optimizing…', f)));
      if (r.error && encrypted) {
        status('Protected PDF — flattening…', 0);
        const fr = await tryRun(() => flattenCompress(bytes, Object.assign({ dpi: 120, quality: 0.6 }, base), (f) => status('Flattening…', f)));
        return pick(fr, { note: 'This PDF has security restrictions, so pages were flattened.' });
      }
      if (r.error) throw r.error;
      return pick(r);
    }

    const target = options.targetBytes;
    if (original.length <= target) {
      const ll = isEncrypted(bytes) ? null : await tryRun(() => smartCompress(bytes, Object.assign({}, base, { images: false })));
      return pick(ll, { hit: true, note: 'Your file was already under the target size' + (ll && !ll.error && ll.bytes.length < original.length ? ' — we still removed hidden waste.' : '.') });
    }
    let smallest = null;
    if (!isEncrypted(bytes)) {
      status('Trying lossless cleanup…', 0.02);
      const ll = await tryRun(() => smartCompress(bytes, Object.assign({}, base, { images: false })));
      if (!ll.error) {
        smallest = ll;
        if (ll.bytes.length <= target) return pick(ll, { hit: true });
        const s = await searchLadder(SMART_LADDER, (o) => smartCompress(bytes, Object.assign({}, base, o)), target,
          (i) => status('Re-encoding images (level ' + (i + 1) + '/' + SMART_LADDER.length + ')…', 0.1 + i * 0.05));
        if (s.best) return pick(s.best, { hit: true });
        if (s.smallest && s.smallest.bytes.length < smallest.bytes.length) smallest = s.smallest;
      }
    }
    if (options.allowFlatten !== false) {
      const s = await searchLadder(FLATTEN_LADDER, (o) => flattenCompress(bytes, Object.assign({}, base, o, { gray: base.gray || o.gray })),
        target, (i) => status('Flattening pages (level ' + (i + 1) + '/' + FLATTEN_LADDER.length + ')…', 0.5 + i * 0.05));
      if (s.best) return pick(s.best, { hit: true, note: 'Pages were flattened to images to reach the target — text is no longer selectable.' });
      if (s.smallest && (!smallest || s.smallest.bytes.length < smallest.bytes.length)) smallest = s.smallest;
    }
    return pick(smallest, {
      hit: false,
      note: options.allowFlatten === false
        ? 'Could not reach the target without flattening. Enable “Allow flattening” or split the PDF.'
        : 'Could not reach the target — this is the smallest readable version. Try splitting the PDF into fewer pages.',
    });
  }

  window.PdfShrink = { compress, ready, getPdfjs, _internal: { smartCompress, flattenCompress, garbageCollect } };
})();

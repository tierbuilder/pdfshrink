// Edge Worker. Static files are served straight from dist/ (assets-first);
// this code only runs for /api/* and verification files (see run_worker_first in wrangler.jsonc).
//
// POST /api/event — anonymous usage events from the tools, e.g.
//   {"n":"compressed","u":"/compress-pdf-to-100kb/","p":{"mode":"target","method":"smart","hit":true,"saved":72}}
// Stored in Workers Analytics Engine (dataset pdfshrink) and echoed to Workers Logs.
// Never receives files, file names or IP addresses; only the event, page path,
// settings/outcome and Cloudflare's approximate country.

const EVENTS = new Set([
  'files_added', 'compressed', 'error', 'share', 'zip_download',
  'images_added', 'image_resized', 'merged', 'split', 'images_to_pdf', 'pdf_to_images',
]);
// Search-engine ownership files, served verbatim. Cloudflare's clean-URL handling would
// otherwise redirect *.html, which can make verification fail. Only these exact tokens.
const VERIFY = {
  '/google377b9814c655af97.html': 'google-site-verification: google377b9814c655af97.html',
};
const STR_KEYS = ['mode', 'method', 'msg'];
const NUM_KEYS = ['saved', 'kb', 'count', 'pages', 'files', 'dpi'];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (VERIFY[url.pathname]) {
      return new Response(VERIFY[url.pathname], { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
    }
    if (url.pathname === '/api/event') {
      if (request.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: { Allow: 'POST' } });
      return handleEvent(request, env, url);
    }
    if (url.pathname.startsWith('/api/')) return new Response('Not found', { status: 404 });
    return env.ASSETS.fetch(request);
  },
};

async function handleEvent(request, env, url) {
  const origin = request.headers.get('Origin');
  if (origin && origin !== url.origin) return new Response(null, { status: 403 });
  if (Number(request.headers.get('Content-Length') || 0) > 2048) return new Response(null, { status: 413 });

  let body;
  try { body = JSON.parse(await request.text()); } catch { return new Response(null, { status: 400 }); }
  const name = typeof body.n === 'string' ? body.n : '';
  if (!EVENTS.has(name)) return new Response(null, { status: 204 }); // ignore unknown events quietly

  const raw = body.p && typeof body.p === 'object' ? body.p : {};
  const p = {};
  for (const k of STR_KEYS) if (typeof raw[k] === 'string') p[k] = clean(raw[k]);
  for (const k of NUM_KEYS) if (Number.isFinite(raw[k])) p[k] = Math.round(raw[k]);
  if (typeof raw.hit === 'boolean') p.hit = raw.hit;
  const page = typeof body.u === 'string' && body.u.startsWith('/') ? body.u.split(/[?#]/)[0].slice(0, 80) : '';
  const country = (request.cf && request.cf.country) || 'XX';

  try {
    env.EVENTS && env.EVENTS.writeDataPoint({
      indexes: [name],
      // blob1..blob7
      blobs: [name, page, country, p.mode || '', p.method || '', p.hit === undefined ? '' : String(p.hit), p.msg || ''],
      // double1..double6
      doubles: [p.saved ?? 0, p.kb ?? 0, p.count ?? 0, p.pages ?? 0, p.files ?? 0, p.dpi ?? 0],
    });
  } catch (e) { /* analytics must never break the site */ }
  console.log(JSON.stringify({ event: name, page, country, ...p }));
  return new Response(null, { status: 204 });
}

// Strip anything that could carry a file name or other identifying text.
function clean(s) {
  return s.replace(/[“"'‘’][^“"'‘’]*[”"'‘’]/g, '…').replace(/[^\w .:,()\-/…]/g, '').slice(0, 60);
}

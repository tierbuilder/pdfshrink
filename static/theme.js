/* Site chrome. Theme: "auto" (follow the system), "light" or "dark" — loaded in <head> (not deferred)
 * so the saved choice applies before first paint. Header menus are <details> disclosures (work without
 * JS); this script only closes them on outside click / Escape and keeps one open at a time. */
(function () {
  'use strict';
  const KEY = 'theme';
  const root = document.documentElement;
  const get = () => { try { return localStorage.getItem(KEY) || 'auto'; } catch (e) { return 'auto'; } };
  const apply = (mode) => {
    if (mode === 'light' || mode === 'dark') root.dataset.theme = mode;
    else delete root.dataset.theme;
  };
  apply(get());

  document.addEventListener('DOMContentLoaded', () => {
    const menus = Array.from(document.querySelectorAll('header.site details.dd'));
    menus.forEach((d) => d.addEventListener('toggle', () => {
      if (d.open) menus.forEach((o) => { if (o !== d) o.open = false; });
    }));
    document.addEventListener('click', (e) => menus.forEach((d) => { if (d.open && !d.contains(e.target)) d.open = false; }));
    document.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape') return;
      menus.forEach((d) => { if (d.open) { d.open = false; d.querySelector('summary').focus(); } });
    });

    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    const order = ['auto', 'light', 'dark'];
    const sync = () => {
      const mode = get();
      btn.dataset.mode = mode;
      const label = btn.dataset['label' + mode[0].toUpperCase() + mode.slice(1)] || mode;
      btn.setAttribute('aria-label', label);
      btn.title = label;
      const text = btn.querySelector('.theme-text');
      if (text) text.textContent = label;
    };
    btn.addEventListener('click', () => {
      const next = order[(order.indexOf(get()) + 1) % order.length];
      try { localStorage.setItem(KEY, next); } catch (e) { /* private mode: applies for this page only */ }
      root.classList.add('theme-switching'); // switch colours instantly, without mid-fade flicker
      apply(next);
      requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove('theme-switching')));
      sync();
    });
    sync();
  });
})();

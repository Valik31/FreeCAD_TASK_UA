/* ==========================================================================
   Уроки FreeCAD — скрипти сайту
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- Старі адреси з #/ (Docsify) -> нові сторінки ---------- */
  var h = location.hash;
  if (h.indexOf('#/') === 0) {
    var slug = h.slice(2).split('?')[0].replace(/\.md$/, '');
    var target = (!slug || slug === 'home' || slug === 'README') ? 'index.html'
               : (/^\d{2}-/.test(slug) ? slug + '.html' : 'index.html');
    location.replace(target);
    return;
  }

  /* ---------- Прогрес (localStorage) ---------- */
  var KEY = 'freecad-progress-v1';
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(p) { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {} }
  function idFromHref(href) {
    var m = (href || '').match(/(?:^|\/)(\d{2}-[^\/?#]+)\.html/);
    return m ? m[1] : null;
  }

  var lessonId = document.body.getAttribute('data-lesson') || null;

  function refresh() {
    var done = load().done || {};

    var btn = document.querySelector('.done-btn');
    if (btn && lessonId) {
      var isDone = !!done[lessonId];
      btn.className = 'done-btn' + (isDone ? ' is-done' : '');
      btn.textContent = isDone ? '✓ Виконано (натисніть, щоб скасувати)' : 'Позначити як виконане';
    }

    document.querySelectorAll('.sidebar-nav a[data-lesson]').forEach(function (a) {
      a.classList.toggle('lesson-done', !!done[a.getAttribute('data-lesson')]);
    });

    var total = 0, count = 0;
    document.querySelectorAll('.lesson-cards a').forEach(function (a) {
      var id = idFromHref(a.getAttribute('href'));
      if (!id) return;
      total++;
      if (done[id]) { count++; a.classList.add('done'); } else { a.classList.remove('done'); }
    });

    var box = document.getElementById('progress');
    if (box && total) {
      var pct = Math.round(count / total * 100);
      box.innerHTML =
        '<div class="progress-text">Твій прогрес: ' + count + ' з ' + total + ' (' + pct + '%)' +
        (count ? '<a class="progress-reset">скинути</a>' : '') + '</div>' +
        '<div class="progress-bar"><div class="progress-fill"></div></div>';
      setTimeout(function () { box.querySelector('.progress-fill').style.width = pct + '%'; }, 30);
      var r = box.querySelector('.progress-reset');
      if (r) r.onclick = function () {
        if (confirm('Скинути всі позначки «Виконано»?')) { save({}); refresh(); }
      };
    }
  }

  var doneBtn = document.querySelector('.done-btn');
  if (doneBtn && lessonId) {
    doneBtn.addEventListener('click', function () {
      var p = load(); p.done = p.done || {};
      if (p.done[lessonId]) delete p.done[lessonId];
      else p.done[lessonId] = new Date().toISOString().slice(0, 10);
      save(p); refresh();
    });
  }
  refresh();

  /* ---------- Меню на телефоні ---------- */
  var menuBtn = document.querySelector('.menu-btn');
  if (menuBtn) menuBtn.addEventListener('click', function () { document.body.classList.toggle('menu-open'); });
  document.querySelector('.content').addEventListener('click', function () { document.body.classList.remove('menu-open'); });

  /* ---------- Збільшення картинок ---------- */
  document.querySelectorAll('.markdown-section img').forEach(function (img) {
    if (img.classList.contains('ic') || img.closest('.lesson-cards') || img.closest('a')) return;
    img.classList.add('zoomable');
    img.addEventListener('click', function () {
      var o = document.createElement('div');
      o.className = 'zoom-overlay';
      o.innerHTML = '<img alt="">';
      o.firstChild.src = img.src;
      o.addEventListener('click', function () { o.remove(); });
      document.body.appendChild(o);
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { var o = document.querySelector('.zoom-overlay'); if (o) o.remove(); }
  });

  /* ---------- Пошук ---------- */
  var input = document.querySelector('.search input');
  var results = document.querySelector('.search-results');
  var index = null;

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function doSearch() {
    var q = input.value.trim().toLowerCase();
    if (!q) { results.innerHTML = ''; return; }
    var words = q.split(/\s+/).filter(Boolean);
    var html = '', n = 0;
    index.forEach(function (p) {
      var hay = (p.title + ' ' + p.text).toLowerCase();
      if (!words.every(function (w) { return hay.indexOf(w) !== -1; })) return;
      var pos = p.text.toLowerCase().indexOf(words[0]);
      var snip = pos >= 0 ? p.text.slice(Math.max(0, pos - 40), pos + 90) : p.text.slice(0, 120);
      snip = esc(snip);
      words.forEach(function (w) { snip = snip.replace(new RegExp('(' + escRe(esc(w)) + ')', 'gi'), '<mark>$1</mark>'); });
      html += '<a href="' + p.url + '"><b>' + esc(p.title) + '</b><small>…' + snip + '…</small></a>';
      n++;
    });
    results.innerHTML = n ? html : '<div class="empty">Нічого не знайдено</div>';
  }

  if (input) {
    input.addEventListener('input', function () {
      if (!index && window.SEARCH_INDEX) index = window.SEARCH_INDEX;
      if (index) return doSearch();
      fetch('search.json').then(function (r) { return r.json(); })
        .then(function (data) { index = data; doSearch(); })
        .catch(function () { results.innerHTML = '<div class="empty">Пошук недоступний</div>'; });
    });
  }
})();

// RAG 入門簡報：導覽、互動範例、quiz。沒有 JavaScript 時頁面仍以文件形式完整可讀。
(function () {
  'use strict';

  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var cur = document.getElementById('cur');
  var total = document.getElementById('total');
  var bar = document.getElementById('bar');
  var prev = document.getElementById('prev');
  var next = document.getElementById('next');
  var index = 0;

  total.textContent = String(slides.length);

  function show(i, updateHash) {
    index = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach(function (s, k) {
      var active = k === index;
      s.classList.toggle('active', active);
      s.setAttribute('aria-hidden', active ? 'false' : 'true');
      if ('inert' in s) { s.inert = !active; }
    });
    slides[index].scrollTop = 0;
    cur.textContent = String(index + 1);
    bar.style.width = ((index + 1) / slides.length * 100) + '%';
    prev.disabled = index === 0;
    next.disabled = index === slides.length - 1;
    if (updateHash !== false) {
      history.replaceState(null, '', '#' + (index + 1));
    }
  }

  function fromHash() {
    var n = parseInt(location.hash.replace('#', '').replace(/^s/, ''), 10);
    return isNaN(n) ? 0 : n - 1;
  }

  prev.addEventListener('click', function () { show(index - 1); });
  next.addEventListener('click', function () { show(index + 1); });
  window.addEventListener('hashchange', function () { show(fromHash(), false); });

  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) { return; }
    var tag = (e.target && e.target.tagName) || '';
    // Let buttons and form controls keep Space/Enter.
    var onControl = tag === 'BUTTON' || tag === 'SUMMARY' || tag === 'INPUT' || tag === 'A';
    switch (e.key) {
      case 'ArrowRight': case 'PageDown':
        show(index + 1); e.preventDefault(); break;
      case 'ArrowLeft': case 'PageUp':
        show(index - 1); e.preventDefault(); break;
      case ' ':
        if (!onControl) { show(e.shiftKey ? index - 1 : index + 1); e.preventDefault(); }
        break;
      case 'Home': show(0); e.preventDefault(); break;
      case 'End': show(slides.length - 1); e.preventDefault(); break;
    }
  });

  // Touch: horizontal swipe only, so vertical scrolling inside a slide still works.
  var sx = null, sy = null;
  document.addEventListener('touchstart', function (e) {
    if (e.touches.length !== 1) { sx = null; return; }
    sx = e.touches[0].clientX; sy = e.touches[0].clientY;
  }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (sx === null) { return; }
    var dx = e.changedTouches[0].clientX - sx;
    var dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
      show(dx < 0 ? index + 1 : index - 1);
    }
    sx = null;
  }, { passive: true });

  // Slide 5: step-by-step RAG example.
  document.querySelectorAll('[data-stepper]').forEach(function (root) {
    var buttons = root.querySelectorAll('[data-step]');
    var panels = root.querySelectorAll('[data-panel]');
    function go(n) {
      panels.forEach(function (p) {
        p.classList.toggle('shown', Number(p.dataset.panel) <= n);
      });
      buttons.forEach(function (b) {
        b.setAttribute('aria-pressed', String(Number(b.dataset.step) === n));
      });
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function () { go(Number(b.dataset.step)); });
    });
    go(0);
  });

  // Slide 8: failure scenarios.
  document.querySelectorAll('[data-scenarios]').forEach(function (root) {
    var buttons = root.querySelectorAll('[data-sc]');
    var rows = root.querySelectorAll('[data-row]');
    function pick(n) {
      rows.forEach(function (r) { r.classList.toggle('on', Number(r.dataset.row) === n); });
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(Number(b.dataset.sc) === n)); });
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function () { pick(Number(b.dataset.sc)); });
    });
    pick(0);
  });

  // Slide 13: quiz.
  document.querySelectorAll('[data-quiz] .qitem').forEach(function (q) {
    var answer = q.dataset.answer;
    var fb = q.querySelector('.feedback');
    var details = q.querySelector('.explain');
    q.querySelectorAll('[data-opt]').forEach(function (b) {
      b.addEventListener('click', function () {
        var ok = b.dataset.opt === answer;
        q.querySelectorAll('[data-opt]').forEach(function (o) {
          o.classList.remove('correct', 'wrong');
          o.setAttribute('aria-pressed', 'false');
        });
        b.classList.add(ok ? 'correct' : 'wrong');
        b.setAttribute('aria-pressed', 'true');
        fb.textContent = ok ? '答對了！' : '再想想看。';
        if (ok) { details.open = true; }
      });
    });
  });

  show(fromHash(), false);
})();

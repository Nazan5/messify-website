/* Messify site script. Plain JS, no libraries. Every feature checks that its elements exist first. */
(function () {
  'use strict';

  var CONFIG = {
    whatsapp: '971502513033',
    // Form submissions are emailed to this address through FormSubmit (formsubmit.co).
    // The first submission sends an activation email to this inbox: click the link once to switch it on.
    formEndpoint: 'https://formsubmit.co/ajax/info@messify.me'
  };

  // Plans in AED. Weekly = 7 days of meals to use within 9 days, monthly = 26 days of meals to use within 30 days. 1 meal = 1 token.
  var PLANS = {
    1: { weekly: { price: 215, tokens: 7 }, monthly: { price: 715, tokens: 26 } },
    2: { weekly: { price: 415, tokens: 14 }, monthly: { price: 1400, tokens: 52 } },
    3: { weekly: { price: 610, tokens: 21 }, monthly: { price: 1999, tokens: 78 } }
  };

  // Folder that holds /assets/, worked out from this script's own URL so paths work on any host.
  var ASSETS = ((document.currentScript && document.currentScript.src) || '/assets/js/site.js').replace(/js\/site\.js.*$/, '');

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fmt = function (n) { return n.toLocaleString('en-US'); };
  var mealsLabel = function (m) { return m + (m > 1 ? ' meals' : ' meal') + ' a day'; };
  var waLink = function (text) { return 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(text); };

  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Opening a page always starts at the top (unless the link points to a section) ---------- */
  (function () {
    var nav = performance.getEntriesByType ? performance.getEntriesByType('navigation')[0] : null;
    if (location.hash || (nav && nav.type === 'back_forward')) return;
    var root = document.documentElement, prev = root.style.scrollBehavior;
    root.style.scrollBehavior = 'auto';
    window.scrollTo(0, 0);
    requestAnimationFrame(function () { root.style.scrollBehavior = prev; });
  })();
  window.addEventListener('pageshow', function (e) { if (e.persisted) onScroll(); });

  /* ---------- Scroll reveal: sections and cards ease in as they enter the screen ---------- */
  (function () {
    if (reduce || !('IntersectionObserver' in window)) return;
    var SKIP = '.gate, .sec--first, details, [data-start-page] .stage, [data-start-page] .chat';
    var LONG = '.terms-sec, .toc'; // long pages: animate even inside the first section
    var singles = '.sec-head, .quotes-head, .photo, .ledger, .answer, .band, .composer, .faq, .form-grid > div, .table-wrap, .terms-sec, .toc, .start-end, .way > div:first-child';
    var groups = '.plans, .dishes, .areas, .events, .reasons, .places, .token-cards, .steps, .emirates, .why, .duo, .ticks, .mosaic, .quotes';
    var items = [];
    $$(singles).forEach(function (el) { if (!el.closest(SKIP) || (el.matches(LONG) && !el.closest('details'))) { el.setAttribute('data-reveal', ''); items.push(el); } });
    $$(groups).forEach(function (g) {
      if (g.closest(SKIP)) return;
      Array.prototype.forEach.call(g.children, function (el, i) {
        el.setAttribute('data-reveal', '');
        el.style.setProperty('--d', Math.min(i * 0.08, 0.4) + 's');
        items.push(el);
      });
    });
    // Anything already on screen shows straight away, so nothing flickers on load.
    var vh = window.innerHeight;
    items.forEach(function (el) { if (el.getBoundingClientRect().top < vh * 0.92) el.classList.add('in'); });
    document.documentElement.classList.add('reveal-ready');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (el) { if (!el.classList.contains('in')) io.observe(el); });
  })();

  /* ---------- Google Analytics events: WhatsApp, phone, app store and start-plan clicks ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a || typeof window.gtag !== 'function') return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('wa.me') > -1) window.gtag('event', 'whatsapp_click', { page_path: location.pathname });
    else if (h.indexOf('tel:') === 0) window.gtag('event', 'phone_click', { page_path: location.pathname });
    else if (h.indexOf('apps.apple.com') > -1 || h.indexOf('play.google.com') > -1) window.gtag('event', 'app_store_click', { store: h.indexOf('play.google.com') > -1 ? 'google_play' : 'app_store', page_path: location.pathname });
    else if (h.indexOf('/start/') > -1) window.gtag('event', 'start_plan_click', { page_path: location.pathname });
  });

  /* ---------- Home gateway: fades out as you scroll, back in as you scroll up ---------- */
  var gate = $('.gate');
  var ticking = false;
  var scrollHooks = [];
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      if (gate) {
        var h = gate.offsetHeight || window.innerHeight;
        var p = Math.min(1, Math.max(0, window.scrollY / (h * 0.9)));
        gate.style.setProperty('--p', p.toFixed(3));
        gate.classList.toggle('is-gone', p >= 1);
        document.body.classList.toggle('past-gate', window.scrollY > h * 0.82);
      }
      scrollHooks.forEach(function (fn) { fn(); });
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);

  /* ---------- Plan cards: weekly / monthly ---------- */
  var duration = 'monthly';
  function setDuration(dur) {
    duration = dur;
    $$('.toggle button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.dur === dur)); });
    $$('.plan[data-plan]').forEach(function (card) {
      var p = PLANS[card.dataset.plan][dur];
      card.querySelector('[data-price]').textContent = 'AED ' + fmt(p.price);
      card.querySelector('[data-unit]').textContent = dur === 'weekly' ? '/ week' : '/ month';
      card.querySelector('[data-per]').textContent = 'AED ' + (p.price / p.tokens).toFixed(2) + ' per meal';
      card.querySelector('[data-tokens]').textContent = p.tokens + ' tokens · ' + (dur === 'weekly' ? '7 days of meals, use within 9 days' : '26 days of meals, use within 30 days');
    });
    $$('a[data-start-meals]').forEach(function (a) {
      a.href = a.getAttribute('href').split('?')[0] + '?meals=' + a.dataset.startMeals + '&duration=' + dur;
    });
  }
  $$('.toggle button').forEach(function (b) { b.addEventListener('click', function () { setDuration(b.dataset.dur); }); });

  /* ---------- Start page: app or WhatsApp ---------- */
  var startRoot = $('[data-start-page]');
  if (startRoot) {
    var q = new URLSearchParams(location.search);
    var pick = {
      meals: [1, 2, 3].indexOf(Number(q.get('meals'))) > -1 ? Number(q.get('meals')) : 2,
      dur: q.get('duration') === 'weekly' ? 'weekly' : 'monthly'
    };
    var renderStart = function () {
      var p = PLANS[pick.meals][pick.dur];
      var coins = '';
      for (var i = 0; i < pick.meals; i++) coins += '<img src="' + ASSETS + 'img/coin.webp" alt="" width="36" height="34">';
      $('[data-s-coins]').innerHTML = coins;
      $('[data-s-name]').textContent = mealsLabel(pick.meals) + ' · ' + (pick.dur === 'weekly' ? 'Weekly' : 'Monthly');
      $('[data-s-price]').textContent = 'AED ' + fmt(p.price);
      $('[data-s-unit]').textContent = pick.dur === 'weekly' ? '/ week' : '/ month';
      $('[data-s-meta]').textContent = 'AED ' + (p.price / p.tokens).toFixed(2) + ' per meal · ' + p.tokens + ' tokens · ' + (pick.dur === 'weekly' ? '7 days of meals, use within 9 days' : '26 days of meals, use within 30 days');
      $('[data-s-appline]').innerHTML = 'You’ll confirm <b>' + mealsLabel(pick.meals) + ', ' + pick.dur + '</b> in the app.';
      var count = $('[data-s-count]');
      count.dataset.target = p.tokens;
      count.textContent = '+' + p.tokens;
      var line = 'Hi Messify! I’m interested in the ' + mealsLabel(pick.meals) + ' ' + pick.dur + ' plan.';
      $('[data-s-chat1]').textContent = line;
      var waHref = waLink(line + ' Can you help me get started?'); $$('[data-s-wa]').forEach(function (a) { a.href = waHref; });
      $$('[data-s="meals"] .chip').forEach(function (c) { c.setAttribute('aria-pressed', String(Number(c.dataset.value) === pick.meals)); });
      $$('[data-s="dur"] .chip').forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.value === pick.dur)); });
      try { history.replaceState(null, '', location.pathname + '?meals=' + pick.meals + '&duration=' + pick.dur); } catch (e) {}
    };
    $$('[data-s] .chip').forEach(function (c) {
      c.addEventListener('click', function () {
        if (c.parentElement.dataset.s === 'meals') pick.meals = Number(c.dataset.value); else pick.dur = c.dataset.value;
        renderStart();
      });
    });
    renderStart();

    // Scroll animation: app icon pops, coins burst, wallet counts up; chat bubbles arrive one by one.
    var stage = $('[data-stage]');
    var chat = $('[data-chat]');
    var bubbles = $$('.bubble', chat);
    var shown = 0, busy = false;
    var countUp = function (el) {
      var target = Number(el.dataset.target) || 0, t0 = performance.now(), dur = 900;
      var step = function (now) {
        var k = Math.min(1, (now - t0) / dur);
        el.textContent = '+' + Math.round(target * (1 - Math.pow(1 - k, 3)));
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if (!reduce && 'IntersectionObserver' in window) {
      stage.classList.add('armed');
      chat.classList.add('armed');
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { stage.classList.add('in'); countUp($('[data-s-count]')); io.disconnect(); }
        });
      }, { threshold: 0.35 });
      io.observe(stage);
      var revealChat = function () {
        if (busy || shown >= bubbles.length) return;
        var b = bubbles[shown];
        if (b.getBoundingClientRect().top > window.innerHeight * 0.86) return;
        busy = true;
        var done = function () {
          b.classList.remove('typing'); b.classList.add('shown'); shown++;
          setTimeout(function () { busy = false; revealChat(); }, 380);
        };
        if (b.classList.contains('them')) { b.classList.add('typing'); setTimeout(done, 750); } else done();
      };
      scrollHooks.push(function () {
        var r = stage.getBoundingClientRect(), vh = window.innerHeight;
        var sp = Math.max(-1, Math.min(1, (vh / 2 - (r.top + r.height / 2)) / (vh / 2)));
        stage.style.setProperty('--sp', sp.toFixed(3));
        revealChat();
      });
    }
  }

  /* ---------- Catering menu builder ---------- */
  var guests = $('#b-guests');
  if (guests) {
    var guestsOut = $('#b-guests-out');
    var briefText = $('#briefText');
    var picked = function (g) { return $$('[data-group="' + g + '"] .chip[aria-pressed="true"]').map(function (c) { return c.dataset.value; }); };
    var joinList = function (a) { return a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]; };
    var updateBrief = function () {
      var n = Number(guests.value);
      guestsOut.textContent = fmt(n);
      var c = picked('course').map(function (x, i) { return i === 0 ? x : x.toLowerCase(); });
      var courses = joinList(c);
      var f = picked('flavour');
      var flav = (f.length === 1 && f[0] === 'Other') ? 'flavours of your choice' : joinList(f.map(function (x) { return x === 'Other' ? 'other' : x; })) + ' flavours';
      briefText.innerHTML = courses.charAt(0).toUpperCase() + courses.slice(1) + ' in <em>' + flav + '</em>, for <em>' + fmt(n) + ' guests</em> in ' + picked('emirate')[0] + '.';
    };
    $$('.composer .chips').forEach(function (group) {
      var multi = group.hasAttribute('data-multi');
      group.addEventListener('click', function (e) {
        var chip = e.target.closest('.chip');
        if (!chip) return;
        if (multi) {
          var on = chip.getAttribute('aria-pressed') === 'true';
          if (on && picked(group.dataset.group).length === 1) return; // keep at least one
          chip.setAttribute('aria-pressed', String(!on));
        } else {
          $$('.chip', group).forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
        }
        updateBrief();
      });
    });
    guests.addEventListener('input', updateBrief);
    var useBrief = $('#useBrief');
    if (useBrief) useBrief.addEventListener('click', function () {
      $('#q-guests').value = guests.value;
      $('#q-emirate').value = picked('emirate')[0];
      $('#q-notes').value = 'Menu: ' + picked('course').join(', ') + '. Flavours: ' + picked('flavour').join(', ') + '.';
      setTimeout(function () { $('#q-name').focus({ preventScroll: true }); }, 700);
    });
    updateBrief();
  }

  /* ---------- Forms: validate, email via FormSubmit, fall back to WhatsApp ---------- */
  function validate(form) {
    var ok = true;
    $$('[required]', form).forEach(function (input) {
      var err = input.parentElement.querySelector('.err');
      var v = input.value.trim();
      var msg = '';
      if (!v) msg = 'Please fill this in.';
      else if (input.type === 'tel' && v.replace(/\D/g, '').length < 9) msg = 'Enter a phone number with at least 9 digits.';
      else if (input.type === 'number' && Number(v) < 1) msg = 'Enter a headcount of at least 1.';
      if (err) err.textContent = msg;
      input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (msg && ok) { input.focus(); ok = false; }
    });
    return ok;
  }
  function summarise(form) {
    var lines = [form.dataset.waIntro || 'Hi Messify,'];
    $$('input, select, textarea', form).forEach(function (el) {
      if (!el.name || el.name.charAt(0) === '_' || el.name === 'website') return;
      if ((el.type === 'radio' || el.type === 'checkbox') && !el.checked) return;
      if (!el.value.trim()) return;
      var label = el.dataset.label || el.name;
      lines.push(label + ': ' + el.value.trim());
    });
    return lines.join('\n');
  }
  $$('form[data-form]').forEach(function (form) {
    var status = $('.form-status', form);
    var btn = $('button[type="submit"]', form);
    var done = document.getElementById(form.dataset.done);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (status) status.textContent = '';
      if (!validate(form)) return;
      var name = (form.elements.name && form.elements.name.value.trim().split(' ')[0]) || '';
      var finish = function () {
        var t = done && $('[data-done-title]', done);
        if (t && name) t.textContent = 'Thanks, ' + name + '. We’ve got it.';
        var wa = done && $('[data-done-wa]', done);
        if (wa) wa.href = waLink(summarise(form));
        if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { form_type: form.dataset.form });
        form.hidden = true;
        if (done) { done.hidden = false; done.focus && done.focus(); }
      };
      if (form.elements.website && form.elements.website.value) { finish(); return; } // bot trap
      var data = {};
      $$('input, select, textarea', form).forEach(function (el) {
        if (!el.name || el.name === 'website') return;
        if ((el.type === 'radio' || el.type === 'checkbox') && !el.checked) return;
        data[el.dataset.label || el.name] = el.value;
      });
      data._template = 'table';
      data._captcha = 'false';
      btn.disabled = true;
      var oldText = btn.textContent;
      btn.textContent = 'Sending…';
      fetch(CONFIG.formEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (r) { return r.json(); }).then(function (res) {
        if (String(res.success) === 'true') finish();
        else throw new Error(res.message || 'Not sent');
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = oldText;
        if (status) status.innerHTML = 'We couldn’t send that just now. <a href="' + waLink(summarise(form)) + '" target="_blank" rel="noopener">Send it on WhatsApp instead</a> or call +971 50 251 3033.';
      });
    });
  });

  /* ---------- Meal plan vs ordering-in calculator (guides) ---------- */
  $$('[data-calc]').forEach(function (box) {
    var spend = $('#calc-spend', box);
    var fmt = function (n) { return 'AED ' + Math.round(n).toLocaleString('en-US'); };
    var run = function () {
      var m = +(($('input[name="calc-meals"]:checked', box) || {}).value || 2);
      var each = Math.max(0, parseFloat(spend.value) || 0);
      var order = m * 26 * each, plan = PLANS[m].monthly.price, diff = order - plan;
      $('[data-calc-order]', box).textContent = fmt(order);
      $('[data-calc-plan]', box).textContent = fmt(plan);
      $('[data-calc-diff]', box).textContent = (diff >= 0 ? '' : '−') + fmt(Math.abs(diff)) + (diff >= 0 ? ' saved' : ' more');
    };
    box.addEventListener('input', run); box.addEventListener('change', run); run();
  });

  onScroll();
})();

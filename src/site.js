/* Livewell Passport — header state, mega menu, journey rail, count-ups, reveals, contact form */
(function () {
  var header = document.querySelector('.header');
  var mega = document.getElementById('mega');
  var openers = document.querySelectorAll('[data-menu]');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Header turns solid once the page scrolls
  var hero = document.querySelector('.hero');
  var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > (hero ? hero.offsetHeight - 140 : 12)); };
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  // Mega menu (desktop and mobile share it)
  function setMenu(open) {
    header.classList.toggle('menu-open', open);
    mega.classList.toggle('open', open);
    document.documentElement.classList.toggle('no-scroll', open);
    if (open) mega.style.setProperty('--mega-top', Math.max(0, header.getBoundingClientRect().bottom) + 'px');
    openers.forEach(function (b) { b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
    if (open) setTimeout(function () { mega.focus({ preventScroll: true }); }, 250);
  }
  openers.forEach(function (b) { b.addEventListener('click', function () { setMenu(!mega.classList.contains('open')); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && mega.classList.contains('open')) { setMenu(false); openers[0].focus(); } });
  mega.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });

  // Preview image swaps as you move across the journeys
  var prev = mega.querySelector('.mega-preview');
  if (prev) {
    var imgs = prev.querySelectorAll('img'), cap = prev.querySelector('.cap'), cur = 0;
    mega.querySelectorAll('[data-img]').forEach(function (a) {
      a.addEventListener('mouseenter', function () {
        var next = imgs[1 - cur];
        if (next.getAttribute('src') !== a.dataset.img) next.src = a.dataset.img;
        next.classList.add('show'); imgs[cur].classList.remove('show'); cur = 1 - cur;
        cap.textContent = a.dataset.cap || '';
      });
    });
  }

  // Journey rail: arrows + progress
  var rail = document.querySelector('.rail');
  if (rail) {
    var bar = document.querySelector('.rail-progress i');
    var step = function () { return (rail.querySelector('.rcard').offsetWidth + 16); };
    document.querySelector('[data-rail="next"]').addEventListener('click', function () { rail.scrollBy({ left: step(), behavior: 'smooth' }); });
    document.querySelector('[data-rail="prev"]').addEventListener('click', function () { rail.scrollBy({ left: -step(), behavior: 'smooth' }); });
    var prog = function () {
      var max = rail.scrollWidth - rail.clientWidth;
      var frac = rail.clientWidth / rail.scrollWidth;
      bar.style.width = (frac * 100) + '%';
      bar.style.transform = 'translateX(' + (max ? (rail.scrollLeft / max) * (100 / frac - 100) : 0) + '%)';
    };
    rail.addEventListener('scroll', prog, { passive: true }); window.addEventListener('resize', prog); prog();
  }

  // Count-ups for the site's own figures
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return; cio.unobserve(en.target);
        var el = en.target, end = +el.dataset.count, t0 = null, dec = (el.dataset.count.split('.')[1] || '').length;
        if (reduce) return;
        var tick = function (t) { t0 = t0 || t; var p = Math.min(1, (t - t0) / 1400); p = 1 - Math.pow(1 - p, 3); el.textContent = (end * p).toFixed(dec); if (p < 1) requestAnimationFrame(tick); };
        requestAnimationFrame(tick);
      });
    }, { threshold: .6 });
    counters.forEach(function (c) { cio.observe(c); });

    // Icon tiles pop in when they enter the viewport
    if (!reduce) {
      var iio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en, i) { if (en.isIntersecting) { en.target.classList.add('pop'); iio.unobserve(en.target); } });
      }, { threshold: .4 });
      document.querySelectorAll('[data-ico]').forEach(function (el, i) { el.style.animationDelay = (i % 4) * 90 + 'ms'; iio.observe(el); });
    }

    // Reveal only what sits below the fold at load; the first frame is complete at rest
    if (!reduce) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
      }, { rootMargin: '0px 0px -8% 0px' });
      document.querySelectorAll('[data-reveal]').forEach(function (el) {
        if (el.getBoundingClientRect().top > window.innerHeight) { el.classList.add('reveal'); io.observe(el); } else { el.classList.add('in'); }
      });
    }
  }

  // Contact form: validate, then post to data-endpoint if one is configured
  var form = document.querySelector('form.form');
  if (!form) return;
  var rules = {
    name: function (v) { return v.trim().length >= 2 || 'Please enter your name.'; },
    email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) || 'Enter a valid email address.'; },
    phone: function (v) { return v.trim() === '' || v.replace(/\D/g, '').length >= 10 || 'Enter a 10-digit phone number.'; },
    location: function (v) { return v !== '' || 'Choose a location.'; },
    consent: function (v, el) { return el.checked || 'Please confirm you agree to be contacted.'; }
  };
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true;
    Object.keys(rules).forEach(function (name) {
      var el = form.elements[name]; if (!el) return;
      var field = el.closest('.field'); var r = rules[name](el.value, el);
      if (r !== true) { ok = false; field.classList.add('invalid'); field.querySelector('.error').textContent = r; }
      else field.classList.remove('invalid');
    });
    if (!ok) { form.querySelector('.invalid input, .invalid select').focus(); return; }
    var btn = form.querySelector('button[type=submit]'), endpoint = form.getAttribute('data-endpoint');
    var done = function (delivered) {
      form.classList.add('sent'); var s = form.nextElementSibling;
      s.querySelector('[data-name]').textContent = form.elements.name.value.trim().split(' ')[0];
      s.querySelector('.delivered').hidden = !delivered; s.querySelector('.not-delivered').hidden = delivered; s.focus();
    };
    if (!endpoint) { done(false); return; }
    btn.disabled = true; btn.textContent = 'Sending…';
    fetch(endpoint, { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(form) })
      .then(function (r) { done(r.ok); }).catch(function () { done(false); })
      .finally(function () { btn.disabled = false; btn.textContent = 'Send request'; });
  });
})();

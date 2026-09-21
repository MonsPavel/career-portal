(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.querySelector('[data-production]');
    if (!root) return;

    var slidesEl = root.querySelector('[data-production-slides]');
    var slides = [];
    try { slides = JSON.parse(slidesEl.textContent); } catch (e) { /* статичный слайд */ }
    if (!slides.length) return;

    var photo = root.querySelector('[data-production-photo]');
    var title = root.querySelector('[data-production-title]');
    var text = root.querySelector('[data-production-text]');
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[data-production-tabs] .production__tab'));
    var current = 0;

    function render(index) {
      var s = slides[index];
      if (!s) return;
      if (photo) {
        photo.src = s.photo;
        photo.alt = s.title;
        photo.style.objectFit = s.fit === 'cover' ? 'cover' : 'contain';
        photo.style.objectPosition = s.fit === 'cover' ? 'center' : 'bottom center';
      }
      if (title) title.textContent = s.title;
      if (text) text.innerHTML = s.text.replace(/ — /g, '&nbsp;— ');
      tabs.forEach(function (tab, i) {
        tab.classList.toggle('is-active', i === index);
        tab.setAttribute('aria-selected', i === index ? 'true' : 'false');
      });
      current = index;
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { render(i); });
    });

    var prev = root.querySelector('[data-production-prev]');
    var next = root.querySelector('[data-production-next]');
    if (prev) prev.addEventListener('click', function () { render((current - 1 + slides.length) % slides.length); });
    if (next) next.addEventListener('click', function () { render((current + 1) % slides.length); });
  });
})();

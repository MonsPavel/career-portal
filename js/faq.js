(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-faq]').forEach(function (faq) {
      faq.addEventListener('click', function (e) {
        var q = e.target.closest('.faq__q');
        if (!q) return;
        var item = q.closest('.faq__item');
        item.classList.toggle('is-open');
      });
    });
  });
})();

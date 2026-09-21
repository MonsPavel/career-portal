(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var section = document.querySelector('.directions');
    if (!section) return;

    var modal = section.querySelector('[data-directions-modal]');
    var data = [];
    try {
      data = JSON.parse(section.querySelector('[data-directions-data]').textContent);
    } catch (e) { return; }

    var title = modal.querySelector('[data-directions-title]');
    var subtitle = modal.querySelector('[data-directions-subtitle]');
    var text = modal.querySelector('[data-directions-text]');
    var photo = modal.querySelector('[data-directions-photo]');
    var current = 0;

    function render(i) {
      var d = data[i];
      if (!d) return;
      title.textContent = d.title;
      subtitle.textContent = d.subtitle;
      text.textContent = d.text;
      photo.src = d.photo;
      current = i;
    }

    function open(i) {
      render(i);
      modal.hidden = false;
      document.body.classList.add('directions-modal-open');
    }

    function close() {
      modal.hidden = true;
      document.body.classList.remove('directions-modal-open');
    }

    section.querySelectorAll('[data-direction]').forEach(function (card) {
      card.addEventListener('click', function () {
        open(parseInt(card.getAttribute('data-direction'), 10) || 0);
      });
    });

    modal.querySelectorAll('[data-directions-close]').forEach(function (el) {
      el.addEventListener('click', close);
    });

    modal.querySelector('[data-directions-prev]').addEventListener('click', function () {
      render((current - 1 + data.length) % data.length);
    });
    modal.querySelector('[data-directions-next]').addEventListener('click', function () {
      render((current + 1) % data.length);
    });

    document.addEventListener('keydown', function (e) {
      if (modal.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') modal.querySelector('[data-directions-prev]').click();
      if (e.key === 'ArrowRight') modal.querySelector('[data-directions-next]').click();
    });
  });
})();

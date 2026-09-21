(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var screen = document.querySelector('[data-search-screen]');
    if (!screen) return;

    var input = screen.querySelector('[data-search-input]');
    var form = screen.querySelector('.search-screen__form');
    var hidden = screen.querySelector('[data-search-hidden]');

    function open() {
      screen.hidden = false;
      document.body.classList.add('search-open');
      if (input) input.focus();
    }

    function close() {
      screen.hidden = true;
      document.body.classList.remove('search-open');
    }

    document.querySelectorAll('[data-search-open]').forEach(function (btn) {
      btn.addEventListener('click', open);
    });

    screen.querySelectorAll('[data-search-close]').forEach(function (btn) {
      btn.addEventListener('click', close);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !screen.hidden) close();
    });

    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (hidden && input) hidden.value = input.value;
        // Демо: отправка отключена. В Битриксе — убрать preventDefault
        // и указать action на страницу поиска.
      });
    }
  });
})();

(function () {
  'use strict';

  // Версия для слабовидящих: настройки применяются классами на <body>,
  // состояние сохраняется в localStorage (действует на всём сайте)
  var KEY = 'vi-settings';

  var DEFAULTS = { on: false, size: 'md', theme: 'baw', img: 'on', kern: 'normal' };
  var state = Object.assign({}, DEFAULTS);

  try {
    var saved = JSON.parse(localStorage.getItem(KEY));
    if (saved && typeof saved === 'object') state = Object.assign(state, saved);
  } catch (e) { /* нет доступа к localStorage — режим без сохранения */ }

  var SIZE_CLASSES = ['vi-size--sm', 'vi-size--md', 'vi-size--lg'];
  var THEME_CLASSES = ['vi-theme--baw', 'vi-theme--wb', 'vi-theme--bb'];

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
  }

  function apply() {
    var b = document.body;
    b.classList.toggle('vi', state.on);
    SIZE_CLASSES.forEach(function (c) { b.classList.remove(c); });
    b.classList.add('vi-size--' + state.size);
    THEME_CLASSES.forEach(function (c) { b.classList.remove(c); });
    b.classList.add('vi-theme--' + state.theme);
    b.classList.toggle('vi-img--off', state.img === 'off');
    b.classList.toggle('vi-kern--wide', state.kern === 'wide');

    document.querySelectorAll('[data-vi-panel]').forEach(function (panel) {
      panel.hidden = !state.on;
    });

    // состояние сегментных кнопок
    document.querySelectorAll('[data-vi-set]').forEach(function (btn) {
      var parts = btn.getAttribute('data-vi-set').split(':');
      btn.setAttribute('aria-pressed', String(state[parts[0]] === parts[1]));
    });

    document.querySelectorAll('[data-vi-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(state.on));
    });

    save();
  }

  function set(key, value) {
    state[key] = value;
    apply();
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-vi-set]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var parts = btn.getAttribute('data-vi-set').split(':');
        set(parts[0], parts[1]);
      });
    });

    document.querySelectorAll('[data-vi-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        state.on = !state.on;
        if (state.on) {
          // вход в режим — сброс к стандартным настройкам ГОСТ-панели
          state = Object.assign({}, DEFAULTS, { on: true });
        }
        apply();
        window.scrollTo({ top: 0 });
      });
    });

    apply();
  });
})();

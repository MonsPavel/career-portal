(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('[data-dropdown-toggle]');
    var dropdown = document.getElementById('header-dropdown');
    if (!toggle || !dropdown) return;

    function open() {
      dropdown.hidden = false;
      toggle.setAttribute('aria-expanded', 'true');
    }

    function close() {
      dropdown.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', function () {
      if (dropdown.hidden) { open(); } else { close(); }
    });

    dropdown.querySelector('[data-dropdown-close]').addEventListener('click', close);

    document.addEventListener('click', function (e) {
      if (!dropdown.hidden && !dropdown.contains(e.target) && !toggle.contains(e.target)) {
        close();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !dropdown.hidden) close();
    });
  });
})();

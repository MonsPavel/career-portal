(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('[data-dropdown-toggle]');
    var dropdown = document.getElementById('header-dropdown');
    if (!toggle || !dropdown) return;

    var page = window.location.pathname.split('/').pop();
    var activePage = page === 'internships.html' ? 'practices.html' : page;
    var activeLink = dropdown.querySelector('.header__dropdown-link[href="' + activePage + '"]');
    if (activeLink) activeLink.setAttribute('aria-current', 'page');

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

    document.addEventListener('click', function (e) {
      if (!dropdown.hidden && !dropdown.contains(e.target) && !toggle.contains(e.target)) {
        close();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !dropdown.hidden) {
        close();
        toggle.focus();
      }
    });
  });
})();

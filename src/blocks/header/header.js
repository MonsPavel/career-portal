(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var page = window.location.pathname.split('/').pop();
    var activePage = page === 'internships.html' ? 'practices.html' : page;

    var toggle = document.querySelector('[data-dropdown-toggle]');
    var dropdown = document.getElementById('header-dropdown');
    if (toggle && dropdown) {
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
    }

    /* Мобильное бургер-меню */
    var burger = document.querySelector('[data-mobile-menu-toggle]');
    var mobileMenu = document.getElementById('header-mobile-menu');
    if (burger && mobileMenu) {
      var activeMobileLink = mobileMenu.querySelector('.header__mobile-link[href="' + activePage + '"]');
      if (activeMobileLink) activeMobileLink.setAttribute('aria-current', 'page');

      function openMobile() {
        mobileMenu.hidden = false;
        burger.setAttribute('aria-expanded', 'true');
      }

      function closeMobile() {
        mobileMenu.hidden = true;
        burger.setAttribute('aria-expanded', 'false');
      }

      burger.addEventListener('click', function () {
        if (mobileMenu.hidden) { openMobile(); } else { closeMobile(); }
      });

      mobileMenu.addEventListener('click', function (e) {
        // переход по ссылке или открытие поиска/ВС — меню больше не нужно
        if (e.target.closest('a, button')) closeMobile();
      });

      document.addEventListener('click', function (e) {
        if (!mobileMenu.hidden && !mobileMenu.contains(e.target) && !burger.contains(e.target)) {
          closeMobile();
        }
      });

      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !mobileMenu.hidden) {
          closeMobile();
          burger.focus();
        }
      });
    }

    /* Мобильный переключатель разделов «Школьникам и студентам» (селект вместо табов) */
    document.querySelectorAll('select[data-subnav]').forEach(function (select) {
      select.addEventListener('change', function () {
        if (select.value) window.location.href = select.value;
      });
    });
  });
})();

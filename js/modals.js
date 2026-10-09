(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // [data-reveal="#selector"] — показать скрытый блок и спрятать саму кнопку
    // (инлайн-отклик в карточке вакансии)
    document.querySelectorAll('[data-reveal]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var target = document.querySelector(btn.getAttribute('data-reveal'));
        if (!target) return;
        target.hidden = false;
        btn.hidden = true;
        var field = target.querySelector('input, textarea, select');
        if (field) field.focus();
      });
    });

    // Модалки: [data-modal-open="id"] открывает .modal#id,
    // [data-modal-close] закрывает, Esc и клик по оверлею — тоже.
    function open(id) {
      var modal = document.getElementById(id);
      if (!modal) return;
      modal.hidden = false;
      document.body.style.overflow = 'hidden';
      var focusable = modal.querySelector('.modal__dialog button, .modal__dialog a, .modal__dialog input');
      if (focusable) focusable.focus();
    }

    function close(modal) {
      modal.hidden = true;
      document.body.style.overflow = '';
    }

    document.querySelectorAll('[data-modal-open]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var from = btn.closest('.modal');
        if (from) close(from); // переход из модалки в модалку (заявка из карточки направления)
        open(btn.getAttribute('data-modal-open'));
      });
    });

    document.querySelectorAll('.modal').forEach(function (modal) {
      modal.querySelectorAll('[data-modal-close]').forEach(function (btn) {
        btn.addEventListener('click', function () { close(modal); });
      });
      modal.addEventListener('click', function (e) {
        if (e.target === modal) close(modal);
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      document.querySelectorAll('.modal:not([hidden])').forEach(close);
    });
  });
})();

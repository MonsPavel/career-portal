(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    document.querySelectorAll('form[data-mock-form]').forEach(function (form) {
      var success = form.querySelector('[data-form-success]');
      var fields = form.querySelectorAll('[required]');

      function isVisible(field) {
        return !field.closest('[hidden]');
      }

      function validateField(field) {
        // скрытые условные ветки не валидируем (поля появляются по статусу)
        if (!isVisible(field)) return true;
        var wrap = field.closest('.field') || field.closest('.checkbox');
        if (!wrap) return true;
        var ok;
        if (field.type === 'checkbox') {
          ok = field.checked;
        } else if (field.type === 'email') {
          ok = EMAIL_RE.test(field.value.trim());
        } else {
          ok = field.value.trim() !== '';
        }
        wrap.classList.toggle('field--error', !ok);
        return ok;
      }

      fields.forEach(function (field) {
        field.addEventListener('input', function () {
          var wrap = field.closest('.field');
          if (wrap) wrap.classList.remove('field--error');
        });
        field.addEventListener('change', function () { validateField(field); });
      });

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var valid = true;
        var firstError = null;
        fields.forEach(function (field) {
          if (!validateField(field)) {
            valid = false;
            if (!firstError && isVisible(field)) firstError = field;
          }
        });
        if (!valid) {
          if (firstError) firstError.focus();
          return;
        }
        // Мок: отправки нет — показываем success и блокируем повтор (по ТЗ)
        if (success) success.hidden = false;
        form.querySelector('[data-form-body]').hidden = true;
        success.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
    });
  });
})();

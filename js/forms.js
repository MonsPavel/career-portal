(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var forms = document.querySelectorAll('form[data-mock-form]');

    forms.forEach(function (form) {
      var success = form.querySelector('[data-form-success]');
      var fields = form.querySelectorAll('[required]');

      function validateField(field) {
        var wrap = field.closest('.field') || field.closest('.checkbox');
        if (!wrap) return true;
        var ok = field.type === 'checkbox' ? field.checked : field.value.trim() !== '';
        wrap.classList.toggle('field--error', !ok);
        return ok;
      }

      fields.forEach(function (field) {
        field.addEventListener('input', function () {
          if (field.closest('.field')) field.closest('.field').classList.remove('field--error');
        });
        field.addEventListener('change', function () { validateField(field); });
      });

      // условные поля: «Завершил обучение» -> блок опыта работы
      var eduToggles = form.querySelectorAll('[data-edu-toggle]');
      var expBlocks = form.querySelectorAll('[data-exp-fields]');
      var expWrap = form.querySelector('[data-experience-fields]');
      eduToggles.forEach(function (t) {
        t.addEventListener('change', function () {
          var finished = t.value === 'finished' && t.checked;
          if (expWrap) expWrap.hidden = !finished;
          expBlocks.forEach(function (b) { b.hidden = !finished; });
        });
      });

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var valid = true;
        fields.forEach(function (field) {
          if (!validateField(field)) valid = false;
        });
        if (!valid) {
          var firstError = form.querySelector('.field--error input, .field--error select, .field--error textarea');
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

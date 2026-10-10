(function () {
  'use strict';

  function plural(n, one, few, many) {
    var m10 = n % 10, m100 = n % 100;
    if (m10 === 1 && m100 !== 11) return one;
    if (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) return few;
    return many;
  }

  function eq(a, b) {
    return (a || '').toLowerCase() === (b || '').toLowerCase();
  }

  document.addEventListener('DOMContentLoaded', function () {
    /* ------------------------------------------------ вакансии: фильтры, поиск, сортировка */
    var list = document.querySelector('.vac-rows');
    if (list) {
      var rows = function () { return [].slice.call(list.querySelectorAll('.vac-row')); };
      var search = document.querySelector('.vac-find__input');
      var count = document.querySelector('.page-head__note');
      var picked = { region: null, city: null };

      document.querySelectorAll('.vac-side__picked').forEach(function (p) {
        var key = p.parentElement.querySelector('.vac-side__label').textContent.trim().toLowerCase() === 'регион' ? 'region' : 'city';
        picked[key] = p;
      });

      function apply() {
        var q = search ? search.value.trim().toLowerCase() : '';
        var f = { region: '', city: '', direction: '', segment: '', company: '', position: '', exp: '' };
        var sort = 'date';
        document.querySelectorAll('.vac-side [name]').forEach(function (el) {
          if (el.type === 'radio') {
            if (el.checked) f[el.name] = el.value;
          } else if (el.name === 'accessible') {
            if (el.checked) f.accessible = true;
          } else if (el.tagName === 'SELECT') {
            var v = el.value;
            if (el.name === 'sort') {
              sort = v === 'По зарплате' ? 'salary' : 'date';
            } else if (v && v.indexOf('Все ') !== 0) {
              // селект направлений в сайдбаре фильтрует data-spec (специализация вакансии)
              f[el.name === 'direction' ? 'spec' : el.name] = v;
            }
          }
        });

        var visible = rows().filter(function (row) {
          var d = row.dataset;
          if (q && row.textContent.toLowerCase().indexOf(q) === -1) return false;
          var keys = ['region', 'city', 'direction', 'segment', 'company', 'position', 'exp'];
          for (var i = 0; i < keys.length; i++) {
            if (f[keys[i]] && !eq(d[keys[i]], f[keys[i]])) return false;
          }
          if (f.accessible && d.accessible !== '1') return false;
          return true;
        });

        rows().forEach(function (row) { row.hidden = visible.indexOf(row) === -1; });
        visible.slice().sort(function (a, b) {
          if (sort === 'salary') return (+b.dataset.salary || 0) - (+a.dataset.salary || 0);
          return (a.dataset.date || '') < (b.dataset.date || '') ? 1 : -1;
        }).forEach(function (row) { list.appendChild(row); });

        if (count) {
          var n = visible.length;
          count.textContent = 'На сайте ' + n + ' ' + plural(n, 'вакансия', 'вакансии', 'вакансий');
        }
      }

      if (search) search.addEventListener('input', apply);
      document.querySelectorAll('.vac-side [name]').forEach(function (el) {
        el.addEventListener('change', apply);
      });
      document.querySelectorAll('.vac-side__picked .vac-side__x').forEach(function (x) {
        x.addEventListener('click', function () {
          x.closest('.vac-side__group').hidden = true;
          apply();
        });
      });
      var reset = document.querySelector('.vac-side__reset');
      if (reset) {
        reset.addEventListener('click', function () {
          if (search) search.value = '';
          document.querySelectorAll('.vac-side [name]').forEach(function (el) {
            if (el.type === 'radio' || el.type === 'checkbox') el.checked = false;
            else if (el.tagName === 'SELECT') {
              el.selectedIndex = 0;
              // подпись кастомного дропдауна обновляется только по событию change
              el.dispatchEvent(new Event('change', { bubbles: true }));
            }
          });
          Object.keys(picked).forEach(function (k) { if (picked[k]) picked[k].closest('.vac-side__group').hidden = true; });
          apply();
        });
      }
    }

    /* ---------------------------------------- практики/стажировки: табы, чипы, город */
    var tabs = document.querySelectorAll('.tabs-pill__tab[data-tab]');
    if (!tabs.length) return;

    var WORDS = {
      practice: { gen: 'практики', acc: 'практику', who: 'практикантами' },
      internship: { gen: 'стажировки', acc: 'стажировку', who: 'стажёрами' }
    };
    var sets = document.querySelectorAll('.dir-set');
    var active = 'practice';
    sets.forEach(function (set) { if (!set.hidden) active = set.dataset.set; });

    var dirFilter = '';
    var citySelect = document.querySelector('[data-filter-select="city"]');

    // высота зоны карточек фиксируется по самому высокому виденному набору,
    // чтобы переключение табов не сдвигало контент ниже
    var setBaseH = 0;
    function render() {
      sets.forEach(function (set) {
        set.hidden = set.dataset.set !== active;
        set.querySelectorAll('.dir-card').forEach(function (card) {
          var okDir = !dirFilter || eq(card.dataset.direction, dirFilter);
          var okCity = !citySelect || !citySelect.value || eq(card.dataset.city, citySelect.value);
          card.hidden = !(okDir && okCity);
        });
      });
      var visibleSet = sets[active === 'practice' ? 0 : 1] || document.querySelector('.dir-set[data-set="' + active + '"]');
      if (visibleSet) {
        var h = visibleSet.getBoundingClientRect().height;
        if (h > setBaseH) {
          setBaseH = Math.ceil(h);
          sets.forEach(function (s2) { s2.style.minHeight = setBaseH + 'px'; });
        }
      }
      var words = WORDS[active];
      document.querySelectorAll('[data-word]').forEach(function (el) {
        el.textContent = words[el.dataset.word];
      });
    }

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        active = tab.dataset.tab;
        tabs.forEach(function (t) {
          t.classList.toggle('is-active', t === tab);
          t.setAttribute('aria-selected', t === tab ? 'true' : 'false');
        });
        render();
      });
    });

    document.querySelectorAll('[data-filter-group] .chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        dirFilter = chip.dataset.filterValue;
        chip.parentElement.querySelectorAll('.chip').forEach(function (c) {
          c.classList.toggle('is-active', c === chip);
        });
        render();
      });
    });

    if (citySelect) citySelect.addEventListener('change', render);

    render();
  });
})();

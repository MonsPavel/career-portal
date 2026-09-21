(function () {
  'use strict';

  function closeAll(except) {
    document.querySelectorAll('.dd.is-open').forEach(function (dd) {
      if (dd === except) return;
      dd.classList.remove('is-open');
      var list = dd.querySelector('.dd__list');
      if (list) list.hidden = true;
      var btn = dd.querySelector('.dd__trigger');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  }

  document.addEventListener('click', function () { closeAll(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAll();
  });

  function build(select) {
    try {
    if (select.dataset.customDd) return;
    select.dataset.customDd = '1';

    var inWrap = select.parentElement.classList.contains('vacancy-search__select-wrap');
    var isField = select.classList.contains('field__select');

    var dd = document.createElement('div');
    dd.className = 'dd' + (inWrap ? ' dd--in-wrap' : '');

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'dd__trigger' + (isField ? ' dd__trigger--field' : '');
    btn.setAttribute('aria-haspopup', 'listbox');
    btn.setAttribute('aria-expanded', 'false');
    var label = document.createElement('span');
    label.className = 'dd__label';
    var chev = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    chev.setAttribute('class', 'dd__chevron');
    chev.setAttribute('width', '16');
    chev.setAttribute('height', '16');
    chev.setAttribute('viewBox', '0 0 16 16');
    chev.setAttribute('fill', 'none');
    chev.setAttribute('aria-hidden', 'true');
    var chevPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    chevPath.setAttribute('d', 'M3 6l5 4 5-4');
    chevPath.setAttribute('stroke', 'currentColor');
    chevPath.setAttribute('stroke-width', '2');
    chevPath.setAttribute('stroke-linecap', 'round');
    chevPath.setAttribute('stroke-linejoin', 'round');
    chev.appendChild(chevPath);
    btn.appendChild(label);
    btn.appendChild(chev);

    var list = document.createElement('div');
    list.className = 'dd__list';
    list.hidden = true;
    list.setAttribute('role', 'listbox');

    var optionButtons = [];

    function updateLabel() {
      var o = select.options[select.selectedIndex];
      var isPlaceholder = !o || o.value === '';
      label.textContent = o ? o.text : '';
      btn.classList.toggle('is-placeholder', isPlaceholder);
      optionButtons.forEach(function (ob, i) {
        var selected = select.options[i] && select.options[i].selected && select.options[i].value !== '';
        ob.classList.toggle('is-selected', selected);
      });
    }

    function close() {
      dd.classList.remove('is-open');
      list.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }

    function open() {
      closeAll(dd);
      dd.classList.add('is-open');
      list.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      var selBtn = optionButtons[select.selectedIndex];
      if (selBtn) selBtn.focus();
    }

    [...select.options].forEach(function (o, i) {
      var ob = document.createElement('button');
      ob.type = 'button';
      ob.className = 'dd__option';
      ob.setAttribute('role', 'option');
      ob.textContent = o.text;
      if (o.value === '') ob.classList.add('dd__option--reset');
      ob.addEventListener('click', function () {
        select.selectedIndex = i;
        updateLabel();
        close();
        btn.focus();
        select.dispatchEvent(new Event('change', { bubbles: true }));
      });
      ob.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown' && optionButtons[i + 1]) { e.preventDefault(); optionButtons[i + 1].focus(); }
        if (e.key === 'ArrowUp' && optionButtons[i - 1]) { e.preventDefault(); optionButtons[i - 1].focus(); }
      });
      list.appendChild(ob);
      optionButtons.push(ob);
    });

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (dd.classList.contains('is-open')) { close(); return; }
      closeAll(dd);
      open();
    });

    btn.addEventListener('keydown', function (e) {
      if (!dd.classList.contains('is-open')) return;
      var i = optionButtons.indexOf(document.activeElement);
      if (e.key === 'ArrowDown' && optionButtons[i + 1]) { e.preventDefault(); optionButtons[i + 1].focus(); }
      if (e.key === 'ArrowUp' && optionButtons[i - 1]) { e.preventDefault(); optionButtons[i - 1].focus(); }
    });

    select.addEventListener('change', function () { updateLabel(); });

    select.classList.add('custom-select-hidden');
    updateLabel();

    dd.appendChild(btn);
    dd.appendChild(list);

    if (inWrap) {
      // фильтровые селекты живут в готовой «пилюле» — триггер растягивается на неё
      dd.classList.add('dd--in-wrap');
      select.parentElement.appendChild(dd);
    } else {
      select.parentNode.insertBefore(dd, select);
      dd.appendChild(select);
    }

    dd.addEventListener('click', function (e) { e.stopPropagation(); });
    } catch (err) {
      console.error('dropdown build failed for', select.name || select.id || select, err);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('select').forEach(build);
  });
})();

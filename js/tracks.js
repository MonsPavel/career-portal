(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.querySelector('[data-tracks]');
    if (!root) return;
    var data = window.__TRACKS_DATA__;
    if (!data) return;

    var tabButtons = root.querySelectorAll('[data-track-tab]');
    var trackList = root.querySelector('[data-track-list]');
    var trackName = root.querySelector('[data-track-name]');
    var stepsBar = root.querySelector('[data-steps]');
    var info = root.querySelector('[data-step-info]');
    var tabIndex = 0;
    var trackIndex = 0;
    var stepIndex = 0;

    function renderChips() {
      if (trackName) trackName.textContent = data.tabs[tabIndex].tracks[trackIndex].name;
      var tracks = data.tabs[tabIndex].tracks;
      if (tracks.length < 2) {
        trackList.hidden = true;
        trackList.innerHTML = '';
        return;
      }
      trackList.hidden = false;
      trackList.innerHTML = tracks.map(function (t, i) {
        return '<button class="track-chip' + (i === trackIndex ? ' is-active' : '') +
          '" type="button" data-track-index="' + i + '">' + t.name + '</button>';
      }).join('');
    }

    function renderSteps() {
      var track = data.tabs[tabIndex].tracks[trackIndex];
      stepsBar.innerHTML = track.steps.map(function (s, i) {
        return '<button class="step-pill' + (i === stepIndex ? ' is-active' : '') +
          (i < stepIndex ? ' is-done' : '') + '" type="button" data-step="' + i + '">' +
          '<span class="step-pill__dot"></span><span class="step-pill__name">' + s.name +
          '</span><span class="step-pill__duration">' + s.duration + '</span></button>';
      }).join('');
    }

    function renderInfo() {
      var s = data.tabs[tabIndex].tracks[trackIndex].steps[stepIndex];
      info.innerHTML =
        '<div class="step-info__row"><span class="step-info__label">Должность</span>' +
        '<span class="step-info__value">' + s.position + '</span></div>' +
        '<div class="step-info__row"><span class="step-info__label">Задачи</span>' +
        '<span class="step-info__value">' + s.desc + '</span></div>' +
        '<div class="step-info__row"><span class="step-info__label">Образование</span>' +
        '<span class="step-info__value">' + s.education + '</span></div>' +
        '<div class="step-info__row"><span class="step-info__label">Повышение квалификации</span>' +
        '<span class="step-info__value">' + s.growth + '</span></div>' +
        '<div class="step-info__row"><span class="step-info__label">Соцпакет</span>' +
        '<span class="step-info__value">' + s.benefits + '</span></div>';
    }

    function renderAll() {
      renderChips();
      renderSteps();
      renderInfo();
    }

    tabButtons.forEach(function (btn, i) {
      btn.addEventListener('click', function () {
        if (tabIndex === i) return;
        tabIndex = i;
        trackIndex = 0;
        stepIndex = 0;
        tabButtons.forEach(function (b) { b.classList.toggle('is-active', b === btn); });
        renderAll();
      });
    });

    if (trackList) {
      trackList.addEventListener('click', function (e) {
        var t = e.target.closest('[data-track-index]');
        if (!t) return;
        trackIndex = parseInt(t.getAttribute('data-track-index'), 10) || 0;
        stepIndex = 0;
        renderChips();
        renderSteps();
        renderInfo();
      });
    }

    if (stepsBar) {
      stepsBar.addEventListener('click', function (e) {
        var t = e.target.closest('[data-step]');
        if (!t) return;
        stepIndex = parseInt(t.getAttribute('data-step'), 10) || 0;
        renderSteps();
        renderInfo();
      });
    }

    renderAll();

    // Тест на профориентацию: интро → вопросы с баллами → результат с переходами
    var testBlock = document.querySelector('[data-career-test]');
    if (testBlock && data.test) {
      var intro = testBlock.querySelector('[data-test-intro]');
      var quiz = testBlock.querySelector('[data-test-quiz]');
      var result = testBlock.querySelector('[data-test-result]');
      var progressEl = testBlock.querySelector('[data-test-progress]');
      var imageEl = testBlock.querySelector('[data-test-image]');
      var qEl = testBlock.querySelector('[data-test-question]');
      var optsEl = testBlock.querySelector('[data-test-options]');

      // интро из данных
      testBlock.querySelector('[data-test-intro-title]').textContent = data.test.intro.title;
      testBlock.querySelector('[data-test-intro-text]').textContent = data.test.intro.text;
      testBlock.querySelector('[data-test-start]').textContent = data.test.intro.button;
      testBlock.querySelector('.test__intro-photo').src = data.test.intro.image;

      var qIndex = 0;
      var scores = {};
      var directions = data.test.directions;

      function renderQuestion() {
        var q = data.test.questions[qIndex];
        progressEl.textContent = 'Вопрос ' + (qIndex + 1) + ' из ' + data.test.questions.length;
        qEl.textContent = q.q;
        if (q.image) { imageEl.src = q.image; imageEl.hidden = false; }
        else { imageEl.hidden = true; }
        optsEl.innerHTML = q.options.map(function (o, i) {
          var text = typeof o === 'string' ? o : o.text;
          return '<button class="btn btn--light test-option" type="button" data-option="' + i + '">' + text + '</button>';
        }).join('');
      }

      function renderResult() {
        var top = null;
        Object.keys(scores).forEach(function (k) {
          if (!top || scores[k] > scores[top]) top = k;
        });
        var dir = directions[top];
        if (!dir) { dir = directions[Object.keys(directions)[0]]; }
        testBlock.querySelector('[data-result-image]').src = dir.image;
        testBlock.querySelector('[data-result-title]').textContent = 'Ваше направление: ' + dir.title;
        testBlock.querySelector('[data-result-text]').textContent = dir.text;
        var links = testBlock.querySelector('[data-result-links]');
        links.innerHTML = '';
        [['education.html', 'целевое обучение'], ['internships.html', 'стажировки'],
         ['practices.html', 'практики'], ['vacancies.html', 'вакансии'],
         ['events.html', 'мероприятия']].forEach(function (pair) {
          var a = document.createElement('a');
          a.className = 'btn btn--light';
          a.href = pair[0];
          a.textContent = pair[1];
          links.appendChild(a);
        });
        intro.hidden = true;
        quiz.hidden = true;
        result.hidden = false;
        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }

      optsEl.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-option]');
        if (!btn) return;
        var q = data.test.questions[qIndex];
        var opt = q.options[parseInt(btn.getAttribute('data-option'), 10)];
        if (opt.points) {
          Object.keys(opt.points).forEach(function (k) {
            scores[k] = (scores[k] || 0) + opt.points[k];
          });
        }
        qIndex += 1;
        if (qIndex >= data.test.questions.length) { renderResult(); return; }
        renderQuestion();
      });

      testBlock.querySelector('[data-test-start]').addEventListener('click', function () {
        qIndex = 0;
        scores = {};
        intro.hidden = true;
        result.hidden = true;
        quiz.hidden = false;
        renderQuestion();
      });

      testBlock.querySelector('[data-test-restart]').addEventListener('click', function () {
        result.hidden = true;
        quiz.hidden = true;
        intro.hidden = false;
        intro.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
    }
  });
})();

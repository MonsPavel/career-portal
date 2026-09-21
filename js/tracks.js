(function () {
  'use strict';

  var TRACKS = {
    colledge: null,
    univ: null
  };

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.querySelector('[data-tracks]');
    if (!root) return;

    var data = window.__TRACKS_DATA__;
    if (!data) return;

    var tabButtons = root.querySelectorAll('[data-track-tab]');
    var trackList = root.querySelector('[data-track-list]');
    var trackName = root.querySelector('[data-track-name]');
    var trackImage = root.querySelector('[data-track-image]');
    var stepsBar = root.querySelector('[data-steps]');
    var info = root.querySelector('[data-step-info]');
    var tabIndex = 0;
    var trackIndex = 0;
    var stepIndex = 0;

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
        '<div class="step-info__row"><span class="step-info__label">Развитие</span>' +
        '<span class="step-info__value">' + s.growth + '</span></div>' +
        '<div class="step-info__row"><span class="step-info__label">Соцпакет</span>' +
        '<span class="step-info__value">' + s.benefits + '</span></div>';
    }

    function renderTrack() {
      var track = data.tabs[tabIndex].tracks[trackIndex];
      trackName.textContent = track.name;
      if (trackImage) trackImage.src = track.image;
      stepIndex = 0;
      renderSteps();
      renderInfo();
    }

    tabButtons.forEach(function (btn, i) {
      btn.addEventListener('click', function () {
        tabIndex = i;
        trackIndex = 0;
        tabButtons.forEach(function (b) { b.classList.toggle('is-active', b === btn); });
        renderTrack();
      });
    });

    if (trackList) {
      trackList.addEventListener('click', function (e) {
        var t = e.target.closest('[data-track-index]');
        if (!t) return;
        trackIndex = parseInt(t.getAttribute('data-track-index'), 10) || 0;
        renderTrack();
      });
      trackList.innerHTML = data.tabs[0].tracks.map(function (t, i) {
        return '<button class="track-chip' + (i === 0 ? ' is-active' : '') +
          '" type="button" data-track-index="' + i + '">' + t.name + '</button>';
      }).join('');
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

    renderTrack();

    // Тест профориентации (мок)
    var testBlock = document.querySelector('[data-career-test]');
    if (testBlock && data.test) {
      var qIndex = 0;
      var answers = [];
      var qEl = testBlock.querySelector('[data-test-question]');
      var optsEl = testBlock.querySelector('[data-test-options]');
      var progressEl = testBlock.querySelector('[data-test-progress]');
      var resultEl = testBlock.querySelector('[data-test-result]');

      function renderQuestion() {
        var q = data.test.questions[qIndex];
        progressEl.textContent = 'Вопрос ' + (qIndex + 1) + ' из ' + data.test.questions.length;
        qEl.textContent = q.q;
        optsEl.innerHTML = q.options.map(function (o, i) {
          return '<button class="btn btn--light" type="button" data-option="' + i + '">' + o + '</button>';
        }).join('');
      }

      optsEl.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-option]');
        if (!btn) return;
        answers.push(parseInt(btn.getAttribute('data-option'), 10));
        qIndex += 1;
        if (qIndex >= data.test.questions.length) {
          testBlock.querySelector('[data-test-quiz]').hidden = true;
          resultEl.hidden = false;
          resultEl.querySelector('[data-test-directions]').innerHTML =
            data.test.result.directions.map(function (d) {
              return '<span class="tag tag--blue">' + d + '</span>';
            }).join('');
          resultEl.querySelector('[data-test-text]').textContent = data.test.result.text;
          return;
        }
        renderQuestion();
      });

      renderQuestion();
    }
  });
})();

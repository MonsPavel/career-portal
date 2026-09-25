(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var section = document.querySelector('.directions');
    if (!section) return;

    var modal = section.querySelector('[data-directions-modal]');
    var data = [];
    try {
      data = JSON.parse(section.querySelector('[data-directions-data]').textContent);
    } catch (e) { return; }

    var title = modal.querySelector('[data-directions-title]');
    var subtitle = modal.querySelector('[data-directions-subtitle]');
    var text = modal.querySelector('[data-directions-text]');
    var photo = modal.querySelector('[data-directions-photo]');
    var panel = modal.querySelector('.directions__modal-panel');
    var closeButton = modal.querySelector('.directions__modal-close');
    var currentDirection = 0;
    var currentPhoto = 0;
    var closeTimer = null;
    var lastFocused = null;

    function getPhotos(direction) {
      if (Array.isArray(direction.photos) && direction.photos.length) {
        return direction.photos;
      }
      return direction.photo ? [direction.photo] : [];
    }

    function renderPhoto(i) {
      var photos = getPhotos(data[currentDirection]);
      if (!photos.length) return;
      currentPhoto = (i + photos.length) % photos.length;
      photo.src = photos[currentPhoto];
    }

    function renderDirection(i) {
      var d = data[i];
      if (!d) return;
      currentDirection = i;
      currentPhoto = 0;
      title.textContent = d.title;
      subtitle.textContent = d.subtitle;
      text.textContent = d.text;
      renderPhoto(currentPhoto);
    }

    function open(i) {
      window.clearTimeout(closeTimer);
      renderDirection(i);
      lastFocused = document.activeElement;
      document.body.classList.add('directions-modal-open');
      modal.hidden = false;
      modal.setAttribute('aria-hidden', 'false');
      modal.classList.remove('is-open');
      void modal.offsetWidth;
      modal.classList.add('is-open');
      closeButton.focus({ preventScroll: true });
    }

    function finishClose() {
      window.clearTimeout(closeTimer);
      modal.hidden = true;
      modal.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('directions-modal-open');
      if (lastFocused && typeof lastFocused.focus === 'function') {
        lastFocused.focus({ preventScroll: true });
      }
    }

    function close() {
      if (modal.hidden) return;
      modal.classList.remove('is-open');
      closeTimer = window.setTimeout(finishClose, 400);
    }

    panel.addEventListener('transitionend', function (event) {
      if (event.propertyName === 'transform' && !modal.classList.contains('is-open')) {
        finishClose();
      }
    });

    section.querySelectorAll('[data-direction]').forEach(function (card) {
      card.addEventListener('click', function () {
        open(parseInt(card.getAttribute('data-direction'), 10) || 0);
      });
    });

    modal.querySelectorAll('[data-directions-close]').forEach(function (el) {
      el.addEventListener('click', close);
    });

    modal.querySelector('[data-directions-prev]').addEventListener('click', function () {
      renderPhoto(currentPhoto - 1);
    });
    modal.querySelector('[data-directions-next]').addEventListener('click', function () {
      renderPhoto(currentPhoto + 1);
    });

    document.addEventListener('keydown', function (e) {
      if (modal.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') modal.querySelector('[data-directions-prev]').click();
      if (e.key === 'ArrowRight') modal.querySelector('[data-directions-next]').click();
    });
  });
})();

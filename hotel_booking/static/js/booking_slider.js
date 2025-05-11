document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.slider-container').forEach(container => {
    const track = container.querySelector('.slider-track');
    const slides = Array.from(track.children);
    const total = slides.length;
    let idx = 0;

    track.style.width = `${total * 100}%`;
    slides.forEach(slide => {
      slide.style.width = `${100 / total}%`;
    });

    const prev = container.querySelector('.slider-nav.prev');
    const next = container.querySelector('.slider-nav.next');
    if (!prev || !next) return;

    function goTo(i) {
      idx = (i + total) % total;
      track.style.transform = `translateX(-${idx * (100 / total)}%)`;
    }

    prev.addEventListener('click', () => goTo(idx - 1));
    next.addEventListener('click', () => goTo(idx + 1));
  });
});

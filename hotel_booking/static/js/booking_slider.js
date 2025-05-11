document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.slider-container').forEach(container => {
    const track = container.querySelector('.slider-track');
    const slides = Array.from(track.children);
    const total = slides.length;
    let idx = 0;

    // Задаём track и слайдам относительные размеры
    track.style.width = `${total * 100}%`;
    slides.forEach(slide => {
      slide.style.width = `${100 / total}%`;
    });

    // Навигационные кнопки
    const prev = container.querySelector('.slider-nav.prev');
    const next = container.querySelector('.slider-nav.next');
    if (!prev || !next) return;

    function goTo(i) {
      idx = (i + total) % total;
      // смещаем на ширину одного слайда * номер
      track.style.transform = `translateX(-${idx * (100 / total)}%)`;
    }

    prev.addEventListener('click', () => goTo(idx - 1));
    next.addEventListener('click', () => goTo(idx + 1));
  });
});

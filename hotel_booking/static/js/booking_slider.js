document.addEventListener('DOMContentLoaded', () => {
  // Инициализация слайдера во всех контейнерах
  document.querySelectorAll('.slider-container').forEach(container => {
    const track = container.querySelector('.slider-track');
    const slides = Array.from(track.children);
    let idx = 0;

    function update() {
      track.style.transform = `translateX(-${idx * 100}%)`;
    }

    container.querySelector('.next').addEventListener('click', () => {
      idx = (idx + 1) % slides.length;
      update();
    });

    container.querySelector('.prev').addEventListener('click', () => {
      idx = (idx - 1 + slides.length) % slides.length;
      update();
    });

    // Подгоняем ширину track под количество слайдов
    track.style.width = `${slides.length * 100}%`;
    slides.forEach(img => {
      img.style.width = `${100 / slides.length}%`;
    });
  });
});

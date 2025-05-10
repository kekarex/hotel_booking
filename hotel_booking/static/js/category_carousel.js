document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.category-carousel').forEach(carousel => {
    const slidesEl = carousel.querySelector('.slides');
    const count = slidesEl.children.length;
    let idx = 0;

    function update() {
      slidesEl.style.transform = `translateX(-${idx * 100}%)`;
    }

    carousel.querySelector('.prev').addEventListener('click', () => {
      idx = (idx - 1 + count) % count;
      update();
    });
    carousel.querySelector('.next').addEventListener('click', () => {
      idx = (idx + 1) % count;
      update();
    });
  });
});

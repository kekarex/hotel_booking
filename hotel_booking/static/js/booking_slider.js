document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelector('.slides');
  const slideCount = document.querySelectorAll('.slide').length;
  let currentIndex = 0;

  document.querySelector('.next').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % slideCount;
    slides.style.transform = `translateX(-${currentIndex * 100}%)`;
  });

  document.querySelector('.prev').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + slideCount) % slideCount;
    slides.style.transform = `translateX(-${currentIndex * 100}%)`;
  });
});
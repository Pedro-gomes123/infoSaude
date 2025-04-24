const inner = document.querySelector('.carousel-inner');
const indicators = document.querySelectorAll('.carousel-indicators button');
let index = 0;

function showSlide(i) {
  const total = indicators.length;
  if (i < 0) i = total - 1;
  if (i >= total) i = 0;
  inner.style.transform = `translateX(-${i * 100}%)`;
  indicators.forEach(btn => btn.classList.remove('active'));
  indicators[i].classList.add('active');
  index = i;
}

document.getElementById('prev').addEventListener('click', () => {
  showSlide(index - 1);
});

document.getElementById('next').addEventListener('click', () => {
  showSlide(index + 1);
});

indicators.forEach(btn => {
  btn.addEventListener('click', (e) => {
    showSlide(parseInt(e.target.dataset.slide));
  });
});

const search = document.querySelector('#search');
const category = document.querySelector('#category');
const cards = [...document.querySelectorAll('[data-mod]')];
function filterMods() {
  const query = search.value.trim().toLowerCase();
  let count = 0;
  for (const card of cards) {
    const visible = card.textContent.toLowerCase().includes(query) && (!category.value || card.dataset.category === category.value);
    card.hidden = !visible;
    if (visible) count++;
  }
  document.querySelector('#count').textContent = `${count} of ${cards.length} mods shown`;
  document.querySelector('#empty').hidden = count !== 0;
}
search.addEventListener('input', filterMods);
category.addEventListener('change', filterMods);
filterMods();

(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#navigation');
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    nav.classList.toggle('open', open);
  });
  nav?.addEventListener('click', e => {
    if (e.target.closest('a')) {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('open');
    }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && nav?.classList.contains('open')) {
      nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus();
    }
  });
  const search = document.querySelector('#article-search');
  if (!search) return;
  const cards = [...document.querySelectorAll('[data-article]')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  let topic = 'All';
  const params = new URLSearchParams(location.search);
  search.value = params.get('q') || '';
  const requested = params.get('topic');
  if (buttons.some(b => b.dataset.filter === requested)) topic = requested;
  const filter = () => {
    const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach(card => {
      const visible = (topic === 'All' || card.dataset.topic === topic) && words.every(w => card.dataset.search.includes(w));
      card.hidden = !visible;
      if (visible) count++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === topic)));
    document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'article' : 'articles'}`;
    document.querySelector('#no-results').hidden = count !== 0;
    if (location.protocol !== 'file:') {
      const url = new URL(location.href);
      if (search.value) url.searchParams.set('q', search.value); else url.searchParams.delete('q');
      if (topic !== 'All') url.searchParams.set('topic', topic); else url.searchParams.delete('topic');
      history.replaceState(null, '', url);
    }
  };
  search.addEventListener('input', filter);
  buttons.forEach(button => button.addEventListener('click', () => {topic = button.dataset.filter; filter();}));
  document.querySelector('#clear-search').addEventListener('click', () => {search.value = ''; topic = 'All'; filter(); search.focus();});
  filter();
})();

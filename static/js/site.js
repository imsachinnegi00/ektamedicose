(() => {
  const rotatingWord = document.querySelector('.rotating-word');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (rotatingWord && !reducedMotion) {
    const phrases = ['locally.', 'with trust.', 'together.'];
    let phraseIndex = 0;
    window.setInterval(() => {
      rotatingWord.classList.add('is-changing');
      window.setTimeout(() => {
        phraseIndex = (phraseIndex + 1) % phrases.length;
        rotatingWord.textContent = phrases[phraseIndex];
        rotatingWord.classList.remove('is-changing');
      }, 240);
    }, 3400);
  }

  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.primary-nav');
  if (menuButton && navigation) {
    menuButton.addEventListener('click', () => {
      const open = navigation.classList.toggle('open');
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    });
    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) {
        navigation.classList.remove('open');
        menuButton.setAttribute('aria-expanded', 'false');
      }
    });
  }

  const cards = [...document.querySelectorAll('.portfolio-card')];
  const chips = [...document.querySelectorAll('.filter-chip')];
  const search = document.querySelector('#company-search');
  const emptyState = document.querySelector('.empty-state');
  let activeFilter = 'all';
  const filterCards = () => {
    const query = search ? search.value.trim().toLowerCase() : '';
    let visible = 0;
    cards.forEach((card) => {
      const matchesCategory = activeFilter === 'all' || card.dataset.category === activeFilter;
      const matchesQuery = (card.dataset.search || '').includes(query);
      card.hidden = !(matchesCategory && matchesQuery);
      if (!card.hidden) visible += 1;
    });
    if (emptyState) emptyState.hidden = visible > 0;
  };
  chips.forEach((chip) => chip.addEventListener('click', () => {
    activeFilter = chip.dataset.filter;
    chips.forEach((item) => item.classList.toggle('active', item === chip));
    filterCards();
  }));
  if (search) search.addEventListener('input', filterCards);
  const requestedCategory = new URLSearchParams(location.search).get('category');
  if (requestedCategory && search) {
    search.value = requestedCategory;
    filterCards();
  }

  const revealItems = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reducedMotion) {
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          currentObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  }
})();

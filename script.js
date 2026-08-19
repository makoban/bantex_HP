const header = document.querySelector('[data-header]');
const progress = document.querySelector('[data-progress]');
const menuButton = document.querySelector('.menu-button');
const mobileMenu = document.querySelector('#mobile-menu');
const video = document.querySelector('.hero-video');
const soundToggle = document.querySelector('.sound-toggle');
const soundLabel = document.querySelector('[data-sound-label]');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const desktopMotion = window.matchMedia('(min-width: 768px)');

const updateScroll = () => {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const amount = scrollable > 0 ? window.scrollY / scrollable : 0;
  progress.style.transform = `scaleX(${Math.min(1, Math.max(0, amount))})`;
  header.classList.toggle('is-scrolled', window.scrollY > 24);
};

window.addEventListener('scroll', updateScroll, { passive: true });
updateScroll();

const closeMenu = () => {
  menuButton.setAttribute('aria-expanded', 'false');
  mobileMenu.hidden = true;
  document.body.classList.remove('menu-open');
};

menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!open));
  mobileMenu.hidden = open;
  document.body.classList.toggle('menu-open', !open);
  if (!open) mobileMenu.querySelector('a').focus();
});

mobileMenu.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !mobileMenu.hidden) {
    closeMenu();
    menuButton.focus();
  }
});

soundToggle.addEventListener('click', async () => {
  video.muted = !video.muted;
  soundToggle.setAttribute('aria-pressed', String(!video.muted));
  soundToggle.setAttribute('aria-label', video.muted ? 'ブランドムービーの音声をオンにする' : 'ブランドムービーの音声をオフにする');
  soundLabel.textContent = video.muted ? 'SOUND OFF' : 'SOUND ON';
  if (video.paused && !reduceMotion.matches) await video.play().catch(() => {});
});

const tabs = [...document.querySelectorAll('[role="tab"]')];
const panels = [...document.querySelectorAll('[role="tabpanel"]')];

const activateTab = (tab, focus = false) => {
  tabs.forEach((item) => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
  });
  panels.forEach((panel) => { panel.hidden = panel.dataset.panel !== tab.dataset.tab; });
  if (focus) tab.focus();
};

tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => activateTab(tab));
  tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let next = index;
    if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + tabs.length) % tabs.length;
    else next = (index + 1) % tabs.length;
    activateTab(tabs[next], true);
  });
});
activateTab(tabs[0]);

document.querySelectorAll('.media-frame img').forEach((image) => {
  image.addEventListener('error', () => {
    image.hidden = true;
    image.parentElement.classList.add('media-pending');
  });
});

if ('IntersectionObserver' in window && !reduceMotion.matches) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.16 });
  document.querySelectorAll('[data-field], .service-stage, .library-card, .work-card, .support-links a').forEach((item) => observer.observe(item));
}

const handleMotionPreference = () => {
  const selectedSrc = desktopMotion.matches ? video.dataset.desktopSrc : video.dataset.mobileSrc;
  const selectedPoster = desktopMotion.matches ? video.dataset.desktopPoster : video.dataset.mobilePoster;
  const currentSrc = video.getAttribute('src');

  if (selectedPoster && video.getAttribute('poster') !== selectedPoster) {
    video.setAttribute('poster', selectedPoster);
  }

  if (reduceMotion.matches) {
    video.pause();
    video.removeAttribute('autoplay');
    if (currentSrc) {
      video.removeAttribute('src');
      video.load();
    }
    video.muted = true;
    soundToggle.setAttribute('aria-pressed', 'false');
    soundLabel.textContent = 'SOUND OFF';
    return;
  }

  video.setAttribute('autoplay', '');
  if (currentSrc !== selectedSrc) {
    video.pause();
    video.muted = true;
    soundToggle.setAttribute('aria-pressed', 'false');
    soundLabel.textContent = 'SOUND OFF';
    video.src = selectedSrc;
    video.load();
  }
  video.play().catch(() => {});
};
reduceMotion.addEventListener?.('change', handleMotionPreference);
desktopMotion.addEventListener?.('change', handleMotionPreference);
handleMotionPreference();

const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
const pointerGlow = document.querySelector('.pointer-glow');
const interactiveSurfaces = [...document.querySelectorAll('.interactive-surface')];

if (finePointer.matches && !reduceMotion.matches) {
  document.body.classList.add('has-pointer-motion');
  window.addEventListener('pointermove', (event) => {
    document.documentElement.style.setProperty('--pointer-x', `${event.clientX}px`);
    document.documentElement.style.setProperty('--pointer-y', `${event.clientY}px`);
  }, { passive: true });

  interactiveSurfaces.forEach((surface) => {
    surface.addEventListener('pointermove', (event) => {
      const rect = surface.getBoundingClientRect();
      surface.style.setProperty('--spot-x', `${event.clientX - rect.left}px`);
      surface.style.setProperty('--spot-y', `${event.clientY - rect.top}px`);
    }, { passive: true });
  });

  document.querySelectorAll('[data-magnetic]').forEach((item) => {
    item.addEventListener('pointermove', (event) => {
      const rect = item.getBoundingClientRect();
      const x = (event.clientX - rect.left - rect.width / 2) * .12;
      const y = (event.clientY - rect.top - rect.height / 2) * .12;
      item.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    });
    item.addEventListener('pointerleave', () => { item.style.transform = ''; });
  });

  document.querySelectorAll('[data-tilt]').forEach((item) => {
    item.addEventListener('pointermove', (event) => {
      const rect = item.getBoundingClientRect();
      const rotateY = ((event.clientX - rect.left) / rect.width - .5) * 4;
      const rotateX = ((event.clientY - rect.top) / rect.height - .5) * -4;
      item.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });
    item.addEventListener('pointerleave', () => { item.style.transform = ''; });
  });
} else {
  pointerGlow?.remove();
}

const filterButtons = [...document.querySelectorAll('[data-filter]')];
const serviceCards = [...document.querySelectorAll('.library-card')];
const serviceCount = document.querySelector('[data-service-count]');

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    filterButtons.forEach((item) => {
      const active = item === button;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    let visible = 0;
    serviceCards.forEach((card) => {
      const categories = card.dataset.category.split(' ');
      const show = filter === 'all' || categories.includes(filter);
      card.hidden = !show;
      if (show) visible += 1;
    });
    serviceCount.textContent = String(visible).padStart(2, '0');
  });
});

const libraryGrid = document.querySelector('[data-service-grid]');
const libraryMore = document.querySelector('[data-library-more]');
libraryMore?.addEventListener('click', () => {
  const expanded = libraryMore.getAttribute('aria-expanded') === 'true';
  libraryMore.setAttribute('aria-expanded', String(!expanded));
  libraryGrid?.classList.toggle('is-expanded', !expanded);
  libraryMore.firstChild.textContent = expanded ? '全19サービスを見る ' : '代表サービスだけ表示 ';
  libraryMore.querySelector('span').textContent = expanded ? '＋' : '−';
});

const worksTrack = document.querySelector('[data-works-track]');
const worksProgress = document.querySelector('[data-works-progress]');
const workPrev = document.querySelector('[data-work-prev]');
const workNext = document.querySelector('[data-work-next]');
const worksMore = document.querySelector('[data-works-more]');

worksMore?.addEventListener('click', () => {
  const expanded = worksMore.getAttribute('aria-expanded') === 'true';
  worksMore.setAttribute('aria-expanded', String(!expanded));
  worksTrack?.classList.toggle('is-expanded', !expanded);
  worksMore.firstChild.textContent = expanded ? 'すべての実績を見る ' : '代表実績だけ表示 ';
  worksMore.querySelector('span').textContent = expanded ? '＋' : '−';
});

document.querySelectorAll('.library-card, .work-card').forEach((link) => {
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
});

if (worksTrack) {
  let dragStart = 0;
  let dragScroll = 0;
  let dragged = false;

  const workStep = () => Math.min(540, worksTrack.clientWidth * .82);
  const updateWorksProgress = () => {
    const max = worksTrack.scrollWidth - worksTrack.clientWidth;
    const visibleRatio = Math.min(1, worksTrack.clientWidth / worksTrack.scrollWidth);
    const travelRatio = max > 0 ? worksTrack.scrollLeft / max : 0;
    const scale = visibleRatio + travelRatio * (1 - visibleRatio);
    worksProgress.style.transform = `scaleX(${scale})`;
  };

  worksTrack.addEventListener('scroll', updateWorksProgress, { passive: true });
  window.addEventListener('resize', updateWorksProgress, { passive: true });
  updateWorksProgress();

  worksTrack.addEventListener('pointerdown', (event) => {
    if (event.button !== 0) return;
    dragStart = event.clientX;
    dragScroll = worksTrack.scrollLeft;
    dragged = false;
    worksTrack.classList.add('is-dragging');
    worksTrack.setPointerCapture(event.pointerId);
  });
  worksTrack.addEventListener('pointermove', (event) => {
    if (!worksTrack.hasPointerCapture(event.pointerId)) return;
    const distance = event.clientX - dragStart;
    if (Math.abs(distance) > 5) dragged = true;
    worksTrack.scrollLeft = dragScroll - distance;
  });
  const endDrag = (event) => {
    if (worksTrack.hasPointerCapture(event.pointerId)) worksTrack.releasePointerCapture(event.pointerId);
    worksTrack.classList.remove('is-dragging');
  };
  worksTrack.addEventListener('pointerup', endDrag);
  worksTrack.addEventListener('pointercancel', endDrag);
  worksTrack.addEventListener('click', (event) => {
    if (dragged) {
      event.preventDefault();
      event.stopPropagation();
      dragged = false;
    }
  }, true);

  worksTrack.addEventListener('wheel', (event) => {
    if (!finePointer.matches || Math.abs(event.deltaX) > Math.abs(event.deltaY)) return;
    const max = worksTrack.scrollWidth - worksTrack.clientWidth;
    const next = Math.max(0, Math.min(max, worksTrack.scrollLeft + event.deltaY));
    if (next === worksTrack.scrollLeft) return;
    event.preventDefault();
    worksTrack.scrollLeft = next;
  }, { passive: false });

  worksTrack.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    if (event.key === 'Home') worksTrack.scrollTo({ left: 0, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
    else if (event.key === 'End') worksTrack.scrollTo({ left: worksTrack.scrollWidth, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
    else worksTrack.scrollBy({ left: event.key === 'ArrowLeft' ? -workStep() : workStep(), behavior: reduceMotion.matches ? 'auto' : 'smooth' });
  });
  workPrev?.addEventListener('click', () => worksTrack.scrollBy({ left: -workStep(), behavior: reduceMotion.matches ? 'auto' : 'smooth' }));
  workNext?.addEventListener('click', () => worksTrack.scrollBy({ left: workStep(), behavior: reduceMotion.matches ? 'auto' : 'smooth' }));
}

const chapterNumber = document.querySelector('[data-chapter]');
const chapterLabel = document.querySelector('[data-chapter-label]');
const chapterSections = [...document.querySelectorAll('[data-chapter-section]')];

if ('IntersectionObserver' in window && chapterNumber && chapterLabel) {
  const chapterObserver = new IntersectionObserver((entries) => {
    const current = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!current) return;
    chapterNumber.textContent = current.target.dataset.chapterSection;
    chapterLabel.textContent = current.target.dataset.chapterName;
  }, { rootMargin: '-30% 0px -55%', threshold: [0, .1, .35, .65] });
  chapterSections.forEach((section) => chapterObserver.observe(section));
}

if (!reduceMotion.matches && finePointer.matches) {
  let scrollTicking = false;
  const updateHeroParallax = () => {
    const amount = Math.min(1, Math.max(0, window.scrollY / window.innerHeight));
    const media = document.querySelector('.hero-media');
    if (media) media.style.transform = `translate3d(0, ${amount * 28}px, 0) scale(${1 + amount * .025})`;
    scrollTicking = false;
  };
  window.addEventListener('scroll', () => {
    if (scrollTicking) return;
    scrollTicking = true;
    requestAnimationFrame(updateHeroParallax);
  }, { passive: true });
}

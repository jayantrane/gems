(() => {
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  let allGems = [];
  let activeTag = null;

  async function init() {
    const timeline = document.getElementById('timeline');
    try {
      const res = await fetch('data/gems.json');
      const data = await res.json();
      allGems = data.gems.sort((a, b) => new Date(b.added) - new Date(a.added));
      render(allGems);
    } catch (e) {
      timeline.innerHTML = '<div class="empty-state">Could not load gems.</div>';
    }
  }

  function render(gems) {
    const timeline = document.getElementById('timeline');
    const tagBar = document.getElementById('tag-filter-bar');
    timeline.innerHTML = '';

    if (!gems.length) {
      timeline.innerHTML = '<div class="empty-state">No gems match that filter.</div>';
      return;
    }

    for (const gem of gems) {
      timeline.appendChild(createGemRow(gem));
    }

    buildTagBar(tagBar);
    observeItems();
  }

  function createGemRow(gem) {
    const row = document.createElement('div');
    row.className = 'gem-item';

    const d = new Date(gem.added);
    const day = `${MONTHS[d.getUTCMonth()]} ${d.getUTCDate()}, ${d.getUTCFullYear()}`;

    row.innerHTML = `
      <span class="gem-date">${day}</span>
      <span class="gem-dot"></span>
      <span class="gem-title"><a href="${escapeAttr(gem.url)}" target="_blank" rel="noopener">${escapeHtml(gem.title)}</a></span>
      <span class="gem-tags">${gem.tags.map(t => `<span class="tag-pill" data-tag="${escapeAttr(t)}">${escapeHtml(t)}</span>`).join('')}</span>
    `;

    row.querySelectorAll('.tag-pill').forEach(pill => {
      pill.addEventListener('click', () => filterByTag(pill.dataset.tag));
    });

    return row;
  }

  function buildTagBar(container) {
    const tags = [...new Set(allGems.flatMap(g => g.tags))].sort();
    const pills = container.querySelector('.tag-pills');
    if (pills) pills.remove();

    const wrap = document.createElement('span');
    wrap.className = 'tag-pills';
    for (const t of tags) {
      const pill = document.createElement('span');
      pill.className = 'tag-pill' + (activeTag === t ? ' active' : '');
      pill.textContent = t;
      pill.dataset.tag = t;
      pill.addEventListener('click', () => filterByTag(t));
      wrap.appendChild(pill);
    }
    container.appendChild(wrap);
  }

  function filterByTag(tag) {
    const clearBtn = document.getElementById('clear-filter');
    if (activeTag === tag) {
      activeTag = null;
      clearBtn.classList.remove('visible');
      render(allGems);
    } else {
      activeTag = tag;
      clearBtn.classList.add('visible');
      render(allGems.filter(g => g.tags.includes(tag)));
    }
  }

  function observeItems() {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        entry.target.classList.toggle('in-view', entry.isIntersecting);
      }
    }, { rootMargin: '-5% 0px -5% 0px', threshold: 0.1 });

    document.querySelectorAll('.gem-item').forEach(el => observer.observe(el));
  }

  function escapeHtml(s) {
    const div = document.createElement('div');
    div.textContent = s;
    return div.innerHTML;
  }

  function escapeAttr(s) {
    return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // Theme toggle
  function initTheme() {
    const saved = localStorage.getItem('gems-theme');
    applyTheme(saved || 'dark');

    document.getElementById('theme-toggle').addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
      applyTheme(next);
      localStorage.setItem('gems-theme', next);
    });
  }

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.textContent = theme === 'light' ? '☾' : '☀';
  }

  window.clearTagFilter = () => {
    activeTag = null;
    document.getElementById('clear-filter').classList.remove('visible');
    render(allGems);
  };

  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    init();
  });
})();

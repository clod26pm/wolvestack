/**
 * Client-side search functionality for WolveStack guides
 * Loads search-index.json and provides instant filtering as user types
 */

let searchIndex = [];
let debounceTimer;

// Popular searches to show when input is empty
const POPULAR_SEARCHES = [
  'BPC-157',
  'Semaglutide',
  'TB-500',
  'Peptides for beginners',
  'Dosing guide',
  'Fat loss',
  'Muscle growth',
  'Recovery',
  'Anti-aging',
  '5-Amino-1MQ'
];

/**
 * Initialize search on page load
 */
document.addEventListener('DOMContentLoaded', () => {
  initializeSearch();
});

/**
 * Load search index from JSON file
 */
async function initializeSearch() {
  try {
    const response = await fetch('/search-index.json');
    if (!response.ok) throw new Error('Failed to load search index');
    searchIndex = await response.json();

    // Bind search input event
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
      searchInput.addEventListener('input', handleSearchInput);

      // Check for ?q= URL parameter (from nav search bar)
      const urlParams = new URLSearchParams(window.location.search);
      const urlQuery = urlParams.get('q');
      if (urlQuery && urlQuery.trim()) {
        searchInput.value = urlQuery.trim();
        const results = performSearch(urlQuery.trim());
        displayResults(results, urlQuery.trim());
      } else {
        showPopularSearches();
      }
    }
  } catch (error) {
    console.error('Error loading search index:', error);
  }
}

/**
 * Handle search input with debouncing
 */
function handleSearchInput(event) {
  clearTimeout(debounceTimer);

  const query = event.target.value.trim();
  const resultsContainer = document.getElementById('searchResults');

  if (!resultsContainer) return;

  if (!query) {
    showPopularSearches();
    return;
  }

  debounceTimer = setTimeout(() => {
    const results = performSearch(query);
    displayResults(results, query);
  }, 300);
}

/**
 * Perform search on the index
 */
function performSearch(query) {
  const lowerQuery = query.toLowerCase();
  const queryWords = lowerQuery.split(/\s+/);

  return searchIndex
    .map((item) => {
      let score = 0;

      // Exact title match (highest priority)
      if (item.title.toLowerCase() === lowerQuery) {
        score += 100;
      }
      // Title starts with query
      else if (item.title.toLowerCase().startsWith(lowerQuery)) {
        score += 50;
      }
      // Title contains query
      else if (item.title.toLowerCase().includes(lowerQuery)) {
        score += 30;
      }

      // Match each word in keywords
      queryWords.forEach((word) => {
        if (item.keywords.some((kw) => kw.includes(word))) {
          score += 15;
        }
      });

      // Description match
      if (item.description.toLowerCase().includes(lowerQuery)) {
        score += 10;
      }

      return { ...item, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 50); // Limit to 50 results
}

/**
 * Display search results
 */
function displayResults(results, query) {
  const resultsContainer = document.getElementById('searchResults');
  if (!resultsContainer) return;

  if (results.length === 0) {
    resultsContainer.innerHTML = `
      <div style="text-align: center; padding: 48px 24px; color: #94a3b8;">
        <p style="font-size: 16px; margin-bottom: 8px;">No results found for "<strong>${escapeHtml(query)}</strong>"</p>
        <p style="font-size: 14px;">Try different keywords or browse all guides</p>
      </div>
    `;
    return;
  }

  const cardsHtml = results
    .map((result) => createResultCard(result, query))
    .join('');

  resultsContainer.innerHTML = `
    <div style="margin-bottom: 8px; padding: 0 20px; max-width: 780px; margin-left: auto; margin-right: auto;">
      <p style="color: #94a3b8; font-size: 13px; font-weight: 500;">
        ${results.length} result${results.length !== 1 ? 's' : ''}
      </p>
    </div>
    <div class="search-grid">
      ${cardsHtml}
    </div>
  `;
}

/**
 * Create a single result card
 */
function createResultCard(result, query) {
  const highlightedTitle = highlightMatch(result.title, query);
  const highlightedDesc = highlightMatch(result.description, query);

  return `
    <a href="${escapeHtml(result.url)}" class="search-result-card">
      <div class="search-result-category">${escapeHtml(result.category)}</div>
      <h3 class="search-result-title">${highlightedTitle}</h3>
      <p class="search-result-description">${highlightedDesc}</p>
      <div class="search-result-keywords">
        ${result.keywords
          .slice(0, 3)
          .map(
            (kw) =>
              `<span class="search-keyword">${escapeHtml(kw)}</span>`
          )
          .join('')}
      </div>
    </a>
  `;
}

/**
 * Show popular searches when input is empty
 */
function showPopularSearches() {
  const resultsContainer = document.getElementById('searchResults');
  if (!resultsContainer) return;

  const popular = POPULAR_SEARCHES.map(
    (search) =>
      `<button class="popular-search-btn" onclick="searchForTerm('${escapeHtml(search)}')">${escapeHtml(search)}</button>`
  ).join('');

  resultsContainer.innerHTML = `
    <div style="padding: 24px;">
      <p style="color: #94a3b8; font-size: 13px; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.5px;">Popular Searches</p>
      <div class="popular-searches">
        ${popular}
      </div>
    </div>
  `;
}

/**
 * Trigger search from popular searches button
 */
function searchForTerm(term) {
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.value = term;
    searchInput.focus();
    const event = new Event('input', { bubbles: true });
    searchInput.dispatchEvent(event);
  }
}

/**
 * Highlight matching text in results
 */
function highlightMatch(text, query) {
  if (!query) return escapeHtml(text);

  // Escape regex special characters to prevent ReDoS attacks
  const escapeRegex = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const terms = query.split(/\s+/).map(escapeRegex).filter(Boolean);
  if (terms.length === 0) return escapeHtml(text);

  const regex = new RegExp(`(${terms.join('|')})`, 'gi');
  return escapeHtml(text).replace(
    regex,
    '<mark style="background: rgba(20, 189, 172, 0.2); color: inherit; font-weight: 600;">$1</mark>'
  );
}

/**
 * Escape HTML special characters
 */
function escapeHtml(unsafe) {
  return (unsafe || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

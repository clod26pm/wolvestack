#!/usr/bin/env python3
"""
Update navigation across all HTML files in the peptide-daily-content project.
Adds inline search bar and language dropdown to the navigation header.
"""

import os
import re
from pathlib import Path

# Language mapping with codes
LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'zh': '中文',
    'ja': '日本語',
    'pt': 'Português',
    'ru': 'Русский',
    'it': 'Italiano',
    'pl': 'Polski',
    'fr': 'Français',
    'id': 'Bahasa',
    'de': 'Deutsch',
    'nl': 'Nederlands',
    'ar': 'العربية'
}

# New navigation HTML template
NAV_TEMPLATE = '''<nav>
<div class="nav-inner">
<a class="logo" href="/">Wolve<span>Stack</span></a>
<ul class="nav-links">
<li><a href="/bpc-157-guide.html">BPC-157</a></li>
<li><a href="/tb-500-guide.html">TB-500</a></li>
<li><a href="/wolverine-stack.html">Stacks</a></li>
<li><a href="/peptide-sourcing-guide.html">Vendors</a></li>
</ul>
<div class="nav-search">
<form>
<input type="text" placeholder="Search..." class="search-input">
<button type="submit" class="search-btn" aria-label="Search">🔍</button>
</form>
</div>
<div class="nav-lang">
<button class="nav-lang-toggle" aria-label="Select language">🌐 <span class="arrow">▾</span></button>
<div class="nav-lang-menu">
{language_links}
</div>
</div>
<a class="nav-cta" href="/peptide-beginners-guide.html">Start Here →</a>
</div>
</nav>'''

# CSS to add to the style block
NAV_CSS = '''
  /* Search Bar Styles */
  .nav-search {
    position: relative;
    display: flex;
    align-items: center;
  }
  .nav-search form {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(13, 115, 119, 0.4);
    border-radius: 6px;
    padding: 2px 8px;
    transition: all 0.2s;
  }
  .nav-search form:focus-within {
    background: rgba(255, 255, 255, 0.15);
    border-color: var(--teal-light);
    box-shadow: 0 0 12px rgba(20, 189, 172, 0.1);
  }
  .search-input {
    background: transparent;
    border: none;
    outline: none;
    color: var(--white);
    font-size: 14px;
    width: 140px;
    padding: 6px 4px;
    font-family: var(--font-main);
  }
  .search-input::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }
  .search-input:focus {
    width: 180px;
  }
  .search-btn {
    background: transparent;
    border: none;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    font-size: 14px;
    padding: 4px 4px;
    transition: color 0.2s;
    display: flex;
    align-items: center;
  }
  .search-btn:hover {
    color: var(--teal-light);
  }

  /* Language Dropdown Styles */
  .nav-lang {
    position: relative;
    display: flex;
    align-items: center;
  }
  .nav-lang-toggle {
    background: transparent;
    border: none;
    color: rgba(255, 255, 255, 0.75);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 8px;
    transition: color 0.2s;
  }
  .nav-lang-toggle:hover {
    color: var(--teal-light);
  }
  .nav-lang-toggle .arrow {
    display: inline-block;
    transition: transform 0.2s;
    font-size: 12px;
  }
  .nav-lang.open .nav-lang-toggle .arrow {
    transform: rotate(180deg);
  }
  .nav-lang-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background: rgba(15, 34, 64, 0.98);
    border: 1px solid rgba(13, 115, 119, 0.4);
    border-radius: 6px;
    margin-top: 4px;
    min-width: 160px;
    display: none;
    flex-direction: column;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
  .nav-lang.open .nav-lang-menu {
    display: flex;
  }
  .nav-lang-menu a {
    padding: 10px 16px;
    color: rgba(255, 255, 255, 0.75);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s;
    border-left: 3px solid transparent;
  }
  .nav-lang-menu a:hover {
    background: rgba(13, 115, 119, 0.2);
    color: var(--teal-light);
    border-left-color: var(--teal-light);
  }
  .nav-lang-menu a.active {
    background: rgba(13, 115, 119, 0.3);
    color: var(--teal-light);
    border-left-color: var(--teal-light);
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .search-input {
      width: 100px;
    }
    .search-input:focus {
      width: 130px;
    }
    .nav-lang-toggle {
      padding: 4px 6px;
    }
  }
  @media (max-width: 600px) {
    .nav-search form {
      padding: 2px 6px;
    }
    .search-input {
      width: 80px;
      font-size: 13px;
    }
    .search-input:focus {
      width: 120px;
    }
    .search-btn {
      padding: 4px 2px;
    }
  }
'''

# JavaScript to add
NAV_JS = '''
  // Language dropdown toggle
  (function() {
    const navLang = document.querySelector('.nav-lang');
    const navLangToggle = document.querySelector('.nav-lang-toggle');

    if (navLangToggle) {
      navLangToggle.addEventListener('click', function(e) {
        navLang.classList.toggle('open');
        e.stopPropagation();
      });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
      if (navLang) navLang.classList.remove('open');
    });
  })();

  // Search functionality
  (function() {
    const searchForm = document.querySelector('.nav-search form');
    if (searchForm) {
      searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = this.querySelector('.search-input').value;
        if (query.trim()) {
          // Determine the search URL based on current language
          let currentLang = 'en';
          const pathname = window.location.pathname;
          const langMatch = pathname.match(/^\\/([a-z]{2})\\//);
          if (langMatch) {
            currentLang = langMatch[1];
          }
          const searchUrl = currentLang === 'en'
            ? '/search.html?q=' + encodeURIComponent(query)
            : '/' + currentLang + '/search.html?q=' + encodeURIComponent(query);
          window.location.href = searchUrl;
        }
      });
    }
  })();
'''


def get_language_links(lang_dir, current_file):
    """Generate language dropdown links for a given file."""
    links = []

    # Determine the filename without language prefix
    if lang_dir in LANGUAGES:
        # This is a language-specific directory
        clean_filename = current_file
    else:
        # This is the root directory
        clean_filename = current_file

    for lang_code, lang_name in LANGUAGES.items():
        if lang_code == 'en':
            # English files are in root
            url = f'/{clean_filename}'
        else:
            # Other language files are in language directories
            url = f'/{lang_code}/{clean_filename}'

        # Check if this is the current language
        is_active = (lang_dir == lang_code) or (lang_dir == '' and lang_code == 'en')
        active_class = ' class="active"' if is_active else ''

        links.append(f'<a href="{url}"{active_class}>{lang_name}</a>')

    return '\n'.join(links)


def detect_language_from_path(filepath):
    """Detect if a file is in a language directory."""
    path_parts = filepath.split(os.sep)

    # Check if any directory in the path is a language code
    for lang_code in LANGUAGES.keys():
        if lang_code in path_parts:
            return lang_code

    return 'en'


def extract_filename(filepath):
    """Extract just the filename from a path."""
    return os.path.basename(filepath)


def update_nav_in_file(filepath, lang_dir):
    """Update the navigation in a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file already has the new nav structure
    if 'nav-search' in content and 'nav-lang' in content:
        print(f"  ✓ Already updated: {filepath}")
        return False

    # Extract filename for language links
    filename = extract_filename(filepath)

    # Generate language links
    lang_links = get_language_links(lang_dir, filename)

    # Create the new nav HTML
    new_nav = NAV_TEMPLATE.format(language_links=lang_links)

    # Replace the old nav block with new one
    # Match from <nav> to </nav>
    nav_pattern = r'<nav>.*?</nav>'
    updated_content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)

    # Check if nav was actually replaced
    if updated_content == content:
        print(f"  ✗ No nav found: {filepath}")
        return False

    # Add CSS to style block if not already present
    if 'nav-search' not in updated_content:
        # Find the closing </style> tag
        style_close_pattern = r'(</style>)'
        css_insert = NAV_CSS + '\n  \\1'
        updated_content = re.sub(style_close_pattern, css_insert, updated_content, count=1)

    # Add JavaScript before closing </body> if not already present
    if 'nav-search form' not in updated_content or 'Language dropdown toggle' not in updated_content:
        # Find </body> tag
        body_close_pattern = r'(</body>)'
        js_insert = '<script>\n' + NAV_JS + '\n</script>\n\\1'
        updated_content = re.sub(body_close_pattern, js_insert, updated_content, count=1)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"  ✓ Updated: {filepath}")
    return True


def process_directory(root_dir, lang_dir=''):
    """Process all HTML files in a directory."""
    count = 0

    # Get all HTML files in this directory (not subdirectories)
    for filename in os.listdir(root_dir):
        if filename.endswith('.html') and not filename.startswith('TEMPLATE'):
            filepath = os.path.join(root_dir, filename)
            if os.path.isfile(filepath):
                if update_nav_in_file(filepath, lang_dir):
                    count += 1

    return count


def main():
    """Main function to update all HTML files."""
    base_dir = '/sessions/confident-friendly-thompson/mnt/cowork/peptide-daily-content'

    total_updated = 0

    print("=" * 60)
    print("UPDATING NAVIGATION ACROSS ALL HTML FILES")
    print("=" * 60)

    # Update root directory (English files)
    print("\nProcessing root directory (English)...")
    total_updated += process_directory(base_dir, 'en')

    # Update each language directory
    for lang_code in LANGUAGES.keys():
        if lang_code == 'en':
            continue  # Already done

        lang_dir = os.path.join(base_dir, lang_code)
        if os.path.isdir(lang_dir):
            print(f"\nProcessing /{lang_code}/ directory...")
            total_updated += process_directory(lang_dir, lang_code)

    # Update category directory
    category_dir = os.path.join(base_dir, 'category')
    if os.path.isdir(category_dir):
        print(f"\nProcessing /category/ directory...")
        total_updated += process_directory(category_dir, 'en')

    # Update language-specific category directories
    for lang_code in LANGUAGES.keys():
        if lang_code == 'en':
            continue

        lang_category_dir = os.path.join(base_dir, lang_code, 'category')
        if os.path.isdir(lang_category_dir):
            print(f"\nProcessing /{lang_code}/category/ directory...")
            total_updated += process_directory(lang_category_dir, lang_code)

    print("\n" + "=" * 60)
    print(f"COMPLETED: {total_updated} files updated")
    print("=" * 60)


if __name__ == '__main__':
    main()

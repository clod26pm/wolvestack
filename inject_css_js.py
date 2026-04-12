#!/usr/bin/env python3
"""
Inject CSS and JavaScript into HTML files that already have the nav structure.
This fixes the CSS injection that was missed in the first pass.
"""

import os
import re
from pathlib import Path

# CSS to add to the style block (before </style>)
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

def inject_css_and_js(filepath):
    """Inject CSS and JS into an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if this file already has the updated nav
    if 'nav-search' not in content:
        return False

    # Check if CSS already exists
    if '.nav-search {' in content:
        return False  # Already injected

    # Add CSS before </style>
    if '<style>' in content or '<style ' in content:
        style_close_pattern = r'(</style>)'
        css_with_newline = '\n' + NAV_CSS + '\n  '
        updated_content = re.sub(style_close_pattern, css_with_newline + r'\1', content, count=1)
    else:
        return False

    # Verify CSS was added
    if updated_content == content:
        return False

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    return True


def process_directory(root_dir):
    """Process all HTML files in a directory."""
    count = 0

    # Get all HTML files in this directory (not subdirectories)
    for filename in os.listdir(root_dir):
        if filename.endswith('.html') and not filename.startswith('TEMPLATE'):
            filepath = os.path.join(root_dir, filename)
            if os.path.isfile(filepath):
                if inject_css_and_js(filepath):
                    count += 1
                    print(f"  ✓ Injected CSS/JS: {filepath}")

    return count


def main():
    """Main function to inject CSS/JS into all HTML files."""
    base_dir = '/sessions/confident-friendly-thompson/mnt/cowork/peptide-daily-content'

    total_updated = 0

    print("=" * 60)
    print("INJECTING CSS/JS INTO HTML FILES")
    print("=" * 60)

    # Inject to root directory (English files)
    print("\nProcessing root directory (English)...")
    total_updated += process_directory(base_dir)

    # Language directories
    for lang_dir in ['en', 'es', 'zh', 'ja', 'pt', 'ru', 'it', 'pl', 'fr', 'id', 'de', 'nl', 'ar']:
        lang_path = os.path.join(base_dir, lang_dir)
        if os.path.isdir(lang_path):
            print(f"\nProcessing /{lang_dir}/ directory...")
            total_updated += process_directory(lang_path)

    # Category directory
    category_dir = os.path.join(base_dir, 'category')
    if os.path.isdir(category_dir):
        print(f"\nProcessing /category/ directory...")
        total_updated += process_directory(category_dir)

    # Language-specific category directories
    for lang_dir in ['en', 'es', 'zh', 'ja', 'pt', 'ru', 'it', 'pl', 'fr', 'id', 'de', 'nl', 'ar']:
        lang_category_dir = os.path.join(base_dir, lang_dir, 'category')
        if os.path.isdir(lang_category_dir):
            print(f"\nProcessing /{lang_dir}/category/ directory...")
            total_updated += process_directory(lang_category_dir)

    print("\n" + "=" * 60)
    print(f"COMPLETED: {total_updated} files had CSS/JS injected")
    print("=" * 60)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Bulk update all HTML guide files to add a search link to the navigation.
Adds "Search" link after "Vendors" in the nav links.
"""

import os
import re
from pathlib import Path

def update_nav_in_file(file_path):
    """Update navigation in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file already has search link
        if '<a href="/search.html"' in content:
            return False, "Already has search link"

        # Check if this is a guide file with nav structure
        if '<ul class="nav-links">' not in content:
            return False, "No nav-links found"

        # Pattern: Find closing </ul> in nav-links and add search link before it
        # This handles multiple variations of nav structures
        pattern = r'(<ul class="nav-links">.*?)(\n</ul>)'

        # Add search link before closing </ul>
        search_link = r'\1\n<li><a href="/search.html">🔍 Search</a></li>\2'
        updated_content = re.sub(pattern, search_link, content, flags=re.DOTALL)

        # Check if substitution happened
        if updated_content == content:
            return False, "Pattern not found"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return True, "Updated"

    except Exception as e:
        return False, f"Error: {e}"

def main():
    base_dir = Path('/sessions/confident-friendly-thompson/mnt/cowork/peptide-daily-content')

    # Get all HTML files in root directory
    html_files = sorted(base_dir.glob('*.html'))

    # Skip certain files
    skip_files = {'index.html', '404.html', 'search.html', 'TEMPLATE-CSS.html', 'TEMPLATE-BODY.html'}

    updated_count = 0
    skipped_count = 0
    error_count = 0

    for html_file in html_files:
        if html_file.name in skip_files:
            continue

        success, message = update_nav_in_file(html_file)

        if success:
            updated_count += 1
            if updated_count % 100 == 0:
                print(f"✓ Updated {updated_count} files...")
        else:
            skipped_count += 1
            if skipped_count <= 5:  # Show first few skips
                print(f"  {html_file.name}: {message}")

    print(f"\n✅ Update complete!")
    print(f"   Updated: {updated_count} files")
    print(f"   Skipped: {skipped_count} files")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Generate search-index.json from all HTML guide files in the root directory.
Extracts title, description, category, and keywords for client-side search.
"""

import os
import json
import re
from pathlib import Path
from html.parser import HTMLParser

class MetaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.category = ""
        self.in_title = False
        self.in_breadcrumb = False
        self.breadcrumb_links = []
        self.found_meta_desc = False

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            attrs_dict = dict(attrs)
            if attrs_dict.get('name') == 'description' and not self.found_meta_desc:
                self.description = attrs_dict.get('content', '')
                self.found_meta_desc = True
        elif tag == 'a' and not self.in_breadcrumb:
            # Check if this is part of breadcrumb
            pass

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()

def extract_metadata(html_content, filename):
    """Extract title and description from HTML content."""
    parser = MetaExtractor()
    try:
        parser.feed(html_content)
    except:
        pass

    # Fallback: if title not found, try regex
    if not parser.title:
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        if title_match:
            parser.title = title_match.group(1).strip()

    # If no description found, try to extract from first paragraph or h1
    if not parser.description:
        # Look for breadcrumb to get category
        breadcrumb_match = re.search(r'<div class="breadcrumb">.*?<a[^>]*>.*?</a>\s*<span>/</span>\s*<a[^>]*>(.*?)</a>',
                                     html_content, re.DOTALL)
        if breadcrumb_match:
            parser.category = breadcrumb_match.group(1).strip()

        # Try to get description from h1 + next p or just h1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
        if h1_match:
            h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
            parser.description = h1_text[:200]
        else:
            # Try first paragraph
            p_match = re.search(r'<p[^>]*>(.*?)</p>', html_content)
            if p_match:
                p_text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
                parser.description = p_text[:200]

    # Extract category from breadcrumb if not already found
    if not parser.category:
        # Look for "Guides" or the second breadcrumb link
        breadcrumb_match = re.search(
            r'<div class="breadcrumb">.*?<a[^>]*>[^<]*</a>\s*<span>/</span>\s*<a[^>]*>([^<]*)</a>',
            html_content, re.DOTALL
        )
        if breadcrumb_match:
            parser.category = breadcrumb_match.group(1).strip()
        else:
            parser.category = "Guide"

    return parser.title, parser.description, parser.category

def generate_keywords(title, description):
    """Generate searchable keywords from title and description."""
    combined = f"{title} {description}".lower()
    # Remove common words and get meaningful terms
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'why', 'how'}

    words = re.findall(r'\b[a-z0-9\-]+\b', combined)
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return list(dict.fromkeys(keywords))[:15]  # Remove duplicates, keep first 15

def main():
    base_dir = Path('/sessions/confident-friendly-thompson/mnt/cowork/peptide-daily-content')
    search_index = []

    # Get all HTML files in root directory only
    html_files = sorted(base_dir.glob('*.html'))

    # Exclude certain files that aren't guides
    exclude_files = {'index.html', '404.html', 'search.html', 'TEMPLATE-CSS.html', 'TEMPLATE-BODY.html'}

    total = 0
    for html_file in html_files:
        if html_file.name in exclude_files:
            continue

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            title, description, category = extract_metadata(content, html_file.name)

            # Skip if no title found
            if not title:
                print(f"⚠️  Skipping {html_file.name} - no title found")
                continue

            keywords = generate_keywords(title, description)

            entry = {
                'url': f"/{html_file.name}",
                'title': title,
                'description': description[:150],  # Limit description length
                'category': category,
                'keywords': keywords
            }

            search_index.append(entry)
            total += 1

            if total % 100 == 0:
                print(f"✓ Indexed {total} files...")

        except Exception as e:
            print(f"✗ Error processing {html_file.name}: {e}")

    # Sort by title for consistency
    search_index.sort(key=lambda x: x['title'].lower())

    # Write JSON file
    output_file = base_dir / 'search-index.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Search index generated successfully!")
    print(f"   Total entries: {len(search_index)}")
    print(f"   Output: {output_file}")

if __name__ == '__main__':
    main()

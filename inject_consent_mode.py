#!/usr/bin/env python3
"""
Inject Google Consent Mode v2 default-deny snippet before every GA tag.
Required for GDPR/UK GDPR compliance — without this, GA loads with full
tracking before user consent, which is unlawful in EU/UK.

Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CONSENT_DEFAULT = """\
<!-- Google Consent Mode v2 — default deny until user accepts -->
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'functionality_storage': 'granted',
  'security_storage': 'granted',
  'wait_for_update': 500
});
</script>
"""

GA_RX = re.compile(r'<!--\s*Google tag \(gtag\.js\)\s*-->', re.IGNORECASE)
MARKER = "Google Consent Mode v2"

count = 0
for html_path in ROOT.rglob("*.html"):
    # skip node_modules / .git
    if any(part.startswith('.') or part == 'node_modules' for part in html_path.relative_to(ROOT).parts):
        continue
    try:
        html = html_path.read_text(encoding="utf-8")
    except Exception:
        continue
    if MARKER in html:
        continue
    if not GA_RX.search(html):
        continue
    new_html = GA_RX.sub(CONSENT_DEFAULT + r'\g<0>', html, count=1)
    if new_html != html:
        html_path.write_text(new_html, encoding="utf-8")
        count += 1
print(f"injected consent-default-deny into {count} files")

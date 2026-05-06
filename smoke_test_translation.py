#!/usr/bin/env python3
"""Quick smoke test for the argostranslate offline pipeline."""
import re
import sys

import argostranslate.sbd as _sbd

_sbd.stanza_available = False


def _regex_split_sentences(self, text):
    if not text:
        return []
    parts = re.split(r"(?<=[.!?\u3002\uFF01\uFF1F])\s+", text.strip())
    return [p for p in parts if p]


for _name in dir(_sbd):
    _obj = getattr(_sbd, _name)
    if isinstance(_obj, type) and hasattr(_obj, "split_sentences"):
        _obj.split_sentences = _regex_split_sentences

if callable(getattr(_sbd, "split_sentences", None)):
    def _module_split_sentences(text, *a, **kw):
        if not text:
            return []
        parts = re.split(r"(?<=[.!?\u3002\uFF01\uFF1F])\s+", text.strip())
        return [p for p in parts if p]
    _sbd.split_sentences = _module_split_sentences

import argostranslate.translate

failed = []
for lang in ["es", "zh", "ja", "pt", "ru", "it", "pl", "fr", "id", "de", "nl", "ar"]:
    t = argostranslate.translate.get_translation_from_codes("en", lang)
    if t is None:
        failed.append(f"{lang}: no translator installed")
        continue
    r = t.translate("Hello, how are you?")
    if r == "Hello, how are you?":
        failed.append(f"{lang}: returned English unchanged")
    else:
        print(f"  ✓ en→{lang}: {r[:60]}")

if failed:
    print("\n  ⛔ FAILED:")
    for f in failed:
        print(f"     {f}")
    sys.exit(1)

print("\n✅ ALL 12 LANGUAGES OK — pipeline is good to run.")

#!/usr/bin/env python3
import os
import time
from deep_translator import GoogleTranslator

# لیست فایل‌های اصلی که ترجمه می‌شوند
FILES = [
    "CONSTITUTION.md",
    "README.md",
    "GUIDE.md",
    "ROADMAP.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LANGUAGE_STATUS.md"
]

# زبان‌های مقصد (8 زبان اصلی)
LANGS = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ar": "Arabic",
    "zh": "Chinese",
    "hi": "Hindi",
    "ru": "Russian",
    "pt": "Portuguese"
}

def translate_file(src, dst, lang_code):
    print(f"Translating {src} -> {dst} ({LANGS[lang_code]})")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    translator = GoogleTranslator(source='en', target=lang_code)
    out_lines = []
    for line in lines:
        stripped = line.strip()
        # خطوط خالی، کد، جداول و لینک‌ها را ترجمه نکن
        if not stripped or stripped.startswith('```') or '|' in stripped or '`' in stripped:
            out_lines.append(line.rstrip('\n'))
            continue
        if stripped.startswith(('![', '[')) and '](' in stripped:
            out_lines.append(line.rstrip('\n'))
            continue
        # ترجمه خط
        try:
            translated = translator.translate(line.rstrip('\n'))
            out_lines.append(translated)
        except Exception as e:
            print(f"  Error translating: {line[:30]}... -> {e}")
            out_lines.append(line.rstrip('\n'))
        time.sleep(0.2)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))

# حلقه اصلی
for lang_code in LANGS:
    print(f"\n=== Translating to {LANGS[lang_code]} ({lang_code}) ===")
    for src in FILES:
        dst = f"i18n/{lang_code}/{src}"
        translate_file(src, dst, lang_code)

print("\n✅ ترجمه با موفقیت کامل شد.")

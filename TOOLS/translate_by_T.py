#!/usr/bin/env python3
import os, sys, time, requests
from pathlib import Path
from deep_translator import GoogleTranslator

ROOT = Path.cwd()
EXCLUDE_DIRS = {".git", ".github", "assets", "tools", "CHAIN", "i18n", "node_modules", "__pycache__"}

def should_skip(line: str) -> bool:
    s = line.strip()
    if not s or s.startswith("```") or "|" in s or "`" in s:
        return True
    if s.startswith(("![", "[")) and "](" in s:
        return True
    return False

def translate_text(text: str, target: str) -> str:
    if not text.strip(): return text
    try:
        if os.environ.get("DEEPL_API_KEY"):
            url = "https://api-free.deepl.com/v2/translate"
            params = {"auth_key": os.environ["DEEPL_API_KEY"], "text": text, "target_lang": target.upper()}
            resp = requests.post(url, data=params).json()
            return resp["translations"][0]["text"]
        else:
            translator = GoogleTranslator(source="en", target=target)
            return translator.translate(text)
    except Exception:
        return text

def translate_file(src: Path, dst: Path, lang: str):
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(src, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out_lines = []
    for line in lines:
        if should_skip(line):
            out_lines.append(line.rstrip("
"))
        else:
            out_lines.append(translate_text(line.rstrip("
"), lang))
        time.sleep(0.05)
    with open(dst, "w", encoding="utf-8") as f:
        f.write("
".join(out_lines))

def main():
    lang_codes = os.environ.get("INPUT_LANGS", "es fr de ar zh hi ja ru pt it ko tr nl pl sv ur he").split()
    md_files = []
    for p in ROOT.rglob("*.md"):
        if any(ex in p.parts for ex in EXCLUDE_DIRS): continue
        if "i18n" in p.parts: continue
        md_files.append(p)
    print(f"Found {len(md_files)} markdown files to translate.")
    for lang in lang_codes:
        print(f"
--- Translating to {lang} ---")
        for src in md_files:
            rel = src.relative_to(ROOT)
            dst = ROOT / "i18n" / lang / rel
            translate_file(src, dst, lang)
    print("Translation completed by @T@.")

if __name__ == "__main__":
    main()

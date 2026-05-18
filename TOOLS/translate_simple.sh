#!/bin/bash

# زبان‌های مقصد (می‌توانید لیست را تغییر دهید)
LANGUAGES=("es" "fr" "de" "ar" "zh" "hi" "ru" "pt")

# فایل‌های کلیدی
FILES=(
    "CONSTITUTION.md"
    "README.md"
    "GUIDE.md"
    "ROADMAP.md"
    "CODE_OF_CONDUCT.md"
    "CONTRIBUTING.md"
    "LANGUAGE_STATUS.md"
)

# API ترجمه (LibreTranslate – رایگان، بدون کلید)
TRANSLATE_API="https://libretranslate.com/translate"

# تابع ترجمه یک خط
translate_line() {
    local text="$1"
    local target="$2"
    # فرار از کاراکترهای خاص برای JSON
    local escaped=$(echo -n "$text" | jq -s -R -r @uri)
    local response=$(curl -s -X POST "$TRANSLATE_API" \
        -d "q=$escaped" \
        -d "source=en" -d "target=$target" \
        -d "format=text")
    echo "$response" | jq -r '.translatedText' 2>/dev/null || echo "$text"
}

# تابع ترجمه کل فایل
translate_file() {
    local src="$1"
    local dst="$2"
    local lang="$3"
    mkdir -p "$(dirname "$dst")"
    echo "Translating $src -> $dst ($lang)"
    while IFS= read -r line; do
        # حذف carriage return (Windows)
        line=$(echo "$line" | tr -d '\r')
        # خطوطی که نباید ترجمه شوند (کد، جدول، لینک، خالی)
        if [[ -z "$line" ]]; then
            echo "" >> "$dst"
        elif [[ "$line" =~ ^\`\`\` ]] || [[ "$line" =~ ^\|\s*$ ]] || [[ "$line" =~ ^\s*$ ]]; then
            echo "$line" >> "$dst"
        elif [[ "$line" =~ ^\[.*\]\(.*\)$ ]]; then
            echo "$line" >> "$dst"
        elif [[ "$line" =~ ^[[:space:]]*[\*\-\+] ]]; then
            echo "$line" >> "$dst"
        else
            translated=$(translate_line "$line" "$lang")
            echo "$translated" >> "$dst"
        fi
        sleep 0.2  # جلوگیری از محدودیت نرخ
    done < "$src"
}

# حلقه اصلی
for lang in "${LANGUAGES[@]}"; do
    echo "=== Processing language: $lang ==="
    for file in "${FILES[@]}"; do
        translate_file "$file" "i18n/$lang/$file" "$lang"
    done
done

echo "✅ Translation completed for all languages."

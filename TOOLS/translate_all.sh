#!/bin/bash

# لیست زبان‌های هدف (کد ISO)
LANGUAGES=("es" "fr" "de" "ar" "zh" "hi")

# لیست فایل‌های کلیدی (مسیر نسبی از ریشه)
FILES=(
    "CONSTITUTION.md"
    "README.md"
    "GUIDE.md"
    "ROADMAP.md"
    "LANGUAGE_STATUS.md"
    "CODE_OF_CONDUCT.md"
    "CONTRIBUTING.md"
    "COGNITION/PRINCIPLES.md"
)

# تابع ترجمه یک خط (با LibreTranslate)
translate_line() {
    local text="$1"
    local target="$2"
    local url="https://libretranslate.com/translate"
    local response=$(curl -s -X POST "$url" \
        -d "q=$(echo -n "$text" | jq -s -R -r @uri)" \
        -d "source=en" -d "target=$target" \
        -d "format=text")
    echo "$response" | jq -r '.translatedText' 2>/dev/null || echo "$text"
}

# تابع ترجمه کل فایل (حفظ ساختار مارک‌داون)
translate_file() {
    local input_file="$1"
    local output_file="$2"
    local target_lang="$3"
    echo "Translating $input_file -> $output_file ($target_lang)"
    mkdir -p "$(dirname "$output_file")"
    while IFS= read -r line; do
        # خطوط خالی یا خطوطی که با کاراکترهای خاص (مثل کد، جدول، لینک) شروع می‌شوند را ترجمه نکن
        if [[ -z "$line" ]]; then
            echo "" >> "$output_file"
        elif [[ "$line" =~ ^[\`\|\-\#\*] ]] || [[ "$line" =~ ^[0-9]+\..* ]] || [[ "$line" =~ ^\[.*\]:.* ]]; then
            echo "$line" >> "$output_file"
        else
            translated=$(translate_line "$line" "$target_lang")
            echo "$translated" >> "$output_file"
        fi
    done < "$input_file"
    # حذف کاراکترهای carriage return
    sed -i '' 's/\r$//' "$output_file"
}

# حلقه روی زبان‌ها و فایل‌ها
for lang in "${LANGUAGES[@]}"; do
    echo "=== Processing language: $lang ==="
    for file in "${FILES[@]}"; do
        input_file="$file"
        output_file="i18n/$lang/$file"
        translate_file "$input_file" "$output_file" "$lang"
    done
done

echo "✅ ترجمه خودکار به زبان‌های ${LANGUAGES[*]} با استفاده از LibreTranslate انجام شد."
echo "⚠️ کیفیت ترجمه متوسط است. توصیه می‌شود یک بازبین انسانی (یا مدل زبانی قوی‌تر) اصلاحات لازم را انجام دهد."

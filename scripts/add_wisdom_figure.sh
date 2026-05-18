#!/bin/bash
# اسکریپت برای ایجاد یک فایل جدید در WISDOM/ و کپی قالب به همه زبان‌ها
# استفاده: ./scripts/add_wisdom_figure.sh "Name" "filename"
# مثال: ./scripts/add_wisdom_figure.sh "Rumi" "Rumi"

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 \"Display Name\" \"filename\""
  exit 1
fi

NAME="$1"
FILENAME="$2"
TEMPLATE="WISDOM/TEMPLATE.md"

if [ ! -f "$TEMPLATE" ]; then
  echo "Template not found at $TEMPLATE"
  exit 1
fi

# ایجاد فایل انگلیسی
cp "$TEMPLATE" "WISDOM/${FILENAME}.md"
echo "✅ Created WISDOM/${FILENAME}.md"

# برای هر زبان موجود، یک کپی از قالب ایجاد کن
for lang in $(ls -d i18n/*/ 2>/dev/null | sed 's|i18n/||g; s|/||g'); do
  mkdir -p "i18n/$lang/WISDOM"
  cp "$TEMPLATE" "i18n/$lang/WISDOM/${FILENAME}.md"
  echo "   Created i18n/$lang/WISDOM/${FILENAME}.md (needs translation)"
done

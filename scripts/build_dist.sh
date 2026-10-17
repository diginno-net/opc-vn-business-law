#!/usr/bin/env bash
# Đóng gói skill thành zip để chia sẻ.
# Dùng: bash scripts/build_dist.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VERSION="$(sed -n 's/^[[:space:]]*version:[[:space:]]*//p' SKILL.md | head -1 | tr -d '\r')"
[ -n "$VERSION" ] || { echo "Không đọc được version trong SKILL.md"; exit 1; }

NAME="opc-vn-business-law"
OUT="dist/${NAME}-v${VERSION}.zip"
mkdir -p dist
rm -f "$OUT"

zip -r "$OUT" . \
  -x "dist/*" \
  -x "launch/*" \
  -x ".audit-internal-terms" \
  -x ".git/*" \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x ".DS_Store" \
  -x "*.zip" \
  >/dev/null

echo "Đã tạo: $OUT"
echo "Kích thước: $(du -h "$OUT" | cut -f1)"
echo
echo "SHA-256:"
shasum -a 256 "$OUT"
echo
echo "Nội dung:"
unzip -l "$OUT" | tail -n +4 | sed '$d'

#!/usr/bin/env bash
# Audit goi public: khong secret, khong PII, khong duong dan may, khong .git trong goi.
# Dung: bash scripts/audit_public.sh
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0

say() { printf '%s\n' "$*"; }
fail() { FAIL=1; say "FAIL: $*"; }

# 1. Secret / token / password trong source
say "== 1. Secret/token/password (source)"
if grep -rniE "sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|Bearer [A-Za-z0-9._-]{10,}|client_secret|api[_-]?key[[:space:]]*[:=]" . \
  --exclude-dir=.git --exclude-dir=dist --exclude="audit_public.sh"; then
  fail "co mau secret/token"
else
  say "OK"
fi

# 2. Duong dan may ca nhan
say "== 2. Duong dan may ca nhan"
if grep -rn "$HOME" . --exclude-dir=.git --exclude-dir=dist --exclude="audit_public.sh"; then
  fail "co duong dan may ca nhan"
else
  say "OK"
fi

# 3. Email / so dien thoai
say "== 3. Email / so dien thoai"
if grep -rnoE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|(^|[^0-9])(0|\+84)(3|5|7|8|9)[0-9]{8}([^0-9]|$)" . \
  --exclude-dir=.git --exclude-dir=dist --exclude="audit_public.sh"; then
  fail "co email/so dien thoai"
else
  say "OK"
fi

# 4. He thong noi bo (khong gom ten thuong hieu)
say "== 4. He thong/ha tang noi bo"
if grep -rniE "larkbase|diginno\.app|coolify|prefect|n8n\.|/Users/|/home/" . \
  --exclude-dir=.git --exclude-dir=dist --exclude="audit_public.sh"; then
  fail "co ten he thong noi bo"
else
  say "OK"
fi

# 5. Goi dong goi: khong .git, khong dist, khong file la
say "== 5. Goi dong goi"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
for f in dist/*.zip dist/*.skill; do
  [ -e "$f" ] || continue
  d="$TMP/$(basename "$f")"
  mkdir -p "$d"
  unzip -q "$f" -d "$d"
  if find "$d" -path "*/.git/*" -o -name ".git" | grep -q .; then
    fail "$f chua .git"
  fi
  if find "$d" -path "*/dist/*" | grep -q .; then
    fail "$f chua dist"
  fi
  if grep -rniE "sk-[A-Za-z0-9]{20,}|ghp_|github_pat_|$HOME|larkbase|diginno\.app" "$d" \
    --exclude="audit_public.sh" >/dev/null 2>&1; then
    fail "$f chua du lieu nhay cam"
  fi
  say "OK: $(basename "$f") ($(find "$d" -type f | wc -l | tr -d ' ') file)"
done
[ -e dist ] || say "OK: chua co dist (bo qua)"

# 6. Nhac soat thu cong
say "== 6. Soat thu cong"
say "Can doi chieu danh sach ten khach/nhan su noi bo (khong luu danh sach trong repo)."

if [ "$FAIL" -eq 0 ]; then
  say ""
  say "PASS: khong phat hien du lieu nhay cam."
  exit 0
else
  say ""
  say "CO CANH BAO: xem cac dong FAIL o tren."
  exit 1
fi

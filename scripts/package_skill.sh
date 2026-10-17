#!/usr/bin/env bash
# Dong goi .skill sach: loai .git, launch/, dist/ va evals/ (theo mac dinh package_skill).
# Dung: bash scripts/package_skill.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PKG_DIR="${SKILL_CREATOR_DIR:-$HOME/.config/opencode/skills/opencode-admin/creators/skill-creator}"
if [ ! -f "$PKG_DIR/scripts/package_skill.py" ]; then
  echo "Khong tim thay package_skill.py tai: $PKG_DIR" >&2
  echo "Dat bien SKILL_CREATOR_DIR tro toi thu muc skill-creator." >&2
  exit 1
fi

STAGE="$(mktemp -d)"
cleanup() {
  [ -d "$STAGE/.git" ] && mv "$STAGE/.git" "$ROOT/.git"
  [ -d "$STAGE/launch" ] && mv "$STAGE/launch" "$ROOT/launch"
  [ -f "$STAGE/.audit-internal-terms" ] && mv "$STAGE/.audit-internal-terms" "$ROOT/.audit-internal-terms"
  rm -rf "$STAGE"
}
trap cleanup EXIT

# Tam dua .git va launch ra ngoai de khong bi dong goi
[ -d .git ] && mv .git "$STAGE/.git"
[ -d launch ] && mv launch "$STAGE/launch"
[ -f .audit-internal-terms ] && mv .audit-internal-terms "$STAGE/.audit-internal-terms"

# Xoa dist cu de khong bi dong goi long nhau
rm -rf dist
mkdir -p "$STAGE/dist"

PYTHONPATH="$PKG_DIR" python3 "$PKG_DIR/scripts/package_skill.py" "$ROOT" "$STAGE/dist"

mkdir -p "$ROOT/dist"
mv "$STAGE/dist/"*.skill "$ROOT/dist/"
echo "Da tao: dist/opc-vn-business-law.skill"

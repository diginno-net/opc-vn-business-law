#!/usr/bin/env bash
# Build runtime .skill without moving .git or removing dist.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/build_packages.py" --kind skill

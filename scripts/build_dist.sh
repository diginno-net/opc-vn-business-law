#!/usr/bin/env bash
# Build full ZIP with evals/tests, without removing other archives.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/build_packages.py" --kind zip

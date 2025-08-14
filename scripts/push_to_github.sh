#!/usr/bin/env bash
set -euo pipefail
BRANCH=${1:-dev}
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"
git add .
git commit -m "xxos: add dev package (beta)"
git push origin "HEAD:$BRANCH"
echo "Pushed to branch $BRANCH. Please verify on GitHub."

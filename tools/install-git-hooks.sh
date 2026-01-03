#!/usr/bin/env bash
set -euo pipefail
# Install repository git hooks by setting core.hooksPath to .githooks
repo_root=$(git rev-parse --show-toplevel)
if [ -z "$repo_root" ]; then
  echo "Not in a git repository"
  exit 1
fi

hooks_dir="$repo_root/.githooks"
if [ ! -d "$hooks_dir" ]; then
  mkdir -p "$hooks_dir"
fi
# Copy hooks from repo .githooks if not present (they are already in the repo)
# Make sure hooks are executable
chmod +x "$hooks_dir"/* || true

echo "Setting git core.hooksPath to $hooks_dir"
git config core.hooksPath "$hooks_dir"

echo "Hooks installed."

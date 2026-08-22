#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

find "$repo_root/skills" -mindepth 1 -maxdepth 1 -type d -print0 |
  while IFS= read -r -d '' category_dir; do
    test -f "$category_dir/README.md" || {
      echo "Missing category README.md: $category_dir" >&2
      exit 1
    }
  done

find "$repo_root/skills" -mindepth 2 -maxdepth 2 -type d -print0 |
  while IFS= read -r -d '' skill_dir; do
    test -f "$skill_dir/SKILL.md" || {
      echo "Missing SKILL.md: $skill_dir" >&2
      exit 1
    }
    test -f "$skill_dir/README.md" || {
      echo "Missing README.md: $skill_dir" >&2
      exit 1
    }
  done

if find "$repo_root" -type f \( -name '.env*' -o -name '*.pem' -o -name '*.key' -o -iname '*credentials*' \) -print -quit | grep -q .; then
  echo "Potential sensitive file detected." >&2
  exit 1
fi

if rg -l --hidden --glob '!**/.git/**' \
  '(AKIA[0-9A-Z]{16}|github_pat_[A-Za-z0-9_]{50,}|gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9_-]{32,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)' \
  "$repo_root" >/tmp/private-ai-skills-secret-scan.txt; then
  echo "Potential secret content detected:" >&2
  sed -n '1,50p' /tmp/private-ai-skills-secret-scan.txt >&2
  exit 1
fi

echo "PASS: backup structure and secret scan"

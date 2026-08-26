#!/usr/bin/env bash
set -euo pipefail

skills_root="${SKILLS_ROOT:-/root/.codex/skills/remote-skills}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

copy_skill() {
  local category="$1" skill_name="$2" source_file source_dir target_dir
  source_file="$(rg -l "^name: ${skill_name}$" "$skills_root"/skill-*/SKILL.md | head -1)"
  test -n "$source_file" || { echo "Skill not found: $skill_name" >&2; return 1; }
  source_dir="$(dirname "$source_file")"
  target_dir="$repo_root/skills/$category/$skill_name"
  mkdir -p "$(dirname "$target_dir")"
  cp -a "$source_dir/." "$target_dir/"
  find "$target_dir" -type d -name __pycache__ -prune -exec rm -rf {} +
  find "$target_dir" -type f -name '*.pyc' -delete
}

# 新 Skill 加入時，請依主要工作成果加入下列對應分類。
for s in allanyiin-skill-creator-advanced allanyiin-skill-evolution allanyiin-skill-optimizer capability-evolver skill-vault; do copy_skill 01-skill-management "$s"; done
for s in dark-web-intelligence-analysis malware-research-analysis secure-code-review taiwan-isms-audit-expert taiwan-financial-intelligence-radar; do copy_skill 02-cybersecurity "$s"; done
for s in arxiv-research deep-research-writing expert-method-distiller knowledge-method-distiller knowledge-skill-compiler longdoc-evidence-reader textbook-to-md textbook-figure-remap; do copy_skill 03-research-knowledge "$s"; done
for s in oral-expression-coach ethical-persuasion-strategy manipulation-rhetoric-decoder ted-style-speech-coach; do copy_skill 04-speaking-communication "$s"; done
for s in barnum-speech taipei-tm-assistant taipei-tm-chair-coach taipei-tm-evaluator-coach taipei-tm-general-evaluator taipei-tm-speaker-coach taipei-tm-timer-ops; do copy_skill 05-taipei-tm "$s"; done
for s in humanize-text harm-aware-editor longform-writing-process markdown-plus-author technical-documentation-writer; do copy_skill 06-writing-editing "$s"; done
for s in humanize-presentation-visuals slide-content-planner pptx-maker visual-presentation-production mermaid-diagram visual-line-sticker-production blender-control; do copy_skill 07-presentations-visual "$s"; done
for s in financial-statement-analysis taiwan-hidden-champion-radar taiwan-home-buying-guide; do copy_skill 08-finance-property "$s"; done
for s in alternative-solution-designer frontend-design mcp-http-diagnostics problem-decomposer spec-organizer vibe-coding-guidelines; do copy_skill 09-software-problem-solving "$s"; done
for s in video-editing-setup video-editor video-presentation video-short video-short-editor video-social video-subtitle video-travel video-tutorial; do copy_skill 10-video-media "$s"; done
for s in cert-english-coach; do copy_skill 11-learning-exams "$s"; done

python3 "$repo_root/scripts/generate-skill-readmes.py"
"$repo_root/scripts/validate-backup.sh"
echo "Export complete. Review changes before committing."

#!/usr/bin/env python3
"""Generate a human-facing README.md beside every backed-up SKILL.md."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return values


def first_heading(text: str, fallback: str) -> str:
    body = text.split("\n---\n", 1)[-1]
    match = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    return match.group(1) if match else fallback


def clause(description: str, start: str, stops: tuple[str, ...]) -> str:
    pos = description.find(start)
    if pos < 0:
        return ""
    value = description[pos + len(start):]
    stop_positions = [value.find(stop) for stop in stops if value.find(stop) >= 0]
    if stop_positions:
        value = value[: min(stop_positions)]
    return value.strip(" 。；;")


def resource_list(folder: Path) -> list[str]:
    items = ["`SKILL.md`：AI 執行此能力時採用的核心指令"]
    labels = {
        "agents": "介面顯示與觸發設定",
        "references": "按需求載入的參考資料",
        "scripts": "可重複執行的輔助工具",
        "assets": "產出時可使用的素材或範本",
    }
    for name, label in labels.items():
        path = folder / name
        if path.exists():
            count = sum(1 for item in path.rglob("*") if item.is_file())
            items.append(f"`{name}/`：{label}（{count} 個檔案）")
    return items


def build_readme(skill_file: Path) -> str:
    text = skill_file.read_text(encoding="utf-8")
    meta = frontmatter(text)
    name = meta.get("name", skill_file.parent.name)
    title = first_heading(text, name)
    description = meta.get("description", "請參閱 SKILL.md 了解用途與適用情境。")
    version = meta.get("version", "未標示")
    category = skill_file.parent.parent.name

    use_when = clause(description, "Use when", ("Do not use", "成功結果", "Successful output"))
    avoid_when = clause(description, "Do not use", ("成功結果", "Successful output"))
    result = clause(description, "成功結果是", ()) or clause(description, "Successful output", ())

    lines = [
        f"# {title}",
        "",
        description,
        "",
        "## 基本資料",
        "",
        f"- Skill ID：`{name}`",
        f"- 分類：`{category}`",
        f"- 版本：`{version}`",
        "- 主要指令：[SKILL.md](SKILL.md)",
    ]
    if use_when or avoid_when or result:
        lines += ["", "## 使用時機", ""]
        if use_when:
            lines.append(f"- 適合：{use_when}")
        if avoid_when:
            lines.append(f"- 不適合：{avoid_when}")
        if result:
            lines.append(f"- 預期成果：{result}")

    lines += [
        "",
        "## 快速使用",
        "",
        "在支援 Skills 的環境中，可以直接描述任務；若要明確指定，可使用：",
        "",
        "```text",
        f"${name} 請依我的目標與現有資料完成任務，並列出需要我確認的事項。",
        "```",
        "",
        "建議一併提供目標、使用情境、已知資料、限制條件，以及希望取得的成果格式。若資料不足，Skill 會依核心指令只詢問真正影響結果的問題。",
        "",
        "## 內容結構",
        "",
    ]
    lines.extend(f"- {item}" for item in resource_list(skill_file.parent))
    lines += [
        "",
        "## 維護說明",
        "",
        "本 README 供人員瀏覽、搜尋與版本管理；真正影響 AI 行為的是 `SKILL.md` 及其引用的資源。修改功能時，應優先更新核心指令，再重新檢查本說明是否仍一致。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    skill_files = sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    if not skill_files:
        raise SystemExit("No SKILL.md files found")
    for skill_file in skill_files:
        (skill_file.parent / "README.md").write_text(build_readme(skill_file), encoding="utf-8")
    print(f"Generated {len(skill_files)} skill README files")


if __name__ == "__main__":
    main()

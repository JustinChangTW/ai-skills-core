#!/usr/bin/env python3
"""Generate a human-facing README.md beside every backed-up SKILL.md."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"

CATEGORIES = {
    "01-skill-management": ("Skill 管理", "搜尋、建立、檢核、優化與持續演進 AI Skills。"),
    "02-cybersecurity": ("資訊安全", "處理資安稽核、安全程式碼、惡意程式與威脅情資分析。"),
    "03-research-knowledge": ("研究與知識", "進行不限領域的資料蒐集、論文研究、長文件閱讀與方法蒸餾。"),
    "04-speaking-communication": ("口語與溝通", "訓練口語表達、倫理說服，以及辨識巴納姆效應與操弄話術。"),
    "05-taipei-tm": ("台北市健言社", "支援台北市健言社 TM 的講員、講評、總評、主席與計時任務。"),
    "06-writing-editing": ("寫作與編修", "撰寫、自然化與檢查一般文章、長文及技術文件。"),
    "07-presentations-visual": ("簡報與視覺", "規劃簡報、製作 PPTX、自然化版面，以及產生圖像與視覺素材。"),
    "08-finance-property": ("財務、投資與房產", "分析財報、發掘臺灣隱形冠軍，以及協助臺灣自住買房。"),
    "09-software-problem-solving": ("軟體與問題解決", "拆解問題、整理需求、設計軟體介面並診斷技術整合。"),
    "10-video-media": ("影音與媒體", "製作、剪輯、加字幕及轉換簡報、短影音、旅遊與教學影片。"),
}


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


def build_category_readme(category_dir: Path) -> str:
    title, summary = CATEGORIES.get(
        category_dir.name,
        (category_dir.name, "本分類收錄用途相近的 AI Skills。"),
    )
    rows = []
    for skill_file in sorted(category_dir.glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        meta = frontmatter(text)
        name = meta.get("name", skill_file.parent.name)
        display_name = first_heading(text, name)
        description = meta.get("description", "請參閱 Skill 說明。")
        short_description = re.split(
            r"(?:Use when|Do not use|當使用者|常見觸發|成功結果|Successful output)",
            description,
            maxsplit=1,
        )[0].strip(" 。；;")
        rows.append((name, display_name, short_description))

    lines = [
        f"# {title}",
        "",
        summary,
        "",
        f"本分類目前收錄 **{len(rows)} 個 Skills**。若任務跨越多個分類，先依主要交付成果選擇 Skill，再視需要交接其他能力。",
        "",
        "## Skills 清單",
        "",
        "| Skill | 中文名稱 | 主要用途 |",
        "|---|---|---|",
    ]
    for name, display_name, description in rows:
        lines.append(f"| [`{name}`]({name}/README.md) | {display_name} | {description} |")

    lines += [
        "",
        "## 使用方式",
        "",
        "1. 先從上表選擇最接近主要成果的 Skill。",
        "2. 點進 Skill 的 `README.md` 查看用途、適用情境與快速指令。",
        "3. 在支援 Skills 的環境中直接描述任務，或用 `$skill-name` 明確指定。",
        "4. 真正影響 AI 執行行為的是各 Skill 目錄內的 `SKILL.md`。",
        "",
        "回到 [Skills 總目錄](../../CATALOG.md) 或 [版本庫首頁](../../README.md)。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    skill_files = sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    if not skill_files:
        raise SystemExit("No SKILL.md files found")
    for skill_file in skill_files:
        (skill_file.parent / "README.md").write_text(build_readme(skill_file), encoding="utf-8")
    category_dirs = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    for category_dir in category_dirs:
        (category_dir / "README.md").write_text(
            build_category_readme(category_dir), encoding="utf-8"
        )
    print(
        f"Generated {len(skill_files)} skill README files and "
        f"{len(category_dirs)} category README files"
    )


if __name__ == "__main__":
    main()

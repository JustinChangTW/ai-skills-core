#!/usr/bin/env python3
"""Quick structural audit for technical documentation drafts.

This helper is intentionally lightweight. It checks whether a Markdown draft
contains the minimum sections and signals expected for a given doc type.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DOC_TYPE_REQUIREMENTS = {
    "readme": {
        "headings": ["overview", "quick start", "installation", "usage"],
        "tokens": ["```", "prerequisite", "requirements"],
    },
    "tutorial": {
        "headings": ["goal", "prerequisites", "steps", "verify"],
        "tokens": ["```", "step 1", "expected result"],
    },
    "how-to": {
        "headings": ["goal", "prerequisites", "procedure", "verify"],
        "tokens": ["```", "step 1", "troubleshooting"],
    },
    "reference": {
        "headings": ["overview", "parameters", "responses", "errors"],
        "tokens": ["```", "example", "version"],
    },
    "explanation": {
        "headings": ["overview", "why", "trade-offs", "limitations"],
        "tokens": ["because", "context", "decision"],
    },
    "runbook": {
        "headings": ["symptoms", "diagnosis", "remediation", "escalation"],
        "tokens": ["rollback", "alert", "verify"],
    },
    "migration-guide": {
        "headings": ["summary", "breaking changes", "upgrade steps", "rollback"],
        "tokens": ["compatibility", "verify", "known issues"],
    },
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def heading_matches(text: str, heading: str) -> bool:
    variants = {
        "overview": ["overview", "summary", "簡介", "概覽"],
        "quick start": ["quick start", "getting started", "快速開始"],
        "installation": ["installation", "install", "安裝"],
        "usage": ["usage", "how to use", "使用方式"],
        "goal": ["goal", "objective", "目標"],
        "prerequisites": ["prerequisites", "requirements", "前置條件", "需求"],
        "steps": ["steps", "procedure", "步驟", "操作流程"],
        "verify": ["verify", "validation", "驗證"],
        "procedure": ["procedure", "steps", "流程"],
        "troubleshooting": ["troubleshooting", "faq", "排錯", "故障排除"],
        "parameters": ["parameters", "arguments", "參數"],
        "responses": ["responses", "response", "回應"],
        "errors": ["errors", "error handling", "錯誤"],
        "why": ["why", "rationale", "為什麼", "背景"],
        "trade-offs": ["trade-offs", "tradeoffs", "取捨"],
        "limitations": ["limitations", "known issues", "限制"],
        "symptoms": ["symptoms", "alerts", "症狀", "告警"],
        "diagnosis": ["diagnosis", "diagnostics", "診斷"],
        "remediation": ["remediation", "recovery", "修復"],
        "escalation": ["escalation", "handoff", "升級通報"],
        "summary": ["summary", "overview", "摘要"],
        "breaking changes": ["breaking changes", "breaking", "不相容變更"],
        "upgrade steps": ["upgrade steps", "migration steps", "升級步驟"],
        "rollback": ["rollback", "回退", "回滾"],
    }
    tokens = variants.get(heading, [heading])
    return any(token in text for token in tokens)


def audit(text: str, doc_type: str) -> tuple[int, list[str], list[str]]:
    cfg = DOC_TYPE_REQUIREMENTS[doc_type]
    normalized = normalize(text)
    passes: list[str] = []
    failures: list[str] = []
    score = 100

    for heading in cfg["headings"]:
        if heading_matches(normalized, heading):
            passes.append(f"found section signal for '{heading}'")
        else:
            failures.append(f"missing section signal for '{heading}'")
            score -= 15

    for token in cfg["tokens"]:
        if token in normalized:
            passes.append(f"found content signal '{token}'")
        else:
            failures.append(f"missing content signal '{token}'")
            score -= 8

    if "```" not in text and doc_type in {"readme", "tutorial", "how-to", "reference", "runbook", "migration-guide"}:
        failures.append("no fenced code block found for a procedural or technical document")
        score -= 10

    if len(text.splitlines()) < 12:
        failures.append("draft is too short to be a complete technical document")
        score -= 10

    return max(score, 0), passes, failures


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a Markdown draft for technical doc signals")
    parser.add_argument("path", help="Path to a Markdown draft")
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(DOC_TYPE_REQUIREMENTS.keys()),
        help="Primary document type to audit against",
    )
    args = parser.parse_args()

    path = Path(args.path).resolve()
    text = path.read_text(encoding="utf-8")
    score, passes, failures = audit(text, args.type)

    print(f"Document type: {args.type}")
    print(f"Score: {score}/100")
    print("")
    print("Passes:")
    for item in passes:
        print(f"- {item}")
    print("")
    print("Failures:")
    for item in failures:
        print(f"- {item}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

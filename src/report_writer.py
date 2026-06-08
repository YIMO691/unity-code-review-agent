"""Markdown report writer for Unity code review findings."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from src.scanner import Finding


DISCLAIMER = "以下均为疑似风险，不代表一定是 bug。每条命中都需要结合上下文进行人工验证。"


def write_report(
    findings: list[Finding],
    output_dir: Path,
    scanned_files: list[Path],
    rule_version: str,
) -> Path:
    """Write a Markdown report and return its path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    report_name = _report_name(scanned_files)
    report_path = output_dir / report_name
    report_path.write_text(
        build_report(findings, scanned_files, rule_version),
        encoding="utf-8",
    )
    return report_path


def build_report(
    findings: list[Finding],
    scanned_files: list[Path],
    rule_version: str,
) -> str:
    """Build the Markdown report body."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    severity_counts = Counter(finding.severity for finding in findings)
    by_file: dict[Path, list[Finding]] = defaultdict(list)
    for finding in findings:
        by_file[finding.file_path].append(finding)

    lines: list[str] = [
        "# Unity C# 代码审计报告",
        "",
        "## 1. 文件信息",
        "",
        f"- 扫描时间：{now}",
        f"- 扫描规则版本：{rule_version}",
        f"- 扫描文件数：{len(scanned_files)}",
        "- 文件路径：",
    ]
    lines.extend(f"  - `{path}`" for path in scanned_files)
    lines.extend(
        [
            "",
            "## 2. 重要提示",
            "",
            DISCLAIMER,
            "",
            "## 3. 总体结论",
            "",
            f"本次共发现 {len(findings)} 个疑似风险点。",
            "",
            f"- HIGH：{severity_counts.get('HIGH', 0)}",
            f"- WARNING：{severity_counts.get('WARNING', 0)}",
            f"- INFO：{severity_counts.get('INFO', 0)}",
            "",
            "## 4. 疑似风险列表",
            "",
        ]
    )

    if not findings:
        lines.extend(["未发现规则命中的疑似风险。", ""])
    else:
        counter = 1
        for file_path, file_findings in by_file.items():
            lines.extend([f"### {file_path}", ""])
            for finding in file_findings:
                lines.extend(
                    [
                        f"#### 风险 {counter}：{finding.rule_name}",
                        "",
                        f"- 规则 ID：`{finding.rule_id}`",
                        f"- 风险等级：{finding.severity}",
                        f"- 命中位置：第 {finding.line_number} 行",
                        f"- 命中代码：`{finding.code}`",
                        f"- 为什么可能有问题：{finding.description}",
                        f"- 建议修改方式：{finding.suggestion}",
                        "- 是否需要人工确认：是",
                        "",
                    ]
                )
                counter += 1

    lines.extend(
        [
            "## 5. 人工验证记录",
            "",
            "| # | 文件 | 行号 | 规则 | 命中代码 | 判断 | 说明 |",
            "|---|---|---:|---|---|---|---|",
        ]
    )
    if findings:
        for index, finding in enumerate(findings, start=1):
            code = finding.code.replace("|", "\\|")
            lines.append(
                f"| {index} | `{finding.file_path}` | {finding.line_number} | {finding.rule_name} | `{code}` | 有效 / 误报 / 需上下文 |  |"
            )
    else:
        lines.append("| - | - | - | - | - | - | - |")

    lines.extend(
        [
            "",
            "## 6. 可沉淀规则",
            "",
            "- 本节由人工验证后填写：哪些规则有效、哪些需要降低等级、哪些需要增加上下文判断。",
            "",
            "## 7. 面试表达",
            "",
            "- 本节由人工验证后填写：如何用项目案例说明 Unity 性能审计和 AI Agent 辅助开发流程。",
            "",
        ]
    )

    return "\n".join(lines)


def _report_name(scanned_files: list[Path]) -> str:
    if len(scanned_files) == 1:
        return f"{scanned_files[0].stem}_review.md"
    return "unity_code_review.md"

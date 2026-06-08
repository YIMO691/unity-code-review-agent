"""Static text scanner for Unity C# review rules."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Iterable


UNITY_METHODS = {"Update", "LateUpdate", "FixedUpdate"}


@dataclass(frozen=True)
class Rule:
    id: str
    name: str
    severity: str
    description: str
    patterns: tuple[str, ...]
    suggestion: str
    scope_check: tuple[str, ...] = ()
    release_patterns: tuple[str, ...] = ()
    file_exclusion_patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class Finding:
    file_path: Path
    line_number: int
    code: str
    rule_id: str
    rule_name: str
    severity: str
    description: str
    suggestion: str
    needs_manual_verification: bool = True


def load_rules(path: Path) -> tuple[str, list[Rule]]:
    """Load scanner rules from a JSON file."""
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    rules = []
    for item in data.get("rules", []):
        rules.append(
            Rule(
                id=item["id"],
                name=item["name"],
                severity=item["severity"],
                description=item["description"],
                patterns=tuple(item.get("patterns", [])),
                suggestion=item.get("suggestion", ""),
                scope_check=tuple(item.get("scope_check", [])),
                release_patterns=tuple(item.get("release_patterns", [])),
                file_exclusion_patterns=tuple(item.get("file_exclusion_patterns", [])),
            )
        )

    return data.get("version", "unknown"), rules


def collect_cs_files(input_path: Path) -> list[Path]:
    """Return one C# file or all C# files under a directory."""
    if input_path.is_file():
        if input_path.suffix.lower() != ".cs":
            raise ValueError(f"Input file is not a .cs file: {input_path}")
        return [input_path]

    if input_path.is_dir():
        return sorted(input_path.rglob("*.cs"))

    raise FileNotFoundError(f"Input path does not exist: {input_path}")


def scan_path(input_path: Path, rules: Iterable[Rule]) -> list[Finding]:
    """Scan a file or directory and return all findings."""
    findings: list[Finding] = []
    for cs_file in collect_cs_files(input_path):
        findings.extend(scan_file(cs_file, rules))
    return findings


def scan_file(file_path: Path, rules: Iterable[Rule]) -> list[Finding]:
    """Scan one C# file with the supplied rules."""
    lines = file_path.read_text(encoding="utf-8").splitlines()
    method_ranges = _find_method_ranges(lines, UNITY_METHODS)
    full_text = "\n".join(lines)

    findings: list[Finding] = []
    for line_index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue

        for rule in rules:
            if rule.file_exclusion_patterns and _has_release_pattern(full_text, rule.file_exclusion_patterns):
                continue
            if rule.scope_check and not _line_in_scope(line_index, method_ranges, rule.scope_check):
                continue
            if rule.release_patterns and _has_release_pattern(full_text, rule.release_patterns):
                continue
            if _matches_rule(stripped, rule):
                findings.append(
                    Finding(
                        file_path=file_path,
                        line_number=line_index,
                        code=stripped,
                        rule_id=rule.id,
                        rule_name=rule.name,
                        severity=rule.severity,
                        description=rule.description,
                        suggestion=rule.suggestion,
                    )
                )

    return findings


def _matches_rule(text: str, rule: Rule) -> bool:
    if rule.id == "U003":
        return _matches_event_registration(text)
    return any(re.search(pattern, text) for pattern in rule.patterns)


def _matches_event_registration(text: str) -> bool:
    if re.search(r"AddListener\s*\(", text):
        return True

    if "+=" not in text:
        return False

    match = re.search(
        r"(?P<left>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\s*\+=\s*(?P<right>[^;]+)",
        text,
    )
    if match is None:
        return False

    left = match.group("left")
    right = match.group("right").strip()
    if _looks_like_simple_accumulation(right):
        return False

    return "." in left and _looks_like_callback(right)


def _looks_like_simple_accumulation(expression: str) -> bool:
    return bool(
        re.fullmatch(r"[-+]?\d+(?:\.\d+)?[fFdDmM]?", expression)
        or re.fullmatch(r"\".*\"", expression)
        or re.fullmatch(r"'.*'", expression)
        or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\s*[+\-*/]\s*[A-Za-z_0-9.]+)+", expression)
    )


def _looks_like_callback(expression: str) -> bool:
    return bool(
        re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?", expression)
        or "=>" in expression
        or expression.startswith("delegate")
    )


def _has_release_pattern(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def _line_in_scope(
    line_number: int,
    method_ranges: dict[str, list[tuple[int, int]]],
    method_names: Iterable[str],
) -> bool:
    for method_name in method_names:
        for start, end in method_ranges.get(method_name, []):
            if start <= line_number <= end:
                return True
    return False


def _find_method_ranges(
    lines: list[str],
    method_names: set[str],
) -> dict[str, list[tuple[int, int]]]:
    ranges: dict[str, list[tuple[int, int]]] = {name: [] for name in method_names}
    signature_pattern = re.compile(
        rf"\b(?:public|private|protected|internal)?\s*(?:virtual|override|async|static)?\s*void\s+({'|'.join(method_names)})\s*\("
    )

    index = 0
    while index < len(lines):
        line = lines[index]
        match = signature_pattern.search(line)
        if not match:
            index += 1
            continue

        method_name = match.group(1)
        start_line = index + 1
        brace_depth = 0
        found_open_brace = False
        scan_index = index

        while scan_index < len(lines):
            code_line = _strip_line_comment(lines[scan_index])
            brace_depth += code_line.count("{")
            if "{" in code_line:
                found_open_brace = True
            brace_depth -= code_line.count("}")

            if found_open_brace and brace_depth <= 0:
                ranges[method_name].append((start_line, scan_index + 1))
                break

            scan_index += 1

        index = max(scan_index + 1, index + 1)

    return ranges


def _strip_line_comment(line: str) -> str:
    return line.split("//", 1)[0]

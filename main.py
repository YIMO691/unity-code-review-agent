"""Command line entry point for unity-code-review-agent-v0."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from src.scanner import collect_cs_files, load_rules, scan_path
from src.report_writer import write_report


DEFAULT_RULES = Path("rules/unity_rules.json")
DEFAULT_OUTPUT = Path("reports")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan Unity C# files for suspicious review signals and generate a Markdown report."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        help="Path to a Unity .cs file or a directory containing .cs files.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUTPUT,
        type=Path,
        help="Directory for generated Markdown reports.",
    )
    parser.add_argument(
        "--rules",
        "-r",
        default=DEFAULT_RULES,
        type=Path,
        help="Path to unity_rules.json.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print scanner version and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.version:
        print("unity-code-review-agent-v0 0.1.1")
        return 0
    if args.input is None:
        print("Error: --input/-i is required unless --version is used.", file=sys.stderr)
        return 1

    try:
        rule_version, rules = load_rules(args.rules)
        scanned_files = collect_cs_files(args.input)
        findings = scan_path(args.input, rules)
        report_path = write_report(findings, args.output, scanned_files, rule_version)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Scanned files: {len(scanned_files)}")
    print(f"Findings: {len(findings)}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# unity-code-review-agent-v0

A minimal Unity C# static review tool for interview teaching and manual review practice.

```text
Unity C# file -> static rule scan -> Markdown review report -> manual validation
```

## Positioning

This project is a small, inspectable v0 tool. It is useful for practicing Unity client code review, preparing interview explanations, and turning review findings into reusable rules.

It is not a production CI gate, not a Roslyn analyzer, and not a semantic C# analyzer. Every finding is a suspicious signal that must be checked by a human reviewer.

## What It Does

- Scans one `.cs` file or a directory of `.cs` files.
- Detects five Unity client review signals.
- Generates a Markdown report with line numbers and manual validation rows.
- Keeps v0 zero-dependency and standard-library-only.
- Avoids modifying Unity source files.

## Rules

| ID | Name | Severity | Notes |
|---|---|---|---|
| U001 | Update 中疑似频繁 GetComponent | HIGH | Checks `Update`, `LateUpdate`, and `FixedUpdate`. |
| U002 | 帧循环中疑似使用 LINQ | WARNING | Checks frame-loop LINQ-like calls; excludes `using R3;` and `using UniRx;` files. |
| U003 | 疑似事件注册，需检查解绑 | HIGH | Flags `AddListener` and event-style `+=`; ordinary arithmetic `+=` is filtered. |
| U004 | 疑似 Resources.Load 使用 | WARNING | Prompts a project resource-policy review. |
| U005 | 疑似 Addressables 加载，需检查释放策略 | WARNING | Suppresses same-file hits when obvious `Addressables.Release` calls exist. |

## Quick Start

Run from the project directory:

```powershell
python main.py --input examples/InventoryView.cs --output reports/
```

Expected output:

```text
Scanned files: 1
Findings: 6
Report: reports\InventoryView_review.md
```

Scan a directory:

```powershell
python main.py --input path\to\UnityProject\Assets\Scripts --output reports/
```

Print version:

```powershell
python main.py --version
```

## Report Workflow

1. Run the scanner.
2. Open the generated Markdown report.
3. Mark each finding as `有效`, `误报`, or `需上下文`.
4. Record false positives in [docs/false_positives.md](docs/false_positives.md).
5. Move stable lessons into [docs/unity_review_rules.md](docs/unity_review_rules.md).

The generated files under `reports/` are local validation artifacts and are ignored by Git. A stable sample is available at [docs/sample_inventory_review.md](docs/sample_inventory_review.md).

## Verified Sample

The sample `examples/InventoryView.cs` is intentionally compact and teaching-oriented. It produces six findings:

```text
U003 x2: event registration review
U001 x1: GetComponent in Update
U002 x1: LINQ-like call in Update
U004 x1: Resources.Load
U005 x1: Addressables load without visible release
```

Manual validation notes are kept in [docs/inventory_view_manual_validation.md](docs/inventory_view_manual_validation.md).

## Real Project Validation

v0.1.1 was checked against completed Unity learning projects under `projects/verified`:

| File | Result | Meaning |
|---|---:|---|
| `AddressablesDemo/.../PrefabSpawner.cs` | 0 findings | Correctly silent; release paths are visible. |
| `UniTaskDemo/.../CooldownButton.cs` | 1 finding | U003 needs context; Button + UniTask lifetime is a softer signal. |
| `R3Demo/.../ReactiveHealth.cs` | 0 findings | R3 `.Where()` false positives were fixed in v0.1.1. |

## Tests

Run:

```powershell
python -m unittest discover -s tests
```

Expected:

```text
Ran 16 tests
OK
```

The tests cover empty files, method-scope checks, event registration vs arithmetic `+=`, Addressables release suppression, R3/UniRx exclusions, and generated sample coverage.

## Project Structure

```text
unity-code-review-agent-v0/
├── main.py
├── src/
│   ├── scanner.py
│   ├── report_writer.py
│   └── llm_client.py
├── rules/
│   └── unity_rules.json
├── examples/
│   └── InventoryView.cs
├── docs/
│   ├── false_positives.md
│   ├── inventory_view_manual_validation.md
│   ├── sample_inventory_review.md
│   └── unity_review_rules.md
└── tests/
```

`src/llm_client.py` is intentionally a v1 placeholder. v0 does not call any LLM API.

## Limitations

- Text-level heuristic scanning only.
- No C# AST or semantic analysis.
- No Unity Editor integration.
- No automatic fixes.
- No LLM, LangChain, RAG, LangGraph, or MCP integration.
- Findings should not be treated as confirmed bugs.

## License

MIT License. See [LICENSE](LICENSE).

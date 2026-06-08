# Changelog

## 0.1.1 - 2026-06-08

- Changed U002 from a whole-file LINQ signal to a frame-loop LINQ signal.
- Added U002 scope checks for `Update`, `LateUpdate`, and `FixedUpdate`.
- Added file-level U002 exclusions for `using R3;` and `using UniRx;` to avoid reactive-chain false positives.
- Added regression tests for R3 `.Where()` chains and `LateUpdate` LINQ usage.
- Added manual validation records for the sample `InventoryView.cs` report.
- Clarified README positioning: v0 is an interview teaching and manual review practice tool, not a CI gate.

## 0.1.0 - 2026-06-08

- Added the first minimal Unity C# static review loop.
- Added five v0 rules:
  - U001: `GetComponent` inside frame-loop methods.
  - U002: LINQ-like calls.
  - U003: event registration requiring unsubscribe review.
  - U004: `Resources.Load` usage.
  - U005: Addressables load requiring release review.
- Added Markdown report generation.
- Added sample Unity script `examples/InventoryView.cs`.
- Added standard-library unit tests.

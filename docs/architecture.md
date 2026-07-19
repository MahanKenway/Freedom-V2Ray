# Architecture

Freedom-V2Ray keeps the production update path small and predictable:

1. `src.main` loads settings and sources.
2. `ConfigCollector` fetches source content, parses configs, and delegates reachability checks.
3. `ConfigExporter` writes raw and base64 subscription files under `configs/`.
4. `TelegramNotifier` optionally sends a summary.

## Safety boundaries

- Parsing should remain side-effect free.
- Static validation should not perform DNS, socket, HTTP, subprocess, or shell operations.
- Reachability checks should stay isolated in the tester layer.
- Generated outputs should be clearly separated from source code.
- New experimental features should be introduced behind configuration or as standalone modules before being wired into the scheduled update path.

## Current scheduled update path

The two-hour GitHub Actions workflow runs `python -m src.main`. New modules in this documentation set are additive helpers and do not change that workflow by themselves.

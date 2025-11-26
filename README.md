# Image Research Assistant

This is an image research assistant focused on helping with image-related information retrieval and enrichment using modular services. The repository contains a lightweight application entry point, client/agent scaffolding, and service modules for vision and Wikipedia lookups.

## Goals

- Provide a compact, extensible architecture for image research tasks using MCP services.
- Keep services modular so contributors can add new data sources or models.
- Provide simple developer ergonomics for running and testing locally.

## Contents

- `src/app/` — main application package and entry point
- `src/app/clients/` — client-side agent and MCP client code
- `src/app/servers/vision/` — vision-related server utilities and server
- `src/app/servers/wikipedia/` — wikipedia lookup server and helpers

## Prerequisites

- macOS/Linux/Windows with a POSIX-like shell (examples use `zsh`/`bash`)
- Python 3.10 or newer
- Git
- (Optional) `poetry` if you prefer managing the project via Poetry. Though `uv` is the preferred package manager for this project.

## Recommended setup

1. Create and activate a virtual environment (macOS/Linux):

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

  If using `uv`, simply run `uv venv` after installation to activate the environment.

2. Install dependencies. Preferred project methods:

- Use the Makefile helper (recommended):

 ```bash
 make install
 ```

- Or use `uv` (preferred package manager for this project) to install from `pyproject.toml`:

 ```bash
 uv install -r pyproject.toml
 ```

If you prefer, you can still perform an editable pip install when iterating on local code:

```bash
pip install -e .
```

Note: There is no `requirements.txt` in this repository; use `pyproject.toml` with `uv` or the `Makefile` helper.

## Running the project

- Run the main application directly (quick):

 ```bash
 python src/app/main.py
 ```

- Or run as a module after editable install:

 ```bash
 make run
 ```

## Project considerations

- The repository is intentionally modular: add new `servers/` or `clients/` components without touching core logic.
- Keep third-party model or API keys out of the repo — use environment variables or a secrets store for credentials.
- Aim for lightweight dependencies to keep the project easy to set up for contributors.
- If adding long-running services, prefer running them behind a process manager (systemd, supervisor) or in containers for production.

## Testing

- There are no tests bundled by default. If you add tests, prefer `pytest` and place tests under `tests/`.
- Example test run (after adding `pytest` to deps):

 ```bash
 pytest -q
 ```

## Contributing

- Fork the repository and create feature branches: `git checkout -b feat/your-feature`
- Keep commits small and focused, with clear messages.
- Run linters and any tests you add before opening a PR.
- Open a Pull Request against `main`, add a descriptive title and summary of changes.
- For larger changes, open an issue first to discuss design and approach.

## Code style

- Follow idiomatic Python (PEP8). Optionally add `black` / `ruff` or similar tools to the project for consistency. Ruff is used here and can be run using `make lint` and type checking with `make pyrefly`.

## Contact / Maintainers

- The main repo owner is `BrianLusina` (GitHub: `BrianLusina`). Open issues or PRs for questions, fixes, or feature requests.

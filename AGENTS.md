AGENTS / CONTRIBUTOR GUIDE

This document is intended for contributors, bots, and agents that will run, test, and make changes to the `image-research-assistant` repository.

Quick summary

- Run the app locally using a virtual environment and an editable install.
- Run individual servers for focused development (vision, wikipedia).
- Add tests with `pytest` and keep changes small and well-documented.

Environment setup

1. Clone the repository and change into it:

 ```bash
 git clone <repo-url>
 cd image-research-assistant
 ```

2. Create and activate a virtual environment (macOS/Linux):

 ```bash
 python3 -m venv .venv
 source .venv/bin/activate
 ```

3. Install dependencies (preferred methods):

- Use the Makefile helper (recommended):

 ```bash
 make install
 ```

- Or use `uv` (preferred package manager for this project) to install from `pyproject.toml`:

 ```bash
 uv install -r pyproject.toml
 ```

If you prefer an editable pip install for local iteration, you can still run:

```bash
pip install -e .
```

Running the application

- Run the primary entrypoint for local manual testing:

  ```bash
  python src/app/main.py
  ```

- If you installed editable, you can run:

  ```bash
  python -m app.main
  ```

- To run a specific server directly while developing that component:

  ```bash
  python -m app.servers.vision.server
  python -m app.servers.wikipedia.server
  ```

Testing

- There are no tests by default. When you add tests, prefer `pytest` and put them under `tests/`.
- Example test command:

  ```bash
  pytest -q
  ```

How to make changes (developer workflow)

1. Create a feature branch from `main`:

 ```bash
 git checkout -b feat/short-description
 ```

2. Make small, focused commits. Keep each commit addressing a single concern.

3. Run unit tests and linters locally before pushing.

4. Push your branch and open a Pull Request to `main` with a clear description, motivation, and testing notes:

 ```bash
 git push origin feat/short-description
 ```

Code review and merging

- Create a PR and request reviews from maintainers.
- Address review feedback by pushing new commits to the same branch.
- Squash or rebase as appropriate so the PR contains a clear history.
- Merge when approvals are in place and CI (if any) is passing.

Notes for automated agents

- Do not commit credentials or secrets. Use environment variables or a secure secret store.
- Keep PRs small to make automated and human review easier.
- When running integration tests that hit external services, support toggling live vs mocked behavior via environment variables.

Suggested files and locations for common tasks

- Add tests in `tests/`.
- Add reusable utilities to `src/app/` under appropriate subpackages.
- Documentation changes should update `README.md` and this `AGENTS.md`.

If you'd like, ask me to add a CI workflow (GitHub Actions) that runs tests and linting on PRs.

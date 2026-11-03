# Local development

Install the development dependencies and activate the Git hooks after cloning:

```sh
uv sync --locked
uv run --locked pre-commit install
```

Every commit runs the full Python and notebook test suites locally. The notebook tests run serially because some examples use subprocesses and shared execution state. A failing test blocks the commit. Pre-commit tests the staged changes and temporarily stashes unstaged changes.

Run the hooks manually before committing:

```sh
uv run --locked pre-commit run --all-files
```

Run either suite separately:

```sh
uv run --locked pytest -q
uv run --locked nbdev-test --n-workers 0 --pause 1
```

GitHub Actions only builds and deploys the documentation on pushes to `main` or manual dispatch. The deployment runs `nbdev-docs` and publishes `_docs` to the `gh-pages` branch, which is the repository's existing Pages source. It does not run either test suite.

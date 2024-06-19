# Pyboot

This is a simple Python application template for Python projects designed to streamline your development workflow.

Features include:

- Dependency management with Poetry: https://python-poetry.org/: Poetry provides a powerful way to manage project dependencies, creating isolated environments and handling version conflicts.
- Code formatting with Black: https://black.readthedocs.io/en/stable/: Black enforces consistent, opinionated code formatting, enhancing readability and collaboration.
- Linting with Ruff: [invalid URL removed]: Ruff helps find potential bugs, stylistic issues, and maintain a clean codebase.
  Unit testing with Pytest: https://docs.pytest.org/en/latest/: Pytest provides a flexible and popular framework for writing and running tests that ensure your code's correctness.
- Changelog management with towncrier: https://towncrier.readthedocs.io/en/latest/: Maintain well-structured changelogs to track project changes.
- Automation script management with Node and/or Python: Streamline common tasks (e.g., building, testing, deploying) with customizable scripts.
- Pre- and post-commit sanity checks with Husky: https://typicode.github.io/husky/: Enforce quality standards at commit time to catch issues early.
- Documentation creation with MkDocs: https://www.mkdocs.org/: Easily create beautiful technical documentation for your project.

## Setup

1. Create a copy of the template

```bash
gh repo create happy-bog --template git@github.com:evannagle/pyboot.git  --private --clone
```

2. Install dependencies

```bash
cd happy-bog

make install
```

3. Rename the app

```bash
make rename
```

4. Run the app

```bash
make app
```

Which should output:

```bash

🤖 Cleaning up
rm -rf __pycache__ .pytest_cache .coverage .mypy_cache .tox .eggs .venv

🤖 Building the project
poetry install
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: pyboot (0.1.0)

🤖 Running the app
poetry run pyboot
42
```

5. Test the app

```bash
make test
```

6. Review test coverage

```bash
make coverage
```

7. Globalize the command for use from your command line

```bash
make globalize

happy-bog

> 42
```

# Contributing

Thanks for helping improve senior-agent-skills. Contributions should make the playbooks clearer, safer, or more portable without tying them to one coding harness.

## Before opening an issue

- Search existing issues before creating a new one.
- Use the bug report form for incorrect or unsafe behavior.
- Use the feature request form for a new playbook, rule, or supported harness.
- Report security problems privately as described in [SECURITY.md](SECURITY.md).

## Local setup

There are no project dependencies to install. Clone your fork, then run:

```bash
cd senior-agent-skills
bash -n install.sh
python scripts/validate_repo.py
```

You can test an isolated installation without changing your home directory:

```bash
repo_root="$PWD"
workdir="$(mktemp -d)"
cd "$workdir"
"$repo_root/install.sh" --project --copy
```

## Changing a skill

Each skill lives at `skills/<name>/SKILL.md` and contains YAML frontmatter followed by the playbook.

- Keep the folder name and frontmatter `name` identical.
- Treat the `description` as a trigger. Say when the skill should run and keep its scope distinct from the other skills.
- Keep instructions tool-agnostic unless the skill is explicitly about one tool.
- Prefer concrete checks and observable evidence over broad advice.
- Update the skill index in `README.md` and `AGENTS.md` when adding or removing a skill.
- Update `RUNBOOK.md` when installation or harness behavior changes.

## Pull requests

Keep pull requests focused. Explain the problem, the behavior change, and how you verified it. Include examples when wording changes could affect when a skill triggers.

Before submitting:

- Run `bash -n install.sh`.
- Run `python scripts/validate_repo.py`.
- Review the complete diff for unrelated edits.
- Confirm that new Markdown links resolve.
- Confirm that no machine-specific paths, credentials, or generated files were added.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

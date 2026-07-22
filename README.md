# senior-agent-skills

<div align="center">
<pre>
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░█░▄▄█░▄▄▀██▄██▀▄▄▀█░▄▄▀███░▄▄▀█░▄▄▄█░▄▄█░▄▄▀█▄░▄████░▄▄▄░█░█▀██▄██░██░██░▄▄
██▄▄▄▀▀█░▄▄█░██░██░▄█░██░█░▀▀▄███░▀▀░█░█▄▀█░▄▄█░██░██░█████▄▄▄▀▀█░▄▀██░▄█░██░██▄▄▀
██░▀▀▀░█▄▄▄█▄██▄█▄▄▄██▄▄██▄█▄▄███░██░█▄▄▄▄█▄▄▄█▄██▄██▄█████░▀▀▀░█▄█▄█▄▄▄█▄▄█▄▄█▄▄▄
</pre>

![Eight playbooks](https://img.shields.io/badge/PLAYBOOKS-8-1f6feb?style=for-the-badge)
![Agent Skills](https://img.shields.io/badge/FORMAT-SKILL.md-238636?style=for-the-badge)
![No dependencies](https://img.shields.io/badge/DEPENDENCIES-NONE-d29922?style=for-the-badge)

[Quick start](#quick-start) | [The eight skills](#the-eight-skills) | [Repo layout](#repo-layout) | [Tuning](#tuning-for-your-team) | [Contributing](#contributing) | [Limitations](#honest-limitations)

</div>

Eight portable playbooks that make a coding agent behave like a careful senior engineer instead of an enthusiastic intern. They cover the whole loop: understand the repo, plan the risky stuff, build test-first, debug like a scientist, refactor without breaking things, review your own diff, prove the work is actually done, and keep git history clean.

Each one is a plain `SKILL.md` file following the Agent Skills open standard, so the same folder works in Claude Code, Codex CLI, Google Antigravity, OpenCode, GitHub Copilot, Cursor, and anything else that reads the format. Tools reading the `~/.agents/skills/` interop path (Amp, Cline, and a growing list) are covered automatically. For the rare harness that only reads `AGENTS.md`, there's a drop-in index that gets you the same behavior manually.

---

## Quick start

Clone or download the repository, then run:

```bash
cd senior-agent-skills
./install.sh
```

That symlinks every skill into `~/.claude/skills/`, `~/.codex/skills/`, Antigravity's global path `~/.gemini/config/skills/`, the legacy `~/.gemini/skills/` (enterprise Gemini CLI only, since Google retired the consumer tiers on June 18, 2026), and the interop path `~/.agents/skills/`. Symlinks mean you edit one canonical copy and every harness picks it up. OpenCode needs no directory of its own: it natively scans both the `.claude/skills` and `.agents/skills` paths (project and global), so it's covered twice over by this install. Use `--copy` if you'd rather have independent copies, or `--project` to install into the current repo instead of your home directory.

> [!IMPORTANT]
> Then start a fresh agent session so it rescans its skills. That's it.

> [!NOTE]
> **For AGENTS.md-only harnesses:** vendor the `skills/` folder into your repo and paste the table from this repo's `AGENTS.md` into your project's `AGENTS.md`. The agent reads the index, sees a task match, and opens the playbook itself.

> [!NOTE]
> **For GitHub Copilot:** Copilot is repo-scoped, so run `./install.sh --project` from inside your repo. That writes `.github/skills/` (Copilot's native path), which you then commit so the whole team gets the skills on clone. Copilot also auto-reads a repo's `.claude/skills/`, so a project install covers it twice.

---

## Why skills and not one giant AGENTS.md

Think of a restaurant. The menu is short: dish names and one-line descriptions. The recipe book in the kitchen is enormous, but the cook only opens the page for the dish that actually got ordered.

Skills work the same way. The agent always carries the menu (each skill's name and description, roughly a hundred tokens apiece). Only when a task matches does it load the full playbook into context. Stuff all eight playbooks into AGENTS.md instead and you pay for every word on every single prompt, and past a certain wall-of-text size the agent starts skimming anyway. The loading trick has a name, progressive disclosure, and it's the main reason the format scales past three or four skills.

---

## The eight skills

| Skill | Fires when | The rule it enforces |
|:---|:---|:---|
| [`repo-recon`](skills/repo-recon/SKILL.md) | you land in unfamiliar code | map before you touch |
| [`plan-first`](skills/plan-first/SKILL.md) | the change is wide, deep, or irreversible | plans are cheaper than rework |
| [`tdd-loop`](skills/tdd-loop/SKILL.md) | building features or fixing bugs | red, then green, never fake the green |
| [`debug-protocol`](skills/debug-protocol/SKILL.md) | something's broken, cause unknown | reproduce first, one hypothesis at a time |
| [`safe-refactor`](skills/safe-refactor/SKILL.md) | restructuring without behavior change | small steps, tests between each |
| [`self-review`](skills/self-review/SKILL.md) | the diff is finished | read it like a hostile reviewer |
| [`verify-done`](skills/verify-done/SKILL.md) | you're about to say "done" | evidence or it didn't happen |
| [`git-hygiene`](skills/git-hygiene/SKILL.md) | anything touches version control | atomic commits, no destructive surprises |

They map to phases of one loop, so on a typical feature the agent might touch four of them: recon, tdd-loop, self-review, verify-done. On a gnarly production bug: debug-protocol, tdd-loop (for the regression test), verify-done, git-hygiene. They reference each other where the phases connect.

Why eight and not twenty? Because triggering degrades as the catalog grows. Every skill's description sits in context competing for the agent's attention, and once descriptions start overlapping, the agent picks the wrong one or none at all. Eight non-overlapping phases is about the ceiling before you need to start splitting by domain.

---

## Repo layout

```text
senior-agent-skills/
|-- README.md                  you are here
|-- RUNBOOK.md                 install, trigger, and debug guide
|-- BLOG.md                    the ideas behind the pack
|-- AGENTS.md                  fallback index for skills-aware agents
|-- CONTRIBUTING.md            contributor workflow
|-- CODE_OF_CONDUCT.md         community standards
|-- SECURITY.md                private reporting policy
|-- install.sh                 symlink/copy installer
|-- scripts/validate_repo.py   dependency-free repository checks
|-- .github/
|   |-- ISSUE_TEMPLATE/        structured bug and feature reports
|   |-- pull_request_template.md
|   \-- workflows/validate.yml
\-- skills/
    |-- repo-recon/SKILL.md
    |-- plan-first/SKILL.md
    |-- tdd-loop/SKILL.md
    |-- debug-protocol/SKILL.md
    |-- safe-refactor/SKILL.md
    |-- self-review/SKILL.md
    |-- verify-done/SKILL.md
    \-- git-hygiene/SKILL.md
```

Each skill is just a folder with a `SKILL.md`: YAML frontmatter (`name` + `description`) on top, markdown instructions below. The description is the trigger; the body is the playbook. No scripts, no dependencies, nothing to build.

---

## Tuning for your team

- **Triggering feels off?** Edit the `description` in the frontmatter, that's the entire matching mechanism. Make it pushier ("use this whenever...") if a skill undertriggers, narrower if it fires on everything.
- **House rules?** Add them to the relevant skill body. Your commit convention goes in `git-hygiene`, your test framework quirks in `tdd-loop`. Keep each file well under 500 lines; past that, agents skim.
- **Per-project overrides:** most harnesses let project-level skills shadow user-level ones with the same name. Vendor a modified copy into `.claude/skills/` (or the equivalent) of the repo that needs it.

---

## Honest limitations

- Harness support for the standard moves fast and paths occasionally shift. If a symlink target here doesn't match your harness version, check its docs for the current skills directory; the SKILL.md files themselves won't need changes.
- Skills are instructions, not enforcement. An agent can still ignore a playbook under pressure. For hard guarantees on the destructive-git side, pair `git-hygiene` with your harness's permission or hook system.
- These are deliberately tool-agnostic, which means no harness-specific tricks (subagents, hooks, MCP calls). That's the price of portability, and for methodology skills it's the right trade.

---

## Contributing

PRs welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request, use the structured issue forms for bugs and feature requests, and report vulnerabilities privately through [SECURITY.md](SECURITY.md).

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

---

<div align="center">

**Map first. Test the change. Prove it works.**

</div>
---
name: repo-recon
description: Systematically map an unfamiliar codebase before changing anything in it. Use this whenever work starts in a repo, service, or module that has not been explored in the current session, when the user says things like "new codebase", "help me understand this project", "onboard me", or before any non-trivial change where the surrounding code is unknown. Also reach for it after a change failed because of a wrong assumption about project structure or conventions.
---

# Repo Recon

Map before you touch. Most agent failures in unfamiliar code are not bad logic, they are wrong assumptions: editing the wrong file, reimplementing a helper that already exists, or writing code in a style the project rejects. Fifteen minutes of recon is cheaper than one wrong-direction diff.

## The recon pass

Work through these in order. Write findings into a scratch note (`NOTES.md` or similar) as you go, because context gets long and rediscovering the test command three times is waste.

### 1. Read the map

Look at the repo root first: README, the package manifest (package.json, pyproject.toml, go.mod, Cargo.toml, etc.), build config, CI config, and the lockfile. From these alone you learn the language, framework, package manager, supported runtimes, and usually the entry points. Skim the top-level directory layout to see how the project thinks about itself (by feature? by layer? monorepo?).

### 2. Learn the commands

Find out how to install, build, test, and lint. The truth usually lives in manifest scripts, a Makefile, a justfile, or the CI workflow files, in that order of convenience. Then run the test suite once before changing anything. This gives you a baseline: if it is green now and red after your change, the problem is yours. If it is already red, record that, so nobody blames your diff for pre-existing failures.

### 3. Trace one flow end to end

Pick one existing feature that resembles the task at hand and follow it from entry point (route, CLI command, event handler) through to its output or persistence. This teaches you more about the project's real conventions than reading directories ever will: how errors are handled, how layers talk to each other, where tests for such things live.

### 4. Note the conventions, then match them

Naming style, folder placement, error handling patterns, test structure, comment culture. The project's existing code is the style guide, whatever your personal preferences are. If two conflicting patterns coexist, prefer the one used in newer code, and say out loud which one you picked and why.

### 5. Write it down

A few lines in your scratch note: the exact test/build/lint commands, key file paths for the task, conventions worth remembering, anything surprising. Cheap insurance against context loss and repeated discovery.

## Standing rules

- Search before assuming. Never guess that a file, function, or config key exists; grep or use code search to confirm the exact name and location.
- Read a file before editing it. The three lines around your change often reveal a guard, a comment, or a convention that changes your approach.
- Prefer copying an existing in-repo example over inventing a new pattern. There is almost always a sibling feature to imitate.
- Scale the recon to the task. A one-line typo fix needs step 2 at most. A new feature in a service you have never seen needs all five.

---
name: safe-refactor
description: Change code structure without changing behavior, in small verified steps. Use this for refactoring, renaming, extracting functions or modules, moving files, removing duplication, dependency and framework migrations, and any "clean this up" or "improve this code" request. Especially important when test coverage is thin, the codebase is unfamiliar, or the diff will exceed a couple hundred lines.
---

# Safe Refactor

A refactor that changes behavior is the worst kind of bug: invisible in review, because everyone reading the diff has been told "no behavior change" and reads accordingly. The whole discipline here is making that promise actually true, and keeping every step small enough that a mistake is trivially findable.

## Ground rules

### 1. Green before you start

Run the test suite over the target area first. If it is red, fix or flag that separately; you cannot preserve behavior you cannot observe. If coverage over the code you are about to reshape is thin, write characterization tests first: tests that pin down what the code currently does, even where the current behavior is ugly. You are photographing the building before moving the walls.

### 2. Refactor commits contain zero behavior change

Structure changes and behavior changes go in separate commits, always. A reviewer can verify "moved code, nothing else" at a glance and "changed logic" with care, but a commit that does both gets neither kind of review. If you spot a real bug mid-refactor, note it, finish or pause the refactor, and fix the bug as its own commit.

### 3. Small mechanical steps, tests between each

One rename. Run tests. One extraction. Run tests. One file move. Run tests. This feels slow and is actually fast, because when something breaks you know it was the last step, not one of forty. Commit at each green state so any single step can be reverted alone.

### 4. Use real tooling for renames

Language-aware rename (LSP, IDE-grade tooling) over naive find-and-replace across the repo. Blind textual replace hits substrings, comments, string literals, and unrelated symbols that happen to share the name. Where only text search is available, review every single match before applying, and search for the old name afterward to confirm zero survivors.

### 5. Watch the blast radius

Anything whose signature, name, or location changes: find all callers and importers and update them in the same step. Then hunt the references tools cannot see: reflection, dynamic imports, string-built attribute access, config files, serialized data, templates, and docs that mention the old name. These are where "safe" refactors go to die.

## Definition of done

- Full suite green, and snapshot or golden-file tests show no diffs (unless an intended cosmetic diff was called out explicitly).
- No public API changes unless the user asked for them.
- Old names return zero search hits.
- The diff reads as an obvious improvement. If the result is not clearly better, simpler, or more consistent, question whether the refactor earned its risk.

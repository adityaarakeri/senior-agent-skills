---
name: git-hygiene
description: Version control discipline for agent work. Atomic commits, meaningful messages, safe operations, and zero destructive surprises. Use this whenever committing, branching, merging, rebasing, resolving conflicts, or preparing pull requests, before any git command that rewrites or discards history, and when the user says "commit this", "clean up the history", or "undo". Consult it before every force push, reset, or clean, without exception.
---

# Git Hygiene

History is a debugging tool. `bisect`, `blame`, and `revert` only work when commits are small, honest, and well described. And nothing torches user trust faster than an agent that ran one destructive git command it was not asked to run. Two goals, then: leave history useful, and never destroy anything without an explicit instruction.

## Committing

1. **Look before staging.** `git status` and `git diff` first, every time. Know exactly what is about to enter the commit; agents that stage blind commit debug prints, secrets, and stray files.
2. **Stage with intent.** Add specific files (or hunks). Avoid blanket add-everything commands when anything unrelated is sitting in the working tree.
3. **Atomic commits.** One logical change per commit. Structure changes separate from behavior changes (see safe-refactor). A reviewer should be able to describe any commit in one sentence.
4. **Messages: imperative summary, then the why.** Summary line around 72 characters or less, written as a command ("Add retry to webhook delivery", not "Added" or "adds"). The body explains why the change exists and any non-obvious decision; the diff already shows what. Check `git log` first and follow the repo's existing convention (conventional commits, ticket prefixes, whatever the house style is).
5. **Never commit** secrets, tokens, keys, credentials, `.env` files, large binaries, or generated artifacts. Scan the staged diff for these every single time; a committed secret is compromised even after the commit is deleted, and rotating it becomes someone's bad afternoon.

## The danger zone

The following require an explicit user instruction naming the operation before you run them. "Clean this up" is not an instruction to rewrite history.

- Any force push. If instructed, prefer `--force-with-lease` so you cannot stomp work pushed by someone else in the meantime.
- `reset --hard`, `clean -f`, and any checkout that discards uncommitted work.
- Amending or rebasing commits that are already pushed to a shared branch.
- Deleting branches, local or remote, that you did not create in this session.
- Any history rewrite (interactive rebase, filter operations) on shared history.

When one of these seems necessary, name the command, say what it will destroy, and wait for a yes.

## Branches, merges, conflicts

Work on a task branch unless told otherwise, named for the change. Sync with the remote before pushing. When conflicts appear, read BOTH sides and understand what each was trying to do; the correct resolution usually preserves both intents, and resolving by mechanically taking one side is how other people's finished work disappears. After resolving, build and run the tests before declaring the merge done, because a textually clean merge can still be semantically broken.

## Recovery beats destruction

Prefer `revert` (a new commit undoing an old one) over `reset` on anything shared; it fixes the mistake without erasing the record. And before anything drastic, remember `git reflog` can usually resurrect what seems lost. Mention that option to the user before reaching for a destructive command on their behalf.

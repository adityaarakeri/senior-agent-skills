---
name: self-review
description: Review the complete diff as a skeptical senior reviewer before handing work back. Use this after finishing any code change and before declaring it done, before committing a substantial diff or opening a pull request, and whenever the user says "review", "check this", or "is this ready". Includes a lightweight security sweep of the changed lines. Make this the last step of every non-trivial coding task.
---

# Self Review

The author's context is a blindfold: you know what the code is supposed to do, so that is what you see. Switching deliberately into reviewer mode catches a different class of bug than writing ever will. You wrote it fast; now read it slow.

## Process

Pull up the FULL actual diff (`git diff`, or a diff of every changed file), not your memory of what you changed. Memory is flattering. Read it top to bottom as if a stranger you slightly distrust wrote it, and fix what you find before handing anything back.

## The checklist

**Correctness.** Does each hunk do what the task asked, and only that? Walk the unhappy paths deliberately: empty input, null/None, zero, one, many, absurdly large, unicode, concurrent access. Most production bugs live in the cases the happy-path author never imagined receiving.

**Leftovers.** Debug prints and temporary logging. Commented-out code. TODOs you meant to resolve this session. Unused imports. Dead branches. Then run `git status` and scan for stray files: editor droppings, test artifacts, an unrelated file you touched while exploring.

**Error handling.** Failures should surface, not vanish. No bare catch-and-ignore. Error messages should tell the next person what went wrong and what to do, not just that something did.

**Security sweep (changed lines only).** Does any user-controlled input reach a SQL query, shell command, file path, HTML output, or deserializer without validation or escaping? Any hardcoded secret, token, key, or password? Any new dependency, and if so, is it genuinely needed and reasonably well known? Any auth or permission check that the change weakened or bypassed? This two-minute pass on the diff catches the embarrassing majority of vulnerabilities.

**Consistency.** Names, style, and patterns match the surrounding file. Code that ignores local convention reads as wrong even when it is correct, and it costs review cycles.

**Tests.** New behavior has coverage. The tests assert behavior, not implementation detail. And the tests would actually fail if the feature broke; a test that cannot fail is decoration.

## Report honestly

After fixing findings, rerun the tests and re-check the diff. Then summarize for the human: what changed, what was deliberately NOT done, and any known limitations or assumptions. A report that admits its gaps is trusted; a report that claims perfection is audited. Never present code containing a known compromise without saying so out loud.

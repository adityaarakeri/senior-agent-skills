---
name: debug-protocol
description: A disciplined, scientific method for diagnosing bugs, failing tests, crashes, and regressions. Use this whenever something is broken and the cause is not already known: error messages, stack traces, "it worked before", flaky tests, wrong output, weird behavior, or after two failed fix attempts on the same problem. Reach for this instead of guess-and-check editing.
---

# Debug Protocol

Guess-and-check debugging burns context, "fixes" symptoms while planting new bugs, and teaches you nothing about the system. Bugs fall to controlled experiments. Treat every bug as a hypothesis to falsify, not a vibe to patch.

## The protocol

### 1. Reproduce first

Get a minimal, deterministic reproduction before touching any code. The best form is a failing test; second best is a small script or exact command. If you cannot reproduce it, you cannot fix it, because you will never know whether you did. For flaky issues, find the loop or seed that makes the failure reliable before proceeding.

### 2. Read the whole error

The full stack trace, top to bottom. The FIRST error, not the last (later errors are usually fallout). The exact file and line. Do not pattern-match on the first familiar word and sprint off; the trace usually names the culprit outright, and agents that skim traces fix the wrong function with total confidence.

### 3. State one hypothesis

Write it down in one sentence: "X happens because Y." If you cannot phrase it that precisely, you are not ready to edit code yet; go read more.

### 4. Run the cheapest experiment that could kill it

A log line printing the actual value, an assertion, a debugger breakpoint, a bisected input. The goal is to make the hypothesis falsifiable fast. Print what the value IS, not what you assume it is; half of all bugs die the moment someone looks at the real data.

### 5. One variable at a time

Change one thing per experiment. If you change three things and it works, you now have a superstition, not a fix, and two of those changes are unexplained diffs in your PR.

### 6. Bisect when lost

For regressions, `git bisect` between the last known good commit and now; it finds the guilty commit in log-n steps. For data or code-path mysteries, binary-search: cut the input in half, disable half the pipeline, and keep halving until the problem corner is small.

### 7. Fix the root cause, not the crash site

Where the pain shows up is rarely where the mistake lives. Before patching, ask once: why did the system allow this state at all? A null check at the crash site hides the bug; fixing whatever produced the null removes it.

### 8. Prove it

The reproduction from step 1 now passes. Keep it as a regression test. Run the full relevant suite so the fix did not break a neighbor. Then remove every debug print, log line, and temporary hack you added along the way. Leave the campsite clean.

## The stuck rule

After three failed hypotheses, stop editing. Re-read the code fresh and question the assumption so basic you never tested it: is this code even running? Is this the config that is loaded? Is the process you are looking at the process that is failing? Am I editing the file that gets imported? If still stuck, summarize the symptom, the hypotheses tried, and the evidence gathered, and ask the user. A crisp stuck-report is senior behavior; a fourth random patch is not.

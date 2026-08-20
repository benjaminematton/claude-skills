---
name: llm-judge-alignment
version: "1.0.0+local.1"
description: >
  Use this skill when a developer wants to validate how well their LLM judge aligns with human judgment.
  Triggers on: "validate my LLM judge", "check if my judge is accurate", "my judge scores don't match
  human ratings", "calibrate my evaluator", "how reliable is my judge", "measure judge alignment",
  "test my eval", "check my judge against human labels", "is my judge any good", "validate my evaluator",
  "my judge is too strict", "my judge keeps missing failures".
  Takes a judge prompt and human-labeled examples, measures pass agreement rate and failure catch rate,
  identifies directional bias (too lenient or too strict), and walks the dev through targeted fixes
  until alignment meets a reliable threshold.
license: MIT
---

# LLM Judge Alignment

<!-- Source: https://github.com/latitude-dev/eval-skills (MIT, Paula Cavero / Latitude).
     Installed 2026-08-19.

     LOCAL CHANGES, 2026-08-19 unless noted:
       1. Removed the closing Latitude product upsell.
       2. Step 2: added the held-out set, drawn once and never read by the fix loop.
       3. Step 6: fixed the judgy snippet — every keyword was wrong upstream and it
          unpacked an object that does not exist. Verified against src/judgy/core.py.
       4. Step 6: the correction inherits bias in the rates it consumes; the CI covers
          sampling variance in the TEST SET ONLY (observed_pass_rate is computed outside
          the bootstrap loop). Option C's synthetic failures named as a source of inflation.
       5. (08-20) Step 5: loop returns to Step 3, not Step 2. An earlier revision sent it
          to Step 2, which re-drew the held-out set every iteration and destroyed change 2.
          Promoted few-shots leave the working pool; the held-out set is never re-drawn.
       6. (08-20) Step 5: the held-out set now has a consumer — score it once at the end,
          report that number, not the working-pool number it was tuned against.
       7. (08-20) Step 3 reads the working pool explicitly, not an ambiguous "test set".
       8. (08-20) Sample floor sized against the working pool (35-50 total, ~100 to act on)
          plus a class-balance minimum, since each rate uses one side of the labels only.
       9. (08-20) Threshold caveat moved into the BODY: 80/90 are conventional, not derived.
      10. (08-20) Removed cross-references to uninstalled sibling skills.

     DELIBERATELY NOT ADDED: Cohen's kappa. Kappa corrects inflation living in the marginal
     class distribution; conditioning on true class already removes the base rate from both
     rates, so adding it back reintroduces prevalence dependence and collapses two
     independently actionable numbers into one. Reasoned from metric structure, not from a
     citation, and the literature is not unanimous.

     Upstream is unmaintained (HEAD 2026-04-24, last commit cosmetic) — this copy is the
     working version, there is nothing to sync back to. Skill 5 of 9 upstream; siblings
     (llm-judge-creator, llm-golden-dataset-builder, llm-regression-runner,
     llm-annotation-guide, llm-issue-discovery) are NOT installed. -->

You help developers validate how well their LLM judge aligns with human judgment and fix it when it doesn't.

The core problem: a judge that looks good overall can still have systematic blind spots. It might catch 9 out of 10 failures but let through the worst kind. Or it might flag good outputs so often that developers stop trusting it. The only way to know is to measure it against human labels — separately for passes and failures.

**Where you are:** judge validation. This assumes you already have a judge prompt and human-labeled examples; downstream, validated judges get run against a golden dataset for regression testing.

**Before starting:** Check if any context documentation exists — `CLAUDE.md`, `product-marketing-context.md`, or any other context files in the project or workspace. If found, read them first.

---

## Step 1 — Get the inputs

You need two things:

**1. A judge prompt.** Theirs, or one generated earlier. If they don't have one yet:
> "To validate a judge you need one first. Write the criterion out as a prompt — what the judge is checking, what counts as a pass, and two or three worked examples with the verdict spelled out — then come back here and we'll measure it."

**2. Human-labeled examples** — input/output pairs with human ratings (pass/fail) on each. You need enough that after setting aside prompt examples and holding back a third for the held-out set, the working pool still has 20+ — so 35–50 labels in total, at the low end. Current practice puts the floor around 30–50 and wants ~100 before you act on a specific number.

The mix matters as much as the count, because each rate is computed on one side of the labels only: pass agreement uses just the human-passes, failure catch uses just the human-fails. Twenty-five examples that are 22 passes and 3 fails give you a catch rate resting on 3 cases. Aim for 15+ on the smaller class before quoting either rate.

**If the judge uses a 1–5 scale:** ask the developer to define their pass/fail threshold before proceeding (e.g., "scores 4–5 = pass, 1–3 = fail"). You need binary labels to measure alignment — the threshold converts the scale to one. Use whatever threshold matches how the scores will actually be used in practice.

If they only have binary labels without notes, that's fine — you can still measure alignment. Notes on failures help diagnose *why* it's misaligned.

### If you only have passing examples (golden dataset with no failures)

A golden dataset contains only good outputs by design — it's not a labeled test set. To measure alignment you need failures too, otherwise you can only measure one direction (whether the judge correctly passes good outputs) and have no signal on whether it catches real failures.

Three ways to get failure examples:

**Option A — Use your annotation data (best).** If you ran `llm-annotation-guide` on production logs, you have labeled outputs that include failures. Pull the ones marked as failing — those are real failures with human judgment already attached. Combine them with a sample of passing examples from your golden dataset and you have a proper test set.

**Option B — Trigger failures from known issues (good).** Take your issue report from `llm-issue-discovery`. For each named failure pattern, either find production traces where that failure occurred, or craft inputs specifically designed to trigger it and run the current prompt against them. Review the outputs yourself and label them as fail. This is more work but produces failures that are grounded in real patterns.

**Option C — Degrade passing outputs synthetically (fast fallback).** Take a sample of passing outputs and manually introduce the failure the judge is meant to catch — add emojis to an emoji-free response, remove a required field, inject fluff into a concise answer. Label these as fail. This is the fastest option and works well for catching whether the judge can recognise an obvious failure, but it produces cleaner failures than you'd see in production. Use it to bootstrap, not as your only source.

Tell the developer which option applies to their situation and help them assemble the mixed test set before proceeding.

---

## Step 2 — Separate test examples from prompt examples

Before measuring anything, identify which examples are already embedded in the judge prompt as few-shot demonstrations. Set those aside.

**Why this matters:** if the judge has already "seen" an example as part of its prompt, scoring it isn't a real test — the judge may pattern-match the example rather than applying the criterion. The test set must be examples the prompt has never seen.

Check the judge prompt: pull out any examples used in the "Examples" section. Everything else in the labeled set is your test set.

Then hold back about a third as a **held-out set**, chosen now, before you see any disagreements. Everything else is the **working pool**. Steps 3–5 read only the working pool.

**Partition the held-out set once and never re-draw it.** Re-drawing after you've seen disagreements rotates tuned-against examples into it and silently undoes the point of having one. Setting aside prompt examples stops contamination but not overfitting — measuring on the pool you tune against makes the rates climb while the judge stays flat. Read the held-out set once, at the end; re-reading it after another fix spends it.

If the **working pool** ends up smaller than 20 examples — that is, after removing both prompt examples and the held-out set:
> "After setting aside your judge prompt's examples and holding back a held-out set, the working pool is [N] cases — that's on the low end. If you can label 15–25 more, the measurement will be more reliable. We can still get a directional read on [N], but treat it as a direction, not a number."

---

## Step 3 — Measure alignment

Run the judge against every example in the working pool — everything except prompt examples and the held-out set — and compare each score to the human label. (At the end of Step 5 you will run this same measurement once against the held-out set.)

Calculate two numbers:

**Pass agreement rate** — of all the examples a human labeled "pass", what percentage did the judge also call "pass"?
```
pass agreement = (judge says pass AND human says pass) / (all human-labeled passes)
```

**Failure catch rate** — of all the examples a human labeled "fail", what percentage did the judge also call "fail"?
```
failure catch rate = (judge says fail AND human says fail) / (all human-labeled failures)
```

These two numbers tell you whether the judge has a directional bias:

| Result | What it means |
|---|---|
| Low failure catch rate | Judge is too lenient — missing real failures |
| Low pass agreement rate | Judge is too strict — flagging outputs that are actually fine |
| Both low | Criteria are unclear or the scale is miscalibrated across the board |
| Both above 80% | Alignment is solid enough to proceed |

**Thresholds:**
- Target: both above 90%
- Minimum acceptable: both above 80%
- Below 80% on either: don't rely on the judge's output yet — fix it first

These numbers are conventional, not derived — there is no canonical threshold in the literature. Treat them as a bar to clear, not as evidence of alignment. On a working pool of 20–30 the rates are each computed on 10–15 cases, and the 95% interval around an observed 9-of-10 runs from roughly 60% to 98% — wide enough that "90%, target met" and "60%, unusable" are the same measurement. Quote the sample size alongside every rate, and don't report a rate you wouldn't restate as "somewhere between X and Y".

---

## Step 4 — Inspect the disagreements

Pull out every case where the judge and human disagreed. Group them by type:

**False passes** (judge said pass, human said fail): the judge is missing something. Look at what the failing outputs have in common — is there a shared trait the judge's criteria don't cover? Is the failing pattern just not represented in the few-shot examples?

**False fails** (judge said fail, human said pass): the judge is over-triggering. Look at what the passing outputs have in common — is the judge applying a stricter standard than what you actually want? Are acceptable variations getting penalized?

For each group, form a hypothesis:
- Is the criterion ambiguous — does it leave room for different interpretations?
- Is a scale anchor pulling scores in the wrong direction?
- Is a few-shot example in the prompt misleading — teaching the wrong pattern?
- Is the judge conflating two separate dimensions in one score?

---

## Step 5 — Fix the judge

Based on the disagreement patterns, suggest the smallest edit that addresses the root cause. Don't rewrite the whole prompt — targeted fixes are easier to validate.

| Problem | Fix |
|---|---|
| Failing outputs share a trait the criteria don't mention | Add that trait explicitly to "What to check" |
| Judge penalizes variation the human accepted | Narrow the criterion or add a few-shot example showing acceptable variation |
| A score-1 or score-5 anchor is pulling scores toward an extreme | Replace the anchor with a more representative example |
| All disagreements involve one specific input type | Add a targeted few-shot example for that input type |
| Judge is conflating two dimensions | Split into two separate judges, one per dimension |

Any example you promote into the judge prompt as a few-shot leaves the working pool — it is now a prompt example and can't be scored again. The held-out set is unaffected: promoted examples come from disagreements, disagreements come from the working pool, so the held-out set was never in scope. Do not re-draw it.

Re-measure on the working pool (Step 3) and repeat until alignment meets the threshold.

**Then score the held-out set — once.** Run the judge against it and compute both rates. That is the number you report; the working-pool number was tuned against and is not a measurement. If held-out is materially below working-pool, the judge was fitted to the working pool rather than fixed. Get more labels rather than continuing to patch — another round of fixes will widen the gap, not close it.

**If alignment stalls:**
- Consider whether the criterion is fundamentally too subjective — some things genuinely need human judgment and resist automation
- Consider using a more capable model for the judge
- Consider splitting the criterion into smaller, more atomic checks — a single judge covering too much ground is hard to calibrate

---

## Step 6 (Optional) — Correct for bias in production metrics

If you're using the judge to report an aggregate pass rate across unlabeled production data, the raw number will be biased — even a well-calibrated judge makes errors, and those errors compound at scale.

A corrected estimate accounts for known errors using the alignment numbers you just measured:

```
corrected pass rate = (observed pass rate + failure catch rate - 1) / (pass agreement rate + failure catch rate - 1)
```

Where `observed pass rate` is the fraction of production outputs the judge scored as passing.

The correction inherits whatever is wrong with the rates it consumes. If `pass agreement` and `failure catch rate` were inflated by tuning against the set that produced them, the corrected figure carries that inflation forward — and synthetically degraded failures (Option C in Step 1) are a concrete source of that inflation, since they are cleaner than production failures and yield a catch rate that is an upper bound rather than an estimate.

`judgy`'s confidence interval covers **sampling variance in the test set only**. Verified in `src/judgy/core.py`: `observed_pass_rate` is computed once at line 106, outside the bootstrap loop that begins at line 125, and only `test_labels`/`test_preds` are resampled. So the interval covers neither bias in the rates nor sampling variance in the production estimate — a narrow interval here means precise, not correct.

The `judgy` library (`pip install judgy`) handles this calculation and also returns a confidence interval:

```python
from judgy import estimate_success_rate

# Verified against ai-evals-course/judgy src/judgy/core.py on 2026-08-19.
# Returns a plain 3-tuple, not an object. Keyword names are exactly these.
theta_hat, lower, upper = estimate_success_rate(
    test_labels=test_human_labels,       # human 1/0 labels, held-out set
    test_preds=test_judge_labels,        # judge's calls on those same examples
    unlabeled_preds=prod_judge_labels,   # judge's calls on unlabeled production output
)
print(f"Corrected rate: {theta_hat:.2f}")
print(f"95% CI: [{lower:.2f}, {upper:.2f}]")
```

If the confidence interval is wide, you need more labeled test examples before the corrected estimate is useful.

---

## Practical notes

**Pin your model version.** Judges run on specific model versions. Providers update models without notice — the same call to `claude-sonnet` or `gpt-4o` may return different results after a silent update. Pin the exact version (e.g., `claude-sonnet-4-6`, `gpt-4o-2024-05-13`) and re-validate when you upgrade.

**Re-validate after prompt changes.** Alignment measured today can degrade when you change your underlying system prompt, add new output formats, or when user behavior shifts. Re-check every 4–6 weeks, or after any meaningful change to the system being evaluated.

**One domain expert beats a crowd.** One person who deeply understands what "good" looks like produces more reliable labels than five people guessing. If you're using multiple annotators, resolve disagreements before using the labels — inconsistent ground truth makes alignment measurement unreliable in ways that are hard to diagnose.

---

Once alignment meets the threshold, end with:

> "Your judge is validated. Next: run it against a golden dataset to catch regressions whenever you change your prompt."

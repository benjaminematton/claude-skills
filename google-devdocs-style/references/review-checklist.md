# Review checklist

For review mode: auditing existing documentation against Google style.

## How to run a review

1. **Scope it.** Ask what's in scope if it isn't obvious — a single file, the
   `docs/` tree, docstrings in one package, or the diff on a branch. Reviewing
   an entire repo unprompted produces a report nobody reads.
2. **Run the mechanical pass first** (the grep patterns below). These catch the
   high-volume, unambiguous violations in seconds and tell you how much
   hand-editing the document actually needs.
3. **Read for the structural checks**, which no pattern catches: heading style,
   lead-in sentences, condition-before-instruction, whether the first paragraph
   answers "what is this and why do I care".
4. **Report with file and line**, grouped by severity. Say what to change it to,
   not just that it's wrong.
5. **Separate deviations from mistakes.** A repo often has a consistent
   convention that departs from the guide — docstrings in a house format,
   numbered headings in a runbook that the body cross-references. Consistency
   that the authors clearly chose is a convention, and the guide's own position
   is that an explicit local convention wins. Say so, recommend keeping it, and
   narrow your finding to the places where the convention actually loses
   information. Mass-rewriting a deliberate house style is the fastest way to
   make a review worthless.
6. **Include a "Left alone" section.** Name what the document already gets
   right, and name the apparent violations you're deliberately not flagging,
   with the reason. Without it, a reader can't tell whether you missed something
   or judged it fine — and they can't tell how much of their document you
   actually read.
7. **Fix only what was asked.** A style review that quietly rewrites the content
   is not a style review. If you find a factual problem, flag it separately.

Severity is roughly: rules that change meaning or block a reader > rules that
break accessibility or translation > house-style consistency.

Expect the mechanical pass to find the small stuff and the structural read to
find everything that matters. Warnings buried in parentheses, procedures that
aren't marked up as procedures, irreversible steps flagged only by capital
letters — no pattern catches any of these, and they're what actually costs a
reader an afternoon. Budget your time accordingly.

## Mechanical pass

Run these from the repo root. Adjust `--glob` for the file types in scope.
Expect false positives — every hit needs a human read, especially the ones that
match inside code blocks.

```bash
# Filler and condescension
rg -n --glob '*.md' -i '\b(simply|just |easy|easily|quickly|please |obviously|of course|clearly,)\b'

# Wordiness with a fixed replacement
rg -n --glob '*.md' -i '\b(in order to|utilize|leverage|allows you to|e\.g\.|i\.e\.|etc\.|and/or)\b'

# Time-anchored language
rg -n --glob '*.md' -i '\b(currently|at this time|as of this writing|for now|newly|coming soon|not yet supported)\b'

# Directional language
rg -n --glob '*.md' -i '\b(above|below|left-hand|right-hand|the left panel|the right side)\b'

# Weak or ambiguous modality
rg -n --glob '*.md' -i '\b(should be|may be able|might want to)\b'

# ALL CAPS used for emphasis. Screen readers may spell these out letter by
# letter, and capitals often mark exactly the irreversible step that deserves a
# real warning instead. Placeholders and acronyms are legitimate — read each hit.
rg -n --glob '*.md' '\b(NOT|NEVER|ALWAYS|MUST|ONLY|REPLACES|REQUIRED|IMPORTANT|WARNING)\b'

# Future tense
rg -n --glob '*.md' '\bwill\b'

# Non-inclusive terms
rg -n -i '\b(whitelist|blacklist|master/slave|sanity check|grandfathered|man-hours|dummy var|hover over|hit the)\b'

# Vague link text
rg -n --glob '*.md' -i '\[(click here|here|this|this document|this page|read more|link)\]'

# First person
rg -n --glob '*.md' -i "\b(we can|we'll|let's|our app)\b"

# Bare URLs as link text
rg -n --glob '*.md' '\[https?://'

# Ambiguous numeric dates
rg -n --glob '*.md' '\b\d{1,2}/\d{1,2}/\d{2,4}\b'

# Ellipsis standing in for omitted code
rg -n --glob '*.md' '^\s*(\.\.\.|…)\s*$'

# Docstring anti-patterns
rg -n --glob '*.py' '"""(This (class|function|method)|Raised when)'
rg -n --glob '*.{ts,js}' '@(param|return)s?\s*\{'   # types in JSDoc — TS already has them
rg -n --glob '*.java' '^\s*\*\s*@return' -B2 | rg -n 'Javadoc'  # spot @return-only blocks
```

## Structural checks

Read for these; no pattern finds them.

**Opening**

- [ ] Does the first sentence say what the thing is, without a preamble?
- [ ] Is the intended reader identifiable — and is *you* used consistently for
      that one person throughout?
- [ ] Is anything critical buried below the fold?

**Headings**

- [ ] Sentence case, no trailing periods.
- [ ] One h1. No skipped levels. No stacked headings with no text between.
- [ ] Task headings use a bare infinitive ("Create an instance"), not a gerund
      ("Creating an instance"). Conceptual headings are noun phrases.
- [ ] No links, no numbering, no code items standing alone in headings.
- [ ] `Optional:` prefix rather than a trailing "(optional)".

**Sentences**

- [ ] Active voice, present tense, second person.
- [ ] Condition, circumstance, or goal comes before the instruction.
- [ ] Nothing over ~26 words.
- [ ] Modality is deliberate: *must* for required, *can* for optional, *might*
      for possible, plain present for expected. No *should* describing a state.
- [ ] Every pronoun has an unmistakable antecedent.
- [ ] One term per concept, all the way through.

**Lists and procedures**

- [ ] Every list has a complete-sentence lead-in — not one the items finish.
- [ ] Parallel structure within each list; consistent end punctuation.
- [ ] No one-item lists. Single-step procedures are bulleted, not numbered.
- [ ] Steps begin with an imperative verb. Location and goal precede the action.
- [ ] Results appear in the same paragraph as their action.

**Procedures wearing a disguise**

Runbooks, deployment guides, and setup docs trip these constantly. In each case
the content *is* a procedure but isn't marked up as one, so it can't be linked
to, navigated by heading, or read a step at a time.

- [ ] **Steps encoded as comments inside one code block** — a single block with
      `# 1.` … `# 5.` and expected results in trailing comments. A reader can't
      work through it incrementally, the expected result isn't associated with
      its step for a screen reader, and you can't link to step 4. Break it into a
      numbered list with one command block per step and the result as prose.
- [ ] **Bolded pseudo-headings** — `**1. Extensions**`, `**Step 2: Restore**` in
      body text where a real heading or list item belongs. These don't appear in
      a table of contents, have no anchor, and are invisible to heading
      navigation. Watch for this in exactly the high-stakes sections (disaster
      recovery, rollback) where someone most needs to jump straight to step 5.
- [ ] **Numbered headings whose numbers are load-bearing** — the guide says not
      to number headings, but if the body cross-references them (`see §4`),
      renumbering silently breaks the references. Usually the right call is to
      keep the numbers and change the cross-reference to name the heading.

**Formatting**

- [ ] Code font on everything typed or parsed; bold on UI element names.
- [ ] No inflected code terms (`POST` the data, `ADDRESS`'s value).
- [ ] Placeholders are `ALL_CAPS_WITH_UNDERSCORES` and explained on first use.
- [ ] Code blocks have an introducing sentence ending in a colon.
- [ ] Omitted code marked with a language comment, not `...`.
- [ ] Filenames use hyphens, and formats are named ("a PNG file", not "a `.png`
      file").

**Links**

- [ ] Link text stands alone and matches the target's title.
- [ ] Punctuation outside the link; no quotation marks around link text.
- [ ] No duplicate links to the same target.
- [ ] Downloads, new tabs, and same-page jumps are flagged in the text.

**Tables and notices**

- [ ] Tables introduced by a complete sentence; sentence-case headers; no merged
      cells; three or more data points per row (otherwise it should be a list).
- [ ] Notices are rare, correctly typed, and don't carry information the reader
      needs to succeed.
- [ ] **No load-bearing warning hidden in parentheses or mid-paragraph.** Readers
      skip parentheticals. When the most expensive fact in a document is inside
      one — "(cancel this and backups break)" — it needs its own sentence, and
      usually a Caution or Warning notice. Ask of each section: what's the worst
      thing a reader could do here, and is that flagged where they'd see it?
- [ ] Irreversible actions (locking a policy, deleting history, force-pushing)
      are marked as warnings, not as an aside in capital letters.

**Accessibility**

- [ ] Alt text on every image; no information conveyed by image alone.
- [ ] No directional references; UI referred to by label, not icon or position.
- [ ] No state conveyed by color alone.
- [ ] No hard line breaks inside sentences.

**Reference comments** (see `code-comments.md`)

- [ ] Every public class, method, parameter, return, and exception documented.
- [ ] Summary starts with the right verb form for the member type, in third
      person present. Doesn't repeat the name. Doesn't say "This class…".
- [ ] No periods inside abbreviations in the summary line.
- [ ] Boolean phrasing follows the fixed forms.
- [ ] Comments add information rather than restating names and types.
- [ ] Implementation comments explain why, not what.

## Report format

Something like this reads well and is easy to act on:

```markdown
## Style review: docs/deploying.md

**Blocking** (changes meaning or blocks a reader)

- L14 — "The value should be true" is ambiguous between a requirement and an
  observation. If it's required: "You must set the value to `true`."

**Accessibility and translation**

- L31 — "as shown in the table below" → "as shown in the following table"
- L52 — link text "click here" → "the Cloud Run quickstart"

**Style**

- L8 — "simply run" → "run"
- L22 — "will return" → "returns"
- L40 — "e.g." → "for example"

**Left alone**

- L60-72 — the `kubectl` examples use `whitelist` because that's the literal
  flag name. Correct per the guide: inclusive term in prose, literal term in
  code font.
```

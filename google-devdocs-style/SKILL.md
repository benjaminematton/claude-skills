---
name: google-devdocs-style
description: "Write and review documentation in the voice of the Google developer documentation style guide — READMEs, docs pages, guides, tutorials, release notes, and API reference comments (Python docstrings, Javadoc, JSDoc/TSDoc, Go doc comments). Use this skill whenever you are drafting, editing, or reviewing prose in a codebase, including a README, a docs page, a how-to, a migration guide, a module or function docstring, a class comment, or a public API reference. Also use it when the user asks to make the docs sound like Google's, to clean up or tighten existing documentation, to write docstrings for a module, or to check writing against a style guide. Trigger even when the user doesn't say Google — if the task is documentation prose in a repo, this skill defines the house style."
---

# Google developer documentation style

This skill encodes the Google developer documentation style guide
(developers.google.com/style) plus Google's per-language comment conventions, so
that prose written across a codebase reads as one voice.

The guide exists because developer docs are read by people who are in a hurry,
often reading in a second language, often through a screen reader, and often
landing mid-document from a search result. Nearly every rule below traces back
to one of those four facts. When you hit a case the rules don't cover, reason
from those facts rather than guessing.

## Two modes

Figure out which one you're in before you start.

**Write mode** — you're producing new prose (a README, a guide, a docstring).
Apply the rules as you draft. Don't write a draft in a generic voice and then
convert it; the conversion pass reliably leaves passive constructions and
future tense behind.

**Review mode** — prose already exists and you're auditing or fixing it. Work
from `references/review-checklist.md`, which orders checks by how often they
catch something and includes grep patterns for the mechanical ones. Report
findings with file and line, grouped by severity, and fix only what the user
asked you to fix.

Two things separate a review someone acts on from one they close. First,
distinguish a deviation from a mistake: a consistent house convention is a
convention, and recommending its wholesale removal makes the whole report easy
to dismiss. Second, say what the document gets right and what you deliberately
left alone — otherwise nobody can tell whether you read it or grepped it.

## Before you write in an existing repo

Spend a minute on reconnaissance. Google's guide is opinionated but it doesn't
cover everything, and a codebase that already has a voice shouldn't get a second
one.

1. Read two or three existing docs in the repo. Note the heading depth, whether
   docstrings use Google or NumPy or reST format, and what the product is
   actually called.
2. Check for a `CONTRIBUTING.md`, `STYLE.md`, `.vale.ini`, or docs linter config.
   An explicit local convention wins over this skill every time — say so rather
   than silently overriding it.
3. Match the docstring format already in use. If a Python repo is on NumPy-style
   docstrings, keep NumPy structure and apply Google's *prose* rules inside it.
   Reformatting every docstring is a separate, larger change the user should opt
   into.

## The rules that carry the most weight

These are the ones that change how text reads. The reference files hold the
full set.

**Second person, active voice, present tense.** Address the reader as *you*.
Name the actor. Describe what the system does, not what it will do.

- Recommended: "Send a query to the service. The server sends an acknowledgment."
- Not recommended: "The service is queried, and an acknowledgment will be sent."

Passive is fine when the actor is genuinely irrelevant ("The database was purged
in January") or when naming the actor would blame the reader ("Over 50 conflicts
were found in the file").

**Condition before instruction.** Readers scan for the branch that applies to
them. Putting the condition first lets them skip the rest of the sentence.

- Recommended: "To delete the entire document, click **Delete**."
- Not recommended: "Click **Delete** if you want to delete the entire document."

**Sentence case everywhere.** Headings, titles, list items, table headers,
captions. Capitalize the first word and proper nouns; nothing else. No trailing
periods on headings.

**Modality is not decoration.** Each word means something specific:

| Intent | Word |
|---|---|
| Required | *must*, or the bare imperative |
| Recommended | *We recommend*; *should* only for recognized best practice |
| Optional | *can* |
| Expected outcome | plain present tense, no auxiliary |
| Possible outcome | *might* |

Never use *should* to describe an actual state. "The value should be true" is
ambiguous between a requirement and an observation. Write "You must set the
value to true" or "The server sets the value to true."

**Cut the filler and the flattery.** Delete *just*, *simply*, *easy*, *easily*,
*quickly*, *please*, *currently*, *now*, *new*, *of course*, *obviously*. They
either add nothing or tell a stuck reader that their problem is trivial. Use
*to* not *in order to*, *run* not *execute*, *lets you* not *allows you to*,
*after* not *once*, *because* not *as*, *for example* not *e.g.*, *that is* not
*i.e.*

**Timeless.** Documentation describes the current state, not the change
history. Drop *currently*, *now*, *new*, *soon*, *as of this writing*, *does not
yet*. Release notes and blog posts are the exception — that's what they're for.

**Code font for anything typed or parsed.** Filenames, paths, method and class
names, flags, env vars, HTTP verbs and status codes, literal values. Bold for UI
element names. Never inflect a code term — write "the `ADDRESS` constant's
value", not "`ADDRESS`'s value"; "Send a `POST` request", not "`POST` the data."

**No directional language.** *Above*, *below*, *the left panel*, *the right-hand
side* break for screen reader users, for translated layouts, and for anyone on a
narrow viewport. Use *preceding* and *following* for document position, and
refer to UI by its label rather than its position or icon.

**Lists need a complete lead-in sentence.** The introduction has to stand on its
own; don't let the list items finish the sentence.

- Recommended: "To get the USB driver, follow these steps:"
- Not recommended: "To get the USB driver:"

**Link text has to survive being read alone.** Screen reader users tab through
links out of context, and so do skimmers. Write "For more information, see
[Load balancing and scaling]", never "see [this document]" or "[click here]".
Punctuation goes outside the link.

**Write for someone reading in a second language.** Keep sentences short — 25
words is a useful ceiling. Keep the optional *that*, *then*, and *of* — the redundancy costs a
word and buys clarity. Don't stack nouns into modifier chains. Use one term per
concept throughout; synonyms read as new concepts.

## Reference files

Read the one that matches what you're writing. Don't load all four.

| File | Covers |
|---|---|
| `references/prose-rules.md` | Voice and tone, grammar, punctuation, inclusive language, the word list |
| `references/structure.md` | Headings, lists, procedures, tables, notices, links, numbers, dates, text formatting |
| `references/code-comments.md` | API reference comments, and Python / Java / TypeScript / Go docstring conventions |
| `references/review-checklist.md` | Ordered audit checklist with grep patterns, for review mode |

## Document shapes

Google's guide is about sentences, not outlines, but these shapes are what its
own docs use and they're a reasonable default when the repo has no precedent.

**README.** One-sentence description of what the thing is. What it's for and who
it's for. Installation. A minimal working example. Links to deeper docs. Don't
open with a history of the project or a wall of badges.

**How-to guide.** Task-based title starting with a bare infinitive ("Deploy to
staging", not "Deploying to staging"). Then: what you'll accomplish,
prerequisites as a list, numbered steps, what success looks like, what to do
next.

**Conceptual page.** Noun-phrase title ("Migration to Cloud Run", not
"Migrating to Cloud Run"). Lead with the definition and why the reader should
care. Explain the model before the mechanics.

**Reference comment.** See `references/code-comments.md` — the phrasing rules
there are tight and mechanical, and getting them right matters more than
anywhere else because doc generators truncate at the first period.

## Failure modes to watch for in yourself

The two most common ways this goes wrong:

*Over-applying to non-prose.* Commit messages, code identifiers, test names, and
log strings are not developer documentation. Don't rewrite a variable name
because it uses a word from the word list — the guide is explicit that when a
term appears literally in code, you use the literal term in code font and the
better term in prose.

*Sanding off real content.* The style rules are about how sentences are built,
not about removing specificity. A shorter document that dropped the caveat about
the race condition is a worse document. Tighten the prose; keep the facts.

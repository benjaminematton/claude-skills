# Code comments and API reference

Sources: developers.google.com/style/api-reference-comments, google.github.io/styleguide
(pyguide, javaguide, tsguide), go.dev/doc/comment.

Reference comments are the highest-leverage prose in a codebase. They're the
only documentation many readers see, they're rendered by generators that
truncate at the first period, and they're read while someone is mid-task and
impatient. The phrasing rules here are tighter and more mechanical than
elsewhere in the style guide — follow them literally.

## Contents

1. [Two kinds of comment](#two-kinds-of-comment)
2. [What to document](#what-to-document)
3. [Class and type descriptions](#class-and-type-descriptions)
4. [Method and function descriptions](#method-and-function-descriptions)
5. [Parameters](#parameters)
6. [Return values](#return-values)
7. [Exceptions](#exceptions)
8. [Fields, constants, and members](#fields-constants-and-members)
9. [Deprecation](#deprecation)
10. [Naming code in prose](#naming-code-in-prose)
11. [Python](#python)
12. [Java](#java)
13. [TypeScript and JavaScript](#typescript-and-javascript)
14. [Go](#go)
15. [Implementation comments](#implementation-comments)

---

## Two kinds of comment

Keep them separate — they have different audiences and different rules.

**Reference comments** (`"""..."""`, `/** ... */`, `// Name does...`) are for
people *using* the code. They describe the contract: what it does, what to pass,
what comes back, what can go wrong. A reader should be able to write a correct
call without reading the implementation.

**Implementation comments** (`#`, `//`) are for people *changing* the code. They
explain why the code is the way it is — the non-obvious tradeoff, the workaround,
the invariant.

Mixing them produces reference docs full of implementation trivia and
implementation code with no explanation of the hard parts.

**Promote a caveat when callers depend on it.** The most common thing a
documentation pass finds is a load-bearing warning sitting in a `//` comment
inside a function body — a security assumption, a precondition, a
"this is only correct if X" — where only someone editing the function ever reads
it. Ask of each body comment: does a caller need this to use the function
correctly, or to decide whether they can trust what it returns? If yes, it
belongs in the reference comment, where the editor surfaces it on hover at every
call site.

A rate-limit helper that reads `x-forwarded-for` is the canonical case. That the
header is caller-controlled unless you're behind a trusted proxy isn't an
implementation detail — it determines whether the return value means anything.
It goes in the doc comment.

Promoting isn't moving. Keep whatever explains *how* the code does it where it
is; lift only the part that describes the contract. And don't invert this rule:
implementation notes that got promoted into reference docs are why so much
generated documentation is unreadable.

---

## What to document

Document every class, interface, struct, and union type; every constant, field,
enum, and typedef; every method — including each parameter, the return value,
and each exception it raises.

Two standing exemptions, both narrow:

- **Self-explanatory members.** A trivial `getFoo()` with genuinely nothing more
  to say can go undocumented. This is not permission to omit information a
  reader needs.
- **Overrides.** A method overriding a documented supertype method doesn't need
  its own comment unless its behavior materially refines the contract.

Worth doing where you can: a 5-20 line usage sample at the top of each major
class or module.

---

## Class and type descriptions

The first sentence states the intended purpose and includes the non-obvious
part. Then:

- **Don't repeat the class name.** The generator already shows it.
- **Don't write "This class…"** or "This class will…".
- **No periods inside abbreviations** — write "for example", never "e.g.". Doc
  generators truncate the summary at the first period, and `e.g.` cuts it in
  half. (The word list bans *e.g.* anyway.)
- Describe what an instance *represents*, not the circumstances in which it gets
  created. An exception class describes the condition, not the moment of raising.

Recommended:

> A primary toolbar within the activity that may display the activity title,
> application-level navigation affordances, and other interactive items.

Later paragraphs cover usage, how to instantiate, key features, best practices,
and pitfalls.

---

## Method and function descriptions

The first sentence states what the method does, in **third-person present
tense** — "Adds a new bird", not "Add a new bird" and not "This method adds".

The starting verb is determined by what kind of method it is:

| Method type | Starting verb |
|---|---|
| Performs an operation and returns data | An action verb — "Adds … and returns …" |
| Boolean getter | "Checks whether …" |
| Non-boolean getter | "Gets the …" |
| Setter, or no return value | "Sets the …" |
| Property update | "Updates the …" |
| Deletion | "Deletes the …" |
| Callback registration | "Registers …" |
| The callback itself (`onX`) | "Called by … Subclasses implement …" |
| Constructor convenience method | "Creates a …" |

Recommended:

> Checks whether this activity is in the process of being destroyed in order to
> be recreated with a new configuration.

Later sentences cover why and how to use it, prerequisites, exception detail,
related APIs, and dependencies such as required permissions.

---

## Parameters

Capitalize the first word. End with a period. Begin with "The" or "A" where the
phrasing allows.

**Boolean parameters have two fixed forms**, depending on whether the parameter
drives behavior or describes state:

- Drives behavior: **"If true, …. If false, …."**
  > `enableCertificateValidation`: If true, validates the SSL certificate before
  > proceeding. If false, trusts the certificate.
- Describes state: **"True if …; false otherwise."**
  > True if the zoom is set; false otherwise.

Don't put `true` or `false` in code font or quotation marks inside these
descriptions.

Default values take the form "Default: *value*".

Don't restate the parameter's name or its type — the signature already carries
both. A description that only says "the maximum number of items" for a parameter
named `maxItems` is noise; say what happens at the boundary, or omit it.

---

## Return values

Keep them brief; detail belongs in the class or method description.

- Non-boolean: start with "The" — "The bird specified by the given ID."
- Boolean: "True if the bird is in the sanctuary; false otherwise."

---

## Exceptions

If the doc generator inserts the word "Throws" for you, begin with "If…":

> If no key is assigned.

If it doesn't, begin with "Thrown when…":

> Thrown when no key is assigned.

---

## Fields, constants, and members

As brief as possible. Link to the methods that use the constant.

> Show 'home' elements in this action bar, leaving more space for other
> navigation elements. This includes logo and icon. See also:
> `setDisplayOptions(int)`.

### Fields on a struct, interface, or dataclass

A returned object is read field by field, out of order, usually from an editor
tooltip — so a field's own comment is often the only thing a reader sees. Three
questions decide whether a field needs one, and what goes in it.

**Does the name and type already say it?** `subtotal: number` on a
`PriceBreakdown` does not need "The subtotal." A comment that restates the name
is worse than nothing: it costs a line, it has to be maintained, and it trains
readers to skip the comments that matter. Skip it and move on.

**Is there a unit, a range, or an encoding?** This is where most of the value
is, and the type system rarely carries it. Whole dollars or cents. Unix
milliseconds or seconds. `0.22` meaning 22 percent. Inclusive or exclusive
bounds. A caller who guesses wrong here ships a bug that typechecks.

**When is it absent, and what does absent mean?** For an optional field, say
what its absence signifies rather than that it's optional — the `?` or the
`| None` already says optional. "Set only on a denial" tells a reader something;
"Optional." does not.

Booleans on a struct take the state form: "True if the request is within the
limit; false if it was denied." A tri-state (`bool | None`, `Boolean`) needs all
three cases spelled out, because the third is exactly the one people get wrong.

**Don't document a field twice.** When fields pass straight through from another
documented type, document them there and leave the pass-through copies bare.
Two copies of a description drift, and the reader can't tell which is current.
The same goes for a field whose meaning is fully explained in the type's own
summary — say it once, at the level where it makes sense.

---

## Deprecation

Put the most important information in the first sentence — it's what appears in
the summary. Name the replacement, give the version it was deprecated in if
that's tracked, and tell the reader how to update.

> Deprecated. Use `#CameraPose` instead.

> Deprecated. Access this field using the `getField` method.

*Deprecated* means "recommended against", not *removed*, *deleted*, or *shut
down*. Don't use it for those.

---

## Naming code in prose

- Spell class names exactly as in code, including capitals, with no spaces:
  `ActionBar`.
- **Never pluralize a class name.** Not "Intents" or "Activities" — write
  "Intent objects" or "Activity instances".
- For the everyday concept rather than the type, use lowercase English with no
  code font: "activities", "the action bar".
- Put API names, classes, and methods in code font, linked where the generator
  supports it.
- String literals go in code font with their quotes: `"wrap_content"`.

---

## Python

Google-style docstrings, per pyguide §3.8.

Triple double quotes. A one-line summary, one physical line under 80 characters,
ending in terminal punctuation. If there's more, a blank line, then the body
starting at the same column as the opening quote.

A docstring is **mandatory** for any function that is part of the public API, is
nontrivially sized, or has non-obvious logic. It should give enough information
to write a call without reading the body — calling syntax and semantics, not
implementation details.

Descriptive (`"""Fetches rows from a Bigtable."""`) or imperative
(`"""Fetch rows from a Bigtable."""`) are both allowed, but be consistent within
a file. pyguide's own examples are descriptive third-person, which makes it the
safer default for a new file.

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will
          be returned.

    Returns:
        A dict mapping keys to the corresponding table row data fetched. Each
        row is represented as a tuple of strings.

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

- **Args:** each parameter by name, colon, description. Hanging indent of 2 or 4
  spaces for wrapped lines. Include types only when there's no annotation.
  Varargs appear as `*foo` and `**bar`.
- **Returns:** describe the semantics, including anything the annotation doesn't
  convey. Omit for functions that only return `None`. Also omittable when the
  docstring starts with "Returns"/"Yields" and the opening sentence fully
  describes the return value.
- **Yields:** for generators, document what `next()` produces, not the generator
  object.
- **Raises:** every exception relevant to the interface.

**Classes** put the docstring below the `class` line, with public attributes in
an `Attributes:` section formatted like `Args:`.

```python
class SampleClass:
    """Summary of class here.

    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
```

Class docstrings start with a one-line summary of what an *instance represents*.
Exception subclasses describe the condition, not the context of raising:

```python
# Preferred
class OutOfCheeseError(Exception):
  """No more cheese is available."""

# Avoid
class OutOfCheeseError(Exception):
  """Raised when no more cheese is available."""
```

**Modules** start with a docstring describing contents and usage, often with a
"Typical usage example:" block. Test modules don't need one unless there's real
added information (how to run it, unusual setup, external dependencies) —
"Tests for foo.bar." adds nothing.

**Overrides** decorated with `@override` don't need a docstring unless they
materially refine the contract. `"""See base class."""` is acceptable.

---

## Java

Javadoc, per javaguide §7.

```java
/**
 * Multiple lines of Javadoc text are written here,
 * wrapped normally.
 *
 * @param p1 The first parameter.
 * @return The customer ID.
 */
public int method(String p1) { ... }
```

Single-line form only when the whole thing fits on one line and there are no
block tags: `/** An especially short bit of Javadoc. */`

**The summary fragment** is the load-bearing rule. Every Javadoc block opens
with one, and it's often the only part that appears in class and method indexes.

- It's a **noun phrase or verb phrase, not a complete sentence** — but it's
  capitalized and punctuated as if it were one.
- It does **not** start with "A `Foo` is a…" or "This method returns…".
- The classic error is `/** @return the customer ID */` with no summary. Write
  `/** Returns the customer ID. */` instead.

**Paragraphs** are separated by a line containing only the aligned asterisk.
Every paragraph after the first starts with `<p>` immediately before the first
word. Block-level HTML like `<ul>` doesn't get a `<p>`.

**Block tag order:** `@param`, `@return`, `@throws`, `@deprecated`. None of them
ever appear with an empty description. Continuation lines indent four spaces
from the `@`.

**Required** at minimum for every visible class, member, and record component:
public top-level classes, and public or protected members of visible classes.

---

## TypeScript and JavaScript

Per tsguide.

**`/** JSDoc */` for documentation, `// line comments` for implementation.**
Multi-line implementation comments stack `//` lines rather than using `/* */`.
No decorative asterisk boxes.

```ts
/** An ancient {@link CoffeeBrewer} */
export class Percolator implements CoffeeBrewer {
  /**
   * Brews coffee.
   * @param amountLitres The amount to brew. Must fit the pot size!
   */
  brew(amountLitres: number) {
    // This implementation creates terrible coffee, but whatever.
    // TODO(b/12345): Improve percolator brewing.
  }
}
```

- **Document all top-level exports.** Also document any property or method —
  exported or not — whose purpose isn't obvious from its name.
- **Omit what TypeScript already says.** No types in `@param` or `@return`; no
  `@implements`, `@enum`, `@private`. `@param {number} maxItems` is wrong;
  `@param maxItems The maximum number of items to retrieve.` is right.
- **Don't use `@override`** — it isn't compiler-enforced, so it drifts.
- **Add information, don't restate names.** Descriptions may be omitted entirely
  when they're obvious from the signature. Method descriptions start with a
  third-person verb phrase, not an imperative.
- JSDoc content is Markdown — plain-text lists need to be Markdown bullets to
  render.
- **Call sites:** for arguments whose meaning isn't obvious, use an inline block
  comment naming the parameter, or switch to a destructured object.
  ```ts
  new Percolator().brew(/* amountLitres= */ 5);
  ```
- **Parameter properties** (a field declared in the constructor signature) are
  documented with `@param` on the constructor, so editors surface them at call
  sites. Ordinary fields get their own JSDoc.
- **JSDoc goes above decorators**, with no blank line between the decorator and
  the class.

---

## Go

Per go.dev/doc/comment. Go's conventions differ from the rest — follow Go's.

A doc comment sits immediately before a top-level declaration with no blank line
between. **Every exported name should have one.**

**Begin with the name of the thing being declared**, in a complete sentence.
This is what makes `go doc` output and search work.

```go
// A Reader serves content from a ZIP archive.
type Reader struct { ... }

// Quote returns a double-quoted Go string literal representing s.
func Quote(s string) string { ... }

// HasPrefix reports whether the string s begins with prefix.
func HasPrefix(s, prefix string) bool { ... }
```

Note `reports whether` — that's the Go idiom for a boolean return, in place of
"Checks whether".

**Package comments** begin with "Package " and the package name:

```go
// Package path implements utility routines for manipulating slash-separated
// paths.
//
// The path package should only be used for paths separated by forward slashes,
// such as the paths in URLs.
package path
```

Complete sentences throughout. Refer to parameters and results by name directly,
with no backticks.

**Deprecation** is a paragraph starting with `Deprecated: `:

```go
// Deprecated: RC4 is cryptographically broken and should not be used except
// for compatibility with legacy systems.
```

**Formatting:** `#` plus a space makes a heading (blank lines around it).
`[Name]`, `[Name.Method]`, and `[pkg.Name]` are doc links to identifiers.
External links are defined in a trailing section as `[Text]: URL`. Bullet lists
use `-`; numbered lists use `1.`. Indented lines become code blocks. `gofmt`
preserves your line breaks, so one sentence per line is a workable habit.

---

## Implementation comments

The rule that matters, from pyguide: **never describe the code.** "Assume the
person reading the code knows Python (though not what you're trying to do)
better than you do" — which generalizes to whatever language you're in. A
comment that narrates the loop is worse than no comment,
because it has to be maintained and it teaches the reader nothing.

Comment the tricky parts — "If you're going to have to explain it at the next
code review, you should comment it now." A few lines before a complicated
operation; an end-of-line note on a non-obvious one.

```python
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```

Inline comments start at least two spaces from the code, with a space after the
comment character.

Write them as readable narrative — proper capitalization and punctuation.
Complete sentences are usually more readable than fragments. End-of-line
comments can be less formal, but stay consistent within a file.

---

## Cross-cutting summary

1. **Summary lines are fragments punctuated as sentences.** Java says so
   explicitly. API reference uses third-person present ("Returns", "Gets",
   "Sets", "Checks whether"). Python allows descriptive or imperative but
   demands consistency per file. Go starts with the declared name.
2. **Booleans have fixed phrasing.** Getter: "Checks whether…" (Go: "reports
   whether"). Return: "True if X; false otherwise." Behavior-driving parameter:
   "If true, …. If false, …."
3. **Never restate the code.** Python: never describe the code. TypeScript: omit
   what the type system says. Java: self-explanatory members may be skipped.
   Comments answer *why* and *how to call*, not *what this line does*.
4. **No periods inside abbreviations in a summary line** — generators truncate
   at the first period. "for example", never "e.g.".
5. **The prose rules still apply inside comments.** Present tense, active voice,
   no *simply* / *just* / *easy*, no *above* / *below*, code font for code terms,
   one term per concept.

# Structure and formatting

Source: developers.google.com/style.

## Contents

1. [Headings and titles](#headings-and-titles)
2. [Lists](#lists)
3. [Procedures](#procedures)
4. [Tables](#tables)
5. [Notices](#notices)
6. [Text formatting](#text-formatting)
7. [Code in text](#code-in-text)
8. [Placeholders](#placeholders)
9. [Command-line syntax](#command-line-syntax)
10. [Filenames](#filenames)
11. [Links and cross-references](#links-and-cross-references)
12. [UI elements](#ui-elements)
13. [Numbers, dates, and units](#numbers-dates-and-units)
14. [Accessibility](#accessibility)

---

## Headings and titles

- **Sentence case.** No trailing period.
- **One h1 per page**, unique across the doc set. Don't skip levels. Don't leave
  a heading empty.
- **Don't stack headings.** Put text between an h2 and its first h3.
- **No links in headings** — a link reads as styling applied to the heading.
- **No numbers** to indicate section sequence; rely on hierarchy and order.
- **Avoid code items in headings.** If you must, add a descriptive noun:
  "The `--hostname` flag" rather than "`--hostname`".
- **Keep punctuation simple.** Complicated punctuation signals a heading that's
  doing too much.
- **Abbreviations** only if the abbreviation is the better-known form.
  Otherwise spell it out (better for search) and define it in the first
  paragraph.

**Task headings** start with a bare infinitive verb, not a gerund.

| Recommended | Not recommended |
|---|---|
| Create an instance | Creating an instance |
| Transfer data sets | Transferring data sets |

**Conceptual headings** are noun phrases.

| Recommended | Not recommended |
|---|---|
| Migration to Google Cloud | Migrating to Google Cloud |

**Optional sections** take an `Optional:` prefix, not a trailing "(optional)".

| Recommended | Not recommended |
|---|---|
| Optional: Customize your alias | Customize your alias (optional) |

**Referring to subsections:** "The following sections describe…", not "This
section…".

**Anchors** are lowercase with hyphens between words, descriptive but concise.
When you rewrite a heading, keep the old anchor ID so inbound links survive.

```markdown
## Help conserve habitat for pollinators {: #conserve-habitat }
```

---

## Lists

| Type | Use for |
|---|---|
| Numbered (`ol`) | Items where sequence matters — ordered steps, phases, priorities |
| Bulleted (`ul`) | Items where sequence doesn't matter — options, examples |
| Description (`dl`) | Terms each paired with a description or definition |
| Run-in headings | An introductory term or phrase followed by its description |

**Never a one-item list.** A single item isn't a list.

**Lead-in must be a complete sentence.** Don't let the list items finish the
sentence for you.

| Recommended | Not recommended |
|---|---|
| Use the **Submit** button for any of the following purposes: | Use the **Submit** button to: |
| To get the USB driver, follow these steps: | To get the USB driver: |
| If you need to add an instance manually, do the following: | If you need to add an instance manually: |

End the lead-in with a colon when the list immediately follows, a period when
other material intervenes.

**Capitalization.** Start each item with a capital letter unless case carries
information.

**End punctuation.** Add a period, except when the item:

- is a single word,
- contains no verb,
- is entirely in code font, or
- is entirely link text or a document title.

Description lists: no period after the term; generally a period after the
description.

**Run-in headings.** End with either a period or a colon, consistently within
the list. After a period, capitalize the description. After a colon, lowercase
it. A description following a colon takes no period if it's a list of short
phrases without verbs, and a period if it contains a verb.

- "**Coffee**: latte, mocha, cappuccino, espresso" (colon, no period)
- "**It increases fuel economy by reducing baggage weight**. By charging…"
  (period, capitalized)

**Parallel structure.** Same syntactic shape for every item. If you can't get
there, add end punctuation to every item for consistency.

**Nesting.** Nested ordered lists use lowercase letters, then lowercase Roman
numerals.

**Multi-paragraph items** use `<p>`, never `<br>`.

**In-paragraph lists** use serial commas: "event logs, clickstream data, social
network interactions, and e-commerce transactions."

---

## Procedures

- Numbered steps. Each step starts with an **imperative verb**, in a complete
  sentence, parallel with the others.
- **Single-step procedures** are a bulleted list, not a one-item numbered list.
- **Sub-steps** use lowercase letters; sub-sub-steps use lowercase Roman
  numerals. Treat the parent step as a lead-in.
- **Order within a step:** the action, then the command, then placeholder
  explanations, then detail, then output, then what the output means.
- **State the location before the action.** "In Google Docs, click **File > New
  > Document**", not "Click **File > New > Document** in Google Docs."
- **State the goal before the action.** "To start a new document, click **File >
  New > Document**."
- **Optional steps** start with `Optional:`, not `(Optional)`.
- **Combine small sequential UI actions:** "Click **Next > Finish**."
- **Results** stay in the same paragraph as their action, after it: "Click
  **Run**. The query results appear after the query runs."
- **Include justifications** where they help: "Store the private key in a secure
  location. You need it later."
- **Document one method**, chosen for accessibility. Prefer keyboard-accessible
  approaches and the shortest path. Put alternatives on separate pages, headings,
  or tabs.
- **One reader decision per step.** Minimize step count.
- **Link to procedures** rather than repeating them. When several headings each
  contain a procedure, restate the context in each.
- No *please*. No directional language.

---

## Tables

**List or table?** Use a list when each entry is one unit or a pair of related
values (a description list handles pairs). Use a table when each entry has three
or more pieces of related data.

**Don't use tables for:** page layout, single-row or single-column data, code
snippets, long one-dimensional lists split into columns, or anything in the
middle of a numbered procedure.

**Introduce every table with a complete sentence** — not every screen reader
announces that a table is coming. "Change the environment variables to values
for your deployment, as listed in the following table:"

**Captions** are optional for a single table, required when a page has more than
one. Format: `**Table 1.** Prehistoric birds` — sentence case, no ending period.
Refer to tables by number in body text.

**Column heads** use sentence case with no ending punctuation. Mark only the
first row and/or first column as headers, with `scope`. Never convey
"this is a header" through font or color.

**Don't merge cells.** No `colspan` or `rowspan`. Sort rows logically or
alphabetically. Split long tables. Multi-paragraph cells use `<p>`. Give images
in cells alt text. Avoid linking directly to a table — refer to it by number.

---

## Notices

| Notice | Meaning |
|---|---|
| **Note** | An ordinary aside or tip. Useful but not critical. |
| **Caution** | Tells the reader to proceed carefully. |
| **Warning** | "Don't do this," or the step may be irreversible — permanent data loss. |
| **Success** | A successful action or error-free status. Interactive content only. |

Use a note only when all three are true: the information is relevant but not
necessary right now; interrupting the reader isn't an obstacle; and the
information isn't part of the flow of what you're writing.

Don't use a note for cross-references, prerequisites, a procedural step, or
anything necessary to the reader's success. That content belongs in the flow.

Minimize notices — overuse destroys their distinctiveness. Avoid stacking two
notices together.

```html
<aside class="note"><b>Note:</b> CONTENT</aside>
```

In Markdown: `**Note:** CONTENT`

---

## Text formatting

| Item | Format |
|---|---|
| UI element names | **Bold** |
| Run-in headings, notice labels | **Bold** |
| Terms being introduced or defined; words as words | *Italic* |
| Semantic emphasis (sparingly) | *Italic* |
| Titles of books, movies, series | *Italic* |
| Mathematical and version variables | *Italic* — *x* + *y*, version 1.4.*x* |
| Titles of shorter works (articles, chapters) | "Quotation marks", unless it's link text |
| Link text | Underline, and nothing else is underlined |
| Placeholders | `CODE FONT, ALL CAPS` |
| Everything typed or parsed | `Code font` — see below |

Don't override font type, size, or color. Don't use `&` for *and*.

Use `<b>` and `<i>`, not `<strong>` and `<em>`, for pure styling — but use `<em>`
when you mean genuine semantic emphasis, since screen readers announce it.

---

## Code in text

Code font signals text to be entered verbatim and marks its boundaries.

**Always code font:** attribute names and values; class names; command output;
command-line utility names (`gcloud`, `kubectl`, `git`); data types; database
row and column names; defined constants; DNS record types; HTML/XML element
names (without the angle brackets); enum names; environment variables;
filenames, extensions, paths, directories; HTTP content types, status codes, and
verbs; IAM role names; IP addresses; language keywords; method and function
names; namespace aliases; package names; port numbers; placeholders; query
parameter names and values; string literals used in commands or code; text the
user types; UI elements rendered from text the user entered.

**Not code font:** domain names in ordinary prose; product, service, and
organization names; URLs the reader is meant to open in a browser.

**Conditional:**

- Booleans: code font for the literal value (`true`, `false`), regular font when
  discussing a boolean condition.
- Command-line utilities: the command is code font, the project isn't —
  "Invoke the GCC 8.3 compiler using `gcc`."
- Email addresses: code font as input or output, regular font as contact info.

**Method names** omit the class unless it's needed to disambiguate: "call its
`get` method", not "call its `animal.get` method".

**HTTP status codes:** "an HTTP `400 Bad Request` status code"; "an HTTP `2xx`
status code"; "a status code in the `200`-`299` range". Say *status code*, not
*response code* or *error code*.

**Never inflect a code element.** Add a noun and inflect that instead.

| Recommended | Not recommended |
|---|---|
| The `ADDRESS` constant's value | `ADDRESS`'s value |
| Send a `POST` request | `POST` the data |
| Call the `close` method | `Close`ing the file |

**Code that's also UI:** use both code font and bold — "In the **Network** list,
select **`my-net-2`**".

**Quotation marks** around code only when the quotes are part of the code.

**Code samples:** wrap at 80 characters; follow the language's own style guide
for indentation; introduce every sample with text ending in a colon ("The
following sample shows how to use the `get` method:"); indicate omitted code
with a comment in the language's syntax, never with `...` or `…`.

---

## Placeholders

- Uppercase with underscores: `API_NAME`, `PROJECT_ID`, `EMAIL_ADDRESS`.
- Not `api-name`, `API_name`, `apiName`, or possessives like `YOUR_API_NAME`.
- Don't use `x` or `xxx` as a placeholder; be informative.
- Markdown: `` *`PLACEHOLDER_NAME`* ``. HTML: `<code><var>PLACEHOLDER</var></code>`.
- **Explain on first use.** One placeholder: "Replace `PLACEHOLDER` with …".
  Several: "Replace the following:" followed by a list in order of appearance,
  each description starting lowercase.
- Repeat the explanation in long documents and in docs read out of order.

---

## Command-line syntax

- `[BRACKETS]` mean optional — one set per optional item.
- `{A|B}` means choose exactly one.
- `...` with no spaces means repeatable: `gcloud dns GROUP [GLOBAL_FLAG ...]`
- **Click-to-copy commands must contain no brackets, braces, pipes, or
  ellipses.** Split into separate blocks per variant instead.
- Line continuation: `\` on Linux, `^` on Windows, preceded by a space.
- Include output only when it adds value — the reader needs to copy something
  from it or verify something in it. Introduce it with "The output is similar to
  the following:".

---

## Filenames

- Lowercase, ASCII alphanumerics, **hyphens not underscores** — `query-data.html`.
  Search engines read hyphens as spaces. Exception: match an existing directory
  convention.
- Avoid generic names like `document1.html`.
- In prose: code font, followed by the word *file* — "In the following `build.sh`
  file, modify the default values."
- **Use the format's name, not the extension:** "a PNG file", not "a `.png`
  file"; "a Bash file", not "an `.sh` file". Names: CSV, JSON, Markdown, PDF,
  Python, SQL, YAML, zip.

---

## Links and cross-references

**Phrasing.** "For more information, see [X]." / "For more information about Y,
see [X]." Use *about*, not *on*.

**Link text** must be a short, unique, descriptive phrase that makes sense read
out of context, with the important words first.

| Recommended | Not recommended |
|---|---|
| For more information, see [Load balancing and scaling] | See [this blog post] |
| see [Make headings into link targets] | Want more? [Click here!] |
| see [Make headings into link targets] | see [this document] |
| [HTTP/1.1 RFC] | [http://www.w3.org/Protocols/rfc2616/rfc2616.html] |
| [Google Kubernetes Engine (GKE)] | [Google Kubernetes Engine] (GKE) |
| run the command with the [`--hostname` flag] | run the command with the [`--hostname`] flag |
| supports the [`GET`], [`HEAD`], and [`OPTIONS`] methods | supports the [`GET` method], [`HEAD` method]… |

Match link text to the title of the page you're linking to.

**Punctuation goes outside the link.** No quotation marks around link text.

**Don't duplicate links** — link once, at the most useful place. Don't send
readers away for something you could state on the page.

**Flag unexpected behavior:** "(opens in a new tab)", "[download the security
features PDF]", "[send email to Technical Support]", "see the [Write descriptive
link text](#descriptive-link-text) section of this document".

**External links** don't need an icon. Mention that the reader is leaving only
when it matters.

---

## UI elements

- UI names in **bold**. Add code font too if the element independently qualifies.
- Follow on-screen capitalization, but convert ALL-CAPS or inconsistent labels to
  sentence case: "Click **Refresh**", not "Click **REFRESH**".
- **Don't use UI elements as verbs.** "In the **Name** field, enter an account
  name", not "**Name** the account."
- Menu paths use `>` with a nonbreaking space before it, wrapped as
  `<span aria-label="and then">></span>`: "Select **View > Tools > Developer
  Tools**".
- Element nouns: the **X** window / page / dialog / pane / tab / list /
  checkbox. Radio buttons take just the label.
- Buttons with icons: icon plus label. Omit ellipses from button names —
  "Click **Browse**", not "**Browse ...**".
- Keys: `<kbd>`, capitalized, modifiers spelled out, with the mac variant —
  "Press `Control+C` (or `Command+C` on macOS)".
- Verbs: *click* buttons, menus, links; *select* checkboxes, radio buttons, list
  items; *choose* among options; *tap* on touchscreens; *enter* or *type* in text
  boxes; *press* keys; *drag*; *hold the pointer over* (not *hover*); *turn on* /
  *turn off* toggles.
- Prepositions: *in* dialogs, fields, lists, menus, panes, windows; *on* pages,
  tabs, toolbars.
- **No directional language.** Not *above*, *below*, *the left panel*, *the
  right-hand side*. Refer to elements by label, or use context.

---

## Numbers, dates, and units

**Numbers.** Spell out zero through nine; use numerals for 10 and up. Spell out
a number that starts a sentence, and a number immediately followed by a numeral
("fifteen 100,000-byte files").

Always numerals, even below 10, for: version numbers, technical quantities (6
queries per second, 50 Mbps, 128 bits), page and step numbers, prices, negative
numbers, decimals, percentages, dimensions, and any number appearing alongside a
number over nine.

Spell out ordinals: *first*, *fifth*, *twelfth* — not *1st*, *5th*, *12th*.

Express fractions as decimals where possible (`0.75`), with a leading zero
(`0.3 inches`). Percentages take a numeral and `%` with no space: `40%`. Four or
more digits take comma separators: `1,532,784 bytes`. Dimensions use a lowercase
`x` with no spaces: `192x192`. Ranges use a hyphen with no spaces: `2012-2016`.

**Dates.** Full month name, day, four-digit year: January 19, 2017. With a
weekday: Tuesday, April 27, 2021. Month and year alone take no comma: April
2021. A full date mid-sentence takes a comma after the year.

Abbreviate only where space is tight (headings, tables): three letters, capital
first, no period — "Mon, Sep 3, 2018". Abbreviate the whole date or none of it.

Numeric-only dates follow ISO 8601: `2017-04-15`, never `04/06/2017`. In
examples, use a day greater than 12 so it can't be mistaken for a month.

**Times.** 12-hour clock, AM/PM in caps, one space: `3:45 PM`. Omit `:00` for
whole hours: `3 PM`. *noon* and *midnight* are fine. Ranges use hyphens with no
spaces. Use 24-hour time only to match a UI or code sample.

Avoid time zones unless necessary. Spell out the region with a UTC parenthetical:
"US and Canadian Pacific Standard Time (UTC-8)". Never abbreviate a time zone
name.

Date before time: `2017-04-15 at 3 PM`, `May 4, 2009, at 6 PM`.

Avoid seasons — they're hemisphere-dependent. Use months or quarters.

**Units.** Nonbreaking space between number and unit — `64&nbsp;GB` — except for
currency, percent, and degrees of angle (`$10`, `65%`, `180°`). Temperature:
`50&nbsp;&deg;C` → 50 °C; Kelvin omits the degree symbol. Ranges of measurements
use *to*, not a hyphen: "-40 °C to 85 °C". Multiplied units hyphenate:
"5 vCPU-hours", "40 person-hours". Rates use *per*, or an established
abbreviation like Gbps. Decimal units are kB/MB/GB; binary are KiB/MiB/GiB.

---

## Accessibility

Much of the style guide exists for this. The rules that matter most in a
codebase:

- **Descriptive headings, correct nesting**, no skipped levels, no empty
  headings.
- **Link text that stands alone.** No "click here" or "read this document".
- **Alt text on every image**, summarizing intent. Empty `alt` for decorative
  images. Never put information only in an image — always give the text
  equivalent. Prefer SVG over PNG. No images of text or code.
- **Introduce tables and interactive elements in text** before they appear.
- **Don't convey state by color, icon, or outline alone.** Change a text label
  too.
- **Avoid camelCase and ALL CAPS in prose** — some screen readers spell out
  capitals letter by letter.
- **Don't rely on punctuation** to carry meaning; not all of it is read aloud.
- **No hard line breaks** inside sentences — they break when text is resized.
- **Break up walls of text.** Front-load the important information. Define
  acronyms on first use. Keep list items parallel. Left-align.
- **Refer to UI by label, not appearance or position.** "Click **Save**", not
  "click the disk icon"; "Click **Notifications**", not "click the bell icon".
- **Use *preceding* and *following***, not *above* and *below*.
- **Captions and transcripts** for video. Avoid flashing content.
- 4.5:1 contrast minimum. Keep style order matching DOM reading order. Don't rely
  on mouseover-only interactions.

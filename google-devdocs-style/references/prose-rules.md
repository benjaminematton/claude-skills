# Prose rules: voice, grammar, punctuation, word choice

Source: developers.google.com/style. Examples are quoted from the guide.

## Contents

1. [Voice and tone](#voice-and-tone)
2. [Person and address](#person-and-address)
3. [Active voice](#active-voice)
4. [Tense](#tense)
5. [Modality: must, should, can, might](#modality)
6. [Sentence and clause structure](#sentence-and-clause-structure)
7. [Writing for a global audience](#global-audience)
8. [Capitalization](#capitalization)
9. [Pronouns, articles, possessives](#pronouns-articles-possessives)
10. [Punctuation](#punctuation)
11. [Inclusive language](#inclusive-language)
12. [Jargon](#jargon)
13. [Timeless documentation](#timeless-documentation)
14. [Excessive claims](#excessive-claims)
15. [Word list](#word-list)

---

## Voice and tone

Aim for the voice of a knowledgeable friend who understands what the developer
wants to do. Conversational and respectful, not slangy, not stiff. Readers are
usually in a hurry — information beats personality.

Avoid: buzzwords and jargon; cuteness; figurative language and metaphors;
placeholder phrases like *please note* and *at this time*; choppy or
long-winded sentences; starting every sentence the same way ("You can…", "To
do…"); pop-culture references; exclamation marks; wackiness; phrasing that
denigrates any group; *let's* constructions; *simply* / *it's easy* / *quickly*
in procedures; internet slang (*tl;dr*, *ymmv*).

| Too informal | Just right | Too formal |
|---|---|---|
| Dude! This API is totally awesome! | This API lets you collect data about what your users like. | The API documented by this page may enable the acquisition of information pertaining to user preferences. |
| Then—BOOM—just garbage-collect, and you're golden. | To clean up, call the `collectGarbage` method. | Please note that completion of the task requires the following prerequisite: executing an automated memory management function. |

**Contractions.** Use common two-word contractions (*you're*, *don't*,
*there's*) — they carry the conversational tone. Negation contractions
(*isn't*, *can't*, *don't*) are especially good because a scanning reader is
less likely to miss them than a standalone *not*. Avoid three-word contractions
(*mightn't've*) and nonstandard ones (*browser's* for "browser is").

**No *please*.** Politeness in instructions reads as padding.

- Recommended: "To view the document, click **View**."
- Not recommended: "To view the document, please click **View**."

---

## Person and address

Use second person. *You* is the reader.

- Recommended: "The following sections describe how you can create a website."
- Not recommended: "The following sections describe how we can create a website."
- Not recommended: "This document shows the user how to develop an app."

Use the imperative for instructions — the *you* is implied. "Click **Submit**."

Reserve *user* for an end user of the software being documented, not for the
person reading the document.

First-person plural is acceptable only when it unambiguously means the
authoring organization: "Example Organization provides A and B, but we don't
provide C and D." / "For more information, contact our sales organization."

Identify who *you* refers to (developer, operator, administrator) and keep it
consistent through the document.

Use second person for reader actions, third person for what the software or an
end user does.

---

## Active voice

The grammatical subject performs the action. Passive voice makes it easy to
omit who is supposed to do something.

- Recommended: "Send a query to the service. The server sends an acknowledgment."
- Not recommended: "The service is queried, and an acknowledgment is sent."
- Not recommended: "The service is queried by you, and an acknowledgment is sent by the server."

Passive is acceptable in three cases:

1. To emphasize the object over the action — "The file is saved."
2. To de-emphasize the actor, especially to avoid blaming the reader — "Over 50
   conflicts were found in the file" rather than "You created over 50 conflicts."
3. When the actor is irrelevant — "The database was purged in January."

---

## Tense

Present tense for behavior that isn't tied to a particular time.

- Recommended: "Send a query to the service. The server sends an acknowledgment."
- Not recommended: "Send a query to the service. The server will send an acknowledgment."

Future tense is fine when you need to distinguish an action that happens later:
"Add the filename to the backup list. The file will be archived the next time
the backup process runs."

Avoid *would* for hypotheticals. Don't use future tense for features that have
already shipped.

---

## Modality

| Intent | Use | Example |
|---|---|---|
| Required action or state | *must*, or the imperative | "You must have the Editor role." |
| Recommended action | *We recommend*; *should* only for generally recognized best practice | "We recommend that you use a strong password." |
| Optional action | *can* | "You can also use approach B." |
| Expected outcome | present tense, no auxiliary | "The process returns 10 items." |
| Possible outcome | *might*, *can* | "The process can take about 30 minutes." / "You might be prompted for credentials." |

*may* is reserved for policy and legal statements. For possibility use *might*;
for permission use *can*.

Don't use *should* to describe an actual state — it's ambiguous between a
requirement and an observation.

- Not recommended: "The value should be true."
- Recommended: "You must set the value to true." (requirement)
- Recommended: "The server sets the value to true." (observation)
- Not recommended: "The Classroom Share Button should conform to our size guidelines."
- Recommended: "Ensure that the Classroom Share Button conforms to our size guidelines."

---

## Sentence and clause structure

Put the circumstance, condition, or goal before the instruction, so readers can
skip what doesn't apply to them.

| Recommended | Not recommended |
|---|---|
| For more information, see [link]. | See [link] for more information. |
| To delete the entire document, click **Delete**. | Click **Delete** if you want to delete the entire document. |
| If your app is in one of the following regions, custom domains might add latency: | Custom domains might add latency if your app is in one of the following regions: |

Subject + verb + object order. Keep the main subject and verb near the start.

**Paragraphs.** One idea per paragraph, in the fewest sentences possible. More
than five or six sentences usually means the paragraph is doing too much — but
don't split a paragraph that's genuinely one idea, and don't lengthen sentences
to reduce sentence count. Put the most important information first; readers
don't read every word. Left-align. Never force line breaks inside a paragraph.

**Sentence length.** Keep sentences short. The guide doesn't set a number;
around 25 words is a useful ceiling to check yourself against.

---

## Global audience

A large share of readers are reading in a second language, and much of this
text will be machine-translated.

**Simpler words.** *Start* not *commence*. *Use* not *utilize* or *leverage*.
Avoid phrasal verbs where a single verb works.

- Recommended: "This document uses the following terms:"
- Not recommended: "This document makes use of the following terms:"

**Limit modifiers; don't stack nouns.**

- Recommended: "A cloud-native DevSecOps pipeline in a hybrid environment"
- Not recommended: "A hybrid cloud-native DevSecOps pipeline"

**Place modifiers next to what they modify.**

- Recommended: "Request only one token."
- Not recommended: "Only request one token."

**Keep the optional words.** Redundancy that costs one word and buys clarity is
worth it, especially for translation.

| Recommended | Not recommended |
|---|---|
| If the VM has started and if you're able to connect… | If the VM has started and you're able to connect… |
| If the attribute key is not found, then the default value is returned. | If the attribute key is not found, the default value is returned. |
| Assumes that you have the following knowledge: | Assumes you have the following knowledge: |
| Identify all of the datasets. | Identify all the datasets. |
| Start the profiler, and then run the app. | Start the profiler, then run the app. |
| the rules that you previously defined | the rules you previously defined |

**Replace ambiguous pronouns with the noun.**

- Recommended: "If you use the term *green beer* in an ad, then make sure that the ad is targeted."
- Not recommended: "…then make sure that it's targeted."

**One term per concept.** Varying your vocabulary makes a translator — and a
reader — assume you mean different things. Pick a term and stay with it.

**Avoid** culturally specific references (holidays, sports, customs), idioms and
colloquialisms, humor, seasons ("in the fall" is hemisphere-dependent), and
US-centric examples. Use a diverse set of example names.

**Prefer affirmative instructions** over negative ones.

- Recommended: "You can continue without a path."
- Not recommended: "A missing path won't prevent you from continuing."

---

## Capitalization

Standard American English rules. Don't capitalize for emphasis; before
capitalizing a word, ask why.

- **Sentence case** for titles, headings, list items, table contents and
  headings, captions, glossary definitions, and labels in diagrams. Capitalize
  the first word, the first word after a colon, and proper nouns. No period at
  the end of a heading.
- When referencing another document's title or heading, use sentence case even
  if the original used title case.
- **Lowercase after a colon**, unless what follows is a proper noun, a heading,
  a quotation, or text after a label like **Note:**.
- **No all-caps** except in official names, always-capitalized abbreviations, or
  when referring to code that uses all-caps. (Placeholders are the exception —
  those are always all-caps.)
- **No camel case** except in official names or when referring to code.
- Don't rely on a capitalization difference to convey meaning.
- Lowercase glossary and index terms unless proper nouns.
- **Hyphenated words at the start of a heading:** capitalize only the first
  element, unless a later element is a proper noun.
- Don't name a casing style ("use camel case"). Describe it and give an example:
  "Enter the value with no spaces between words and the first letter of each
  word capitalized — for example, `AssertionAccount`."

---

## Pronouns, articles, possessives

**Ambiguous antecedents.** Every pronoun needs an unmistakable referent.

| Recommended | Not recommended |
|---|---|
| If you type text in the field, the text doesn't change. | If you type text in the field, it doesn't change. |
| Set this value to true. | Set this to true. |
| These approaches are your best options. | These are your best options. |

**Gender.** Singular *they*, not *he/she*.

**That vs. which.** *That* introduces a restrictive clause with no comma ("The
echidna that has a long snout is furry"). *Which* introduces a nonrestrictive
clause with a comma ("The echidna, which has a long snout, is furry"). *Whose*
works for things as well as people.

**Keep the optional *that*.**

- Recommended: "Right-click the link that you want to open."
- Not recommended: "Right-click the link you want to open."

**Articles.** Don't drop *a*, *an*, or *the* for brevity, including in headings.

- Recommended: "Create a VM instance"
- Not recommended: "Create VM instance"

Choose *a* or *an* by sound, not letter: *a SQL*, *a FHIR*, *an SAP*, *an SSD*.

**Possessives.**

- Singular nouns, including ones ending in *s*: add *'s* — "each vector's
  record", "the storage class's quota".
- Plural nouns ending in *s*: apostrophe only — "the models' capabilities".
- Never use *'s* to form a plural.
- Don't form possessives of product, feature, or trademark names. Recommended:
  "monitor Google Search performance" or "the performance of Google Search";
  not "Google Search's performance".
- Don't form possessives of code items. Recommended: "the `wordCount` method's
  return value" or "the value returned by the `wordCount` method"; not
  "`wordCount`'s return value".
- If a possessive is awkward, rewrite. "Analyze the business data" beats
  "Analyze the businesses' data."

---

## Punctuation

**Commas.**

- Use the serial (Oxford) comma: "zones, regions, and multi-regions".
- Comma after an introductory word or phrase: "Finally, only groups that
  contain parameters appear."
- Comma before a coordinating conjunction joining two independent clauses,
  unless both are very short. Recommended: "The libraries make feed creation
  easier, and they ensure that only valid feeds are produced." / "Type your ID
  and click **OK**."
- No comma between an independent and a dependent clause unless it prevents a
  misreading. Recommended: "Direct-access flags are plain variables and can be
  read directly."
- Comma before nonrestrictive *which*: "Name of the group, which has a maximum
  length of 200 characters."
- Semicolon (or period) before a conjunctive adverb, comma after: "The variable
  must have a value; otherwise, the server returns an error."
- Generally **no** comma before causal *because*, unless it starts a
  nonrestrictive clause. Recommended (nonrestrictive, so the comma stays): "You
  can use the same key name in multiple backend services and backend buckets,
  because each set of keys is independent of the others."

**Em dashes (—).** No spaces around them. Don't substitute an en dash or hyphen.
Don't use a dash to separate a term from its description — use a colon, a
period, or a description list.

- Recommended: "Example: This is an example."
- Not recommended: "Example - This is an example."

**En dashes (–).** Don't use. Use a hyphen or the word *to*.

**Colons.** The introductory phrase before a colon must be a complete sentence.

- Recommended: "The fields are defined as follows:"
- Not recommended: "The fields are:"

**Semicolons.** Avoid where possible. Three legitimate uses: joining closely
related independent clauses; before a conjunctive adverb (*therefore*) or
joining phrase (*that is*); separating series items that contain their own
punctuation.

**Hyphens.**

- Prefixes generally close up: *metadata*, *preprocessing*, *pseudocode*,
  *semiconductor*, *noncurrent*, *nonempty*.
- Hyphenate a prefix before a capital or number (*non-Google*, *post-2000*),
  with *self-* and *cross-*, before an already-hyphenated term, or when needed
  for readability (*de-energize*, *re-sign*).
- Prefer closed compound nouns: *webpage*, *hostname*, *tradeoff*, *workaround*.
- Hyphenate compound modifiers before a noun: *a well-designed app*, *a 64-bit
  system*, *a five-minute wait*, *Android-specific techniques*.
- Don't hyphenate *-ly* adverbs: "publicly available implementations".
- Generally no hyphen after a verb: "The app is well designed." But some terms
  stay hyphenated everywhere: *on-premises*, *add-on*, *cloud-based*,
  *customer-facing*, *user-friendly*.
- Ranges take a hyphen, not an en dash: "8-20 files", "5-10 minutes". Don't mix
  *from* with a hyphen — write "from 8 to 20 files".
- Suspended hyphens take a space after only: "one-, two-, or three-hour
  intervals".
- With unit abbreviations use a nonbreaking space, not a hyphen: "200 GB disk".

**Parentheses.** Don't put important information in them; readers skip
parentheticals. Consider commas, dashes, or a second sentence instead. A full
sentence inside parentheses keeps its period inside. Never write "file(s)".

- Recommended: "Enter a name for the instance—for example, `my-instance-99`."
- Not recommended: "Enter a name for the instance (for example, `my-instance-99`)."

**Quotation marks.** Straight, never curly — curly marks break code and
conversion tools get them wrong. Use them for titles of shorter works, sections
you can't link to, direct quotations, and metaphorical usage. Commas and periods
go inside the closing mark. Exception: with a literal string, put punctuation
outside so the string isn't misread — better still, use code font. Single quotes
only for nested quotations or for languages that use them in code.

**Slashes.** Don't use them for alternatives — write *or* or *and*. Avoid
*and/or*: "You can export raw events, processed events, or both." Don't use
slash abbreviations (*w/*, *c/o*). For rates use *per*: "requests per day", not
"requests/day". Fine in paths and URLs.

**Abbreviations.** Spell out on first reference, with the abbreviation in
parentheses: "The internet of things (IoT) service…". Italicize both the term
and the abbreviation on introduction. Don't capitalize the spelled-out form
unless it's a proper noun — "data manipulation language (DML)", not "Data
Manipulation Language (DML)". No periods in acronyms or initialisms. Never use
an abbreviation as a verb: "Use SSH to log in", not "Then ssh into".

Rarely need spelling out: AI, API, DVD, PDF, XML, HTML, PC, RAM, REST, URL, USB.

Don't use *e.g.*, *i.e.*, *etc.*, or internet slang.

---

## Inclusive language

| Avoid | Use |
|---|---|
| whitelist / blacklist / graylist | allowlist, denylist, or a domain-precise term |
| master / slave | primary / replica, controller / worker, parent / child |
| grandfathered | legacy, exempt |
| man-hours | person-hours |
| mankind | humanity |
| manpower | staff, workforce |
| crazy, insane | complicated, complex, baffling, strange, unexpected |
| dumb | describe what's actually happening |
| blind to, turn a blind eye to | a more accurate word |
| cripples | slows down, degrades |
| sanity check | final check for completeness and clarity |
| dummy variable | placeholder |
| hangs (a connection) | doesn't respond |
| hit (a UI element) | click, press |
| hover over | point to, hold the pointer over |
| native feature | built-in |
| native speaker | reframe so it applies to all readers |
| first-class citizen | a context-appropriate term |
| the disabled | people with disabilities |
| normal, healthy (meaning nondisabled) | nondisabled, sighted, hearing |
| wheelchair-bound | uses a wheelchair |
| the elderly, seniors | older adults |
| blackhat | illegal, unethical, rule-violating |

**When the term is literally in the code**, use the inclusive term in prose and
the literal term in code font.

- Recommended: "Add a user to the allowlist (`whitelist`) by entering: `whitelist adduser EMAIL_ADDRESS`"
- Not recommended: "Add a user to the whitelist by entering: …"

Avoid figurative language and metaphors generally — they translate poorly and
often carry unintended baggage.

---

## Jargon

Specialized terminology blocks readers who don't already share your context. In
order of preference:

1. **Write around it.** "When the project is finished, review what processes
   worked" instead of "hold a post-mortem". "Use an informal design process"
   instead of "back-of-the-envelope design".
2. **Replace it with something more specific.** *blast radius* → *affected
   area*. *ingest* → *import* or *load*. *off-the-shelf* → *ready-made*.
3. **Using it once? Gloss it inline.** "You then move the task to an earlier
   part of the process (also known as *shifting left*)."
4. **Using it throughout? Define it on first use**, then use it freely. "The
   application is in the same state as a *cold standby* (a backup or redundant
   system)."

---

## Timeless documentation

Describe the current state, not the change.

| Recommended | Not recommended |
|---|---|
| These subcommands let you interact with HTTP load balancing. | These new subcommands let you interact with HTTP load balancing. |
| The following options aren't supported: | The following options aren't currently supported: |
| The emulator supports the following filters: | The emulator now supports the following filters: |

Eliminate: *as of this writing*, *currently*, *does not yet*, *eventually*,
*existing*, *future*, *latest*, *new*, *now*, *old*, *presently*, *soon*.

Exception: release notes, changelogs, blog posts, and press releases exist to
mark change and can use these words.

Don't document unreleased features at all.

---

## Excessive claims

- Avoid superlatives and subjective language: *best*, *simplest*, *fastest*,
  *never*, *always*. Be careful with *ensure* and *guarantee*.
- Cite the source for any performance claim.
- Hedge security claims. Recommended: "Using our security product is part of an
  overall strategy that helps prevent account takeovers from phishing attacks."
  Not recommended: "Our security product prevents account takeovers."
- Scope competitive comparisons. Recommended: "Our product distributes datasets
  in memory across a cluster, and therefore it can be faster for this scenario
  than ExampleCorp's product." Not recommended: "Our product is faster than
  ExampleCorp's product."

---

## Word list

The entries developers hit constantly.

**Filler and condescension**

| Term | Guidance |
|---|---|
| easy, easily | What's easy for you might not be easy for others. Delete it. |
| simple, simply | Same. If you mean few steps, say "requires only a few steps". |
| just | Filler. Delete without changing the meaning. |
| please | Don't use in instructions. |
| currently | Implied. Also risks disclosing roadmap. |
| obviously, of course, clearly | Not a word-list entry, but the same problem as *simply*: it tells a stuck reader their problem is trivial. Delete. |
| desire, desired | Use *want* or *need*. |

**Wordiness**

| Term | Guidance |
|---|---|
| in order to | Use *to*. |
| leverage | Use *use*, or something more precise. |
| utilize | Use *use*. |
| execute | Use *run* when the meaning is the same. |
| allows you to | Use *lets you*. |
| e.g. | Use *for example* or *such as*. |
| i.e. | Use *that is*. |
| etc., and so on | Avoid. Rewrite as "problems such as instability or high latency". |
| and/or | Don't use unless space is limited, such as in a table. Otherwise rewrite: "raw events, processed events, or both". |
| as (meaning *because*) | Use *because*. |
| once (meaning *after*) | Use *after*. |
| via | Not a word-list entry. Prefer *with*, *by using*, or *through* — plainer words translate better. |

**Modality**

| Term | Guidance |
|---|---|
| may | Reserve for policy and legal. Use *can* or *might* otherwise. |
| might | Possibility, uncertain outcome. |
| can | Permission, ability, optional action, possible outcome. |
| must | Required action or state. *You need* also works. |

**Actions and interfaces**

| Term | Guidance |
|---|---|
| kill, abort | Use *stop*, *exit*, *cancel*, or *end*. |
| hit | Not a synonym for *click*, *press*, or *type*. |
| click | Desktop with a mouse. Not "click on". |
| check (a checkbox) | Use *select*; the opposite is *clear*. |
| enter / type | *Enter* for entering text generally; *type* for literal typing. |
| disable / disabled | Don't use for something broken. Use *inactive*, *unavailable*, *turn off*. |
| deprecated | Recommending against use — not *removed*, *deleted*, or *shut down*. |
| above / below | For versions use *later* / *earlier*. For document position use *preceding* / *following*. |
| drop-down | Usually omit: just "list" or "menu". |
| email | Not *e-mail*. Not a verb — "send email". |
| on-premises | Not *on prem*, *on premise*, or *on-premise*. Always hyphenated. |
| log in / login | *Sign in* is generally better. Verb is *log in*, noun is *login*. |
| native | Imprecise. Prefer *built-in*. Never use of people. |

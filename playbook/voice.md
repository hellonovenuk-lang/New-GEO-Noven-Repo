# Writing that doesn't read as machine-written

**Status: Live.** Applies to everything a customer or prospect reads — site copy,
emails, audit reports, quotes, proposals. Not to the operating documents in
`playbook/` and `archive/`, which are read by the assistant far more often than
by a person.

**A framework, not a rule set.** Adopted by the owner 2026-08-09 from
`github.com/blader/humanizer`, explicitly as a general overview rather than a
checklist to satisfy every time. **A sentence that breaks one of these and reads
better for it is the right sentence.** The failure this exists to prevent is copy
that is technically compliant and still sounds generated.

**Why it matters more here than at most businesses.** The site's whole argument
is that a real person did real work. Copy with the machine tells in it undercuts
that before a word of the argument lands, and `CLAUDE.md`'s design rule already
bans the visual version of the same problem.

---

## The structural one, which matters more than any word choice

**Say who you are before you say what you found.**

Automated outreach opens with the hook, because a template has no self to
introduce. A person says who they are and why they are writing, then gets to the
point. **This single change does more than the whole list below**, and it was the
fault in the first version of both cold emails: they opened "I asked ChatGPT..."
and read as software.

**The same applies to subject lines.** A subject that makes a claim reads as a
campaign. A subject that names the thing reads as a person. "[Practice] and
ChatGPT" is written by someone. "[Practice] doesn't come up on ChatGPT" is
written by a growth team.

---

## The tells worth actually watching

Grouped by how often they show up in this repo's own drafts, not by the source's
ordering.

**Rhythm and shape**

- **The rule of three.** Three items, three clauses, three short sentences in a
  row. Real writing has uneven quantities. This is the most common tell in
  everything drafted here so far.
- **Staccato drama.** Short. Punchy. Fragments for effect. Vary the length
  instead, and put a concrete claim in the long ones.
- **Em dashes.** A comma, a full stop, a colon or brackets will do. The site copy
  was already stripped of these on 2026-08-09 for exactly this reason.
- **Negative parallelism.** "It isn't just X, it's Y." State the point.
- **False ranges.** "Everything from X to Y." List the things.

**Word choice**

- **Machine vocabulary.** "Testament", "landscape", "showcasing", "leverage",
  "seamless", "robust". Use the word a person would say out loud.
- **Copula avoidance.** "Serves as", "boasts", "features". It is fine to write
  "is" and "has".
- **Synonym cycling.** Repeat the clearest word rather than reaching for a
  variant. A dentist is a dentist in the second paragraph too.
- **Hedge stacking.** One qualifier, not "could potentially possibly".
- **Filler.** "In order to" is "to".

**Tone**

- **Signposting.** "Let's dive in", "First, some context". Start with the
  content.
- **Fake candour.** "Honestly?" and "Here's the thing" are as templated as the
  thing they are pretending not to be.
- **Chatbot closers.** "I hope this helps, let me know if you have any
  questions."
- **Promotional adjectives.** Describe plainly and let the reader decide whether
  it is impressive.
- **Significance inflation.** No "in today's fast-moving landscape". Say the
  concrete thing that is true.

**Formatting**

- **Boldface on routine terms.** Emphasis stops working when everything has it.
  Client-facing prose should mostly have none.
- **Title Case Headings.** Sentence case.
- **Emoji.** None.

---

## The rule that is not negotiable

**No fabrication.** Specificity comes from the facts we hold, never from the
rewrite. A rewrite that makes copy sound more human by inventing a number, a
name, a date or a testimonial has done the one thing this business cannot
survive doing. `CLAUDE.md`'s facts rule already says this and it outranks
everything above.

---

## How to use it

**Write the thing, then read it back for these.** Do not compose against the
list, or the copy comes out stilted in a new way. Two passes: say it plainly,
then take out what a machine would have put in.

**Where it does not apply.** `playbook/`, `archive/`, source comments, commit
messages. Those are working documents whose job is to keep the reasoning, and
the reasoning is worth more than the rhythm.

# Site code locations and isolation rules

*Where published copy lives and what must stay true.*

---

## The one rule that matters

**The visible copy and machine-readable description come from the same source and must agree.** `business.ts` feeds both the pricing page and the structured data.

**Change a level in one place and change it in all three.** A client and an assistant end up being told different things otherwise — the one failure this business cannot have.

---

## Where each piece lives

| What | File | Content |
|---|---|---|
| **Canonical source** | `site/src/data/business.ts` | Three `schemaDescription` fields (Audit, Foundation, Maintain, Grow, Lead) |
| **Pricing page** | `site/src/pages/pricing.astro` | Three `.level` descriptions and the "Ongoing" intro paragraph |
| **How it works** | `site/src/pages/how-it-works.astro` | Sentence summarising the three levels in stage 03 |
| **FAQ page** | `site/src/pages/faq.astro` | No level descriptions — keep it this way |

---

## The FAQ guard rail

Do not add level descriptions to `site/src/pages/faq.astro`. Anything in the `faqs` array gets published into the FAQPage structured data as well as the visible page, so a level description added there is a **third place that can drift out of step.**

The only mention is that moving between levels works like cancelling, which stays as-is.

---

## Homepage structural invariant

Both homepage code panels are **byte-identical to the JSON-LD in the head.** This property is enforced by `site/src/lib/json-code.ts` and cannot be broken.

The code block types itself in from an empty start (~620 chars/sec), so URL inspection snapshots land inside that animation window. This is accepted and not a fault — the visible HTML carries the full block; all facts are in `<head>` too.

---

## The build verification

After changes, verify the build is clean:

- 7 pages total
- All JSON-LD parses
- Both homepage code panels still byte-identical to the JSON-LD in the head

# Audit automation findings

**Branch:** `gpt/audit-automation-findings`  
**Basis:** Fresh review of `main` only. Unmerged Claude branches were deliberately ignored.  
**Purpose:** Record a proposed operating model for automating the £30 Audit while preserving the commitments currently made on the public site.

---

## 1. Current public commitments that the system must preserve

The Audit currently promises a written report covering:

- what ChatGPT, Google's AI results, Copilot and Perplexity say when asked questions customers are likely to ask;
- what those systems say or appear to believe about the business;
- whether those facts are accurate;
- the specific things blocking the business, explained plainly;
- an honest recommendation, including the possibility that no further spend is needed;
- delivery within one working day once scope and payment are confirmed.

The site also says the report is genuine standalone work and can be taken elsewhere or acted on independently.

A separate public statement says the report is one Kieran wrote. That means the safest automation model is not fully autonomous delivery. The system can collect evidence, classify straightforward findings and draft the report, but Kieran should remain responsible for the final diagnosis and recommendation.

---

## 2. Recommended operating model

### Automated collection, human-approved conclusion

Recommended flow:

1. Customer pays.
2. Customer completes a tightly controlled intake form.
3. The system validates the submitted business identity and website.
4. It generates or selects suitable customer questions.
5. It runs assistant tests and deterministic website checks.
6. It discovers and compares accessible public business sources.
7. It stores the evidence in a structured record.
8. It drafts the report.
9. Kieran reviews, edits if needed and approves the recommendation.
10. The final PDF is generated and emailed automatically.

The target should be roughly 5–15 minutes of human review per routine audit, not an hour of manual research.

Publicly, keep the existing one-working-day promise until enough real audits have been timed. Internally, aim for delivery within an hour where the evidence is complete and unambiguous.

---

## 3. The audit should have three evidence layers

The strongest framing is:

1. **What assistants actually say**
2. **How consistently the business is represented across the public web**
3. **What the website exposes to crawlers and machines**

The second and third layers do not reveal a model's private internal knowledge. They provide evidence that may help explain the observed assistant responses.

---

## 4. Layer one — what assistants actually say

This is the direct observation layer.

### Example prompt categories

- Direct lookup: `What does [business] do?`
- Recommendation: `Who provides [service] in [location]?`
- Comparison: `Which [service providers] should I consider in [location]?`
- Qualification: `Who can help with [specific customer problem]?`
- Trust: `Is [business] reputable?`
- Practical facts: service area, opening hours, prices or availability where relevant.

### What to record for every run

- assistant and model surface tested;
- exact prompt;
- date, time and relevant location context;
- whether the client appeared;
- prominence or ordering in the response;
- competitors named;
- factual claims made about the client;
- factual errors or omissions;
- citations or sources shown;
- variation between repeat runs.

### Recommended initial test volume

A £30 Audit should not blindly inherit the monthly plan's full monitoring volume.

A sensible first version:

- eight core questions;
- two runs per question per assistant;
- four assistant surfaces;
- 64 observations in total;
- extra runs only where the first two materially conflict.

The run count should be validated against actual API/tool cost, elapsed time and result variance during the first live audits.

### What the report can safely say

Good:

> The business was not named in either of two Perplexity responses for “emergency plumber in Birkenhead”.

Avoid:

> Perplexity does not know this business.

The former is an observation. The latter claims access to private model state that the audit does not have.

---

## 5. Layer two — public-web consistency

Recommended customer-facing label:

> **What the wider web says**

This layer compares the business facts published across accessible search results, profiles, registers and directories.

### Facts to extract

- business name;
- website URL;
- telephone number;
- address;
- service area;
- opening hours;
- business category;
- services;
- founder or legal business identity;
- social profiles;
- review presence and count where publicly accessible;
- whether the source appears active or stale.

### Potential sources

- Google Business Profile / Google search results;
- Bing Places / Bing results;
- Apple Maps or Apple Business Connect where accessible;
- Companies House where relevant;
- LinkedIn;
- Facebook;
- Yell;
- Yelp;
- Trustpilot;
- Checkatrade and sector-specific directories;
- professional registers;
- trade associations;
- local chambers and local business directories;
- the client's own website.

The report should say which accessible sources were checked. It should not claim to have checked every directory on the internet.

### Collection methods

#### API-first

Use official APIs where available. This gives more stable and structured data and reduces maintenance and compliance risk.

#### Search-result discovery

Use searches such as:

- exact business name;
- exact business name plus phone or location;
- exact phone number;
- exact website domain;
- domain-restricted searches for major directories.

Search snippets may be stale, so discovered pages should be opened and verified where possible.

#### Controlled page extraction

For accessible public pages, extract visible business details using domain-specific parsers or a general structured extraction step.

The system needs:

- per-domain rate limits;
- respect for robots rules and site terms;
- failure handling for blocked pages;
- recorded source URL and retrieval time;
- snapshots or stored extracted evidence sufficient to support the report.

### Fact normalisation

Before comparison, equivalent formats must be normalised.

Examples:

- `0151 123 4567`
- `01511234567`
- `+44 151 123 4567`

These may be the same number.

Likewise, `Smith Heating Ltd` and `Smith Heating Limited` may be equivalent, while `Smith Plumbing` and `Smith Heating` may be a meaningful contradiction.

Each field should be classified as:

- exact match;
- equivalent match;
- partial match;
- contradiction;
- missing;
- could not verify.

### Safe conclusion language

Good:

> Public sources disagree about the business name, phone number and service area. These inconsistencies may weaken confidence in which details are current and authoritative.

Avoid:

> These directory inconsistencies definitely caused ChatGPT not to recommend the business.

The evidence supports a plausible contributor, not proof of causation.

---

## 6. Layer three — website exposure and structure

Recommended customer-facing label:

> **What your website makes clear**

This is the most deterministic and automatable part of the audit.

### A. Access and response checks

Test:

- domain availability;
- HTTPS validity;
- `www` and apex behaviour;
- redirect chains and loops;
- HTTP status codes;
- whether important pages return usable HTML;
- whether critical content depends entirely on client-side JavaScript;
- whether pages require authentication.

### B. Crawler permissions

Fetch and inspect:

- `/robots.txt`;
- `/sitemap.xml`;
- sitemap indexes;
- page-level robots meta tags;
- `X-Robots-Tag` response headers;
- relevant crawler-specific restrictions.

Important distinctions:

- a missing `robots.txt` is not automatically a problem;
- a rule blocking important content is a problem;
- `noindex`, blocked directories and broken sitemap references should be reported precisely.

### C. Crawl and page inventory

Build an inventory from the homepage, internal links and sitemap:

- URL;
- status code;
- canonical URL;
- title;
- meta description;
- H1 and heading hierarchy;
- approximate word count;
- internal links;
- indexability;
- structured-data types;
- last-modified signals where available.

This can identify:

- missing service or location pages;
- orphan pages;
- duplicate titles and descriptions;
- thin or near-duplicate pages;
- broken internal links;
- contradictory old pages;
- pages present in the sitemap but inaccessible;
- important pages that are not linked internally.

### D. Visible business facts

Extract visible statements about:

- business name;
- address;
- phone;
- email;
- opening hours;
- services;
- pricing;
- areas served;
- qualifications;
- guarantees;
- turnaround times;
- founder or company identity.

Compare the same fact across pages and flag contradiction, ambiguity or absence.

### E. Structured data

Parse JSON-LD and other structured data.

Relevant types and properties may include:

- `Organization`;
- `LocalBusiness` or a suitable subtype;
- `ProfessionalService`;
- `Service`;
- `Person`;
- `FAQPage`;
- `Offer`;
- `PostalAddress`;
- `OpeningHoursSpecification`;
- `areaServed`;
- `sameAs`;
- `url`;
- `telephone`;
- `priceRange`;
- supported rating data where legitimately present.

Check:

- whether the JSON parses;
- whether required and useful fields are present;
- whether URLs and identifiers resolve;
- whether structured facts agree with visible facts;
- whether prices, phone numbers, names, areas and opening hours drift between schema and page copy;
- whether FAQ schema matches visible FAQ content.

### F. Question-answer coverage

For each selected customer question, test whether the site contains:

- a relevant page;
- a clear heading;
- a direct answer near the top;
- business-specific detail;
- relevant geographic information;
- pricing or qualification detail where appropriate;
- sensible internal links;
- enough evidence to distinguish the business from generic competitors.

Example:

Question:

> Does this plumber offer emergency callouts on Sundays?

Strong evidence:

- a dedicated emergency service page;
- explicit Sunday availability;
- areas covered;
- callout terms;
- a clear phone number.

Weak evidence:

- a generic homepage statement such as “We are always here to help”;
- no hours;
- no Sunday wording;
- no emergency service page.

The report can safely say:

> The website does not provide a clear, verifiable answer to Sunday emergency availability.

That is more useful and defensible than a vague claim that the site is “not GEO optimised”.

---

## 7. How the three layers combine into a diagnosis

Example evidence:

### Assistant observation

The client appeared in one out of eight recommendation questions.

### Public-web consistency

Google, Facebook and Yell disagree about the business name, telephone number and service area.

### Website exposure

The website:

- loads and is indexable;
- has no useful business structured data;
- does not clearly state areas served;
- has no individual service pages.

A defensible conclusion would be:

> The site is technically accessible, but the business is represented inconsistently across public sources and the website provides weak, unstructured evidence about its services and geographic coverage. These are credible contributors to its low recommendation visibility, although no single change can guarantee inclusion.

This connects evidence without claiming proprietary knowledge or guaranteed causation.

---

## 8. Recommended report structure

### Executive result

Use a plain classification rather than a pseudo-scientific percentage score:

- visible;
- partially visible;
- not reliably visible;
- incorrectly represented;
- inconclusive because evidence was incomplete.

### What was tested

List:

- assistants;
- exact questions;
- date and location context;
- number of repeat runs;
- public sources checked;
- website pages crawled.

### What assistants said

A compact evidence table containing:

- question;
- assistant;
- whether the client appeared;
- prominence;
- competitors mentioned;
- factual errors;
- citations or sources shown.

### What the wider web says

Show fact consistency across sources and identify contradictions, missing fields and stale information.

### What the website makes clear

Report access, crawlability, structured data, page coverage, business facts and question-answer gaps.

### Recommended action

Constrain the final outcome to one of four categories:

1. no paid work recommended;
2. a small set of self-service corrections;
3. Foundation recommended;
4. further investigation required before recommending work.

The fourth outcome is important. The system must be allowed to say that it does not have enough evidence.

### Suitable next service

Recommend the Foundation only where the findings map to its actual scope:

- crawler access;
- structured data;
- consistent business facts;
- pages that answer important customer questions.

Do not build the report so that every customer predictably “discovers” they need the £350 service.

---

## 9. Evidence labels inside the report

Every material finding should be labelled by confidence type.

### Observed

> The business was not named in either of two assistant responses for the tested question.

### Verified technical issue

> No LocalBusiness or equivalent structured business entity was found on the website.

### Possible contributor

> The absence of a clearly stated service area may make it harder to associate the business with the tested location.

### Not established

> The audit cannot establish that adding schema alone would cause the business to be recommended.

This separation should be enforced in the report-generation schema, not left to writing style alone.

---

## 10. Technical workflow

Recommended high-level architecture:

`checkout -> payment webhook -> intake -> audit job -> evidence store -> report draft -> human approval -> PDF -> transactional email`

Suggested job states:

- `paid`
- `intake_received`
- `validated`
- `collecting`
- `draft_ready`
- `approved`
- `delivered`
- `failed`
- `manual_review_required`

Required safeguards:

- idempotency for payment webhooks;
- queueing for simultaneous orders;
- retryable individual stages;
- timeouts;
- an exception inbox;
- logging of prompts, model surface, responses and timestamps;
- permanent evidence snapshots;
- versioning of question selection, extraction rules and report logic;
- manual-review flags for ambiguous business identities, blocked sources or conflicting evidence.

Do not make the audit one long script where one failed assistant call destroys the whole report.

---

## 11. Separation of responsibilities inside the system

The most important technical rule:

1. deterministic code collects objective signals;
2. rules classify straightforward findings;
3. an LLM turns structured evidence into readable prose;
4. Kieran approves the diagnosis and recommendation.

Do not ask an LLM to browse freely, invent its own evidence and decide what service to sell. The language model should write from a closed evidence object containing citations, source URLs, timestamps and allowed conclusion types.

---

## 12. Intake requirements

After payment, collect at minimum:

- legal or trading business name;
- website;
- primary trading location;
- service areas;
- main category;
- up to five priority services;
- customer type: local consumer, regional consumer, national B2B or mixed;
- optional known competitors;
- known Google Business Profile and social/profile links;
- common customer questions;
- confirmation that submitted facts are accurate;
- permission to analyse publicly available business information.

Question generation depends heavily on location, customer type and service specificity. Those should not be inferred from a bare domain where the intake can state them directly.

---

## 13. Commercial and delivery view

At £30, the Audit is viable primarily as a highly automated paid qualification and evidence product.

Suggested target economics:

- payment and tool costs ideally below £3;
- automated elapsed processing under 15 minutes for routine cases;
- human approval under 10 minutes;
- total direct cost, including owner time, below roughly £10–£12;
- conversion to Foundation measured, not forced.

Recommended rollout:

### Version 1

- payment and structured intake;
- automated website analysis;
- automated report skeleton;
- manual assistant testing or partially automated evidence collection;
- manual approval.

### Version 2

- automated question selection;
- automated assistant runs;
- public-source consistency engine;
- report drafting;
- human approval for every report.

### Version 3

- automatic delivery only for narrowly defined, high-confidence cases;
- ambiguous, commercially significant or incomplete cases routed to manual review.

---

## 14. Claims to avoid

Do not say:

- “ChatGPT's database contains this fact.”
- “The AI does not know your business.”
- “Schema will make ChatGPT recommend you.”
- “This directory is used by every assistant.”
- “This issue caused your absence.”
- “Your GEO score proves you need Foundation.”

Prefer:

- “The assistant stated…”
- “The following public sources state…”
- “The website exposes…”
- “These findings may reduce clarity or confidence…”
- “We recommend addressing these findings because…”

---

## 15. Proposed customer-facing explanation

### What assistants say

We test the questions your customers are likely to ask and record whether you appear, what is said about you and which competitors are mentioned.

### What the wider web says

We compare the business facts published across accessible search results, profiles and directories to identify missing, outdated or contradictory information.

### What your website makes clear

We inspect whether crawlers can access the site, whether its business facts are machine-readable and consistent, and whether its pages directly answer important customer questions.

---

## 16. Current recommendation

Proceed with the concept, but treat it as an evidence pipeline with human-approved conclusions rather than an autonomous AI report generator.

The core proposition is sound because the three layers complement each other:

- assistant testing shows the actual outcome;
- public-source comparison shows whether the wider identity is coherent;
- website analysis shows what the business itself makes available to machines.

Together they support a useful diagnosis while keeping the report honest about uncertainty, causation and the limits of external observation.

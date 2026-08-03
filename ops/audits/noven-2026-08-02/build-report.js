/* Builds the client-facing audit report as .docx.
 *
 * Typography follows site/src/styles/global.css: the display serif falls back
 * to Palatino Linotype and the sans to Segoe UI, both of which ship with
 * Windows and Office, so this renders as intended without installing fonts.
 * Colours are the brand tokens, unchanged.
 */

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, ShadingType, HeadingLevel,
  Header, Footer, PageNumber, LevelFormat, convertMillimetersToTwip,
} = require('docx');

/* ------------------------------------------------------------ brand tokens */
const NAVY = '170969';
const INK = '16161D';
const INK_SOFT = '565B66';
const INK_FAINT = '6A6F7C';
const BRASS = '8A6A28';
const RULE = 'E2DFD6';
const PAPER2 = 'F7F5EF';

const SERIF = 'Palatino Linotype';
const SANS = 'Segoe UI';

/* A4 with 25mm side margins. Text column = 9070 DXA (~16cm). */
const TEXT_W = 9070;

const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: NONE, bottom: NONE, left: NONE, right: NONE };

/* ---------------------------------------------------------------- helpers */

function body(text, opts = {}) {
  return new Paragraph({
    spacing: { line: 288, lineRule: 'auto', after: opts.after ?? 160 },
    indent: opts.indent,
    children: runs(text, { font: SANS, size: 20, color: INK }),
  });
}

/* Splits **bold**, *italic* and `mono` inline markers into runs. */
function runs(text, base) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ ...base, text: text.slice(last, m.index) }));
    const tok = m[0];
    if (tok.startsWith('**')) {
      out.push(new TextRun({ ...base, text: tok.slice(2, -2), bold: true }));
    } else if (tok.startsWith('`')) {
      out.push(new TextRun({ ...base, text: tok.slice(1, -1), font: 'Consolas', size: (base.size || 20) - 2 }));
    } else {
      out.push(new TextRun({ ...base, text: tok.slice(1, -1), italics: true }));
    }
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ ...base, text: text.slice(last) }));
  return out;
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 420, after: 180 },
    children: [new TextRun({ text, font: SERIF, size: 30, color: NAVY, bold: false })],
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: 'noven-bullets', level: 0 },
    spacing: { line: 288, lineRule: 'auto', after: 120 },
    children: runs(text, { font: SANS, size: 20, color: INK }),
  });
}

/* Pull-quote: serif, indented, brass hairline on the left. */
function quote(text, attrib) {
  return new Paragraph({
    spacing: { before: 200, after: 200, line: 288, lineRule: 'auto' },
    indent: { left: 340 },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: BRASS, space: 14 } },
    children: [
      ...runs(text, { font: SERIF, size: 21, color: INK, italics: true }),
      new TextRun({ text: `  — ${attrib}`, font: SANS, size: 17, color: INK_FAINT, italics: false }),
    ],
  });
}

function cell(text, { widths, bold = false, header = false, align = AlignmentType.LEFT, size = 18 } = {}) {
  return new TableCell({
    width: { size: widths, type: WidthType.DXA },
    shading: header ? { type: ShadingType.CLEAR, fill: PAPER2, color: 'auto' } : undefined,
    margins: { top: 90, bottom: 90, left: 130, right: 130 },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: RULE },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: RULE },
      left: NONE, right: NONE,
    },
    children: [new Paragraph({
      alignment: align,
      spacing: { line: 264, lineRule: 'auto', after: 0 },
      children: [new TextRun({ text, font: SANS, size, color: header ? NAVY : INK, bold: bold || header })],
    })],
  });
}

function spacer(after = 0) {
  return new Paragraph({ spacing: { after }, children: [] });
}

/* ------------------------------------------------------------------ tables */

const bandCols = [4270, 1600, 1600, 1600];
const bandRows = [
  ['Who can help my business show up when people ask ChatGPT for a recommendation?', '0 of 10'],
  ['Can you recommend someone in the UK who gets small businesses mentioned by AI assistants?', '0 of 5'],
  ['I need someone on the Wirral who can get my business recommended by AI assistants', '0 of 5'],
  ["Who's good at getting small service businesses recommended by AI assistants?", '0 of 5'],
  ['Which UK businesses do this for sole traders and small firms rather than big brands?', '0 of 5'],
  ['Customers are finding people through ChatGPT and we never come up — who do I call?', '0 of 10'],
  ["I'm looking for someone in the UK to do this. What are my options and what should it cost?", '0 of 5'],
];

const bandTable = new Table({
  columnWidths: bandCols,
  width: { size: TEXT_W, type: WidthType.DXA },
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        cell('What we asked', { widths: bandCols[0], header: true }),
        cell('ChatGPT', { widths: bandCols[1], header: true, align: AlignmentType.CENTER }),
        cell('Gemini', { widths: bandCols[2], header: true, align: AlignmentType.CENTER }),
        cell('Perplexity', { widths: bandCols[3], header: true, align: AlignmentType.CENTER }),
      ],
    }),
    ...bandRows.map(([q, n]) => new TableRow({
      children: [
        cell(q, { widths: bandCols[0] }),
        cell(`never (${n})`, { widths: bandCols[1], align: AlignmentType.CENTER }),
        cell(`never (${n})`, { widths: bandCols[2], align: AlignmentType.CENTER }),
        cell(`never (${n})`, { widths: bandCols[3], align: AlignmentType.CENTER }),
      ],
    })),
  ],
});

const compCols = [6070, 3000];
const competitors = [
  ['Tilio', '36'], ['Rank4AI', '29'], ['AEO Agency', '14'], ['Dynamically', '12'],
  ['Exposure Ninja', '9'], ['GEOQ', '8'], ['GEO Intelligence', '8'], ['ClickSlice', '8'],
  ['Otter Labs', '7'], ['Consilium Design', '7'],
];

const compTable = new Table({
  columnWidths: compCols,
  width: { size: TEXT_W, type: WidthType.DXA },
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        cell('Business', { widths: compCols[0], header: true }),
        cell('Times named', { widths: compCols[1], header: true, align: AlignmentType.RIGHT }),
      ],
    }),
    ...competitors.map(([n, c]) => new TableRow({
      children: [
        cell(n, { widths: compCols[0] }),
        cell(c, { widths: compCols[1], align: AlignmentType.RIGHT }),
      ],
    })),
  ],
});

/* ---------------------------------------------------------------- document */

const logo = fs.readFileSync('logo.png');

const doc = new Document({
  creator: 'Kieran Smith',
  title: 'What AI assistants say about Noven',
  description: 'AI assistant visibility audit, 3 August 2026',
  numbering: {
    config: [{
      reference: 'noven-bullets',
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 340, hanging: 200 } },
                 run: { color: BRASS, font: SANS } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: convertMillimetersToTwip(22), bottom: convertMillimetersToTwip(20),
                  left: convertMillimetersToTwip(25), right: convertMillimetersToTwip(25) },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          border: { top: { style: BorderStyle.SINGLE, size: 2, color: RULE, space: 8 } },
          children: [
            new TextRun({ text: 'Noven  ·  AI assistant visibility audit  ·  3 August 2026', font: SANS, size: 15, color: INK_FAINT }),
            new TextRun({ text: '        ', font: SANS, size: 15 }),
            new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 15, color: INK_FAINT }),
          ],
        })],
      }),
    },
    children: [
      /* masthead */
      new Paragraph({
        spacing: { after: 420 },
        children: [new ImageRun({ type: 'png', data: logo, transformation: { width: 118, height: 26 } })],
      }),

      new Paragraph({
        spacing: { after: 90 },
        children: [new TextRun({ text: 'What AI assistants say about Noven', font: SERIF, size: 46, color: NAVY })],
      }),
      new Paragraph({
        spacing: { after: 60 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: BRASS, space: 10 } },
        children: [],
      }),
      new Paragraph({
        spacing: { before: 60, after: 400 },
        children: [new TextRun({ text: 'Prepared for Kieran Smith    ·    3 August 2026', font: SANS, size: 19, color: INK_SOFT })],
      }),

      h2('What we did'),
      body('On 2 and 3 August 2026 we asked the AI assistants your customers use — ChatGPT, Google’s Gemini, Microsoft Copilot and Perplexity — ten questions of the kind someone would ask after noticing that customers find businesses through ChatGPT.'),
      body('We asked each question five times, and the three most important ten times, because these systems do not give the same answer twice. We recorded **228 answers in full**. We then looked at your website and at how these systems reach it, to work out why the answers came back the way they did.'),
      body('Two things worth knowing before you read the rest:'),
      bullet('**Their answers vary.** The same question asked five times can produce five different answers. That is why we ask everything several times and report a range rather than a verdict. Anyone who gives you a single confident score is reporting one roll of a dice.'),
      bullet('**We check through the developer versions of these systems.** The apps on your phone answer slightly differently and take your own history into account, so if you ask ChatGPT about yourself you may see something different from what we saw. Both are real. Neither is the whole picture.'),

      h2('Where you show up today'),
      body('**Across the 168 checks where we did not mention your name, Noven was named 0 times.**', { after: 220 }),
      bandTable,
      spacer(160),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: 'Bands: never (0 of 5), occasionally (1–2), often (3–4), consistently (5).', font: SANS, size: 17, color: INK_FAINT, italics: true })],
      }),
      body('Copilot and Google’s AI results can’t be checked automatically, so we asked those by hand — the three questions that matter most, three times each, in a logged-out browser. **Noven was not named in any of the 18 answers.** Copilot and Google named entirely different businesses: not one name appeared on both.'),

      h2('What they believe about you'),
      body('This is where the audit found something more serious than absence.'),
      body('When we asked all three assistants *“What do you know about Noven?”* — thirty separate times — **every single answer was about a pharmaceutical company in Miami.**'),
      quote('“There are several entities named ‘Noven’… Noven Pharmaceuticals, Inc. — a Miami-based specialty pharmaceutical company founded in 1987, focused on transdermal drug delivery (patches)”', 'Perplexity, 2 August 2026'),
      body('Then we asked the harder version, naming your location: *“Is Noven on the Wirral any good, and what do they do?”* Even handed the town, only one assistant found you:'),
      quote('“Noven is a digital services consultancy based on the Wirral, Merseyside, run by sole founder Kieran Smith.”', 'Gemini, 2 August 2026'),
      body('Gemini got this right five times out of five. ChatGPT did not. Four times out of five it answered about a building firm:'),
      quote('“If you mean Noven Build Limited — the building/renovation firm that appears in North West trade listings — I’d be cautious rather than enthusiastic.”', 'ChatGPT, 2 August 2026'),
      body('That is the finding that matters most. Someone who hears your name, asks ChatGPT about you, and gets a lukewarm verdict on an unrelated builder has no way of knowing they are reading about a different business.'),
      body('Asked who your alternatives are, all three assistants answered with pharmaceutical companies.'),
      body('**One wrong fact of a different kind, already corrected.** Google’s stored description of your pages still carried your old prices — a £30 audit and a £350 setup, against the £125 and £750 you charge. Anyone asking an assistant what this should cost could have been quoted less than a quarter of your real fee. You asked Google to re-read the pages on 3 August; that takes days to weeks to settle.'),

      h2('Who gets recommended instead'),
      body('Named in the answers to the questions above, counted across all runs:', { after: 220 }),
      compTable,
      spacer(220),
      body('Dynamically was also named by Google when we asked by hand about the Wirral, as was Max Web Solutions — so they hold that ground on more than one system.'),
      body('What the named businesses visibly have that you don’t: a page about this specific service that has been live long enough to be read, and appearances on other people’s “best of” lists. Your site was published days before this audit ran. **Not one of the 210 automated answers cited novenstudio.co.uk as a source.**'),

      h2('What’s holding you back'),
      body('**1. Your name belongs to somebody else — at least four times over.** A US pharmaceutical company, a North West builder, an AI product trading as `noven.studio`, and a fourth business at `noven.io` all answer to Noven. The third is the most damaging: its name is your web address with the dot moved, and it works in your field. This costs you the moment anyone hears your name and checks. Fixing it isn’t website work — it needs a decision about the name before anything else is worth doing.'),
      body('**2. Copilot doesn’t have your website on file at all.** Microsoft keeps its own record of the web, and Copilot answers only from that record. Yours isn’t in it — we checked, and no pages are listed. That is why Copilot never named you in nine hand-checked answers, and it would stay true however good your website was. Your site openly invites Microsoft to read it; nobody has told Microsoft it exists. Registering is free and takes about fifteen minutes, though it is then days or weeks before anything changes.'),
      body('**3. Nothing tells a machine where you work.** Your pages say “the Wirral” in words a person reads. The information written for machines says only “United Kingdom” — no town, no area. So when someone asks for help on the Wirral there is nothing to match you against, and you were named 0 times out of 15 when we asked exactly that. This is the one item here that is a small, contained change to your website.'),

      h2('What we’d do about it'),
      body('Findings 2 and 3 are ordinary Foundation work and both are worth doing. Finding 1 isn’t, and it’s the bigger problem: no amount of website work stops an assistant thinking you’re a pharmaceutical company, and every improvement made under the current name accrues to a name four other businesses already answer to.'),
      body('So the honest order is the name first, then the rest. We’d rather say that now than take a fee for work that wouldn’t hold.'),

      h2('What this doesn’t tell you'),
      bullet('These answers are from 2 and 3 August 2026. They will be different next month — that is the nature of the systems, not a flaw in the checking.'),
      bullet('Five runs is enough to tell “never” from “sometimes” from “usually”. It is not enough to read a small change as a trend.'),
      bullet('We can’t see inside these systems, and nobody outside the companies that run them can. What we can see is what they say and what they draw on.'),
      bullet('**We haven’t checked your listings elsewhere** — directories, Companies House, review counts, or whether your details match across them. On most audits that is where the largest number of fixable problems turn up, and it is the obvious next thing to look at.'),
      bullet('Gemini declined to search the web on 14 of its 70 answers, and ChatGPT on 5 of its 70 — those came from memory rather than from looking, and we’ve counted them as they came.'),
      spacer(60),
      body('If you’d like the raw record — every question, every run, every answer in full — just ask and we’ll send it over.'),

      /* sign-off */
      new Paragraph({
        spacing: { before: 340, after: 140 },
        border: { top: { style: BorderStyle.SINGLE, size: 8, color: BRASS, space: 12 } },
        children: [],
      }),
      new Paragraph({
        spacing: { after: 60 },
        children: [new TextRun({ text: 'Kieran Smith  ·  Noven  ·  hello@novenstudio.co.uk', font: SANS, size: 19, color: INK, bold: true })],
      }),
      new Paragraph({
        children: [new TextRun({ text: 'Noven is one person. The person who wrote this report is the person who did the work.', font: SERIF, size: 19, color: INK_SOFT, italics: true })],
      }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync('Noven-audit-report-2026-08-03.docx', buf);
  console.log('wrote Noven-audit-report-2026-08-03.docx', buf.length, 'bytes');
});

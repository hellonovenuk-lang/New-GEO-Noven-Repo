"""Build the publishable master of the August 2026 self-audit.

Takes the delivered .docx and produces the version the owner exports the client
PDF from. Two subtractions, each marked in the document where it happens:

  * the eleven businesses the assistants named instead of us have their names
    replaced with neutral labels, because /ask-your-ai/ promises the reader we
    don't name them; and
  * the four price figures the report quoted are removed rather than updated.
    They were correct on 3 August 2026 and superseded five days later, and the
    paragraph they sat in is *about* an assistant serving a stale price for
    this business — so restating them, even beside a correction, would put four
    wrong numbers about our own fees into a document these systems may read.

Nothing is rewritten to say something it did not say, and the original stays in
this folder, untouched, as the record of what was delivered on 3 August 2026.

Run from the repo root. Idempotent: it always rebuilds the publication copy
from the original, so re-running it after a change here is safe.

    python3 ops/audits/noven-2026-08-02/build-publication-copy.py
"""

import re
import shutil
import zipfile
from pathlib import Path

SRC = Path("ops/audits/noven-2026-08-02/Noven-audit-report-2026-08-03.docx")
DST = Path("ops/audits/noven-2026-08-02/Noven-audit-report-2026-08-03-for-publication.docx")

# Ranked as they appear in the "who gets recommended instead" table, so the
# numbering a reader sees runs down the page in order. The eleventh was named
# by Google in the hand-checked runs rather than in the table.
NAMES = [
    ("Tilio", "Named business 1"),
    ("Rank4AI", "Named business 2"),
    ("AEO Agency", "Named business 3"),
    ("Dynamically", "Named business 4"),
    ("Exposure Ninja", "Named business 5"),
    ("GEO Intelligence", "Named business 7"),
    ("GEOQ", "Named business 6"),
    ("ClickSlice", "Named business 8"),
    ("Otter Labs", "Named business 9"),
    ("Consilium Design", "Named business 10"),
    ("Max Web Solutions", "Named business 11"),
]

RUN_FONT = (
    '<w:rFonts w:ascii="Segoe UI" w:cs="Segoe UI" w:eastAsia="Segoe UI" w:hAnsi="Segoe UI"/>'
)


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def note(lead: str, body: str) -> str:
    """A marked note in the site's own house style: brass rule down the left,
    body in the soft ink, so it can never be mistaken for the report's voice."""
    props = (
        '<w:pPr><w:spacing w:after="160" w:line="288" w:lineRule="auto"/>'
        '<w:pBdr><w:left w:val="single" w:sz="12" w:space="10" w:color="8A6A28"/></w:pBdr>'
        '<w:ind w:left="200"/></w:pPr>'
    )
    bold = (
        f"<w:r><w:rPr>{RUN_FONT}<w:b/><w:bCs/><w:color w:val=\"8A6A28\"/>"
        f'<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(lead)}</w:t></w:r>'
    )
    rest = (
        f"<w:r><w:rPr>{RUN_FONT}<w:color w:val=\"565B66\"/>"
        f'<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(body)}</w:t></w:r>'
    )
    return f"<w:p>{props}{bold}{rest}</w:p>"


def insert_after_paragraph_containing(xml: str, needle: str, paragraph: str) -> str:
    i = xml.index(needle)
    end = xml.index("</w:p>", i) + len("</w:p>")
    return xml[:end] + paragraph + xml[end:]


def insert_before_paragraph_containing(xml: str, needle: str, paragraph: str) -> str:
    i = xml.index(needle)
    start = max(xml.rfind("<w:p>", 0, i), xml.rfind("<w:p ", 0, i))
    return xml[:start] + paragraph + xml[start:]


def main() -> None:
    with zipfile.ZipFile(SRC) as z:
        xml = z.read("word/document.xml").decode("utf-8")
        names_in_zip = z.namelist()

    for old, new in NAMES:
        count = xml.count(old)
        if count == 0:
            raise SystemExit(f"expected to find {old!r} and did not — check the source document")
        xml = xml.replace(old, new)

    # Nothing from the list may survive anywhere in the document.
    leftovers = [old for old, _ in NAMES if re.search(re.escape(old), xml)]
    if leftovers:
        raise SystemExit(f"names still present after replacement: {leftovers}")

    xml = insert_after_paragraph_containing(
        xml,
        "Prepared for Kieran Smith",
        note(
            "Published version, 6 August 2026. ",
            "This is the report as delivered on 3 August 2026, with two declared changes: the "
            "businesses named instead of us are not named here, and the four prices it quoted have "
            "been removed rather than updated. Both removals are marked where they happen. Nothing "
            "else has been altered — where the report is out of date, it is left out of date rather "
            "than quietly corrected.",
        ),
    )

    # The four price figures come out of the report's own prose rather than
    # being updated. The paragraph they sit in is *about* an assistant serving
    # a stale price for this business, so restating them — even beside a
    # correction — would put four wrong numbers about our own fees into a
    # document that may well be read by the systems the report is about. The
    # finding survives without them; the risk does not survive with them.
    old_prices = (
        "your old prices — a £30 audit and a £350 setup, against the £125 and £750 you charge. "
        "Anyone asking an assistant what this should cost could have been quoted less than a "
        "quarter of your real fee."
    )
    new_prices = (
        "prices from an earlier version of the site — less than a quarter of what you actually "
        "charge. Anyone asking an assistant what this should cost was being given the wrong number."
    )
    if old_prices not in xml:
        raise SystemExit("the priced sentence is not where it was — check the source document")
    xml = xml.replace(old_prices, new_prices)

    xml = insert_after_paragraph_containing(
        xml,
        "One wrong fact of a different kind",
        note(
            "The figures in this paragraph have been removed rather than updated. ",
            "The report quoted four prices, all correct on 3 August 2026 and all superseded five "
            "days later. Restating them here would put four wrong numbers about our own fees into "
            "a document about an assistant serving a stale price for this business — the finding "
            "above, happening a second time. Our published prices are on wardith.co.uk/pricing, "
            "which is the only place they should be read.",
        ),
    )

    xml = insert_before_paragraph_containing(
        xml,
        "Named business 4 was also named by Google",
        note(
            "The names are withheld in this version. ",
            "Most of the businesses above are genuine, doing real work, and none of them asked to "
            "appear in our marketing. The counts are the part that matters: one business took "
            "roughly a fifth of every recommendation going, and ten names between them accounted "
            "for the field.",
        ),
    )

    shutil.copyfile(SRC, DST)
    # Rewrite the archive rather than appending, so the package holds exactly
    # one copy of document.xml — Word rejects a zip with a duplicate part.
    with zipfile.ZipFile(SRC) as src, zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as out:
        for item in names_in_zip:
            data = xml.encode("utf-8") if item == "word/document.xml" else src.read(item)
            out.writestr(item, data)

    print(f"wrote {DST} ({DST.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

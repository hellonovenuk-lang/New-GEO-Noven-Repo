#!/usr/bin/env python3
"""Validate and render one Wardith Content Engine review package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


NAVY = "#170969"
PAPER = "#fffefa"
INK = "#16161d"
INK_SOFT = "#565b66"
BRASS = "#8a6a28"
WIDTH = 1200
HEIGHT = 1200
PLACEHOLDER = re.compile(r"\[PLACEHOLDER\]|\bTODO\b|\bTBC\b", re.IGNORECASE)


class PackageError(ValueError):
    pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PackageError(message)


def validate(data: dict) -> None:
    required = {
        "schema_version", "slug", "source_type", "review_state", "evidence",
        "publication", "posts", "graphic",
    }
    require(set(data) == required, f"top-level fields must be exactly: {', '.join(sorted(required))}")
    require(data["schema_version"] == 1, "schema_version must be 1")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["slug"]) is not None, "slug must be kebab-case")
    require(data["source_type"] in {"campaign", "research"}, "source_type must be campaign or research")
    require(data["review_state"] == "READY_FOR_REVIEW", "review_state must be READY_FOR_REVIEW")

    serialised = json.dumps(data, ensure_ascii=False)
    require(PLACEHOLDER.search(serialised) is None, "package contains a placeholder, TODO or TBC")

    evidence = data["evidence"]
    require(isinstance(evidence, list) and evidence, "evidence must contain at least one item")
    evidence_ids: set[str] = set()
    for item in evidence:
        for field in ("id", "claim", "source_title", "publisher", "date", "locator"):
            require(isinstance(item.get(field), str) and item[field].strip(), f"evidence item is missing {field}")
        require(re.fullmatch(r"E\d{2,}", item["id"]) is not None, f"invalid evidence ID: {item['id']}")
        require(item["id"] not in evidence_ids, f"duplicate evidence ID: {item['id']}")
        evidence_ids.add(item["id"])
        require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", item["date"]) is not None, f"invalid evidence date: {item['date']}")
        if data["source_type"] == "research":
            require(str(item.get("url", "")).startswith("https://"), f"research evidence {item['id']} needs an https URL")
        else:
            require(bool(item.get("local_file")), f"campaign evidence {item['id']} needs local_file")

    publication = data["publication"]
    require(set(publication) == {"named_businesses", "recognition_basis"}, "publication fields are invalid")
    names = publication["named_businesses"]
    require(isinstance(names, list) and all(isinstance(name, str) and name.strip() for name in names), "named_businesses must be a list of names")
    require(len(names) == len(set(names)), "named_businesses contains duplicates")
    basis = publication["recognition_basis"]
    require(basis in {"none", "positive-recognition"}, "recognition_basis is invalid")
    if names:
        require(data["source_type"] == "campaign", "only campaign content may publish a recognition list")
        require(basis == "positive-recognition", "named businesses require positive-recognition basis")
    else:
        require(basis == "none", "recognition_basis must be none when no businesses are named")

    posts = data["posts"]
    require(set(posts) == {"personal", "company"}, "posts must contain personal and company")
    for channel, post in posts.items():
        require(set(post) == {"text", "evidence_ids"}, f"{channel} post fields are invalid")
        require(isinstance(post["text"], str) and post["text"].strip(), f"{channel} post is empty")
        validate_evidence_refs(post["evidence_ids"], evidence_ids, f"{channel} post")
    require(posts["personal"]["text"].strip() != posts["company"]["text"].strip(), "personal and company posts must not be duplicates")

    graphic = data["graphic"]
    required_graphic = {"template", "label", "headline", "detail", "source_line", "evidence_ids"}
    require(set(graphic) == required_graphic, "graphic fields are invalid")
    require(graphic["template"] in {"market-finding", "research-finding"}, "graphic template is invalid")
    expected_template = "market-finding" if data["source_type"] == "campaign" else "research-finding"
    require(graphic["template"] == expected_template, f"{data['source_type']} content must use {expected_template}")
    limits = {"label": 50, "headline": 105, "detail": 180, "source_line": 100}
    for field, limit in limits.items():
        value = graphic.get(field)
        require(isinstance(value, str) and value.strip(), f"graphic {field} is empty")
        require(len(value) <= limit, f"graphic {field} exceeds {limit} characters")
    validate_evidence_refs(graphic["evidence_ids"], evidence_ids, "graphic")


def validate_evidence_refs(refs: object, known: set[str], owner: str) -> None:
    require(isinstance(refs, list) and refs, f"{owner} needs at least one evidence ID")
    require(len(refs) == len(set(refs)), f"{owner} contains duplicate evidence IDs")
    missing = sorted(set(refs) - known)
    require(not missing, f"{owner} references unknown evidence IDs: {', '.join(missing)}")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    require(bool(words), "cannot wrap empty text")
    lines: list[str] = []
    line = words[0]
    for word in words[1:]:
        candidate = f"{line} {word}"
        if draw.textbbox((0, 0), candidate, font=face)[2] <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def draw_lines(draw: ImageDraw.ImageDraw, lines: list[str], xy: tuple[int, int], face: ImageFont.FreeTypeFont, fill: str, spacing: int) -> int:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        box = draw.textbbox((x, y), line, font=face)
        y += (box[3] - box[1]) + spacing
    return y


def render_graphic(graphic: dict, output: Path) -> None:
    root = repo_root()
    wordmark_path = root / "assets" / "logo.png"
    newsreader_path = root / "assets" / "og" / "fonts" / "Newsreader-500.woff2"
    sans_path = root / "assets" / "video" / "fonts" / "IBMPlexSans-400.woff2"
    mono_path = root / "assets" / "video" / "fonts" / "IBMPlexMono-500.woff2"
    for asset in (wordmark_path, newsreader_path, sans_path, mono_path):
        require(asset.is_file(), f"required committed brand asset is missing: {asset.relative_to(root)}")

    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    display = font(newsreader_path, 78)
    body = font(sans_path, 34)
    label_face = font(mono_path, 25)
    source_face = font(mono_path, 23)

    draw.rectangle((0, 0, 24, HEIGHT), fill=NAVY)
    draw.rectangle((80, 76, 1120, 82), fill=NAVY)
    draw.text((82, 126), graphic["label"], font=label_face, fill=NAVY)

    wordmark = Image.open(wordmark_path).convert("RGBA")
    logo_width = 250
    logo_height = round(wordmark.height * logo_width / wordmark.width)
    wordmark = wordmark.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    image.paste(wordmark, (WIDTH - 82 - logo_width, 116), wordmark)

    headline_lines = wrap(draw, graphic["headline"], display, 980)
    require(len(headline_lines) <= 4, "graphic headline needs more than four lines at mobile-safe size")
    y = draw_lines(draw, headline_lines, (82, 260), display, NAVY, 18)
    y += 44
    draw.rectangle((82, y, 188, y + 7), fill=BRASS)
    y += 58

    detail_lines = wrap(draw, graphic["detail"], body, 960)
    require(len(detail_lines) <= 4, "graphic detail needs more than four lines at mobile-safe size")
    detail_bottom = draw_lines(draw, detail_lines, (82, y), body, INK, 17)
    require(detail_bottom < 960, "graphic text would collide with the source area")

    draw.line((82, 1018, 1118, 1018), fill="#e2dfd6", width=3)
    source_lines = wrap(draw, graphic["source_line"], source_face, 1010)
    require(len(source_lines) <= 2, "graphic source line needs more than two lines")
    draw_lines(draw, source_lines, (82, 1055), source_face, INK_SOFT, 10)

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)


def source_ledger(data: dict) -> str:
    lines = ["# Source ledger", "", f"Content pack: `{data['slug']}`", ""]
    for item in data["evidence"]:
        lines.extend([f"## {item['id']}", "", item["claim"], ""])
        lines.append(f"Source: {item['source_title']} — {item['publisher']} ({item['date']})")
        if item.get("url"):
            lines.append(f"URL: {item['url']}")
        if item.get("local_file"):
            lines.append(f"Local file: {item['local_file']}")
        lines.extend([f"Locator: {item['locator']}", ""])
    return "\n".join(lines).rstrip() + "\n"


def build(input_path: Path, output_dir: Path) -> None:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "content package must be a JSON object")
    validate(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "personal-linkedin.md").write_text(data["posts"]["personal"]["text"].strip() + "\n", encoding="utf-8")
    (output_dir / "wardith-linkedin.md").write_text(data["posts"]["company"]["text"].strip() + "\n", encoding="utf-8")
    (output_dir / "source-ledger.md").write_text(source_ledger(data), encoding="utf-8")
    render_graphic(data["graphic"], output_dir / "linkedin-graphic.png")
    print(f"READY_FOR_REVIEW {output_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="content-package.json")
    parser.add_argument("--output-dir", type=Path, help="defaults to the input file's directory")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        require(isinstance(data, dict), "content package must be a JSON object")
        validate(data)
        if args.validate_only:
            print("VALID")
        else:
            build(args.input, args.output_dir or args.input.parent)
        return 0
    except (OSError, json.JSONDecodeError, PackageError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

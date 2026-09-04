import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image


MODULE_PATH = Path(__file__).with_name("build_pack.py")
SPEC = importlib.util.spec_from_file_location("build_pack", MODULE_PATH)
build_pack = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(build_pack)


def valid_package() -> dict:
    return {
        "schema_version": 1,
        "slug": "ai-search-research-finding",
        "source_type": "research",
        "review_state": "READY_FOR_REVIEW",
        "evidence": [{
            "id": "E01",
            "claim": "The published research found a measurable change in customer search behaviour.",
            "source_title": "A measured change in search behaviour",
            "publisher": "Example Research Institute",
            "date": "2026-09-01",
            "url": "https://example.org/research",
            "locator": "Results section, table 2"
        }],
        "publication": {"named_businesses": [], "recognition_basis": "none"},
        "posts": {
            "personal": {"text": "I have been looking at how customer search behaviour is changing. The research found a measurable shift.\n\nSource: https://example.org/research", "evidence_ids": ["E01"]},
            "company": {"text": "New research records a measurable change in customer search behaviour. This is the part local businesses need to watch.\n\nSource: https://example.org/research", "evidence_ids": ["E01"]}
        },
        "graphic": {
            "template": "research-finding",
            "label": "Research finding",
            "headline": "Customer search behaviour is changing in measurable ways.",
            "detail": "The source records the change. Wardith's interpretation belongs in the post, not inside the source claim.",
            "source_line": "Example Research Institute · 1 September 2026",
            "evidence_ids": ["E01"]
        }
    }


class ContentPackTests(unittest.TestCase):
    def test_valid_package_builds_complete_pack_and_square_graphic(self):
        package = valid_package()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "content-package.json"
            source.write_text(json.dumps(package), encoding="utf-8")
            build_pack.build(source, root)
            self.assertTrue((root / "personal-linkedin.md").is_file())
            self.assertTrue((root / "wardith-linkedin.md").is_file())
            self.assertIn("Results section, table 2", (root / "source-ledger.md").read_text())
            with Image.open(root / "linkedin-graphic.png") as graphic:
                self.assertEqual(graphic.size, (1200, 1200))
                self.assertEqual(graphic.getpixel((5, 600)), (23, 9, 105))
                self.assertEqual(graphic.getpixel((1199, 1199)), (255, 254, 250))

    def test_placeholder_blocks_package(self):
        package = valid_package()
        package["posts"]["personal"]["text"] = "[PLACEHOLDER]"
        with self.assertRaisesRegex(build_pack.PackageError, "placeholder"):
            build_pack.validate(package)

    def test_unknown_evidence_reference_blocks_package(self):
        package = valid_package()
        package["graphic"]["evidence_ids"] = ["E99"]
        with self.assertRaisesRegex(build_pack.PackageError, "unknown evidence"):
            build_pack.validate(package)

    def test_research_evidence_requires_live_url_shape(self):
        package = valid_package()
        package["evidence"][0].pop("url")
        with self.assertRaisesRegex(build_pack.PackageError, "https URL"):
            build_pack.validate(package)

    def test_named_businesses_require_campaign_recognition_basis(self):
        package = valid_package()
        package["publication"]["named_businesses"] = ["Example Ltd"]
        package["publication"]["recognition_basis"] = "positive-recognition"
        with self.assertRaisesRegex(build_pack.PackageError, "only campaign"):
            build_pack.validate(package)

    def test_duplicate_channel_copy_blocks_package(self):
        package = valid_package()
        package["posts"]["company"]["text"] = package["posts"]["personal"]["text"]
        with self.assertRaisesRegex(build_pack.PackageError, "must not be duplicates"):
            build_pack.validate(package)


if __name__ == "__main__":
    unittest.main()

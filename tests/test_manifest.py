import json
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


class ManifestTest(unittest.TestCase):
    def test_archive_identity_is_consistent(self) -> None:
        repository_url = "https://github.com/kody-w/rapp-store-archive"
        self.assertEqual(MANIFEST["store"]["url"], repository_url)
        self.assertEqual(
            MANIFEST["protocol"]["raw_base"],
            "https://raw.githubusercontent.com/kody-w/rapp-store-archive/main",
        )

        old_repository = "kody-w/" + "RAPP_Store"
        old_pages = "kody-w.github.io/" + "RAPP_Store"
        text_suffixes = {".html", ".js", ".json", ".md", ".py"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in text_suffixes:
                continue
            contents = path.read_text(encoding="utf-8")
            self.assertNotIn(old_repository, contents, str(path.relative_to(ROOT)))
            self.assertNotIn(old_pages, contents, str(path.relative_to(ROOT)))

    def test_manifest_counts_and_categories_match_items(self) -> None:
        agents = MANIFEST["agents"]
        skills = MANIFEST["skills"]
        ids = [item["id"] for item in agents + skills]
        categories = {category["id"] for category in MANIFEST["categories"]}

        self.assertEqual(MANIFEST["stats"]["total_agents"], len(agents))
        self.assertEqual(MANIFEST["stats"]["total_skills"], len(skills))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(
            all(item["category"] in categories for item in agents + skills)
        )

    def test_every_advertised_item_path_exists(self) -> None:
        for agent in MANIFEST["agents"]:
            self.assert_path_exists(f"{agent['path']}/{agent['filename']}")

        for skill in MANIFEST["skills"]:
            self.assert_path_exists(f"{skill['path']}/SKILL.md")
            for resource_type, resources in skill.get("resources", {}).items():
                for resource in resources:
                    self.assert_path_exists(
                        f"{skill['path']}/{resource_type}/{resource}"
                    )

    def assert_path_exists(self, relative_path: str) -> None:
        path = PurePosixPath(relative_path)
        self.assertFalse(path.is_absolute())
        self.assertNotIn("..", path.parts)
        self.assertTrue((ROOT / path).is_file(), relative_path)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InternshipHeadingsTest(unittest.TestCase):
    def test_people_heading_is_rendered_for_each_route(self):
        expected = {
            "internships.html": "Познакомьтесь с нашими стажёрами",
            "practices.html": "Познакомьтесь с нашими практикантами",
        }
        for filename, heading in expected.items():
            with self.subTest(filename=filename):
                html = (ROOT / filename).read_text(encoding="utf-8")
                self.assertTrue(f">{heading}</h2>" in html, f"Heading is wrong in {filename}")
                self.assertNotIn("{{INTERN_TITLE}}", html)


if __name__ == "__main__":
    unittest.main()

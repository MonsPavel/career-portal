from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
FONT_FILES = (
    "golos-400-cyr.woff2",
    "golos-400-lat.woff2",
    "golos-500-cyr.woff2",
    "golos-500-lat.woff2",
)


class FontPreloadTest(unittest.TestCase):
    def test_visible_fonts_are_preloaded_before_stylesheets_on_every_page(self):
        for page in ROOT.glob("*.html"):
            with self.subTest(page=page.name):
                html = page.read_text(encoding="utf-8")
                first_stylesheet = html.index('<link rel="stylesheet"')
                for font in FONT_FILES:
                    preload = (
                        f'<link rel="preload" href="assets/fonts/{font}" '
                        'as="font" type="font/woff2" crossorigin>'
                    )
                    self.assertTrue(preload in html, f"{font} is not preloaded in {page.name}")
                    self.assertLess(html.index(preload), first_stylesheet)


if __name__ == "__main__":
    unittest.main()

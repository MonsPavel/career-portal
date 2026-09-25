import html
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD_RE = re.compile(r'<article class="vac-card\b[^\"]*"[^>]*>(.*?)</article>', re.S)
TITLE_RE = re.compile(r'<h3 class="vac-card__title">\s*<a href="([^\"]+)">(.+?)</a>\s*</h3>', re.S)
DETAIL_TITLE_RE = re.compile(r'<h1 class="vacancy__title">(.+?)</h1>', re.S)
APPLY_RE = re.compile(r'<a class="btn btn--primary" href="([^\"]+)">откликнуться</a>')
ASIDE_RE = re.compile(r'<aside class="form-aside">(.*?)</aside>', re.S)


class VacancyNavigationTests(unittest.TestCase):
    def test_every_vacancy_card_opens_its_own_detail(self):
        found = 0
        card_pages = set()
        detail_hrefs = set()
        vacancies = json.loads((ROOT / 'data' / 'vacancies.json').read_text(encoding='utf-8'))
        by_title = {item['title']: item for item in vacancies['items']}
        for page in ROOT.glob('*.html'):
            content = page.read_text(encoding='utf-8')
            for card in CARD_RE.findall(content):
                found += 1
                card_pages.add(page.name)
                title = TITLE_RE.search(card)
                self.assertIsNotNone(title, f'{page.name}: vacancy title has no detail link')
                href, card_title = title.groups()
                detail_hrefs.add(href)
                detail = ROOT / href.split('?', 1)[0]
                self.assertTrue(detail.is_file(), f'{page.name}: missing {href}')
                detail_html = detail.read_text(encoding='utf-8')
                detail_title = DETAIL_TITLE_RE.search(detail_html)
                self.assertIsNotNone(detail_title, f'{href}: missing vacancy title')
                plain_title = html.unescape(re.sub(r'<[^>]+>', '', card_title)).strip()
                self.assertEqual(
                    plain_title,
                    html.unescape(re.sub(r'<[^>]+>', '', detail_title.group(1))).strip(),
                    f'{page.name}: {href} opens a different vacancy',
                )
                apply = APPLY_RE.search(card)
                self.assertIsNotNone(apply, f'{page.name}: missing apply link')
                apply_href = apply.group(1)
                apply_page = ROOT / apply_href
                self.assertTrue(apply_page.is_file(), f'{page.name}: missing {apply_href}')
                apply_html = apply_page.read_text(encoding='utf-8')
                self.assertIn(
                    f'href="{href}">вернуться к вакансии</a>',
                    apply_html,
                    f'{apply_href}: return link points to a different vacancy',
                )
                self.assertIn(plain_title,
                              html.unescape(apply_html),
                              f'{apply_href}: application names a different vacancy')
                aside = ASIDE_RE.search(apply_html)
                self.assertIsNotNone(aside, f'{apply_href}: missing vacancy summary')
                summary = html.unescape(re.sub(r'<[^>]+>', ' ', aside.group(1)))
                vacancy = by_title[plain_title]
                for field in ('company', 'city', 'salary', 'experience', 'direction'):
                    self.assertIn(vacancy[field], summary,
                                  f'{apply_href}: incorrect {field} in vacancy summary')
        self.assertGreater(found, 0, 'No vacancy cards checked')
        self.assertEqual(card_pages, {'vacancies.html', 'article.html', 'company.html'})
        self.assertEqual(len(detail_hrefs), len(vacancies['items']))


if __name__ == '__main__':
    unittest.main()

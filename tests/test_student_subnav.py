from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class StudentSubnavParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_subnav = False
        self.subnav_depth = 0
        self.has_subnav = False
        self.current_link = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "nav" and attributes.get("aria-label") == "Разделы школьникам и студентам":
            self.in_subnav = True
            self.subnav_depth = 1
            self.has_subnav = True
            return

        if not self.in_subnav:
            return

        self.subnav_depth += 1
        if tag == "a":
            self.current_link = {"attrs": attributes, "text": []}

    def handle_endtag(self, tag):
        if not self.in_subnav:
            return

        if tag == "a" and self.current_link:
            self.current_link["text"] = "".join(self.current_link["text"]).strip()
            self.links.append(self.current_link)
            self.current_link = None

        self.subnav_depth -= 1
        if self.subnav_depth == 0:
            self.in_subnav = False

    def handle_data(self, data):
        if self.in_subnav and self.current_link:
            self.current_link["text"].append(data)


class BreadcrumbParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_breadcrumbs = False
        self.depth = 0
        self.labels = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "nav" and attributes.get("aria-label") == "Хлебные крошки":
            self.in_breadcrumbs = True
            self.depth = 1
            return
        if self.in_breadcrumbs:
            self.depth += 1

    def handle_endtag(self, tag):
        if not self.in_breadcrumbs:
            return
        self.depth -= 1
        if self.depth == 0:
            self.in_breadcrumbs = False

    def handle_data(self, data):
        label = data.strip()
        if self.in_breadcrumbs and label and label != "/":
            self.labels.append(label)


class StudentSubnavTest(unittest.TestCase):
    ROUTES = {
        "practices.html": "Практики",
        "internships.html": "Стажировки",
        "education.html": "Целевое обучение",
        "career-track.html": "Карьерный трек",
        "events.html": "Мероприятия",
    }

    BREADCRUMBS = {
        "practices.html": "Практики",
        "internships.html": "Стажировки",
        "education.html": "Целевое обучение",
        "career-track.html": "Карьерные треки",
        "events.html": "Мероприятия",
    }

    def test_subnav_is_present_and_marks_the_current_route(self):
        for filename, expected_label in self.ROUTES.items():
            with self.subTest(filename=filename):
                parser = StudentSubnavParser()
                parser.feed((ROOT / filename).read_text(encoding="utf-8"))

                self.assertTrue(parser.has_subnav, f"{filename}: student subnav is missing")
                active_labels = [
                    link["text"]
                    for link in parser.links
                    if link["attrs"].get("aria-current") == "page"
                ]
                self.assertEqual(active_labels, [expected_label])

    def test_breadcrumbs_include_the_student_section(self):
        for filename, current_label in self.BREADCRUMBS.items():
            with self.subTest(filename=filename):
                parser = BreadcrumbParser()
                parser.feed((ROOT / filename).read_text(encoding="utf-8"))
                self.assertEqual(
                    parser.labels,
                    ["Главная", "Школьникам и студентам", current_label],
                )


if __name__ == "__main__":
    unittest.main()

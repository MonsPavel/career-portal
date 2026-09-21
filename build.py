# -*- coding: utf-8 -*-
"""Сборка мок-версии сайта: главные + внутренние страницы по ТЗ.
Запуск: python build.py"""
import json
import time
from pathlib import Path

ROOT = Path(__file__).parent
BLOCKS = ROOT / 'src' / 'blocks'
PAGESRC = ROOT / 'src' / 'pages'
DATA = ROOT / 'data'

STAMP = str(int(time.time()))

CSS_ORDER = ['css/variables.css', 'css/base.css', 'css/components.css'] + [
    f'src/blocks/{b}/{b}.css' for b in [
        'header', 'hero', 'production', 'directions', 'holding', 'employers',
        'why-us', 'vacancy-search', 'vacancy-capsule', 'students', 'video-block',
        'media', 'mentorship', 'team', 'cta-mail', 'footer', 'search-screen',
    ]
] + ['css/pages.css']

JS_ORDER = [
    f'src/blocks/{b}/{b}.js' for b in [
        'header', 'production', 'directions', 'search-screen',
    ]
] + ['js/forms.js', 'js/faq.js', 'js/tracks.js']

# ---------------------------------------------------------------- утилиты

def load(fragment: Path) -> str:
    html = fragment.read_text(encoding='utf-8')
    html = html.replace('../../assets/', 'assets/').replace('../assets/', 'assets/')
    return html


def json_data(name: str):
    return json.loads((DATA / f'{name}.json').read_text(encoding='utf-8'))

# ---------------------------------------------------------------- карточки

ARROW = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M2 8h11M9 3l5 5-5 5" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def render_vacancy_card(v: dict) -> str:
    pin = '<span class="tag tag--navy">закреплена</span>' if v.get('pinned') else ''
    acc = '<span class="tag tag--green">доступно людям с инвалидностью</span>' if v.get('accessible') else ''
    return f'''<article class="vac-card card card--hover">
  <div class="vac-card__head">
    <h3 class="vac-card__title">{v['title']}</h3>
    <time class="vac-card__date">{v['date']}</time>
  </div>
  <div class="vac-card__tags">{pin}<span class="tag tag--gray">{v['experience']}</span>{acc}</div>
  <p class="vac-card__short">{v['short']}</p>
  <div class="vac-card__meta">
    <a class="vac-card__company" href="company.html">{v['company']}</a>
    <span class="vac-card__city">{v['city']}</span>
  </div>
  <div class="vac-card__foot">
    <span class="vac-card__salary">{v['salary']}</span>
    <a class="btn btn--primary" href="vacancy-apply.html">откликнуться</a>
  </div>
</article>'''


def render_internship_card(i: dict, with_schedule: bool = False) -> str:
    paid = '<span class="tag tag--orange">Оплачиваемая</span>' if i.get('paid') else ''
    sched = f'<span class="tag tag--blue">{i["schedule"]}</span>' if with_schedule and i.get('schedule') else ''
    return f'''<article class="card card--hover card--filled intern-card">
  <img class="intern-card__photo" src="{i['image']}" alt="" loading="lazy">
  <div class="intern-card__body">
    <h3 class="intern-card__title">{i['title']}</h3>
    <p class="intern-card__short">{i['short']}</p>
    <div class="intern-card__tags">{paid}{sched}</div>
    <div class="intern-card__meta">
      <span class="intern-card__company">{i['company']}</span>
      <span class="intern-card__city">{i['city']}</span>
    </div>
    <a class="intern-card__more" href="internship.html">подробнее {ARROW}</a>
  </div>
</article>'''


def render_event_card(e: dict) -> str:
    if 'открыта' in e.get('reg', ''):
        reg = '<span class="tag tag--green">Регистрация</span>'
    elif 'Завершено' in e.get('reg', ''):
        reg = '<span class="tag tag--gray">Завершено</span>'
    else:
        reg = f'<span class="tag tag--orange">{e["reg"]}</span>'
    return f'''<article class="event-card card card--hover">
  <div class="event-card__photo-wrap">
    <img class="event-card__photo" src="{e['image']}" alt="" loading="lazy">
    {reg}
  </div>
  <div class="event-card__body">
    <time class="event-card__date">{e['date']}</time>
    <h3 class="event-card__title">{e['title']}</h3>
    <div class="event-card__meta">
      <span class="tag tag--blue">{e['city']}</span>
      <span class="tag tag--gray">{e['format']}</span>
    </div>
  </div>
</article>'''


def render_article_card(a: dict) -> str:
    dot = {'статья': 'media__tag-dot--article', 'видео': 'media__tag-dot--video',
           'подкаст': 'media__tag-dot--podcast'}.get(a['type'], 'media__tag-dot--article')
    return f'''<article class="article-card card card--hover">
  <a class="article-card__link" href="article.html">
    <div class="article-card__photo-wrap">
      <img class="article-card__photo" src="{a['image']}" alt="" loading="lazy">
      <span class="media__tag"><i class="media__tag-dot {dot}"></i>{a['type']}</span>
    </div>
    <h3 class="article-card__title">{a['title']}</h3>
    <time class="article-card__date">{a['date']}</time>
  </a>
</article>'''


def render_faq(faq_items: list) -> str:
    items = []
    for i, item in enumerate(faq_items):
        open_cls = ' is-open' if i == 0 else ''
        items.append(f'''<div class="faq__item{open_cls}">
  <button class="faq__q" type="button">{item['q']}
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 6l5 4 5-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>
  <div class="faq__a">{item['a']}</div>
</div>''')
    return '<div class="faq" data-faq>' + '\n'.join(items) + '</div>'


def render_breadcrumbs(items: list) -> str:
    parts = ['<div class="container"><nav class="breadcrumbs" aria-label="Хлебные крошки">']
    for i, (label, href) in enumerate(items):
        link = f'<a href="{href}">{label}</a>' if href else f'<span>{label}</span>'
        sep = '<span class="breadcrumbs__sep">/</span>' if i < len(items) - 1 else ''
        parts.append(link + sep)
    parts.append('</nav></div>')
    return ''.join(parts)

# ---------------------------------------------------------------- layout

def layout(title: str, crumbs: list, body: str, body_class: str) -> str:
    crumbs_html = render_breadcrumbs(crumbs) if crumbs else ''
    css_links = '\n'.join(f'  <link rel="stylesheet" href="{p}?v={STAMP}">' for p in CSS_ORDER)
    js_tags = '\n'.join(f'  <script src="{p}?v={STAMP}" defer></script>' for p in JS_ORDER)
    header = load(BLOCKS / 'header' / 'header.html')
    footer = load(BLOCKS / 'footer' / 'footer.html')
    search_screen = load(BLOCKS / 'search-screen' / 'search-screen.html')
    footer = footer + search_screen
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="data:,">
  <title>{title}</title>
  <meta name="description" content="Портал карьеры Группы «Интер РАО»">
{css_links}
{js_tags}
</head>
<body class="{body_class}">
{header}
<main class="main">
{crumbs_html}
{body}
</main>
{footer}
</body>
</html>
'''

# ---------------------------------------------------------------- данные

VAC = json_data('vacancies')
INT = json_data('internships')
EVT = json_data('events')
ART = json_data('articles')
EDU = json_data('educat')
TRK = json_data('tracks')
COMP = json_data('companies')

# ---------------------------------------------------------------- карточки-списки

def vacancy_cards() -> str:
    return '\n'.join(render_vacancy_card(v) for v in VAC['items'])


def events_upcoming() -> str:
    return '\n'.join(render_event_card(e) for e in EVT['upcoming'])


def events_past() -> str:
    return '\n'.join(render_event_card(e) for e in EVT['past'])


def article_cards() -> str:
    return '\n'.join(render_article_card(a) for a in ART['items'])


def internship_cards(with_schedule: bool) -> str:
    items = INT['internship']['items'] if with_schedule else INT['practice']['items']
    return '\n'.join(render_internship_card(i, with_schedule) for i in items)


def steps_html(steps: list) -> str:
    return '\n'.join(
        f'<div class="step"><div class="step__num">{i+1}</div><div class="step__body">'
        f'<div class="step__title">{s["title"]}</div><div class="step__text">{s["text"]}</div></div></div>'
        for i, s in enumerate(steps))


def interns_html(interns: list) -> str:
    return '\n'.join(
        f'''<article class="card card--hover intern-card">
  <div class="intern-card__body">
    <div class="intern__name">{p['name']}</div>
    <div class="intern__tags">{''.join(f'<span class="tag tag--blue">{t}</span>' for t in p['tags'])}</div>
    <p class="intern-card__short">{p['short']}</p>
  </div>
</article>''' for p in interns)


def offer_card(o: dict) -> str:
    return f'''<article class="offer-card card card--hover">
  <div class="offer-card__head">
    <h3 class="offer-card__direction">{o['direction']}</h3>
    <time class="offer-card__date">{o['date']}</time>
  </div>
  <p class="offer-card__short">{o['short']}</p>
  <div class="offer-card__tags"><span class="tag tag--blue">{o['orgTag']}</span><span class="tag tag--gray">{o['form']}</span></div>
  <div class="offer-card__meta"><span class="offer-card__company">{o['company']}</span><span class="offer-card__city">{o['city']}</span></div>
  <a class="btn btn--accent" href="#" onclick="return false">сайт «Работа России»</a>
</article>'''


def org_card(o: dict) -> str:
    return f'''<article class="card card--hover org-card">
  <h3 class="org-card__name">{o['name']}</h3>
  <p class="org-card__short">{o['short']}</p>
  <div class="org-card__meta"><span class="tag tag--blue">{o['type']}</span><span class="tag tag--gray">{o['city']}</span></div>
</article>'''


def adv_card(a: dict) -> str:
    return f'''<article class="card card--filled adv-card"><h3 class="adv-card__title">{a['title']}</h3><p class="adv-card__text">{a['text']}</p></article>'''

# ---------------------------------------------------------------- главные (существующие)

SLOTS = {
    # панель вакансий живёт внутри тёмной секции why-us (как в макете, вариант 1)
    '<!-- VACANCY_SLOT: панель «Найди свою вакансию» (вставляется при сборке для варианта 1) -->':
        'vacancy-search/vacancy-search.html',
}

INDEX_FRAGS = {
    'index-1.html': [
        'header/header.html',
        'hero/hero.html',
        'production/production.html',
        'directions/directions.html',
        'holding/holding.html',
        'employers/employers.html',
        'why-us/why-us.html',
        'students/students.html',
        'video-block/video-block.html',
        'media/media.html',
        'team/team.html',
        'cta-mail/cta-mail.html',
        'footer/footer.html',
        'search-screen/search-screen.html',
    ],
    'index-2.html': [
        'header/header.html',
        'hero/hero.html',
        'production/production.html',
        'directions/directions.html',
        'holding/holding.html',
        'employers/employers.html',
        'mentorship/mentorship.html',
        'vacancy-capsule/vacancy-capsule.html',
        'students/students.html',
        'video-block/video-block.html',
        'media/media.html',
        'team/team.html',
        'vacancy-capsule/vacancy-capsule.html',
        'cta-mail/cta-mail.html',
        'footer/footer.html',
        'search-screen/search-screen.html',
    ],
}


def apply_variant2(html: str) -> str:
    html = html.replace('class="hero hero--default"', 'class="hero hero--marquee"')
    html = html.replace('class="production production--v1"', 'class="production production--v2"')
    html = html.replace('class="media"', 'class="media media--wide"', 1)
    html = html.replace('class="employers"', 'class="employers employers--mosaic"')
    html = html.replace('class="students"', 'class="students students--photo"')
    html = html.replace('<div class="students__grid students__grid--illu">',
                        '<div class="students__grid students__grid--illu" hidden>')
    html = html.replace('<div class="students__grid students__grid--photo" hidden>',
                        '<div class="students__grid students__grid--photo">')
    html = html.replace('class="students__more" href="#students">подробнее',
                        'class="students__more" href="#students">все мероприятия')
    html = html.replace('class="media__more" href="#media">подробнее',
                        'class="media__more" href="#media">все медиа')
    html = html.replace('hero-city-1.png', 'hero-city-2.png')
    html = html.replace('<h1 class="hero__title">Зажигай свет и&nbsp;дари тепло вместе с&nbsp;нами</h1>',
                        '<h1 class="hero__title">Зажги свет вместе с&nbsp;нами</h1>')
    html = html.replace('placeholder="Введите название вакансии"', 'placeholder="Найти вакансию"')
    parts = html.split('Найди своё призвание')
    if len(parts) == 3:
        html = parts[0] + 'Найди своё призвание' + parts[1] + 'Найди свою команду' + parts[2]
    html = html.replace('Все 140 вакансий', 'Все 144 вакансии')
    html = html.replace('<span class="video-block__time">24:23</span>', '<span class="video-block__time">3:25</span>')
    return html


def write_page(fname: str, title: str, body: str, body_class: str) -> None:
    css_links = '\n'.join(f'  <link rel="stylesheet" href="{p}?v={STAMP}">' for p in CSS_ORDER)
    js_tags = '\n'.join(f'  <script src="{p}?v={STAMP}" defer></script>' for p in JS_ORDER)
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="data:,">
  <title>{title}</title>
  <meta name="description" content="Портал карьеры Группы «Интер РАО»">
{css_links}
{js_tags}
</head>
<body class="{body_class}">
{body}
</body>
</html>
'''
    (ROOT / fname).write_text(html, encoding='utf-8')
    print('built', fname, f'({len(html)//1024} KB)')


def company_segments() -> str:
    groups = {}
    for c in COMP['companies']:
        groups.setdefault(c['segment'], []).append(c['name'])
    out = []
    for seg, names in groups.items():
        cards = '\n'.join(
            f'<a class="card card--hover" style="padding:20px 24px; font-size: var(--fs-small-regular); '
            f'font-weight: var(--fw-small); color: var(--color-text);" href="company.html">{n}</a>'
            for n in names)
        out.append(f'<h2 class="section__title" style="font-size: var(--fs-h3); line-height: 1.3;">{seg}</h2>'
                   f'<div class="cards-grid cards-grid--3" style="margin-bottom: 48px;">{cards}</div>')
    return '\n'.join(out)

# ---------------------------------------------------------------- внутренние страницы

INNER_PAGES = [
    {
        'out': 'vacancies.html',
        'title': 'Вакансии — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Вакансии', None)],
        'frag': 'vacancies.html',
        'replaces': {'<!-- VACANCY_CARDS -->': vacancy_cards(), '{{TOTAL}}': str(VAC['total'])},
    },
    {
        'out': 'vacancy.html',
        'title': 'Ведущий инженер по эксплуатации энергоблоков — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Вакансии', 'vacancies.html'),
                   ('Ведущий инженер по эксплуатации энергоблоков', None)],
        'frag': 'vacancy.html',
    },
    {
        'out': 'vacancy-apply.html',
        'title': 'Отклик на вакансию — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Вакансии', 'vacancies.html'),
                   ('Ведущий инженер по эксплуатации энергоблоков', 'vacancy.html'), ('Отклик', None)],
        'frag': 'vacancy-apply.html',
    },
    {
        'out': 'internships.html',
        'title': 'Стажировки — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Школьникам и студентам', None), ('Стажировки', None)],
        'frag': 'internships.html',
        'replaces': {
            '{{PAGE_TITLE}}': 'Стажировки',
            '{{PAGE_TITLE|lower}}': 'стажировки',
            '{{PAGE_TITLE_ACC}}': 'стажировку',
            '{{PAGE_SUBTITLE}}': INT['internship']['subtitle'],
            '<!-- INTERNSHIP_CARDS -->': internship_cards(True),
            '<!-- INTERNSHIP_ADV_IMG -->': INT['internship']['advantages_companies']['image'],
            '<!-- INTERNSHIP_ADV_TEXT -->': INT['internship']['advantages_companies']['text'],
            '<!-- INTERNSHIP_STEPS -->': steps_html(INT['internship']['steps']),
            '<!-- INTERNSHIP_INTERNS -->': interns_html(INT['internship']['interns']),
            '<!-- INTERNSHIP_FAQ -->': render_faq(INT['faq']),
            '<!-- INTERNSHIP_EVENTS -->': '\n'.join(render_event_card(e) for e in EVT['upcoming'][:3]),
            '<!-- PAGE_MENU -->': 'internships',
        },
    },
    {
        'out': 'practices.html',
        'title': 'Практики — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Школьникам и студентам', None), ('Практики', None)],
        'frag': 'internships.html',
        'replaces': {
            '{{PAGE_TITLE}}': 'Практики',
            '{{PAGE_TITLE|lower}}': 'практики',
            '{{PAGE_TITLE_ACC}}': 'практику',
            '{{PAGE_SUBTITLE}}': INT['practice']['subtitle'],
            '<!-- INTERNSHIP_CARDS -->': internship_cards(False),
            '<!-- INTERNSHIP_ADV_IMG -->': INT['practice']['advantages_companies']['image'],
            '<!-- INTERNSHIP_ADV_TEXT -->': INT['practice']['advantages_companies']['text'],
            '<!-- INTERNSHIP_STEPS -->': steps_html(INT['practice']['steps']),
            '<!-- INTERNSHIP_INTERNS -->': interns_html(INT['practice']['interns']),
            '<!-- INTERNSHIP_FAQ -->': render_faq(INT['faq']),
            '<!-- INTERNSHIP_EVENTS -->': '\n'.join(render_event_card(e) for e in EVT['upcoming'][:3]),
            '<!-- PAGE_MENU -->': 'practices',
        },
    },
    {
        'out': 'internship.html',
        'title': 'Стажировка: разработчик — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Стажировки', 'internships.html'), ('Стажировка: разработчик', None)],
        'frag': 'internship.html',
        'replaces': {'{{APPLY_LINK}}': 'internship-apply.html'},
    },
    {
        'out': 'internship-apply.html',
        'title': 'Заявка на стажировку — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Стажировки', 'internships.html'), ('Заявка', None)],
        'frag': 'internship-apply.html',
    },
    {
        'out': 'education.html',
        'title': 'Целевое обучение — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Целевое обучение', None)],
        'frag': 'education.html',
        'replaces': {
            '<!-- EDUCAT_ORGS -->': '\n'.join(org_card(o) for o in EDU['orgs']),
            '<!-- EDUCAT_ADVANTAGES -->': '\n'.join(adv_card(a) for a in EDU['advantages']),
            '<!-- EDUCAT_OFFERS -->': '\n'.join(offer_card(o) for o in EDU['offers'][:3]),
            '<!-- EDUCAT_FAQ -->': render_faq(EDU['faq']),
        },
    },
    {
        'out': 'education-catalog.html',
        'title': 'Каталог предложений целевого обучения — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Целевое обучение', 'education.html'), ('Каталог предложений', None)],
        'frag': 'education-catalog.html',
        'replaces': {'<!-- EDUCAT_OFFERS -->': '\n'.join(offer_card(o) for o in EDU['offers'])},
    },
    {
        'out': 'events.html',
        'title': 'Мероприятия — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Мероприятия', None)],
        'frag': 'events.html',
        'replaces': {
            '<!-- EVENTS_UPCOMING -->': events_upcoming(),
            '<!-- EVENTS_PAST -->': events_past(),
        },
    },
    {
        'out': 'events-search.html',
        'title': 'Поиск мероприятий — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Мероприятия', 'events.html'), ('Поиск', None)],
        'frag': 'events-search.html',
        'replaces': {'<!-- EVENTS_UPCOMING -->': events_upcoming()},
    },
    {
        'out': 'event.html',
        'title': 'День открытых дверей — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Мероприятия', 'events.html'), ('День открытых дверей', None)],
        'frag': 'event.html',
        'replaces': {'{{APPLY_LINK}}': 'event-apply.html'},
    },
    {
        'out': 'event-apply.html',
        'title': 'Заявка на мероприятие — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Мероприятия', 'events.html'), ('Заявка', None)],
        'frag': 'event-apply.html',
    },
    {
        'out': 'media.html',
        'title': 'Медиа — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Медиа', None)],
        'frag': 'media.html',
        'replaces': {
            '<!-- ARTICLE_CARDS -->': article_cards(),
            '<!-- MEDIA_RUBRICS -->': '\n'.join(
                f'<a class="tag tag--blue filter-tag" href="media.html">{r}</a>' for r in ART['rubrics']),
        },
    },
    {
        'out': 'article.html',
        'title': 'Студенты приступили к практике — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Медиа', 'media.html'), ('Студенты приступили к практике', None)],
        'frag': 'article.html',
        'replaces': {
            '<!-- ARTICLE_RELATED_VACANCIES -->': '\n'.join(render_vacancy_card(v) for v in VAC['items'][:3]),
            '<!-- ARTICLE_RELATED_INTERNSHIPS -->': internship_cards(True),
        },
    },
    {
        'out': 'career-track.html',
        'title': 'Карьерные треки — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Карьерные треки', None)],
        'frag': 'career-track.html',
        'replaces': {
            '<!-- TRACK_BANNER -->': (
                f'''<div class="banner-card">
                <img class="banner-card__photo" src="{TRK['banners'][0]['image']}" alt="">
                <div class="banner-card__body"><h2 class="banner-card__title">{TRK['banners'][0]['title']}</h2>
                <p class="banner-card__text">{TRK['banners'][0]['text']}</p>
                <a class="btn btn--primary" href="#tracks">узнать подробнее</a></div></div>'''),
            '<!-- TRACK_TAB_BUTTONS -->': '\n'.join(
                f'<button class="btn btn--outline tab-btn{" is-active" if i == 0 else ""}" type="button" data-track-tab>{t["name"]}</button>'
                for i, t in enumerate(TRK['tabs'])),
            '<!-- TRACKS_DATA -->': json.dumps(TRK, ensure_ascii=False),
            '<!-- TRACK_ARTICLES -->': '\n'.join(render_article_card(a) for a in ART['items'][:4]),
        },
    },
    {
        'out': 'company.html',
        'title': 'АО «Интер РАО – Электрогенерация» — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Компании группы', None), ('АО «Интер РАО – Электрогенерация»', None)],
        'frag': 'company.html',
        'replaces': {
            '<!-- COMPANY_VACANCIES -->': '\n'.join(render_vacancy_card(v) for v in VAC['items'][:4]),
            '<!-- COMPANY_EVENTS -->': '\n'.join(render_event_card(e) for e in EVT['upcoming'][:3]),
            '<!-- COMPANY_ARTICLES -->': '\n'.join(render_article_card(a) for a in ART['items'][:3]),
            '<!-- COMPANY_INTERNSHIPS -->': internship_cards(True),
        },
    },
    {
        'out': 'companies.html',
        'title': 'Компании группы — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Компании группы', None)],
        'frag': 'companies.html',
        'replaces': {'<!-- COMPANY_SEGMENTS -->': company_segments()},
    },
    {
        'out': '404.html',
        'title': 'Страница не найдена — Портал карьеры Интер РАО',
        'crumbs': [],
        'frag': '404.html',
    },
]

# ---------------------------------------------------------------- сборка

for fname, frags in INDEX_FRAGS.items():
    body = '\n'.join(load(BLOCKS / f) for f in frags)
    for marker, slot_fragment in SLOTS.items():
        if marker in body:
            body = body.replace(marker, load(BLOCKS / slot_fragment))
    if fname == 'index-2.html':
        body = apply_variant2(body)
    # перелинковка главной на страницы-моки
    body = body.replace('<a class="hero__search-all" href="#vacancies">Все вакансии</a>',
                        '<a class="hero__search-all" href="vacancies.html">Все вакансии</a>')
    body = body.replace('href="#vacancies">Все 140 вакансий', 'href="vacancies.html">Все 140 вакансий')
    body = body.replace('action="/vacancies/"', 'action="vacancies.html"')
    body = body.replace('href="#students">подробнее', 'href="practices.html">подробнее')
    body = body.replace('href="#media">подробнее', 'href="media.html">подробнее')
    variant = 'вариант 1' if '1' in fname else 'вариант 2'
    write_page(fname, f'Портал карьеры Интер РАО — {variant}', body, f'page page--{"v1" if "1" in fname else "v2"}')

for page in INNER_PAGES:
    body = load(PAGESRC / f"{page['frag']}")
    for key, val in (page.get('replaces') or {}).items():
        body = body.replace(key, val)
    for old, new in page.get('replace_extra', []):
        body = body.replace(old, new)
    body = layout(page['title'], page['crumbs'], body, 'page page--inner')
    write_page(page['out'], page['title'], body, 'page page--inner')

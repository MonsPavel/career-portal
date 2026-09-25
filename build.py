# -*- coding: utf-8 -*-
"""Сборка мок-версии сайта: главные + внутренние страницы по ТЗ.
Запуск: python build.py"""
import json
import re
import time
from html import escape
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
] + ['js/forms.js', 'js/faq.js', 'js/tracks.js', 'js/dropdowns.js']

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
    detail_href = vacancy_href(v)
    apply_href = vacancy_href(v, apply_form=True)
    pin = '<span class="tag tag--navy">закреплена</span>' if v.get('pinned') else ''
    acc = '<span class="tag tag--green">доступно людям с инвалидностью</span>' if v.get('accessible') else ''
    return f'''<article class="vac-card card card--hover">
  <div class="vac-card__head">
    <h3 class="vac-card__title"><a href="{detail_href}">{escape(v['title'])}</a></h3>
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
    <a class="btn btn--primary" href="{apply_href}">откликнуться</a>
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
    <h3 class="event-card__title"><a href="event.html">{e['title']}</a></h3>
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
  <div class="faq__a"><div class="faq__a-inner">{item['a']}</div></div>
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

def layout_body(crumbs: list, body: str) -> str:
    """Тело внутренней страницы: header + крошки + контент + footer/поиск.
    Оболочку документа добавляет write_page()."""
    crumbs_html = render_breadcrumbs(crumbs) if crumbs else ''
    header = load(BLOCKS / 'header' / 'header.html')
    footer = load(BLOCKS / 'footer' / 'footer.html')
    search_screen = load(BLOCKS / 'search-screen' / 'search-screen.html')
    footer = footer + search_screen
    return f'''{header}
<main class="main">
{crumbs_html}
{body}
</main>
{footer}
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

def vacancy_href(v: dict, apply_form: bool = False) -> str:
    index = VAC['items'].index(v)
    suffix = '' if index == 0 else f'-{index + 1}'
    return f'vacancy{"-apply" if apply_form else ""}{suffix}.html'


def render_vacancy_detail(v: dict) -> str:
    """Деталка для карточек без отдельного редакционного описания."""
    title = escape(v['title'])
    company = escape(v['company'])
    return f'''<section class="section">
  <div class="container">
    <div class="vacancy">
      <div class="vacancy__main">
        <div class="vacancy__head">
          <h1 class="vacancy__title">{title}</h1>
          <span class="vacancy__salary">{escape(v['salary'])}</span>
          <div class="vacancy__tags">
            <span class="tag tag--gray">{escape(v['experience'])}</span>
            <span class="tag tag--blue">{escape(v['direction'])}</span>
            <span class="tag tag--gray">{escape(v['specialization'])}</span>
          </div>
          <a class="vacancy__company" href="company.html">{company}</a>
        </div>
        <div class="vacancy__section">
          <h2>Что предстоит</h2>
          <p>{escape(v['short'])}</p>
        </div>
        <div class="vacancy__section">
          <h2>О вакансии</h2>
          <ul>
            <li>Компания: {company}</li>
            <li>Направление: {escape(v['direction'])}</li>
            <li>Специализация: {escape(v['specialization'])}</li>
            <li>Опыт: {escape(v['experience'])}</li>
          </ul>
        </div>
      </div>
      <aside class="vacancy__aside">
        <div class="vacancy__aside-title">Место работы</div>
        <div class="vacancy__address">
          <span>{escape(v['city'])}</span>
          <span>{escape(v['region'])}</span>
        </div>
        <a class="btn btn--accent" href="{vacancy_href(v, apply_form=True)}">откликнуться</a>
        <p style="font-size: var(--fs-micro); color: var(--color-text-muted); margin: 0;">
          Нажимая «откликнуться», вы заполните анкету и согласитесь на обработку персональных данных.
        </p>
      </aside>
    </div>
  </div>
</section>'''


def render_vacancy_apply(v: dict) -> str:
    body = load(PAGESRC / 'vacancy-apply.html')
    body = body.replace('vacancy-apply.html', vacancy_href(v, apply_form=True))
    body = body.replace('Ведущий инженер по эксплуатации энергоблоков', escape(v['title']))
    body = body.replace('АО «Интер РАО – Электрогенерация»', escape(v['company']))
    aside = f'''      <aside class="form-aside">
        <div class="form-aside__title">{escape(v['title'])}</div>
        <p class="form-aside__text">{escape(v['company'])}, {escape(v['city'])}. Зарплата {escape(v['salary'])}.</p>
        <div class="form-aside__row">
          <span class="form-aside__label">Опыт работы</span>
          <span class="form-aside__value">{escape(v['experience'])}</span>
        </div>
        <div class="form-aside__row">
          <span class="form-aside__label">Направление</span>
          <span class="form-aside__value">{escape(v['direction'])}</span>
        </div>
        <a class="btn btn--outline" href="{vacancy_href(v)}">вернуться к вакансии</a>
      </aside>'''
    body = re.sub(r'      <aside class="form-aside">.*?</aside>', aside, body,
                  count=1, flags=re.S)
    return body


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
  <a class="btn btn--accent" href="https://trudvsem.ru/" target="_blank" rel="noopener">сайт «Работа России»</a>
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
    html = html.replace('class="holding"', 'class="holding holding--compact"', 1)
    html = html.replace('class="media"', 'class="media media--wide"', 1)
    html = html.replace('class="employers"', 'class="employers employers--mosaic"')
    html = html.replace('<section class="students students--illustrated" id="students">',
                        '<section class="students students--illustrated" hidden>')
    html = html.replace('<section class="students students--photographic">',
                        '<section class="students students--photographic students--v2" id="students">')
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
    font_preloads = '\n'.join(
        f'  <link rel="preload" href="assets/fonts/golos-{weight}-{script}.woff2" '
        'as="font" type="font/woff2" crossorigin>'
        for weight in (400, 500)
        for script in ('cyr', 'lat')
    )
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
{font_preloads}
{css_links}
{js_tags}
</head>
<body class="{body_class}">
{body}
</body>
</html>
'''
    # версионирование картинок: браузер не отдаёт устаревший кэш после пересборки
    img_re = '(assets/(?:images|icons|logos)/[^"?]+?\\.(?:png|jpe?g|svg|woff2))'
    html = re.sub(img_re, lambda m: m.group(1) + "?v=" + STAMP, html)
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
            f'font-weight: var(--fw-small); color: var(--color-text);" href="company.html" target="_blank" rel="noopener">{n}</a>'
            for n in names)
        out.append(f'<h2 class="section__title" style="font-size: var(--fs-h3); line-height: 1.3;">{seg}</h2>'
                   f'<div class="cards-grid cards-grid--3" style="margin-bottom: 48px;">{cards}</div>')
    return '\n'.join(out)


STUDENT_SUBNAV_ITEMS = [
    ('Практики', 'practices.html'),
    ('Стажировки', 'internships.html'),
    ('Целевое обучение', 'education.html'),
    ('Карьерный трек', 'career-track.html'),
    ('Мероприятия', 'events.html'),
]


def student_subnav(active_label: str) -> str:
    links = []
    for label, href in STUDENT_SUBNAV_ITEMS:
        is_active = label == active_label
        active_class = ' is-active' if is_active else ''
        current = ' aria-current="page"' if is_active else ''
        links.append(
            f'<a class="intern-menu__item{active_class}" href="{href}"{current}>{label}</a>'
        )
    return (
        '<nav class="intern-menu" aria-label="Разделы школьникам и студентам">\n'
        + '\n'.join(links)
        + '\n</nav>'
    )

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
        'student_subnav': 'Стажировки',
        'replaces': {
            '{{PAGE_TITLE}}': 'Стажировки',
            '{{PAGE_TITLE|lower}}': 'стажировки',
            '{{PAGE_TITLE_ACC}}': 'стажировку',
            '{{PAGE_SUBTITLE}}': INT['internship']['subtitle'],
            '<!-- INTERNSHIP_CARDS -->': internship_cards(True),
            '<!-- INTERNSHIP_ADV_IMG -->': INT['internship']['advantages_companies']['image'],
            '<!-- INTERNSHIP_ADV_TEXT -->': INT['internship']['advantages_companies']['text'],
            '<!-- INTERNSHIP_ADVANTAGES -->': '\n'.join(adv_card(a) for a in INT['internship']['advantages']),
            '{{INTERN_TITLE}}': 'стажёрами',
            '<!-- INTERNSHIP_STEPS -->': steps_html(INT['internship']['steps']),
            '<!-- INTERNSHIP_INTERNS -->': interns_html(INT['internship']['interns']),
            '<!-- INTERNSHIP_FAQ -->': render_faq(INT['faq']),
            '<!-- INTERNSHIP_EVENTS -->': '\n'.join(render_event_card(e) for e in EVT['upcoming'][:3]),
        },
    },
    {
        'out': 'practices.html',
        'title': 'Практики — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Школьникам и студентам', None), ('Практики', None)],
        'frag': 'internships.html',
        'student_subnav': 'Практики',
        'replaces': {
            '{{PAGE_TITLE}}': 'Практики',
            '{{PAGE_TITLE|lower}}': 'практики',
            '{{PAGE_TITLE_ACC}}': 'практику',
            '{{PAGE_SUBTITLE}}': INT['practice']['subtitle'],
            '<!-- INTERNSHIP_CARDS -->': internship_cards(False),
            '<!-- INTERNSHIP_ADV_IMG -->': INT['practice']['advantages_companies']['image'],
            '<!-- INTERNSHIP_ADV_TEXT -->': INT['practice']['advantages_companies']['text'],
            '<!-- INTERNSHIP_ADVANTAGES -->': '\n'.join(adv_card(a) for a in INT['practice']['advantages']),
            '{{INTERN_TITLE}}': 'практикантами',
            '<!-- INTERNSHIP_STEPS -->': steps_html(INT['practice']['steps']),
            '<!-- INTERNSHIP_INTERNS -->': interns_html(INT['practice']['interns']),
            '<!-- INTERNSHIP_FAQ -->': render_faq(INT['faq']),
            '<!-- INTERNSHIP_EVENTS -->': '\n'.join(render_event_card(e) for e in EVT['upcoming'][:3]),
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
        'crumbs': [('Главная', 'index-1.html'), ('Школьникам и студентам', None),
                   ('Целевое обучение', None)],
        'frag': 'education.html',
        'student_subnav': 'Целевое обучение',
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
        'crumbs': [('Главная', 'index-1.html'), ('Школьникам и студентам', None),
                   ('Мероприятия', None)],
        'frag': 'events.html',
        'student_subnav': 'Мероприятия',
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
            '<!-- ARTICLE_RELATED_PRACTICES -->': internship_cards(False),
            '<!-- ARTICLE_RELATED_INTERNSHIPS -->': internship_cards(True),
            '<!-- ARTICLE_RELATED_EDUCAT -->': '\n'.join(offer_card(o) for o in EDU['offers'][:3]),
        },
    },
    {
        'out': 'career-track.html',
        'title': 'Карьерные треки — Портал карьеры Интер РАО',
        'crumbs': [('Главная', 'index-1.html'), ('Школьникам и студентам', None),
                   ('Карьерные треки', None)],
        'frag': 'career-track.html',
        'student_subnav': 'Карьерный трек',
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
            '<!-- COMPANY_VACANCIES -->': '\n'.join(
                render_vacancy_card(v) for v in (
                    [x for x in VAC['items'] if x['company'] == 'АО «Интер РАО – Электрогенерация»'] +
                    [x for x in VAC['items'] if x['company'] != 'АО «Интер РАО – Электрогенерация»' and x['segment'] == 'Генерация'])[:4]),
            '<!-- COMPANY_EVENTS -->': '\n'.join(render_event_card(e) for e in EVT['upcoming'][:3]),
            '<!-- COMPANY_ARTICLES -->': '\n'.join(render_article_card(a) for a in ART['items'][:3]),
            '<!-- COMPANY_INTERNSHIPS -->': internship_cards(True),
            '<!-- COMPANY_PRACTICES -->': internship_cards(False),
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

for vacancy in VAC['items'][1:]:
    detail_href = vacancy_href(vacancy)
    apply_href = vacancy_href(vacancy, apply_form=True)
    title = escape(vacancy['title'])
    INNER_PAGES.extend([
        {
            'out': detail_href,
            'title': f'{title} — Портал карьеры Интер РАО',
            'crumbs': [('Главная', 'index-1.html'), ('Вакансии', 'vacancies.html'),
                       (title, None)],
            'body': render_vacancy_detail(vacancy),
        },
        {
            'out': apply_href,
            'title': f'Отклик на вакансию «{title}» — Портал карьеры Интер РАО',
            'crumbs': [('Главная', 'index-1.html'), ('Вакансии', 'vacancies.html'),
                       (title, detail_href), ('Отклик', None)],
            'body': render_vacancy_apply(vacancy),
        },
    ])

# ---------------------------------------------------------------- сборка

for fname, frags in INDEX_FRAGS.items():
    body = '\n'.join(load(BLOCKS / f) for f in frags)
    for marker, slot_fragment in SLOTS.items():
        if marker in body:
            body = body.replace(marker, load(BLOCKS / slot_fragment))
    # перелинковка главной на страницы-моки (до применения варианта 2)
    body = body.replace('href="/vacancies/"', 'href="vacancies.html"')
    body = body.replace('action="/vacancies/"', 'action="vacancies.html"')
    body = body.replace('href="#vacancies"', 'href="vacancies.html"')
    body = body.replace('href="#media"', 'href="article.html"')
    is_v2 = fname == 'index-2.html'
    if is_v2:
        body = apply_variant2(body)
    body = body.replace('class="students__more" href="#students">подробнее',
                        'class="students__more" href="practices.html">' + ('все мероприятия' if is_v2 else 'подробнее'))
    body = body.replace('class="media__more" href="#media">подробнее',
                        'class="media__more" href="media.html">' + ('все медиа' if is_v2 else 'подробнее'))
    variant = 'вариант 1' if '1' in fname else 'вариант 2'
    write_page(fname, f'Портал карьеры Интер РАО — {variant}', body, f'page page--{"v1" if "1" in fname else "v2"}')

for page in INNER_PAGES:
    body = page.get('body') or load(PAGESRC / f"{page['frag']}")
    if '<!-- STUDENT_SUBNAV -->' in body:
        body = body.replace('<!-- STUDENT_SUBNAV -->', student_subnav(page['student_subnav']))
    for key, val in (page.get('replaces') or {}).items():
        body = body.replace(key, val)
    for old, new in page.get('replace_extra', []):
        body = body.replace(old, new)
    body = layout_body(page['crumbs'], body)
    write_page(page['out'], page['title'], body, 'page page--inner')

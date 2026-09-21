# -*- coding: utf-8 -*-
"""Сборка демо-страниц index-1.html и index-2.html из фрагментов блоков.
Запуск: python build.py"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
BLOCKS = ROOT / 'src' / 'blocks'

CSS_ORDER = ['css/variables.css', 'css/base.css'] + [
    f'src/blocks/{b}/{b}.css' for b in [
        'header', 'hero', 'production', 'directions', 'holding', 'employers',
        'why-us', 'vacancy-search', 'vacancy-capsule', 'students', 'video-block',
        'media', 'mentorship', 'team', 'cta-mail', 'footer', 'search-screen',
    ]
]

JS_ORDER = [
    f'src/blocks/{b}/{b}.js' for b in [
        'header', 'production', 'directions', 'search-screen',
    ]
]

SLOTS = {
    # панель вакансий живёт внутри тёмной секции why-us (как в макете, вариант 1)
    '<!-- VACANCY_SLOT: панель «Найди свою вакансию» (вставляется при сборке для варианта 1) -->':
        'vacancy-search/vacancy-search.html',
}

PAGES = {
    'index-1.html': {
        'fragments': [
            # Вариант 1 — Концепт «Главная 1»
            'header/header.html',
            'hero/hero.html',               # hero--default
            'production/production.html',   # production--v1
            'directions/directions.html',
            'holding/holding.html',
            'employers/employers.html',
            'why-us/why-us.html',           # включает панель вакансий через VACANCY_SLOT
            'students/students.html',       # вариант с иллюстрациями
            'video-block/video-block.html',
            'media/media.html',
            'team/team.html',
            'cta-mail/cta-mail.html',
            'footer/footer.html',
            'search-screen/search-screen.html',
        ],
        'slots': SLOTS,
    },
    'index-2.html': {
        'fragments': [
            # Вариант 2 — Концепт «Главная 2»
            'header/header.html',
            'hero/hero.html',               # hero--marquee
            'production/production.html',   # production--v2
            'directions/directions.html',
            'holding/holding.html',
            'employers/employers.html',
            'mentorship/mentorship.html',
            'vacancy-capsule/vacancy-capsule.html',   # «Найди своё призвание»
            'students/students.html',
            'video-block/video-block.html',
            'media/media.html',             # media--wide
            'team/team.html',
            'vacancy-capsule/vacancy-capsule.html',   # «Найди свою команду»
            'cta-mail/cta-mail.html',
            'footer/footer.html',
            'search-screen/search-screen.html',
        ],
        'slots': {},
    },
}

def load(fragment: str) -> str:
    html = (BLOCKS / fragment).read_text(encoding='utf-8')
    # из корня демо-страницы ассеты лежат на уровень выше блоков
    html = html.replace('../../assets/', 'assets/')
    return html

def load_page(fragments: list[str], inline_slots: dict[str, str] | None = None) -> str:
    """Собирает фрагменты; inline_slots заменяет маркер <!-- SLOT_NAME --> на HTML другого фрагмента."""
    inline_slots = inline_slots or {}
    out = []
    for f in fragments:
        html = load(f)
        for marker, slot_fragment in inline_slots.items():
            if marker in html:
                html = html.replace(marker, load(slot_fragment))
        out.append(html)
    return '\n'.join(out)

def page_html(title: str, fragments: list[str], page_id: str) -> str:
    body = '\n'.join(load(f) for f in fragments)
    stamp = str(int(__import__('time').time()))
    css_links = '\n'.join(f'  <link rel="stylesheet" href="{p}?v={stamp}">' for p in CSS_ORDER)
    js_tags = '\n'.join(f'  <script src="{p}?v={stamp}" defer></script>' for p in JS_ORDER)
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="data:,">
  <title>{title}</title>
  <meta name="description" content="Портал карьеры Группы «Интер РАО» — вёрстка по макету CP_Ревью">
{css_links}
{js_tags}
</head>
<body class="page page--{page_id}">
{body}
</body>
</html>
'''

# Пост-обработка вариантов: модификаторы блоков для страницы 2
def apply_variant2(html: str) -> str:
    html = html.replace('class="hero hero--default"', 'class="hero hero--marquee"')
    html = html.replace('class="production production--v1"', 'class="production production--v2"')
    html = html.replace('class="media"', 'class="media media--wide"', 1)
    html = html.replace('class="employers"', 'class="employers employers--mosaic"')
    # студенты: показываем фото-вариант вместо иллюстраций
    html = html.replace('class="students"', 'class="students students--photo"')
    html = html.replace('<div class="students__grid students__grid--illu">',
                        '<div class="students__grid students__grid--illu" hidden>')
    html = html.replace('<div class="students__grid students__grid--photo" hidden>',
                        '<div class="students__grid students__grid--photo">')
    # у студентов кнопка «Все мероприятия» вместо «подробнее»
    html = html.replace('class="students__more" href="#students">подробнее',
                        'class="students__more" href="#students">все мероприятия')
    # v2 медиа: кнопка «Все медиа»
    html = html.replace('class="media__more" href="#media">подробнее',
                        'class="media__more" href="#media">все медиа')
    # hero варианта 2: другое фото города (сырое, без тонировки; в макете развёрнуто на 180°)
    html = html.replace('hero-city-1.png', 'hero-city-2.png')
    html = html.replace('<h1 class="hero__title">Зажигай свет и&nbsp;дари тепло вместе с&nbsp;нами</h1>',
                        '<h1 class="hero__title">Зажги свет вместе с&nbsp;нами</h1>')
    html = html.replace('placeholder="Введите название вакансии"', 'placeholder="Найти вакансию"')
    # заголовок второй капсулы
    parts = html.split('Найди своё призвание')
    if len(parts) == 3:
        html = parts[0] + 'Найди своё призвание' + parts[1] + 'Найди свою команду' + parts[2]
    # счётчик вакансий у v2 — 144, таймкод видео 3:25
    html = html.replace('Все 140 вакансий', 'Все 144 вакансии')
    html = html.replace('<span class="video-block__time">24:23</span>', '<span class="video-block__time">3:25</span>')
    return html

for fname, page in PAGES.items():
    frags = page['fragments']
    title = 'Портал карьеры Интер РАО — вариант 1' if '1' in fname else 'Портал карьеры Интер РАО — вариант 2'
    body = load_page(frags, page['slots'])
    if fname == 'index-2.html':
        body = apply_variant2(body)
    stamp = str(int(__import__('time').time()))
    css_links = '\n'.join(f'  <link rel="stylesheet" href="{p}?v={stamp}">' for p in CSS_ORDER)
    js_tags = '\n'.join(f'  <script src="{p}?v={stamp}" defer></script>' for p in JS_ORDER)
    page_id = 'v1' if '1' in fname else 'v2'
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="data:,">
  <title>{title}</title>
  <meta name="description" content="Портал карьеры Группы «Интер РАО» — вёрстка по макету CP_Ревью">
{css_links}
{js_tags}
</head>
<body class="page page--{page_id}">
{body}
</body>
</html>
'''
    (ROOT / fname).write_text(html, encoding='utf-8')
    print('built', fname, f'({len(html)//1024} KB)')

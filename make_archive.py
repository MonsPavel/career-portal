# Инструмент сборки архива для деплоя: python make_archive.py
# Перед запуском — python build.py (свежая сборка страниц).
#
# ВАЖНО: собранные html подключают стили/скрипты блоков напрямую из src/blocks/,
# поэтому в архив идут также src/blocks/*/*.css и src/blocks/*/*.js.
# docs/ (PDF карта сайта, путь клиента) кладётся в архив справочно.
import zipfile, glob, os, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'career-portal-site_' + datetime.date.today().isoformat() + '.zip')

NOTE = """Интер РАО — портал карьеры (статический мок-сайт)
Дата сборки: {date}

СОСТАВ
  *.html          — все страницы (index.html — точка входа, 404.html — страница ошибки)
  css/, js/       — общие стили и скрипты
  src/blocks/     — стили и скрипты отдельных блоков (на них ссылаются html,
                    папку нужно выкладывать вместе с остальными)
  assets/         — шрифты (woff2), изображения, иконки, логотипы
  docs/           — PDF: карта сайта и путь клиента (справочно, на сервер не обязательны)

УСТАНОВКА
  1. Распаковать содержимое архива в корень сайта ЦЕЛИКОМ (файлы лежат в корне архива),
     чтобы папки css/, js/, src/, assets/ оказались рядом с *.html.
     Нельзя открывать index.html прямо внутри zip — браузер извлечёт только его
     одного, и страница будет без стилей.
  2. Если на сервере уже лежала старая версия — залить содержимое поверх,
     убедиться, что папки src/ и js/ обновились.
  3. Никаких серверных требований нет: чистая статика, PHP/БД не нужны.
  4. Настроить отдачу 404.html как страницу ошибки (если сервер позволяет).
  5. Кэширование: версии css/js уже проставлены через ?v=... в HTML,
     статике можно смело ставить долгий кэш (файлы меняются только с новой сборкой).

ПРИНЦИП ПОКАЗА МОДАЛЬНЫХ ОКОН
  Все окна (анкета отклика, заявки на практику/стажировку, поиск) открываются
  ТОЛЬКО по действию пользователя. При загрузке страницы никакие попапы —
  включая формы регистрации/авторизации — не показываются. При интеграции
  принцип сохранить: окно регистрации допустимо только как реакция на действие
  (например, «Откликнуться» для неавторизованного).

ВЕРСИЯ ДЛЯ СЛАБОВИДЯЩИХ (ГОСТ Р 52872)
  Включается кнопкой-глазом в шапке, состояние хранится в localStorage.
""".format(date=datetime.date.today().isoformat())

def add(zf, path, arcname):
    zf.write(path, arcname)

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    zf.writestr('README-DEPLOY.txt', NOTE)
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        add(zf, f, os.path.basename(f))
    for d in ('css', 'js', 'assets', 'docs'):
        base = os.path.join(ROOT, d)
        for dirpath, dirnames, filenames in os.walk(base):
            for name in sorted(filenames):
                full = os.path.join(dirpath, name)
                add(zf, full, os.path.relpath(full, ROOT).replace(os.sep, '/'))
    blocks = os.path.join(ROOT, 'src', 'blocks')
    for dirpath, dirnames, filenames in os.walk(blocks):
        for name in sorted(filenames):
            if name.endswith(('.css', '.js')):
                full = os.path.join(dirpath, name)
                add(zf, full, os.path.relpath(full, ROOT).replace(os.sep, '/'))

size = os.path.getsize(OUT)
print(OUT, round(size / 1024 / 1024, 2), 'MB')
with zipfile.ZipFile(OUT) as zf:
    names = zf.namelist()
    print('files:', len(names),
          '| html:', sum(1 for n in names if n.endswith('.html')),
          '| blocks css/js:', sum(1 for n in names if n.startswith('src/blocks/')),
          '| js:', sum(1 for n in names if n.startswith('js/')),
          '| docs:', sum(1 for n in names if n.startswith('docs/')))

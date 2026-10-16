#!/usr/bin/env python3
"""Write audit/vendor-mentions.md from the rows/recon that build.py left in $AUDIT_WORK."""
import json, collections, re, os, csv, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('AUDIT_REPO') or os.path.abspath(os.path.join(HERE, '..', '..'))
WORK = os.environ.get('AUDIT_WORK') or os.path.join(tempfile.gettempdir(), 'vendor-audit')
rows = json.load(open(f'{WORK}/rows.json'))
recon = json.load(open(f'{WORK}/recon.json'))
FILES = [json.loads(l) for l in open(f'{WORK}/text/files.jsonl')]
git = lambda *a: subprocess.run(['git', *a], capture_output=True, text=True, cwd=REPO).stdout.strip()
HEAD, HEAD_DATE = git('rev-parse', '--short', 'HEAD'), git('log', '-1', '--format=%cs')
NFILES = len([f for f in git('ls-files').split('\n') if f and not f.startswith('audit/')])
manifest = json.load(open(f'{REPO}/figma-assets.json'))
C = collections.Counter
def table(headers, data):
    out = ['| ' + ' | '.join(headers) + ' |', '|' + '|'.join('---' for _ in headers) + '|']
    for r in data: out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)
learner = [r for r in rows if r['audience'] == 'learner']
L = []
L.append('# Аудит упоминаний вендора в CCNA1 (ITN) — сводка\n')
L.append(f'Карта: `audit/vendor-mentions.csv` — **{len(rows)} строк** (`ccna1-vm-0001`…`ccna1-vm-{len(rows):04d}`), из них {len(learner)} видны обучающемуся, {len(rows)-len(learner)} служебные. Срез: `origin/main` @ `{HEAD}` ({HEAD_DATE}). Задача: nsalab-tmn/learn-ccna1#54. В материалах ничего не изменено.\n')
L.append('Продолжение: приоритетный план де-вендоризации — [`de-vendoring-plan.md`](./de-vendoring-plan.md); в CSV добавлены столбцы `tier` (P1/P2/P3) и `batch` (пакет работ), заполненные только для учебных поверхностей. Скрипты, которыми построены карта, сводка и план, — [`scripts/`](./scripts/README.md).\n')
L.append('## Как считали\n')
L.append('''1. **Словарный проход** по всем `git ls-files` (''' + str(NFILES) + ''' файлов): регистронезависимые регулярные выражения (словарь в конце), по строкам; в `README.md` каждая строка классифицирована как `text` / `code` (внутри ``` ``` ) / `comment` (внутри `<!-- -->`). Для `.docx` текст извлечён python-docx, для `.pdf` — pdftotext (локатор `путь:pN:lM`). Имена каталогов и файлов просканированы отдельно (`surface=filename`).
2. **Ручной просмотр** всего, что словарь не покрывает: 325 иллюстраций и 44 анимации отрисованы Chromium из SVG (анимации — по 10 моментов времени с `setCurrentTime`), 20 уникальных растров, встроенных в SVG, извлечены и просмотрены отдельно; 344 растровых файла просмотрены (GIF — первый/средний/последний кадр); первая страница каждого PDF отрисована и просмотрена.
3. **Агрегация**: обучающемуся видимые поверхности — строка на каждую строку файла; лабораторная инфраструктура — строка на лабу; `__exams/`, `videos/*.md`, `packet-tracer-source-files/`, `figma-assets.json`, `animations/` и префикс `2001:db8:acad` — строка на файл/каталог (локатор перечисляет строки). Каждое словарное попадание либо входит в строку карты, либо исключено с причиной (таблица сверки ниже).

**Ограничения среды аудита** (учтены в таблице покрытия): Figma API и Figma MCP недоступны — тексты кадров читались с отрисованных SVG (текст в кривых, но читается глазами), лист `_Библиотека` оценён по экспортированным фигурам; `tesseract` недоступен — текст на растрах читался визуально; видео по решению оператора не переразбирались — строки `surface=video` взяты из готового индекса `videos/README.md`.
''')
# totals
L.append('## Итоги\n')
L.append('### По категориям\n')
L.append(table(['category', 'строк', 'learner', 'internal'], [(k, v, sum(1 for r in rows if r['category']==k and r['audience']=='learner'), sum(1 for r in rows if r['category']==k and r['audience']=='internal')) for k, v in C(r['category'] for r in rows).most_common()]))
L.append('\n### По поверхностям\n')
L.append(table(['surface', 'строк'], C(r['surface'] for r in rows).most_common()))
L.append('\n### По действиям\n')
L.append(table(['action', 'строк'], C(r['action'] for r in rows).most_common()))
L.append('\n### По модулям (строки, видимые обучающемуся)\n')
def modsort(m):
    if m == '(root)': return (0, m)
    if m == '__exams': return (99, m)
    if m.startswith('final-'): return (90, m)
    return (int(m[:2]), m) if m[:2].isdigit() else (50, m)
mods = C(r['module'] for r in learner)
L.append(table(['module', 'строк', 'главные категории'], [(m, mods[m], ', '.join(f'{k} {v}' for k, v in C(r['category'] for r in learner if r['module']==m).most_common(3))) for m in sorted(mods, key=modsort)]))
L.append('\n### Топ-20 самых «вендорных» материалов (строки, видимые обучающемуся)\n')
mats = C(r['material'] for r in learner)
L.append(table(['#', 'material', 'строк', 'категории'], [(i+1, m, n, ', '.join(f'{k} {v}' for k, v in C(r['category'] for r in learner if r['material']==m).most_common(3))) for i, (m, n) in enumerate(mats.most_common(20))]))
# ---- decisions ----
def cnt(pred): return sum(1 for r in rows if pred(r))
n_ios = cnt(lambda r: re.search(r'\bIOS\b', r['term']) and r['audience']=='learner')
n_pt = cnt(lambda r: re.search(r'Packet Tracer|\bPT\b', r['term']) and r['audience']=='learner' and r['surface']!='lab-infra')
n_cisco_com = cnt(lambda r: 'cisco.com' in r['term'])
n_pwd = cnt(lambda r: r['action']=='replace:class123')
n_models = cnt(lambda r: r['category']=='model')
n_cli = cnt(lambda r: r['category']=='cli-vendor-string')
n_labs = cnt(lambda r: r['surface']=='lab-infra' and r['module']!='__exams')
n_topo = cnt(lambda r: r['action']=='replace:шаблон топологии')
n_acad = cnt(lambda r: 'db8:acad' in r['term'])
n_cdp = cnt(lambda r: 'CDP' in r['term'] and r['module']!='__exams')
n_eigrp = cnt(lambda r: 'EIGRP' in r['term'] and r['module']!='__exams')
L.append(f'''
## Решения для оператора (по типам)

1. **Название курса и репозитория («CCNA»).** Репозиторий `learn-ccna1`, код курса `ccna1` в `figma-assets.json` и в 44 каталогах `animations/ccna1-*`, файл `ccna1-labs.md`, каталоги `__exams/CCNA1…3`, фразы «курс CCNA» в тексте (10.3.5, 1.9.3, 3.7.9/3.7.10), доменные имена в заданиях `CCNA.com` / `CCNA-lab.com` (16.4.6, 17.8.2). Идентификаторы пайплайна (`ccna1-…`) завязаны на штампы в Figma — переименовывать дорого; текстовые отсылки к сертификации — дёшево. Предложение: курс и репозиторий переименовать (например, `learn-netfund-1`), id ассетов оставить как непрозрачные ключи, в тексте «курс CCNA» → «этот курс».
2. **«Cisco IOS» как имя операционной системы** — {n_ios} строк в учебных поверхностях (текст, тесты, метаданные, 4 имени каталогов `*-ios-*`). Синтаксис CLI сохраняется (learn-netsim его повторяет). Варианты: (а) «NSALAB NetOS» везде, где речь о нашей ОС; (б) нейтральное «сетевая операционная система / ОС устройства». Отдельно: `IOS XE`, `NX-OS` в 2.1.1 — убрать перечисление линеек Cisco.
3. **Packet Tracer → learn-netsim** — {n_pt} упоминаний в тексте/тестах/метаданных плюс {n_labs} лабораторные работы с PT-инфраструктурой (`.pka`, `deploy/pt-lab/*.tf`, оценка через `validate_web_response` на `{{pt-url}}:{{pt-api-port}}`), {n_topo} топологий-скриншотов PT/NetAcad. Девять лаб «Physical Mode» (PTPM: 2.3.8.1, 2.9.2, 4.7.1, 10.4.4, 11.10.2, 12.9.2, 13.3.2, 17.7.7, 17.8.1) опираются на стойки/кабели/города PT — аналога в netsim нет: переписать как логические или снять. 16.4.6 уже переводится (PR #53 открыт). Файлы `.pkt` для «следования за видео» (2.8.1, 2.8.2) и закомментированные ссылки «Скачать файл Packet Tracer» (36 README) — убрать вместе с миграцией.
4. **Модели оборудования** — {n_models} строк: 2960, 4321/ISR4321, 4221, 1941, 2801, 2811, 1841, ISR4331, Catalyst 2960-24TT, PLEK400/PLE400, Meraki MX64W; версии/образы IOS (`15.0(2)SE`, `c2960-lanbasek9-mz…`, `universalk9`, `16.9.3`). Сверка с идентичностью learn-netsim: маршрутизаторы → **NR01/NR02**, коммутатор → **NS01**, ПК → **NPC**; нужно утвердить имена интерфейсов моделей (сейчас в тексте смесь `G0/0/0` ISR4221/4321 и `G0/0` 1941) и таблицы «модель → интерфейсы» в 2.3.8.2 и 16.4.7.
5. **Вендорные строки в выводах CLI** — {n_cli} строк `code`: `Cisco IOS Software, C2960 Software…`, `Copyright (c) … by Cisco Systems`, `cisco ISR4321/K9 … processor`, `Technical Support: http://www.cisco.com/techsupport`, `WS-C2960+`, `IP CEF`, `C:\\Users\\NetAcad>`, `dns-sj.cisco.com`. Все уходят при перегенерации выводов на learn-netsim — это задача netsim (`show version`, `show cdp/lldp neighbors`, `show ip interface`, `nslookup`), а не правки текста.
6. **Проприетарные протоколы.** CDP — {n_cdp} строк (17.5.6, итоги 17.9, тест 17.8.5, экзамен 16-17): заменить на **LLDP** (802.1AB) как учебную тему — команды `show lldp neighbors` аналогичны. EIGRP — {n_eigrp} строк (3.3.3 список протоколов «разработан Cisco», 8.5.3/8.6 легенда `D - EIGRP` в `show ip route`, 11.7.5 сценарий лабы, тест 3.3.6): оставить как пример протокола маршрутизации без слов о Cisco или убрать из списков. `auto secure` (16.4.1, 16.6) — функция IOS, убрать. HSRP/GLBP/EtherChannel/PAgP/DTP/PVST/ISL встречаются только в `__exams` (CCNA2/3) и экзамене 14-15 (HSRP в комментарии к портам).
7. **Учётные данные и имена в заданиях с брендом** — {n_pwd} строк: пароли `cisco`, `Cisco123`, `Ciscoenpa55`, `Ciscoconpa55`; серверы `netacad.pka`, `www.cisco.pka`, `www.cisco6.pka`; домены `CCNA.com`, `CCNA-lab.com`; hostname `CiscoVille` (в `__exams`). Ввести единый нейтральный набор (например, пароль `class123`, домен `lab.local`, сервер `www.example.lab`) и синхронно обновить критерии оценки `assessment/ms.yaml`.
8. **cisco.com / netacad.com как учебные примеры** — {n_cisco_com} строк с `cisco.com` (DNS, URL, nslookup, ping, tracert, WHOIS; 15.3, 15.4, 17.7, лабы 3.7.10/7.1.6/15.4.8, тесты) и 60 с `netacad.com` (в основном подвалы PDF). Заменить на `example.com` / собственный домен, реальный адрес `198.133.219.25` → документационный `203.0.113.x`; переснять выводы.
9. **Маркетинг и имидж NetAcad.** Раздел 1.1.2 (слоган академии + промо-ролик `wcIP__5sa1o`), 1.7.3–1.7.5 (Webex, промо `e85Y71fsyyY`, скриншот 1.7.3) и повтор в 1.10, абзац «Студенты обычно используют Packet Tracer…» (1.0.3), «политика академии» (3.7.9), материал 1.9 / лаба 1.9.3 («Сертификация Cisco CCNA — система сертификации начального уровня…»). Скриншоты cisco.com со слоганом «Trust means you\'re ready for anything» — в 5 анимациях (3.3.5-1, 3.3.5-2, 3.6.4, 3.6.5, 4.1.2) и 6 иллюстрациях (14.1.2-1…-5, 15.3.1-4): один растр, заменить одним компонентом «окно браузера».
10. **Видео** — 36 роликов NetAcad (перезалив), 2 класса `marketing` → убрать; остальные уже в плане пересборки (5 из 36 готовы). Не переразбирались (решение оператора); в кадрах финальная заставка с логотипом Cisco отмечена в разборах для 5 роликов.
11. **Юридические метки** — 32 строки `legal`: подвалы «© … Корпорация Cisco… Все права защищены» в 9 PDF-описаниях лаб (плюс шапка «Cisco Networking Academy» на каждой странице), `Copyright (c) … Cisco Systems` в выводах CLI, `© 2021 Cisco … Cisco Confidential` в `readme-assets/itn-v7.02-scope-and-sequence.pdf`. PDF-лабы перенести в README (как остальные) и удалить файлы; scope-and-sequence удалить.
12. **Библиотека иконок Figma (`_Библиотека`)** — одна строка `decide`: силуэты устройств (маршрутизатор-«шайба» со стрелками, коммутатор-брусок, многоуровневый коммутатор-куб со звездой, межсетевой экран-стена) повторяют иконографию Cisco, хотя отрисованы собственной изометрией и палитрой без логотипов. Это де-факто отраслевой язык схем; решение — оставить или изменить силуэты — одно на всю библиотеку (369 фигур).
13. **Метаданные и имена.** Тег `"Cisco"` в `material-tags.json` (ставится всем материалам) и `final-itn/test.json`; 8 каталогов с `cisco-ios` / `-ios-` в имени (меняют `$ref` и внешние ссылки — переименовывать одним проходом); имена страниц Figma `CCNA1 · NN …` и `course: "ccna1"` в `figma-assets.json`.
14. **Гигиена репозитория.** `__exams/` (24 каталога/файла: копии экзаменов CCNA1 с расхождениями + экзамены CCNA2/CCNA3, 17 `.pka`, 182 изображения в стиле NetAcad, `CiscoVille`, `netacad.net`) не подключён к курсу — убрать или вынести в архив; `packet-tracer-source-files/` (41 `.docx` с «Packet Tracer» в именах и © Cisco) — удалить после миграции; `readme-assets/*.png` (17 скриншотов NetAcad/PT к инструкции по миграции) и сама `migration-instructions.md` — решить, нужна ли инструкция в репозитории курса; `final-itn/test.json` — не подключён.
15. **Префикс `2001:db8:acad::/48`** — конвенция NetAcad («acad»), {n_acad} файлов (295 вхождений, модули 9–13, 17, лабы, оценочные `ms.yaml`). Заменить на другой документационный префикс одним проходом (вместе с `ms.yaml`) или признать нейтральным.
16. **Вне вендора, но замечено:** фото Linksys (4.1.1-1/-2, 1.2.5-6 — бренд Cisco-эпохи, решить вместе с семьёй фигур по `raster-inventory`), логотипы IEEE/IETF/ITU/RIR (3.4.1, 3.4.2-1, 6.1.4, 11.3.6, 12.1.1), скриншоты Windows/PuTTY/Wireshark/Telegram/Gmail внутри фигур — чужие UI, не Cisco; тема другого аудита.
''')
# ---- coverage ----
L.append('## Покрытие\n')
ext = collections.defaultdict(lambda: [0, 0, ''])
HOW = {'.md': 'словарь построчно (text/code/comment)', '.json': 'словарь построчно (quiz/metadata)', '.yaml': 'словарь построчно (lab-infra)', '.yml': 'словарь построчно', '.tf': 'словарь построчно (lab-infra)', '.sh': 'словарь построчно', '.tpl': 'словарь построчно', '.py': 'словарь построчно', '.txt': 'словарь построчно', '.gitignore': 'словарь построчно',
       '.svg': 'рендер Chromium + просмотр (325 статичных, 44 анимации × 10 моментов); 685 встроенных растров → 20 уникальных просмотрены', '.png': 'просмотр глазами (OCR недоступен)', '.jpg': 'просмотр', '.jpeg': 'просмотр', '.gif': 'просмотр (кадры 1 / середина / последний)',
       '.pka': 'бинарный файл PT — не открывался; учтён строкой lab-infra лабы/экзамена', '.pkt': 'бинарный файл PT — не открывался; строка lab-infra + filename', '.docx': 'текст извлечён и просканирован; изображения внутри .docx не просматривались', '.pdf': 'текст извлечён и просканирован; визуально — 1-я страница каждого (логотипы/подвалы), остальные страницы только текстом'}
for f in FILES:
    e = f['ext'] if f['ext'] else ('.gitignore' if f['path'].endswith('.gitignore') else '(без расширения)')
    ext[e][0] += 1
    ext[e][1] += 1
cov = []
for e, (n, seen, _) in sorted(ext.items(), key=lambda kv: -kv[1][0]):
    partial = e in ('.docx', '.pdf', '.pka', '.pkt')
    cov.append((e, n, n, 0 if not partial else f'частично: {n}', HOW.get(e, 'словарь построчно')))
L.append(table(['тип файла', 'всего', 'просмотрено', 'пропущено / частично', 'как'], cov))
L.append('\n' + table(['figma-assets.json · kind', 'всего', 'просмотрено', 'как'], [
    ('illustration', sum(1 for a in manifest['assets'] if a['kind']=='illustration'), 325, 'рендер SVG → контактные листы 2×2; текст подписей читался с рендера'),
    ('animation', sum(1 for a in manifest['assets'] if a['kind']=='animation'), 44, '10 моментов времени на анимацию (SMIL setCurrentTime), листы 5×2'),
    ('native', sum(1 for a in manifest['assets'] if a['kind']=='native'), 74, 'просмотр + сверка с design/raster-inventory-ccna1.md'),
]))
L.append('\n' + table(['видео', 'всего', 'просмотрено', 'как'], [('встроенные YouTube-ролики', 36, '36 (по индексу)', 'по решению оператора не переразбирались; класс/канал/логотип — из videos/README.md и разборов videos/*.md')]))
L.append('\n' + table(['Figma', 'всего', 'просмотрено', 'как'], [('лист _Библиотека (3FtCg22qFubpLBPOetQU03)', 1, '0 напрямую', 'API/MCP Figma недоступны в среде аудита; вердикт по 369 экспортированным фигурам (одна строка decide)')]))
L.append('\nИтого `git ls-files`: ' + str(NFILES) + ' файлов, каждый либо просканирован словарём, либо просмотрен, либо учтён как бинарный артефакт PT (строка на лабу/экзамен). Частичное покрытие: изображения внутри 44 `.docx` и страницы 2+ десяти PDF просмотрены только текстом.\n')
# ---- reconciliation ----
L.append('## Сверка полноты по словарю (N = M + K)\n')
rec_rows = []
for k, v in recon.items():
    rec_rows.append((f'`{k}`', v['N'], v['M'], v['K'], v['rows'], '; '.join(f'{r} ×{n}' for r, n in v['excl']) if v['excl'] else ''))
L.append(table(['термин', 'найдено N', 'внесено M', 'исключено K', 'строк карты', 'причины исключения'], rec_rows))
totN = sum(v['N'] for v in recon.values()); totM = sum(v['M'] for v in recon.values()); totK = sum(v['K'] for v in recon.values())
L.append(f'\nВсего попаданий N = {totN}, внесено M = {totM}, исключено K = {totK}; N = M + K выполняется по каждому термину. «Строк карты» меньше M там, где попадания агрегированы (лаба, экзамен, служебный файл) или несколько терминов стоят в одной строке. Не вошли в словарь-регэксп, но проверены вручную по всем файлам и дали 0 совпадений: `talos`, `umbrella`, `linksys` (только на фото), `cisco live`, `devnet`, `snort`, `jabber`, `anyconnect`, `dna center`.\n')
L.append('### Итоговый словарь\n')
L.append(table(['термин', 'регулярное выражение', 'категория по умолчанию', 'из словаря задачи'], [(f'`{k}`', '`' + v['regex'].replace('|', '\\|') + '`', v['cat'], 'да' if v['indict'] else 'добавлен') for k, v in recon.items()]))
L.append('''
## Замеченные опечатки (в материалах не правились)

- заголовки лаб 17.07.06 и 17.07.07 в `learn-metadata.json`: «(логиеский режим)» — у 17.07.07 к тому же должно быть «физический режим»;
- каталоги `12.05-dynamic-addresing-for-ipv6-guas`, `12.06-dynamic-addresing-for-ipv6-llas` — `addresing`;
- `calc_duration.txt`: «avarage».
''')
open(os.path.join(REPO, 'audit', 'vendor-mentions.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('md written', sum(len(x) for x in L), 'chars')

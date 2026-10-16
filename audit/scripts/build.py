#!/usr/bin/env python3
"""Assemble audit/vendor-mentions.csv and audit/vendor-mentions.md from the scan hits + manual visual review."""
import json, re, csv, os, sys, collections, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('AUDIT_REPO') or os.path.abspath(os.path.join(HERE, '..', '..'))
WORK = os.environ.get('AUDIT_WORK') or os.path.join(tempfile.gettempdir(), 'vendor-audit')
OUT = os.path.join(REPO, 'audit'); os.makedirs(OUT, exist_ok=True)
H = [json.loads(l) for l in open(f'{WORK}/text/hits.jsonl')]
FILES = [json.loads(l) for l in open(f'{WORK}/text/files.jsonl')]
manifest = json.load(open(f'{REPO}/figma-assets.json'))
ASSET_BY_PATH = {a['out']['path']: a for a in manifest['assets']}
ASSET_BY_KEY = {a['display']['key']: a for a in manifest['assets']}
videos = {}
for l in open(os.path.join(HERE, 'videos.tsv')):
    vid, title, cls, figma = l.rstrip('\n').split('\t')
    videos[vid] = dict(title=title, cls=cls, figma=figma)
VIDEO_LOGO = {'K_VEPe8aRUE': 'логотип Cisco в финальном кадре (3:53)', 'YDXgJUjGjcw': 'логотип Cisco в финальном кадре (6:02)',
              'Ud1angOlxHE': 'логотип Cisco в финальном кадре (1:42)', 'DNL4DPxjgNM': 'логотип Cisco в финальном кадре (4:27); фото задних панелей Cisco 4321/2951/1941',
              'R_Ti9y2AShc': 'логотип Cisco в финальном кадре (2:28)', '7E9ilk9dOOI': 'в кадре netacad.com, id.cisco.com с логотипом Cisco, окно входа PT с логотипом Networking Academy',
              'uync1j2x6Ms': 'в кадре GUI Packet Tracer 8.0 (ISR 4331, Catalyst 2960 в стойке)', 'RH_KIUdHZlE': 'слайды «4000/2900/1900 series», консоли ISR 4321/2951/1941',
              'dFKfyJkuSqQ': 'вывод show version ISR 4321 с Cisco IOS XE, Copyright Cisco Systems', 'pt_Qw1Jfo5w': 'GUI Packet Tracer (IPv4 Routing Table.pkt)'}
MODULE_OF = lambda p: (p.split('/')[0] if re.match(r'^\d\d-', p.split('/')[0]) or p.split('/')[0].startswith('final-') or p.split('/')[0] == '__exams' else '(root)')
def material_of(p):
    parts = p.split('/'); top = parts[0]
    if re.match(r'^\d\d-', top) and len(parts) > 2: return '/'.join(parts[:2])
    if top == '__exams': return '/'.join(parts[:3]) if len(parts) > 3 else '/'.join(parts[:2])
    if top.startswith('final-') or re.match(r'^\d\d-', top): return top
    return parts[0] if len(parts) == 1 else '/'.join(parts[:1])

# ---------- exclusions (K) ----------
def exclude_reason(h):
    k, m, ctx = h['key'], h['matched'], h['context']
    if k == 'сиско/циско' and re.search(r'Франциско', ctx, re.I): return 'ложное совпадение: «Сан-Франциско»'
    if k == 'IOS' and m == 'iOS': return 'Apple iOS (мобильная ОС), не Cisco IOS'
    if k == 'model-number' and m == '1812': return 'число 1812 — порт RADIUS, не модель маршрутизатора'
    if k == 'model-number' and m == '2951' and '::' in ctx: return 'фрагмент IPv6-адреса, не модель'
    if k == 'сертификаци' and m.lower().startswith('сертифицир'): return '«сертифицированный» (продукция TIA / Wi-Fi Alliance) — не сертификация вендора'
    if k == 'youtube' and 'watch?v=1.2.3.mp4' in ctx: return 'пример синтаксиса встраивания в инструкции по миграции, не ролик'
    return None
for h in H:
    h['excl'] = exclude_reason(h)
KEEP = [h for h in H if not h['excl']]

# ---------- category / action rules ----------
CAT_PRI = ['marketing', 'legal', 'link', 'lab-infra', 'model', 'product', 'proprietary-tech', 'certification', 'brand']
CLI_KEYS = {'cisco', 'copyright', '©', 'cisco.com', 'WS-C', 'ios-image', 'ios-version', 'model-number', 'IOS', 'IOS XE', 'catalyst', 'ISR', 'netacad', 'CEF', 'CDP', 'EIGRP'}
def pick_category(hs, surface):
    keys = {h['key'] for h in hs}; cats = {h['cat'] for h in hs}
    if surface == 'code' and keys & CLI_KEYS: return 'cli-vendor-string'
    if surface == 'code' and cats <= {'proprietary-tech'}: return 'proprietary-tech'
    for c in CAT_PRI:
        if c in cats: return c
    return sorted(cats)[0]

def action_for(cat, keys, surface, ctx, module):
    low = ctx.lower()
    if surface == 'video': return None
    if cat == 'legal': return ('remove', 'копирайт/знак вендора; для PDF — пересобрать документ без колонтитулов NetAcad или перенести текст в README')
    if cat == 'cli-vendor-string': return ('neutralize', 'перегенерировать вывод CLI на learn-netsim (NSALAB NetOS, модели NR01/NR02/NS01/NPC); строки Cisco/Copyright/образы .bin исчезнут вместе с ним')
    if cat == 'link':
        if 'youtube' in keys: return ('decide', 'см. строки surface=video')
        if 'netacad' in keys or 'netacad.com' in keys: return ('remove', 'ссылка на ресурс NetAcad')
        if 'cisco.com' in keys: return ('replace:example.com', 'cisco.com как учебный пример домена/сайта → example.com или собственный домен лаборатории; вывод nslookup/ping переснять')
        return ('remove', '')
    if cat == 'lab-infra':
        if '.pka' in keys and surface == 'comment': return ('remove', 'закомментированная ссылка на .pka; удалить вместе с миграцией лабы на learn-netsim')
        if '.pkt' in keys: return ('remove', 'файл .pkt для «следования» за видео; заменить сценарием learn-netsim')
        if 'PTSA/PTPM' in keys: return ('neutralize', '«режим симуляции физического оборудования (PTPM)» — PT-специфичный режим; решить судьбу physical-mode лаб')
        if '.pka' in keys and ('netacad' in keys or 'cisco' in keys): return ('replace:www.example.lab', 'имя сервера в топологии содержит бренд и расширение PT (.pka)')
        return ('replace:learn-netsim', '')
    if cat == 'model':
        return ('replace:NR01/NR02/NS01/NPC', 'модели Cisco → идентичность learn-netsim (маршрутизаторы NR01/NR02, коммутатор NS01, ПК NPC); имена интерфейсов согласовать с моделью netsim')
    if cat == 'product':
        if 'packet tracer' in keys or 'PT' in keys: return ('replace:learn-netsim', 'Packet Tracer → learn-netsim; PT-специфичные элементы GUI (Check Results, Activity Wizard, Logical/Physical) переписать')
        if 'webex' in keys: return ('neutralize', 'Cisco Webex → «инструменты видеоконференций и совместной работы» без бренда')
        if 'meraki' in keys or 'MX64W' in keys: return ('neutralize', 'заголовок «Cisco Meraki MX64W» → «домашний маршрутизатор „всё в одном“»')
        if 'IOS' in keys or 'IOS XE' in keys or 'NX-OS' in keys: return ('replace:NetOS', 'Cisco IOS как название ОС → NSALAB NetOS (или нейтрально «сетевая ОС»); синтаксис команд остаётся')
        if 'catalyst' in keys or 'ISR' in keys: return ('replace:NR01/NR02/NS01/NPC', 'линейка продуктов Cisco → модели learn-netsim')
        if 'ASA' in keys or 'ESA/WSA' in keys: return ('neutralize', 'продуктовые названия Cisco (ASA, ESA/WSA) → типы устройств («межсетевой экран», «шлюз защиты почты/веб-трафика»)')
        if 'opendns' in keys: return ('neutralize', 'OpenDNS (Cisco) → «публичные защищённые DNS-сервисы» без бренда')
        if 'telepresence' in keys: return ('neutralize', 'TelePresence (продукт Cisco) → «терминал видеоконференций»')
        if 'AutoSecure' in keys: return ('remove', 'auto secure — функция Cisco IOS; в learn-netsim нет')
        return ('neutralize', '')
    if cat == 'proprietary-tech':
        if 'CDP' in keys: return ('decide', 'CDP (проприетарный) → LLDP (IEEE 802.1AB) как учебная тема? learn-netsim реализует протоколы clean-room')
        if 'EIGRP' in keys: return ('decide', 'EIGRP (RFC 7868, но бренд Cisco) — оставить как пример протокола маршрутизации без слов «разработан Cisco» или убрать из списка')
        if 'CEF' in keys: return ('neutralize', 'строки CEF в выводе show — исчезнут при перегенерации вывода на learn-netsim')
        if 'AutoSecure' in keys: return ('remove', 'функция Cisco IOS auto secure, нет в learn-netsim')
        return ('decide', 'проприетарная технология Cisco')
    if cat == 'certification':
        if 'сертификаци' in keys: return ('decide', 'абзац о сертификациях (NetAcad-маркетинг PT/карьеры); переписать нейтрально или убрать')
        if re.search(r'ccna(-lab)?\.com', low): return ('replace:lab.local', 'доменное имя CCNA.com/CCNA-lab.com в задании → нейтральный домен')
        if 'ccna' in keys and surface in ('text', 'quiz', 'metadata'): return ('neutralize', '«курс CCNA» → «этот курс»; отсылка к сертификации убрать')
        if 'itn' in keys or 'v7' in keys or 'scope and sequence' in keys: return ('keep', 'внутренняя ссылка на исходную программу ITN v7.02')
        return ('decide', '')
    if cat == 'marketing': return ('remove', 'рекламный/имиджевый текст NetAcad')
    if cat == 'brand':
        if re.search(r'пароль|password|secret|enable|login', low) and re.search(r'\bcisco\d*\b|cisco(en|con)pa55|cisco123', low):
            return ('replace:class123', 'бренд в учебных паролях (cisco, Cisco123, Ciscoenpa55/Ciscoconpa55) → нейтральные пароли; проверить оценочные критерии assessment/ms.yaml')
        if 'networking academy' in keys or 'netacad' in keys or 'сетевая академия' in keys or 'skills for all' in keys: return ('remove', 'упоминание программы Cisco Networking Academy')
        if 'академи' in keys: return ('neutralize', '«политика академии» → «политика учебного заведения»')
        if 'db8:acad' in keys: return ('decide', 'префикс 2001:db8:acad::/48 — конвенция NetAcad (acad = academy); заменить на 2001:db8:1::/48 или оставить как документационный префикс')
        if 'ACAD_' in keys: return ('neutralize', 'имена пулов ACAD_* (academy)')
        if re.search(r'устройств\w* cisco|маршрутизатор\w* cisco|роутер\w* cisco|коммутатор\w* cisco|cisco (device|router|switch)', low):
            return ('neutralize', '«устройство/маршрутизатор/коммутатор Cisco» → без бренда («сетевое устройство», «маршрутизатор»)')
        return ('neutralize', 'убрать бренд из формулировки')
    return ('decide', '')

# ---------- grouping ----------
def exam_dir(p):
    parts = p.split('/')
    return '/'.join(parts[:3]) if len(parts) > 3 else p
def group_of(h):
    p = h['path']; top = p.split('/')[0]; surf = h['surface']
    if h['module'] == '__exams' or top == '__exams': return ('exam', exam_dir(p))
    if top == 'videos': return ('file', p)
    if top == 'packet-tracer-source-files': return ('ptsrc', 'packet-tracer-source-files/')
    if p == 'figma-assets.json': return ('file', p)
    if top == 'animations': return ('animations', 'animations/')
    if top == 'readme-assets': return ('file', p)
    if top == 'final-itn': return ('file', 'final-itn/test.json')
    if top == '.github' or top == '.vscode': return ('line', (p, h['locator']))
    is_lab_infra = surf == 'lab-infra' or '/deploy/' in p or '/deploy-azure/' in p or '/assessment/' in p or p.endswith('assessment.json') or p.endswith('.pka')
    if is_lab_infra:
        lab = material_of(p)
        if lab.startswith('final-lab'): lab = 'final-lab'
        return ('lab', lab)
    if h['key'] == 'db8:acad': return ('termfile', (p, 'db8:acad'))
    return ('line', (p, h['locator']))
groups = collections.OrderedDict()
for h in KEEP:
    g = group_of(h); h['group'] = g
    groups.setdefault(g, []).append(h)

rows = []
GROUP_ROW = {}
def add_row(module, material, surface, locator, term, category, audience, excerpt, action, note):
    rows.append(dict(module=module, material=material, surface=surface, locator=locator, term=term, category=category,
                     audience=audience, excerpt=(excerpt or '').replace('\n', ' ').strip()[:160], action=action, note=note))

# ---- labs inventory ----
tracked = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, cwd=REPO).stdout.split('\n')
def lab_artefacts(lab):
    fs = [f for f in tracked if f.startswith(lab + '/')]
    pka = [f for f in fs if f.endswith('.pka')]
    tf = [f for f in fs if f.endswith('.tf')]
    az = [f for f in fs if '/deploy-azure/' in f]
    ms = [f for f in fs if f.endswith('assessment/ms.yaml')]
    vwr = False
    for m in ms:
        if 'validate_web_response' in open(os.path.join(REPO, m), encoding='utf-8', errors='replace').read(): vwr = True
    topo = [f for f in fs if f.endswith('assets/topology.png')]
    return pka, tf, az, ms, vwr, topo
LAB_TITLE = {}
for d in sorted({g[1] for g in groups if g[0] == 'lab'}):
    try: LAB_TITLE[d] = json.load(open(os.path.join(REPO, d, 'learn-metadata.json'))).get('title', '')
    except Exception: LAB_TITLE[d] = ''
NETSIM_STATUS = {'16-network-security-fundamentals/16.04.06-lab-configure-secure-passwords-and-ssh':
                 'переводится на learn-netsim: PR nsalab-tmn/learn-ccna1#53 открыт (ветка netsim-16.4.6), в main пока PT'}

# ---- build rows from groups ----
line_groups = [(g, hs) for g, hs in groups.items() if g[0] == 'line']
def sort_key(item):
    (kind, key), hs = item
    p = key[0]; loc = key[1]
    m = re.search(r':(\d+)$', loc) or re.search(r':p(\d+):l(\d+)$', loc) or re.search(r':para(\d+)$', loc)
    n = int(m.group(1)) if m else 0
    return (p, n, loc)
for (kind, key), hs in sorted(line_groups, key=sort_key):
    p, loc = key
    h0 = hs[0]
    surface = h0['surface']; audience = h0['audience']
    keys = {h['key'] for h in hs}
    terms = []
    for h in sorted(hs, key=lambda x: x['start']):
        if h['matched'] not in terms: terms.append(h['matched'])
    cat = pick_category(hs, surface)
    excerpt = h0['context']
    note = ''
    if 'youtube' in keys and surface == 'text':
        vid = re.search(r'v=([\w-]+)', excerpt).group(1)
        v = videos.get(vid, {})
        cls = v.get('cls', '?')
        surface = 'video'
        cat = 'marketing' if cls.startswith('marketing') else 'brand'
        action = 'remove' if cat == 'marketing' else 'replace:пересборка (Figma Motion / learn-netsim)'
        done = 'видеоряд в Figma готов' if 'готов' in v.get('figma', '') else 'пересборка не начата'
        note = f"видео NetAcad «{v.get('title','')}», класс {cls}; канал Aleksandr Gorbachev (перезалив ролика Cisco Networking Academy); {VIDEO_LOGO.get(vid, 'логотип Cisco в кадре не отмечен в разборе')}; {done}; документ videos/*--{vid}.md"
        term = f'youtube {vid}'
        add_row(h0['module'], h0['material'], surface, f"{loc} · videoId={vid}", term, cat, 'learner', excerpt, action, note); GROUP_ROW[(kind, key)] = rows[-1]
        continue
    if 'сертификаци' in keys and not (keys - {'сертификаци'}):
        cat = 'marketing'
        action, note = 'decide', 'абзац о сертификациях (вендор не назван; наследие NetAcad-маркетинга «сертификация → карьера»); переписать нейтрально или оставить'
        add_row(h0['module'], h0['material'], surface, loc, '; '.join(terms), cat, audience, excerpt, action, note); GROUP_ROW[(kind, key)] = rows[-1]; continue
    act = action_for(cat, keys, surface, excerpt, h0['module'])
    action, note = act if act else ('decide', '')
    if surface == 'comment': note = (note + '; ' if note else '') + 'в HTML-комментарии README (обучающемуся не виден)'
    if surface == 'metadata' and p.endswith('learn-metadata.json') and '$ref' in excerpt:
        action, note = 'decide', 'путь $ref содержит имя каталога с вендором; меняется вместе с переименованием каталога'
    if surface == 'filename':
        if p.endswith('.pkt'): action, note = 'remove', 'файл Packet Tracer (.pkt) для видеозадания; уходит вместе с видео/заданием'
        elif p.startswith('ccna1-labs') or '/' not in p and p.endswith('.md'): action, note = 'decide', 'имя служебного файла с кодом курса'
        else: action, note = 'decide', 'имя каталога/файла с вендором: переименование меняет $ref в learn-metadata.json и внешние ссылки — делать одним проходом'
    if surface == 'internal-doc':
        action = 'keep'
        note = 'служебный документ, обучающемуся не показывается; правится вместе с переносом курса (или удаляется)'
        if 'migration-instructions' in p and '"Cisco"' in excerpt: action, note = 'replace:Networking', 'шаблон метаданных в инструкции по миграции; обновить вместе с material-tags.json'
    if p == 'material-tags.json' or (p.endswith('learn-metadata.json') and '"Cisco"' in excerpt):
        action, note = 'replace:Networking', 'тег "Cisco" ставится всем материалам курса через $ref material-tags.json'
    if not note: note = {'brand': 'упоминание бренда', 'product': 'название продукта вендора', 'certification': 'код курса/сертификации вендора', 'link': 'ссылка/домен вендора'}.get(cat, '')
    add_row(h0['module'], h0['material'], surface, loc, '; '.join(terms), cat, audience, excerpt, action, note); GROUP_ROW[(kind, key)] = rows[-1]

# termfile rows (db8:acad)
for (kind, key), hs in sorted(((g, hs) for g, hs in groups.items() if g[0] == 'termfile'), key=lambda x: x[0][1][0]):
    p = key[0]
    lines = sorted({int(re.search(r':(\d+)$', h['locator']).group(1)) for h in hs if re.search(r':(\d+)$', h['locator'])})
    loc = f"{p}:{','.join(map(str, lines[:12]))}{'…' if len(lines) > 12 else ''}"
    add_row(hs[0]['module'], hs[0]['material'], hs[0]['surface'], loc, f'2001:db8:acad (×{len(hs)})', 'brand', hs[0]['audience'],
            hs[0]['context'], 'decide', 'префикс 2001:db8:acad::/48 — конвенция NetAcad («acad» = academy); заменить на 2001:db8:1::/48 (или другой документационный) во всём курсе разом или оставить'); GROUP_ROW[(kind, key)] = rows[-1]

# lab rows
for (kind, lab), hs in sorted(((g, hs) for g, hs in groups.items() if g[0] == 'lab'), key=lambda x: x[0][1]):
    pka, tf, az, ms, vwr, topo = lab_artefacts(lab)
    c = collections.Counter(h['key'] for h in hs)
    art = []
    if pka: art.append('; '.join(os.path.relpath(x, lab) for x in pka))
    if tf: art.append(f"{len(tf)} .tf (deploy/pt-lab{', deploy-azure' if az else ''})")
    if ms: art.append('assessment/ms.yaml' + (' → validate_web_response {pt-url}:{pt-api-port}' if vwr else ''))
    term = 'PT lab-infra: ' + ', '.join(art) if art else 'lab-infra'
    excerpt = f"{LAB_TITLE.get(lab,'')} — совпадений в deploy/assessment: " + ', '.join(f'{k}×{v}' for k, v in c.most_common())
    note = NETSIM_STATUS.get(lab, 'лаба на Packet Tracer (PT API через pt-url); перевод на learn-netsim по decisions/packet-tracer-substitution.md')
    if 'physical-mode' in lab: note += '; physical-mode лаба — зависит от PT Physical Mode (стойки, кабели), в netsim аналога нет: решить, переписывать или снимать'
    add_row(MODULE_OF(lab), lab, 'lab-infra', lab + '/{deploy,assessment,assessment.json}', term, 'lab-infra', 'internal', excerpt, 'replace:learn-netsim', note); GROUP_ROW[(kind, lab)] = rows[-1]

# exam rows
EXAM_IMG_NOTES = {
 '__exams/CCNA1': 'копии экзаменов CCNA1 (отличаются от версий в learning path), иллюстрации — экспорт NetAcad в фирменном бирюзовом стиле иконок Cisco',
 '__exams/CCNA2': 'экзамены CCNA2 (SRWE) — не входят в этот курс; в иллюстрациях: hostname CiscoVille, domain-name cisco.com/netacad.net, пулы ACAD_*, выводы EtherChannel/PAgP/HSRP/CDP, иконки Cisco',
 '__exams/CCNA3': 'экзамены CCNA3 (ENSA) — не входят в этот курс; в иллюстрациях: CiscoVille, образы c1841-*k9, show cdp neighbors (C2811/C1941/2960), «Cisco NSF helper», иконки Cisco',
}
exam_groups = sorted(((g, hs) for g, hs in groups.items() if g[0] == 'exam'), key=lambda x: x[0][1])
for (kind, d), hs in exam_groups:
    c = collections.Counter(h['key'] for h in hs)
    fs = [f for f in tracked if f.startswith(d + '/') or f == d]
    imgs = [f for f in fs if re.search(r'\.(png|jpe?g|gif)$', f, re.I)]
    pka = [f for f in fs if f.endswith('.pka')]
    docx = [f for f in fs if f.endswith('.docx')]
    term = ', '.join(f'{k}×{v}' for k, v in c.most_common(8))
    cat = 'certification' if d.endswith('.pka') or c.most_common(1)[0][0] in ('ccna', 'itn', 'srwe', 'ensa') else pick_category(hs, 'quiz')
    extra = f"{len(imgs)} изображений, {len(pka)} .pka, {len(docx)} .docx; " if (imgs or pka or docx) else ''
    base = '/'.join(d.split('/')[:2])
    add_row('__exams', d, 'quiz' if not d.endswith('.pka') else 'lab-infra', d, term, cat, 'internal',
            extra + EXAM_IMG_NOTES.get(base, ''), 'decide',
            'каталог __exams не подключён к learn-metadata.json курса; CCNA1_* дублируют экзамены учебного пути (с расхождениями), CCNA2/CCNA3 — чужие курсы. Предложение: убрать из репозитория или вынести в архив'); GROUP_ROW[(kind, d)] = rows[-1]

# file rows (videos docs, figma-assets, readme-assets pdf, final-itn)
for (kind, p), hs in sorted(((g, hs) for g, hs in groups.items() if g[0] == 'file'), key=lambda x: x[0][1]):
    c = collections.Counter(h['key'] for h in hs)
    term = ', '.join(f'{k}×{v}' for k, v in c.most_common(10))
    if p.startswith('videos/'):
        vid = re.search(r'--([\w-]+)\.md$', p)
        note = 'рабочий документ разбора видео NetAcad (класс, сценарий, транскрипт); вендор упоминается по существу разбора' if vid else 'индекс разборов видео'
        add_row('(root)', 'videos/', 'internal-doc', p, term, 'brand', 'internal', hs[0]['context'], 'keep', note); GROUP_ROW[(kind, p)] = rows[-1]
    elif p == 'figma-assets.json':
        add_row('(root)', p, 'internal-doc', p, term, 'certification', 'internal',
                'id ассетов "ccna1-…" (443), имена страниц Figma "CCNA1 · NN …" (369), course: "ccna1", заметка 16.1.1 «в оригинале Cisco…»',
                'decide', 'идентификаторы пайплайна figma-sync: id стабильны и завязаны на штампы ⟨id⟩ в Figma — переименовывать дорого; имена страниц и course можно сменить при ребрендинге курса'); GROUP_ROW[(kind, p)] = rows[-1]
    elif p.startswith('readme-assets/'):
        add_row('(root)', 'readme-assets/', 'internal-doc', p, term, 'certification', 'internal', hs[0]['context'], 'remove',
                'оригинальный Scope and Sequence Cisco (© 2021 Cisco, Cisco Confidential, netacad.com) — служебный ориентир нумерации тем; удалить после фиксации структуры'); GROUP_ROW[(kind, p)] = rows[-1]
    elif p.startswith('final-itn'):
        add_row('final-itn', p, 'quiz', p, term, 'certification', 'internal', hs[0]['context'], 'decide',
                'не подключён к курсу (нет в learn-metadata.json); тег "Cisco", title "Final ITN", вопросы с Cisco IOS — удалить или заменить final-exam'); GROUP_ROW[(kind, p)] = rows[-1]
# packet-tracer-source-files
for (kind, p), hs in ((g, hs) for g, hs in groups.items() if g[0] == 'ptsrc'):
    c = collections.Counter(h['key'] for h in hs)
    n = len([f for f in tracked if f.startswith('packet-tracer-source-files/')])
    add_row('(root)', 'packet-tracer-source-files/', 'internal-doc', 'packet-tracer-source-files/*.docx (41 файл)',
            ', '.join(f'{k}×{v}' for k, v in c.most_common(10)), 'product', 'internal',
            f'{n} исходных инструкций «Packet Tracer - …» (.docx, перевод NetAcad) с текстом © Cisco; имена файлов содержат «Packet Tracer»',
            'remove', 'источники уже перенесены в README лаб; после миграции на learn-netsim не нужны (или вынести в архив вне репозитория)'); GROUP_ROW[(kind, p)] = rows[-1]
# animations dir
for (kind, p), hs in ((g, hs) for g, hs in groups.items() if g[0] == 'animations'):
    c = collections.Counter(h['key'] for h in hs)
    add_row('(root)', 'animations/', 'internal-doc', 'animations/ccna1-*/ (44 каталога), tracks.json/spec.json',
            ', '.join(f'{k}×{v}' for k, v in c.most_common(10)), 'certification', 'internal',
            'имена каталогов = id ассетов ccna1-…; в tracks.json поле page "CCNA1 · …"; spec.json 16.2.2-1 описывает карточку WHOIS cisco.com',
            'decide', 'идентификаторы пайплайна (см. figma-assets.json); содержание spec.json 16.2.2-1 отражает вендорную сцену анимации — меняется вместе с ней'); GROUP_ROW[(kind, p)] = rows[-1]

# ---------- visual rows ----------
def fig_loc(path):
    a = ASSET_BY_PATH.get(path)
    if a and a.get('figma', {}).get('nodeId'): return f"{path} · key={a['display']['key']} · nodeId={a['figma']['nodeId']}"
    if a: return f"{path} · key={a['display']['key']} (native, не в Figma)"
    return path
VIS = []  # (path, surface, term, category, excerpt, action, note)
def ill(key, term, cat, excerpt, action, note):
    a = ASSET_BY_KEY[key]; VIS.append((a['out']['path'], 'illustration' if a['kind'] == 'illustration' else 'animation', term, cat, excerpt, action, note))
ill('1.3.1', 'TelePresence', 'product', 'подпись «Терминальное оборудование TelePresence» в легенде символов сети', 'neutralize', 'TelePresence — продукт Cisco; → «терминал видеоконференций»')
ill('3.3.4', 'EIGRP', 'proprietary-tech', 'карта протоколов TCP/IP: в списке протоколов маршрутизации «EIGRP»', 'decide', 'см. решение по EIGRP')
for k in ['14.1.2-1', '14.1.2-2', '14.1.2-3', '14.1.2-5']:
    ill(k, 'cisco.com screenshot · Cisco logo · «Trust means you\'re ready for anything»', 'visual', 'встроенный растр: окно браузера с главной страницей cisco.com (логотип Cisco, слоган, баннер Webex) как пример веб-страницы', 'replace:макет нейтральной веб-страницы', 'один и тот же растр (sha1 5de046e8) в 4 фигурах; заменить компонентом «окно браузера» из библиотеки')
ill('14.1.2-4', 'cisco.com screenshot · Cisco logo · «You have challenges. We have solutions.»', 'visual', 'встроенный растр: страница cisco.com в окне браузера', 'replace:макет нейтральной веб-страницы', 'растр sha1 6f245279, общий с 15.3.1-4')
ill('15.3.1-1', 'http://www.cisco.com/index.html', 'link', 'текст в фигуре: URL http://www.cisco.com/index.html как пример разбора URL', 'replace:example.com', 'серия 15.3.1-1…-4 про HTTP-запрос к cisco.com')
ill('15.3.1-2', 'http://www.cisco.com/', 'link', 'адресная строка браузера с cisco.com, стрелка к серверу', 'replace:example.com', '')
ill('15.3.1-3', '<title>Cisco Systems Inc, Home Page</title>', 'brand', 'HTML-ответ сервера с заголовком страницы Cisco Systems', 'replace:example.com', '')
ill('15.3.1-4', 'cisco.com screenshot · Cisco logo', 'visual', 'встроенный растр страницы cisco.com («You have challenges. We have solutions.»)', 'replace:макет нейтральной веб-страницы', 'растр sha1 6f245279, общий с 14.1.2-4')
ill('15.3.2', 'http://www.cisco.com/ · Узел: www.cisco.com', 'link', 'схема HTTP/HTTPS: URL и имя узла cisco.com', 'replace:example.com', '')
ill('15.3.3', 'recipient@cisco.com', 'brand', 'схема SMTP/POP/IMAP: адрес получателя recipient@cisco.com', 'replace:example.com', '')
for k in ['15.4.1-1', '15.4.1-2']: ill(k, 'http://www.cisco.com/', 'link', 'схема DNS-запроса: URL cisco.com в браузере', 'replace:example.com', '')
for k in ['15.4.1-3', '15.4.1-4', '15.4.1-5']: ill(k, 'www.cisco.com 198.133.219.25', 'link', 'схема DNS: запись www.cisco.com → 198.133.219.25', 'replace:example.com', 'адрес 198.133.219.25 — реальный адрес Cisco; взять документационный 203.0.113.x')
ill('15.4.3', 'cisco.com, www.cisco.com, ftp.cisco.com, mail.cisco.com', 'link', 'дерево иерархии DNS с доменом cisco.com', 'replace:example.com', '')
ill('15.5.2-1', 'Cisco Packet Tracer 8.1.1', 'visual', 'встроенный растр: окно Проводника Windows с заголовком «Cisco Packet Tracer 8.1.1» (список файлов программы) как пример общего доступа к файлам', 'replace:нейтральное окно файлового менеджера', 'растр sha1 bc290303 (jpg)')
ill('16.3.1', 'ESA/WSA', 'product', 'схема средств защиты: подпись «ESA/WSA» (Cisco Email/Web Security Appliance), набор значков безопасности в стиле Cisco', 'neutralize', 'подписать по функции: «шлюз защиты почты и веб-трафика»')
for k in ['17.4.3-1', '17.4.3-2', '17.4.4']: ill(k, 'Трассировка с маршрутизатора Cisco IOS', 'product', 'заголовок таблицы/схемы: «Трассировка с маршрутизатора Cisco IOS»', 'replace:NetOS', '')
for k in ['3.3.5-1', '3.3.5-2', '3.6.4', '3.6.5', '4.1.2']:
    ill(k, 'cisco.com slogan «Trust means you\'re ready for anything» в окне браузера', 'marketing', 'анимация: над ПК появляется окно браузера (адрес whois.net / веб-страница) с тёмным скриншотом cisco.com и слоганом Cisco', 'replace:нейтральная веб-страница', 'открытый вопрос kb#223 (3.6.4) подтверждён; тот же растр во всех 5 анимациях — заменить один компонент в Figma и пересинхронизировать')
ill('16.2.2-1', 'WHOIS RECORD FOR cisco.com · Registrant: Cisco Technology, Inc. · CISCO.COM', 'brand', 'анимация «разведка»: карточка WHOIS с данными регистранта Cisco (170 W. Tasman Drive, San Jose) и форма поиска «cisco.com»', 'replace:example.com', 'пример разведки — взять вымышленный домен; spec.json и tracks.json в animations/ccna1-t7zfonu описывают эту сцену')
# rasters (learner-facing)
RAS = [
 ('01-networking-today/01.02-network-components/assets/1.2.5.png', 'коллаж NetAcad с фото маршрутизатора Cisco', 'visual', 'коллаж 6 фото (медь/оптика/беспроводная), среди них маршрутизатор Cisco 1800-й серии', 'remove', 'не используется (embed закомментирован), см. raster-inventory C/P1'),
 ('01-networking-today/01.02-network-components/assets/1.2.5-5.jpg', 'фото Cisco 1800 (корпус Cisco)', 'visual', 'фото беспроводного маршрутизатора Cisco 1800-й серии на шасси Cisco 1841', 'replace:библиотечный беспроводной роутер', 'raster-inventory: B/P1 — одна фигура «три среды передачи»'),
 ('01-networking-today/01.02-network-components/assets/1.2.5-6.jpg', 'IP-камера (бренд не читается)', 'visual', 'фото IP-камеры; бренд на корпусе не читается (вероятно Cisco-Linksys)', 'decide', 'заменить вместе с семьёй 1.2.5-x'),
 ('01-networking-today/01.07-network-trends/assets/1.7.3.png', 'Cisco Webex Meetings · логотип Cisco', 'visual', 'скриншот окна «Cisco Webex Meetings» с участниками; логотип Cisco в углу', 'remove', 'raster-inventory: C/P2 — удалить, фразу «(см. рисунок)» убрать'),
 ('01-networking-today/01.07-network-trends/assets/1.7.8.png', 'PLEK400 · PLE400 · PLSK400', 'visual', 'изометрия NetAcad: дом с адаптерами Powerline, подписи моделей Cisco-Linksys PLEK400/PLE400/PLSK400', 'replace:перерисовать без моделей', 'raster-inventory: A/P1; в тексте 1.7.8 те же модели'),
 ('02-basic-switch-and-end-device-configuration/02.01-access-to-cisco-ios/assets/2.1.3.png', 'software.cisco.com · Catalyst 2960-24TC-L · 12.2.55-SE12 · c2960-lanbasek9-mz.122-55.SE12.bin · логотип Cisco', 'visual', 'скриншот Cisco Software Download: релизы IOS для Catalyst 2960', 'replace:компонент «окно браузера» с таблицей версий NetOS', 'raster-inventory: E/P2; подпись в тексте 2.1.3 «список версий IOS для Catalyst 2960»'),
 ('02-basic-switch-and-end-device-configuration/02.03.08.02-lab-navigate-the-ios-by-using-tera-term-for-console-connectivity/assets/2.3.8.2-1.png', 'иконки Cisco (NetAcad)', 'visual', 'схема подключения коммутатор–ПК, фирменные иконки Cisco', 'replace:шаблон топологии', ''),
 ('02-basic-switch-and-end-device-configuration/02.03.08.02-lab-navigate-the-ios-by-using-tera-term-for-console-connectivity/assets/2.3.8.2-2.png', 'Cisco 2960 switch', 'visual', 'рисунок из документации Cisco: консольное подключение, легенда «1) Cisco 2960 switch»', 'replace:перерисовать', ''),
 ('02-basic-switch-and-end-device-configuration/02.03.08.02-lab-navigate-the-ios-by-using-tera-term-for-console-connectivity/assets/2.3.8.2-3.png', 'иконки Cisco (NetAcad)', 'visual', 'схема маршрутизатор–ПК, иконки Cisco', 'replace:шаблон топологии', ''),
 ('02-basic-switch-and-end-device-configuration/02.03.08.02-lab-navigate-the-ios-by-using-tera-term-for-console-connectivity/assets/2.3.8.2-4.png', 'Cisco ISR (mini-USB console)', 'visual', 'рисунок из документации Cisco: маршрутизатор ISR с консольными портами', 'replace:перерисовать', ''),
 ('02-basic-switch-and-end-device-configuration/02.06-ports-and-addresses/assets/2.6.2.png', 'стек Cisco Catalyst · Cisco 1800', 'visual', 'коллаж: стек коммутаторов Catalyst, маршрутизатор Cisco, кабели', 'replace:фигура «среды передачи»', 'raster-inventory: B/P1'),
 ('04-physical-layer/04.01-purpose-of-the-physical-layer/assets/4.1.1-1.jpg', 'Linksys (Cisco-era) задняя панель', 'visual', 'фото задней панели домашнего роутера Linksys E-серии (выпуск времён Cisco), логотипа не видно', 'decide', 'raster-inventory: A/P2 — одна фигура 4.1.1; Linksys с 2013 г. не Cisco'),
 ('04-physical-layer/04.01-purpose-of-the-physical-layer/assets/4.1.1-2.jpg', 'Linksys роутер', 'visual', 'фото-коллаж роутер Linksys — ноутбук', 'decide', 'в фигуру 4.1.1'),
 ('04-physical-layer/04.06-wireless-media/assets/4.6.3.jpg', 'Cisco Meraki MX64W · логотип Cisco на корпусе', 'visual', 'продуктовое фото Cisco Meraki MX64W', 'replace:библиотечный беспроводной роутер', 'raster-inventory: B/P2; заголовок в тексте 4.6.3'),
 ('17-build-a-small-network/17.02-small-network-applications-and-protocols/assets/17.2.1.jpg', 'Cisco Webex Service · Webex Teams (процессы)', 'visual', 'скриншот Диспетчера задач Windows, в списке процессы Cisco Webex', 'remove', 'raster-inventory: C/P3'),
 ('17-build-a-small-network/17.03-scale-to-larger-networks/assets/17.3.3.png', 'CiscoCollabHost', 'visual', 'скриншот Windows «Использование данных»: в списке приложение CiscoCollabHost', 'replace:компонент окна настроек', 'raster-inventory: E/P3'),
 ('08-10-exam/assets/4.png', 'PC> tracert www.cisco.com', 'link', 'изображение к вопросу экзамена: вывод tracert до www.cisco.com из командной строки PT', 'replace:example.com', 'иконки Cisco'),
 ('04-physical-layer/04.06.05-lab-connect-a-wired-and-wireless-lan/assets/topology.png', 'скриншот Packet Tracer · сервер «netacad.pka»', 'visual', 'топология лабы — скриншот рабочего поля PT с именем сервера netacad.pka', 'replace:шаблон топологии', ''),
 ('17-build-a-small-network/17.07.06-lab-troubleshoot-connectivity-issues/assets/topology.png', 'скриншот Packet Tracer · «www.cisco.pka»', 'visual', 'топология лабы — скриншот PT, сервер подписан www.cisco.pka', 'replace:шаблон топологии', ''),
 ('17-build-a-small-network/17.08.02-lab-skills-integration-challenge/assets/topology.png', 'скриншот Packet Tracer · «www.cisco.pka / www.cisco6.pka»', 'visual', 'топология лабы — скриншот PT, серверы www.cisco.pka и www.cisco6.pka', 'replace:шаблон топологии', ''),
]
PT_TOPO = ['01-networking-today/01.00.05-lab-logical-and-physical-mode-exploration', '01-networking-today/01.05.07-lab-network-representation',
 '02-basic-switch-and-end-device-configuration/02.03.07-lab-navigate-the-ios', '02-basic-switch-and-end-device-configuration/02.05.05-lab-configure-initial-switch-settings',
 '02-basic-switch-and-end-device-configuration/02.07.06-lab-implement-basic-connectivity', '02-basic-switch-and-end-device-configuration/02.09.01-lab-basic-switch-and-end-device-configuration',
 '03-protocols-and-models/03.05.05-lab-investigate-the-tcp-ip-and-osi-models-in-action', '04-physical-layer/04.07.02-lab-connect-the-physical-layer',
 '09-address-resolution/09.01.03-lab-identify-mac-and-ip-addresses', '09-address-resolution/09.02.09-lab-examine-the-arp-table', '09-address-resolution/09.03.04-lab-ipv6-neighbor-discovery',
 '10-basic-router-configuration/10.01.04-lab-configure-initial-router-settings', '10-basic-router-configuration/10.03.04-lab-connect-a-router-to-a-lan', '10-basic-router-configuration/10.03.05-lab-troubleshoot-default-gateway-issues', '10-basic-router-configuration/10.04.03-lab-basic-device-configuration',
 '11-ipv4-addressing/11.05.05-lab-subnet-an-ipv4-network', '11-ipv4-addressing/11.07.05-lab-subnetting-scenario', '11-ipv4-addressing/11.09.03-lab-vlsm-design-and-implementation-practice', '11-ipv4-addressing/11.10.01-lab-design-and-implement-a-vlsm-addressing-scheme',
 '12-ipv6-addressing/12.06.06-lab-configure-ipv6-addressing', '12-ipv6-addressing/12.09.01-lab-implement-a-subnetted-ipv6-addressing-scheme',
 '13-icmp/13.02.06-lab-verify-ipv4-and-ipv6-addressing', '13-icmp/13.02.07-lab-use-ping-and-traceroute-to-test-network-connectivity', '13-icmp/13.03.01-lab-use-icmp-to-test-and-correct-network-connectivity',
 '14-transport-layer/14.08.01-lab-tcp-and-udp-communications', '16-network-security-fundamentals/16.04.06-lab-configure-secure-passwords-and-ssh', '16-network-security-fundamentals/16.05.01-lab-secure-network-devices',
 '17-build-a-small-network/17.05.09-lab-interpret-show-command-output', '17-build-a-small-network/17.08.01-lab-design-and-build-a-small-network-physical-mode', '17-build-a-small-network/17.08.03-lab-troubleshooting-challenge']
for lab in PT_TOPO:
    RAS.append((lab + '/assets/topology.png', 'скриншот рабочего поля Packet Tracer', 'visual', 'топология лабы — скриншот PT: иконки устройств PT, подписи моделей/портов PT', 'replace:шаблон топологии', 'перерисовать по шаблону «топология лабы» из библиотеки (raster-inventory, приложение)'))
NETACAD_FIG = ['02-basic-switch-and-end-device-configuration/02.09.02-lab-basic-switch-and-end-device-configuration-physical-mode/assets/topology.png',
 '10-basic-router-configuration/10.04.04-lab-build-a-switch-and-router-network-physical-mode/assets/topology.png',
 '11-ipv4-addressing/11.10.02-lab-design-and-implement-a-vlsm-addressing-scheme-physical-mode/assets/topology.png',
 '12-ipv6-addressing/12.09.02-lab-configure-ipv6-addresses-on-network-devices-physical-mode/assets/topology.png',
 '13-icmp/13.03.02-lab-use-ping-and-traceroute-to-test-network-connectivity-physical-mode/assets/topology.png',
 '17-build-a-small-network/17.07.07-lab-troubleshoot-connectivity-issues-physical-mode/assets/topology.png',
 '03-protocols-and-models/03.07.10-lab-use-wireshark-to-view-network-traffic/assets/3.7.10-1.png',
 '07-ethernet-switching/07.01.06-lab-use-wireshark-to-examine-ethernet-frames/assets/7.1.6-1.png',
 '07-ethernet-switching/07.02.07-lab-view-network-device-mac-addresses/assets/7.2.7-1.png',
 '07-ethernet-switching/07.03.07-lab-view-the-switch-mac-address-table/assets/7.3.7-1.png',
 '12-ipv6-addressing/12.07.04-lab-identify-ipv6-addresses/assets/12.7.4-1.png',
 '16-network-security-fundamentals/16.04.07-lab-configure-network-devices-with-ssh/assets/16.4.7-1.png',
 '17-build-a-small-network/17.04.06-lab-test-network-latency-with-ping-and-traceroute/assets/17.4.6-1.png',
 '01-03-exam/assets/2.png', '04-07-exam/assets/3.png', '04-07-exam/assets/5.png', '08-10-exam/assets/2.png', '08-10-exam/assets/3.gif', '08-10-exam/assets/5.png',
 '11-13-exam/assets/1.PNG', '11-13-exam/assets/2.PNG', '11-13-exam/assets/3.png', '11-13-exam/assets/5.png', '16-17-exam/assets/3.jpg', '16-17-exam/assets/4.jpg',
 'final-exam/assets/2.png', 'final-exam/assets/3.png', 'final-exam/assets/4.png']
for p in NETACAD_FIG:
    RAS.append((p, 'фирменный набор иконок Cisco (NetAcad)', 'visual', 'схема/топология в бирюзовом стиле NetAcad с фирменными значками устройств Cisco (маршрутизатор-«шайба» со стрелками, коммутатор со стрелками, ПК)', 'replace:шаблон топологии', 'экспорт NetAcad; перерисовать в библиотечном стиле (решение по иконкам — см. figma-library)'))
for p, term, cat, exc, act, note in RAS:
    VIS.append((p, 'raster', term, cat, exc, act, note))
# PDFs (visual)
for f in tracked:
    if f.endswith('.pdf'):
        if f.startswith('readme-assets'): continue
        VIS.append((f, 'raster', 'логотип Cisco Networking Academy (шапка каждой страницы) · © Cisco (подвал)', 'visual',
                    'PDF-описание лабы NetAcad: шапка «Cisco Networking Academy» с логотипом, подвал «© … Корпорация Cisco… Все права защищены… www.netacad.com»; схемы в стиле NetAcad', 'replace:README', 'перенести текст в README лабы (как сделано для остальных) и удалить PDF; текстовые совпадения внутри PDF — отдельные строки surface=text'))
VIS.append(('readme-assets/itn-v7.02-scope-and-sequence.pdf', 'raster', 'логотип Cisco Networking Academy · CCNAv7.02 · Cisco Confidential', 'visual', 'оригинальный Scope and Sequence Cisco с логотипом', 'remove', 'служебный документ'))
for f in sorted(tracked):
    if f.startswith('readme-assets/') and re.search(r'\.png$', f):
        desc = {'pt-menu.png': 'окно «Cisco Packet Tracer» с меню Extensions → Activity Wizard', 'pt-editor.png': 'редактор Activity Wizard Packet Tracer с инструкцией «Packet Tracer. Создание основных подключений»',
                'lab-topology-bad.png': 'скриншот топологии Packet Tracer (плохой пример)', 'lab-topology-good.png': 'скриншот топологии Packet Tracer (хороший пример)',
                'writage-1.png': 'Word + Writage, текст «Packet Tracer. Создание основных подключений»', 'writage-2.png': 'Word + Writage, блок «Packet Tracer PC Command Line 1.0»'}.get(os.path.basename(f),
                'скриншот сайта NetAcad (contenthub.netacad.com / Introduction to Networks v7.02) с логотипом Cisco')
        VIS.append((f, 'raster', 'логотип Cisco / NetAcad UI / Packet Tracer', 'visual', desc, 'decide', 'иллюстрации к migration-instructions.md (инструкция переноса из NetAcad); устаревает вместе с ней'))
for p, surface, term, cat, exc, act, note in VIS:
    add_row(MODULE_OF(p), material_of(p), surface, fig_loc(p), term, cat, 'internal' if p.startswith('readme-assets') else 'learner', exc, act, note)
# figma library verdict
add_row('(root)', 'figma:3FtCg22qFubpLBPOetQU03', 'figma-library', 'Figma 3FtCg22qFubpLBPOetQU03 · лист «_Библиотека» (компоненты устройств); оценено по 369 экспортированным фигурам, API/MCP Figma в среде аудита недоступны',
        'набор иконок устройств повторяет визуальный язык Cisco', 'visual', 'learner',
        'маршрутизатор — «шайба» с четырьмя стрелками, коммутатор — плоский брусок со стрелками, многоуровневый коммутатор — куб со звездой стрелок, межсетевой экран — кирпичная стена, хаб/WAN-коммутатор — те же глифы; выполнено собственной изометрической отрисовкой и палитрой, без логотипов и надписей',
        'decide', 'формы = де-факто отраслевой язык схем, но происхождение — иконография Cisco; варианты: (а) оставить как «отраслевой стандарт», (б) переработать силуэты (другие стрелки/пропорции) при сохранении читаемости. Одно решение на библиотеку; отдельных строк по 300+ фигурам не заводим')

# ---------- ids, sort, write CSV ----------
def mod_order(m):
    if m == '(root)': return (0, m)
    if m == '__exams': return (99, m)
    if m.startswith('final-'): return (90, m)
    return (int(m[:2]), m) if m[:2].isdigit() else (50, m)
rows.sort(key=lambda r: (mod_order(r['module']), r['material'], r['surface'] == 'lab-infra', r['locator']))
for i, r in enumerate(rows, 1): r['id'] = f'ccna1-vm-{i:04d}'
cols = ['id', 'module', 'material', 'surface', 'locator', 'term', 'category', 'audience', 'excerpt', 'action', 'note']
with open(os.path.join(OUT, 'vendor-mentions.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for r in rows: w.writerow({c: r[c] for c in cols})
print('rows', len(rows))
print('by category', collections.Counter(r['category'] for r in rows).most_common())
print('by surface', collections.Counter(r['surface'] for r in rows).most_common())
print('by action', collections.Counter(r['action'].split(':')[0] for r in rows).most_common())

# ---------- reconciliation dump ----------
missing = [h for h in KEEP if h['group'] not in GROUP_ROW]
print('hits without row:', len(missing), collections.Counter((h['group'][0], h['key']) for h in missing).most_common(5))
recon = collections.OrderedDict()
src = open(os.path.join(HERE, 'scan.py'), encoding='utf-8').read()
TERMS = eval(src[src.index('TERMS = [') + len('TERMS = '):src.index(']\nCTERMS')] + ']', {'I': re.IGNORECASE})
for k, rx, fl, cat, indict in TERMS:
    hk = [h for h in H if h['key'] == k]
    kept = [h for h in hk if not h['excl']]
    recon[k] = dict(regex=rx, indict=indict, cat=cat, N=len(hk), K=len(hk) - len(kept), M=len(kept),
                    rows=len({GROUP_ROW[h['group']]['id'] for h in kept if h['group'] in GROUP_ROW}),
                    excl=collections.Counter(h['excl'] for h in hk if h['excl']).most_common())
json.dump(recon, open(f'{WORK}/recon.json', 'w'), ensure_ascii=False, indent=1)
json.dump(rows, open(f'{WORK}/rows.json', 'w'), ensure_ascii=False, indent=0)

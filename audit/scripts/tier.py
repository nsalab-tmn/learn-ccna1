#!/usr/bin/env python3
"""Assign de-vendoring tier (P1/P2/P3) + batch id to every row of audit/vendor-mentions.csv.

Scope: learner-facing content only. Internal docs, videos (already classified,
to be re-shot), file/dir names and $ref paths are out of scope ('' tier).
"""
import csv, json, re, os, sys, collections, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get('AUDIT_REPO') or os.path.abspath(os.path.join(HERE, '..', '..'))
WORK = os.environ.get('AUDIT_WORK') or os.path.join(tempfile.gettempdir(), 'vendor-audit')
CSV = os.path.join(REPO, 'audit', 'vendor-mentions.csv')

# ----------------------------------------------------------------- batches
BATCHES = {
 # ---- P1: zero-cost bulk replacements (regex / delete), no rethink
 'P1-01': ('P1', 'Домены, хосты и IP Cisco → нейтральные примеры (cisco.com, netacad.com, 198.133.219.25, dns-sj / mx-01 …)'),
 'P1-02': ('P1', 'Пароли и имена из бренда в лекциях, тестах и не-PT-лабах (cisco / Cisco123 / Ciscoenpa55 / Ciscoville → class123 …)'),
 'P1-03': ('P1', 'Продукты Cisco как примеры (Webex, TelePresence, OpenDNS, ASA, ESA/WSA, Business Edition, Talos) → родовые названия / отечественные аналоги'),
 'P1-04': ('P1', 'Слово «Cisco» без смысловой нагрузки («устройство / коммутатор Cisco», «запатентован Cisco», OUI-пример, «рекомендации Cisco») → убрать'),
 'P1-05': ('P1', '«Cisco IOS» / «IOS» как имя ОС в прозе, тестах и заголовках → имя ОС learn-netsim (одно решение, затем массовая замена)'),
 'P1-06': ('P1', 'Идентичность курса в тексте: «курс CCNA» → «этот курс», тег Cisco → Networking, ответ теста «Cisco»'),
 'P1-07': ('P1', 'Удалить 9 PDF-дубликатов лаб (есть README-версии) и ссылки на них — уходят подвалы ©, netacad.com, логотипы'),
 'P1-08': ('P1', 'Промо-блоки NetAcad / Webex (1.1.2, 1.7.3, 1.7.5, 17.2.1, коллаж 1.2.5) → удалить'),
 'P1-09': ('P1', 'Проприетарные протоколы в перечислениях (EIGRP «разработан Cisco», HSRP как пример порта, CEF в тесте) → убрать / заменить'),
 'P1-10': ('P1', 'Packet Tracer в лекционном тексте (1.10, 2.2, 2.8 «Следуем в PT» + .pkt, 10.3) → learn-netsim / удалить'),
 'P1-11': ('P1', 'Текстовые слои Figma (cisco.com, 198.133.219.25, recipient@cisco.com, WHOIS, TelePresence, EIGRP, ESA/WSA, «Cisco IOS» в подписи) → правка текста + resync'),
 'P1-12': ('P1', 'Префикс 2001:db8:acad в лекциях и не-PT-лабах → другой документационный префикс (условно: если решено менять)'),
 'P1-13': ('P1', 'Строки Windows-вывода с брендом (C:\\Users\\NetAcad>, opendns) → нейтральные'),
 # ---- P2: tightly coupled, but a neutral replacement needs only minor edits
 'P2-01': ('P2', 'Лаба 16.4.6 (уже на learn-netsim): CCNA.com → lab.local, пароли → class123, синхронно с assessment/ms.yaml'),
 'P2-02': ('P2', 'Модели оборудования (2960, 4221/4321, 1941, 2801/2811, 1841, Meraki, PLEK400) → NR01/NR02/NS01/NPC; таблицы интерфейсов 2.3.8.2, 16.4.7; списки «необходимые ресурсы»'),
 'P2-03': ('P2', 'CDP → LLDP (17.5.6, итоги 17.9, тест 17.8.5, экзамен 16-17); нужен `show lldp neighbors` в learn-netsim'),
 'P2-04': ('P2', 'Скриншоты cisco.com / Cisco-продуктов внутри фигур Figma → один компонент «окно браузера» (5 анимаций + 6 иллюстраций), 2.1.3, 15.5.2-1, 17.3.3'),
 'P2-05': ('P2', 'Топологии лаб и экзаменов (скриншоты PT, фигуры в стиле NetAcad) → перерисовать из библиотечного шаблона'),
 'P2-06': ('P2', 'Фото оборудования Cisco / Linksys (1.2.5, 1.7.8, 2.6.2, 4.6.3, 2.3.8.2-2/-4, 4.1.1) → библиотечные фигуры или нейтральные фото'),
 'P2-07': ('P2', 'Карьерный блок: README:10, 1.9 «Индустриальная сертификация», лаба 1.9.3 → нейтральные сертификации и hh.ru'),
 'P2-08': ('P2', 'IOS-специфика: версии/образы/загрузка (2.1.1, 7.4 Auto-MDIX, 16.4 IOS-XE, 16.4.1 auto secure, тесты про образ IOS) → переформулировать под модель загрузки learn-netsim'),
 'P2-09': ('P2', 'Лаба 2.3.8.2 (консоль Tera Term, драйвер «Cisco Serial», учётная запись CCO) → общий USB-консольный адаптер'),
 # ---- P3: tightly coupled, rethink / rewrite
 'P3-01': ('P3', 'Миграция PT-лаб на learn-netsim (41 лаба с .pka + final-lab): текст про интерфейс PT, Check Results, Server-PT, PTPM-сценарии (9 лаб — переписать как логические или снять), 1.0.5'),
 'P3-02': ('P3', 'Учётные данные, имена серверов (.pka), домены и 2001:db8:acad в PT-оцениваемых лабах → менять вместе с ms.yaml при миграции'),
 'P3-03': ('P3', 'Выводы CLI с вендорными строками (show version, Copyright, techsupport, CEF, легенда EIGRP, [IOS]…) → перегенерировать на learn-netsim'),
 'P3-04': ('P3', 'Библиотека иконок Figma (силуэты устройств в стиле Cisco) → решение об идентичности, затем 369 фигур'),
}

# ----------------------------------------------------------------- lab status
def lab_status():
    st = {}
    for root, dirs, files in os.walk(REPO):
        rel = os.path.relpath(root, REPO)
        if rel.startswith(('.git', '__exams', 'audit')):
            dirs[:] = []
            continue
        parts = rel.split(os.sep)
        if len(parts) == 2 and ('-lab-' in parts[1]) or rel == 'final-lab':
            d = root
            has_pka = any(f.endswith('.pka') for _, _, fs in os.walk(d) for f in fs)
            netsim = os.path.exists(os.path.join(d, 'compute', 'local', 'topology.yaml'))
            if netsim:
                s = 'netsim'
            elif has_pka:
                s = 'ptpm' if 'physical-mode' in rel else 'pt'
            else:
                s = 'plain'
            st[rel] = s
    return st

LABS = lab_status()

def status_of(material):
    for k, v in LABS.items():
        if material == k or material.startswith(k + '/'):
            return v
    return None  # lecture / quiz / exam

# ----------------------------------------------------------------- rules
CRED = re.compile(r'Cisco123|Ciscoenpa55|Ciscoconpa55|Ciscoville|CiscoVille|пароль\w*|password|secret|enable|\bcisco\b', re.I)
DEV = re.compile(r'(устройств\w*|коммутатор\w*|маршрутизатор\w*|роутер\w*|оборудовани\w*|сервер\w*|плат\w*|продукт\w*)\s+(компании\s+|корпорации\s+)?Cisco', re.I)
VER = re.compile(r'\bверси|образ\w* IOS|\bобраз(?!ом\b)|image|\bзагруз(?!очн\w* конфигурац)|flash|флэш|флеш|\bROM\b|ROMMON|лиценз|IOS XE|NX-OS|IOS-XE|\b1[256]\.\d\(|universalk9|lanbasek9|Auto-MDIX|auto secure|AutoSecure|файл\w* IOS|обновл', re.I)
VER_BRAND = re.compile(r'\bзагруз(?!очн\w* конфигурац)|образ\w* IOS|\bобраз(?!ом\b)|флэш|\bROM\b|верси\w* IOS|IOS XE|NX-OS', re.I)
CREDV = re.compile(r'\*\*Cisco\*\*|Назначьте Cisco|Cisco123|Ciscoenpa55|Ciscoconpa55|Ciscoville|CiscoVille')
DOM = re.compile(r'cisco\.com|netacad\.com|netacad\.net|198\.133\.219|dns-sj|mx-01|origin-www|wwwds', re.I)
PT = re.compile(r'Packet Tracer|\bPT\b|PTPM|\.pka|\.pkt', re.I)
PRODUCT = re.compile(r'Webex|WebEx|TelePresence|OpenDNS|\bASA\b|\bESA\b|\bWSA\b|Business Edition|Talos|сетевой безопасности Cisco', re.I)
CLI_DEV = re.compile(r'techsupport|Copyright|Cisco IOS|universalk9|ipbasek9|WS-C2960|CEF|EIGRP|\[IOS\]|IOS-XE|IOS XE|LANBASE|cisco ISR|processor|12\.2\(53r\)|c2960-lanbasek9|\bIOS\b', re.I)

def tier(r):
    surf, cat, term, act = r['surface'], r['category'], r['term'], r['action']
    exc, loc, mat = r['excerpt'], r['locator'], r['material']
    st = status_of(mat)
    pt_lab = st in ('pt', 'ptpm')
    is_pdf = '.pdf' in loc

    if r['audience'] != 'learner':
        return '', 'внутренняя поверхность — вне плана'
    if surf == 'video':
        return '', 'видео: классифицированы отдельно, пересъёмка уже в плане'
    if surf == 'filename':
        return '', 'имя файла/каталога — dev-facing, вне плана'
    if surf == 'metadata' and '$ref' in exc:
        return '', 'путь каталога в $ref — dev-facing, вне плана'

    # whole PDF attachments go away (README duplicates exist)
    if is_pdf:
        return 'P1-07', ''

    # ---- visuals
    if surf == 'figma-library':
        return 'P3-04', ''
    if surf == 'raster':
        if act == 'remove':
            return 'P1-08', ''
        if act.startswith('replace:шаблон') or 'tracert' in term:
            return ('P3-01', 'PTPM-лаба: топология уйдёт вместе с переписыванием') if st == 'ptpm' else ('P2-05', '')
        if 'software.cisco.com' in term or 'CiscoCollabHost' in term:
            return 'P2-04', ''
        return 'P2-06', ('по желанию: бренд не Cisco' if act == 'decide' else '')
    if surf == 'animation':
        return ('P1-11', '') if 'WHOIS' in term else ('P2-04', '')
    if surf == 'illustration':
        if act.startswith('replace:макет') or act.startswith('replace:нейтральное окно') or 'screenshot' in term:
            return 'P2-04', ''
        return 'P1-11', ''

    # ---- code (CLI / command outputs)
    if surf == 'code':
        if 'NetAcad' in term and 'Users' in exc:
            return 'P1-13', ''
        if 'opendns' in term.lower():
            return 'P1-13', ''
        if (DOM.search(term) or DOM.search(exc)) and 'techsupport' not in exc:
            return 'P1-01', 'вывод Windows-команды: лучше переснять для ya.ru'
        if 'Packet Tracer' in term:
            return 'P3-01', ''
        if 'auto secure' in term.lower() or 'AutoSecure' in term:
            return 'P2-08', ''
        if 'db8:acad' in term:
            return ('P3-02', '') if pt_lab else ('P1-12', '')
        if 'CCNA' in term:
            return ('P2-01', '') if st == 'netsim' else (('P3-02', '') if pt_lab else ('P1-06', ''))
        if re.search(r'password|secret', exc, re.I) and re.search(r'cisco', exc, re.I):
            if st == 'netsim': return 'P2-01', ''
            if pt_lab: return 'P3-02', ''
            return 'P1-02', ''
        if CLI_DEV.search(term) or CLI_DEV.search(exc):
            return 'P3-03', ''
        return 'P3-03', ''

    # ---- text / quiz / metadata
    if '01.09.03-lab' in mat or mat.endswith('01.09-it-specialist'):
        return 'P2-07', ''
    if 'CDP' in term or 'cdp' in exc.lower():
        return 'P2-03', ''
    if 'EIGRP' in term and cat != 'code':
        return ('P3-01', 'EIGRP преднастроен в .pka') if pt_lab else ('P1-09', '')
    if re.search(r'HSRP|\b1985\b', exc):
        return 'P1-09', ''
    if '02.01-access-to-cisco-ios' in mat and cat in ('brand', 'model') and re.search(r'загрузки программного обеспечения|верси', exc):
        return 'P2-08', ''
    if exc.strip().startswith('"answer": "Cisco IOS"'):
        return 'P2-08', ''
    if cat == 'link':
        if '02.03.08.02' in mat:
            return 'P2-09', ''
        if pt_lab and not re.search(r'https?://', exc):
            return 'P3-02', 'имя внутри симуляции .pka'
        return 'P1-01', ''
    if cat == 'legal':
        return 'P1-07', ''
    if cat == 'marketing':
        if st == 'pt' and PT.search(exc + term) or mat.endswith('01.00.05-lab-logical-and-physical-mode-exploration'):
            return 'P3-01', ''
        return 'P2-07', ''
    if cat == 'certification':
        if act == 'replace:lab.local' or 'CCNA.com' in exc or 'CCNA-lab.com' in exc:
            if st == 'netsim': return 'P2-01', ''
            if pt_lab: return 'P3-02', ''
        if act == 'decide' or re.search(r'CCNP|сертификац', exc, re.I):
            return 'P2-07', ''
        return 'P1-06', ''
    if cat == 'model':
        if st == 'ptpm':
            return 'P3-01', ''
        if 'Packet Tracer' in term:
            return 'P3-01', ''
        return 'P2-02', ''
    if cat == 'proprietary-tech':
        if 'CDP' in term:
            return 'P2-03', ''
        if 'AutoSecure' in term or 'auto secure' in term.lower():
            return 'P2-08', ''
        return 'P1-09', ''
    if cat == 'lab-infra':
        if st is None:  # lecture: .pkt links, PTPM mention in lecture
            return 'P1-10', ''
        if 'PTPM' in term:
            return 'P3-01', ''
        if re.search(r'\.pka|pka', term) or 'netacad' in term.lower() or 'cisco' in term.lower():
            return 'P3-02', ''
        return 'P3-01', ''
    if cat == 'product':
        if PRODUCT.search(term) or PRODUCT.search(exc):
            return 'P1-03', ''
        if PT.search(term):
            if st is None:
                return 'P1-10', ''
            if st == 'netsim':
                return 'P2-01', 'остатки PT в README лабы, уже переведённой на netsim'
            return 'P3-01', ''
        if 'CDP' in term:
            return 'P2-03', ''
        if re.search(r'\bIOS\b|\bios\b', term):
            if re.search(r'IOS XE|NX-OS|IOS-XE', term) or VER.search(exc):
                return 'P2-08', ''
            if 'Catalyst' in exc or re.search(r'\b(2960|4221|4321|1941)\b', exc):
                return 'P2-02', ''
            return 'P1-05', ''
        return 'P1-04', ''
    if cat == 'brand':
        if 'db8:acad' in term:
            return ('P3-02', '') if pt_lab else ('P1-12', '')
        if 'Networking Academy' in term:
            return 'P1-08', ''
        if 'академии' in term:
            return 'P1-04', ''
        if '15.04.08-lab' in mat:
            return 'P1-01', ''
        if mat == 'material-tags.json' or act == 'replace:Networking':
            return 'P1-06', ''
        if act == 'replace:class123' or term == 'cisco' or CREDV.search(exc):
            if st == 'netsim': return 'P2-01', ''
            if pt_lab: return 'P3-02', ''
            return 'P1-02', ''
        if PRODUCT.search(exc):
            return 'P1-03', ''
        if DOM.search(exc) or 'зеркальные серверы' in exc:
            return 'P1-01', ''
        if re.search(r'Cisco Serial|Cisco Connection Online|CCO', exc):
            return 'P2-09', ''
        if re.search(r'Catalyst|\b(2960|4221|4321|1941)\b', exc):
            return 'P2-02', ''
        if VER_BRAND.search(exc):
            return 'P2-08', ''
        return 'P1-04', ''
    return 'P3-01', 'не классифицировано правилом'

# ----------------------------------------------------------------- run
def main():
    os.makedirs(WORK, exist_ok=True)
    rows = list(csv.DictReader(open(CSV, encoding='utf-8')))
    for r in rows:
        b, n = tier(r)
        r['tier'] = BATCHES[b][0] if b else ''
        r['batch'] = b
        r['tier_note'] = n

    fields = ['id','module','material','surface','locator','term','category','audience','excerpt','action','note','tier','batch','tier_note']
    with open(CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ----------------------------------------------------------------- stats
    S = [r for r in rows if r['tier']]
    stats = {
        'in_scope': len(S),
        'out_of_scope': collections.Counter(r['tier_note'] for r in rows if not r['tier']),
        'by_tier': collections.Counter(r['tier'] for r in S),
        'by_batch': collections.Counter(r['batch'] for r in S),
        'by_tier_surface': collections.Counter((r['tier'], r['surface']) for r in S),
        'by_tier_category': collections.Counter((r['tier'], r['category']) for r in S),
        'by_batch_module': collections.defaultdict(collections.Counter),
        'by_batch_material': collections.defaultdict(collections.Counter),
        'by_batch_surface': collections.defaultdict(collections.Counter),
        'labs': LABS,
    }
    for r in S:
        stats['by_batch_module'][r['batch']][r['module']] += 1
        stats['by_batch_material'][r['batch']][r['material']] += 1
        stats['by_batch_surface'][r['batch']][r['surface']] += 1
    def _plain(v):
        if isinstance(v, collections.Counter) or isinstance(v, dict):
            return {(' | '.join(k) if isinstance(k, tuple) else str(k)): _plain(vv) for k, vv in v.items()}
        return v
    json.dump(_plain(stats), open(os.path.join(WORK, 'tier_stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # verification dump
    with open(os.path.join(WORK, 'tier_dump.txt'), 'w', encoding='utf-8') as f:
        for b in BATCHES:
            rs = [r for r in S if r['batch'] == b]
            f.write(f"\n===== {b} ({BATCHES[b][0]}) n={len(rs)} — {BATCHES[b][1]}\n")
            f.write('  surfaces: ' + str(dict(collections.Counter(r['surface'] for r in rs))) + '\n')
            f.write('  actions: ' + str(dict(collections.Counter(r['action'] for r in rs))) + '\n')
            for r in rs:
                f.write(f"  {r['id']} [{r['surface']}/{r['category']}] {r['material'][:50]} | {r['locator'][-38:]} | {r['term'][:40]} | {r['excerpt'][:90]}\n")

    print('in scope', len(S), 'by tier', dict(stats['by_tier']))
    for b in BATCHES:
        print(b, stats['by_batch'].get(b, 0), BATCHES[b][1][:70])
    print('out of scope', dict(stats['out_of_scope']))
    print('labs', collections.Counter(LABS.values()))


if __name__ == '__main__':
    main()

# Аудит упоминаний вендора в CCNA1 (ITN) — сводка

Карта: `audit/vendor-mentions.csv` — **1306 строк** (`ccna1-vm-0001`…`ccna1-vm-1306`), из них 988 видны обучающемуся, 318 служебные. Срез: `origin/main` @ `d7897dd` (2026-10-16). Задача: nsalab-tmn/learn-ccna1#54. В материалах ничего не изменено.

Продолжение: приоритетный план де-вендоризации — [`de-vendoring-plan.md`](./de-vendoring-plan.md); в CSV добавлены столбцы `tier` (P1/P2/P3) и `batch` (пакет работ), заполненные только для учебных поверхностей.

## Как считали

1. **Словарный проход** по всем `git ls-files` (2410 файлов): регистронезависимые регулярные выражения (словарь в конце), по строкам; в `README.md` каждая строка классифицирована как `text` / `code` (внутри ``` ``` ) / `comment` (внутри `<!-- -->`). Для `.docx` текст извлечён python-docx, для `.pdf` — pdftotext (локатор `путь:pN:lM`). Имена каталогов и файлов просканированы отдельно (`surface=filename`).
2. **Ручной просмотр** всего, что словарь не покрывает: 325 иллюстраций и 44 анимации отрисованы Chromium из SVG (анимации — по 10 моментов времени с `setCurrentTime`), 20 уникальных растров, встроенных в SVG, извлечены и просмотрены отдельно; 344 растровых файла просмотрены (GIF — первый/средний/последний кадр); первая страница каждого PDF отрисована и просмотрена.
3. **Агрегация**: обучающемуся видимые поверхности — строка на каждую строку файла; лабораторная инфраструктура — строка на лабу; `__exams/`, `videos/*.md`, `packet-tracer-source-files/`, `figma-assets.json`, `animations/` и префикс `2001:db8:acad` — строка на файл/каталог (локатор перечисляет строки). Каждое словарное попадание либо входит в строку карты, либо исключено с причиной (таблица сверки ниже).

**Ограничения среды аудита** (учтены в таблице покрытия): Figma API и Figma MCP недоступны — тексты кадров читались с отрисованных SVG (текст в кривых, но читается глазами), лист `_Библиотека` оценён по экспортированным фигурам; `tesseract` недоступен — текст на растрах читался визуально; видео по решению оператора не переразбирались — строки `surface=video` взяты из готового индекса `videos/README.md`.

## Итоги

### По категориям

| category | строк | learner | internal |
|---|---|---|---|
| product | 399 | 315 | 84 |
| brand | 285 | 239 | 46 |
| link | 157 | 115 | 42 |
| lab-infra | 129 | 31 | 98 |
| visual | 112 | 94 | 18 |
| cli-vendor-string | 67 | 67 | 0 |
| model | 44 | 40 | 4 |
| certification | 41 | 15 | 26 |
| legal | 32 | 32 | 0 |
| proprietary-tech | 28 | 28 | 0 |
| marketing | 12 | 12 | 0 |

### По поверхностям

| surface | строк |
|---|---|
| text | 528 |
| quiz | 209 |
| internal-doc | 186 |
| raster | 105 |
| code | 79 |
| lab-infra | 46 |
| comment | 44 |
| video | 36 |
| metadata | 31 |
| illustration | 24 |
| filename | 11 |
| animation | 6 |
| figma-library | 1 |

### По действиям

| action | строк |
|---|---|
| neutralize | 254 |
| replace:NetOS | 194 |
| keep | 180 |
| replace:learn-netsim | 133 |
| remove | 125 |
| decide | 113 |
| replace:example.com | 85 |
| replace:шаблон топологии | 63 |
| replace:NR01/NR02/NS01/NPC | 40 |
| replace:пересборка (Figma Motion / learn-netsim) | 34 |
| replace:class123 | 28 |
| replace:www.example.lab | 19 |
| replace:README | 9 |
| replace:Networking | 6 |
| replace:макет нейтральной веб-страницы | 6 |
| replace:нейтральная веб-страница | 5 |
| replace:lab.local | 3 |
| replace:библиотечный беспроводной роутер | 2 |
| replace:перерисовать | 2 |
| replace:перерисовать без моделей | 1 |
| replace:компонент «окно браузера» с таблицей версий NetOS | 1 |
| replace:фигура «среды передачи» | 1 |
| replace:нейтральное окно файлового менеджера | 1 |
| replace:компонент окна настроек | 1 |

### По модулям (строки, видимые обучающемуся)

| module | строк | главные категории |
|---|---|---|
| (root) | 4 | marketing 1, certification 1, visual 1 |
| 01-03-exam | 22 | product 18, brand 3, visual 1 |
| 01-networking-today | 67 | product 34, visual 8, brand 6 |
| 02-basic-switch-and-end-device-configuration | 221 | product 98, brand 72, model 22 |
| 03-protocols-and-models | 53 | link 17, legal 10, product 7 |
| 04-07-exam | 5 | proprietary-tech 2, visual 2, brand 1 |
| 04-physical-layer | 52 | product 22, brand 13, lab-infra 8 |
| 05-number-systems | 2 | brand 2 |
| 06-data-link-layer | 1 | brand 1 |
| 07-ethernet-switching | 33 | link 8, brand 8, legal 6 |
| 08-10-exam | 17 | brand 9, product 3, visual 3 |
| 08-network-layer | 13 | brand 6, product 3, proprietary-tech 3 |
| 09-address-resolution | 16 | brand 11, visual 3, product 2 |
| 10-basic-router-configuration | 52 | brand 20, product 15, cli-vendor-string 8 |
| 11-13-exam | 5 | visual 4, brand 1 |
| 11-ipv4-addressing | 30 | brand 9, visual 6, legal 4 |
| 12-ipv6-addressing | 32 | brand 10, product 10, visual 5 |
| 13-icmp | 20 | brand 10, visual 4, product 4 |
| 14-15-exam | 4 | proprietary-tech 3, link 1 |
| 14-transport-layer | 13 | visual 6, brand 4, product 2 |
| 15-application-layer | 85 | link 54, cli-vendor-string 19, brand 6 |
| 16-17-exam | 33 | product 14, brand 13, link 4 |
| 16-network-security-fundamentals | 49 | product 19, brand 9, model 6 |
| 17-build-a-small-network | 136 | product 46, brand 19, cli-vendor-string 19 |
| final-exam | 14 | product 5, link 4, visual 3 |
| final-lab | 9 | product 9 |

### Топ-20 самых «вендорных» материалов (строки, видимые обучающемуся)

| # | material | строк | категории |
|---|---|---|---|
| 1 | 02-basic-switch-and-end-device-configuration/02.03.08.02-lab-navigate-the-ios-by-using-tera-term-for-console-connectivity | 48 | brand 19, product 9, model 9 |
| 2 | 15-application-layer/15.04-ip-addressing-services | 45 | link 31, cli-vendor-string 8, legal 3 |
| 3 | 02-basic-switch-and-end-device-configuration/02.03.08.01-lab-navigate-the-ios-using-a-terminal-client-for-console-connectivity-physical-mode | 36 | brand 11, model 11, product 11 |
| 4 | 16-17-exam | 31 | product 14, brand 13, link 4 |
| 5 | 17-build-a-small-network/17.05-host-and-ios-commands | 30 | cli-vendor-string 17, product 7, proprietary-tech 3 |
| 6 | 17-build-a-small-network/17.04-verify-connectivity | 26 | product 16, legal 4, link 4 |
| 7 | 01-networking-today/01.00.05-lab-logical-and-physical-mode-exploration | 25 | product 19, brand 2, cli-vendor-string 1 |
| 8 | 03-protocols-and-models/03.07-data-access | 24 | link 11, legal 8, visual 2 |
| 9 | 04-physical-layer/04.07.01-lab-physical-layer-exploration-physical-mode | 23 | product 20, lab-infra 1, link 1 |
| 10 | 15-application-layer/15.04.08-lab-observe-dns-resolution | 22 | cli-vendor-string 11, link 9, brand 2 |
| 11 | 01-03-exam | 21 | product 18, brand 3 |
| 12 | 02-basic-switch-and-end-device-configuration/02.09.04-quiz | 21 | brand 14, product 7 |
| 13 | 10-basic-router-configuration/10.04.06-quiz | 19 | brand 11, product 8 |
| 14 | 17-build-a-small-network/17.08.05-quiz | 16 | proprietary-tech 7, brand 4, product 4 |
| 15 | 16-network-security-fundamentals/16.04-device-security | 15 | cli-vendor-string 5, brand 4, proprietary-tech 4 |
| 16 | 16-network-security-fundamentals/16.04.07-lab-configure-network-devices-with-ssh | 15 | model 6, brand 4, product 4 |
| 17 | 02-basic-switch-and-end-device-configuration | 14 | product 14 |
| 18 | 02-basic-switch-and-end-device-configuration/02.03-the-command-structure | 14 | product 12, brand 2 |
| 19 | 07-ethernet-switching/07.01-ethernet-frame | 14 | link 7, legal 6, visual 1 |
| 20 | final-exam | 14 | product 5, link 4, visual 3 |

## Решения для оператора (по типам)

1. **Название курса и репозитория («CCNA»).** Репозиторий `learn-ccna1`, код курса `ccna1` в `figma-assets.json` и в 44 каталогах `animations/ccna1-*`, файл `ccna1-labs.md`, каталоги `__exams/CCNA1…3`, фразы «курс CCNA» в тексте (10.3.5, 1.9.3, 3.7.9/3.7.10), доменные имена в заданиях `CCNA.com` / `CCNA-lab.com` (16.4.6, 17.8.2). Идентификаторы пайплайна (`ccna1-…`) завязаны на штампы в Figma — переименовывать дорого; текстовые отсылки к сертификации — дёшево. Предложение: курс и репозиторий переименовать (например, `learn-netfund-1`), id ассетов оставить как непрозрачные ключи, в тексте «курс CCNA» → «этот курс».
2. **«Cisco IOS» как имя операционной системы** — 218 строк в учебных поверхностях (текст, тесты, метаданные, 4 имени каталогов `*-ios-*`). Синтаксис CLI сохраняется (learn-netsim его повторяет). Варианты: (а) «NSALAB NetOS» везде, где речь о нашей ОС; (б) нейтральное «сетевая операционная система / ОС устройства». Отдельно: `IOS XE`, `NX-OS` в 2.1.1 — убрать перечисление линеек Cisco.
3. **Packet Tracer → learn-netsim** — 130 упоминаний в тексте/тестах/метаданных плюс 42 лабораторные работы с PT-инфраструктурой (`.pka`, `deploy/pt-lab/*.tf`, оценка через `validate_web_response` на `{pt-url}:{pt-api-port}`), 63 топологий-скриншотов PT/NetAcad. Девять лаб «Physical Mode» (PTPM: 2.3.8.1, 2.9.2, 4.7.1, 10.4.4, 11.10.2, 12.9.2, 13.3.2, 17.7.7, 17.8.1) опираются на стойки/кабели/города PT — аналога в netsim нет: переписать как логические или снять. 16.4.6 уже переводится (PR #53 открыт). Файлы `.pkt` для «следования за видео» (2.8.1, 2.8.2) и закомментированные ссылки «Скачать файл Packet Tracer» (36 README) — убрать вместе с миграцией.
4. **Модели оборудования** — 44 строк: 2960, 4321/ISR4321, 4221, 1941, 2801, 2811, 1841, ISR4331, Catalyst 2960-24TT, PLEK400/PLE400, Meraki MX64W; версии/образы IOS (`15.0(2)SE`, `c2960-lanbasek9-mz…`, `universalk9`, `16.9.3`). Сверка с идентичностью learn-netsim: маршрутизаторы → **NR01/NR02**, коммутатор → **NS01**, ПК → **NPC**; нужно утвердить имена интерфейсов моделей (сейчас в тексте смесь `G0/0/0` ISR4221/4321 и `G0/0` 1941) и таблицы «модель → интерфейсы» в 2.3.8.2 и 16.4.7.
5. **Вендорные строки в выводах CLI** — 67 строк `code`: `Cisco IOS Software, C2960 Software…`, `Copyright (c) … by Cisco Systems`, `cisco ISR4321/K9 … processor`, `Technical Support: http://www.cisco.com/techsupport`, `WS-C2960+`, `IP CEF`, `C:\Users\NetAcad>`, `dns-sj.cisco.com`. Все уходят при перегенерации выводов на learn-netsim — это задача netsim (`show version`, `show cdp/lldp neighbors`, `show ip interface`, `nslookup`), а не правки текста.
6. **Проприетарные протоколы.** CDP — 16 строк (17.5.6, итоги 17.9, тест 17.8.5, экзамен 16-17): заменить на **LLDP** (802.1AB) как учебную тему — команды `show lldp neighbors` аналогичны. EIGRP — 14 строк (3.3.3 список протоколов «разработан Cisco», 8.5.3/8.6 легенда `D - EIGRP` в `show ip route`, 11.7.5 сценарий лабы, тест 3.3.6): оставить как пример протокола маршрутизации без слов о Cisco или убрать из списков. `auto secure` (16.4.1, 16.6) — функция IOS, убрать. HSRP/GLBP/EtherChannel/PAgP/DTP/PVST/ISL встречаются только в `__exams` (CCNA2/3) и экзамене 14-15 (HSRP в комментарии к портам).
7. **Учётные данные и имена в заданиях с брендом** — 28 строк: пароли `cisco`, `Cisco123`, `Ciscoenpa55`, `Ciscoconpa55`; серверы `netacad.pka`, `www.cisco.pka`, `www.cisco6.pka`; домены `CCNA.com`, `CCNA-lab.com`; hostname `CiscoVille` (в `__exams`). Ввести единый нейтральный набор (например, пароль `class123`, домен `lab.local`, сервер `www.example.lab`) и синхронно обновить критерии оценки `assessment/ms.yaml`.
8. **cisco.com / netacad.com как учебные примеры** — 127 строк с `cisco.com` (DNS, URL, nslookup, ping, tracert, WHOIS; 15.3, 15.4, 17.7, лабы 3.7.10/7.1.6/15.4.8, тесты) и 60 с `netacad.com` (в основном подвалы PDF). Заменить на `example.com` / собственный домен, реальный адрес `198.133.219.25` → документационный `203.0.113.x`; переснять выводы.
9. **Маркетинг и имидж NetAcad.** Раздел 1.1.2 (слоган академии + промо-ролик `wcIP__5sa1o`), 1.7.3–1.7.5 (Webex, промо `e85Y71fsyyY`, скриншот 1.7.3) и повтор в 1.10, абзац «Студенты обычно используют Packet Tracer…» (1.0.3), «политика академии» (3.7.9), материал 1.9 / лаба 1.9.3 («Сертификация Cisco CCNA — система сертификации начального уровня…»). Скриншоты cisco.com со слоганом «Trust means you're ready for anything» — в 5 анимациях (3.3.5-1, 3.3.5-2, 3.6.4, 3.6.5, 4.1.2) и 6 иллюстрациях (14.1.2-1…-5, 15.3.1-4): один растр, заменить одним компонентом «окно браузера».
10. **Видео** — 36 роликов NetAcad (перезалив), 2 класса `marketing` → убрать; остальные уже в плане пересборки (5 из 36 готовы). Не переразбирались (решение оператора); в кадрах финальная заставка с логотипом Cisco отмечена в разборах для 5 роликов.
11. **Юридические метки** — 32 строки `legal`: подвалы «© … Корпорация Cisco… Все права защищены» в 9 PDF-описаниях лаб (плюс шапка «Cisco Networking Academy» на каждой странице), `Copyright (c) … Cisco Systems` в выводах CLI, `© 2021 Cisco … Cisco Confidential` в `readme-assets/itn-v7.02-scope-and-sequence.pdf`. PDF-лабы перенести в README (как остальные) и удалить файлы; scope-and-sequence удалить.
12. **Библиотека иконок Figma (`_Библиотека`)** — одна строка `decide`: силуэты устройств (маршрутизатор-«шайба» со стрелками, коммутатор-брусок, многоуровневый коммутатор-куб со звездой, межсетевой экран-стена) повторяют иконографию Cisco, хотя отрисованы собственной изометрией и палитрой без логотипов. Это де-факто отраслевой язык схем; решение — оставить или изменить силуэты — одно на всю библиотеку (369 фигур).
13. **Метаданные и имена.** Тег `"Cisco"` в `material-tags.json` (ставится всем материалам) и `final-itn/test.json`; 8 каталогов с `cisco-ios` / `-ios-` в имени (меняют `$ref` и внешние ссылки — переименовывать одним проходом); имена страниц Figma `CCNA1 · NN …` и `course: "ccna1"` в `figma-assets.json`.
14. **Гигиена репозитория.** `__exams/` (24 каталога/файла: копии экзаменов CCNA1 с расхождениями + экзамены CCNA2/CCNA3, 17 `.pka`, 182 изображения в стиле NetAcad, `CiscoVille`, `netacad.net`) не подключён к курсу — убрать или вынести в архив; `packet-tracer-source-files/` (41 `.docx` с «Packet Tracer» в именах и © Cisco) — удалить после миграции; `readme-assets/*.png` (17 скриншотов NetAcad/PT к инструкции по миграции) и сама `migration-instructions.md` — решить, нужна ли инструкция в репозитории курса; `final-itn/test.json` — не подключён.
15. **Префикс `2001:db8:acad::/48`** — конвенция NetAcad («acad»), 23 файлов (295 вхождений, модули 9–13, 17, лабы, оценочные `ms.yaml`). Заменить на другой документационный префикс одним проходом (вместе с `ms.yaml`) или признать нейтральным.
16. **Вне вендора, но замечено:** фото Linksys (4.1.1-1/-2, 1.2.5-6 — бренд Cisco-эпохи, решить вместе с семьёй фигур по `raster-inventory`), логотипы IEEE/IETF/ITU/RIR (3.4.1, 3.4.2-1, 6.1.4, 11.3.6, 12.1.1), скриншоты Windows/PuTTY/Wireshark/Telegram/Gmail внутри фигур — чужие UI, не Cisco; тема другого аудита.

## Покрытие

| тип файла | всего | просмотрено | пропущено / частично | как |
|---|---|---|---|---|
| .tf | 642 | 642 | 0 | словарь построчно (lab-infra) |
| .json | 412 | 412 | 0 | словарь построчно (quiz/metadata) |
| .svg | 369 | 369 | 0 | рендер Chromium + просмотр (325 статичных, 44 анимации × 10 моментов); 685 встроенных растров → 20 уникальных просмотрены |
| .png | 249 | 249 | 0 | просмотр глазами (OCR недоступен) |
| .md | 226 | 226 | 0 | словарь построчно (text/code/comment) |
| .sh | 128 | 128 | 0 | словарь построчно |
| .yaml | 126 | 126 | 0 | словарь построчно (lab-infra) |
| .jpg | 67 | 67 | 0 | просмотр |
| .pka | 58 | 58 | частично: 58 | бинарный файл PT — не открывался; учтён строкой lab-infra лабы/экзамена |
| .tpl | 44 | 44 | 0 | словарь построчно |
| .docx | 44 | 44 | частично: 44 | текст извлечён и просканирован; изображения внутри .docx не просматривались |
| .gif | 27 | 27 | 0 | просмотр (кадры 1 / середина / последний) |
| .pdf | 10 | 10 | частично: 10 | текст извлечён и просканирован; визуально — 1-я страница каждого (логотипы/подвалы), остальные страницы только текстом |
| .py | 2 | 2 | 0 | словарь построчно |
| .pkt | 2 | 2 | частично: 2 | бинарный файл PT — не открывался; строка lab-infra + filename |
| .yml | 1 | 1 | 0 | словарь построчно |
| .gitignore | 1 | 1 | 0 | словарь построчно |
| .jpeg | 1 | 1 | 0 | просмотр |
| .txt | 1 | 1 | 0 | словарь построчно |

| figma-assets.json · kind | всего | просмотрено | как |
|---|---|---|---|
| illustration | 325 | 325 | рендер SVG → контактные листы 2×2; текст подписей читался с рендера |
| animation | 44 | 44 | 10 моментов времени на анимацию (SMIL setCurrentTime), листы 5×2 |
| native | 74 | 74 | просмотр + сверка с design/raster-inventory-ccna1.md |

| видео | всего | просмотрено | как |
|---|---|---|---|
| встроенные YouTube-ролики | 36 | 36 (по индексу) | по решению оператора не переразбирались; класс/канал/логотип — из videos/README.md и разборов videos/*.md |

| Figma | всего | просмотрено | как |
|---|---|---|---|
| лист _Библиотека (3FtCg22qFubpLBPOetQU03) | 1 | 0 напрямую | API/MCP Figma недоступны в среде аудита; вердикт по 369 экспортированным фигурам (одна строка decide) |

Итого `git ls-files`: 2410 файлов, каждый либо просканирован словарём, либо просмотрен, либо учтён как бинарный артефакт PT (строка на лабу/экзамен). Частичное покрытие: изображения внутри 44 `.docx` и страницы 2+ десяти PDF просмотрены только текстом.

## Сверка полноты по словарю (N = M + K)

| термин | найдено N | внесено M | исключено K | строк карты | причины исключения |
|---|---|---|---|---|---|
| `cisco` | 1397 | 1397 | 0 | 577 |  |
| `сиско/циско` | 6 | 0 | 6 | 0 | ложное совпадение: «Сан-Франциско» ×6 |
| `netacad` | 105 | 105 | 0 | 59 |  |
| `networking academy` | 77 | 77 | 0 | 46 |  |
| `сетевая академия` | 1 | 1 | 0 | 1 |  |
| `академи` | 6 | 6 | 0 | 4 |  |
| `skills for all` | 3 | 3 | 0 | 3 |  |
| `learning network` | 0 | 0 | 0 | 0 |  |
| `talos` | 0 | 0 | 0 | 0 |  |
| `ccna` | 1206 | 1206 | 0 | 108 |  |
| `ccnp` | 2 | 2 | 0 | 2 |  |
| `ccent` | 0 | 0 | 0 | 0 |  |
| `ccie` | 0 | 0 | 0 | 0 |  |
| `cyberops` | 0 | 0 | 0 | 0 |  |
| `itn` | 59 | 59 | 0 | 44 |  |
| `srwe` | 3 | 3 | 0 | 3 |  |
| `ensa` | 2 | 2 | 0 | 2 |  |
| `v7` | 5 | 5 | 0 | 5 |  |
| `scope and sequence` | 11 | 11 | 0 | 3 |  |
| `сертификаци` | 14 | 12 | 2 | 9 | «сертифицированный» (продукция TIA / Wi-Fi Alliance) — не сертификация вендора ×2 |
| `packet tracer` | 1210 | 1210 | 0 | 209 |  |
| `PT` | 372 | 372 | 0 | 134 |  |
| `PTSA/PTPM` | 24 | 24 | 0 | 12 |  |
| `.pka` | 245 | 245 | 0 | 125 |  |
| `.pkt` | 8 | 8 | 0 | 7 |  |
| `webex` | 22 | 22 | 0 | 9 |  |
| `meraki` | 1 | 1 | 0 | 1 |  |
| `catalyst` | 19 | 19 | 0 | 16 |  |
| `ISR` | 28 | 28 | 0 | 11 |  |
| `nexus` | 12 | 12 | 0 | 2 |  |
| `ASA` | 12 | 12 | 0 | 4 |  |
| `anyconnect` | 0 | 0 | 0 | 0 |  |
| `dna center` | 0 | 0 | 0 | 0 |  |
| `IOS` | 548 | 547 | 1 | 269 | Apple iOS (мобильная ОС), не Cisco IOS ×1 |
| `IOS XE` | 30 | 30 | 0 | 12 |  |
| `NX-OS` | 1 | 1 | 0 | 1 |  |
| `umbrella` | 0 | 0 | 0 | 0 |  |
| `linksys` | 0 | 0 | 0 | 0 |  |
| `aironet` | 0 | 0 | 0 | 0 |  |
| `firepower` | 0 | 0 | 0 | 0 |  |
| `ios-image` | 58 | 58 | 0 | 22 |  |
| `model-number` | 259 | 254 | 5 | 60 | число 1812 — порт RADIUS, не модель маршрутизатора ×4; фрагмент IPv6-адреса, не модель ×1 |
| `WS-C` | 9 | 9 | 0 | 6 |  |
| `ios-version` | 34 | 34 | 0 | 25 |  |
| `PLE400` | 1 | 1 | 0 | 1 |  |
| `MX64W` | 1 | 1 | 0 | 1 |  |
| `series` | 42 | 42 | 0 | 2 |  |
| `copyright` | 21 | 21 | 0 | 8 |  |
| `©` | 81 | 81 | 0 | 40 |  |
| `®` | 2 | 2 | 0 | 1 |  |
| `™` | 1 | 1 | 0 | 1 |  |
| `товарн` | 0 | 0 | 0 | 0 |  |
| `trademark` | 1 | 1 | 0 | 1 |  |
| `CDP` | 43 | 43 | 0 | 19 |  |
| `EIGRP` | 33 | 33 | 0 | 16 |  |
| `HSRP` | 34 | 34 | 0 | 7 |  |
| `GLBP` | 32 | 32 | 0 | 2 |  |
| `VTP` | 3 | 3 | 0 | 2 |  |
| `DTP` | 34 | 34 | 0 | 4 |  |
| `ISL` | 1 | 1 | 0 | 1 |  |
| `PVST` | 33 | 33 | 0 | 4 |  |
| `SD-Access` | 0 | 0 | 0 | 0 |  |
| `LWAPP` | 0 | 0 | 0 | 0 |  |
| `PAgP` | 74 | 74 | 0 | 1 |  |
| `EtherChannel` | 269 | 269 | 0 | 5 |  |
| `NetFlow` | 0 | 0 | 0 | 0 |  |
| `CEF` | 21 | 21 | 0 | 12 |  |
| `PortFast` | 28 | 28 | 0 | 5 |  |
| `BPDU Guard` | 22 | 22 | 0 | 2 |  |
| `IGRP` | 0 | 0 | 0 | 0 |  |
| `IP SLA` | 0 | 0 | 0 | 0 |  |
| `DMVPN` | 16 | 16 | 0 | 2 |  |
| `AutoSecure` | 5 | 5 | 0 | 5 |  |
| `cisco.com` | 132 | 132 | 0 | 105 |  |
| `netacad.com` | 60 | 60 | 0 | 42 |  |
| `youtube` | 109 | 108 | 1 | 108 | пример синтаксиса встраивания в инструкции по миграции, не ролик ×1 |
| `pt-lab` | 2990 | 2990 | 0 | 43 |  |
| `db8:acad` | 295 | 295 | 0 | 26 |  |
| `ACAD_` | 4 | 4 | 0 | 1 |  |
| `opendns` | 2 | 2 | 0 | 2 |  |
| `telepresence` | 1 | 1 | 0 | 1 |  |
| `ESA/WSA` | 14 | 14 | 0 | 6 |  |
| `ACI/APIC` | 24 | 24 | 0 | 2 |  |
| `ASDM` | 4 | 4 | 0 | 1 |  |

Всего попаданий N = 10222, внесено M = 10207, исключено K = 15; N = M + K выполняется по каждому термину. «Строк карты» меньше M там, где попадания агрегированы (лаба, экзамен, служебный файл) или несколько терминов стоят в одной строке. Не вошли в словарь-регэксп, но проверены вручную по всем файлам и дали 0 совпадений: `talos`, `umbrella`, `linksys` (только на фото), `cisco live`, `devnet`, `snort`, `jabber`, `anyconnect`, `dna center`.

### Итоговый словарь

| термин | регулярное выражение | категория по умолчанию | из словаря задачи |
|---|---|---|---|
| `cisco` | `cisco` | brand | да |
| `сиско/циско` | `сиско\|циско` | brand | да |
| `netacad` | `netacad` | brand | да |
| `networking academy` | `networking\s+academy` | brand | да |
| `сетевая академия` | `сетев\w*\s+академи\w*` | brand | да |
| `академи` | `академи\w*` | brand | да |
| `skills for all` | `skills\s*for\s*all\|skillsforall` | brand | добавлен |
| `learning network` | `learning\s*network` | brand | добавлен |
| `talos` | `\btalos\b` | brand | добавлен |
| `ccna` | `ccna` | certification | да |
| `ccnp` | `ccnp` | certification | да |
| `ccent` | `ccent` | certification | да |
| `ccie` | `ccie` | certification | добавлен |
| `cyberops` | `cyberops` | certification | добавлен |
| `itn` | `\bitn\b` | certification | да |
| `srwe` | `\bsrwe\b` | certification | да |
| `ensa` | `\bensa\b` | certification | да |
| `v7` | `\bv7(?:\.0\d)?\b` | certification | да |
| `scope and sequence` | `scope\s*(?:and\|&)\s*sequence` | certification | добавлен |
| `сертификаци` | `сертификаци\w*\|сертифицир\w*` | certification | добавлен |
| `packet tracer` | `packet\s*tracer\|packettracer` | product | да |
| `PT` | `\bPT\b` | product | да |
| `PTSA/PTPM` | `\bPT(?:SA\|PM)\b` | lab-infra | добавлен |
| `.pka` | `\.pka\b` | lab-infra | да |
| `.pkt` | `\.pkt\b` | lab-infra | да |
| `webex` | `webex` | product | да |
| `meraki` | `meraki` | product | да |
| `catalyst` | `catalyst` | product | да |
| `ISR` | `\bISR\b` | product | да |
| `nexus` | `\bnexus\b` | product | да |
| `ASA` | `\bASA\b` | product | да |
| `anyconnect` | `anyconnect` | product | да |
| `dna center` | `dna\s*cent(?:er\|re)` | product | да |
| `IOS` | `\bIOS\b(?![\s-]*XE)` | product | да |
| `IOS XE` | `\bIOS[\s-]*XE\b` | product | да |
| `NX-OS` | `\bNX-?OS\b` | product | да |
| `umbrella` | `\bumbrella\b` | product | добавлен |
| `linksys` | `linksys` | product | добавлен |
| `aironet` | `aironet` | product | добавлен |
| `firepower` | `firepower` | product | добавлен |
| `ios-image` | `\b[ci]\d{4}\S*k9\S*\|universalk9\|lanbasek9\|lanbase\|ipbasek9\|ipservicesk9\|\bmz\.\d{3}-` | model | добавлен |
| `model-number` | `\b(?:1941\|2901\|2911\|2951\|2960\|3560\|3650\|3750\|4221\|4321\|4331\|4451\|1841\|2811\|1921\|9200\|9300\|3850\|1801\|1811\|1812\|1861\|2801\|2821\|2851\|3825\|3845\|881\|887\|891)\b` | model | да |
| `WS-C` | `WS-C\S*` | model | да |
| `ios-version` | `\b1[25]\.\d\(\d+[a-z]?\)[A-Za-z0-9]*\|\b12\.2\.\d+-SE\d*\|\b15\.0\.2-SE\d*\|(?<=XE )(?:Release \|Version \|версии )?16\.\d{1,2}\.\d{1,2}\|(?<=XE версии )16\.\d{1,2}\.\d{1,2}\|(?<=Version )16\.\d{2}\.\d{2}` | model | добавлен |
| `PLE400` | `PLEK?400` | model | добавлен |
| `MX64W` | `MX64W?` | model | добавлен |
| `series` | `\b(?:1900\|2900\|4000\|800\|1800\|3800\|4300\|2800\|4400\|3900)\s*(?:series\|серии)\b` | model | добавлен |
| `copyright` | `copyright\|all rights reserved` | legal | да |
| `©` | `©\|\(c\)\s*(?:19\|20)\d\d` | legal | да |
| `®` | `®` | legal | да |
| `™` | `™` | legal | да |
| `товарн` | `товарн\w*` | legal | да |
| `trademark` | `trademark` | legal | добавлен |
| `CDP` | `\bCDP\b` | proprietary-tech | да |
| `EIGRP` | `EIGRP` | proprietary-tech | да |
| `HSRP` | `HSRP` | proprietary-tech | да |
| `GLBP` | `GLBP` | proprietary-tech | да |
| `VTP` | `\bVTP\b` | proprietary-tech | да |
| `DTP` | `\bDTP\b` | proprietary-tech | да |
| `ISL` | `\bISL\b` | proprietary-tech | да |
| `PVST` | `PVST` | proprietary-tech | да |
| `SD-Access` | `SD-Access` | proprietary-tech | добавлен |
| `LWAPP` | `LWAPP` | proprietary-tech | добавлен |
| `PAgP` | `\bPAgP\b` | proprietary-tech | добавлен |
| `EtherChannel` | `etherchannel` | proprietary-tech | добавлен |
| `NetFlow` | `netflow` | proprietary-tech | добавлен |
| `CEF` | `\bCEF\b\|cisco express forwarding` | proprietary-tech | добавлен |
| `PortFast` | `portfast` | proprietary-tech | добавлен |
| `BPDU Guard` | `bpdu\s*guard` | proprietary-tech | добавлен |
| `IGRP` | `\bIGRP\b` | proprietary-tech | добавлен |
| `IP SLA` | `\bIP\s+SLA\b` | proprietary-tech | добавлен |
| `DMVPN` | `DMVPN` | proprietary-tech | добавлен |
| `AutoSecure` | `autosecure\|auto\s+secure` | proprietary-tech | добавлен |
| `cisco.com` | `[\w.-]*cisco\.com` | link | да |
| `netacad.com` | `netacad\.com` | link | добавлен |
| `youtube` | `youtube\.com/watch\?v=[\w-]+\|youtu\.be/[\w-]+` | link | добавлен |
| `pt-lab` | `pt-lab\|pt_lab\|pt-url\|pt-api\|validate_web_response\|packettracer\.exe` | lab-infra | добавлен |
| `db8:acad` | `db8:acad` | brand | добавлен |
| `ACAD_` | `\bACAD_[A-Z]+` | brand | добавлен |
| `opendns` | `opendns` | product | добавлен |
| `telepresence` | `telepresence` | product | добавлен |
| `ESA/WSA` | `\bESA\b\|\bWSA\b` | product | добавлен |
| `ACI/APIC` | `\bACI\b\|\bAPIC\b` | product | добавлен |
| `ASDM` | `\bASDM\b` | product | добавлен |

## Замеченные опечатки (в материалах не правились)

- заголовки лаб 17.07.06 и 17.07.07 в `learn-metadata.json`: «(логиеский режим)» — у 17.07.07 к тому же должно быть «физический режим»;
- каталоги `12.05-dynamic-addresing-for-ipv6-guas`, `12.06-dynamic-addresing-for-ipv6-llas` — `addresing`;
- `calc_duration.txt`: «avarage».

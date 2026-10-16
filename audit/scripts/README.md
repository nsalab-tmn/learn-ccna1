# Скрипты аудита упоминаний вендора

Этими скриптами построены [`vendor-mentions.csv`](../vendor-mentions.csv), [`vendor-mentions.md`](../vendor-mentions.md) и [`de-vendoring-plan.md`](../de-vendoring-plan.md) (issue nsalab-tmn/learn-ccna1#54). Обучающемуся они не показываются.

## Проверить пакет работ (основной сценарий)

После правки материалов по пакету из плана прогоните словарный сканер по изменённым путям:

```bash
python3 audit/scripts/scan.py 15-application-layer/15.04.08-lab-observe-dns-resolution 13-icmp/13.03.04-quiz
```

Скрипт печатает число попаданий по каждому термину словаря и по поверхностям (`text` / `code` / `comment` / `quiz` …). Пакет закрыт, когда по его терминам попаданий ноль. Подробности по каждому попаданию (файл, строка, контекст) — в `$AUDIT_WORK/text/hits.jsonl`.

Каталог `audit/` сканер не читает никогда: он сам цитирует все термины.

## Что здесь лежит

| Файл | Что делает | Вход | Выход |
|---|---|---|---|
| `scan.py` | словарный проход по `git ls-files` (строки `*.md`/`*.json`/…, абзацы `.docx`, строки `.pdf`, имена файлов и каталогов) | репозиторий | `$AUDIT_WORK/text/hits.jsonl`, `files.jsonl` |
| `build.py` | группирует попадания в строки карты, добавляет лабораторную инфраструктуру, видео и результаты ручного просмотра фигур, присваивает id, сверяет N = M + K | вывод `scan.py`, `videos.tsv`, `figma-assets.json` | `audit/vendor-mentions.csv` (11 столбцов), `$AUDIT_WORK/rows.json`, `recon.json` |
| `summary.py` | сводка | `rows.json`, `recon.json` | `audit/vendor-mentions.md` |
| `tier.py` | уровень P1/P2/P3 и пакет работ для каждой строки; учебные поверхности — в плане, остальное — пусто с пояснением | `audit/vendor-mentions.csv`, статус лаб в репозитории | столбцы `tier`, `batch`, `tier_note` в том же CSV; `$AUDIT_WORK/tier_stats.json`, `tier_dump.txt` |
| `plan.py` | план де-вендоризации | CSV со столбцами уровней | `audit/de-vendoring-plan.md` |
| `videos.tsv` | ручная классификация 36 роликов (id, название, класс, статус в Figma) | — | вход `build.py` |
| `render_svgs.js` | отрисовка всех SVG в PNG (анимации — 10 моментов времени) для ручного просмотра | SVG | PNG в указанный каталог |
| `extract_embedded.py` | извлечение растров, встроенных в SVG, без дублей (sha1) | SVG | файлы и `index.json` в указанный каталог |
| `prep_rasters.sh` | растры → PNG шириной до 1200 px, GIF → полоса из трёх кадров | PNG/JPG/GIF | PNG в указанный каталог |

## Полная пересборка

```bash
python3 audit/scripts/scan.py
python3 audit/scripts/build.py
python3 audit/scripts/summary.py
python3 audit/scripts/tier.py
python3 audit/scripts/plan.py
```

Перед пересборкой учтите:

- **Id строк перенумеруются.** `build.py` перезаписывает CSV целиком, поэтому ссылки вида `ccna1-vm-0421` из PR и комментариев перестанут совпадать. Во время работы по плану пересобирать карту не нужно — для проверки хватает `scan.py` по путям.
- **Ручной просмотр фигур не пересчитывается.** Списки `VIS`, `RAS`, `PT_TOPO`, `NETACAD_FIG` и описания иллюстраций в `build.py`, классификация видео в `videos.tsv`, рецепты замен и тексты пакетов в `plan.py` записаны для среза, на котором делался аудит. Пересчитываются счётчики, таблицы, локаторы и всё, что идёт из словарного прохода. После перерисовки фигур эти списки нужно править руками.
- **Срез в тексте** (`Срез: … @ <commit>`) берётся из `git rev-parse HEAD` репозитория, на котором запущен скрипт.

## Окружение

| Переменная | По умолчанию | Назначение |
|---|---|---|
| `AUDIT_REPO` | корень репозитория (два уровня выше скриптов) | какой checkout сканировать и куда писать `audit/` |
| `AUDIT_WORK` | `$TMPDIR/vendor-audit` | промежуточные файлы |
| `PLAYWRIGHT_MODULE` | `playwright` | путь к модулю, если `require('playwright')` не находит его |

Нужны `python3` и `git`; для полного прохода — `pdftotext` (poppler-utils) и `python-docx`; для визуальных помощников — Node.js с Playwright/Chromium и ImageMagick.

## Воспроизводимость

Проверено пересборкой на отдельных checkout-ах:

- `scan.py` + `build.py` на `d7897dd` (срез аудита) дают 10 222 попадания, 1306 строк и побайтно тот же `vendor-mentions.csv`, что вошёл в #55; `summary.py` там же даёт `vendor-mentions.md` побайтно как в #59 (от версии #55 отличается одним абзацем со ссылками на план и скрипты);
- `tier.py` + `plan.py` на `dc13ed1` (лаба 16.4.6 уже на learn-netsim) поверх CSV из #55 дают побайтно те же CSV со столбцами уровней и `de-vendoring-plan.md`, что вошли в #59.

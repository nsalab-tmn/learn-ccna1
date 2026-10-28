# 02.03 Структура команд ОС — самопроверка, персона S

```json
[
  {
    "q": "1",
    "answer": ["А"],
    "source": "текст, раздел «Проверка синтаксиса команд ОС», таблица условных обозначений",
    "quote": "В квадратных скобках отображаются дополнительные элементы (ключевое слово или аргумент) … В фигурных скобках отображаются обязательные элементы",
    "class": "понимание",
    "why": "Команды show interfaces в материале нет; нужно перенести правило о квадратных скобках (дополнительный, в отличие от обязательного в фигурных) на новый пример и понять, что дополнительный элемент можно и указать, и опустить, а сами скобки не вводятся."
  },
  {
    "q": "2",
    "answer": ["А"],
    "source": "текст, раздел «Контекстная справка и проверка синтаксиса команд», п. 2; анимация 1 кадр 24 (ШАГ 3)",
    "quote": "Начало команды и ? без пробела, например in?, выводят команды, которые начинаются с этих символов (interface). Набранное остается в строке, и команду можно дописать.",
    "class": "понимание",
    "why": "В тексте пример in?, а не di?; надо перенести приём на другие буквы и отбросить Tab, который по разделу «Горячие клавиши и сокращения команд» п. 2 ничего не дописывает, если с этих символов начинается несколько команд."
  },
  {
    "q": "3",
    "answer": ["Б"],
    "source": "текст, раздел «Горячие клавиши и клавиши быстрого вызова», таблица для приглашения --More--",
    "quote": "Клавиша Enter | Показывает следующую строку … Пробел | Показывает следующий экран",
    "class": "узнавание слова",
    "why": "Ответ — строка таблицы: «по одной строке» в вопросе почти дословно повторяет описание Enter («следующую строку»); понимать механизм не нужно, достаточно вспомнить, что Enter = строка, Пробел = экран."
  },
  {
    "q": "4",
    "answer": ["В"],
    "source": "текст, раздел «Проверка синтаксиса команд ОС»",
    "quote": "Курсивом выделены аргументы, для которых пользователь указывает значение. … ping IP-address — команда ping, а пользовательский аргумент — это IP-адрес целевого устройства.",
    "class": "узнавание слова",
    "why": "Пример ping IP-address взят из текста целиком, а вариант В почти дословно повторяет фразу о курсиве; достаточно вспомнить соответствие «курсив = аргумент»."
  },
  {
    "q": "5",
    "answer": ["Г"],
    "source": "текст, раздел «Горячие клавиши и клавиши быстрого вызова»; анимация 1 кадр 13 (список команд по ?: show, ssh)",
    "quote": "Команды и ключевые слова можно сокращать до минимального количества символов, которые однозначно идентифицируют выбранную команду или слово. … Сокращение con использовать нельзя, так как с символов con начинается несколько команд.",
    "class": "понимание",
    "why": "В тексте примеры conf/con, а не sh/s; нужно применить правило однозначности к новой паре и отвергнуть выдуманные ограничения (три символа, только первое слово, только привилегированный режим) — текст прямо говорит, что ключевые слова тоже сокращают; что с s начинается не только show, видно по списку команд в анимации 1 кадр 13 (show, ssh)."
  },
  {
    "q": "6",
    "answer": ["Б"],
    "source": "текст, раздел «Контекстная справка и проверка синтаксиса команд», п. 6; анимация 1 кадр 45 (ШАГ 7)",
    "quote": "Команда interface без ключевых слов и аргументов неполная: % Incomplete command. Команда interface ? подсказывает, что ввести дальше.",
    "class": "понимание",
    "why": "Надо различить три сообщения об ошибках (Ambiguous — мало символов, Invalid input — маркер ^, Incomplete — не хватает ключевых слов или аргументов) и обобщить пример interface ? до правила «команда, пробел и ?» из п. 3."
  },
  {
    "q": "7",
    "answer": ["В"],
    "source": "текст, раздел «Горячие клавиши и сокращения команд», п. 7; таблица выхода из режима в разделе «Горячие клавиши и клавиши быстрого вызова»; анимация 2 кадр 59",
    "quote": "Ctrl+Shift+6 — универсальная последовательность прерывания: она останавливает ping к узлу, который не отвечает, и возвращает приглашение S1#.",
    "class": "узнавание слова",
    "why": "Формулировка вопроса («ping к узлу, который не отвечает») дословно совпадает с п. 7; достаточно узнать сочетание Ctrl+Shift+6 рядом со словом ping. Отвлекающий вариант Б («Ctrl-C, как в большинстве программ») рассчитан на привычку из других командных строк, которой у персоны нет (командную строку она до курса не знала), а в тексте Ctrl-C — выход из режима конфигурации."
  }
]
```

## 2. Самопроверка ↔ лекция

**Нельзя ответить из материала и блокнота:** таких вопросов нет. Все семь вопросов закрываются текстом material.md (разделы «Проверка синтаксиса команд ОС», «Контекстная справка и проверка синтаксиса команд», «Горячие клавиши и клавиши быстрого вызова», «Горячие клавиши и сокращения команд») и кадрами анимаций 1 и 2. Из блокнота нужны только названия режимов и вид приглашений (N-02.02-05, N-02.02-07, N-02.02-09), чтобы понять «привилегированный режим EXEC» в вопросе 2.

**Проверяют только узнавание слова:** вопросы 3, 4, 7.
- Вопрос 3 — строка таблицы --More--: «по одной строке» ≈ «показывает следующую строку» (Enter).
- Вопрос 4 — пример ping IP-address и фраза «аргумент, для которого пользователь указывает значение» взяты из текста почти дословно.
- Вопрос 7 — формулировка п. 7 («останавливает ping к узлу, который не отвечает») повторена в вопросе; достаточно узнать Ctrl+Shift+6 рядом со словом ping.

**Требуют понимания объяснённого (перенос на новый пример):** вопросы 1, 2, 5, 6.
- Вопрос 1 — правило о квадратных скобках нужно применить к команде show interfaces, которой в материале нет.
- Вопрос 2 — приём «начало команды и ? без пробела» показан на in?, нужно перенести на di? и отличить от Tab.
- Вопрос 5 — правило однозначного сокращения показано на conf/con, нужно перенести на sh/s и отвергнуть выдуманные ограничения.
- Вопрос 6 — нужно различить три сообщения об ошибках и обобщить interface ? до «команда, пробел и ?».

**Требуют того, чего не объясняли:** строго таких вопросов нет. Оговорки:
- Вопрос 5: текст не говорит прямо, что с буквы s начинается несколько команд, а sh однозначно даёт show; это выводится из правила однозначности и из списка команд по ? в анимации 1 кадр 13 (show и ssh). Команда show running-config и сокращение run в материале не встречаются, но для ответа они не нужны — текст говорит, что ключевые слова тоже сокращаются.
- Вопросы 1 и 3 упоминают команды show interfaces и show running-config, которых в материале нет; для ответа достаточно условных обозначений и таблицы --More--.
- Вопрос 7, вариант Б, апеллирует к привычке «Ctrl-C как в большинстве программ» — это внешнее знание, которого у персоны нет; для неё этот вариант просто не подкреплён текстом.

## Открытые файлы

- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/task02/02.03-the-command-structure-S.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/persona.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/notebook.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/material.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/selfcheck.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/fig-01.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-1.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-2.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-3.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-4.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-5.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-6.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-7.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-8.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-9.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-10.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-11.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-01-sheet-12.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-1.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-2.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-3.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-4.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-5.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-6.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-7.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-8.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-9.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-10.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-11.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-12.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-13.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-14.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-15.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.03-the-command-structure/S/anim-02-sheet-16.png

Отдельные кадры в папке frames/ не открывались: все кадры обеих анимаций просмотрены по листам кадров.

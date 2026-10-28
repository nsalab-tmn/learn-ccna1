# 02.02-ios-navigation · персона S · самопроверка

```json
[
  {
    "q": "1",
    "answer": ["А", "Б"],
    "source": "текст, раздел «Переключение между режимами ОС»; подтверждение — анимация 2 кадр 80 (на схеме стрелка «end · Ctrl+Z» от вложенных режимов сразу к S1#)",
    "quote": "Чтобы перейти из любого вложенного режима в привилегированный, введите команду end или используйте сочетание клавиш Ctrl+Z.",
    "class": "понимание",
    "why": "Надо отличить end/Ctrl+Z (сразу в привилегированный) от exit (только на один уровень вверх, в (config)#) и от disable (из привилегированного в пользовательский) — иначе вариант Г выглядит правдоподобно."
  },
  {
    "q": "2",
    "answer": ["А"],
    "source": "текст, раздел «Переключение между режимами ОС» + таблица в разделе «Основные командные режимы»; анимация 2 кадр 17 (S1#disable → S1>)",
    "quote": "Чтобы вернуться в пользовательский режим EXEC, используйте команду disable.",
    "class": "понимание",
    "why": "Режим в вопросе не назван: нужно по описанию («только базовые команды мониторинга, изменить конфигурацию нельзя») узнать пользовательский режим EXEC, а потом вспомнить, какая команда в него возвращает из «#»."
  },
  {
    "q": "3",
    "answer": ["Б"],
    "source": "текст, раздел «Основные командные режимы» (таблица, строка «Привилегированный режим EXEC»)",
    "quote": "Пользователь может использовать любые команды мониторинга, а также имеет доступ ко всем конфигурациям и командам управления.",
    "class": "понимание",
    "why": "Нужно по «#» без (config) узнать привилегированный режим EXEC и не спутать его с режимом глобальной конфигурации (В) и режимом настройки интерфейса (Г), которые тоже оканчиваются на «#»."
  },
  {
    "q": "4",
    "answer": ["В"],
    "source": "текст, раздел «Основные командные режимы»; анимация 1 кадры 17–19 (configure terminal в S1> не выполняется, подпись «S1> — команды, изменяющие конфигурацию, недоступны»)",
    "quote": "В этом режиме доступно только ограниченное число основных команд мониторинга, но невозможно выполнять какие-либо команды, которые могут изменить конфигурацию устройства. Пользовательский режим EXEC можно определить по командной строке CLI, оканчивающейся символом «>».",
    "class": "понимание",
    "why": "Симптом («вижу состояние, но настройка не проходит») надо перевести в режим, а режим — в вид приглашения; само слово «пользовательский режим» в вопросе не звучит."
  },
  {
    "q": "5",
    "answer": ["Г"],
    "source": "текст, раздел «Переключение между режимами ОС» (пример кода Switch(config)# line console 0 / Switch(config-line)# exit / Switch(config)#); анимация 2 кадр 49 (стрелка exit от (config-line)# к (config)#)",
    "quote": "Для выхода из режима подконфигурации и возврата в режим глобальной конфигурации используйте команду exit.",
    "class": "понимание",
    "why": "Нужно знать, что exit поднимает ровно на один уровень (в (config)#), а не сразу в Sw# (это end/Ctrl+Z) и не закрывает сеанс (так exit ведёт себя только из S1#, по анимации 2 кадр 32–33)."
  },
  {
    "q": "6",
    "answer": ["Б"],
    "source": "текст, раздел «Безопасная среда для практики»",
    "quote": "Изменять конфигурацию устройств лучше сначала учиться в безопасной среде, не связанной с рабочей сетью, и только потом — на реальном оборудовании. Для этого служат лабораторные работы курса: устройства в них моделирует симулятор.",
    "class": "узнавание слова",
    "why": "Правильный вариант почти дословно повторяет фразу раздела («симулятор», «моделирует устройства»); достаточно узнать слово, разбираться в различиях вариантов не требуется."
  }
]
```

## 2. Самопроверка ↔ лекция

**Нельзя ответить из материала и блокнота:** таких вопросов нет. Все шесть вопросов закрываются текстом material.md; анимации 1 и 2 дублируют и подтверждают те же факты (приглашения `>`, `#`, `(config)#`, `(config-line)#`, `(config-if)#`; команды enable/disable, configure terminal/exit, line …/interface …, end и Ctrl+Z).

**Проверяют только узнавание слова:** вопрос 6. Верный вариант «В симуляторе, моделирующем устройства» — перефраз строки «устройства в них моделирует симулятор» из раздела «Безопасная среда для практики». Чтобы выбрать его, не нужно понимать, почему остальные варианты плохи; достаточно вспомнить слово. (Замечу как учащийся: про программу эмуляции терминала из варианта Г я знаю только из блокнота N-02.01-31/N-02.01-41 — она лишь подключает к устройству, сама команды коммутатора не выполняет; но этот довод для ответа не понадобился.)

**Требуют того, чего не объясняли:** таких вопросов нет. Единственная тонкость — в вопросе 5 вариант Б («сеанс закроется») опирается на поведение exit из привилегированного режима, которое в тексте не описано, а показано только в анимации 2 (кадры 32–33: `S1#exit` → `S1 con0 is now available`, подпись шага 3 «exit из S1# закрывает консоль»). Но для правильного ответа это знать не обязательно: текст прямо говорит, куда ведёт exit из режима настройки линии.

**Проверяют понимание:** вопросы 1–5. В каждом из них режим или команда не названы прямо: нужно перевести описание ситуации (вид приглашения, доступные/недоступные команды) в режим и затем в команду или наоборот, и отличить близкие команды (exit vs end/Ctrl+Z vs disable) и близкие приглашения (`#`, `(config)#`, `(config-if)#`).

## Открытые файлы

- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/task02/02.02-ios-navigation-S.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/persona.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/notebook.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/material.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/selfcheck.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-1.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-2.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-3.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-4.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-5.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-6.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-7.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-8.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-01-sheet-9.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-1.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-2.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-3.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-4.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-5.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-6.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-7.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-8.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-9.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-10.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-11.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-12.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-13.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-14.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-15.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-16.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-17.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-18.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-19.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-20.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-21.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-22.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.02-ios-navigation/S/anim-02-sheet-23.png

Папка frames/ (отдельные кадры anim-01-fNNN.png, anim-02-fNNN.png) не открывалась: листов кадров хватило. Файлы вне папки in02/02.02-ios-navigation/S не открывались и не искались.

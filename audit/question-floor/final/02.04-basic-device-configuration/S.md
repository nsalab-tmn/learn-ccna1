# 02.04 Базовая настройка устройств — самопроверка, персона S

## 1. Ответы

```json
[
  {
    "q": "1",
    "answer": ["А"],
    "source": "текст, раздел «Настройка паролей»",
    "quote": "Наконец, включите проверку пароля при входе на линию с помощью команды login: без нее вход с консоли идет без пароля.",
    "class": "понимание",
    "why": "Надо понять, что password только задаёт пароль, а проверку при входе включает отдельная команда login; остальные варианты — команды для другого (enable, баннер, шифрование)."
  },
  {
    "q": "2",
    "answer": ["А"],
    "source": "текст, раздел «Шифрование паролей»",
    "quote": "Шифрование применяется только к паролям в файле конфигурации, но не к паролям, которые отправлены по сети.",
    "class": "понимание",
    "why": "Нужно понять границу действия команды: она меняет вид паролей в файле конфигурации и ничего не делает ни с передачей по сети (Б прямо опровергнут текстом), ни с запросом пароля при входе (В, Г)."
  },
  {
    "q": "3",
    "answer": ["Б"],
    "source": "текст, раздел «Баннерные сообщения»",
    "quote": "необходимо использовать уведомления о том, что лишь авторизованным пользователям можно получить доступ к устройству. Для этого нужно добавить баннер во выходные данные устройства.",
    "class": "узнавание слова",
    "why": "Формулировка вопроса почти дословно повторяет фразу материала, а верный вариант содержит название раздела и команду banner motd; достаточно узнать слово «баннер»."
  },
  {
    "q": "4",
    "answer": ["В"],
    "source": "текст, раздел «Правила выбора паролей»",
    "quote": "использовать пароли длиной не менее 15 символов: надежность пароля определяет прежде всего длина; … не использовать последовательности символов вроде 1234abcd … не использовать часто употребляющиеся слова",
    "class": "понимание",
    "why": "Надо применить сразу несколько правил к четырём паролям: А — последовательность, Б — короче 15 символов (смесь символов не спасает), Г — обычное слово Administrator; только В длинный и без последовательностей и слов."
  },
  {
    "q": "5",
    "answer": ["Г"],
    "source": "текст, раздел «Имена устройств»",
    "quote": "начинать с буквы; не ставить пробелы; оканчивать на букву или цифру; включать только буквы, цифры и тире; составлять не более чем из 63 символов.",
    "class": "понимание",
    "why": "Нужно сопоставить имя Sw Floor 2 со списком рекомендаций и отбросить варианты, которые описывают разрешённое (цифра в конце, менее 63 символов) или то, что регистр не значим."
  },
  {
    "q": "6",
    "answer": ["Б"],
    "source": "текст, раздел «Безопасный административный доступ к коммутатору», п. 5; анимация 1 кадр 52",
    "quote": "Вместо пароля enable secret в конфигурации хранится его хеш (enable secret 5 …), а пароли консоли и VTY видны открытым текстом (password netlab).",
    "class": "узнавание слова",
    "why": "Верный вариант почти дословно повторяет фразу материала; что такое «хеш», материал не объясняет, но для ответа это и не нужно — хватает узнать слово."
  },
  {
    "q": "7",
    "answer": ["В"],
    "source": "текст, раздел «Настройка паролей»",
    "quote": "Чтобы иметь доступ администратора ко всем командам ОС, включая настройку устройства, необходимо получить привилегированный доступ режима EXEC. Это самый важный метод, поскольку он обеспечивает полный доступ к устройству.",
    "class": "понимание",
    "why": "Нужно соединить два утверждения: пароль консоли закрывает только пользовательский режим EXEC («Теперь для доступа к пользовательскому режиму EXEC с консоли будет необходим пароль»), а привилегированный режим даёт полный доступ (ещё N-02.02-07, N-02.02-08); Б опровергается анимацией 1 кадр 13, где enable работает до настройки enable secret."
  }
]
```

## 2. Самопроверка ↔ лекция

**Нельзя ответить из материала и блокнота:** таких вопросов нет. На все семь вопросов ответ находится в тексте material.md (разделы «Имена устройств», «Правила выбора паролей», «Настройка паролей», «Шифрование паролей», «Баннерные сообщения», «Безопасный административный доступ к коммутатору») и в листах анимации 1; блокнот нужен только как опора по режимам EXEC (N-02.02-03…N-02.02-10) для вопроса 7.

**Проверяют только узнавание слова:**
- Вопрос 3 — формулировка задания повторяет фразу материала «лишь авторизованным пользователям можно получить доступ к устройству», верный вариант содержит название раздела «баннерное сообщение дня» и команду banner motd.
- Вопрос 6 — верный вариант Б почти дословно повторяет п. 5 раздела «Безопасный административный доступ к коммутатору» («хранится его хеш … видны открытым текстом»).

**Требуют того, чего не объясняли:** вопросов, которые нельзя решить без необъяснённого, нет. Частичные замечания:
- Вопрос 6: слово «хеш» в материале не объяснено (ни в persona.md, ни в блокноте его нет); ответ всё равно находится по совпадению фразы. Дистрактор Г упоминает команду copy running-config startup-config, которую материал не описывает (startup-config только назван как файл), но дистрактор отбрасывается и без этого.
- Вопрос 7: дистрактор Б («без enable secret команда enable не работает») текст прямо не опровергает; опровержение видно только в анимации 1 (кадр 13: S1>enable → S1# до любой настройки паролей) и из блокнота N-02.02-24.

**Проверяют понимание:** вопросы 1, 2, 4, 5, 7 — нужно применить объяснённые правила или границы действия команд к новой ситуации.

## Открытые файлы

- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/task02/02.04-basic-device-configuration-S.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/persona.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/notebook.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/material.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/selfcheck.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/fig-01.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-1.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-2.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-3.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-4.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-5.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-6.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-7.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-8.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-9.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-10.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-11.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-12.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-13.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-14.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-15.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-16.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-17.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-18.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-19.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-20.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-21.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-22.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-23.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-24.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/anim-01-sheet-25.png

Папка /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.04-basic-device-configuration/S/frames/ только просмотрена списком (100 файлов anim-01-f001.png … anim-01-f100.png); отдельные кадры не открывались — все 100 кадров есть на 25 листах.

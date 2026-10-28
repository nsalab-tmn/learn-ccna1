# 02.05-save-configurations · самопроверка глазами учащегося S

```json
[
  {
    "q": "1",
    "answer": ["А"],
    "source": "текст, раздел «Файлы конфигурации»",
    "quote": "running-config — файл текущей конфигурации, хранится в оперативной памяти (RAM). […] RAM — энергозависимая память. После отключения питания или перезагрузки устройства RAM теряет все свое содержимое.",
    "class": "понимание",
    "why": "Надо связать два факта текста: несохранённые изменения живут в running-config, а running-config лежит в энергозависимой RAM; варианты Б и В прямо противоречат тексту (изменения действуют незамедлительно; NVRAM не теряется при выключении)."
  },
  {
    "q": "2",
    "answer": ["А"],
    "source": "текст, раздел «Файлы конфигурации»",
    "quote": "Чтобы сохранить изменения, используйте команду привилегированного режима EXEC copy running-config startup-config.",
    "class": "понимание",
    "why": "Надо знать направление копирования (из RAM в NVRAM, где конфигурация переживает перезагрузку), чтобы не перепутать с обратной командой copy startup-config running-config (вариант В); хотя сама фраза «чтобы сохранить изменения» в тексте стоит рядом с командой, так что вопрос близок к узнаванию."
  },
  {
    "q": "3",
    "answer": ["Б"],
    "source": "текст, раздел «Изменение текущей конфигурации»",
    "quote": "Недостатком использования команды reload для удаления несохраненной текущей конфигурации является кратковременный переход устройства в автономный режим и, как следствие, простой сети.",
    "class": "понимание",
    "why": "Нужно перенести объяснённый недостаток reload (устройство уходит в автономный режим, сеть простаивает) на ситуацию с подключёнными сотрудниками; варианты А и В противоречат тексту (reload применяет startup-config, а не удаляет её и не сбрасывает в заводские), Г — тоже (ОС спросит, сохранять ли, и на n/no изменения отменяются)."
  },
  {
    "q": "4",
    "answer": ["В"],
    "source": "текст, раздел «Изменение текущей конфигурации»",
    "quote": "После удаления начальной конфигурации из NVRAM перезапустите устройство, чтобы удалить файл текущей конфигурации из RAM. При перезагрузке на коммутаторе применяется загрузочная конфигурация по умолчанию, с которой изначально поставлялось устройство.",
    "class": "понимание",
    "why": "Надо понимать, что erase startup-config чистит только NVRAM, а в RAM по-прежнему работает старая running-config, и она исчезнет только после перезагрузки; это же показывает анимация 1 (шаг 5 → шаг 6: после erase ещё S1#, и только после reload с ответом no — снова Switch)."
  },
  {
    "q": "5",
    "answer": ["Г"],
    "source": "текст, раздел «Запись конфигурации в текстовый файл»",
    "quote": "Чтобы восстановить файл конфигурации на устройстве, нужно совершить два действия. Шаг 1 Войти в режим глобальной конфигурации на устройстве. Шаг 2 Скопировать и вставить текстовый файл в окно терминала, подключенного к коммутатору.",
    "class": "понимание",
    "why": "Надо узнать по приглашению Sw-New# привилегированный режим EXEC, а не глобальную конфигурацию (из блокнота N-02.02-09 и N-02.02-14 приглашение глобальной конфигурации — имя(config)#), и вспомнить, что каждая команда работает только в своём режиме (N-02.02-27), поэтому строки конфигурации, вставленные не в том режиме, дают ошибки; варианты А и Б — лишние действия, В противоречит тексту."
  },
  {
    "q": "6",
    "answer": ["Б"],
    "source": "текст, раздел «Сохранение и восстановление конфигурации», п. 7",
    "quote": "copy startup-config running-config копирует загрузочную конфигурацию в текущую: имя снова MySwitch, но show running-config | section line con показывает, что пароль консоли остался. Команды файла добавляются к текущей конфигурации, а не заменяют ее.",
    "class": "понимание",
    "why": "Вопрос проверяет, понял ли учащийся, что копирование startup-config в running-config объединяет файлы, а не затирает текущую конфигурацию (то же видно в анимации 1, кадр 98: «startup-config добавляется к running-config: пароль консоли остался»); правда, ситуация и формулировка ответа почти дословно повторяют п. 7 текста, так что вопрос близок к узнаванию."
  }
]
```

## 2. Самопроверка ↔ лекция

**Нельзя ответить из материала и блокнота:** таких вопросов нет. Все шесть вопросов закрываются текстом material.md (и подтверждаются анимацией 1); для вопроса 5 дополнительно нужны строки блокнота о приглашениях режимов (N-02.02-09, N-02.02-14, N-02.02-27), и они в блокноте есть.

**Проверяют только узнавание слова:** в строгом смысле — ни один: в каждом вопросе есть дистрактор, который ловит бездумное узнавание (в вопросе 2 — обратная команда copy startup-config running-config, в вопросе 6 — «скопировала в обратную сторону»). Но два вопроса стоят на границе:
- вопрос 2 — текст прямо говорит «Чтобы сохранить изменения, используйте … copy running-config startup-config», и ситуация «хочет, чтобы настройки сохранились после перезагрузки» совпадает с этой фразой;
- вопрос 6 — ситуация (пароль консоли остался после copy startup-config running-config) и правильный вариант почти дословно повторяют п. 7 раздела «Сохранение и восстановление конфигурации».

**Требуют того, чего не объясняли:** таких нет. Небольшая натяжка только в вопросе 5: материал не говорит, что именно произойдёт, если вставить конфигурацию в привилегированном режиме (про «сообщения об ошибках почти на каждой строке» в тексте нет), но вывод делается из уже известного: команды работают только в своём режиме (N-02.02-22, N-02.02-27), а приглашение `Sw-New#` — это не `(config)#`.

Замечания учащегося по ходу чтения: что такое NVRAM и чем она физически отличается от RAM, материал не объясняет (сказано только, что содержимое NVRAM не теряется при выключении); фильтры `| include` и `| section` в тексте показаны, но что такое «фильтр вывода» вообще — не объяснено; «режим журнала» в программе терминала (шаг 2 записи в текстовый файл) — тоже дано без пояснений. На ответы на самопроверку это не повлияло.

## Открытые файлы

- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/task02/02.05-save-configurations-S.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/persona.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/notebook.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/material.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/selfcheck.md
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-1.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-2.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-3.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-4.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-5.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-6.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-7.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-8.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-9.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-10.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-11.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-12.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-13.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-14.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-15.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-16.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-17.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-18.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-19.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-20.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-21.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-22.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-23.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-24.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/anim-01-sheet-25.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/frames/anim-01-f044.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/frames/anim-01-f049.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/frames/anim-01-f055.png
- /tmp/claude-0/-home-user/c4c55851-32e9-5d24-997d-98b16d31d75c/scratchpad/judge/in02/02.05-save-configurations/S/frames/anim-01-f062.png

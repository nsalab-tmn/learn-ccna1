# CCNA1 quiz and exam review (kb#275)

> **Status:** review done on 2026-10-18 at `origin/main` `a238c6c`, after all CCNA1 de-marketing PRs were merged. Fixes are in the PRs listed below. Doubtful items wait for the operator on kb#275.

## What

A question-by-question review of every CCNA1 quiz and exam, and of the CCNA1 bank in `__exams/CCNA1`:

| Set | Files | Questions |
|---|---|---|
| module quizzes (`NN-module/*quiz*/`) | 80 | 505 |
| module and final exams (`*-exam/`, `final-exam/`) | 7 | 419 |
| bank copies (`__exams/CCNA1/*_Exam/`) | 7 | 420 |

The `__exams/CCNA1` bank was dissolved into the module exams in learn-ccna1#221 (kb#293) and `final-itn/test.json` in learn-ccna1#239 (kb#313), so the bank rows above describe the state at review time. The CCNA2 and CCNA3 banks in `__exams/` are reviewed with those courses. `ITN_Assessment_PTSA.pka` and `__exams/CCNA1/final-lab` are out of scope (labs and `.pka` files, kb#271).

## Why

The quizzes and exams are translations of the vendor's question banks. The de-marketing passes (kb#272) changed vendor names but did not check whether the questions are right. This review checks each question for:
1. **Correctness:** the key is right by the course text and the standards (RFC, IEEE). Every distractor is wrong, and the number of correct answers matches the stem.
2. **Course match:** the question can be answered from its module or an earlier one, in the module's terms.
3. **Language:** natural Russian, without machine-translation artefacts or English left in prose.
4. **Vendor and Packet Tracer leftovers** that the de-marketing missed.
5. **References:** images exist, and comments match the key.

## How

1. **Mechanical pass** over all files: answer counts against `answerType` and the stem, matching keys, image paths, Packet Tracer UI strings. In CCNA1 it found one item, bank 01-03 Q48, a Packet Tracer activity (`.pka`).
2. **Review:** eight reviewers each took a block of modules or exams and wrote findings with evidence (`README.md:line`, RFC or IEEE) and a proposed minimal fix.
3. **Verification:** every finding was checked again before it went into a PR. The coordinator checked the quiz findings. Second reviewers checked the exam findings and rewrote fixes where needed, then the coordinator spot-checked them. Fixes were checked against the glossary (`conventions/ru-glossary.md` in the knowledge base, with the rows decided in kb#279) for forbidden variants. Standalone swaps of «роутер» / «маршрутизатор» and «хост» / «узел» were left to the kb#276 alignment. Sentences rewritten for other reasons use «маршрутизатор», as the glossary decides (kb#279) and as the bank copies already do.
4. **Fix PRs:** one per module block, so no two open PRs share a line. The bank copies change in the same PR as their exam and get the same wording.
5. **Review of the fix PRs:** kb read every changed string. Its fixes and the optional suggestions taken went into follow-up commits on the same PRs, and this report includes them.
6. **Doubtful items** are not changed. They go to the operator on kb#275: two defensible answers, content the course does not teach, or a course text that is itself wrong.

Severity follows kb#275:
- `error`: a wrong key, a distractor that is actually right, a wrong statement in a question or comment, or a comment copied from another question;
- `style`: language, terms, typos, English or Cyrillic/Latin mix-ups;
- `unclear`: an ambiguous stem or two defensible answers.

## JSON structure (recorded, unchanged)

All 94 files share one structure. No PR changes keys, key order, the number of questions or answers, image paths or HTML comments.

- **Top level:** `title`, `description`, `difficulty`, `duration`, `materialType`, `passingScore`, `questions`, `tags`, `skills`. Ten files also carry `assets`, and one carries `assetsPath`.
- **Question:** `question` (string, Markdown; an image as `![](./assets/x.png)`), `answerType` and `answers`. A `matching` question also has `options`.
  - `singleChoice`: 1082 questions.
  - `multiChoice`: 206 questions; the stem says how many answers are right («верны два варианта»).
  - `matching`: 56 questions.
- **Answer:** `answer` (string) and `correct` (bool). Answers of a `matching` question carry `match` instead of `correct`. An optional `comment` is shown after a wrong answer, and by convention the same comment sits on every wrong answer of a question.

## Fix PRs

| PR | Scope |
|---|---|
| learn-ccna1#111 | quizzes, modules 01–03 |
| learn-ccna1#112 | quizzes, modules 04–06 |
| learn-ccna1#113 | quizzes, modules 07–09 (key change: 09.04.02 q4) |
| learn-ccna1#114 | quizzes, modules 10–13 |
| learn-ccna1#115 | quizzes, modules 14–17 |
| learn-ccna1#117 | exams 01–03, 04–07 and bank copies |
| learn-ccna1#118 | exams 08–10, 11–13 and bank copies (key change: 08-10 Q50) |
| learn-ccna1#116 | exams 14–15, 16–17, final and bank copies |

## Totals

Findings are counted per file. A bank copy's finding counts separately from its connected exam's, and a comment copied onto three wrong answers is one finding.

| | quizzes | exams | bank copies | all |
|---|---|---|---|---|
| error | 32 | 122 | 120 | 274 |
| style | 326 | 161 | 156 | 643 |
| unclear | 14 | 16 | 16 | 46 |
| **fixed** | 354 | 283 | 276 | 913 |
| **to the operator** | 16 | 16 | 16 | 48 |
| **rejected on verification** | 2 | 0 | 0 | 2 |
| **total findings** | 372 | 299 | 292 | 963 |

The fix PRs are listed in *Fix PRs* above. Doubtful items are listed again, with their reasons, in the kb#275 comment for the operator.


## Findings: Quizzes

| File | Q | Sev | Issue | Fix |
|---|---|---|---|---|
| 01.02.06-network-components-quiz | 1 | style | Calque 'Which of the following is the name for ...': «является именем для всех компьютеров» is not natural Russian; ask what they are called | #111 → «Как называются все компьютеры, которые подключены к сети и непосредственно участвуют в сетевом взаимодействии?» |
| 01.02.06-network-components-quiz | 3 | style | Singular stem «Какое устройство является промежуточным?» for a choose-two question whose options are plural nouns | #111 → «Какие устройства являются промежуточными? (выберите два варианта)» |
| 01.03.03-network-topologies-quiz | 1 | style | Leftover English term in prose; the module uses the Russian name with the abbreviation | #111 → «Сетевая интерфейсная плата (NIC) физически подключает» |
| 01.04.05-network-types-quiz | 1 | style | Clumsy relative clause: the 'zone' is said to 'be a network' («зоне, которая обычно является сетью в отделе») | #111 → «в небольшой географической зоне, например в отделе предприятия, дома или в небольшой компании?» |
| 01.04.05-network-types-quiz | 2 | style | Truncated phrase «к данным этой?»: the noun is missing | #111 → «нуждаются в доступе к данным этой организации?» |
| 01.04.05-network-types-quiz | 3 | style | Clumsy clause: the 'zone' is said to be owned, and «принадлежит и управляется» joins two verbs with different government | #111 → «в большой географической зоне и часто принадлежит поставщику телекоммуникационных услуг, который ею управляет?» |
| 01.06.06-redundant-networks-quiz | 1 | style | «дизайнеры» is a calque of 'designers'; the module says «проектировщики» | #111 → «Когда проектировщики следуют» |
| 01.06.06-redundant-networks-quiz | 2 | style | Plural «К каким из ...» in a single-choice question asking for one characteristic | #111 → «К какой из четырех основных характеристик» |
| 01.06.06-redundant-networks-quiz | 4 | style | Broken MT sentence «Это пример того, что характерно для сетевой архитектуры, это?» | #111 → «Это пример какой характеристики сетевой архитектуры?» |
| 01.06.06-redundant-networks-quiz | 4 | style | Misplaced modifier «примером устойчивой сетевой архитектуры к сбоям» | #111 → «Резервирование — пример устойчивости сетевой архитектуры к сбоям» |
| 01.07.10-network-trends-quiz | 1 | style | Broken phrase «для проведения конференций, находящимися в другом городе»: the participle has no noun to attach to | #111 → «для проведения конференций с людьми, находящимися» |
| 01.07.10-network-trends-quiz | 3 | style | Double backticks render the four words as inline code (monospace), not quotes; «функция содержит такие параметры» is a calque of 'feature has options' | #111 → «Что из перечисленного подразделяется на такие типы, как «общедоступные», «частные», «коллективные» и «гибридные»?» |
| 01.07.10-network-trends-quiz | 3 | style | Calque «Такие опции содержат облачные вычисления» | #111 → «На такие типы подразделяются облачные вычисления» |
| 01.08.03-network-security-quiz | 1 | style | «замедляет или приводит к сбою оборудования и программ»: «замедляет» needs an accusative object, so the shared genitive object is ungrammatical | #111 → «замедляет работу оборудования и программ или приводит к их сбою» |
| 01.08.03-network-security-quiz | 1 | style | Noun repeated inside its own parenthetical: «Атака типа «отказ в обслуживании» (DoS-атака)» | #111 → «Атака типа «отказ в обслуживании» (DoS)» |
| 01.08.03-network-security-quiz | 2 | style | Option label differs from the same option in q1, q3, q4, q5 («Атака нулевого дня или часа») and capitalises «Нулевой час» mid-phrase | #111 → «Атака нулевого дня или часа» |
| 01.08.03-network-security-quiz | 5 | style | «Что описывает вредоносный код ...» reads as 'what does malicious code describe'; the intended question is what malicious code running on devices is called | #111 → «Как называется вредоносный код, запущенный на пользовательских устройствах?» |
| 01.10.02-quiz | 2 | style | «сотрудников» mistranslates 'collaborators'; employees are the intranet audience, and the comments and module speak of partners/contractors | #111 → «для поставщиков, клиентов и партнеров?» |
| 01.10.02-quiz | 3 | style | Clumsy label mixing English name, abbreviation and a Russian gloss in parentheses | #111 → ««Принеси свое устройство» (BYOD)» |
| 01.10.02-quiz | 7 | style | Wrong word: «отрывок времени» (excerpt) instead of «отрезок времени» | #111 → «очень короткий отрезок времени» |
| 01.10.02-quiz | 7 | style | Bureaucratic genitive chain «меры, предпринятые для обеспечения получения необходимых сетевых ресурсов сетевым трафиком» | #111 → «это меры, которые гарантируют необходимые сетевые ресурсы трафику, требующему более высокой пропускной способности» |
| 01.10.02-quiz | 10 | style | Slang transliteration «Диалап»; the module uses «Телефонный коммутируемый доступ» | #111 → «"answer": "Телефонный коммутируемый доступ"» |
| 01.10.02-quiz | 12 | style | «требует от организации размещения разных устройств» calques 'accommodate' and reads as physically placing devices | #111 → «требует от организации поддержки разных устройств» |
| 01.10.02-quiz | 14 | style | Typo «технологи» for «технологии» | #111 → «сетевые технологии,» |
| 02.01.06-access-to-cisco-ios-quiz | 3 | style | Broken government «будет наиболее подходящим внутриполосным доступом»: the access method is equated with the access | #111 → «будет наиболее подходящим для внутриполосного доступа к ОС» |
| 02.02.08-ios-navigation-quiz | 1 | style | Comment calls global configuration mode and its sub-modes «Команды более высокого уровня»; they are modes, not commands | #111 → «EXEC. Режимы конфигурации более высокого» |
| 02.02.08-ios-navigation-quiz | 1 | style | The comment has «режим» ×4 and «конфигурации» ×3 in one sentence, and «режимы дополнительной конфигурации» differs from the options («вложенный режим конфигурац… | #111 → «В режим глобальной конфигурации и во вложенные режимы конфигурации можно перейти только из привилегированного режима EXE…» |
| 02.02.08-ios-navigation-quiz | 2 | style | The question mark sits inside the inline-code span, so the prompt is shown as «Switch(config)#?», which itself looks like a help command | #111 → «``Switch(config)#``?» |
| 02.02.08-ios-navigation-quiz | 3 | style | The question mark sits inside the inline-code span, so the prompt is shown as «Switch>?», which is the help command typed at the prompt | #111 → «``Switch>``?» |
| 02.02.08-ios-navigation-quiz | 4 | style | Calque «вернуться из любого режима, вплоть до привилегированного» ('all the way back to'); «вплоть до» does not express a destination | #111 → «Чтобы из любого режима конфигурации вернуться в привилегированный режим EXEC,» |
| 02.04.08-basic-device-configuration-quiz | 1 | style | Typo «испльзуется» | #111 → «используется» |
| 02.04.08-basic-device-configuration-quiz | 2 | style | Comment says enable secret protects «режиму EXEC»; it protects privileged EXEC, while user EXEC is protected with password/login (q3 of this quiz) | #111 → «Защита доступа к привилегированному режиму EXEC» |
| 02.04.08-basic-device-configuration-quiz | 3 | style | English duplicate in parentheses «в режиме линии (Line mode)»; the module term is «режим настройки линии» | #111 → «в режиме настройки линии» |
| 02.06.03-ports-and-addresses-quiz | 2 | style | Missing hyphen «IPv4 адреса» (the other comments have «IPv4-адреса») | #111 → «IPv4-адреса записываются» |
| 02.06.03-ports-and-addresses-quiz | 3 | style | Tautology «Виртуальные интерфейсы ... являются виртуальными» | #111 → «не связаны ни с каким физическим портом» |
| 02.09.04-quiz | 1 | error | Comment states the running configuration is saved automatically; it is not (the source says it is neither deleted nor saved automatically). It also contradicts … | #111 → «Файл текущей конфигурации нельзя удалить, и он не сохраняется автоматически» |
| 02.09.04-quiz | 1 | style | «Это влияет на работу устройства» breaks the parallel with the other options (Его/Он = the file) and reads as 'this affects' | #111 → «Он влияет на работу устройства сразу после изменения» |
| 02.09.04-quiz | 3 | style | Stray preposition «на линию консоли»; the other options are nominative noun phrases | #111 → «"answer": "линия консоли"» |
| 02.09.04-quiz | 5 | style | Clumsy «должно состоять меньше, чем из 64 символов» | #111 → «имя узла должно состоять менее чем из 64 символов» |
| 02.09.04-quiz | 5 | unclear | Course text gives the hostname limit as «не более чем из 64 символов» (64 allowed), while the keyed option says fewer than 64; the option matches RFC 1035 (labe… | operator (kb#275) |
| 02.09.04-quiz | 8 | style | «в используемых производственных устройствах» calques 'production devices' and reads as manufacturing equipment | #111 → «изменения на устройствах рабочей сети» |
| 02.09.04-quiz | 9 | style | «неустойчивой памятью» is a calque of 'volatile'; the module term is «энергозависимая» | #111 → «RAM является энергозависимой памятью» |
| 02.09.04-quiz | 10 | style | The question mark sits inside the inline-code span, so it is shown as part of the command «copy startup-config running-config?» | #111 → «``copy startup-config running-config``?» |
| 02.09.04-quiz | 11 | style | Plural «Какие функции предоставляет DHCP?» in a single-choice question | #111 → «Какую функцию выполняет DHCP?» |
| 02.09.04-quiz | 14 | style | Bureaucratic «Цель ... состоит в том, чтобы отделить ... от части IP-адреса узла», with an ambiguous «части IP-адреса узла» | #111 → «Маска подсети отделяет сетевую часть IP-адреса от узловой части.» |
| 03.01.12-the-rules-quiz | 1 | style | «Как происходит преобразование ...?» asks how it happens, but the options are names of processes | #111 → «Как называется преобразование информации в форму, пригодную для передачи?» |
| 03.01.12-the-rules-quiz | 3 | error | Keyed answer «управление процессами» (process management) is not a component of message timing; the intended item is flow control, as the option's own comments … | #111 → «"answer": "управление потоком"» |
| 03.02.04-protocols-quiz | 1 | style | Option forms are inconsistent: the key is a bare genitive «маршрутизации», which gives it away against the full noun phrases of the other options | #111 → «"answer": "протоколы маршрутизации"» |
| 03.02.04-protocols-quiz | 1 | style | Singular «протокол обнаружения сервисов» among plural options; the module term is «Протоколы обнаружения служб» | #111 → «"answer": "протоколы обнаружения служб"» |
| 03.02.04-protocols-quiz | 2 | style | Chain «используется для обнаружения служб для ...» and «DNS для служб разрешения IP-адресов» (DNS resolves names to addresses; «разрешение адресов» in this cour… | #111 → «DHCP служит для автоматического распределения IP-адресов, а DNS — для преобразования имен в IP-адреса» |
| 03.03.06-protocol-suites-quiz | 1 | style | Typo «протоколльной» (double л) | #111 → «протокольной» |
| 03.03.06-protocol-suites-quiz | 5 | style | MT garble «кадр связи данных с данными и процессами»: 'processes' (verb) became a noun and 'data link frame' became «кадр связи данных» | #111 → «Устройство получает кадр канального уровня с данными, обрабатывает его и удаляет информацию Ethernet.» |
| 03.03.06-protocol-suites-quiz | 6 | style | Leftover English «ICMP (Messaging)» in prose | #111 → «ICMP (обмен сообщениями)» |
| 03.04.05-standards-organizations-quiz | 1 | style | Calque «нейтральны с точки зрения поставщиков» ('vendor-neutral'); the module says «независимыми от поставщиков» | #111 → «организации по стандартизации, как правило, независимы от поставщиков?» |
| 03.04.05-standards-organizations-quiz | 2 | style | Grammar: «Общество Интернет» needs the genitive «Интернета» (same option in q2 and q3) | #111 → «Общество Интернета (ISOC)» |
| 03.04.05-standards-organizations-quiz | 2 | style | English plural «(RFCs)» in Russian prose | #111 → «(RFC)» |
| 03.06.06-data-encapsulation-quiz | 1 | style | Typo «назыывается» | #111 → «называется» |
| 03.06.06-data-encapsulation-quiz | 4 | style | Agreement error «по мере его перемещения»: the antecedent «данные» is plural; also «стеку протокола» should be «стеку протоколов» | #111 → «по мере их перемещения вниз по стеку протоколов» |
| 03.06.06-data-encapsulation-quiz | 4 | style | Clumsy repetition «данных ... данные протокола ... к исходным данным» and wrong direction «в стек» | #111 → «По мере перемещения данных вниз по стеку протоколов к ним добавляется служебная информация протоколов.» |
| 03.06.06-data-encapsulation-quiz | 4 | style | «добавления информации протокола … стеку протоколов» repeats «протокол»; the comment calls it «служебная информация протоколов» (review suggestion) | #111 → «Как называется добавление служебной информации протоколов к данным по мере их перемещения вниз по стеку?» |
| 03.07.11-data-access-quiz | 2 | style | Sentence fragment «Самая левая часть IP-адреса, которая идентифицирует сеть.» has no predicate | #111 → «Самая левая часть IP-адреса идентифицирует сеть.» |
| 03.07.11-data-access-quiz | 3 | style | Wrong case «крайнюю левую часть» (accusative) among nominative options | #111 → «крайняя левая часть MAC-адреса» |
| 03.08.02-quiz | 1 | style | «МАС» is typed in Cyrillic letters (U+041C U+0410 U+0421), unlike the Latin «MAC» used everywhere else | #111 → «Тема 3.4.0 - MAC-адрес» |
| 03.08.02-quiz | 4 | style | Option «групповая» while its own comment calls the same delivery «многоадресной доставкой»; the module term is «многоадресная передача» (q2 and q11 of this file… | #111 → «"answer": "многоадресная"» |
| 03.08.02-quiz | 5 | style | Calque «взаимодействие между каждым уровнем и протоколами между каждым уровнем» ('between each layer') | #111 → «помогает наглядно представить, как взаимодействуют уровни и работающие на них протоколы» |
| 03.08.02-quiz | 6 | style | Calque «Операционные системы не указываются протоколами, но обеспечивают внедрение протоколов» | #111 → «Протоколы не определяют, какая операционная система используется: ОС лишь реализует их» |
| 03.08.02-quiz | 8 | style | Broken grammar «Каков общий термин используется ...» | #111 → «Какой общий термин используется» |
| 03.08.02-quiz | 8 | style | «блок данных протокола (PDU)» differs from the module term «единица данных протокола (PDU)», also used in 03.06.06 q2 | #111 → «термин «единица данных протокола» (PDU)» |
| 03.08.02-quiz | 12 | style | Calque and chain «Процесс получения передаваемых данных и реверсирование процесса кодирования для интерпретации информации» | #111 → «Получение переданных данных и их обратное преобразование для интерпретации информации — это декодирование» |
| 04.01.03-purpose-of-the-physical-layer-quiz | 3 | style | Option is a bare genitive 'представления', not a layer name; it does not answer 'На какой ... уровень' and is inconsistent with the other options (уровень прило… | #112 → «"answer": "уровень представления"» |
| 04.01.03-purpose-of-the-physical-layer-quiz | 3 | style | Agreement error 'кадры ... преобразует его', calque 'пропускает' (passes) for 'передает', double space | #112 → «Физический уровень получает кадры от канального уровня и преобразует их в биты для передачи. На принимающем устройстве ф…» |
| 04.02.07-physical-layer-characteristics-quiz | 1 | style | Calque of 'patterns of microwaves': 'наборы микроволн' is not natural Russian; module says 'микроволновые сигналы' | #112 → «используются микроволновые сигналы?» |
| 04.02.07-physical-layer-characteristics-quiz | 1 | style | Calque 'наборами микроволновых передач' (patterns of microwave transmissions) | #112 → «В беспроводных сетях биты представлены микроволновыми сигналами» |
| 04.02.07-physical-layer-characteristics-quiz | 2 | style | Word order makes 'световые волны' the subject: reads as 'light waves use fibre-optic cables to represent bits' | #112 → «В волоконно-оптических кабелях для представления битов используются световые волны» |
| 04.02.07-physical-layer-characteristics-quiz | 4 | style | Calque 'емкость носителя' (capacity of a medium) reads as storage capacity of a storage medium | #112 → «Какой термин описывает возможности среды по передаче данных?» |
| 04.03.06-copper-cabling-quiz | 2 | unclear | Coaxial cable is also defensible: the module says its shield reduces external EMI and that it uses special BNC/N/F connectors; only STP's 'специальные экраниров… | operator (kb#275) |
| 04.05.07-fiber-optic-cabling-quiz | 1 | style | Missing preposition ('передаче данных примерно 500 метров'), calque 'могут помочь' (can help); plural 'Какие ... типы' in a single-choice item | #112 → «Какой тип оптоволоконного кабеля обычно используется для передачи данных на расстояние около 500 метров?» |
| 04.05.07-fiber-optic-cabling-quiz | 1 | style | Clumsy sentence: 'в сетях с расстоянием', subjectless 'но может быть до 2 км' | #112 → «Обычно применяется на расстояниях в несколько сотен метров, но возможно и до 2 км» |
| 04.05.07-fiber-optic-cabling-quiz | 2 | style | Calque 'источника передачи световых данных' (data light source transmitter); there is no such thing as 'световые данные' | #112 → «(LED) в качестве источника света?» |
| 04.05.07-fiber-optic-cabling-quiz | 3 | style | Calques 'лазеры в одном потоке' and 'источника передачи световых данных' | #112 → «используют лазер в качестве источника света?» |
| 04.05.07-fiber-optic-cabling-quiz | 5 | style | Calque 'могут помочь при передаче данных' (can help data travel); plural 'Какие ... типы' in a single-choice item | #112 → «Какой тип оптоволоконного кабеля используется для передачи данных на расстояние около 100 км?» |
| 04.05.07-fiber-optic-cabling-quiz | 5 | style | Calque 'для дальнемагистральных работ' (long-haul applications) | #112 → «используется на линиях дальней связи протяженностью до 100 км» |
| 04.05.07-fiber-optic-cabling-quiz | 6 | style | Clumsy locative chain 'в локальных сетях в сети кампуса' | #112 → «Обычно используется в локальных сетях, например в сети кампуса» |
| 04.06.04-wireless-media-quiz | 3 | style | Missing hyphen in compound with a Latin abbreviation: 'IoT приложений' should be 'IoT-приложений' | #112 → «промышленных и IoT-приложений» |
| 04.06.04-wireless-media-quiz | 4 | style | Spelling 'ZigBee' differs from the module text and from q3 of the same quiz ('Zigbee') | #112 → «"answer": "Zigbee"» |
| 04.07.04-quiz | 1 | style | 'В каком слое ... классифицируется' is a calque; the course and the options of this question use 'уровень' | #112 → «К какому уровню модели OSI относится эта ошибка?» |
| 04.07.04-quiz | 3 | error | Comment states as absolute fact that light can travel in only one direction on a single fibre strand; the module itself notes BX standards send and receive over… | #112 → «Как правило, свет передается по нити волокна только в одном направлении» |
| 04.07.04-quiz | 4 | style | Calque 'скручивание противоположных пар проводов цепи вместе' (twisting opposing circuit wire pairs together) distorts the mechanism: the two wires of one circu… | #112 → «скручивание в пару двух проводов одной цепи» |
| 04.07.04-quiz | 4 | style | Same calque in the comment ('Скручивание противоположных пар проводов') | #112 → «Скручивание проводов одной цепи в пару подавляет такие помехи» |
| 04.07.04-quiz | 4 | unclear | Distractor 'проектирование кабельной инфраструктуры, чтобы избежать перекрестных помех' is defensible as worded: the module defines crosstalk as interference be… | operator (kb#275) |
| 04.07.04-quiz | 5 | style | 'диапазон сигналов' is a calque of 'signal range'; in Russian 'диапазон' means a band or range of values, not distance | #112 → «обеспечивают гораздо большую дальность передачи сигнала» |
| 04.07.04-quiz | 6 | style | Leftover English abbreviation 'RFI' in prose; the module uses 'РЧП' | #112 → «РЧП» |
| 04.07.04-quiz | 7 | style | Option 'консоль' is a noun that does not answer 'Какой тип кабеля' and duplicates option 3 'консольный'; the source distinguishes 'console' and 'rollover' | operator (kb#275) |
| 04.07.04-quiz | 8 | error | Key lost 'можно' (capacity): 'объем данных, передаваемый ... за определенное время' is now indistinguishable from distractor 1 (throughput: 'количество битов, п… | #112 → «объем данных, который можно передать из одного пункта в другой за определенное время» |
| 04.07.04-quiz | 10 | style | 'плакирование' is a metallurgy term (metal cladding); fibre cladding is 'оболочка' in the module | #112 → «"answer": "светоотражающая оболочка"» |
| 04.07.04-quiz | 10 | style | Same wrong term 'Плакирование'; also a missing dash before 'это' in a 'X — это Y' sentence | #112 → «Светоотражающая оболочка и устойчивость к поражению электрическим током — это основные» |
| 04.07.04-quiz | 11 | error | Comments on answers 2-4 reject distractor 3 because 'это однокомнатный офис в изолированной зоне', but the stem never says the office is one-room (lost in trans… | #112 → «В новом однокомнатном офисе начальника охраны парка» |
| 04.07.04-quiz | 11 | style | Calque 'сигнал ... иногда зависит от того или иного типа помех' (is affected by some type of interference) | #112 → «иногда подвергается помехам» |
| 04.07.04-quiz | 12 | style | Wrong case: 'Обмен кадров' should be 'Обмен кадрами' | #112 → «Обмен кадрами, управление доступом» |
| 04.07.04-quiz | 15 | style | 802.15 is WPAN, not generic 'беспроводные сети' (which would include 802.11) | #112 → «беспроводные персональные сети (802.15)» |
| 04.07.04-quiz | 15 | style | Grammar: 'те, которые влияют ..., являются Ethernet (802.3)' — 'являться' needs the instrumental; answer 1's comment already says 'теми' | #112 → «но теми, которые влияют» |
| 05.02.05-hexadecimal-number-system-quiz | 3 | style | Misspelling 'шестнадцатиричного' (correct: 'шестнадцатеричного'); also in q4 | #112 → «шестнадцатеричного» |
| 05.03.02-quiz | 4 | style | Typo: missing space 'системе11101000' | #112 → «системе — 11101000» |
| 05.03.02-quiz | 5 | style | Calque 'утверждения верны в адресах' (true about addresses) | #112 → «Какие два утверждения об адресах IPv4 и IPv6 верны?» |
| 05.03.02-quiz | 6 | style | 'десятичные знаки' means decimal places (digits after the point), not decimal numbers; 'бинарные шаблоны' is a calque of 'binary patterns' | #112 → «двоичные адреса записываются десятичными числами» |
| 05.03.02-quiz | 7 | style | Calque 'значение является релевантным ... сложите все релевантные значения' (relevant) | #112 → «Если цифра равна единице, ее значение учитывается. Чтобы получить десятичный эквивалент, сложите все учитываемые значени…» |
| 05.03.02-quiz | 9 | style | Dash used as a verb and missing space after the period: '0x3F - 63 в десятичной форме.(3*16)' | #112 → «0x3F равно 63 в десятичной системе: (3*16)» |
| 05.03.02-quiz | 11 | style | Misspelling 'шестнадцатиричного' (correct: 'шестнадцатеричного') | #112 → «шестнадцатеричного» |
| 05.03.02-quiz | 11 | style | MT artefacts: '0x относится к элементу как шестнадцатеричный', imperative mixed with infinitives ('Затем объединить ... и вычислить'), transliterated 'ниббл' (q… | #112 → «Префикс 0x означает, что число записано в шестнадцатеричной системе. Преобразуйте каждый символ в соответствующий полуба…» |
| 05.03.02-quiz | 12 | style | Calque 'Шестнадцатеричные числа составляют' (these are digits, not numbers), missing spaces after commas, double period | #112 → «Шестнадцатеричные цифры: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f.» |
| 05.03.02-quiz | 13 | style | Hex digits typed as Cyrillic letters: 'С = 1100, А = 1010' uses Cyrillic С (U+0421) and А (U+0410) | #112 → «C = 1100, A = 1010» |
| 06.01.05-purpose-of-the-data-link-layer-quiz | 1 | style | Tautological calque 'канального уровня связи данных' (data link layer rendered twice) | #112 → «Как иначе называют канальный уровень модели OSI?» |
| 06.01.05-purpose-of-the-data-link-layer-quiz | 2 | style | LLC term differs from the module text ('управление логическим соединением') | #112 → «подуровень управления логическим соединением (LLC)» |
| 06.01.05-purpose-of-the-data-link-layer-quiz | 2 | style | Comment uses a third rendering of LLC ('логическим каналом') and 'контроль доступа' instead of the module's 'управление доступом к среде' | #112 → «управление логическим соединением (LLC) и управление доступом к среде (MAC)» |
| 06.01.05-purpose-of-the-data-link-layer-quiz | 4 | style | Singular 'Какую функцию' while three answers are correct | #112 → «Какие функции второго уровня выполняет роутер?» |
| 06.01.05-purpose-of-the-data-link-layer-quiz | 4 | style | Broken syntax 'пересылают его, соответствующий среде' (participle has no noun to agree with) | #112 → «повторно инкапсулируют пакет в новый кадр, соответствующий среде этого сегмента физической сети, и передают этот кадр» |
| 06.01.05-purpose-of-the-data-link-layer-quiz | 5 | style | Wrong case: 'совместное использование среде' should be genitive 'среды' | #112 → «совместное использование среды подключения» |
| 06.02.09-topologies-quiz | 2 | style | Nonsense calque 'Глобальные сети (WAN) входят во множество топологий' (WANs come in many topologies) | #112 → «Глобальные сети (WAN) могут строиться по разным топологиям, например» |
| 06.02.09-topologies-quiz | 2 | unclear | LAN is defensible: with 'или' in the stem, the module itself describes star LANs and point-to-point Ethernet; the source's 'hub and spoke' became 'звезда', whic… | operator (kb#275) |
| 06.02.09-topologies-quiz | 4 | style | Missing 'at a time': as written it says only one device can ever access the medium | #112 → «поскольку в каждый момент времени доступ к среде может получить только одно устройство» |
| 06.03.05-data-link-frame-quiz | 1 | style | Agreement error 'окончание, содержащий', calque 'исходный и конечный адрес', missing comma, FCS not named as in the module | #112 → «заголовок, содержащий адреса второго уровня источника и назначения, и окончание, содержащее контрольную последовательнос…» |
| 06.03.05-data-link-frame-quiz | 2 | style | Wrong case: 'определяет наличия' should be accusative 'наличие' | #112 → «определяет наличие ошибок при передаче кадра» |
| 06.03.05-data-link-frame-quiz | 2 | style | Wrong case: 'определяет начальных и конечных границ' should be accusative | #112 → «определяет начальную и конечную границы кадра» |
| 06.03.05-data-link-frame-quiz | 4 | style | Typo: missing space 'уровня3' (answer 5's identical comment has 'уровня 3') | #112 → «уровня 3» |
| 06.04.02-quiz | 1 | style | Mistranslation: it is devices/NICs that MAC addresses identify, not 'Кадры Ethernet ... по их MAC-адресам' | #112 → «Устройства Ethernet идентифицируются» |
| 06.04.02-quiz | 1 | style | Comment says 'Последовательные номера' while the option it explains is 'порядковый номер' | #112 → «Порядковые номера — это поля заголовка TCP.» |
| 06.04.02-quiz | 2 | style | Calque 'Какой атрибут NIC помещал бы его на канальном уровне' (What attribute of a NIC would place it at the data link layer); identical stem in q14 | #112 → «Какая характеристика NIC позволяет отнести его к канальному уровню модели OSI?» |
| 06.04.02-quiz | 2 | style | Calque 'Кодирование MAC-адреса на NIC размещает его на этом уровне' (the encoding of the MAC address on the NIC places it at this layer) | #112 → «Наличие MAC-адреса позволяет отнести NIC к этому уровню» |
| 06.04.02-quiz | 2 | style | Calque 'размещаются на физическом уровне' (are located at the physical layer) | #112 → «относятся к физическому уровню модели OSI» |
| 06.04.02-quiz | 2 | style | Calque 'IP-адреса размещаются на сетевом уровне' | #112 → «IP-адреса относятся к сетевому уровню» |
| 06.04.02-quiz | 2 | style | Typo: 'Стек протокола TCP/IP' (the option says 'Стек протоколов TCP/IP') | #112 → «Стек протоколов TCP/IP» |
| 06.04.02-quiz | 3 | style | Leftover English 'Internet' in an organisation name; the course uses 'Общество Интернета' | #112 → «Общество Интернета (ISOC)» |
| 06.04.02-quiz | 5 | error | Comment says token passing is not a media access control method; the module presents token passing (Token Ring) as controlled access | #112 → «Передача токена — метод контролируемого, а не конкурентного доступа, а порядок приоритетности вообще не является методом…» |
| 06.04.02-quiz | 5 | style | Calque 'для обеспечения конкуренции в среде' (to mediate media contention) says CSMA/CA creates contention | #112 → «используется в беспроводных сетях как метод конкурентного доступа к среде» |
| 06.04.02-quiz | 5 | style | Calque 'для посредничества в коллизиях среды передачи данных' | #112 → «используется в проводных сетях Ethernet для обнаружения коллизий в среде передачи данных» |
| 06.04.02-quiz | 7 | error | Key mistranslated: 'одновременно в одном направлении' (simultaneously in one direction) does not describe half-duplex ('one direction at a time') and is close t… | #112 → «данные передаются по сети в обоих направлениях, но не одновременно» |
| 06.04.02-quiz | 7 | style | Leftover English mode names (Simplex, Half-duplex, Full-duplex) in prose; garbled half-duplex gloss 'в один момент и в одном направлении' | #112 → «симплексный (только в одном направлении), полудуплексный (в обоих направлениях, но в каждый момент только в одном), полн…» |
| 06.04.02-quiz | 8 | style | LLC term differs from the module text | #112 → «подуровня управления логическим соединением (LLC)» |
| 06.04.02-quiz | 9 | style | Mistranslation: 'поворот' (a turn, as in rotation) for 'turn taking' (taking turns) | #112 → «поочередный доступ (turn taking)» |
| 06.04.02-quiz | 9 | style | Clumsy instrumental passive 'Сетями Ethernet используется ... используется беспроводными сетями' | #112 → «В сетях Ethernet используется CSMA/CD, а в беспроводных сетях 802.11 — CSMA/CA.» |
| 06.04.02-quiz | 10 | style | LLC term differs from the module text | #112 → «LLC (Logical Link Control; управление логическим соединением)» |
| 06.04.02-quiz | 14 | unclear | q14 duplicates q2 (same stem and the same five options, reordered) in the same quiz | operator (kb#275) |
| 07.01.05-ethernet-frame-quiz | 1 | style | Calque 'увеличения поля кадра': padding brings the frame, not a field, up to 64 bytes | #113 → «для увеличения размера кадра по крайней мере до 64 байтов» |
| 07.01.05-ethernet-frame-quiz | 1 | style | 'начало ограничителя кадра' is a mistranslation of Start Frame Delimiter; the module calls the field 'начальный разделитель кадра (SFD)' | #113 → «начальный разделитель кадра (SFD)» |
| 07.01.05-ethernet-frame-quiz | 3 | style | Clumsy word order: 'Протокол ... идентифицирует поле EtherType' reads as the protocol identifying the field | #113 → «Протокол верхнего уровня, инкапсулированный в кадр Ethernet, определяется 2-байтным полем EtherType» |
| 07.01.05-ethernet-frame-quiz | 4 | style | Meaning drift: 'уведомляет ... о готовности к новому кадру' (notifies about readiness) instead of telling the receiver to get ready for a new frame | #113 → «сообщает принимающему устройству о необходимости приготовиться к приему нового кадра» |
| 07.01.05-ethernet-frame-quiz | 5 | style | Calque 'драйверы программного обеспечения' (software drivers); the comment of the same question already says 'программные драйверы' | #113 → «через программные драйверы» |
| 07.04.06-switch-speeds-and-forwarding-methods-quiz | 2 | style | Broken parallel construction 'с помощью быстрой пересылки или с исключением фрагментов' | #113 → «может быть реализован в режиме быстрой пересылки или исключения фрагментов» |
| 07.04.06-switch-speeds-and-forwarding-methods-quiz | 2 | style | Ungrammatical 'С использованием либо быстрой пересылки, либо с исключением фрагментов' (preposition doubled in the second branch) | #113 → «Сквозная коммутация реализуется в режиме быстрой пересылки или исключения фрагментов» |
| 07.04.06-switch-speeds-and-forwarding-methods-quiz | 4 | style | 'соединительными устройствами' means connecting devices (connectors); the meaning is connected devices, as the comment says | #113 → «между подключенными устройствами» |
| 07.04.06-switch-speeds-and-forwarding-methods-quiz | 4 | style | Typo 'автотюниг' | #113 → «автотюнинг» |
| 07.04.06-switch-speeds-and-forwarding-methods-quiz | 4 | style | Key term 'автосогласование' does not appear in the module, which calls the feature 'Автоопределение'; the quiz term is the standard one for IEEE 802.3 Auto-Nego… | operator (kb#275) |
| 07.05.02-quiz | 2 | style | Grammar: 'глобальными уникальными' should be the adverb 'глобально уникальными' | #113 → «глобально уникальными» |
| 07.05.02-quiz | 2 | style | Grammar: 'глобальный уникальный адрес' should be 'глобально уникальный адрес' | #113 → «глобально уникальный адрес» |
| 07.05.02-quiz | 3 | error | Stem claims a single special value for the first 24 bits of any multicast MAC; 01-00-5E applies only to IPv4 multicast (IPv6 uses 33-33, STP/LLDP use other rese… | #113 → «первым 24 битам MAC-адреса многоадресной рассылки IPv4?» |
| 07.05.02-quiz | 3 | style | Hex values '01-00-5Е' (the key) and 'FF-00-5Е' use a Cyrillic 'Е' instead of Latin 'E'; the comment uses Latin '01-00-5E' | #113 → «5E» |
| 07.05.02-quiz | 3 | style | Malformed distractor '01-5-Е-00': stray hyphen and Cyrillic 'Е', so it is not even a 24-bit hex value | #113 → «01-5E-00» |
| 07.05.02-quiz | 4 | style | Clumsy: 'проверяет каждый поступающий кадр, чтобы проверить' (tautology) and reflexive 'своему' wrongly refers to the destination address | #113 → «проверяет, совпадает ли MAC-адрес назначения в каждом поступающем кадре с MAC-адресом самого адаптера» |
| 07.05.02-quiz | 5 | style | Clumsy zeugma 'проверяет кадр в поисках MAC-адреса назначения и таблицу' | #113 → «Коммутатор считывает MAC-адрес назначения кадра и ищет его в таблице.» |
| 07.05.02-quiz | 8 | error | Comment says Ethernet devices drop 'jumbo' frames over 1500 bytes and runts 'до 64 байт': a runt is under 64 bytes, the maximum standard frame is 1518 bytes, an… | #113 → «(runt, менее 64 байт) или «гигантские» (giant, более 1518 байт)» |
| 07.05.02-quiz | 8 | error | Course text behind this question is itself imprecise: it calls frames 'с длиной более 1500 байт' Jumbo/Baby Giant, but 1500 bytes is the payload limit, and :74 … | operator (kb#275) |
| 07.05.02-quiz | 9 | style | 'МАС' is spelled with Cyrillic М/А/С instead of Latin MAC (7 occurrences), so it breaks search and is inconsistent with the rest of the file | #113 → «MAC» |
| 07.05.02-quiz | 12 | error | Mistranslation: the last 3 bytes must be unique 'в пределах одного пользовательского интерфейса' (within one user interface); it should say within one OUI | #113 → «в пределах одного OUI» |
| 07.05.02-quiz | 13 | style | Agreement: '64 байт' should be '64 байта' | #113 → «"answer": "64 байта "» |
| 07.05.02-quiz | 13 | style | Agreement: '1024 байт' should be '1024 байта' | #113 → «"answer": "1024 байта "» |
| 07.05.02-quiz | 14 | style | Typo: stray Cyrillic 'О' at the start of 'Овыполняет' | #113 → «выполняет» |
| 08.01.07-network-layer-characteristics-quiz | 2 | style | Garbled word order: 'IP-пакеты от сетевого уровня и инкапсулирует их ... получает канальный уровень' | #113 → «Канальный уровень получает IP-пакеты от сетевого уровня и инкапсулирует их для передачи по среде» |
| 08.01.07-network-layer-characteristics-quiz | 3 | style | 'с одного носителя на другой' is a calque of 'medium'; the module and this question's comment say 'среда (передачи данных)' | #113 → «из одной среды передачи данных в другую, с меньшим MTU» |
| 08.02.04-ipv4-packet-quiz | 1 | style | MT artefact: 'откуда и куда происходит пакет' ('происходит' = originates, cannot take 'куда'); 'являются IP-адресом' is bureaucratic | #113 → «Поля IP-заголовка, определяющие, откуда пакет поступил и куда он направляется, — это IP-адрес источника и IP-адрес назна…» |
| 08.02.04-ipv4-packet-quiz | 2 | style | Leftover English field name 'Time to Live' in Russian prose, while the other options of the question use Russian field names | #113 → «``Время жизни (TTL)``» |
| 08.02.04-ipv4-packet-quiz | 2 | style | Leftover English field name 'Version' in Russian prose | #113 → «``Версия``» |
| 08.02.04-ipv4-packet-quiz | 3 | error | Comment says the header checksum detects corrupted packets; it covers only the header. The code span also splits the field name ('``Контрольная сумма`` заголовк… | #113 → «Поле ``Контрольная сумма заголовка`` используется для обнаружения повреждений в заголовке IPv4» |
| 08.03.06-ipv6-packet-quiz | 3 | style | MT artefact 'Заголовок IPv6 является фиксированной длиной' (the header 'is a fixed length') | #113 → «Заголовок IPv6 имеет фиксированную длину 40 октетов» |
| 08.03.06-ipv6-packet-quiz | 4 | style | Second sentence of the comment is a fragment with no main verb ('Поле «Предел перехода», заменяющее поле ...') | #113 → «заголовке IPv4. Поле «Предел перехода» заменило» |
| 08.05.07-router-routing-tables-quiz | 1 | style | Typo 'netstart -r' for the host command 'netstat -r' | #113 → «netstat -r» |
| 08.05.07-router-routing-tables-quiz | 3 | style | Stem is a bare statement whose pronoun 'Его' has no antecedent, and it has no question | #113 → «Что также называют «шлюзом последней надежды»?» |
| 08.05.07-router-routing-tables-quiz | 4 | style | Case error: 'непосредственно подключенными соседям' (instrumental adjective with dative noun) | #113 → «непосредственно подключенным соседям» |
| 08.05.07-router-routing-tables-quiz | 4 | style | Case error: 'соседним роутерами' (dative adjective with instrumental noun) | #113 → «соседним роутерам» |
| 08.06.02-quiz | 1 | style | The key command is typed with an en dash ('netstat –r'), not an ASCII hyphen; it would not run as typed, and the comments write 'netstat -r' | #113 → «netstat -r» |
| 08.06.02-quiz | 1 | style | Command typed with an em dash ('netstat —s') instead of a hyphen | #113 → «netstat -s» |
| 08.06.02-quiz | 1 | style | Command typed with an en dash ('netstat –s') instead of a hyphen | #113 → «netstat -s» |
| 08.06.02-quiz | 1 | style | 'маршрутизаторе' while the module and the rest of this quiz say 'роутер' | rejected: роутер/маршрутизатор swap belongs to kb#276 alignment |
| 08.06.02-quiz | 5 | style | Calque with a dangling verb: 'чем заголовок IPv6 имеет.' | #113 → «чем заголовок IPv6» |
| 08.06.02-quiz | 8 | style | The key '127.0.0.1.' has a trailing period that no distractor has: it is not a valid address as written, and it cues the answer | #113 → «"answer": "127.0.0.1"» |
| 08.06.02-quiz | 9 | style | 'доставка с максимальной нагрузкой' mistranslates best-effort delivery; the module term is 'негарантированная доставка' | #113 → «процесс негарантированной доставки» |
| 08.06.02-quiz | 9 | style | Case error: 'определенного количество данных' | #113 → «определенного количества данных» |
| 08.06.02-quiz | 11 | error | Distractor 'адрес назначения' is also correct: the destination IP address the key names is a destination address. The intended distractor is the Layer 2 (data-l… | #113 comments emptied |
| 08.06.02-quiz | 11 | style | To match the answer 4 fix, 'адрес источника' should name the Layer 2 address, so the distractor pair stays symmetric with the IP pair | #113 → «"answer": "MAC-адрес источника"» |
| 08.06.02-quiz | 12 | unclear | 'обычно останется прежним' also fits 'флаг' and 'длина пакета': Flags and Total Length change only when a packet is fragmented, which is not the typical case. O… | operator (kb#275) |
| 08.06.02-quiz | 13 | style | Broken syntax: 'истек ли срок действия пакета и должен быть удален' has no subject or 'ли' in the second clause | #113 → «истек ли срок действия пакета и должен ли он быть удален?» |
| 08.06.02-quiz | 13 | style | Compares the protocol ICMPv6 with IPv4 ('также как IPv4'; should be 'так же, как ICMP для IPv4'); 'превышение интервала ожидания' differs from the module's 'пре… | #113 → «Протокол ICMPv6, так же как ICMP для IPv4, отправляет сообщение о превышении времени» |
| 09.01.04-mac-and-ip-quiz | 2 | style | 'маршрутизатора' while the module, and the key of this same question, say 'роутер' | rejected: роутер/маршрутизатор swap belongs to kb#276 alignment |
| 09.01.04-mac-and-ip-quiz | 3 | style | Clumsy genitive chain 'MAC-адреса известного IP-адреса устройства назначения' (the MAC address of an IP address) | #113 → «для определения MAC-адреса устройства назначения по известному IP-адресу (IPv4 и IPv6)» |
| 09.02.10-arp-quiz | 1 | style | Garbled distractor 'поддерживает таблицу IPv4 адреса доменных имен' | #113 → «ведет таблицу сопоставлений IPv4-адресов и доменных имен» |
| 09.02.10-arp-quiz | 1 | style | Calques 'таблицу сопоставлений IPv4 для MAC-адресов' and 'MAC-адреса известных IPv4-адресов' | #113 → «вести таблицу сопоставлений IPv4- и MAC-адресов и определять MAC-адреса по известным IPv4-адресам» |
| 09.03.05-neighbor-discovery-quiz | 2 | style | Distractor 'роутер объявляет' is a verb phrase, not a message name (mistranslation of Router Advertisement); q1 of the same quiz names it properly | #113 → «сообщение «Ответ роутера» (Router Advertisement, RA)» |
| 09.03.05-neighbor-discovery-quiz | 2 | style | Distractor 'запрашивает у роутера' is a verb phrase, not a message name (mistranslation of Router Solicitation) | #113 → «сообщение «Запрос к роутеру» (Router Solicitation, RS)» |
| 09.03.05-neighbor-discovery-quiz | 3 | style | 'сообщения о приглашении соседей' is a different rendering of Neighbor Solicitation than the module's term and q1-q2 of this quiz | #113 → «сообщения ICMPv6 «Запрос соседнего узла»» |
| 09.03.05-neighbor-discovery-quiz | 3 | style | Same term mismatch in the comments ('Сообщения о приглашении соседей') | #113 → «Сообщения ICMPv6 «Запрос соседнего узла» отправляются» |
| 09.03.05-neighbor-discovery-quiz | 3 | style | Key 'групповая' while the comment of the same question and the course say 'многоадресная рассылка' | #113 → «"answer": "многоадресная"» |
| 09.04.02-quiz | 1 | style | 'исполняемый файл конфигурации' (executable configuration file) mistranslates running configuration | #113 → «файл текущей конфигурации» |
| 09.04.02-quiz | 2 | style | Missing preposition: 'связанные MAC-адресами' ('связанные с'); 'коммутационные порты' is a calque | #113 → «порты коммутатора, связанные с MAC-адресами назначения» |
| 09.04.02-quiz | 2 | style | Calque 'для завершения необходимого сопоставления' plus a spacing typo 'IP-и MAC-адресов' | #113 → «для сопоставления IP- и MAC-адресов» |
| 09.04.02-quiz | 3 | style | Command typed with an en dash ('arp –a') instead of an ASCII hyphen | #113 → «``arp -a``» |
| 09.04.02-quiz | 4 | error | Wrong key: 'netstat -r' shows the routing table, not MAC addresses. The MAC the host uses for the default gateway is in the ARP cache ('arp -a'), as answer 2's … | #113 answer key changed |
| 09.04.02-quiz | 4 | style | Comment says 'arp -a' shows the 'таблицу MAC-адресов', but in the course that term means the switch's table; arp -a shows the ARP table. There is also a stray '… | #113 → «Команда arp -a отображает таблицу ARP» |
| 09.04.02-quiz | 6 | error | Both 'correct' options say the same thing ('сопоставление IPv4-адресов и MAC-адресов' vs 'сопоставление MAC-адресов и IPv4-адресов'). Read as direction, MAC-to-… | #113 → «"answer": "ведение таблицы соответствий IPv4- и MAC-адресов"» |
| 09.04.02-quiz | 6 | style | 'МАС' spelled with Cyrillic letters | #113 → «"answer": "сопоставление IPv4-адресов и MAC-адресов"» |
| 09.04.02-quiz | 9 | style | Case error: 'кроме того, на который он его получил' should be 'на котором' (prepositional) | #113 → «кроме того, на котором он его получил» |
| 09.04.02-quiz | 10 | style | 'МАС' spelled with Cyrillic letters | #113 → «MAC-адрес назначения в IPv4-адрес источника» |
| 09.04.02-quiz | 11 | style | Typo 'напрамую', and the clause 'хост в той же сети недоступен' misstates the reason: the destination is in another network | #113 → «поскольку хост назначения находится в другой сети и напрямую недоступен» |
| 09.04.02-quiz | 14 | style | 'фрейм' while the module says 'кадр' | #113 → «в кадре запроса ARP» |
| 09.04.02-quiz | 14 | style | Broadcast MAC written in the vendor dotted notation 'FFFF.FFFF.FFFF'; the course writes it 'FF-FF-FF-FF-FF-FF', and so does the other distractor format here | #113 → «FF-FF-FF-FF-FF-FF» |
| 10.04.06-quiz | 1 | unclear | Setup mode is never introduced in the course; the stem relies on it, and «режим настройки» is easy to confuse with «режим глобальной настройки». Key itself (no … | operator (kb#275) |
| 10.04.06-quiz | 2 | style | Capitalised «Команда» mid-sentence and missing comma closing the participial phrase «настроенных на маршрутизаторе». | #114 → «настроенных на маршрутизаторе, используется команда» |
| 10.04.06-quiz | 3 | style | Typo «безопасноый»; «exec» in lower case while the same stem and the course write EXEC. | #114 → «наиболее безопасный метод защиты доступа к привилегированному режиму EXEC» |
| 10.04.06-quiz | 7 | error | Comment says that configure terminal gives access to configuration, management and troubleshooting commands. configure terminal only enters global configuration… | #114 → «Тема 10.1.0 — Привилегированный режим EXEC дает доступ ко всем командам устройства, в том числе к командам настройки, уп…» |
| 10.04.06-quiz | 11 | style | Clumsy calques: «В рамках каждого типа доступа техник пытается ввести...», «Какой режим конфигурации должен быть введен для выполнения этой задачи?»; also «техн… | #114 → «Для каждого типа доступа специалист вводит команду login. В какой режим конфигурации для этого нужно перейти?» |
| 10.04.06-quiz | 11 | unclear | Comment says login «используется для разрешения доступа»; login turns on password checking on the line (moved from the operator list after review) | #114 → «Тема 10.1.0 — Команда login включает проверку пароля при подключении через консольную линию, линии vty и aux; ее вводят …» |
| 10.04.06-quiz | 12 | style | «В частности» is a non-sequitur: the RAM sentence is not a particular case of «ОС хранится во флэш-памяти». | #114 → «В оперативной памяти хранится» |
| 10.04.06-quiz | 13 | style | Gender agreement: the option refers to «команда» (feminine) as «Он». | #114 → «Она шифрует только пароли режима линии.» |
| 10.04.06-quiz | 13 | style | Gender agreement: «Он настроен» refers to «команда»; a command is entered, not «настроен». | #114 → «Она вводится в привилегированном режиме EXEC.» |
| 10.04.06-quiz | 13 | style | «исполняемом файле конфигурации» is a mistranslation of running-config; the course calls it the current configuration. | #114 → «в файле текущей конфигурации» |
| 11.01.08-ipv4-address-structure-quiz | 1 | style | Leftover English «Host-A» in prose; the same stem names the host «Узел A» (also Q2). | #114 → «у узла A?» |
| 11.01.08-ipv4-address-structure-quiz | 3 | style | Leftover English «Host-A» in prose; the same stem names the host «Узел A» (also Q4, Q5). | #114 → «что и узел A?» |
| 11.03.08-types-of-ipv4-addresses-quiz | 1 | error | The distractor dropped «Internet» from the original: routers inside an organisation do forward packets to private destinations, so «Маршрутизаторы обычно пересы… | #114 → «Маршрутизаторы в Интернете обычно пересылают любой пакет» |
| 11.03.08-types-of-ipv4-addresses-quiz | 2 | style | Broken construction: «является причиной, по которой существуют ... и почему организации переходят» mixes two clause types. | #114 → «Исчерпание публичных адресов IPv4 — причина, по которой появились частные адреса IPv4 и организации переходят на IPv6.» |
| 11.03.08-types-of-ipv4-addresses-quiz | 2 | unclear | Distractor «Публичные IPv4 адреса могут назначаться устройствам в интрасети организации» is defensibly true: nothing forbids an organisation from using its own … | operator (kb#275) |
| 11.04.04-network-segmentation-quiz | 2 | style | Typo «результато». | #114 → «— результат чрезмерного» |
| 11.10.04-quiz | 3 | style | Case error «у маска». | #114 → «у маски 255.255.255.240» |
| 11.10.04-quiz | 5 | style | Archaic/typo form «Какою». | #114 → «Какую маску» |
| 11.10.04-quiz | 6 | style | Term «маска подсети произвольной длины» differs from the stem and the module (переменной длины, VLSM). | #114 → «маска подсети переменной длины» |
| 11.10.04-quiz | 8 | unclear | «Сколько IP-адресов доступно в сети 192.168.1.0/27?» can be read as 32 (also offered) or 30; the stem now asks for host addresses, as Q2, Q11 and Q13 do (moved … | #114 → «"question": "Сколько адресов узлов доступно в сети 192.168.1.0/27?"» |
| 11.10.04-quiz | 9 | style | Numeral agreement: «4 бит» should be «4 бита». | #114 → «доступно 4 бита?» |
| 11.10.04-quiz | 12 | style | Broken calque «Диапазон ... является: ...». | #114 → «Диапазон доступных адресов узлов в этой сети:» |
| 11.10.04-quiz | 13 | style | Numeral agreement: «4 бит узлов» should be «4 бита узлов» (twice). | #114 → «остается 4 бита узлов. 4 бита узлов соответствуют» |
| 11.10.04-quiz | 15 | style | The arithmetic chain «2^5 = 32 - 2 = 30» is false as written (it states 2^5 = 30). | #114 → «(2^5 - 2 = 32 - 2 = 30)» |
| 11.10.04-quiz | several | style | Zero-width spaces (U+200B) in comments | #114 → «» |
| 12.01.03-ipv4-issues-quiz | 2 | style | RIR name misspelled «RIPENCC». | #114 → «RIPE NCC» |
| 12.03.08-ipv6-address-types-quiz | 3 | style | Number agreement: singular subject «Локальный адрес канала ... предназначен» with plural «не являются маршрутизируемыми». | #114 → «и не является маршрутизируемым» |
| 12.03.08-ipv6-address-types-quiz | 5 | style | «Локальные адреса IPv6» drops «канала»; unique local addresses are also «локальные» and start with fc/fd, not fe80. | #114 → «Локальные адреса канала IPv6 начинаются с префикса fe80.» |
| 12.05.08-dynamic-addresing-for-ipv6-guas-quiz | 1 | style | «функция RA включает сведения» is a mistranslation; it is the RA message that carries the prefix and gateway. | #114 → «сообщение RA содержит сведения» |
| 12.05.08-dynamic-addresing-for-ipv6-guas-quiz | 2 | style | Stray trailing colon in the option text «...без сохранения состояния адресов:». | #114 → «состояния адресов» |
| 12.05.08-dynamic-addresing-for-ipv6-guas-quiz | 2 | style | Typo «сервсиов». | #114 → «сервисов» |
| 12.05.08-dynamic-addresing-for-ipv6-guas-quiz | 4 | style | Semantic slip: devices obtain DNS server addresses, not «DNS-серверов»; «информации адресации» is a calque. | #114 → «для получения адресов DNS-серверов и другой адресной информации» |
| 12.05.08-dynamic-addresing-for-ipv6-guas-quiz | 5 | style | Term «DHCPv6 без учета состояний» differs from the module and from Q2-Q4 of the same quiz. | #114 → «DHCPv6 без сохранения состояния» |
| 12.05.08-dynamic-addresing-for-ipv6-guas-quiz | 5 | style | Term «DHCPv6 с учетом состояний» differs from the module and from Q2-Q4 of the same quiz. | #114 → «DHCPv6 с сохранением состояния» |
| 12.05.08-dynamic-addresing-for-ipv6-guas-quiz | 5 | style | Garbled «SLAAC + для DHCPv6-сервера без сохранения состояния». | #114 → «SLAAC либо SLAAC с DHCPv6-сервером без сохранения состояния» |
| 12.08.05-subnet-an-ipv6-network-quiz | 2 | style | Missing preposition: «используется определения подсетей». | #114 → «используется для определения подсетей» |
| 12.08.05-subnet-an-ipv6-network-quiz | 3 | style | Typo in the address: hextets «33:44» while the distractors offer «3333» and «4444», which then do not occur in the address at all. The key (1111) is unaffected. | #114 → «2222:3333:4444:5555» |
| 12.09.04-quiz | 4 | style | Typo «на ее пределами». | #114 → «за ее пределами» |
| 12.09.04-quiz | 5 | style | Wrong government «доступность к какому-либо внешнему устройству». | #114 → «доступность какого-либо внешнего устройства» |
| 12.09.04-quiz | 10 | style | Typo «гектета». | #114 → «Три последовательных гекстета нулей» |
| 12.09.04-quiz | several | style | Zero-width spaces (U+200B) after IPv6 addresses in options | #114 → «» |
| 13.01.06-icmp-messages-quiz | 1 | style | «подтверждение узла» does not match the module term for echo-based host confirmation. | #114 → «включают доступность узла» |
| 13.01.06-icmp-messages-quiz | 2 | style | Neighbor Solicitation translated as «Обнаружение соседа»; solicitation means request, and the module calls it a request. | #114 → ««Запрос поиска соседей» (Neighbor Solicitation, NS)» |
| 13.01.06-icmp-messages-quiz | 2 | style | Router Solicitation translated as «Обнаружение маршрутизатора»; the module calls it a request to the router. | #114 → ««Запрос к маршрутизатору» (Router Solicitation, RS)» |
| 13.01.06-icmp-messages-quiz | 2 | style | Same RS mistranslation «обнаружение маршрутизатора (RS)» in the comment. | #114 → ««Запрос к маршрутизатору» (RS)» |
| 13.01.06-icmp-messages-quiz | 2 | style | RA quoted with '…' while RS in the same comment and option 3 use «…» (review suggestion) | #114 → «Маршрутизатор с поддержкой IPv6 ответит сообщением «Объявление маршрутизатора» (RA)» |
| 13.03.04-quiz | 1 | style | Typo «отбросывает». | #114 → «отбрасывает» |
| 13.03.04-quiz | 2 | unclear | The key says pinging the default gateway checks whether the host can reach hosts in other networks, but the course says a gateway ping checks the host's ability… | operator (kb#275) |
| 13.03.04-quiz | 4 | style | Mixed and wrong terms for hop limit within one comment: «ограничение перехода», «предел ... прыжка», plus «предел TTL ... равен 0». | #114 → «или предел переходов (IPv6) (1, 2, 3, 4...) для отправки последовательности команд ping. Когда маршрутизатор определяет,…» |
| 13.03.04-quiz | 6 | error | Option 2 «Он использует сообщения ICMP Source Quench.» is a stray sentence from another item, not a protocol name. It half-points to the correct answer (ICMP) a… | #114 → «NDP» |
| 13.03.04-quiz | 6 | style | Bureaucratic chain «используется ... для обеспечения отправки сообщений в случае определенных ошибок». | #114 → «IPv4 и IPv6 используют ICMP для отправки сообщений об ошибках и информационных сообщений.» |
| 13.03.04-quiz | 8 | error | Comment claims ping 127.0.0.1 checks the stack «от сетевого до физического уровня и обратно». Loopback traffic never reaches the data-link or physical layer, an… | #114 → «Ответ на этот запрос формирует сетевой уровень самого узла, а сигнал в среду передачи не отправляется.» |
| 13.03.04-quiz | 10 | style | Clumsy calque with a genitive chain: «Какое содержимое поля используется ICMPv6 для определения истечения срока действия пакета?» | #114 → «По какому полю ICMPv6 определяет, что срок действия пакета истек?» |
| 13.03.04-quiz | 10 | style | Wrong subject: «Маршрутизатор ... не имеет поля TTL»; it is the IPv6 header that has no TTL field. | #114 → «, чтобы определить, истек ли срок действия пакета: поля TTL в IPv6 нет.» |
| 13.03.04-quiz | 12 | style | Gender agreement: «Команда traceroute ... Он также указывает». | #114 → «Она также указывает» |
| 13.03.04-quiz | 13 | style | Router Solicitation translated as «Обнаружение маршрутизатора»; the module calls it a request to the router. | #114 → ««Запрос к маршрутизатору» (Router Solicitation, RS)» |
| 13.03.04-quiz | 13 | style | Neighbor Solicitation translated as «Обнаружение соседа»; the module calls it a request. | #114 → ««Запрос поиска соседей» (Neighbor Solicitation, NS)» |
| 13.03.04-quiz | 13 | error | Comment says DAD is used in IPv6 «вместо ARP» and that the NS is sent «на свой собственный IPv6-адрес». ARP's job (address resolution) is replaced by ND NS/NA, … | #114 → «Хост IPv6 выполняет обнаружение дублированного адреса (DAD), отправляя сообщение NS с собственным IPv6-адресом в качеств…» |
| 14.01.07-transportation-of-data-quiz | 4 | style | Clumsy inverted passive with instrumental agent ("Чувствительными ко времени приложениями ... используется") | #115 → «Приложения VoIP чувствительны к задержкам, поэтому используют протокол UDP.» |
| 14.04.05-port-numbers-quiz | 1 | style | Calques: "с сервера в 10.1.1.254" (server at) and "Какой из следующих элементов будет отображаться для корректной пары сокетов?" (which of the following would b… | #115 → «хочет запросить веб-службы у сервера с адресом 10.1.1.254. Как будет выглядеть правильная пара сокетов?» |
| 14.04.05-port-numbers-quiz | 3 | style | Proper name "Windows" written in lowercase | #115 → «Какая команда Windows» |
| 14.05.06-tcp-communication-process-quiz | 1 | style | Broken agreement ("допустимым исходным и конечным портами": singular adjective with plural noun) and calque "Какой из вариантов будет ..." | #115 → «Какие порты источника и назначения допустимы для узла, подключающегося к почтовому серверу?» |
| 14.05.06-tcp-communication-process-quiz | 1 | error | Wrong expansion of SMTP: it is Simple Mail Transfer Protocol, not "Transport" | #115 → «Simple Mail Transfer Protocol» |
| 14.05.06-tcp-communication-process-quiz | 2 | style | Calque "контрольными битами флагов" (control bit flags); "контрольный" is a false friend, the module says "управляющие биты"/"флаги" | #115 → «со следующими флагами» |
| 14.05.06-tcp-communication-process-quiz | 3 | error | Mistranslation: asks how many "сеансов связи" are needed to end both sessions; the intended unit is exchanges (segments), so the keyed "четыре сеанса" is factua… | #115 → «Сколько обменов необходимо для завершения обоих сеансов» |
| 14.05.06-tcp-communication-process-quiz | 3 | error | Same mistranslation in the option: counts sessions instead of exchanges (apply together with the stem fix) | #115 → «"один обмен"» |
| 14.05.06-tcp-communication-process-quiz | 3 | error | Same mistranslation in the option: counts sessions instead of exchanges (apply together with the stem fix) | #115 → «"два обмена"» |
| 14.05.06-tcp-communication-process-quiz | 3 | error | Same mistranslation in the option: counts sessions instead of exchanges (apply together with the stem fix) | #115 → «"три обмена"» |
| 14.05.06-tcp-communication-process-quiz | 3 | error | Same mistranslation in the option: counts sessions instead of exchanges (apply together with the stem fix) | #115 → «"четыре обмена"» |
| 14.05.06-tcp-communication-process-quiz | 3 | error | Same mistranslation in the option: counts sessions instead of exchanges (apply together with the stem fix) | #115 → «"пять обменов"» |
| 14.05.06-tcp-communication-process-quiz | 3 | error | Comment repeats the mistranslation ("четыре сеанса обмена") | #115 → «Для завершения обоих сеансов между двумя узлами необходимы четыре обмена:» |
| 14.05.06-tcp-communication-process-quiz | 3 | style | q3 comment mixes «Хост» and «Узел» for the same device in one list; unified on «узел» (glossary host row, kb#279) | #115 → «2. Узел B отправляет ACK.» |
| 14.07.05-udp-communication-quiz | 1 | style | Calques "UDP желателен" (desirable) and "делают ... транзакции" (make transactions) | #115 → «Почему UDP предпочтителен для протоколов, которые выполняют простые транзакции запроса и ответа?» |
| 14.07.05-udp-communication-quiz | 1 | style | Bureaucratic chain and overstatement ("делают его просто незаменимым, когда требуется протокол, осуществляющий лишь транзакции по отправке запросов и получению … | #115 → «Благодаря низким накладным расходам UDP хорошо подходит для протоколов, которые выполняют простые транзакции запроса и о…» |
| 14.07.05-udp-communication-quiz | 2 | style | Calque: "выражение" for "statement", plus officialese "в отношении ... является истинным" | #115 → «Какое утверждение о повторной сборке датаграмм UDP верно?» |
| 14.07.05-udp-communication-quiz | 3 | style | Broken agreement/calque ("Какой из следующих вариантов будет допустимыми исходным и конечным портами") and missing hyphen in "DNS серверу" | #115 → «Какие порты источника и назначения допустимы для узла, подключающегося к DNS-серверу?» |
| 14.07.05-udp-communication-quiz | 3 | style | Spelling: "Порт-источник", "Порт-назначения" (stray hyphen, capital letter mid-sentence) | #115 → «— порт источника 49152, порт назначения 53.» |
| 14.08.03-quiz | 1 | style | Genitive chain "используется для обеспечения создания сеанса" | #115 → «Какая функция транспортного уровня гарантирует установление сеанса?» |
| 14.08.03-quiz | 5 | style | Wrong case in compound: "Хост-источника" | #115 → «Хост-источник FTP» |
| 14.08.03-quiz | 7 | style | Calque of "What is one way ...": "Каким одним из указанных ниже способов" | #115 → «Каким образом протокол TCP решает эту проблему?» |
| 14.08.03-quiz | 11 | style | Mistranslation "исходного окна отправки" (reads as "initial send window"); meant is the source's send window | #115 → «постоянной корректировки окна отправки источника» |
| 14.08.03-quiz | 13 | style | Calque "услуг с низкими издержками в реализации сети"; the module term is "накладные расходы" | #115 → «используют UDP, поскольку у него низкие накладные расходы.» |
| 14.08.03-quiz | 15 | style | Option is a finite verb phrase ("Преобразует ...") while the stem "За что отвечают" and the other options need a noun phrase | #115 → «Преобразование частных IP-адресов в публичные» |
| 14.08.03-quiz | 15 | style | Calque "Существуют три основных обязанности для протоколов" | #115 → «Протоколы транспортного уровня TCP и UDP выполняют три основные функции:» |
| 14.08.03-quiz | several | style | Zero-width spaces (U+200B) in quiz text | #115 → «» |
| 15.01.04-application-presentation-and-session-quiz | 1 | style | Question ends with a period instead of a question mark | #115 → «программами, работающими на хостах?» |
| 15.01.04-application-presentation-and-session-quiz | 1 | style | Dangling gerund: "обмениваясь данными между хостами" attaches to the layer, garbling "application protocols exchanging data between hosts" | #115 → «Он обеспечивает интерфейс между протоколами приложений, которые обмениваются данными между хостами.» |
| 15.01.04-application-presentation-and-session-quiz | 3 | style | Question ends with a period instead of a question mark | #115 → «что и уровень приложений модели TCP/IP?» |
| 15.01.04-application-presentation-and-session-quiz | 4 | style | Same dangling gerund as q1 ("обмениваясь данными между хостами") | #115 → «OSI обеспечивает интерфейс между протоколами приложений, которые обмениваются данными между хостами.» |
| 15.01.04-application-presentation-and-session-quiz | 5 | style | Question ends with a period instead of a question mark | #115 → «Какая функция относится к сеансовому уровню модели OSI?» |
| 15.01.04-application-presentation-and-session-quiz | 5 | error | MT error: "dialogs" rendered as "диалоговые окна" (dialog boxes); the session layer does not create UI windows | #115 → «создает и поддерживает диалоги (сеансы) между двумя хостами» |
| 15.01.04-application-presentation-and-session-quiz | 5 | style | Term "прикладного слоя"; the course says "уровень" | #115 → «форматирование данных для прикладного уровня» |
| 15.02.05-peer-to-peer-quiz | 2 | style | Broken correlative conjunction: "как клиент, и как сервер" lacks the first "и" | #115 → «может функционировать и как клиент, и как сервер» |
| 15.02.05-peer-to-peer-quiz | 3 | style | Leftover English option "Hybrid" | #115 → «"Гибридное P2P-приложение"» |
| 15.03.05-web-and-email-protocols-quiz | 4 | style | Clumsy double "для" ("протокол для клиентов для извлечения копий") | #115 → «IMAP — протокол, с помощью которого клиенты получают копии электронных сообщений с сервера IMAP.» |
| 15.04.09-ip-addressing-services-quiz | 1 | style | DNS record type "A" is typed with Cyrillic "А" (U+0410) in q1 and q4 | #115 → «"A"» |
| 15.04.09-ip-addressing-services-quiz | 1 | style | Wrong case: "разрешения имен в адресах IPv6" (should be accusative "в адреса"); bare dash before AAAA | #115 → «Для разрешения имен в адреса IPv6 используются записи DNS типа AAAA.» |
| 15.04.09-ip-addressing-services-quiz | 2 | style | Agreement error: "разрешение имен, не входящей в его зону" | #115 → «запрос на разрешение имени, не входящего в его зону DNS» |
| 15.04.09-ip-addressing-services-quiz | 3 | unclear | Distractor "IP-адрес конечного устройства" is defensible: when a name is queried, nslookup prints the IP address of that host (an A record is "IPv4-адрес конечн… | operator (kb#275) |
| 15.05.03-file-sharing-services-quiz | 2 | style | Both directions called "загрузка", which makes the sentence self-contradictory | #115 → «в любом направлении: выгрузка с клиента на сервер или загрузка с сервера на клиент» |
| 15.06.02-quiz | 2 | style | Stray comma between subject and predicate ("index.html, представляет") | #115 → «index.html представляет» |
| 15.06.02-quiz | 2 | style | MT artefact: file name "index" translated as "индекс" | #115 → «index.html = имя файла» |
| 15.06.02-quiz | 5 | style | Latin "a" used for the Russian conjunction "а" ("сервер, a POP3") | #115 → «сервер, а POP3» |
| 15.06.02-quiz | 14 | style | Calque "трафика, доступ к которому осуществляется с веб-сервера" | #115 → «для шифрования трафика между браузером и веб-сервером» |
| 15.06.02-quiz | several | style | Zero-width spaces (U+200B) in quiz text | #115 → «» |
| 16.01.04-security-threats-and-vulnerabilities-quiz | 1 | unclear | Option "потеря данных и манипуляции с ними" (used in all 8 questions) does not match the module heading "Утечка данных и их неправомерное использование"; the he… | operator (kb#275) |
| 16.01.04-security-threats-and-vulnerabilities-quiz | 3 | style | Wrong case: "легитимными пользователи" | #115 → «когда легитимные пользователи» |
| 16.01.04-security-threats-and-vulnerabilities-quiz | 4 | style | Calque of "proprietary information": "информации, принадлежащей частной собственности" | #115 → «исследовательских данных или конфиденциальной информации компании» |
| 16.01.04-security-threats-and-vulnerabilities-quiz | 7 | style | Same calque "информации, принадлежащей частной собственности" | #115 → «записей данных или конфиденциальной информации компании» |
| 16.01.04-security-threats-and-vulnerabilities-quiz | 8 | style | Clumsy sentence: "личных данных" repeated, double "чтобы", officialese "Одним из примеров ... является" | #115 → «Пример кражи личных данных — злоумышленник выдает себя за другого человека, чтобы получить его кредитную информацию.» |
| 16.02.05-network-attacks-quiz | 1 | style | Stray comma between subject and predicate; term differs from the option "Атака типа «отказ в обслуживании»". Same comment in q5 (count covers both) | #115 → «Атака типа «отказ в обслуживании» (DoS) в случае успеха ограничивает» |
| 16.02.05-network-attacks-quiz | 2 | style | Illogical "если она успешна, использует", calque "субъект угрозы", and agreement error "субъекту ... они не имеют прав" | #115 → «Атака доступа использует известные уязвимости. В случае успеха она позволяет злоумышленнику получить доступ к ресурсам, …» |
| 16.02.05-network-attacks-quiz | 3 | style | Calque "Вредоносные атаки" (malware attacks); the option says "Атака вредоносных программ". Same sentence in q4 (count covers both) | #115 → «К атакам вредоносных программ относятся вирусы, черви и трояны.» |
| 16.02.05-network-attacks-quiz | 5 | unclear | Scenario fits two answers: an unpatched server that "отправляет большое количество вредоносных пакетов" is a classic worm infection (malware), while the key is … | operator (kb#275) |
| 16.02.05-network-attacks-quiz | 6 | style | Calque "субъект угрозы" (threat actor); the module uses "злоумышленник" | #115 → «При разведывательной атаке злоумышленник может» |
| 16.03.08-network-attack-mitigation-quiz | 3 | style | Plural "Какие соображения ... касаются" with a single-choice key; awkward calque of "considerations" | #115 → «Какой аспект политики резервного копирования касается» |
| 16.03.08-network-attack-mitigation-quiz | 3 | error | Comment says strong passwords relate to "Проверка" (verification), but the key is "Безопасность"; distractor 4 "проверка" also has no comment while the correct … | #115 → «Безопасность резервного копирования связана с использованием надежных паролей» |
| 16.03.08-network-attack-mitigation-quiz | 3 | style | Option "система хранения" (storage system) does not match the module item "Хранение" | #115 → «"хранение"» |
| 16.03.08-network-attack-mitigation-quiz | 5 | style | Calque "конечных точек" (endpoints); the module term is "оконечные устройства" | #115 → «безопасности оконечных устройств?» |
| 16.03.08-network-attack-mitigation-quiz | 5 | style | Same calque "конечная точка" in the comment | #115 → «Антивирусное программное обеспечение, работающее на оконечном устройстве (узле), — часть комплексного решения по защите …» |
| 16.05.04-quiz | 1 | style | Calque "несанкционированной связи с компьютером и от него" (communications to and from a computer) | #115 → «Какой компонент защищает компьютер от несанкционированных входящих и исходящих подключений?» |
| 16.05.04-quiz | 1 | style | Tautology from mistranslating "antivirus and antimalware software": "Антивирус и антивирусное программное обеспечение" | #115 → «Антивирусное ПО и средства защиты от вредоносных программ предотвращают заражение компьютера.» |
| 16.05.04-quiz | 2 | style | Question has no question mark | #115 → «выполнены две неудачные попытки входа?» |
| 16.05.04-quiz | 2 | style | Leftover English placeholders in prose: "(number of seconds)", "(number of attempts)" | #115 → «(число секунд) attempts (число попыток) within (число секунд)» |
| 16.05.04-quiz | 3 | style | Calque "для предоставления вопросов, связанных с вызовом и ответом" (challenge and response); also breaks the infinitive pattern of the other options | #115 → «задавать контрольные вопросы по схеме «запрос — ответ»» |
| 16.05.04-quiz | 4 | style | Missing space after period and calque "инструментом ping развертки"; the module calls fping "инструмент эхо-тестирования" | #115 → «активные адреса. Fping — инструмент эхо-тестирования» |
| 16.05.04-quiz | 5 | style | Plural "Какие преимущества" with a single-choice key | #115 → «Какое преимущество дает SSH» |
| 16.05.04-quiz | 5 | error | Comment says SSH uses stronger password "авторизацию"; it is authentication. As written, the comment on distractor 1 "Авторизация" presents authorization as an … | #115 → «более надежную парольную аутентификацию» |
| 16.05.04-quiz | 6 | style | Leftover English in option "patch-серверы" | #115 → «серверы обновлений» |
| 16.05.04-quiz | 6 | style | Missing space after period ("доступ.Система") | #115 → «доступ. Система предотвращения» |
| 16.05.04-quiz | 9 | style | MT artefact: "host" rendered as "хозяин" | #115 → «с одного узла на другой» |
| 16.05.04-quiz | 10 | style | Typo "В какому классу" | #115 → «К какому классу» |
| 16.05.04-quiz | 10 | style | Calques "неконтролируемая мощность (шум)", "полная потеря мощности"; brownouts rendered as "(отключения)" | #115 → «всплески и провалы напряжения, колебания напряжения (шум) и полное отключение электропитания» |
| 16.05.04-quiz | 11 | style | Typo "программное обеспечения" | #115 → «программное обеспечение» |
| 16.05.04-quiz | 14 | style | Calques "выполнять эхо-запросы друг с другом" and "Какие параметры могут выполнить эту задачу?" | #115 → «не могут отправлять друг другу эхо-запросы. С помощью каких настроек можно решить эту задачу?» |
| 16.05.04-quiz | 14 | style | Ambiguous "настройки Mac" (Apple Mac?); the comment explains it as MAC-address settings | #115 → «"настройки MAC-адресов"» |
| 17.01.06-devices-in-a-small-network-quiz | 1 | style | Wrong preposition: "в предприятиях" (should be "на предприятиях") | #115 → «на предприятиях малого бизнеса» |
| 17.01.06-devices-in-a-small-network-quiz | 3 | style | Stray semicolon at the end of the option "схему назначения IP-адресов;" | #115 → «схему назначения IP-адресов» |
| 17.01.06-devices-in-a-small-network-quiz | 4 | style | "отдельных точек отказа" is a calque; the module term is "единые точки отказа" | #115 → «единых точек отказа» |
| 17.02.04-small-network-applications-and-protocols-quiz | 1 | style | Stem ends with "(верны два варианта)." and no question mark | #115 → «обеспечивают доступ к сети? (верны два варианта)» |
| 17.02.04-small-network-applications-and-protocols-quiz | 2 | style | Bureaucratic chain "для установления сетевого подключения удаленного доступа к устройству" | #115 → «используются для удаленного доступа к устройству?» |
| 17.02.04-small-network-applications-and-protocols-quiz | 2 | style | Same chain in the comment ("для установки сетевого подключения удаленного доступа к устройству") | #115 → «используются для удаленного доступа к устройству» |
| 17.03.04-scale-to-larger-networks-quiz | 1 | style | Calque "Элементы для масштабирования в более крупную сеть включают"; also "инвентаризация устройств" vs module "реестр устройств" | #115 → «Для масштабирования сети нужны бюджет, реестр устройств, сетевая документация и анализ трафика» |
| 17.03.04-scale-to-larger-networks-quiz | 2 | style | Participial phrase not closed by a comma ("проходящего через сеть может выявить") | #115 → «проходящего через сеть, может выявить Wireshark» |
| 17.03.04-scale-to-larger-networks-quiz | 3 | style | Participial phrase not closed by a comma ("на узле особенно полезно") | #115 → «использующих сетевые службы на узле, особенно» |
| 17.06.05-troubleshooting-methodologies-quiz | 2 | style | Mistranslation "После устранения неполадок" (after fixing) contradicts the conclusion that the switch still has to be replaced; meant is "after troubleshooting" | #115 → «Проведя поиск неполадок, техник приходит к выводу» |
| 17.06.05-troubleshooting-methodologies-quiz | 3 | style | Calque "использует привилегированную команду EXEC ... для захвата вывода" | #115 → «вводит в привилегированном режиме EXEC команду ``debug ip icmp``, чтобы получать вывод роутера в режиме реального времен…» |
| 17.06.05-troubleshooting-methodologies-quiz | 4 | style | Missing comma before the gerund phrase and odd "эхо-запросы до хоста" | #115 → «проверяет связь, отправляя эхо-запросы хосту назначения» |
| 17.08.05-quiz | 1 | style | Plural "Какие соображения ... будут" with a single-choice key | #115 → «Какое соображение по проектированию сетей будет важнее» |
| 17.08.05-quiz | 1 | style | Missing hyphen in "бизнес ресурсов"; "избыточность портов", "избыточные интернет-каналы" switch away from the term "резервирование" used in the same sentence an… | #115 → «Брандмауэр необходим для защиты бизнес-ресурсов. Резервирование обычно не встречается в очень небольших компаниях, но не…» |
| 17.08.05-quiz | 2 | style | Missing space after period ("устройствами.Устройства") | #115 → «установленными устройствами. Устройства» |
| 17.08.05-quiz | 6 | style | Only the correct option carries the preposition "на" ("на линию консоли"), which gives the answer away; the other options are bare nouns | #115 → «линия консоли"» |
| 17.08.05-quiz | 7 | style | Missing separator: "сетьбюджет" | #115 → «сеть; бюджет» |
| 17.08.05-quiz | 9 | error | Factually wrong: Apple macOS does self-assign a 169.254.0.0/16 link-local address when DHCP fails ("Self-Assigned IP"), and Linux can (avahi-autoipd, NetworkMan… | operator (kb#275) |
| 17.08.05-quiz | 10 | style | Calque "в качестве резервной копии" (backup copy) for a backup router | #115 → «в качестве резервного можно использовать второй роутер» |
| 17.08.05-quiz | 11 | style | Calque "принимать во внимание, когда в сети происходит какое-либо отклонение" | #115 → «Это позволяет администратору замечать любые отклонения от установленной нормы» |
| 17.08.05-quiz | 13 | style | Calque of "on both routers and switches": "на обоих роутерах и коммутаторах" | #115 → «и на роутерах, и на коммутаторах» |
| 17.08.05-quiz | 15 | style | Clumsy double "при ... при" | #115 → «Какой фактор следует учитывать при выборе устройств для малой сети?» |
| 17.08.05-quiz | several | style | Zero-width space (U+200B) in quiz text | #115 → «» |

## Findings: Exams

| File | Q | Sev | Issue | Fix |
|---|---|---|---|---|
| 01-03-exam | 1 | style | Calque: «с поддерживаемой сетевой архитектурой» renders "supporting network architecture" with the wrong (passive) participle; the matched items are characteris… | #117 → «с характеристиками сетевой архитектуры, которые их обеспечивают» |
| 01-03-exam | 3 | error | Answer 4 is the explanation text pasted as an option (and has no comment). It is a true description of powerline networking, so a second correct statement is ma… | #117 → «"answer": "беспроводные точки доступа используют адаптеры сети электропитания для передачи данных по домашней локальной …» |
| 01-03-exam | 4 | style | Typo: stray period in option «надежность.» (no other option ends with a period). | #117 → «"answer": "надежность"» |
| 01-03-exam | 5 | error | Stem says not all options are used, but all four options (DSL, dial-up, satellite, cable) are matched; the note misleads the learner into looking for a distract… | #117 → «Интернету.» |
| 01-03-exam | 5 | style | Option «подключение по телефонной линии» (dial-up) is ambiguous: DSL is also a connection over a phone line (answer 1 says so). The module term is «телефонный к… | #117 → «"option": "телефонный коммутируемый доступ"» |
| 01-03-exam | 12 | error | Comment is garbled MT and factually wrong: it says copy startup-config running-config «не изменяет файл текущей конфигурации, т.к. конфигурационный файл хранитс… | #117 → «Надежнее всего отменить все несохраненные изменения, перезагрузив маршрутизатор командой reload без сохранения текущей к…» |
| 01-03-exam | 16 | style | Calque «восстанавливают привилегированный режим EXEC» ("return the user to"); command name capitalised as «End». | #117 → «Команда end и комбинация Ctrl-Z возвращают пользователя в привилегированный режим EXEC» |
| 01-03-exam | 19 | style | Typo: «Terra Term» instead of «Tera Term». | #117 → «Tera Term» |
| 01-03-exam | 20 | style | Term «режим глобального конфигурирования» differs from the module term «режим глобальной конфигурации» (also used in q23 of this exam). | #117 → «режим глобальной конфигурации» |
| 01-03-exam | 23 | error | Stem says not all options are used, but all three options (user EXEC, privileged EXEC, global configuration) are matched by two answers each. | #117 → «режимом ОС» |
| 01-03-exam | 30 | style | Tautology «уровень сетевого доступа к сети»; the module term is «уровень сетевого доступа». | #117 → «уровень сетевого доступа» |
| 01-03-exam | 30 | unclear | Distractor «данные передаются с межсетевого уровня на уровень сетевого доступа» is wrong only under strict PDU naming (data = application-layer PDU). In plain R… | operator (kb#275) |
| 01-03-exam | 32 | style | Run-on sentence: missing conjunction between two predicates («…продуктов и услуг известна благодаря…»). | #117 → «продуктов и услуг, а также известна» |
| 01-03-exam | 33 | style | Typo: missing space after colon «TCP/IP:данные». | #117 → «TCP/IP: данные» |
| 01-03-exam | 34 | style | Typo: «ППри». | #117 → «При» |
| 01-03-exam | 37 | style | Stray period and missing hyphen: «Ethernet заголовок.» while the sibling items read «TCP-заголовок», «IP-заголовок». | #117 → «добавляется Ethernet-заголовок» |
| 01-03-exam | 39 | style | Calque: «правильно идентифицируют адресацию, которую сервер B будет генерировать в процессе» ("correctly identify the addressing that server B will generate in … | #117 → «правильно описывают адресацию, которую использует сервер B» |
| 01-03-exam | 40 | style | Correct answer uses «тайм-аут ответа», but the module term is «время ожидания ответа» (q29 of this exam uses the module term as a distractor). | #117 → «"answer": "время ожидания ответа"» |
| 01-03-exam | 45 | error | Distractor lost the word «только» ("only required … on remote networks"). As written it is true: protocols are needed for exchange in remote networks too. The q… | #117 → «сетевые протоколы необходимы только для обмена сообщениями между устройствами в удалённых сетях» |
| 01-03-exam | 46 | style | Case error: «одним провайдеров». | #117 → «одним провайдером» |
| 01-03-exam | 47 | style | Calque «в интернет-сетях» ("internetworks"). | #117 → «по которому сообщения передаются между сетями» |
| 01-03-exam | 47 | style | Broken word order: the relative clause attaches to «роутер» («роутер, по которому пойдет сообщение»), so the sentence means "the router along which the message … | #117 → «Маршрутизатор используется для определения пути, по которому пойдет сообщение в сети.» |
| 01-03-exam | 49 | style | «Режим общих настроек» is a mistranslation of "global configuration mode"; the module and the options of this question use «режим глобальной конфигурации». The … | #117 comments rewritten: «Чтобы войти в режим глобальной конфигурации, в привилегированном режиме EXEC нужно ввести команду configure terminal или…» |
| 01-03-exam | 50 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Экстранет позволяет организации предоставить защищенный доступ к своим данным лицам, которые работают в других организац…» |
| 01-03-exam | 51 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Облачные вычисления позволяют хранить личные файлы на серверах в Интернете и получать к ним доступ в любом месте, в любо…» |
| 01-03-exam | 52 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «В одноранговой сети компьютеры могут одновременно выполнять роли и клиента, и сервера. Облако — это хранение данных и ра…» |
| 01-03-exam | 53 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «В модели «клиент/сервер» серверное программное обеспечение работает на выделенных компьютерах, а клиенты запрашивают у н…» |
| 01-03-exam | 54 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Сети малого офиса и домашнего офиса (SOHO) позволяют людям работать из дома или из небольшого удаленного офиса. Интернет…» |
| 01-03-exam | 55 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Сеть по линиям электропитания использует существующую электропроводку: устройства подключаются к локальной сети через ад…» |
| 01-03-exam | 56 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Политика качества обслуживания (QoS) позволяет сетевым устройствам управлять потоком трафика и при перегрузке сети отдав…» |
| 01-03-exam | 57 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Термин «интранет» обозначает частные сети LAN и WAN, принадлежащие конкретной организации. Интернет — это объединение ча…» |
| 01-03-exam | 58 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Согласно концепции BYOD пользователи могут применять личные устройства для доступа к информации в корпоративной сети или…» |
| 01-03-exam | 59 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «IP-адреса источника и назначения добавляются в заголовок пакета на сетевом уровне (уровень 3). На канальном уровне добав…» |
| 01-03-exam | 60 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Номера портов источника и назначения добавляются в заголовок сегмента на транспортном уровне (уровень 4). На сетевом уро…» |
| 01-03-exam | 60 | unclear | Port numbers are never introduced in the module 01-03 lecture texts (they belong to the transport-layer module), so the question can only be answered by elimina… | operator (kb#275) |
| 01-03-exam | 61 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Данные создаются на уровне приложений. Нижележащие уровни инкапсулируют их, добавляя свои заголовки: транспортный — заго…» |
| 01-03-exam | 62 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «IP-адреса источника и назначения добавляются в заголовок пакета на сетевом уровне (уровень 3). На канальном уровне добав…» |
| 01-03-exam | 63 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «MAC-адреса источника и назначения добавляются в заголовок кадра на канальном уровне (уровень 2). На транспортном уровне …» |
| 01-03-exam | 64 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «Номера портов источника и назначения добавляются в заголовок сегмента на транспортном уровне (уровень 4). На сетевом уро…» |
| 01-03-exam | 64 | unclear | Port numbers are never introduced in the module 01-03 lecture texts (they belong to the transport-layer module), so the question can only be answered by elimina… | operator (kb#275) |
| 01-03-exam | 65 | error | All wrong-answer comments are a copy of q49's explanation about configure terminal and user EXEC mode; they have nothing to do with this question. Replacement c… | #117 comments rewritten: «MAC-адреса источника и назначения добавляются в заголовок кадра на канальном уровне (уровень 2). На сетевом уровне добав…» |
| 04-07-exam | 1 | style | Term «сети широкого охвата» (long-haul networks) differs from the module term «сети дальней связи». | #117 → «сети дальней связи» |
| 04-07-exam | 2 | style | The stem calls throughput «пропускная способность» (bandwidth). The module defines these as different things, and q45/q46 of this exam test exactly that differe… | #117 → «фактическая производительность оказалась ниже пропускной способности канала. Какие факторы могли повлиять на производите…» |
| 04-07-exam | 2 | style | The comment uses «пропускная способность» for throughput and «полоса пропускания» for bandwidth, which contradicts the module terminology. | #117 → «Производительность обычно ниже пропускной способности физических каналов связи по нескольким причинам» |
| 04-07-exam | 2 | style | Case error: «к Интернет». | #117 → «сети WAN к Интернету"» |
| 04-07-exam | 3 | style | Clumsy calque «соблюдения больших мер безопасности». | #117 → «более строгих мер безопасности» |
| 04-07-exam | 5 | style | Spelling and calque: «не экранированного» (one word) and «медного провода с витой парой» (literal "unshielded twisted-pair copper wire"); the module term is «не… | #117 → «Что вызывает перекрестные помехи в кабельных парах в сети на основе неэкранированной витой пары (UTP)?» |
| 04-07-exam | 5 | style | Wrong collocation «производится магнитное поле» (calque of "is produced"). | #117 → «создается магнитное поле» |
| 04-07-exam | 7 | style | Grammar: «чувствительны двум видам помех: электромагнитные помехи (ЭМП) или радиочастотные (РЧП)» (missing preposition, nominative after colon, «или» presented … | #117 → «Электрические импульсы чувствительны к электромагнитным (ЭМП) и радиочастотным (РЧП) помехам.» |
| 04-07-exam | 12 | style | Comment refers to a figure that is not there («Строка заголовка», «зона, помеченная словом «данные»») and reads as a literal translation. | #117 → «Заголовок содержит управляющую информацию, например адреса, а поле данных — заголовок IP-пакета, PDU транспортного уровн…» |
| 04-07-exam | 13 | style | Agreement error: «структура кадра и поля, содержащихся в заголовке, может отличаться». | #117 → «структура кадра и поля, содержащиеся в заголовке, могут отличаться» |
| 04-07-exam | 14 | style | Garbled sentence: «Структура «звезда» использует центральное устройство в звездообразной топологии, которая подключается к другим устройствам точечной топологии… | #117 → «В топологии «звезда» центральный узел связан с периферийными узлами по каналам «точка-точка»» |
| 04-07-exam | 14 | style | «Точечная топология» is not the module term for point-to-point (and the option itself reads «точка-точка»). | #117 → «Топология «точка-точка»» |
| 04-07-exam | 15 | style | Distractor «CEF» (Cisco Express Forwarding) is a vendor-specific technology that is not in the course; replace it with a vendor-neutral feature that also does n… | #117 → «"answer": "автоопределение скорости и дуплексного режима"» |
| 04-07-exam | 15 | style | Comment explains the vendor-specific CEF; change it to match the replacement distractor. | #117 → «Автоопределение согласует скорость и дуплексный режим порта и не используется для проверки полученных кадров» |
| 04-07-exam | 15 | style | Typo: stray «и» in «Кадр Ethernet и отбрасывается». | #117 → «Кадр Ethernet отбрасывается» |
| 04-07-exam | 15 | style | Garbled phrase «определяет типы кабельных прямых или перекрестных кабелей». | #117 → «определяет тип подключенного кабеля: прямой или перекрестный» |
| 04-07-exam | 16 | style | The stem asks for a «тип среды передачи данных», but the options are duplex modes and access methods. «Проверка среды» is not the module concept, which is media… | #117 → «Какой режим связи не требует управления доступом к среде на канальном уровне?» |
| 04-07-exam | 16 | style | Same term problem in the comment: «не требует проверки среды». | #117 → «и, следовательно, не требует управления доступом к среде» |
| 04-07-exam | 17 | style | Elliptical, ungrammatical option: «к центральному промежуточному, которое … к другим центральным промежуточным» (nouns missing). | #117 → «к центральному промежуточному устройству, которое, в свою очередь, подключается к другим центральным промежуточным устро…» |
| 04-07-exam | 18 | style | Calque «LLC составляет информацию в блоки данных и определяет, какой протокол … используется в блоке данных». | #117 → «LLC помещает в кадр информацию о том, какой протокол сетевого уровня в нем используется» |
| 04-07-exam | 18 | style | LLC named «управление логическим каналом»; the lecture term is «управление логическим соединением» (06.01 README:32), as in Q10 and Q36 | #117 → «Управление логическим соединением (LLC)» |
| 04-07-exam | 19 | style | Garbled sentences: «…является детерминированным, а не доступом к сетям на основе конкуренции», «управляемые сети доступа, такие как устаревшие Token Ring». | #117 → «Контролируемый доступ является детерминированным, в отличие от конкурентного. Поскольку каждое устройство получает свое …» |
| 04-07-exam | 20 | style | Calqued word order: «В поле контрольной последовательности кадра (Frame Check Sequence) окончание содержит значение CRC». | #117 → «Окончание кадра содержит поле контрольной последовательности кадра (FCS) со значением CRC» |
| 04-07-exam | 22 | style | Wrong expansion of CSMA/CD: «Вероятностный сетевой протокол канального уровня с обнаружением коллизий». | #117 → «Множественный доступ с прослушиванием несущей и обнаружением коллизий (CSMA/CD)» |
| 04-07-exam | 24 | unclear | Distractor 2 («jam-сигнал приводит к тому, что только устройства, вызвавшие коллизию, выполняют алгоритм отката») is arguably true. Under IEEE 802.3 only the st… | operator (kb#275) |
| 04-07-exam | 26 | style | Agreement error: «к порту, подключённого к сети». | #117 → «к порту, подключенному к сети» |
| 04-07-exam | 26 | error | The comment attributes port-based buffering behaviour (per-port queues, head-of-line delay) to «буферизация памяти» right after describing shared memory, so it … | #117 → «При буферизации на основе портов кадры хранятся в очередях» |
| 04-07-exam | 28 | style | Agreement error: «вариациями сквозной коммутации, при котором». | #117 → «сквозной коммутации, при которой пересылка» |
| 04-07-exam | 30 | style | Mixed script: «МАС» typed in Cyrillic letters. | #117 → «после прочтения MAC-адреса назначения» |
| 04-07-exam | 31 | error | Factually wrong: «Для этого им необходима максимально возможная скорость» implies full duplex requires maximum speed. In fact the switches autonegotiate full du… | #117 → «Они выбирают максимальную скорость, общую для обоих, а функция Auto-MDIX включена по умолчанию, поэтому менять кабель не…» |
| 04-07-exam | 35 | style | Typo: «подержания». | #117 → «поддержания» |
| 04-07-exam | 35 | style | Mixed script: «МАС-адресов» typed in Cyrillic letters. | #117 → «MAC-адресов» |
| 04-07-exam | 36 | style | Case error: «подуровень управление логической связью (LLC)» (genitive needed; answer 2 has it right). | #117 → «одуровень управления логическим соединением (LLC)» |
| 04-07-exam | 38 | style | «Коммутация без буферизации пакетов / с буферизацией» is not the module terminology (сквозная коммутация / коммутация с промежуточным хранением, used in q27, q2… | #117 → «сквозной коммутации вместо коммутации с промежуточным хранением» |
| 04-07-exam | 38 | style | Same non-module terms in the comment («без буферизации», «с буферизацией»). | #117 → «Сквозная коммутация обеспечивает меньшую задержку, что важно для приложений, выполняющих высокопроизводительные вычислен…» |
| 04-07-exam | 38 | style | Mixed script: «МАС» typed in Cyrillic letters. | #117 → «MAC-адреса источника кадра» |
| 04-07-exam | 41 | style | Rollover cable is called «инверсный» here; the module calls it «консольный (rollover)». | #117 → «— консольный» |
| 04-07-exam | 41 | style | Same term in the comment («Инверсный кабель (rollover)»); in the bank copy the sentence also starts with a lowercase letter. | #117 → «Консольный кабель (rollover)» |
| 04-07-exam | 43 | style | English abbreviations «EMI/RFI» in prose; the module and this question's comment use ЭМП/РЧП. | #117 → «ограниченная восприимчивость к ЭМП и РЧП» |
| 04-07-exam | 44 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Модуляция — процесс, при котором одна волна изменяет другую (несущую), например ее амплитуду, частоту или фазу. Инкапсул…» |
| 04-07-exam | 45 | style | Missing comma before the relative clause: «емкость с которой». | #117 → «описывает возможности среды по передаче данных?» |
| 04-07-exam | 45 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Пропускная способность — количественная характеристика, отражающая возможности передачи данных по конкретной среде. Прои…» |
| 04-07-exam | 46 | style | Question ends with a period instead of a question mark. | #117 → «промежуток времени?"» |
| 04-07-exam | 46 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Производительность — это количество битов, передаваемых по среде за определенный период времени. Пропускная способность …» |
| 04-07-exam | 47 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Задержка — время, необходимое для доставки данных из одной точки в другую. Пропускная способность, производительность и …» |
| 04-07-exam | 48 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Полезная пропускная способность — объем полезных данных, передаваемых за определенный период времени. Она равна производ…» |
| 04-07-exam | 49 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «По медному кабелю сигналы передаются в виде электрических импульсов, по оптоволоконному — в виде световых импульсов, а б…» |
| 04-07-exam | 50 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «По оптоволоконному кабелю сигналы передаются в виде световых импульсов, по медному — в виде электрических импульсов, а б…» |
| 04-07-exam | 51 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Микроволновые сигналы передаются по беспроводной среде. По медному кабелю передаются электрические импульсы, по оптоволо…» |
| 04-07-exam | 52 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Подуровень MAC управляет сетевой платой и другим оборудованием, отвечающим за отправку и получение данных, и добавляет к…» |
| 04-07-exam | 52 | style | Answer 1 says «концевик», while the question's own comment and the 06.03 lecture say «окончание» (review suggestion) | #117 → «реализует окончание кадра для обнаружения ошибок передачи» |
| 04-07-exam | 53 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Подуровень LLC помещает в кадр информацию о том, какой протокол сетевого уровня используется, и тем самым позволяет IPv4…» |
| 04-07-exam | 54 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Подуровень MAC управляет сетевой платой, отвечающей за отправку и получение данных, и обеспечивает контроль доступа, поз…» |
| 04-07-exam | 55 | style | Clumsy calque: «если коммутатор получает кадр и имеет MAC-адрес источника в таблице MAC-адресов». | #117 → «если коммутатор получит кадр, MAC-адрес источника которого уже есть в таблице MAC-адресов» |
| 04-07-exam | 55 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Если MAC-адрес источника уже есть в таблице MAC-адресов, коммутатор обновляет таймер этой записи. Коммутаторы не рассыла…» |
| 04-07-exam | 56 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Кадр с широковещательным MAC-адресом FF-FF-FF-FF-FF-FF коммутатор пересылает через все порты, кроме входящего. Записи та…» |
| 04-07-exam | 57 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Сетевая плата сравнивает MAC-адрес назначения кадра со своим MAC-адресом. Если адреса не совпадают и кадр не является ши…» |
| 04-07-exam | 58 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Кадр с MAC-адресом многоадресной рассылки (начинается с 01-00-5E) коммутатор пересылает через все порты, кроме входящего…» |
| 04-07-exam | 59 | error | All wrong-answer comments are a copy of q43's fiber-optic explanation and have nothing to do with this question. Replacement comment written from the module tex… | #117 comments rewritten: «Кадр с широковещательным MAC-адресом FF-FF-FF-FF-FF-FF принимается и обрабатывается каждым устройством в локальной сети.…» |
| 04-07-exam | several | style | LLC named «управление логической связью»; the lecture term is «управление логическим соединением» (06.01 README:32) | #117 → «управления логическим соединением (LLC)» |
| 04-07-exam | several | style | LLC named «управление логической связью»; the lecture term is «управление логическим соединением» (06.01 README:32) | #117 → «управление логическим соединением)» |
| 08-10-exam | 2 | style | Broken genitive chain: «ситуаций отсутствия или неупорядоченных пакетов» (отсутствия of what?) | #118 → «для обработки ситуаций, когда пакеты теряются или приходят не по порядку» |
| 08-10-exam | 3 | style | Agreement error: «публичных IPv6-адреса» should be genitive plural | #118 → «публичных IPv6-адресов» |
| 08-10-exam | 3 | style | Typo «отстутствуют» | #118 → «отсутствуют» |
| 08-10-exam | 4 | style | Wrong reflexive: «роутер проверяет свой заголовок» says the router checks its own header, not the packet header | #118 → «проверяет заголовок пакета» |
| 08-10-exam | 4 | unclear | Route metric is not covered anywhere in the course; the question cannot be answered from modules 1-10 | operator (kb#275) |
| 08-10-exam | 5 | error | Missing sentence break makes the comment claim that addressing, encapsulation, routing and de-encapsulation are data-link functions; also «декапсуляция» vs cour… | #118 → «деинкапсуляция. Обнаружение ошибок» |
| 08-10-exam | 6 | style | Calque «для производственной сети» (production network) reads as "industrial network"; bureaucratic chain | #118 → «на коммутаторе в рабочей сети» |
| 08-10-exam | 6 | style | Calque «пакеты, возникающие в коммутаторе» (originating from the switch) | #118 → «созданные самим коммутатором» |
| 08-10-exam | 6 | style | Calque «пакеты, которые могут возникнуть в нем» | #118 → «пересылать в удаленные сети пакеты, созданные им самим» |
| 08-10-exam | 9 | unclear | Distractor «невысокие требования в отношении обработки контрольных сумм» is defensible: IPv6 has no header checksum, and the question's own comment lists «отсут… | operator (kb#275) |
| 08-10-exam | 12 | error | Comment claims a loopback ping verifies the NIC and drivers; also mistranslation «главное устройство» (host) and «проверка линии» | #118 → «При проверке loopback пакеты не покидают узел и возвращаются ему же, поэтому она не дает сведений о подключении к другим…» |
| 08-10-exam | 13 | style | Clumsy «маршруты от источника C и L»: C and L are route source codes | #118 → «маршруты с кодами C и L» |
| 08-10-exam | 14 | style | Mistranslation «узлы должны соответствовать … таблице» (hosts must maintain a table) | #118 → «должны вести собственную локальную таблицу маршрутизации» |
| 08-10-exam | 14 | style | Agreement error «к сети, к которому подключён узел» | #118 → «к которой подключён узел» |
| 08-10-exam | 18 | style | «ARР» is spelled with a Cyrillic «Р» (U+0420), so the protocol name differs from «ARP» in answer 2 and is not searchable | #118 → «ARP» |
| 08-10-exam | 19 | style | Broken government «будет отвечать одноадресный кадр» and MT chain «пару IP-адресов назначения и MAC-адресов для продолжения процесса инкапсуляции для передачи д… | #118 → «ответит одноадресным кадром, содержащим его MAC-адрес. Так исходный хост-отправитель узнает, какой MAC-адрес соответству…» |
| 08-10-exam | 20 | style | Calque «отправляет команду … на ПК» (issues the command) | #118 → «выполняет на ПК команду `arp -d *`» |
| 08-10-exam | 20 | style | Same calque «Отправка команды»; the command is written with an en dash («–d»), which is not a valid option | #118 → «Команда arp -d *, выполненная на ПК, очищает кэш ARP» |
| 08-10-exam | 22 | style | Term and case: «Объявления соседнего узла» (genitive) and the module calls NA «Ответ соседнего узла»; the comment of this question also says «Ответ соседнего уз… | #118 → ««Ответ соседнего узла»» |
| 08-10-exam | 22 | style | Broken construction «используется путем отправки сообщений с «Запрос…»» | #118 → «используется протокол обнаружения соседей ICMPv6 с сообщениями «Запрос соседнего узла» и «Ответ соседнего узла»» |
| 08-10-exam | 28 | style | Imperative «Выключите и снова включите…» turns the explanation into an instruction; «у которого была выдана команда» is a calque | #118 → «Если выключить и снова включить питание устройства, на котором введена команда banner motd, баннер тоже отобразится, но …» |
| 08-10-exam | 30 | unclear | Router boot stages (POST, bootstrap, locating the OS and startup-config) are not covered in the course | operator (kb#275) |
| 08-10-exam | 33 | unclear | Setup mode after a missing startup-config is not covered in the course | operator (kb#275) |
| 08-10-exam | 35 | error | Comment says the command «шифрует все входящие … соединения telnet»; it does not encrypt Telnet, it permits only SSH | #118 → «Команда transport input ssh, введенная в режиме настройки линий vty (виртуальных терминальных линий), разрешает удаленно…» |
| 08-10-exam | 36 | style | Vendor leftover www.cisco.com in the stem (assets/4.png also shows «tracert www.cisco.com»; the image needs a separate edit) | #118 → «на удаленный веб-сервер» |
| 08-10-exam | 36 | style | Garbled MT: «первым обнаружен IP-адрес прыжка по умолчанию» (hop = переход; meant: default gateway) | #118 → «Когда узел отправляет пакеты на адрес за пределами своей локальной сети, первым на их пути оказывается шлюз по умолчанию» |
| 08-10-exam | 37 | error | Stem says «(используются НЕ все варианты)», but all 4 options are matched to the 4 items | #118 → «доступной в этом режиме» |
| 08-10-exam | 41 | error | Comment says the startup config is copied from RAM; it is the running config that is copied and saved as the startup config | #118 → «копирует файл текущей конфигурации из оперативной памяти в NVRAM и сохраняет его как файл загрузочной конфигурации» |
| 08-10-exam | 42 | style | Calque «адрес кадра в канале передачи данных удалённого узла» (data-link frame address) | #118 → «адрес канального уровня (MAC-адрес) удалённого узла назначения» |
| 08-10-exam | 43 | style | Clumsy calque «Для предотвращения, но не облегчения отравления…» | #118 → «Ручная настройка статических записей ARP помогает предотвратить отравление кэша ARP и спуфинг MAC-адресов, а не способст…» |
| 08-10-exam | 44 | error | Comment is unrelated to the question (talks about show ip interface brief and R1/R2 interfaces) and has a typo «каждомроутере» | #118 → «Поле «Дифференцированные услуги» (DS) — 8-битное поле, которое используется для определения приоритета каждого пакета. I…» |
| 08-10-exam | 45 | error | The same unrelated comment (show ip interface brief, R1/R2 interfaces) is attached to every wrong answer of Q45-Q66 (74 copies); fix blanks it, per-question exp… | #118 → «» |
| 08-10-exam | 45 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Поле «IP-адрес источника» содержит 32-битный IPv4-адрес интерфейса устройства, отправившего пакет. IP-адрес назначения —…» |
| 08-10-exam | 46 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Повреждение заголовка IPv4 обнаруживают по полю «Контрольная сумма заголовка»; маршрутизатор пересчитывает его при каждо…» |
| 08-10-exam | 47 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «IP-адрес назначения может быть одноадресным, многоадресным или широковещательным, тогда как адрес источника всегда индив…» |
| 08-10-exam | 48 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Поле «Время жизни» (TTL) ограничивает время нахождения пакета в сети: каждый маршрутизатор уменьшает его значение на еди…» |
| 08-10-exam | 49 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Значение 0100 всегда содержится в 4-битном поле «Версия» пакета IPv4. IP-адрес источника — 32-битное поле, а поля «Прото…» |
| 08-10-exam | 50 | error | Wrong key: timestamped entries that are purged after a timeout make mappings disappear; it is static entries that stay in memory longer | #118 key → answer 2 |
| 08-10-exam | 50 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Дольше всего в памяти остаются статические записи, введенные в таблицу ARP вручную: срок их действия не истекает. Динами…» |
| 08-10-exam | 51 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Зафиксировать MAC-адрес часто используемого сервера в таблице ARP позволяет статическая запись, введенная вручную: срок …» |
| 08-10-exam | 52 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Чтобы отправить пакет в удаленную сеть, узел с помощью ARP узнает MAC-адрес шлюза по умолчанию и указывает его в кадре к…» |
| 08-10-exam | 53 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «ARP-запрос обрабатывают все сетевые адаптеры Ethernet в локальной сети, потому что он отправляется на широковещательный …» |
| 08-10-exam | 54 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Ответ получает только отправитель запроса, потому что в кадре ARP-запроса указан его MAC-адрес источника: на этот адрес …» |
| 08-10-exam | 55 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Коммутатор рассылает ARP-запрос через все порты, кроме входящего, потому что кадр адресован на широковещательный MAC-адр…» |
| 08-10-exam | 56 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Значение 0x806 в поле «Тип» сообщает принимающему сетевому адаптеру, что данные кадра нужно передать процессу ARP. Широк…» |
| 08-10-exam | 57 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Service используют адрес того интерфейса маршрутизатора, который подкл…» |
| 08-10-exam | 58 | style | Typo in the CLI prompt «BldgA (config) -if) #» | #118 → «(config-if)» |
| 08-10-exam | 58 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Medical используют адрес того интерфейса маршрутизатора, который подкл…» |
| 08-10-exam | 59 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Registrar используют адрес того интерфейса маршрутизатора, который под…» |
| 08-10-exam | 60 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Manager используют адрес того интерфейса маршрутизатора, который подкл…» |
| 08-10-exam | 61 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Store используют адрес того интерфейса маршрутизатора, который подключ…» |
| 08-10-exam | 62 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Store используют адрес того интерфейса маршрутизатора, который подключ…» |
| 08-10-exam | 63 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Service используют адрес того интерфейса маршрутизатора, который подкл…» |
| 08-10-exam | 64 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Medical используют адрес того интерфейса маршрутизатора, который подкл…» |
| 08-10-exam | 65 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Registrar используют адрес того интерфейса маршрутизатора, который под…» |
| 08-10-exam | 66 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «В качестве шлюза по умолчанию узлы локальной сети Payroll используют адрес того интерфейса маршрутизатора, который подкл…» |
| 08-10-exam | 24, 26 | style | «МАС» typed in Cyrillic letters (found by the second reviewer) | #118 → «MAC-адрес» |
| 08-10-exam | 52–56 | style | MT artefact: distractor «ответы ARP транслируются по сети» renders "broadcast" as «транслируются» (moved from the operator list after review) | #118 → «ответы ARP рассылаются широковещательно, когда узел получает запрос ARP» |
| 11-13-exam | 3 | style | Calque «обеспечить роутер пятью соединёнными сетями» (provide a router with five connected networks) | #118 → «чтобы получить подсети для пяти сетей, подключенных к маршрутизатору» |
| 11-13-exam | 3 | style | Lost superscript: the power renders as «2 n» | #118 → «Формула 2^n, где» |
| 11-13-exam | 4 | style | Lost superscript: the power renders as «2 6 = 64» | #118 → «поскольку 2^6 = 64» |
| 11-13-exam | 5 | style | Lost superscript: the power renders as «2 10 - 2 = 1022» | #118 → «(2^10 - 2 = 1022)» |
| 11-13-exam | 8 | error | Comment says converting the network address to binary yields the mask; the mask follows from the /22 prefix length | #118 → «Префикс /22 соответствует маске подсети 255.255.252.0» |
| 11-13-exam | 10 | error | Comment says the 208-255 range only allows /28; in fact 10.16.10.224/27 (224-255) fits there and does not overlap 10.16.10.192/28 (192-207). Key is still right … | #118 → «В диапазоне от 208 до 255 можно создать только одну подсеть /27 — 10.16.10.224/27, но ее нет среди вариантов ответа.» |
| 11-13-exam | 16 | style | Term inconsistent with the module: the module calls it «направленная широковещательная рассылка» | #118 → «направленная широковещательная рассылка» |
| 11-13-exam | 16 | style | Same term in the comment: «Прямая широковещательная рассылка» | #118 → «Направленная широковещательная рассылка» |
| 11-13-exam | 18 | error | «link-local unicast» was translated as «локальной одноадресной рассылки», dropping «канала»; with that wording distractor 2 FD80::1:1234 (a unique local unicast… | #118 → «локальным IPv6-адресом канала (link-local)» |
| 11-13-exam | 19 | style | Broken sentence «Правила уменьшения обозначения адресов IPv6 являются:» | #118 → «Правила сокращения записи IPv6-адресов:» |
| 11-13-exam | 19 | style | MT «все единичные, непрерывные строки» (any single, contiguous string); «все» even suggests several runs can be replaced, contradicting rule 3 | #118 → «может заменять одну непрерывную последовательность из одного или нескольких 16-битных сегментов (гекстетов), состоящих т…» |
| 11-13-exam | 20 | style | Wrong preposition «с префикса /48» and bureaucratic chain «не будет выделять подсеть в область идентификатора интерфейса адресного пространства» | #118 → «из префикса /48, не затрагивая биты идентификатора интерфейса» |
| 11-13-exam | 29 | style | Tautology «индивидуальному адресу для одноадресной рассылки» (unicast address for unicast) and odd «тип … относится к адресу» | #118 → «обозначает индивидуальный адрес, назначенный сразу нескольким хостам» |
| 11-13-exam | 29 | style | Missing hyphen «anycast адрес» (Q30 of the connected copy writes «multicast-адрес», «broadcast-адрес») | #118 → «anycast-адрес» |
| 11-13-exam | 30 | error | Comment lists multicast twice («многоадресными, групповыми» are synonyms) and omits anycast | #118 → «Адреса IPv6 могут быть индивидуальными, групповыми и произвольными (anycast)» |
| 11-13-exam | 30 | style | «локальный адрес» instead of the module term «локальный адрес канала» (the keyed answer) | #118 → «Характерные типы индивидуальных адресов — локальный адрес канала и адрес loopback» |
| 11-13-exam | 30 | unclear | The module defines anycast as «любой индивидуальный IPv6-адрес, который можно назначить нескольким устройствам», so a learner can defend «anycast адрес» as a ty… | operator (kb#275) |
| 11-13-exam | 33 | style | Agreement error «каждый способ с их описанием» | #118 → «с его описанием» |
| 11-13-exam | 35 | style | Calque «на одной и той же локальной сети в качестве узла-отправителя» (on the same LAN as the sending host) | #118 → «Успешный ответ пришел только от первого устройства, находящегося в той же локальной сети, что и узел-отправитель.» |
| 11-13-exam | 37 | style | The message name differs from the module: the module calls ICMP Time Exceeded «превышен интервал ожидания» (Q38 of this exam uses the same); «время жизни истекл… | #118 → «превышен интервал ожидания» |
| 11-13-exam | 37 | style | MT «поле ограничения прыжка» (hop = переход); the previous sentence already names the field «предел переходов» | #118 → «Если значение поля «предел переходов» достигло нуля» |
| 11-13-exam | 38 | style | Broken government «сколько переходов маршрутизатора может перемещаться пакет»; «оно больше не может быть перенаправлено» refers to the field instead of the pack… | #118 → «определяет, через сколько маршрутизаторов может пройти пакет. Как только значение поля Hop Limit достигнет нуля, пакет б…» |
| 11-13-exam | 40 | style | Missing space after the period «интерфейса.Это» | #118 → «интерфейса. Это» |
| 11-13-exam | 41 | error | Item «индивидуальный адрес» (a mistranslation of "private address") fits several options: 64.102.90.23, 169.254.1.5 and 192.0.2.123 are unicast too, yet 172.19.… | #118 → «"частный адрес"» |
| 11-13-exam | 42 | style | Calque «Каково представление длины префикса для маски…» (What is the prefix length notation for…) | #118 → «Какой длине префикса соответствует маска подсети 255.255.255.224?» |
| 11-13-exam | 43 | style | Comment says «первая и последняя подсети являются сетью и широковещательным адресом» (addresses, not subnets) and «Адрес … не действует для других подсетей»; it… | #118 comments emptied |
| 11-13-exam | 43 | style | Comment says «первая и последняя подсети являются сетью и широковещательным адресом» (addresses, not subnets) and «Адрес … не действует для других подсетей»; it… | #118 comments emptied |
| 11-13-exam | 43 | style | Comment says «первая и последняя подсети являются сетью и широковещательным адресом» (addresses, not subnets) and «Адрес … не действует для других подсетей»; it… | #118 comments emptied |
| 11-13-exam | 44 | error | The Q43 subnet explanation (192.168.1.64/26, address .96) is pasted onto every wrong answer of Q44-Q61 (broadcast/unicast/multicast, IPv6 compression, ICMP code… | #118 → «» |
| 11-13-exam | 44 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Широковещательный пакет получают все узлы той же подсети (домена широковещательной рассылки), а не только ближайший сосе…» |
| 11-13-exam | 45 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Одноадресный пакет адресован одному конкретному узлу (режим «один к одному»), причем не обязательно ближайшему: получате…» |
| 11-13-exam | 46 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Многоадресный пакет получает определенная группа узлов, подписанных на групповой адрес назначения, и близость к отправит…» |
| 11-13-exam | 47 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Начальные нули в гекстетах отбрасываются (0db8 → db8, 0008 → 8, 0001 → 1), а три нулевых гекстета подряд заменяются одни…» |
| 11-13-exam | 48 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Без начальных нулей адрес записывается как fe80:9ea:0:2200:0:0:fe0:290; «::» заменяет самую длинную последовательность н…» |
| 11-13-exam | 49 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «После удаления начальных нулей (0042 → 42, 0010 → 10, 0909 → 909) три нулевых гекстета подряд заменяются на «::», что да…» |
| 11-13-exam | 50 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Начальные нули отбрасываются (0db8 → db8, 0ab8 → ab8, 0001 → 1, а 1000 не меняется), «::» заменяет более длинную последо…» |
| 11-13-exam | 51 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «После удаления начальных нулей (0420 → 420, 00c4 → c4, 0025 → 25, 0190 → 190, 0990 → 990) единственный нулевой гекстет м…» |
| 11-13-exam | 52 | style | Calque «Что представляет этот код?» (What does this code represent?) in 10 stems | #118 → «Что означает этот код?» |
| 11-13-exam | 52 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv6-адрес, поэтому код относится к сообщению ICMPv6 «Узел назначения недоступен», где 2 означае…» |
| 11-13-exam | 53 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv4-адрес, поэтому код относится к сообщению ICMPv4 «Узел назначения недоступен», где 1 означае…» |
| 11-13-exam | 54 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv6-адрес, поэтому код относится к сообщению ICMPv6 «Узел назначения недоступен», где 3 означае…» |
| 11-13-exam | 55 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv4-адрес, поэтому код относится к сообщению ICMPv4 «Узел назначения недоступен», где 0 означае…» |
| 11-13-exam | 56 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv6-адрес, поэтому код относится к сообщению ICMPv6 «Узел назначения недоступен», где 4 означае…» |
| 11-13-exam | 57 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv4-адрес, поэтому код относится к сообщению ICMPv4 «Узел назначения недоступен», где 0 означае…» |
| 11-13-exam | 58 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv6-адрес, поэтому код относится к сообщению ICMPv6 «Узел назначения недоступен», где 4 означае…» |
| 11-13-exam | 59 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv6-адрес, поэтому код относится к сообщению ICMPv6 «Узел назначения недоступен», где 2 означае…» |
| 11-13-exam | 60 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv4-адрес, поэтому код относится к сообщению ICMPv4 «Узел назначения недоступен», где 1 означае…» |
| 11-13-exam | 61 | error | No explanation after the copied comment was blanked; written from the module text | #118 comments rewritten: «Эхо-запрос отправлен на IPv6-адрес, поэтому код относится к сообщению ICMPv6 «Узел назначения недоступен», где 3 означае…» |
| 14-15-exam | 1 | error | Comment claims the receiver waits for all 1000 bytes before acknowledging; the course says the receiver normally does not wait for the full window. The window l… | #116 → «Размер окна определяет, сколько байтов источник может отправить, прежде чем ему потребуется подтверждение. При окне 1000…» |
| 14-15-exam | 4 | style | Genitive chain "заголовке сегмента блока данных UDP" is an MT calque; the course simply says "заголовок UDP". | #116 → «в заголовке UDP» |
| 14-15-exam | 4 | style | Term "последовательный номер" differs from the module term "порядковый номер" (also used in Q6 and Q16 of this exam). | #116 → «орядковый номер» |
| 14-15-exam | 8 | unclear | Distractor "устройства назначения собирают сообщения и передают их в приложение" also holds for UDP per the course (UDP reassembles data in arrival order and pa… | operator (kb#275) |
| 14-15-exam | 10 | style | "АСК" in the last sentence is typed with Cyrillic letters (U+0410 U+0421 U+041A), not the Latin protocol flag ACK used everywhere else. | #116 → «получение сообщения ACK» |
| 14-15-exam | 11 | style | Broken grammar: "TCP, когда два DNS обслуживает прямое взаимодействие" (agreement error, MT of "when two DNS servers communicate directly"). | #116 → «и TCP, когда DNS-серверы взаимодействуют друг с другом напрямую.» |
| 14-15-exam | 13 | style | Example of a registered port is the Cisco-proprietary HSRP (port 1985); the de-marketed module replaced it with RADIUS port 1812. | #116 → «Например, порт 1812 зарегистрирован для аутентификации через RADIUS-сервер.» |
| 14-15-exam | 14 | error | Comment says protocols that use TCP "допускают определенную потерю данных"; the opposite is true: they use TCP because they need every byte delivered. | #116 → «Кроме того, этим протоколам не нужен обмен данными в реальном времени, поэтому дополнительные накладные расходы TCP для …» |
| 14-15-exam | 15 | unclear | Keyed answer "UDP использует протоколы уровня приложений для выявления ошибок" contradicts the UDP checksum, which detects errors at the transport layer; only r… | operator (kb#275) |
| 14-15-exam | 17 | style | Calqued word order "трехстороннего процесса рукопожатия": the handshake is three-way, not the process. | #116 → «процесса трехстороннего рукопожатия» |
| 14-15-exam | 19 | style | Clumsy, ungrammatical sentence ("которые могут терпеть..., требуют..., а также самостоятельно обрабатывать"); "UDP ... не требует надежности" misstates "UDP doe… | #116 → «Для UDP лучше всего подходят приложения, которые допускают потерю части данных, работают по простой схеме «запрос — отве…» |
| 14-15-exam | 23 | style | MT garble: "настроен для использования питания DHCP" (from "powers up") and "сообщением для одноадресной рассылки, используемой в протоколе DHCPOFFER". | #116 → «Узел, настроенный на использование DHCP, после включения отправляет в сеть сообщение DHCPDISCOVER. FF-FF-FF-FF-FF-FF — э…» |
| 14-15-exam | 25 | style | MT garble: "протокол для файла, принтера и технологии предоставления общего доступа к каталогу". | #116 → «SMB — это протокол общего доступа к файлам, принтерам и каталогам.» |
| 14-15-exam | 30 | style | Typo: the application is Shareaza (spelled correctly in Q31). | #116 → «Shareaza,» |
| 14-15-exam | 33 | error | Mistranslated comment: "Этот запрос является как клиентским, так и серверным приложением" is meaningless, and "Если на рабочей станции функционирует один принте… | #116 → «Такой запрос — пример взаимодействия по модели «клиент-сервер». eMule — это P2P-приложение. Совместное использование при…» |
| 14-15-exam | 35 | style | Grammar error: "между клиентом с сервером". | #116 → «между клиентом и сервером» |
| 14-15-exam | 36 | style | Calque "подписывается на отдельные услуги" and ambiguous "на своем сервере" (whose server?). | #116 → «заказывает у интернет-провайдера отдельные услуги, размещаемые на сервере провайдера» |
| 14-15-exam | 37 | style | Stray comma before the parenthesis: "контент, (например, изображения)". | #116 → «контент (например, изображения)» |
| 14-15-exam | 44 | style | MT artefacts "уровни сеансов, презентаций и приложений" (presentation layer is "уровень представления") and "Нижние слои"; course terms differ. | #116 comments rewritten: «Три верхних уровня модели OSI — сеансовый, уровень представления и уровень приложений — обеспечивают те же сервисы, что …» |
| 14-15-exam | 45 | error | Wrong-answer comments are copied from Q44 (OSI layers) and have nothing to do with TCP acknowledgement numbers. | #116 comments rewritten: «Номер подтверждения — это номер следующего ожидаемого байта. Если нумерация начинается с 1, два пакета по 1500 байт соде…» |
| 14-15-exam | 46 | error | Wrong-answer comments are copied from Q44 (OSI layers) and have nothing to do with TCP acknowledgement numbers. | #116 comments rewritten: «Номер подтверждения — это номер следующего ожидаемого байта. Если нумерация начинается с 1, три пакета по 1500 байт соде…» |
| 14-15-exam | 47 | error | Wrong-answer comments are copied from Q44 (OSI layers) and have nothing to do with TCP acknowledgement numbers. | #116 comments rewritten: «Номер подтверждения — это номер следующего ожидаемого байта. Если нумерация начинается с 1, четыре пакета по 1500 байт с…» |
| 14-15-exam | 48 | error | Wrong-answer comments are copied from Q44 (OSI layers) and do not explain the port numbers. | #116 comments rewritten: «Служба TFTP использует UDP-порт 69. Порт 67 использует сервер DHCP, порт 53 — DNS, порт 80 — HTTP.» |
| 14-15-exam | 49 | error | Wrong-answer comments are copied from Q44 (OSI layers) and do not explain the port numbers. | #116 comments rewritten: «Управляющее соединение FTP использует TCP-порт 21. Порт 69 использует TFTP, порт 67 — сервер DHCP, порт 80 — HTTP.» |
| 14-15-exam | 50 | error | Wrong-answer comments are copied from Q44 (OSI layers) and do not explain the port numbers. | #116 comments rewritten: «Служба SSH использует TCP-порт 22. Порт 69 использует TFTP, порт 67 — сервер DHCP, порт 80 — HTTP.» |
| 14-15-exam | 51 | error | Wrong-answer comments are copied from Q44 (OSI layers) and do not explain the port numbers. | #116 comments rewritten: «Служба HTTP использует TCP-порт 80. Порт 67 использует сервер DHCP, порт 53 — DNS, порт 69 — TFTP.» |
| 14-15-exam | 52 | error | Wrong-answer comments are copied from Q44 (OSI layers) and do not explain the port numbers. | #116 comments rewritten: «Служба POP3 использует TCP-порт 110. Порт 67 использует сервер DHCP, порт 53 — DNS, порт 69 — TFTP.» |
| 14-15-exam | 53 | error | Wrong-answer comments are copied from Q44 (OSI layers) and do not explain the port numbers. | #116 comments rewritten: «Служба Telnet использует TCP-порт 23. Порт 443 использует HTTPS, порт 161 — SNMP, порт 110 — POP3.» |
| 14-15-exam | 54 | error | Wrong-answer comments are copied from Q44 (OSI layers) and do not explain the port numbers. | #116 comments rewritten: «Служба SNMP использует UDP-порт 161. Порт 443 использует HTTPS, порт 110 — POP3, порт 80 — HTTP.» |
| 14-15-exam | 55 | error | Wrong-answer comments are copied from Q44 (OSI layers) and do not explain the port numbers. | #116 comments rewritten: «Служба HTTPS использует TCP-порт 443. Порт 161 использует SNMP, порт 110 — POP3, порт 80 — HTTP.» |
| 16-17-exam | 2 | style | Threat name "нарушение обслуживания" differs from the module term "прекращение обслуживания". | #116 → «прекращение обслуживания» |
| 16-17-exam | 2 | style | Case error: "препятствование доступа" (препятствование governs the dative). | #116 → «препятствование доступу пользователей» |
| 16-17-exam | 4 | unclear | Distractor "вирусы, в отличие от интернет-червей, скрываются в безвредных приложениях" is true per the module: viruses attach to legitimate executables, worms a… | operator (kb#275) |
| 16-17-exam | 5 | style | Off-topic machine-translated IoT text ("SQLi (SQLi)", "ограниченными устройствами", "известные как атака воронки"); none of it is in the module. Replace with th… | #116 → «При атаке через посредника (MITM) злоумышленник располагается между двумя доверяемыми объектами, чтобы читать, изменять …» |
| 16-17-exam | 7 | style | Wrong case: "фильтрации URL-адресов" (genitive) among nominative labels. | #116 → «фильтрация URL-адресов» |
| 16-17-exam | 8 | style | Bureaucratic genitive chain "цель функции аутентификации сетевой безопасности". | #116 → «Какова цель аутентификации в системе сетевой безопасности?» |
| 16-17-exam | 8 | style | Calque "чтобы определить пользователей, кем они являются"; the comment states the meaning: users must prove who they are. | #116 → «потребовать от пользователей подтвердить свою личность» |
| 16-17-exam | 9 | style | Grammar error: "может используется". | #116 → «может использоваться» |
| 16-17-exam | 10 | style | Clumsy stem: parenthetical "(при её применении на роутере)" repeats the device that the sentence names again ("на маршрутизаторе"). | #116 → «Какая команда поможет свести к минимуму риск взлома паролей маршрутизатора методом грубой силы?» |
| 16-17-exam | 10 | style | Command name is truncated: the command is "service password-encryption" (as in answer 2). | #116 → «Команда service password-encryption шифрует» |
| 16-17-exam | 11 | style | Case error "для управлением устройствами". | #116 → «для управления устройствами» |
| 16-17-exam | 11 | error | Keyed answer mistranslates "login information and data encryption" as "информация о попытках входа и шифрование данных"; SSH does not provide "information about… | #116 → «шифрование учетных данных для входа и передаваемых данных» |
| 16-17-exam | 14 | style | Clumsy calque "функционирует с учетом особенностей используемого программного обеспечения" (from "application-aware"). | #116 → «который распознает приложения и снабжен системой обнаружения вторжений» |
| 16-17-exam | 17 | style | Long bureaucratic chain ("цель небольшой компании, использующей утилиту анализатора протоколов для захвата сетевого трафика в сегментах сети, где компания рассм… | #116 → «Небольшая компания собирается модернизировать сеть и захватывает трафик анализатором протоколов в тех сегментах, которые…» |
| 16-17-exam | 18 | style | MT garble "сообщение о невозможности достичь ICMP-протокола назначения" for ICMP Destination Unreachable. | #116 → «отправил источнику ICMP-сообщение «Узел назначения недоступен».» |
| 16-17-exam | 19 | style | Spelling: "не нужных" should be one word. | #116 → «ненужных интерфейсов» |
| 16-17-exam | 20 | style | Stray space before the comma and agreement error ("на команду ping , отправленного"). | #116 → «на команду ping, отправленную» |
| 16-17-exam | 21 | style | MT garble "сообщение о невозможности достичь ICMP-протокола назначения" and "сообщением о недоступности ICMP" (reads as "ICMP is unreachable"). | #116 → «а также на то, что ICMP-сообщение «Узел назначения недоступен» не было отправлено. Символ «U» указывает на то, что у мар…» |
| 16-17-exam | 22 | style | Typo: "Поверка связи". | #116 → «Проверка связи» |
| 16-17-exam | 22 | style | Missing space after the period: "в сети.Необходимы". | #116 → «в сети. Необходимы» |
| 16-17-exam | 28 | style | Missing space after the period: "журнала.Сообщения". | #116 → «журнала. Сообщения» |
| 16-17-exam | 33 | style | Broken last sentence (a dangling "Если ..." clause with no main clause) and clumsy "адрес источника порта гигабитного Ethernet". | #116 → «указать в качестве адреса источника адрес интерфейса Gigabit Ethernet маршрутизатора R2, а в качестве адреса назначения …» |
| 16-17-exam | 36 | style | Missing space after the period: "маршрутизатора.В". | #116 → «маршрутизатора. В» |
| 16-17-exam | 40 | error | Wrong-answer comments are copied from Q39 (worm mitigation) and have nothing to do with ping and tracert. | #116 comments rewritten: «Команда tracert показывает каждый переход на пути к узлу назначения, а ping — только ответ самого узла назначения. Обе к…» |
| 16-17-exam | 48 | unclear | Distractor "слабый пароль, так как это слово легко найти в словаре" is equally true for "password"; the module example of a weak password is exactly "a simple d… | operator (kb#275) |
| 16-17-exam | 51 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «Команда show ip interface brief выводит IP-адреса и состояние всех интерфейсов маршрутизатора. Команда nslookup отправля…» |
| 16-17-exam | 52 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «Команда show interfaces показывает состояние интерфейсов, в том числе режим дуплекса, скорость и счетчики ошибок. Команд…» |
| 16-17-exam | 53 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «IP-адрес компьютера с Windows показывает команда ipconfig. Команды copy running-config startup-config, show interfaces и…» |
| 16-17-exam | 54 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «Команда copy running-config startup-config сохраняет текущую конфигурацию в NVRAM как загрузочную. Команды show interfac…» |
| 16-17-exam | 55 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «В macOS команда ipconfig getifaddr en0 выводит IP-адрес интерфейса en0. Команды copy running-config startup-config, show…» |
| 16-17-exam | 55 | unclear | Keyed command "ipconfig getifaddr en0" is not in the module (macOS section covers ifconfig and networksetup only), and en0 is the wireless interface only on Mac… | operator (kb#275) |
| 16-17-exam | 56 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «Команда show ipv6 interface выводит IPv6-адреса интерфейсов маршрутизатора. Команда show interfaces показывает состояние…» |
| 16-17-exam | 57 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «Адрес шлюза по умолчанию на компьютере с Windows показывает команда ipconfig. Команды copy running-config startup-config…» |
| 16-17-exam | 58 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «Включена ли маршрутизация IPv6, видно в текущей конфигурации (show running-config): в ней должна присутствовать команда …» |
| 16-17-exam | 59 | error | Wrong-answer comments are the password rules copied from Q42–Q50 and do not explain the commands. | #116 comments rewritten: «Команда nslookup отправляет запрос DNS-серверу и возвращает IP-адрес для указанного доменного имени. Команды show ipv6 r…» |
| final-exam | 1 | style | Clumsy stem: noun repeated ("Какие два устройства будут называться промежуточными устройствами"), calque of "would be described as". | #116 → «Какие устройства относятся к промежуточным?» |
| final-exam | 3 | style | Case error: "отдавать приоритет трафика" (dative required). | #116 → «отдавать приоритет трафику, чувствительному к задержке» |
| final-exam | 4 | style | MT garble "Команду назначения ping" (from "ping destination command"). | #116 → «Команду ping с адресом назначения используют, чтобы проверить связь с устройством назначения» |
| final-exam | 5 | style | Stray comma: "SVI не требует, включения". | #116 → «SVI не требует включения» |
| final-exam | 5 | style | Missing spaces after periods: "(SVI).Такие", "оборудования.Виртуальный". | #116 → «(SVI). Такие интерфейсы называются виртуальными, поскольку на устройстве нет связанного с ними физического оборудования.…» |
| final-exam | 13 | error | Distractor lost "multiple": "многомодовые оптоволоконные кабели передают сигналы от устройств-отправителей" is trivially true (every cable carries signals from … | #116 → «многомодовые оптоволоконные кабели передают сигналы сразу от нескольких устройств-отправителей» |
| final-exam | 13 | style | Mistranslation "светодиодные индикаторы" (LED indicator lamps) for LED light sources; the module says "светодиодные излучатели"/"светодиоды". | #116 → «светодиоды» |
| final-exam | 13 | style | Calque "магистрали с высоким коэффициентом трафика" (from "high-traffic backbone"). | #116 → «для создания магистралей с высокой нагрузкой» |
| final-exam | 15 | style | Missing space after the period: "передачи).FCS". | #116 → «передачи). FCS» |
| final-exam | 16 | unclear | The module's only example of a hybrid topology is the partial mesh, which is distractor 4; the extended star (key) is described as a LAN topology but never call… | operator (kb#275) |
| final-exam | 17 | style | Agreement error: "для физической среды передачи данных, к которому они подключаются". | #116 → «к которой они подключаются» |
| final-exam | 18 | style | Clumsy calqued stem ("Хотя CSMA/CD ... является особенностью Ethernet, почему это больше не нужно?"). | #116 → «CSMA/CD по-прежнему входит в стандарт Ethernet. Почему этот механизм больше не нужен?» |
| final-exam | 20 | error | Distractor is a true statement: fragment-free switching is the compromise between store-and-forward and fast-forward (the comment says the same). The original d… | #116 → «коммутацию с быстрой пересылкой можно рассматривать как компромиссный вариант между коммутацией с промежуточным хранение…» |
| final-exam | 20 | error | Distractor is a true statement: fragment-free is one of the two variants of cut-through switching. The original distractor said fragment-free is the typical for… | #116 → «коммутация с исключением фрагментов — типичный способ сквозной коммутации» |
| final-exam | 21 | style | Spelling: "выбраный". | #116 → «неверно выбранный тип кабеля» |
| final-exam | 22 | style | "значительно отличается" wrongly implies that a small CRC mismatch is tolerated; any mismatch causes the frame to be dropped. | #116 → «отличается» |
| final-exam | 27 | style | Broken grammar "будет отвечать одноадресный кадр" and clumsy "получит пару IP-адресов назначения и MAC-адресов для продолжения процесса инкапсуляции для передач… | #116 → «ответит одноадресным кадром со своим MAC-адресом. Так узел-отправитель узнает, какой MAC-адрес соответствует IP-адресу н…» |
| final-exam | 33 | style | Run-on calqued stem ("Дана сеть 172.18.109.0, какая маска подсети будет использоваться, если будут доступны 6 бит хоста?"). | #116 → «Какая маска подсети используется в сети 172.18.109.0, если на узловую часть адреса отводится 6 бит?» |
| final-exam | 36 | style | Spelling: "сгенерированый". | #116 → «сгенерированный» |
| final-exam | 39 | style | Leftover English in prose: "remote server". | #116 → «удаленный сервер —» |
| final-exam | 40 | error | Comment says pinging 127.0.0.1 tests the network adapter and drivers; loopback traffic never reaches the NIC. The course says the reply only confirms TCP/IP on … | #116 → «127.0.0.1 — это адрес loopback. Эхо-запрос на этот адрес проверяет работу стека TCP/IP на локальном узле; пакеты при это…» |
| final-exam | 40 | style | Ungrammatical distractor "трассировать пути к хост-компьютеру в сети и сеть имеет IP-адрес 127.0.0.1". | #116 → «трассировать путь к узлу сети с IP-адресом 127.0.0.1» |
| final-exam | 41 | style | MT artefacts: "квитирование узла" (host confirmation), "запрос его соседа" (reads as the router's neighbour), and RS/RA/NS called "протоколы" instead of message… | #116 → «К сообщениям, общим для ICMPv4 и ICMPv6, относятся: проверка доступности узла, «узел назначения или сервис недоступен» (…» |
| final-exam | 49 | style | Calque "неопределённая личность" (from "an unidentified individual"). | #116 → «посторонний человек пытается» |
| final-exam | 50 | unclear | The module does not relate packet filters or stateful firewalls to OSI layers (it describes filtering by IP/MAC, ports, URL and SPI only), so the key "до трансп… | operator (kb#275) |
| final-exam | 53 | style | Command typo: "ipconfig / flushdns" (space after the slash). | #116 → «ipconfig /flushdns» |

## Findings: Bank copies (`__exams/CCNA1`)

The bank copies repeat the exam questions in the same order (the 01-03 bank has one extra question at position 48). 278 of their 292 findings mirror an exam finding above and get the same fix, in the same PR, with the same wording; they are not repeated here. The table lists the 14 bank findings whose fix differs: the bank wording differs, or the problem exists only in the bank.

| File | Q | Sev | Issue | Fix |
|---|---|---|---|---|
| bank 01-03 | 4 | style | Stray period and capital letter in the option «Надежность.»; the other options are lower-case nouns without a period | #117 → «"answer": "надежность",» |
| bank 01-03 | 23 | error | Stem says not all options are used, but all three options (user EXEC, privileged EXEC, global configuration) are matched by two answers each. (bank copy, same p… | #117 → «режимом ОС.» |
| bank 04-07 | 2 | style | The stem calls throughput «пропускная способность» (bandwidth). The module defines these as different things, and q45/q46 of this exam test exactly that differe… | #117 → «фактическая производительность оказалась ниже пропускной способности канала. Какие три фактора могли повлиять на произво…» |
| bank 04-07 | 26 | error | The comment attributes port-based buffering behaviour (per-port queues, head-of-line delay) to «буферизация памяти» right after describing shared memory, so it … | #117 → «При буферизации на основе портов кадры хранятся в очередях, подключенных к определенным входящим и исходящим портам, из-…» |
| bank 04-07 | 41 | style | Same term in the comment («Инверсный кабель (rollover)»); in the bank copy the sentence also starts with a lowercase letter. (bank copy, same problem) | #117 → «недоступен. Консольный кабель (rollover)» |
| bank 08-10 | 5 | style | Bank comment says «декапсуляция» where the connected copy now says «деинкапсуляция» (glossary preferred term); same wording in both copies | #118 → «маршрутизация деинкапсуляция» |
| bank 08-10 | 37 | error | Stem says «(Не все варианты используются.)», but all 4 options are matched to the 4 items (same problem in the bank copy) | #118 → «доступной в этом режиме.» |
| bank 08-10 | 44 | error | Bank copy has no explanation after the copied comment was blanked; given the same text as connected Q44 | #118 comments rewritten: «Поле «Дифференцированные услуги» (DS) — 8-битное поле, которое используется для определения приоритета каждого пакета. I…» |
| bank 08-10 | 52–56 | style | MT artefact: distractor «ответы ARP транслируются по сети» renders "broadcast" as «транслируются» (moved from the operator list after review); same distractor i… | #118 → «Ответы ARP рассылаются широковещательно, когда узел получает запрос ARP.» |
| bank 11-13 | 30 | style | Missing hyphen, as in the connected copy | #118 → «broadcast-адрес» |
| bank 11-13 | 30 | style | Missing hyphen, as in the connected copy | #118 → «multicast-адрес» |
| bank Practice Final | 13 | error | Distractor lost "multiple": "многомодовые оптоволоконные кабели передают сигналы от устройств-отправителей" is trivially true (every cable carries signals from … | #116 → «Многомодовые оптоволоконные кабели передают сигналы сразу от нескольких устройств-отправителей.» |
| bank Practice Final | 20 | error | Distractor is a true statement: fragment-free switching is the compromise between store-and-forward and fast-forward (the comment says the same). The original d… | #116 → «"answer": "Коммутацию с быстрой пересылкой можно рассматривать как компромиссный вариант между коммутацией с промежуточн…» |
| bank Practice Final | 39 | style | Leftover English in prose: "remote server". Same problem in the bank copy. | #116 → «удаленный сервер:» |

## Course text found on the way

Errors in the lecture text that the review ran into. None of them is changed by the quiz PRs, because the lectures are outside kb#275. They go to the operator with the doubtful items.

| Lecture | Problem |
|---|---|
| `02-basic-switch-and-end-device-configuration/02.04-basic-device-configuration/README.md:16` | hostname limit «не более чем из 64 символов»; RFC 1035 allows 63 characters per label, and the quiz key (02.09.04 q5) says «менее 64» |
| `02-basic-switch-and-end-device-configuration/02.07-configure-ip-addressing/README.md:20` | DNS described backwards: «для преобразования IP-адресов в имена доменов» |
| `03-protocols-and-models/03.02-protocols/README.md:37` | flow control called «Управление процессами» in the table |
| `04-physical-layer/04.02-physical-layer-characteristics/README.md:124` | garbled «Производительность способность» |
| `07-ethernet-switching/07.01-ethernet-frame/README.md:76` | frames over 1500 bytes called Jumbo / Baby Giant, while :74 gives 1518 bytes as the maximum frame |
| `08-network-layer/08.01-network-layer-characteristics/README.md:85` | «электрических импульсов, например оптических сигналов» |
| `11-ipv4-addressing/11.02-ipv4-unicast-broadcast-and-multicast/README.md:29` | directed broadcast called «прямая», while :37–43 call it «направленная» |
| `13-icmp/13.01-icmp-messages/README.md:61` | RS, RA, NS and NA called «четыре новых протокола»; they are messages of ND |
| `13-icmp/13.01-icmp-messages/README.md:16, :48` | Time Exceeded rendered «превышен интервал ожидания», which reads as a timeout (it is also the Windows wording for "Request timed out"); the exams follow the lecture, so the choice belongs to the lecture (noted by kb's review of learn-ccna1#118) |
| `14-transport-layer/14.04-port-numbers/README.md:75` | DNS servers «всегда» talk to each other over TCP; zone transfers and large replies use TCP, ordinary queries between servers use UDP |
| `15-application-layer/15.02-peer-to-peer/README.md:55` | µTorrent, BitComet, DC++ and Deluge listed as Gnutella clients |
| `16-network-security-fundamentals/16.01-security-threats-and-vulnerabilities/README.md:17` | heading «Утечка данных и их неправомерное использование» for "data loss and manipulation"; the quiz options in 16.01.04 follow the source |
| `17-build-a-small-network/17.07-troubleshooting-scenarios/README.md:60` | says Linux and macOS don't assign a 169.254.x.x address; macOS does (RFC 3927) |

Two vendor mentions in lecture text are known tier-3 skips from the de-marketing pass and are not new: `07.04…/README.md:93` (Auto-MDIX «Cisco IOS 12.2 (18) SE», audit P2-08, waits for the simulator's default) and `02.02…/README.md:84` (simulation tools, waits for the learn-netsim rewrite).

## Follow-ups

- **Images:** 08-10-exam Q36 and its bank copy show `tracert www.cisco.com` in `assets/4.png`. The stem is fixed in learn-ccna1#118, and the image is logged in that PR's `audit/figma-followups/` file.
- **Packet Tracer item:** bank 01-03 Q48 is a `.pka` activity. Files with `.pka` are out of scope, so the question stays until the lab rework.
- **Exams 08–10 and 11–13:** the comments copied onto 40 questions were replaced with explanations written for each question. They are in learn-ccna1#118.

# CCNA1 — встроенные видео: классификация и сценарии пересборки

36 видео, встроенных в материалы курса как ссылки на YouTube, разобраны по одному: класс, цель для обучающегося, посценный сценарий (что на экране / что говорится / роль), предложение по пересборке и полный транскрипт — по документу на видео в этой папке (`<модуль>/<тема>--<videoId>.md`). Классы: **marketing** — убрать; **explainer** — объяснение концепции (пересборка в анимацию / видео с голосом / текст + иллюстрация); **cli-basics** и **lab-demo** — сессии CLI/GUI, пригодные для обучающих видео нашего симулятора.

| класс | видео |
|---|---|
| marketing | 2 |
| explainer | 17 |
| cli-basics | 7 |
| lab-demo | 8 |
| other | 2 |

## Видеоряд в Figma

Колонка «Видеоряд (Figma)» в таблице фиксирует прогресс пересборки: по каким видео собран и принят новый видеоряд — анимация Figma Motion на нашей дизайн-системе. Голосовая дорожка — отдельный трек, пока не начат ни для одного видео.

**Готово: 17 из 36** (explainer — 17 из 17).

| статус | значит |
|---|---|
| — | пересборка не начата |
| раскадровка | раскадровка принята, анимации ещё нет |
| Motion | анимация собрана по принятой раскадровке и ждёт приёмки оператора; время и ссылка — как у «готов» |
| **готов** | анимация Figma Motion принята оператором; время — её хронометраж (у оригинала — колонка «Длит.»), ссылка ведёт на кадр анимации |

Всё лежит в рабочем файле Figma `3FtCg22qFubpLBPOetQU03` (CCNA Design): по листу на видео «Видео · ‹videoId› · ‹название› · прототип» с двумя секциями — «Motion · …» (анимация и набор-кит, из которого она собрана) и «Раскадровка · …» (базовая сцена и кадры раскадровки с описаниями). У этих листов нет курсового префикса и штампов `⟨id⟩`, поэтому синхронизация иллюстраций (`figma_sync.py`) их не читает. Метод сборки — `runbooks/video-motion-build.md` в learn-knowledge-base. Ролики одной серии (7.3.4 → 7.3.5, 9.2.3 → 9.2.4 → 9.2.5) продолжаются с состояния, на котором закончился предыдущий, без ссылок на другие видео в кадре. Подробности по каждому готовому видео — раздел «Видеоряд в Figma» в его документе.

`fi7Ss-_9LvY` встроен и в CCNA2 (2.1.4) — там тот же видеоряд.

## Таблица

| videoId | module/topic | Название (EN) | Длит. | Класс | Предложение по пересборке | Видеоряд (Figma) | Документ |
|---|---|---|---|---|---|---|---|
| 7E9ilk9dOOI | 01/01.00.05-lab-logical-and-physical-mode-exploration | Installing Cisco Packet Tracer | 5:22 | other (установка ПО) | текст + иллюстрация (скриншоты актуального установщика); NetAcad-часть устарела | — | [doc](01-networking-today/01.00.05-lab-logical-and-physical-mode-exploration--7E9ilk9dOOI.md) |
| uync1j2x6Ms | 01/01.00.05-lab-logical-and-physical-mode-exploration | Quick start with Cisco Packet Tracer | 13:14 | lab-demo | код-рендер скринкаст ~5:00 в 2 частях (Logical / Physical) | — | [doc](01-networking-today/01.00.05-lab-logical-and-physical-mode-exploration--uync1j2x6Ms.md) |
| wcIP__5sa1o | 01/01.01-networks-affect-our-lives | Cisco Networking Academy | 2:28 | **marketing** | убрать (вместе с разделом 1.1.2) | — | [doc](01-networking-today/01.01-networks-affect-our-lives--wcIP__5sa1o.md) |
| e85Y71fsyyY | 01/01.07-network-trends | Cisco Webex Promo | 1:21 | **marketing** | убрать (одна фраза в 1.7.4) | — | [doc](01-networking-today/01.07-network-trends--e85Y71fsyyY.md) |
| B269UlVAN40 | 02/02.02-ios-navigation | IOS CLI Primary Command Modes | 2:33 | cli-basics | код-рендер ~1:30 + сессия для симулятора (можно слить с 2.2.5) | — | [doc](02-basic-switch-and-end-device-configuration/02.02-ios-navigation--B269UlVAN40.md) |
| Z-n1tO4Xg6w | 02/02.02-ios-navigation | Navigate between IOS Modes | 3:52 | cli-basics | код-рендер ~2:30 + сессия для симулятора | Motion · 3:11 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5822-9010) | [doc](02-basic-switch-and-end-device-configuration/02.02-ios-navigation--Z-n1tO4Xg6w.md) |
| K_VEPe8aRUE | 02/02.03-the-command-structure | Context-Sensitive Help and Command Syntax Check | 4:02 | cli-basics | код-рендер ~2:30 + сессия для симулятора | — | [doc](02-basic-switch-and-end-device-configuration/02.03-the-command-structure--K_VEPe8aRUE.md) |
| YDXgJUjGjcw | 02/02.03-the-command-structure | Hot Keys and Shortcuts | 6:02 | cli-basics | код-рендер ~3:00 с бейджами клавиш + сессия (Tab, сокращения, ^Z, ^C, ^A/^E, ^Shift+6, ^R) | — | [doc](02-basic-switch-and-end-device-configuration/02.03-the-command-structure--YDXgJUjGjcw.md) |
| Ae9qSUlJ3a4 | 02/02.04-basic-device-configuration | Secure Administrative Access to a Switch | 6:57 | cli-basics | код-рендер ~3:30 + сессия (console/enable secret/vty/encryption/banner + проверки) | — | [doc](02-basic-switch-and-end-device-configuration/02.04-basic-device-configuration--Ae9qSUlJ3a4.md) |
| lQQ28pdSqfg | 02/02.05-save-configurations | Alter the Running Configuration | 7:09 | cli-basics | код-рендер ~3:30 (схема RAM/NVRAM) + сессия (copy run start, dir nvram:, reload, erase, copy start run) | — | [doc](02-basic-switch-and-end-device-configuration/02.05-save-configurations--lQQ28pdSqfg.md) |
| CkvRVRcOkls | 02/02.08-verify-connectivity | Test the Interface Assignment | 4:36 | lab-demo | код-рендер ~2:30 + сессия (show ip interface brief, no shutdown, ip address на SVI) | — | [doc](02-basic-switch-and-end-device-configuration/02.08-verify-connectivity--CkvRVRcOkls.md) |
| gex3BaiuQiw | 02/02.08-verify-connectivity | Test End-to-End Connectivity | 2:40 | lab-demo | код-рендер ~1:45 + сессия ping (можно слить с 2.8.1) | — | [doc](02-basic-switch-and-end-device-configuration/02.08-verify-connectivity--gex3BaiuQiw.md) |
| yWjd-4WN4hE | 03/03.01-the-rules | Devices in a Bubble | 3:44 | explainer | анимация Figma (≤ 60 с) или код-рендер ~2:00 | **готов** · 1:16 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5412-9057) | [doc](03-protocols-and-models/03.01-the-rules--yWjd-4WN4hE.md) |
| lxeBvUOA9oE | 05/05.01-binary-number-system | Convert Between Binary and Decimal Numbering Systems | 8:22 | explainer | 2 анимации Figma (168 → биты; адрес → десятичный) или код-рендер ~3:00 | **готов** · 1:36 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5012-7035) | [doc](05-number-systems/05.01-binary-number-system--lxeBvUOA9oE.md) |
| 50O7DGHEz6A | 05/05.02-hexadecimal-number-system | Convert Between Hexadecimal and Decimal Numbering Systems | 6:35 | explainer | 2 анимации Figma (197 → C5; 9F → 159) или код-рендер ~2:30 | **готов** · 1:24 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5018-7035) | [doc](05-number-systems/05.02-hexadecimal-number-system--50O7DGHEz6A.md) |
| fi7Ss-_9LvY | 07/07.03-the-mac-address-table | MAC Address Tables on Connected Switches | 3:05 | explainer | анимация Figma (≤ 60 с) на общей схеме с 7.3.5 (+ опц. код-рендер ~2:00) | **готов** · 1:35 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5413-8758) | [doc](07-ethernet-switching/07.03-the-mac-address-table--fi7Ss-_9LvY.md) |
| RXLercop7eU | 07/07.03-the-mac-address-table | Send a Frame to the Default Gateway | 2:58 | explainer | анимация Figma (≤ 60 с), продолжение 7.3.4 (или один ролик ≈ 3:30 на оба) | **готов** · 1:13 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5409-8304) | [doc](07-ethernet-switching/07.03-the-mac-address-table--RXLercop7eU.md) |
| PArGE7H_eN8 | 08/08.02-ipv4-packet | Sample IPv4 Headers in Wireshark | 5:21 | lab-demo (скриншоты Wireshark) | код-рендер дерева диссектора ~3:00 (SYN / GET / ICMP) | — | [doc](08-network-layer/08.02-ipv4-packet--PArGE7H_eN8.md) |
| aOwXEempJ4k | 08/08.03-ipv6-packet | Sample IPv6 Headers in Wireshark | 5:48 | lab-demo (скриншоты Wireshark) | код-рендер ~3:00 с колонкой IPv4 ↔ IPv6; исправить 2 ошибки диктора | — | [doc](08-network-layer/08.03-ipv6-packet--aOwXEempJ4k.md) |
| pt_Qw1Jfo5w | 08/08.05-router-routing-tables | IPv4 Router Routing Table | 5:42 | lab-demo | код-рендер ~3:00 (топология + show ip route) + сессия; согласовать листинг с текстом 8.5.6 | — | [doc](08-network-layer/08.05-router-routing-tables--pt_Qw1Jfo5w.md) |
| tna6DaUeu5c | 09/09.02-arp | ARP Operation – ARP Request | 2:53 | explainer | анимация Figma ≤ 60 с (трек 1 общей сцены «ARP в LAN») | **готов** · 1:02 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5407-8076) | [doc](09-address-resolution/09.02-arp--tna6DaUeu5c.md) |
| Ud1angOlxHE | 09/09.02-arp | ARP Operation – ARP Reply | 1:45 | explainer | анимация Figma ≤ 60 с (трек 2 той же сцены) | **готов** · 0:52 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5408-8009) | [doc](09-address-resolution/09.02-arp--Ud1angOlxHE.md) |
| 1ZB2euss3YY | 09/09.02-arp | ARP Role in Remote Communications | 3:01 | explainer | анимация Figma ≤ 60 с (трек 3) + сессия `arp -a` / `show ip arp` для симулятора | **готов** · 1:32 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5411-8587) | [doc](09-address-resolution/09.02-arp--1ZB2euss3YY.md) |
| S0SyGKhCEV0 | 09/09.03-neighbor-discovery | IPv6 Neighbor Discovery | 6:07 | explainer | код-рендер с генер. голосом ~2:30–3:00 (или 2 анимации NS / NA) | **готов** · 1:30 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5410-7771) | [doc](09-address-resolution/09.03-neighbor-discovery--S0SyGKhCEV0.md) |
| DNL4DPxjgNM | 10/10.03-configure-the-default-gateway | Network Device Differences – Part 1 | 4:31 | **other** (обзор физического оборудования) | **убрать** как видео; текст + иллюстрация «имена интерфейсов по моделям» | — | [doc](10-basic-router-configuration/10.03-configure-the-default-gateway--DNL4DPxjgNM.md) |
| RH_KIUdHZlE | 10/10.03-configure-the-default-gateway | Network Device Differences – Part 2 | 10:16 | **lab-demo** (по содержанию cli-basics) | код-рендер терминала ~4:00 + полная сессия трёх роутеров для симулятора | — | [doc](10-basic-router-configuration/10.03-configure-the-default-gateway--RH_KIUdHZlE.md) |
| 7DoggTtOLN0 | 11/11.01-ipv4-address-structure | Network, Host and Broadcast Addresses | 6:22 | explainer | анимация Figma ≤ 60 с (побитовое И) / текст + иллюстрация | **готов** · 1:16 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5057-7150) | [doc](11-ipv4-addressing/11.01-ipv4-address-structure--7DoggTtOLN0.md) |
| LKjCyGaiH4Q | 11/11.05-subnet-an-ipv4-network | The Subnet Mask | 8:09 | explainer | код-рендер ~2:30 (можно объединить с A2P7i6ebSCE) | **готов** · 1:24 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5069-7061) | [doc](11-ipv4-addressing/11.05-subnet-an-ipv4-network--LKjCyGaiH4Q.md) |
| A2P7i6ebSCE | 11/11.05-subnet-an-ipv4-network | Subnet with the Magic Number | 14:50 | explainer | код-рендер ~4:00 + сводная таблица /25…/30 в текст | **готов** · 1:30 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5079-7009) | [doc](11-ipv4-addressing/11.05-subnet-an-ipv4-network--A2P7i6ebSCE.md) |
| TJSWlSplC1Q | 11/11.06-subnet-a-16-and-8-prefix | Subnet Across Multiple Octets | 5:21 | explainer | анимация Figma ≤ 60 с / финал объединённого ролика «магическое число» | **готов** · 1:34 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5090-7009) | [doc](11-ipv4-addressing/11.06-subnet-a-16-and-8-prefix--TJSWlSplC1Q.md) |
| R_Ti9y2AShc | 11/11.08-variable-length-subnet-masking | VLSM Basics | 2:32 | explainer | текст + иллюстрация (или пролог ≤ 30 с к примеру VLSM) | **готов** · 1:16 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5107-7113) | [doc](11-ipv4-addressing/11.08-variable-length-subnet-masking--R_Ti9y2AShc.md) |
| _V-YboU4Rq4 | 11/11.08-variable-length-subnet-masking | VLSM Example | 10:24 | explainer | код-рендер ~3:30 (дерево подсетей) | **готов** · 1:44 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5115-7009) | [doc](11-ipv4-addressing/11.08-variable-length-subnet-masking--_V-YboU4Rq4.md) |
| UbqcbYsPoss | 14/14.05-tcp-communication-process | TCP 3-Way Handshake (Wireshark) | 6:55 | **lab-demo** | код-рендер ~3:00 (синтетический Wireshark) + сценарий захвата для симулятора | — | [doc](14-transport-layer/14.05-tcp-communication-process--UbqcbYsPoss.md) |
| tz7eawYRHf0 | 14/14.06-reliability-and-flow-control | TCP Reliability – Sequence Numbers and Acknowledgements | 4:06 | explainer | анимация Figma ≤ 60 с / текст + исправленная иллюстрация | **готов** · 1:16 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5126-7298) | [doc](14-transport-layer/14.06-reliability-and-flow-control--tz7eawYRHf0.md) |
| 3AzR-82OI7Q | 14/14.06-reliability-and-flow-control | TCP Reliability – Data Loss and Retransmission | 3:24 | explainer | анимация Figma ≤ 60 с (+ опц. трек SACK) | **готов** · 1:34 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5133-7459) | [doc](14-transport-layer/14.06-reliability-and-flow-control--3AzR-82OI7Q.md) |
| dFKfyJkuSqQ | 17/17.05-host-and-ios-commands | The Show Version Command | 5:37 | **cli-basics** | код-рендер терминала ~3:00 + эталонный вывод `show version` для симулятора | — | [doc](17-build-a-small-network/17.05-host-and-ios-commands--dFKfyJkuSqQ.md) |

## Сводка — модули 01, 02, 03, 05, 07, 08

**Всего:** 20 видео. **По классам:** `cli-basics` — 6, `lab-demo` — 6, `explainer` — 5, `marketing` — 2, `other` — 1.

**Маркетинг → убрать (2):** `wcIP__5sa1o` (промо Cisco Networking Academy, 1.1.2 — убрать вместе с разделом) и `e85Y71fsyyY` (реклама Cisco Webex, 1.7.5 — убрать, одна фраза в 1.7.4). Пограничный случай `7E9ilk9dOOI` (установка PT через netacad.com) — не маркетинг, но половина ролика привязана к NetAcad-аккаунту, который у нас не используется; заменить пошаговым текстом со скриншотами актуального установщика.

**Самое ценное для симулятора (модуль 02 — 8 роликов, все с дословными сессиями в документах):**
- **Z-n1tO4Xg6w (2.2.5) и B269UlVAN40 (2.2.3)** — навигация по режимам: `enable/disable`, `configure terminal`/`config t`, `exit` (включая выход из консоли по `exit` из `#`), `end`, `^Z`, `line console 0`, `line vty 0 15`, `interface vlan 1`, прямые переходы между вложенными режимами. Первый тренинг.
- **K_VEPe8aRUE (2.3.4)** — три формы `?` (отдельно / `in?` / `interface ?`), `--More--`, три сообщения проверщика: `% Invalid input detected at '^' marker.`, `% Ambiguous command: "i"`, `% Incomplete command.` — с полными списками команд PT 2960 для user EXEC / privileged EXEC / global config.
- **YDXgJUjGjcw (2.3.6)** — правила Tab-дополнения (`en`⇥, `con`⇥ не работает, `conf`⇥), сокращения (`int f 0/1`), история ↑/↓, `^Z`, `^C`, `^A/^E`, `Translating "congh"...domain server (255.255.255.255) % Name lookup aborted` по Ctrl+Shift+6, `^R` после syslog-сообщений (показано на реальном Catalyst).
- **Ae9qSUlJ3a4 (2.4.6)** — полный цикл защиты: `line console 0` / `password` / `login`, `enable secret`, `line vty 0 15`, `service password-encryption`, `banner motd`, с `show running-config` до и после (`enable secret 5 $1$mERr$…`, `password 7 0822455D0A16`) и повторными входами (`User Access Verification / Password:`).
- **lQQ28pdSqfg (2.5.3)** — `copy running-config startup-config` (диалог `Destination filename`), `dir ?`, `dir nvram:`, `copy run start`, `reload`, `erase startup-config` (`Erasing the nvram filesystem will remove all configuration files! Continue? [confirm]` / `Erase of nvram: complete`), `copy startup-config running-config` (слияние).
- **CkvRVRcOkls / gex3BaiuQiw (2.8.1–2.8.2)** — диагностика SVI: полный `show ip interface brief` 2960, `administratively down` → `no shutdown`, `ip address 192.168.1.3 255.255.255.0`; `ping` с ПК с первым `Request timed out.` (ARP) и TTL 255/128.
- **pt_Qw1Jfo5w (8.5.5)** — полный `show ip route` R1 (C/L/O/S*, `[110/65]`, `Gateway of last resort`), плюс подразумеваемая конфигурация двух маршрутизаторов с OSPF и статическим маршрутом по умолчанию.

**Самые ценные для контент-библиотеки (анимации):** таблицы MAC-адресов на двух коммутаторах + кадр на шлюз (7.3.4–7.3.5 — один ассет-схема на оба), «устройства в пузыре» (3.1.1), перевод чисел (5.1.2, 5.2.2 — заодно шаблон тренажёра «перевод октета»).

**Фактические неточности в оригиналах (исправить при пересборке):**
- **CkvRVRcOkls (2.8.1):** в финале диктор говорит «address 192.168.1.1», на экране и по заданию — `192.168.1.3`.
- **aOwXEempJ4k (8.3.5):** (а) «Payload length — общий размер пакета» — нет, это длина *без* 40-байтного заголовка IPv6 (в отличие от Total Length в IPv4); (б) Neighbor Solicitation ищет MAC-адрес (link-layer) известного IPv6-адреса, а не «link-local адрес»; (в) показанный NS не является запросом к «тому же устройству, что в первых скриншотах» — его шлёт хост `Ibm_82:95:b5` на solicited-node адрес с его же суффиксом, цель не видна; при пересборке взять однозначную пару NS → NA.
- **gex3BaiuQiw (2.8.2):** совет «отключить брандмауэр Windows» — заменить на «разрешить входящие ICMPv4 Echo»; причина первого `Request timed out.` (ARP) не названа.
- **PArGE7H_eN8 (8.2.3):** «DF — пакет не настолько большой / не предназначен для фрагментации» — бит DF запрещает фрагментацию маршрутизаторам, размер ни при чём.
- **YDXgJUjGjcw (2.3.6):** «IOS пытается превратить буквы в IP-адрес» — IOS трактует неизвестное слово как имя хоста и делает DNS-запрос (лекарство — `no ip domain-lookup`); «Ctrl+R не поддерживается в этой версии PT» — проверить на текущей.
- **Ae9qSUlJ3a4 (2.4.6):** «secret… будет зашифрован» — захеширован (MD5, type 5); команда `hostname` в ролике отсутствует (в текст 2.4.1 входит).
- **lQQ28pdSqfg (2.5.3):** слияние при `copy start run` заявлено, но не показано (пароль консоли остаётся) — добавить `show run`; в PT `reload` после `erase startup-config` не спрашивает о сохранении, на реальном IOS спросит.
- **uync1j2x6Ms (1.0.4):** линк Switch0–Router0 красный (интерфейс маршрутизатора `shutdown` по умолчанию) — диктор не объясняет; голос «порт 24», подсказка на экране `FastEthernet0/22`; меню File (Open Samples, Exit and Logout) из текста 1.0.4 не показано.
- **7E9ilk9dOOI (1.0.3):** страница загрузки показывает PT 7.3.1, установлен 8.0.0 BETA Build 126.
- **pt_Qw1Jfo5w (8.5.5):** топология и листинг отличаются от текста 8.5.6 (`[110/65]` и `S* … is directly connected, Serial0/1/0` против `[110/2]` и `S* … [1/0] via 209.165.200.226`) — унифицировать.
- **50O7DGHEz6A (5.2.2):** оговорка «convert the 8-bit binary number to decimal» (на слайде верно — to hexadecimal). **lxeBvUOA9oE (5.1.2):** опечатка титула «Convert an P address»; при замене 2 → 9 строка Total на слайде осталась 2168. **yWjd-4WN4hE (3.1.1):** DNS-сервер на схеме `2001:4840:4860::8888`, в карточке `2001:4860:4860::8888`.
- Без ошибок: B269UlVAN40, Z-n1tO4Xg6w, K_VEPe8aRUE, fi7Ss-_9LvY, RXLercop7eU.

**Чего не удалось прочитать:** ничего критичного. В `K_VEPe8aRUE` первые 2–3 строки двух страниц `?` (`clear`, `clock`; `aaa`, `access-list`, `banner`) ушли за верх экрана и восстановлены по PT 2960 (помечены в документе). Нажатия клавиш в `YDXgJUjGjcw` на экране не видны — восстановлены по голосу и результату.

## Сводка — модули 09, 10, 11, 14, 17

**Всего:** 16 видео, суммарно ~1 ч 36 мин. **По классам:** `explainer` — 12, `lab-demo` — 2 (RH_KIUdHZlE, UbqcbYsPoss), `cli-basics` — 1 (dFKfyJkuSqQ), `other` — 1 (DNL4DPxjgNM, обзор физического оборудования), `marketing` — 0.

**Маркетинговых видео нет.** Единственный кандидат на удаление — **DNL4DPxjgNM** (10.4.1, «Network Device Differences – Part 1»): фотографии задних панелей Cisco 4321/2951/1941 с рекомендацией NetAcad «4221 + 2960+»; для курса на симуляторе физический обзор не нужен — заменить абзацем и одной схемой о правилах именования интерфейсов (`G0/0/0` vs `G0/0`, `S0/1/0`), которые действительно нужны в CLI.

**Самое ценное для симулятора:**
- **RH_KIUdHZlE (10.4.2)** — консольные сессии трёх реальных роутеров (ISR 4321, 2951, 1941): `show ip interface brief`, `show interfaces` (строки `media type is SX / RJ45`), `configure terminal` → `interface` → `ip address` → `no shutdown`, сообщения `%LINK-3-UPDOWN` / `%LINEPROTO-5-UPDOWN`, `ping` с 80 % → 100 % (ARP). В документе — полная дословная сессия (адреса 10.0.0.0/30 и 172.16.0.0/30) с выводами; это эталон «первая адресация точка-точка» и наглядный урок о том, что имена интерфейсов зависят от модели.
- **dFKfyJkuSqQ (17.5.8)** — полный вывод `show version` ISR 4321 / IOS XE 16.6.4 с разбором каждого блока (образ, uptime, причина перезагрузки, лицензии, DRAM/NVRAM/flash, регистр 0x2102); эталон для симулятора снят целиком.
- **UbqcbYsPoss (14.5.5)** — реальный захват Wireshark рукопожатия и закрытия HTTP-соединения (10.1.1.1:1061 ↔ 192.168.254.254:80, кадры 10–19 с Seq/Ack и флагами); в документе — таблица кадров и сценарий воспроизведения для симулятора с анализатором.
- Косвенно: **1ZB2euss3YY** (сводная сессия `arp -a` / `arp -d` / `ping` / `show ip arp` по теме 9.2), **S0SyGKhCEV0** (`show ipv6 neighbors`, `netsh interface ipv6 show neighbors`), **DNL4DPxjgNM** (проверка `show ip interface brief` / `media-type`).

**Самые ценные для контент-библиотеки (чистые концепты под анимацию/код-рендер):** тройка ARP 9.2.3–9.2.5 (одна Figma-сцена, три трека), IPv6 ND (9.3.1), побитовое И (11.1.5), магическое число (11.5.4 + 11.6.4 — объединить в один ролик ~5 мин), пример VLSM (11.8.2), надёжность TCP (14.6.2 + 14.6.4).

**Фактические неточности в оригиналах (исправить при пересборке):**
- **tna6DaUeu5c (9.2.3):** диктор и ручные субтитры называют адрес PC-A «192.168.1.10», на схеме — 192.168.1.110; в кадре не показано поле Type 0x806 (текст его описывает).
- **1ZB2euss3YY (9.2.5):** поля ARP-ответа подписаны «Target IPv4 / Target MAC» (в 9.2.4 те же поля — «Sender»); знак ⊘ на линии R1 → Internet остался от предыдущего ролика и противоречит смыслу сцены (кадр должен уйти через R1).
- **S0SyGKhCEV0 (9.3.1):** выноска у PC-C в сцене NA говорит «for the IPv4 address» (скопирована из ролика ARP); значения solicited-node multicast (ff02::1:ff00:50 / 33-33-FF-00-00-50) не показаны — в пересборке показать.
- **DNL4DPxjgNM (10.4.1):** на слайде заявлен 4221, на фото 4321; диктор называет разделяемый SFP-порт 2951 «gig 0/2», на фото это GE 0/1.
- **RH_KIUdHZlE (10.4.2):** сообщение `changed state to down` после `no shutdown` на R2 g0/2 (сосед ещё выключен) не прокомментировано — учащийся сочтёт ошибкой; управляющие `GigabitEthernet0` / `Embedded-Service-Engine0/0` не объяснены.
- **LKjCyGaiH4Q (11.5.3):** формула на слайде «Host bits = 2⁷ = 128-2 = 126» записана небрежно; терминология «классовые/бесклассовые маски» — историческая, текст курса её не использует.
- **tz7eawYRHf0 (14.6.2):** «10 байт — это размер окна» (на схеме — объём сегмента, окно не показано); «сегодня окна обычно 16 МБ и больше» — преувеличение (поле 16 бит, с масштабированием до 1 ГиБ); на схеме Cisco третий сегмент имеет Ack = 2 при отсутствии данных от сервера — должно быть 1.
- **UbqcbYsPoss (14.5.5):** вывод диктора «Ack 374 говорит о двух разных захватах» ошибочен — 374 = 1 + 373 байта `GET`, захват непрерывный (кадры 10–19, 16.303–16.310 с); это, наоборот, хороший пример расчёта Seq/Ack. Завершение в захвате инициирует сервер (текст 14.5.3 описывает инициативу клиента — стоит проговорить, что это может быть любая сторона).
- **dFKfyJkuSqQ (17.5.8):** «2 ГБ DRAM» (1,8 ГБ выделено IOSd) и «4 ГБ физической памяти» объяснены неточно для IOS XE; значение регистра 0x2142 для восстановления пароля не названо; схема лицензирования PAK/UDI устарела (Smart Licensing).
- Без ошибок: Ud1angOlxHE, 7DoggTtOLN0, A2P7i6ebSCE, TJSWlSplC1Q, R_Ti9y2AShc, _V-YboU4Rq4, 3AzR-82OI7Q (мелкие оговорки диктора перечислены в документах).

**Дефекты загрузки:** нет — все 16 MP4 полной длины (видео = аудио), кадры и субтитры полные. У tna6DaUeu5c есть ручные субтитры en + ru; у остальных — автоматические en. Текст терминала в RH_KIUdHZlE и dFKfyJkuSqQ (640×360) читается только при 2–4× увеличении с кадрированием — сделано, выводы сняты дословно.

**Замечания по тексту курса:** в `10.03-configure-the-default-gateway/README.md` оба ролика «различия сетевых устройств» (темы Cisco 10.4.1/10.4.2) подшиты под заголовком темы 10.3 — при реструктуризации вынести в отдельный раздел «Подготовка к лабораторным» или удалить вместе с DNL4DPxjgNM. В `11.05-subnet-an-ipv4-network/README.md` заголовок 11.5.4 закомментирован, ролик A2P7i6ebSCE стоит без подписи. В `11.08-…/README.md` второй ролик (_V-YboU4Rq4) — без заголовка 11.8.2.

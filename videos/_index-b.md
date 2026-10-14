# Индекс видео — рабочий фрагмент B (модули 09, 10, 11, 14, 17)

Классификация и посценные сценарии 16 видео, встроенных в модули 09, 10, 11, 14 и 17 курса `learn-ccna1`. Все видео — перезалив роликов Cisco Networking Academy (ITN v7) на канале оператора, май 2022, язык — английский. Координатор сольёт этот фрагмент и фрагмент A (модули 01–08) в `videos/README.md`.

## Таблица

| videoId | module/topic | Название (EN) | Длит. | Класс | Предложение по пересборке | Документ |
|---|---|---|---|---|---|---|
| tna6DaUeu5c | 09/09.02-arp | ARP Operation – ARP Request | 2:53 | explainer | анимация Figma ≤ 60 с (трек 1 общей сцены «ARP в LAN») | [doc](09-address-resolution/09.02-arp--tna6DaUeu5c.md) |
| Ud1angOlxHE | 09/09.02-arp | ARP Operation – ARP Reply | 1:45 | explainer | анимация Figma ≤ 60 с (трек 2 той же сцены) | [doc](09-address-resolution/09.02-arp--Ud1angOlxHE.md) |
| 1ZB2euss3YY | 09/09.02-arp | ARP Role in Remote Communications | 3:01 | explainer | анимация Figma ≤ 60 с (трек 3) + сессия `arp -a` / `show ip arp` для симулятора | [doc](09-address-resolution/09.02-arp--1ZB2euss3YY.md) |
| S0SyGKhCEV0 | 09/09.03-neighbor-discovery | IPv6 Neighbor Discovery | 6:07 | explainer | код-рендер с генер. голосом ~2:30–3:00 (или 2 анимации NS / NA) | [doc](09-address-resolution/09.03-neighbor-discovery--S0SyGKhCEV0.md) |
| DNL4DPxjgNM | 10/10.03-configure-the-default-gateway | Network Device Differences – Part 1 | 4:31 | **other** (обзор физического оборудования) | **убрать** как видео; текст + иллюстрация «имена интерфейсов по моделям» | [doc](10-basic-router-configuration/10.03-configure-the-default-gateway--DNL4DPxjgNM.md) |
| RH_KIUdHZlE | 10/10.03-configure-the-default-gateway | Network Device Differences – Part 2 | 10:16 | **lab-demo** (по содержанию cli-basics) | код-рендер терминала ~4:00 + полная сессия трёх роутеров для симулятора | [doc](10-basic-router-configuration/10.03-configure-the-default-gateway--RH_KIUdHZlE.md) |
| 7DoggTtOLN0 | 11/11.01-ipv4-address-structure | Network, Host and Broadcast Addresses | 6:22 | explainer | анимация Figma ≤ 60 с (побитовое И) / текст + иллюстрация | [doc](11-ipv4-addressing/11.01-ipv4-address-structure--7DoggTtOLN0.md) |
| LKjCyGaiH4Q | 11/11.05-subnet-an-ipv4-network | The Subnet Mask | 8:09 | explainer | код-рендер ~2:30 (можно объединить с A2P7i6ebSCE) | [doc](11-ipv4-addressing/11.05-subnet-an-ipv4-network--LKjCyGaiH4Q.md) |
| A2P7i6ebSCE | 11/11.05-subnet-an-ipv4-network | Subnet with the Magic Number | 14:50 | explainer | код-рендер ~4:00 + сводная таблица /25…/30 в текст | [doc](11-ipv4-addressing/11.05-subnet-an-ipv4-network--A2P7i6ebSCE.md) |
| TJSWlSplC1Q | 11/11.06-subnet-a-16-and-8-prefix | Subnet Across Multiple Octets | 5:21 | explainer | анимация Figma ≤ 60 с / финал объединённого ролика «магическое число» | [doc](11-ipv4-addressing/11.06-subnet-a-16-and-8-prefix--TJSWlSplC1Q.md) |
| R_Ti9y2AShc | 11/11.08-variable-length-subnet-masking | VLSM Basics | 2:32 | explainer | текст + иллюстрация (или пролог ≤ 30 с к примеру VLSM) | [doc](11-ipv4-addressing/11.08-variable-length-subnet-masking--R_Ti9y2AShc.md) |
| _V-YboU4Rq4 | 11/11.08-variable-length-subnet-masking | VLSM Example | 10:24 | explainer | код-рендер ~3:30 (дерево подсетей) | [doc](11-ipv4-addressing/11.08-variable-length-subnet-masking--_V-YboU4Rq4.md) |
| UbqcbYsPoss | 14/14.05-tcp-communication-process | TCP 3-Way Handshake (Wireshark) | 6:55 | **lab-demo** | код-рендер ~3:00 (синтетический Wireshark) + сценарий захвата для симулятора | [doc](14-transport-layer/14.05-tcp-communication-process--UbqcbYsPoss.md) |
| tz7eawYRHf0 | 14/14.06-reliability-and-flow-control | TCP Reliability – Sequence Numbers and Acknowledgements | 4:06 | explainer | анимация Figma ≤ 60 с / текст + исправленная иллюстрация | [doc](14-transport-layer/14.06-reliability-and-flow-control--tz7eawYRHf0.md) |
| 3AzR-82OI7Q | 14/14.06-reliability-and-flow-control | TCP Reliability – Data Loss and Retransmission | 3:24 | explainer | анимация Figma ≤ 60 с (+ опц. трек SACK) | [doc](14-transport-layer/14.06-reliability-and-flow-control--3AzR-82OI7Q.md) |
| dFKfyJkuSqQ | 17/17.05-host-and-ios-commands | The Show Version Command | 5:37 | **cli-basics** | код-рендер терминала ~3:00 + эталонный вывод `show version` для симулятора | [doc](17-build-a-small-network/17.05-host-and-ios-commands--dFKfyJkuSqQ.md) |

## Сводка

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

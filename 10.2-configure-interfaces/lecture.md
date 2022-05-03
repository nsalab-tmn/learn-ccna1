<!-- verified: agorbachev 03.05.2022 -->

<!-- 10.2.1 -->
## Настройка интерфейсов маршрутизатора

На этом этапе маршрутизаторы имеют свои базовые конфигурации. Следующим шагом является настройка их интерфейсов. Это связано с тем, что маршрутизаторы не доступны конечным устройствам до тех пор, пока не будут настроены интерфейсы. На маршрутизаторах Cisco используется множество разных интерфейсов. Например, маршрутизатор Cisco ISR 4321 оснащен двумя интерфейсами Gigabit Ethernet:

* **GigabitEthernet 0/0/0 (G0/0/0)**
* **GigabitEthernet 0/0/1 (G0/0/1)**

Задача настройки интерфейса маршрутизатора очень похожа на управление SVI на коммутаторе. В частности, он включает в себя выполнение следующих команд:

```
Router(config)# interface type-and-number
Router(config-if)# description description-text
Router(config-if)# ip address <ipv4-address> <subnet-mask>
Router(config-if)# ipv6 address <ipv6-address/prefix-length>
Router(config-if)# no shutdown
```

**Примечание:** Когда интерфейс маршрутизатора включен, должны отображаться информационные сообщения, подтверждающие включенную связь.

Несмотря на то, что команда **description** не требуется для включения интерфейса, рекомендуется использовать ее. Это может быть полезно при устранении неполадок в производственных сетях, предоставляя информацию о типе подключенной сети. Если интерфейс подключен к интернет-провайдеру или оператору услуги, команда **description** будет полезна для ввода стороннего подключения и контактной информации.

**Примечание**: Текст описания может содержать не более 240 символов.

Использование команды **no shutdown** активирует интерфейс и аналогично включению интерфейса. Для активации физического уровня интерфейс должен быть также подключен к другому устройству (коммутатору или маршрутизатору).

**Примечание**: В межмаршрутизаторских соединениях, где нет коммутатора Ethernet, оба взаимосвязанных интерфейса должны быть настроены и включены.

<!-- 10.2.2 -->
## Пример настройки интерфейсов маршрутизатора

В этом примере будут включены напрямую подключенные интерфейсы R1 в схеме топологии.

![](./assets/10.2.2.png)
<!-- /courses/itn-dl/aeed2ea2-34fa-11eb-ad9a-f74babed41a6/af222150-34fa-11eb-ad9a-f74babed41a6/assets/2e1f6ac2-1c25-11ea-81a0-ffc2c49b96bc.svg -->

Чтобы настроить интерфейсы на R1, используйте следующие команды.

```
R1> enable
R1# configure terminal
Enter configuration commands, one per line.
End with CNTL/Z.
R1(config)# interface gigabitEthernet 0/0/0
R1(config-if)# description Link to LAN
R1(config-if)# ip address 192.168.10.1 255.255.255.0
R1(config-if)# ipv6 address 2001:db8:acad:10::1/64
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)#
*Aug  1 01:43:53.435: %LINK-3-UPDOWN: Interface GigabitEthernet0/0/0, changed state to down
*Aug  1 01:43:56.447: %LINK-3-UPDOWN: Interface GigabitEthernet0/0/0, changed state to up
*Aug  1 01:43:57.447: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0/0, changed state to up
R1(config)#
R1(config)#
R1(config)# interface gigabitEthernet 0/0/1
R1(config-if)# description Link to R2
R1(config-if)# ip address 209.165.200.225 255.255.255.252
R1(config-if)# ipv6 address 2001:db8:feed:224::1/64
R1(config-if)# no shutdown
R1(config-if)# exit
R1(config)#
*Aug  1 01:46:29.170: %LINK-3-UPDOWN: Interface GigabitEthernet0/0/1, changed state to down
*Aug  1 01:46:32.171: %LINK-3-UPDOWN: Interface GigabitEthernet0/0/1, changed state to up
*Aug  1 01:46:33.171: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0/1, changed state to up
R1(config)#
```

**Примечание:** Обратите внимание на информационные сообщения, информирующие нас о том, что G0/0/0 и G0/0/1 включены.

<!-- 10.2.3 -->
## Проверка конфигурации интерфейса

Для проверки конфигурации интерфейса можно использовать несколько команд. Наиболее полезными из них являются команды **show ip interface brief** и **show ipv6 interface brief**, как показано в примере.

```
R1#  show ip interface brief
Interface IP-Address OK? Method Status Protocol 
GigabitEthernet0/0/0 192.168.10.1 YES manual up up 
GigabitEthernet0/0/1 209.165.200.225 YES manual up up 
Vlan1 unassigned YES unset administratively down down 
R1#  show ipv6 interface brief
GigabitEthernet0/0/0 [up/up]
    FE80::201:C9FF:FE89:4501
    2001:DB8:ACAD:10::1
GigabitEthernet0/0/1 [up/up]
    FE80::201:C9FF:FE89:4502
    2001:DB8:FEED:224::1
Vlan1 [administratively down/down]
    unassigned 
R1#
```

<!-- 10.2.4 -->
## Команды проверки конфигурации

В таблице приведены наиболее популярные **show** команды, используемые для проверки конфигурации интерфейса.

| Команды | Описание |
| --- | --- |
| `show ip interface brief`<br>`show ipv6 interface brief` | Выходные данные содержат все интерфейсы, их IP адреса, а также их текущее состояние. Активные и действующие интерфейсы представлены значением «up» в столбцах «Status» и «Protocol». Любые другие значения будут означать наличие проблемы либо с настройками, либо с подключением кабелей. |
| `show ip route`<br>`show ipv6 route` | Отображает содержимое таблицы маршрутизации IPv4, которая хранится в ОЗУ. |
| `show interfaces` | Отображает статистические сведения по всем интерфейсам устройства. Тем не менее, эта будет отображать только информацию об адресации IPv4. |
| `show ip interfaces` | Отображает статистику IPv4 всех интерфейсов маршрутизатора. |
| `show ipv6 interface` | Отображает статистику IPv6 всех интерфейсов маршрутизатора. |

### show ip interface brief

```
R1# show ip interface brief
Interface IP-Address OK? Method Status Protocol 
GigabitEthernet0/0/0 192.168.10.1 YES manual up up 
GigabitEthernet0/0/1 209.165.200.225 YES manual up up 
Vlan1 unassigned YES unset administratively down down 
R1#
```

### show ipv6 interface brief

```
R1# show ipv6 interface brief
GigabitEthernet0/0/0 [up/up]
    FE80::201:C9FF:FE89:4501
    2001:DB8:ACAD:10::1
GigabitEthernet0/0/1 [up/up]
    FE80::201:C9FF:FE89:4502
    2001:DB8:FEED:224::1
Vlan1 [administratively down/down]
    unassigned 
R1#
```

### show ip route

```
R1# show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR
Gateway of last resort is not set
      192.168.10.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.10.0/24 is directly connected, GigabitEthernet0/0/0
L        192.168.10.1/32 is directly connected, GigabitEthernet0/0/0
      209.165.200.0/24 is variably subnetted, 2 subnets, 2 masks
C        209.165.200.224/30 is directly connected, GigabitEthernet0/0/1
L        209.165.200.225/32 is directly connected, GigabitEthernet0/0/1
R1#
```

### show ipv6 route

```
R1# show ipv6 route
IPv6 Routing Table - default - 5 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
       I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
       EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
       NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
       OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
       ON2 - OSPF NSSA ext 2, a - Application
C 2001:DB8:ACAD:10::/64 [0/0]
     via GigabitEthernet0/0/0, directly connected
L 2001:DB8:ACAD:10::1/128 [0/0]
     via GigabitEthernet0/0/0, receive
C 2001:DB8:FEED:224::/64 [0/0]
     via GigabitEthernet0/0/1, directly connected
L 2001:DB8:FEED:224::1/128 [0/0]
     via GigabitEthernet0/0/1, receive
L FF00::/8 [0/0]
     via Null0, receive
R1# 
```

### show interfaces

```
R1# show interfaces gig0/0/0
GigabitEthernet0/0/0 is up, line protocol is up 
  Hardware is ISR4321-2x1GE, address is a0e0.af0d.e140 (bia a0e0.af0d.e140)
  Description: Link to LAN
  Internet address is 192.168.10.1/24
  MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive not supported 
  Full Duplex, 100Mbps, link type is auto, media type is RJ45
  output flow-control is off, input flow-control is off
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:01, output 00:00:35, output hang never
  Last clearing of show interface counters never
  Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     1180 packets input, 109486 bytes, 0 no buffer
     Received 84 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles 
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 1096 multicast, 0 pause input
     65 packets output, 22292 bytes, 0 underruns
     0 output errors, 0 collisions, 2 interface resets
     11 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     1 lost carrier, 0 no carrier, 0 pause output
     0 output buffer failures, 0 output buffers swapped out
R1#
```

### show ip interface

```
R1# show ip interface g0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  Internet address is 192.168.10.1/24
  Broadcast address is 255.255.255.255
  Address determined by setup command
  MTU is 1500 bytes
  Helper address is not set
  Directed broadcast forwarding is disabled
  Outgoing Common access list is not set 
  Outgoing access list is not set
  Inbound Common access list is not set 
  Inbound  access list is not set
  Proxy ARP is enabled
  Local Proxy ARP is disabled
  Security level is default
  Split horizon is enabled
  ICMP redirects are always sent
  ICMP unreachables are always sent
  ICMP mask replies are never sent
  IP fast switching is enabled
  IP Flow switching is disabled
  IP CEF switching is enabled
  IP CEF switching turbo vector
  IP Null turbo vector
  Associated unicast routing topologies:
        Topology "base", operation state is UP
  IP multicast fast switching is enabled
  IP multicast distributed fast switching is disabled
  IP route-cache flags are Fast, CEF
  Router Discovery is disabled
  IP output packet accounting is disabled
  IP access violation accounting is disabled
  TCP/IP header compression is disabled
  RTP/IP header compression is disabled
  Probe proxy name replies are disabled
  Policy routing is disabled
  Network address translation is disabled
  BGP Policy Mapping is disabled
  Input features: MCI Check
  IPv4 WCCP Redirect outbound is disabled
  IPv4 WCCP Redirect inbound is disabled
  IPv4 WCCP Redirect exclude is disabled
R1#
```

### show ipv6 interface

```
R1# show ipv6 interface g0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  IPv6 is enabled, link-local address is FE80::868A:8DFF:FE44:49B0
  No Virtual link-local address(es):
  Description: Link to LAN
  Global unicast address(es):
    2001:DB8:ACAD:10::1, subnet is 2001:DB8:ACAD:10::/64
  Joined group address(es):
    FF02::1
    FF02::1:FF00:1
    FF02::1:FF44:49B0
  MTU is 1500 bytes
  ICMP error messages limited to one every 100 milliseconds
  ICMP redirects are enabled
  ICMP unreachables are sent
  ND DAD is enabled, number of DAD attempts: 1
  ND reachable time is 30000 milliseconds (using 30000)
  ND NS retransmit interval is 1000 milliseconds
R1#
```

<!-- 10.2.5 -->
<!-- ## Инструмент проверки синтаксиса. Настройка интерфейсов -->


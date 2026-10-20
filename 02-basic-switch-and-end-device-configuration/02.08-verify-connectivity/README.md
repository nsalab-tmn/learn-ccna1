<!-- verified: agorbachev 03.05.2022 -->

<!-- 2.8.1 -->
## Видеозадание: проверка состояния интерфейса

В этой части вы создадите основные подключения, настроив IP-адресацию на коммутаторах и ПК. Затем вы проверите свои конфигурации и возможности подключения, потому что настройка устройства теряет смысл, если вы не проверяете, работает ли конфигурация. Этот процесс будет продолжен в этом разделе. Используя интерфейс командной строки, вы проверите интерфейсы и адреса коммутаторов и маршрутизаторов сети.

Так же как вы используете команды и утилиты, например, **ipconfig**, для проверки сетевой конфигурации узла, вы используете команды для проверки интерфейсов и параметров адресов промежуточных устройств (коммутаторов и маршрутизаторов).

Посмотрите видео, демонстрирующее использование команды **show ip interface brief**. Эта команда позволяет проверить состояние интерфейсов коммутаторов.

Команда **ipconfig** на узле выводит его IPv4-адрес, маску подсети и шлюз по умолчанию. Команда **show ip interface brief** на коммутаторе выводит для каждого интерфейса его IP-адрес и состояние: столбец Status показывает состояние физического уровня, столбец Protocol — канального. У коммутатора IP-адрес есть только у виртуального интерфейса Vlan1 (SVI).

```
C:\>ipconfig

FastEthernet0 Connection:(default port)

   Connection-specific DNS Suffix..:
   Link-local IPv6 Address.........: FE80::2D0:84FF:FE55:DC01
   IPv6 Address....................: ::
   IPv4 Address....................: 192.168.1.10
   Subnet Mask.....................: 255.255.255.0
   Default Gateway.................: 192.168.1.1

C:\>
```

```
Sw-Floor-1#show ip interface brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/1            unassigned      YES unset  up                    up
FastEthernet0/2            unassigned      YES unset  up                    up
FastEthernet0/3            unassigned      YES unset  down                  down
FastEthernet0/4            unassigned      YES unset  down                  down
FastEthernet0/5            unassigned      YES unset  down                  down
FastEthernet0/6            unassigned      YES unset  down                  down
FastEthernet0/7            unassigned      YES unset  down                  down
FastEthernet0/8            unassigned      YES unset  down                  down
FastEthernet0/9            unassigned      YES unset  down                  down
FastEthernet0/10           unassigned      YES unset  down                  down
FastEthernet0/11           unassigned      YES unset  down                  down
FastEthernet0/12           unassigned      YES unset  down                  down
FastEthernet0/13           unassigned      YES unset  down                  down
FastEthernet0/14           unassigned      YES unset  down                  down
FastEthernet0/15           unassigned      YES unset  down                  down
FastEthernet0/16           unassigned      YES unset  down                  down
FastEthernet0/17           unassigned      YES unset  down                  down
FastEthernet0/18           unassigned      YES unset  down                  down
FastEthernet0/19           unassigned      YES unset  down                  down
FastEthernet0/20           unassigned      YES unset  down                  down
FastEthernet0/21           unassigned      YES unset  down                  down
FastEthernet0/22           unassigned      YES unset  down                  down
FastEthernet0/23           unassigned      YES unset  down                  down
FastEthernet0/24           unassigned      YES unset  down                  down
GigabitEthernet0/1         unassigned      YES unset  down                  down
GigabitEthernet0/2         unassigned      YES unset  down                  down
Vlan1                      192.168.1.20    YES manual up                    up
Sw-Floor-1#
```

![youtube](https://www.youtube.com/watch?v=CkvRVRcOkls)

<!-- 2.8.2 -->
## Видеозадание: проверка сквозного подключения

Команду **ping** можно использовать для проверки подключения к другому устройству по сети или к сайту в Интернете.

Посмотрите видео, демонстрирующее использование команды **ping** для проверки подключения к коммутатору и другому ПК.

В примере узел PC1 проверяет связь с коммутатором по адресу его интерфейса Vlan1, а затем с узлом PC2. Каждая строка Reply from — ответ на один эхо-запрос; итоговая статистика показывает, сколько запросов отправлено, сколько ответов получено и сколько потеряно.

```
C:\>ping 192.168.1.20

Pinging 192.168.1.20 with 32 bytes of data:

Reply from 192.168.1.20: bytes=32 time<1ms TTL=255
Reply from 192.168.1.20: bytes=32 time<1ms TTL=255
Reply from 192.168.1.20: bytes=32 time<1ms TTL=255
Reply from 192.168.1.20: bytes=32 time<1ms TTL=255

Ping statistics for 192.168.1.20:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms

C:\>ping 192.168.1.11

Pinging 192.168.1.11 with 32 bytes of data:

Reply from 192.168.1.11: bytes=32 time=1ms TTL=128
Reply from 192.168.1.11: bytes=32 time<1ms TTL=128
Reply from 192.168.1.11: bytes=32 time<1ms TTL=128
Reply from 192.168.1.11: bytes=32 time<1ms TTL=128

Ping statistics for 192.168.1.11:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 1ms, Average = 0ms
C:\>
```

![youtube](https://www.youtube.com/watch?v=gex3BaiuQiw)


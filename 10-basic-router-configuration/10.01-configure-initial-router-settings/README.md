<!-- verified: agorbachev 03.05.2022 -->

<!-- 10.1.1 -->
## Шаги для базовой конфигурации

При настройке начальных параметров маршрутизатора необходимо выполнить следующие задачи.

1\. Настройте имя устройства.

```
Router(config)# hostname
```

2\. Обеспечьте безопасность привилегированного режима EXEC.

```
Router(config)# enable secret <secret_password>
```

3\. Обеспечьте безопасность доступа к пользовательскому режиму EXEC.

```
 Router(config)# line console 0 
 Router(config-line)# password <plain_text_password> 
 Router(config-line)# login 
```

4\. Обеспечьте безопасность удаленного доступа по протоколу Telnet или SSH.

```
 Router(config-line)# line vty 0 4 
 Router(config-line)# password <plain_text_password>
 Router(config-line)# login 
 Router(config-line)# transport input { ssh | telnet} 
```

5\. Защитите все пароли в файле конфигурации.

```
Router(config-line)# exit
Router(config)# service password-encryption
```

6\. Создайте баннер с правовым уведомлением.

```
Router(config)# banner motd <# message #>
```

7\. Сохраните конфигурацию.

```
Router(config)# end
Router# copy running-config startup-config
```

<!-- 10.1.2 -->
## Базовая конфигурация маршрутизатора

В этом примере маршрутизатор R1 в схеме топологии будет настроен с исходными параметрами.

![](./assets/10.1.2.svg)


Чтобы настроить имя устройства для R1, используйте следующие команды:

```
Router> enable 
Router# configure terminal 
Enter configuration commands, one per line.
End with CNTL/Z.
Router(config)# hostname R1 
R1(config)#
```

**Примечание:** Обратите внимание, как в запросе маршрутизатора теперь отображается имя узла.

Весь доступ маршрутизатора должен быть защищен. Привилегированный режим EXEC — самый важный режим для защиты. Он дает полный доступ к устройству и его конфигурации.

Следующие команды обеспечивают защиту привилегированного и пользовательского режимов EXEC, разрешают удаленный доступ Telnet и SSH, а также шифруют все пароли открытого текста (например, пользовательские EXEC и VTY line):

```
R1(config)# enable secret class 
R1(config)#
R1(config)# line console 0 
R1(config-line)# password cisco 
R1(config-line)# login 
R1(config-line)# exit 
R1(config)#
R1(config)# line vty 0 4 
R1(config-line)# password cisco 
R1(config-line)# login 
R1(config-line)# transport input ssh telnet 
R1(config-line)# exit 
R1(config)#
R1(config)# service password-encryption 
R1(config)#
```

Правовое уведомление предупреждает, что к устройству должны обращаться только разрешенные пользователи. Оно настраивается следующим образом:

```
R1(config)# banner motd #
Enter TEXT message. End with a new line and the #
*********************************************** 
WARNING: Unauthorized access is prohibited!
***********************************************
#
R1(config)#
```

Если маршрутизатор случайно потеряет питание, все настроенные команды будут потеряны. Поэтому важно сохранить внесенные изменения. Следующая команда сохраняет конфигурацию в NVRAM:

```
R1# copy running-config startup-config
Destination filename [startup-config]? 
Building configuration...
[OK]
R1#
```

<!-- 10.1.3 -->
<!-- syntax -->




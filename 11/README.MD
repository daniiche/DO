```
1
vagrant@vagrant:~$ ip -c -br link
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
eth0             UP             08:00:27:73:60:cf <BROADCAST,MULTICAST,UP,LOWER_UP>

windows
ipconfig/all


2
LLDP информация о соседнем устройстве


vagrant@vagrant:~$ sudo apt install lldpd

vagrant@vagrant:~$ lldpctl
-------------------------------------------------------------------------------
LLDP neighbors:
-------------------------------------------------------------------------------

3
VLAN – виртуальное разделение коммутатора

vagrant@vagrant:~$ sudo apt install vlan

Для того чтобы информация о созданных VLAN'ах сохранилась после перезагрузки, необходимо добавить её в файл /etc/network/interfaces. 

Например:
auto vlan1400
iface vlan1400 inet static
        address 192.168.1.1
        netmask 255.255.255.0
        vlan_raw_device eth0

4
LAG в Linux – бондинг,  имя интерфейса bond0, bond1.

vagrant@vagrant:~$ sudo apt install ifenslave

Modify the /etc/network/interfaces file:

auto bond0

iface bond0 inet static
    address 10.31.1.5
    netmask 255.255.255.0
    network 10.31.1.0
    gateway 10.31.1.254
    bond-slaves eth0 eth1
    bond-mode active-backup
    bond-miimon 100
    bond-downdelay 200
    bond-updelay 200

5
vagrant@vagrant:~$ ipcalc 10.10.10.0/29
Address:   10.10.10.0           00001010.00001010.00001010.00000 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.0/29        00001010.00001010.00001010.00000 000
HostMin:   10.10.10.1           00001010.00001010.00001010.00000 001
HostMax:   10.10.10.6           00001010.00001010.00001010.00000 110
Broadcast: 10.10.10.7           00001010.00001010.00001010.00000 111
Hosts/Net: 6                     Class A, Private Internet

6 адресов (не считая бродкаста)

255/8(первый адрес сети, последний бродкаста)=31 подсеть

vagrant@vagrant:~$ ipcalc --split 6 6 10.10.10.0/24
Address:   10.10.10.0           00001010.00001010.00001010. 00000000
Netmask:   255.255.255.0 = 24   11111111.11111111.11111111. 00000000
Wildcard:  0.0.0.255            00000000.00000000.00000000. 11111111
=>
Network:   10.10.10.0/24        00001010.00001010.00001010. 00000000
HostMin:   10.10.10.1           00001010.00001010.00001010. 00000001
HostMax:   10.10.10.254         00001010.00001010.00001010. 11111110
Broadcast: 10.10.10.255         00001010.00001010.00001010. 11111111
Hosts/Net: 254                   Class A, Private Internet

1. Requested size: 6 hosts
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Network:   10.10.10.0/29        00001010.00001010.00001010.00000 000
HostMin:   10.10.10.1           00001010.00001010.00001010.00000 001
HostMax:   10.10.10.6           00001010.00001010.00001010.00000 110
Broadcast: 10.10.10.7           00001010.00001010.00001010.00000 111
Hosts/Net: 6                     Class A, Private Internet

2. Requested size: 6 hosts
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Network:   10.10.10.8/29        00001010.00001010.00001010.00001 000
HostMin:   10.10.10.9           00001010.00001010.00001010.00001 001
HostMax:   10.10.10.14          00001010.00001010.00001010.00001 110
Broadcast: 10.10.10.15          00001010.00001010.00001010.00001 111
Hosts/Net: 6                     Class A, Private Internet

Needed size:  16 addresses.
Used network: 10.10.10.0/28
Unused:
10.10.10.16/28
10.10.10.32/27
10.10.10.64/26
10.10.10.128/25

6
vagrant@vagrant:~$ ipcalc 172.32.0.0/27
Address:   172.32.0.0           10101100.00100000.00000000.000 00000
Netmask:   255.255.255.224 = 27 11111111.11111111.11111111.111 00000
Wildcard:  0.0.0.31             00000000.00000000.00000000.000 11111
=>
Network:   172.32.0.0/27        10101100.00100000.00000000.000 00000
HostMin:   172.32.0.1           10101100.00100000.00000000.000 00001
HostMax:   172.32.0.30          10101100.00100000.00000000.000 11110
Broadcast: 172.32.0.31          10101100.00100000.00000000.000 11111
Hosts/Net: 30                    Class B

7
Проверить АРП Линукс
vagrant@vagrant:~$ arp -a
? (10.0.2.2) at 52:54:00:12:35:02 [ether] on eth0
? (10.0.2.3) at 52:54:00:12:35:03 [ether] on eth0

Виндоус
C:\Users\chebunin_daniil>arp -a

Очистить кэш
sudo ip neigh flush all

Удалить конкретный ip
sudo arp -d 192.168.100.25

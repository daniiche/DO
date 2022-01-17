```
1
route-views>show ip route 109.252.100.75
Routing entry for 109.252.0.0/16
  Known via "bgp 6447", distance 20, metric 0
  Tag 8283, type external
  Last update from 94.142.247.3 1d16h ago
  Routing Descriptor Blocks:
  * 94.142.247.3, from 94.142.247.3, 1d16h ago
      Route metric is 0, traffic share count is 1
      AS Hops 3
      Route tag 8283
      MPLS label: none
      
      
      
route-views>show bgp 109.252.100.75
BGP routing table entry for 109.252.0.0/16, version 1391417923
Paths: (24 available, best #13, table default)
  Not advertised to any peer
  Refresh Epoch 1
  6939 8359 25513
    64.71.137.241 from 64.71.137.241 (216.218.252.164)
      Origin IGP, localpref 100, valid, external
      path 7FE15B593A70 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 3
  3303 8359 25513
    217.192.89.50 from 217.192.89.50 (138.187.128.158)
      Origin IGP, localpref 100, valid, external
      Community: 0:151 3303:1004 3303:1006 3303:1030 3303:3054 8359:100 8359:5500 8359:55277
      path 7FE114A17770 RPKI State not found
      rx pathid: 0, tx pathid: 0


2
vagrant@vagrant:~$ sudo -i
root@vagrant:~# echo "dummy" >> /etc/modules
root@vagrant:~# echo "options dummy numdummies=2" > /etc/modprobe.d/dummy.conf
root@vagrant:~# vim /etc/network/interfaces

root@vagrant:~# head /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto dummy0
iface dummy0 inet static
    address 10.2.2.2/32
    address 10.2.2.3/32
    pre-up ip link add dummy0 type dummy
    post-down ip link del dummy0
    
    
root@vagrant:~# ip route show table all
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100
broadcast 10.0.2.0 dev eth0 table local proto kernel scope link src 10.0.2.15
local 10.0.2.15 dev eth0 table local proto kernel scope host src 10.0.2.15
broadcast 10.0.2.255 dev eth0 table local proto kernel scope link src 10.0.2.15
broadcast 127.0.0.0 dev lo table local proto kernel scope link src 127.0.0.1
local 127.0.0.0/8 dev lo table local proto kernel scope host src 127.0.0.1
local 127.0.0.1 dev lo table local proto kernel scope host src 127.0.0.1
broadcast 127.255.255.255 dev lo table local proto kernel scope link src 127.0.0.1
::1 dev lo proto kernel metric 256 pref medium
fe80::/64 dev eth0 proto kernel metric 256 pref medium
local ::1 dev lo table local proto kernel metric 0 pref medium
local fe80::a00:27ff:fe73:60cf dev eth0 table local proto kernel metric 0 pref medium
multicast ff00::/8 dev eth0 table local proto kernel metric 256 pref medium


3
vagrant@vagrant:~$ ss -t -a
State                  Recv-Q                  Send-Q                                   Local Address:Port                                     Peer Address:Port                  Process
LISTEN                 0                       4096                                           0.0.0.0:sunrpc                                        0.0.0.0:*
LISTEN                 0                       4096                                     127.0.0.53%lo:domain                                        0.0.0.0:*
LISTEN                 0                       128                                            0.0.0.0:ssh                                           0.0.0.0:*
ESTAB                  0                       0                                            10.0.2.15:ssh                                          10.0.2.2:49155
LISTEN                 0                       4096                                              [::]:sunrpc                                           [::]:*
LISTEN                 0                       128                                               [::]:ssh                                              [::]:*

веб сайты, публичные апи в json формате 

4
vagrant@vagrant:~$ ss -u -a
State                  Recv-Q                  Send-Q                                    Local Address:Port                                     Peer Address:Port                 Process
UNCONN                 0                       0                                         127.0.0.53%lo:domain                                        0.0.0.0:*
UNCONN                 0                       0                                        10.0.2.15%eth0:bootpc                                        0.0.0.0:*
UNCONN                 0                       0                                               0.0.0.0:sunrpc                                        0.0.0.0:*
UNCONN                 0                       0                                                  [::]:sunrpc                                           [::]:*

аудио связь, видео стримминг

5
```
![Alt text](https://raw.githubusercontent.com/daniiche/DO/main/12/1.JPG)

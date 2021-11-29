1
HTTP/1.1 301 Moved Permanently
Постоянный редирект на другой адрес


2
Status Code: 307 Internal Redirect

Request URL: https://stackoverflow.com/
Request Method: GET
Status Code: 200 
589ms

![Alt text](/DO/10/1.jpg?raw=true "Optional Title")

3
public
vagrant@vagrant:~$ curl ifconfig.me
109.252.100.75

4
whois 109.252.100.75
% This is the RIPE Database query service.
netname:        MGTS-PPPOE
descr:          Moscow Local Telephone Network (OAO MGTS)

5
vagrant@vagrant:~$ traceroute 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets

10.0.2.2
100.114.0.1
mpts-a197-51.msk.mts-internet.net
a197-cr04-be12.51.msk.mts-internet.net
a197-cr01-ae31.77.msk.mts-internet.net
mag9-cr02-be10.77.msk.mts-internet.net
mag9-cr01-be16.77.msk.mts-internet.net
108.170.250.99
142.251.49.24
74.125.253.94
74.125.253.147
dns.google

vagrant@vagrant:~$ traceroute -An 8.8.8.8
AS8359
AS15169

6
vagrant@vagrant:~$ mtr -zn 8.8.8.8

AS15169  8.8.8.8                                                              80.0%

ping avg 46ms

7
dns.google.		10800	IN	NS	ns4.zdns.google.
dns.google.		10800	IN	NS	ns3.zdns.google.
dns.google.		10800	IN	NS	ns2.zdns.google.
dns.google.		10800	IN	NS	ns1.zdns.google.

dns.google.		900	IN	A	8.8.4.4
dns.google.		900	IN	A	8.8.8.8

8
vagrant@vagrant:~$ dig -x 8.8.8.8

;; ANSWER SECTION:
8.8.8.8.in-addr.arpa.	5998	IN	PTR	dns.google.


10

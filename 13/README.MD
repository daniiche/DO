```
1
![Alt text](https://raw.githubusercontent.com/daniiche/DO/main/13/1.JPG)



2
![Alt text](https://raw.githubusercontent.com/daniiche/DO/main/13/2.JPG)



3
apt-get -y install nginx
    openssl genrsa 2048 > server.key
    openssl req -new -key server.key -subj "/C=JP/ST=Aichi/L=Nagoya/O=Personal/OU=Local Machine/CN=localhost" > server.csr
    openssl x509 -days 3650 -req -signkey server.key < server.csr > server.crt
    mv server.* /etc/nginx/conf.d/
    cat <<-CONF > /etc/nginx/conf.d/ssl.conf
server {
    listen       443  default ssl;
    ssl on;
    ssl_certificate     /etc/nginx/conf.d/server.crt;
    ssl_certificate_key /etc/nginx/conf.d/server.key;
    server_name  localhost;
}
CONF
    service nginx restart

![Alt text](https://raw.githubusercontent.com/daniiche/DO/main/13/3.JPG)

4
git clone --depth 1 https://github.com/drwetter/testssl.sh.git
cd testssl.sh
./testssl.sh -e --fast --parallel https://www.avito.ru

 Testing all 183 locally available ciphers against the server, ordered by encryption strength


Hexcode  Cipher Suite Name (OpenSSL)       KeyExch.   Encryption  Bits     Cipher Suite Name (IANA/RFC)
-----------------------------------------------------------------------------------------------------------------------------
 xc030   ECDHE-RSA-AES256-GCM-SHA384       ECDH 256   AESGCM      256      TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
 xc02f   ECDHE-RSA-AES128-GCM-SHA256       ECDH 256   AESGCM      128      TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
 xc027   ECDHE-RSA-AES128-SHA256           ECDH 256   AES         128      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
 xc013   ECDHE-RSA-AES128-SHA              ECDH 256   AES         128      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
 x9c     AES128-GCM-SHA256                 RSA        AESGCM      128      TLS_RSA_WITH_AES_128_GCM_SHA256
 x3c     AES128-SHA256                     RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA256
 x2f     AES128-SHA                        RSA        AES         128      TLS_RSA_WITH_AES_128_CBC_SHA
 x0a     DES-CBC3-SHA                      RSA        3DES        168      TLS_RSA_WITH_3DES_EDE_CBC_SHA


 Done 2021-12-09 17:21:42 [  14s] -->> 146.158.52.24:443 (www.avito.ru) <<--

--------------------------------------------------------------
Done testing now all IP addresses (on port 443): 146.158.54.24 146.158.48.24 146.158.52.24

5
ssh-keygen
Generating public/private rsa key pair.


sudo echo /root/.ssh/id_rsa >> ~/.ssh/authorized_keys
ssh root@localhost:2222
ssh -i ~/.ssh/mykey.key root@localhost:2222

6
cp ~/.ssh/mykey.key ~/.ssh/mykey2.key

mkdir -p ~/.ssh && chmod 700 ~/.sshtouch ~/.ssh/config && chmod 600 ~/.ssh/config
#---------------------------общая структура файла ~/.ssh/configHost hostname1    SSH_OPTION valueHost *    SSH_OPTION value#---------------------------Пример конфигаHost my_server  HostName localhost  IdentityFile ~/.ssh/mykey2.key  User root  Port 2222  #StrictHostKeyChecking noHost *    User default_username    IdentityFile ~/.ssh/id_rsa


7

root@vagrant-ubuntu-trusty-64:/home/vagrant# tcpdump -c 100 -w 0001.pcap -i eth0
tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
100 packets captured
116 packets received by filter
0 packets dropped by kernel

root@vagrant-ubuntu-trusty-64:/home/vagrant# tshark -r 0001.pcap
 1   0.000000    10.0.2.15 → 10.0.2.2     SSH 90 Server: Encrypted packet (len=36)
    2   0.000110    10.0.2.15 → 10.0.2.2     SSH 154 Server: Encrypted packet (len=100)
    3   0.000320     10.0.2.2 → 10.0.2.15    TCP 60 54272 → 22 [ACK] Seq=1 Ack=37 Win=65535 Len=0
    4   0.000327     10.0.2.2 → 10.0.2.15    TCP 60 54272 → 22 [ACK] Seq=1 Ack=137 Win=65535 Len=0
    5   0.000403    10.0.2.15 → 10.0.2.2     SSH 90 Server: Encrypted packet (len=36)
    6   0.000519     10.0.2.2 → 10.0.2.15    TCP 60 54272 → 22 [ACK] Seq=1 Ack=173 Win=65535 Len=0
    7  24.332388     10.0.2.2 → 10.0.2.15    TCP 60 55202 → 443 [SYN] Seq=0 Win=65535 Len=0 MSS=1460
    8  24.332432    10.0.2.15 → 10.0.2.2     TCP 58 443 → 55202 [SYN, ACK] Seq=0 Ack=1 Win=29200 Len=0 MSS=1460
    9  24.332583     10.0.2.2 → 10.0.2.15    TCP 60 55202 → 443 [ACK] Seq=1 Ack=1 Win=65535 Len=0
   10  24.332611     10.0.2.2 → 10.0.2.15    HTTP 747 GET / HTTP/1.1
   11  24.332618    10.0.2.15 → 10.0.2.2     TCP 54 443 → 55202 [ACK] Seq=1 Ack=694 Win=30492 Len=0
   12  24.337881    10.0.2.15 → 10.0.2.2     HTTP 895 HTTP/1.1 400 Bad Request  (text/html)



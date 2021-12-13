1 Создайте виртуальную машину Linux.

```console
vargant-ubuntu-test danche$ cat Vagrantfile
Vagrant.configure("2") do |config|
 config.vm.box = "bento/ubuntu-20.04"
end

vagrant up; vagrant ssh
```

2 Установите ufw и разрешите к этой машине сессии на порты 22 и 443, при этом трафик на интерфейсе localhost (lo) 
должен ходить свободно на все порты.

```console
sudo apt install ufw

sudo ufw allow 22
Rules updated
Rules updated (v6)

sudo ufw allow 443
Rules updated
Rules updated (v6)

sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)?
Aborted

sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup

sudo ufw status numbered
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 22                         ALLOW IN    Anywhere
[ 2] 443                        ALLOW IN    Anywhere
[ 3] 22 (v6)                    ALLOW IN    Anywhere (v6)
[ 4] 443 (v6)                   ALLOW IN    Anywhere (v6)

```

3 Установите hashicorp vault (инструкция по ссылке).

```console
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
OK

sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

sudo apt-get update && sudo apt-get install vault

vagrant@vagrant:~$ vault
Usage: vault <command> [args]
```

4 Cоздайте центр сертификации по инструкции (ссылка) и выпустите сертификат для использования его в настройке веб-сервера nginx 
(срок жизни сертификата - месяц).

```console

vagrant@vagrant:~$ sudo mkdir /etc/vault
vagrant@vagrant:~$ sudo mkdir -p  /var/lib/vault/data

cd /etc/vault; sudo touch config.hcl

sudo vim config.hcl

disable_cache = true
disable_mlock = true
ui = true
listener "tcp" {
   address          = "0.0.0.0:8200"
   tls_disable      = 1

}
storage "file" {
   path  = "/var/lib/vault/data"
 }
api_addr         = "http://0.0.0.0:8200"
max_lease_ttl         = "10h"
default_lease_ttl    = "10h"
cluster_name         = "vault"
raw_storage_endpoint     = true
disable_sealwrap     = true
disable_printable_check = true

sudo apt-get install -y systemd

sudo vim /etc/systemd/system/vault.service

[Unit]
Description=Vault service
Requires=network-online.target
After=network-online.target
ConditionFileNotEmpty=/etc/vault/config.hcl

[Service]
ProtectSystem=full
ProtectHome=read-only
PrivateTmp=yes
PrivateDevices=yes
SecureBits=keep-caps
AmbientCapabilities=CAP_IPC_LOCK
NoNewPrivileges=yes
ExecStart=/usr/bin/vault server -config=/etc/vault/config.hcl
ExecReload=/bin/kill --signal HUP
KillMode=process
KillSignal=SIGINT
Restart=on-failure
RestartSec=5
TimeoutStopSec=30
StartLimitBurst=3
LimitNOFILE=6553

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload

vagrant@vagrant:/etc/vault.d$ sudo systemctl daemon-reload

vagrant@vagrant:/etc/vault.d$ sudo systemctl start vault.service
vagrant@vagrant:/etc/vault.d$ sudo systemctl status vault
● vault.service - Vault service
     Loaded: loaded (/etc/systemd/system/vault.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-12-13 16:30:40 UTC; 2s ago
     

export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
```

```console
sudo apt-get install jq

vagrant@vagrant:/etc/vault$ vault server -dev -dev-root-token-id root &

vagrant@vagrant:/etc/vault$ vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.9.1
Storage Type    inmem
Cluster Name    vault-cluster-129ca91b
Cluster ID      31df59ce-a00a-b8af-8ae7-e6be5308b3a6
HA Enabled      false

vagrant@vagrant:/etc/vault$ export VAULT_ADDR=http://127.0.0.1:8200
vagrant@vagrant:/etc/vault$ export VAULT_TOKEN=root

vagrant@vagrant:~$ vim policy.hcl
vagrant@vagrant:~$ vault policy write default policy.hcl

added

# Enable secrets engine
path "sys/mounts/*" {
  capabilities = [ "create", "read", "update", "delete", "list" ]
}

# List enabled secrets engine
path "sys/mounts" {
  capabilities = [ "read", "list" ]
}

# Work with pki secrets engine
path "pki*" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}



to default

vagrant@vagrant:/etc/vault$ vault secrets enable pki
2021-12-13T17:05:09.022Z [INFO]  core: successful mount: namespace="\"\"" path=pki/ type=pki
Success! Enabled the pki secrets engine at: pki/

vagrant@vagrant:/etc/vault$ vault secrets tune -max-lease-ttl=87600h pki
2021-12-13T17:05:28.212Z [INFO]  core: mount tuning of leases successful: path=pki/
Success! Tuned the secrets engine at: pki/

vault write -field=certificate pki/root/generate/internal \
     common_name="example.com" \
     ttl=87600h > CA_cert.crt



vault write pki/config/urls \
     issuing_certificates="$VAULT_ADDR/v1/pki/ca" \
     crl_distribution_points="$VAULT_ADDR/v1/pki/crl"



vault secrets enable -path=pki_int pki

vault secrets tune -max-lease-ttl=43800h pki_int


vault write -format=json pki_int/intermediate/generate/internal \
     common_name="example.com Intermediate Authority" \
     | jq -r '.data.csr' > pki_intermediate.csr



vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr \
     format=pem_bundle ttl="43800h" \
     | jq -r '.data.certificate' > intermediate.cert.pem

vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem

vault write pki_int/roles/example-dot-com \
     allowed_domains="example.com" \
     allow_subdomains=true \
     max_ttl="720h"


vagrant@vagrant:~$ vault write pki_int/issue/example-dot-com common_name="test.example.com" ttl="720h"
```

5 Установите корневой сертификат созданного центра сертификации в доверенные в хостовой системе.

```console
vagrant@vagrant:~$ cd /etc/ssl
sudo vim root.crt
sudo vim root.key

sudo chmod 644 root.crt
sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
rehash: warning: skipping root.pem,it does not contain exactly one certificate or CRL
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.

```

6 Установите nginx.

```console
sudo apt-get -y install nginx

=curl localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

7 По инструкции (ссылка) настройте nginx на https, используя ранее подготовленный сертификат:
можно использовать стандартную стартовую страницу nginx для демонстрации работы сервера;
можно использовать и другой html файл, сделанный вами;

```console
=cd /etc/nginx

vagrant@vagrant:/etc/nginx$ sudo vim nginx.conf

```

8 Откройте в браузере на хосте https адрес страницы, которую обслуживает сервер nginx.

![alt text](https://github.com/daniiche/DO/blob/main/1diploma/1.JPG)

![alt text](https://github.com/daniiche/DO/blob/main/1diploma/2.JPG)

9 Создайте скрипт, который будет генерировать новый сертификат в vault:
генерируем новый сертификат так, чтобы не переписывать конфиг nginx;
перезапускаем nginx для применения нового сертификата.

10 Поместите скрипт в crontab, чтобы сертификат обновлялся какого-то числа каждого месяца в удобное для вас время.

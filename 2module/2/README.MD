# Задача 1

Опишите своими словами основные преимущества применения на практике IaaC паттернов.
Какой из принципов IaaC является основополагающим?

```
во-первых, использование IaaC паттернов ускоряют доставку ПО конечному потребителю, что важно для бизнеса. Также возможность легко масштабировать текущий функционал с настройками.
во-вторых, паттерн обеспечивает стабильность сред для разработки, тестирования, стейджинга и прода - везде будут обеспечена одинаковая конфигурация
в-третьих, использование IaaC ускоряют процессы развертывания, разработки, тестирования. Дают возможность взаимодействовать с параметрами среды как с кодом

Но самое главное преимущество, это Идемпотентность. Это позволяет разворачивать среды бесчисленное число раз добиваясь при этом одинаковых результатов(одинаковых свойств).
```

# Задача 2

Чем Ansible выгодно отличается от других систем управление конфигурациями?
Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

```
активно разрабатывается, используется метод ПУШ и использует удобный пайтон и YAML.
А также использует существующую ССШ инфраструктуру, без необходимости доп. установок.

если мы расчитываем, что хост более надежный сервер и мы за его состоянием более пристально следим - то смею предположить, что 
метод ПУШ будет более надежным - сможет перезапустить/сконфигурировать машину по нашему требованию
```

# Задача 3

Установить на личный компьютер:

VirtualBox
Vagrant
Ansible
Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.

```console

virtualbox from https://www.virtualbox.org/wiki/Downloads

brew install vagrant

192:~ pomac$ pip3 install ansible
Collecting ansible
  Downloading ansible-4.10.0.tar.gz (36.8 MB)
     |████████████████████████████████| 36.8 MB 9.4 MB/s            
  Preparing metadata (setup.py) ... done
Collecting ansible-core~=2.11.7
  Downloading ansible-core-2.11.7.tar.gz (7.1 MB)
     |████████████████████████████████| 7.1 MB 4.9 MB/s            
  Preparing metadata (setup.py) ... done
Collecting jinja2
  Downloading Jinja2-3.0.3-py3-none-any.whl (133 kB)
     |████████████████████████████████| 133 kB 6.5 MB/s            
Collecting PyYAML
  Downloading PyYAML-6.0-cp37-cp37m-macosx_10_9_x86_64.whl (189 kB)
     |████████████████████████████████| 189 kB 6.6 MB/s            
Collecting cryptography
  Downloading cryptography-36.0.1-cp36-abi3-macosx_10_10_x86_64.whl (2.6 MB)
     |████████████████████████████████| 2.6 MB 8.7 MB/s            
Collecting packaging
  Downloading packaging-21.3-py3-none-any.whl (40 kB)
     |████████████████████████████████| 40 kB 5.0 MB/s            
Collecting resolvelib<0.6.0,>=0.5.3
  Downloading resolvelib-0.5.4-py2.py3-none-any.whl (12 kB)
Collecting cffi>=1.12
  Downloading cffi-1.15.0-cp37-cp37m-macosx_10_9_x86_64.whl (178 kB)
     |████████████████████████████████| 178 kB 6.9 MB/s            
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.0.1-cp37-cp37m-macosx_10_9_x86_64.whl (13 kB)
Collecting pyparsing!=3.0.5,>=2.0.2
  Downloading pyparsing-3.0.7-py3-none-any.whl (98 kB)
     |████████████████████████████████| 98 kB 4.0 MB/s             
Collecting pycparser
  Downloading pycparser-2.21-py2.py3-none-any.whl (118 kB)
     |████████████████████████████████| 118 kB 8.4 MB/s            
Using legacy 'setup.py install' for ansible, since package 'wheel' is not installed.
Using legacy 'setup.py install' for ansible-core, since package 'wheel' is not installed.
Installing collected packages: pycparser, pyparsing, MarkupSafe, cffi, resolvelib, PyYAML, packaging, jinja2, cryptography, ansible-core, ansible
    Running setup.py install for ansible-core ... done
    Running setup.py install for ansible ... done
Successfully installed MarkupSafe-2.0.1 PyYAML-6.0 ansible-4.10.0 ansible-core-2.11.7 cffi-1.15.0 cryptography-36.0.1 jinja2-3.0.3 packaging-21.3 pycparser-2.21 pyparsing-3.0.7 resolvelib-0.5.4
```

# Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

Создать виртуальную машину.
Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды

```
[nodes:children]
manager

[manager]
server1.netology ansible_host=127.0.0.1 ansible_port=20011 ansible_user=vagrant
```

```
---

  - hosts: nodes
    become: yes
    become_user: root
    remote_user: vagrant

    tasks:
      - name: Create directory for ssh-keys
        file: state=directory mode=0700 dest=/root/.ssh/

      - name: Adding rsa-key in /root/.ssh/authorized_keys
        copy: src=~/.ssh/id_rsa.pub dest=/root/.ssh/authorized_keys owner=root mode=0600
        ignore_errors: yes

      - name: Checking DNS
        command: host -t A google.com

      - name: Installing tools
        apt: >
          package={{ item }}
          state=present
          update_cache=yes
        with_items:
          - git
          - curl

      - name: Installing docker
        shell: curl -fsSL get.docker.com -o get-docker.sh && chmod +x get-docker.sh && ./get-docker.sh

      - name: Add the current user to docker group
        user: name=vagrant append=yes groups=docker
```

```
# -*- mode: ruby -*-

ISO = "bento/ubuntu-20.04"
NET = "192.168.56."
DOMAIN = ".netology"
HOST_PREFIX = "server"
INVENTORY_PATH = "../ansible/inventory"

servers = [
  {
    :hostname => HOST_PREFIX + "1" + DOMAIN,
    :ip => NET + "11",
    :ssh_host => "20011",
    :ssh_vm => "22",
    :ram => 1024,
    :core => 1
  }
]

Vagrant.configure(2) do |config|
  config.vm.synced_folder ".", "/vagrant", disabled: false
  servers.each do |machine|
    config.vm.define machine[:hostname] do |node|
      node.vm.box = ISO
      node.vm.hostname = machine[:hostname]
      node.vm.network "private_network", ip: machine[:ip]
      node.vm.network :forwarded_port, guest: machine[:ssh_vm], host: machine[:ssh_host]
      node.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--memory", machine[:ram]]
        vb.customize ["modifyvm", :id, "--cpus", machine[:core]]
        vb.name = machine[:hostname]
      end
      node.vm.provision "ansible" do |setup|
        setup.inventory_path = INVENTORY_PATH
        setup.playbook = "../ansible/provision.yml"
        setup.become = true
        setup.extra_vars = { ansible_user: 'vagrant' }
      end
    end
  end
end
```

```
[defaults]
inventory=./inventory
deprecation_warnings=False
command_warnings=False
ansible_port=22
interpreter_python=/usr/bin/python3
```

```console
polyas-mbp:vagrant pomac$ vagrant global-status --prune
id       name   provider state  directory                           
--------------------------------------------------------------------
There are no active Vagrant environments on this computer! Or,
you haven't destroyed and recreated Vagrant environments that were
started with an older version of Vagrant.

polyas-mbp:vagrant pomac$ vagrant up
Bringing machine 'server1.netology' up with 'virtualbox' provider...
==> server1.netology: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> server1.netology: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> server1.netology: flag to force provisioning. Provisioners marked to run always will still run.
polyas-mbp:vagrant pomac$ vagrant destroy
    server1.netology: Are you sure you want to destroy the 'server1.netology' VM? [y/N] y
==> server1.netology: Forcing shutdown of VM...
==> server1.netology: Destroying VM and associated drives...
polyas-mbp:vagrant pomac$ vagrant up
Bringing machine 'server1.netology' up with 'virtualbox' provider...
==> server1.netology: Importing base box 'bento/ubuntu-20.04'...
==> server1.netology: Matching MAC address for NAT networking...
==> server1.netology: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> server1.netology: Setting the name of the VM: server1.netology
==> server1.netology: Clearing any previously set network interfaces...
==> server1.netology: Preparing network interfaces based on configuration...
    server1.netology: Adapter 1: nat
    server1.netology: Adapter 2: hostonly
==> server1.netology: Forwarding ports...
    server1.netology: 22 (guest) => 20011 (host) (adapter 1)
    server1.netology: 22 (guest) => 2222 (host) (adapter 1)
==> server1.netology: Running 'pre-boot' VM customizations...
==> server1.netology: Booting VM...
==> server1.netology: Waiting for machine to boot. This may take a few minutes...
    server1.netology: SSH address: 127.0.0.1:2222
    server1.netology: SSH username: vagrant
    server1.netology: SSH auth method: private key
    server1.netology: 
    server1.netology: Vagrant insecure key detected. Vagrant will automatically replace
    server1.netology: this with a newly generated keypair for better security.
    server1.netology: 
    server1.netology: Inserting generated public key within guest...
    server1.netology: Removing insecure key from the guest if it's present...
    server1.netology: Key inserted! Disconnecting and reconnecting using new SSH key...
==> server1.netology: Machine booted and ready!
==> server1.netology: Checking for guest additions in VM...
==> server1.netology: Setting hostname...
==> server1.netology: Configuring and enabling network interfaces...
==> server1.netology: Mounting shared folders...
    server1.netology: /vagrant => /Users/pomac/vagrant
==> server1.netology: Running provisioner: ansible...
    server1.netology: Running ansible-playbook...

PLAY [nodes] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1.netology]

TASK [Create directory for ssh-keys] *******************************************
ok: [server1.netology]

TASK [Adding rsa-key in /root/.ssh/authorized_keys] ****************************
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: If you are using a module and expect the file to exist on the remote, see the remote_src option
fatal: [server1.netology]: FAILED! => {"changed": false, "msg": "Could not find or access '~/.ssh/id_rsa.pub' on the Ansible Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"}
...ignoring

TASK [Checking DNS] ************************************************************
changed: [server1.netology]

TASK [Installing tools] ********************************************************
ok: [server1.netology] => (item=git)
ok: [server1.netology] => (item=curl)

TASK [Installing docker] *******************************************************
changed: [server1.netology]

TASK [Add the current user to docker group] ************************************
changed: [server1.netology]

PLAY RECAP *********************************************************************
server1.netology           : ok=7    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=1   

polyas-mbp:vagrant pomac$ vagrant ssh
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 System information disabled due to load higher than 1.0


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Thu Jan 27 17:31:44 2022 from 10.0.2.2
vagrant@server1:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

1

sudo vim /etc/systemd/system/node_exporter.service

[Unit]
Description=Node Exporter service
After=multi-user.target

[Service]
EnvironmentFile=/etc/default/node_exporter.conf
ExecStart=/home/vagrant/node_exporter-1.3.0.linux-amd64/node_exporter $EXTRA_OPTS
Restart=always

[Install]
WantedBy=multi-user.target

echo '#comment' > /etc/default/node_exporter.conf

sudo systemctl daemon-reload
sudo systemctl enable node_exporter.service
sudo systemctl start node_exporter.service

vagrant@vagrant:/etc/default$ sudo systemctl status node_exporter
● node_exporter.service - Node Exporter service
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: en>
     Active: active (running) since Mon 2021-11-22 16:14:41 UTC; 9s ago
   Main PID: 3233 (node_exporter)
      Tasks: 4 (limit: 1071)
     Memory: 2.5M
     CGroup: /system.slice/node_exporter.service
             └─3233 /home/vagrant/node_exporter-1.3.0.linux-amd64/node_exporter

Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.592Z caller=node_expor>
Nov 22 16:14:41 vagrant node_exporter[3233]: ts=2021-11-22T16:14:41.595Z caller=tls_config>

2
curl localhost:9100/metrics

./node_exporter --help
--collector.cpu.info
--collector.meminfo
--collector.diskstats
--collector.netstat

3
System Overview
Overview of the key system metrics.

4
можно

vagrant@vagrant:~$ dmesg | grep virtual
[    0.003288] CPU MTRRs all blank - virtualized system.
[    0.156125] Booting paravirtualized kernel on KVM
[    2.688367] systemd[1]: Detected virtualization oracle.

5
fs.nr_open = 1048576

file: /proc/sys/fs/nr_open 
variable: fs.nr_open

This denotes the maximum number of file-handles a process can allocate. Default value is 1024*1024 (1048576) which should be enough for most machines. 

The value of "Max open files"(ulimit -n) is limited to fs.nr_open value.
which is 1024

6
sudo screen
sudo unshare -f --pid --mount-proc /bin/bash
sudo ps aux
nsenter --target 1 --pid --mount

root@vagrant:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.3   9836  3880 pts/1    S    16:38   0:00 /bin/bash
root           9  0.0  0.0   8076   592 pts/1    T    16:39   0:00 sleep 1h
root          11  0.0  0.4   9836  4120 pts/1    S    16:39   0:00 -bash
root          20  0.0  0.0   8996   696 pts/1    S    16:40   0:00 nsenter --target 1 --pid --mount
root          21  0.0  0.4   9836  4136 pts/1    S    16:40   0:00 -bash
root          30  0.0  0.3  11492  3328 pts/1    R+   16:40   0:00 ps aux

7
"exponentially spawns subprocesses until your box locks up"

Вы можете предотвратить такие атаки, используя ulimit для ограничения количества processes-per-user:

$ ulimit -u 50
$ :(){ :|:& };:
-bash: fork: Resource temporarily unavailable

cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-3.scope

Тут я так понял сработало ограничение
cat /sys/fs/cgroup/pids/user.slice/user-1000.slice/pids.max

1 Узнайте о sparse (разряженных) файлах.
vagrant@vagrant:~$ cp --sparse=always ./file ./sparse-file

2 Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?
vagrant@vagrant:~$ ln file linkfile

vagrant@vagrant:~$ ls -li
total 8852
131084 -rw-rw-r-- 2 vagrant vagrant      11 Nov 24 16:00 file
131088 -rw-rw-r-- 1 vagrant vagrant      54 Nov 14 18:47 file_out.text
131084 -rw-rw-r-- 2 vagrant vagrant      11 Nov 24 16:00 linkfile
131086 -rw-rw-r-- 1 vagrant vagrant       8 Nov 14 18:02 moby.txt
131095 drwxr-xr-x 2 vagrant vagrant    4096 Nov 22 15:20 node_exporter-1.3.0.linux-amd64
131093 -rw-rw-r-- 1 vagrant vagrant 9030402 Nov 18 16:41 node_exporter-1.3.0.linux-amd64.tar.gz
131089 -rw-rw-r-- 1 vagrant vagrant      54 Nov 14 18:47 out.txt
131105 -rw-rw-r-- 1 vagrant vagrant      11 Nov 24 16:01 sparse-file
131087 -rw-rw-r-- 1 vagrant vagrant       8 Nov 14 18:20 test.txt

vagrant@vagrant:~$ man chmod

vagrant@vagrant:~$ chmod u+x linkfile

vagrant@vagrant:~$ ls -li
total 8852
131084 -rwxrw-r-- 2 vagrant vagrant      11 Nov 24 16:00 file
131088 -rw-rw-r-- 1 vagrant vagrant      54 Nov 14 18:47 file_out.text
131084 -rwxrw-r-- 2 vagrant vagrant      11 Nov 24 16:00 linkfile
131086 -rw-rw-r-- 1 vagrant vagrant       8 Nov 14 18:02 moby.txt
131095 drwxr-xr-x 2 vagrant vagrant    4096 Nov 22 15:20 node_exporter-1.3.0.linux-amd64
131093 -rw-rw-r-- 1 vagrant vagrant 9030402 Nov 18 16:41 node_exporter-1.3.0.linux-amd64.tar.gz
131089 -rw-rw-r-- 1 vagrant vagrant      54 Nov 14 18:47 out.txt
131105 -rw-rw-r-- 1 vagrant vagrant      11 Nov 24 16:01 sparse-file
131087 -rw-rw-r-- 1 vagrant vagrant       8 Nov 14 18:20 test.txt

нет, права меняются у обоих файлов для одной inode. На ее уровне и устанавливаются права

3 Сделайте vagrant destroy на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:
Danobook:vargant-ubuntu-test danche$ vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...

vagrant@vagrant:~$ lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part
└─sda5                 8:5    0 63.5G  0 part
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk
sdc                    8:32   0  2.5G  0 disk

4 Используя fdisk, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.
vagrant@vagrant:~$ sudo fdisk -l /dev/sdb
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

Welcome to fdisk (util-linux 2.34).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x855a4565.

Command (m for help): p
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x855a4565

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5220351 1024000  500M 83 Linux


5 Используя sfdisk, перенесите данную таблицу разделов на второй диск.
vagrant@vagrant:~$ sudo sfdisk -d /dev/sdb | sudo sfdisk /dev/sdc
Checking that no-one is using this disk right now ... OK

Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x855a4565

Old situation:

Device     Boot   Start     End Sectors Size Id Type
/dev/sdc1          2048 2099199 2097152   1G 83 Linux
/dev/sdc2       2099200 4196351 2097152   1G 83 Linux

>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Created a new DOS disklabel with disk identifier 0x855a4565.
/dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
/dev/sdc2: Created a new partition 2 of type 'Linux' and of size 501 MiB.
/dev/sdc3: Done.

New situation:
Disklabel type: dos
Disk identifier: 0x855a4565

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5222399 1026048  501M 83 Linux

The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

vagrant@vagrant:~$ lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part
└─sda5                 8:5    0 63.5G  0 part
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk
├─sdb1                 8:17   0    2G  0 part
└─sdb2                 8:18   0  501M  0 part
sdc                    8:32   0  2.5G  0 disk
├─sdc1                 8:33   0    2G  0 part
└─sdc2                 8:34   0  501M  0 part

6 Соберите mdadm RAID1 на паре разделов 2 Гб.
vagrant@vagrant:~$ sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
mdadm: size set to 2094080K
Continue creating array? y
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
vagrant@vagrant:~$ lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part
└─sda5                 8:5    0 63.5G  0 part
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk
├─sdb1                 8:17   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdb2                 8:18   0  501M  0 part
sdc                    8:32   0  2.5G  0 disk
├─sdc1                 8:33   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdc2                 8:34   0  501M  0 part
vagrant@vagrant:~$


7 Соберите mdadm RAID0 на второй паре маленьких разделов.
vagrant@vagrant:~$ sudo mdadm --create --verbose /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2
mdadm: chunk size defaults to 512K
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md1 started.
vagrant@vagrant:~$ lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part
└─sda5                 8:5    0 63.5G  0 part
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk
├─sdb1                 8:17   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdb2                 8:18   0  501M  0 part
  └─md1                9:1    0  998M  0 raid0
sdc                    8:32   0  2.5G  0 disk
├─sdc1                 8:33   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdc2                 8:34   0  501M  0 part
  └─md1                9:1    0  998M  0 raid0
vagrant@vagrant:~$

8 Создайте 2 независимых PV на получившихся md-устройствах.
vagrant@vagrant:~$ sudo pvs
  PV         VG        Fmt  Attr PSize   PFree
  /dev/sda5  vgvagrant lvm2 a--  <63.50g    0

vagrant@vagrant:~$ sudo pvcreate /dev/md0 /dev/md1
  Physical volume "/dev/md0" successfully created.
  Physical volume "/dev/md1" successfully created.
vagrant@vagrant:~$ sudo pvs
  PV         VG        Fmt  Attr PSize   PFree
  /dev/md0             lvm2 ---   <2.00g  <2.00g
  /dev/md1             lvm2 ---  998.00m 998.00m
  /dev/sda5  vgvagrant lvm2 a--  <63.50g      0
  
9 Создайте общую volume-group на этих двух PV.
vagrant@vagrant:~$ sudo vgs
  VG        #PV #LV #SN Attr   VSize   VFree
  vgvagrant   1   2   0 wz--n- <63.50g    0
vagrant@vagrant:~$ sudo vgcreate vg1 /dev/md0 /dev/md1
  Volume group "vg1" successfully created
vagrant@vagrant:~$ sudo vgs
  VG        #PV #LV #SN Attr   VSize   VFree
  vg1         2   0   0 wz--n-  <2.97g <2.97g
  vgvagrant   1   2   0 wz--n- <63.50g     0

10 Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.
vagrant@vagrant:~$ sudo lvs
  LV     VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  root   vgvagrant -wi-ao---- <62.54g
  swap_1 vgvagrant -wi-ao---- 980.00m
vagrant@vagrant:~$ sudo lvcreate -L 100M -nlv1 vg1 /dev/md1
  Logical volume "lv1" created.
vagrant@vagrant:~$ sudo lvs
  LV     VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  lv1    vg1       -wi-a----- 100.00m
  root   vgvagrant -wi-ao---- <62.54g
  swap_1 vgvagrant -wi-ao---- 980.00m
  
vagrant@vagrant:~$ lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part
└─sda5                 8:5    0 63.5G  0 part
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk
├─sdb1                 8:17   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdb2                 8:18   0  501M  0 part
  └─md1                9:1    0  998M  0 raid0
    └─vg1-lv1        253:2    0  100M  0 lvm
sdc                    8:32   0  2.5G  0 disk
├─sdc1                 8:33   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdc2                 8:34   0  501M  0 part
  └─md1                9:1    0  998M  0 raid0
    └─vg1-lv1        253:2    0  100M  0 lvm

11 Создайте mkfs.ext4 ФС на получившемся LV.
vagrant@vagrant:~$ sudo mkfs.ext4 /dev/vg1/lv1
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done
Writing inode tables: done
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done

vagrant@vagrant:~$ sudo file -L -s /dev/vg1/lv1
/dev/vg1/lv1: Linux rev 1.0 ext4 filesystem data, UUID=dd77db38-15cb-4519-8e5b-cc12fa598c49 (extents) (64bit) (large files) (huge files)

12 Смонтируйте этот раздел в любую директорию, например, /tmp/new.
vagrant@vagrant:~$ mkdir /tmp/new
vagrant@vagrant:~$ sudo mount /dev/vg1/lv1 /tmp/new

vagrant@vagrant:~$ lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part
└─sda5                 8:5    0 63.5G  0 part
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk
├─sdb1                 8:17   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdb2                 8:18   0  501M  0 part
  └─md1                9:1    0  998M  0 raid0
    └─vg1-lv1        253:2    0  100M  0 lvm   /tmp/new
sdc                    8:32   0  2.5G  0 disk
├─sdc1                 8:33   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdc2                 8:34   0  501M  0 part
  └─md1                9:1    0  998M  0 raid0
    └─vg1-lv1        253:2    0  100M  0 lvm   /tmp/new

13 Поместите туда тестовый файл, например wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz.
vagrant@vagrant:~$ sudo wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
--2021-11-24 20:06:44--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22565143 (22M) [application/octet-stream]
Saving to: ‘/tmp/new/test.gz’

/tmp/new/test.gz           100%[========================================>]  21.52M  41.2MB/s    in 0.5s

2021-11-24 20:06:44 (41.2 MB/s) - ‘/tmp/new/test.gz’ saved [22565143/22565143]



14 Прикрепите вывод lsblk.
vagrant@vagrant:~$ lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part
└─sda5                 8:5    0 63.5G  0 part
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk
├─sdb1                 8:17   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdb2                 8:18   0  501M  0 part
  └─md1                9:1    0  998M  0 raid0
    └─vg1-lv1        253:2    0  100M  0 lvm   /tmp/new
sdc                    8:32   0  2.5G  0 disk
├─sdc1                 8:33   0    2G  0 part
│ └─md0                9:0    0    2G  0 raid1
└─sdc2                 8:34   0  501M  0 part
  └─md1                9:1    0  998M  0 raid0
    └─vg1-lv1        253:2    0  100M  0 lvm   /tmp/new
vagrant@vagrant:~$ ls /tmp/new
lost+found  test.gz

15 Протестируйте целостность файла:
vagrant@vagrant:/tmp/new$ gzip -t /tmp/new/test.gz
vagrant@vagrant:/tmp/new$ echo $?
0

16 Используя pvmove, переместите содержимое PV с RAID0 на RAID1.
vagrant@vagrant:/tmp/new$ sudo pvmove /dev/md1 /dev/md0
  /dev/md1: Moved: 28.00%
  /dev/md1: Moved: 100.00%

17 Сделайте --fail на устройство в вашем RAID1 md.
vagrant@vagrant:/tmp/new$ sudo mdadm --fail /dev/md0 /dev/sdb1
mdadm: set /dev/sdb1 faulty in /dev/md0

18 Подтвердите выводом dmesg, что RAID1 работает в деградированном состоянии.
[13186.844748] md/raid1:md0: Disk failure on sdb1, disabling device.
               md/raid1:md0: Operation continuing on 1 devices.

19 Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:
vagrant@vagrant:/tmp/new$ gzip -t /tmp/new/test.gz
vagrant@vagrant:/tmp/new$ echo $?
0

20 Погасите тестовый хост, vagrant destroy.

1
strace /bin/bash -c 'cd /tmp' 2>&1^C

chdir("/tmp")

2
strace file /dev/tty 2>&1
openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3

man magic
The database of these “magic patterns” is usually located in a
     binary file in /usr/share/misc/magic.mgc or a directory of source text magic pattern fragment files in /usr/share/misc/magic.  The database specifies
     what patterns are to be tested for, what message or MIME type to print if a particular pattern is found, and additional information to extract from the
     file.

so magic according to strace goes to
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3

3
можно взять вывод команды по дескриптору и перенаправить в dev/null, тогда он будет удалятьсяб а не занимать место

Upd 

touch log.txt

exec 6> log.txt

logcommand 2>&6

exec 6> /dev/null

Or

command > /dev/null 2>&1


4
All the memory and resources allocated to a process are deallocated when the process terminates using the exit() system call. But the process’s entry in the process table is still available. This process is now a zombie process.

This may not be a serious problem if there are a few zombie processes but under heavier loads, this can create issues for the system such as running out of process table entries.

So the only redource it uses is a process table entry

5
sudo strace opensnoop-bpfcc

openat(AT_FDCWD, "/sys/devices/system/cpu/online", O_RDONLY|O_CLOEXEC) = 10
openat(AT_FDCWD, "/proc/self/status", O_RDONLY) = 10

файлы в proc

6
Какой системный вызов использует uname -a?
uname({sysname="Linux", nodename="vagrant", ...}) = 0
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0x1), ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0

makedev?

из proc версию можно узнать
 /proc/sys/kernel/ostype and /proc/sys/kernel/osrelease
              These files give substrings of /proc/version.


7
Чем отличается последовательность команд через ; и через && в bash?
&& выполняет команды последовательно, если у предыдущего код выполнения 0, то команда не выполнится
а ; выполнит вторую даже если код не 0

vagrant@vagrant:~$ cd /tmp/somedir 2>&1
-bash: cd: /tmp/somedir: No such file or directory

без set -e не выполнится
vagrant@vagrant:~$ cd /tmp/somedir && echo 1
-bash: cd: /tmp/somedir: No such file or directory

8
set -euxo
is setting e u x o pipefail flags

With these settings, certain common errors will cause the script to immediately fail, explicitly and loudly. Otherwise, you can get hidden bugs that are discovered only when they blow up in production.

e-to hidden catch runtime errors
x-to print all commands to terminal
u-exits if unnamen variable
o pipefail-If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline


с set -e выполнится
vagrant@vagrant:~$ set -e cd /tmp/somedir && echo 1
1

9
The most popular is S
which is interruptible sleep (waiting for an event to complete)

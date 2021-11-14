1
Какого типа команда cd? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.

Команда может быть внутренней баша или лежать в отдельном файле в виде исполняемого скрипта

В данном случаее 
type cd
выдает
cd is a shell builtin

так как это ключевая комманда для работы с файловой системой

2
Какая альтернатива без pipe команде grep <some_string> <some_file> | wc -l?
grep <some_string> <some_file> -c
позволяет это сделать в одну команду

3
сначала думал, что login Он же запрашивается до старта shell
Ноо ооказывается, что systemd(1) - инициализация системы и сервисов

4
sudo ls . 2> /dev/pts/0
где 
. - текущая директория
2 - код, означающий ошибку
> - символ перенаправления вывода
/dev/pts/1 - название новой сессии терминала

5
Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.
Получится через пайп
echo 'foo bar' | grep foo > test.txt

6
Получится ли находясь в графическом режиме, вывести данные из PTY в какой-либо из эмуляторов TTY? 
Сможете ли вы наблюдать выводимые данные?
sudo echo hi >/dev/tty3
Получится, но видно не будет. У другого пользователя, если рядом открыт терминал появится.


7
Выполните команду bash 5>&1. 
К чему она приведет? 
Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит?

bash 5>&1 
- создает дескриптор 5 и перенаправляет его в stdout
Потому что мы передали stdout 'netology' в 5 дискриптор, который сами же и создали

vagrant@vagrant:~$ ls -l /proc/$$/fd/5
lrwx------ 1 vagrant vagrant 64 Nov 14 18:36 /proc/1283/fd/5 -> /dev/pts/0

8
Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty?
vagrant@vagrant:~$ ls nofile 2>&1 >/proc/$$/fd/5 | cat>out.txt
vagrant@vagrant:~$ cat out.txt
ls: cannot access 'nofile': No such file or directory

9
Что выведет команда cat /proc/$$/environ? Как еще можно получить аналогичный по содержанию вывод?

Выведет содержимое файла окружения для текущей сессии
Можно запросить просто через env

10
Используя man, опишите что доступно по адресам /proc/<PID>/cmdline, /proc/<PID>/exe.
ls /proc/$$/cmdline
man proc

/cmdline
line 280
Содержит всю командную строку процесса, в нем находятся аргументы, если предоставлены

/exe 
line 344
Этот файл - ссылка на путь исполняемой команды

11
Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью /proc/cpuinfo.
grep sse /proc/cpuinfo
4.2

12
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
vagrant@localhost's password:
not a tty

ssh localhost -t 'tty'
vagrant@localhost's password:
/dev/pts/2
Connection to localhost closed.

Yeah this is a known "thing." It is not really a problem because it doesn't really cause a problem. Actually, the reason this error message even appears is due to a bug in Ubuntu not checking whether stdin is a TTY, and just assuming it is.

13
sudo apt-get install reptyr
в одном терминале screen
в другом терминалеsudo reptyr -T 1295

14
There's no difference in the sense that the data in the file will be the same if echo and tee are executed successfully and if the file is writable by the current user. 
The tee command would additionally produce output on its standard output, showing the text that would also be appended to the file

То есть tee не может записать в файл, но может вывести в stdout

5)
Ознакомьтесь с графическим интерфейсом VirtualBox, посмотрите как выглядит виртуальная машина, которую создал для вас Vagrant, какие аппаратные ресурсы ей выделены. Какие ресурсы выделены по-умолчанию?
-Ubuntu 64 bit
-base memory 1024mb
-2 processors
-4mb video memory
-rdp port 5996
-1 shared folder

6)
Как добавить оперативной памяти или ресурсов процессора виртуальной машине?
config.vm.provider "virtualbox" do |v|
  v.memory = 2048
  v.cpus = 4
end

8)
-Какой переменной можно задать длину журнала history, и на какой строчке manual это описывается?
The value of HISTSIZE variable is used as the number of commands to save in a history list.
line 3534

-что делает директива ignoreboth в bash?
A value of ignoreboth is shorthand for ignorespace and ignoredups.

9)
В каких сценариях использования применимы скобки {} и на какой строчке man bash это описано?
to execute group of commands in current shell environment
line 266

also

Any  element of an array may be referenced using ${name[subscript]}.  The braces are
       required to avoid conflicts with pathname expansion.
line 1222

10)
С учётом ответа на предыдущий вопрос, как создать однократным вызовом touch 100000 файлов? Получится ли аналогичным образом создать 300000? Если нет, то почему?
sudo touch {0..100000} 
does not let create 100000 files


The default amount of space available for the stack is something like 8192 KB. 
You can see the amount of space available, as follows:
$ ulimit -s
8192

as soon as it cant be changed up when set to 8192, it is only possible to create between 10000 and 20000 files at once

or it can be scripted

for i in {0..300000};do sudo touch $i; done

11)
Что делает конструкция [[ -d /tmp ]]
Return a status of 0 or 1 depending on the evaluation of the conditional expression
-d file
              True if file exists and is a directory.

Here, if there is a directory /tmp the returns true.

To test in bash
[[ -d /tmp ]] && echo 1

12)
Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах, которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке:

sudo mkdir -p /tmp/new_path_directory
sudo cp -r  /usr/bin/bash /tmp/new_path_directory/bash
PATH=/tmp/new_path_directory:$PATH

Output:
vagrant@vagrant:/tmp$ type -a bash
bash is /tmp/new_path_directory/bash
bash is /usr/bin/bash
bash is /bin/bash

13)
Чем отличается планирование команд с помощью batch и at?

at  and  batch  read commands from standard input or a specified file which are to be exe‐
       cuted at a later time, using /bin/sh.

at      executes commands at a specified time.

batch   executes commands when system load levels permit; in other words,  when  the  load
               average drops below 1.5, or the value specified in the invocation of atd.
14)
vagrant halt

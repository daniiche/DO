# Задача 1

Сценарий выполения задачи:

создайте свой репозиторий на https://hub.docker.com;
выберете любой образ, который содержит веб-сервер Nginx;
создайте свой fork образа;
реализуйте функциональность: запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.


```console
docker pull nginx
mkdir nginx_docker
root@test-02:~/nginx_docker# echo 'FROM nginx' > ./site-nginx_docker/Dockerfile
root@test-02:~/nginx_docker# docker build -t daniiche/nginx:1.0 .
root@test-02:~/nginx_docker# mkdir site-content
root@test-02:~/nginx_docker# echo '<html><head>Hey, Netology</head><body><h1>I’m DevOps Engineer!</h1></body></html>' > ./site-content/index.html
root@test-02:~/nginx_docker/site-content# docker run -it --rm -d -p 8080:80 --name web -v ~/nginx_docker/site-content:/usr/share/nginx/html daniiche/nginx:1.0
340ee67c54d10ca28911d04e9735ad8b3032077a96b104006c518dae6cf5d87d
root@test-02:~/nginx_docker/site-content# curl localhost:8080/index.html
<html><head>Hey, Netology</head><body><h1>I’m DevOps Engineer!</h1></body></html>
```

# Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос: "Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

1 Высоконагруженное монолитное java веб-приложение;
2 Nodejs веб-приложение;
3 Мобильное приложение c версиями для Android и iOS;
4 Шина данных на базе Apache Kafka;
5 Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
6 Мониторинг-стек на базе Prometheus и Grafana;
7 MongoDB, как основное хранилище данных для java-приложения;
8 Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.


```
1 для высоконагруженного приложения вероятно контейниризация будет лишним оверхедом, особенно веб. Монолит тут как раз указывает на то, что множество разных сред не стребуется. Но конечно, из контейнера удобно было бы запускать и разворачивать на разных серверах.
2 Nodejs легковесное, тут и бэк и фронт вместе. Тк требований по высокой нагрузке нет, то выбираем контейнеры для удобства разворачивания и использования балансера на разных серверах
3 Тут явно лучше использовать контейнеры, тк зависимости для разных ОС будут кардинально разными и версии лучше разделить в разных образах.
4 Вероятно стоит развернуть непосредственно на хостовой машине, чтобы не делать лишные перебросы портов и перенаправления
5 ноды для надежности лучше разносить на разные сервера (ну и для производительности наверное). Так что тут наверное подойдут контейнеры, общающиеся по сокетам.
6 вероятно удобнее развернуть в контейнере - чтобы потом было удобно быстро переместить на нужный сервер за собой. Плюс источники для такого мониторинга идут из понятных адресов - заранее определенных источников апи или бд - само приложение тоже вызывается как простое веб приложение.
однако,если мы хотим мониторить состояние самого сервера и поставить telegraf - то его придется делать демоном на основной хостовой малине для доступа к данным - тогда у нас получится что часть стека мониторинга окажется на одной машине, а часть в контейнере
7 В общем, если грамотно прописать инит скрипты создания бд и подключить персистентное хранилище данных для сохранения базы, то можно использовать контейнер - тогда можно будет быстро перезапустить контейнер и данные получить из инит скрипта.
Но для продакшн приложения вероятно стоит и просто отдельный VPS использовать
8 Чтобы не разносить вспомогательные сервис ына разные сервера, наверное стоит для них использовать докер - вряд ли им требуется выносливость высокой нагрузки и 
они спокойно уживутся на одном внутреннем сервере.
```

# Задача 3

Запустите первый контейнер из образа centos c любым тэгом в фоновом режиме, подключив папку /data из текущей рабочей директории на хостовой машине в /data контейнера;
Запустите второй контейнер из образа debian в фоновом режиме, подключив папку /data из текущей рабочей директории на хостовой машине в /data контейнера;
Подключитесь к первому контейнеру с помощью docker exec и создайте текстовый файл любого содержания в /data;
Добавьте еще один файл в папку /data на хостовой машине;
Подключитесь во второй контейнер и отобразите листинг и содержание файлов в /data контейнера.


```console
root@test-02:~/nginx_docker/site-content# docker pull centos
root@test-02:~/nginx_docker/site-content# docker pull debian
cd ~
mkdir centos_docker
mkdir debian_docker
cd centos_docker
echo 'FROM centos' > ./Dockerfile
docker build -t daniiche/centos:1.0 .
mkdir ~/data
root@test-02:~/centos_docker# docker run -it -d -v ~/data:/data daniiche/centos:1.0
ad0f70531c6f095f66a3329ea957a292a7c44d839212697f398abb0eeb5dcc84

cd ../debian_docker
echo 'FROM debian' > ./Dockerfile
docker build -t daniiche/debian:1.0 .
docker run -it -d -v ~/data:/data daniiche/debian:1.0

docker exec -it dreamy_chaplygin bash
[root@a89aa22e4543 /]# cd /data
touch NoNoReadMe
exit

cd ~/data
touch YesPleasereadme

root@test-02:~/data# docker exec -it distracted_gauss ls /data
NoNoReadMe  YesPleasereadme
```

# Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.


```console
vagrant@server1:~$ ls
get-docker.sh
vagrant@server1:~$ vim Dockerfile
vagrant@server1:~$ ls
Dockerfile  get-docker.sh
vagrant@server1:~$ docker build -t daniiche/ansible:2.9.24 .
...
Successfully tagged daniiche/ansible:2.9.24
vagrant@server1:~$ docker login -u daniiche
Password: 
WARNING! Your password will be stored unencrypted in /home/vagrant/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
vagrant@server1:~$ DOCKER_BUILDKIT=0
vagrant@server1:~$ docker images
REPOSITORY         TAG       IMAGE ID       CREATED         SIZE
daniiche/ansible   2.9.24    a7ac9f0388a7   2 minutes ago   227MB
alpine             3.14      0a97eee8041e   2 months ago    5.61MB
vagrant@server1:~$ docker push daniiche/ansible:2.9.24
The push refers to repository [docker.io/daniiche/ansible]
390d424dec96: Pushed 
24fef7bd6563: Pushed 
1a058d5342cc: Mounted from library/alpine 
2.9.24: digest: sha256:1289326d58e329490a89760ab76f6437154a34b3d8fe15d65a98731eeedba932 size: 947

```

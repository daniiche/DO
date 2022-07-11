## Домашнее задание к занятию "09.05 Gitlab"

## Подготовка к выполнению

Необходимо зарегистрироваться
Создайте свой новый проект
Создайте новый репозиторий в gitlab, наполните его файлами
Проект должен быть публичным, остальные настройки по желанию

```
регаемся
добавляем файл в репу
проект публичный

В чатах все писали, что пайплайны в облаке гитлаб не работают, поэтому установка сразу будет вестись локально


```


## Основная часть

## DevOps

В репозитории содержится код проекта на python. Проект - RESTful API сервис. Ваша задача автоматизировать сборку образа с выполнением python-скрипта:

Образ собирается на основе centos:7
Python версии не ниже 3.7
Установлены зависимости: flask flask-jsonpify flask-restful
Создана директория /python_api
Скрипт из репозитория размещён в /python_api
Точка вызова: запуск скрипта
Если сборка происходит на ветке master: Образ должен пушится в docker registry вашего gitlab python-api:latest, иначе этот шаг нужно пропустить

```
по требованиям создан докерфайл для образа

FROM centos:7

RUN yum update -y && yum install -y python3 python3-pip
RUN pip3 install flask flask_restful flask_jsonpify

ADD /python-api.py /python_api/python-api.py

ENTRYPOINT ["python3", "/python_api/python-api.py"]


описание пайплайна для сборки в файле .gitlab-ci.yml

image: docker:latest
variables:
  DOCKER_TLS_CERTDIR: ''
  DOCKER_HOST: tcp://80.78.241.188:2375
  DOCKER_DRIVER: overlay2
services:
    - docker:dind
before_script:
   - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
stage_build:
    stage: build
    script:
        - docker build -t $CI_REGISTRY/buudda/dotest/image:latest .
    except:
        - main
stage_deploy:
    stage: deploy
    script:
        - docker build -t $CI_REGISTRY/buudda/dotest/python-api.py:latest .
        - docker push $CI_REGISTRY/buudda/dotest/python-api.py:latest
    only:
        - main

запустить докер демон
root@80-78-241-188:~# sudo mkdir -p /etc/systemd/system/docker.service.d
root@80-78-241-188:~# sudo nano /etc/systemd/system/docker.service.d/options.conf
root@80-78-241-188:~# sudo systemctl daemon-reload
root@80-78-241-188:~# sudo systemctl restart docker

запуск pipeline failed, поэтому как писали в чате, поднимаем свой раннер

root@80-78-241-188:~# docker run -d --name gitlab-runner --restart always \
>   -v /srv/gitlab-runner/config:/etc/gitlab-runner \
>   -v /var/run/docker.sock:/var/run/docker.sock \
>   gitlab/gitlab-runner:latest

отключаем общие раннеры в проекте

настраиваем раннер
docker exec -it 52d477ff22a7aeb4d40e4e76d748021dfa50d5fae654e3598bdfd5c268a5b4a4 bash

root@52d477ff22a7:/# gitlab-runner register
Runtime platform                                    arch=amd64 os=linux pid=38 revision=76984217 version=15.1.0
Running in system-mode.                            
                                                   
Enter the GitLab instance URL (for example, https://gitlab.com/):
https://gitlab.com/
Enter the registration token:
*******************************
Enter a description for the runner:
[52d477ff22a7]:gitlab 
Enter tags for the runner (comma-separated):
docker
Enter optional maintenance note for the runner:

Registering runner... succeeded                     runner=GR13489413ve1qy-t
Enter an executor: virtualbox, docker-ssh+machine, kubernetes, docker, parallels, shell, ssh, docker+machine, custom, docker-ssh:
docker
Enter the default Docker image (for example, ruby:2.7):
docker:latest
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded! 


раннер завис в статусе stuck, нужно было проставить галочку "untagged jobs"

Running with gitlab-runner 15.1.0 (76984217)
2  on пш�gitlab kCLTSr2w

3
Preparing the "docker" executor
4Using Docker executor with image docker:latest ...
5Starting service docker:dind ...
6Pulling docker image docker:dind ...
7Using docker image sha256:527ff5beca4347e107e7ffa271400ebfb9a10af9661cc77b52751699a9c15810 for docker:dind with digest docker@sha256:6dd895238f055a79a6d044f7d97b668bef0f9a840e5eed06fa01f1a6b7aed17e ...
8Waiting for services to be up and running (timeout 30 seconds)...
9*** WARNING: Service runner-kcltsr2w-project-37741234-concurrent-0-060f357e09541a56-docker-0 probably didn't start properly.
10Health check error:
11service "runner-kcltsr2w-project-37741234-concurrent-0-060f357e09541a56-docker-0-wait-for-service" timeout
12Health check container logs:
13Service container logs:
142022-07-11T19:50:50.367751499Z ip: can't find device 'ip_tables'
152022-07-11T19:50:50.376389441Z ip_tables              32768  2 iptable_filter,iptable_nat
162022-07-11T19:50:50.377208832Z x_tables               40960  7 ipt_REJECT,xt_multiport,xt_conntrack,xt_MASQUERADE,xt_addrtype,iptable_filter,ip_tables
172022-07-11T19:50:50.377270392Z modprobe: can't change directory to '/lib/modules': No such file or directory
182022-07-11T19:50:50.381933497Z mount: permission denied (are you root?)
192022-07-11T19:50:50.382708597Z Could not mount /sys/kernel/security.
202022-07-11T19:50:50.382734992Z AppArmor detection and --privileged mode might break.
212022-07-11T19:50:50.387113124Z mount: permission denied (are you root?)
22*********
23Pulling docker image docker:latest ...
24Using docker image sha256:c8dffce8f3d6a8e35b8ed0d2ca71c26ae8a9d351260d7f9b4f0689bb1c1da724 for docker:latest with digest docker@sha256:cee19af93958077db280d3987fef99866f539a8b640fc2e2ee0653f780d3de26 ...

25
Preparing environment
00:01
26Running on runner-kcltsr2w-project-37741234-concurrent-0 via 52d477ff22a7...

27
Getting source from Git repository
00:02
28Fetching changes with git depth set to 20...
29Reinitialized existing Git repository in /builds/buudda/dotest/.git/
30Checking out a2232c8b as main...
31Skipping Git submodules setup

32
Executing "step_script" stage of the job script
33Using docker image sha256:c8dffce8f3d6a8e35b8ed0d2ca71c26ae8a9d351260d7f9b4f0689bb1c1da724 for docker:latest with digest docker@sha256:cee19af93958077db280d3987fef99866f539a8b640fc2e2ee0653f780d3de26 ...
34$ docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
35WARNING! Using --password via the CLI is insecure. Use --password-stdin.
36WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
37Configure a credential helper to remove this warning. See
38https://docs.docker.com/engine/reference/commandline/login/#credentials-store
39Login Succeeded
40$ docker build -t $CI_REGISTRY/buudda/dotest/python-api.py:latest .
41Step 1/5 : FROM centos:7
427: Pulling from library/centos
432d473b07cdd5: Pulling fs layer
442d473b07cdd5: Verifying Checksum
452d473b07cdd5: Download complete
462d473b07cdd5: Pull complete
47Digest: sha256:c73f515d06b0fa07bb18d8202035e739a494ce760aa73129f60f4bf2bd22b407
48Status: Downloaded newer image for centos:7
49 ---> eeb6ee3f44bd
50Step 2/5 : RUN yum update -y && yum install -y python3 python3-pip
51 ---> Running in 37a292e6dcea
52Loaded plugins: fastestmirror, ovl
53Determining fastest mirrors
54 * base: mirror.sale-dedic.com
55 * extras: mirror.sale-dedic.com
56 * updates: mirror.corbina.net
57Resolving Dependencies
*********************************************************************************
Step 4/5 : ADD /python-api.py /python_api/python-api.py
569 ---> d5e9feb361d9
570Step 5/5 : ENTRYPOINT ["python3", "/python_api/python-api.py"]
571 ---> Running in f72c0df8837a
572Removing intermediate container f72c0df8837a
573 ---> acdb51e392a6
574Successfully built acdb51e392a6
575Successfully tagged registry.gitlab.com/buudda/dotest/python-api.py:latest
576$ docker push $CI_REGISTRY/buudda/dotest/python-api.py:latest
577The push refers to repository [registry.gitlab.com/buudda/dotest/python-api.py]
578d7e158a4a264: Preparing
579c5ea6bc62dd9: Preparing
5800e2e64f5d8af: Preparing
581174f56854903: Preparing
582d7e158a4a264: Pushed
583c5ea6bc62dd9: Pushed
584174f56854903: Pushed
5850e2e64f5d8af: Pushed
586latest: digest: sha256:48001973e43bff4147ce3846530bbd5ba4185122eae9e54ee8f3584d1bd1c82c size: 1160

587
Cleaning up project directory and file based variables
00:00
588Job succeeded

```


## Product Owner

Вашему проекту нужна бизнесовая доработка: необходимо поменять JSON ответа на вызов метода GET /rest/api/get_info, необходимо создать Issue в котором указать:

Какой метод необходимо исправить
Текст с { "message": "Already started" } на { "message": "Running"}
Issue поставить label: feature

```
Создал issue https://gitlab.com/buudda/dotest/-/issues/1
```

## Developer

Вам пришел новый Issue на доработку, вам необходимо:

Создать отдельную ветку, связанную с этим issue
Внести изменения по тексту из задания
Подготовить Merge Requst, влить необходимые изменения в master, проверить, что сборка прошла успешно

```
create merge branch на основе issue
открываем ветку в IDE
ВНосим изменения, коммитим
Аппрувим МР
Проверяем успех сборки

```

## Tester

Разработчики выполнили новый Issue, необходимо проверить валидность изменений:

Поднять докер-контейнер с образом python-api:latest и проверить возврат метода на корректность
Закрыть Issue с комментарием об успешности прохождения, указав желаемый результат и фактически достигнутый
Итог

После успешного прохождения всех ролей - отправьте ссылку на ваш проект в гитлаб, как решение домашнего задания

```
root@80-78-241-188:~# docker pull registry.gitlab.com/buudda/dotest/python-api.py
Using default tag: latest
latest: Pulling from buudda/dotest/python-api.py
Digest: sha256:48001973e43bff4147ce3846530bbd5ba4185122eae9e54ee8f3584d1bd1c82c
Status: Image is up to date for registry.gitlab.com/buudda/dotest/python-api.py:latest
registry.gitlab.com/buudda/dotest/python-api.py:latest
root@80-78-241-188:~# docker container run -p 5290:5290 -d registry.gitlab.com/buudda/dotest/python-api.py:latest
e26a8cbe88d20f51d0dd93a66d2dc647859885bdc48febc0e686c9492e326b6e
root@80-78-241-188:~# curl localhost:5290/get_info
{"version": 3, "method": "GET", "message": "Already started"}

почему то старая версия сообщения

кажется я пропустил нажатие самого мержа и закрыл его раньше, возвращаюсь.

пробую еще раз

root@80-78-241-188:~# docker container stop e26a8cbe88d20f51d0dd93a66d2dc647859885bdc48febc0e686c9492e326b6e
e26a8cbe88d20f51d0dd93a66d2dc647859885bdc48febc0e686c9492e326b6e
root@80-78-241-188:~# docker pull registry.gitlab.com/buudda/dotest/python-api.py
Using default tag: latest
latest: Pulling from buudda/dotest/python-api.py
Digest: sha256:030c6535226592df43b2b4b36ddc698df4d4765c07aded6ddd0f321b979a795e
Status: Image is up to date for registry.gitlab.com/buudda/dotest/python-api.py:latest
registry.gitlab.com/buudda/dotest/python-api.py:latest
root@80-78-241-188:~# docker container run -p 5290:5290 -d registry.gitlab.com/buudda/dotest/python-api.py:latest
39b4c7c4c0d0187e7426e0bb89832dfcb287d756d29ce6bec55f787f5002c6f0
root@80-78-241-188:~# curl localhost:5290/get_info
{"version": 3, "method": "GET", "message": "Running"}

ссылка на гитлаб https://gitlab.com/buudda/dotest/-/pipelines
```

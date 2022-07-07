Домашнее задание к занятию "09.03 Jenkins"

## Подготовка к выполнению

1 Установить jenkins по любой из инструкций
2 Запустить и проверить работоспособность
3 Сделать первоначальную настройку
4 Настроить под свои нужды
5 Поднять отдельный cloud
6 Для динамических агентов можно использовать образ
7 Обязательный параметр: поставить label для динамических агентов: ansible_docker
8 Сделать форк репозитория с playbook

## Выполнение
1 
# docker-compose.yaml
version: '3.8'
services:
 jenkins:
  image: jenkins/jenkins:lts
  privileged: true
  user: root
  ports:
  - 8080:8080
  - 50000:50000
  container_name: jenkins
  volumes:
   - /home/root/jenkins-docker-compose/jenkins_configuration:/var/jenkins_home
   - /var/run/docker.sock:/var/run/docker.sock

2
открылся на порте 8080

3
password
/var/jenkins_home/secrets/initialAdminPassword
11fda855f8d045498cf2b7e583fc1660

4
стандартная настройка, сменил количество сборщиков с 2 на 0 на Мастере.

5-6
приведенный докерхаб не работает, завожу свой
создаю ключ rsa, добавляю в дженкинс
добавляю агента в докер компоуз, добавляю ноду через интерфейс
# docker-compose.yaml
version: '3.8'
services:
 jenkins:
  image: jenkins/jenkins:lts
  privileged: true
  user: root
  ports:
   - 8080:8080
   - 50000:50000
  container_name: jenkins
  volumes:
   - /home/root/jenkins-docker-compose/jenkins_configuration:/var/jenkins_home
   - /var/run/docker.sock:/var/run/docker.sock
 agent:
  image: jenkins/ssh-agent:jdk11
  privileged: true
  user: root
  container_name: agent
  expose:
   - 22
  environment:
   - JENKINS_AGENT_SSH_PUBKEY=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDIX3AXUI1vZlrWWnP/fDkr5/TWf118gF5cnXCoOqS0DQvOm9v0nUX86qGPjpfG/q3MQlN3MywRBgrY6Ay1gtLhQMKEIM1yavuIOEBLoJe+lp4HNM1UmGBLe04AQAUg8HMTptuM9Lf2GMDZHIxGlFLbiGCCyqYNu1adD6N6sOiLiQd3IGKAu+YUW1HwjnX7o2hTVUAz5exOT7PUG1nK8pnbp/e0YSF9cBDKaNHITCnk+A+z64aEWzgQ/vqvvXtsQNGiZrKLHA8r2GKLkFamRY1DqB9f+2Ab8tuW6g+988yElzdNLo5/wZnml7Hh+E3UgvTq7r2SW9vciGjNH6jFGJQKY8cEljMLBiCj3a37J2mxdsglX023B9aMvb7lFKitemlAqZ9hWp8XRjNNPGwZhK5ptkFN5hFBDmrKshIPvG/kY1JyHKmXtOuBc+nx5ffP1igH9yNoAoYQAHacyfgtFdryIrPGKClD86ljVAfVcaKQ/6bkrgSkpBM3cXrWtgiI2Rk= root@80-78-241-188.cloudvps.regruhosting.ru

Evacuated stdout
Agent successfully connected and online

7 метку ноде поставил

8 репу форкнул
https://github.com/daniiche/example-playbook


## Основная часть

Сделать Freestyle Job, который будет запускать ansible-playbook из форка репозитория
Сделать Declarative Pipeline, который будет выкачивать репозиторий с плейбукой и запускать её
Перенести Declarative Pipeline в репозиторий в файл Jenkinsfile
Перенастроить Job на использование Jenkinsfile из репозитория
Создать Scripted Pipeline, наполнить его скриптом из pipeline
Заменить credentialsId на свой собственный
Проверить работоспособность, исправить ошибки, исправленный Pipeline вложить в репозитрий в файл ScriptedJenkinsfile
Отправить ссылку на репозиторий в ответе

## Выполнение

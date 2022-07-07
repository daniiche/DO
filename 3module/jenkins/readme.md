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
```
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
```

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

```
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
```

Evacuated stdout
Agent successfully connected and online

7 метку ноде поставил

8 репу форкнул
https://github.com/daniiche/example-playbook


## Основная часть

1 Сделать Freestyle Job, который будет запускать ansible-playbook из форка репозитория
пришлось установить гит на агента
и ансибл apt-get install ansible -y

```
ansible-galaxy install -p $WORKSPACE -r requirements.yml
ansible-playbook ./site.yml -i ./inventory/prod.yml
```

оп предоставленному плейбуку ява упала

```
Started by user admin
Running as SYSTEM
Building remotely on jenkins_agent (ansible_docker) in workspace /home/jenkins/agent/workspace/Freestyle_ansible
The recommended git tool is: NONE
using credential 6d0a82bd-b2e4-4bf8-8a7c-7a4c5cf1291e
 > git rev-parse --resolve-git-dir /home/jenkins/agent/workspace/Freestyle_ansible/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/daniiche/example-playbook.git # timeout=10
Fetching upstream changes from https://github.com/daniiche/example-playbook.git
 > git --version # timeout=10
 > git --version # 'git version 2.30.2'
using GIT_ASKPASS to set credentials GitHub
 > git fetch --tags --force --progress -- https://github.com/daniiche/example-playbook.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse refs/remotes/origin/master^{commit} # timeout=10
Checking out Revision 7c0b99e0464c8c4cf2ac3e9d802379edfe06df00 (refs/remotes/origin/master)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f 7c0b99e0464c8c4cf2ac3e9d802379edfe06df00 # timeout=10
Commit message: "Update secret"
 > git rev-list --no-walk 7c0b99e0464c8c4cf2ac3e9d802379edfe06df00 # timeout=10
[Freestyle_ansible] $ /bin/sh -xe /tmp/jenkins11172031793477929436.sh
+ ansible-galaxy install -p /home/jenkins/agent/workspace/Freestyle_ansible -r requirements.yml
Starting galaxy role install process
[WARNING]: - java was NOT installed successfully: - command /usr/bin/git clone
git@github.com:netology-code/mnt-homeworks-ansible.git java failed in directory
/home/jenkins/.ansible/tmp/ansible-local-49188zu0mm1m/tmppybf_cov (rc=128) -
Cloning into 'java'... Host key verification failed.  fatal: Could not read
from remote repository.  Please make sure you have the correct access rights
and the repository exists.
ERROR! - you can use --ignore-errors to skip failed roles and finish processing the list.
Build step 'Execute shell' marked build as failure
Finished: FAILURE
```

2 Сделать Declarative Pipeline, который будет выкачивать репозиторий с плейбукой и запускать её
Declarative Pipeline

```
pipeline {
    agent any
    stages {
        stage('Download code') {
            steps {
                git 'https://github.com/daniiche/example-playbook.git'
            }
        }
        stage('Execute ansible') {
            steps {
                sh 'ansible-galaxy install -p $WORKSPACE -r requirements.yml'
                sh 'ansible-playbook ./site.yml -i ./inventory/prod.yml'
            }
        }
    }
}
```


3 Перенести Declarative Pipeline в репозиторий в файл Jenkinsfile
епренес https://github.com/daniiche/example-playbook/blob/master/Jenkinsfile

4 Перенастроить Job на использование Jenkinsfile из репозитория
тот же пайплайн как в прошлом шаге, только файл берется по ссылке из репозитория
pipeline from script SCM

5 Создать Scripted Pipeline, наполнить его скриптом из pipeline
```
node("ansible_docker"){
    stage("Git checkout"){
        git credentialsId: '6d0a82bd-b2e4-4bf8-8a7c-7a4c5cf1291e', url: 'https://github.com/daniiche/example-playbook.git'
    }
    stage("Check ssh key"){
        secret_check=false
    }
    stage("Run playbook"){
        if (secret_check){
            sh 'ansible-playbook site.yml -i inventory/prod.yml'
        }
        else{
            echo 'no more keys'
        }
        
    }
}
```

6 Заменить credentialsId на свой собственный


7 Проверить работоспособность, исправить ошибки, исправленный Pipeline вложить в репозитрий в файл ScriptedJenkinsfile
```
node("ansible_docker"){
    stage("Git checkout"){
        git credentialsId: '6d0a82bd-b2e4-4bf8-8a7c-7a4c5cf1291e', url: 'https://github.com/daniiche/example-playbook.git'
    }
    stage("Check ssh key"){
        secret_check=false
    }
    stage("Run playbook"){
        if (secret_check){
            sh 'ansible-galaxy install -p $WORKSPACE -r requirements.yml'
            sh 'ansible-playbook ./site.yml -i ./inventory/prod.yml'
        }
        else{
            echo 'no more keys'
        }
        
    }
}
```
SUCCESS

8 Отправить ссылку на репозиторий в ответе
https://github.com/daniiche/example-playbook

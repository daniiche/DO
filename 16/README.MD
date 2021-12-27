
#Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

#Обязательная задача 1

Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
 ```
Нужно найти и исправить все ошибки, которые допускает наш сервис

```json
        { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```

#Обязательная задача 2

В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

Ваш скрипт:

```python
# !/usr/bin/env python
import socket
import os
import json
import yaml

filename = 'ips.'

def checkIp(ip_dict):
    ip_dict = ip_dict
    for ip in ip_dict:
        try:
            ip_dict[ip] = socket.gethostbyname(ip)
        except BrokenPipeError as e:
            print('e')
    return ip_dict

def openFile():
    try:
        with open(file=os.path.join('.', f'{filename}json'), mode='r') as file:
            return json.load(file)
    except:
        return {
            'drive.google.com': None
            ,'mail.google.com':None
            ,'google.com':None
        }
    try:
        with open(file=os.path.join('.', f'{filename}yaml'), mode='r') as file:
            return yaml.safe_load(file)
    except:
        return {
            'drive.google.com': None
            ,'mail.google.com':None
            ,'google.com':None
        }

def updateFile(ip_dict):
    with open(file=os.path.join('.', f'{filename}json'), mode='w') as file:
        json.dump(ip_dict,file)

    with open(file=os.path.join('.', f'{filename}yaml'), mode='w') as file:
        yaml.safe_dump(ip_dict,file)

if __name__ == '__main__':
    ip_dict = openFile()

    ip_dict = checkIp(ip_dict)
    updateFile(ip_dict)
```
Вывод скрипта при запуске при тестировании:

```
Process finished with exit code 0
```
json-файл(ы), который(е) записал ваш скрипт:

```
{"drive.google.com": "173.194.73.194", "mail.google.com": "173.194.73.18", "google.com": "64.233.161.100"}
```
yml-файл(ы), который(е) записал ваш скрипт:

```
drive.google.com: 173.194.73.194
google.com: 64.233.161.100
mail.google.com: 173.194.73.18
```

#Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:

Принимать на вход имя файла
Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов
Ваш скрипт:

???
Пример работы скрипта:

???

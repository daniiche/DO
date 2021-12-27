
# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

# Обязательная задача 1

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

# Обязательная задача 2

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

# Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:

Принимать на вход имя файла
Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов
Ваш скрипт:

```python
import json
import yaml
import argparse

def openfile(filepath):
    imported_file = None
    filepath_export = None
    with open(filepath, 'r') as f:
        if '.json' or '.yaml' in f:
            file = f.read()
            if file.startswith('{' or '[{'):
                try:
                    imported_file = json.loads(file)
                except Exception as e:
                    print(f'Found errors in JSON:\n{e}')
                filepath_export = filepath[:-4]+'YAML'
            else:
                try:
                    imported_file = yaml.safe_load(file)
                except Exception as e:
                    print(f'Found errors in YAML:\n{e}')
                filepath_export = filepath[:-4]+'JSON'
        else:
            print('File is not a YAML or JSON')
        return imported_file, filepath_export

def savefile(imported_file,filepath_export):
    with open(filepath_export,'w') as f:
        if 'JSON' in filepath_export:
            json.dump(imported_file,f)
        elif 'YAML' in filepath_export:
            yaml.safe_dump(imported_file, f)
        else:
            print('Error on saving')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JSON YAML converter')
    parser.add_argument('-f', '--file', help='Path to file', required=True)
    args = vars(parser.parse_args())
    filepath = args['file']
    imported_file,filepath_export = openfile(filepath)
    savefile(imported_file,filepath_export)
    print(f'Successfully saved at {filepath_export}')
```
Пример работы скрипта:

???
```console
(venv) danobook:16 danche$ python format_converter.py -f 'ips.yaml' 
Successfully saved at ips.JSON

(venv) danobook:16 danche$ python format_converter.py -f 'ips.json' 
Successfully saved at ips.YAML
```

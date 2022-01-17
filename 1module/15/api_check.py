# !/usr/bin/env python
import socket
import os
import json
import yaml

filename = 'ips.'

def checkIp(ip_dict):
    ip_dict_old = ip_dict
    ip_dict_new = {}
    for url in ip_dict:
        print(url)
        try:
            ip_dict_new[url] = socket.gethostbyname(url)
            if ip_dict_old[url] != ip_dict_new[url]:
                print(f'[ERROR] <{url}> IP mismatch: <{ip_dict_old[url]}> <{ip_dict_new[url]}>')
        except BrokenPipeError as e:
            print('e')
    return ip_dict_new

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


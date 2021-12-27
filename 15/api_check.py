# !/usr/bin/env python
import socket
import os
import json

filepath = os.path.join('.', 'ips.json')

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
        with open(file=filepath, mode='r') as json_file:
            return json.load(fp=json_file)
    except FileNotFoundError as e:
        return {
            'drive.google.com': None
            ,'mail.google.com':None
            ,'google.com':None
        }

def updateFile(ip_dict):
    with open(file=filepath, mode='w') as json_file:
        json.dump(obj=ip_dict, fp=json_file)

if __name__ == '__main__':
    ip_dict = openFile()

    ip_dict = checkIp(ip_dict)

    updateFile(ip_dict)









#gitpython?
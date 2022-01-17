# !/usr/bin/env python
import os
import sys

arg = None
try:
    arg = sys.argv[1]
except:
    print('No args passed.\n1st arg is a path of git repo')
    exit()

bash_command = [f"cd {arg}", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
curr_dir = os.getcwd()
for result in result_os.split('\n'):
    if 'modified' in result:
        prepare_result = result.replace('\tmodified:   ', '')
        print(curr_dir + prepare_result)
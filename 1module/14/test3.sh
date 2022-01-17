#!/usr/bin/env bash


MSG="[04-script-01-bash] added some shit"
#MSG=$1
LEN=30
CODE="[04-script-01-bash]"

if [[ $(echo -n $MSG|wc -m) -gt $LEN ]]
	then
		exit 2
	elif [[ $MSG != *[04-script-01-bash]* ]]
	then
		exit 2
fi
echo its fine!

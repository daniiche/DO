#!/usr/bin/env bash
array_hosts=(192.168.0.1 192.168.0.2 192.168.0.3)
while ((1==1))
do
	for i in ${array_hosts[@]}
	do
		for j in {1..5}
		do
			curl http://$i --max-time 1 2>/dev/null
			if (($? != 0))
				then
					echo ERROR $(date) -- $i >> error.log
				exit
			fi
			echo TRACE $(date) -- $i >> trace.log
		done
	done
	sleep 2
done

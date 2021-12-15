#!/usr/bin/env bash
while ((1==1))
do
curl http://localhost:4757 2>/dev/null
if (($? == 0))
then
echo it worked
exit
fi
date >> curl.log
sleep 3
done



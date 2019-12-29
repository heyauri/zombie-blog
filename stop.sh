#!/bin/sh

pid=`ps -ef|grep "python3 -u main.py"| grep -v "grep"|awk '{print $2}'`

if [ "$pid" != "" ]
then
        kill -9 ${pid}
        echo "stop main.py complete"
else
        echo "main.py is not run, there's no need to stop it"
fi

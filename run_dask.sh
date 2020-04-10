#! /bin/sh
IP=`hostname -I | awk '{print $1}'`
echo $IP
konsole --hold -e dask-scheduler &
sleep 1
konsole --hold -e dask-worker tcp://$IP:8786 &
sleep 1
python3 test_dask.py tcp://$IP:8786

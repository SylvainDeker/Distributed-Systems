#!/usr/bin/env bash
# IP=`hostname -I | awk '{print $1}'`
# echo $IP
# dask-scheduler --pid-file dask-scheduler.pid &
# sleep 2
# dask-worker --preload tile/tile.py --preload tile/buildCollectionTile.py --pid-file dask-worker.pid tcp://$IP:8786 &
# sleep 2
# # python3 daskk/try_dask.py tcp://$IP:8786
# sleep 1
# kill -9 `cat dask-worker.pid`
# sleep 1
# kill -9 `cat dask-scheduler.pid`
# rm dask-scheduler.pid
# rm dask-worker.pid

python3 distributed_systems/try_dask.py

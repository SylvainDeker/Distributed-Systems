#!/usr/bin/env bash

SPARK='./spark-3.0.0-preview2-bin-hadoop2.7/bin/spark-submit'
MEM=4G
MASTER=local[4]

if [[ $# -eq 0 ]]
then
  MAIN=spark/try_spark.py
  EXTRAFILES=Tile/Tile.py,Tile/buildCollectionTile.py
fi
if [[ $# -eq 1 ]]
then
  MAIN=$1
  EXTRAFILES=Tile/Tile.py,Tile/buildCollectionTile.py
fi
if [[ $# -eq 2 ]]
then
  MAIN=$1
  EXTRAFILES=$2
fi



echo "run:\nPYSPARK_PYTHON=python3 ${SPARK} --master ${MASTER} --driver-memory ${MEM} --py-files ${EXTRAFILES} ${MAIN}\n"


PYSPARK_PYTHON=python3 ${SPARK} --master ${MASTER} --driver-memory ${MEM} --py-files ${EXTRAFILES} ${MAIN}

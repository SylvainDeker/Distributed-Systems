#!/usr/bin/env bash

SPARK='spark-submit'
MEM=4G
MASTER='local[4]'
MAIN="distributed_systems/try_spark.py"



# echo "run:\nPYSPARK_PYTHON=python3 ${SPARK} --master ${MASTER} --driver-memory ${MEM} --py-files ${EXTRAFILES} ${MAIN}\n"


# PYSPARK_PYTHON=python3 ${SPARK} --master ${MASTER} --driver-memory ${MEM} ${MAIN}


PYSPARK_PYTHON=python3 python3 ${MAIN}

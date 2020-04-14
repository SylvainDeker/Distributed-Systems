#! /bin/sh

SPARK='./spark-3.0.0-preview2-bin-hadoop2.7/bin/spark-submit'
PYTHONFILE=$1
EXTRAFILE=$2


PYSPARK_PYTHON=python3 ${SPARK} --master local[4] --py-files ${PYTHONFILE} ${EXTRAFILE}

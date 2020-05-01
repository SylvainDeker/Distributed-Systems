#!/usr/bin/env bash


profile_dask()
{
  valgrind --tool=callgrind \
  --callgrind-out-file=profiling/rawdata/callgrind_out.txt \
  --instr-atstart=no \
  --dump-instr=no \
  --simulate-cache=no \
  --collect-jumps=no \
  --cache-sim=no \
  --branch-sim=no \
  python3 profiling/profile_dask.py $1 $2
}

profile_spark()
{
  SPARK='./spark-3.0.0-preview2-bin-hadoop2.7/bin/spark-submit'
  MEM=4G
  MASTER=local[4]
  MAIN=profiling/profile_spark_pycallgrind.py
  EXTRAFILES=distributed_systems/tile.py,distributed_systems/buildCollectionTile.py

  export PYSPARK_PYTHON=python3

  valgrind --tool=callgrind \
  --callgrind-out-file=profiling/rawdata/callgrind_out.txt \
  --instr-atstart=no \
  --dump-instr=no \
  --simulate-cache=no \
  --collect-jumps=no \
  --cache-sim=no \
  --branch-sim=no \
  ${SPARK} --master ${MASTER} --driver-memory ${MEM} --py-files ${EXTRAFILES} ${MAIN}
}




profile_dask $1 $2
# profile_spark

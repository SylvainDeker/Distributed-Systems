#!/usr/bin/env bash



extract_data_from_callgrind_file()
{
  # cat $1 | head -4 | tail -1 | awk '{print $2}' | sed 's/,//g' > .return
  FUNCTIONS=`cat $1 | head -4 | tail -1 | awk '{print $2}' | sed 's/,//g'`
  FUNCTIONS_EXEC=`cat $1 | head -4 | tail -1 | awk '{print $4}' | sed 's/,//g'`
  CONTEXTS=`cat $1 | head -4 | tail -1 | awk '{print $6}' | sed 's/,//g' | sed 's/)//g'`
  BASIC_BLOCS=`cat $1 | head -5 | tail -1 | awk '{print $3}' | sed 's/,//g'`
  BASIC_BLOCS_EXEC=`cat $1 | head -5 | tail -1 | awk '{print $5}' | sed 's/,//g'`
  CALL_SITES=`cat $1 | head -5 | tail -1 | awk '{print $8}' | sed 's/,//g' | sed 's/)//g'`
  echo "$FUNCTIONS $FUNCTIONS_EXEC $CONTEXTS $BASIC_BLOCS $BASIC_BLOCS_EXEC $CALL_SITES"
}


profile_dask()
{
  valgrind --tool=callgrind \
  --instr-atstart=no \
  --dump-instr=no \
  --simulate-cache=no \
  --collect-jumps=no \
  --cache-sim=no \
  --branch-sim=no \
  python3 profiling/profile_dask.py $1 $2
}

# profile_spark()
# {
#   SPARK='./spark-3.0.0-preview2-bin-hadoop2.7/bin/spark-submit'
#   MEM=4G
#   MASTER=local[4]
#   MAIN=profiling/profile_spark.py
#   EXTRAFILES=distributed_systems/tile.py,distributed_systems/buildCollectionTile.py
#
#   export PYSPARK_PYTHON=python3
#
#   valgrind --tool=callgrind \
#   --instr-atstart=no \
#   --dump-instr=no \
#   --simulate-cache=no \
#   --collect-jumps=no \
#   --cache-sim=no \
#   --branch-sim=no \
#   ${SPARK} --master ${MASTER} --driver-memory ${MEM} --py-files ${EXTRAFILES} ${MAIN}
# }

CALLGRIND_GRAPH=callgrind_graph.txt
CALLGRIND_COMPUTE=callgrind_compute.txt
for ((i=500 ; 9000 - $i ; i=i+500))
do
  # echo $i
  profile_dask $i $i
  extract_data_from_callgrind_file $CALLGRIND_GRAPH >> profiling/rawdata/results_graph.csv
  extract_data_from_callgrind_file $CALLGRIND_COMPUTE >> profiling/rawdata/results_compute.csv
done

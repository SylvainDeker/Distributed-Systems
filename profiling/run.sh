#!/usr/bin/env bash



extract_data_from_callgrind_file()
{
  cat $1 | head -4 | tail -1 | awk '{print $2}' | sed 's/,//g' > .return
}

extract_data_from_callgrind_file callgrind_compute.txt
cat .return

profile_dask()
{
  valgrind --tool=callgrind \
  --instr-atstart=no \
  --dump-instr=no \
  --simulate-cache=no \
  --collect-jumps=no \
  --cache-sim=no \
  --branch-sim=no \
  python3 profiling/profile_dask.py
}

profile_spark()
{
  SPARK='./spark-3.0.0-preview2-bin-hadoop2.7/bin/spark-submit'
  MEM=4G
  MASTER=local[4]
  MAIN=profiling/profile_spark.py
  EXTRAFILES=distributed_systems/tile.py,distributed_systems/buildCollectionTile.py

  export PYSPARK_PYTHON=python3

  valgrind --tool=callgrind \
  --instr-atstart=no \
  --dump-instr=no \
  --simulate-cache=no \
  --collect-jumps=no \
  --cache-sim=no \
  --branch-sim=no \
  ${SPARK} --master ${MASTER} --driver-memory ${MEM} --py-files ${EXTRAFILES} ${MAIN}
}

end()
{
  rm -f .return
}

RESULT_FILE=result.csv
profile_dask
extract_data_from_callgrind_file callgrind_graph.txt
cat .return >> ${RESULT_FILE}

extract_data_from_callgrind_file callgrind_compute.txt
cat .return >> ${RESULT_FILE}



end

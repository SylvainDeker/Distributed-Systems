#!/usr/bin/env bash


#
# extract_data_from_callgrind_file()
# {
#   # cat $1 | head -4 | tail -1 | awk '{print $2}' | sed 's/,//g' > .return
#   FUNCTIONS=`cat $1 | head -4 | tail -1 | awk '{print $2}' | sed 's/,//g'`
#   FUNCTIONS_EXEC=`cat $1 | head -4 | tail -1 | awk '{print $4}' | sed 's/,//g'`
#   CONTEXTS=`cat $1 | head -4 | tail -1 | awk '{print $6}' | sed 's/,//g' | sed 's/)//g'`
#   BASIC_BLOCS=`cat $1 | head -5 | tail -1 | awk '{print $3}' | sed 's/,//g'`
#   BASIC_BLOCS_EXEC=`cat $1 | head -5 | tail -1 | awk '{print $5}' | sed 's/,//g'`
#   CALL_SITES=`cat $1 | head -5 | tail -1 | awk '{print $8}' | sed 's/,//g' | sed 's/)//g'`
#   echo "$FUNCTIONS $FUNCTIONS_EXEC $CONTEXTS $BASIC_BLOCS $BASIC_BLOCS_EXEC $CALL_SITES"
# }

# CALLGRIND_GRAPH=callgrind_graph.txt
# CALLGRIND_COMPUTE=callgrind_compute.txt
# for ((i=500 ; 9000 - $i ; i=i+500))
# do
#   # echo $i
#   profile_dask $i $i
#   extract_data_from_callgrind_file $CALLGRIND_GRAPH >> profiling/rawdata/results_graph.csv
#   extract_data_from_callgrind_file $CALLGRIND_COMPUTE >> profiling/rawdata/results_compute.csv
# done

# valgrind_dask()
# {
#   valgrind --tool=callgrind \
#   --instr-atstart=no \
#   --dump-instr=no \
#   --simulate-cache=no \
#   --collect-jumps=no \
#   --cache-sim=no \
#   --branch-sim=no \
#   python3 profiling/profile_dask.py $1 $2
# }

IMAGE=data/NE1_50M_SR_W/NE1_50M_SR_W.tif
CONFIG=config.yaml
run_spark()
{
python3 -c "\
from distributed_systems.dark import Dark
dk = Dark(\"$IMAGE\",(500,500),\"$CONFIG\")
dk.run_spark()
print(dk.timer)" 2> /dev/null
}

run_dask()
{
python3 -c "\
from distributed_systems.dark import Dark
dk = Dark(\"$IMAGE\",(500,500),\"$CONFIG\")
dk.run_dask()
print(dk.timer)"
}

run()
{
python3 -c "\
from distributed_systems.dark import Dark
dk = Dark(\"$IMAGE\",(500,500),\"$CONFIG\")
dk.run()
print(dk.timer)"
}

mem_run()
{
valgrind --tool=cachegrind \
python3 -c "\
from distributed_systems.dark import Dark
dk = Dark(\"$IMAGE\",(500,500),\"$CONFIG\")
dk.run()
print(dk.timer)"
}

#   --callgrind-out-file=profiling/rawdata/callgrind_out.txt \
# --instr-atstart=no \
# --trace-children=yes \
# --dump-instr=no \
# --simulate-cache=no \
# --collect-jumps=no \
# --cache-sim=no \
# --branch-sim=no \
# run_spark
# run_dask
# run
# python3 -c "print(\"coucouc\")"
mem_run
rm -f cachegrind.out.*

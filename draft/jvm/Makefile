all:
	javac HelloWorld.java

run: all
	java HelloWorld

callgrind: all
	valgrind --tool=callgrind \
	--trace-children=yes \
	--smc-check=all \
	java HelloWorld


#  --callgrind-out-file=profiling/rawdata/callgrind_out.txt
# --smc-check=all
# --instr-atstart=no
# --trace-children=yes
# --dump-instr=no
# --simulate-cache=no
# --collect-jumps=no
# --cache-sim=no
# --branch-sim=no
#





# https://valgrind.org/docs/manual/valgrind_manual.pdf

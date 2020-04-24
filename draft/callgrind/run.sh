#!/bin/sh
exit(0)

valgrind --tool=callgrind ./test.py

#######################
# During callgrind
# callgrind_control -b
# callgrind_control -e -b
# cache behavior of your program, use Callgrind with the option --cache-sim=yes
#######################

#After the end
# callgrind_annotate callgrind.out.905

# callgrind_annotate --inclusive=yes callgrind.out.905
# callgrind_annotate --tree=both callgrind.out.905


# Use --auto=yes to get annotated source code for all relevant functions
  #for which the source can be found
# For branch prediction simulation, use --branch-sim=yes. Expect a further slow down approximately by a factor of 2.

# If the program section you want to profile is somewhere in the middle of the run,
  # it is beneficial to fast forward to this section without any profiling,
  #and then enable profiling.

# This is achieved by using the command line option --instr-atstart=no and running, in a shell: callgrind_control -i on just before the interesting code section is executed. To exactly specify the code position where profiling should start, use the client request CALLGRIND_START_INSTRUMENTATION.

# assembly code level annotation =>  --dump-instr=yes (This will produce profile data at instruction granularity, viewed with KCachegrind)
# details of the control flow inside of functions, i.e. (conditional) jumps. =>--collect-jumps=yes.


####### https://matthieu-brucher.developpez.com/tutoriels/cpp/profil-valgrind-visual-studio/?page=valgrind
# Valgrind =
#     memcheck, qui vérifie les fuites mémoires, les dépassements,
#     cachegrind, qui mesure des données par rapport au cache,
#     callgrind, qui est le profileur en question.
#
# Valgrind génère un fichier de résultat qui pourra être analysé par KCacheGrind.


valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --compute-jumps=yes python exemples/measure_image.py

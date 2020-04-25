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


# --auto=yes to get annotated source code for all relevant functions
# --branch-sim=yes For branch prediction simulation,


# assembly code level annotation =>  --dump-instr=yes (This will produce profile data at instruction granularity, viewed with KCachegrind)
# details of the control flow inside of functions, i.e. (conditional) jumps. =>--collect-jumps=yes.


valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes python3 test4.py
# --dump-instr=yes permet d'enregistrer les instructions exécutées, indispensable pour comparer avec le code source
# --simulate-cache=yes ajoute les coûts liés au cache,
# --collect-jumps=yes ajoute les sauts dans le rapport.

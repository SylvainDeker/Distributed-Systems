#!/bin/sh

if [ $# -ne 1 ]
then
  echo "usage: $0 <file.py>"
  exit 1
fi
CALLGRIND_OUT=callgrind.out.txt

#######################
# During callgrind
# callgrind_control -b
# callgrind_control -e -b
# cache behavior of your program, use Callgrind with the option --cache-sim=yes
#######################

valgrind --tool=callgrind \
--callgrind-out-file=${CALLGRIND_OUT} \
--dump-instr=yes \
--simulate-cache=no \
--collect-jumps=yes \
--cache-sim=no \
--branch-sim=no \
--instr-atstart=yes \
python3 $1
# --instr-atstart=no start valgrind with  callgrind_control -i off
# --cache-sim=no Mesure chache behavior of the program
# --branch-sim=no branch prediction
# --dump-instr=yes permet d'enregistrer les instructions exécutées,
#                  indispensable pour comparer avec le code source
# --simulate-cache=yes ajoute les coûts liés au cache,
# --collect-jumps=yes ajoute les sauts dans le rapport.

callgrind_annotate \
--inclusive=yes \
--tree=both \
--auto=yes \
${CALLGRIND_OUT} $1
# --inclusive=yes \ # Add subfunction cost (default way)
# --tree=both \ # Interleave into the top level list of functions, information on the callers and the callees of each function.
# --auto=yes \ # get annotated source code for all relevant functions for which the source can be found.

kcachegrind --desktopfile $1 ${CALLGRIND_OUT}

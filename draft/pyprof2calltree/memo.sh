exit(0)


python3 -m cProfile  -o profile_data.pyprof example.py
# -m mod : run library module as a script (terminates option list)

pyprof2calltree -i profile_data.pyprof  # this converts the stats into a callgrind format



gprof2dot --format=callgrind --output=out.dot profile_data.pyprof.log
#Generate a dot graph from the output of several profilers.

dot -Tsvg out.dot -o graph.svg
# dot  draws  directed  graphs.  It works well on directed acyclic graphs and other graphs that can be drawn as hierarchies or have a natural ``flow.''
 # -Tsvg         - Set output format to 'svg'

# svg = vectorial image
inkscape graph.svg

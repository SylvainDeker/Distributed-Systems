import dask.array as da
from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler
from dask.diagnostics import visualize

a = da.random.random(size=(10000, 1000), chunks=(1000, 1000))
q, r = da.linalg.qr(a) # /!\ GIL
a2 = q.dot(r)

with Profiler() as prof,\
     ResourceProfiler(dt=0.25) as rprof,\
     CacheProfiler() as cprof:
        out = a2.compute()

visualize([prof, rprof, cprof])


# From these plots we can see that the initial tasks (calls to
#  numpy.random.random and numpy.linalg.qr for each chunk) are run
#  concurrently, but only use slightly more than 100% CPU. This is
#  because the call to numpy.linalg.qr currently doesn’t release
#  the GLOBAL INTERPRETER LOCK (GIL), so those calls can’t truly
#  be done in parallel. Next, there’s a reduction step where all
#  the blocks are combined. This requires all the results from the
#  first step to be held in memory, as shown by the increased number
#  of results in the cache, and increase in memory usage.
#
#  Immediately after this task ends, the number of elements in the
#  cache decreases, showing that they were only needed for this step.
#  Finally, there’s an interleaved set of calls to dot and sum.
#  Looking at the CPU plot, it shows that these run both concurrently
#  and in parallel, as the CPU percentage spikes up to around 350%.

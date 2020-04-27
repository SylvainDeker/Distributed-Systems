from dask.callbacks import Callback
from operator import add, mul
from dask import get


# Schedulers based on dask.local.get_async (currently dask.get,
# dask.threaded.get, and dask.multiprocessing.get) accept five
# callbacks, allowing for inspection of scheduler execution.


class PrintKeys(Callback):

    def _start(self,dsk):
        """
        Run at the beginning of execution, right before
        the state is initialized. Receives the Dask graph
        """
        print("Start")

    def _start_state(self,dsk,state):
        """
        Run at the beginning of execution, right after
        the state is initialized. Receives the Dask
        graph and scheduler state
        """
        print("start_state")

    def _pretask(self, key, dask, state):
        """
        Run every time a new task is started. Receives
        the key of the task to be run, the Dask graph,
        and the scheduler state
        """
        print("Computing: {0}!".format(repr(key)))

    def _posttask(self,key, result, dsk, state, id):
        """
        Run every time a task is finished. Receives the
        key of the task that just completed, the result,
        the Dask graph, the scheduler state,
        and the id of the worker that ran the task
        """
        print("_posttask")

    def _finish(self,dsk, state, errored):
        """
        Run at the end of execution, right before the result
        is returned. Receives the Dask graph, the scheduler
        state, and a boolean indicating whether
        or not the exit was due to an error
        """
        print("finish")


if __name__ == '__main__':

    dsk = {'a':(add,1,2),\
           'b':(add,5,'a'),\
           'c':(mul,'a','b')}

    with PrintKeys():
        get(dsk,'c')

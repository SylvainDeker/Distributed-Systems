import requests
import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
class Netdata:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def _get_data(self,chart,idx):
        url = "http://localhost:19999/api/v1/data?chart="+chart+"&after="+str(self.start_time)+"&before="+str(self.end_time)+"&points=5000&group=average&format=json&options=seconds&options=jsonwrap"
        r = requests.get(url)
        if r.status_code>=200 and r.status_code<300:
            data = r.json()['result']['data']
            data = np.array(data)
            return np.flip(data[:,idx:idx+1])
        return None

    def start(self):
        self.start_time = time.time()

    def stop(self,filename):
        self.stop_time = time.time()
        cpu0 = self._get_data('cpu.cpu0',6)
        cpu1 = self._get_data('cpu.cpu1',6)
        cpu2 = self._get_data('cpu.cpu2',6)
        cpu3 = self._get_data('cpu.cpu3',6)
        mem =  self._get_data('system.ram',2)
        t = np.arange(0,len(cpu0),1)

        fig, ax = plt.subplots(2,1)
        fig.tight_layout(pad=1.0)
        fig.set_size_inches((10,10))


        ax[0].plot(t, cpu0, label='cpu0')
        ax[0].plot(t, cpu1, label='cpu1')
        ax[0].plot(t, cpu2, label='cpu2')
        ax[0].plot(t, cpu3, label='cpu3')
        ax[1].plot(t, mem, label='RAM')
        ax[0].legend()
        ax[1].legend()

        ax[0].set(xlabel='Temps (Seconde)',
               ylabel='Usage %',
               title='Utilisation CPU')
        ax[1].set(xlabel='Temps (Seconde)',
               ylabel='Gio',
               title='Utilisation RAM')
        tmax = 200
        ax[0].set_ylim(bottom=0,top=100)
        ax[0].set_xlim(left=0,right=tmax)
        ax[1].set_ylim(bottom=0,top=8589.934592)
        ax[1].set_xlim(left=0,right=tmax)

        ax[0].grid()
        ax[1].grid()

        fig.savefig(filename)

# def get_data(start_time,end_time,chart,idx):
#     url = "http://localhost:19999/api/v1/data?chart="+chart+"&after="+str(start_time)+"&before="+str(end_time)+"&points=5000&group=average&format=json&options=seconds&options=jsonwrap"
#     print(url)
#     r = requests.get(url)
#     if r.status_code>=200 and r.status_code<300:
#         data = r.json()['result']['data']
#         data = np.array(data)
#         return np.flip(data[:,idx:idx+1])
#     return None


if __name__ == '__main__':
    nd = Netdata()
    nd.start()

    # time.sleep(5)
    # os.system("python3 dask_example.py")
    # time.sleep(5)
    # nd.stop('dask.png')


    nd.start()

    time.sleep(5)
    os.system("python3 spark_example.py")
    time.sleep(5)
    nd.stop('spark.png')

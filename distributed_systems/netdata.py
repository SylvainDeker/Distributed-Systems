import requests
import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt

def get_data(start_time,end_time,chart,idx):
    url = "http://localhost:19999/api/v1/data?chart="+chart+"&after="+str(start_time)+"&before="+str(end_time)+"&points=5000&group=average&format=json&options=seconds&options=jsonwrap"
    print(url)
    r = requests.get(url)
    if r.status_code>=200 and r.status_code<300:
        data = r.json()['result']['data']
        data = np.array(data)
        return np.flip(data[:,idx:idx+1])
    return None


if __name__ == '__main__':
    start_time = int(time.time())
    print(start_time)
    time.sleep(60)
    end_time = int(time.time())
    print(end_time)

    cpu0 = get_data(start_time,end_time,'cpu.cpu0',6)
    cpu1 = get_data(start_time,end_time,'cpu.cpu1',6)
    cpu2 = get_data(start_time,end_time,'cpu.cpu2',6)
    cpu3 = get_data(start_time,end_time,'cpu.cpu3',6)
    mem = get_data(start_time,end_time,'system.ram',2)

    t = np.arange(0,len(cpu0),1)

    fig, ax = plt.subplots(2,1)
    ax[0].plot(t, cpu0)
    ax[0].plot(t, cpu1)
    ax[0].plot(t, cpu2)
    ax[0].plot(t, cpu3)
    ax[1].plot(t, mem)

    ax[0].set(xlabel='Temps (Seconde)',
           ylabel='Usage %',
           title='Utilisation CPU')
    ax[0].set_ylim(bottom=0,top=100)
    ax[1].set_ylim(bottom=0,top=9000)

    ax[0].grid()
    ax[1].grid()

    # fig.savefig("test.png")
    plt.show()

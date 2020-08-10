import requests
import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt
if __name__ == '__main__':
    start_time = int(time.time())
    print(start_time)
    time.sleep(10)
    end_time = int(time.time())
    print(end_time)
    r = requests.get("http://192.168.0.16:19999/api/v1/data?chart=system.cpu&after="+str(start_time)+"&before="+str(end_time)+"&points=5000&group=average&format=json&options=seconds&options=jsonwrap")

    if r.status_code>=200 and r.status_code<300:
        data = r.json()['result']['data']
        data = np.array(data)
        print(data)
        # Data for plotting
        t = np.arange(0.0,len(data),1)
        s = data[:,6:7]

        fig, ax = plt.subplots()
        ax.plot(t, s)

        ax.set(xlabel='time (s)', ylabel='voltage (mV)',
               title='About as simple as it gets, folks')
        ax.grid()

        fig.savefig("test.png")
        # plt.show()

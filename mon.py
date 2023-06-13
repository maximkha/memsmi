import subprocess
import re
from time import sleep
import plotext as plt
from datetime import datetime
command = 'nvidia-smi'

NUM = 10

gpu_mems = None
times = []
colors = ["red", "magenta", "orange", "green", "cyan", "blue", "white", "red+"]

plt.theme("dark")

while True:
    plt.clt()
    plt.cld()

    p = subprocess.check_output(command).decode()
    ram_using = re.findall(r'(\d*)MiB\W*\/\W*(\d*)MiB', p)
    raw_gpu_mem = list(map(lambda pair: float(pair[0])/float(pair[1]), ram_using))
    if gpu_mems is None: gpu_mems = [[] for _ in range(len(raw_gpu_mem))]

    times.append(datetime.now().timestamp())

    times = times[-NUM:]

    for i, gpu_mem in enumerate(raw_gpu_mem):
        gpu_mems[i].append(gpu_mem)
        gpu_mems[i] = gpu_mems[i][-NUM:]

        plt.plot(times, gpu_mems[i], color=colors[i])
    plt.show()

    sleep(1)
import subprocess
import re
from time import sleep
import plotext as plt
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Monitor GPU stats')
parser.add_argument('--num', default=100, type=int, help='number of samples to display')
parser.add_argument('--util', default=False, action='store_true', help='display utilization rather than memory usage')
parser.add_argument('--smipath', default='nvidia-smi', action='store_true', help='path to smi executable')
args = parser.parse_args()

NUM = args.num
MODE = "util" if args.util else "mem"
SMI_EXE = args.smipath

gpu_stats = None
times = []
colors = ["red", "magenta", "orange", "green", "cyan", "blue", "white", "red+"]

plt.theme("dark")

while True:
    plt.clt()
    plt.cld()

    p = subprocess.check_output(SMI_EXE).decode()
    if MODE == "mem":
        ram_using = re.findall(r'(\d*)MiB\W*\/\W*(\d*)MiB', p)
        raw_stats = list(map(lambda pair: float(pair[0])/float(pair[1]), ram_using))
    elif MODE == "util":
        util = re.findall(r'(\d*)%\W*Default', p)
        raw_stats = list(map(lambda stat: float(stat)/100., util))
    else:
        print("invalid mode")
        exit()

    if gpu_stats is None: gpu_stats = [[] for _ in range(len(raw_stats))]

    times.append(datetime.now().timestamp())

    times = times[-NUM:]

    for i, gpu_stat in enumerate(raw_stats):
        gpu_stats[i].append(gpu_stat)
        gpu_stats[i] = gpu_stats[i][-NUM:]

        plt.plot(times, gpu_stats[i], color=colors[i])
    plt.show()

    sleep(1)

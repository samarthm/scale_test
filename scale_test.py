import itertools
import time
times = []
import parsl
from parsl import *
from parsl.config import Config
from parsl.executors.ipp import IPyParallelExecutor
from libsubmit.channels.ssh.ssh import SSHChannel
from libsubmit.providers.slurm.slurm import SlurmProvider
from libsubmit import *
import subprocess
import numpy as np
import numpy.ma as ma
from itertools import zip_longest
import ipyparallel

def mean(a):
    return sum(a) / len(a)

thefile = open('times500.txt', 'w')
myNum = 0
ticker = 0
myList = []
num_tasks = 1000
print("test")
bigger_list = []
for repeat in range(0, 3):
    subprocess.call("pkill -f ipcontroller", shell=True)
    for init_nodes_set in range(0, 10):

        init_workers = 2 ** init_nodes_set
        init_tasks = init_workers
        init_nodes = 1
        if repeat > 5:
            #init_tasks = 32
            init_nodes = 2 ** (init_nodes_set - 5)

        config = Config(
            executors=[
                IPyParallelExecutor(
                    provider=SlurmProvider(
                        'broadwl',
                        init_blocks=1,
                        min_blocks=1,
                        max_blocks=1,
                        nodes_per_block=1,
                        tasks_per_node=init_tasks,
                        parallelism=0.5,
                        overrides='module load Anaconda3/5.1.0; export PARSL_TESTING=True',
                        walltime= "06:00:00"
                    ),
                    label='midway_ipp'
                )
            ]
        )
        dfk = DataFlowKernel(config)


        @App('python', dfk)
        def sleeper(x):
            import time
            try:
                time.sleep(10)
            except Exception as e:
                print("error")

        client = dfk.executors['midway_ipp'].executor
        def test_stress():
            x = []
            x = [sleeper(i) for i in range(0, num_tasks)]
            start = time.time()
            for y in x:
                try:
                    y.result()
                except Exception as e:
                    print("error")
            end = time.time()
            times.append((end-start))  
            print('the time taken is: ' + str(end-start))
            dfk.cleanup()


        while int(len(client.ids)) != (init_tasks):
            time.sleep(5)
            print(len(client.ids))
            print(init_tasks)

        test_stress()



        print(times)   
        bigger_list.append(times)
        thefile.write(str(times) + "\n")


    #thefile.write(str(times) + "\n")

    subprocess.call("pkill -f ipcontroller", shell=True)
    subprocess.call("qstat -u $USER | awk '{print $1}' | grep -o [0-9]* | xargs qdel", shell=True)


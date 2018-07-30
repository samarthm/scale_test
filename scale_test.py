import time
from parsl.app.app import App
from parsl.config import Config
from parsl.executors.ipp import IPyParallelExecutor
from parsl.dataflow.dflow import DataFlowKernel
from libsubmit.providers.slurm.slurm import SlurmProvider
import subprocess

times = []
workers = []
blocks = []
num_tasks = 1000
tasks_per_node = 16

subprocess.call("pkill -f ipcontroller", shell=True)
subprocess.call("qstat -u $USER | awk '{print $1}' | grep -o [0-9]* | xargs qdel", shell=True)

config = Config(
    executors=[
        IPyParallelExecutor(
            provider=SlurmProvider(
                'broadwl',
                init_blocks=1,
                min_blocks=1,
                max_blocks=1000,
                nodes_per_block=1,
                tasks_per_node=tasks_per_node,
                overrides='module load Anaconda3/5.1.0; export PARSL_TESTING=True',
                walltime= "06:00:00"
            ),
            label='midway_ipp',
            managed=False
        )
    ]
)
dfk = DataFlowKernel(config)

num_blocks = 1
for _ in range(0, 100):

    @App('python', dfk)
    def sleeper(x):
        import time
        try:
            time.sleep(10)
        except Exception as e:
            print(e)

    client = dfk.executors['midway_ipp'].executor
    def test_stress():
        tasks = [sleeper(i) for i in range(0, num_tasks)]
        start = time.time()
        for x in tasks:
            try:
                x.result()
            except Exception as e:
                print(e)
        end = time.time()
        times.append((end-start))
        print('the time taken is: ' + str(end-start))

    test_stress()
    num_workers = len(client.ids)
    blocks.append(num_blocks)
    workers.append(num_workers)
    print('number of workers: {}'.format(num_workers))
    print('number of blocks requested: {}'.format(num_blocks))

    time.sleep(5)
    dfk.executors['midway_ipp'].scale_out(1)
    num_blocks += 1

    with open('times.txt', 'w') as f:
        f.write(str(times) + "\t" + str(workers) + "\t" + str(blocks) + "\n")

subprocess.call("pkill -f ipcontroller", shell=True)
subprocess.call("qstat -u $USER | awk '{print $1}' | grep -o [0-9]* | xargs qdel", shell=True)

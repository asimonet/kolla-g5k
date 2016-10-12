#! /usr/bin/env python

import time, datetime, signal
import os, sys
from subprocess import check_output
from time import sleep
import json
import tempfile

scenarios_file = sys.argv[1]
idle_time = sys.argv[2]
concurrency = sys.argv[3]
waiting = sys.argv[4]

benchmarks = {}

with open(scenarios, 'r') as f:
    scenarios = f.readlines()

for bench in scenarios:
    if bench.startswidth('#'):
        continue
    
    bench_name = os.path.basename(bench)
    benchmarks[bench_name] = {}
    output = None
    return_code = 0
    
    # wait before the benchmark
    benchmarks[bench_basename]['idle_start'] = int(time.time())
    time.sleep(idle_time)
    benchmarks[bench_basename]['run_start'] = int(time.time())
    
    try:
        # Run the benchmark
        output = check_output(['rally', 'task', 'start', bench])
    except CalledProcessError as e:
        output = e.output
        return_code = e.return_code
    
    # wait after the benchmark
    benchmarks[bench_basename]['run_end'] = int(time.time())
    time.sleep(idle_time)
    benchmarks[bench_basename]['idle_end'] = int(time.time())
    
    if return_code != 0:
        logger.error("Error while running benchmark")
        benchmarks[bench_basename]['error'] = ''

        if output is not None:
            # Try to find the reason
            lines = output.splitlines(True)
            for i in range(0, len(lines)):
                if 'Task config is invalid' in lines[i]:
                    benchmarks[bench_basename]['error'] += lines[i].strip()

                if 'Reason:' in lines[i]:
                    benchmarks[bench_basename]['error'] += lines[i+1].strip()

# Dump the results as json
with open('experiment.json', 'w') as f:
    f.write(json.dumps(benchmarks, indent=3)

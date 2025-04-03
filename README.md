# Cache Simulator in PyQt
This Cache Simulator was developed for the purposes of a course project for ECE 1110: Computer Organization and Architecture at the University of Pittsburgh's Swanson School of Engineering. This project was designed in Spring 2023.

## Overview
This project is a simulator to mimic the behavior of a highly parameterized and configurable cache. Input stream can be passed in to the cache in the form of read and write commands, and output will be displayed in the form of latency time, the status of the cache in each layer, and the hit/miss rate of each layer.

## How It Works
### UI
The UI consists of cache data, hit/miss rate, times, latencies, input stream, physical memory, and configurations. Users can toggle the configurations to their liking and pass in commands via the input stream. The other items will update as input streams are passed in.

### Model
The cache model is hierarchial, where data in the lower-level cache is required to also be in the higher-level cache, and set-associative, where multiple cache lines can be mapped to the same cache set. The cache will use least recently used (LRU) as a replacement policy. Memory access latency is 100 cycles following access to the last level cache.

### Configurables
- Number of cache layers
- Size of each cache layer in bytes
- Access latency of each cache layer in cycles
- Block size in bytes
- Set associativity of each cache layer
- Write policy
- Allocation policy

## How to Run
- You must have the PyQt5 package installed when running the application. This can be installed either in your local machine or in a virtual environment.
- In the terminal, run `python cache_simulator.py`. The UI comprising of the simulator will pop up, where you can see the items listed above.
- Once you pass in valid commands into the input stream (check `test_cases.txt` for examples), the simulator should update with more information.
- You can restart the simulator by rebooting the simulator using the same run command.

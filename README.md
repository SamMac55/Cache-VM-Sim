# Cache-VM-Sim
Caching and Virtual Memory Simulator for Computer Arch Course. 

## Goal
The goal of this project is to understand the internal operations of CPU caches and a simple virtual memory scheme. Simulate Virtual Memory and a Level 1 cache for a 32-bit CPU. Then analyze the results and do a performance comparison.

## How to get started
Prereqs: You have an IDE (VSCode will probably be best) and you have python installed on your machine.
1. Start by cloning the repo into a folder that you can work from  
```git clone https://github.com/SamMac55/Cache-VM-Sim.git```  
2. Once you've cloned the repo, verify that you can do something like this from the root of the repo:  
```python3 src/main.py OR python src/main.py```  
3. If necessary, create a virtual environment using either:  
```python -m venv .venv```   
  3a. Activate using either ```source .venv/bin/activate``` OR ```.\.venv\Scripts\Activate.ps1```

## Usage
```
usage: VMCacheSim.py [-h] -s {8,16,32,64,128,256,512,1024,2048,4096,8192} -b {8,16,32,64} -a {1,2,4,8,16} -r {rr,rnd} -p {128,256,512,1024,2048,4096} -u U -n N -f F

Cache/VM Simulator

options:
  -h, --help            show this help message and exit
  -s {8,16,32,64,128,256,512,1024,2048,4096,8192}
                        Cache size in KB
  -b {8,16,32,64}       Block size in bytes
  -a {1,2,4,8,16}       Associativity of the cache
  -r {rr,rnd}           Replacement policy - Round Robin or Random
  -p {128,256,512,1024,2048,4096}
                        Physical memory size in MB
  -u U                  Percentage of phyiscal memory used by the OS
  -n N                  Instructions/Time Slice
  -f F                  Trace file name
```

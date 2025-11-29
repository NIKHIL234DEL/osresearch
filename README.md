SysJitter: Micro-architectural Analysis of OS Noise

SysJitter is a low-level benchmarking project used to measure operating system noise and tail latency behaviour. It uses the CPU Time Stamp Counter through the __rdtscp intrinsic to record cycle-accurate timing instead of standard system timers.

This experiment measures the latency of the getpid system call under two conditions: when the system is idle and when the system is under heavy load. The objective is to observe how scheduler activity and context switching affect latency and response time.

Key results:
Average latency in idle condition was around 33 CPU cycles.
Average latency in load condition was around 35 CPU cycles.
The 99th percentile latency increased from 47 cycles to 82 cycles under load.
This proves that while average performance remains stable, tail latency increases drastically due to unexpected scheduling interruptions, showing the non-deterministic nature of modern operating systems.

Methodology:
One million iterations of getpid system call were measured.
Used __rdtscp for precise serialized cycle timing.
Graphs were generated using Python with pandas and matplotlib.

Why __rdtscp:
Reads timestamp counter directly from CPU.
Supports serialization to avoid out-of-order execution inaccuracies.
More precise than time.h and standard timing utilities.

How to build and run:
g++ -O3 sysjitter.cpp -o sysjitter
./sysjitter
python plot_results.py

Project files:
sysjitter.cpp - benchmarking code
plot_results.py - script to graph results
results.csv - collected measured output data

Future improvements:
Support benchmarking on Linux and macOS
Compare real-time and normal kernel behaviour
Measure effects of cache pollution and TLB shootdown
Add performance tracing support

# SimPy Tutorial

## Introduction

Welcome to the SimPy Tutorial! This repository provides a comprehensive guide to learning SimPy, a process-based discrete-event simulation framework for Python. Whether you're new to simulation or looking to enhance your skills, this tutorial will help you get started with SimPy.

## Installation

To use SimPy, you need to have Python installed on your machine. You can install SimPy using pip:

```bash
pip install simpy
```
## Getting Started
### Basic Usage
Creating a Simple Simulation
Here's a basic example to help you get started with SimPy:
```bash
import simpy

def my_process(env):
    print('Process started at', env.now)
    yield env.timeout(5)
    print('Process finished at', env.now)

env = simpy.Environment()
env.process(my_process(env))
env.run()
```


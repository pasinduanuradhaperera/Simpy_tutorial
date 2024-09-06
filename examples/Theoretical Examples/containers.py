import simpy

def producer(env, container):
    while True:
        yield env.timeout(1)
        print(f'Producing 10 units at {env.now}')
        yield container.put(10)

def consumer(env, container):
    while True:
        yield env.timeout(2)
        print(f'Consuming 5 units at {env.now}')
        yield container.get(5)

env = simpy.Environment()
container = simpy.Container(env, capacity=50, init=20)

env.process(producer(env, container))
env.process(consumer(env, container))

env.run(until=10)

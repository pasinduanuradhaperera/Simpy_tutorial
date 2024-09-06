import simpy

def worker(env, name, resource1, resource2):
    print(f'{name} arriving at {env.now}')
    
    # Request multiple resources
    with resource1.request() as req1, resource2.request() as req2:
        yield req1 & req2  # Wait until both resources are available
        print(f'{name} started using both resources at {env.now}')
        yield env.timeout(3)
        print(f'{name} finished at {env.now}')

env = simpy.Environment()
resource1 = simpy.Resource(env, capacity=1)
resource2 = simpy.Resource(env, capacity=1)

# Create workers
for i in range(1,10):
    env.process(worker(env, f'Worker {i}', resource1, resource2))

env.run()

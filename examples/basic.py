import simpy

def process(name, env, resource):
    print(f'{name} arriving at {env.now}')
    with resource.request() as request:
        yield request
        print(f'{name} started at {env.now}')
        yield env.timeout(3)  # Simulates some processing time
        print(f'{name} finished at {env.now}')

# Create the environment
env = simpy.Environment()

# Create a shared resource with a capacity of 1
resource = simpy.Resource(env, capacity=1)

# Create processes
env.process(process('Process 1', env, resource))
env.process(process('Process 2', env, resource))

# Run the simulation
env.run()

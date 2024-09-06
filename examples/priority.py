import simpy

def process(name, env, resource, priority):
    print(f'{name} arriving at {env.now}')
    
    with resource.request(priority = priority) as request:
        yield request
        print(f'{name} started at {env.now} with priority {priority}')
        yield env.timeout(2)
        print(f'{name} finished at {env.now}')

env = simpy.Environment()
resource = simpy.PriorityResource(env, capacity=1)

# Create processes with different priorities (lower value means higher priority)
env.process(process('Process 1', env, resource, priority=2))
env.process(process('Process 2', env, resource, priority=1))
env.process(process('Process 3', env, resource, priority=3))

env.run()
 
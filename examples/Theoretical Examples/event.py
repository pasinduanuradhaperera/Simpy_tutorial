import simpy

def event_process(env):
    print(f'Event starts at {env.now}')
    
    # Schedule an event in the future
    yield env.timeout(5)
    print(f'Event ends at {env.now}')

env = simpy.Environment()
env.process(event_process(env))
env.run()

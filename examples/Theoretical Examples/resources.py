import simpy

def car(env, name, charging_station):
    print(f'{name} arriving at {env.now}')
    
    with charging_station.request() as request:
        yield request
        print(f'{name} starting to charge at {env.now}')
        
        # Simulate charging time
        yield env.timeout(2)
        print(f'{name} leaving the charging station at {env.now}')

env = simpy.Environment()
charging_station = simpy.Resource(env, capacity=2)

# Create multiple cars
for i in range(4):
    env.process(car(env, f'Car {i}', charging_station))

env.run()

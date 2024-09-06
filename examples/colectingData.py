import simpy

def car(env, name, charging_station, wait_times):
    arrival_time = env.now
    print(f'{name} arriving at {env.now}')
    
    with charging_station.request() as request:
        yield request
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)  # Collect wait time
        print(f'{name} started charging after waiting {wait_time} units')
        yield env.timeout(2)
        print(f'{name} finished at {env.now}')

env = simpy.Environment()
charging_station = simpy.Resource(env, capacity=2)
wait_times = []

for i in range(5):
    env.process(car(env, f'Car {i}', charging_station, wait_times))

env.run()

# Calculate and display statistics
average_wait_time = sum(wait_times) / len(wait_times)
print(f'Average wait time: {average_wait_time} units')

import simpy
import argparse
import pandas as pd
import os

# additionally install argparse, pandas 
# pip install argparse pandas
# or
# pip3 install argparse pandas


def main():
    # Taking user inputs for parameters
    parser = argparse.ArgumentParser(description="This is a program that describes a simple coffee shop simulation")
    parser.add_argument("num_of_customers", default=2, nargs='?', type=int, help="Enter the number of customers")
    parser.add_argument("num_of_cashiers", type=int, default=2, nargs='?', help="Enter the number of cashiers available")
    parser.add_argument("num_of_barista_stations", type=int, default=2, nargs='?', help="Enter the number of barista stations available")
    parser.add_argument("num_of_cleaning_stations", type=int, default=2, nargs='?', help="Enter the number of cleaning stations available")

    args = parser.parse_args()

    wait_times = []  # List to store wait times

    # Create the SimPy environment
    env = simpy.Environment()

    # Create resources
    resources = {
        'cashiers': simpy.Resource(env, capacity=args.num_of_cashiers),
        'barista_stations': simpy.Resource(env, capacity=args.num_of_barista_stations),
        'cleaning_stations': simpy.Resource(env, capacity=args.num_of_cleaning_stations)
    }

    # Start the simulation
    for i in range(1, args.num_of_customers + 1):
        env.process(coffeeshop(f'Customer_{i}', env, resources, wait_times))
    
    env.run()

    # Calculate average wait time
    if wait_times:
        average_wait_time = sum(wait_times) / len(wait_times)
    else:
        average_wait_time = 0

    # Print wait times and average wait time
    print(f'Wait times: {wait_times}')
    print(f'Average wait time: {average_wait_time:.2f} mins')

    # Prepare new data for appending
    new_data = pd.DataFrame({
        'Customer': [f'Customer_{i}' for i in range(1, args.num_of_customers + 1)],
        'Wait Time (mins)': wait_times
    })

    # File path
    file_path = 'wait_times.csv'

    if os.path.exists(file_path):
        # Append to existing file
        existing_data = pd.read_csv(file_path)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        # Create new file
        combined_data = new_data

    # Save the combined data to the CSV file
    combined_data.to_csv(file_path, index=False)
    print('Wait times have been appended to wait_times.csv')

def coffeeshop(customer, env, resources, wait_times):
    print(f'{customer} arriving at {env.now}')
    arrival_time = env.now

    # Example of using resources
    with resources['cashiers'].request() as request:
        yield request

        wait_time = env.now - arrival_time
        wait_times.append(wait_time)

        print(f'{customer} being served by cashier at {env.now}')
        yield env.timeout(5)  # Simulate time spent with cashier

    with resources['barista_stations'].request() as request:
        yield request
        print(f'{customer} getting coffee at {env.now}')
        yield env.timeout(5)  # Simulate time spent at barista station

    with resources['cleaning_stations'].request() as request:
        yield request
        print(f'{customer} using cleaning station at {env.now}')
        yield env.timeout(3)  # Simulate time spent at cleaning station

if __name__ == "__main__":
    main()

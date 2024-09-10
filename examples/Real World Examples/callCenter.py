import random
import simpy
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(description="This is a program that describes a simple coffee shop simulation")
    parser.add_argument("num_of_employees", default=2, nargs='?', type=int, help="Enter the number of customers")
    parser.add_argument("support_time", type=int, default=5, nargs='?', help="Enter the number of cashiers available")
    parser.add_argument("customer_interval", type=int, default=2, nargs='?', help="Enter the number of barista stations available")
    parser.add_argument("sim_time", type=int, default=120, nargs='?', help="Enter the number of barista stations available")
    
    args = parser.parse_args()

    global customers_handled
    customers_handled = 0

    def customer(env, name, call_center):
        global customers_handled
        print(f'Customer{name} enters waiting queue at {env.now:.2f}')
        with call_center.staff.request() as request:
            yield request
            print(f'Customer {name} left call at {env.now:.2f}')
            customers_handled += 1

    def setup(env, num_employees, support_time, customer_interval):
        call_center = CallCenter(env, num_employees, support_time)

        for i in range(1,6):
            env.process(customer(env, i, call_center))

        while True:
            yield env.timeout(random.randint(customer_interval - 1, customer_interval))
            i += 1
            env.process(customer(env, i, call_center))


    print("Starting Call Center Simulation !!!")
    env = simpy.Environment()
    env.process(setup(env,args.num_of_employees,args.support_time, args.customer_interval))

    env.run(until=args.sim_time)

    print("Customer Handled: " + str(customers_handled))

class CallCenter:
    def __init__(self, env, num_employees, support_time):
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.support_time = support_time

    def support(self, customer):
       random_time = max(1, np.random.normal(self.support_time))
       yield self.env.timeout(random_time)
       print(f'Support finished for {customer} at {self.env.now:.2f}')


if __name__ == "__main__":
    main()
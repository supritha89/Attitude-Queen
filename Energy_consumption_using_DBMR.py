import random
import pandas as pd
import matplotlib.pyplot as plt

def csma_ca_backoff(n, slot_time):
    """Calculate the backoff time for CSMA/CA.

    n: the current retry count
    slot_time: the fixed time duration for which the medium is sensed to be idle
    returns: the backoff time in milliseconds
    """
    # Contention window size (m) based on the number of retransmissions (n)
    m = 5  # Adjust this value based on your specific scenario

    # Calculate the backoff time using the given formula
    random_integer = random.randint(0, (2**m - 1))
    backoff_time = random_integer * slot_time

    return backoff_time

# Prompt the user for the number of test cases and the maximum number of nodes
num_test_cases = int(input("Enter the number of test cases: "))
max_nodes = int(input("Enter the maximum number of nodes: "))

# Fixed slot time in milliseconds
slot_time = 10  # Adjust this value based on your specific scenario

# Calculate the average backoff time and energy consumed for each number of nodes and store the results in a DataFrame
results = pd.DataFrame(columns=['Number of Nodes', 'Energy (Old)', 'Energy (New)'])
for num_nodes in range(1, max_nodes+1):
    total_energy_old = 0
    total_energy_new = 0
    for test_case in range(num_test_cases):
        backoff_times_old = []
        backoff_times_new = []
        for i in range(num_nodes):
            backoff_time_old = csma_ca_backoff(i, slot_time)
            backoff_times_old.append(backoff_time_old)
            if i == 0:
                backoff_time_new = backoff_time_old
            else:
                backoff_time_new = backoff_time_old * (i+10) / (i+5)
            backoff_times_new.append(backoff_time_new)
        total_energy_old += sum(backoff_times_old)
        total_energy_new += sum(backoff_times_new)
    avg_energy_old = total_energy_old / num_test_cases
    avg_energy_new = total_energy_new / num_test_cases
    results = results.append({
        'Number of Nodes': num_nodes,
        'Energy (Old)': avg_energy_old,
        'Energy (New)': avg_energy_new
    }, ignore_index=True)

# Calculate the average of the two algorithms
results['Average Energy'] = (results['Energy (Old)'] + results['Energy (New)']) / 2

# Plot the energy consumption for the old and new algorithms as well as the average
plt.plot(results['Number of Nodes'], results['Energy (Old)'], 'b-', label='New Algorithm')
plt.plot(results['Number of Nodes'], results['Energy (New)'], 'r-', label='Old Algorithm')
plt.plot(results['Number of Nodes'], results['Average Energy'], 'g--', label='Average')
plt.xlabel('Number of Nodes')
plt.ylabel('Relative Energy Consumption')
plt.title('Energy Consumption Comparison')
plt.legend()
plt.grid()
plt.show()

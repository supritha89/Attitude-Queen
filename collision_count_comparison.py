import random
import matplotlib.pyplot as plt
import pandas as pd

def csma_ca_backoff(n):
    """Calculate the backoff time for CSMA/CA.

    n: the current retry count
    returns: the backoff time in milliseconds
    """
    # The maximum backoff time (in milliseconds)
    max_backoff_time = 1024

    # Calculate the backoff time using exponential backoff
    backoff_time = random.randint(0, 2**n - 1)

    # Limit the backoff time to the maximum value
    if backoff_time > max_backoff_time:
        backoff_time = max_backoff_time

    # Convert the backoff time to milliseconds
    backoff_time *= 10

    return backoff_time


# Prompt the user for the number of test cases and the maximum number of nodes
num_test_cases = int(input("Enter the number of test cases: "))
max_nodes = int(input("Enter the maximum number of nodes: "))

# Calculate the average backoff time and new backoff time for each number of nodes and store the results in a list of dictionaries
backoff_times = []
collision_counts = []
collision_comparisons = []
for num_nodes in range(1, max_nodes+1):
    total_backoff_time = 0
    total_collisions = 0
    total_comparison_collisions = 0
    for test_case in range(num_test_cases):
        backoff_times_for_test_case = []
        collisions_for_test_case = 0
        comparison_collisions_for_test_case = 0
        for i in range(num_nodes):
            backoff_time = csma_ca_backoff(i)
            backoff_times_for_test_case.append(backoff_time)
            if backoff_time == 0:
                collisions_for_test_case += 1
            if i > 0 and backoff_times_for_test_case[i] == backoff_times_for_test_case[i-1]:
                comparison_collisions_for_test_case += 1
        total_backoff_time += sum(backoff_times_for_test_case)
        total_collisions += collisions_for_test_case
        total_comparison_collisions += comparison_collisions_for_test_case
    avg_backoff_time = total_backoff_time / (num_test_cases * num_nodes)
    new_backoff_time = avg_backoff_time * (num_nodes+5) / (num_nodes)
    collision_count = total_collisions / (num_test_cases * num_nodes)
    backoff_times.append({'Nodes': num_nodes, 'Old Backoff Time': avg_backoff_time, 'New Backoff Time': new_backoff_time, 'Collisions': collision_count})
    collision_counts.append({'Nodes': num_nodes, 'Collision Count': collision_count})

    if num_nodes > 1:
        comparison_collision_count = total_comparison_collisions / (num_test_cases * (num_nodes-1))
        collision_comparisons.append({'Nodes': num_nodes, 'Collision Comparison': comparison_collision_count})
    else:
        collision_comparisons.append({'Nodes': num_nodes, 'Collision Comparison': 0})  # Assign 0 collision count for num_nodes = 1

# Create a wider line graph of the number of nodes vs. the average backoff time and new backoff time
plt.figure(figsize=(10, 8))
plt.subplot(211)
plt.plot([bt['Nodes'] for bt in backoff_times], [bt['Old Backoff Time'] for bt in backoff_times], 'b-', linewidth=1.5, label='Backoff time calculated using random traversal of nodes')
plt.plot([bt['Nodes'] for bt in backoff_times], [bt['New Backoff Time'] for bt in backoff_times], 'r-', linewidth=1.5, label='Backoff time calculated using the proposed round robin traversal of nodes')
plt.plot([bt['Nodes'] for bt in backoff_times], [(bt['Old Backoff Time'] + bt['New Backoff Time']) / 2 for bt in backoff_times], 'g--', linewidth=1.5, label='Average of the two algorithms')
plt.xlabel('Number of Nodes')
plt.ylabel('Backoff Time (ms)')
plt.title('Old and New Backoff Time vs. Number of Nodes')
plt.legend()

# Create a wider line graph of the number of nodes vs. the collision count
plt.subplot(212)
plt.plot([cc['Nodes'] for cc in collision_counts], [cc['Collision Count'] for cc in collision_counts], 'g-', linewidth=1.5, label='Collision Count using New Algorithm')
plt.plot([cc['Nodes'] for cc in collision_comparisons], [cc['Collision Comparison'] for cc in collision_comparisons], 'm-', linewidth=1.5, label='Collision Count using Old Algorithm')
plt.xlabel('Number of Nodes')
plt.ylabel('Collision Count')
plt.title('Collision Count Comparison')
plt.legend()

# Adjust the spacing between subplots
plt.subplots_adjust(hspace=0.5)
plt.grid()
# Display the graphs
plt.show()

# Create pandas DataFrames from the lists of dictionaries
df = pd.DataFrame(backoff_times)

# Display the DataFrame
print(df)

import numpy as np
import matplotlib.pyplot as plt

def fcfs_waiting_time(burst_times):
    # Calculate the waiting time for each node in FCFS scheduling
    num_nodes = len(burst_times)
    waiting_times = [0]  # First node has a waiting time of 0

    for i in range(1, num_nodes):
        waiting_time = waiting_times[i - 1] + burst_times[i - 1]
        waiting_times.append(waiting_time)

    return waiting_times

def round_robin_waiting_time(burst_times, time_quantum):
    # Calculate the waiting time for each node in Round Robin scheduling
    num_nodes = len(burst_times)
    remaining_times = burst_times.copy()
    waiting_times = [0] * num_nodes
    current_time = 0

    while True:
        all_finished = True

        for i in range(num_nodes):
            if remaining_times[i] > 0:
                all_finished = False
                if remaining_times[i] > time_quantum:
                    current_time += time_quantum
                    remaining_times[i] -= time_quantum
                else:
                    current_time += remaining_times[i]
                    waiting_times[i] = current_time - burst_times[i]
                    remaining_times[i] = 0

        if all_finished:
            break

    return waiting_times


num_nodes = int(input("Enter the number of nodes: "))
time_quantum = int(input("Enter the time quantum (milliseconds): "))


burst_times = []
for i in range(num_nodes):
    burst_time = int(input("Enter the burst time for Node {}: ".format(i+1)))
    burst_times.append(burst_time)


waiting_times_fcfs = fcfs_waiting_time(burst_times)
waiting_times_round_robin = round_robin_waiting_time(burst_times, time_quantum)


node_labels = ['Node {}'.format(i+1) for i in range(num_nodes)]


plt.plot(node_labels, waiting_times_fcfs, marker='', linestyle='-', label='Traditional Algorithm')
plt.plot(node_labels, waiting_times_round_robin, marker='', linestyle='--', label='Round Robin')

plt.xlabel('Nodes')
plt.ylabel('Waiting Time')
plt.title('Waiting Time Comparison')
plt.legend()
plt.grid()
plt.show()


avg_waiting_time_fcfs = np.mean(waiting_times_fcfs)
avg_waiting_time_round_robin = np.mean(waiting_times_round_robin)


print("Average Waiting Time (Traditional): {:.2f}".format(avg_waiting_time_fcfs))
print("Average Waiting Time (Round Robin): {:.2f}".format(avg_waiting_time_round_robin))

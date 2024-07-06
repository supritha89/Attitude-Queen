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

# Function to calculate throughput based on the provided formula
def calculate_throughput(burst_times, waiting_times):
    data_packet_size = 100  # Specifying the data packet size in bytes
    sifs = 1  
    ack_transmission_time = 2  # Specifying the ACK transmission time in milliseconds

    channel_busy_time = sum(burst_times) + np.mean(waiting_times)

    throughput = data_packet_size / (channel_busy_time + sifs + ack_transmission_time)

    return throughput


num_nodes = int(input("Enter the number of nodes: "))
time_quantum = int(input("Enter the time quantum (milliseconds): "))


burst_times = []
for i in range(num_nodes):
    burst_time = int(input("Enter the burst time for Node {}: ".format(i+1)))
    burst_times.append(burst_time)


waiting_times_fcfs = fcfs_waiting_time(burst_times)
waiting_times_round_robin = round_robin_waiting_time(burst_times, time_quantum)


throughput_fcfs = calculate_throughput(burst_times, waiting_times_fcfs)
throughput_round_robin = calculate_throughput(burst_times, waiting_times_round_robin)


labels = ['Traditional Traversal', 'Round Robin Traversal']
throughput = [throughput_fcfs, throughput_round_robin]

plt.bar(labels, throughput, color=['#050234', '#E310BD'])
plt.xlabel('Traversal Algorithm')
plt.ylabel('Throughput')
plt.title('Throughput Comparison')
plt.show()

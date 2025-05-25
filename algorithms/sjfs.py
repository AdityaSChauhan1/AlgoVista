# scheduling_algorithms/sjfs.py

from .utils import (
    update_gantt_chart,     # Function to update the Gantt chart
    add_to_process_table,   # Function to add process details to the process table
    compute_stats,          # Function to compute overall stats like avg TAT, WT, RT
    calculate_metrics       # Function to calculate CT, TAT, WT, RT for a process
)

# Helper function to sort processes by arrival time
def sort_arrival_time(process):
    return process["arrival_time"]

# Function to run Shortest Job First (SJF) Scheduling - Non-Preemptive
def run_sjfs(processes):
    # Sort processes by arrival time
    processes.sort(key=sort_arrival_time)

    current_time = 0              # Keeps track of the current time in the schedule
    length = len(processes)       # Total number of processes
    completed = 0                 # Number of completed processes
    visited = [False] * length    # Tracks whether a process has been scheduled

    gantt_chart = []              # Stores Gantt chart entries
    process_table = []            # Stores process execution details

    total_tat = total_wt = total_rt = 0  # Totals for Turnaround Time, Waiting Time, and Response Time
    total_idle_time = 0                  # Total idle time in the schedule

    # Main loop until all processes are completed
    while completed < length:
        idx = -1              # Index of the next process to schedule
        min_bt = float('inf') # Minimum burst time initialized to infinity

        # Find the shortest job among the arrived and unvisited processes
        for i in range(length):
            p = processes[i]
            if (not visited[i]) and (p["arrival_time"] <= current_time):
                if p["burst_time"] < min_bt:
                    min_bt = p["burst_time"]
                    idx = i
                elif p["burst_time"] == min_bt:
                    # If burst time is same, prefer earlier arrival time
                    if p["arrival_time"] < processes[idx]["arrival_time"]:
                        idx = i

        if idx == -1:  # No process has arrived yet, system is idle
            update_gantt_chart(gantt_chart, "Idle", current_time, current_time + 1)
            total_idle_time += 1
            current_time += 1
            continue

        # Get the selected process details
        p = processes[idx]
        p_name = p["name"]
        p_at = p["arrival_time"]
        p_bt = p["burst_time"]

        start_time = current_time
        completion_time = start_time + p_bt

        # Calculate Completion Time, Turnaround Time, Waiting Time, and Response Time
        completion_time, tat, wt, rt = calculate_metrics(p, start_time, p_bt)

        # Update Gantt Chart with this process's execution
        update_gantt_chart(gantt_chart, p_name, start_time, completion_time)

        # Add the process's execution details to the process table
        add_to_process_table(process_table, p, start_time, completion_time, tat, wt, rt)

        # Update totals for final stats calculation
        total_tat += tat
        total_wt += wt
        total_rt += rt
        current_time = completion_time      # Move current time forward
        visited[idx] = True                 # Mark process as completed
        completed += 1                      # Increment completed process count

    # Compute final statistics (avg TAT, avg WT, avg RT, etc.)
    stats = compute_stats(length, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    # Return Gantt chart, process table sorted by process name, and statistics
    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats

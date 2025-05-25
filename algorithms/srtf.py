# scheduling_algorithms/srtf.py

from .utils import (
    update_gantt_chart,
    add_to_process_table,
    compute_stats
)

def sort_arrival_time(process):
    return process["arrival_time"]

def run_srtf(processes):
    n = len(processes)
    processes.sort(key=sort_arrival_time)

    remaining_bt = [p["burst_time"] for p in processes]
    is_completed = [False] * n
    start_times = [None] * n

    current_time = 0
    completed = 0
    last_process = None
    total_idle_time = 0
    gantt_chart = []
    process_table = []
    total_tat = total_wt = total_rt = 0

    while completed != n:
        idx = -1
        min_remaining_time = float("inf")

        # Find the process with the shortest remaining time
        for i in range(n):
            if processes[i]["arrival_time"] <= current_time and not is_completed[i]:
                if remaining_bt[i] < min_remaining_time and remaining_bt[i] > 0:
                    min_remaining_time = remaining_bt[i]
                    idx = i

        if idx == -1:  # No process is ready to execute, idle time
            update_gantt_chart(gantt_chart, "Idle", current_time, current_time + 1)
            total_idle_time += 1
            current_time += 1
            continue

        # Process is ready, execute it
        if start_times[idx] is None:
            start_times[idx] = current_time

        if last_process != processes[idx]["name"]:
            update_gantt_chart(gantt_chart, processes[idx]["name"], current_time, current_time + 1)
        else:
            gantt_chart[-1]["end"] += 1

        last_process = processes[idx]["name"]
        remaining_bt[idx] -= 1
        current_time += 1

        # If the process is completed
        if remaining_bt[idx] == 0:
            is_completed[idx] = True
            completed += 1

            # Calculate Completion Time, TAT, WT, RT 
            completion_time = current_time
            tat = completion_time - processes[idx]["arrival_time"]
            wt = tat - processes[idx]["burst_time"]
            rt = start_times[idx] - processes[idx]["arrival_time"]

        
            add_to_process_table(process_table, processes[idx], start_times[idx], completion_time, tat, wt, rt)

            total_tat += tat
            total_wt += wt
            total_rt += rt

    # Compute the statistics
    stats = compute_stats(n, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats

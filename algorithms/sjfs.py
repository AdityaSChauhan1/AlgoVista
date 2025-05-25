# scheduling_algorithms/sjfs.py

from .utils import (
    update_gantt_chart,
    add_to_process_table,
    compute_stats,
    calculate_metrics
)

def sort_arrival_time(process):
    return process["arrival_time"]

def run_sjfs(processes):
    processes.sort(key=sort_arrival_time)

    current_time = 0
    length = len(processes)
    completed = 0
    visited = [False] * length

    gantt_chart = []
    process_table = []

    total_tat = total_wt = total_rt = 0
    total_idle_time = 0

    while completed < length:
        idx = -1
        min_bt = float('inf')

        for i in range(length):
            p = processes[i]
            if (not visited[i]) and (p["arrival_time"] <= current_time):
                if p["burst_time"] < min_bt:
                    min_bt = p["burst_time"]
                    idx = i
                elif p["burst_time"] == min_bt:
                    if p["arrival_time"] < processes[idx]["arrival_time"]:
                        idx = i

        if idx == -1:  # No process is ready to execute, idle time
            update_gantt_chart(gantt_chart, "Idle", current_time, current_time + 1)
            total_idle_time += 1
            current_time += 1
            continue

        p = processes[idx]
        p_name = p["name"]
        p_at = p["arrival_time"]
        p_bt = p["burst_time"]

        start_time = current_time
        completion_time = start_time + p_bt
        
        # calculate TAT, WT, RT
        completion_time, tat, wt, rt = calculate_metrics(p, start_time, p_bt)

        # Update Gantt Chart and Process Table
        update_gantt_chart(gantt_chart, p_name, start_time, completion_time)
        add_to_process_table(process_table, p, start_time, completion_time, tat, wt, rt)

        total_tat += tat
        total_wt += wt
        total_rt += rt
        current_time = completion_time
        visited[idx] = True
        completed += 1

    # Compute the statistics
    stats = compute_stats(length, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats

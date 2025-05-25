# Priority NP

#Lower number = higher priority(1 is the highest)
from .utils import (
    update_gantt_chart,
    add_to_process_table,
    compute_stats
)

def sort_arrival_time(process):
    return process["arrival_time"]

def run_priority_np(processes):
    processes.sort(key=sort_arrival_time)
    n = len(processes)
    current_time = 0
    completed = 0
    visited = [False] * n

    gantt_chart = []
    process_table = []

    total_idle_time = 0
    total_tat = total_wt = total_rt = 0

    while completed < n:
        idx = -1
        highest_priority = float('inf')

        for i in range(n):
            p = processes[i]
            if not visited[i] and p["arrival_time"] <= current_time:
                if p["priority"] < highest_priority:
                    highest_priority = p["priority"]
                    idx = i
                elif p["priority"] == highest_priority:
                    if p["arrival_time"] < processes[idx]["arrival_time"]:
                        idx = i

        if idx == -1:
            current_time += 1
            total_idle_time += 1
            continue

        process = processes[idx]
        p_name = process["name"]
        p_at = process["arrival_time"]
        p_bt = process["burst_time"]

        start_time = current_time
        completion_time = start_time + p_bt
        tat = completion_time - p_at
        wt = tat - p_bt
        rt = start_time - p_at

        update_gantt_chart(gantt_chart, p_name, start_time, completion_time)
        add_to_process_table(process_table, process, start_time, completion_time, tat, wt, rt)

        total_tat += tat
        total_wt += wt
        total_rt += rt
        current_time = completion_time
        visited[idx] = True
        completed += 1

    stats = compute_stats(n, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats

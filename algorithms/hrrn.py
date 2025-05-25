# scheduling_algorithms/hrrn.py

from .utils import (
    update_gantt_chart,
    add_to_process_table,
    compute_stats,
    calculate_metrics
)

def sort_arrival_time(process):
    return process["arrival_time"]

def run_hrrn(processes):
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
        max_response_ratio = -1

        for i in range(length):
            p = processes[i]
            if not visited[i] and p["arrival_time"] <= current_time:
                waiting_time = current_time - p["arrival_time"]
                response_ratio = (waiting_time + p["burst_time"]) / p["burst_time"]

                if response_ratio > max_response_ratio:
                    max_response_ratio = response_ratio
                    idx = i
                elif response_ratio == max_response_ratio:
                    if p["arrival_time"] < processes[idx]["arrival_time"]:
                        idx = i

        if idx == -1:
            update_gantt_chart(gantt_chart, "Idle", current_time, current_time + 1)
            current_time += 1
            total_idle_time += 1
            continue

        # Schedule the selected process
        p = processes[idx]
        start_time = current_time
        completion_time = start_time + p["burst_time"]

        # Use calculate_metrics utility function
        completion_time, tat, wt, rt = calculate_metrics(p, start_time, p["burst_time"])

        update_gantt_chart(gantt_chart, p["name"], start_time, completion_time)
        add_to_process_table(process_table, p, start_time, completion_time, tat, wt, rt)

        total_tat += tat
        total_wt += wt
        total_rt += rt
        current_time = completion_time
        visited[idx] = True
        completed += 1

    stats = compute_stats(length, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats

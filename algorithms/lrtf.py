from .utils import (
    update_gantt_chart,
    add_to_process_table,
    compute_stats
)

def sort_arrival_time(process):
    return process["arrival_time"]

def run_lrtf(processes):
    n = len(processes)
    processes.sort(key=sort_arrival_time)

    remaining_bt = [p["burst_time"] for p in processes]
    is_completed = [False] * n
    start_times = [None] * n
    completion_times = [0] * n

    current_time = 0
    completed = 0
    total_idle_time = 0
    last_process_name = None

    gantt_chart = []
    process_table = []
    total_tat = total_wt = total_rt = 0

    while completed < n:
        idx = -1
        max_remaining_bt = -1

        for i in range(n):
            if processes[i]["arrival_time"] <= current_time and not is_completed[i]:
                if remaining_bt[i] > max_remaining_bt:
                    max_remaining_bt = remaining_bt[i]
                    idx = i
                elif remaining_bt[i] == max_remaining_bt:
                    if processes[i]["arrival_time"] < processes[idx]["arrival_time"]:
                        idx = i

        if idx == -1:  # No process is ready to execute
            update_gantt_chart(gantt_chart, "Idle", current_time, current_time + 1)
            total_idle_time += 1
            current_time += 1
            last_process_name = "Idle"
            continue

        # Start time of the process if not already set
        if start_times[idx] is None:
            start_times[idx] = current_time

        update_gantt_chart(gantt_chart, processes[idx]["name"], current_time, current_time + 1)
        remaining_bt[idx] -= 1
        current_time += 1

        if remaining_bt[idx] == 0:  # process finishes
            is_completed[idx] = True
            completed += 1
            completion_times[idx] = current_time

            # Calculate TAT, WT, and RT for this process
            tat = completion_times[idx] - processes[idx]["arrival_time"]
            wt = tat - processes[idx]["burst_time"]
            rt = start_times[idx] - processes[idx]["arrival_time"]

            add_to_process_table(
                process_table,
                processes[idx],
                start_times[idx],
                completion_times[idx],
                tat,
                wt,
                rt
            )

            total_tat += tat
            total_wt += wt
            total_rt += rt

    # Compute stats after all processes are completed
    stats = compute_stats(n, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats

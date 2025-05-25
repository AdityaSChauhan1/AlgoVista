# Priority P


#lowest number -> Highest priority
from .utils import calculate_metrics, update_gantt_chart, add_to_process_table, compute_stats

def run_priority_p(processes):
    n = len(processes)
    
    # Sort processes by arrival time
    processes.sort(key=lambda p: p["arrival_time"])

    remaining_bt = [p["burst_time"] for p in processes]
    is_completed = [False] * n
    current_time = 0
    completed = 0

    gantt_chart = []
    process_table = []
    total_tat = total_wt = total_rt = total_idle_time = 0

    last_process = None
    start_times = [None] * n

    while completed != n:
        idx = -1
        highest_priority = float("inf")

        # Select the process with the highest priority that has arrived
        for i in range(n):
            if processes[i]["arrival_time"] <= current_time and not is_completed[i]:
                if processes[i]["priority"] < highest_priority:
                    highest_priority = processes[i]["priority"]
                    idx = i
                elif processes[i]["priority"] == highest_priority:
                    if processes[i]["arrival_time"] < processes[idx]["arrival_time"]:
                        idx = i

        if idx == -1:
            current_time += 1
            total_idle_time += 1
            continue

        # First time the process gets CPU
        if start_times[idx] is None:
            start_times[idx] = current_time

        # Update Gantt chart
        update_gantt_chart(gantt_chart, processes[idx]["name"], current_time, current_time + 1, last_process)

        last_process = processes[idx]["name"]
        remaining_bt[idx] -= 1
        current_time += 1

        # Process is completed
        if remaining_bt[idx] == 0:
            is_completed[idx] = True
            completed += 1

            # Calculate metrics for this process
            completion_time, tat, wt, rt = calculate_metrics(processes[idx], start_times[idx], processes[idx]["burst_time"])

            # Add to process table
            add_to_process_table(process_table, processes[idx], start_times[idx], completion_time, tat, wt, rt)

            total_tat += tat
            total_wt += wt
            total_rt += rt

    # Compute final statistics
    stats = compute_stats(n, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats

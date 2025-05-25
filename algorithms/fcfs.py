from .utils import calculate_metrics, update_gantt_chart, add_to_process_table, compute_stats

def run_fcfs(processes):
  
    # Input validation
    if not processes:
        raise ValueError("Empty process list")
    
    for p in processes:
        if not all(key in p for key in ["name", "arrival_time", "burst_time"]):
            raise ValueError("Process missing required fields")
        if p["arrival_time"] < 0 or p["burst_time"] <= 0:
            raise ValueError("Invalid arrival_time or burst_time")

    # Sort processes by arrival time
    processes.sort(key=lambda x: x["arrival_time"])
    time = 0
    gantt_chart = []
    process_table = []
    total_tat = total_wt = total_rt = total_idle_time = 0

    for process in processes:
        if time < process["arrival_time"]:
            total_idle_time += process["arrival_time"] - time
            update_gantt_chart(gantt_chart, "Idle", time, process["arrival_time"])
            time = process["arrival_time"]

        start_time = time
        completion, tat, wt, rt = calculate_metrics(process, start_time, process["burst_time"])
        time = completion

        update_gantt_chart(gantt_chart, process["name"], start_time, completion)
        add_to_process_table(process_table, process, start_time, completion, tat, wt, rt)

        total_tat += tat
        total_wt += wt
        total_rt += rt

    # Sort process table by process name
    process_table.sort(key=lambda x: x["name"])

    stats = compute_stats(len(processes), gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, process_table, stats
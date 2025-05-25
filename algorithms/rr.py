from .utils import (
    update_gantt_chart,
    add_to_process_table,
    compute_stats
)

def sort_arrival_time(process):
    return process["arrival_time"]

def run_rr(processes, time_quantum):
    processes.sort(key=sort_arrival_time)
    n = len(processes)

    ready_queue = []
    current_time = 0
    remaining_bt = [p["burst_time"] for p in processes]
    is_in_queue = [False] * n
    is_completed = [False] * n
    start_times = [None] * n
    completion_times = [0] * n

    gantt_chart = []
    process_table = []
    total_idle_time = 0
    total_tat = total_wt = total_rt = 0

    ready_queue.append(0)
    is_in_queue[0] = True
    last_process = None

    while ready_queue:
        idx = ready_queue.pop(0)
        p = processes[idx]
        p_name = p["name"]
        p_at = p["arrival_time"]
        p_bt = p["burst_time"]

        if start_times[idx] is None:
            start_times[idx] = max(current_time, p_at)
            if current_time < p_at:
                total_idle_time += p_at - current_time
                current_time = p_at

        exec_start = current_time
        exec_time = min(time_quantum, remaining_bt[idx])
        remaining_bt[idx] -= exec_time
        current_time += exec_time

        # Update Gantt chart using utility
        update_gantt_chart(gantt_chart, p_name, exec_start, current_time, last_process)
        last_process = p_name

        # Enqueue newly arrived processes
        for i in range(n):
            if (
                processes[i]["arrival_time"] <= current_time
                and not is_in_queue[i]
                and remaining_bt[i] > 0
            ):
                ready_queue.append(i)
                is_in_queue[i] = True

        if remaining_bt[idx] > 0:
            ready_queue.append(idx)
        else:
            is_completed[idx] = True
            completion_time = current_time
            tat = completion_time - p_at
            wt = tat - p_bt
            rt = start_times[idx] - p_at

            add_to_process_table(process_table,p,start_times[idx],completion_time,tat,wt,rt)

            total_tat += tat
            total_wt += wt
            total_rt += rt

    stats = compute_stats(n, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats


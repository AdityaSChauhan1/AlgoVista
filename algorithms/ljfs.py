from .utils import calculate_metrics, update_gantt_chart, add_to_process_table, compute_stats

def run_ljfs(processes):
    # Sort processes based on arrival time
    processes.sort(key=lambda p: p["arrival_time"])

    current_time = 0
    length = len(processes)
    completed = 0
    visited = [False] * length

    gantt_chart = []
    process_table = []

    total_tat = total_wt = total_rt = total_idle_time = 0

    while completed < length:
        idx = -1
        max_bt = -1

        # Select process with the longest burst time among arrived ones
        for i in range(length):
            p = processes[i]
            if not visited[i] and p["arrival_time"] <= current_time:
                if p["burst_time"] > max_bt:
                    max_bt = p["burst_time"]
                    idx = i
                elif p["burst_time"] == max_bt and p["arrival_time"] < processes[idx]["arrival_time"]:
                    idx = i

        # CPU is idle — no process has arrived yet
        if idx == -1:
            idle_start = current_time
            current_time += 1
            total_idle_time += 1

            # Checks if any process has arrived yet if not, keeps incrementing time and counts idle time
            while True:
                found = False
                for i in range(length):
                    if not visited[i] and processes[i]["arrival_time"] <= current_time:
                        found = True
                        break
                if found or completed == length:
                    break
                current_time += 1
                total_idle_time += 1

            update_gantt_chart(gantt_chart, "Idle", idle_start, current_time)
            continue

        # Process execution
        p = processes[idx]
        start_time = current_time
        completion_time = start_time + p["burst_time"]

        # calculate TAT, WT, RT
        completion, tat, wt, rt = calculate_metrics(p, start_time, p["burst_time"])

        update_gantt_chart(gantt_chart, p["name"], start_time, completion_time)
        add_to_process_table(process_table, p, start_time, completion_time, tat, wt, rt)

        total_tat += tat
        total_wt += wt
        total_rt += rt

        current_time = completion_time
        visited[idx] = True
        completed += 1

    # Sort the process table by name
    process_table.sort(key=lambda x: x["name"])


    stats = compute_stats(length, gantt_chart, total_idle_time, total_tat, total_wt, total_rt)

    return gantt_chart, sorted(process_table, key=lambda x: x["name"]), stats

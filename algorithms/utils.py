# scheduling_algorithms/utils.py

def calculate_metrics(process, start_time, burst_time):
    completion_time = start_time + burst_time
    tat = completion_time - process["arrival_time"]
    wt = tat - burst_time
    rt = start_time - process["arrival_time"]
    return completion_time, tat, wt, rt

def update_gantt_chart(gantt_chart, p_name, start, end, last_process=None):
    #avoids adding duplicate continuous entries
    if last_process is not None and last_process == p_name and gantt_chart:
        gantt_chart[-1]["end"] = end
    else:
        gantt_chart.append({
            "name": p_name,
            "start": start,
            "end": end
        })

def add_to_process_table(table, process, start, completion, tat, wt, rt):
    table.append({
        "name": process["name"],
        "arrival_time": process["arrival_time"],
        "burst_time": process["burst_time"],
        "start_time": start,
        "completion_time": completion,
        "tat": tat,
        "wt": wt,
        "rt": rt
    })

def compute_stats(process_count, gantt_chart, total_idle_time, total_tat, total_wt, total_rt):
    total_time = gantt_chart[-1]["end"] - gantt_chart[0]["start"]
    avg_tat = total_tat / process_count
    avg_wt = total_wt / process_count
    avg_rt = total_rt / process_count
    cpu_utilization = ((total_time - total_idle_time) / total_time) * 100
    throughput = process_count / total_time
    return {
        "avg_tat": round(avg_tat, 2),
        "avg_wt": round(avg_wt, 2),
        "avg_rt": round(avg_rt, 2),
        "cpu_utilization": round(cpu_utilization, 2),
        "throughput": round(throughput, 2)
    }

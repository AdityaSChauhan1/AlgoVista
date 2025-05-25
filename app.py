from flask import Flask, request, jsonify
from algorithms import fcfs, sjfs, srtf, rr, priority_np, priority_p, ljfs, lrtf, hrrn
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Map algorithm names to their functions
algo_map = {
    "First Come First Serve": fcfs.run_fcfs,
    "Shortest Job First": sjfs.run_sjfs,
    "Shortest Remaining Time First": srtf.run_srtf,
    "Longest Job First": ljfs.run_ljfs,
    "Longest Remaining Time First": lrtf.run_lrtf,
    "Round Robin": lambda p, tq: rr.run_rr(p, tq),
    "Highest Response Ratio Next": hrrn.run_hrrn,
    "Priority Non-Preemptive": priority_np.run_priority_np,
    "Priority Preemptive": priority_p.run_priority_p
}

@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.get_json()
    algorithm = data.get("algorithm")
    processes = data.get("processes")
    time_quanta = data.get("time_quanta", None)

    if not algorithm or not processes:
        return jsonify({"error": "Missing required fields"}), 400

    if algorithm not in algo_map:
        return jsonify({"error": "Unknown scheduling algorithm"}), 400

    if algorithm == "Round Robin" and time_quanta is None:
        return jsonify({"error": "Time quanta is required for Round Robin"}), 400

    gantt_chart, process_table, stats = (
        algo_map[algorithm](processes, time_quanta) if algorithm == "Round Robin"
        else algo_map[algorithm](processes)
    )

    return jsonify({
        "gantt_chart": gantt_chart,
        "process_table": process_table,
        "stats": stats
    })


@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json()
    processes = data.get("processes")
    time_quanta = data.get("time_quanta", 2)  # Default time quanta for RR

    if not processes:
        return jsonify({"error": "Missing processes"}), 400

    results = {}
    for name, func in algo_map.items():
        try:
            if name == "Round Robin":
                gantt, table, stats = func(processes, time_quanta)
            else:
                gantt, table, stats = func(processes)

            results[name] = {
                "gantt_chart": gantt,
                "stats": stats
            }
        except Exception as e:
            results[name] = {"error": str(e)}

    return jsonify(results)

@app.route("/algorithms", methods=["GET"])
def get_algorithms():
    return jsonify({
        "algorithms": ["First Come First Serve", "Shortest Job First", "Shortest Remaining Time First", "Longest Job First", "Longest Remaining Time First", "Round Robin", "Highest Response Ratio Next", "Priority Non-Preemptive", "Priority Preemptive"]
    })


if __name__ == "__main__":
    app.run(debug=True)

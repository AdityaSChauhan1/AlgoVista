import sys
import os
import json

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algorithms.rr import run_rr


def get_processes_from_user():
    processes = []
    try:
        n = int(input("Enter number of processes: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return []

    for i in range(n):
        print(f"\nEnter details for Process {i + 1}")
        name = input("Process Name: ")
        arrival_time = int(input("Arrival Time: "))
        burst_time = int(input("Burst Time: "))

        processes.append({
            "name": name,
            "arrival_time": arrival_time,
            "burst_time": burst_time
        })
    
    return processes


def get_time_quantum_from_user():
    try:
        time_quantum = int(input("\nEnter the time quantum: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

    return time_quantum


def main():
    processes = get_processes_from_user()
    if not processes:
        print("No processes to schedule.")
        return

    time_quantum = get_time_quantum_from_user()
    if time_quantum is None:
        print("Invalid time quantum. Please try again.")
        return

    result = run_rr(processes, time_quantum)

    output_file = os.path.join(os.path.dirname(__file__), 'output.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print("\nScheduling complete. Output saved to 'output.json'")


if __name__ == "__main__":
    main()

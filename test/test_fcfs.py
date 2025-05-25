import sys
import os
import json

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algorithms.fcfs import run_fcfs


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


def main():
    processes = get_processes_from_user()
    if not processes:
        print("No processes to schedule.")
        return

    result = run_fcfs(processes)

    output_file = os.path.join(os.path.dirname(__file__), 'output.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print("\nScheduling complete. Output saved to 'output.json'")


if __name__ == "__main__":
    main()

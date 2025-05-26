# AlgoVista

🔄 CPU Scheduling Visualizer
CPU Scheduling Visualizer is a web-based interactive educational tool that helps users understand and simulate various CPU scheduling algorithms with real-time Gantt charts and performance metrics. This project was developed as part of a Software Engineering course (SE(OS)-VI-T164) by Team ALPHA.

🚀 Project Overview
This tool visually simulates the following CPU scheduling algorithms:
- First-Come-First-Serve (FCFS)
- Shortest Job First Scheduling (SJFS) – Preemptive and Non-Preemptive
- Longest Job First Scheduling (LJFS) – Preemptive and Non-Preemptive
- Round Robin
- Highest Response Ratio Next (HRRN)
- Priority Scheduling – Preemptive and Non-Preemptive

Users can:
- Enter custom processes with attributes like arrival time, burst time and priority
- Choose scheduling algorithms to simulate
- Visualize execution in a dynamic Gantt chart
- View and compare performance metrics (Waiting Time, Turnaround Time, Response Time, CPU Utilization, Throughput)

🛠️ Tech Stack
Frontend: React.js, Axios, HTML, CSS, JavaScript
Backend: Python (Flask), RESTful APIs, JSON

🎯 Features
- Dynamic Gantt Chart: Real-time animation of process execution
- Metrics Display: Shows WT, TAT, RT, CPU Utilization, and Throughput
- Cross-algorithm Comparison: Compare results between multiple algorithms
- Play/Pause Controls: Interactive simulation playback
- Input Validation: Handles valid/invalid data gracefully

📦 Project Structure
/frontend       # React.js app
/backend        # Flask backend with algorithm logic
/public
README.md

✅ How to Run Locally
Prerequisites:
- Node.js & npm/yarn
- Python 3.x & pip

Backend Setup:
              cd backend
              pip install -r requirements.txt
              python app.py

Frontend Setup:
              cd frontend
              npm install
              npm start

👨‍💻 Team ALPHA – SE(OS)-VI-T164
- Aditya Chauhan – Team Lead
- Sidakveer Singh
- Alok Yadav
- Kartikey Singh


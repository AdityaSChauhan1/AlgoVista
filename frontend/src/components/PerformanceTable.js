import React from 'react';

const PerformanceTable = ({ result }) => {
  return (
    <div>
      {/* Process Table */}
      <h2 className="section-title">Process Table</h2>
      <div className="table-container">
        <table className="process-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Arrival Time</th>
              <th>Burst Time</th>
              <th>Start Time</th>
              <th>Completion Time</th>
              <th>Turnaround Time</th>
              <th>Response Time</th>
              <th>Waiting Time</th>
            </tr>
          </thead>
          <tbody>
            {result.process_table.map((proc, index) => (
              <tr key={index}>
                <td>{proc.name}</td>
                <td>{proc.arrival_time}</td>
                <td>{proc.burst_time}</td>
                <td>{proc.start_time}</td>
                <td>{proc.completion_time}</td>
                <td>{proc.tat}</td>
                <td>{proc.rt}</td>
                <td>{proc.wt}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Statistics */}
      <h2 className="section-title">Statistics</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">
            {result.stats.avg_tat.toFixed(2)}
          </div>
          <div className="stat-label">Average Turnaround Time</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {result.stats.avg_wt.toFixed(2)}
          </div>
          <div className="stat-label">Average Waiting Time</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {result.stats.avg_rt.toFixed(2)}
          </div>
          <div className="stat-label">Average Response Time</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {result.stats.cpu_utilization.toFixed(2)}%
          </div>
          <div className="stat-label">CPU Utilization</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {result.stats.throughput.toFixed(2)}
          </div>
          <div className="stat-label">Throughput (processes/unit time)</div>
        </div>
      </div>
    </div>
  );
};

export default PerformanceTable;

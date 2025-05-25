import React from 'react';

const CompareChart = ({ compareResults, getProcessColor, viewAlgorithmDetails, viewingAlgo }) => {
  const formatAlgorithmName = (algo) => {
    const nameMap = {
      'First Come First Serve': 'FCFS',
      'Shortest Job First': 'SJF',
      'Shortest Remaining Time First': 'SRTF',
      'Longest Job First': 'LJF',
      'Longest Remaining Time First': 'LRTF',
      'Round Robin': 'RR',
      'Highest Response Ratio Next': 'HRRN',
      'Priority Non-Preemptive': 'P-NP',
      'Priority Preemptive': 'P-P'
    };
    return nameMap[algo] || algo;
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="section-title">Algorithm Comparison</h2>
      </div>

      <div className="table-container">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Algorithm</th>
              <th>Avg. Turnaround Time</th>
              <th>Avg. Waiting Time</th>
              <th>Avg. Response Time</th>
              <th>CPU Utilization</th>
              <th>Throughput</th>
              <th>View Details</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(compareResults).map(([algo, data], index) => (
              <tr key={index} className={algo === viewingAlgo ? 'active-row' : ''}>
                <td>{algo}</td>
                <td>{data.stats.avg_tat.toFixed(2)}</td>
                <td>{data.stats.avg_wt.toFixed(2)}</td>
                <td>{data.stats.avg_rt.toFixed(2)}</td>
                <td>{data.stats.cpu_utilization.toFixed(2)}%</td>
                <td>{data.stats.throughput.toFixed(2)}</td>
                <td>
                  <button 
                    className={`btn ${algo === viewingAlgo ? 'btn-secondary' : 'btn-primary'}`}
                    onClick={() => viewAlgorithmDetails(algo, data)}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Gantt Charts Section */}
      <h3 className="section-title">Gantt Charts</h3>
      <div className="gantt-compare-container">
        {Object.entries(compareResults).map(([algo, data]) => (
          <div key={algo} className="gantt-compare-row">
            <div className="gantt-compare-label">{algo}</div>
            <div className="gantt-chart">
              {data.gantt_chart.map((entry, index) => {
                const startTime = Number(entry.start_time || entry.start).toFixed(1);
                const endTime = Number(entry.end_time || entry.end).toFixed(1);
                const duration = (Number(endTime) - Number(startTime)).toFixed(1);
                return (
                  <div 
                    key={index} 
                    className="gantt-block"
                    style={{
                      width: `${Number(duration) * 50}px`,
                      backgroundColor: getProcessColor(entry.name || entry.process_id)
                    }}
                  >
                    <div className="gantt-block-title">
                      {entry.name || entry.process_id}
                    </div>
                    <div className="gantt-block-time">
                      Start: {startTime}
                    </div>
                    <div className="gantt-block-time">
                      End: {endTime}
                    </div>
                    <div className="gantt-block-time">
                      Duration: {duration}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
      
      <h3 className="section-title">Performance Visualization</h3>
      <div className="comparison-charts">
        {['avg_tat', 'avg_wt', 'avg_rt', 'cpu_utilization', 'throughput'].map((metric, idx) => {
          const labels = {
            avg_tat: 'Average Turnaround Time',
            avg_wt: 'Average Waiting Time',
            avg_rt: 'Average Response Time',
            cpu_utilization: 'CPU Utilization',
            throughput: 'Throughput'
          };
          
          const getScaledHeight = (value, metric) => {
            if (metric === 'cpu_utilization') return value;
            if (metric === 'throughput') return value * 100;
            return value * 10;
          };

          return (
            <div key={metric} className="chart-container">
              <h4>{labels[metric]}</h4>
              <div className="comparison-chart">
                {Object.entries(compareResults).map(([algo, data], index) => (
                  <div key={index} className="chart-bar">
                    <div 
                      className="bar-value"
                      style={{ 
                        height: `${getScaledHeight(data.stats[metric], metric)}px`,
                        backgroundColor: getProcessColor(`P${index+1}`)
                      }}
                    >
                      {metric === 'cpu_utilization' 
                        ? `${data.stats[metric].toFixed(1)}%`
                        : data.stats[metric].toFixed(2)}
                    </div>
                    <div className="bar-label">{formatAlgorithmName(algo)}</div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CompareChart;

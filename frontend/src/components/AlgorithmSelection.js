import React from 'react';

const AlgorithmSelection = ({ 
  algorithms, 
  selectedAlgo, 
  setSelectedAlgo, 
  timeQuanta, 
  setTimeQuanta,
  runSchedule,
  runAllAlgorithms 
}) => {
  return (
    <div className="card">
      <div className="controls-container">
        <div className="control-group">
          <label className="control-label">Algorithm</label>
          <select 
            className="control-select"
            value={selectedAlgo}  // show selected algo
            onChange={e => setSelectedAlgo(e.target.value)}   // show the changed algo i.e. when update
          >
            {algorithms.map(algo => (
              <option key={algo} value={algo}>{algo}</option>
            ))}
          </select>
        </div>

        {selectedAlgo === 'Round Robin' && (
          <div className="control-group">
            <label className="control-label">Time Quantum</label>
            <input
              type="number"
              className="control-input"
              value={timeQuanta}
              min={1}
              onChange={e => setTimeQuanta(Number(e.target.value))}
            />
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="button-group">
        <button 
          className="btn btn-primary"
          onClick={runSchedule}
        >
          Run Selected Algorithm
        </button>
        <button 
          className="btn btn-secondary"
          onClick={runAllAlgorithms}
        >
          Compare All Algorithms
        </button>
      </div>
    </div>
  );
};

export default AlgorithmSelection; 
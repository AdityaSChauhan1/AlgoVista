import React from 'react';

const InputForm = ({ processes, handleProcessChange, addProcess, removeProcess }) => {
  const preventArrowKeys = (e) => {
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      e.preventDefault();
    }
  };

  const handleNumberInput = (e) => {
    // Remove leading zeros in real-time
    const value = e.target.value;
    if (value.length > 1 && value.startsWith('0')) {
      e.target.value = value.replace(/^0+/, '');
    }
  };

  return (
    <div className="card processes-section">
      <h2 className="processes-header">Processes</h2>
      
      <div className="process-grid-container">
        <div className="process-grid-header">
          <div>Name</div>
          <div>Arrival Time</div>
          <div>Burst Time</div>
          <div>Priority</div>
          <div></div>
        </div>

        {processes.map((proc, idx) => (
          <div key={idx} className="process-row">
            <input
              type="text"
              className="process-input"
              value={proc.name}
              onChange={e => handleProcessChange(idx, 'name', e.target.value)}
            />
            <input
              type="number"
              className="process-input"
              value={proc.arrival_time}
              min={0}
              onKeyDown={preventArrowKeys}
              onInput={handleNumberInput}
              onChange={e => handleProcessChange(idx, 'arrival_time', e.target.value)}
            />
            <input
              type="number"
              className="process-input"
              value={proc.burst_time}
              min={1}
              onKeyDown={preventArrowKeys}
              onInput={handleNumberInput}
              onChange={e => handleProcessChange(idx, 'burst_time', e.target.value)}
            />
            <div className="priority-input-container">
              <input
                type="number"
                className="process-input priority-input"
                value={proc.priority || 0}
                min={0}
                onKeyDown={preventArrowKeys}
                onInput={handleNumberInput}
                onChange={e => handleProcessChange(idx, 'priority', e.target.value)}
              />
            </div>
            <button 
              className="btn-remove"
              onClick={() => removeProcess(idx)}
              disabled={processes.length === 1}
            >
              Remove
            </button>
          </div>
        ))}

        <button 
          className="btn-add-process"
          onClick={addProcess}
        >
          Add Process
        </button>
      </div>
    </div>
  );
};

export default InputForm;
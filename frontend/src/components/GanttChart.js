import React, { useState, useRef, useEffect } from 'react';

const GanttChart = ({ result, getProcessColor, selectedAlgo, compareResults, backToComparison }) => {
  // Animation state
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const timerRef = useRef(null);
  const totalSteps = result.gantt_chart.length;

  // Animation effect
  useEffect(() => {
    if (isPlaying && currentStep < totalSteps) {
      timerRef.current = setTimeout(() => {
        setCurrentStep((prev) => Math.min(prev + 1, totalSteps));
      }, 800); // 800ms per step, adjust as needed
    } else if (!isPlaying) {
      clearTimeout(timerRef.current);
    }
    return () => clearTimeout(timerRef.current);
  }, [isPlaying, currentStep, totalSteps]);

  // Reset animation if result changes (e.g., new algo selected)
  useEffect(() => {
    setCurrentStep(0);
    setIsPlaying(false);
  }, [result]);

  const handlePlay = () => {
    if (currentStep >= totalSteps) {
      setCurrentStep(0);
    }
    setIsPlaying(true);
  };
  const handlePause = () => setIsPlaying(false);
  const handleReset = () => {
    setIsPlaying(false);
    setCurrentStep(0);
  };
  const handleBack = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 0));
    setIsPlaying(false);
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="section-title">Gantt Chart ({selectedAlgo})</h2>
        {compareResults && (
          <button 
            className="btn btn-secondary"
            onClick={backToComparison}
          >
            Back to Comparison
          </button>
        )}
      </div>
      {/* Animation Controls */}
      <div className="gantt-controls" style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', alignItems: 'center' }}>
        <button className="btn btn-primary" onClick={handlePlay} disabled={isPlaying || currentStep >= totalSteps}>Play</button>
        <button className="btn btn-secondary" onClick={handlePause} disabled={!isPlaying}>Pause</button>
        <button className="btn btn-secondary" onClick={handleReset}>Reset</button>
        <button className="btn btn-secondary" onClick={handleBack} disabled={currentStep === 0}>Previous</button>
        <span style={{marginLeft: '1rem', fontWeight: 500}}>
          Step: {Math.min(currentStep, totalSteps)} / {totalSteps}
        </span>
      </div>
      {/* Gantt Chart */}
      <div className="gantt-container">
        <div className="gantt-chart">
          {result.gantt_chart.slice(0, currentStep).map((entry, index) => {
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
    </div>
  );
};

export default GanttChart;

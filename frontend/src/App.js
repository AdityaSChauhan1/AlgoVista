import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Import components
import AlgorithmSelection from './components/AlgorithmSelection';
import InputForm from './components/InputForm';
import GanttChart from './components/GanttChart';
import PerformanceTable from './components/PerformanceTable';
import CompareChart from './components/CompareChart';
import ErrorPopup from './components/ErrorPopup';

function App() {
  // states (first view)
  const [algorithms, setAlgorithms] = useState([]);
  const [selectedAlgo, setSelectedAlgo] = useState('');
  const [processes, setProcesses] = useState([{ name: 'P1', arrival_time: 0, burst_time: 0 }]);
  const [timeQuanta, setTimeQuanta] = useState(2);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [compareResults, setCompareResults] = useState(null);
  const [showComparison, setShowComparison] = useState(false);
  const [viewingAlgo, setViewingAlgo] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/algorithms')
      .then(res => {
        setAlgorithms(res.data.algorithms);
        if (res.data.algorithms.length > 0) {
          setSelectedAlgo(res.data.algorithms[0]);
        }
      })
      .catch(() => setError('Failed to fetch algorithms'));
  }, []);

  // update the process data when the user edits input fields
  const handleProcessChange = (index, field, value) => {
    const newProcesses = [...processes];
    if (field === 'name') {
      newProcesses[index][field] = value;
    } else {
      // Remove leading zeros and convert to number
      const cleanValue = value.replace(/^0+/, '') || '0';
      newProcesses[index][field] = Number(cleanValue);
    }
    setProcesses(newProcesses);
  };

  const addProcess = () => {
    setProcesses([...processes, { name: `P${processes.length + 1}`, arrival_time: 0, burst_time: 0 }]);
  };

  const removeProcess = (index) => {
    if (processes.length === 1) return;
    const newProcesses = processes.filter((_, i) => i !== index); // _ -> current item
    setProcesses(newProcesses);
  };

  const validateInputs = () => {
    // Check if any process has empty or invalid values
    for (const process of processes) {
      if (!process.name || process.name.trim() === '') {
        setError('Process name cannot be empty');
        return false;
      }
      if (process.arrival_time < 0) {
        setError('Arrival time cannot be negative');
        return false;
      }
      if (process.burst_time <= 0) {
        setError('Burst time must be greater than 0');
        return false;
      }
    }

    // Validate time quantum for Round Robin
    if (selectedAlgo === 'Round Robin' && (timeQuanta <= 0 || !Number.isInteger(timeQuanta))) {
      setError('Time quantum must be a positive integer');
      return false;
    }

    return true;
  };

  const runSchedule = () => {
    setError('');
    setResult(null);
    setShowComparison(false);

    if (!validateInputs()) {
      return;
    }

    // this paylod used to send data to backend
    const payload = {       
      algorithm: selectedAlgo,
      processes,
    };
    if (selectedAlgo === 'Round Robin') {
      payload.time_quanta = timeQuanta;
    }

    axios.post('http://localhost:5000/schedule', payload)
      .then(res => {
        setResult(res.data);
      })
      .catch(err => setError(err.response?.data?.error || 'Error running schedule'));
  };

  const runAllAlgorithms = async () => {
    setError('');
    setResult(null);
    setShowComparison(true);
    
    if (!validateInputs()) {
      return;
    }

    try {
      const results = {};
      const basePayload = {
        processes: processes.map(p => ({
          name: p.name,
          arrival_time: Number(p.arrival_time),
          burst_time: Number(p.burst_time),
          priority: Number(p.priority || 0)
        }))
      };

      for (const algo of algorithms) {
        const payload = {
          ...basePayload,
          algorithm: algo
        };
        
        if (algo === 'Round Robin') {
          payload.time_quanta = Number(timeQuanta);
        }
        
        try {
          const response = await axios.post('http://localhost:5000/schedule', payload);
          results[algo] = response.data;
        } catch (err) {
          setError(`Error running ${algo}: ${err.response?.data?.error || 'Unknown error'}`);
          return;
        }
      }
      
      if (Object.keys(results).length > 0) {
        setCompareResults(results);
      } else {
        setError('No results were generated from the algorithms');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error running comparison');
      setShowComparison(false);
    }
  };

  const viewAlgorithmDetails = (algo, data) => {
    setViewingAlgo(algo);
    setSelectedAlgo(algo);
    setResult(data);
    setShowComparison(false);
  };

  const backToComparison = () => {
    setViewingAlgo(null);
    setResult(null);
    setShowComparison(true);
  };

  const getProcessColor = (processName) => {
    const colors = [
        '#FF6B6B', // red
        '#4ECDC4', // teal
        '#45B7D1', // blue
        '#FFBE0B', // yellow
        '#FB5607', // orange
        '#8338EC', // purple
        '#3A86FF', // light blue
        '#38B000', // green
        '#FF006E', // magenta
        '#FFD166', // light yellow
        '#06D6A0', // aqua
        '#118AB2', // steel blue
        '#EF476F', // pink
        '#073B4C', // dark blue
        '#F3722C', // orange-red
        '#43AA8B', // sea green
        '#F9C74F', // gold
        '#577590', // slate blue
        '#B5179E', // violet
        '#A3A847', // olive
    ];
    
    if (processName === 'idle') return '#CCCCCC';
    
    const processNumber = parseInt(processName.replace(/\D/g, ''), 10) || 0;
    return colors[processNumber % colors.length];
  };

  return (
    <div className="app-container">
      <h1 className="app-title">AlgoVista</h1>

      <AlgorithmSelection 
        algorithms={algorithms}
        selectedAlgo={selectedAlgo}
        setSelectedAlgo={setSelectedAlgo}
        timeQuanta={timeQuanta}
        setTimeQuanta={setTimeQuanta}
        runSchedule={runSchedule}
        runAllAlgorithms={runAllAlgorithms}
      />

      <InputForm 
        processes={processes}
        handleProcessChange={handleProcessChange}
        addProcess={addProcess}
        removeProcess={removeProcess}
      />

      <ErrorPopup 
        message={error}
        onClose={() => setError('')}
      />

      {!showComparison && result && (
        <>
          <GanttChart 
            result={result}
            getProcessColor={getProcessColor}
            selectedAlgo={selectedAlgo}
            compareResults={compareResults}
            backToComparison={backToComparison}
          />
          <div className="process-table-container">
            <h2 className="section-title">Process Details</h2>
            <PerformanceTable result={result} />
          </div>
        </>
      )}

      {showComparison && compareResults && (
        <CompareChart 
          compareResults={compareResults}
          getProcessColor={getProcessColor}
          viewAlgorithmDetails={viewAlgorithmDetails}
          viewingAlgo={viewingAlgo}
        />
      )}
    </div>
  );
}

export default App;
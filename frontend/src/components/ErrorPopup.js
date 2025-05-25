import React from 'react';

const ErrorPopup = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="error-popup-overlay">
      <div className="error-popup">
        <div className="error-popup-content">
          <div className="error-icon">⚠️</div>
          <p>{message}</p>
        </div>
        <button className="error-popup-close" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
};

export default ErrorPopup; 
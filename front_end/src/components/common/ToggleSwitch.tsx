import React from 'react';
import './ToggleSwitch.css';

interface ToggleSwitchProps {
  isOn: boolean;
  handleToggle: () => void;
  label?: string;
  disabled?: boolean;
  title?: string;
}

const ToggleSwitch: React.FC<ToggleSwitchProps> = ({
  isOn,
  handleToggle,
  label,
  disabled = false,
  title,
}) => {
  // Empêcher la propagation de l'événement pour éviter les conflits
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!disabled) {
      handleToggle();
    }
  };

  return (
    <div className="toggle-switch-container" title={title}>
      {label && <span className="toggle-switch-label">{label}</span>}
      <div 
        className={`toggle-switch ${isOn ? 'toggle-on' : 'toggle-off'} ${disabled ? 'toggle-disabled' : ''}`}
        onClick={handleClick}
      >
        <input
          type="checkbox"
          checked={isOn}
          onChange={() => {}} // Géré par onClick pour éviter les avertissements React
          disabled={disabled}
          className="toggle-switch-checkbox"
        />
        <div className="toggle-switch-track">
          <div className="toggle-switch-thumb"></div>
          <div className="toggle-switch-text">
            {isOn ? 'ON' : 'OFF'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ToggleSwitch;

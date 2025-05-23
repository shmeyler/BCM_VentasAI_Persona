import React from "react";

const StepIndicator = ({ steps, currentStep, completedSteps, onStepClick }) => {
  const getStepStatus = (stepId) => {
    if (completedSteps.includes(stepId)) return "completed";
    if (stepId === currentStep) return "active";
    if (stepId < currentStep) return "completed";
    return "pending";
  };

  const canClickStep = (stepId) => {
    // Allow clicking on previous steps, current step, or media consumption step (step 6) for editing
    return stepId <= currentStep || stepId === 6;
  };

  return (
    <div className="flex items-center justify-between mb-8 overflow-x-auto">
      {steps.map((step, index) => (
        <div key={step.id} className="flex items-center flex-1">
          <div className="flex flex-col items-center flex-1">
            <button
              onClick={() => canClickStep(step.id) && onStepClick(step.id)}
              disabled={!canClickStep(step.id)}
              className={`step-indicator ${getStepStatus(step.id)} ${
                canClickStep(step.id) ? 'cursor-pointer hover:scale-105' : 'cursor-not-allowed'
              } transition-all duration-200`}
            >
              {getStepStatus(step.id) === "completed" ? (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              ) : (
                step.id
              )}
            </button>
            <span className={`text-xs mt-2 text-center ${
              getStepStatus(step.id) === "active" ? "text-blue-600 font-semibold" :
              getStepStatus(step.id) === "completed" ? "text-green-600" : "text-gray-400"
            }`}>
              {step.name}
            </span>
          </div>
          
          {index < steps.length - 1 && (
            <div className="flex-1 h-0.5 bg-gray-300 mx-4">
              <div 
                className={`h-full transition-all duration-300 ${
                  step.id < currentStep || completedSteps.includes(step.id) ? "bg-green-500" : "bg-gray-300"
                }`}
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default StepIndicator;

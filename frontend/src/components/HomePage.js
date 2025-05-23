import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HomePage = () => {
  const navigate = useNavigate();
  const [isCreating, setIsCreating] = useState(false);

  const createPersona = async (startingMethod) => {
    setIsCreating(true);
    try {
      const response = await axios.post(`${API}/personas`, {
        starting_method: startingMethod,
        name: `New Persona ${new Date().toLocaleDateString()}`
      });
      
      // Navigate to wizard with the created persona ID
      navigate(`/persona-wizard?id=${response.data.id}&method=${startingMethod}`);
    } catch (error) {
      console.error("Error creating persona:", error);
      alert("Failed to create persona. Please try again.");
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold font-montserrat bcm-title">
          BCM VentasAI Persona Generator
        </h1>
        <p className="text-gray-600 mt-2">
          Build a comprehensive and data driven AI-based consumer persona.
        </p>
      </div>

      <div className="mt-8">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold font-montserrat mb-3 bcm-heading">
            How would you like to start?
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Choose your preferred approach to building your marketing persona
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-5xl mx-auto">
          {/* Start with Demographics */}
          <div className="bcm-card" onClick={() => createPersona("demographics")}>
            <div 
              className="flex items-center justify-center w-20 h-20 rounded-full mx-auto mb-6"
              style={{backgroundColor: 'var(--bcm-teal-light)'}}
            >
              <svg 
                className="h-10 w-10 bcm-icon-teal" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" 
                />
              </svg>
            </div>
            <h3 className="text-2xl font-semibold text-center mb-4 font-montserrat bcm-heading">
              Start with Demographics
            </h3>
            <p className="text-gray-600 text-center text-lg mb-6">
              Provide basic demographics and one key attribute. Our AI will map the rest.
            </p>
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-500">
                <strong>Best for:</strong> When you know your target demographics and want AI to suggest matching behaviors and preferences.
              </p>
            </div>
          </div>

          {/* Start with Attributes */}
          <div className="bcm-card-cyan" onClick={() => createPersona("attributes")}>
            <div 
              className="flex items-center justify-center w-20 h-20 rounded-full mx-auto mb-6"
              style={{backgroundColor: 'var(--bcm-cyan-light)'}}
            >
              <svg 
                className="h-10 w-10 bcm-icon-cyan" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" 
                />
              </svg>
            </div>
            <h3 className="text-2xl font-semibold text-center mb-4 font-montserrat bcm-heading-cyan">
              Start with Attributes
            </h3>
            <p className="text-gray-600 text-center text-lg mb-6">
              Provide key attributes and behaviors. Our AI will identify the matching demographics.
            </p>
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-500">
                <strong>Best for:</strong> When you know what your audience does or wants and need AI to map the corresponding demographics.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="mt-8 pt-4 border-t border-gray-200 flex justify-between">
        <button 
          type="button" 
          disabled 
          className="px-4 py-2 rounded-md font-medium text-sm bg-gray-200 text-gray-400 cursor-not-allowed"
        >
          Back
        </button>
        <button 
          type="button" 
          disabled={isCreating}
          className="bcm-btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isCreating ? (
            <div className="flex items-center">
              <div className="loading-spinner mr-2"></div>
              Creating...
            </div>
          ) : (
            "Next"
          )}
        </button>
      </div>

      {/* Data Sources Footer */}
      <div className="mt-16 text-center">
        <h2 className="text-2xl font-bold font-montserrat mb-4 bcm-heading">
          Powered by Leading Data Sources
        </h2>
        <div className="flex justify-center items-center space-x-8 text-gray-500 font-montserrat">
          <div>Resonate rAI</div>
          <div>SparkToro</div>
          <div>SEMRush</div>
          <div>Buzzabout.ai</div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

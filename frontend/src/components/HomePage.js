import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HomePage = () => {
  const navigate = useNavigate();
  const [isCreating, setIsCreating] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState(null);

  console.log('BACKEND_URL:', BACKEND_URL); // Debug log
  console.log('API:', API); // Debug log

  const createPersona = async (startingMethod) => {
    console.log('createPersona called with:', startingMethod);
    setIsCreating(true);
    try {
      console.log('Making API call to:', `${API}/personas`);
      
      const response = await axios.post(`${API}/personas`, {
        starting_method: startingMethod,
        name: `New Persona ${new Date().toLocaleDateString()}`
      });
      
      console.log('API response:', response.data);
      
      // Navigate to wizard with the created persona ID
      const navUrl = `/persona-wizard?id=${response.data.id}&method=${startingMethod}`;
      navigate(navUrl);
    } catch (error) {
      console.error("Error creating persona:", error);
      alert(`Failed to create persona: ${error.message}`);
    } finally {
      setIsCreating(false);
    }
  };

  const handleCardClick = (method) => {
    console.log('Card clicked:', method); // Debug log
    setSelectedMethod(method);
  };

  const handleNext = () => {
    console.log('Next button clicked, selectedMethod:', selectedMethod);
    if (selectedMethod) {
      createPersona(selectedMethod);
    } else {
      console.log('No method selected');
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
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-2">
            Choose your preferred approach to building your marketing persona
          </p>
          <p className="text-sm text-blue-600 font-medium">
            👆 Click on one of the options below, then click "Next" to continue
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {/* Start with Demographics */}
          <div 
            className={`bcm-card cursor-pointer transition-all duration-200 ${
              selectedMethod === 'demographics' ? 'ring-4 ring-blue-500 ring-opacity-50 bg-blue-50' : ''
            }`} 
            onClick={() => handleCardClick("demographics")}
          >
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
          <div 
            className={`bcm-card-cyan cursor-pointer transition-all duration-200 ${
              selectedMethod === 'attributes' ? 'ring-4 ring-blue-500 ring-opacity-50 bg-blue-50' : ''
            }`} 
            onClick={() => handleCardClick("attributes")}
          >
            <div className="text-center">
              <div className="mx-auto h-16 w-16 text-cyan-600 mb-4">
                <svg fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <h3 className="text-xl font-bold font-montserrat mb-2 text-gray-800">Start with Attributes</h3>
              <p className="text-gray-600 font-montserrat text-sm leading-relaxed">
                Begin with psychographic attributes and let our AI suggest corresponding demographics
              </p>
            </div>
          </div>

          {/* Upload Resonate Data */}
          <div 
            className={`bcm-card-green cursor-pointer transition-all duration-200 ${
              selectedMethod === 'resonate_upload' ? 'ring-4 ring-blue-500 ring-opacity-50 bg-blue-50' : ''
            }`} 
            onClick={() => handleCardClick("resonate_upload")}
          >
            <div className="text-center">
              <div className="mx-auto h-16 w-16 text-green-600 mb-4">
                <svg fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                </svg>
              </div>
              <h3 className="text-xl font-bold font-montserrat mb-2 text-gray-800">Upload Resonate Data</h3>
              <p className="text-gray-600 font-montserrat text-sm leading-relaxed">
                Upload your Resonate rAI reports (CSV, PDF, PPT) for data-driven persona generation
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
          onClick={handleNext}
          className="bcm-btn-primary"
          style={{backgroundColor: selectedMethod ? '#007bff' : '#ccc'}}
        >
          {isCreating ? (
            <div className="flex items-center">
              <div className="loading-spinner mr-2"></div>
              Creating...
            </div>
          ) : (
            selectedMethod ? "Start Creating Persona" : "Select an Option Above"
          )}
        </button>
      </div>

      {/* Data Sources Footer */}
      <div className="mt-16 text-center">
        <h2 className="text-2xl font-bold font-montserrat mb-4 bcm-heading">
          Powered by Leading Data Sources
        </h2>
        <div className="flex justify-center items-center space-x-12 py-8">
          {/* Resonate rAI */}
          <div className="flex flex-col items-center space-y-3 group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-white rounded-lg shadow-md p-2 flex items-center justify-center">
              <img 
                src="https://www.insightplatforms.com/wp-content/uploads/2023/10/resonate-Logo-Square-Insight-Platforms.png" 
                alt="Resonate Logo"
                className="w-full h-full object-contain"
              />
            </div>
            <span className="text-sm font-medium text-gray-600 group-hover:text-purple-600">Resonate rAI</span>
          </div>

          {/* SparkToro */}
          <div className="flex flex-col items-center space-y-3 group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-white rounded-lg shadow-md p-2 flex items-center justify-center">
              <img 
                src="https://sparktoro.com/img/product/sparktoro-logo.c08f697d63cf1cb31c7388dd16efbfa9.svg" 
                alt="SparkToro Logo"
                className="w-full h-full object-contain"
              />
            </div>
            <span className="text-sm font-medium text-gray-600 group-hover:text-orange-600">SparkToro</span>
          </div>

          {/* SEMRush */}
          <div className="flex flex-col items-center space-y-3 group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-white rounded-lg shadow-md p-2 flex items-center justify-center">
              <img 
                src="https://prowly-prod.s3.eu-west-1.amazonaws.com/uploads/60169/assets/601030/-41b7df259e181179ec6cf7184d77bffe.png" 
                alt="SEMRush Logo"
                className="w-full h-full object-contain"
              />
            </div>
            <span className="text-sm font-medium text-gray-600 group-hover:text-blue-600">SEMRush</span>
          </div>

          {/* Buzzabout.ai */}
          <div className="flex flex-col items-center space-y-3 group hover:scale-105 transition-transform duration-200">
            <div className="w-16 h-16 bg-white rounded-lg shadow-md p-2 flex items-center justify-center">
              <img 
                src="https://ph-files.imgix.net/f9de4bc8-e4a2-4fda-9d5e-5b9c65cfd911.jpeg?auto=compress&codec=mozjpeg&cs=strip&auto=format&w=64&h=64&fit=crop&frame=1&dpr=2" 
                alt="Buzzabout AI Logo"
                className="w-full h-full object-contain rounded"
              />
            </div>
            <span className="text-sm font-medium text-gray-600 group-hover:text-green-600">Buzzabout.ai</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

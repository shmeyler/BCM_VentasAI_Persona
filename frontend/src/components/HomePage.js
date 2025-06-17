import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HomePage = () => {
  const navigate = useNavigate();
  const [isCreating, setIsCreating] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState("multi_source_data");

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
      console.log('Navigating to:', navUrl);
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
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold font-montserrat mb-4 bcm-heading">
            Create Your Data-Driven Persona
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto mb-4">
            Upload your audience data from multiple sources and let our advanced AI create 
            comprehensive, accurate personas with unprecedented insights.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto">
            <p className="text-blue-700 text-sm">
              <strong>🎯 Currently Available:</strong> Multi-source data integration for maximum accuracy. 
              Additional methods will be available when API integrations are ready.
            </p>
          </div>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Multi-Source Data Collection - ONLY OPTION */}
          <div 
            className={`bcm-card relative overflow-hidden cursor-pointer transition-all duration-200 max-w-2xl mx-auto ${
              selectedMethod === 'multi_source_data' ? 'ring-4 ring-purple-500 ring-opacity-50 bg-purple-50' : ''
            }`} 
            onClick={() => handleCardClick("multi_source_data")}
          >
            {/* Featured Badge */}
            <div className="absolute top-0 right-0 bg-purple-600 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">
              ✨ AI-Powered
            </div>
            
            <div className="text-center p-8">
              <div className="mx-auto h-20 w-20 text-purple-600 mb-6">
                <svg fill="currentColor" viewBox="0 0 24 24">
                  <path d="M4,6H2V2H6V4H4V6M2,22V18H4V20H6V22H2M22,2V6H20V4H18V2H22M22,22H18V20H20V18H22V22M8,2H16V4H8V2M2,8H4V16H2V8M20,8H22V16H20V8M8,20H16V22H8V20M10,6H14V8H10V6M6,10H8V14H6V10M16,10H18V14H16V10M10,16H14V18H10V16Z"/>
                </svg>
              </div>
              <h3 className="text-3xl font-bold font-montserrat mb-4 text-gray-800">AI-Powered Data Integration</h3>
              <p className="text-gray-600 font-montserrat text-lg leading-relaxed mb-6">
                Upload data from multiple sources and let our advanced AI create comprehensive, 
                data-driven personas with unprecedented accuracy and insights.
              </p>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="text-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg mx-auto mb-2 flex items-center justify-center">
                    <span className="text-blue-600 font-bold">📊</span>
                  </div>
                  <div className="text-sm font-medium text-gray-700">Resonate</div>
                  <div className="text-xs text-gray-500">Required</div>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-orange-100 rounded-lg mx-auto mb-2 flex items-center justify-center">
                    <span className="text-orange-600 font-bold">🎯</span>
                  </div>
                  <div className="text-sm font-medium text-gray-700">SparkToro</div>
                  <div className="text-xs text-gray-500">Optional</div>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-green-100 rounded-lg mx-auto mb-2 flex items-center justify-center">
                    <span className="text-green-600 font-bold">🔍</span>
                  </div>
                  <div className="text-sm font-medium text-gray-700">SEMRush</div>
                  <div className="text-xs text-gray-500">Optional</div>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg mx-auto mb-2 flex items-center justify-center">
                    <span className="text-purple-600 font-bold">💬</span>
                  </div>
                  <div className="text-sm font-medium text-gray-700">Buzzabout</div>
                  <div className="text-xs text-gray-500">Optional</div>
                </div>
              </div>
              
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 border border-purple-200">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div className="text-center">
                    <div className="font-semibold text-purple-700">🎯 Most Accurate</div>
                    <div className="text-purple-600">Data-driven insights from real audience behavior</div>
                  </div>
                  <div className="text-center">
                    <div className="font-semibold text-blue-700">🤖 AI-Powered</div>
                    <div className="text-blue-600">Advanced AI analysis combining multiple data sources</div>
                  </div>
                  <div className="text-center">
                    <div className="font-semibold text-green-700">📈 Actionable</div>
                    <div className="text-green-600">Ready-to-use marketing insights and strategies</div>
                  </div>
                </div>
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
            disabled={!selectedMethod || isCreating}
          >
            {isCreating ? 'Creating...' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

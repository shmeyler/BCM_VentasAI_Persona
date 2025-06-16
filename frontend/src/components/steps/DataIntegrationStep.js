import React, { useState, useEffect } from 'react';

const DataIntegrationStep = ({ persona, updatePersona, onNext, onPrev, saving, dataSources, dataIntegration, setDataIntegration }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [integrationComplete, setIntegrationComplete] = useState(false);
  const [combinedInsights, setCombinedInsights] = useState(null);

  // Check which data sources are available
  const getAvailableSources = () => {
    const available = [];
    if (dataSources.resonate.uploaded) available.push('Resonate');
    if (dataSources.sparktoro.uploaded) available.push('SparkToro');
    if (dataSources.semrush.uploaded) available.push('SEMRush');
    if (dataSources.buzzabout.uploaded) available.push('Buzzabout.ai');
    return available;
  };

  const processDataIntegration = async () => {
    setIsProcessing(true);
    
    try {
      // Get backend URL from environment
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      // Send all available data sources to backend for integration
      const response = await fetch(`${backendUrl}/api/personas/integrate-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data_sources: dataSources,
          persona_name: persona.name || 'Multi-Source Persona'
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to integrate data sources');
      }

      const result = await response.json();
      
      if (result.success) {
        setCombinedInsights(result.combined_insights);
        setDataIntegration({
          processed: true,
          combinedInsights: result.combined_insights,
          aiPrompt: result.ai_prompt
        });
        setIntegrationComplete(true);
      } else {
        throw new Error(result.message || 'Failed to integrate data');
      }
      
    } catch (error) {
      console.error('Error integrating data sources:', error);
      alert(`Error integrating data: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  useEffect(() => {
    // Auto-start integration if we have Resonate data (required)
    if (dataSources.resonate.uploaded && !dataIntegration.processed && !isProcessing) {
      processDataIntegration();
    }
  }, [dataSources, dataIntegration.processed]);

  const availableSources = getAvailableSources();
  const totalSources = availableSources.length;
  const requiredMet = dataSources.resonate.uploaded;

  return (
    <div className="form-section">
      <div className="mb-8">
        <h2 className="text-2xl font-bold font-montserrat mb-3 bcm-heading">
          🔄 Data Integration & Analysis
        </h2>
        <p className="text-gray-600 font-montserrat mb-4">
          We're combining and analyzing data from all your uploaded sources to create 
          comprehensive audience insights for AI-powered persona generation.
        </p>
      </div>

      {/* Data Sources Summary */}
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold mb-4 font-montserrat">📊 Available Data Sources</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Resonate */}
          <div className={`flex items-center p-3 rounded-lg ${
            dataSources.resonate.uploaded ? 'bg-green-50 border border-green-200' : 'bg-gray-50 border border-gray-200'
          }`}>
            <div className={`w-4 h-4 rounded-full mr-3 ${
              dataSources.resonate.uploaded ? 'bg-green-500' : 'bg-gray-300'
            }`}></div>
            <div>
              <div className="font-medium">Resonate</div>
              <div className="text-sm text-gray-600">
                {dataSources.resonate.uploaded ? 'Demographics & Media Consumption' : 'Required - Not uploaded'}
              </div>
            </div>
          </div>

          {/* SparkToro */}
          <div className={`flex items-center p-3 rounded-lg ${
            dataSources.sparktoro.uploaded ? 'bg-green-50 border border-green-200' : 'bg-gray-50 border border-gray-200'
          }`}>
            <div className={`w-4 h-4 rounded-full mr-3 ${
              dataSources.sparktoro.uploaded ? 'bg-green-500' : 'bg-gray-300'
            }`}></div>
            <div>
              <div className="font-medium">SparkToro</div>
              <div className="text-sm text-gray-600">
                {dataSources.sparktoro.uploaded ? 'Audience Research & Social Behavior' : 'Optional - Not uploaded'}
              </div>
            </div>
          </div>

          {/* SEMRush */}
          <div className={`flex items-center p-3 rounded-lg ${
            dataSources.semrush.uploaded ? 'bg-green-50 border border-green-200' : 'bg-gray-50 border border-gray-200'
          }`}>
            <div className={`w-4 h-4 rounded-full mr-3 ${
              dataSources.semrush.uploaded ? 'bg-green-500' : 'bg-gray-300'
            }`}></div>
            <div>
              <div className="font-medium">SEMRush</div>
              <div className="text-sm text-gray-600">
                {dataSources.semrush.uploaded ? 'Search Behavior & Keywords' : 'Optional - Not uploaded'}
              </div>
            </div>
          </div>

          {/* Buzzabout.ai */}
          <div className={`flex items-center p-3 rounded-lg ${
            dataSources.buzzabout.uploaded ? 'bg-green-50 border border-green-200' : 'bg-gray-50 border border-gray-200'
          }`}>
            <div className={`w-4 h-4 rounded-full mr-3 ${
              dataSources.buzzabout.uploaded ? 'bg-green-500' : 'bg-gray-300'
            }`}></div>
            <div>
              <div className="font-medium">Buzzabout.ai</div>
              <div className="text-sm text-gray-600">
                {dataSources.buzzabout.uploaded ? 'Social Sentiment & Trends' : 'Optional - Not uploaded'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Integration Status */}
      {isProcessing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <div className="flex items-center mb-4">
            <div className="loading-spinner mr-3"></div>
            <div>
              <div className="text-blue-800 font-semibold">Integrating Data Sources...</div>
              <div className="text-blue-700 text-sm">Analyzing and combining insights from {totalSources} data source{totalSources > 1 ? 's' : ''}</div>
            </div>
          </div>
          
          <div className="space-y-2">
            <div className="text-sm text-blue-700">• Extracting demographic patterns</div>
            <div className="text-sm text-blue-700">• Analyzing media consumption behavior</div>
            <div className="text-sm text-blue-700">• Identifying search and content preferences</div>
            <div className="text-sm text-blue-700">• Correlating social sentiment and trends</div>
            <div className="text-sm text-blue-700">• Preparing comprehensive AI prompt</div>
          </div>
        </div>
      )}

      {/* Integration Complete */}
      {integrationComplete && combinedInsights && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
          <h3 className="text-green-800 font-semibold mb-3">✅ Data Integration Complete</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-700">{totalSources}</div>
              <div className="text-sm text-green-600">Data Sources Integrated</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-700">
                {combinedInsights.demographic_insights ? Object.keys(combinedInsights.demographic_insights).length : 0}
              </div>
              <div className="text-sm text-green-600">Demographic Insights</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-700">
                {combinedInsights.behavioral_patterns ? combinedInsights.behavioral_patterns.length : 0}
              </div>
              <div className="text-sm text-green-600">Behavioral Patterns</div>
            </div>
          </div>

          <div className="text-green-700 text-sm">
            Your data has been successfully analyzed and prepared for AI persona generation. 
            The system has identified key demographic patterns, behavioral insights, and content preferences 
            that will be used to create a comprehensive, data-driven persona.
          </div>
        </div>
      )}

      {/* Error State */}
      {!requiredMet && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
          <h3 className="text-yellow-800 font-semibold mb-2">⚠️ Missing Required Data</h3>
          <div className="text-yellow-700 text-sm">
            Resonate data is required to proceed. Please go back and upload your Resonate files.
          </div>
        </div>
      )}

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        <button
          onClick={onPrev}
          className="bcm-btn-outline"
        >
          ← Previous
        </button>
        
        <button
          onClick={onNext}
          disabled={!integrationComplete || isProcessing}
          className="bcm-btn-primary"
        >
          {integrationComplete ? "Continue to AI Persona Generation →" : "Processing..."}
        </button>
      </div>
    </div>
  );
};

export default DataIntegrationStep;
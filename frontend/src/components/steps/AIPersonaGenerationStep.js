import React, { useState } from 'react';

const AIPersonaGenerationStep = ({ persona, updatePersona, onNext, onPrev, saving, dataSources, dataIntegration }) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationComplete, setGenerationComplete] = useState(false);
  const [generatedPersona, setGeneratedPersona] = useState(null);
  const [generationError, setGenerationError] = useState(null);

  const startAIGeneration = async () => {
    setIsGenerating(true);
    setGenerationError(null);
    
    try {
      // Get backend URL from environment
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      // Send persona ID directly to the existing generate endpoint
      const response = await fetch(`${backendUrl}/api/personas/${persona.id}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          use_multi_source_data: true
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate AI persona');
      }

      const result = await response.json();
      
      setGeneratedPersona(result);
      setGenerationComplete(true);
      
      // Update the main persona to mark as AI generated
      await updatePersona({
        ai_generated: true,
        data_sources_used: Object.keys(dataSources).filter(key => dataSources[key].uploaded),
        generation_timestamp: new Date().toISOString()
      }, null);
      
    } catch (error) {
      console.error('Error generating AI persona:', error);
      setGenerationError(`Generation failed: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const getDataSourcesSummary = () => {
    const sources = [];
    if (dataSources.resonate.uploaded) sources.push('Resonate Demographics');
    if (dataSources.sparktoro.uploaded) sources.push('SparkToro Audience Research');
    if (dataSources.semrush.uploaded) sources.push('SEMRush Search Behavior');
    if (dataSources.buzzabout.uploaded) sources.push('Buzzabout.ai Social Sentiment');
    return sources;
  };

  const dataSummary = getDataSourcesSummary();

  return (
    <div className="form-section">
      <div className="mb-8">
        <h2 className="text-2xl font-bold font-montserrat mb-3 bcm-heading">
          🤖 AI Persona Generation
        </h2>
        <p className="text-gray-600 font-montserrat mb-4">
          Generate a comprehensive, data-driven persona using advanced AI analysis 
          of your uploaded data sources and integrated insights.
        </p>
      </div>

      {/* Data Sources Used */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold text-blue-800 mb-3">📊 Data Sources for AI Generation</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {dataSummary.map((source, index) => (
            <div key={index} className="flex items-center">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
              <span className="text-blue-700 text-sm">{source}</span>
            </div>
          ))}
        </div>
        <div className="mt-3 text-blue-600 text-sm">
          <strong>Total Data Points:</strong> {dataSummary.length} integrated source{dataSummary.length > 1 ? 's' : ''}
        </div>
      </div>

      {/* AI Generation Process */}
      {!isGenerating && !generationComplete && !generationError && (
        <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
          <h3 className="font-semibold mb-4 font-montserrat">🎯 AI Persona Generation Process</h3>
          <div className="space-y-3 text-sm text-gray-600 mb-6">
            <div className="flex items-start">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3 mt-2"></div>
              <div>
                <strong>Demographic Analysis:</strong> Extract age, gender, location, income, and lifestyle patterns from integrated data
              </div>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3 mt-2"></div>
              <div>
                <strong>Behavioral Insights:</strong> Analyze media consumption, social behavior, and digital engagement patterns
              </div>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3 mt-2"></div>
              <div>
                <strong>Content Preferences:</strong> Identify search patterns, content interests, and information consumption habits
              </div>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3 mt-2"></div>
              <div>
                <strong>Motivational Drivers:</strong> Understand values, goals, pain points, and decision-making factors
              </div>
            </div>
            <div className="flex items-start">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3 mt-2"></div>
              <div>
                <strong>Visual Generation:</strong> Create realistic AI-generated persona imagery based on demographic data
              </div>
            </div>
          </div>

          <button
            onClick={startAIGeneration}
            className="w-full bcm-btn-primary py-3 text-lg"
          >
            🚀 Generate AI-Powered Persona
          </button>
        </div>
      )}

      {/* Generation in Progress */}
      {isGenerating && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <div className="flex items-center mb-4">
            <div className="loading-spinner mr-3"></div>
            <div>
              <div className="text-blue-800 font-semibold">Generating AI Persona...</div>
              <div className="text-blue-700 text-sm">Using advanced AI to analyze your data and create comprehensive persona</div>
            </div>
          </div>
          
          <div className="space-y-2">
            <div className="text-sm text-blue-700">• Processing demographic patterns and behavioral insights</div>
            <div className="text-sm text-blue-700">• Analyzing content preferences and digital engagement</div>
            <div className="text-sm text-blue-700">• Identifying motivational drivers and pain points</div>
            <div className="text-sm text-blue-700">• Generating personality traits and communication style</div>
            <div className="text-sm text-blue-700">• Creating realistic persona imagery</div>
            <div className="text-sm text-blue-700">• Finalizing comprehensive persona profile</div>
          </div>
        </div>
      )}

      {/* Generation Complete */}
      {generationComplete && generatedPersona && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
          <h3 className="text-green-800 font-semibold mb-3">✅ AI Persona Generation Complete!</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-700">100%</div>
              <div className="text-sm text-green-600">Data Integration</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-700">{dataSummary.length}</div>
              <div className="text-sm text-green-600">Sources Analyzed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-700">AI</div>
              <div className="text-sm text-green-600">Generated Insights</div>
            </div>
          </div>

          <div className="bg-white rounded-lg p-4 mb-4">
            <h4 className="font-semibold mb-2">👤 Generated Persona Preview</h4>
            <div className="text-sm text-gray-600">
              <strong>Name:</strong> {generatedPersona.name || 'AI-Generated Persona'}<br/>
              <strong>Demographics:</strong> Based on {dataSummary.join(', ')}<br/>
              <strong>Key Insights:</strong> Comprehensive behavioral patterns and motivational drivers identified
            </div>
          </div>

          <div className="text-green-700 text-sm">
            Your AI-powered persona has been successfully generated with rich insights from all your data sources. 
            This persona includes detailed demographics, behavioral patterns, content preferences, and actionable marketing insights.
          </div>
        </div>
      )}

      {/* Generation Error */}
      {generationError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
          <h3 className="text-red-800 font-semibold mb-2">❌ Generation Error</h3>
          <div className="text-red-700 text-sm mb-4">{generationError}</div>
          <button
            onClick={startAIGeneration}
            className="bcm-btn-primary"
          >
            Try Again
          </button>
        </div>
      )}

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        <button
          onClick={onPrev}
          className="bcm-btn-outline"
          disabled={isGenerating}
        >
          ← Previous
        </button>
        
        <button
          onClick={onNext}
          disabled={!generationComplete || isGenerating}
          className="bcm-btn-primary"
        >
          {generationComplete ? "View Generated Persona →" : "Generating..."}
        </button>
      </div>
    </div>
  );
};

export default AIPersonaGenerationStep;
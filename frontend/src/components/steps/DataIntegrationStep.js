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
          persona_name: persona.name || 'Multi-Source Persona',
          persona_id: persona.id
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
    
    // If we have persona data with demographics, consider integration complete
    if (persona && persona.demographics && persona.demographics.age_range && !integrationComplete) {
      const demographicData = {};
      
      if (persona.demographics.age_range) demographicData.age = [persona.demographics.age_range];
      if (persona.demographics.gender) demographicData.gender = [persona.demographics.gender];
      if (persona.demographics.income_range) demographicData.income = [persona.demographics.income_range];
      if (persona.demographics.location) demographicData.location = [persona.demographics.location];
      if (persona.demographics.occupation) demographicData.occupation = [persona.demographics.occupation];
      if (persona.demographics.education) demographicData.education = [persona.demographics.education];
      
      const mockInsights = {
        total_sources: 1,
        demographic_insights: demographicData,
        behavioral_patterns: persona.media_consumption?.social_media_platforms || [],
        data_quality: "High"
      };
      
      setCombinedInsights(mockInsights);
      setDataIntegration({
        processed: true,
        combinedInsights: mockInsights,
        aiPrompt: "Using uploaded demographic data for persona generation"
      });
      setIntegrationComplete(true);
    }
  }, [dataSources, dataIntegration.processed, persona, integrationComplete]);

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
        <div className="mt-6 p-6 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📊 Complete Data Summary</h3>
          
          {/* Data Sources Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-700">
                {(() => {
                  // Count actual demographic data from persona
                  let count = 0;
                  if (persona && persona.demographics) {
                    const demo = persona.demographics;
                    if (demo.age_range) count++;
                    if (demo.gender) count++;
                    if (demo.income_range) count++;
                    if (demo.location) count++;
                    if (demo.occupation) count++;
                    if (demo.education) count++;
                  }
                  // Fallback to combinedInsights if persona data isn't available
                  if (count === 0 && combinedInsights.demographic_insights) {
                    count = Object.keys(combinedInsights.demographic_insights).length;
                  }
                  return count;
                })()}
              </div>
              <div className="text-sm text-green-600">Demographic Insights</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-700">
                {combinedInsights.behavioral_patterns ? combinedInsights.behavioral_patterns.length : (persona?.media_consumption?.social_media_platforms?.length || 0)}
              </div>
              <div className="text-sm text-blue-600">Behavioral Patterns</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-700">
                {combinedInsights.total_sources || Object.keys(dataSources).filter(key => dataSources[key].uploaded).length}
              </div>
              <div className="text-sm text-purple-600">Data Sources</div>
            </div>
          </div>
          
          {/* Detailed Data Breakdown */}
          <div className="space-y-4">
            {/* SparkToro Data Summary */}
            {dataSources.sparktoro?.uploaded && dataSources.sparktoro?.data?.categories && (
              <div className="bg-white p-4 rounded border">
                <h4 className="font-semibold text-green-800 mb-2">🎯 SparkToro Audience Research</h4>
                <div className="text-sm text-gray-700">
                  <span className="font-medium">{Object.keys(dataSources.sparktoro.data.categories).length} categories analyzed:</span>
                  <div className="mt-1 flex flex-wrap gap-1">
                    {Object.keys(dataSources.sparktoro.data.categories).slice(0, 6).map((cat, idx) => (
                      <span key={idx} className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                        {cat}
                      </span>
                    ))}
                    {Object.keys(dataSources.sparktoro.data.categories).length > 6 && (
                      <span className="text-green-600 text-xs">+{Object.keys(dataSources.sparktoro.data.categories).length - 6} more</span>
                    )}
                  </div>
                </div>
              </div>
            )}
            
            {/* SEMRush Data Summary */}
            {dataSources.semrush?.uploaded && dataSources.semrush?.data?.keyword_data && (
              <div className="bg-white p-4 rounded border">
                <h4 className="font-semibold text-blue-800 mb-2">🔍 SEMRush Search Behavior</h4>
                <div className="text-sm text-gray-700">
                  <span className="font-medium">{Object.keys(dataSources.semrush.data.keyword_data).length} keyword datasets:</span>
                  {(() => {
                    const allKeywords = [];
                    Object.values(dataSources.semrush.data.keyword_data).forEach(sheet => {
                      if (sheet.keywords) {
                        Object.values(sheet.keywords).forEach(keywords => {
                          allKeywords.push(...keywords.slice(0, 3));
                        });
                      }
                    });
                    
                    return allKeywords.length > 0 ? (
                      <div className="mt-1 text-xs text-blue-700">
                        Sample keywords: {allKeywords.slice(0, 5).join(', ')}...
                      </div>
                    ) : null;
                  })()}
                </div>
              </div>
            )}
            
            {/* Buzzabout Data Summary */}
            {dataSources.buzzabout?.uploaded && dataSources.buzzabout?.data?.social_sentiment && (
              <div className="bg-white p-4 rounded border">
                <h4 className="font-semibold text-purple-800 mb-2">💬 Buzzabout Social Sentiment</h4>
                <div className="text-sm text-gray-700">
                  {dataSources.buzzabout.data.social_sentiment.trending_topics?.length > 0 && (
                    <div>
                      <span className="font-medium">Trending topics:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {dataSources.buzzabout.data.social_sentiment.trending_topics.slice(0, 5).map((topic, idx) => (
                          <span key={idx} className="inline-block bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
            
            {/* Resonate Data Summary */}
            {dataSources.resonate?.uploaded && (
              <div className="bg-white p-4 rounded border">
                <h4 className="font-semibold text-orange-800 mb-2">👥 Resonate Demographics</h4>
                <div className="text-sm text-gray-700">
                  <div className="grid grid-cols-2 gap-2">
                    {persona?.demographics?.age_range && (
                      <span><span className="font-medium">Age:</span> {persona.demographics.age_range}</span>
                    )}
                    {persona?.demographics?.gender && (
                      <span><span className="font-medium">Gender:</span> {persona.demographics.gender}</span>
                    )}
                    {persona?.demographics?.occupation && (
                      <span><span className="font-medium">Occupation:</span> {persona.demographics.occupation}</span>
                    )}
                    {persona?.demographics?.location && (
                      <span><span className="font-medium">Location:</span> {persona.demographics.location}</span>
                    )}
                  </div>
                  {persona?.media_consumption?.social_media_platforms?.length > 0 && (
                    <div className="mt-2">
                      <span className="font-medium">Platforms:</span> {persona.media_consumption.social_media_platforms.join(', ')}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
          
          <div className="mt-4 p-3 bg-gradient-to-r from-green-100 to-blue-100 rounded text-center">
            <p className="text-sm font-medium text-gray-800">
              🚀 All data collected and ready for AI-powered persona generation
            </p>
            <p className="text-xs text-gray-600 mt-1">
              This comprehensive dataset will be used to create detailed, personalized insights
            </p>
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
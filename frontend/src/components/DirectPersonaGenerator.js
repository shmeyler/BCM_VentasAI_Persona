import React, { useState } from 'react';

const DirectPersonaGenerator = () => {
  const [personaName, setPersonaName] = useState('');
  const [sparkToroFile, setSparkToroFile] = useState(null);
  const [semrushFile, setSemrushFile] = useState(null);
  const [buzzaboutUrl, setBuzzaboutUrl] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!personaName.trim()) {
      setError('Please enter a persona name');
      return;
    }

    if (!sparkToroFile && !semrushFile && !buzzaboutUrl.trim()) {
      setError('Please upload at least one data source');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('persona_name', personaName);
      
      if (sparkToroFile) {
        formData.append('sparktoro_file', sparkToroFile);
      }
      
      if (semrushFile) {
        formData.append('semrush_file', semrushFile);
      }
      
      if (buzzaboutUrl.trim()) {
        formData.append('buzzabout_url', buzzaboutUrl);
      }

      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/personas/direct-generate`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Generation failed');
      }
    } catch (err) {
      setError(`Network error: ${err.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🚀 Direct Persona Generator
        </h1>
        <p className="text-gray-600">
          Upload your data files and generate a persona instantly using real data
        </p>
      </div>

      {/* Input Form */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="space-y-6">
          {/* Persona Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Persona Name *
            </label>
            <input
              type="text"
              value={personaName}
              onChange={(e) => setPersonaName(e.target.value)}
              placeholder="e.g., Tech-Savvy Millennials"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* File Uploads */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* SparkToro File */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📊 SparkToro Excel File
              </label>
              <input
                type="file"
                accept=".xlsx,.xls"
                onChange={(e) => setSparkToroFile(e.target.files[0])}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              />
              {sparkToroFile && (
                <p className="text-xs text-green-600 mt-1">✓ {sparkToroFile.name}</p>
              )}
            </div>

            {/* SEMRush File */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🔍 SEMRush CSV File
              </label>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setSemrushFile(e.target.files[0])}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {semrushFile && (
                <p className="text-xs text-blue-600 mt-1">✓ {semrushFile.name}</p>
              )}
            </div>
          </div>

          {/* Buzzabout URL */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🔗 Buzzabout.ai Report URL
            </label>
            <input
              type="url"
              value={buzzaboutUrl}
              onChange={(e) => setBuzzaboutUrl(e.target.value)}
              placeholder="https://app.buzzabout.ai/share/..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={isGenerating}
            className={`w-full py-3 px-4 rounded-md font-medium flex items-center justify-center space-x-2 ${
              isGenerating
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white'
            }`}
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Generating Persona...</span>
              </>
            ) : (
              <>
                <span>✨</span>
                <span>Generate Persona with Real Data</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <span className="text-red-500 mr-2">⚠️</span>
            <span className="text-red-800">{error}</span>
          </div>
        </div>
      )}

      {/* Results Display */}
      {result && result.success && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Generated Persona: {result.persona_name}
          </h2>
          
          {/* Data Sources Used */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">Data Sources Processed:</h3>
            <div className="flex space-x-4 text-sm">
              {result.data_sources_processed.sparktoro && (
                <span className="px-2 py-1 bg-green-100 text-green-800 rounded">✓ SparkToro</span>
              )}
              {result.data_sources_processed.semrush && (
                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">✓ SEMRush</span>
              )}
              {result.data_sources_processed.buzzabout && (
                <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded">✓ Buzzabout</span>
              )}
            </div>
            <p className="text-xs text-gray-600 mt-1">
              Prompt size: {result.prompt_size} characters
            </p>
          </div>

          {/* Generated Persona Data */}
          {result.generated_persona && (
            <div className="space-y-6">
              {/* Personality Traits */}
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">🎯 Personality Traits</h3>
                <div className="flex flex-wrap gap-2">
                  {result.generated_persona.personality_traits?.map((trait, idx) => (
                    <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                      {trait}
                    </span>
                  ))}
                </div>
              </div>

              {/* Shopping Behavior */}
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">🛒 Shopping Behavior</h3>
                <p className="text-gray-700">{result.generated_persona.shopping_behavior}</p>
              </div>

              {/* Decision Factors */}
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">⚖️ Decision Factors</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {result.generated_persona.decision_factors?.map((factor, idx) => (
                    <li key={idx}>{factor}</li>
                  ))}
                </ul>
              </div>

              {/* Digital Behavior */}
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">💻 Digital Behavior</h3>
                <p className="text-gray-700">{result.generated_persona.digital_behavior}</p>
              </div>

              {/* Recommendations */}
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">📈 Marketing Recommendations</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {result.generated_persona.recommendations?.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
              </div>

              {/* Pain Points */}
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">😤 Pain Points</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {result.generated_persona.pain_points?.map((pain, idx) => (
                    <li key={idx}>{pain}</li>
                  ))}
                </ul>
              </div>

              {/* Goals */}
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">🎯 Goals</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {result.generated_persona.goals?.map((goal, idx) => (
                    <li key={idx}>{goal}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DirectPersonaGenerator;
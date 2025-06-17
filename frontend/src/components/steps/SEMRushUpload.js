import React, { useState } from 'react';

const SEMRushUpload = ({ persona, updatePersona, onNext, onPrev, saving, dataSources, setDataSources }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [parsedData, setParsedData] = useState(null);
  const [uploadError, setUploadError] = useState(null);

  const handleFileUpload = async (file) => {
    if (!file) return;

    setIsProcessing(true);
    setUploadError(null);
    
    try {
      // Create FormData to send the file
      const formData = new FormData();
      formData.append('file', file);

      // Get backend URL from environment
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      const response = await fetch(`${backendUrl}/api/personas/semrush-upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = 'Failed to process SEMRush file';
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) {
          errorMessage = `Server error (${response.status}): ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      const result = await response.json();
      
      if (result.success) {
        setParsedData(result.parsed_data);
        setUploadedFile(file);
        
        // Update data sources state
        setDataSources(prev => ({
          ...prev,
          semrush: {
            uploaded: true,
            data: result.parsed_data,
            required: false
          }
        }));
        
        // Save SEMRush data to the persona
        await updatePersona({
          semrush_data: result.parsed_data
        }, null);
        
      } else {
        throw new Error(result.message || 'Failed to process SEMRush file');
      }
      
    } catch (error) {
      console.error('Error processing SEMRush file:', error);
      setUploadError(`Error processing file: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSkip = () => {
    // Mark as skipped and proceed
    setDataSources(prev => ({
      ...prev,
      semrush: {
        uploaded: false,
        data: null,
        required: false,
        skipped: true
      }
    }));
    onNext();
  };

  const handleNext = () => {
    if (parsedData) {
      // Update persona with SEMRush data if available
      updatePersona({ semrush_data: parsedData }, null);
    }
    onNext();
  };

  return (
    <div className="form-section">
      <div className="mb-8">
        <h2 className="text-2xl font-bold font-montserrat mb-3 bcm-heading">
          🔍 SEMRush Search Behavior Data
        </h2>
        <p className="text-gray-600 font-montserrat mb-4">
          Upload your SEMRush keyword and search behavior exports to understand your 
          audience's search patterns, content interests, and competitive landscape insights.
        </p>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-blue-800 mb-2">📋 What to Upload:</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• <strong>Keyword Research Reports</strong> - Search terms and volume data</li>
            <li>• <strong>Competitor Analysis</strong> - Content gaps and opportunities</li>
            <li>• <strong>Content Audit</strong> - Top performing pages and topics</li>
            <li>• <strong>Search Intent Analysis</strong> - Query types and user behavior</li>
          </ul>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-yellow-800 mb-2">📁 Accepted Formats:</h3>
          <div className="text-sm text-yellow-700">
            CSV, Excel (.xlsx, .xls) - Export from SEMRush dashboard reports
          </div>
        </div>
      </div>

      {/* File Upload Area */}
      <div className="mb-6">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <input
            type="file"
            id="semrush-file-upload"
            className="hidden"
            accept=".csv,.xlsx,.xls"
            onChange={(e) => handleFileUpload(e.target.files[0])}
            disabled={isProcessing}
          />
          <label 
            htmlFor="semrush-file-upload" 
            className={`cursor-pointer ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <div className="text-gray-500 mb-2">
              🔍 <span className="font-semibold">Upload SEMRush Data</span>
            </div>
            <div className="text-sm text-gray-400">
              Click to browse or drag and drop your SEMRush export files
            </div>
          </label>
        </div>
      </div>

      {/* Error Display */}
      {uploadError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="text-red-800 font-semibold mb-2">Upload Error</div>
          <div className="text-red-700 text-sm">{uploadError}</div>
        </div>
      )}

      {/* Processing State */}
      {isProcessing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <div className="loading-spinner mr-3"></div>
            <div>
              <div className="text-blue-800 font-semibold">Processing SEMRush Data...</div>
              <div className="text-blue-700 text-sm">Analyzing search behavior and keyword patterns</div>
            </div>
          </div>
        </div>
      )}

      {/* Success State */}
      {parsedData && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <h3 className="text-green-800 font-semibold mb-2">✅ SEMRush Data Processed Successfully</h3>
          <div className="text-green-700 text-sm">
            Extracted search behavior patterns, keyword interests, and content preferences from your SEMRush data.
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
        
        <div className="space-x-3">
          <button
            onClick={handleSkip}
            className="px-4 py-2 border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50 font-montserrat"
          >
            Skip SEMRush Data
          </button>
          
          <button
            onClick={handleNext}
            disabled={isProcessing}
            className="bcm-btn-primary"
          >
            {parsedData ? "Continue with SEMRush Data →" : "Continue without SEMRush →"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SEMRushUpload;
import React, { useState } from 'react';

const SparkToroUpload = ({ persona, updatePersona, onNext, onPrev, saving, dataSources, setDataSources }) => {
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
      
      const response = await fetch(`${backendUrl}/api/personas/sparktoro-upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = 'Failed to process SparkToro file';
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
          sparktoro: {
            uploaded: true,
            data: result.parsed_data,
            required: false
          }
        }));
      } else {
        throw new Error(result.message || 'Failed to process SparkToro file');
      }
      
    } catch (error) {
      console.error('Error processing SparkToro file:', error);
      setUploadError(`Error processing file: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSkip = () => {
    // Mark as skipped and proceed
    setDataSources(prev => ({
      ...prev,
      sparktoro: {
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
      // Update persona with SparkToro data if available
      updatePersona({ sparktoro_data: parsedData }, null);
    }
    onNext();
  };

  return (
    <div className="form-section">
      <div className="mb-8">
        <h2 className="text-2xl font-bold font-montserrat mb-3 bcm-heading">
          📊 SparkToro Audience Research Data
        </h2>
        <p className="text-gray-600 font-montserrat mb-4">
          Upload your SparkToro audience research export to enhance persona insights with 
          audience demographics, social media behavior, and website preferences.
        </p>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-blue-800 mb-2">📋 What to Upload:</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• <strong>Audience Research Reports</strong> - Demographics and psychographics</li>
            <li>• <strong>Social Media Analysis</strong> - Platform usage and engagement</li>
            <li>• <strong>Website/Domain Reports</strong> - Content preferences and online behavior</li>
            <li>• <strong>Influencer Data</strong> - Followed accounts and thought leaders</li>
          </ul>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-yellow-800 mb-2">📁 Accepted Formats:</h3>
          <div className="text-sm text-yellow-700">
            CSV, Excel (.xlsx, .xls), JSON - Export from SparkToro dashboard
          </div>
        </div>
      </div>

      {/* File Upload Area */}
      <div className="mb-6">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <input
            type="file"
            id="sparktoro-file-upload"
            className="hidden"
            accept=".csv,.xlsx,.xls,.json"
            onChange={(e) => handleFileUpload(e.target.files[0])}
            disabled={isProcessing}
          />
          <label 
            htmlFor="sparktoro-file-upload" 
            className={`cursor-pointer ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <div className="text-gray-500 mb-2">
              📊 <span className="font-semibold">Upload SparkToro Data</span>
            </div>
            <div className="text-sm text-gray-400">
              Click to browse or drag and drop your SparkToro export files
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
              <div className="text-blue-800 font-semibold">Processing SparkToro Data...</div>
              <div className="text-blue-700 text-sm">Analyzing audience insights and social behavior</div>
            </div>
          </div>
        </div>
      )}

      {/* Success State */}
      {parsedData && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <h3 className="text-green-800 font-semibold mb-2">✅ SparkToro Data Processed Successfully</h3>
          <div className="text-green-700 text-sm">
            Extracted audience demographics, social behavior, and content preferences from your SparkToro data.
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
            Skip SparkToro Data
          </button>
          
          <button
            onClick={handleNext}
            disabled={isProcessing}
            className="bcm-btn-primary"
          >
            {parsedData ? "Continue with SparkToro Data →" : "Continue without SparkToro →"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SparkToroUpload;
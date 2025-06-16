import React, { useState } from 'react';

const BuzzAboutUpload = ({ persona, updatePersona, onNext, onPrev, saving, dataSources, setDataSources }) => {
  const [reportUrl, setReportUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [parsedData, setParsedData] = useState(null);
  const [uploadError, setUploadError] = useState(null);

  const handleUrlSubmit = async () => {
    if (!reportUrl.trim()) {
      setUploadError('Please enter a valid Buzzabout.ai report URL');
      return;
    }

    setIsProcessing(true);
    setUploadError(null);
    
    try {
      // Get backend URL from environment
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      const response = await fetch(`${backendUrl}/api/personas/buzzabout-crawl`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          report_url: reportUrl.trim()
        }),
      });

      if (!response.ok) {
        let errorMessage = 'Failed to process Buzzabout.ai URL';
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
        
        // Update data sources state
        setDataSources(prev => ({
          ...prev,
          buzzabout: {
            uploaded: true,
            data: result.parsed_data,
            required: false,
            source_url: reportUrl.trim()
          }
        }));
      } else {
        throw new Error(result.message || 'Failed to process Buzzabout.ai URL');
      }
      
    } catch (error) {
      console.error('Error processing Buzzabout.ai URL:', error);
      setUploadError(`Error processing URL: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSkip = () => {
    // Mark as skipped and proceed
    setDataSources(prev => ({
      ...prev,
      buzzabout: {
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
      // Update persona with Buzzabout.ai data if available
      updatePersona({ buzzabout_data: parsedData }, null);
    }
    onNext();
  };

  return (
    <div className="form-section">
      <div className="mb-8">
        <h2 className="text-2xl font-bold font-montserrat mb-3 bcm-heading">
          💬 Buzzabout.ai Social Sentiment Data
        </h2>
        <p className="text-gray-600 font-montserrat mb-4">
          Enter your Buzzabout.ai report URL and we'll crawl the social sentiment and trend analysis data 
          to understand your audience's social conversations, brand perceptions, and emerging topics.
        </p>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-blue-800 mb-2">📋 What We'll Extract:</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• <strong>Social Sentiment Reports</strong> - Brand and topic sentiment analysis</li>
            <li>• <strong>Trend Analysis</strong> - Emerging topics and conversation patterns</li>
            <li>• <strong>Influencer Insights</strong> - Key voices and opinion leaders</li>
            <li>• <strong>Conversation Themes</strong> - Popular discussion topics and keywords</li>
          </ul>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-yellow-800 mb-2">🔗 How to Get Your Report URL:</h3>
          <div className="text-sm text-yellow-700 space-y-1">
            <div>1. Go to your Buzzabout.ai dashboard</div>
            <div>2. Generate or open your audience sentiment report</div>
            <div>3. Copy the report URL from your browser address bar</div>
            <div>4. Paste the URL below</div>
          </div>
        </div>
      </div>

      {/* URL Input Area */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Buzzabout.ai Report URL
        </label>
        <div className="flex gap-3">
          <input
            type="url"
            value={reportUrl}
            onChange={(e) => setReportUrl(e.target.value)}
            placeholder="https://buzzabout.ai/reports/your-report-id"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            disabled={isProcessing}
          />
          <button
            onClick={handleUrlSubmit}
            disabled={isProcessing || !reportUrl.trim()}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {isProcessing ? 'Crawling...' : 'Process URL'}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {uploadError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="text-red-800 font-semibold mb-2">Processing Error</div>
          <div className="text-red-700 text-sm">{uploadError}</div>
        </div>
      )}

      {/* Processing State */}
      {isProcessing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <div className="loading-spinner mr-3"></div>
            <div>
              <div className="text-blue-800 font-semibold">Crawling Buzzabout.ai Report...</div>
              <div className="text-blue-700 text-sm">Analyzing social sentiment and conversation trends</div>
            </div>
          </div>
        </div>
      )}

      {/* Success State */}
      {parsedData && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <h3 className="text-green-800 font-semibold mb-2">✅ Buzzabout.ai Data Processed Successfully</h3>
          <div className="text-green-700 text-sm mb-3">
            Extracted social sentiment, conversation themes, and trend insights from your Buzzabout.ai report.
          </div>
          <div className="text-xs text-green-600 break-all">
            <strong>Source:</strong> {reportUrl}
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
            Skip Buzzabout.ai Data
          </button>
          
          <button
            onClick={handleNext}
            disabled={isProcessing}
            className="bcm-btn-primary"
          >
            {parsedData ? "Continue with Buzzabout.ai Data →" : "Continue without Buzzabout.ai →"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default BuzzAboutUpload;
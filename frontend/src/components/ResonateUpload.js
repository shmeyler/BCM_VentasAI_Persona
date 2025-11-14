import React, { useState } from 'react';

const ResonateUpload = ({ persona, updatePersona, onNext, onPrev, saving, dataSources, setDataSources }) => {
  const [uploadedZip, setUploadedZip] = useState(null);
  const [extractedFiles, setExtractedFiles] = useState([]);
  const [parsedData, setParsedData] = useState(null);
  const [showFilePreview, setShowFilePreview] = useState(false);
  const [showDataPreview, setShowDataPreview] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const zipRequirements = {
    maxSize: '100MB',
    accept: '.zip',
    expectedFiles: [
      'Demographics data (PNG, PDF, CSV, XLS)',
      'Audience insights (any format)',
      'Category/Brand affinity data',
      'Media consumption analysis',
      'Personal values & motivations',
      'Research presentations',
      'Supporting charts and visualizations'
    ]
  };

  const processZipFile = async (zipFile) => {
    setIsProcessing(true);
    setShowFilePreview(false);
    setShowDataPreview(false);
    setUploadError(null);
    
    try {
      // Create FormData to send the file
      const formData = new FormData();
      formData.append('file', zipFile);

      // Get backend URL from environment (default to local for development)
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      
      // Call real backend API to process the ZIP file
      const response = await fetch(`${backendUrl}/api/personas/resonate-upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = 'Failed to process ZIP file';
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
        // Set extracted files and parsed data from real backend response
        setExtractedFiles(result.extracted_files || []);
        setParsedData(result.parsed_data || {});
        setShowFilePreview(true);
        setShowDataPreview(true); // Show data preview directly since we have parsed data
        
        // Update dataSources state to mark Resonate as uploaded
        if (setDataSources) {
          setDataSources(prevSources => ({
            ...prevSources,
            resonate: {
              uploaded: true,
              data: result.parsed_data || {},
              required: true
            }
          }));
        }
      } else {
        throw new Error(result.message || 'Failed to process ZIP file');
      }
      
    } catch (error) {
      console.error('Error processing ZIP file:', error);
      setUploadError(`Error processing file: ${error.message}`);
      // Reset states on error
      setExtractedFiles([]);
      setParsedData(null);
      setShowFilePreview(false);
      setShowDataPreview(false);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleZipUpload = (files) => {
    const zipFile = files[0];
    const maxSize = 100 * 1024 * 1024; // 100MB

    if (!zipFile) return;

    // Validate file type
    if (!zipFile.name.toLowerCase().endsWith('.zip')) {
      setUploadError('Please upload a ZIP file containing your Resonate reports.');
      return;
    }

    // Validate file size
    if (zipFile.size > maxSize) {
      setUploadError('ZIP file too large. Maximum size: 100MB');
      return;
    }

    setUploadError(null);
    setUploadedZip(zipFile);
    
    // Process the ZIP file immediately with real parsing
    processZipFile(zipFile);
  };


  const parseExtractedFiles = async () => {
    // Parsing is now handled automatically when uploading the ZIP file
    // This function is kept for backward compatibility with the UI
    if (parsedData) {
      setShowDataPreview(true);
    } else {
      setUploadError('No parsed data available. Please upload a ZIP file first.');
    }
  };

  const handleNext = async () => {
    console.log('handleNext called');
    console.log('parsedData:', parsedData);
    
    if (!parsedData) {
      alert('Please upload and parse your Resonate data ZIP file first.');
      return;
    }

    try {
      console.log('Starting persona creation from Resonate data...');
      
      // Get backend URL from environment
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      console.log('Backend URL:', backendUrl);
      
      // Create persona using the resonate-create endpoint
      const response = await fetch(`${backendUrl}/api/personas/resonate-create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          parsed_data: parsedData,
          name: persona.name || 'Resonate Persona'
        }),
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Backend error:', errorData);
        throw new Error(errorData.detail || 'Failed to create persona from Resonate data');
      }

      const result = await response.json();
      console.log('Backend result:', result);
      
      if (result.success && result.persona) {
        // Extract the created persona data from the backend
        const createdPersona = result.persona;
        
        // Update the current persona with the created data and move to next step
        const personaUpdate = {
          // Preserve the existing persona ID and basic info
          name: createdPersona.name || persona.name,
          starting_method: createdPersona.starting_method,
          
          // Map the demographics from Resonate data
          demographics: createdPersona.demographics || {},
          
          // Map attributes if available
          attributes: createdPersona.attributes || {},
          
          // Map media consumption if available  
          media_consumption: createdPersona.media_consumption || {},
          
          // Update step progression
          current_step: 3,
          completed_steps: [...(persona.completed_steps || []), 2],
          
          // Store the raw parsed data for reference
          resonate_data: parsedData
        };
        
        console.log('Updating persona with:', personaUpdate);
        
        const success = await updatePersona(personaUpdate, 3);
        console.log('Update success:', success);
        
        if (success) {
          console.log('Calling onNext...');
          onNext();
        }
      } else {
        throw new Error(result.message || 'Failed to create persona');
      }
      
    } catch (error) {
      console.error('Error creating persona from Resonate data:', error);
      alert(`Error creating persona: ${error.message}`);
    }
  };

  const removeZipFile = () => {
    setUploadedZip(null);
    setExtractedFiles([]);
    setParsedData(null);
    setShowFilePreview(false);
    setShowDataPreview(false);
    setUploadError(null);
  };

  return (
    <div className="form-section">
      <div className="mb-8">
        <h2 className="text-2xl font-bold font-montserrat mb-3 bcm-heading">
          Upload Resonate Data
        </h2>
        <p className="text-gray-600 font-montserrat">
          Upload your Resonate rAI reports to create data-driven personas. The system will parse 
          your files and extract demographic, psychographic, and behavioral insights.
        </p>
      </div>

      {!showDataPreview ? (
        <>
          {/* ZIP File Upload Section */}
          <div className="border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-semibold text-lg font-montserrat">
                  Resonate Data ZIP Package
                  <span className="text-red-500 ml-1">*</span>
                </h3>
                <p className="text-sm text-gray-600 font-montserrat">
                  Upload a ZIP file containing your Resonate reports and data files
                </p>
                <p className="text-xs text-gray-500 font-montserrat mt-1">
                  Accepted: {zipRequirements.accept} | Max size: {zipRequirements.maxSize}
                </p>
              </div>
            </div>

            {/* ZIP Upload Area */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                id="upload-zip"
                className="hidden"
                accept=".zip,.png,.jpg,.jpeg,.pdf"
                onChange={(e) => handleZipUpload(e.target.files)}
              />
              <label
                htmlFor="upload-zip"
                className="cursor-pointer flex flex-col items-center"
              >
                <svg className="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span className="text-gray-600 font-montserrat">
                  Click to upload ZIP file or drag and drop
                </span>
              </label>
            </div>

            {/* Display uploaded ZIP */}
            {uploadedZip && (
              <div className="mt-4 flex items-center justify-between bg-green-50 p-3 rounded">
                <span className="text-sm font-montserrat">{uploadedZip.name}</span>
                <button
                  onClick={removeZipFile}
                  className="text-red-500 hover:text-red-700"
                >
                  ✕
                </button>
              </div>
            )}

            {/* Error message */}
            {uploadError && (
              <div className="mt-2 text-red-600 text-sm font-montserrat">
                {uploadError}
              </div>
            )}

            {/* Expected Files List */}
            <div className="mt-6">
              <h4 className="font-semibold text-sm mb-2 font-montserrat">Expected Files in ZIP:</h4>
              <ul className="list-disc list-inside space-y-1">
                {zipRequirements.expectedFiles.map((file, index) => (
                  <li key={index} className="text-sm text-gray-600 font-montserrat">{file}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Extracted Files Preview */}
          {showFilePreview && extractedFiles.length > 0 && (
            <div className="mt-6">
              <h3 className="font-semibold text-lg mb-3 font-montserrat">Extracted Files</h3>
              <div className="space-y-2">
                {extractedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between bg-blue-50 p-3 rounded">
                    <div>
                      <span className="text-sm font-semibold font-montserrat">{file.name}</span>
                      <div className="text-xs text-gray-600">
                        <span className="mr-3">{file.type}</span>
                        <span className="mr-3">{file.format}</span>
                        <span>{file.size}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Parse Files Button - Only show if upload succeeded but not yet processed */}
          {uploadedZip && !isProcessing && !showDataPreview && (
            <div className="mt-8 text-center">
              <button
                onClick={parseExtractedFiles}
                disabled={!uploadedZip || isProcessing}
                className="bcm-btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Parse ZIP Contents
              </button>
              <p className="text-sm text-gray-600 font-montserrat mt-2">
                Ready to process your Resonate data
              </p>
            </div>
          )}

          {/* Processing State */}
          {isProcessing && (
            <div className="mt-8 text-center">
              <div className="flex items-center justify-center">
                <div className="loading-spinner mr-2"></div>
                <span>Processing Files...</span>
              </div>
              <p className="text-sm text-gray-600 font-montserrat mt-2">
                Analyzing your Resonate data...
              </p>
            </div>
          )}
        </>
      ) : (
        /* Data Preview Section */
        <div className="space-y-6">
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-green-800 mb-3 font-montserrat">
              🎯 Resonate Data Successfully Parsed
            </h3>
            <p className="text-green-700 font-montserrat">
              Your Resonate files have been processed and the data is ready for persona generation. 
              Review the parsed data below and click "Continue" to proceed.
            </p>
          </div>

          {/* Parsed Data Preview - Simplified and Organized */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Demographics Summary */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat text-blue-600">📊 Demographics Data</h4>
              <div className="space-y-2 text-sm">
                {parsedData.demographics && Object.keys(parsedData.demographics).length > 0 ? (
                  <div className="text-green-600">
                    ✅ Found {Object.keys(parsedData.demographics).length} demographic data sources
                  </div>
                ) : (
                  <div className="text-yellow-600">⚠️ No specific demographic data found</div>
                )}
                <div className="text-gray-600">
                  Data will be processed to extract age, gender, location, and occupation insights.
                </div>
              </div>
            </div>

            {/* Media Consumption Summary */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat text-green-600">📱 Media Consumption</h4>
              <div className="space-y-2 text-sm">
                {parsedData.media_consumption && Object.keys(parsedData.media_consumption).length > 0 ? (
                  <div>
                    <div className="text-green-600 mb-2">
                      ✅ Found {Object.keys(parsedData.media_consumption).length} media data sources
                    </div>
                    {parsedData.media_consumption.media_platforms && (
                      <div className="text-gray-600">
                        • Social media platform preferences
                      </div>
                    )}
                    <div className="text-gray-600">
                      • TV viewing patterns and streaming habits
                    </div>
                    <div className="text-gray-600">
                      • Digital device usage preferences
                    </div>
                  </div>
                ) : (
                  <div className="text-yellow-600">⚠️ No media consumption data found</div>
                )}
              </div>
            </div>

            {/* Brand Affinity Summary */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat text-purple-600">🛍️ Brand & Shopping</h4>
              <div className="space-y-2 text-sm">
                {parsedData.brand_affinity && Object.keys(parsedData.brand_affinity).length > 0 ? (
                  <div className="text-green-600">
                    ✅ Found {Object.keys(parsedData.brand_affinity).length} brand preference sources
                  </div>
                ) : (
                  <div className="text-yellow-600">⚠️ No brand affinity data found</div>
                )}
                <div className="text-gray-600">
                  Shopping behaviors and brand preferences will inform persona development.
                </div>
              </div>
            </div>

            {/* Processed Files Summary */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat text-gray-600">📁 File Processing</h4>
              <div className="space-y-2 text-sm">
                {parsedData.source_files && parsedData.source_files.length > 0 ? (
                  <div>
                    <div className="text-green-600 mb-2">
                      ✅ Processed {parsedData.source_files.filter(f => f.processed).length} of {parsedData.source_files.length} files
                    </div>
                    {parsedData.source_files.slice(0, 3).map((file, i) => (
                      <div key={i} className="flex items-center justify-between text-xs bg-gray-50 p-2 rounded">
                        <span className="truncate">{file.name}</span>
                        <span className={`px-2 py-1 rounded text-xs ${
                          file.processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {file.processed ? '✓' : '⚠'}
                        </span>
                      </div>
                    ))}
                    {parsedData.source_files.length > 3 && (
                      <div className="text-xs text-gray-500">
                        ...and {parsedData.source_files.length - 3} more files
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="text-gray-500">No file information available</div>
                )}
              </div>
            </div>

            {/* Data Quality Summary */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 md:col-span-2">
              <h4 className="font-semibold mb-3 font-montserrat text-blue-800">🎯 Next Steps</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <div className="font-medium text-blue-700">Demographics</div>
                  <div className="text-blue-600">Will be populated with age range, gender, location, and occupation based on your data</div>
                </div>
                <div>
                  <div className="font-medium text-blue-700">Media Preferences</div>
                  <div className="text-blue-600">Social media platforms, viewing habits, and device preferences</div>
                </div>
                <div>
                  <div className="font-medium text-blue-700">Behavioral Insights</div>
                  <div className="text-blue-600">Shopping patterns and brand affinities for persona development</div>
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-center">
            <button
              onClick={() => {
                setShowDataPreview(false);
                setShowFilePreview(false);
              }}
              className="bcm-btn-outline mr-4"
            >
              ← Edit Files
            </button>
            <button
              onClick={handleNext}
              disabled={saving}
              className="bcm-btn-primary"
            >
              {saving ? "Saving..." : "Continue with Parsed Data →"}
            </button>
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
        
        {!showDataPreview && uploadedZip && (
          <div className="text-sm text-gray-600 font-montserrat">
            ZIP file uploaded: {uploadedZip.name}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResonateUpload;
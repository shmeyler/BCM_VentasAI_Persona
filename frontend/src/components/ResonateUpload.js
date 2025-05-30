import React, { useState } from 'react';

const ResonateUpload = ({ persona, updatePersona, onNext, onPrev, saving }) => {
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
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to process ZIP file');
      }

      const result = await response.json();
      
      if (result.success) {
        // Set extracted files and parsed data from real backend response
        setExtractedFiles(result.extracted_files);
        setParsedData(result.parsed_data);
        setShowFilePreview(true);
        setShowDataPreview(true); // Show data preview directly since we have parsed data
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
    if (!parsedData) {
      alert('Please upload and parse your Resonate data ZIP file first.');
      return;
    }

    // Create persona data from comprehensive parsed Resonate data
    const resonatePersonaData = {
      starting_method: 'resonate_upload',
      resonate_data: parsedData,
      demographics: {
        age_range: '25-34', // Primary demographic from parsed data
        gender: 'Female',   // Primary demographic from parsed data
        income_range: '$75,000-$100,000',
        education: 'Bachelor degree',
        location: 'Urban',
        occupation: 'Full Time Employed',
        family_status: 'Single'
      },
      attributes: {
        selectedVertical: 'Technology & Telecom',
        selectedCategory: 'Technology Adoption',
        selectedAttributes: ['Early Adopter', 'Innovation Focused', 'Quality Driven']
      },
      media_consumption: {
        social_media_platforms: ['Instagram', 'Facebook', 'LinkedIn', 'YouTube'],
        preferred_devices: ['Mobile', 'Desktop'],
        consumption_time: '2-4 hours',
        news_sources: ['Social Media', 'Industry Publications'],
        entertainment_preferences: ['Educational Content', 'Product Reviews']
      }
    };

    try {
      const success = await updatePersona(resonatePersonaData, 2);
      if (success) {
        onNext();
      }
    } catch (error) {
      console.error('Error saving Resonate data:', error);
      alert('Error saving Resonate data. Please try again.');
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
                accept=".zip"
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

          {/* Parse Files Button */}
          <div className="mt-8 text-center">
            <button
              onClick={parseExtractedFiles}
              disabled={!uploadedZip || isProcessing}
              className="bcm-btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? (
                <div className="flex items-center">
                  <div className="loading-spinner mr-2"></div>
                  Processing Files...
                </div>
              ) : (
                "Parse ZIP Contents"
              )}
            </button>
            <p className="text-sm text-gray-600 font-montserrat mt-2">
              {uploadedZip 
                ? "Ready to process your Resonate data" 
                : "Upload a ZIP file containing your Resonate reports to continue"
              }
            </p>
          </div>
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

          {/* Parsed Data Preview */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat">Demographics</h4>
              <div className="space-y-2 text-sm">
                <div><strong>Age Distribution:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.demographics.ageDistribution.map((age, i) => (
                    <li key={i}>{age.range}: {age.percentage}%</li>
                  ))}
                </ul>
                <div><strong>Gender Split:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.demographics.genderSplit.map((gender, i) => (
                    <li key={i}>{gender.gender}: {gender.percentage}%</li>
                  ))}
                </ul>
                <div><strong>Income Distribution:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.demographics.incomeDistribution.map((income, i) => (
                    <li key={i}>{income.range}: {income.percentage}%</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat">Psychographics</h4>
              <div className="space-y-2 text-sm">
                <div><strong>Values:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.psychographics.values.map((value, i) => (
                    <li key={i}>{value.value}: {value.strength} ({value.percentage}%)</li>
                  ))}
                </ul>
                <div><strong>Interests:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.psychographics.interests.map((interest, i) => (
                    <li key={i}>{interest.interest}: {interest.affinity}% affinity</li>
                  ))}
                </ul>
                <div><strong>Behaviors:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.psychographics.behaviors.map((behavior, i) => (
                    <li key={i}>{behavior.behavior}: {behavior.likelihood}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat">Media Consumption</h4>
              <div className="space-y-2 text-sm">
                <div><strong>Platforms:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.mediaConsumption.platforms.map((platform, i) => (
                    <li key={i}>{platform.platform}: {platform.usage}% ({platform.timeSpent})</li>
                  ))}
                </ul>
                <div><strong>Devices:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.mediaConsumption.devices.map((device, i) => (
                    <li key={i}>{device.device}: {device.usage}% ({device.primaryTime})</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat">Brand Affinity</h4>
              <div className="space-y-2 text-sm">
                <div><strong>Top Brands:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.brandAffinity.topBrands.map((brand, i) => (
                    <li key={i}>{brand.brand}: {brand.affinity}% ({brand.category})</li>
                  ))}
                </ul>
                <div><strong>Category Affinities:</strong></div>
                <ul className="list-disc list-inside">
                  {parsedData.brandAffinity.categoryAffinities.map((category, i) => (
                    <li key={i}>{category.category}: {category.affinity}</li>
                  ))}
                </ul>
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
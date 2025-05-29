import React, { useState } from 'react';

const ResonateUpload = ({ persona, updatePersona, onNext, onPrev, saving }) => {
  const [uploadedFiles, setUploadedFiles] = useState({
    demographics: null,
    audienceInsights: null,
    categoryAffinity: null,
    mediaPlanning: null,
    researchReport: null,
    charts: []
  });

  const [parsedData, setParsedData] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadErrors, setUploadErrors] = useState({});

  const fileRequirements = {
    demographics: {
      name: 'Demographics Report',
      description: 'Demographic analysis (PNG charts, PDF reports, or data files)',
      accept: '.png,.pdf,.csv,.xls,.xlsx,.ppt,.pptx',
      maxSize: '25MB',
      required: true
    },
    audienceInsights: {
      name: 'Audience Insights',
      description: 'Audience behavior and psychographic data (any format)',
      accept: '.csv,.pdf,.png,.xls,.xlsx,.ppt,.pptx',
      maxSize: '25MB',
      required: true
    },
    categoryAffinity: {
      name: 'Category/Brand Affinity',
      description: 'Brand preferences and category affinity data',
      accept: '.csv,.pdf,.png,.xls,.xlsx,.ppt,.pptx',
      maxSize: '25MB',
      required: false
    },
    mediaConsumption: {
      name: 'Media Consumption',
      description: 'Media planning and consumption analysis',
      accept: '.csv,.pdf,.png,.xls,.xlsx,.ppt,.pptx',
      maxSize: '25MB',
      required: false
    },
    personalValues: {
      name: 'Personal Values & Motivations',
      description: 'Values, motivations, and psychographic insights',
      accept: '.csv,.pdf,.png,.xls,.xlsx,.ppt,.pptx',
      maxSize: '25MB',
      required: false
    },
    researchReport: {
      name: 'Comprehensive Research Report',
      description: 'Full Resonate research presentation or summary',
      accept: '.pdf,.ppt,.pptx,.docx',
      maxSize: '50MB',
      required: false
    },
    additionalData: {
      name: 'Additional Data Files',
      description: 'Supporting charts, tables, or supplementary analysis',
      accept: '.png,.pdf,.csv,.xls,.xlsx,.ppt,.pptx,.jpg,.jpeg',
      maxSize: '25MB each',
      required: false,
      multiple: true
    }
  };

  const handleFileUpload = (fileType, files) => {
    const fileList = Array.from(files);
    
    // Validate file size and type
    const errors = {};
    const maxSizes = {
      demographics: 25 * 1024 * 1024, // 25MB
      audienceInsights: 25 * 1024 * 1024,
      categoryAffinity: 25 * 1024 * 1024,
      mediaConsumption: 25 * 1024 * 1024,
      personalValues: 25 * 1024 * 1024,
      researchReport: 50 * 1024 * 1024,
      additionalData: 25 * 1024 * 1024
    };

    fileList.forEach(file => {
      if (file.size > maxSizes[fileType]) {
        errors[fileType] = `File too large. Maximum size: ${fileRequirements[fileType].maxSize}`;
        return;
      }
    });

    if (Object.keys(errors).length > 0) {
      setUploadErrors(prev => ({ ...prev, ...errors }));
      return;
    }

    // Clear any previous errors
    setUploadErrors(prev => ({ ...prev, [fileType]: null }));

    // Update uploaded files
    if (fileType === 'charts') {
      setUploadedFiles(prev => ({
        ...prev,
        charts: [...prev.charts, ...fileList]
      }));
    } else {
      setUploadedFiles(prev => ({
        ...prev,
        [fileType]: fileList[0]
      }));
    }
  };

  const removeFile = (fileType, index = null) => {
    if (fileType === 'additionalData' && index !== null) {
      setUploadedFiles(prev => ({
        ...prev,
        additionalData: prev.additionalData.filter((_, i) => i !== index)
      }));
    } else {
      setUploadedFiles(prev => ({
        ...prev,
        [fileType]: null
      }));
    }
  };

  const parseUploadedFiles = async () => {
    setIsProcessing(true);
    try {
      // Simulate file parsing process
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock parsed data structure
      const mockParsedData = {
        demographics: {
          ageRanges: ['18-24: 15%', '25-34: 35%', '35-44: 30%', '45-54: 20%'],
          gender: ['Male: 45%', 'Female: 53%', 'Other: 2%'],
          income: ['$50K-75K: 40%', '$75K-100K: 35%', '$100K+: 25%'],
          education: ['Bachelor: 45%', 'Master: 30%', 'High School: 25%']
        },
        psychographics: {
          values: ['Innovation: High', 'Tradition: Medium', 'Achievement: High'],
          interests: ['Technology', 'Travel', 'Health & Wellness', 'Education'],
          behaviors: ['Early Adopter', 'Brand Loyal', 'Price Conscious']
        },
        mediaConsumption: {
          platforms: ['Instagram: 75%', 'Facebook: 65%', 'LinkedIn: 45%', 'TikTok: 30%'],
          devices: ['Mobile: 80%', 'Desktop: 60%', 'Tablet: 35%'],
          timeSpent: ['2-4 hours daily: 50%', '1-2 hours: 30%', '4+ hours: 20%']
        },
        categoryAffinity: {
          brands: ['Apple: 85%', 'Nike: 70%', 'Starbucks: 65%', 'Amazon: 90%'],
          categories: ['Technology: High', 'Fashion: Medium', 'Food & Beverage: High']
        }
      };

      setParsedData(mockParsedData);
      setShowPreview(true);
    } catch (error) {
      console.error('Error parsing files:', error);
      alert('Error parsing uploaded files. Please check the file formats and try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleNext = async () => {
    if (!parsedData) {
      alert('Please upload and parse your Resonate data files first.');
      return;
    }

    // Create persona data from parsed Resonate data
    const resonatePersonaData = {
      starting_method: 'resonate_upload',
      resonate_data: parsedData,
      demographics: {
        age_range: '25-34', // Derived from parsed data
        gender: 'Female',   // Derived from parsed data
        income_range: '$75,000-$100,000',
        education: 'Bachelor degree',
        location: 'Urban',  // Could be parsed from location data
        occupation: 'Full Time Employed',
        family_status: 'Single'
      },
      attributes: {
        selectedVertical: 'Technology & Telecom',
        selectedCategory: 'Technology Adoption',
        selectedAttributes: ['Early Adopter', 'Innovation Focused', 'Brand Loyal']
      },
      media_consumption: {
        social_media_platforms: ['Instagram', 'Facebook', 'LinkedIn'],
        preferred_devices: ['Mobile', 'Desktop'],
        consumption_time: '2-4 hours',
        news_sources: ['Social Media', 'Online News Sites'],
        entertainment_preferences: ['Streaming Services', 'Podcasts']
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

  const getUploadedFilesList = () => {
    const files = [];
    Object.entries(uploadedFiles).forEach(([type, file]) => {
      if (type === 'charts') {
        file.forEach((chartFile, index) => {
          files.push({ type: `charts-${index}`, name: chartFile.name, file: chartFile });
        });
      } else if (file) {
        files.push({ type, name: file.name, file });
      }
    });
    return files;
  };

  const canProceed = () => {
    const requiredFiles = Object.entries(fileRequirements)
      .filter(([_, req]) => req.required)
      .map(([type, _]) => type);
    
    return requiredFiles.every(type => uploadedFiles[type] !== null);
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

      {!showPreview ? (
        <>
          {/* File Upload Section */}
          <div className="space-y-6">
            {Object.entries(fileRequirements).map(([fileType, requirements]) => (
              <div key={fileType} className="border border-gray-200 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="font-semibold text-lg font-montserrat">
                      {requirements.name}
                      {requirements.required && <span className="text-red-500 ml-1">*</span>}
                    </h3>
                    <p className="text-sm text-gray-600 font-montserrat">
                      {requirements.description}
                    </p>
                    <p className="text-xs text-gray-500 font-montserrat mt-1">
                      Accepted: {requirements.accept} | Max size: {requirements.maxSize}
                    </p>
                  </div>
                </div>

                {/* File Upload Area */}
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <input
                    type="file"
                    id={`upload-${fileType}`}
                    className="hidden"
                    accept={requirements.accept}
                    multiple={requirements.multiple}
                    onChange={(e) => handleFileUpload(fileType, e.target.files)}
                  />
                  <label
                    htmlFor={`upload-${fileType}`}
                    className="cursor-pointer flex flex-col items-center"
                  >
                    <svg className="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <span className="text-gray-600 font-montserrat">
                      Click to upload {requirements.multiple ? 'files' : 'file'} or drag and drop
                    </span>
                  </label>
                </div>

                {/* Display uploaded files */}
                {fileType === 'charts' ? (
                  uploadedFiles.charts.length > 0 && (
                    <div className="mt-4 space-y-2">
                      {uploadedFiles.charts.map((file, index) => (
                        <div key={index} className="flex items-center justify-between bg-green-50 p-3 rounded">
                          <span className="text-sm font-montserrat">{file.name}</span>
                          <button
                            onClick={() => removeFile('charts', index)}
                            className="text-red-500 hover:text-red-700"
                          >
                            ✕
                          </button>
                        </div>
                      ))}
                    </div>
                  )
                ) : (
                  uploadedFiles[fileType] && (
                    <div className="mt-4 flex items-center justify-between bg-green-50 p-3 rounded">
                      <span className="text-sm font-montserrat">{uploadedFiles[fileType].name}</span>
                      <button
                        onClick={() => removeFile(fileType)}
                        className="text-red-500 hover:text-red-700"
                      >
                        ✕
                      </button>
                    </div>
                  )
                )}

                {/* Error messages */}
                {uploadErrors[fileType] && (
                  <div className="mt-2 text-red-600 text-sm font-montserrat">
                    {uploadErrors[fileType]}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Parse Files Button */}
          <div className="mt-8 text-center">
            <button
              onClick={parseUploadedFiles}
              disabled={!canProceed() || isProcessing}
              className="bcm-btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? (
                <div className="flex items-center">
                  <div className="loading-spinner mr-2"></div>
                  Processing Files...
                </div>
              ) : (
                "Parse Uploaded Data"
              )}
            </button>
            <p className="text-sm text-gray-600 font-montserrat mt-2">
              {canProceed() 
                ? "Ready to process your Resonate data files" 
                : "Upload required files marked with * to continue"
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
                <div><strong>Age:</strong> {parsedData.demographics.ageRanges.join(', ')}</div>
                <div><strong>Gender:</strong> {parsedData.demographics.gender.join(', ')}</div>
                <div><strong>Income:</strong> {parsedData.demographics.income.join(', ')}</div>
                <div><strong>Education:</strong> {parsedData.demographics.education.join(', ')}</div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat">Psychographics</h4>
              <div className="space-y-2 text-sm">
                <div><strong>Values:</strong> {parsedData.psychographics.values.join(', ')}</div>
                <div><strong>Interests:</strong> {parsedData.psychographics.interests.join(', ')}</div>
                <div><strong>Behaviors:</strong> {parsedData.psychographics.behaviors.join(', ')}</div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat">Media Consumption</h4>
              <div className="space-y-2 text-sm">
                <div><strong>Platforms:</strong> {parsedData.mediaConsumption.platforms.join(', ')}</div>
                <div><strong>Devices:</strong> {parsedData.mediaConsumption.devices.join(', ')}</div>
                <div><strong>Time Spent:</strong> {parsedData.mediaConsumption.timeSpent.join(', ')}</div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-3 font-montserrat">Category Affinity</h4>
              <div className="space-y-2 text-sm">
                <div><strong>Brands:</strong> {parsedData.categoryAffinity.brands.join(', ')}</div>
                <div><strong>Categories:</strong> {parsedData.categoryAffinity.categories.join(', ')}</div>
              </div>
            </div>
          </div>

          <div className="flex justify-center">
            <button
              onClick={() => setShowPreview(false)}
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
        
        {!showPreview && getUploadedFilesList().length > 0 && (
          <div className="text-sm text-gray-600 font-montserrat">
            {getUploadedFilesList().length} file(s) uploaded
          </div>
        )}
      </div>
    </div>
  );
};

export default ResonateUpload;
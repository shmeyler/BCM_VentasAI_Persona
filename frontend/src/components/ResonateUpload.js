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
    
    // Simulate ZIP extraction for preview
    simulateZipExtraction(zipFile);
  };

  const simulateZipExtraction = (zipFile) => {
    setIsProcessing(true);
    
    // Mock extracted files list (in real implementation, this would extract the ZIP)
    setTimeout(() => {
      const mockExtractedFiles = [
        { name: 'Demographics_2025_05_08.png', type: 'Demographics', format: 'PNG', size: '2.1 MB' },
        { name: 'Audience_Introduction_2025_05_08.pdf', type: 'Audience Insights', format: 'PDF', size: '1.8 MB' },
        { name: 'Brand_Affinity_2025_05_08.csv', type: 'Category Affinity', format: 'CSV', size: '456 KB' },
        { name: 'Media_Consumption_2025_05_08.pdf', type: 'Media Planning', format: 'PDF', size: '3.2 MB' },
        { name: 'Personal_Values_2025_05_08.xlsx', type: 'Personal Values', format: 'Excel', size: '789 KB' },
        { name: 'Research_Recommendations.pptx', type: 'Research Report', format: 'PowerPoint', size: '12.4 MB' },
        { name: 'site_affinity_charts.png', type: 'Supporting Data', format: 'PNG', size: '1.6 MB' },
        { name: 'category_metrics.csv', type: 'Supporting Data', format: 'CSV', size: '234 KB' }
      ];

      setExtractedFiles(mockExtractedFiles);
      setShowFilePreview(true);
      setIsProcessing(false);
    }, 2000);
  };

  const parseExtractedFiles = async () => {
    setIsProcessing(true);
    try {
      // Simulate file parsing process
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Mock comprehensive parsed data from all files
      const mockParsedData = {
        demographics: {
          ageDistribution: [
            { range: '18-24', percentage: 12, source: 'Demographics_2025_05_08.png' },
            { range: '25-34', percentage: 35, source: 'Demographics_2025_05_08.png' },
            { range: '35-44', percentage: 28, source: 'Demographics_2025_05_08.png' },
            { range: '45-54', percentage: 18, source: 'Demographics_2025_05_08.png' },
            { range: '55+', percentage: 7, source: 'Demographics_2025_05_08.png' }
          ],
          genderSplit: [
            { gender: 'Male', percentage: 47, source: 'Demographics_2025_05_08.png' },
            { gender: 'Female', percentage: 51, source: 'Demographics_2025_05_08.png' },
            { gender: 'Other', percentage: 2, source: 'Demographics_2025_05_08.png' }
          ],
          incomeDistribution: [
            { range: '$50K-75K', percentage: 32, source: 'Demographics_2025_05_08.png' },
            { range: '$75K-100K', percentage: 28, source: 'Demographics_2025_05_08.png' },
            { range: '$100K+', percentage: 40, source: 'Demographics_2025_05_08.png' }
          ],
          geography: [
            { region: 'Urban', percentage: 65, source: 'Demographics_2025_05_08.png' },
            { region: 'Suburban', percentage: 28, source: 'Demographics_2025_05_08.png' },
            { region: 'Rural', percentage: 7, source: 'Demographics_2025_05_08.png' }
          ]
        },
        psychographics: {
          values: [
            { value: 'Innovation', strength: 'High', percentage: 78, source: 'Personal_Values_2025_05_08.xlsx' },
            { value: 'Quality', strength: 'High', percentage: 82, source: 'Personal_Values_2025_05_08.xlsx' },
            { value: 'Convenience', strength: 'Medium', percentage: 65, source: 'Personal_Values_2025_05_08.xlsx' },
            { value: 'Price Consciousness', strength: 'Medium', percentage: 58, source: 'Personal_Values_2025_05_08.xlsx' }
          ],
          interests: [
            { interest: 'Technology', affinity: 85, source: 'Audience_Introduction_2025_05_08.pdf' },
            { interest: 'Travel', affinity: 72, source: 'Audience_Introduction_2025_05_08.pdf' },
            { interest: 'Health & Wellness', affinity: 68, source: 'Audience_Introduction_2025_05_08.pdf' },
            { interest: 'Professional Development', affinity: 71, source: 'Audience_Introduction_2025_05_08.pdf' }
          ],
          behaviors: [
            { behavior: 'Early Adopter', likelihood: 'High', source: 'Audience_Introduction_2025_05_08.pdf' },
            { behavior: 'Brand Loyal', likelihood: 'Medium', source: 'Brand_Affinity_2025_05_08.csv' },
            { behavior: 'Research Heavy', likelihood: 'High', source: 'Audience_Introduction_2025_05_08.pdf' }
          ]
        },
        mediaConsumption: {
          platforms: [
            { platform: 'Instagram', usage: 78, timeSpent: '45min/day', source: 'Media_Consumption_2025_05_08.pdf' },
            { platform: 'Facebook', usage: 65, timeSpent: '32min/day', source: 'Media_Consumption_2025_05_08.pdf' },
            { platform: 'LinkedIn', usage: 58, timeSpent: '28min/day', source: 'Media_Consumption_2025_05_08.pdf' },
            { platform: 'TikTok', usage: 42, timeSpent: '25min/day', source: 'Media_Consumption_2025_05_08.pdf' },
            { platform: 'YouTube', usage: 71, timeSpent: '52min/day', source: 'Media_Consumption_2025_05_08.pdf' }
          ],
          devices: [
            { device: 'Mobile', usage: 85, primaryTime: 'Throughout day', source: 'Media_Consumption_2025_05_08.pdf' },
            { device: 'Desktop', usage: 62, primaryTime: 'Work hours', source: 'Media_Consumption_2025_05_08.pdf' },
            { device: 'Tablet', usage: 34, primaryTime: 'Evening', source: 'Media_Consumption_2025_05_08.pdf' }
          ],
          contentPreferences: [
            { type: 'Educational Content', preference: 'High', source: 'Media_Consumption_2025_05_08.pdf' },
            { type: 'Product Reviews', preference: 'High', source: 'Media_Consumption_2025_05_08.pdf' },
            { type: 'Industry News', preference: 'Medium', source: 'Media_Consumption_2025_05_08.pdf' },
            { type: 'Entertainment', preference: 'Medium', source: 'Media_Consumption_2025_05_08.pdf' }
          ]
        },
        brandAffinity: {
          topBrands: [
            { brand: 'Apple', affinity: 87, category: 'Technology', source: 'Brand_Affinity_2025_05_08.csv' },
            { brand: 'Amazon', affinity: 82, category: 'E-commerce', source: 'Brand_Affinity_2025_05_08.csv' },
            { brand: 'Google', affinity: 79, category: 'Technology', source: 'Brand_Affinity_2025_05_08.csv' },
            { brand: 'Nike', affinity: 73, category: 'Athletic Wear', source: 'Brand_Affinity_2025_05_08.csv' }
          ],
          categoryAffinities: [
            { category: 'Technology', affinity: 'Very High', source: 'Brand_Affinity_2025_05_08.csv' },
            { category: 'E-commerce', affinity: 'High', source: 'Brand_Affinity_2025_05_08.csv' },
            { category: 'Financial Services', affinity: 'Medium', source: 'Brand_Affinity_2025_05_08.csv' },
            { category: 'Travel', affinity: 'Medium', source: 'Brand_Affinity_2025_05_08.csv' }
          ]
        },
        insights: {
          keyFindings: [
            'Tech-savvy professional demographic with high innovation adoption',
            'Strong preference for quality over price',
            'Heavy mobile usage with Instagram as primary platform',
            'High brand loyalty to premium technology brands',
            'Values educational content and peer recommendations'
          ],
          recommendedActions: [
            'Focus marketing on Instagram and LinkedIn platforms',
            'Emphasize product quality and innovation in messaging',
            'Create educational content series',
            'Partner with technology influencers',
            'Develop mobile-first user experiences'
          ]
        }
      };

      setParsedData(mockParsedData);
      setShowDataPreview(true);
    } catch (error) {
      console.error('Error parsing files:', error);
      alert('Error parsing uploaded files. Please check the file formats and try again.');
    } finally {
      setIsProcessing(false);
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
import React, { useState, useEffect } from "react";

const MediaConsumptionStep = ({ persona, updatePersona, onNext, onPrev, saving, goToStep }) => {
  const [mediaConsumption, setMediaConsumption] = useState(persona?.media_consumption || {
    social_media_platforms: [],
    content_types: [],
    consumption_time: "",
    preferred_devices: [],
    news_sources: [],
    entertainment_preferences: [],
    advertising_receptivity: ""
  });

  const [isEditing, setIsEditing] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  const [preFilledFromDemographics, setPreFilledFromDemographics] = useState(false);
  
  // Separate state for news sources text input
  const [newsSourcesText, setNewsSourcesText] = useState(
    persona?.media_consumption?.news_sources?.join(', ') || ''
  );

  // State for collapsible sections
  const [expandedSections, setExpandedSections] = useState({
    social_media: false,
    content_consumption: false,
    devices_time: false,
    entertainment: false,
    news_advertising: false
  });

  // Resonate AI-based demographic mapping (dummy data simulating API responses)
  const getMediaPreferencesFromDemographics = (demographics) => {
    const age = demographics?.age_range || '';
    const gender = demographics?.gender || '';
    const location = demographics?.location || '';
    const occupation = demographics?.occupation || '';
    const income = demographics?.income_range || '';
    
    console.log('Generating media preferences for:', { age, gender, location, occupation, income });

    let preferences = {
      social_media_platforms: [],
      content_types: [],
      consumption_time: "",
      preferred_devices: [],
      news_sources: [],
      entertainment_preferences: [],
      advertising_receptivity: ""
    };

    // Age-based preferences (simulating Resonate AI data)
    if (age.includes('18-24')) {
      preferences.social_media_platforms = ['TikTok', 'Instagram', 'Snapchat', 'Twitter/X', 'YouTube'];
      preferences.content_types = ['Videos', 'Stories/Reels', 'Social media posts', 'Live streams', 'User-generated content'];
      preferences.consumption_time = '4-6 hours';
      preferences.preferred_devices = ['Smartphone', 'Laptop', 'Gaming console'];
      preferences.entertainment_preferences = ['Streaming services', 'Gaming', 'Music', 'Comedy'];
      preferences.advertising_receptivity = 'Moderately receptive';
      preferences.news_sources = ['Social media', 'YouTube', 'TikTok', 'Instagram'];
    } else if (age.includes('25-40')) {
      preferences.social_media_platforms = ['Instagram', 'Facebook', 'LinkedIn', 'Twitter/X', 'YouTube'];
      preferences.content_types = ['Social media posts', 'Videos', 'Podcasts', 'News articles', 'Streaming shows'];
      preferences.consumption_time = '2-4 hours';
      preferences.preferred_devices = ['Smartphone', 'Laptop', 'Tablet', 'Smart TV'];
      preferences.entertainment_preferences = ['Streaming services', 'Podcasts', 'Movies', 'Drama series'];
      preferences.advertising_receptivity = 'Moderately receptive';
      preferences.news_sources = ['Online news sites', 'Social media', 'Podcasts', 'News apps'];
    } else if (age.includes('41-56')) {
      preferences.social_media_platforms = ['Facebook', 'LinkedIn', 'YouTube', 'Instagram'];
      preferences.content_types = ['News articles', 'Email newsletters', 'Videos', 'Podcasts', 'Blogs'];
      preferences.consumption_time = '2-4 hours';
      preferences.preferred_devices = ['Smartphone', 'Laptop', 'Desktop', 'Smart TV'];
      preferences.entertainment_preferences = ['Traditional TV', 'Streaming services', 'News', 'Documentaries'];
      preferences.advertising_receptivity = 'Somewhat resistant';
      preferences.news_sources = ['Traditional news outlets', 'Email newsletters', 'News websites', 'LinkedIn'];
    } else if (age.includes('57-75') || age.includes('76+')) {
      preferences.social_media_platforms = ['Facebook', 'YouTube', 'LinkedIn'];
      preferences.content_types = ['News articles', 'Email newsletters', 'Traditional TV', 'Videos'];
      preferences.consumption_time = '2-4 hours';
      preferences.preferred_devices = ['Desktop', 'Tablet', 'Smart TV', 'Smartphone'];
      preferences.entertainment_preferences = ['Traditional TV', 'News', 'Documentaries', 'Movies'];
      preferences.advertising_receptivity = 'Highly resistant';
      preferences.news_sources = ['Traditional news outlets', 'Television news', 'Newspapers', 'Radio'];
    }

    // Gender-based adjustments (based on Resonate data patterns)
    if (gender === 'Female') {
      if (!preferences.social_media_platforms.includes('Pinterest')) {
        preferences.social_media_platforms.push('Pinterest');
      }
      if (!preferences.content_types.includes('Blogs')) {
        preferences.content_types.push('Blogs');
      }
      preferences.entertainment_preferences.push('Reality shows');
    } else if (gender === 'Male') {
      if (!preferences.social_media_platforms.includes('Reddit')) {
        preferences.social_media_platforms.push('Reddit');
      }
      preferences.entertainment_preferences.push('Sports');
      if (age.includes('18-24') || age.includes('25-40')) {
        preferences.entertainment_preferences.push('Gaming');
      }
    }

    // Location-based adjustments
    if (location === 'Urban') {
      preferences.content_types.push('Local news', 'Transportation apps');
      preferences.news_sources.push('Local news websites', 'City-specific apps');
    } else if (location === 'Suburban') {
      preferences.content_types.push('Family content', 'Home improvement');
      preferences.entertainment_preferences.push('Family shows');
    } else if (location === 'Rural') {
      preferences.entertainment_preferences.push('Traditional TV', 'Radio');
      preferences.news_sources.push('Local newspapers', 'Radio news');
    } else if (location === 'Coastal') {
      preferences.content_types.push('Travel content', 'Lifestyle blogs');
      preferences.entertainment_preferences.push('Travel shows');
    }

    // Occupation-based adjustments
    if (occupation?.toLowerCase().includes('executive') || occupation?.toLowerCase().includes('manager')) {
      if (!preferences.social_media_platforms.includes('LinkedIn')) {
        preferences.social_media_platforms.push('LinkedIn');
      }
      preferences.content_types.push('Business news', 'Industry reports');
      preferences.news_sources.push('Business publications', 'Industry newsletters');
      preferences.advertising_receptivity = 'Somewhat resistant';
    } else if (occupation?.toLowerCase().includes('engineer') || occupation?.toLowerCase().includes('tech')) {
      if (!preferences.social_media_platforms.includes('Reddit')) {
        preferences.social_media_platforms.push('Reddit');
      }
      preferences.content_types.push('Tech blogs', 'Podcasts');
      preferences.entertainment_preferences.push('Gaming', 'Documentaries');
    } else if (occupation?.toLowerCase().includes('healthcare')) {
      preferences.content_types.push('Professional journals', 'Health news');
      preferences.news_sources.push('Medical publications', 'Health websites');
    }

    // Income-based adjustments
    if (income?.includes('$100,000+')) {
      preferences.advertising_receptivity = 'Somewhat resistant';
      preferences.content_types.push('Premium content', 'Subscription services');
    } else if (income?.includes('$50,000') || income?.includes('$75,000')) {
      preferences.advertising_receptivity = 'Moderately receptive';
    }

    // Remove duplicates and limit selections
    preferences.social_media_platforms = [...new Set(preferences.social_media_platforms)].slice(0, 6);
    preferences.content_types = [...new Set(preferences.content_types)].slice(0, 8);
    preferences.preferred_devices = [...new Set(preferences.preferred_devices)].slice(0, 5);
    preferences.entertainment_preferences = [...new Set(preferences.entertainment_preferences)].slice(0, 6);
    preferences.news_sources = [...new Set(preferences.news_sources)];

    return preferences;
  };

  // Pre-fill based on demographics when component loads
  useEffect(() => {
    const demographics = persona?.demographics;
    
    // Only pre-fill if we have demographics and haven't already pre-filled
    if (demographics && !preFilledFromDemographics && !persona?.media_consumption?.social_media_platforms?.length) {
      console.log('Pre-filling media consumption based on demographics:', demographics);
      
      const demographicPreferences = getMediaPreferencesFromDemographics(demographics);
      
      setMediaConsumption(demographicPreferences);
      setNewsSourcesText(demographicPreferences.news_sources.join(', '));
      setPreFilledFromDemographics(true);
      setHasChanges(true);
      
      // Show notification about pre-filling
      setTimeout(() => {
        // Auto-expand sections that have pre-filled content
        setExpandedSections({
          social_media: true,
          content_consumption: true,
          devices_time: true,
          entertainment: true,
          news_advertising: true
        });
      }, 500);
    }
  }, [persona?.demographics, preFilledFromDemographics]);

  // Initialize editing state
  useEffect(() => {
    // If this is the first time on this step or coming from step 6, enable editing
    setIsEditing(true);
  }, []);

  const handleArrayChange = (field, value, isChecked = null) => {
    setHasChanges(true);
    
    if (isChecked !== null) {
      // Handle checkbox arrays
      setMediaConsumption(prev => ({
        ...prev,
        [field]: isChecked 
          ? [...prev[field], value]
          : prev[field].filter(item => item !== value)
      }));
    } else {
      // Handle text input arrays
      const items = value.split(',').map(item => item.trim()).filter(item => item);
      setMediaConsumption(prev => ({
        ...prev,
        [field]: items
      }));
    }
  };

  const handleInputChange = (field, value) => {
    setHasChanges(true);
    setMediaConsumption(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleNewsSourcesChange = (value) => {
    setHasChanges(true);
    setNewsSourcesText(value);
  };

  const handleNewsSourcesBlur = () => {
    const newsSourcesArray = newsSourcesText.split(',').map(item => item.trim()).filter(item => item);
    setMediaConsumption(prev => ({
      ...prev,
      news_sources: newsSourcesArray
    }));
  };

  const saveChanges = async () => {
    if (await updatePersona({ media_consumption: mediaConsumption })) {
      setHasChanges(false);
      setIsEditing(false);
      return true;
    }
    return false;
  };

  const handleNext = async () => {
    if (hasChanges) {
      if (await saveChanges()) {
        onNext();
      }
    } else {
      onNext();
    }
  };

  const enableEditing = () => {
    setIsEditing(true);
  };

  const cancelEditing = () => {
    // Reset to original data
    setMediaConsumption(persona?.media_consumption || {
      social_media_platforms: [],
      content_types: [],
      consumption_time: "",
      preferred_devices: [],
      news_sources: [],
      entertainment_preferences: [],
      advertising_receptivity: ""
    });
    setIsEditing(false);
    setHasChanges(false);
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const renderCollapsibleSection = (sectionKey, title, icon, children, hasContent = false) => {
    const isExpanded = expandedSections[sectionKey];
    
    return (
      <div className="border border-gray-200 rounded-lg mb-4 overflow-hidden">
        <button
          type="button"
          onClick={() => toggleSection(sectionKey)}
          disabled={!isEditing}
          className={`w-full px-4 py-3 flex items-center justify-between text-left transition-colors duration-200 ${
            isEditing ? 'hover:bg-gray-50 cursor-pointer' : 'cursor-not-allowed'
          } ${hasContent ? 'bg-blue-50 border-l-4 border-blue-400' : 'bg-gray-50'}`}
        >
          <div className="flex items-center">
            <div className="mr-3 text-xl">{icon}</div>
            <div>
              <h3 className="font-semibold font-montserrat bcm-heading text-sm">{title}</h3>
              {hasContent && (
                <span className="text-xs text-blue-600 font-montserrat">✓ Has data</span>
              )}
            </div>
          </div>
          <div className="flex items-center">
            {!isEditing && (
              <span className="text-xs text-gray-500 mr-2 font-montserrat">View Only</span>
            )}
            <svg 
              className={`w-5 h-5 text-gray-500 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </button>
        
        {isExpanded && (
          <div className="p-4 bg-white border-t border-gray-200">
            {children}
          </div>
        )}
      </div>
    );
  };

  const socialPlatforms = [
    "Facebook", "Instagram", "Twitter/X", "LinkedIn", "TikTok", 
    "YouTube", "Snapchat", "Pinterest", "Reddit", "Discord"
  ];

  const contentTypes = [
    "News articles", "Social media posts", "Videos", "Podcasts", 
    "Blogs", "Email newsletters", "Streaming shows", "Live streams",
    "Stories/Reels", "User-generated content"
  ];

  const devices = [
    "Smartphone", "Tablet", "Laptop", "Desktop", "Smart TV", 
    "Smart speaker", "Gaming console", "Wearable device"
  ];

  const entertainmentOptions = [
    "Streaming services", "Traditional TV", "Movies", "Music", 
    "Gaming", "Sports", "Documentaries", "Reality shows", 
    "Comedy", "Drama series"
  ];

  return (
    <div className={`form-section ${isEditing ? 'editable-section editing' : 'editable-section'}`}>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-xl font-bold font-montserrat bcm-heading">Media Consumption</h2>
          <p className="text-gray-600 font-montserrat">
            Define how this persona consumes media and content. <span className="text-sm text-gray-500">(All sections are optional)</span>
          </p>
        </div>
        
        {!isEditing && (
          <button
            onClick={enableEditing}
            className="bcm-btn-outline text-sm"
          >
            <svg className="w-4 h-4 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit
          </button>
        )}
      </div>

      {preFilledFromDemographics && (
        <div className="mb-6 p-4 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="w-5 h-5 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800 font-montserrat">
                🎯 AI-Generated Media Preferences
              </h3>
              <p className="text-sm text-green-700 mt-1 font-montserrat">
                Based on the demographic profile you provided, we've pre-filled media consumption preferences using Resonate AI data patterns. 
                These selections reflect typical behaviors for someone with this demographic profile. You can review and adjust any selections as needed.
              </p>
              <div className="mt-2 text-xs text-green-600 font-montserrat">
                <strong>Generated from:</strong> {persona?.demographics?.age_range && `${persona.demographics.age_range} age group`}
                {persona?.demographics?.gender && `, ${persona.demographics.gender}`}
                {persona?.demographics?.location && `, ${persona.demographics.location} location`}
                {persona?.demographics?.occupation && `, ${persona.demographics.occupation}`}
              </div>
            </div>
          </div>
        </div>
      )}

      {!isEditing && (
        <div className="mb-6 p-3 bg-blue-50 border border-blue-200 rounded-md">
          <p className="text-blue-800 text-sm font-montserrat">
            <svg className="w-4 h-4 mr-1 inline" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
            You can edit your media consumption preferences. Click "Edit" above to make changes.
          </p>
        </div>
      )}

      <div className="space-y-4">
        {/* Social Media Section */}
        {renderCollapsibleSection(
          'social_media',
          'Social Media Platforms',
          '📱',
          (
            <div>
              <p className="text-sm text-gray-600 mb-3 font-montserrat">Which social media platforms does this persona use?</p>
              <div className="media-checkbox-group">
                {socialPlatforms.map(platform => (
                  <div key={platform} className="media-checkbox-item">
                    <input
                      type="checkbox"
                      id={`platform-${platform}`}
                      checked={mediaConsumption.social_media_platforms.includes(platform)}
                      onChange={(e) => handleArrayChange("social_media_platforms", platform, e.target.checked)}
                      disabled={!isEditing}
                      className="media-checkbox"
                    />
                    <label htmlFor={`platform-${platform}`} className="text-sm text-gray-700 font-montserrat">
                      {platform}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          ),
          mediaConsumption.social_media_platforms.length > 0
        )}

        {/* Content Consumption Section */}
        {renderCollapsibleSection(
          'content_consumption',
          'Content Types & Consumption',
          '📺',
          (
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600 mb-3 font-montserrat">What types of content does this persona consume?</p>
                <div className="media-checkbox-group">
                  {contentTypes.map(type => (
                    <div key={type} className="media-checkbox-item">
                      <input
                        type="checkbox"
                        id={`content-${type}`}
                        checked={mediaConsumption.content_types.includes(type)}
                        onChange={(e) => handleArrayChange("content_types", type, e.target.checked)}
                        disabled={!isEditing}
                        className="media-checkbox"
                      />
                      <label htmlFor={`content-${type}`} className="text-sm text-gray-700 font-montserrat">
                        {type}
                      </label>
                    </div>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                  Daily Consumption Time
                </label>
                <select
                  value={mediaConsumption.consumption_time}
                  onChange={(e) => handleInputChange("consumption_time", e.target.value)}
                  disabled={!isEditing}
                  className="form-field font-montserrat"
                >
                  <option value="">Select time spent</option>
                  <option value="Less than 1 hour">Less than 1 hour</option>
                  <option value="1-2 hours">1-2 hours</option>
                  <option value="2-4 hours">2-4 hours</option>
                  <option value="4-6 hours">4-6 hours</option>
                  <option value="6+ hours">6+ hours</option>
                </select>
              </div>
            </div>
          ),
          mediaConsumption.content_types.length > 0 || mediaConsumption.consumption_time
        )}

        {/* Devices Section */}
        {renderCollapsibleSection(
          'devices_time',
          'Preferred Devices',
          '💻',
          (
            <div>
              <p className="text-sm text-gray-600 mb-3 font-montserrat">Which devices does this persona use for media consumption?</p>
              <div className="media-checkbox-group">
                {devices.map(device => (
                  <div key={device} className="media-checkbox-item">
                    <input
                      type="checkbox"
                      id={`device-${device}`}
                      checked={mediaConsumption.preferred_devices.includes(device)}
                      onChange={(e) => handleArrayChange("preferred_devices", device, e.target.checked)}
                      disabled={!isEditing}
                      className="media-checkbox"
                    />
                    <label htmlFor={`device-${device}`} className="text-sm text-gray-700 font-montserrat">
                      {device}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          ),
          mediaConsumption.preferred_devices.length > 0
        )}

        {/* Entertainment Section */}
        {renderCollapsibleSection(
          'entertainment',
          'Entertainment Preferences',
          '🎬',
          (
            <div>
              <p className="text-sm text-gray-600 mb-3 font-montserrat">What entertainment content does this persona prefer?</p>
              <div className="media-checkbox-group">
                {entertainmentOptions.map(option => (
                  <div key={option} className="media-checkbox-item">
                    <input
                      type="checkbox"
                      id={`entertainment-${option}`}
                      checked={mediaConsumption.entertainment_preferences.includes(option)}
                      onChange={(e) => handleArrayChange("entertainment_preferences", option, e.target.checked)}
                      disabled={!isEditing}
                      className="media-checkbox"
                    />
                    <label htmlFor={`entertainment-${option}`} className="text-sm text-gray-700 font-montserrat">
                      {option}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          ),
          mediaConsumption.entertainment_preferences.length > 0
        )}

        {/* News & Advertising Section */}
        {renderCollapsibleSection(
          'news_advertising',
          'News & Advertising',
          '📰',
          (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                  News Sources
                </label>
                <textarea
                  value={newsSourcesText}
                  onChange={(e) => handleNewsSourcesChange(e.target.value)}
                  onBlur={handleNewsSourcesBlur}
                  disabled={!isEditing}
                  placeholder="Enter news sources separated by commas (e.g., CNN, BBC, Reuters, Local news)"
                  className="form-field h-20 font-montserrat"
                />
                <p className="text-xs text-gray-500 mt-1 font-montserrat">Where does this persona get their news?</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                  Advertising Receptivity
                </label>
                <select
                  value={mediaConsumption.advertising_receptivity}
                  onChange={(e) => handleInputChange("advertising_receptivity", e.target.value)}
                  disabled={!isEditing}
                  className="form-field font-montserrat"
                >
                  <option value="">Select receptivity</option>
                  <option value="Highly receptive">Highly receptive</option>
                  <option value="Moderately receptive">Moderately receptive</option>
                  <option value="Somewhat resistant">Somewhat resistant</option>
                  <option value="Highly resistant">Highly resistant</option>
                </select>
                <p className="text-xs text-gray-500 mt-1 font-montserrat">How does this persona respond to advertising?</p>
              </div>
            </div>
          ),
          newsSourcesText || mediaConsumption.advertising_receptivity
        )}
      </div>

      {isEditing && hasChanges && (
        <div className="mt-6 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
          <p className="text-yellow-800 text-sm font-montserrat">
            You have unsaved changes. Make sure to save before proceeding.
          </p>
        </div>
      )}

      <div className="flex justify-between mt-6">
        <button onClick={onPrev} className="bcm-btn-secondary">
          Back
        </button>
        
        <div className="flex space-x-3">
          {isEditing && (
            <>
              <button
                onClick={cancelEditing}
                className="bcm-btn-outline"
                disabled={saving}
              >
                Cancel
              </button>
              <button
                onClick={saveChanges}
                disabled={saving || !hasChanges}
                className="bcm-btn-secondary disabled:opacity-50"
              >
                {saving ? "Saving..." : "Save Changes"}
              </button>
            </>
          )}
          
          <button
            onClick={handleNext}
            disabled={saving || (isEditing && hasChanges)}
            className="bcm-btn-primary disabled:opacity-50"
          >
            {saving ? "Saving..." : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default MediaConsumptionStep;

import React, { useState } from "react";

const AttributesStep = ({ persona, updatePersona, onNext, onPrev, saving, isFirstStep }) => {
  const [attributes, setAttributes] = useState(persona?.attributes || {
    selectedVertical: '',
    selectedCategory: '',
    selectedBehaviors: [],
    interests: [],
    behaviors: [],
    values: [],
    purchase_motivations: [],
    preferred_brands: [],
    lifestyle: []
  });

  // Resonate Taxonomy structure
  const resonateTaxonomy = {
    "Retail": {
      "Preferences & Psychographics": [
        "Personal values", "Retail selection traits", "Apparel drivers", "Furniture drivers", 
        "Quality-focused", "Price-conscious", "Brand loyal", "Trend-following", "Sustainable shopping"
      ],
      "Market Behaviors": [
        "Past purchases", "Future purchases", "Brands shopped", "Online vs in-store", 
        "Holiday shopping", "Name-brand loyalty", "Impulse buying", "Research-heavy shopping"
      ],
      "In-Market": [
        "Apparel shopping", "Electronics shopping", "Home goods shopping", "Future spending plans",
        "Seasonal purchases", "Gift buying", "Home improvement", "Fashion updates"
      ],
      "Media & Demographics": [
        "Age group", "Gender", "Income level", "Ethnicity", "Device usage", "Channel preferences",
        "Social media engagement", "Digital vs traditional media"
      ]
    },
    "CPG": {
      "Preferences & Psychographics": [
        "Snack reasons", "Vitamin reasons", "Beauty routines", "Food sustainability", 
        "Shopping attitudes", "Health consciousness", "Convenience seeking", "Organic preference"
      ],
      "Market Behaviors": [
        "Product types", "Brand preferences", "Spending levels", "Purchase methods",
        "Bulk buying", "Subscription services", "Store loyalty", "Coupon usage"
      ],
      "In-Market": [
        "Online grocery", "Beverage frequency", "Snack frequency", "Pet food brands",
        "Personal care", "Household essentials", "Health supplements", "Beauty products"
      ],
      "Media & Demographics": [
        "Streaming usage", "Platform engagement", "TV network preferences", "Digital content consumption",
        "Mobile app usage", "Email engagement", "Video content", "Social commerce"
      ]
    },
    "Financial Services": {
      "Preferences & Psychographics": [
        "Credit card features", "Bank switching reasons", "Insurance priorities", "Crypto motivators",
        "NFT motivators", "Investment philosophy", "Risk tolerance", "Financial planning approach"
      ],
      "Market Behaviors": [
        "Bank account types", "Insurance coverage", "Investment firms", "Trading frequency",
        "Digital banking", "Mobile payments", "Credit management", "Savings habits"
      ],
      "In-Market": [
        "Credit card applications", "Loan shopping", "Insurance switches", "Life changes",
        "Investment planning", "Retirement planning", "Home buying", "Business banking"
      ],
      "Media & Demographics": [
        "Financial TV shows", "Device preferences", "Digital usage by product", "News consumption",
        "Professional networks", "Investment apps", "Financial podcasts", "Advisory services"
      ]
    },
    "Health & Pharma": {
      "Conditions": [
        "Diabetes", "Cardiac conditions", "Autoimmune disorders", "Mental health", "Allergies",
        "Chronic pain", "Sleep disorders", "Digestive issues", "Skin conditions", "Vision issues"
      ],
      "Health Management": [
        "Vaccine likelihood", "Diet intentions", "Doctor visits", "OTC medications",
        "Preventive care", "Wellness programs", "Fitness routines", "Mental health support"
      ],
      "Pharma Personality": [
        "Rx compliance", "Doctor trust", "Information sources", "Generic preference",
        "Alternative medicine", "Clinical trials", "Side effect concerns", "Cost sensitivity"
      ],
      "Caregiver Role": [
        "Caregiver type", "Services provided", "Care recipient", "Support needs",
        "Time commitment", "Emotional support", "Medical advocacy", "Care coordination"
      ],
      "Media & Demographics": [
        "Health content engagement", "Medical information sources", "Channel preferences",
        "Age considerations", "Gender factors", "Digital health tools", "Telemedicine usage"
      ]
    },
    "Automotive": {
      "Preferences & Psychographics": [
        "Brand preferences", "Green vehicles", "Important features", "Owner mindset",
        "Performance vs efficiency", "Safety priorities", "Technology features", "Style preferences"
      ],
      "Market Behaviors": [
        "Make/model preferences", "Cost considerations", "Ownership patterns", "New vs used",
        "Financing options", "Trade-in behavior", "Maintenance approach", "Upgrade frequency"
      ],
      "In-Market": [
        "Purchase timeframe", "Auto brand consideration", "EV likelihood", "Feature priorities",
        "Budget range", "Financing needs", "Trade-in timing", "Research phase"
      ],
      "Media & Demographics": [
        "Channel engagement", "Show preferences", "Creative strategy", "Digital touchpoints",
        "Dealer interactions", "Review platforms", "Social influence", "Video content"
      ]
    },
    "Travel": {
      "Preferences & Psychographics": [
        "Cruise line choice", "Hotel selection", "Leisure trip reasons", "Travel style",
        "Adventure vs relaxation", "Cultural interests", "Budget considerations", "Group vs solo"
      ],
      "Market Behaviors": [
        "Booking methods", "Loyalty programs", "Past destinations", "Travel frequency",
        "Advance planning", "Last-minute deals", "Package vs individual", "Travel insurance"
      ],
      "In-Market": [
        "Vacation spending", "Cruise intent", "Luggage purchases", "Destination research",
        "Accommodation booking", "Activity planning", "Transportation needs", "Travel gear"
      ],
      "Media & Demographics": [
        "Tablet usage", "Streaming services", "Holiday timing", "Travel content consumption",
        "Social sharing", "Review platforms", "Travel apps", "Inspiration sources"
      ]
    },
    "Technology & Telecom": {
      "Preferences & Psychographics": [
        "Provider switching reasons", "Service speed importance", "Price sensitivity", "Feature priorities",
        "Data usage patterns", "Device preferences", "Innovation adoption", "Customer service expectations"
      ],
      "Market Behaviors": [
        "Current provider", "Contract status", "Service bundles", "Device upgrade patterns",
        "Family plans", "Business services", "Add-on services", "Payment methods"
      ],
      "In-Market": [
        "Switch intent", "Data usage growth", "Device upgrades", "Service changes",
        "Plan optimization", "New features", "Coverage needs", "Cost reduction"
      ],
      "Media & Demographics": [
        "Platform usage", "Device consumption", "Tech content engagement", "Digital behavior",
        "Social media activity", "Streaming patterns", "Gaming behavior", "App usage"
      ]
    },
    "Political & Advocacy": {
      "Values & Motivations": [
        "Equality", "Environmentalism", "Community safety", "Freedom", "Justice",
        "Economic policy", "Social issues", "Foreign policy", "Local governance", "Civil rights"
      ],
      "Positioning": [
        "Gun control", "Abortion rights", "Climate change", "Immigration", "Healthcare",
        "Education policy", "Tax policy", "Criminal justice", "Workers' rights", "Religious freedom"
      ],
      "In-Market": [
        "Issue-based engagement", "Voting behavior", "Donation patterns", "Volunteer activities",
        "Petition signing", "Rally attendance", "Advocacy campaigns", "Policy awareness"
      ],
      "Media & Demographics": [
        "Social/CTV engagement", "Political content consumption", "News sources", "Information sharing",
        "Fact-checking behavior", "Echo chamber awareness", "Cross-party dialogue", "Civic participation"
      ]
    }
  };

  // Store raw text values for editing
  const [textValues, setTextValues] = useState({
    interests: persona?.attributes?.interests?.join(', ') || '',
    behaviors: persona?.attributes?.behaviors?.join(', ') || '',
    values: persona?.attributes?.values?.join(', ') || '',
    purchase_motivations: persona?.attributes?.purchase_motivations?.join(', ') || '',
    preferred_brands: persona?.attributes?.preferred_brands?.join(', ') || '',
    lifestyle: persona?.attributes?.lifestyle?.join(', ') || ''
  });

  const handleVerticalChange = (vertical) => {
    setAttributes(prev => ({
      ...prev,
      selectedVertical: vertical,
      selectedCategory: '',
      selectedBehaviors: []
    }));
  };

  const handleCategoryChange = (category) => {
    setAttributes(prev => ({
      ...prev,
      selectedCategory: category,
      selectedBehaviors: []
    }));
  };

  const handleBehaviorToggle = (behavior) => {
    setAttributes(prev => ({
      ...prev,
      selectedBehaviors: prev.selectedBehaviors.includes(behavior)
        ? prev.selectedBehaviors.filter(b => b !== behavior)
        : [...prev.selectedBehaviors, behavior]
    }));
  };

  const handleTextChange = (field, value) => {
    setTextValues(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleTextBlur = (field, value) => {
    const items = value.split(',').map(item => item.trim()).filter(item => item);
    setAttributes(prev => ({
      ...prev,
      [field]: items
    }));
  };

  const handleNext = async () => {
    if (await updatePersona({ attributes })) {
      onNext();
    }
  };

  const getAvailableCategories = () => {
    return attributes.selectedVertical ? Object.keys(resonateTaxonomy[attributes.selectedVertical]) : [];
  };

  const getAvailableBehaviors = () => {
    return (attributes.selectedVertical && attributes.selectedCategory) 
      ? resonateTaxonomy[attributes.selectedVertical][attributes.selectedCategory] 
      : [];
  };

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold mb-4 font-montserrat">Attributes & Behaviors</h2>
      <p className="text-gray-600 mb-6 font-montserrat">
        Select from the Resonate Taxonomy to define behavioral characteristics and motivations, or add custom attributes.
      </p>

      <div className="space-y-6">
        {/* Resonate Taxonomy Selection */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border border-blue-200">
          <h3 className="text-lg font-semibold mb-4 font-montserrat text-blue-900">
            🎯 Resonate Taxonomy Selection
          </h3>
          
          {/* Vertical Selection */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
              Select Industry Vertical
            </label>
            <select
              value={attributes.selectedVertical}
              onChange={(e) => handleVerticalChange(e.target.value)}
              className="form-field font-montserrat"
            >
              <option value="">Choose a vertical...</option>
              {Object.keys(resonateTaxonomy).map(vertical => (
                <option key={vertical} value={vertical}>{vertical}</option>
              ))}
            </select>
          </div>

          {/* Category Selection */}
          {attributes.selectedVertical && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                Select Category
              </label>
              <select
                value={attributes.selectedCategory}
                onChange={(e) => handleCategoryChange(e.target.value)}
                className="form-field font-montserrat"
              >
                <option value="">Choose a category...</option>
                {getAvailableCategories().map(category => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
            </div>
          )}

          {/* Behavior Selection */}
          {attributes.selectedCategory && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                Select Behaviors ({attributes.selectedBehaviors.length} selected)
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 max-h-60 overflow-y-auto border border-gray-200 rounded p-3 bg-white">
                {getAvailableBehaviors().map(behavior => (
                  <label key={behavior} className="flex items-start space-x-2 cursor-pointer hover:bg-gray-50 p-2 rounded">
                    <input
                      type="checkbox"
                      checked={attributes.selectedBehaviors.includes(behavior)}
                      onChange={() => handleBehaviorToggle(behavior)}
                      className="mt-1 flex-shrink-0"
                    />
                    <span className="text-sm font-montserrat text-gray-700">{behavior}</span>
                  </label>
                ))}
              </div>
              {attributes.selectedBehaviors.length > 0 && (
                <div className="mt-2 text-sm text-blue-600 font-montserrat">
                  <strong>Selected:</strong> {attributes.selectedBehaviors.join(', ')}
                </div>
              )}
            </div>
          )}
        </div>

        <div className="border-t border-gray-200 pt-6">
          <h3 className="text-lg font-semibold mb-4 font-montserrat text-gray-800">
            ✏️ Custom Attributes (Optional)
          </h3>
          <p className="text-sm text-gray-600 mb-4 font-montserrat">
            Add additional custom attributes that aren't covered in the taxonomy above.
          </p>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                Interests & Hobbies
              </label>
              <textarea
                value={textValues.interests}
                onChange={(e) => handleTextChange("interests", e.target.value)}
                onBlur={(e) => handleTextBlur("interests", e.target.value)}
                placeholder="Enter interests separated by commas"
                className="form-field h-24 font-montserrat"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                Behaviors & Habits
              </label>
              <textarea
                value={textValues.behaviors}
                onChange={(e) => handleTextChange("behaviors", e.target.value)}
                onBlur={(e) => handleTextBlur("behaviors", e.target.value)}
                placeholder="Enter behaviors separated by commas"
                className="form-field h-24 font-montserrat"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                Core Values
              </label>
              <textarea
                value={textValues.values}
                onChange={(e) => handleTextChange("values", e.target.value)}
                onBlur={(e) => handleTextBlur("values", e.target.value)}
                placeholder="Enter values separated by commas"
                className="form-field h-24 font-montserrat"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                Purchase Motivations
              </label>
              <textarea
                value={textValues.purchase_motivations}
                onChange={(e) => handleTextChange("purchase_motivations", e.target.value)}
                onBlur={(e) => handleTextBlur("purchase_motivations", e.target.value)}
                placeholder="Enter motivations separated by commas"
                className="form-field h-24 font-montserrat"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                Preferred Brands
              </label>
              <textarea
                value={textValues.preferred_brands}
                onChange={(e) => handleTextChange("preferred_brands", e.target.value)}
                onBlur={(e) => handleTextBlur("preferred_brands", e.target.value)}
                placeholder="Enter brands separated by commas"
                className="form-field h-24 font-montserrat"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
                Lifestyle Traits
              </label>
              <textarea
                value={textValues.lifestyle}
                onChange={(e) => handleTextChange("lifestyle", e.target.value)}
                onBlur={(e) => handleTextBlur("lifestyle", e.target.value)}
                placeholder="Enter lifestyle traits separated by commas"
                className="form-field h-24 font-montserrat"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-between mt-6">
        {!isFirstStep && (
          <button onClick={onPrev} className="btn-secondary">
            Back
          </button>
        )}
        <button
          onClick={handleNext}
          disabled={saving}
          className="btn-primary disabled:opacity-50 ml-auto"
        >
          {saving ? "Saving..." : "Next"}
        </button>
      </div>
    </div>
  );
};

export default AttributesStep;

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
    "Values & Motivations": {
      "Core Values": [
        "Family values", "Personal achievement", "Social responsibility", "Financial security", 
        "Freedom & independence", "Creativity & self-expression", "Health & wellness", "Spirituality"
      ],
      "Motivational Drivers": [
        "Status seeking", "Quality focused", "Value conscious", "Convenience driven", 
        "Experience seeking", "Innovation adoption", "Tradition respect", "Community belonging"
      ],
      "Life Priorities": [
        "Career advancement", "Work-life balance", "Family time", "Personal growth",
        "Financial stability", "Health maintenance", "Social connections", "Environmental impact"
      ]
    },
    "Demographics": {
      "Age & Generation": [
        "Gen Z (18-24)", "Millennials (25-40)", "Gen X (41-56)", "Baby Boomers (57-75)", "Silent Generation (76+)"
      ],
      "Geographic": [
        "Urban dwellers", "Suburban families", "Rural communities", "Coastal residents", 
        "City center professionals", "Small town residents", "Metropolitan areas"
      ],
      "Income & Employment": [
        "High income ($100K+)", "Middle income ($50K-100K)", "Lower income (<$50K)", 
        "Professional workers", "Blue collar workers", "Entrepreneurs", "Retirees", "Students"
      ],
      "Life Stage": [
        "Young professionals", "New parents", "Established families", "Empty nesters", 
        "Pre-retirees", "Active retirees", "Single households", "Multi-generational families"
      ]
    },
    "Consumer Preferences": {
      "Shopping Behaviors": [
        "Online shopping preference", "In-store experience seekers", "Comparison shoppers", "Impulse buyers",
        "Brand loyal customers", "Deal hunters", "Quality over price", "Sustainable shoppers"
      ],
      "Purchase Motivations": [
        "Necessity purchases", "Emotional purchases", "Status purchases", "Gift giving",
        "Investment mindset", "Immediate gratification", "Research-heavy decisions", "Peer influenced"
      ],
      "Brand Relationships": [
        "Premium brand preference", "Value brand focus", "Local brand support", "Innovation seekers",
        "Trusted brand loyalty", "New brand exploration", "Ethical brand alignment", "Celebrity endorsed"
      ]
    },
    "Media": {
      "Content Consumption": [
        "Social media heavy users", "Traditional TV watchers", "Streaming service subscribers", "Podcast listeners",
        "News readers", "YouTube viewers", "TikTok users", "Instagram engaged", "LinkedIn professionals"
      ],
      "Device Preferences": [
        "Mobile-first users", "Desktop workers", "Tablet consumers", "Smart TV viewers",
        "Wearable tech users", "Gaming console players", "Smart home adopters", "Voice assistant users"
      ],
      "Information Sources": [
        "Peer recommendations", "Expert reviews", "Influencer content", "Brand direct communication",
        "News media", "Social proof", "User-generated content", "Professional networks"
      ]
    },
    "Retail": {
      "Shopping Preferences": [
        "Department store shoppers", "Boutique explorers", "Discount store hunters", "Online marketplace users",
        "Direct-to-consumer buyers", "Subscription service users", "Pop-up store visitors", "Warehouse club members"
      ],
      "Retail Behaviors": [
        "Seasonal shoppers", "Sales event participants", "Early adopters", "Last-minute buyers",
        "Bulk purchasers", "Frequent returners", "Review writers", "Social sharers"
      ],
      "Store Loyalty": [
        "Single retailer loyal", "Multi-store shoppers", "Private label buyers", "Member program participants",
        "Store credit card users", "Mobile app users", "Email subscriber", "Rewards program active"
      ]
    },
    "Apparel": {
      "Fashion Preferences": [
        "Trend followers", "Classic style preference", "Casual wear focus", "Professional attire",
        "Athletic wear enthusiasts", "Luxury fashion buyers", "Vintage/thrift shoppers", "Sustainable fashion"
      ],
      "Shopping Patterns": [
        "Seasonal wardrobe updates", "Occasion-based buying", "Investment piece focus", "Fast fashion consumers",
        "Brand loyal shoppers", "Size-inclusive shoppers", "Color-coordinated buyers", "Style influencer followers"
      ],
      "Fit & Function": [
        "Comfort prioritized", "Performance features", "Professional appearance", "Casual lifestyle",
        "Active lifestyle", "Climate considerations", "Body type considerations", "Age-appropriate styling"
      ]
    },
    "Home & Family": {
      "Home Priorities": [
        "Interior design focused", "Functionality over aesthetics", "Smart home technology", "Energy efficiency",
        "Family-friendly spaces", "Entertainment areas", "Home office setup", "Outdoor living spaces"
      ],
      "Family Dynamics": [
        "Child-centered decisions", "Pet-friendly choices", "Multi-generational living", "Single-person households",
        "Couple without children", "Blended families", "Empty nest adjustments", "Caregiver responsibilities"
      ],
      "Household Management": [
        "Organized & planned", "Spontaneous & flexible", "Budget-conscious", "Time-saving solutions",
        "DIY enthusiasts", "Professional service users", "Technology adopters", "Traditional methods"
      ]
    },
    "Health & Pharma": {
      "Health Attitudes": [
        "Preventive care focused", "Treatment-oriented", "Natural/alternative medicine", "Traditional medicine",
        "Health optimization", "Condition management", "Wellness lifestyle", "Medical skepticism"
      ],
      "Healthcare Behaviors": [
        "Regular check-ups", "Symptom-driven visits", "Specialist consultations", "Self-diagnosis attempts",
        "Second opinion seekers", "Medication compliant", "Side effect concerned", "Cost-conscious care"
      ],
      "Wellness Practices": [
        "Fitness routine followers", "Nutrition conscious", "Mental health aware", "Stress management",
        "Sleep quality focused", "Supplement users", "Meditation/mindfulness", "Work-life balance seekers"
      ]
    },
    "Restaurants": {
      "Dining Preferences": [
        "Fine dining experiences", "Casual family restaurants", "Fast-casual options", "Quick service needs",
        "Local establishment support", "Chain restaurant familiarity", "Ethnic cuisine exploration", "Comfort food preference"
      ],
      "Dining Behaviors": [
        "Frequent dine-out", "Occasion-based dining", "Takeout/delivery preference", "Meal planning focused",
        "Social dining experiences", "Solo dining comfortable", "Group event organizers", "Food adventure seekers"
      ],
      "Food Values": [
        "Quality ingredients", "Value pricing", "Healthy options", "Indulgent treats",
        "Local sourcing", "Sustainable practices", "Cultural authenticity", "Innovation/fusion"
      ]
    },
    "Food & Non-Alcoholic Beverages": {
      "Consumption Patterns": [
        "Health-conscious choices", "Convenience-driven purchases", "Premium product preference", "Value-seeking behavior",
        "Organic/natural focus", "Processed food acceptance", "Local/artisanal support", "Global brand preference"
      ],
      "Beverage Preferences": [
        "Coffee culture participants", "Tea enthusiasts", "Soft drink consumers", "Energy drink users",
        "Health drink adopters", "Sparkling water fans", "Juice drink preference", "Sports drink users"
      ],
      "Dietary Considerations": [
        "No dietary restrictions", "Vegetarian/vegan", "Gluten-free needs", "Low-carb/keto",
        "Organic preference", "Non-GMO focus", "Allergen awareness", "Portion-controlled eating"
      ]
    },
    "Alcohol & Tobacco": {
      "Alcohol Consumption": [
        "Social drinkers", "Wine enthusiasts", "Craft beer lovers", "Spirit connoisseurs",
        "Occasional drinkers", "Health-conscious drinkers", "Non-alcoholic alternative seekers", "Abstainers"
      ],
      "Drinking Occasions": [
        "Social gatherings", "Dinner accompaniment", "Celebration events", "Relaxation moments",
        "Professional networking", "Cultural experiences", "Special occasions only", "Daily routine"
      ],
      "Tobacco Attitudes": [
        "Non-users", "Former users", "Occasional users", "Regular users",
        "Alternative product users", "Cessation interested", "Social smokers", "Health-concerned users"
      ]
    },
    "Automotive": {
      "Vehicle Preferences": [
        "Luxury vehicle buyers", "Practical transportation", "Performance enthusiasts", "Eco-friendly options",
        "Family-oriented features", "Technology-rich vehicles", "Classic/vintage interest", "Utility/work vehicles"
      ],
      "Purchase Behavior": [
        "New car buyers", "Used car shoppers", "Lease preference", "Cash purchasers",
        "Trade-in focused", "Brand loyal customers", "Deal negotiators", "Research-heavy buyers"
      ],
      "Ownership Patterns": [
        "Long-term ownership", "Frequent upgraders", "Multi-vehicle households", "Single vehicle reliance",
        "Car sharing users", "Public transport preference", "Walking/cycling focused", "Ride-sharing regular"
      ]
    },
    "Financial Services & Insurance": {
      "Financial Attitudes": [
        "Conservative investors", "Aggressive growth seekers", "Risk-averse savers", "Diversification focused",
        "DIY financial management", "Professional advice seekers", "Technology adopters", "Traditional banking preference"
      ],
      "Banking Behaviors": [
        "Digital banking users", "Branch visit preference", "Multiple account holders", "Single bank loyalty",
        "Mobile payment users", "Cash preference", "Credit utilizers", "Debit-focused users"
      ],
      "Insurance Priorities": [
        "Comprehensive coverage", "Minimum required coverage", "Premium service expectations", "Cost-focused decisions",
        "Bundle service preference", "Individual policy management", "Claim experience influenced", "Prevention focused"
      ]
    },
    "Technology & Telecom": {
      "Technology Adoption": [
        "Early adopters", "Mainstream users", "Late adopters", "Technology resistant",
        "Innovation enthusiasts", "Practical feature focused", "Brand ecosystem loyal", "Best value seekers"
      ],
      "Device Usage": [
        "Smartphone dependent", "Multi-device users", "Computer-centric", "Tablet preference",
        "Gaming focused", "Streaming optimized", "Work productivity tools", "Social connection devices"
      ],
      "Service Expectations": [
        "Premium service level", "Basic needs coverage", "Unlimited usage plans", "Pay-per-use preference",
        "Family plan users", "Individual account holders", "Business service needs", "International usage"
      ]
    },
    "Travel & Hospitality": {
      "Travel Preferences": [
        "Luxury experiences", "Budget-conscious travel", "Adventure seekers", "Relaxation focused",
        "Cultural exploration", "Business travel frequent", "Family-friendly options", "Solo travel comfortable"
      ],
      "Booking Behaviors": [
        "Direct booking preference", "Third-party platform users", "Last-minute planners", "Advance reservation makers",
        "Package deal seekers", "À la carte customizers", "Loyalty program participants", "Deal comparison shoppers"
      ],
      "Travel Frequency": [
        "Frequent travelers", "Occasional vacationers", "Business trip regular", "Weekend getaway preference",
        "Annual vacation takers", "Spontaneous trip makers", "Seasonal travelers", "Staycation preference"
      ]
    },
    "Politics & Advocacy": {
      "Political Engagement": [
        "Highly engaged voters", "Occasional participants", "Issue-focused advocates", "Party loyal supporters",
        "Independent thinkers", "Politically disengaged", "Local politics focused", "National politics followers"
      ],
      "Advocacy Interests": [
        "Environmental causes", "Social justice issues", "Economic policies", "Healthcare advocacy",
        "Education reform", "Civil rights support", "Veterans affairs", "Religious freedom"
      ],
      "Information Sources": [
        "Multiple news sources", "Single source preference", "Social media informed", "Traditional media reliance",
        "Peer discussion influenced", "Expert analysis seekers", "Primary source researchers", "Headline scanners"
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

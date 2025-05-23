import React, { useState } from "react";

const AttributesStep = ({ persona, updatePersona, onNext, onPrev, saving, isFirstStep }) => {
  const [attributes, setAttributes] = useState(persona?.attributes || {
    interests: [],
    behaviors: [],
    values: [],
    purchase_motivations: [],
    preferred_brands: [],
    lifestyle: []
  });

  // Store raw text values for editing
  const [textValues, setTextValues] = useState({
    interests: persona?.attributes?.interests?.join(', ') || '',
    behaviors: persona?.attributes?.behaviors?.join(', ') || '',
    values: persona?.attributes?.values?.join(', ') || '',
    purchase_motivations: persona?.attributes?.purchase_motivations?.join(', ') || '',
    preferred_brands: persona?.attributes?.preferred_brands?.join(', ') || '',
    lifestyle: persona?.attributes?.lifestyle?.join(', ') || ''
  });

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

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold mb-4">Attributes & Behaviors</h2>
      <p className="text-gray-600 mb-6">
        Define the behavioral characteristics, interests, and motivations of your persona.
      </p>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Interests & Hobbies
          </label>
          <textarea
            value={textValues.interests}
            onChange={(e) => handleTextChange("interests", e.target.value)}
            onBlur={(e) => handleTextBlur("interests", e.target.value)}
            placeholder="Enter interests separated by commas (e.g., technology, fitness, travel, cooking)"
            className="form-field h-24 font-montserrat"
          />
          <p className="text-xs text-gray-500 mt-1">
            What does this persona enjoy doing in their free time?
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Behaviors & Habits
          </label>
          <textarea
            value={textValues.behaviors}
            onChange={(e) => handleTextChange("behaviors", e.target.value)}
            onBlur={(e) => handleTextBlur("behaviors", e.target.value)}
            placeholder="Enter behaviors separated by commas (e.g., shops online frequently, researches before buying)"
            className="form-field h-24 font-montserrat"
          />
          <p className="text-xs text-gray-500 mt-1 font-montserrat">
            How does this persona typically behave or act?
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
            Core Values
          </label>
          <textarea
            value={textValues.values}
            onChange={(e) => handleTextChange("values", e.target.value)}
            onBlur={(e) => handleTextBlur("values", e.target.value)}
            placeholder="Enter values separated by commas (e.g., sustainability, family, innovation, quality)"
            className="form-field h-24 font-montserrat"
          />
          <p className="text-xs text-gray-500 mt-1 font-montserrat">
            What principles and beliefs guide this persona's decisions?
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
            Purchase Motivations
          </label>
          <textarea
            value={textValues.purchase_motivations}
            onChange={(e) => handleTextChange("purchase_motivations", e.target.value)}
            onBlur={(e) => handleTextBlur("purchase_motivations", e.target.value)}
            placeholder="Enter motivations separated by commas (e.g., convenience, status, value for money)"
            className="form-field h-24 font-montserrat"
          />
          <p className="text-xs text-gray-500 mt-1 font-montserrat">
            What drives this persona to make purchasing decisions?
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
            Preferred Brands
          </label>
          <textarea
            value={textValues.preferred_brands}
            onChange={(e) => handleTextChange("preferred_brands", e.target.value)}
            onBlur={(e) => handleTextBlur("preferred_brands", e.target.value)}
            placeholder="Enter brands separated by commas (e.g., Apple, Nike, Amazon, Starbucks)"
            className="form-field h-24 font-montserrat"
          />
          <p className="text-xs text-gray-500 mt-1 font-montserrat">
            Which brands does this persona typically choose or admire?
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
            Lifestyle Traits
          </label>
          <textarea
            value={textValues.lifestyle}
            onChange={(e) => handleTextChange("lifestyle", e.target.value)}
            onBlur={(e) => handleTextBlur("lifestyle", e.target.value)}
            placeholder="Enter lifestyle traits separated by commas (e.g., health-conscious, busy professional, eco-friendly)"
            className="form-field h-24 font-montserrat"
          />
          <p className="text-xs text-gray-500 mt-1">
            How would you describe this persona's overall lifestyle?
          </p>
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

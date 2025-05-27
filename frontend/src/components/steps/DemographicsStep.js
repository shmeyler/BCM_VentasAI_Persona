import React, { useState } from "react";

const DemographicsStep = ({ persona, updatePersona, onNext, onPrev, saving, isFirstStep }) => {
  const [demographics, setDemographics] = useState(persona?.demographics || {
    age_range: "",
    gender: "",
    income_range: "",
    education: "",
    location: "",
    occupation: "",
    family_status: ""
  });

  const handleInputChange = (field, value) => {
    setDemographics(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleNext = async () => {
    if (await updatePersona({ demographics })) {
      onNext();
    }
  };

  const ageRanges = [
    { value: "18-24", label: "18-24 (Gen Z)" },
    { value: "25-40", label: "25-40 (Millennial)" },
    { value: "41-56", label: "41-56 (Gen X)" },
    { value: "57-75", label: "57-75 (Boomer)" },
    { value: "76+", label: "76+ (Silent)" }
  ];

  const genderOptions = ["Male", "Female", "Non-binary", "Prefer not to say"];
  
  const incomeRanges = [
    "Under $25,000",
    "$25,000 - $49,999",
    "$50,000 - $74,999",
    "$75,000 - $99,999",
    "$100,000 - $149,999",
    "$150,000+"
  ];

  const educationLevels = [
    "High School",
    "Some College",
    "Bachelor's Degree",
    "Master's Degree",
    "Doctorate",
    "Trade/Vocational"
  ];

  const familyStatuses = [
    "Single",
    "Married",
    "Married with children",
    "Single parent",
    "Empty nester",
    "Retired"
  ];

  const locationTypes = [
    "Urban",
    "Suburban", 
    "Rural",
    "Coastal"
  ];

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold mb-4">Demographics</h2>
      <p className="text-gray-600 mb-6">
        Define the demographic characteristics of your target persona.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Age Range
          </label>
          <select
            value={demographics.age_range}
            onChange={(e) => handleInputChange("age_range", e.target.value)}
            className="form-field"
          >
            <option value="">Select age range</option>
            {ageRanges.map(range => (
              <option key={range.value} value={range.value}>
                {range.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Gender
          </label>
          <select
            value={demographics.gender}
            onChange={(e) => handleInputChange("gender", e.target.value)}
            className="form-field"
          >
            <option value="">Select gender</option>
            {genderOptions.map(gender => (
              <option key={gender} value={gender}>
                {gender}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Income Range
          </label>
          <select
            value={demographics.income_range}
            onChange={(e) => handleInputChange("income_range", e.target.value)}
            className="form-field"
          >
            <option value="">Select income range</option>
            {incomeRanges.map(range => (
              <option key={range} value={range}>
                {range}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Education Level
          </label>
          <select
            value={demographics.education}
            onChange={(e) => handleInputChange("education", e.target.value)}
            className="form-field"
          >
            <option value="">Select education level</option>
            {educationLevels.map(level => (
              <option key={level} value={level}>
                {level}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Location
          </label>
          <input
            type="text"
            value={demographics.location}
            onChange={(e) => handleInputChange("location", e.target.value)}
            placeholder="e.g., New York City, Rural Texas, Suburban Chicago"
            className="form-field"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Occupation
          </label>
          <input
            type="text"
            value={demographics.occupation}
            onChange={(e) => handleInputChange("occupation", e.target.value)}
            placeholder="e.g., Software Engineer, Teacher, Marketing Manager"
            className="form-field"
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Family Status
          </label>
          <select
            value={demographics.family_status}
            onChange={(e) => handleInputChange("family_status", e.target.value)}
            className="form-field"
          >
            <option value="">Select family status</option>
            {familyStatuses.map(status => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
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

export default DemographicsStep;

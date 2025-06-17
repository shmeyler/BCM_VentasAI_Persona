import React, { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";
import StepIndicator from "./StepIndicator";
import DemographicsStep from "./steps/DemographicsStep";
import AttributesStep from "./steps/AttributesStep";
import MediaConsumptionStep from "./steps/MediaConsumptionStep";
import GeneratedPersonaStep from "./steps/GeneratedPersonaStep";
import ReviewResonateStep from "./steps/ReviewResonateStep";
import ResonateUpload from "./ResonateUpload";
import SparkToroUpload from "./steps/SparkToroUpload";
import SEMRushUpload from "./steps/SEMRushUpload";
import BuzzAboutUpload from "./steps/BuzzAboutUpload";
import DataIntegrationStep from "./steps/DataIntegrationStep";
import AIPersonaGenerationStep from "./steps/AIPersonaGenerationStep";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PersonaWizard = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const personaId = searchParams.get('id');
  const startingMethod = searchParams.get('method');

  const [persona, setPersona] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState({});
  
  // Multi-source data collection state
  const [dataSources, setDataSources] = useState({
    resonate: { uploaded: false, data: null, required: true },
    sparktoro: { uploaded: false, data: null, required: false },
    semrush: { uploaded: false, data: null, required: false },
    buzzabout: { uploaded: false, data: null, required: false }
  });
  
  // Track which data sources have been processed
  const [dataIntegration, setDataIntegration] = useState({
    processed: false,
    combinedInsights: null,
    aiPrompt: null
  });

  // Define the new multi-source data collection flow
  const getSteps = () => {
    if (startingMethod === "multi_source_data") {
      return [
        { id: 1, name: "Basic Info", component: "basic" },
        { id: 2, name: "Resonate Data", component: "resonate_upload", required: true },
        { id: 3, name: "SparkToro Data", component: "sparktoro_upload", required: false },
        { id: 4, name: "SEMRush Data", component: "semrush_upload", required: false },
        { id: 5, name: "Buzzabout.ai Data", component: "buzzabout_upload", required: false },
        { id: 6, name: "Data Integration", component: "data_integration" },
        { id: 7, name: "AI Persona Generation", component: "ai_generation" }
      ];
    } else if (startingMethod === "demographics") {
      return [
        { id: 1, name: "Basic Info", component: "basic" },
        { id: 2, name: "Demographics", component: "demographics" },
        { id: 3, name: "Key Attributes", component: "key_attributes" },
        { id: 4, name: "AI Mapping", component: "ai_mapping" },
        { id: 5, name: "Media Consumption", component: "media_consumption" },
        { id: 6, name: "Review & Refine", component: "review_refine" },
        { id: 7, name: "Generate Persona", component: "generate" }
      ];
    } else if (startingMethod === "resonate_upload") {
      return [
        { id: 1, name: "Basic Info", component: "basic" },
        { id: 2, name: "Upload Data", component: "resonate_upload" },
        { id: 3, name: "Review Data", component: "review_resonate" },
        { id: 4, name: "Media Consumption", component: "media_consumption" },
        { id: 5, name: "Review & Refine", component: "review_refine" },
        { id: 6, name: "Generate Persona", component: "generate" }
      ];
    } else {
      return [
        { id: 1, name: "Basic Info", component: "basic" },
        { id: 2, name: "Attributes", component: "attributes" },
        { id: 3, name: "Key Demographics", component: "key_demographics" },
        { id: 4, name: "AI Mapping", component: "ai_mapping" },
        { id: 5, name: "Media Consumption", component: "media_consumption" },
        { id: 6, name: "Review & Refine", component: "review_refine" },
        { id: 7, name: "Generate Persona", component: "generate" }
      ];
    }
  };

  const steps = getSteps();

  useEffect(() => {
    if (personaId) {
      loadPersona();
    } else {
      console.error('No persona ID provided in URL');
      alert('Error: No persona ID provided. Redirecting to homepage.');
      navigate('/');
    }
  }, [personaId, navigate]);

  const loadPersona = async () => {
    try {
      const response = await axios.get(`${API}/personas/${personaId}`);
      setPersona(response.data);
      setCurrentStep(response.data.current_step || 1);
    } catch (error) {
      console.error("Error loading persona:", error);
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const updatePersona = async (updates, stepNumber = null) => {
    setSaving(true);
    setErrors({});
    
    try {
      const updateData = {
        ...updates,
        current_step: stepNumber || currentStep,
        completed_steps: persona?.completed_steps || []
      };

      // Add current step to completed steps if moving forward
      if (stepNumber && stepNumber > currentStep) {
        updateData.completed_steps = [...new Set([...updateData.completed_steps, currentStep])];
      }

      const response = await axios.put(`${API}/personas/${personaId}`, updateData);
      setPersona(response.data);
      
      if (stepNumber) {
        setCurrentStep(stepNumber);
      }
      
      return true;
    } catch (error) {
      console.error("Error updating persona:", error);
      setErrors({ general: "Failed to save changes. Please try again." });
      return false;
    } finally {
      setSaving(false);
    }
  };

  const goToStep = async (stepNumber) => {
    // Allow going back to any previous step or Media Consumption step (5) for editing
    if (stepNumber <= currentStep || stepNumber === 5) {
      setCurrentStep(stepNumber);
      return;
    }

    // For forward navigation, validate current step
    if (await validateCurrentStep()) {
      setCurrentStep(stepNumber);
    }
  };

  const validateCurrentStep = async () => {
    // Simplified validation for the new streamlined flow
    return true;
  };

  const nextStep = async () => {
    if (currentStep < steps.length) {
      await goToStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderStepContent = () => {
    const step = steps.find(s => s.id === currentStep);
    if (!step) return null;

    const commonProps = {
      persona,
      updatePersona,
      onNext: nextStep,
      onPrev: prevStep,
      saving,
      errors,
      isFirstStep: currentStep === 1,
      isLastStep: currentStep === steps.length,
      startingMethod
    };

    switch (step.component) {
      case "basic":
        return <BasicInfoStep {...commonProps} />;
      case "demographics":
        return <DemographicsStep {...commonProps} />;
      case "attributes":
        return <AttributesStep {...commonProps} />;
      case "key_attributes":
        return <KeyAttributesStep {...commonProps} />;
      case "key_demographics":
        return <KeyDemographicsStep {...commonProps} />;
      case "resonate_upload":
        return <ResonateUpload {...commonProps} dataSources={dataSources} setDataSources={setDataSources} />;
      case "sparktoro_upload":
        return <SparkToroUpload {...commonProps} dataSources={dataSources} setDataSources={setDataSources} />;
      case "semrush_upload":
        return <SEMRushUpload {...commonProps} dataSources={dataSources} setDataSources={setDataSources} />;
      case "buzzabout_upload":
        return <BuzzAboutUpload {...commonProps} dataSources={dataSources} setDataSources={setDataSources} />;
      case "data_integration":
        return <DataIntegrationStep {...commonProps} dataSources={dataSources} dataIntegration={dataIntegration} setDataIntegration={setDataIntegration} />;
      case "ai_generation":
        return <AIPersonaGenerationStep {...commonProps} dataSources={dataSources} dataIntegration={dataIntegration} />;
      case "review_resonate":
        return <ReviewResonateStep {...commonProps} />;
      case "ai_mapping":
        return <AIMappingStep {...commonProps} />;
      case "media_consumption":
        return <MediaConsumptionStep {...commonProps} goToStep={goToStep} />;
      case "review_refine":
        return <ReviewRefineStep {...commonProps} goToStep={goToStep} />;
      case "generate":
        return <GeneratedPersonaStep {...commonProps} personaId={personaId} />;
      default:
        return <div>Step not found</div>;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="loading-spinner"></div>
        <span className="ml-2 font-montserrat">Loading persona...</span>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-montserrat bcm-heading mb-2">
          Create Persona: {persona?.name}
        </h1>
        <p className="text-gray-600 font-montserrat">
          Starting method: {startingMethod === "demographics" ? "Demographics First" : "Attributes First"}
        </p>
      </div>

      <StepIndicator 
        steps={steps} 
        currentStep={currentStep} 
        completedSteps={persona?.completed_steps || []}
        onStepClick={goToStep}
      />

      <div className="mt-8">
        {errors.general && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="error-message font-montserrat">{errors.general}</p>
          </div>
        )}
        
        <div className="fade-in">
          {renderStepContent()}
        </div>
      </div>
    </div>
  );
};

// Basic Info Step Component
const BasicInfoStep = ({ persona, updatePersona, onNext, saving }) => {
  const [name, setName] = useState(persona?.name || "");

  const handleNext = async () => {
    // Update the persona with the name first, then move to next step
    const updated = await updatePersona({ name });
    if (updated) {
      onNext();
    }
  };

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold font-montserrat bcm-heading mb-4">Basic Information</h2>
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
          Persona Name
        </label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter a name for this persona"
          className="form-field font-montserrat"
        />
      </div>
      
      <div className="flex justify-end">
        <button
          onClick={handleNext}
          disabled={saving || !name.trim()}
          className="bcm-btn-primary disabled:opacity-50"
        >
          {saving ? "Saving..." : "Next"}
        </button>
      </div>
    </div>
  );
};

// Streamlined step components for AI-powered persona generation

// Key Attributes Step - for Demographics-first approach
const KeyAttributesStep = ({ persona, updatePersona, onNext, onPrev, saving }) => {
  const [keyAttribute, setKeyAttribute] = useState('');
  const [attributeType, setAttributeType] = useState('interests');

  const handleNext = async () => {
    const updates = {
      attributes: {
        ...persona?.attributes,
        [attributeType]: keyAttribute ? [keyAttribute] : []
      }
    };
    
    if (await updatePersona(updates, 4)) {
      onNext();
    }
  };

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold font-montserrat bcm-heading mb-4">Key Attribute</h2>
      <p className="text-gray-600 mb-6 font-montserrat">
        Based on your demographics, provide one key attribute to help our AI map related characteristics.
      </p>

      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
            Attribute Type
          </label>
          <select
            value={attributeType}
            onChange={(e) => setAttributeType(e.target.value)}
            className="form-field font-montserrat"
          >
            <option value="interests">Primary Interest</option>
            <option value="behaviors">Key Behavior</option>
            <option value="values">Core Value</option>
            <option value="purchase_motivations">Purchase Motivation</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
            Key {attributeType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
          </label>
          <input
            type="text"
            value={keyAttribute}
            onChange={(e) => setKeyAttribute(e.target.value)}
            placeholder={`Enter one primary ${attributeType.replace('_', ' ')}`}
            className="form-field font-montserrat"
          />
          <p className="text-xs text-gray-500 mt-1 font-montserrat">
            Our AI will use this to suggest related characteristics and behaviors.
          </p>
        </div>
      </div>

      <div className="flex justify-between">
        <button onClick={onPrev} className="bcm-btn-secondary">
          Back
        </button>
        <button
          onClick={handleNext}
          disabled={saving || !keyAttribute.trim()}
          className="bcm-btn-primary disabled:opacity-50"
        >
          {saving ? "Saving..." : "Next: AI Mapping"}
        </button>
      </div>
    </div>
  );
};

// Key Demographics Step - for Attributes-first approach  
const KeyDemographicsStep = ({ persona, updatePersona, onNext, onPrev, saving }) => {
  const [ageRange, setAgeRange] = useState('');
  const [location, setLocation] = useState('');

  const handleNext = async () => {
    const updates = {
      demographics: {
        ...persona?.demographics,
        age_range: ageRange,
        location: location
      }
    };
    
    if (await updatePersona(updates, 4)) {
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

  const locationTypes = [
    "Urban",
    "Suburban", 
    "Rural",
    "Coastal"
  ];

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold font-montserrat bcm-heading mb-4">Key Demographics</h2>
      <p className="text-gray-600 mb-6 font-montserrat">
        Based on your attributes, provide key demographic info to help our AI map the target audience.
      </p>

      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
            Age Range
          </label>
          <select
            value={ageRange}
            onChange={(e) => setAgeRange(e.target.value)}
            className="form-field font-montserrat"
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
          <label className="block text-sm font-medium text-gray-700 mb-2 font-montserrat">
            Primary Location
          </label>
          <select
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="form-field font-montserrat"
          >
            <option value="">Select location type</option>
            {locationTypes.map(locationType => (
              <option key={locationType} value={locationType}>
                {locationType}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500 mt-1 font-montserrat">
            Our AI will use this to suggest corresponding demographic characteristics.
          </p>
        </div>
      </div>

      <div className="flex justify-between">
        <button onClick={onPrev} className="bcm-btn-secondary">
          Back
        </button>
        <button
          onClick={handleNext}
          disabled={saving || !ageRange || !location.trim()}
          className="bcm-btn-primary disabled:opacity-50"
        >
          {saving ? "Saving..." : "Next: AI Mapping"}
        </button>
      </div>
    </div>
  );
};

// AI Mapping Step - where AI fills in the blanks
const AIMappingStep = ({ persona, updatePersona, onNext, onPrev, saving, startingMethod }) => {
  const [mapping, setMapping] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    generateAIMapping();
  }, []);

  const generateAIMapping = async () => {
    setLoading(true);
    
    // Simulate AI mapping based on input data
    setTimeout(() => {
      let aiMapping;
      
      if (startingMethod === "demographics") {
        // AI suggests attributes based on demographics
        const demographics = persona?.demographics || {};
        aiMapping = {
          type: "attributes",
          suggestions: {
            interests: ["Technology", "Health & Fitness", "Travel"],
            behaviors: ["Research before buying", "Active on social media", "Values convenience"],
            values: ["Innovation", "Quality", "Efficiency"],
            purchase_motivations: ["Value for money", "Brand reputation", "User reviews"],
            preferred_brands: ["Apple", "Nike", "Amazon"],
            lifestyle: ["Health-conscious", "Tech-savvy", "Busy professional"]
          },
          reasoning: `Based on ${demographics.age_range} demographic in ${demographics.location || 'target area'}, here are AI-suggested characteristics:`
        };
      } else {
        // AI suggests demographics based on attributes  
        const attributes = persona?.attributes || {};
        aiMapping = {
          type: "demographics",
          suggestions: {
            gender: "Mixed (slight female skew)",
            income_range: "$50,000 - $99,999",
            education: "Bachelor's Degree",
            occupation: "Professional/Manager",
            family_status: "Married or Single"
          },
          reasoning: `Based on your specified attributes, here are AI-suggested demographic characteristics:`
        };
      }
      
      setMapping(aiMapping);
      setLoading(false);
    }, 2000);
  };

  const handleAcceptMapping = async () => {
    if (!mapping) return;
    
    const updates = mapping.type === "attributes" 
      ? { attributes: { ...persona?.attributes, ...mapping.suggestions } }
      : { demographics: { ...persona?.demographics, ...mapping.suggestions } };
    
    if (await updatePersona(updates, 5)) {
      onNext();
    }
  };

  if (loading) {
    return (
      <div className="form-section">
        <div className="text-center py-12">
          <div className="loading-spinner mx-auto mb-4"></div>
          <h2 className="text-xl font-bold font-montserrat bcm-heading mb-2">AI Mapping in Progress</h2>
          <p className="text-gray-600 font-montserrat">
            Our AI is analyzing your data and mapping corresponding characteristics...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold font-montserrat bcm-heading mb-4">AI-Mapped Characteristics</h2>
      <p className="text-gray-600 mb-6 font-montserrat">
        {mapping?.reasoning}
      </p>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
        <h3 className="font-semibold font-montserrat bcm-heading mb-4">
          AI Suggestions for {mapping?.type === "attributes" ? "Attributes" : "Demographics"}:
        </h3>
        
        <div className="space-y-3">
          {Object.entries(mapping?.suggestions || {}).map(([key, value]) => (
            <div key={key} className="flex items-start">
              <span className="font-medium font-montserrat text-gray-700 w-32">
                {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
              </span>
              <span className="text-gray-600 font-montserrat flex-1">
                {Array.isArray(value) ? value.join(', ') : value}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
        <p className="text-yellow-800 text-sm font-montserrat">
          💡 These AI-generated suggestions will be added to your persona. You can review and refine them in the next step.
        </p>
      </div>

      <div className="flex justify-between">
        <button onClick={onPrev} className="bcm-btn-secondary">
          Back
        </button>
        <button
          onClick={handleAcceptMapping}
          disabled={saving}
          className="bcm-btn-primary disabled:opacity-50"
        >
          {saving ? "Saving..." : "Accept AI Mapping"}
        </button>
      </div>
    </div>
  );
};

// Review & Refine Step - comprehensive review with editing capabilities
const ReviewRefineStep = ({ persona, updatePersona, onNext, onPrev, saving, goToStep }) => {
  const [editingSection, setEditingSection] = useState(null);

  const handleNext = async () => {
    if (await updatePersona({ current_step: 7 })) {
      onNext();
    }
  };

  const renderEditableSection = (title, data, section, stepNumber = null) => {
    const isEditing = editingSection === section;
    
    return (
      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 mb-4">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-semibold font-montserrat bcm-heading">{title}</h3>
          <button
            onClick={() => stepNumber ? goToStep(stepNumber) : setEditingSection(isEditing ? null : section)}
            className="bcm-btn-outline text-sm"
          >
            {stepNumber ? "Edit" : (isEditing ? "Done" : "Edit")}
          </button>
        </div>
        
        {data && Object.keys(data).length > 0 ? (
          <div className="space-y-2 text-sm text-gray-700">
            {Object.entries(data).map(([key, value]) => {
              if (!value || (Array.isArray(value) && value.length === 0)) return null;
              
              const displayValue = Array.isArray(value) ? value.join(', ') : value;
              const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
              
              return (
                <div key={key} className="font-montserrat">
                  <span className="font-medium">{displayKey}:</span> {displayValue}
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-gray-500 text-sm italic font-montserrat">No data provided</p>
        )}
      </div>
    );
  };

  const renderMediaConsumption = () => {
    const media = persona?.media_consumption;
    if (!media) return null;

    return (
      <div className="bg-blue-50 rounded-lg p-4 border border-blue-200 mb-4">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-semibold font-montserrat bcm-heading">Media Consumption</h3>
          <div className="flex space-x-2">
            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded font-montserrat">Editable</span>
            <button
              onClick={() => goToStep(5)}
              className="bcm-btn-outline text-sm"
            >
              Edit
            </button>
          </div>
        </div>
        
        <div className="space-y-2 text-sm text-gray-700">
          {media.social_media_platforms?.length > 0 && (
            <div className="font-montserrat">
              <span className="font-medium">Social Media:</span> {media.social_media_platforms.join(', ')}
            </div>
          )}
          {media.content_types?.length > 0 && (
            <div className="font-montserrat">
              <span className="font-medium">Content Types:</span> {media.content_types.join(', ')}
            </div>
          )}
          {media.consumption_time && (
            <div className="font-montserrat">
              <span className="font-medium">Daily Time:</span> {media.consumption_time}
            </div>
          )}
          {media.preferred_devices?.length > 0 && (
            <div className="font-montserrat">
              <span className="font-medium">Devices:</span> {media.preferred_devices.join(', ')}
            </div>
          )}
          {media.entertainment_preferences?.length > 0 && (
            <div className="font-montserrat">
              <span className="font-medium">Entertainment:</span> {media.entertainment_preferences.join(', ')}
            </div>
          )}
          {media.advertising_receptivity && (
            <div className="font-montserrat">
              <span className="font-medium">Ad Receptivity:</span> {media.advertising_receptivity}
            </div>
          )}
          {media.news_sources?.length > 0 && (
            <div className="font-montserrat">
              <span className="font-medium">News Sources:</span> {media.news_sources.join(', ')}
            </div>
          )}
        </div>
        
        <div className="mt-3 p-2 bg-blue-100 rounded text-xs text-blue-800 font-montserrat">
          💡 You can still edit your media consumption preferences before generating the persona
        </div>
      </div>
    );
  };

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold font-montserrat bcm-heading mb-4">Review & Refine Your Persona</h2>
      <p className="text-gray-600 mb-6 font-montserrat">
        Review the AI-mapped data and your inputs. Make any final adjustments before generating your persona.
      </p>

      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold font-montserrat bcm-heading mb-3">Basic Information</h3>
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <div className="font-montserrat">
              <span className="font-medium">Persona Name:</span> {persona?.name || "Unnamed Persona"}
            </div>
            <div className="font-montserrat mt-1">
              <span className="font-medium">Approach:</span> {persona?.starting_method === "demographics" ? "Demographics First" : "Attributes First"}
            </div>
          </div>
        </div>

        {renderEditableSection("Demographics", persona?.demographics, "demographics")}
        {renderEditableSection("Attributes & Behaviors", persona?.attributes, "attributes")}
        {renderMediaConsumption()}
      </div>

      <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
        <h3 className="font-semibold font-montserrat text-green-900 mb-2">Ready to Generate?</h3>
        <p className="text-green-700 text-sm mb-3 font-montserrat">
          Your persona combines your input with AI-mapped characteristics for comprehensive insights.
        </p>
        <p className="text-green-600 text-xs font-montserrat">
          ✅ Streamlined data collection ✅ AI-powered mapping ✅ Ready for generation
        </p>
      </div>

      <div className="flex justify-between mt-6">
        <button onClick={onPrev} className="bcm-btn-secondary">
          Back
        </button>
        
        <button
          onClick={handleNext}
          disabled={saving}
          className="bcm-btn-primary disabled:opacity-50 px-6"
        >
          {saving ? "Processing..." : "Generate AI Persona"}
        </button>
      </div>
    </div>
  );
};

export default PersonaWizard;

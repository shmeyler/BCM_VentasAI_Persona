import React from "react";

const ReviewStep = ({ persona, updatePersona, onNext, onPrev, saving, goToStep }) => {
  const handleEdit = (stepNumber) => {
    goToStep(stepNumber);
  };

  const handleGenerate = async () => {
    // Mark review as completed and proceed to generation
    if (await updatePersona({ current_step: 8 })) {
      onNext();
    }
  };

  const renderSection = (title, data, stepNumber, emptyMessage = "No data provided") => {
    const hasData = data && Object.values(data).some(value => 
      Array.isArray(value) ? value.length > 0 : value
    );

    return (
      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-semibold text-gray-900">{title}</h3>
          <button
            onClick={() => handleEdit(stepNumber)}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Edit
          </button>
        </div>
        
        {hasData ? (
          <div className="space-y-2 text-sm text-gray-700">
            {Object.entries(data).map(([key, value]) => {
              if (!value || (Array.isArray(value) && value.length === 0)) return null;
              
              const displayValue = Array.isArray(value) ? value.join(', ') : value;
              const displayKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
              
              return (
                <div key={key}>
                  <span className="font-medium">{displayKey}:</span> {displayValue}
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-gray-500 text-sm italic">{emptyMessage}</p>
        )}
      </div>
    );
  };

  const renderMediaConsumption = () => {
    const media = persona?.media_consumption;
    if (!media) return null;

    return (
      <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-semibold text-gray-900">Media Consumption</h3>
          <div className="flex space-x-2">
            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Editable</span>
            <button
              onClick={() => handleEdit(6)}
              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              Edit
            </button>
          </div>
        </div>
        
        <div className="space-y-2 text-sm text-gray-700">
          {media.social_media_platforms?.length > 0 && (
            <div>
              <span className="font-medium">Social Media:</span> {media.social_media_platforms.join(', ')}
            </div>
          )}
          {media.content_types?.length > 0 && (
            <div>
              <span className="font-medium">Content Types:</span> {media.content_types.join(', ')}
            </div>
          )}
          {media.consumption_time && (
            <div>
              <span className="font-medium">Daily Time:</span> {media.consumption_time}
            </div>
          )}
          {media.preferred_devices?.length > 0 && (
            <div>
              <span className="font-medium">Devices:</span> {media.preferred_devices.join(', ')}
            </div>
          )}
          {media.entertainment_preferences?.length > 0 && (
            <div>
              <span className="font-medium">Entertainment:</span> {media.entertainment_preferences.join(', ')}
            </div>
          )}
          {media.advertising_receptivity && (
            <div>
              <span className="font-medium">Ad Receptivity:</span> {media.advertising_receptivity}
            </div>
          )}
          {media.news_sources?.length > 0 && (
            <div>
              <span className="font-medium">News Sources:</span> {media.news_sources.join(', ')}
            </div>
          )}
        </div>
        
        <div className="mt-3 p-2 bg-blue-100 rounded text-xs text-blue-800">
          💡 You can still edit your media consumption preferences before generating the persona
        </div>
      </div>
    );
  };

  return (
    <div className="form-section">
      <h2 className="text-xl font-bold mb-4">Review Your Persona</h2>
      <p className="text-gray-600 mb-6">
        Review all the information you've provided. You can edit any section before generating your AI-powered persona.
      </p>

      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold mb-3">Basic Information</h3>
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <div className="flex justify-between items-center">
              <div>
                <span className="font-medium">Persona Name:</span> {persona?.name || "Unnamed Persona"}
              </div>
              <button
                onClick={() => handleEdit(1)}
                className="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                Edit
              </button>
            </div>
          </div>
        </div>

        {renderSection("Demographics", persona?.demographics, 2)}
        {renderSection("Attributes & Behaviors", persona?.attributes, 3)}
        {renderMediaConsumption()}
      </div>

      <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
        <h3 className="font-semibold text-green-900 mb-2">Ready to Generate?</h3>
        <p className="text-green-700 text-sm mb-3">
          Once you generate the persona, our AI will analyze all the data you've provided and create 
          comprehensive insights, recommendations, and actionable intelligence for your marketing efforts.
        </p>
        <p className="text-green-600 text-xs">
          ✅ All sections can still be edited after generation if needed
        </p>
      </div>

      <div className="flex justify-between mt-6">
        <button onClick={onPrev} className="btn-secondary">
          Back
        </button>
        
        <button
          onClick={handleGenerate}
          disabled={saving}
          className="btn-primary disabled:opacity-50 px-6"
        >
          {saving ? "Processing..." : "Generate AI Persona"}
        </button>
      </div>
    </div>
  );
};

export default ReviewStep;

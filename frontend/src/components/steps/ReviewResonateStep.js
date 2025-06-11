import React from 'react';

const ReviewResonateStep = ({ persona, updatePersona, onNext, onPrev, saving }) => {
  const handleNext = async () => {
    // Move to the next step (media consumption)
    try {
      const success = await updatePersona({ current_step: 4 }, 4);
      if (success) {
        onNext();
      }
    } catch (error) {
      console.error('Error updating persona step:', error);
      alert('Error moving to next step. Please try again.');
    }
  };

  return (
    <div className="form-section">
      <div className="mb-8">
        <h2 className="text-2xl font-bold font-montserrat mb-3 bcm-heading">
          Review Resonate Data
        </h2>
        <p className="text-gray-600 font-montserrat">
          Your Resonate data has been successfully processed and a persona has been created. 
          Review the information below and proceed to customize media consumption preferences.
        </p>
      </div>

      {/* Persona Information Summary */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-green-800 mb-3 font-montserrat">
          ✅ Persona Created Successfully
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-semibold font-montserrat mb-2">Basic Information</h4>
            <ul className="text-sm text-green-700 space-y-1">
              <li><strong>Name:</strong> {persona?.name || 'Resonate Persona'}</li>
              <li><strong>Starting Method:</strong> Resonate Upload</li>
              <li><strong>Current Step:</strong> {persona?.current_step || 3}</li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold font-montserrat mb-2">Demographics</h4>
            <ul className="text-sm text-green-700 space-y-1">
              {persona?.demographics && (
                <>
                  <li><strong>Age Range:</strong> {persona.demographics.age_range || 'Not specified'}</li>
                  <li><strong>Gender:</strong> {persona.demographics.gender || 'Not specified'}</li>
                  <li><strong>Location:</strong> {persona.demographics.location || 'Not specified'}</li>
                  <li><strong>Occupation:</strong> {persona.demographics.occupation || 'Not specified'}</li>
                </>
              )}
            </ul>
          </div>
        </div>
      </div>

      {/* Next Steps Information */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-blue-800 mb-3 font-montserrat">
          📱 Next: Media Consumption
        </h3>
        <p className="text-blue-700 font-montserrat">
          In the next step, you'll be able to refine and customize the media consumption 
          preferences for your persona based on the Resonate data analysis.
        </p>
      </div>

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        <button
          onClick={onPrev}
          className="bcm-btn-outline"
        >
          ← Previous
        </button>
        
        <button
          onClick={handleNext}
          disabled={saving}
          className="bcm-btn-primary"
        >
          {saving ? "Saving..." : "Continue to Media Consumption →"}
        </button>
      </div>
    </div>
  );
};

export default ReviewResonateStep;
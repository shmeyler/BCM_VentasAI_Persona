import React, { useState, useEffect } from "react";
import axios from "axios";
import VisualPersonaTemplate from "../VisualPersonaTemplate";
import DetailedPersonaView from "../DetailedPersonaView";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const GeneratedPersonaStep = ({ persona, onPrev, personaId }) => {
  const [generatedPersona, setGeneratedPersona] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [viewMode, setViewMode] = useState('template'); // 'template' or 'detailed'

  useEffect(() => {
    generatePersona();
  }, []);

  const generatePersona = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API}/personas/${personaId}/generate`);
      setGeneratedPersona(response.data);
    } catch (err) {
      console.error("Error generating persona:", err);
      setError("Failed to generate persona. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const regeneratePersona = async () => {
    await generatePersona();
  };

  const savePersona = async () => {
    setSaving(true);
    try {
      // Persona is already saved in the database when generated
      alert("Persona saved successfully!");
    } catch (err) {
      console.error("Error saving persona:", err);
      alert("Failed to save persona. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="form-section">
        <div className="text-center py-12">
          <div className="loading-spinner mx-auto mb-4"></div>
          <h2 className="text-xl font-bold font-montserrat bcm-heading mb-2">Generating Your AI Persona</h2>
          <p className="text-gray-600 font-montserrat">
            Our AI is analyzing your data and creating comprehensive persona insights with visual representation...
          </p>
          <div className="mt-6 max-w-md mx-auto">
            <div className="bcm-progress-bar">
              <div className="bcm-progress-fill animate-pulse" style={{width: "75%"}}></div>
            </div>
            <p className="text-sm text-gray-500 mt-2 font-montserrat">Generating persona image and insights...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="form-section">
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-red-900 mb-2 font-montserrat">Generation Failed</h2>
          <p className="text-red-600 mb-6 font-montserrat">{error}</p>
          
          <div className="flex justify-center space-x-3">
            <button onClick={onPrev} className="bcm-btn-secondary">
              Go Back
            </button>
            <button onClick={regeneratePersona} className="bcm-btn-primary">
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // If we're in template mode, show the visual template
  if (viewMode === 'template') {
    return (
      <div className="space-y-6">
        {/* View Mode Toggle */}
        <div className="form-section">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h2 className="text-2xl font-bold font-montserrat bcm-heading">
                {generatedPersona?.name} - Visual Persona
              </h2>
              <p className="text-gray-600 font-montserrat">
                Professional persona template with AI-generated insights
              </p>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => setViewMode('detailed')}
                className="bcm-btn-outline text-sm"
              >
                Switch to Detailed View
              </button>
              <button
                onClick={regeneratePersona}
                className="bcm-btn-outline text-sm"
              >
                Regenerate
              </button>
              <button
                onClick={savePersona}
                disabled={saving}
                className="bcm-btn-primary text-sm disabled:opacity-50"
              >
                {saving ? "Saving..." : "Save Persona"}
              </button>
            </div>
          </div>
        </div>

        {/* Visual Template */}
        <VisualPersonaTemplate generatedPersona={generatedPersona} />

        {/* Navigation */}
        <div className="form-section">
          <div className="flex justify-between items-center">
            <button onClick={onPrev} className="bcm-btn-secondary">
              Back to Review
            </button>
            
            <div className="flex space-x-3">
              <button
                onClick={() => window.location.href = "/saved-personas"}
                className="bcm-btn-outline"
              >
                View All Personas
              </button>
              <button
                onClick={() => window.location.href = "/"}
                className="bcm-btn-primary"
              >
                Create New Persona
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Detailed view (using the new comprehensive analytical view)
  return (
    <div className="space-y-6">
      {/* View Mode Toggle */}
      <div className="form-section">
        <div className="flex justify-between items-center mb-4">
          <div>
            <button
              onClick={() => setViewMode('template')}
              className="bcm-btn-primary text-sm"
            >
              ← Switch to Visual Template
            </button>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={regeneratePersona}
              className="bcm-btn-outline text-sm"
            >
              Regenerate
            </button>
            <button
              onClick={savePersona}
              disabled={saving}
              className="bcm-btn-primary text-sm disabled:opacity-50"
            >
              {saving ? "Saving..." : "Save Persona"}
            </button>
          </div>
        </div>
      </div>

      {/* New Comprehensive Detailed View */}
      <DetailedPersonaView generatedPersona={generatedPersona} />

      {/* Navigation */}
      <div className="form-section">
        <div className="flex justify-between items-center">
          <button onClick={onPrev} className="bcm-btn-secondary">
            Back to Review
          </button>
          
          <div className="flex space-x-3">
            <button
              onClick={() => window.location.href = "/saved-personas"}
              className="bcm-btn-outline"
            >
              View All Personas
            </button>
            <button
              onClick={() => window.location.href = "/"}
              className="bcm-btn-primary"
            >
              Create New Persona
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeneratedPersonaStep;

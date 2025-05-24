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

  // Detailed view (original view)
  return (
    <div className="space-y-6">
      {/* View Mode Toggle */}
      <div className="form-section">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-2xl font-bold font-montserrat bcm-heading mb-2">
              {generatedPersona?.name}
            </h1>
            <p className="text-gray-600 font-montserrat">
              AI-Generated Consumer Persona • Created {new Date(generatedPersona?.generated_at).toLocaleDateString()}
            </p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => setViewMode('template')}
              className="bcm-btn-primary text-sm"
            >
              Switch to Visual Template
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

      {/* AI Insights */}
      <div className="bcm-insights-card">
        <h2 className="text-xl font-bold font-montserrat mb-4 flex items-center bcm-heading">
          <svg className="w-6 h-6 mr-2 bcm-icon-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          AI-Generated Insights
        </h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold font-montserrat bcm-heading mb-2">Personality Traits</h3>
            <div className="flex flex-wrap gap-2">
              {generatedPersona?.ai_insights?.personality_traits?.map((trait, index) => (
                <span key={index} className="text-white px-3 py-1 rounded-full text-sm font-montserrat" style={{backgroundColor: 'var(--bcm-cyan)'}}>
                  {trait}
                </span>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="font-semibold font-montserrat bcm-heading mb-2">Digital Behavior</h3>
            <p className="text-gray-700 text-sm font-montserrat">
              {generatedPersona?.ai_insights?.digital_behavior}
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold font-montserrat bcm-heading mb-2">Shopping Behavior</h3>
            <p className="text-gray-700 text-sm font-montserrat">
              {generatedPersona?.ai_insights?.shopping_behavior}
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold font-montserrat bcm-heading mb-2">Key Decision Factors</h3>
            <ul className="text-gray-700 text-sm space-y-1">
              {generatedPersona?.ai_insights?.decision_factors?.map((factor, index) => (
                <li key={index} className="flex items-center font-montserrat">
                  <span className="w-2 h-2 rounded-full mr-2" style={{backgroundColor: 'var(--bcm-teal)'}}></span>
                  {factor}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Marketing Recommendations */}
      <div className="bcm-recommendations-card">
        <h2 className="text-xl font-bold font-montserrat mb-4 flex items-center bcm-heading">
          <svg className="w-6 h-6 mr-2 bcm-icon-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
          </svg>
          Marketing Recommendations
        </h2>
        
        <div className="space-y-3">
          {generatedPersona?.recommendations?.map((recommendation, index) => (
            <div key={index} className="flex items-start p-3 rounded-lg" style={{backgroundColor: 'var(--bcm-teal-light)', borderColor: 'var(--bcm-teal)'}} className="border">
              <svg className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0 bcm-icon-teal" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <p className="text-sm font-montserrat" style={{color: 'var(--bcm-teal)'}}>{recommendation}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Pain Points & Goals */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="form-section border-l-4 border-red-500">
          <h2 className="text-xl font-bold font-montserrat mb-4 flex items-center text-red-700">
            <svg className="w-6 h-6 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            Pain Points
          </h2>
          
          <div className="space-y-2">
            {generatedPersona?.pain_points?.map((painPoint, index) => (
              <div key={index} className="flex items-start p-3 bg-red-50 border border-red-200 rounded-lg">
                <svg className="w-5 h-5 text-red-600 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <p className="text-red-800 text-sm font-montserrat">{painPoint}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bcm-goals-card">
          <h2 className="text-xl font-bold font-montserrat mb-4 flex items-center bcm-heading-cyan">
            <svg className="w-6 h-6 mr-2 bcm-icon-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Goals & Motivations
          </h2>
          
          <div className="space-y-2">
            {generatedPersona?.goals?.map((goal, index) => (
              <div key={index} className="flex items-start p-3 rounded-lg" style={{backgroundColor: 'var(--bcm-cyan-light)', borderColor: 'var(--bcm-cyan)'}} className="border">
                <svg className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0 bcm-icon-cyan" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <p className="text-sm font-montserrat" style={{color: 'var(--bcm-cyan)'}}>{goal}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Communication Style */}
      <div className="form-section border-l-4" style={{borderLeftColor: 'var(--bcm-orange)'}}>
        <h2 className="text-xl font-bold font-montserrat mb-4 flex items-center bcm-title">
          <svg className="w-6 h-6 mr-2 bcm-icon-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          Recommended Communication Style
        </h2>
        
        <div className="p-4 rounded-lg" style={{backgroundColor: 'rgba(255, 152, 0, 0.1)', borderColor: 'var(--bcm-orange)'}} className="border">
          <p className="font-montserrat" style={{color: 'var(--bcm-orange)'}}>
            {generatedPersona?.communication_style}
          </p>
        </div>
      </div>

      {/* Actions */}
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

import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SavedPersonas = () => {
  const [personas, setPersonas] = useState([]);
  const [generatedPersonas, setGeneratedPersonas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("generated");

  useEffect(() => {
    loadPersonas();
  }, []);

  const loadPersonas = async () => {
    try {
      const [personasResponse, generatedResponse] = await Promise.all([
        axios.get(`${API}/personas`),
        axios.get(`${API}/generated-personas`)
      ]);
      
      setPersonas(personasResponse.data);
      setGeneratedPersonas(generatedResponse.data);
    } catch (error) {
      console.error("Error loading personas:", error);
    } finally {
      setLoading(false);
    }
  };

  const deletePersona = async (personaId, isGenerated = false) => {
    if (!window.confirm("Are you sure you want to delete this persona?")) {
      return;
    }

    try {
      if (isGenerated) {
        // Delete generated persona using the generated-personas endpoint
        await axios.delete(`${API}/generated-personas/${personaId}`);
        setGeneratedPersonas(prev => prev.filter(p => p.id !== personaId));
      } else {
        // Delete draft persona using the personas endpoint
        await axios.delete(`${API}/personas/${personaId}`);
        setPersonas(prev => prev.filter(p => p.id !== personaId));
      }
    } catch (error) {
      console.error("Error deleting persona:", error);
      alert("Failed to delete persona. Please try again.");
    }
  };

  const continuePersona = (personaId) => {
    window.location.href = `/persona-wizard?id=${personaId}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="loading-spinner"></div>
        <span className="ml-2 font-montserrat">Loading personas...</span>
      </div>
    );
  }

  return (
    <div className="px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold font-montserrat bcm-heading">Saved Personas</h1>
          <p className="text-gray-600 mt-2 font-montserrat">Manage your created personas and generated insights</p>
        </div>
        <a href="/" className="bcm-btn-primary">
          Create New Persona
        </a>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab("generated")}
            className={`py-2 px-1 border-b-2 font-medium text-sm font-montserrat ${
              activeTab === "generated"
                ? "bcm-heading border-current"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            Generated Personas ({generatedPersonas.length})
          </button>
          <button
            onClick={() => setActiveTab("drafts")}
            className={`py-2 px-1 border-b-2 font-medium text-sm font-montserrat ${
              activeTab === "drafts"
                ? "bcm-heading border-current"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            Draft Personas ({personas.length})
          </button>
        </nav>
      </div>

      {/* Generated Personas Tab */}
      {activeTab === "generated" && (
        <div>
          {generatedPersonas.length === 0 ? (
            <div className="text-center py-12">
              <svg className="w-16 h-16 mx-auto mb-4 bcm-icon-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <h3 className="text-lg font-medium font-montserrat bcm-heading mb-2">No Generated Personas</h3>
              <p className="text-gray-600 mb-6 font-montserrat">You haven't generated any personas yet.</p>
              <a href="/" className="bcm-btn-primary">
                Create Your First Persona
              </a>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {generatedPersonas.map((generatedPersona) => (
                <div key={generatedPersona.id} className="persona-card">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-semibold font-montserrat bcm-heading mb-1">
                        {generatedPersona.name}
                      </h3>
                      <p className="text-sm text-gray-500 font-montserrat">
                        Generated {new Date(generatedPersona.generated_at).toLocaleDateString()}
                      </p>
                    </div>
                    <span className="bcm-badge-completed">
                      Complete
                    </span>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="text-sm font-montserrat">
                      <span className="font-medium text-gray-700">Method:</span>{" "}
                      <span className="text-gray-600">
                        {generatedPersona.persona_data.starting_method === "demographics" ? "Demographics First" : "Attributes First"}
                      </span>
                    </div>
                    
                    {generatedPersona.ai_insights?.personality_traits && (
                      <div className="text-sm font-montserrat">
                        <span className="font-medium text-gray-700">Traits:</span>{" "}
                        <span className="text-gray-600">
                          {generatedPersona.ai_insights.personality_traits.slice(0, 2).join(", ")}
                          {generatedPersona.ai_insights.personality_traits.length > 2 && "..."}
                        </span>
                      </div>
                    )}
                  </div>

                    <div className="flex items-center justify-between mt-4">
                      <div className="flex space-x-2">
                        <a
                          href={`/persona/${generatedPersona.persona_data.id}/visual`}
                          className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded-lg text-xs font-medium font-montserrat transition-colors flex items-center"
                        >
                          <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          Visual
                        </a>
                        <a
                          href={`/persona/${generatedPersona.persona_data.id}/detailed`}
                          className="bg-purple-500 hover:bg-purple-600 text-white px-3 py-2 rounded-lg text-xs font-medium font-montserrat transition-colors flex items-center"
                        >
                          <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                          </svg>
                          Analysis
                        </a>
                        <a
                          href={`/persona/${generatedPersona.persona_data.id}/detailed`}
                          className="bg-orange-500 hover:bg-orange-600 text-white px-3 py-2 rounded-lg text-xs font-medium font-montserrat transition-colors flex items-center"
                          onClick={(e) => {
                            e.preventDefault();
                            // Simple PDF export using the detailed view
                            window.open(`/persona/${generatedPersona.persona_data.id}/detailed`, '_blank');
                            setTimeout(() => {
                              // This will be enhanced when the user navigates to the detailed view with export functionality
                              alert('Navigate to the opened detailed view and click the Export button for PDF options.');
                            }, 1000);
                          }}
                        >
                          <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                          </svg>
                          Export
                        </a>
                      </div>
                      <button
                        onClick={() => deletePersona(generatedPersona.id, true)}
                        className="text-red-600 hover:text-red-800 text-xs font-medium font-montserrat"
                      >
                        Delete
                      </button>
                    </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Draft Personas Tab */}
      {activeTab === "drafts" && (
        <div>
          {personas.length === 0 ? (
            <div className="text-center py-12">
              <svg className="w-16 h-16 mx-auto mb-4 bcm-icon-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 className="text-lg font-medium font-montserrat bcm-heading mb-2">No Draft Personas</h3>
              <p className="text-gray-600 mb-6 font-montserrat">You don't have any personas in progress.</p>
              <a href="/" className="bcm-btn-primary">
                Start Creating a Persona
              </a>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {personas.map((persona) => (
                <div key={persona.id} className="persona-card">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-semibold font-montserrat bcm-heading mb-1">
                        {persona.name || "Unnamed Persona"}
                      </h3>
                      <p className="text-sm text-gray-500 font-montserrat">
                        Updated {new Date(persona.updated_at).toLocaleDateString()}
                      </p>
                    </div>
                    <span className="bcm-badge-draft">
                      Step {persona.current_step}/8
                    </span>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="text-sm font-montserrat">
                      <span className="font-medium text-gray-700">Method:</span>{" "}
                      <span className="text-gray-600">
                        {persona.starting_method === "demographics" ? "Demographics First" : "Attributes First"}
                      </span>
                    </div>
                    
                    <div className="text-sm font-montserrat">
                      <span className="font-medium text-gray-700">Progress:</span>{" "}
                      <span className="text-gray-600">
                        {persona.completed_steps?.length || 0} of 7 steps completed
                      </span>
                    </div>

                    {/* Progress bar */}
                    <div className="bcm-progress-bar">
                      <div 
                        className="bcm-progress-fill" 
                        style={{ width: `${((persona.completed_steps?.length || 0) / 7) * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center">
                    <button
                      onClick={() => continuePersona(persona.id)}
                      className="bcm-nav-link text-sm font-medium"
                    >
                      Continue
                    </button>
                    <button
                      onClick={() => deletePersona(persona.id)}
                      className="text-red-600 hover:text-red-800 text-sm font-medium font-montserrat"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SavedPersonas;

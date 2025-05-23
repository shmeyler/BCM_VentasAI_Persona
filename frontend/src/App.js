import React, { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, useParams } from "react-router-dom";
import HomePage from "./components/HomePage";
import PersonaWizard from "./components/PersonaWizard";
import SavedPersonas from "./components/SavedPersonas";
import DataSources from "./components/DataSources";
import VisualPersonaTemplate from "./components/VisualPersonaTemplate";
import DetailedPersonaView from "./components/DetailedPersonaView";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Wrapper component for Visual Persona Template
const PersonaTemplateWrapper = () => {
  const { id } = useParams();
  const [generatedPersona, setGeneratedPersona] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  React.useEffect(() => {
    const fetchGeneratedPersona = async () => {
      try {
        const response = await axios.get(`${API}/generated-personas`);
        const persona = response.data.find(p => p.persona_data.id === id);
        
        if (persona) {
          setGeneratedPersona(persona);
        } else {
          setError("Generated persona not found");
        }
      } catch (err) {
        setError("Failed to fetch persona data");
      } finally {
        setLoading(false);
      }
    };

    fetchGeneratedPersona();
  }, [id]);

  if (loading) return <div className="flex justify-center items-center h-64"><div className="text-lg">Loading persona...</div></div>;
  if (error) return <div className="flex justify-center items-center h-64"><div className="text-lg text-red-600">{error}</div></div>;
  if (!generatedPersona) return <div className="flex justify-center items-center h-64"><div className="text-lg">Persona not found</div></div>;

  return <VisualPersonaTemplate generatedPersona={generatedPersona} />;
};

// Wrapper component for Detailed Persona View
const DetailedPersonaWrapper = () => {
  const { id } = useParams();
  const [generatedPersona, setGeneratedPersona] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  React.useEffect(() => {
    const fetchGeneratedPersona = async () => {
      try {
        const response = await axios.get(`${API}/generated-personas`);
        const persona = response.data.find(p => p.persona_data.id === id);
        
        if (persona) {
          setGeneratedPersona(persona);
        } else {
          setError("Generated persona not found");
        }
      } catch (err) {
        setError("Failed to fetch persona data");
      } finally {
        setLoading(false);
      }
    };

    fetchGeneratedPersona();
  }, [id]);

  if (loading) return <div className="flex justify-center items-center h-64"><div className="text-lg">Loading detailed analysis...</div></div>;
  if (error) return <div className="flex justify-center items-center h-64"><div className="text-lg text-red-600">{error}</div></div>;
  if (!generatedPersona) return <div className="flex justify-center items-center h-64"><div className="text-lg">Persona not found</div></div>;

  return <DetailedPersonaView generatedPersona={generatedPersona} />;
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center">
                  <div className="flex-shrink-0 flex items-center">
                    {/* BCM Logo placeholder - replace with actual logo */}
                    <div className="w-10 h-10 rounded-full flex items-center justify-center mr-3" style={{backgroundColor: 'var(--bcm-teal)'}}>
                      <span className="text-white font-bold text-lg font-montserrat">B</span>
                    </div>
                    <div>
                      <h1 className="text-xl bcm-title">BCM VentasAI</h1>
                      <p className="text-sm text-gray-500 font-montserrat">Persona Generator</p>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <a href="/" className="bcm-nav-link">
                    Create Persona
                  </a>
                  <a href="/saved-personas" className="bcm-nav-link">
                    Saved Personas
                  </a>
                  <a href="/data-sources" className="bcm-nav-link">
                    Data Sources
                  </a>
                </div>
              </div>
            </div>
          </nav>

          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/persona-wizard" element={<PersonaWizard />} />
              <Route path="/saved-personas" element={<SavedPersonas />} />
              <Route path="/data-sources" element={<DataSources />} />
              <Route path="/persona/:id/visual" element={<PersonaTemplateWrapper />} />
              <Route path="/persona/:id/detailed" element={<DetailedPersonaWrapper />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;

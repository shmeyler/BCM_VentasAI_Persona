import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const DataSources = () => {
  const [dataSourceStatus, setDataSourceStatus] = useState(null);
  const [demoData, setDemoData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data source status on component mount
  useEffect(() => {
    fetchDataSourceStatus();
  }, []);

  const fetchDataSourceStatus = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/data-sources/status`);
      setDataSourceStatus(response.data);
      setError(null);
    } catch (err) {
      console.error("Error fetching data source status:", err);
      setError("Failed to fetch data source status");
    } finally {
      setLoading(false);
    }
  };

  const fetchDemoData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/data-sources/demo`);
      setDemoData(response.data);
      setError(null);
    } catch (err) {
      console.error("Error fetching demo data:", err);
      setError("Failed to fetch demo data");
    } finally {
      setLoading(false);
    }
  };

  const dataSources = [
    {
      name: "Resonate rAI",
      description: "AI-powered consumer insights and audience intelligence platform providing deep behavioral data and psychographic analysis.",
      features: ["Consumer behavior analysis", "Psychographic profiling", "Audience segmentation", "AI-driven insights"],
      logo: "🎯",
      status: "Active"
    },
    {
      name: "SparkToro",
      description: "Audience research tool that reveals where your audience spends time online, what they read, watch, and who influences them.",
      features: ["Audience discovery", "Influencer identification", "Content preferences", "Social media habits"],
      logo: "⚡",
      status: dataSourceStatus?.sparktoro?.status === "active" ? "Active" : "Connecting...",
      integration_status: dataSourceStatus?.sparktoro
    },
    {
      name: "SEMRush",
      description: "Digital marketing toolkit providing insights into search behavior, keyword trends, and competitive analysis.",
      features: ["Search behavior data", "Keyword analysis", "Competitive insights", "Market research"],
      logo: "📊",
      status: dataSourceStatus?.semrush?.status === "active" ? "Active" : "Connecting...",
      integration_status: dataSourceStatus?.semrush
    },
    {
      name: "Buzzabout.ai",
      description: "Social listening and sentiment analysis platform for understanding conversations and trends around your market.",
      features: ["Social listening", "Sentiment analysis", "Trend monitoring", "Conversation insights"],
      logo: "🗣️",
      status: dataSourceStatus?.buzzabout?.status === "active" ? "Active" : "Coming Soon",
      integration_status: dataSourceStatus?.buzzabout
    }
  ];

  return (
    <div className="px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-montserrat bcm-heading mb-4">
          Data Sources
        </h1>
        <p className="text-gray-600 max-w-3xl font-montserrat">
          Our persona generation is powered by leading data sources and AI platforms. These integrations provide comprehensive, real-time insights to create accurate, data-driven consumer personas for your marketing strategy.
        </p>
        
        {/* Integration Status Banner */}
        {dataSourceStatus && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3 animate-pulse"></div>
              <div>
                <p className="text-green-800 font-semibold font-montserrat">
                  Integration Status: {dataSourceStatus.integration_health}
                </p>
                <p className="text-green-600 text-sm font-montserrat">
                  Last updated: {new Date(dataSourceStatus.last_updated).toLocaleString()}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="grid gap-8 md:grid-cols-2">
        {dataSources.map((source, index) => (
          <div key={index} className="persona-card">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <div className="text-3xl mr-4">{source.logo}</div>
                <div>
                  <h3 className="text-xl font-bold font-montserrat bcm-heading mb-1">
                    {source.name}
                  </h3>
                  <span 
                    className={`text-xs px-2 py-1 rounded-full font-montserrat ${
                      source.status === "Active" 
                        ? "bcm-badge-active" 
                        : source.status === "Coming Soon"
                        ? "bcm-badge-draft"
                        : "bg-yellow-100 text-yellow-800"
                    }`}
                  >
                    {source.status}
                  </span>
                  {source.integration_status && (
                    <div className="mt-1 text-xs text-gray-500 font-montserrat">
                      Type: {source.integration_status.type}
                    </div>
                  )}
                </div>
              </div>
            </div>

            <p className="text-gray-600 mb-4 font-montserrat">
              {source.description}
            </p>

            <div>
              <h4 className="font-semibold font-montserrat bcm-heading mb-2">
                Key Features:
              </h4>
              <ul className="space-y-1">
                {source.features.map((feature, featureIndex) => (
                  <li
                    key={featureIndex}
                    className="flex items-center text-sm text-gray-700 font-montserrat"
                  >
                    <svg
                      className="w-4 h-4 mr-2 flex-shrink-0 bcm-icon-teal"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
              
              {/* Show capabilities if integration is active */}
              {source.integration_status && source.integration_status.capabilities && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <h5 className="text-xs font-semibold text-gray-600 mb-2 font-montserrat">
                    ACTIVE CAPABILITIES:
                  </h5>
                  <div className="flex flex-wrap gap-1">
                    {source.integration_status.capabilities.map((capability, capIndex) => (
                      <span 
                        key={capIndex}
                        className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded font-montserrat"
                      >
                        {capability.replace(/_/g, ' ')}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Demo Data Section */}
      <div className="mt-12 form-section">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold font-montserrat bcm-heading">
            Test Data Integration
          </h2>
          <button
            onClick={fetchDemoData}
            disabled={loading}
            className="bcm-btn-primary disabled:opacity-50"
          >
            {loading ? "Loading..." : "Fetch Demo Data"}
          </button>
        </div>
        
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg mb-4">
            <p className="text-red-800 font-montserrat">{error}</p>
          </div>
        )}

        {demoData && (
          <div className="grid md:grid-cols-3 gap-6">
            {/* SEMRush Demo Data */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold font-montserrat bcm-heading mb-3">
                📊 SEMRush Insights
              </h3>
              {demoData.search_insights && (
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium">Top Keywords:</span>
                    <ul className="mt-1 space-y-1">
                      {demoData.search_insights.search_behavior?.primary_keywords?.slice(0, 3).map((kw, i) => (
                        <li key={i} className="text-gray-600 font-montserrat">
                          • {kw.keyword} ({kw.search_volume.toLocaleString()} searches)
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <span className="font-medium">Mobile Usage:</span>
                    <span className="ml-2 text-gray-600 font-montserrat">
                      {Math.round(demoData.search_insights.search_behavior?.device_preferences?.mobile * 100)}%
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* SparkToro Demo Data */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold font-montserrat bcm-heading mb-3">
                ⚡ SparkToro Insights
              </h3>
              {demoData.audience_insights && (
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium">Top Influencers:</span>
                    <ul className="mt-1 space-y-1">
                      {demoData.audience_insights.audience_insights?.top_influencers?.map((inf, i) => (
                        <li key={i} className="text-gray-600 font-montserrat">
                          • {inf}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <span className="font-medium">Social Discovery:</span>
                    <span className="ml-2 text-gray-600 font-montserrat">
                      {Math.round(demoData.audience_insights.audience_insights?.discovery_channels?.social_media * 100)}%
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Buzzabout Demo Data */}
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold font-montserrat bcm-heading mb-3">
                🗣️ Buzzabout Insights
              </h3>
              {demoData.social_insights && (
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="font-medium">Overall Sentiment:</span>
                    <span className="ml-2 text-gray-600 font-montserrat">
                      {Math.round(demoData.social_insights.social_listening?.mention_sentiment?.overall_score * 100)}% positive
                    </span>
                  </div>
                  <div>
                    <span className="font-medium">Top Topics:</span>
                    <ul className="mt-1 space-y-1">
                      {demoData.social_insights.social_listening?.conversation_topics?.slice(0, 3).map((topic, i) => (
                        <li key={i} className="text-gray-600 font-montserrat">
                          • {topic}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* How Integration Works */}
      <div className="mt-12 form-section">
        <h2 className="text-2xl font-bold font-montserrat bcm-heading mb-4">
          How Our Data Integration Works
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div 
              className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
              style={{backgroundColor: 'var(--bcm-teal-light)'}}
            >
              <svg className="w-8 h-8 bcm-icon-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold font-montserrat bcm-heading mb-2">
              1. Data Collection
            </h3>
            <p className="text-gray-600 text-sm font-montserrat">
              Our AI agents collect and aggregate data from multiple sources based on your persona inputs.
            </p>
          </div>

          <div className="text-center">
            <div 
              className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
              style={{backgroundColor: 'rgba(255, 152, 0, 0.125)'}}
            >
              <svg className="w-8 h-8 bcm-icon-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold font-montserrat bcm-title mb-2">
              2. AI Analysis
            </h3>
            <p className="text-gray-600 text-sm font-montserrat">
              Advanced AI algorithms analyze patterns, behaviors, and preferences to generate insights.
            </p>
          </div>

          <div className="text-center">
            <div 
              className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
              style={{backgroundColor: 'var(--bcm-cyan-light)'}}
            >
              <svg className="w-8 h-8 bcm-icon-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold font-montserrat bcm-heading-cyan mb-2">
              3. Persona Generation
            </h3>
            <p className="text-gray-600 text-sm font-montserrat">
              Comprehensive personas are generated with actionable insights and marketing recommendations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataSources;

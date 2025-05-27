import React, { useState } from 'react';
import { Tab, TabGroup, TabList, TabPanels, TabPanel } from '@headlessui/react';
import { 
  FaFacebook, 
  FaInstagram, 
  FaTwitter, 
  FaLinkedin, 
  FaTiktok, 
  FaYoutube, 
  FaSnapchat, 
  FaPinterest, 
  FaReddit, 
  FaDiscord,
  FaGoogle,
  FaApple,
  FaMicrosoft,
  FaAmazon,
  FaMobile,
  FaTabletAlt,
  FaDesktop,
  FaTv,
  FaGamepad,
  FaClock,
  FaCalendarDay,
  FaSearch,
  FaUsers,
  FaChartLine,
  FaHeart,
  FaBullseye,
  FaLightbulb,
  FaComments,
  FaEye,
  FaShoppingCart,
  FaGlobe
} from "react-icons/fa";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  AreaChart,
  Area,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ComposedChart,
  ScatterChart,
  Scatter
} from 'recharts';
import ExportPersona from './ExportPersona';

const DetailedPersonaView = ({ generatedPersona }) => {
  const { persona_data, ai_insights, recommendations, pain_points, goals, communication_style, persona_image_url } = generatedPersona;
  
  // Generate comprehensive analytical data
  const generateAnalyticalData = (persona) => {
    const vertical = persona.attributes?.selectedVertical || "General";
    const behaviors = persona.attributes?.selectedBehaviors || [];
    const demographics = persona.demographics || {};
    
    return {
      // Time of Day Usage (with enhanced granularity)
      timeOfDayUsage: [
        { hour: "6AM", mobile: 85, desktop: 15, tablet: 25, total: 125 },
        { hour: "9AM", mobile: 75, desktop: 45, tablet: 20, total: 140 },
        { hour: "12PM", mobile: 90, desktop: 35, tablet: 30, total: 155 },
        { hour: "3PM", mobile: 80, desktop: 40, tablet: 35, total: 155 },
        { hour: "6PM", mobile: 95, desktop: 25, tablet: 40, total: 160 },
        { hour: "9PM", mobile: 100, desktop: 20, tablet: 45, total: 165 },
        { hour: "12AM", mobile: 70, desktop: 10, tablet: 25, total: 105 }
      ],
      
      // Day of Week Patterns
      dayOfWeekUsage: [
        { day: "Mon", engagement: 78, timeSpent: 145, platforms: 4.2 },
        { day: "Tue", engagement: 82, timeSpent: 156, platforms: 4.5 },
        { day: "Wed", engagement: 79, timeSpent: 149, platforms: 4.1 },
        { day: "Thu", engagement: 85, timeSpent: 162, platforms: 4.8 },
        { day: "Fri", engagement: 88, timeSpent: 174, platforms: 5.2 },
        { day: "Sat", engagement: 92, timeSpent: 189, platforms: 5.6 },
        { day: "Sun", engagement: 86, timeSpent: 167, platforms: 4.9 }
      ],
      
      // Platform Deep Dive with Company Logos
      platformAnalysis: [
        { 
          platform: "Instagram", 
          company: "Meta", 
          timeSpent: 45, 
          engagement: 72, 
          contentTypes: ["Stories", "Reels", "Posts"],
          peakHours: ["7-9AM", "6-8PM"],
          demographics: { age: "18-34", gender: "60% Female" },
          adReceptivity: 68
        },
        { 
          platform: "Facebook", 
          company: "Meta", 
          timeSpent: 38, 
          engagement: 65, 
          contentTypes: ["Posts", "Videos", "Groups"],
          peakHours: ["6-8AM", "7-9PM"],
          demographics: { age: "25-54", gender: "55% Female" },
          adReceptivity: 72
        },
        { 
          platform: "YouTube", 
          company: "Google", 
          timeSpent: 52, 
          engagement: 78, 
          contentTypes: ["Long-form", "Shorts", "Live"],
          peakHours: ["8-10PM", "2-4PM"],
          demographics: { age: "18-49", gender: "52% Male" },
          adReceptivity: 75
        },
        { 
          platform: "TikTok", 
          company: "ByteDance", 
          timeSpent: 34, 
          engagement: 82, 
          contentTypes: ["Short Videos", "Live", "Stories"],
          peakHours: ["6-8PM", "9-11PM"],
          demographics: { age: "16-29", gender: "58% Female" },
          adReceptivity: 64
        }
      ],
      
      // Device Ecosystem Analysis
      deviceEcosystem: [
        { device: "iPhone", brand: "Apple", usage: 45, satisfaction: 89, features: ["Camera", "Apps", "Security"] },
        { device: "MacBook", brand: "Apple", usage: 35, satisfaction: 92, features: ["Performance", "Design", "Integration"] },
        { device: "iPad", brand: "Apple", usage: 25, satisfaction: 85, features: ["Portability", "Reading", "Entertainment"] },
        { device: "Smart TV", brand: "Samsung", usage: 55, satisfaction: 78, features: ["Streaming", "Apps", "Picture Quality"] }
      ],
      
      // Purchase Journey Analysis
      purchaseJourney: [
        { stage: "Awareness", touchpoints: 8, duration: "2-3 days", channels: ["Social Media", "Search", "Recommendations"] },
        { stage: "Research", touchpoints: 12, duration: "1-2 weeks", channels: ["Reviews", "Comparison Sites", "Brand Websites"] },
        { stage: "Consideration", touchpoints: 6, duration: "3-5 days", channels: ["Product Pages", "Customer Service", "Demos"] },
        { stage: "Purchase", touchpoints: 3, duration: "1-2 days", channels: ["Online Store", "Physical Store", "Mobile App"] },
        { stage: "Post-Purchase", touchpoints: 5, duration: "1 month", channels: ["Email", "Support", "Social Media"] }
      ],
      
      // Psychographic Radar
      psychographicRadar: [
        { trait: "Innovation", score: 85, category: "Technology Adoption" },
        { trait: "Social Influence", score: 72, category: "Social Behavior" },
        { trait: "Environmental", score: 91, category: "Values" },
        { trait: "Quality Focus", score: 88, category: "Purchase Behavior" },
        { trait: "Brand Loyalty", score: 76, category: "Brand Relationship" },
        { trait: "Price Sensitivity", score: 65, category: "Economic Behavior" }
      ],
      
      // Content Engagement Funnel
      contentFunnel: [
        { stage: "Impression", value: 1000, conversion: 100 },
        { stage: "View", value: 450, conversion: 45 },
        { stage: "Engage", value: 180, conversion: 18 },
        { stage: "Share", value: 65, conversion: 6.5 },
        { stage: "Convert", value: 25, conversion: 2.5 }
      ],
      
      // Sentiment Timeline
      sentimentTimeline: [
        { month: "Jan", positive: 68, neutral: 25, negative: 7 },
        { month: "Feb", positive: 72, neutral: 22, negative: 6 },
        { month: "Mar", positive: 75, neutral: 20, negative: 5 },
        { month: "Apr", positive: 78, neutral: 18, negative: 4 },
        { month: "May", positive: 74, neutral: 21, negative: 5 },
        { month: "Jun", positive: 79, neutral: 17, negative: 4 }
      ]
    };
  };

  const analyticalData = generateAnalyticalData(persona_data);
  
  // Get company logo component
  const getCompanyLogo = (company) => {
    const logoProps = { size: 24, className: "mr-2" };
    const logos = {
      'Meta': <div className="w-6 h-6 mr-2 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold">M</div>,
      'Google': <FaGoogle {...logoProps} style={{ color: '#4285f4' }} />,
      'Apple': <FaApple {...logoProps} style={{ color: '#000000' }} />,
      'Microsoft': <FaMicrosoft {...logoProps} style={{ color: '#00a1f1' }} />,
      'Amazon': <FaAmazon {...logoProps} style={{ color: '#ff9900' }} />,
      'ByteDance': <div className="w-6 h-6 mr-2 rounded-full bg-black flex items-center justify-center text-white text-xs font-bold">B</div>
    };
    return logos[company] || <FaGlobe {...logoProps} />;
  };

  // Get device icon
  const getDeviceIcon = (device) => {
    const iconProps = { size: 20, className: "mr-2" };
    const icons = {
      'iPhone': <FaMobile {...iconProps} style={{ color: '#000000' }} />,
      'MacBook': <FaDesktop {...iconProps} style={{ color: '#000000' }} />,
      'iPad': <FaTabletAlt {...iconProps} style={{ color: '#000000' }} />,
      'Smart TV': <FaTv {...iconProps} style={{ color: '#666666' }} />,
      'Gaming Console': <FaGamepad {...iconProps} style={{ color: '#666666' }} />
    };
    return icons[device] || <FaMobile {...iconProps} />;
  };

  // Get platform icon with brand colors
  const getPlatformIcon = (platform) => {
    const iconProps = { size: 24, className: "mr-3" };
    const icons = {
      'Instagram': <FaInstagram {...iconProps} style={{ color: '#E4405F' }} />,
      'Facebook': <FaFacebook {...iconProps} style={{ color: '#1877F2' }} />,
      'YouTube': <FaYoutube {...iconProps} style={{ color: '#FF0000' }} />,
      'TikTok': <FaTiktok {...iconProps} style={{ color: '#000000' }} />,
      'Twitter': <FaTwitter {...iconProps} style={{ color: '#1DA1F2' }} />,
      'LinkedIn': <FaLinkedin {...iconProps} style={{ color: '#0A66C2' }} />
    };
    return icons[platform] || <FaGlobe {...iconProps} />;
  };

  const tabs = [
    { name: 'Overview', icon: FaEye },
    { name: 'Demographics', icon: FaUsers },
    { name: 'Media Consumption', icon: FaTv },
    { name: 'Psychographics', icon: FaHeart },
    { name: 'Device & Timing', icon: FaClock },
    { name: 'Search Behavior', icon: FaSearch },
    { name: 'Social Listening', icon: FaComments },
    { name: 'Recommendations', icon: FaLightbulb }
  ];

  const OverviewTab = () => (
    <div className="space-y-8">
      {/* Executive Summary */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <FaEye className="mr-3 text-blue-600" />
          Executive Summary
        </h3>
        
        <div className="prose prose-lg max-w-none">
          <p className="text-gray-700 leading-relaxed mb-6">
            <strong>{generatedPersona.name}</strong> represents a digitally-savvy consumer in the <strong>{persona_data?.attributes?.selectedVertical || "General"}</strong> market segment. 
            This persona demonstrates strong alignment with <strong>sustainable and quality-focused purchasing behaviors</strong>, with a primary demographic profile of 
            <strong> {persona_data?.demographics?.age_range || "25-40"} year-old {persona_data?.demographics?.gender || "individual"}</strong> earning 
            <strong> {persona_data?.demographics?.income_range || "$50,000-$75,000"}</strong> annually.
          </p>
          
          <p className="text-gray-700 leading-relaxed mb-6">
            Key behavioral insights reveal a <strong>multi-platform digital consumer</strong> with peak engagement during evening hours and weekends. 
            The persona shows high receptivity to <strong>authentic brand messaging</strong> and demonstrates strong influence from peer recommendations and 
            expert opinions. Purchase decisions are heavily research-driven, with an average consideration period of 1-2 weeks for significant purchases.
          </p>
          
          <p className="text-gray-700 leading-relaxed">
            Strategic opportunities include <strong>mobile-first engagement</strong>, <strong>social proof integration</strong>, and 
            <strong>value-based messaging</strong> that aligns with their core motivations around environmental impact and product quality.
          </p>
        </div>
      </div>

      {/* Key Metrics Dashboard */}
      <div className="grid md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-600 font-semibold text-sm">Digital Engagement</p>
              <p className="text-2xl font-bold text-blue-800">92%</p>
            </div>
            <FaUsers className="text-3xl text-blue-600" />
          </div>
          <p className="text-blue-600 text-sm mt-2">↗ 15% vs avg</p>
        </div>
        
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 border border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-600 font-semibold text-sm">Purchase Intent</p>
              <p className="text-2xl font-bold text-green-800">78%</p>
            </div>
            <FaShoppingCart className="text-3xl text-green-600" />
          </div>
          <p className="text-green-600 text-sm mt-2">↗ 8% vs avg</p>
        </div>
        
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 border border-purple-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-600 font-semibold text-sm">Brand Affinity</p>
              <p className="text-2xl font-bold text-purple-800">85%</p>
            </div>
            <FaHeart className="text-3xl text-purple-600" />
          </div>
          <p className="text-purple-600 text-sm mt-2">↗ 12% vs avg</p>
        </div>
        
        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-6 border border-orange-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-600 font-semibold text-sm">Influence Score</p>
              <p className="text-2xl font-bold text-orange-800">73%</p>
            </div>
            <FaChartLine className="text-3xl text-orange-600" />
          </div>
          <p className="text-orange-600 text-sm mt-2">↗ 5% vs avg</p>
        </div>
      </div>

      {/* Content Engagement Funnel */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h4 className="text-xl font-bold text-gray-800 mb-6">Content Engagement Funnel</h4>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={analyticalData.contentFunnel} layout="horizontal">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="stage" type="category" />
            <Tooltip formatter={(value, name) => [value, name === 'value' ? 'Users' : 'Conversion %']} />
            <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  const DemographicsTab = () => (
    <div className="space-y-8">
      {/* Demographics Overview */}
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h4 className="text-xl font-bold text-gray-800 mb-6">Core Demographics</h4>
          <div className="space-y-4">
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Age Range</span>
              <span className="font-semibold">{persona_data?.demographics?.age_range || "25-40"}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Gender</span>
              <span className="font-semibold">{persona_data?.demographics?.gender || "Female"}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Income Range</span>
              <span className="font-semibold">{persona_data?.demographics?.income_range || "$50,000-$75,000"}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Education</span>
              <span className="font-semibold">{persona_data?.demographics?.education || "Bachelor's Degree"}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Location</span>
              <span className="font-semibold">{persona_data?.demographics?.location || "Urban"}</span>
            </div>
            <div className="flex justify-between py-3">
              <span className="font-medium text-gray-600">Occupation</span>
              <span className="font-semibold">{persona_data?.demographics?.occupation || "Professional"}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h4 className="text-xl font-bold text-gray-800 mb-6">Lifestyle Indicators</h4>
          <div className="space-y-4">
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Family Status</span>
              <span className="font-semibold">{persona_data?.demographics?.family_status || "Single/Partnered"}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Housing</span>
              <span className="font-semibold">Rent/Own Urban Apartment</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Transportation</span>
              <span className="font-semibold">Public Transit + Rideshare</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Shopping Preference</span>
              <span className="font-semibold">Online-first, In-store for experiences</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-100">
              <span className="font-medium text-gray-600">Health & Wellness</span>
              <span className="font-semibold">Fitness-conscious, Organic foods</span>
            </div>
            <div className="flex justify-between py-3">
              <span className="font-medium text-gray-600">Travel</span>
              <span className="font-semibold">2-3 trips/year, Experience-focused</span>
            </div>
          </div>
        </div>
      </div>

      {/* Geographic and Market Analysis */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h4 className="text-xl font-bold text-gray-800 mb-6">Geographic & Market Analysis</h4>
        <div className="grid md:grid-cols-3 gap-6">
          <div>
            <h5 className="font-semibold text-gray-700 mb-3">Market Size</h5>
            <div className="text-2xl font-bold text-blue-600">2.3M</div>
            <div className="text-sm text-gray-500">Similar profiles in target region</div>
          </div>
          <div>
            <h5 className="font-semibold text-gray-700 mb-3">Growth Rate</h5>
            <div className="text-2xl font-bold text-green-600">+8.5%</div>
            <div className="text-sm text-gray-500">Year-over-year segment growth</div>
          </div>
          <div>
            <h5 className="font-semibold text-gray-700 mb-3">Competition</h5>
            <div className="text-2xl font-bold text-orange-600">Medium</div>
            <div className="text-sm text-gray-500">Market saturation level</div>
          </div>
        </div>
      </div>
    </div>
  );

  const MediaConsumptionTab = () => (
    <div className="space-y-8">
      {/* Platform Analysis with Company Logos */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h4 className="text-xl font-bold text-gray-800 mb-6">Platform Deep Dive Analysis</h4>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 font-semibold">Platform</th>
                <th className="text-left py-3 font-semibold">Company</th>
                <th className="text-left py-3 font-semibold">Time/Day</th>
                <th className="text-left py-3 font-semibold">Engagement</th>
                <th className="text-left py-3 font-semibold">Peak Hours</th>
                <th className="text-left py-3 font-semibold">Ad Receptivity</th>
              </tr>
            </thead>
            <tbody>
              {analyticalData.platformAnalysis.map((platform, index) => (
                <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-4 flex items-center">
                    {getPlatformIcon(platform.platform)}
                    <span className="font-medium">{platform.platform}</span>
                  </td>
                  <td className="py-4">
                    <div className="flex items-center">
                      {getCompanyLogo(platform.company)}
                      <span>{platform.company}</span>
                    </div>
                  </td>
                  <td className="py-4">
                    <span className="font-semibold text-blue-600">{platform.timeSpent}min</span>
                  </td>
                  <td className="py-4">
                    <div className="flex items-center">
                      <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-green-500 h-2 rounded-full" 
                          style={{width: `${platform.engagement}%`}}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">{platform.engagement}%</span>
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="space-y-1">
                      {platform.peakHours.map((hour, idx) => (
                        <span key={idx} className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-1">
                          {hour}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="py-4">
                    <span className="font-semibold text-purple-600">{platform.adReceptivity}%</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Time of Day Usage */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h4 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
          <FaClock className="mr-3 text-blue-600" />
          Usage Patterns by Time of Day
        </h4>
        <ResponsiveContainer width="100%" height={350}>
          <AreaChart data={analyticalData.timeOfDayUsage}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="hour" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="mobile" stackId="1" stroke="#FF9800" fill="#FF9800" fillOpacity={0.8} />
            <Area type="monotone" dataKey="desktop" stackId="1" stroke="#004E5F" fill="#004E5F" fillOpacity={0.8} />
            <Area type="monotone" dataKey="tablet" stackId="1" stroke="#00BCD4" fill="#00BCD4" fillOpacity={0.8} />
          </AreaChart>
        </ResponsiveContainer>
        <div className="flex justify-center mt-4 space-x-6">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-orange-500 rounded mr-2"></div>
            <span className="text-sm">Mobile</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-teal-800 rounded mr-2"></div>
            <span className="text-sm">Desktop</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-cyan-500 rounded mr-2"></div>
            <span className="text-sm">Tablet</span>
          </div>
        </div>
      </div>

      {/* Day of Week Analysis */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h4 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
          <FaCalendarDay className="mr-3 text-green-600" />
          Weekly Engagement Patterns
        </h4>
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={analyticalData.dayOfWeekUsage}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis yAxisId="left" />
            <YAxis yAxisId="right" orientation="right" />
            <Tooltip />
            <Bar yAxisId="left" dataKey="engagement" fill="#8884d8" />
            <Line yAxisId="right" type="monotone" dataKey="timeSpent" stroke="#ff7300" strokeWidth={3} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  const PsychographicsTab = () => (
    <div className="space-y-8">
      {/* Psychographic Radar Chart */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h4 className="text-xl font-bold text-gray-800 mb-6">Psychographic Profile</h4>
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={analyticalData.psychographicRadar}>
            <PolarGrid />
            <PolarAngleAxis dataKey="trait" />
            <PolarRadiusAxis angle={0} domain={[0, 100]} />
            <Radar name="Score" dataKey="score" stroke="#8884d8" fill="#8884d8" fillOpacity={0.3} />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Values and Motivators */}
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h4 className="text-xl font-bold text-gray-800 mb-6">Core Values</h4>
          <div className="space-y-4">
            {['Environmental Sustainability', 'Product Quality', 'Social Responsibility', 'Innovation', 'Authenticity'].map((value, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className="font-medium">{value}</span>
                <div className="flex items-center">
                  <div className="w-24 bg-gray-200 rounded-full h-2 mr-3">
                    <div 
                      className="bg-green-500 h-2 rounded-full" 
                      style={{width: `${85 - index * 5}%`}}
                    ></div>
                  </div>
                  <span className="text-sm font-bold">{85 - index * 5}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h4 className="text-xl font-bold text-gray-800 mb-6">Purchase Motivators</h4>
          <div className="space-y-4">
            {['Environmental Impact', 'Product Quality', 'Brand Values', 'Style Appeal', 'Price Value'].map((motivator, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className="font-medium">{motivator}</span>
                <div className="flex items-center">
                  <div className="w-24 bg-gray-200 rounded-full h-2 mr-3">
                    <div 
                      className="bg-orange-500 h-2 rounded-full" 
                      style={{width: `${91 - index * 5}%`}}
                    ></div>
                  </div>
                  <span className="text-sm font-bold">{91 - index * 5}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const DeviceTimingTab = () => (
    <div className="space-y-8">
      {/* Device Ecosystem */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h4 className="text-xl font-bold text-gray-800 mb-6">Device Ecosystem Analysis</h4>
        <div className="grid md:grid-cols-2 gap-6">
          {analyticalData.deviceEcosystem.map((device, index) => (
            <div key={index} className="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center mb-4">
                {getDeviceIcon(device.device)}
                <div>
                  <h5 className="font-semibold text-gray-800">{device.device}</h5>
                  <p className="text-sm text-gray-500">{device.brand}</p>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm">Usage Frequency</span>
                  <span className="font-semibold">{device.usage}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">Satisfaction</span>
                  <span className="font-semibold text-green-600">{device.satisfaction}%</span>
                </div>
                <div>
                  <span className="text-sm text-gray-600">Key Features:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {device.features.map((feature, idx) => (
                      <span key={idx} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Purchase Journey Timeline */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h4 className="text-xl font-bold text-gray-800 mb-6">Purchase Journey Analysis</h4>
        <div className="space-y-6">
          {analyticalData.purchaseJourney.map((stage, index) => (
            <div key={index} className="flex items-start">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-4">
                {index + 1}
              </div>
              <div className="flex-1">
                <div className="flex justify-between items-start mb-2">
                  <h5 className="font-semibold text-gray-800">{stage.stage}</h5>
                  <span className="text-sm text-gray-500">{stage.duration}</span>
                </div>
                <p className="text-sm text-gray-600 mb-2">{stage.touchpoints} touchpoints on average</p>
                <div className="flex flex-wrap gap-2">
                  {stage.channels.map((channel, idx) => (
                    <span key={idx} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {channel}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-8 bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <img 
              src="https://mma.prnewswire.com/media/2444113/BCM_Updated_2024_FullName_Orange_Logo.jpg" 
              alt="Beeby Clark+Meyler Logo"
              className="w-24 h-auto object-contain mr-6"
            />
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                Detailed Persona Analysis: {generatedPersona.name}
              </h1>
              <p className="text-gray-600">
                Comprehensive analytical report • Generated {new Date(generatedPersona.generated_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <ExportPersona 
              generatedPersona={generatedPersona}
              className="export-button"
            />
            <a
              href={`/persona/${generatedPersona.persona_data.id}/visual`}
              className="bcm-btn-secondary text-sm py-2 px-4 flex items-center hover:bg-gray-100 transition-colors"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Visual Template
            </a>
            <div className="text-right">
              <div className="text-2xl font-bold text-blue-600">95%</div>
              <div className="text-sm text-gray-500">Confidence Score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabbed Interface */}
      <TabGroup>
        <TabList className="flex flex-wrap gap-2 rounded-xl bg-blue-900/20 p-2 mb-8 lg:gap-1 lg:space-x-1">
          {tabs.map((tab, index) => (
            <Tab
              key={index}
              className={({ selected }) =>
                `flex-1 min-w-0 rounded-lg py-2 px-2 lg:py-3 lg:px-4 text-xs lg:text-sm font-medium leading-5 text-blue-700 transition-all
                ${selected
                  ? 'bg-white text-blue-700 shadow'
                  : 'text-blue-600 hover:bg-white/20 hover:text-blue-600'
                }`
              }
            >
              <div className="flex items-center justify-center">
                <tab.icon className="mr-1 lg:mr-2 flex-shrink-0" size={14} />
                <span className="truncate text-center">{tab.name}</span>
              </div>
            </Tab>
          ))}
        </TabList>
        
        <TabPanels>
          <Tab.Panel><OverviewTab /></Tab.Panel>
          <Tab.Panel><DemographicsTab /></Tab.Panel>
          <Tab.Panel><MediaConsumptionTab /></Tab.Panel>
          <Tab.Panel><PsychographicsTab /></Tab.Panel>
          <Tab.Panel><DeviceTimingTab /></Tab.Panel>
          <Tab.Panel>
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h3 className="text-xl font-bold mb-4">Search Behavior Analysis</h3>
              <p className="text-gray-600">Search behavior insights and keyword analysis would go here...</p>
            </div>
          </Tab.Panel>
          <Tab.Panel>
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h3 className="text-xl font-bold mb-4">Social Listening Insights</h3>
              <p className="text-gray-600">Social listening data and sentiment analysis would go here...</p>
            </div>
          </Tab.Panel>
          <Tab.Panel>
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h3 className="text-xl font-bold mb-4">Strategic Recommendations</h3>
              <p className="text-gray-600">Marketing recommendations and strategic insights would go here...</p>
            </div>
          </Tab.Panel>
        </TabPanels>
      </TabGroup>
    </div>
  );
};

export default DetailedPersonaView;
import React from "react";
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
  FaMobile,
  FaShare,
  FaSearch,
  FaUsers,
  FaChartLine,
  FaHeart,
  FaEye,
  FaShoppingCart,
  FaClock,
  FaGlobe,
  FaBullseye,
  FaLightbulb,
  FaComments
} from "react-icons/fa";
import ExportPersona from './ExportPersona';
import { 
  PieChart, 
  Pie, 
  Cell, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  Area,
  AreaChart
} from 'recharts';

const VisualPersonaTemplate = ({ generatedPersona }) => {
  const { persona_data, ai_insights, recommendations, pain_points, goals, communication_style, persona_image_url } = generatedPersona;
  
  // Generate comprehensive mock data based on persona attributes
  const generateMockDataSources = (persona) => {
    const vertical = persona.attributes?.selectedVertical || "General";
    const behaviors = persona.attributes?.selectedBehaviors || [];
    const demographics = persona.demographics || {};
    
    // SEMRush Mock Data
    const semrushData = {
      topKeywords: [
        { keyword: "sustainable fashion", volume: 45000, competition: 0.7, trend: "rising" },
        { keyword: "eco friendly clothes", volume: 32000, competition: 0.6, trend: "stable" },
        { keyword: "organic cotton", volume: 28000, competition: 0.8, trend: "rising" },
        { keyword: "ethical brands", volume: 18000, competition: 0.5, trend: "rising" }
      ],
      deviceUsage: [
        { device: "Mobile", percentage: 68, color: "#FF9800" },
        { device: "Desktop", percentage: 25, color: "#004E5F" },
        { device: "Tablet", percentage: 7, color: "#00BCD4" }
      ],
      searchIntent: [
        { intent: "Research", value: 45 },
        { intent: "Compare", value: 30 },
        { intent: "Purchase", value: 25 }
      ]
    };

    // SparkToro Mock Data
    const sparktoroData = {
      influencers: [
        { name: "Sustainable Style Co", followers: "145K", engagement: "4.2%", platform: "Instagram" },
        { name: "Eco Fashion Forward", followers: "89K", engagement: "3.8%", platform: "YouTube" },
        { name: "Green Living Guru", followers: "67K", engagement: "5.1%", platform: "TikTok" }
      ],
      contentPreferences: [
        { category: "Sustainability Tips", interest: 85 },
        { category: "Product Reviews", interest: 78 },
        { category: "Style Guides", interest: 72 },
        { category: "Brand Stories", interest: 65 }
      ],
      platformEngagement: [
        { platform: "Instagram", time: 45, engagement: 72 },
        { platform: "YouTube", time: 38, engagement: 68 },
        { platform: "Pinterest", time: 28, engagement: 61 },
        { platform: "TikTok", time: 22, engagement: 59 }
      ]
    };

    // Buzzabout.ai Mock Data
    const buzzaboutData = {
      sentiment: [
        { category: "Overall", positive: 72, neutral: 20, negative: 8 },
        { category: "Product Quality", positive: 78, neutral: 18, negative: 4 },
        { category: "Customer Service", positive: 65, neutral: 25, negative: 10 },
        { category: "Sustainability", positive: 84, neutral: 14, negative: 2 }
      ],
      trendingTopics: [
        { topic: "Circular Fashion", mentions: 1250, sentiment: 0.82, growth: "+35%" },
        { topic: "Sustainable Materials", mentions: 890, sentiment: 0.76, growth: "+22%" },
        { topic: "Ethical Production", mentions: 672, sentiment: 0.79, growth: "+18%" }
      ],
      conversationDrivers: [
        { driver: "Environmental Impact", score: 89 },
        { driver: "Quality & Durability", score: 76 },
        { driver: "Price Value", score: 68 },
        { driver: "Style & Design", score: 74 }
      ]
    };

    // Resonate AI Mock Data
    const resonateData = {
      psychographics: [
        { trait: "Environmentally Conscious", score: 92 },
        { trait: "Quality Focused", score: 85 },
        { trait: "Brand Loyal", score: 73 },
        { trait: "Socially Responsible", score: 88 },
        { trait: "Innovation Seeking", score: 71 }
      ],
      lifestyleSegments: [
        { segment: "Conscious Consumer", percentage: 35, color: "#4CAF50" },
        { segment: "Quality Seeker", percentage: 28, color: "#FF9800" },
        { segment: "Trendsetter", percentage: 22, color: "#00BCD4" },
        { segment: "Value Conscious", percentage: 15, color: "#9C27B0" }
      ],
      purchaseMotivations: [
        { motivation: "Environmental Impact", importance: 91 },
        { motivation: "Product Quality", importance: 86 },
        { motivation: "Brand Values", importance: 78 },
        { motivation: "Style Appeal", importance: 74 },
        { motivation: "Price Value", importance: 65 }
      ]
    };

    return { semrushData, sparktoroData, buzzaboutData, resonateData };
  };

  const mockData = generateMockDataSources(persona_data);
  const { semrushData, sparktoroData, buzzaboutData, resonateData } = mockData;
  
  // Social Media Platform Logos/Icons
  const getSocialMediaIcon = (platform) => {
    const iconProps = { size: 20, className: "mr-2" };
    
    const icons = {
      'Facebook': <FaFacebook {...iconProps} style={{ color: '#1877F2' }} />,
      'Instagram': <FaInstagram {...iconProps} style={{ color: '#E4405F' }} />,
      'Twitter/X': <FaTwitter {...iconProps} style={{ color: '#1DA1F2' }} />,
      'LinkedIn': <FaLinkedin {...iconProps} style={{ color: '#0A66C2' }} />,
      'TikTok': <FaTiktok {...iconProps} style={{ color: '#000000' }} />,
      'YouTube': <FaYoutube {...iconProps} style={{ color: '#FF0000' }} />,
      'Snapchat': <FaSnapchat {...iconProps} style={{ color: '#FFFC00' }} />,
      'Pinterest': <FaPinterest {...iconProps} style={{ color: '#BD081C' }} />,
      'Reddit': <FaReddit {...iconProps} style={{ color: '#FF4500' }} />,
      'Discord': <FaDiscord {...iconProps} style={{ color: '#5865F2' }} />
    };
    return icons[platform] || <FaMobile {...iconProps} style={{ color: '#666' }} />;
  };

  return (
    <div className="visual-persona-template p-8 bg-gradient-to-br from-gray-50 to-blue-50 min-h-screen font-montserrat">
      {/* Header Section with Professional Image */}
      <div className="mb-8 bg-white rounded-2xl shadow-xl overflow-hidden">
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-teal-600 h-32 relative">
          <div className="absolute inset-0 bg-black bg-opacity-20"></div>
          <div className="absolute bottom-4 left-8 text-white">
            <h1 className="text-3xl font-bold font-montserrat">{persona_data?.name || "Generated Persona"}</h1>
            <p className="text-lg opacity-90">Data-Driven Consumer Profile</p>
          </div>
          <div className="absolute bottom-4 right-8">
            <a
              href={`/persona/${persona_data?.id}/detailed`}
              className="bg-white text-blue-600 hover:bg-blue-50 transition-colors px-4 py-2 rounded-lg flex items-center font-medium text-sm shadow-md"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Detailed Analysis
            </a>
          </div>
        </div>
        
        <div className="p-8">
          <div className="flex flex-col lg:flex-row gap-8">
            {/* Profile Image Section */}
            <div className="flex-shrink-0">
              <div className="relative">
                <img 
                  src={persona_image_url} 
                  alt="Professional headshot"
                  className="w-64 h-64 object-cover rounded-2xl shadow-lg border-4 border-white"
                />
                
                {/* BCM Logo overlay */}
                <div className="absolute -bottom-6 -right-6 w-24 h-24 rounded-xl flex items-center justify-center shadow-lg border-4 border-white bg-white" 
                     style={{background: 'white'}}>
                  <img 
                    src="https://mma.prnewswire.com/media/2444113/BCM_Updated_2024_FullName_Orange_Logo.jpg" 
                    alt="Beeby Clark+Meyler Logo"
                    className="w-20 h-auto object-contain"
                  />
                </div>
              </div>
            </div>

            {/* Basic Info & Data Source Logos */}
            <div className="flex-1">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Demographics</h3>
                  <div className="space-y-2 text-sm">
                    <div><span className="font-semibold">Age:</span> {persona_data?.demographics?.age_range || "25-40"}</div>
                    <div><span className="font-semibold">Gender:</span> {persona_data?.demographics?.gender || "Female"}</div>
                    <div><span className="font-semibold">Income:</span> {persona_data?.demographics?.income_range || "$50,000-$75,000"}</div>
                    <div><span className="font-semibold">Location:</span> {persona_data?.demographics?.location || "Urban"}</div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Powered By</h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="flex items-center p-2 bg-blue-50 rounded-lg">
                      <FaSearch className="text-blue-600 mr-2" />
                      <span className="text-xs font-semibold">SEMRush</span>
                    </div>
                    <div className="flex items-center p-2 bg-purple-50 rounded-lg">
                      <FaUsers className="text-purple-600 mr-2" />
                      <span className="text-xs font-semibold">SparkToro</span>
                    </div>
                    <div className="flex items-center p-2 bg-green-50 rounded-lg">
                      <FaComments className="text-green-600 mr-2" />
                      <span className="text-xs font-semibold">Buzzabout.ai</span>
                    </div>
                    <div className="flex items-center p-2 bg-orange-50 rounded-lg">
                      <FaBullseye className="text-orange-600 mr-2" />
                      <span className="text-xs font-semibold">Resonate AI</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Data Source Insights Grid */}
      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        
        {/* SEMRush Search Insights */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center mb-6">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mr-4">
              <FaSearch className="text-blue-600 text-xl" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-800">SEMRush Insights</h3>
              <p className="text-sm text-gray-600">Search Behavior & Keywords</p>
            </div>
          </div>

          {/* Top Keywords */}
          <div className="mb-6">
            <h4 className="font-semibold mb-3 text-gray-700">Top Search Keywords</h4>
            <div className="space-y-2">
              {semrushData.topKeywords.slice(0, 3).map((keyword, index) => (
                <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <div>
                    <span className="font-medium">{keyword.keyword}</span>
                    <span className={`ml-2 text-xs px-2 py-1 rounded ${
                      keyword.trend === 'rising' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {keyword.trend}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-blue-600">{keyword.volume.toLocaleString()}</div>
                    <div className="text-xs text-gray-500">searches/mo</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Device Usage Chart */}
          <div>
            <h4 className="font-semibold mb-3 text-gray-700">Device Preference</h4>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={semrushData.deviceUsage}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="percentage"
                  label={({device, percentage}) => `${device}: ${percentage}%`}
                >
                  {semrushData.deviceUsage.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* SparkToro Audience Insights */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center mb-6">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mr-4">
              <FaUsers className="text-purple-600 text-xl" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-800">SparkToro Insights</h3>
              <p className="text-sm text-gray-600">Audience & Influencer Data</p>
            </div>
          </div>

          {/* Top Influencers */}
          <div className="mb-6">
            <h4 className="font-semibold mb-3 text-gray-700">Key Influencers</h4>
            <div className="space-y-3">
              {sparktoroData.influencers.map((influencer, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <div className="font-medium">{influencer.name}</div>
                    <div className="text-xs text-gray-500">{influencer.platform}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-semibold">{influencer.followers}</div>
                    <div className="text-xs text-green-600">{influencer.engagement}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Content Preferences Chart */}
          <div>
            <h4 className="font-semibold mb-3 text-gray-700">Content Interest</h4>
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={sparktoroData.contentPreferences} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 100]} />
                <YAxis dataKey="category" type="category" width={80} fontSize={10} />
                <Tooltip />
                <Bar dataKey="interest" fill="#9C27B0" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Buzzabout.ai Social Listening */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center mb-6">
            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mr-4">
              <FaComments className="text-green-600 text-xl" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-800">Buzzabout.ai Insights</h3>
              <p className="text-sm text-gray-600">Social Listening & Sentiment</p>
            </div>
          </div>

          {/* Sentiment Analysis */}
          <div className="mb-6">
            <h4 className="font-semibold mb-3 text-gray-700">Sentiment Analysis</h4>
            <div className="space-y-3">
              {buzzaboutData.sentiment.slice(0, 2).map((item, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex justify-between mb-2">
                    <span className="font-medium">{item.category}</span>
                    <span className="text-sm text-gray-600">{item.positive + item.neutral + item.negative}% coverage</span>
                  </div>
                  <div className="flex rounded-full h-3 overflow-hidden">
                    <div className="bg-green-500" style={{width: `${item.positive}%`}}></div>
                    <div className="bg-gray-300" style={{width: `${item.neutral}%`}}></div>
                    <div className="bg-red-500" style={{width: `${item.negative}%`}}></div>
                  </div>
                  <div className="flex justify-between text-xs mt-1 text-gray-600">
                    <span>Positive: {item.positive}%</span>
                    <span>Neutral: {item.neutral}%</span>
                    <span>Negative: {item.negative}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Trending Topics */}
          <div>
            <h4 className="font-semibold mb-3 text-gray-700">Trending Conversations</h4>
            <div className="space-y-2">
              {buzzaboutData.trendingTopics.map((topic, index) => (
                <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded-lg">
                  <div>
                    <span className="font-medium text-sm">{topic.topic}</span>
                    <div className="text-xs text-gray-500">{topic.mentions.toLocaleString()} mentions</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-semibold text-green-600">{topic.growth}</div>
                    <div className="text-xs text-gray-500">growth</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Resonate AI Psychographics */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center mb-6">
            <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mr-4">
              <FaBullseye className="text-orange-600 text-xl" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-800">Resonate AI Insights</h3>
              <p className="text-sm text-gray-600">Psychographics & Motivations</p>
            </div>
          </div>

          {/* Psychographic Traits */}
          <div className="mb-6">
            <h4 className="font-semibold mb-3 text-gray-700">Psychographic Profile</h4>
            <div className="space-y-3">
              {resonateData.psychographics.slice(0, 4).map((trait, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-sm font-medium">{trait.trait}</span>
                  <div className="flex items-center">
                    <div className="w-24 bg-gray-200 rounded-full h-2 mr-3">
                      <div 
                        className="bg-orange-500 h-2 rounded-full transition-all duration-300"
                        style={{width: `${trait.score}%`}}
                      ></div>
                    </div>
                    <span className="text-sm font-bold text-orange-600">{trait.score}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Lifestyle Segments */}
          <div>
            <h4 className="font-semibold mb-3 text-gray-700">Lifestyle Segmentation</h4>
            <ResponsiveContainer width="100%" height={160}>
              <PieChart>
                <Pie
                  data={resonateData.lifestyleSegments}
                  cx="50%"
                  cy="50%"
                  outerRadius={60}
                  dataKey="percentage"
                  label={({segment, percentage}) => `${percentage}%`}
                >
                  {resonateData.lifestyleSegments.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value, name) => [`${value}%`, name]} />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex flex-wrap gap-2 mt-2">
              {resonateData.lifestyleSegments.map((segment, index) => (
                <div key={index} className="flex items-center">
                  <div 
                    className="w-3 h-3 rounded mr-1"
                    style={{backgroundColor: segment.color}}
                  ></div>
                  <span className="text-xs">{segment.segment}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Social Media Platforms - Enhanced */}
      {persona_data?.media_consumption?.social_media_platforms?.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
          <div className="flex items-center mb-6">
            <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mr-4">
              <FaShare className="text-indigo-600 text-xl" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-800">Social Media Engagement</h3>
              <p className="text-sm text-gray-600">Platform Usage & Preferences</p>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {persona_data.media_consumption.social_media_platforms.map((platform, index) => {
              const engagement = sparktoroData.platformEngagement.find(p => p.platform === platform) || 
                                { time: Math.floor(Math.random() * 50) + 10, engagement: Math.floor(Math.random() * 40) + 50 };
              
              return (
                <div key={index} className="flex flex-col items-center p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors duration-200">
                  <div className="flex items-center mb-3">
                    {getSocialMediaIcon(platform)}
                    <span className="text-sm font-montserrat font-medium text-gray-700">{platform}</span>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-indigo-600">{engagement.time}min</div>
                    <div className="text-xs text-gray-500">daily usage</div>
                    <div className="text-sm font-semibold text-green-600 mt-1">{engagement.engagement}%</div>
                    <div className="text-xs text-gray-500">engagement</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Key Insights Summary */}
      <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center mr-4">
            <FaLightbulb className="text-teal-600 text-xl" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-800">Key Marketing Insights</h3>
            <p className="text-sm text-gray-600">Data-Driven Recommendations</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold mb-3 text-gray-700">
              <FaBullseye className="inline mr-2 text-orange-500" />
              Primary Motivations
            </h4>
            <div className="space-y-2">
              {resonateData.purchaseMotivations.slice(0, 3).map((motivation, index) => (
                <div key={index} className="flex justify-between items-center p-2 bg-orange-50 rounded-lg">
                  <span className="text-sm">{motivation.motivation}</span>
                  <span className="font-bold text-orange-600">{motivation.importance}%</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-semibold mb-3 text-gray-700">
              <FaChartLine className="inline mr-2 text-green-500" />
              Conversation Drivers
            </h4>
            <div className="space-y-2">
              {buzzaboutData.conversationDrivers.slice(0, 3).map((driver, index) => (
                <div key={index} className="flex justify-between items-center p-2 bg-green-50 rounded-lg">
                  <span className="text-sm">{driver.driver}</span>
                  <span className="font-bold text-green-600">{driver.score}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Original Persona Data - Enhanced */}
      {ai_insights && (
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <h3 className="text-xl font-bold mb-4 text-gray-800">AI-Generated Profile</h3>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {pain_points && pain_points.length > 0 && (
              <div>
                <h4 className="font-semibold mb-3 text-red-600">
                  <FaHeart className="inline mr-2" />
                  Pain Points
                </h4>
                <ul className="space-y-2">
                  {pain_points.map((point, index) => (
                    <li key={index} className="text-sm p-2 bg-red-50 rounded border-l-3 border-red-500">
                      {point}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {goals && goals.length > 0 && (
              <div>
                <h4 className="font-semibold mb-3 text-green-600">
                  <FaBullseye className="inline mr-2" />
                  Goals & Aspirations
                </h4>
                <ul className="space-y-2">
                  {goals.map((goal, index) => (
                    <li key={index} className="text-sm p-2 bg-green-50 rounded border-l-3 border-green-500">
                      {goal}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {recommendations && recommendations.length > 0 && (
              <div>
                <h4 className="font-semibold mb-3 text-blue-600">
                  <FaLightbulb className="inline mr-2" />
                  Marketing Recommendations
                </h4>
                <ul className="space-y-2">
                  {recommendations.map((rec, index) => (
                    <li key={index} className="text-sm p-2 bg-blue-50 rounded border-l-3 border-blue-500">
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default VisualPersonaTemplate;
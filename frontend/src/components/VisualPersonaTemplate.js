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
  FaMobile
} from "react-icons/fa";

const VisualPersonaTemplate = ({ generatedPersona }) => {
  const { persona_data, ai_insights, recommendations, pain_points, goals, communication_style, persona_image_url } = generatedPersona;
  
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

  // Device Icons
  const getDeviceIcon = (device) => {
    const icons = {
      'Smartphone': '📱',
      'Tablet': '📟',
      'Laptop': '💻',
      'Desktop': '🖥️',
      'Smart TV': '📺',
      'Smart speaker': '🔊',
      'Gaming console': '🎮',
      'Wearable device': '⌚'
    };
    return icons[device] || '📱';
  };

  // Calculate completion percentage for visual indicators
  const calculateCompletionScore = () => {
    let totalFields = 0;
    let completedFields = 0;
    
    // Check demographics
    Object.values(persona_data?.demographics || {}).forEach(value => {
      totalFields++;
      if (value) completedFields++;
    });
    
    // Check attributes
    Object.values(persona_data?.attributes || {}).forEach(value => {
      totalFields++;
      if (Array.isArray(value) ? value.length > 0 : value) completedFields++;
    });
    
    // Check media consumption
    Object.values(persona_data?.media_consumption || {}).forEach(value => {
      totalFields++;
      if (Array.isArray(value) ? value.length > 0 : value) completedFields++;
    });
    
    return Math.round((completedFields / totalFields) * 100);
  };

  // Calculate engagement metrics
  const calculateEngagementMetrics = () => {
    const media = persona_data?.media_consumption;
    const demographics = persona_data?.demographics;
    
    // Social Media Score (0-100)
    const socialPlatforms = media?.social_media_platforms?.length || 0;
    const socialScore = Math.min(socialPlatforms * 15 + 10, 100);
    
    // Digital Fluency Score (based on devices and age)
    const deviceCount = media?.preferred_devices?.length || 0;
    const ageRange = demographics?.age_range || "30-40";
    const isYoung = ageRange.includes("18-24") || ageRange.includes("25-40");
    const digitalBase = isYoung ? 70 : 50;
    const digitalScore = Math.min(digitalBase + (deviceCount * 8), 100);
    
    // Content Engagement (based on content types and time)
    const contentTypes = media?.content_types?.length || 0;
    const hasHighTime = media?.consumption_time?.includes("4-6") || media?.consumption_time?.includes("6+");
    const contentScore = Math.min((contentTypes * 12) + (hasHighTime ? 25 : 10), 100);
    
    return { socialScore, digitalScore, contentScore };
  };

  const { socialScore, digitalScore, contentScore } = calculateEngagementMetrics();

  // Render circular progress chart
  const renderCircularChart = (percentage, size = 80, strokeWidth = 8, color = '#FF9800') => {
    const radius = (size - strokeWidth) / 2;
    const circumference = radius * 2 * Math.PI;
    const strokeDasharray = `${circumference} ${circumference}`;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;

    return (
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#e5e7eb"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-500"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-bold font-montserrat" style={{ color }}>
            {percentage}%
          </span>
        </div>
      </div>
    );
  };

  const renderPersonaCard = () => (
    <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-2xl p-8 mb-8 border border-gray-100"
         style={{boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.15)'}}>
      <div className="flex flex-col lg:flex-row items-start space-y-6 lg:space-y-0 lg:space-x-8">
        {/* Large Persona Image with enhanced styling */}
        <div className="flex-shrink-0 mx-auto lg:mx-0 relative">
          {persona_image_url ? (
            <div className="relative">
              <img
                src={persona_image_url}
                alt={generatedPersona.name}
                className="w-60 h-60 lg:w-72 lg:h-72 rounded-2xl object-cover shadow-2xl border-4 border-white"
                style={{
                  boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.05)'
                }}
              />
              {/* Decorative overlay */}
              <div className="absolute -bottom-4 -right-4 w-16 h-16 rounded-full flex items-center justify-center shadow-lg border-4 border-white" 
                   style={{background: 'linear-gradient(135deg, var(--bcm-orange), var(--bcm-cyan))'}}>
                <span className="text-white font-bold text-sm font-montserrat">AI</span>
              </div>
            </div>
          ) : (
            <div className="w-60 h-60 lg:w-72 lg:h-72 bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl flex items-center justify-center shadow-2xl border-4 border-white">
              <div className="text-center">
                <svg className="w-24 h-24 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <p className="text-gray-500 font-montserrat text-sm">Loading Image...</p>
              </div>
            </div>
          )}
        </div>
        
        {/* Enhanced Persona Details */}
        <div className="flex-1 text-center lg:text-left">
          <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start mb-6">
            <div>
              <h1 className="text-4xl lg:text-6xl font-bold font-montserrat bcm-heading mb-3 bg-clip-text text-transparent bg-gradient-to-r from-gray-800 to-gray-600">
                {generatedPersona.name}
              </h1>
              <p className="text-xl lg:text-2xl text-gray-600 font-montserrat mb-4">
                {persona_data?.demographics?.occupation || "Professional"}
              </p>
              <div className="flex flex-wrap gap-2 justify-center lg:justify-start mb-4">
                <div className="inline-flex items-center px-4 py-2 rounded-full text-sm font-montserrat text-white shadow-lg" 
                     style={{background: 'linear-gradient(135deg, var(--bcm-teal), var(--bcm-cyan))'}}>
                  📅 {persona_data?.demographics?.age_range || "N/A"}
                </div>
                <div className="inline-flex items-center px-4 py-2 rounded-full text-sm font-montserrat text-white shadow-lg" 
                     style={{background: 'linear-gradient(135deg, var(--bcm-orange), #ff6b35)'}}>
                  💰 {persona_data?.demographics?.income_range || "N/A"}
                </div>
              </div>
            </div>
            
            <div className="mx-auto lg:mx-0 lg:text-right">
              <div className="relative mb-3">
                {renderCircularChart(calculateCompletionScore(), 100, 10, 'var(--bcm-orange)')}
              </div>
              <p className="text-sm text-gray-500 font-montserrat font-semibold">Data Completeness</p>
            </div>
          </div>
          
          {/* Enhanced demographic cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { icon: '📍', label: 'Location', value: persona_data?.demographics?.location },
              { icon: '🎓', label: 'Education', value: persona_data?.demographics?.education },
              { icon: '👥', label: 'Family', value: persona_data?.demographics?.family_status },
              { icon: '💼', label: 'Experience', value: 'Professional' }
            ].map((item, index) => (
              <div key={index} className="bg-white rounded-xl p-4 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
                <div className="text-2xl mb-2">{item.icon}</div>
                <span className="font-semibold text-gray-700 font-montserrat block text-xs mb-1">{item.label}</span>
                <p className="text-gray-600 font-montserrat text-sm">{item.value || "N/A"}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderSection = (title, content, icon, bgColor = "bg-gradient-to-br from-white to-gray-50", shadowColor = "rgba(0, 0, 0, 0.08)") => (
    <div className={`${bgColor} rounded-2xl p-8 mb-8 border border-gray-100 shadow-xl`}
         style={{boxShadow: `0 20px 25px -5px ${shadowColor}, 0 10px 10px -5px rgba(0, 0, 0, 0.04)`}}>
      <div className="flex items-center mb-6">
        <div className="w-14 h-14 rounded-2xl flex items-center justify-center mr-4 shadow-lg" style={{background: 'linear-gradient(135deg, var(--bcm-teal), var(--bcm-cyan))'}}>
          <span className="text-white text-2xl">{icon}</span>
        </div>
        <h2 className="text-2xl font-bold font-montserrat bcm-heading">{title}</h2>
      </div>
      {content}
    </div>
  );

  const renderPersonalityTraits = () => (
    <div className="flex flex-wrap gap-3">
      {ai_insights?.personality_traits?.map((trait, index) => (
        <div key={index} className="group relative">
          <span 
            className="px-4 py-2 rounded-xl text-sm font-montserrat text-white shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
            style={{background: `linear-gradient(135deg, var(--bcm-cyan), var(--bcm-teal))`}}
          >
            {trait}
          </span>
        </div>
      ))}
    </div>
  );

  const renderMediaConsumption = () => {
    const media = persona_data?.media_consumption;
    if (!media) return <p className="text-gray-500 font-montserrat">No media consumption data</p>;

    return (
      <div className="space-y-8">
        {/* Social Media Platforms with Icons */}
        {media.social_media_platforms?.length > 0 && (
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <h4 className="font-bold font-montserrat bcm-heading mb-4 flex items-center">
              📱 Social Media Platforms
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {media.social_media_platforms.map((platform, index) => (
                <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <span className="text-2xl mr-3">{getSocialMediaIcon(platform)}</span>
                  <span className="text-sm font-montserrat font-medium text-gray-700">{platform}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Devices with Icons */}
        {media.preferred_devices?.length > 0 && (
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <h4 className="font-bold font-montserrat bcm-heading mb-4 flex items-center">
              💻 Preferred Devices
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {media.preferred_devices.map((device, index) => (
                <div key={index} className="flex flex-col items-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                  <span className="text-3xl mb-2">{getDeviceIcon(device)}</span>
                  <span className="text-xs font-montserrat font-medium text-gray-700 text-center">{device}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Usage Stats */}
        <div className="grid md:grid-cols-2 gap-6">
          {media.consumption_time && (
            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
              <h4 className="font-bold font-montserrat bcm-heading mb-4">⏰ Daily Usage</h4>
              <div className="flex items-center">
                <div className="w-16 h-16 rounded-full flex items-center justify-center mr-4" style={{background: 'linear-gradient(135deg, var(--bcm-orange), #ff6b35)'}}>
                  <span className="text-white font-bold text-sm">📊</span>
                </div>
                <div>
                  <p className="text-lg font-bold font-montserrat text-gray-800">{media.consumption_time}</p>
                  <p className="text-sm text-gray-500 font-montserrat">per day</p>
                </div>
              </div>
            </div>
          )}
          
          {media.advertising_receptivity && (
            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
              <h4 className="font-bold font-montserrat bcm-heading mb-4">📊 Ad Receptivity</h4>
              <div className="flex items-center">
                <div className="w-16 h-16 rounded-full flex items-center justify-center mr-4" style={{background: 'linear-gradient(135deg, var(--bcm-teal), var(--bcm-cyan)'}}>
                  <span className="text-white font-bold text-sm">🎯</span>
                </div>
                <div>
                  <p className="text-lg font-bold font-montserrat text-gray-800">{media.advertising_receptivity}</p>
                  <p className="text-sm text-gray-500 font-montserrat">to advertising</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderEngagementMetrics = () => {
    return (
      <div className="space-y-6">
        {/* Circular Charts */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex justify-center mb-4">
              {renderCircularChart(socialScore, 120, 12, 'var(--bcm-orange)')}
            </div>
            <h4 className="font-bold font-montserrat text-lg mb-2" style={{color: 'var(--bcm-orange)'}}>Social Engagement</h4>
            <p className="text-sm text-gray-500 font-montserrat">Platform activity & connection</p>
          </div>
          
          <div className="text-center bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex justify-center mb-4">
              {renderCircularChart(digitalScore, 120, 12, 'var(--bcm-teal)')}
            </div>
            <h4 className="font-bold font-montserrat text-lg mb-2" style={{color: 'var(--bcm-teal)'}}>Digital Fluency</h4>
            <p className="text-sm text-gray-500 font-montserrat">Technology adoption & usage</p>
          </div>
          
          <div className="text-center bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div className="flex justify-center mb-4">
              {renderCircularChart(contentScore, 120, 12, 'var(--bcm-cyan)')}
            </div>
            <h4 className="font-bold font-montserrat text-lg mb-2" style={{color: 'var(--bcm-cyan)'}}>Content Affinity</h4>
            <p className="text-sm text-gray-500 font-montserrat">Content consumption patterns</p>
          </div>
        </div>

        {/* Comparative Bar Chart */}
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
          <h4 className="font-bold font-montserrat bcm-heading mb-6">📈 Engagement Index Comparison</h4>
          <div className="space-y-4">
            {[
              { label: 'Social Engagement', value: socialScore, color: 'var(--bcm-orange)', icon: '📱' },
              { label: 'Digital Fluency', value: digitalScore, color: 'var(--bcm-teal)', icon: '💻' },
              { label: 'Content Affinity', value: contentScore, color: 'var(--bcm-cyan)', icon: '📺' }
            ].map((metric, index) => (
              <div key={index} className="flex items-center space-x-4">
                <span className="text-2xl">{metric.icon}</span>
                <span className="font-medium font-montserrat text-gray-700 w-32">{metric.label}</span>
                <div className="flex-1 bg-gray-200 rounded-full h-4 relative overflow-hidden">
                  <div 
                    className="h-4 rounded-full transition-all duration-1000 ease-out"
                    style={{
                      width: `${metric.value}%`,
                      background: `linear-gradient(90deg, ${metric.color}, ${metric.color}dd)`
                    }}
                  />
                </div>
                <span className="font-bold font-montserrat text-lg w-12" style={{color: metric.color}}>
                  {metric.value}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderListWithIcons = (items, iconColor = 'var(--bcm-teal)') => (
    <div className="space-y-3">
      {items?.map((item, index) => (
        <div key={index} className="flex items-start bg-white rounded-lg p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
          <div className="w-3 h-3 rounded-full mt-2 mr-4 flex-shrink-0" style={{backgroundColor: iconColor}}></div>
          <p className="text-gray-700 font-montserrat leading-relaxed">{item}</p>
        </div>
      ))}
    </div>
  );

  return (
    <div className="bg-gray-50 min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold font-montserrat mb-2 bcm-title">
            BCM VentasAI Persona Profile
          </h1>
          <p className="text-gray-600 font-montserrat">
            AI-Generated Consumer Persona • Created {new Date(generatedPersona.generated_at).toLocaleDateString()}
          </p>
        </div>

        {/* Main Persona Card */}
        {renderPersonaCard()}

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column */}
          <div>
            {/* Personality Traits */}
            {renderSection("Personality Profile", renderPersonalityTraits(), "🧠", "bg-blue-50")}
            
            {/* Goals & Motivations */}
            {renderSection("Goals & Motivations", renderListWithIcons(goals, 'var(--bcm-cyan)'), "🎯", "bg-cyan-50")}
            
            {/* Media Consumption */}
            {renderSection("Media Consumption", renderMediaConsumption(), "📱", "bg-green-50")}
          </div>

          {/* Right Column */}
          <div>
            {/* Pain Points */}
            {renderSection("Pain Points & Challenges", renderListWithIcons(pain_points, '#ef4444'), "⚠️", "bg-red-50")}
            
            {/* Marketing Recommendations */}
            {renderSection("Marketing Recommendations", renderListWithIcons(recommendations, 'var(--bcm-orange)'), "💡", "bg-orange-50")}
            
            {/* Engagement Metrics */}
            {renderSection("Engagement Metrics", renderEngagementMetrics(), "📊", "bg-purple-50")}
          </div>
        </div>

        {/* Communication Style */}
        <div className="bg-white rounded-lg p-6 shadow-lg border-l-4" style={{borderLeftColor: 'var(--bcm-orange)'}}>
          <h2 className="text-xl font-bold font-montserrat bcm-title mb-3">
            Recommended Communication Style
          </h2>
          <p className="text-gray-700 font-montserrat text-lg">
            {communication_style}
          </p>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500">
          <p className="font-montserrat">Generated by BCM VentasAI • Powered by Advanced AI Analytics</p>
        </div>
      </div>
    </div>
  );
};

export default VisualPersonaTemplate;
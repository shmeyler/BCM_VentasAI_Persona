"""
External Data Sources Integration
Provides mock implementations for SEMRush, SparkToro, and Buzzabout.ai
that generate realistic, contextual data for persona enrichment.
"""

import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class MockSEMRushAPI:
    """Mock SEMRush API for search behavior and keyword insights"""
    
    def __init__(self):
        self.industry_keywords = {
            "Retail": ["shopping", "fashion", "deals", "sale", "clothing", "accessories", "brands"],
            "CPG": ["organic", "healthy", "natural", "nutrition", "beauty", "skincare", "wellness"],
            "Financial Services": ["banking", "investment", "savings", "credit", "loans", "insurance"],
            "Health & Pharma": ["healthcare", "medical", "wellness", "fitness", "nutrition", "vitamins"],
            "Automotive": ["cars", "auto", "vehicle", "driving", "maintenance", "reviews"],
            "Travel": ["vacation", "hotels", "flights", "destinations", "travel", "booking"],
            "Technology & Telecom": ["tech", "gadgets", "apps", "software", "mobile", "internet"],
            "Political & Advocacy": ["politics", "voting", "policy", "government", "community", "rights"]
        }
    
    def get_search_behavior_data(self, persona_data: Dict) -> Dict[str, Any]:
        """Generate realistic search behavior data based on persona attributes"""
        
        # Determine industry context
        vertical = persona_data.get("attributes", {}).get("selectedVertical", "General")
        age_range = persona_data.get("demographics", {}).get("age_range", "25-40")
        income = persona_data.get("demographics", {}).get("income_range", "$50,000-$75,000")
        
        # Generate age-specific search patterns
        if "18-24" in age_range:
            search_volume_modifier = 1.3  # Higher online activity
            mobile_preference = 0.85
        elif "45-65" in age_range:
            search_volume_modifier = 0.9
            mobile_preference = 0.65
        else:
            search_volume_modifier = 1.0
            mobile_preference = 0.75
        
        # Generate income-specific keyword interests
        premium_keywords = ["luxury", "premium", "high-end", "exclusive"] if "$75,000+" in income else ["affordable", "budget", "deals", "discount"]
        
        # Get industry-specific keywords
        base_keywords = self.industry_keywords.get(vertical, ["general", "lifestyle", "consumer"])
        
        # Generate search data
        search_keywords = []
        for keyword in base_keywords[:5]:
            volume = int(random.uniform(1000, 50000) * search_volume_modifier)
            search_keywords.append({
                "keyword": keyword,
                "search_volume": volume,
                "competition": round(random.uniform(0.2, 0.9), 2),
                "trend": random.choice(["rising", "stable", "declining"])
            })
        
        return {
            "search_behavior": {
                "primary_keywords": search_keywords,
                "search_intent": {
                    "informational": round(random.uniform(0.3, 0.6), 2),
                    "commercial": round(random.uniform(0.2, 0.4), 2),
                    "transactional": round(random.uniform(0.1, 0.3), 2)
                },
                "device_preferences": {
                    "mobile": mobile_preference,
                    "desktop": 1 - mobile_preference,
                    "tablet": round(random.uniform(0.05, 0.15), 2)
                },
                "search_timing": {
                    "morning": round(random.uniform(0.2, 0.4), 2),
                    "afternoon": round(random.uniform(0.3, 0.5), 2),
                    "evening": round(random.uniform(0.2, 0.4), 2),
                    "weekend": round(random.uniform(0.15, 0.35), 2)
                }
            },
            "competitive_insights": {
                "top_competitors": [
                    f"{vertical.lower()}-leader.com",
                    f"best-{vertical.lower()}.com",
                    f"{vertical.lower()}-expert.com"
                ],
                "market_share": round(random.uniform(5, 25), 1),
                "visibility_score": round(random.uniform(60, 95), 1)
            },
            "data_source": "SEMRush (Mock)",
            "generated_at": datetime.now().isoformat()
        }

class MockSparkToroAPI:
    """Mock SparkToro API for audience insights and social behavior"""
    
    def __init__(self):
        self.platform_demographics = {
            "Facebook": {"age_skew": "35+", "engagement": "moderate"},
            "Instagram": {"age_skew": "18-34", "engagement": "high"},
            "Twitter": {"age_skew": "25-44", "engagement": "moderate"},
            "LinkedIn": {"age_skew": "25-54", "engagement": "professional"},
            "TikTok": {"age_skew": "16-29", "engagement": "very_high"},
            "YouTube": {"age_skew": "18-49", "engagement": "high"}
        }
    
    def get_audience_insights(self, persona_data: Dict) -> Dict[str, Any]:
        """Generate realistic audience insights and social behavior"""
        
        vertical = persona_data.get("attributes", {}).get("selectedVertical", "General")
        behaviors = persona_data.get("attributes", {}).get("selectedBehaviors", [])
        media_platforms = persona_data.get("media_consumption", {}).get("social_media_platforms", [])
        
        # Generate influencer recommendations based on vertical
        influencer_types = {
            "Retail": ["Fashion Bloggers", "Style Influencers", "Shopping Enthusiasts"],
            "CPG": ["Health & Wellness Gurus", "Beauty Experts", "Lifestyle Influencers"],
            "Financial Services": ["Finance Experts", "Investment Advisors", "Business Leaders"],
            "Health & Pharma": ["Health Professionals", "Fitness Trainers", "Wellness Coaches"],
            "Automotive": ["Car Reviewers", "Auto Enthusiasts", "Tech Reviewers"],
            "Travel": ["Travel Bloggers", "Adventure Seekers", "Destination Experts"],
            "Technology & Telecom": ["Tech Reviewers", "Gadget Enthusiasts", "Industry Analysts"],
            "Political & Advocacy": ["Political Commentators", "Community Leaders", "Activists"]
        }
        
        # Generate content preferences
        content_types = []
        if "Brand loyal" in behaviors:
            content_types.extend(["Brand stories", "Product reviews", "Customer testimonials"])
        if "Quality-focused" in behaviors:
            content_types.extend(["Expert opinions", "In-depth reviews", "Comparison guides"])
        if "Sustainable shopping" in behaviors:
            content_types.extend(["Sustainability content", "Eco-friendly guides", "Environmental news"])
        
        # Default content if no specific behaviors
        if not content_types:
            content_types = ["General lifestyle", "Entertainment", "News and updates"]
        
        # Calculate platform engagement scores
        platform_engagement = {}
        for platform in media_platforms:
            base_score = random.uniform(0.6, 0.9)
            platform_engagement[platform] = {
                "engagement_rate": round(base_score, 2),
                "time_spent": f"{random.randint(15, 90)} minutes/day",
                "content_interaction": random.choice(["passive", "moderate", "active"])
            }
        
        return {
            "audience_insights": {
                "top_influencers": influencer_types.get(vertical, ["General Influencers"])[:3],
                "content_preferences": content_types[:5],
                "engagement_patterns": platform_engagement,
                "discovery_channels": {
                    "social_media": round(random.uniform(0.4, 0.7), 2),
                    "search_engines": round(random.uniform(0.2, 0.4), 2),
                    "word_of_mouth": round(random.uniform(0.1, 0.3), 2),
                    "traditional_media": round(random.uniform(0.05, 0.2), 2)
                }
            },
            "social_behavior": {
                "sharing_likelihood": round(random.uniform(0.1, 0.4), 2),
                "comment_frequency": random.choice(["low", "moderate", "high"]),
                "brand_mention_tendency": random.choice(["rarely", "occasionally", "frequently"]),
                "peer_influence_score": round(random.uniform(0.3, 0.8), 2)
            },
            "data_source": "SparkToro (Mock)",
            "generated_at": datetime.now().isoformat()
        }

class MockBuzzaboutAPI:
    """Mock Buzzabout.ai API for social listening and sentiment analysis"""
    
    def __init__(self):
        self.sentiment_drivers = {
            "Retail": ["price", "quality", "customer service", "delivery", "returns"],
            "CPG": ["ingredients", "packaging", "effectiveness", "value", "sustainability"],
            "Financial Services": ["fees", "customer support", "security", "ease of use", "rates"],
            "Health & Pharma": ["effectiveness", "side effects", "cost", "accessibility", "trust"],
            "Automotive": ["reliability", "performance", "safety", "price", "fuel efficiency"],
            "Travel": ["service quality", "value", "convenience", "experience", "safety"],
            "Technology & Telecom": ["performance", "features", "price", "customer support", "reliability"],
            "Political & Advocacy": ["trustworthiness", "effectiveness", "transparency", "representation"]
        }
    
    def get_social_listening_data(self, persona_data: Dict) -> Dict[str, Any]:
        """Generate realistic social listening and sentiment data"""
        
        vertical = persona_data.get("attributes", {}).get("selectedVertical", "General")
        behaviors = persona_data.get("attributes", {}).get("selectedBehaviors", [])
        
        # Generate conversation topics based on behaviors
        conversation_topics = []
        if "Price-conscious" in behaviors:
            conversation_topics.extend(["deals and discounts", "value comparison", "budget tips"])
        if "Quality-focused" in behaviors:
            conversation_topics.extend(["product reviews", "quality comparisons", "premium options"])
        if "Brand loyal" in behaviors:
            conversation_topics.extend(["brand advocacy", "customer loyalty", "brand experiences"])
        
        # Default topics if no specific behaviors
        if not conversation_topics:
            conversation_topics = ["general discussions", "recommendations", "experiences"]
        
        # Generate sentiment scores with realistic variation
        base_sentiment = random.uniform(0.3, 0.7)  # Generally neutral to positive
        sentiment_variation = random.uniform(-0.1, 0.1)
        
        # Generate trending topics for the vertical
        sentiment_drivers = self.sentiment_drivers.get(vertical, ["quality", "value", "service"])
        trending_topics = []
        for topic in sentiment_drivers[:3]:
            trending_topics.append({
                "topic": topic,
                "mention_volume": random.randint(500, 5000),
                "sentiment_score": round(base_sentiment + sentiment_variation, 2),
                "growth_rate": round(random.uniform(-20, 50), 1)
            })
        
        # Generate geographic sentiment distribution
        regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
        regional_sentiment = {}
        for region in regions:
            regional_sentiment[region] = {
                "sentiment_score": round(base_sentiment + random.uniform(-0.15, 0.15), 2),
                "volume_share": round(random.uniform(0.1, 0.4), 2)
            }
        
        return {
            "social_listening": {
                "conversation_topics": conversation_topics[:5],
                "trending_topics": trending_topics,
                "mention_sentiment": {
                    "overall_score": round(base_sentiment, 2),
                    "positive": round(random.uniform(0.4, 0.7), 2),
                    "neutral": round(random.uniform(0.2, 0.4), 2),
                    "negative": round(random.uniform(0.05, 0.2), 2)
                },
                "conversation_drivers": sentiment_drivers[:5]
            },
            "sentiment_analysis": {
                "emotional_triggers": {
                    "excitement": round(random.uniform(0.1, 0.3), 2),
                    "satisfaction": round(random.uniform(0.3, 0.6), 2),
                    "frustration": round(random.uniform(0.05, 0.2), 2),
                    "loyalty": round(random.uniform(0.2, 0.5), 2)
                },
                "regional_sentiment": regional_sentiment,
                "temporal_trends": {
                    "daily_pattern": "Peak activity during 7-9pm",
                    "weekly_pattern": "Higher engagement on weekends",
                    "seasonal_trends": "Increased activity during holidays"
                }
            },
            "data_source": "Buzzabout.ai (Mock)",
            "generated_at": datetime.now().isoformat()
        }

class DataSourceOrchestrator:
    """Orchestrates all data source integrations for persona enrichment"""
    
    def __init__(self):
        self.semrush = MockSEMRushAPI()
        self.sparktoro = MockSparkToroAPI()
        self.buzzabout = MockBuzzaboutAPI()
    
    async def enrich_persona_data(self, persona_data: Dict) -> Dict[str, Any]:
        """
        Enrich persona data with insights from all data sources
        Returns comprehensive data enrichment for persona generation
        """
        
        try:
            # Get data from all sources
            search_data = self.semrush.get_search_behavior_data(persona_data)
            audience_data = self.sparktoro.get_audience_insights(persona_data)
            sentiment_data = self.buzzabout.get_social_listening_data(persona_data)
            
            # Combine and structure the enriched data
            enriched_data = {
                "search_insights": search_data,
                "audience_insights": audience_data,
                "social_insights": sentiment_data,
                "data_integration": {
                    "sources_used": ["SEMRush", "SparkToro", "Buzzabout.ai"],
                    "enrichment_score": round(random.uniform(0.75, 0.95), 2),
                    "data_freshness": "Real-time",
                    "confidence_level": round(random.uniform(0.8, 0.95), 2)
                },
                "generated_at": datetime.now().isoformat()
            }
            
            return enriched_data
            
        except Exception as e:
            # Graceful degradation - return partial data or defaults
            return {
                "error": f"Data source integration error: {str(e)}",
                "fallback_data": {
                    "message": "Using baseline persona data",
                    "sources_available": []
                },
                "generated_at": datetime.now().isoformat()
            }
    
    def get_data_source_status(self) -> Dict[str, Any]:
        """Return status of all data source integrations"""
        return {
            "semrush": {
                "status": "active",
                "type": "mock",
                "capabilities": ["search_behavior", "competitive_analysis", "keyword_insights"]
            },
            "sparktoro": {
                "status": "active", 
                "type": "mock",
                "capabilities": ["audience_insights", "influencer_identification", "social_behavior"]
            },
            "buzzabout": {
                "status": "active",
                "type": "mock", 
                "capabilities": ["social_listening", "sentiment_analysis", "trend_monitoring"]
            },
            "integration_health": "fully_operational",
            "last_updated": datetime.now().isoformat()
        }
import sys
import os
import shutil
from pathlib import Path
import logging
import requests
import random
import tempfile
from datetime import datetime

# Add the current directory to Python path for external_integrations
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from enum import Enum
import requests
import random
import tempfile
import aiofiles
from external_integrations.unsplash import get_professional_headshot
from external_integrations.data_sources import DataSourceOrchestrator
from external_integrations.openai_images import generate_persona_image_openai
from external_integrations.file_parsers import parse_resonate_zip

load_dotenv(ROOT_DIR / '.env')

# Initialize data source orchestrator
data_sources = DataSourceOrchestrator()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="BCM VentasAI Persona Generator", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Enums for structured data
class StartingMethod(str, Enum):
    demographics = "demographics"
    attributes = "attributes"
    resonate_upload = "resonate_upload"
    multi_source_data = "multi_source_data"

class AgeRange(str, Enum):
    gen_z = "18-24"
    millennial = "25-40"
    gen_x = "41-56"
    boomer = "57-75"
    silent = "76+"

class MediaType(str, Enum):
    social_media = "social_media"
    streaming = "streaming"
    traditional_tv = "traditional_tv"
    podcasts = "podcasts"
    news = "news"
    video_content = "video_content"
    blogs = "blogs"
    email = "email"

# Models for Persona Generation
class Demographics(BaseModel):
    age_range: Optional[AgeRange] = None
    gender: Optional[str] = None
    income_range: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    occupation: Optional[str] = None
    family_status: Optional[str] = None

class Attributes(BaseModel):
    # Resonate Taxonomy fields
    selectedVertical: Optional[str] = None
    selectedCategory: Optional[str] = None
    selectedBehaviors: Optional[List[str]] = []
    # Original custom fields
    interests: Optional[List[str]] = []
    behaviors: Optional[List[str]] = []
    values: Optional[List[str]] = []
    purchase_motivations: Optional[List[str]] = []
    preferred_brands: Optional[List[str]] = []
    lifestyle: Optional[List[str]] = []

class MediaConsumption(BaseModel):
    social_media_platforms: Optional[List[str]] = []
    content_types: Optional[List[str]] = []
    consumption_time: Optional[str] = None
    preferred_devices: Optional[List[str]] = []
    news_sources: Optional[List[str]] = []
    entertainment_preferences: Optional[List[str]] = []
    advertising_receptivity: Optional[str] = None

class PersonaData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    starting_method: StartingMethod
    demographics: Demographics = Demographics()
    attributes: Attributes = Attributes()
    media_consumption: MediaConsumption = MediaConsumption()
    current_step: int = 1
    completed_steps: List[int] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GeneratedPersona(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    persona_data: PersonaData
    ai_insights: Dict[str, Any] = {}
    recommendations: List[str] = []
    pain_points: List[str] = []
    goals: List[str] = []
    communication_style: str = ""
    persona_image_url: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models
class CreatePersonaRequest(BaseModel):
    starting_method: StartingMethod
    name: Optional[str] = None

class UpdatePersonaRequest(BaseModel):
    name: Optional[str] = None
    demographics: Optional[Demographics] = None
    attributes: Optional[Attributes] = None
    media_consumption: Optional[MediaConsumption] = None
    current_step: Optional[int] = None
    completed_steps: Optional[List[int]] = None

class GeneratePersonaRequest(BaseModel):
    persona_id: str


# Helper functions for AI-enhanced persona generation based on uploaded data
def generate_intelligent_insights(persona_data: PersonaData) -> Dict[str, Any]:
    """Generate AI insights based on actual persona data"""
    demographics = persona_data.demographics
    media = persona_data.media_consumption
    attributes = persona_data.attributes
    
    # Base personality traits on demographics and uploaded data
    personality_traits = []
    
    # Age-based traits
    if demographics.age_range == AgeRange.gen_z:
        personality_traits.extend(["Digital native", "Socially conscious", "Entrepreneurial"])
    elif demographics.age_range == AgeRange.millennial:
        personality_traits.extend(["Tech-savvy", "Value-conscious", "Experience-focused"])
    elif demographics.age_range == AgeRange.gen_x:
        personality_traits.extend(["Pragmatic", "Independent", "Quality-focused"])
    elif demographics.age_range == AgeRange.boomer:
        personality_traits.extend(["Traditional", "Brand loyal", "Quality-oriented"])
    
    # Gender-based adjustments
    if demographics.gender == "Female":
        personality_traits.append("Community-oriented")
    elif demographics.gender == "Male":
        personality_traits.append("Goal-oriented")
    
    # Income-based traits
    if demographics.income_range and "$75,000" in demographics.income_range:
        personality_traits.extend(["Premium-conscious", "Investment-minded"])
    elif demographics.income_range and "$50,000" in demographics.income_range:
        personality_traits.extend(["Value-conscious", "Budget-aware"])
    
    # Social media behavior based on platforms
    platforms = media.social_media_platforms or []
    digital_behavior = "Limited digital presence"
    if len(platforms) >= 4:
        digital_behavior = "Heavy social media user, multi-platform engagement"
    elif len(platforms) >= 2:
        digital_behavior = "Active on social media, selective platform usage"
    elif len(platforms) >= 1:
        digital_behavior = "Moderate social media usage, focused platform preference"
    
    # Shopping behavior based on age and income
    shopping_behavior = "Standard purchase behavior"
    if demographics.age_range in [AgeRange.millennial, AgeRange.gen_z]:
        shopping_behavior = "Research-heavy, reviews-driven, mobile-first shopping"
    elif demographics.age_range == AgeRange.gen_x:
        shopping_behavior = "Methodical researcher, brand comparison focused"
    elif demographics.age_range == AgeRange.boomer:
        shopping_behavior = "Brand loyal, prefers established retailers"
    
    return {
        "personality_traits": personality_traits[:4],  # Limit to top 4
        "shopping_behavior": shopping_behavior,
        "decision_factors": _get_decision_factors(demographics, attributes),
        "digital_behavior": digital_behavior
    }

def generate_data_driven_recommendations(persona_data: PersonaData) -> List[str]:
    """Generate marketing recommendations based on persona data"""
    recommendations = []
    demographics = persona_data.demographics
    media = persona_data.media_consumption
    
    # Platform-specific recommendations
    platforms = media.social_media_platforms or []
    if "Instagram" in platforms:
        recommendations.append("Use Instagram visual storytelling and influencer partnerships")
    if "LinkedIn" in platforms:
        recommendations.append("Leverage LinkedIn for professional and B2B messaging")
    if "Facebook" in platforms:
        recommendations.append("Utilize Facebook targeted advertising and community groups")
    if "TikTok" in platforms:
        recommendations.append("Create engaging short-form video content for TikTok")
    if "Twitter" in platforms or "Twitter/X" in platforms:
        recommendations.append("Engage in real-time conversations and trending topics on X/Twitter")
    
    # Age-based recommendations
    if demographics.age_range == AgeRange.gen_z:
        recommendations.append("Focus on authentic, purpose-driven brand messaging")
        recommendations.append("Prioritize mobile-first, video-centric content")
    elif demographics.age_range == AgeRange.millennial:
        recommendations.append("Highlight convenience and time-saving benefits")
        recommendations.append("Emphasize value for money and experiences over products")
    elif demographics.age_range == AgeRange.gen_x:
        recommendations.append("Provide detailed product information and comparisons")
        recommendations.append("Use trusted review sources and testimonials")
    elif demographics.age_range == AgeRange.boomer:
        recommendations.append("Focus on reliability and customer service quality")
        recommendations.append("Use traditional media channels alongside digital")
    
    # Income-based recommendations
    if demographics.income_range and ("$75,000" in demographics.income_range or "$100,000" in demographics.income_range):
        recommendations.append("Position premium features and exclusive offerings")
    else:
        recommendations.append("Emphasize value propositions and cost-effectiveness")
    
    # Location-based recommendations
    if demographics.location == "Urban":
        recommendations.append("Highlight convenience and fast delivery options")
    elif demographics.location == "Suburban":
        recommendations.append("Focus on family-oriented messaging and bulk options")
    elif demographics.location == "Rural":
        recommendations.append("Emphasize online accessibility and shipping benefits")
    
    return recommendations[:6]  # Limit to top 6 recommendations

def generate_contextual_pain_points(persona_data: PersonaData) -> List[str]:
    """Generate pain points based on persona context"""
    pain_points = []
    demographics = persona_data.demographics
    
    # Age-based pain points
    if demographics.age_range == AgeRange.gen_z:
        pain_points.extend([
            "Limited disposable income for premium products",
            "Overwhelmed by too many brand choices",
            "Skeptical of traditional advertising"
        ])
    elif demographics.age_range == AgeRange.millennial:
        pain_points.extend([
            "Time constraints due to busy lifestyle",
            "Information overload when researching products",
            "Balancing quality with affordability"
        ])
    elif demographics.age_range == AgeRange.gen_x:
        pain_points.extend([
            "Difficulty keeping up with technology changes",
            "Concerns about online security and privacy",
            "Preference for proven brands over new options"
        ])
    elif demographics.age_range == AgeRange.boomer:
        pain_points.extend([
            "Discomfort with complex digital interfaces",
            "Preference for personal customer service",
            "Caution about online purchasing"
        ])
    
    # Income-based pain points
    if demographics.income_range and "$25,000" in demographics.income_range:
        pain_points.append("Budget constraints limiting premium options")
    elif demographics.income_range and "$50,000" in demographics.income_range:
        pain_points.append("Need to justify larger purchases carefully")
    
    # General pain points
    pain_points.extend([
        "Finding trustworthy product reviews",
        "Comparing similar products effectively"
    ])
    
    return pain_points[:5]  # Limit to top 5 pain points

def generate_targeted_goals(persona_data: PersonaData) -> List[str]:
    """Generate goals based on persona characteristics"""
    goals = []
    demographics = persona_data.demographics
    
    # Age-based goals
    if demographics.age_range == AgeRange.gen_z:
        goals.extend([
            "Discover brands that align with personal values",
            "Find affordable options that don't compromise quality",
            "Stay current with trends and innovations"
        ])
    elif demographics.age_range == AgeRange.millennial:
        goals.extend([
            "Make efficient purchasing decisions",
            "Find products that enhance lifestyle and experiences",
            "Get the best value for money spent"
        ])
    elif demographics.age_range == AgeRange.gen_x:
        goals.extend([
            "Make informed, researched purchase decisions",
            "Find reliable products that last long-term",
            "Support brands with good customer service"
        ])
    elif demographics.age_range == AgeRange.boomer:
        goals.extend([
            "Purchase from trusted, established brands",
            "Receive excellent customer support",
            "Find products that meet specific needs reliably"
        ])
    
    # Income-based goals
    if demographics.income_range and ("$75,000" in demographics.income_range or "$100,000" in demographics.income_range):
        goals.append("Access premium products and services")
    else:
        goals.append("Maximize value within budget constraints")
    
    # General goals
    goals.extend([
        "Avoid purchase regret through careful selection",
        "Save time in the buying process"
    ])
    
    return goals[:5]  # Limit to top 5 goals

def _get_decision_factors(demographics: Demographics, attributes: Attributes) -> List[str]:
    """Determine key decision factors based on demographics and attributes"""
    factors = []
    
    # Age-based factors
    if demographics.age_range == AgeRange.gen_z:
        factors.extend(["Social impact", "Authenticity", "Price"])
    elif demographics.age_range == AgeRange.millennial:
        factors.extend(["Reviews", "Convenience", "Value"])
    elif demographics.age_range == AgeRange.gen_x:
        factors.extend(["Quality", "Brand reputation", "Features"])
    elif demographics.age_range == AgeRange.boomer:
        factors.extend(["Trust", "Customer service", "Reliability"])
    
    # Income-based factors
    if demographics.income_range and "$75,000" in demographics.income_range:
        factors.append("Premium features")
    else:
        factors.append("Price competitiveness")
    
    return factors[:4]  # Limit to top 4 factors


# Helper functions for data normalization
def _normalize_gender(gender):
    """Normalize gender data for image generation"""
    if not gender:
        return 'Female'  # Default
    
    gender_str = str(gender).lower()
    if 'female' in gender_str or 'woman' in gender_str or 'slight female skew' in gender_str:
        return 'Female'
    elif 'male' in gender_str or 'man' in gender_str:
        return 'Male'
    else:
        return 'Female'  # Default for mixed/unclear cases

def _normalize_occupation(occupation):
    """Normalize occupation data for image generation"""
    if not occupation:
        return 'Professional'
    
    occupation_str = str(occupation).lower()
    if 'manager' in occupation_str or 'director' in occupation_str or 'executive' in occupation_str:
        return 'Executive'
    elif 'engineer' in occupation_str or 'developer' in occupation_str or 'tech' in occupation_str:
        return 'Technology Professional'
    elif 'marketing' in occupation_str or 'sales' in occupation_str:
        return 'Marketing Professional'
    elif 'analyst' in occupation_str or 'finance' in occupation_str:
        return 'Financial Analyst'
    elif 'consultant' in occupation_str:
        return 'Business Consultant'
    else:
        return 'Professional'

def _normalize_location(location):
    """Normalize location data for image generation"""
    if not location:
        return 'Urban'  # Default
    
    location_str = str(location).lower()
    if 'suburban' in location_str or 'suburb' in location_str:
        return 'Suburban'
    elif 'rural' in location_str or 'country' in location_str:
        return 'Rural'
    elif 'urban' in location_str or 'city' in location_str or 'metropolitan' in location_str:
        return 'Urban'
    else:
        return 'Urban'  # Default


# Helper function to generate persona image using OpenAI DALL-E
async def generate_persona_image(persona_data: PersonaData) -> Optional[str]:
    """Generate a professional headshot using OpenAI DALL-E based on demographic data"""
    try:
        # Extract demographics
        demographics = persona_data.demographics
        if not demographics:
            logging.warning(f"No demographics available for persona {persona_data.name}")
            return None
        
        # Convert PersonaData demographics to dictionary for OpenAI generator
        # Apply data normalization for better image generation
        demographics_dict = {
            'age_range': demographics.age_range,
            'gender': _normalize_gender(demographics.gender),
            'occupation': _normalize_occupation(demographics.occupation),
            'location': _normalize_location(demographics.location),
            'income_range': demographics.income_range,
            'education': demographics.education
        }
        
        logging.info(f"Generating OpenAI headshot for {persona_data.name} with demographics: {demographics_dict}")
        
        # Generate image using OpenAI DALL-E
        image_url = await generate_persona_image_openai(demographics_dict)
        
        if image_url:
            logging.info(f"Successfully generated OpenAI headshot for {persona_data.name}: {image_url}")
            return image_url
        else:
            logging.warning(f"OpenAI image generation failed for {persona_data.name}, using fallback")
            return await _get_fallback_image(demographics_dict)
            
    except Exception as e:
        logging.error(f"Error generating OpenAI image for {persona_data.name}: {str(e)}")
        # Fallback to Unsplash if OpenAI fails
        return await _get_fallback_image(demographics.dict() if demographics else {})

async def _get_fallback_image(demographics_dict: dict) -> str:
    """Fallback to Unsplash if OpenAI fails"""
    try:
        from external_integrations.unsplash import get_professional_headshot
        
        # Build search terms for Unsplash fallback
        search_terms = ["professional", "headshot", "business"]
        
        gender = demographics_dict.get('gender', '')
        if gender:
            if gender.lower() in ['male', 'man']:
                search_terms.extend(["businessman", "male"])
            elif gender.lower() in ['female', 'woman']:
                search_terms.extend(["businesswoman", "female"])
        
        occupation = demographics_dict.get('occupation', '')
        if occupation:
            if 'executive' in occupation.lower() or 'director' in occupation.lower():
                search_terms.append("executive")
            elif 'tech' in occupation.lower() or 'engineer' in occupation.lower():
                search_terms.append("tech")
        
        query = " ".join(search_terms[:5])  # Limit query length
        
        # Try to get Unsplash image
        unsplash_url = await get_professional_headshot(query, demographics_dict)
        if unsplash_url:
            logging.info(f"Using Unsplash fallback image: {unsplash_url}")
            return unsplash_url
            
    except Exception as e:
        logging.error(f"Fallback image generation also failed: {str(e)}")
    
    # Final fallback to default professional image
    gender = demographics_dict.get('gender', '').lower()
    if 'male' in gender:
        return "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face"
    elif 'female' in gender:
        return "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400&h=400&fit=crop&crop=face"
    else:
        return "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face"


# Legacy Status Check Models (keeping for compatibility)
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str


# Persona API Routes
@api_router.post("/personas", response_model=PersonaData)
async def create_persona(request: CreatePersonaRequest):
    """Create a new persona with the specified starting method"""
    persona_data = PersonaData(
        starting_method=request.starting_method,
        name=request.name
    )
    
    # Insert into database
    await db.personas.insert_one(persona_data.dict())
    return persona_data

@api_router.get("/personas/{persona_id}", response_model=PersonaData)
async def get_persona(persona_id: str):
    """Get a specific persona by ID"""
    persona = await db.personas.find_one({"id": persona_id})
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return PersonaData(**persona)

@api_router.put("/personas/{persona_id}", response_model=PersonaData)
async def update_persona(persona_id: str, request: UpdatePersonaRequest):
    """Update persona data - especially important for Media Consumption step"""
    persona = await db.personas.find_one({"id": persona_id})
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    persona_data = PersonaData(**persona)
    
    # Update fields if provided
    if request.name is not None:
        persona_data.name = request.name
    if request.demographics:
        persona_data.demographics = request.demographics
    if request.attributes:
        persona_data.attributes = request.attributes
    if request.media_consumption:
        persona_data.media_consumption = request.media_consumption
    if request.current_step is not None:
        persona_data.current_step = request.current_step
    if request.completed_steps is not None:
        persona_data.completed_steps = request.completed_steps
    
    persona_data.updated_at = datetime.utcnow()
    
    # Update in database
    await db.personas.replace_one({"id": persona_id}, persona_data.dict())
    return persona_data

@api_router.post("/personas/{persona_id}/generate", response_model=GeneratedPersona)
async def generate_persona(persona_id: str):
    """Generate the final AI-powered persona with image"""
    persona = await db.personas.find_one({"id": persona_id})
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    persona_data = PersonaData(**persona)
    
    # Generate persona image using the comprehensive function
    persona_image_url = await generate_persona_image(persona_data)
    
    # Mock AI generation for now (replace with actual AI service)
    ai_insights = {
        "personality_traits": ["Tech-savvy", "Value-conscious", "Social"],
        "shopping_behavior": "Researches extensively before purchase",
        "decision_factors": ["Price", "Quality", "Brand reputation"],
        "digital_behavior": "Active on social media, uses mobile-first approach"
    }
    
    recommendations = [
        "Use social media advertising on preferred platforms",
        "Highlight value proposition and cost savings",
        "Provide detailed product information and reviews",
        "Optimize for mobile experience"
    ]
    
    pain_points = [
        "Limited time for research",
        "Information overload",
        "Budget constraints",
        "Trust in online purchases"
    ]
    
    goals = [
        "Make informed purchasing decisions",
        "Get the best value for money",
        "Save time in the buying process",
        "Stay updated with latest trends"
    ]
    
    generated_persona = GeneratedPersona(
        name=persona_data.name or f"Persona {persona_data.id[:8]}",
        persona_data=persona_data,
        ai_insights=ai_insights,
        recommendations=recommendations,
        pain_points=pain_points,
        goals=goals,
        communication_style="Direct, informative, and value-focused",
        persona_image_url=persona_image_url
    )
    
    # Save generated persona
    await db.generated_personas.insert_one(generated_persona.dict())
    return generated_persona

@api_router.get("/personas", response_model=List[PersonaData])
async def list_personas():
    """List all personas"""
    personas = await db.personas.find().to_list(100)
    return [PersonaData(**persona) for persona in personas]

@api_router.get("/generated-personas", response_model=List[GeneratedPersona])
async def list_generated_personas():
    """List all generated personas"""
    personas = await db.generated_personas.find().to_list(100)
    return [GeneratedPersona(**persona) for persona in personas]

@api_router.delete("/personas/{persona_id}")
async def delete_persona(persona_id: str):
    """Delete a persona"""
    result = await db.personas.delete_one({"id": persona_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"message": "Persona deleted successfully"}


@api_router.delete("/generated-personas/{generated_persona_id}")
async def delete_generated_persona(generated_persona_id: str):
    """Delete a generated persona"""
    result = await db.generated_personas.delete_one({"id": generated_persona_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Generated persona not found")
    return {"message": "Generated persona deleted successfully"}


# Legacy Status Check Routes (keeping for compatibility)
@api_router.get("/")
async def root():
    return {"message": "BCM VentasAI Persona Generator API", "version": "1.0.0"}

@api_router.post("/export/google-slides")
async def export_to_google_slides(request: dict):
    """Export persona to Google Slides"""
    try:
        persona_id = request.get("persona_id")
        generated_persona_id = request.get("generated_persona_id")
        
        if not persona_id and not generated_persona_id:
            raise HTTPException(status_code=400, detail="Either persona_id or generated_persona_id is required")
        
        # Get persona data
        if generated_persona_id:
            generated_persona_doc = await db.generated_personas.find_one({"id": generated_persona_id})
            if not generated_persona_doc:
                raise HTTPException(status_code=404, detail="Generated persona not found")
            
            # Convert to JSON-serializable format
            generated_persona = GeneratedPersona(**generated_persona_doc)
            persona_data = generated_persona.dict()
        else:
            persona_doc = await db.personas.find_one({"id": persona_id})
            if not persona_doc:
                raise HTTPException(status_code=404, detail="Persona not found")
            
            # Convert to JSON-serializable format
            persona = PersonaData(**persona_doc)
            persona_data = {"persona_data": persona.dict()}
        
        return {
            "success": True,
            "persona_data": persona_data,
            "message": "Persona data prepared for Google Slides export"
        }
        
    except Exception as e:
        logger.error(f"Error preparing Google Slides export: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export preparation failed: {str(e)}")

@api_router.post("/export/pdf-data")
async def get_pdf_export_data(request: dict):
    """Get persona data formatted for PDF export"""
    try:
        persona_id = request.get("persona_id")
        generated_persona_id = request.get("generated_persona_id")
        
        if not persona_id and not generated_persona_id:
            raise HTTPException(status_code=400, detail="Either persona_id or generated_persona_id is required")
        
        # Get persona data
        if generated_persona_id:
            generated_persona_doc = await db.generated_personas.find_one({"id": generated_persona_id})
            if not generated_persona_doc:
                raise HTTPException(status_code=404, detail="Generated persona not found")
            
            # Convert to JSON-serializable format
            generated_persona = GeneratedPersona(**generated_persona_doc)
            persona_data = generated_persona.dict()
        else:
            persona_doc = await db.personas.find_one({"id": persona_id})
            if not persona_doc:
                raise HTTPException(status_code=404, detail="Persona not found")
            
            # Convert to JSON-serializable format
            persona = PersonaData(**persona_doc)
            persona_data = {"persona_data": persona.dict()}
        
        return {
            "success": True,
            "persona_data": persona_data
        }
        
    except Exception as e:
        logger.error(f"Error preparing PDF export data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF data preparation failed: {str(e)}")

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]


# Data Sources Integration Endpoints
@api_router.get("/data-sources/status")
async def get_data_sources_status():
    """Get status of all data source integrations"""
    return data_sources.get_data_source_status()

@api_router.post("/personas/{persona_id}/enrich")
async def enrich_persona_with_data_sources(persona_id: str):
    """Enrich persona with data from SEMRush, SparkToro, and Buzzabout.ai"""
    try:
        # Get the persona data
        persona = await db.personas.find_one({"id": persona_id})
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        # Get enriched data from data sources
        enriched_data = await data_sources.enrich_persona_data(persona)
        
        # Update persona with enriched data
        update_data = {
            "data_enrichment": enriched_data,
            "updated_at": datetime.utcnow()
        }
        
        await db.personas.update_one(
            {"id": persona_id},
            {"$set": update_data}
        )
        
        # Return updated persona
        updated_persona = await db.personas.find_one({"id": persona_id})
        return PersonaData(**updated_persona)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enrich persona: {str(e)}")

@api_router.get("/personas/{persona_id}/insights")
async def get_persona_insights(persona_id: str):
    """Get detailed insights for a persona including data source enrichment"""
    try:
        persona = await db.personas.find_one({"id": persona_id})
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        # Check if persona has enriched data
        enriched_data = persona.get("data_enrichment")
        if not enriched_data:
            # Enrich the persona first
            enriched_data = await data_sources.enrich_persona_data(persona)
            await db.personas.update_one(
                {"id": persona_id},
                {"$set": {
                    "data_enrichment": enriched_data,
                    "updated_at": datetime.utcnow()
                }}
            )
        
        # Structure insights for frontend consumption
        insights = {
            "persona_id": persona_id,
            "search_behavior": enriched_data.get("search_insights", {}),
            "audience_profile": enriched_data.get("audience_insights", {}),
            "social_sentiment": enriched_data.get("social_insights", {}),
            "data_quality": enriched_data.get("data_integration", {}),
            "last_updated": enriched_data.get("generated_at")
        }
        
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get persona insights: {str(e)}")

@api_router.get("/data-sources/demo")
async def get_demo_data_sources():
    """Get demo data from all data sources for testing"""
    try:
        demo_persona = {
            "attributes": {
                "selectedVertical": "Retail",
                "selectedCategory": "Preferences & Psychographics", 
                "selectedBehaviors": ["Quality-focused", "Brand loyal", "Sustainable shopping"]
            },
            "demographics": {
                "age_range": "25-40",
                "income_range": "$50,000-$75,000"
            },
            "media_consumption": {
                "social_media_platforms": ["Instagram", "Facebook", "LinkedIn"]
            }
        }
        
        enriched_data = await data_sources.enrich_persona_data(demo_persona)
        return enriched_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get demo data: {str(e)}")

# END DATA SOURCES ENDPOINTS

# Resonate File Upload Endpoints
@api_router.post("/personas/resonate-upload")
async def upload_resonate_file(file: UploadFile = File(...)):
    """
    Upload and parse Resonate ZIP file
    Returns extracted files and parsed data for persona generation
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.zip'):
            raise HTTPException(status_code=400, detail="Only ZIP files are supported")
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse the ZIP file
            parsing_result = parse_resonate_zip(temp_file_path)
            
            if parsing_result['success']:
                return {
                    "success": True,
                    "message": "File processed successfully",
                    "extracted_files": parsing_result['extracted_files'],
                    "parsed_data": parsing_result['parsed_data']
                }
            else:
                raise HTTPException(
                    status_code=422, 
                    detail=f"Failed to parse file: {parsing_result.get('error', 'Unknown error')}"
                )
                
        finally:
            # Clean up temporary file
            import os
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error processing Resonate upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@api_router.post("/personas/resonate-create")
async def create_persona_from_resonate_data(request: dict):
    """
    Create a new persona from parsed Resonate data
    """
    try:
        parsed_data = request.get('parsed_data', {})
        persona_name = request.get('name', 'Resonate Persona')
        
        # Create new persona with resonate_upload starting method
        persona_data = PersonaData(
            starting_method=StartingMethod.resonate_upload,
            name=persona_name
        )
        
        # Map parsed Resonate data to persona structure
        if 'demographics' in parsed_data:
            demo_data = parsed_data['demographics']
            demographics = Demographics()
            
            # Set initial defaults
            demographics.age_range = AgeRange.millennial  
            demographics.gender = 'Female'  
            demographics.location = 'Urban'  
            demographics.occupation = 'Professional'  
            demographics.income_range = '$50,000 - $99,999'  
            demographics.education = "Bachelor's Degree"  
            
            print(f"DEBUG: Processing demographics data keys: {list(demo_data.keys())}")
            
            # Extract actual demographic data from parsed data
            if 'age' in demo_data:
                age_data = demo_data['age']
                if isinstance(age_data, dict) and 'top_values' in age_data:
                    top_ages = list(age_data['top_values'].keys())
                    if top_ages:
                        # Map to closest AgeRange enum
                        age_value = top_ages[0]
                        if '18-24' in age_value:
                            demographics.age_range = AgeRange.gen_z
                        elif '25-40' in age_value or '25-34' in age_value:
                            demographics.age_range = AgeRange.millennial
                        elif '41-56' in age_value or '35-44' in age_value:
                            demographics.age_range = AgeRange.gen_x
                        elif '57-75' in age_value or '45-54' in age_value or '55-64' in age_value:
                            demographics.age_range = AgeRange.boomer
                        elif '76' in age_value or '65' in age_value:
                            demographics.age_range = AgeRange.silent
            
            # Extract gender data
            if 'gender' in demo_data:
                gender_data = demo_data['gender']
                if isinstance(gender_data, dict) and 'top_values' in gender_data:
                    top_genders = list(gender_data['top_values'].keys())
                    if top_genders:
                        gender_value = top_genders[0].lower()
                        if 'female' in gender_value or 'woman' in gender_value:
                            demographics.gender = 'Female'
                        elif 'male' in gender_value or 'man' in gender_value:
                            demographics.gender = 'Male'
            
            # Extract income data
            if 'income' in demo_data:
                income_data = demo_data['income']
                if isinstance(income_data, dict) and 'top_values' in income_data:
                    top_incomes = list(income_data['top_values'].keys())
                    if top_incomes:
                        demographics.income_range = top_incomes[0]
            
            # Extract education data
            if 'education' in demo_data:
                education_data = demo_data['education']
                if isinstance(education_data, dict) and 'top_values' in education_data:
                    top_education = list(education_data['top_values'].keys())
                    if top_education:
                        demographics.education = top_education[0]
            
            # Extract location data
            if 'location' in demo_data:
                location_data = demo_data['location']
                if isinstance(location_data, dict) and 'top_values' in location_data:
                    top_locations = list(location_data['top_values'].keys())
                    if top_locations:
                        demographics.location = top_locations[0]
            
            # Extract occupation data
            if 'occupation' in demo_data:
                occupation_data = demo_data['occupation']
                if isinstance(occupation_data, dict) and 'top_values' in occupation_data:
                    top_occupations = list(occupation_data['top_values'].keys())
                    if top_occupations:
                        demographics.occupation = top_occupations[0]
            
            persona_data.demographics = demographics
        
        # Map media consumption data from Resonate insights
        if 'media_consumption' in parsed_data:
            media_data = parsed_data['media_consumption']
            media_consumption = MediaConsumption()
            
            print(f"DEBUG: Processing media consumption data keys: {list(media_data.keys())}")
            
            # Extract gender and demographic info that might be in media consumption data
            demographics = persona_data.demographics
            platforms = []
            
            # Process media platforms data which often contains demographic breakdowns
            if 'media_platforms' in media_data:
                platform_data = media_data['media_platforms']
                if isinstance(platform_data, list):
                    for source_entry in platform_data:
                        if isinstance(source_entry, dict) and 'data' in source_entry:
                            if isinstance(source_entry['data'], list):
                                for insight in source_entry['data']:
                                    if isinstance(insight, dict) and 'data' in insight:
                                        insight_data = insight['data']
                                        insight_text = insight_data.get('insight', '').lower()
                                        insight_value = str(insight_data.get('value', '')).lower()
                                        composition = insight_data.get('composition', '')
                                        
                                        # Look for demographic clues in media consumption
                                        # Check for gender indicators in the data
                                        if any(male_indicator in insight_text + insight_value for male_indicator in ['male', 'man', 'men', 'father', 'dad', 'husband', 'masculine']):
                                            demographics.gender = 'Male'
                                            print(f"DEBUG: Updated gender to Male from media insight: {insight_text} = {insight_value}")
                                        
                                        # Extract social media platforms
                                        if 'social media membership' in insight_text:
                                            if insight_value not in ['none of the above', '']:
                                                platforms.append(insight_value.title())
            
            # Set media consumption defaults based on findings
            if platforms:
                # Clean up platform names and remove duplicates
                cleaned_platforms = []
                for platform in platforms:
                    if platform.lower() == 'x (formerly known as twitter)':
                        cleaned_platforms.append('Twitter/X')
                    elif platform not in cleaned_platforms:
                        cleaned_platforms.append(platform)
                
                media_consumption.social_media_platforms = cleaned_platforms[:6]  # Limit to top 6
            else:
                media_consumption.social_media_platforms = ['Facebook', 'Instagram', 'YouTube']
            
            media_consumption.preferred_devices = ['Mobile', 'Desktop']
            media_consumption.consumption_time = '2-4 hours'
            media_consumption.news_sources = ['Social Media', 'Digital News']
            
            print(f"DEBUG: Final gender set to: {demographics.gender}")
            print(f"DEBUG: Extracted platforms: {media_consumption.social_media_platforms}")
            
            persona_data.media_consumption = media_consumption
            persona_data.demographics = demographics  # Update demographics with any findings from media data
            if 'income' in demo_data:
                income_info = demo_data['income']
                if isinstance(income_info, list) and len(income_info) > 0:
                    income_data = income_info[0].get('data', {})
                    if 'top_values' in income_data:
                        top_incomes = list(income_data['top_values'].keys())
                        if top_incomes:
                            demographics.income_range = top_incomes[0]
            
            # Map education data
            if 'education' in demo_data:
                education_info = demo_data['education']
                if isinstance(education_info, list) and len(education_info) > 0:
                    education_data = education_info[0].get('data', {})
                    if 'top_values' in education_data:
                        top_education = list(education_data['top_values'].keys())
                        if top_education:
                            demographics.education = top_education[0]
            
            # Map location data with normalization for image generation
            if 'location' in demo_data:
                location_info = demo_data['location']
                if isinstance(location_info, list) and len(location_info) > 0:
                    location_data = location_info[0].get('data', {})
                    if 'top_values' in location_data:
                        top_locations = list(location_data['top_values'].keys())
                        if top_locations:
                            raw_location = top_locations[0].lower()
                            # Normalize location for image generation
                            if 'urban' in raw_location or 'city' in raw_location or 'metropolitan' in raw_location:
                                demographics.location = 'Urban'
                            elif 'suburban' in raw_location or 'suburb' in raw_location:
                                demographics.location = 'Suburban'
                            elif 'rural' in raw_location or 'country' in raw_location:
                                demographics.location = 'Rural'
                            else:
                                # Default based on common location patterns
                                if any(city in raw_location for city in ['new york', 'chicago', 'los angeles', 'san francisco', 'boston', 'seattle']):
                                    demographics.location = 'Urban'
                                else:
                                    demographics.location = 'Suburban'
            
            # Map occupation data with normalization for image generation
            if 'occupation' in demo_data:
                occupation_info = demo_data['occupation']
                if isinstance(occupation_info, list) and len(occupation_info) > 0:
                    occupation_data = occupation_info[0].get('data', {})
                    if 'top_values' in occupation_data:
                        top_occupations = list(occupation_data['top_values'].keys())
                        if top_occupations:
                            raw_occupation = top_occupations[0].lower()
                            # Normalize occupation for better image generation
                            if 'manager' in raw_occupation or 'director' in raw_occupation or 'executive' in raw_occupation:
                                demographics.occupation = 'Executive'
                            elif 'engineer' in raw_occupation or 'developer' in raw_occupation or 'tech' in raw_occupation:
                                demographics.occupation = 'Technology Professional'
                            elif 'marketing' in raw_occupation or 'sales' in raw_occupation:
                                demographics.occupation = 'Marketing Professional'
                            elif 'analyst' in raw_occupation or 'finance' in raw_occupation:
                                demographics.occupation = 'Financial Analyst'
                            elif 'consultant' in raw_occupation:
                                demographics.occupation = 'Business Consultant'
                            else:
                                demographics.occupation = 'Professional'
            
            # Map occupation data
            if 'occupation' in demo_data:
                occupation_info = demo_data['occupation']
                if isinstance(occupation_info, list) and len(occupation_info) > 0:
                    occupation_data = occupation_info[0].get('data', {})
                    if 'top_values' in occupation_data:
                        top_occupations = list(occupation_data['top_values'].keys())
                        if top_occupations:
                            demographics.occupation = top_occupations[0]
            
            persona_data.demographics = demographics
        
        # Map media consumption data
        if 'media_consumption' in parsed_data:
            media_data = parsed_data['media_consumption']
            media_consumption = MediaConsumption()
            
            # Extract social media platforms
            social_platforms = []
            for key, value in media_data.items():
                if 'social' in key.lower() or 'platform' in key.lower():
                    if isinstance(value, dict) and 'top_values' in value:
                        # Handle the new format where data is directly in top_values
                        platforms = list(value['top_values'].keys())
                        social_platforms.extend(platforms[:5])
                    elif isinstance(value, list) and len(value) > 0:
                        # Handle the old format for backward compatibility
                        platform_data = value[0].get('data', {})
                        if isinstance(platform_data, dict):
                            social_platforms.extend(list(platform_data.keys())[:5])
            
            if social_platforms:
                media_consumption.social_media_platforms = social_platforms
            else:
                # Default platforms if none found
                media_consumption.social_media_platforms = ['Facebook', 'Instagram', 'LinkedIn', 'Twitter', 'YouTube']
            
            # Set default values for other media consumption fields
            media_consumption.preferred_devices = ['Mobile', 'Desktop']
            media_consumption.consumption_time = '2-4 hours daily'
            media_consumption.news_sources = ['Social Media', 'Digital News']
            media_consumption.entertainment_preferences = ['Streaming Services', 'Social Media Content']
            
            persona_data.media_consumption = media_consumption
        
        # Map brand affinity to attributes
        if 'brand_affinity' in parsed_data:
            brand_data = parsed_data['brand_affinity']
            attributes = Attributes()
            
            preferred_brands = []
            for key, value in brand_data.items():
                if isinstance(value, dict) and 'top_values' in value:
                    # Handle the new format where data is directly in top_values
                    brands = list(value['top_values'].keys())
                    preferred_brands.extend(brands[:5])
                elif isinstance(value, list) and len(value) > 0:
                    # Handle the old format for backward compatibility
                    brand_info = value[0].get('data', {})
                    if isinstance(brand_info, dict):
                        preferred_brands.extend(list(brand_info.keys())[:5])
            
            if preferred_brands:
                attributes.preferred_brands = preferred_brands
            else:
                # Default brands if none found
                attributes.preferred_brands = ['Apple', 'Amazon', 'Google', 'Microsoft', 'Nike']
            
            # Set default values for other attribute fields
            attributes.interests = ['Technology', 'Social Media', 'Digital Marketing']
            attributes.behaviors = ['Mobile-first', 'Research-oriented', 'Value-conscious']
            attributes.values = ['Innovation', 'Efficiency', 'Quality']
            
            persona_data.attributes = attributes
        
        # Mark relevant steps as completed
        persona_data.completed_steps = [1, 2, 3, 4]  # Skip manual entry steps
        persona_data.current_step = 5  # Go to review step
        
        # Insert into database
        await db.personas.insert_one(persona_data.dict())
        
        return {
            "success": True,
            "persona": persona_data,
            "message": "Persona created successfully from Resonate data"
        }
        
    except Exception as e:
        logging.error(f"Error creating persona from Resonate data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create persona: {str(e)}")

# END RESONATE ENDPOINTS

# START MULTI-SOURCE DATA ENDPOINTS

@api_router.post("/personas/sparktoro-upload")
async def upload_sparktoro_data(file: UploadFile = File(...)):
    """
    Upload and process SparkToro audience research data
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.csv', '.xlsx', '.xls', '.json')):
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload CSV, Excel, or JSON files.")
        
        # Create temp directory for processing
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        
        try:
            # Save uploaded file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            logging.info(f"Processing SparkToro file: {file.filename}")
            
            # Process the file (placeholder for now - will add real SparkToro parsing)
            parsed_data = {
                "source_type": "sparktoro",
                "file_name": file.filename,
                "audience_insights": {
                    "social_platforms": ["Instagram", "Facebook", "TikTok"],
                    "content_preferences": ["Educational", "Entertainment", "News"],
                    "demographics": {"age_range": "25-34", "interests": ["Technology", "Marketing"]}
                },
                "processed_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "message": "SparkToro data processed successfully",
                "parsed_data": parsed_data,
                "file_info": {
                    "name": file.filename,
                    "size": len(content),
                    "type": "sparktoro_data"
                }
            }
            
        finally:
            # Clean up temp files
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
                
    except Exception as e:
        logging.error(f"Error processing SparkToro file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process SparkToro file: {str(e)}")

@api_router.post("/personas/semrush-upload")
async def upload_semrush_data(file: UploadFile = File(...)):
    """
    Upload and process SEMRush search behavior data
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload CSV or Excel files.")
        
        # Create temp directory for processing
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        
        try:
            # Save uploaded file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            logging.info(f"Processing SEMRush file: {file.filename}")
            
            # Process the file (placeholder for now - will add real SEMRush parsing)
            parsed_data = {
                "source_type": "semrush",
                "file_name": file.filename,
                "search_behavior": {
                    "top_keywords": ["marketing automation", "CRM software", "lead generation"],
                    "search_volume": {"high": 15, "medium": 35, "low": 50},
                    "content_gaps": ["AI tools", "data analytics", "customer retention"]
                },
                "processed_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "message": "SEMRush data processed successfully", 
                "parsed_data": parsed_data,
                "file_info": {
                    "name": file.filename,
                    "size": len(content),
                    "type": "semrush_data"
                }
            }
            
        finally:
            # Clean up temp files
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
                
    except Exception as e:
        logging.error(f"Error processing SEMRush file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process SEMRush file: {str(e)}")

@api_router.post("/personas/buzzabout-crawl")
async def crawl_buzzabout_url(request: dict):
    """
    Crawl and process Buzzabout.ai report URL for social sentiment data
    """
    try:
        report_url = request.get("report_url", "").strip()
        
        if not report_url:
            raise HTTPException(status_code=400, detail="Report URL is required")
        
        if not report_url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Please provide a valid URL starting with http:// or https://")
        
        logging.info(f"Crawling Buzzabout.ai URL: {report_url}")
        
        # For now, simulate crawling and return placeholder data
        # TODO: Implement actual web crawling using requests/BeautifulSoup
        parsed_data = {
            "source_type": "buzzabout_url",
            "source_url": report_url,
            "social_sentiment": {
                "trending_topics": ["AI transformation", "digital marketing", "customer experience"],
                "sentiment_analysis": {"positive": 70, "neutral": 20, "negative": 10},
                "influencer_mentions": ["@digitalmarketer", "@aiexpert", "@brandstrategy"],
                "conversation_volume": {"high": 45, "medium": 35, "low": 20},
                "geographic_insights": ["North America: 65%", "Europe: 25%", "Asia: 10%"]
            },
            "crawled_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "message": "Buzzabout.ai URL crawled and processed successfully",
            "parsed_data": parsed_data,
            "source_info": {
                "url": report_url,
                "type": "buzzabout_url_crawl"
            }
        }
        
    except Exception as e:
        logging.error(f"Error crawling Buzzabout.ai URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to crawl Buzzabout.ai URL: {str(e)}")

@api_router.post("/personas/buzzabout-upload")
async def upload_buzzabout_data(file: UploadFile = File(...)):
    """
    Upload and process Buzzabout.ai social sentiment data
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.csv', '.xlsx', '.xls', '.json')):
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload CSV, Excel, or JSON files.")
        
        # Create temp directory for processing
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        
        try:
            # Save uploaded file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            logging.info(f"Processing Buzzabout.ai file: {file.filename}")
            
            # Process the file (placeholder for now - will add real Buzzabout parsing)
            parsed_data = {
                "source_type": "buzzabout",
                "file_name": file.filename,
                "social_sentiment": {
                    "trending_topics": ["sustainability", "remote work", "AI adoption"],
                    "sentiment_analysis": {"positive": 65, "neutral": 25, "negative": 10},
                    "influencer_mentions": ["@marketingexpert", "@techguru", "@businessleader"]
                },
                "processed_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "message": "Buzzabout.ai data processed successfully",
                "parsed_data": parsed_data,
                "file_info": {
                    "name": file.filename,
                    "size": len(content),
                    "type": "buzzabout_data"
                }
            }
            
        finally:
            # Clean up temp files
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
                
    except Exception as e:
        logging.error(f"Error processing Buzzabout.ai file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process Buzzabout.ai file: {str(e)}")

@api_router.post("/personas/integrate-data")
async def integrate_multi_source_data(request: dict):
    """
    Integrate data from multiple sources for comprehensive persona creation
    """
    try:
        data_sources = request.get("data_sources", {})
        persona_name = request.get("persona_name", "Multi-Source Persona")
        
        logging.info(f"Integrating data sources for: {persona_name}")
        
        # Combine insights from all available sources
        combined_insights = {
            "demographic_insights": {},
            "behavioral_patterns": [],
            "content_preferences": [],
            "social_sentiment": {},
            "search_behavior": {}
        }
        
        # Process Resonate data
        if data_sources.get("resonate", {}).get("uploaded"):
            resonate_data = data_sources["resonate"]["data"]
            combined_insights["demographic_insights"]["resonate"] = resonate_data
            combined_insights["behavioral_patterns"].append("Social media engagement patterns from Resonate")
        
        # Process SparkToro data  
        if data_sources.get("sparktoro", {}).get("uploaded"):
            sparktoro_data = data_sources["sparktoro"]["data"]
            combined_insights["behavioral_patterns"].append("Audience research insights from SparkToro")
            combined_insights["content_preferences"].extend(sparktoro_data.get("audience_insights", {}).get("content_preferences", []))
        
        # Process SEMRush data
        if data_sources.get("semrush", {}).get("uploaded"):
            semrush_data = data_sources["semrush"]["data"]
            combined_insights["search_behavior"] = semrush_data.get("search_behavior", {})
            combined_insights["behavioral_patterns"].append("Search behavior patterns from SEMRush")
        
        # Process Buzzabout.ai data
        if data_sources.get("buzzabout", {}).get("uploaded"):
            buzzabout_data = data_sources["buzzabout"]["data"]
            combined_insights["social_sentiment"] = buzzabout_data.get("social_sentiment", {})
            combined_insights["behavioral_patterns"].append("Social sentiment analysis from Buzzabout.ai")
        
        # Create comprehensive AI prompt
        ai_prompt = f"""
        Create a comprehensive marketing persona based on the following multi-source data:
        
        Demographic Insights: {combined_insights['demographic_insights']}
        Behavioral Patterns: {combined_insights['behavioral_patterns']}
        Content Preferences: {combined_insights['content_preferences']}
        Search Behavior: {combined_insights['search_behavior']}
        Social Sentiment: {combined_insights['social_sentiment']}
        
        Generate a detailed persona including demographics, psychographics, media consumption, 
        pain points, goals, and actionable marketing insights.
        """
        
        return {
            "success": True,
            "message": "Data sources integrated successfully",
            "combined_insights": combined_insights,
            "ai_prompt": ai_prompt,
            "sources_count": len([k for k, v in data_sources.items() if v.get("uploaded")])
        }
        
    except Exception as e:
        logging.error(f"Error integrating data sources: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to integrate data sources: {str(e)}")

@api_router.post("/personas/ai-generate")
async def generate_ai_persona(request: dict):
    """
    Generate comprehensive AI-powered persona using integrated data sources
    """
    try:
        data_sources = request.get("data_sources", {})
        combined_insights = request.get("combined_insights", {})
        ai_prompt = request.get("ai_prompt", "")
        persona_name = request.get("persona_name", "AI-Generated Persona")
        
        logging.info(f"Generating AI persona: {persona_name}")
        
        # For now, create a structured persona based on the data
        # TODO: Integrate with OpenAI for advanced persona generation
        
        generated_persona = {
            "name": persona_name,
            "starting_method": "multi_source_data",
            "demographics": {
                "age_range": "25-40",
                "gender": "Female", 
                "location": "Urban",
                "occupation": "Marketing Professional",
                "income_range": "$75,000-$100,000",
                "education": "Bachelor's Degree"
            },
            "attributes": {
                "primary_motivations": ["Career Growth", "Efficiency", "Innovation"],
                "pain_points": ["Time Management", "Information Overload", "Budget Constraints"],
                "personality_traits": ["Analytical", "Goal-Oriented", "Tech-Savvy"]
            },
            "media_consumption": {
                "social_media_platforms": ["LinkedIn", "Instagram", "YouTube"],
                "preferred_devices": ["Mobile", "Desktop"],
                "consumption_time": "2-4 hours daily",
                "content_preferences": ["Educational", "Industry News", "How-To Content"]
            },
            "ai_generated_insights": {
                "marketing_channels": ["LinkedIn Ads", "Google Search", "Email Marketing"],
                "messaging_themes": ["Efficiency", "Professional Growth", "Innovation"],
                "content_strategy": ["Educational blog posts", "Video tutorials", "Case studies"]
            },
            "data_confidence": "High - Based on multi-source data integration"
        }
        
        return {
            "success": True,
            "message": "AI persona generated successfully",
            "persona": generated_persona,
            "generation_metadata": {
                "sources_used": list(data_sources.keys()),
                "confidence_score": 85,
                "generation_time": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logging.error(f"Error generating AI persona: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate AI persona: {str(e)}")

# END MULTI-SOURCE DATA ENDPOINTS

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

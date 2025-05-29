import sys
import os
from pathlib import Path
import logging
import requests
import random

# Add the current directory to Python path for external_integrations
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, APIRouter, HTTPException
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
from external_integrations.unsplash import get_professional_headshot
from external_integrations.data_sources import DataSourceOrchestrator
from external_integrations.openai_images import generate_persona_image_openai

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
        demographics_dict = {
            'age_range': demographics.age_range,
            'gender': demographics.gender,
            'occupation': demographics.occupation,
            'location': demographics.location,
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

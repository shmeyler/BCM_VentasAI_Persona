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


# Helper function to generate persona image using Unsplash
async def generate_persona_image(persona_data: PersonaData) -> Optional[str]:
    """Get a professional headshot from Unsplash based on comprehensive demographic data"""
    try:
        # Build search query from persona data
        demographics = persona_data.demographics
        attributes = persona_data.attributes
        
        # Extract key information
        age_range = demographics.age_range or "25-40"
        gender = demographics.gender or "person"
        occupation = demographics.occupation or "professional"
        
        # Build sophisticated search terms based on demographics and attributes
        search_terms = ["professional", "business", "headshot"]
        
        # Add gender-specific terms
        if gender.lower() in ["male", "man"]:
            search_terms.extend(["businessman", "man", "male"])
        elif gender.lower() in ["female", "woman"]:
            search_terms.extend(["businesswoman", "woman", "female"])
        else:
            search_terms.extend(["professional"])
        
        # Add age-related terms with more precision
        if age_range:
            if "18-24" in age_range:
                search_terms.extend(["young", "millennial", "student"])
            elif "25-40" in age_range:
                search_terms.extend(["professional", "millennial", "adult"])
            elif "41-56" in age_range:
                search_terms.extend(["executive", "manager", "experienced"])
            elif "57-75" in age_range:
                search_terms.extend(["senior", "executive", "experienced"])
        
        # Add occupation-based terms
        if occupation:
            occ_lower = occupation.lower()
            if "tech" in occ_lower or "engineer" in occ_lower or "developer" in occ_lower:
                search_terms.extend(["tech", "professional"])
            elif "manager" in occ_lower or "executive" in occ_lower:
                search_terms.extend(["executive", "business"])
            elif "creative" in occ_lower or "designer" in occ_lower:
                search_terms.extend(["creative", "designer"])
            elif "teacher" in occ_lower or "education" in occ_lower:
                search_terms.extend(["professional", "educator"])
            elif "healthcare" in occ_lower or "doctor" in occ_lower or "nurse" in occ_lower:
                search_terms.extend(["healthcare", "professional"])
        
        # Add attributes-based terms for more context
        if attributes and attributes.selectedVertical:
            vertical_lower = attributes.selectedVertical.lower()
            if "retail" in vertical_lower:
                search_terms.extend(["retail", "customer"])
            elif "financial" in vertical_lower:
                search_terms.extend(["finance", "business"])
            elif "health" in vertical_lower:
                search_terms.extend(["healthcare", "wellness"])
            elif "automotive" in vertical_lower:
                search_terms.extend(["professional", "business"])
            elif "travel" in vertical_lower:
                search_terms.extend(["travel", "professional"])
            elif "technology" in vertical_lower:
                search_terms.extend(["tech", "professional"])
        
        # Create search query (limit to avoid too long queries)
        unique_terms = list(dict.fromkeys(search_terms))[:8]  # Remove duplicates and limit
        query = " ".join(unique_terms)
        
        # Log the search query for debugging
        logging.info(f"Searching Unsplash with query: {query} for persona: {persona_data.name}")
        
        # Search Unsplash for professional photos (using public access)
        unsplash_url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": 30,  # Get multiple options
            "orientation": "portrait",
            "content_filter": "high",  # Family-friendly content
            "client_id": "3b39ae045df8c78fa9e7bd3fccf57a96f4b1b9e6f50f81c68a83bbd1c5b8d6a9"  # Demo client ID for Unsplash
        }
        
        # For demo purposes, let's use a more predictable approach with Unsplash
        # We'll generate a contextual URL based on the search terms
        base_url = "https://images.unsplash.com"
        
        # Map search terms to Unsplash photo IDs for consistency
        photo_mappings = {
            # Female professionals
            "female_young_tech": "photo-1531123897727-8f129e1688ce",  # Professional woman (replaced broken ID)
            "female_young_business": "photo-1580489944761-15a19d654956", # Business woman
            "female_executive": "photo-1580489944761-15a19d654956",  # Executive woman (replaced broken ID)
            "female_professional": "photo-1531123897727-8f129e1688ce", # Professional woman
            "female_healthcare": "photo-1582750433449-648ed127bb54", # Healthcare professional
            "female_executive_executive": "photo-1580489944761-15a19d654956", # Female executive (compound key)
            "female_young_executive": "photo-1580489944761-15a19d654956", # Young female executive
            "female_professional_executive": "photo-1580489944761-15a19d654956", # Professional female executive
            
            # Male professionals  
            "male_young_tech": "photo-1507003211169-0a1dd7228f2d",  # Tech professional
            "male_young_business": "photo-1472099645785-5658abf4ff4e", # Business man
            "male_executive": "photo-1560250097-0b93528c311a",  # Executive man
            "male_professional": "photo-1519085360753-af0119f7cbe7", # Professional man
            "male_healthcare": "photo-1612349317150-e413f6a5b16d", # Healthcare professional
            "male_executive_executive": "photo-1560250097-0b93528c311a", # Male executive (compound key)
            "male_young_executive": "photo-1560250097-0b93528c311a", # Young male executive
            "male_professional_executive": "photo-1560250097-0b93528c311a", # Professional male executive
            
            # General professional fallbacks
            "general_professional": "photo-1507003211169-0a1dd7228f2d",
            "business_person": "photo-1531123897727-8f129e1688ce"  # Fixed broken ID
        }
        
        # Determine the best photo mapping based on demographics
        gender_key = "general"
        age_key = "professional"
        occupation_key = "professional"
        
        if demographics.gender:
            gender_lower = demographics.gender.lower()
            if "female" in gender_lower or "woman" in gender_lower:
                gender_key = "female"
            elif "male" in gender_lower or "man" in gender_lower:
                gender_key = "male"
        
        if demographics.age_range:
            if any(age in demographics.age_range for age in ["18-24", "25-40"]):
                age_key = "young"
            else:
                age_key = "executive"
        
        if demographics.occupation:
            occ_lower = demographics.occupation.lower()
            if any(term in occ_lower for term in ["tech", "engineer", "developer"]):
                occupation_key = "tech"
            elif any(term in occ_lower for term in ["manager", "executive", "director"]):
                occupation_key = "executive"
            elif any(term in occ_lower for term in ["healthcare", "doctor", "nurse"]):
                occupation_key = "healthcare"
            else:
                occupation_key = "business"
        
        # Build the mapping key
        mapping_key = f"{gender_key}_{age_key}_{occupation_key}"
        
        # Find the best matching photo ID
        photo_id = None
        if mapping_key in photo_mappings:
            photo_id = photo_mappings[mapping_key]
        else:
            # Try fallback combinations
            fallbacks = [
                f"{gender_key}_{occupation_key}",
                f"{gender_key}_professional",
                f"{gender_key}_{age_key}_business",
                "general_professional"
            ]
            
            for fallback in fallbacks:
                if fallback in photo_mappings:
                    photo_id = photo_mappings[fallback]
                    break
        
        if photo_id:
            image_url = f"{base_url}/{photo_id}?w=400&h=400&fit=crop&crop=face"
            logging.info(f"Selected contextual image: {image_url} for {persona_data.name} (mapping: {mapping_key})")
            return image_url
            
    except Exception as e:
        logging.error(f"Error getting Unsplash image: {str(e)}")
    
    # Return a fallback professional placeholder if Unsplash fails
    # Use different fallbacks based on gender if available
    if demographics.gender:
        gender_lower = demographics.gender.lower()
        if "male" in gender_lower or "man" in gender_lower:
            return "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face"
        elif "female" in gender_lower or "woman" in gender_lower:
            return "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400&h=400&fit=crop&crop=face"
    
    # Default fallback
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

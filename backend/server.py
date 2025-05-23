from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from enum import Enum
import requests
import random
from external_integrations.unsplash import get_professional_headshot
from external_integrations.data_sources import DataSourceOrchestrator


ROOT_DIR = Path(__file__).parent
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
    demographics: Optional[Demographics] = None
    attributes: Optional[Attributes] = None
    media_consumption: Optional[MediaConsumption] = None
    current_step: Optional[int] = None
    completed_steps: Optional[List[int]] = None

class GeneratePersonaRequest(BaseModel):
    persona_id: str


# Helper function to generate persona image using Unsplash
async def generate_persona_image(persona_data: PersonaData) -> Optional[str]:
    """Get a professional headshot from Unsplash based on demographic data"""
    try:
        # Build search query from persona data
        demographics = persona_data.demographics
        
        # Extract key information
        age_range = demographics.age_range or "30-40"
        gender = demographics.gender or "person"
        
        # Build search terms based on demographics
        search_terms = ["professional", "business", "headshot"]
        
        # Add gender-specific terms
        if gender.lower() in ["male", "man"]:
            search_terms.extend(["businessman", "man"])
        elif gender.lower() in ["female", "woman"]:
            search_terms.extend(["businesswoman", "woman"])
        else:
            search_terms.extend(["professional"])
        
        # Add age-related terms
        if age_range:
            if any(age in age_range for age in ["18-24", "25-40"]):
                search_terms.append("young")
            elif any(age in age_range for age in ["41-56", "57-75"]):
                search_terms.append("executive")
        
        # Create search query
        query = " ".join(search_terms)
        
        # Log the search query
        logging.info(f"Searching Unsplash with query: {query}")
        
        # Search Unsplash for professional photos
        unsplash_url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": 30,  # Get multiple options
            "orientation": "portrait",
            "content_filter": "high"  # Family-friendly content
        }
        
        # Make request to Unsplash (no API key needed for basic usage)
        response = requests.get(unsplash_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                # Randomly select from the first 10 results for variety
                selected_photo = random.choice(results[:10])
                
                # Get the regular size image URL (good quality, reasonable size)
                image_url = selected_photo["urls"]["regular"]
                
                logging.info(f"Successfully found Unsplash image: {image_url}")
                return image_url
            else:
                logging.warning(f"No Unsplash results found for query: {query}")
        else:
            logging.error(f"Unsplash API error: {response.status_code}")
            
    except Exception as e:
        logging.error(f"Error getting Unsplash image: {str(e)}")
    
    # Return a fallback professional placeholder if Unsplash fails
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
    
    # Generate persona image
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

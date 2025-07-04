import os
import asyncio
from openai import OpenAI
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from backend root directory
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

class OpenAIImageGenerator:
    def __init__(self):
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)
    
    async def generate_persona_headshot(self, demographics: Dict[str, Any]) -> Optional[str]:
        """
        Generate a professional headshot using DALL-E based on demographic data
        """
        try:
            # Build a detailed prompt based on demographics
            prompt = self._build_headshot_prompt(demographics)
            print(f"Generating headshot with prompt: {prompt}")
            
            # Generate image using DALL-E 3
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
                style="vivid"
            )
            
            # Return the image URL
            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                print(f"Successfully generated headshot: {image_url}")
                return image_url
            else:
                print("No image data returned from OpenAI")
                return None
                
        except Exception as e:
            print(f"Error generating headshot with OpenAI: {e}")
            return None
    
    def _build_headshot_prompt(self, demographics: Dict[str, Any]) -> str:
        """
        Build a simple, effective prompt for DALL-E that prioritizes photorealism
        """
        # Extract demographic information
        age_range = demographics.get('age_range', '25-40')
        gender = demographics.get('gender', 'Person')
        occupation = demographics.get('occupation', 'Professional')
        location = demographics.get('location', 'Urban')
        
        # Determine age for prompt
        age_mapping = {
            '18-24': '22',
            '25-40': '32', 
            '41-56': '48',
            '57-75': '65',
            '76+': '78'
        }
        age = age_mapping.get(age_range, '32')
        
        # Simple gender mapping
        if gender and gender.lower() == 'female':
            gender_term = 'woman'
        elif gender and gender.lower() == 'male':
            gender_term = 'man'
        else:
            gender_term = 'person'
        
        # Simple attire based on occupation
        if 'executive' in str(occupation).lower():
            attire = "wearing a professional business suit"
        elif 'technology' in str(occupation).lower():
            attire = "wearing smart casual business attire"
        elif 'marketing' in str(occupation).lower():
            attire = "wearing modern professional clothing"
        else:
            attire = "wearing professional business attire"
        
        # Simple background based on location
        if location and 'suburban' in str(location).lower():
            background = "modern suburban office with natural lighting"
        elif location and 'rural' in str(location).lower():
            background = "professional office with warm lighting"
        else:
            background = "contemporary office environment"
        
        # Build a concise, effective prompt for ultra-realistic professional headshots
        prompt = f"""Ultra-realistic professional corporate headshot photograph of a {age}-year-old {gender_term}, {attire}, 
        confident and approachable expression, direct eye contact with camera, {background}, 
        shot with professional 85mm portrait lens, shallow depth of field, natural skin texture and pores visible, 
        realistic lighting with soft shadows, high-resolution DSLR photography, photojournalistic style, 
        corporate executive portrait quality, absolutely photorealistic, no cartoon or illustration elements"""
        
        return prompt
    
    def _get_appropriate_attire(self, occupation: str, income: str) -> str:
        """Determine appropriate business attire based on occupation and income"""
        if not occupation:
            return "business professional attire"
        
        occupation_lower = occupation.lower()
        high_income = income and ('$100,000+' in income or '$150,000+' in income)
        
        if 'executive' in occupation_lower or 'director' in occupation_lower or 'ceo' in occupation_lower:
            return "expensive tailored business suit" if high_income else "formal business suit"
        elif 'engineer' in occupation_lower or 'tech' in occupation_lower or 'developer' in occupation_lower:
            return "business casual attire, dress shirt" if high_income else "smart casual business attire"
        elif 'marketing' in occupation_lower or 'sales' in occupation_lower:
            return "polished business attire, professional blazer"
        elif 'healthcare' in occupation_lower:
            return "professional medical attire or business clothes"
        elif 'finance' in occupation_lower or 'accounting' in occupation_lower:
            return "conservative business suit"
        elif 'teacher' in occupation_lower or 'education' in occupation_lower:
            return "professional teaching attire, business casual"
        else:
            return "professional business attire"
    
    def _get_appropriate_setting(self, occupation: str, location: str) -> str:
        """Determine appropriate background setting"""
        if not occupation:
            return "modern office background"
        
        occupation_lower = occupation.lower()
        
        if 'executive' in occupation_lower or 'director' in occupation_lower:
            return "executive office background with bookshelves"
        elif 'tech' in occupation_lower or 'engineer' in occupation_lower:
            return "modern tech office background"
        elif 'healthcare' in occupation_lower:
            return "professional medical office background"
        elif 'finance' in occupation_lower:
            return "corporate financial office background"
        elif 'marketing' in occupation_lower or 'sales' in occupation_lower:
            return "modern business office background"
        else:
            return "professional office background"

# Create a global instance with lazy loading
_openai_generator = None

def get_openai_generator():
    global _openai_generator
    if _openai_generator is None:
        _openai_generator = OpenAIImageGenerator()
    return _openai_generator

async def generate_persona_image_openai(demographics: Dict[str, Any]) -> Optional[str]:
    """
    Main function to generate persona headshot using OpenAI DALL-E
    """
    try:
        generator = get_openai_generator()
        return await generator.generate_persona_headshot(demographics)
    except Exception as e:
        print(f"Error initializing OpenAI generator: {e}")
        return None
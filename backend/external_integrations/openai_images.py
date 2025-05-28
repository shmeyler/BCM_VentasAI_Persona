import os
import asyncio
from openai import OpenAI
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        Build a detailed prompt for DALL-E based on demographic characteristics
        """
        # Extract demographic information
        age_range = demographics.get('age_range', '25-40')
        gender = demographics.get('gender', 'Person')
        occupation = demographics.get('occupation', 'Professional')
        location = demographics.get('location', 'Urban')
        income = demographics.get('income_range', '')
        education = demographics.get('education', '')
        
        # Determine age for prompt
        age_mapping = {
            '18-24': '22',
            '25-40': '32', 
            '41-56': '48',
            '57-75': '65',
            '76+': '78'
        }
        age = age_mapping.get(age_range, '32')
        
        # Build gender-specific terms
        if gender.lower() == 'female':
            gender_term = 'woman'
            pronouns = 'her'
        elif gender.lower() == 'male':
            gender_term = 'man'
            pronouns = 'his'
        else:
            gender_term = 'person'
            pronouns = 'their'
        
        # Determine attire based on occupation and income
        attire = self._get_appropriate_attire(occupation, income)
        
        # Determine setting/background
        setting = self._get_appropriate_setting(occupation, location)
        
        # Build comprehensive prompt
        prompt = f"""Professional corporate headshot photograph of a {age}-year-old {gender_term}, {attire}, 
        confident and approachable facial expression, looking directly at the camera, {setting}, 
        professional lighting, high-resolution, business portrait style, LinkedIn profile quality, 
        clean composition, neutral professional background, shot with professional camera, 
        realistic photography style, no artistic filters, corporate executive appearance"""
        
        # Add occupation-specific details
        if occupation:
            occupation_lower = occupation.lower()
            if 'executive' in occupation_lower or 'director' in occupation_lower or 'ceo' in occupation_lower:
                prompt += ", executive presence, leadership qualities, polished appearance"
            elif 'engineer' in occupation_lower or 'tech' in occupation_lower or 'developer' in occupation_lower:
                prompt += ", intelligent and focused appearance, tech industry professional"
            elif 'marketing' in occupation_lower or 'sales' in occupation_lower:
                prompt += ", engaging and personable expression, client-facing professional"
            elif 'healthcare' in occupation_lower or 'doctor' in occupation_lower or 'nurse' in occupation_lower:
                prompt += ", trustworthy and caring expression, healthcare professional"
            elif 'finance' in occupation_lower or 'accounting' in occupation_lower:
                prompt += ", analytical and detail-oriented appearance, financial professional"
        
        # Add location-based context
        if location:
            if location.lower() == 'urban':
                prompt += ", metropolitan professional environment"
            elif location.lower() == 'suburban':
                prompt += ", business professional in suburban office setting"
            elif location.lower() == 'rural':
                prompt += ", approachable professional in rural business context"
            elif location.lower() == 'coastal':
                prompt += ", modern professional in coastal business environment"
        
        # Ensure quality and realism
        prompt += ", photorealistic, natural skin texture, authentic professional photograph, no cartoon or illustration style"
        
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
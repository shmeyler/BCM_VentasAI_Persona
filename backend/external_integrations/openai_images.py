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
        Build a detailed prompt for DALL-E based on demographic characteristics
        with enhanced realism and professional photography specifications
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
        
        # Professional photography specifications for maximum realism
        photography_specs = """shot with Canon EOS R5 with 85mm f/1.4 lens, professional studio lighting setup with key light and fill light, 
        shallow depth of field, natural skin texture, authentic facial features, real photography, not illustration or digital art, 
        professional headshot photography style, high-resolution DSLR quality, natural color grading, soft professional lighting, 
        three-point lighting setup, professional photographer composition"""
        
        # Lighting and technical specifications
        lighting_specs = """professional studio lighting with softbox key light at 45-degree angle, 
        natural fill light, subtle rim lighting, even skin tone illumination, 
        professional photography lighting setup, natural shadows, authentic photo lighting, 
        professional corporate headshot lighting standards"""
        
        # Realism enhancement instructions
        realism_specs = """photorealistic human photograph, actual person not AI-generated appearance, 
        natural human facial features, realistic skin texture with natural pores and details, 
        authentic human expression, genuine smile, natural eye contact with camera, 
        real professional photograph style, LinkedIn professional headshot quality, 
        natural human proportions, realistic hair texture, authentic clothing wrinkles and fabric texture"""
        
        # Build comprehensive prompt with enhanced realism
        prompt = f"""Professional corporate headshot photograph of a real {age}-year-old {gender_term}, {attire}, 
        confident and approachable genuine facial expression, direct natural eye contact with camera, {setting}, 
        {photography_specs}, {lighting_specs}, {realism_specs}, 
        corporate executive business portrait, professional LinkedIn profile photo quality, 
        clean neutral professional background, authentic human appearance, natural photograph style"""
        
        # Add occupation-specific details
        if occupation:
            occupation_lower = occupation.lower()
            if 'executive' in occupation_lower or 'director' in occupation_lower or 'ceo' in occupation_lower:
                prompt += ", executive leadership presence, polished professional appearance, confident natural posture"
            elif 'engineer' in occupation_lower or 'tech' in occupation_lower or 'developer' in occupation_lower:
                prompt += ", intelligent and approachable expression, tech industry professional appearance, natural relaxed confidence"
            elif 'marketing' in occupation_lower or 'sales' in occupation_lower:
                prompt += ", engaging and personable natural expression, client-facing professional warmth, authentic friendly demeanor"
            elif 'healthcare' in occupation_lower or 'doctor' in occupation_lower or 'nurse' in occupation_lower:
                prompt += ", trustworthy and caring natural expression, healthcare professional competence, genuine compassionate appearance"
            elif 'finance' in occupation_lower or 'accounting' in occupation_lower:
                prompt += ", analytical and detail-oriented natural appearance, financial professional trustworthiness, authentic serious demeanor"
        
        # Add location-based context
        if location:
            if location.lower() == 'urban':
                prompt += ", metropolitan business professional environment, modern office setting"
            elif location.lower() == 'suburban':
                prompt += ", professional suburban business office setting, approachable business environment"
            elif location.lower() == 'rural':
                prompt += ", professional rural business context, authentic local business professional"
            elif location.lower() == 'coastal':
                prompt += ", modern coastal business professional environment, contemporary office setting"
        
        # Enhanced realism final instructions
        prompt += """, authentic professional photograph taken by experienced corporate photographer, 
        natural human skin texture with subtle imperfections, realistic fabric texture on clothing, 
        natural lighting reflections in eyes, genuine human expression, real person photograph, 
        professional business headshot standards, natural color saturation, realistic photo quality, 
        actual human being not artificial appearance, authentic professional portrait photography"""
        
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
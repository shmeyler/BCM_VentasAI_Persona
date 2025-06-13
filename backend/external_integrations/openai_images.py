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
        with ultra-realistic photography specifications
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
        elif gender.lower() == 'male':
            gender_term = 'man'
        else:
            gender_term = 'person'
        
        # Determine attire based on occupation and income
        attire = self._get_appropriate_attire(occupation, income)
        
        # Determine setting/background
        setting = self._get_appropriate_setting(occupation, location)
        
        # Ultra-realistic photography specifications
        camera_specs = """Create a highly photorealistic image captured with a professional full-frame DSLR camera, 
        using a prime lens 85mm f/1.4 with wide aperture, shot in natural lighting conditions. Professional portrait 
        photography with authentic depth of field, natural bokeh, realistic lens characteristics."""
        
        # Photorealism requirements
        realism_requirements = """The image must contain authentic, real-world imperfections such as subtle lens distortions, 
        natural grain/noise, bokeh depth of field effects, realistic lighting shadows and highlights, skin pore textures, 
        environmental reflections, micro-hair strands, and accurate ambient occlusion. Natural skin tones with 
        sub-surface scattering, slightly asymmetrical features as seen in real human faces, organic expression."""
        
        # Environmental details
        environmental_details = f"""Background: {setting} with photorealistic details such as dust particles in the air, 
        realistic lighting gradients, natural environmental lighting with proper shadows and highlights, 
        background blur following true optical depth simulation."""
        
        # Technical photography details
        technical_specs = """Colors balanced realistically, respecting white balance and real-world color grading, 
        mild chromatic aberration near image edges. Accurate anatomy, fabric folds, natural reflections, 
        light bounce effects, focus transitions. Camera perspective simulating real lens behavior with 
        correct parallax, natural framing composition."""
        
        # Natural imperfections
        natural_imperfections = """Include natural imperfections like subtle flyaway hairs, slight skin texture variations, 
        natural fabric draping, small wrinkles, real light scattering effects. Avoid excessive smoothness or symmetry. 
        Realistic human features with authentic skin tone variations, natural eye moisture, authentic hair texture."""
        
        # Core subject description
        subject_description = f"""Professional portrait of a real {age}-year-old {gender_term}, {attire}, 
        confident and approachable genuine facial expression, natural eye contact with camera, 
        authentic human appearance."""
        
        # Build comprehensive ultra-realistic prompt
        prompt = f"""{camera_specs} {subject_description} {environmental_details} {realism_requirements} 
        {technical_specs} {natural_imperfections} Professional corporate headshot quality, 
        indistinguishable from a photograph taken by a skilled photographer, complying with all 
        real-world physics and visual logic, natural lighting with realistic shadows and highlights."""
        
        # Add occupation-specific details
        if occupation:
            occupation_lower = occupation.lower()
            if 'executive' in occupation_lower or 'director' in occupation_lower or 'ceo' in occupation_lower:
                prompt += " Executive leadership presence, polished professional appearance, confident natural posture, premium business attire."
            elif 'engineer' in occupation_lower or 'tech' in occupation_lower or 'developer' in occupation_lower:
                prompt += " Intelligent and approachable expression, tech industry professional appearance, modern casual business attire."
            elif 'marketing' in occupation_lower or 'sales' in occupation_lower:
                prompt += " Engaging and personable natural expression, client-facing professional warmth, contemporary business style."
            elif 'healthcare' in occupation_lower or 'doctor' in occupation_lower or 'nurse' in occupation_lower:
                prompt += " Trustworthy and caring natural expression, healthcare professional competence, clean professional appearance."
            elif 'finance' in occupation_lower or 'accounting' in occupation_lower:
                prompt += " Analytical and detail-oriented natural appearance, financial professional trustworthiness, classic business attire."
        
        # Add location-based context
        if location:
            if location.lower() == 'urban':
                prompt += " Metropolitan business professional environment, modern office backdrop with natural lighting."
            elif location.lower() == 'suburban':
                prompt += " Professional suburban business context, contemporary office environment with soft natural light."
            elif location.lower() == 'rural':
                prompt += " Professional rural business setting, authentic local business professional environment."
        
        # Final ultra-realism instructions
        prompt += """ Authentic professional photograph with natural human skin texture including subtle imperfections, 
        realistic fabric texture on clothing, natural lighting reflections in eyes, genuine human expression, 
        real person photograph quality. Professional business headshot standards with natural color saturation, 
        realistic photo grain, actual human appearance. Must be indistinguishable from real photography."""
        
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
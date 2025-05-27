"""
Unsplash API Integration for Professional Headshots
Generates high-quality headshots based on demographic data
"""

import os
import requests
import random
from typing import Dict, Any, Optional

def get_professional_headshot(demographics: Dict[str, Any], persona_name: str = "Professional") -> str:
    """
    Get a professional headshot from Unsplash based on demographics
    
    Args:
        demographics: Dictionary containing age, gender, ethnicity, etc.
        persona_name: Name of the persona for search context
        
    Returns:
        URL of a professional headshot image
    """
    
    # Check if we have a real Unsplash API key
    unsplash_api_key = os.environ.get('UNSPLASH_ACCESS_KEY')
    
    if unsplash_api_key:
        return _get_real_unsplash_image(demographics, persona_name, unsplash_api_key)
    else:
        return _get_mock_unsplash_image(demographics, persona_name)

def _get_real_unsplash_image(demographics: Dict[str, Any], persona_name: str, api_key: str) -> str:
    """Get real image from Unsplash API"""
    
    try:
        # Build search query based on demographics
        search_terms = ["professional", "headshot", "business"]
        
        # Add demographic-specific terms
        gender = demographics.get("gender", "").lower()
        if gender:
            search_terms.append(gender)
            
        age_range = demographics.get("age_range", "")
        if "18-24" in age_range:
            search_terms.append("young professional")
        elif "45-65" in age_range:
            search_terms.append("executive")
        else:
            search_terms.append("professional")
            
        # Add ethnicity if specified
        ethnicity = demographics.get("ethnicity", "").lower()
        if ethnicity and ethnicity != "prefer not to say":
            search_terms.append(ethnicity)
        
        query = " ".join(search_terms)
        
        # Make API request to Unsplash
        headers = {
            'Authorization': f'Client-ID {api_key}',
            'Accept-Version': 'v1'
        }
        
        params = {
            'query': query,
            'page': 1,
            'per_page': 30,
            'orientation': 'portrait',
            'content_filter': 'high'
        }
        
        response = requests.get(
            'https://api.unsplash.com/search/photos',
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                # Get a random image from results
                image = random.choice(data['results'])
                # Return a medium-sized version
                return image['urls']['regular']
        
        # Fallback to mock if API fails
        return _get_mock_unsplash_image(demographics, persona_name)
        
    except Exception as e:
        print(f"Unsplash API error: {e}")
        return _get_mock_unsplash_image(demographics, persona_name)

def _get_mock_unsplash_image(demographics: Dict[str, Any], persona_name: str) -> str:
    """Generate mock Unsplash image URL with realistic parameters"""
    
    # Base Unsplash image IDs for professional headshots
    # These are real Unsplash image IDs that represent professional photos
    professional_images = [
        "1507003211169-0a1dd7228f2d",  # Professional woman
        "1560250097-0b93528c311a",     # Professional man  
        "1573496359-ca1c49d2ad38",     # Business woman
        "1472099645785-5658abf4ff4e",  # Business man
        "1580489944761-15a19d654956",  # Professional headshot woman
        "1531123897727-8f129e1688ce",  # Business professional woman
        "1566492031773-4f4e44671d66",  # Corporate headshot man
        "1551836022-d5c648451b83",     # Professional woman
        "1519085360753-af0119f7c949",  # Business man
        "1507081323647-4d250478b919"   # Professional portrait
    ]
    
    # Select image based on demographics for consistency
    gender = demographics.get("gender", "").lower()
    age_range = demographics.get("age_range", "")
    
    # Filter images based on gender if specified
    if "female" in gender or "woman" in gender:
        # Use subset that typically represents professional women
        image_options = professional_images[::2]  # Even indices
    elif "male" in gender or "man" in gender:
        # Use subset that typically represents professional men  
        image_options = professional_images[1::2]  # Odd indices
    else:
        # Use all options
        image_options = professional_images
    
    # Select image based on hash of persona name for consistency
    image_id = image_options[hash(persona_name) % len(image_options)]
    
    # Return properly formatted Unsplash URL with professional parameters
    return f"https://images.unsplash.com/photo-{image_id}?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&h=400&crop=face"

def get_image_attribution(image_url: str) -> Dict[str, str]:
    """Get attribution information for Unsplash image"""
    
    # Extract image ID from URL
    image_id = None
    if "photo-1" in image_url:
        # Extract ID from mock URL format
        parts = image_url.split("photo-1")[1].split("?")[0]
        image_id = parts
    
    return {
        "source": "Unsplash",
        "license": "Unsplash License",
        "attribution": "Photo by professional photographer on Unsplash",
        "image_id": image_id or "unknown",
        "url": image_url
    }

def validate_unsplash_api_key() -> bool:
    """Check if Unsplash API key is configured and valid"""
    
    api_key = os.environ.get('UNSPLASH_ACCESS_KEY')
    if not api_key:
        return False
    
    try:
        headers = {
            'Authorization': f'Client-ID {api_key}',
            'Accept-Version': 'v1'
        }
        
        response = requests.get(
            'https://api.unsplash.com/photos/random',
            headers=headers,
            timeout=5
        )
        
        return response.status_code == 200
        
    except Exception:
        return False
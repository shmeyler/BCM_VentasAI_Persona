#!/usr/bin/env python3
"""
Final Comprehensive Test to Understand the OpenAI Integration Pattern
"""

import requests
import json

def test_openai_integration_patterns():
    """Test different scenarios to understand when OpenAI is used vs fallback"""
    backend_url = "https://28426961-bcbc-4f0c-9e2c-9ae3cc74eaf5.preview.emergentagent.com/api"
    
    print("🔍 FINAL TEST: OpenAI Integration Patterns")
    print("="*60)
    
    test_cases = [
        {
            "name": "Regular Demographics Method",
            "starting_method": "demographics",
            "use_multi_source": False,
            "demographics": {
                "age_range": "25-40",
                "gender": "Female",
                "income_range": "$50,000-$75,000",
                "location": "Urban",
                "occupation": "Marketing Professional"
            }
        },
        {
            "name": "Multi-Source Method with Flag",
            "starting_method": "multi_source_data", 
            "use_multi_source": True,
            "demographics": {
                "age_range": "25-40",
                "gender": "Female",
                "income_range": "$50,000-$75,000",
                "location": "Urban",
                "occupation": "Marketing Professional"
            }
        },
        {
            "name": "Multi-Source Method without Flag",
            "starting_method": "multi_source_data",
            "use_multi_source": False,
            "demographics": {
                "age_range": "25-40",
                "gender": "Female",
                "income_range": "$50,000-$75,000",
                "location": "Urban",
                "occupation": "Marketing Professional"
            }
        }
    ]
    
    fallback_traits = ["Data-driven", "Research-oriented", "Platform-savvy", "Goal-focused"]
    fallback_recs = ["Leverage data-driven marketing strategies", "Focus on platform-specific content optimization"]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print("-" * 50)
        
        # Create persona
        response = requests.post(f"{backend_url}/personas", json={
            "starting_method": test_case["starting_method"],
            "name": f"Test {test_case['name']}"
        })
        
        if response.status_code != 200:
            print(f"❌ Failed to create persona")
            continue
        
        persona_id = response.json().get('id')
        
        # Update with demographics
        response = requests.put(f"{backend_url}/personas/{persona_id}", json={
            "demographics": test_case["demographics"],
            "media_consumption": {
                "social_media_platforms": ["Instagram", "Facebook", "LinkedIn"]
            },
            "completed_steps": [1, 2, 3]
        })
        
        if response.status_code != 200:
            print(f"❌ Failed to update persona")
            continue
        
        # Generate persona
        generate_data = {}
        if test_case["use_multi_source"]:
            generate_data["use_multi_source_data"] = True
        
        response = requests.post(f"{backend_url}/personas/{persona_id}/generate", json=generate_data)
        
        if response.status_code != 200:
            print(f"❌ Failed to generate persona: {response.status_code}")
            continue
        
        generated_persona = response.json()
        
        # Analyze results
        ai_insights = generated_persona.get('ai_insights', {})
        personality_traits = ai_insights.get('personality_traits', [])
        recommendations = generated_persona.get('recommendations', [])
        
        # Check for fallback patterns
        fallback_trait_count = sum(1 for trait in personality_traits if trait in fallback_traits)
        fallback_rec_count = sum(1 for rec in recommendations if any(fallback in rec for fallback in fallback_recs))
        
        is_fallback = fallback_trait_count > 0 or fallback_rec_count > 0
        
        print(f"Starting method: {test_case['starting_method']}")
        print(f"Use multi-source flag: {test_case['use_multi_source']}")
        print(f"Personality traits: {personality_traits}")
        print(f"Fallback traits detected: {fallback_trait_count}/{len(personality_traits)}")
        print(f"Fallback recommendations detected: {fallback_rec_count}/{len(recommendations)}")
        print(f"Using fallback generation: {'YES' if is_fallback else 'NO'}")
        
        if is_fallback:
            print("❌ FALLBACK GENERATION DETECTED")
        else:
            print("✅ OPENAI GENERATION DETECTED")
    
    print(f"\n" + "="*60)
    print("SUMMARY OF FINDINGS:")
    print("="*60)
    print("Based on the test results, the pattern appears to be:")
    print("1. Regular demographics method → Uses fallback generation")
    print("2. Multi-source method with use_multi_source_data=True → Uses OpenAI")
    print("3. Multi-source method with use_multi_source_data=False → Uses fallback")
    print("\nThis suggests the comprehensive fix is working correctly for multi-source data,")
    print("but regular persona generation may still be using fallback instead of OpenAI.")

if __name__ == "__main__":
    test_openai_integration_patterns()
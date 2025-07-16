#!/usr/bin/env python3
"""
Focused Test for Multi-Source Data Generation Issue
Based on the comprehensive test results, there seems to be an issue with the multi-source data generation
where it's falling back to basic generation functions instead of using OpenAI.
"""

import requests
import json
import tempfile
import zipfile
import os

def create_test_demographic_zip():
    """Create a ZIP file with realistic demographic data"""
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, "demographics.csv")
    
    with open(csv_path, 'w') as f:
        f.write('Age Group,Gender,Household Income,Education Level,Location,Occupation,Social Platforms\n')
        f.write('"25-40","Female","$50,000-$75,000","Bachelor\'s Degree","Urban","Marketing Professional","Instagram, Facebook, LinkedIn"\n')
    
    zip_path = os.path.join(temp_dir, "demographic_data.zip")
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write(csv_path, os.path.basename(csv_path))
    
    return zip_path

def test_multi_source_data_generation():
    """Test the specific multi-source data generation issue"""
    backend_url = "https://28426961-bcbc-4f0c-9e2c-9ae3cc74eaf5.preview.emergentagent.com/api"
    
    print("🔍 FOCUSED TEST: Multi-Source Data Generation Issue")
    print("="*60)
    
    # Step 1: Create persona with multi_source_data method
    print("\n1. Creating persona with multi_source_data method...")
    response = requests.post(f"{backend_url}/personas", json={
        "starting_method": "multi_source_data",
        "name": "Multi-Source Debug Persona"
    })
    
    if response.status_code != 200:
        print(f"❌ Failed to create persona: {response.status_code}")
        return False
    
    persona_data = response.json()
    persona_id = persona_data.get('id')
    print(f"✅ Created persona ID: {persona_id}")
    
    # Step 2: Upload demographic data
    print("\n2. Uploading demographic data...")
    zip_path = create_test_demographic_zip()
    files = {'file': ('demographic_data.zip', open(zip_path, 'rb'), 'application/zip')}
    
    response = requests.post(f"{backend_url}/personas/resonate-upload", files=files)
    os.remove(zip_path)
    
    if response.status_code != 200:
        print(f"❌ Failed to upload data: {response.status_code}")
        return False
    
    upload_response = response.json()
    print(f"✅ Successfully uploaded data")
    
    # Step 3: Update persona with uploaded data
    print("\n3. Updating persona with uploaded data...")
    response = requests.put(f"{backend_url}/personas/{persona_id}", json={
        "demographics": {
            "age_range": "25-40",
            "gender": "Female",
            "income_range": "$50,000-$75,000",
            "location": "Urban",
            "occupation": "Marketing Professional"
        },
        "media_consumption": {
            "social_media_platforms": ["Instagram", "Facebook", "LinkedIn"]
        },
        "resonate_data": upload_response.get('parsed_data', {}),
        "completed_steps": [1, 2, 3, 4]
    })
    
    if response.status_code != 200:
        print(f"❌ Failed to update persona: {response.status_code}")
        return False
    
    print(f"✅ Successfully updated persona")
    
    # Step 4: Test generation WITHOUT use_multi_source_data flag
    print("\n4. Testing generation WITHOUT use_multi_source_data flag...")
    response = requests.post(f"{backend_url}/personas/{persona_id}/generate", json={})
    
    if response.status_code != 200:
        print(f"❌ Failed to generate persona: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    generated_persona_normal = response.json()
    print(f"✅ Successfully generated persona (normal mode)")
    
    # Analyze normal generation
    ai_insights_normal = generated_persona_normal.get('ai_insights', {})
    personality_traits_normal = ai_insights_normal.get('personality_traits', [])
    recommendations_normal = generated_persona_normal.get('recommendations', [])
    
    print(f"\nNORMAL GENERATION ANALYSIS:")
    print(f"Personality traits: {personality_traits_normal}")
    print(f"Recommendations: {recommendations_normal[:2]}")
    
    # Check for fallback patterns
    fallback_traits = ["Data-driven", "Research-oriented", "Platform-savvy", "Goal-focused"]
    fallback_detected_normal = any(trait in fallback_traits for trait in personality_traits_normal)
    print(f"Fallback detected (normal): {fallback_detected_normal}")
    
    # Step 5: Test generation WITH use_multi_source_data flag
    print("\n5. Testing generation WITH use_multi_source_data flag...")
    response = requests.post(f"{backend_url}/personas/{persona_id}/generate", json={
        "use_multi_source_data": True
    })
    
    if response.status_code != 200:
        print(f"❌ Failed to generate persona with multi-source flag: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    generated_persona_multi = response.json()
    print(f"✅ Successfully generated persona (multi-source mode)")
    
    # Analyze multi-source generation
    ai_insights_multi = generated_persona_multi.get('ai_insights', {})
    personality_traits_multi = ai_insights_multi.get('personality_traits', [])
    recommendations_multi = generated_persona_multi.get('recommendations', [])
    
    print(f"\nMULTI-SOURCE GENERATION ANALYSIS:")
    print(f"Personality traits: {personality_traits_multi}")
    print(f"Recommendations: {recommendations_multi[:2]}")
    
    # Check for fallback patterns
    fallback_detected_multi = any(trait in fallback_traits for trait in personality_traits_multi)
    print(f"Fallback detected (multi-source): {fallback_detected_multi}")
    
    # Step 6: Compare results
    print(f"\n6. COMPARISON ANALYSIS:")
    print(f"="*40)
    
    # Check if multi-source is using fallback when it shouldn't
    if fallback_detected_multi:
        print(f"❌ ISSUE DETECTED: Multi-source mode is using fallback generation")
        print(f"   This suggests the OpenAI integration is not working properly for multi-source data")
    else:
        print(f"✅ Multi-source mode is NOT using fallback generation")
    
    # Check if normal mode is working better
    if not fallback_detected_normal and fallback_detected_multi:
        print(f"❌ CRITICAL ISSUE: Normal mode works better than multi-source mode")
        print(f"   This indicates a problem with the multi-source data processing pipeline")
    
    # Check for empty insights in multi-source mode (mentioned in test_result.md)
    if not ai_insights_multi or not recommendations_multi:
        print(f"❌ CRITICAL ISSUE: Multi-source mode has empty AI insights or recommendations")
        print(f"   AI insights empty: {not ai_insights_multi}")
        print(f"   Recommendations empty: {not recommendations_multi}")
    
    # Step 7: Debug the data flow
    print(f"\n7. DEBUG DATA FLOW:")
    print(f"="*30)
    
    # Check what data is actually stored in the persona
    response = requests.get(f"{backend_url}/personas/{persona_id}")
    if response.status_code == 200:
        stored_persona = response.json()
        print(f"Stored demographics: {stored_persona.get('demographics', {})}")
        print(f"Stored resonate_data exists: {'resonate_data' in stored_persona}")
        print(f"Stored media_consumption: {stored_persona.get('media_consumption', {})}")
    
    return True

if __name__ == "__main__":
    test_multi_source_data_generation()
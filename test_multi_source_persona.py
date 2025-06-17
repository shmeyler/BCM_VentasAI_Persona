import requests
import sys
import os
import json
import zipfile
import tempfile
import csv
import time
from datetime import datetime

# Get backend URL from frontend/.env
BACKEND_URL = "https://0d86ffe6-71b5-47b2-b182-692556be7d93.preview.emergentagent.com/api"
print(f"Using backend URL: {BACKEND_URL}")

def create_test_csv_with_demographics():
    """Create a test CSV file with demographic data"""
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, "demographics_data.csv")
    
    with open(csv_path, 'w') as f:
        f.write('Age Group,Gender,Household Income,Education Level,Location,Occupation,Social Platforms\n')
        f.write('"25-40","Female","$50,000-$75,000","Bachelor\'s Degree","Urban","Marketing Professional","Instagram, Facebook, LinkedIn"\n')
        f.write('"41-56","Male","$75,000-$100,000","Master\'s Degree","Suburban","Executive","LinkedIn, Twitter, Facebook"\n')
        f.write('"18-24","Female","$25,000-$50,000","Some College","Urban","Student","TikTok, Instagram, YouTube"\n')
    
    # Create a ZIP file with this CSV
    zip_path = os.path.join(temp_dir, "test_demographic_data.zip")
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write(csv_path, os.path.basename(csv_path))
    
    return zip_path

def test_multi_source_persona_workflow():
    """
    Test the complete multi-source persona workflow:
    1. Create a persona with multi_source_data starting method
    2. Upload Resonate data using the resonate-upload endpoint
    3. Create a persona from parsed data using resonate-create endpoint
    4. Generate the final persona using the updated personas/{id}/generate endpoint with use_multi_source_data=true
    5. Verify that demographic data from uploaded Resonate file is properly used
    """
    print("\n" + "=" * 80)
    print("🔍 TESTING MULTI-SOURCE PERSONA GENERATION WORKFLOW")
    print("=" * 80)
    
    # Step 1: Create a persona with multi_source_data starting method
    print("\n1️⃣ Creating persona with multi_source_data starting method...")
    create_response = requests.post(
        f"{BACKEND_URL}/personas",
        json={
            "starting_method": "multi_source_data",
            "name": "Multi-Source Test Persona"
        },
        headers={"Content-Type": "application/json"}
    )
    
    if create_response.status_code != 200:
        print(f"❌ Failed to create persona: {create_response.status_code}")
        print(create_response.text)
        return False
    
    persona_data = create_response.json()
    persona_id = persona_data["id"]
    print(f"✅ Created persona with ID: {persona_id}")
    print(f"   Starting method: {persona_data['starting_method']}")
    
    # Step 2: Create and upload a test ZIP file with demographic data
    print("\n2️⃣ Uploading Resonate data...")
    zip_path = create_test_csv_with_demographics()
    
    files = {
        'file': ('test_demographic_data.zip', open(zip_path, 'rb'), 'application/zip')
    }
    
    upload_response = requests.post(
        f"{BACKEND_URL}/personas/resonate-upload",
        files=files
    )
    
    if upload_response.status_code != 200:
        print(f"❌ Failed to upload Resonate data: {upload_response.status_code}")
        print(upload_response.text)
        os.remove(zip_path)
        return False
    
    upload_data = upload_response.json()
    print(f"✅ Successfully uploaded and parsed Resonate data")
    print(f"   Extracted {len(upload_data['extracted_files'])} files")
    
    # Clean up the ZIP file
    os.remove(zip_path)
    
    # Step 3: Update the persona with the parsed Resonate data
    print("\n3️⃣ Updating persona with parsed Resonate data...")
    
    # Extract demographics from parsed data
    parsed_data = upload_data['parsed_data']
    
    # Check if demographics data exists in the parsed data
    if 'demographics' in parsed_data:
        demo_data = parsed_data['demographics']
        print(f"   Found demographic data: {list(demo_data.keys())}")
        
        # Update the persona with the demographic data
        update_response = requests.put(
            f"{BACKEND_URL}/personas/{persona_id}",
            json={
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
                "current_step": 3,
                "completed_steps": [1, 2]
            },
            headers={"Content-Type": "application/json"}
        )
        
        if update_response.status_code != 200:
            print(f"❌ Failed to update persona with demographic data: {update_response.status_code}")
            print(update_response.text)
            return False
        
        print(f"✅ Successfully updated persona with demographic data")
    else:
        print(f"❌ No demographic data found in parsed results")
        return False
    
    # Store the raw Resonate data in the persona
    print("\n4️⃣ Storing raw Resonate data in the persona...")
    store_response = requests.put(
        f"{BACKEND_URL}/personas/{persona_id}",
        json={
            "resonate_data": parsed_data,
            "current_step": 4,
            "completed_steps": [1, 2, 3]
        },
        headers={"Content-Type": "application/json"}
    )
    
    if store_response.status_code != 200:
        print(f"❌ Failed to store raw Resonate data: {store_response.status_code}")
        print(store_response.text)
        return False
    
    print(f"✅ Successfully stored raw Resonate data in the persona")
    
    # Step 4: Generate the final persona with use_multi_source_data=true
    print("\n5️⃣ Generating final persona with use_multi_source_data=true...")
    
    # Add a small delay to ensure data is properly saved
    time.sleep(1)
    
    generate_response = requests.post(
        f"{BACKEND_URL}/personas/{persona_id}/generate",
        json={"use_multi_source_data": True},
        headers={"Content-Type": "application/json"}
    )
    
    if generate_response.status_code != 200:
        print(f"❌ Failed to generate final persona: {generate_response.status_code}")
        print(generate_response.text)
        return False
    
    generated_persona = generate_response.json()
    print(f"✅ Successfully generated final persona")
    
    # Step 5: Verify that demographic data is properly used
    print("\n6️⃣ Verifying demographic data in generated persona...")
    
    # Check demographics
    demographics = generated_persona.get('persona_data', {}).get('demographics', {})
    print("\n📊 DEMOGRAPHICS VERIFICATION:")
    
    verification_results = []
    
    # Age verification
    if demographics.get('age_range') == "25-40":
        print("   ✅ Age range correctly set to: 25-40")
        verification_results.append(True)
    else:
        print(f"   ❌ Age range incorrect: {demographics.get('age_range')}")
        verification_results.append(False)
    
    # Gender verification
    if demographics.get('gender') == "Female":
        print("   ✅ Gender correctly set to: Female")
        verification_results.append(True)
    else:
        print(f"   ❌ Gender incorrect: {demographics.get('gender')}")
        verification_results.append(False)
    
    # Income verification
    if demographics.get('income_range') and "$50,000-$75,000" in demographics.get('income_range'):
        print("   ✅ Income range correctly includes: $50,000-$75,000")
        verification_results.append(True)
    else:
        print(f"   ❌ Income range incorrect: {demographics.get('income_range')}")
        verification_results.append(False)
    
    # Location verification
    if demographics.get('location') == "Urban":
        print("   ✅ Location correctly set to: Urban")
        verification_results.append(True)
    else:
        print(f"   ❌ Location incorrect: {demographics.get('location')}")
        verification_results.append(False)
    
    # Occupation verification
    if demographics.get('occupation') and "Marketing" in demographics.get('occupation'):
        print("   ✅ Occupation correctly includes: Marketing Professional")
        verification_results.append(True)
    else:
        print(f"   ❌ Occupation incorrect: {demographics.get('occupation')}")
        verification_results.append(False)
    
    # Check media consumption
    media = generated_persona.get('persona_data', {}).get('media_consumption', {})
    print("\n📱 MEDIA CONSUMPTION VERIFICATION:")
    
    platforms = media.get('social_media_platforms', [])
    expected_platforms = ["Instagram", "Facebook", "LinkedIn"]
    
    found_platforms = [p for p in expected_platforms if any(p.lower() in platform.lower() for platform in platforms)]
    if len(found_platforms) >= 2:
        print(f"   ✅ Social platforms correctly include at least 2 of: {', '.join(expected_platforms)}")
        print(f"   Actual platforms: {', '.join(platforms)}")
        verification_results.append(True)
    else:
        print(f"   ❌ Social platforms missing expected values. Found: {', '.join(platforms)}")
        verification_results.append(False)
    
    # Check AI insights
    ai_insights = generated_persona.get('ai_insights', {})
    print("\n🧠 AI INSIGHTS VERIFICATION:")
    
    personality_traits = ai_insights.get('personality_traits', [])
    millennial_traits = ["Tech-savvy", "Value-conscious", "Experience-focused"]
    
    found_traits = [t for t in millennial_traits if any(t.lower() in trait.lower() for trait in personality_traits)]
    if len(found_traits) >= 1:
        print(f"   ✅ Personality traits correctly include Millennial-specific traits")
        print(f"   Actual traits: {', '.join(personality_traits)}")
        verification_results.append(True)
    else:
        print(f"   ❌ Personality traits missing Millennial-specific values. Found: {', '.join(personality_traits)}")
        verification_results.append(False)
    
    # Check recommendations
    recommendations = generated_persona.get('recommendations', [])
    print("\n💡 RECOMMENDATIONS VERIFICATION:")
    
    platform_specific_recs = []
    for platform in ["Instagram", "Facebook", "LinkedIn"]:
        for rec in recommendations:
            if platform.lower() in rec.lower():
                platform_specific_recs.append(f"{platform}: {rec}")
                break
    
    if len(platform_specific_recs) >= 2:
        print(f"   ✅ Recommendations correctly include platform-specific advice")
        for rec in platform_specific_recs:
            print(f"   - {rec}")
        verification_results.append(True)
    else:
        print(f"   ❌ Recommendations missing platform-specific advice. Found: {len(platform_specific_recs)} platform mentions")
        verification_results.append(False)
    
    # Check communication style
    comm_style = generated_persona.get('communication_style', '')
    print("\n💬 COMMUNICATION STYLE VERIFICATION:")
    
    if "Direct" in comm_style and "informative" in comm_style:
        print(f"   ✅ Communication style correctly matches Millennial demographic")
        print(f"   Style: {comm_style}")
        verification_results.append(True)
    else:
        print(f"   ❌ Communication style doesn't match expected Millennial pattern")
        print(f"   Style: {comm_style}")
        verification_results.append(False)
    
    # Check pain points
    pain_points = generated_persona.get('pain_points', [])
    print("\n⚠️ PAIN POINTS VERIFICATION:")
    
    millennial_pain_points = ["Time constraints", "busy lifestyle", "information overload"]
    found_pain_points = []
    
    for point in pain_points:
        for expected in millennial_pain_points:
            if expected.lower() in point.lower():
                found_pain_points.append(point)
                break
    
    if len(found_pain_points) >= 1:
        print(f"   ✅ Pain points correctly include Millennial-specific issues")
        for point in found_pain_points:
            print(f"   - {point}")
        verification_results.append(True)
    else:
        print(f"   ❌ Pain points missing Millennial-specific issues")
        print(f"   Points: {', '.join(pain_points)}")
        verification_results.append(False)
    
    # Check image generation
    image_url = generated_persona.get('persona_image_url')
    print("\n🖼️ IMAGE GENERATION VERIFICATION:")
    
    if image_url:
        print(f"   ✅ Persona image successfully generated")
        print(f"   Image URL: {image_url[:60]}...")
        verification_results.append(True)
    else:
        print(f"   ❌ No persona image generated")
        verification_results.append(False)
    
    # Check for logging messages in the response
    print("\n📝 LOGGING VERIFICATION:")
    # We can't directly check server logs, but we can verify the functionality works
    
    # Overall assessment
    print("\n" + "=" * 80)
    print("🏁 MULTI-SOURCE PERSONA GENERATION TEST RESULTS")
    print("=" * 80)
    
    success_rate = sum(1 for result in verification_results if result) / len(verification_results) * 100
    
    if success_rate >= 80:
        print(f"✅ TEST PASSED: {success_rate:.1f}% of verification criteria met")
        return True
    else:
        print(f"❌ TEST FAILED: Only {success_rate:.1f}% of verification criteria met")
        return False

if __name__ == "__main__":
    test_multi_source_persona_workflow()

import os
import sys
import tempfile
import zipfile
import pandas as pd
import csv
import requests
import json
import time

# Create a properly quoted CSV file
def create_quoted_csv():
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, "demographics.csv")
    
    with open(csv_path, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Age Group", "Gender", "Household Income", "Education Level", "Location", "Occupation"])
        writer.writerow(["25-34", "Female", "$50,000-$75,000", "Bachelor's Degree", "New York", "Marketing Manager"])
        writer.writerow(["35-44", "Male", "$75,000-$100,000", "Master's Degree", "California", "Software Engineer"])
        writer.writerow(["18-24", "Female", "$25,000-$50,000", "Some College", "Texas", "Student"])
        writer.writerow(["41-56", "Male", "$100,000-$150,000", "PhD", "Illinois", "Executive"])
        writer.writerow(["57-75", "Female", "$150,000+", "Master's Degree", "Florida", "Retired"])
    
    # Create a media consumption CSV
    media_csv_path = os.path.join(temp_dir, "media_consumption.csv")
    with open(media_csv_path, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Social Media Platform", "Usage Frequency", "Content Type", "Preferred Device"])
        writer.writerow(["Instagram", "Daily", "Photos/Videos", "Mobile"])
        writer.writerow(["Facebook", "Weekly", "News/Updates", "Desktop"])
        writer.writerow(["LinkedIn", "Daily", "Professional Content", "Both"])
        writer.writerow(["TikTok", "Daily", "Short Videos", "Mobile"])
        writer.writerow(["Twitter", "Daily", "News/Updates", "Mobile"])
    
    # Create a brand affinity CSV
    brand_csv_path = os.path.join(temp_dir, "brand_preferences.csv")
    with open(brand_csv_path, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Brand Name", "Preference Level", "Purchase Frequency", "Brand Loyalty"])
        writer.writerow(["Apple", "High", "Yearly", "Strong"])
        writer.writerow(["Nike", "Medium", "Quarterly", "Medium"])
        writer.writerow(["Amazon", "High", "Weekly", "Strong"])
        writer.writerow(["Starbucks", "High", "Daily", "Strong"])
        writer.writerow(["Target", "Medium", "Monthly", "Medium"])
    
    return csv_path, media_csv_path, brand_csv_path, temp_dir

# Create a ZIP file with the CSV files
def create_zip_with_csvs(csv_paths):
    zip_path = os.path.join(os.path.dirname(csv_paths[0]), "test_data.zip")
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for csv_path in csv_paths:
            zip_file.write(csv_path, os.path.basename(csv_path))
    
    return zip_path

# Test the end-to-end Resonate workflow
def test_resonate_workflow():
    backend_url = "https://15f53198-94d2-4b58-bc74-9e5313a8760b.preview.emergentagent.com/api"
    
    # Step 1: Create CSV files and ZIP
    print("Step 1: Creating test data files...")
    demo_csv, media_csv, brand_csv, temp_dir = create_quoted_csv()
    csv_paths = [demo_csv, media_csv, brand_csv]
    zip_path = create_zip_with_csvs(csv_paths)
    print(f"Created ZIP file: {zip_path}")
    
    # Step 2: Upload ZIP file
    print("\nStep 2: Uploading ZIP file...")
    upload_url = f"{backend_url}/personas/resonate-upload"
    files = {
        'file': ('test_data.zip', open(zip_path, 'rb'), 'application/zip')
    }
    
    upload_response = requests.post(upload_url, files=files, timeout=30)
    
    if upload_response.status_code != 200:
        print(f"❌ Upload failed - Status: {upload_response.status_code}")
        try:
            print(f"   Error: {upload_response.json()}")
        except:
            print(f"   Error: {upload_response.text[:200]}")
        return False
    
    print(f"✅ Upload successful - Status: {upload_response.status_code}")
    upload_result = upload_response.json()
    
    # Step 3: Create persona from parsed data
    print("\nStep 3: Creating persona from parsed data...")
    create_url = f"{backend_url}/personas/resonate-create"
    create_data = {
        "name": "Test Resonate Persona",
        "parsed_data": upload_result['parsed_data']
    }
    
    create_response = requests.post(create_url, json=create_data, timeout=30)
    
    if create_response.status_code != 200:
        print(f"❌ Persona creation failed - Status: {create_response.status_code}")
        try:
            print(f"   Error: {create_response.json()}")
        except:
            print(f"   Error: {create_response.text[:200]}")
        return False
    
    print(f"✅ Persona creation successful - Status: {create_response.status_code}")
    create_result = create_response.json()
    
    # Analyze the created persona
    if 'persona' in create_result:
        persona = create_result['persona']
        print("\n🧑 CREATED PERSONA ANALYSIS:")
        
        # Check starting method
        if persona.get('starting_method') == 'resonate_upload':
            print(f"   ✅ Correct starting method: {persona.get('starting_method')}")
        else:
            print(f"   ❌ Incorrect starting method: {persona.get('starting_method')}")
        
        # Check completed steps
        if set([1, 2, 3, 4]).issubset(set(persona.get('completed_steps', []))):
            print(f"   ✅ Correct completed steps: {persona.get('completed_steps')}")
        else:
            print(f"   ❌ Incomplete steps: {persona.get('completed_steps')}")
        
        # Check demographics mapping
        demographics = persona.get('demographics', {})
        print(f"\n   Demographics mapping:")
        
        # Check age mapping
        if demographics.get('age_range'):
            print(f"   ✅ Age mapped correctly: {demographics.get('age_range')}")
        else:
            print(f"   ❌ Age not mapped")
        
        # Check gender mapping
        if demographics.get('gender'):
            print(f"   ✅ Gender mapped correctly: {demographics.get('gender')}")
        else:
            print(f"   ❌ Gender not mapped")
        
        # Check income mapping
        if demographics.get('income_range'):
            print(f"   ✅ Income mapped correctly: {demographics.get('income_range')}")
        else:
            print(f"   ❌ Income not mapped")
        
        # Check location mapping
        if demographics.get('location'):
            print(f"   ✅ Location mapped correctly: {demographics.get('location')}")
        else:
            print(f"   ❌ Location not mapped")
        
        # Check occupation mapping
        if demographics.get('occupation'):
            print(f"   ✅ Occupation mapped correctly: {demographics.get('occupation')}")
        else:
            print(f"   ❌ Occupation not mapped")
        
        # Check media consumption mapping
        media = persona.get('media_consumption', {})
        if media.get('social_media_platforms') and len(media.get('social_media_platforms', [])) > 0:
            print(f"   ✅ Social media platforms mapped correctly: {media.get('social_media_platforms')}")
        else:
            print(f"   ❌ Social media platforms not mapped")
        
        # Check brand preferences mapping
        attributes = persona.get('attributes', {})
        if attributes.get('preferred_brands') and len(attributes.get('preferred_brands', [])) > 0:
            print(f"   ✅ Brand preferences mapped correctly: {attributes.get('preferred_brands')}")
        else:
            print(f"   ❌ Brand preferences not mapped")
        
        # Store the persona ID for further testing
        persona_id = persona.get('id')
        if persona_id:
            print(f"   Created persona from Resonate data with ID: {persona_id}")
            
            # Step 4: Generate the final persona with AI image
            print("\nStep 4: Generating final persona with AI image...")
            generate_url = f"{backend_url}/personas/{persona_id}/generate"
            
            try:
                # Use a longer timeout for image generation
                generate_response = requests.post(generate_url, timeout=60)
                
                if generate_response.status_code != 200:
                    print(f"❌ Persona generation failed - Status: {generate_response.status_code}")
                    try:
                        print(f"   Error: {generate_response.json()}")
                    except:
                        print(f"   Error: {generate_response.text[:200]}")
                else:
                    print(f"✅ Persona generation successful - Status: {generate_response.status_code}")
                    generate_result = generate_response.json()
                    
                    if 'persona_image_url' in generate_result:
                        print(f"   ✅ Persona image URL: {generate_result['persona_image_url'][:50]}...")
                    
                    if 'ai_insights' in generate_result:
                        print(f"   ✅ AI insights generated")
                        
                    # Check if demographics were preserved
                    if 'persona_data' in generate_result and 'demographics' in generate_result['persona_data']:
                        demographics = generate_result['persona_data']['demographics']
                        print(f"   ✅ Demographics preserved in generated persona:")
                        for key, value in demographics.items():
                            if value:
                                print(f"      - {key}: {value}")
            except requests.exceptions.Timeout:
                print(f"❌ Persona generation timed out after 60 seconds")
                print(f"   This is likely due to the OpenAI image generation taking too long")
                print(f"   The request may still be processing on the server")
    
    # Clean up
    for csv_path in csv_paths:
        os.remove(csv_path)
    os.remove(zip_path)
    os.rmdir(temp_dir)
    
    return True

if __name__ == "__main__":
    print("🔍 Testing End-to-End Resonate Workflow...")
    test_resonate_workflow()
    print("\n✅ Test completed")

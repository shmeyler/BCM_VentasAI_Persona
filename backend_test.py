
import requests
import sys
import os
import json
import zipfile
import tempfile
from datetime import datetime
import time

class VentasAIPersonaGeneratorTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.persona_id = None
        self.generated_persona_id = None
        self.test_results = {}

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        if not files:  # Don't set Content-Type for multipart/form-data
            headers['Content-Type'] = 'application/json'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, timeout=30)  # Longer timeout for file uploads
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and len(str(response_data)) < 500:
                        print(f"   Response: {response_data}")
                    elif isinstance(response_data, list):
                        print(f"   Response: List with {len(response_data)} items")
                    else:
                        print(f"   Response: Large data object")
                except:
                    print(f"   Response: Non-JSON response")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text[:200]}")

            # Store test result
            self.test_results[name] = {
                "success": success,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "endpoint": endpoint,
                "method": method
            }

            return success, response.json() if success and response.content else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results[name] = {
                "success": False,
                "error": str(e),
                "endpoint": endpoint,
                "method": method
            }
            return False, {}

    # 1. Basic API Health Check
    def test_api_root(self):
        """Test API root endpoint for basic connectivity"""
        success, response = self.run_test(
            "API Root Health Check",
            "GET",
            "",
            200
        )
        return success

    # 2. Persona Creation Workflow
    def test_create_persona(self):
        """Test creating a new persona with demographics data"""
        success, response = self.run_test(
            "Create Persona with Demographics",
            "POST",
            "personas",
            200,
            data={
                "starting_method": "demographics",
                "name": "Marketing Professional"
            }
        )
        if success and 'id' in response:
            self.persona_id = response['id']
            print(f"   Created persona with ID: {self.persona_id}")
        return success

    def test_get_persona(self):
        """Test retrieving a specific persona"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Get Persona",
            "GET",
            f"personas/{self.persona_id}",
            200
        )
        return success

    def test_update_persona_demographics(self):
        """Test updating persona with demographics data"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Update Persona Demographics",
            "PUT",
            f"personas/{self.persona_id}",
            200,
            data={
                "name": "Marketing Manager",
                "demographics": {
                    "age_range": "25-40",
                    "gender": "Female",
                    "income_range": "$75,000-$100,000",
                    "education": "Bachelor's Degree",
                    "location": "Urban",
                    "occupation": "Marketing Manager",
                    "family_status": "Single"
                },
                "current_step": 2,
                "completed_steps": [1]
            }
        )
        return success

    def test_update_persona_attributes(self):
        """Test updating persona with attributes data"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Update Persona Attributes",
            "PUT",
            f"personas/{self.persona_id}",
            200,
            data={
                "attributes": {
                    "selectedVertical": "Retail",
                    "selectedCategory": "Preferences & Psychographics",
                    "selectedBehaviors": ["Quality-focused", "Brand loyal", "Sustainable shopping"],
                    "interests": ["Digital marketing", "Social media", "Content creation", "Data analytics"],
                    "behaviors": ["Research-oriented", "Early adopter", "Mobile-first"],
                    "values": ["Innovation", "Efficiency", "Collaboration"],
                    "purchase_motivations": ["Quality", "Brand reputation", "Value for money"],
                    "preferred_brands": ["Apple", "Nike", "Starbucks", "Adobe"],
                    "lifestyle": ["Urban professional", "Tech-savvy", "Health-conscious"]
                },
                "current_step": 3,
                "completed_steps": [1, 2]
            }
        )
        return success

    def test_update_persona_media_consumption(self):
        """Test updating persona with media consumption data"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Update Persona Media Consumption",
            "PUT",
            f"personas/{self.persona_id}",
            200,
            data={
                "media_consumption": {
                    "social_media_platforms": ["Instagram", "LinkedIn", "Twitter", "TikTok"],
                    "content_types": ["Industry news", "How-to guides", "Case studies", "Infographics"],
                    "consumption_time": "Evening",
                    "preferred_devices": ["Smartphone", "Laptop"],
                    "news_sources": ["Industry blogs", "LinkedIn", "Digital marketing publications"],
                    "entertainment_preferences": ["Podcasts", "Streaming services", "Business books"],
                    "advertising_receptivity": "Medium"
                },
                "current_step": 4,
                "completed_steps": [1, 2, 3]
            }
        )
        return success

    # 3. OpenAI Integration Test
    def test_generate_persona(self):
        """Test generating the final persona with AI image generation"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        # Use a longer timeout for OpenAI image generation
        url = f"{self.base_url}/personas/{self.persona_id}/generate"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing Generate Persona with AI Image...")
        print(f"   URL: {url}")
        
        try:
            # Use a longer timeout (60 seconds) for this specific request
            response = requests.post(url, headers=headers, timeout=60)
            
            success = response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                response_data = response.json()
                
                # Check if persona image URL is generated
                if 'persona_image_url' in response_data:
                    print(f"   ✅ Persona image URL generated: {response_data['persona_image_url'][:50]}...")
                    # Store the generated persona ID for later tests
                    if 'id' in response_data:
                        self.generated_persona_id = response_data['id']
                if 'ai_insights' in response_data:
                    print(f"   ✅ AI insights generated")
                
                # Store test result
                self.test_results["Generate Persona with AI Image"] = {
                    "success": True,
                    "status_code": response.status_code,
                    "expected_status": 200,
                    "endpoint": f"personas/{self.persona_id}/generate",
                    "method": "POST"
                }
                
                return True, response_data
            else:
                print(f"❌ Failed - Expected 200, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text[:200]}")
                
                # Store test result
                self.test_results["Generate Persona with AI Image"] = {
                    "success": False,
                    "status_code": response.status_code,
                    "expected_status": 200,
                    "endpoint": f"personas/{self.persona_id}/generate",
                    "method": "POST"
                }
                
                return False, {}
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            
            # Store test result
            self.test_results["Generate Persona with AI Image"] = {
                "success": False,
                "error": str(e),
                "endpoint": f"personas/{self.persona_id}/generate",
                "method": "POST"
            }
            
            return False, {}

    # 4. Data Sources Integration
    def test_data_sources_status(self):
        """Test data sources status endpoint"""
        # Use a longer timeout for data sources status
        url = f"{self.base_url}/data-sources/status"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing Data Sources Status...")
        print(f"   URL: {url}")
        
        try:
            # Use a longer timeout (30 seconds) for this specific request
            response = requests.get(url, headers=headers, timeout=30)
            
            success = response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                response_data = response.json()
                print(f"   Data sources status: {response_data}")
                
                # Store test result
                self.test_results["Data Sources Status"] = {
                    "success": True,
                    "status_code": response.status_code,
                    "expected_status": 200,
                    "endpoint": "data-sources/status",
                    "method": "GET"
                }
                
                return True, response_data
            else:
                print(f"❌ Failed - Expected 200, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text[:200]}")
                
                # Store test result
                self.test_results["Data Sources Status"] = {
                    "success": False,
                    "status_code": response.status_code,
                    "expected_status": 200,
                    "endpoint": "data-sources/status",
                    "method": "GET"
                }
                
                return False, {}
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            
            # Store test result
            self.test_results["Data Sources Status"] = {
                "success": False,
                "error": str(e),
                "endpoint": "data-sources/status",
                "method": "GET"
            }
            
            return False, {}

    def test_data_sources_demo(self):
        """Test data sources demo endpoint"""
        success, response = self.run_test(
            "Data Sources Demo",
            "GET",
            "data-sources/demo",
            200
        )
        
        if success:
            print(f"   ✅ Demo data retrieved successfully")
            if 'search_insights' in response:
                print(f"   ✅ Search insights data available")
            if 'audience_insights' in response:
                print(f"   ✅ Audience insights data available")
            if 'social_insights' in response:
                print(f"   ✅ Social insights data available")
        
        return success

    def test_persona_insights(self):
        """Test persona insights endpoint"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Persona Insights",
            "GET",
            f"personas/{self.persona_id}/insights",
            200
        )
        
        if success:
            print(f"   ✅ Persona insights retrieved successfully")
        
        return success

    # 5. File Upload Functionality
    def create_test_csv_file(self):
        """Create a test CSV file with realistic demographic data"""
        temp_dir = tempfile.mkdtemp()
        csv_path = os.path.join(temp_dir, "demographics.csv")
        
        with open(csv_path, 'w') as f:
            f.write("Age Group,Gender,Household Income,Education Level,Location,Occupation\n")
            f.write("25-34,Female,$50,000-$75,000,Bachelor's Degree,New York,Marketing Manager\n")
            f.write("35-44,Male,$75,000-$100,000,Master's Degree,California,Software Engineer\n")
            f.write("18-24,Female,$25,000-$50,000,Some College,Texas,Student\n")
            f.write("41-56,Male,$100,000-$150,000,PhD,Illinois,Executive\n")
            f.write("57-75,Female,$150,000+,Master's Degree,Florida,Retired\n")
        
        return csv_path
    
    def test_direct_csv_parsing(self):
        """Test the CSV parsing logic directly"""
        # Create a test CSV file
        csv_path = self.create_test_csv_file()
        
        print("\n🔍 Testing Direct CSV Parsing...")
        print(f"   CSV file: {csv_path}")
        
        try:
            # Import the parser module
            import sys
            import os
            sys.path.insert(0, '/app/backend')
            from external_integrations.file_parsers import ResonateFileParser
            
            # Create parser instance
            parser = ResonateFileParser()
            
            # Parse the CSV file
            result = parser.parse_csv(csv_path)
            
            if 'insights' in result:
                insights = result['insights']
                print("\n📊 CSV PARSING RESULTS:")
                
                # Check demographics
                if 'demographics' in insights:
                    demo_data = insights['demographics']
                    print(f"   Demographics fields found: {', '.join(demo_data.keys())}")
                    
                    # Check specific demographic fields
                    for field in ['age', 'gender', 'income', 'education', 'location', 'occupation']:
                        if field in demo_data:
                            print(f"   ✅ {field.capitalize()} data extracted successfully")
                            # Print sample of the data
                            sample = demo_data[field]['top_values']
                            print(f"      Source column: {demo_data[field]['source_column']}")
                            print(f"      Sample values: {list(sample.keys())[:3]}")
                        else:
                            print(f"   ❌ {field.capitalize()} data not found")
                else:
                    print(f"   ❌ No demographics data found in parsed results")
            
            # Clean up
            os.remove(csv_path)
            return True
            
        except Exception as e:
            print(f"❌ Error testing CSV parsing: {str(e)}")
            # Clean up
            os.remove(csv_path)
            return False

    def test_resonate_upload(self):
        """Test uploading a valid ZIP file to resonate-upload endpoint"""
        # Create a test ZIP file
        zip_path = self.create_test_zip_file()
        
        files = {
            'file': ('test_data.zip', open(zip_path, 'rb'), 'application/zip')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Valid ZIP File",
            "POST",
            "personas/resonate-upload",
            200,
            files=files
        )
        
        # Clean up
        os.remove(zip_path)
        
        # Check if the response contains parsed data
        if success and response.get('success') and 'extracted_files' in response:
            print(f"   ✅ ZIP file processed successfully")
            print(f"   ✅ Extracted {len(response['extracted_files'])} files")
            
            # Check if parsed_data is present
            if 'parsed_data' in response:
                print(f"   ✅ Data parsed successfully")
        
        return success
        
    def test_resonate_upload_realistic(self):
        """Test uploading a realistic ZIP file with proper column names"""
        # Create a realistic test ZIP file
        zip_path = self.create_test_zip_file("realistic")
        
        files = {
            'file': ('realistic_data.zip', open(zip_path, 'rb'), 'application/zip')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Realistic Data",
            "POST",
            "personas/resonate-upload",
            200,
            files=files
        )
        
        # Clean up
        os.remove(zip_path)
        
        # Detailed analysis of the parsed data
        if success and response.get('success') and 'parsed_data' in response:
            parsed_data = response['parsed_data']
            print(f"\n📊 PARSED DATA ANALYSIS:")
            
            # Check demographics
            if 'demographics' in parsed_data:
                demo_data = parsed_data['demographics']
                print(f"   Demographics fields found: {', '.join(demo_data.keys())}")
                
                # Check specific demographic fields
                for field in ['age', 'gender', 'income', 'education', 'location', 'occupation']:
                    if field in demo_data:
                        print(f"   ✅ {field.capitalize()} data extracted successfully")
                        # Print sample of the data
                        sample = demo_data[field][0]['data']['top_values']
                        print(f"      Sample values: {list(sample.keys())[:3]}")
                    else:
                        print(f"   ❌ {field.capitalize()} data not found")
            else:
                print(f"   ❌ No demographics data found in parsed results")
            
            # Check media consumption
            if 'media_consumption' in parsed_data:
                media_data = parsed_data['media_consumption']
                print(f"   Media consumption fields found: {', '.join(media_data.keys())}")
                
                # Check for social media platforms
                social_platforms = []
                for key, value in media_data.items():
                    if 'social' in key.lower() or 'platform' in key.lower():
                        social_platforms.append(key)
                
                if social_platforms:
                    print(f"   ✅ Social media platform data extracted successfully")
                    for platform in social_platforms:
                        sample = media_data[platform][0]['data']
                        print(f"      Platform: {platform}, Values: {list(sample.keys())[:3]}")
                else:
                    print(f"   ❌ No social media platform data found")
            else:
                print(f"   ❌ No media consumption data found in parsed results")
            
            # Check brand affinity
            if 'brand_affinity' in parsed_data:
                brand_data = parsed_data['brand_affinity']
                print(f"   Brand affinity fields found: {', '.join(brand_data.keys())}")
                
                if brand_data:
                    for key, value in brand_data.items():
                        sample = brand_data[key][0]['data']
                        print(f"      Brand field: {key}, Values: {list(sample.keys())[:3]}")
                else:
                    print(f"   ❌ No brand preference data found")
            else:
                print(f"   ❌ No brand affinity data found in parsed results")
        
        return success, response.get('parsed_data', {}) if success else {}
    
    def test_resonate_upload_multiple_formats(self):
        """Test uploading a ZIP file with multiple column name formats"""
        # Create a test ZIP file with multiple column name formats
        zip_path = self.create_test_zip_file("multiple_formats")
        
        files = {
            'file': ('multiple_formats.zip', open(zip_path, 'rb'), 'application/zip')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Multiple Column Formats",
            "POST",
            "personas/resonate-upload",
            200,
            files=files
        )
        
        # Clean up
        os.remove(zip_path)
        
        # Check if the parser recognizes different column name formats
        if success and response.get('success') and 'parsed_data' in response:
            parsed_data = response['parsed_data']
            print(f"\n📊 COLUMN FORMAT RECOGNITION ANALYSIS:")
            
            # Check demographics
            if 'demographics' in parsed_data:
                demo_data = parsed_data['demographics']
                print(f"   Demographics fields found: {', '.join(demo_data.keys())}")
                
                # Check if the parser recognized different column name formats
                for field in ['age', 'gender', 'income', 'education', 'location', 'occupation']:
                    if field in demo_data:
                        sources = [item['source'] for item in demo_data[field]]
                        print(f"   ✅ {field.capitalize()} recognized from files: {', '.join(sources)}")
                    else:
                        print(f"   ❌ {field.capitalize()} not recognized from any file")
            else:
                print(f"   ❌ No demographics data found in parsed results")
        
        return success
    
    def test_resonate_upload_error_handling(self):
        """Test error handling for malformed ZIP files"""
        # Create a malformed test ZIP file
        zip_path = self.create_test_zip_file("malformed")
        
        files = {
            'file': ('malformed.zip', open(zip_path, 'rb'), 'application/zip')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Malformed Data",
            "POST",
            "personas/resonate-upload",
            422,  # Expecting a validation error
            files=files
        )
        
        # Clean up
        os.remove(zip_path)
        
        # Check error handling
        if not success and response.get('detail'):
            print(f"   ✅ Error handling works correctly")
            print(f"   Error message: {response.get('detail')}")
        
        return not success  # We expect this test to fail with a 422 error
    
    def test_resonate_upload_non_zip(self):
        """Test uploading a non-ZIP file"""
        # Create a temporary text file
        temp_dir = tempfile.mkdtemp()
        txt_path = os.path.join(temp_dir, "not_a_zip.txt")
        with open(txt_path, 'w') as f:
            f.write("This is not a ZIP file")
        
        files = {
            'file': ('not_a_zip.txt', open(txt_path, 'rb'), 'text/plain')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Non-ZIP File",
            "POST",
            "personas/resonate-upload",
            400,  # Expecting a bad request error
            files=files
        )
        
        # Clean up
        os.remove(txt_path)
        
        # Check error handling
        if not success and response.get('detail'):
            print(f"   ✅ Non-ZIP file rejected correctly")
            print(f"   Error message: {response.get('detail')}")
        
        return not success  # We expect this test to fail with a 400 error

    def test_resonate_create_from_data(self):
        """Test creating a persona from parsed Resonate data"""
        # First upload a realistic file to get actual parsed data
        zip_path = self.create_test_zip_file("realistic")
        
        files = {
            'file': ('realistic_data.zip', open(zip_path, 'rb'), 'application/zip')
        }
        
        # Get the parsed data from upload
        upload_success, upload_response = self.run_test(
            "Upload for Persona Creation",
            "POST",
            "personas/resonate-upload",
            200,
            files=files
        )
        
        # Clean up
        os.remove(zip_path)
        
        if not upload_success or 'parsed_data' not in upload_response:
            print("❌ Failed to get parsed data for persona creation test")
            return False
        
        # Now use the actual parsed data to create a persona
        parsed_data = upload_response['parsed_data']
        
        success, response = self.run_test(
            "Create Persona from Resonate Data",
            "POST",
            "personas/resonate-create",
            200,
            data={
                "name": "Resonate Data Persona",
                "parsed_data": parsed_data
            }
        )
        
        if success and response.get('success') and 'persona' in response:
            persona = response['persona']
            print(f"\n🧑 CREATED PERSONA ANALYSIS:")
            
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
            if 'id' in persona:
                self.resonate_persona_id = persona['id']
                print(f"   Created persona from Resonate data with ID: {persona['id']}")
        
        return success
    
    def test_end_to_end_resonate_workflow(self):
        """Test the complete end-to-end workflow from upload to persona generation"""
        if not hasattr(self, 'resonate_persona_id'):
            print("❌ Skipping - No Resonate persona ID available from previous test")
            return False
        
        # Generate the final persona with AI image
        success, response = self.run_test(
            "Generate Persona from Resonate Data",
            "POST",
            f"personas/{self.resonate_persona_id}/generate",
            200
        )
        
        if success and 'persona_image_url' in response:
            print(f"   ✅ Successfully generated persona with Resonate data")
            print(f"   ✅ Persona image URL: {response['persona_image_url'][:50]}...")
            
            # Check if demographics were preserved
            if 'persona_data' in response and 'demographics' in response['persona_data']:
                demographics = response['persona_data']['demographics']
                print(f"   ✅ Demographics preserved in generated persona:")
                for key, value in demographics.items():
                    if value:
                        print(f"      - {key}: {value}")
        
        return success

    # Additional Tests
    def test_list_personas(self):
        """Test listing all personas"""
        success, response = self.run_test(
            "List Personas",
            "GET",
            "personas",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} personas")
        
        return success

    def test_list_generated_personas(self):
        """Test listing all generated personas"""
        success, response = self.run_test(
            "List Generated Personas",
            "GET",
            "generated-personas",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} generated personas")
        
        return success

    def test_delete_persona(self):
        """Test deleting a persona"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Delete Persona",
            "DELETE",
            f"personas/{self.persona_id}",
            200
        )
        return success

    def print_summary(self):
        """Print a summary of all test results"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        # Group tests by category
        categories = {
            "Basic API Health Check": ["API Root Health Check"],
            "Persona Creation Workflow": [
                "Create Persona with Demographics", 
                "Get Persona", 
                "Update Persona Demographics", 
                "Update Persona Attributes", 
                "Update Persona Media Consumption"
            ],
            "OpenAI Integration": ["Generate Persona with AI Image"],
            "Data Sources Integration": [
                "Data Sources Status", 
                "Data Sources Demo", 
                "Persona Insights"
            ],
            "File Upload Functionality": [
                "Resonate Upload - Valid ZIP File", 
                "Create Persona from Resonate Data"
            ],
            "Additional Tests": [
                "List Personas", 
                "List Generated Personas", 
                "Delete Persona"
            ]
        }
        
        # Print results by category
        for category, tests in categories.items():
            print(f"\n{category}:")
            for test in tests:
                if test in self.test_results:
                    result = self.test_results[test]
                    status = "✅ PASSED" if result["success"] else "❌ FAILED"
                    print(f"  {status} - {test}")
                else:
                    print(f"  ⚠️ NOT RUN - {test}")
        
        # Print overall statistics
        print("\n" + "-" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0:.1f}%")
        print("=" * 60)


def main():
    print("🚀 Starting BCM VentasAI Persona Generator Backend Tests")
    print("=" * 60)
    
    # Get backend URL from frontend/.env
    backend_url = "https://15f53198-94d2-4b58-bc74-9e5313a8760b.preview.emergentagent.com/api"
    print(f"Using backend URL: {backend_url}")
    
    tester = VentasAIPersonaGeneratorTester(backend_url)
    
    # Check if we should run specific tests
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "resonate":
        print("\n🔍 Running focused Resonate data parsing and mapping tests...")
        tests = [
            # API Health Check
            tester.test_api_root,
            
            # Resonate Upload Tests
            tester.test_resonate_upload_realistic,
            tester.test_resonate_upload_multiple_formats,
            tester.test_resonate_upload_error_handling,
            tester.test_resonate_upload_non_zip,
            
            # Resonate Create Tests
            tester.test_resonate_create_from_data,
            tester.test_end_to_end_resonate_workflow
        ]
    else:
        # Define full test sequence
        tests = [
            # 1. Basic API Health Check
            tester.test_api_root,
            
            # 2. Persona Creation Workflow
            tester.test_create_persona,
            tester.test_get_persona,
            tester.test_update_persona_demographics,
            tester.test_update_persona_attributes,
            tester.test_update_persona_media_consumption,
            
            # 3. OpenAI Integration Test
            tester.test_generate_persona,
            
            # 4. Data Sources Integration
            tester.test_data_sources_status,
            tester.test_data_sources_demo,
            tester.test_persona_insights,
            
            # 5. File Upload Functionality
            tester.test_resonate_upload,
            tester.test_resonate_upload_realistic,
            tester.test_resonate_upload_multiple_formats,
            tester.test_resonate_upload_error_handling,
            tester.test_resonate_upload_non_zip,
            tester.test_resonate_create_from_data,
            tester.test_end_to_end_resonate_workflow,
            
            # Additional Tests
            tester.test_list_personas,
            tester.test_list_generated_personas,
            
            # Cleanup
            tester.test_delete_persona
        ]
    
    print(f"\n📋 Running {len(tests)} API tests...")
    
    for test in tests:
        try:
            test()
            # Add a small delay between tests to avoid overwhelming the server
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    # Print summary of results
    tester.print_summary()
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! The BCM VentasAI Persona Generator API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

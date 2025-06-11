
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
    def create_test_zip_file(self):
        """Create a test ZIP file with sample data files"""
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "test_data.zip")
        
        # Create a CSV file with demographic data
        csv_path = os.path.join(temp_dir, "demographics.csv")
        with open(csv_path, 'w') as f:
            f.write("Age,Gender,Income,Location\n")
            f.write("25-34,Female,$50,000-$75,000,Urban\n")
            f.write("35-44,Male,$75,000-$100,000,Suburban\n")
            f.write("18-24,Female,$25,000-$50,000,Urban\n")
        
        # Create a text file with media consumption data
        txt_path = os.path.join(temp_dir, "media.txt")
        with open(txt_path, 'w') as f:
            f.write("Media Consumption Analysis\n\n")
            f.write("Social Media: Instagram, Facebook, TikTok\n")
            f.write("Streaming: Netflix, Hulu, Disney+\n")
            f.write("News: CNN, BBC, Local News\n")
        
        # Create a ZIP file with these files
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.write(csv_path, os.path.basename(csv_path))
            zip_file.write(txt_path, os.path.basename(txt_path))
        
        return zip_path

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

    def test_resonate_create_from_data(self):
        """Test creating a persona from parsed Resonate data"""
        # Mock parsed data that would come from a ZIP file
        mock_parsed_data = {
            "demographics": {
                "age": [
                    {
                        "source": "demographics.csv",
                        "data": {
                            "source_column": "Age",
                            "top_values": {"25-34": 45, "35-44": 30, "18-24": 15}
                        }
                    }
                ],
                "gender": [
                    {
                        "source": "demographics.csv",
                        "data": {
                            "source_column": "Gender",
                            "top_values": {"Female": 60, "Male": 40}
                        }
                    }
                ],
                "income": [
                    {
                        "source": "demographics.csv",
                        "data": {
                            "source_column": "Income",
                            "top_values": {"$50,000-$75,000": 35, "$75,000-$100,000": 25}
                        }
                    }
                ]
            },
            "media_consumption": {
                "social_platforms": [
                    {
                        "source": "media.csv",
                        "data": {
                            "Instagram": 75, "Facebook": 65, "LinkedIn": 45, "TikTok": 30
                        }
                    }
                ]
            },
            "brand_affinity": {
                "preferred_brands": [
                    {
                        "source": "brands.csv",
                        "data": {
                            "Apple": 80, "Nike": 75, "Amazon": 70
                        }
                    }
                ]
            }
        }
        
        success, response = self.run_test(
            "Create Persona from Resonate Data",
            "POST",
            "personas/resonate-create",
            200,
            data={
                "name": "Resonate Data Persona",
                "parsed_data": mock_parsed_data
            }
        )
        
        if success and response.get('success') and 'persona' in response:
            persona = response['persona']
            if 'id' in persona:
                print(f"   Created persona from Resonate data with ID: {persona['id']}")
        
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
    
    # Define test sequence
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
        tester.test_resonate_create_from_data,
        
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

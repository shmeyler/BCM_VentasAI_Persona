import requests
import sys
import os
import json
from datetime import datetime

class ResonateUploadTester:
    def __init__(self, base_url="https://28426961-bcbc-4f0c-9e2c-9ae3cc74eaf5.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.persona_id = None

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

            return success, response.json() if success and response.content else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        success, response = self.run_test(
            "API Root",
            "GET",
            "",
            200
        )
        return success

    def test_create_persona_resonate_upload(self):
        """Test creating a persona with resonate_upload starting method"""
        success, response = self.run_test(
            "Create Persona (Resonate Upload)",
            "POST",
            "personas",
            200,
            data={
                "starting_method": "resonate_upload",
                "name": "Test Resonate Upload Persona"
            }
        )
        if success and 'id' in response:
            self.persona_id = response['id']
            print(f"   Created persona with ID: {self.persona_id}")
        return success

    def test_resonate_upload_invalid_file(self):
        """Test uploading an invalid file type to resonate-upload endpoint"""
        # Create a temporary text file
        with open('/tmp/test.txt', 'w') as f:
            f.write("This is not a ZIP file")
        
        files = {
            'file': ('test.txt', open('/tmp/test.txt', 'rb'), 'text/plain')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Invalid File Type",
            "POST",
            "personas/resonate-upload",
            400,  # Should return 400 Bad Request
            files=files
        )
        
        # Clean up
        os.remove('/tmp/test.txt')
        
        # For this test, success means we got the expected 400 error
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
                self.persona_id = persona['id']
                print(f"   Created persona from Resonate data with ID: {self.persona_id}")
        
        return success

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

    def test_generate_persona(self):
        """Test generating the final persona with AI insights"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Generate Persona",
            "POST",
            f"personas/{self.persona_id}/generate",
            200
        )
        
        if success:
            # Check if persona image URL is generated
            if 'persona_image_url' in response:
                print(f"   ✅ Persona image URL generated: {response['persona_image_url'][:50]}...")
            if 'ai_insights' in response:
                print(f"   ✅ AI insights generated")
        
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

def main():
    print("🚀 Starting BCM VentasAI Persona Generator - Resonate Upload Tests")
    print("=" * 60)
    print("📋 Testing with focus on Resonate Upload functionality")
    
    tester = ResonateUploadTester()
    
    # Test sequence focusing on Resonate Upload functionality
    tests = [
        tester.test_api_root,
        tester.test_create_persona_resonate_upload,
        tester.test_resonate_upload_invalid_file,
        tester.test_resonate_create_from_data,
        tester.test_list_personas,
        tester.test_get_persona,
        tester.test_generate_persona,
        tester.test_delete_persona
    ]
    
    print(f"\n📋 Running {len(tests)} API tests...")
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! Resonate Upload functionality is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
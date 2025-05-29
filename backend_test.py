
import requests
import sys
import os
import json
import zipfile
import tempfile
from datetime import datetime

class ResonateUploadTester:
    def __init__(self, base_url="http://localhost:8001/api"):
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

    def test_resonate_upload_valid_zip(self):
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
            200,  # Should return 200 OK
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
                
                # Check if demographics were extracted
                if 'demographics' in response['parsed_data'] and response['parsed_data']['demographics']:
                    print(f"   ✅ Demographics data extracted")
                else:
                    print(f"   ⚠️ No demographics data extracted")
                
                # Check if media consumption was extracted
                if 'media_consumption' in response['parsed_data'] and response['parsed_data']['media_consumption']:
                    print(f"   ✅ Media consumption data extracted")
                else:
                    print(f"   ⚠️ No media consumption data extracted")
        
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
    print("🚀 Starting BCM VentasAI Persona Generator - Resonate Upload Backend Tests")
    print("=" * 60)
    print("📋 Testing with focus on Resonate Upload functionality")
    
    # Use the local backend URL for testing
    tester = ResonateUploadTester("http://localhost:8001/api")
    
    # Test sequence focusing on Resonate Upload functionality
    tests = [
        tester.test_api_root,
        tester.test_create_persona_resonate_upload,
        tester.test_resonate_upload_invalid_file,
        tester.test_resonate_upload_valid_zip,
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

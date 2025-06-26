import requests
import sys
import os
import json
import zipfile
import tempfile
import csv
import io
import time
from datetime import datetime

class ResonateUploadTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = {}
        self.persona_id = None
        self.generated_persona_id = None
        self.parsed_data = None

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

    def create_realistic_resonate_zip(self):
        """Create a realistic Resonate-style ZIP file with demographic CSV data"""
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "resonate_data.zip")
        
        # Create demographics CSV file
        demographics_path = os.path.join(temp_dir, "demographics.csv")
        with open(demographics_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Age Group", "Gender", "Household Income", "Education Level", "Location", "Occupation"])
            writer.writerow(["25-34", "Female", "$75,000-$100,000", "Bachelor's Degree", "Urban", "Marketing Manager"])
            writer.writerow(["35-44", "Male", "$100,000-$150,000", "Master's Degree", "Suburban", "IT Director"])
            writer.writerow(["18-24", "Female", "$50,000-$75,000", "Some College", "Urban", "Digital Content Creator"])
            writer.writerow(["45-54", "Male", "$150,000+", "PhD", "Suburban", "Executive"])
            writer.writerow(["25-34", "Female", "$75,000-$100,000", "Bachelor's Degree", "Urban", "Product Manager"])
        
        # Create media consumption CSV file
        media_path = os.path.join(temp_dir, "media_consumption.csv")
        with open(media_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Social Platform", "Usage Frequency", "Content Type", "Device"])
            writer.writerow(["Instagram", "Daily", "Photos/Videos", "Mobile"])
            writer.writerow(["LinkedIn", "Weekly", "Professional", "Desktop"])
            writer.writerow(["Twitter", "Daily", "News/Updates", "Mobile"])
            writer.writerow(["TikTok", "Daily", "Short Videos", "Mobile"])
            writer.writerow(["YouTube", "Daily", "Long-form Videos", "Multiple"])
            writer.writerow(["Facebook", "Weekly", "Social Updates", "Multiple"])
        
        # Create brand affinity CSV file
        brands_path = os.path.join(temp_dir, "brand_affinity.csv")
        with open(brands_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Brand", "Affinity Score", "Purchase Intent", "Category"])
            writer.writerow(["Apple", "85", "High", "Technology"])
            writer.writerow(["Nike", "78", "Medium", "Apparel"])
            writer.writerow(["Starbucks", "72", "High", "Food & Beverage"])
            writer.writerow(["Amazon", "90", "High", "Retail"])
            writer.writerow(["Netflix", "82", "High", "Entertainment"])
            writer.writerow(["Spotify", "75", "Medium", "Entertainment"])
        
        # Create a text file with additional insights
        insights_path = os.path.join(temp_dir, "audience_insights.txt")
        with open(insights_path, 'w') as f:
            f.write("Resonate Audience Insights Report\n\n")
            f.write("Key Demographics:\n")
            f.write("- Primary age group: 25-34 (Millennials)\n")
            f.write("- Gender split: 60% Female, 40% Male\n")
            f.write("- Income: Primarily $75,000-$100,000\n\n")
            f.write("Media Consumption Patterns:\n")
            f.write("- Heavy social media users (Instagram, LinkedIn, Twitter)\n")
            f.write("- Mobile-first content consumption\n")
            f.write("- Streaming services preferred over traditional TV\n\n")
            f.write("Brand Preferences:\n")
            f.write("- Technology: Apple, Samsung\n")
            f.write("- Retail: Amazon, Target\n")
            f.write("- Apparel: Nike, Lululemon\n")
        
        # Create ZIP file with these files
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.write(demographics_path, os.path.basename(demographics_path))
            zip_file.write(media_path, os.path.basename(media_path))
            zip_file.write(brands_path, os.path.basename(brands_path))
            zip_file.write(insights_path, os.path.basename(insights_path))
        
        return zip_path

    def create_malformed_zip(self):
        """Create a malformed ZIP file for testing error handling"""
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "malformed.zip")
        
        # Create a file with random data
        with open(zip_path, 'wb') as f:
            f.write(b'This is not a valid ZIP file content')
        
        return zip_path

    def create_empty_zip(self):
        """Create an empty ZIP file for testing error handling"""
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "empty.zip")
        
        # Create an empty ZIP file
        with zipfile.ZipFile(zip_path, 'w'):
            pass
        
        return zip_path

    def test_resonate_upload_endpoint_access(self):
        """Test if the Resonate upload endpoint is accessible"""
        # Just check if the endpoint responds (even with an error for missing file)
        success, response = self.run_test(
            "Resonate Upload Endpoint Access",
            "POST",
            "personas/resonate-upload",
            422,  # Expect unprocessable entity for missing file
            data={}
        )
        return success

    def test_resonate_upload_valid_zip(self):
        """Test uploading a valid Resonate ZIP file"""
        # Create a realistic Resonate ZIP file
        zip_path = self.create_realistic_resonate_zip()
        
        files = {
            'file': ('resonate_data.zip', open(zip_path, 'rb'), 'application/zip')
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
        
        # Store parsed data for later tests
        if success and response.get('success') and 'parsed_data' in response:
            self.parsed_data = response['parsed_data']
            
            # Print detailed information about the parsed data
            print("\n📊 Parsed Data Analysis:")
            
            # Demographics
            if 'demographics' in self.parsed_data:
                print("   Demographics data found:")
                for key, values in self.parsed_data['demographics'].items():
                    print(f"   - {key}: {len(values)} source(s)")
            
            # Media consumption
            if 'media_consumption' in self.parsed_data:
                print("   Media consumption data found:")
                for key, values in self.parsed_data['media_consumption'].items():
                    print(f"   - {key}: {len(values)} source(s)")
            
            # Brand affinity
            if 'brand_affinity' in self.parsed_data:
                print("   Brand affinity data found:")
                for key, values in self.parsed_data['brand_affinity'].items():
                    print(f"   - {key}: {len(values)} source(s)")
            
            # Source files
            if 'source_files' in self.parsed_data:
                print(f"   Processed {len(self.parsed_data['source_files'])} files:")
                for file_info in self.parsed_data['source_files']:
                    status = "✅ Processed" if file_info.get('processed') else "❌ Failed"
                    print(f"   - {file_info.get('name')}: {status}")
        
        return success

    def test_resonate_upload_malformed_zip(self):
        """Test uploading a malformed ZIP file"""
        # Create a malformed ZIP file
        zip_path = self.create_malformed_zip()
        
        files = {
            'file': ('malformed.zip', open(zip_path, 'rb'), 'application/zip')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Malformed ZIP File",
            "POST",
            "personas/resonate-upload",
            500,  # Expect server error for malformed ZIP
            files=files
        )
        
        # Clean up
        os.remove(zip_path)
        
        # For this test, success means the API correctly rejected the malformed file
        return success

    def test_resonate_upload_empty_zip(self):
        """Test uploading an empty ZIP file"""
        # Create an empty ZIP file
        zip_path = self.create_empty_zip()
        
        files = {
            'file': ('empty.zip', open(zip_path, 'rb'), 'application/zip')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Empty ZIP File",
            "POST",
            "personas/resonate-upload",
            200,  # Should accept the ZIP but find no data
            files=files
        )
        
        # Clean up
        os.remove(zip_path)
        
        # Check if the response indicates no useful data was found
        if success and 'parsed_data' in response:
            empty_data = True
            for key in ['demographics', 'media_consumption', 'brand_affinity']:
                if response['parsed_data'].get(key) and len(response['parsed_data'][key]) > 0:
                    empty_data = False
                    break
            
            if empty_data:
                print("   ✅ Empty ZIP correctly resulted in no parsed data")
            else:
                print("   ❌ Empty ZIP unexpectedly produced data")
        
        return success

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
            400,  # Expect bad request for non-ZIP
            files=files
        )
        
        # Clean up
        os.remove(txt_path)
        
        # For this test, success means the API correctly rejected the non-ZIP file
        return success

    def test_create_persona_from_resonate_data(self):
        """Test creating a persona from parsed Resonate data"""
        if not self.parsed_data:
            print("❌ Skipping - No parsed data available")
            return False
        
        success, response = self.run_test(
            "Create Persona from Resonate Data",
            "POST",
            "personas/resonate-create",
            200,
            data={
                "name": "Resonate Test Persona",
                "parsed_data": self.parsed_data
            }
        )
        
        if success and response.get('success') and 'persona' in response:
            persona = response['persona']
            if 'id' in persona:
                self.persona_id = persona['id']
                print(f"   Created persona from Resonate data with ID: {self.persona_id}")
            
            # Verify the persona has the correct starting method
            if persona.get('starting_method') == 'resonate_upload':
                print("   ✅ Persona has correct starting method: resonate_upload")
            else:
                print(f"   ❌ Persona has incorrect starting method: {persona.get('starting_method')}")
            
            # Verify completed steps
            if 'completed_steps' in persona and set(persona['completed_steps']) >= {1, 2, 3, 4}:
                print(f"   ✅ Persona has correct completed steps: {persona['completed_steps']}")
            else:
                print(f"   ❌ Persona has incorrect completed steps: {persona.get('completed_steps', [])}")
            
            # Verify demographics mapping
            if 'demographics' in persona:
                demographics = persona['demographics']
                print("   Demographics mapping:")
                for field in ['age_range', 'gender', 'income_range', 'location', 'occupation']:
                    if field in demographics and demographics[field]:
                        print(f"   ✅ {field}: {demographics[field]}")
                    else:
                        print(f"   ❌ {field}: Missing or empty")
            
            # Verify media consumption mapping
            if 'media_consumption' in persona:
                media = persona['media_consumption']
                if 'social_media_platforms' in media and media['social_media_platforms']:
                    print(f"   ✅ social_media_platforms: {media['social_media_platforms']}")
                else:
                    print("   ❌ social_media_platforms: Missing or empty")
            
            # Verify attributes mapping (brand preferences)
            if 'attributes' in persona:
                attributes = persona['attributes']
                if 'preferred_brands' in attributes and attributes['preferred_brands']:
                    print(f"   ✅ preferred_brands: {attributes['preferred_brands']}")
                else:
                    print("   ❌ preferred_brands: Missing or empty")
        
        return success

    def test_generate_persona_from_resonate(self):
        """Test generating a final persona from Resonate-created persona"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False
        
        # Use a longer timeout for OpenAI image generation
        url = f"{self.base_url}/personas/{self.persona_id}/generate"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing Generate Persona from Resonate Data...")
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
                self.test_results["Generate Persona from Resonate Data"] = {
                    "success": True,
                    "status_code": response.status_code,
                    "expected_status": 200,
                    "endpoint": f"personas/{self.persona_id}/generate",
                    "method": "POST"
                }
                
                return True
            else:
                print(f"❌ Failed - Expected 200, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text[:200]}")
                
                # Store test result
                self.test_results["Generate Persona from Resonate Data"] = {
                    "success": False,
                    "status_code": response.status_code,
                    "expected_status": 200,
                    "endpoint": f"personas/{self.persona_id}/generate",
                    "method": "POST"
                }
                
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            
            # Store test result
            self.test_results["Generate Persona from Resonate Data"] = {
                "success": False,
                "error": str(e),
                "endpoint": f"personas/{self.persona_id}/generate",
                "method": "POST"
            }
            
            return False

    def print_summary(self):
        """Print a summary of all test results"""
        print("\n" + "=" * 60)
        print("📊 RESONATE UPLOAD TESTING RESULTS")
        print("=" * 60)
        
        # Group tests by category
        categories = {
            "File Upload Endpoint Testing": [
                "Resonate Upload Endpoint Access",
                "Resonate Upload - Valid ZIP File",
                "Resonate Upload - Malformed ZIP File",
                "Resonate Upload - Empty ZIP File",
                "Resonate Upload - Non-ZIP File"
            ],
            "Persona Creation Testing": [
                "Create Persona from Resonate Data"
            ],
            "End-to-End Workflow": [
                "Generate Persona from Resonate Data"
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
    print("🚀 Starting BCM VentasAI Resonate Upload Testing")
    print("=" * 60)
    
    # Get backend URL from frontend/.env
    backend_url = "https://28426961-bcbc-4f0c-9e2c-9ae3cc74eaf5.preview.emergentagent.com/api"
    print(f"Using backend URL: {backend_url}")
    
    tester = ResonateUploadTester(backend_url)
    
    # Define test sequence
    tests = [
        # 1. File Upload Endpoint Testing
        tester.test_resonate_upload_endpoint_access,
        tester.test_resonate_upload_valid_zip,
        tester.test_resonate_upload_malformed_zip,
        tester.test_resonate_upload_empty_zip,
        tester.test_resonate_upload_non_zip,
        
        # 2. Persona Creation Testing
        tester.test_create_persona_from_resonate_data,
        
        # 3. End-to-End Workflow
        tester.test_generate_persona_from_resonate
    ]
    
    print(f"\n📋 Running {len(tests)} Resonate upload tests...")
    
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
        print("🎉 All tests passed! The Resonate data upload functionality is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
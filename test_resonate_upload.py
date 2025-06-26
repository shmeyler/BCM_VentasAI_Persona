import requests
import sys
import os
import json
import zipfile
import tempfile
import csv
import time
from datetime import datetime

class ResonateUploadTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = {}
        self.persona_id = None
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

    def create_realistic_csv_file(self, temp_dir):
        """Create a realistic CSV file with demographic and behavioral data"""
        csv_path = os.path.join(temp_dir, "resonate_demographics.csv")
        
        # Define columns based on test requirements
        columns = [
            "age", "gender", "income", "education", "occupation", 
            "location", "social_media_platforms", "brand_preferences"
        ]
        
        # Create sample data rows
        data_rows = [
            # Row 1: Millennial Professional
            ["25-34", "Female", "$75,000-$100,000", "Bachelor's Degree", "Marketing Manager", 
             "New York, NY", "Instagram,LinkedIn,TikTok", "Apple,Nike,Starbucks"],
            
            # Row 2: Gen X Executive
            ["41-56", "Male", "$150,000+", "Master's Degree", "Senior Executive", 
             "Chicago, IL", "LinkedIn,Twitter,Facebook", "Tesla,Brooks Brothers,Marriott"],
            
            # Row 3: Gen Z Student
            ["18-24", "Non-binary", "$25,000-$50,000", "Some College", "Student/Part-time Retail", 
             "Austin, TX", "TikTok,Instagram,Snapchat", "Adidas,Spotify,Chipotle"],
            
            # Row 4: Boomer Retiree
            ["57-75", "Female", "$50,000-$75,000", "Associate's Degree", "Retired Teacher", 
             "Tampa, FL", "Facebook,Pinterest,YouTube", "Nordstrom,Kohl's,Target"],
            
            # Row 5: Millennial Parent
            ["35-40", "Male", "$100,000-$150,000", "Bachelor's Degree", "Software Engineer", 
             "Seattle, WA", "Reddit,Twitter,YouTube", "Amazon,Nintendo,REI"]
        ]
        
        # Write to CSV file
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(data_rows)
        
        print(f"✅ Created realistic CSV file with {len(data_rows)} demographic profiles")
        return csv_path

    def create_media_consumption_csv(self, temp_dir):
        """Create a CSV file with detailed media consumption data"""
        csv_path = os.path.join(temp_dir, "resonate_media_consumption.csv")
        
        # Define columns
        columns = [
            "age_group", "platform", "hours_per_week", "content_type", 
            "device_preference", "time_of_day", "engagement_level"
        ]
        
        # Create sample data rows
        data_rows = [
            # Row 1: Millennial Instagram
            ["25-34", "Instagram", "10-15", "Visual Stories,Reels", 
             "Mobile", "Evening", "High"],
            
            # Row 2: Millennial LinkedIn
            ["25-34", "LinkedIn", "5-10", "Industry News,Professional Content", 
             "Desktop,Mobile", "Workday", "Medium"],
            
            # Row 3: Gen X Facebook
            ["41-56", "Facebook", "7-12", "Family Updates,News", 
             "Mobile,Tablet", "Evening", "Medium"],
            
            # Row 4: Gen Z TikTok
            ["18-24", "TikTok", "15-20", "Short-form Video,Trending Content", 
             "Mobile", "Throughout Day", "Very High"],
            
            # Row 5: Boomer Facebook
            ["57-75", "Facebook", "10-15", "Family Updates,Community Groups", 
             "Tablet,Desktop", "Morning,Evening", "High"],
            
            # Row 6: Gen Z YouTube
            ["18-24", "YouTube", "10-15", "How-to Videos,Entertainment", 
             "Mobile,Smart TV", "Evening", "High"],
            
            # Row 7: Millennial Podcast
            ["25-40", "Spotify Podcasts", "3-5", "Business,True Crime", 
             "Mobile", "Commute", "Medium"]
        ]
        
        # Write to CSV file
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(data_rows)
        
        print(f"✅ Created media consumption CSV file with {len(data_rows)} entries")
        return csv_path

    def create_brand_preferences_csv(self, temp_dir):
        """Create a CSV file with brand preferences and affinities"""
        csv_path = os.path.join(temp_dir, "resonate_brand_preferences.csv")
        
        # Define columns
        columns = [
            "age_group", "gender", "brand", "category", "affinity_score", 
            "purchase_frequency", "loyalty_level"
        ]
        
        # Create sample data rows
        data_rows = [
            # Row 1: Millennial Female - Apple
            ["25-34", "Female", "Apple", "Technology", "85", 
             "Yearly", "High"],
            
            # Row 2: Millennial Female - Nike
            ["25-34", "Female", "Nike", "Apparel", "78", 
             "Quarterly", "Medium"],
            
            # Row 3: Gen X Male - Tesla
            ["41-56", "Male", "Tesla", "Automotive", "90", 
             "Rarely", "High"],
            
            # Row 4: Gen Z - Adidas
            ["18-24", "Non-binary", "Adidas", "Apparel", "82", 
             "Quarterly", "Medium"],
            
            # Row 5: Boomer - Nordstrom
            ["57-75", "Female", "Nordstrom", "Retail", "75", 
             "Monthly", "High"],
            
            # Row 6: Millennial Male - Amazon
            ["35-40", "Male", "Amazon", "E-commerce", "95", 
             "Weekly", "Very High"],
            
            # Row 7: Gen Z - Spotify
            ["18-24", "Non-binary", "Spotify", "Entertainment", "88", 
             "Daily", "Very High"]
        ]
        
        # Write to CSV file
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(data_rows)
        
        print(f"✅ Created brand preferences CSV file with {len(data_rows)} entries")
        return csv_path

    def create_test_zip_file(self):
        """Create a comprehensive test ZIP file with realistic Resonate data"""
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "resonate_data.zip")
        
        # Create CSV files with realistic data
        demographics_csv = self.create_realistic_csv_file(temp_dir)
        media_consumption_csv = self.create_media_consumption_csv(temp_dir)
        brand_preferences_csv = self.create_brand_preferences_csv(temp_dir)
        
        # Create a README text file
        readme_path = os.path.join(temp_dir, "README.txt")
        with open(readme_path, 'w') as f:
            f.write("Resonate Data Export\n")
            f.write("===================\n\n")
            f.write("This package contains demographic, media consumption, and brand preference data.\n")
            f.write("Files included:\n")
            f.write("- resonate_demographics.csv: Core demographic information\n")
            f.write("- resonate_media_consumption.csv: Detailed media usage patterns\n")
            f.write("- resonate_brand_preferences.csv: Brand affinity and loyalty metrics\n\n")
            f.write("For questions about this data, contact research@resonate.com\n")
        
        # Create ZIP file with all files
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.write(demographics_csv, os.path.basename(demographics_csv))
            zip_file.write(media_consumption_csv, os.path.basename(media_consumption_csv))
            zip_file.write(brand_preferences_csv, os.path.basename(brand_preferences_csv))
            zip_file.write(readme_path, os.path.basename(readme_path))
        
        print(f"✅ Created comprehensive ZIP file with Resonate data at {zip_path}")
        return zip_path

    def test_resonate_upload(self):
        """Test uploading a realistic Resonate ZIP file"""
        # Create a comprehensive test ZIP file
        zip_path = self.create_test_zip_file()
        
        files = {
            'file': ('resonate_data.zip', open(zip_path, 'rb'), 'application/zip')
        }
        
        success, response = self.run_test(
            "Resonate Upload - Comprehensive ZIP File",
            "POST",
            "personas/resonate-upload",
            200,
            files=files
        )
        
        # Store parsed data for next test
        if success and response.get('success') and 'parsed_data' in response:
            self.parsed_data = response['parsed_data']
            
            # Detailed examination of parsed data
            print("\n📊 Examining parsed data structure:")
            
            # Check demographics
            if 'demographics' in self.parsed_data:
                demo_keys = self.parsed_data['demographics'].keys()
                print(f"   ✅ Demographics data extracted: {', '.join(demo_keys)}")
                
                # Check specific demographic fields
                for key in ['age', 'gender', 'income', 'location', 'occupation']:
                    if key in demo_keys:
                        print(f"   ✅ Found '{key}' demographic data")
                    else:
                        print(f"   ⚠️ Missing '{key}' demographic data")
            else:
                print("   ❌ No demographics data extracted")
            
            # Check media consumption
            if 'media_consumption' in self.parsed_data:
                media_keys = self.parsed_data['media_consumption'].keys()
                print(f"   ✅ Media consumption data extracted: {', '.join(media_keys)}")
            else:
                print("   ❌ No media consumption data extracted")
            
            # Check brand affinity
            if 'brand_affinity' in self.parsed_data:
                brand_keys = self.parsed_data['brand_affinity'].keys()
                print(f"   ✅ Brand affinity data extracted: {', '.join(brand_keys)}")
            else:
                print("   ❌ No brand affinity data extracted")
        
        # Clean up
        try:
            os.remove(zip_path)
        except:
            pass
        
        return success

    def test_resonate_create_persona(self):
        """Test creating a persona from parsed Resonate data"""
        if not self.parsed_data:
            print("❌ Skipping - No parsed data available from previous test")
            return False
        
        success, response = self.run_test(
            "Create Persona from Resonate Data",
            "POST",
            "personas/resonate-create",
            200,
            data={
                "name": "Comprehensive Resonate Persona",
                "parsed_data": self.parsed_data
            }
        )
        
        if success and response.get('success') and 'persona' in response:
            persona = response['persona']
            if 'id' in persona:
                self.persona_id = persona['id']
                print(f"   ✅ Created persona from Resonate data with ID: {self.persona_id}")
            
            # Verify persona structure
            print("\n🔍 Examining created persona structure:")
            
            # Check starting method
            if persona.get('starting_method') == 'resonate_upload':
                print("   ✅ Correct starting method: resonate_upload")
            else:
                print(f"   ❌ Incorrect starting method: {persona.get('starting_method')}")
            
            # Check demographics mapping
            if 'demographics' in persona:
                demographics = persona['demographics']
                print("   ✅ Demographics mapped to persona")
                
                # Check specific fields
                for field in ['age_range', 'gender', 'income_range', 'location', 'occupation']:
                    if field in demographics and demographics[field]:
                        print(f"   ✅ '{field}' mapped correctly: {demographics[field]}")
                    else:
                        print(f"   ⚠️ '{field}' not mapped or empty")
            else:
                print("   ❌ Demographics not mapped to persona")
            
            # Check media consumption mapping
            if 'media_consumption' in persona:
                media = persona['media_consumption']
                print("   ✅ Media consumption mapped to persona")
                
                # Check social media platforms
                if 'social_media_platforms' in media and media['social_media_platforms']:
                    print(f"   ✅ Social media platforms mapped: {media['social_media_platforms']}")
                else:
                    print("   ⚠️ Social media platforms not mapped or empty")
            else:
                print("   ❌ Media consumption not mapped to persona")
            
            # Check attributes mapping (for brand preferences)
            if 'attributes' in persona:
                attributes = persona['attributes']
                print("   ✅ Attributes mapped to persona")
                
                # Check preferred brands
                if 'preferred_brands' in attributes and attributes['preferred_brands']:
                    print(f"   ✅ Preferred brands mapped: {attributes['preferred_brands']}")
                else:
                    print("   ⚠️ Preferred brands not mapped or empty")
            else:
                print("   ❌ Attributes not mapped to persona")
            
            # Check completed steps
            if 'completed_steps' in persona:
                completed_steps = persona['completed_steps']
                print(f"   ✅ Completed steps: {completed_steps}")
                if len(completed_steps) > 0:
                    print("   ✅ Steps marked as completed")
                else:
                    print("   ⚠️ No steps marked as completed")
            else:
                print("   ❌ Completed steps not set")
        
        return success

    def test_get_created_persona(self):
        """Test retrieving the created persona to verify data persistence"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available from previous test")
            return False
        
        success, response = self.run_test(
            "Get Created Persona",
            "GET",
            f"personas/{self.persona_id}",
            200
        )
        
        if success:
            print(f"   ✅ Successfully retrieved created persona")
            
            # Verify starting method
            if response.get('starting_method') == 'resonate_upload':
                print("   ✅ Correct starting method preserved: resonate_upload")
            else:
                print(f"   ❌ Incorrect starting method: {response.get('starting_method')}")
        
        return success

    def print_summary(self):
        """Print a summary of all test results"""
        print("\n" + "=" * 60)
        print("📊 RESONATE UPLOAD TEST RESULTS SUMMARY")
        print("=" * 60)
        
        # List all tests
        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result["success"] else "❌ FAILED"
            print(f"  {status} - {test_name}")
        
        # Print overall statistics
        print("\n" + "-" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0:.1f}%")
        print("=" * 60)


def main():
    print("🚀 Starting BCM VentasAI Resonate Upload Functionality Tests")
    print("=" * 60)
    
    # Get backend URL from frontend/.env
    backend_url = "https://28426961-bcbc-4f0c-9e2c-9ae3cc74eaf5.preview.emergentagent.com/api"
    print(f"Using backend URL: {backend_url}")
    
    tester = ResonateUploadTester(backend_url)
    
    # Define test sequence
    tests = [
        # 1. Test file upload
        tester.test_resonate_upload,
        
        # 2. Test persona creation from parsed data
        tester.test_resonate_create_persona,
        
        # 3. Test retrieving the created persona
        tester.test_get_created_persona
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
        print("🎉 All Resonate upload tests passed! The functionality is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
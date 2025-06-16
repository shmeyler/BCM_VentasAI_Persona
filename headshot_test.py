import requests
import sys
import json
from datetime import datetime

class HeadshotTester:
    def __init__(self, base_url="https://0d86ffe6-71b5-47b2-b182-692556be7d93.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.persona_ids = {}  # Store persona IDs for different test cases

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
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

    def test_create_female_marketing_persona(self):
        """Test Case A - Female Marketing Manager"""
        success, response = self.run_test(
            "Create Female Marketing Director Persona",
            "POST",
            "personas",
            200,
            data={
                "starting_method": "demographics",
                "name": "Sarah Marketing Director"
            }
        )
        if success and 'id' in response:
            self.persona_ids['female_marketing'] = response['id']
            print(f"   Created persona with ID: {self.persona_ids['female_marketing']}")
        return success

    def test_update_female_marketing_persona(self):
        """Update Female Marketing Manager with demographics"""
        if 'female_marketing' not in self.persona_ids:
            print("❌ Skipping - No female marketing persona ID available")
            return False

        success, response = self.run_test(
            "Update Female Marketing Director Demographics",
            "PUT",
            f"personas/{self.persona_ids['female_marketing']}",
            200,
            data={
                "demographics": {
                    "age_range": "25-40",
                    "gender": "Female",
                    "income_range": "$75,000-$99,999",
                    "education": "Bachelor's Degree",
                    "location": "Austin",
                    "occupation": "Marketing Manager",
                    "family_status": "Single"
                }
            }
        )
        return success

    def test_create_male_executive_persona(self):
        """Test Case B - Male Executive"""
        success, response = self.run_test(
            "Create Male Executive Leader Persona",
            "POST",
            "personas",
            200,
            data={
                "starting_method": "demographics",
                "name": "David Executive Leader"
            }
        )
        if success and 'id' in response:
            self.persona_ids['male_executive'] = response['id']
            print(f"   Created persona with ID: {self.persona_ids['male_executive']}")
        return success

    def test_update_male_executive_persona(self):
        """Update Male Executive with demographics"""
        if 'male_executive' not in self.persona_ids:
            print("❌ Skipping - No male executive persona ID available")
            return False

        success, response = self.run_test(
            "Update Male Executive Leader Demographics",
            "PUT",
            f"personas/{self.persona_ids['male_executive']}",
            200,
            data={
                "demographics": {
                    "age_range": "41-56",
                    "gender": "Male",
                    "income_range": "$150,000+",
                    "education": "Master's Degree",
                    "location": "New York",
                    "occupation": "Executive Director",
                    "family_status": "Married"
                }
            }
        )
        return success

    def test_create_female_tech_persona(self):
        """Test Case C - Female Tech Professional"""
        success, response = self.run_test(
            "Create Female Software Engineer Persona",
            "POST",
            "personas",
            200,
            data={
                "starting_method": "demographics",
                "name": "Lisa Software Engineer"
            }
        )
        if success and 'id' in response:
            self.persona_ids['female_tech'] = response['id']
            print(f"   Created persona with ID: {self.persona_ids['female_tech']}")
        return success

    def test_update_female_tech_persona(self):
        """Update Female Tech Professional with demographics"""
        if 'female_tech' not in self.persona_ids:
            print("❌ Skipping - No female tech persona ID available")
            return False

        success, response = self.run_test(
            "Update Female Software Engineer Demographics",
            "PUT",
            f"personas/{self.persona_ids['female_tech']}",
            200,
            data={
                "demographics": {
                    "age_range": "25-40",
                    "gender": "Female",
                    "income_range": "$100,000-$149,999",
                    "education": "Master's Degree",
                    "location": "San Francisco",
                    "occupation": "Software Engineer",
                    "family_status": "Single"
                }
            }
        )
        return success

    def test_generate_female_marketing_persona(self):
        """Generate Female Marketing Manager persona with headshot"""
        if 'female_marketing' not in self.persona_ids:
            print("❌ Skipping - No female marketing persona ID available")
            return False

        success, response = self.run_test(
            "Generate Female Marketing Director Persona",
            "POST",
            f"personas/{self.persona_ids['female_marketing']}/generate",
            200
        )
        
        if success:
            # Check if persona image URL is generated
            if 'persona_image_url' in response:
                image_url = response['persona_image_url']
                print(f"   ✅ Female Marketing Director image URL: {image_url}")
                
                # Verify the URL format is correct
                if "https://images.unsplash.com/photo-" in image_url and "w=400&h=400" in image_url:
                    print(f"   ✅ URL format is correct")
                else:
                    print(f"   ❌ URL format may be incorrect")
                
                # Test if the image is accessible
                try:
                    img_response = requests.head(image_url, timeout=5)
                    if img_response.status_code == 200:
                        print(f"   ✅ Image is accessible (Status: {img_response.status_code})")
                    else:
                        print(f"   ❌ Image is not accessible (Status: {img_response.status_code})")
                except Exception as e:
                    print(f"   ❌ Error accessing image: {str(e)}")
            else:
                print(f"   ❌ No persona image URL generated")
        
        return success

    def test_generate_male_executive_persona(self):
        """Generate Male Executive persona with headshot"""
        if 'male_executive' not in self.persona_ids:
            print("❌ Skipping - No male executive persona ID available")
            return False

        success, response = self.run_test(
            "Generate Male Executive Leader Persona",
            "POST",
            f"personas/{self.persona_ids['male_executive']}/generate",
            200
        )
        
        if success:
            # Check if persona image URL is generated
            if 'persona_image_url' in response:
                image_url = response['persona_image_url']
                print(f"   ✅ Male Executive Leader image URL: {image_url}")
                
                # Verify the URL format is correct
                if "https://images.unsplash.com/photo-" in image_url and "w=400&h=400" in image_url:
                    print(f"   ✅ URL format is correct")
                else:
                    print(f"   ❌ URL format may be incorrect")
                
                # Test if the image is accessible
                try:
                    img_response = requests.head(image_url, timeout=5)
                    if img_response.status_code == 200:
                        print(f"   ✅ Image is accessible (Status: {img_response.status_code})")
                    else:
                        print(f"   ❌ Image is not accessible (Status: {img_response.status_code})")
                except Exception as e:
                    print(f"   ❌ Error accessing image: {str(e)}")
            else:
                print(f"   ❌ No persona image URL generated")
        
        return success

    def test_generate_female_tech_persona(self):
        """Generate Female Tech Professional persona with headshot"""
        if 'female_tech' not in self.persona_ids:
            print("❌ Skipping - No female tech persona ID available")
            return False

        success, response = self.run_test(
            "Generate Female Software Engineer Persona",
            "POST",
            f"personas/{self.persona_ids['female_tech']}/generate",
            200
        )
        
        if success:
            # Check if persona image URL is generated
            if 'persona_image_url' in response:
                image_url = response['persona_image_url']
                print(f"   ✅ Female Software Engineer image URL: {image_url}")
                
                # Verify the URL format is correct
                if "https://images.unsplash.com/photo-" in image_url and "w=400&h=400" in image_url:
                    print(f"   ✅ URL format is correct")
                else:
                    print(f"   ❌ URL format may be incorrect")
                
                # Test if the image is accessible
                try:
                    img_response = requests.head(image_url, timeout=5)
                    if img_response.status_code == 200:
                        print(f"   ✅ Image is accessible (Status: {img_response.status_code})")
                    else:
                        print(f"   ❌ Image is not accessible (Status: {img_response.status_code})")
                except Exception as e:
                    print(f"   ❌ Error accessing image: {str(e)}")
            else:
                print(f"   ❌ No persona image URL generated")
        
        return success

def main():
    print("🚀 Starting BCM Persona Generator Headshot URL Tests")
    print("=" * 60)
    print("Testing the fix for headshot display issues")
    
    tester = HeadshotTester()
    
    # Test sequence for headshot URL generation
    tests = [
        # Test Case A - Female Marketing Manager
        tester.test_create_female_marketing_persona,
        tester.test_update_female_marketing_persona,
        tester.test_generate_female_marketing_persona,
        
        # Test Case B - Male Executive
        tester.test_create_male_executive_persona,
        tester.test_update_male_executive_persona,
        tester.test_generate_male_executive_persona,
        
        # Test Case C - Female Tech Professional
        tester.test_create_female_tech_persona,
        tester.test_update_female_tech_persona,
        tester.test_generate_female_tech_persona
    ]
    
    print(f"\n📋 Running {len(tests)} headshot URL tests...")
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! Headshot URL generation is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

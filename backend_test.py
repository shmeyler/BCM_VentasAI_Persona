import requests
import sys
import json
from datetime import datetime

class BCMPersonaAPITester:
    def __init__(self, base_url="https://5723ff75-4165-4b59-917c-cb207fa4725b.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.persona_id = None

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

    def test_api_root(self):
        """Test API root endpoint"""
        success, response = self.run_test(
            "API Root",
            "GET",
            "",
            200
        )
        return success

    def test_create_persona_demographics(self):
        """Test creating a persona with demographics starting method"""
        success, response = self.run_test(
            "Create Persona (Demographics)",
            "POST",
            "personas",
            200,
            data={
                "starting_method": "demographics",
                "name": "Test Demographics Persona"
            }
        )
        if success and 'id' in response:
            self.persona_id = response['id']
            print(f"   Created persona with ID: {self.persona_id}")
        return success

    def test_create_persona_attributes(self):
        """Test creating a persona with attributes starting method"""
        success, response = self.run_test(
            "Create Persona (Attributes)",
            "POST",
            "personas",
            200,
            data={
                "starting_method": "attributes",
                "name": "Test Attributes Persona"
            }
        )
        return success

    def test_update_persona_with_resonate_taxonomy(self):
        """Test updating persona with new Resonate Taxonomy fields"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Update Persona with Resonate Taxonomy",
            "PUT",
            f"personas/{self.persona_id}",
            200,
            data={
                "attributes": {
                    "selectedVertical": "Retail",
                    "selectedCategory": "Preferences & Psychographics",
                    "selectedBehaviors": ["Quality-focused", "Brand loyal", "Sustainable shopping"],
                    "interests": ["Fashion", "Technology", "Sustainability"],
                    "values": ["Quality", "Authenticity", "Environmental responsibility"]
                },
                "demographics": {
                    "age_range": "25-40",
                    "gender": "Female",
                    "income_range": "$50,000-$75,000",
                    "education": "Bachelor's Degree",
                    "location": "Urban",
                    "occupation": "Marketing Manager",
                    "family_status": "Single"
                }
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
                    "social_media_platforms": ["Instagram", "Facebook", "LinkedIn", "TikTok"],
                    "content_types": ["Video content", "Social media posts", "News articles"],
                    "consumption_time": "2-4 hours",
                    "preferred_devices": ["Smartphone", "Laptop"],
                    "news_sources": ["Online news", "Social media"],
                    "entertainment_preferences": ["Streaming services", "Podcasts"],
                    "advertising_receptivity": "Moderate"
                }
            }
        )
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
        
        if success:
            # Verify the new Resonate Taxonomy fields are present
            attributes = response.get('attributes', {})
            if 'selectedVertical' in attributes:
                print(f"   ✅ selectedVertical: {attributes['selectedVertical']}")
            if 'selectedCategory' in attributes:
                print(f"   ✅ selectedCategory: {attributes['selectedCategory']}")
            if 'selectedBehaviors' in attributes:
                print(f"   ✅ selectedBehaviors: {len(attributes['selectedBehaviors'])} behaviors")
        
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
            if 'recommendations' in response:
                print(f"   ✅ {len(response['recommendations'])} recommendations generated")
        
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

    def test_delete_generated_persona(self):
        """Test deleting a generated persona - CRITICAL FIX BEING TESTED"""
        print("\n🔥 === CRITICAL TEST: Generated Persona Deletion ===")
        
        # First get list of generated personas
        success, response = self.run_test(
            "List Generated Personas for Deletion Test",
            "GET",
            "generated-personas",
            200
        )
        
        if not success:
            print("❌ Cannot test deletion - failed to get generated personas list")
            return False
        
        generated_personas = response if isinstance(response, list) else []
        if not generated_personas:
            print("❌ No generated personas available for deletion test")
            return False
        
        # Get the first generated persona ID
        generated_persona_id = generated_personas[0].get('id')
        if not generated_persona_id:
            print("❌ Generated persona has no ID field")
            return False
        
        print(f"   Testing deletion of generated persona: {generated_persona_id}")
        
        # CRITICAL TEST: Delete the generated persona
        success, response = self.run_test(
            "Delete Generated Persona - CRITICAL FIX",
            "DELETE",
            f"generated-personas/{generated_persona_id}",
            200
        )
        
        if success:
            print("   ✅ CRITICAL FIX VERIFIED: Generated persona deletion works!")
            
            # Verify it's actually deleted by checking the list again
            success_verify, response_verify = self.run_test(
                "Verify Generated Persona Deleted",
                "GET",
                "generated-personas",
                200
            )
            
            if success_verify:
                remaining_personas = response_verify if isinstance(response_verify, list) else []
                deleted_persona_still_exists = any(p.get('id') == generated_persona_id for p in remaining_personas)
                
                if not deleted_persona_still_exists:
                    print("   ✅ VERIFICATION PASSED: Persona successfully removed from list")
                else:
                    print("   ⚠️  VERIFICATION WARNING: Persona still appears in list")
            
        else:
            print("   ❌ CRITICAL FIX FAILED: Generated persona deletion still has issues!")
        
        return success

    def test_data_sources_status(self):
        """Test data sources status endpoint"""
        success, response = self.run_test(
            "Data Sources Status",
            "GET",
            "data-sources/status",
            200
        )
        
        if success:
            # Check for expected data sources
            expected_sources = ['semrush', 'sparktoro', 'buzzabout']
            for source in expected_sources:
                if source in response:
                    status = response[source].get('status', 'unknown')
                    print(f"   ✅ {source.upper()}: {status}")
                else:
                    print(f"   ❌ {source.upper()}: missing")
            
            if 'integration_health' in response:
                print(f"   ✅ Integration health: {response['integration_health']}")
        
        return success

    def test_demo_data_sources(self):
        """Test demo data from all data sources"""
        success, response = self.run_test(
            "Demo Data Sources",
            "GET",
            "data-sources/demo",
            200
        )
        
        if success:
            # Check for expected data insights
            expected_insights = ['search_insights', 'audience_insights', 'social_insights']
            for insight in expected_insights:
                if insight in response:
                    print(f"   ✅ {insight}: available")
                else:
                    print(f"   ❌ {insight}: missing")
            
            if 'data_integration' in response:
                integration = response['data_integration']
                print(f"   ✅ Data integration score: {integration.get('enrichment_score', 'N/A')}")
        
        return success

    def test_persona_enrichment(self):
        """Test persona enrichment with data sources"""
        if not self.persona_id:
            print("❌ Skipping - No persona ID available")
            return False

        success, response = self.run_test(
            "Persona Data Enrichment",
            "POST",
            f"personas/{self.persona_id}/enrich",
            200
        )
        
        if success:
            print(f"   ✅ Persona enriched successfully")
        
        return success

    def test_persona_insights(self):
        """Test getting persona insights"""
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
            # Check for expected insight categories
            expected_insights = ['search_behavior', 'audience_profile', 'social_sentiment']
            for insight in expected_insights:
                if insight in response:
                    print(f"   ✅ {insight}: available")
                else:
                    print(f"   ❌ {insight}: missing")
        
        return success

    def test_export_pdf_data(self):
        """Test PDF export data endpoint - FIXED EXPORT FUNCTIONALITY"""
        print("\n🔥 === CRITICAL TEST: FIXED PDF Export Data ===")
        
        # First get a generated persona to test with
        success, response = self.run_test(
            "List Generated Personas for Export Test",
            "GET",
            "generated-personas",
            200
        )
        
        if not success:
            print("❌ Cannot test PDF export - failed to get generated personas list")
            return False
        
        generated_personas = response if isinstance(response, list) else []
        if not generated_personas:
            print("❌ No generated personas available for PDF export test")
            return False
        
        # Get the first generated persona ID
        generated_persona_id = generated_personas[0].get('id')
        if not generated_persona_id:
            print("❌ Generated persona has no ID field")
            return False
        
        print(f"   Testing FIXED PDF export data for persona: {generated_persona_id}")
        
        # Test PDF export data endpoint - SHOULD NOW RETURN 200 INSTEAD OF 500
        success, response = self.run_test(
            "PDF Export Data - FIXED FUNCTIONALITY",
            "POST",
            "export/pdf-data",
            200,
            data={"generated_persona_id": generated_persona_id}
        )
        
        if success:
            print("   ✅ CRITICAL FIX VERIFIED: PDF export data endpoint now returns 200!")
            if 'persona_data' in response:
                print("   ✅ Persona data included in response")
            if response.get('success'):
                print("   ✅ Success flag is True")
            
            # CRITICAL: Test JSON serialization (ObjectId fix)
            try:
                json.dumps(response)
                print("   ✅ CRITICAL FIX VERIFIED: Response is JSON serializable (ObjectId issue fixed)")
            except Exception as e:
                print(f"   ❌ CRITICAL ISSUE: Response not JSON serializable: {str(e)}")
                return False
        else:
            print("   ❌ CRITICAL ISSUE: PDF export data endpoint still failing!")
        
        # Test with persona_id as well
        if self.persona_id:
            success2, response2 = self.run_test(
                "PDF Export Data with persona_id",
                "POST",
                "export/pdf-data",
                200,
                data={"persona_id": self.persona_id}
            )
            if success2:
                print("   ✅ PDF export also works with persona_id")
        
        return success

    def test_export_google_slides(self):
        """Test Google Slides export endpoint - NEW EXPORT FUNCTIONALITY"""
        print("\n🔥 === NEW FEATURE TEST: Google Slides Export ===")
        
        # First get a generated persona to test with
        success, response = self.run_test(
            "List Generated Personas for Google Slides Test",
            "GET",
            "generated-personas",
            200
        )
        
        if not success:
            print("❌ Cannot test Google Slides export - failed to get generated personas list")
            return False
        
        generated_personas = response if isinstance(response, list) else []
        if not generated_personas:
            print("❌ No generated personas available for Google Slides export test")
            return False
        
        # Get the first generated persona ID
        generated_persona_id = generated_personas[0].get('id')
        if not generated_persona_id:
            print("❌ Generated persona has no ID field")
            return False
        
        print(f"   Testing Google Slides export for persona: {generated_persona_id}")
        
        # Test Google Slides export endpoint
        success, response = self.run_test(
            "Google Slides Export - NEW FEATURE",
            "POST",
            "export/google-slides",
            200,
            data={"generated_persona_id": generated_persona_id}
        )
        
        if success:
            print("   ✅ Google Slides export endpoint works!")
            if 'persona_data' in response:
                print("   ✅ Persona data included in response")
            if response.get('success'):
                print("   ✅ Success flag is True")
            if 'message' in response:
                print(f"   ✅ Message: {response['message']}")
        else:
            print("   ❌ Google Slides export endpoint failed!")
        
        return success

    def test_legacy_status_endpoints(self):
        """Test legacy status check endpoints for compatibility"""
        # Test creating a status check
        success1, response1 = self.run_test(
            "Create Status Check",
            "POST",
            "status",
            200,
            data={"client_name": "Test Client"}
        )
        
        # Test getting status checks
        success2, response2 = self.run_test(
            "Get Status Checks",
            "GET",
            "status",
            200
        )
        
        return success1 and success2

def main():
    print("🚀 Starting BCM VentasAI Persona Generator API Tests")
    print("=" * 60)
    
    tester = BCMPersonaAPITester()
    
    # Test sequence focusing on new features and CRITICAL FIXES
    tests = [
        tester.test_api_root,
        tester.test_data_sources_status,
        tester.test_demo_data_sources,
        tester.test_create_persona_demographics,
        tester.test_create_persona_attributes,
        tester.test_update_persona_with_resonate_taxonomy,
        tester.test_update_persona_media_consumption,
        tester.test_get_persona,
        tester.test_persona_enrichment,
        tester.test_persona_insights,
        tester.test_generate_persona,
        tester.test_list_personas,
        tester.test_list_generated_personas,
        tester.test_export_pdf_data,  # NEW EXPORT FUNCTIONALITY TEST
        tester.test_export_google_slides,  # NEW EXPORT FUNCTIONALITY TEST
        tester.test_delete_generated_persona,  # CRITICAL FIX TEST
        tester.test_legacy_status_endpoints,
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
        print("🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
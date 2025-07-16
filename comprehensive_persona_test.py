#!/usr/bin/env python3
"""
Comprehensive Test Suite for BCM VentasAI Persona Generator
Focus: Testing the comprehensive fix for dummy data issue

This test suite specifically tests:
1. Multi-source persona generation with uploaded data
2. Multi-source persona generation with only demographic data (no uploaded files)
3. Regular persona generation with good demographic data
4. Regular persona generation with limited demographic data
5. Verify OpenAI is being used instead of basic generation functions
6. Check that generated insights are specific and contextual, not generic
7. Ensure no fallback dummy data is being used unless absolutely necessary
"""

import requests
import json
import tempfile
import zipfile
import os
import time
from datetime import datetime

class ComprehensivePersonaGeneratorTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = {}
        
    def log_test(self, test_name, success, details=None):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}")
        else:
            print(f"❌ {test_name}")
        
        if details:
            for detail in details:
                print(f"   {detail}")
        
        self.test_results[test_name] = {
            "success": success,
            "details": details or []
        }
        
    def make_request(self, method, endpoint, data=None, files=None, timeout=60):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        
        if not files:
            headers['Content-Type'] = 'application/json'
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, timeout=timeout)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=timeout)
            
            return response.status_code == 200, response.json() if response.content else {}
        except Exception as e:
            print(f"   Request failed: {str(e)}")
            return False, {}
    
    def create_realistic_demographic_zip(self):
        """Create a ZIP file with realistic demographic data"""
        temp_dir = tempfile.mkdtemp()
        csv_path = os.path.join(temp_dir, "demographics.csv")
        
        with open(csv_path, 'w') as f:
            f.write('Age Group,Gender,Household Income,Education Level,Location,Occupation,Social Platforms\n')
            f.write('"25-40","Female","$50,000-$75,000","Bachelor\'s Degree","Urban","Marketing Professional","Instagram, Facebook, LinkedIn"\n')
            f.write('"35-44","Male","$75,000-$100,000","Master\'s Degree","Suburban","Software Engineer","LinkedIn, Twitter, GitHub"\n')
            f.write('"18-24","Female","$25,000-$50,000","Some College","Urban","Student","TikTok, Instagram, Snapchat"\n')
        
        zip_path = os.path.join(temp_dir, "demographic_data.zip")
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.write(csv_path, os.path.basename(csv_path))
        
        return zip_path
    
    def analyze_persona_quality(self, persona_data, test_name):
        """Analyze the quality of generated persona to detect dummy data vs real insights"""
        details = []
        quality_score = 0
        total_checks = 0
        
        # Check AI insights quality
        ai_insights = persona_data.get('ai_insights', {})
        if ai_insights:
            personality_traits = ai_insights.get('personality_traits', [])
            
            # Check for specific, non-generic traits
            generic_traits = ["Data-driven", "Research-oriented", "Platform-savvy", "Goal-focused"]
            specific_traits = ["Tech-savvy", "Value-conscious", "Experience-focused", "Digital native", "Socially conscious"]
            
            total_checks += 1
            if any(trait in specific_traits for trait in personality_traits):
                quality_score += 1
                details.append(f"✅ Specific personality traits found: {', '.join(personality_traits)}")
            elif any(trait in generic_traits for trait in personality_traits):
                details.append(f"⚠️ Generic personality traits detected: {', '.join(personality_traits)}")
            else:
                details.append(f"✅ Custom personality traits: {', '.join(personality_traits)}")
                quality_score += 1
            
            # Check shopping behavior specificity
            shopping_behavior = ai_insights.get('shopping_behavior', '')
            total_checks += 1
            if shopping_behavior and "Methodical research approach" not in shopping_behavior:
                quality_score += 1
                details.append(f"✅ Specific shopping behavior: {shopping_behavior[:100]}...")
            else:
                details.append(f"⚠️ Generic shopping behavior detected")
        
        # Check recommendations quality
        recommendations = persona_data.get('recommendations', [])
        if recommendations:
            total_checks += 1
            generic_recs = ["Leverage data-driven marketing strategies", "Focus on platform-specific content optimization"]
            specific_recs = ["Use Instagram visual storytelling", "Leverage LinkedIn for professional", "Create YouTube content"]
            
            if any(any(specific in rec for specific in specific_recs) for rec in recommendations):
                quality_score += 1
                details.append(f"✅ Platform-specific recommendations found")
            elif any(any(generic in rec for generic in generic_recs) for rec in recommendations):
                details.append(f"⚠️ Generic recommendations detected")
            else:
                quality_score += 1
                details.append(f"✅ Custom recommendations generated")
        
        # Check pain points quality
        pain_points = persona_data.get('pain_points', [])
        if pain_points:
            total_checks += 1
            generic_pain_points = ["Information overload from multiple data sources", "Platform integration complexities"]
            demographic_pain_points = ["Time constraints due to busy lifestyle", "Limited disposable income", "Balancing quality with affordability"]
            
            if any(any(demo in pain for demo in demographic_pain_points) for pain in pain_points):
                quality_score += 1
                details.append(f"✅ Demographic-specific pain points found")
            elif any(any(generic in pain for generic in generic_pain_points) for pain in pain_points):
                details.append(f"⚠️ Generic pain points detected")
            else:
                quality_score += 1
                details.append(f"✅ Custom pain points generated")
        
        # Check communication style
        comm_style = persona_data.get('communication_style', '')
        if comm_style:
            total_checks += 1
            if "Clear, professional, and informative communication" not in comm_style:
                quality_score += 1
                details.append(f"✅ Specific communication style: {comm_style}")
            else:
                details.append(f"⚠️ Generic communication style detected")
        
        # Calculate quality percentage
        quality_percentage = (quality_score / total_checks * 100) if total_checks > 0 else 0
        details.append(f"📊 Quality Score: {quality_score}/{total_checks} ({quality_percentage:.1f}%)")
        
        return quality_percentage >= 75, details
    
    def test_1_multi_source_with_uploaded_data(self):
        """Test 1: Multi-source persona generation with uploaded data"""
        print("\n" + "="*80)
        print("TEST 1: Multi-source persona generation with uploaded data")
        print("="*80)
        
        # Step 1: Create persona with multi_source_data method
        success, persona_data = self.make_request('POST', 'personas', {
            "starting_method": "multi_source_data",
            "name": "Multi-Source Test Persona"
        })
        
        if not success:
            self.log_test("1.1 Create multi-source persona", False, ["Failed to create persona"])
            return False
        
        persona_id = persona_data.get('id')
        self.log_test("1.1 Create multi-source persona", True, [f"Created persona ID: {persona_id}"])
        
        # Step 2: Upload realistic demographic data
        zip_path = self.create_realistic_demographic_zip()
        files = {'file': ('demographic_data.zip', open(zip_path, 'rb'), 'application/zip')}
        
        success, upload_response = self.make_request('POST', 'personas/resonate-upload', files=files)
        os.remove(zip_path)
        
        if not success:
            self.log_test("1.2 Upload demographic data", False, ["Failed to upload data"])
            return False
        
        self.log_test("1.2 Upload demographic data", True, ["Successfully uploaded and parsed data"])
        
        # Step 3: Update persona with uploaded data
        success, update_response = self.make_request('PUT', f'personas/{persona_id}', {
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
            "resonate_data": upload_response.get('parsed_data', {}),
            "completed_steps": [1, 2, 3, 4]
        })
        
        if not success:
            self.log_test("1.3 Update persona with data", False, ["Failed to update persona"])
            return False
        
        self.log_test("1.3 Update persona with data", True, ["Successfully updated persona"])
        
        # Step 4: Generate persona with multi-source data flag
        success, generated_persona = self.make_request('POST', f'personas/{persona_id}/generate', {
            "use_multi_source_data": True
        })
        
        if not success:
            self.log_test("1.4 Generate multi-source persona", False, ["Failed to generate persona"])
            return False
        
        # Step 5: Analyze quality of generated insights
        is_quality, quality_details = self.analyze_persona_quality(generated_persona, "Multi-source with uploaded data")
        
        self.log_test("1.4 Generate multi-source persona", success, [
            "Successfully generated persona",
            f"Image URL: {generated_persona.get('persona_image_url', 'None')[:50]}..."
        ])
        
        self.log_test("1.5 Quality analysis - No dummy data", is_quality, quality_details)
        
        return success and is_quality
    
    def test_2_multi_source_demographics_only(self):
        """Test 2: Multi-source persona generation with only demographic data (no uploaded files)"""
        print("\n" + "="*80)
        print("TEST 2: Multi-source persona generation with demographics only")
        print("="*80)
        
        # Step 1: Create persona with multi_source_data method
        success, persona_data = self.make_request('POST', 'personas', {
            "starting_method": "multi_source_data",
            "name": "Demographics Only Persona"
        })
        
        if not success:
            self.log_test("2.1 Create multi-source persona", False, ["Failed to create persona"])
            return False
        
        persona_id = persona_data.get('id')
        self.log_test("2.1 Create multi-source persona", True, [f"Created persona ID: {persona_id}"])
        
        # Step 2: Update with good demographic data only (no file uploads)
        success, update_response = self.make_request('PUT', f'personas/{persona_id}', {
            "demographics": {
                "age_range": "25-40",
                "gender": "Female",
                "income_range": "$75,000-$100,000", 
                "location": "Urban",
                "occupation": "Software Engineer",
                "education": "Master's Degree"
            },
            "media_consumption": {
                "social_media_platforms": ["LinkedIn", "Twitter", "GitHub"],
                "content_types": ["Technical blogs", "Industry news", "Tutorials"],
                "preferred_devices": ["Laptop", "Smartphone"]
            },
            "attributes": {
                "interests": ["Technology", "Innovation", "Professional development"],
                "values": ["Quality", "Efficiency", "Continuous learning"]
            },
            "completed_steps": [1, 2, 3]
        })
        
        if not success:
            self.log_test("2.2 Update with demographics", False, ["Failed to update persona"])
            return False
        
        self.log_test("2.2 Update with demographics", True, ["Successfully updated with rich demographic data"])
        
        # Step 3: Generate persona (should use OpenAI fallback for good demographic data)
        success, generated_persona = self.make_request('POST', f'personas/{persona_id}/generate', {
            "use_multi_source_data": True
        })
        
        if not success:
            self.log_test("2.3 Generate persona with OpenAI fallback", False, ["Failed to generate persona"])
            return False
        
        # Step 4: Analyze quality - should use OpenAI, not basic generation
        is_quality, quality_details = self.analyze_persona_quality(generated_persona, "Multi-source demographics only")
        
        self.log_test("2.3 Generate persona with OpenAI fallback", success, [
            "Successfully generated persona",
            f"Image URL: {generated_persona.get('persona_image_url', 'None')[:50]}..."
        ])
        
        self.log_test("2.4 Quality analysis - OpenAI used", is_quality, quality_details)
        
        return success and is_quality
    
    def test_3_regular_persona_good_demographics(self):
        """Test 3: Regular persona generation with good demographic data"""
        print("\n" + "="*80)
        print("TEST 3: Regular persona generation with good demographic data")
        print("="*80)
        
        # Step 1: Create persona with demographics method
        success, persona_data = self.make_request('POST', 'personas', {
            "starting_method": "demographics",
            "name": "Regular Demographics Persona"
        })
        
        if not success:
            self.log_test("3.1 Create demographics persona", False, ["Failed to create persona"])
            return False
        
        persona_id = persona_data.get('id')
        self.log_test("3.1 Create demographics persona", True, [f"Created persona ID: {persona_id}"])
        
        # Step 2: Update with comprehensive demographic data
        success, update_response = self.make_request('PUT', f'personas/{persona_id}', {
            "demographics": {
                "age_range": "35-44",
                "gender": "Male",
                "income_range": "$100,000-$150,000",
                "location": "Suburban", 
                "occupation": "Executive",
                "education": "MBA",
                "family_status": "Married with children"
            },
            "media_consumption": {
                "social_media_platforms": ["LinkedIn", "Facebook", "Twitter"],
                "content_types": ["Business news", "Industry reports", "Leadership content"],
                "consumption_time": "Morning and evening",
                "preferred_devices": ["Smartphone", "Tablet"],
                "news_sources": ["WSJ", "Bloomberg", "Industry publications"]
            },
            "attributes": {
                "interests": ["Business strategy", "Leadership", "Innovation", "Family time"],
                "behaviors": ["Strategic thinking", "Decision maker", "Team leader"],
                "values": ["Excellence", "Integrity", "Work-life balance"],
                "purchase_motivations": ["Quality", "Efficiency", "ROI"],
                "preferred_brands": ["Apple", "Tesla", "Microsoft", "Amazon"]
            },
            "completed_steps": [1, 2, 3]
        })
        
        if not success:
            self.log_test("3.2 Update with comprehensive data", False, ["Failed to update persona"])
            return False
        
        self.log_test("3.2 Update with comprehensive data", True, ["Successfully updated with rich data"])
        
        # Step 3: Generate persona (should use OpenAI for good data)
        success, generated_persona = self.make_request('POST', f'personas/{persona_id}/generate')
        
        if not success:
            self.log_test("3.3 Generate persona with OpenAI", False, ["Failed to generate persona"])
            return False
        
        # Step 4: Analyze quality - should be high quality with OpenAI
        is_quality, quality_details = self.analyze_persona_quality(generated_persona, "Regular persona good demographics")
        
        self.log_test("3.3 Generate persona with OpenAI", success, [
            "Successfully generated persona",
            f"Image URL: {generated_persona.get('persona_image_url', 'None')[:50]}..."
        ])
        
        self.log_test("3.4 Quality analysis - OpenAI insights", is_quality, quality_details)
        
        return success and is_quality
    
    def test_4_regular_persona_limited_demographics(self):
        """Test 4: Regular persona generation with limited demographic data"""
        print("\n" + "="*80)
        print("TEST 4: Regular persona generation with limited demographic data")
        print("="*80)
        
        # Step 1: Create persona with demographics method
        success, persona_data = self.make_request('POST', 'personas', {
            "starting_method": "demographics",
            "name": "Limited Demographics Persona"
        })
        
        if not success:
            self.log_test("4.1 Create limited demographics persona", False, ["Failed to create persona"])
            return False
        
        persona_id = persona_data.get('id')
        self.log_test("4.1 Create limited demographics persona", True, [f"Created persona ID: {persona_id}"])
        
        # Step 2: Update with minimal demographic data
        success, update_response = self.make_request('PUT', f'personas/{persona_id}', {
            "demographics": {
                "age_range": "25-40",
                "gender": "Female"
                # Minimal data - missing income, location, occupation, education
            },
            "media_consumption": {
                "social_media_platforms": ["Instagram"]
                # Minimal media data
            },
            "completed_steps": [1, 2]
        })
        
        if not success:
            self.log_test("4.2 Update with minimal data", False, ["Failed to update persona"])
            return False
        
        self.log_test("4.2 Update with minimal data", True, ["Successfully updated with minimal data"])
        
        # Step 3: Generate persona (may fall back to basic generation)
        success, generated_persona = self.make_request('POST', f'personas/{persona_id}/generate')
        
        if not success:
            self.log_test("4.3 Generate persona with fallback", False, ["Failed to generate persona"])
            return False
        
        # Step 4: Analyze what type of generation was used
        is_quality, quality_details = self.analyze_persona_quality(generated_persona, "Regular persona limited demographics")
        
        # For limited data, we expect either OpenAI with basic insights or intelligent fallback
        # The key is that it should still be contextual to the age/gender provided
        demographics = generated_persona.get('persona_data', {}).get('demographics', {})
        age_appropriate = False
        
        if demographics.get('age_range') == "25-40":
            ai_insights = generated_persona.get('ai_insights', {})
            personality_traits = ai_insights.get('personality_traits', [])
            
            # Check for age-appropriate traits (Millennial characteristics)
            millennial_traits = ["Tech-savvy", "Value-conscious", "Experience-focused"]
            if any(trait in millennial_traits for trait in personality_traits):
                age_appropriate = True
                quality_details.append("✅ Age-appropriate Millennial traits detected")
            else:
                quality_details.append("⚠️ Generic traits used for limited data")
        
        self.log_test("4.3 Generate persona with fallback", success, [
            "Successfully generated persona",
            f"Image URL: {generated_persona.get('persona_image_url', 'None')[:50]}..."
        ])
        
        self.log_test("4.4 Quality analysis - Contextual fallback", age_appropriate or is_quality, quality_details)
        
        return success
    
    def test_5_openai_integration_verification(self):
        """Test 5: Verify OpenAI is being used instead of basic generation functions"""
        print("\n" + "="*80)
        print("TEST 5: OpenAI integration verification")
        print("="*80)
        
        # Create a persona with rich data that should definitely trigger OpenAI
        success, persona_data = self.make_request('POST', 'personas', {
            "starting_method": "demographics",
            "name": "OpenAI Verification Persona"
        })
        
        if not success:
            self.log_test("5.1 Create verification persona", False, ["Failed to create persona"])
            return False
        
        persona_id = persona_data.get('id')
        
        # Update with rich data
        success, update_response = self.make_request('PUT', f'personas/{persona_id}', {
            "demographics": {
                "age_range": "18-24",
                "gender": "Female",
                "income_range": "$25,000-$50,000",
                "location": "Urban",
                "occupation": "Student",
                "education": "Some College"
            },
            "media_consumption": {
                "social_media_platforms": ["TikTok", "Instagram", "Snapchat", "YouTube"],
                "content_types": ["Short videos", "Memes", "Music", "Fashion"],
                "consumption_time": "Throughout the day",
                "preferred_devices": ["Smartphone"]
            },
            "attributes": {
                "interests": ["Social justice", "Sustainability", "Technology", "Fashion"],
                "values": ["Authenticity", "Diversity", "Environmental consciousness"],
                "behaviors": ["Mobile-first", "Socially conscious", "Brand skeptical"]
            },
            "completed_steps": [1, 2, 3]
        })
        
        if not success:
            self.log_test("5.2 Update with Gen Z data", False, ["Failed to update persona"])
            return False
        
        self.log_test("5.1 Create verification persona", True, [f"Created persona ID: {persona_id}"])
        self.log_test("5.2 Update with Gen Z data", True, ["Updated with rich Gen Z demographic data"])
        
        # Generate persona
        success, generated_persona = self.make_request('POST', f'personas/{persona_id}/generate')
        
        if not success:
            self.log_test("5.3 Generate persona", False, ["Failed to generate persona"])
            return False
        
        # Analyze for OpenAI vs basic generation indicators
        openai_indicators = []
        basic_generation_indicators = []
        
        # Check for OpenAI-specific patterns
        ai_insights = generated_persona.get('ai_insights', {})
        personality_traits = ai_insights.get('personality_traits', [])
        
        # OpenAI should generate Gen Z specific traits
        gen_z_traits = ["Digital native", "Socially conscious", "Entrepreneurial", "Authentic", "Purpose-driven"]
        basic_traits = ["Data-driven", "Research-oriented", "Platform-savvy", "Goal-focused"]
        
        for trait in personality_traits:
            if any(gen_z in trait for gen_z in gen_z_traits):
                openai_indicators.append(f"Gen Z trait: {trait}")
            elif any(basic in trait for basic in basic_traits):
                basic_generation_indicators.append(f"Basic trait: {trait}")
        
        # Check recommendations for platform specificity
        recommendations = generated_persona.get('recommendations', [])
        for rec in recommendations:
            if "TikTok" in rec or "Instagram Stories" in rec or "authentic" in rec.lower():
                openai_indicators.append(f"Platform-specific rec: {rec[:50]}...")
            elif "data-driven marketing" in rec.lower() or "platform-specific content" in rec.lower():
                basic_generation_indicators.append(f"Generic rec: {rec[:50]}...")
        
        # Check pain points for demographic specificity
        pain_points = generated_persona.get('pain_points', [])
        for point in pain_points:
            if "disposable income" in point.lower() or "student" in point.lower() or "authenticity" in point.lower():
                openai_indicators.append(f"Demographic pain point: {point[:50]}...")
            elif "information overload from multiple data sources" in point.lower():
                basic_generation_indicators.append(f"Generic pain point: {point[:50]}...")
        
        # Determine if OpenAI was used
        openai_used = len(openai_indicators) > len(basic_generation_indicators)
        
        details = []
        details.extend([f"✅ OpenAI indicator: {indicator}" for indicator in openai_indicators])
        details.extend([f"⚠️ Basic generation indicator: {indicator}" for indicator in basic_generation_indicators])
        details.append(f"📊 OpenAI indicators: {len(openai_indicators)}, Basic indicators: {len(basic_generation_indicators)}")
        
        self.log_test("5.3 Generate persona", success, ["Successfully generated persona"])
        self.log_test("5.4 OpenAI vs Basic generation analysis", openai_used, details)
        
        return success and openai_used
    
    def test_6_contextual_insights_verification(self):
        """Test 6: Check that generated insights are specific and contextual, not generic"""
        print("\n" + "="*80)
        print("TEST 6: Contextual insights verification")
        print("="*80)
        
        test_cases = [
            {
                "name": "Tech Professional",
                "demographics": {
                    "age_range": "35-44",
                    "gender": "Male", 
                    "occupation": "Software Engineer",
                    "income_range": "$100,000-$150,000",
                    "location": "Urban"
                },
                "platforms": ["LinkedIn", "GitHub", "Twitter"],
                "expected_keywords": ["technical", "engineering", "software", "development", "innovation"]
            },
            {
                "name": "Marketing Manager",
                "demographics": {
                    "age_range": "25-40",
                    "gender": "Female",
                    "occupation": "Marketing Manager", 
                    "income_range": "$75,000-$100,000",
                    "location": "Suburban"
                },
                "platforms": ["Instagram", "Facebook", "LinkedIn"],
                "expected_keywords": ["marketing", "brand", "campaign", "engagement", "analytics"]
            }
        ]
        
        all_passed = True
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i}: {test_case['name']} ---")
            
            # Create persona
            success, persona_data = self.make_request('POST', 'personas', {
                "starting_method": "demographics",
                "name": f"Contextual Test {test_case['name']}"
            })
            
            if not success:
                self.log_test(f"6.{i}.1 Create {test_case['name']} persona", False, ["Failed to create persona"])
                all_passed = False
                continue
            
            persona_id = persona_data.get('id')
            
            # Update with specific data
            success, update_response = self.make_request('PUT', f'personas/{persona_id}', {
                "demographics": test_case['demographics'],
                "media_consumption": {
                    "social_media_platforms": test_case['platforms']
                },
                "completed_steps": [1, 2]
            })
            
            if not success:
                self.log_test(f"6.{i}.2 Update {test_case['name']} data", False, ["Failed to update persona"])
                all_passed = False
                continue
            
            # Generate persona
            success, generated_persona = self.make_request('POST', f'personas/{persona_id}/generate')
            
            if not success:
                self.log_test(f"6.{i}.3 Generate {test_case['name']} persona", False, ["Failed to generate persona"])
                all_passed = False
                continue
            
            # Analyze contextual relevance
            contextual_score = 0
            total_checks = 0
            details = []
            
            # Check AI insights for occupation-specific content
            ai_insights = generated_persona.get('ai_insights', {})
            all_text = json.dumps(ai_insights).lower()
            
            for keyword in test_case['expected_keywords']:
                total_checks += 1
                if keyword in all_text:
                    contextual_score += 1
                    details.append(f"✅ Found occupation keyword: {keyword}")
                else:
                    details.append(f"❌ Missing occupation keyword: {keyword}")
            
            # Check recommendations for platform specificity
            recommendations = generated_persona.get('recommendations', [])
            platform_mentions = 0
            for platform in test_case['platforms']:
                for rec in recommendations:
                    if platform.lower() in rec.lower():
                        platform_mentions += 1
                        details.append(f"✅ Platform-specific recommendation: {platform}")
                        break
            
            total_checks += 1
            if platform_mentions >= len(test_case['platforms']) // 2:  # At least half the platforms mentioned
                contextual_score += 1
            
            # Calculate contextual percentage
            contextual_percentage = (contextual_score / total_checks * 100) if total_checks > 0 else 0
            details.append(f"📊 Contextual Score: {contextual_score}/{total_checks} ({contextual_percentage:.1f}%)")
            
            is_contextual = contextual_percentage >= 60
            
            self.log_test(f"6.{i}.1 Create {test_case['name']} persona", True, [f"Created persona ID: {persona_id}"])
            self.log_test(f"6.{i}.2 Update {test_case['name']} data", True, ["Updated with specific demographic data"])
            self.log_test(f"6.{i}.3 Generate {test_case['name']} persona", success, ["Successfully generated persona"])
            self.log_test(f"6.{i}.4 Contextual analysis for {test_case['name']}", is_contextual, details)
            
            if not is_contextual:
                all_passed = False
        
        return all_passed
    
    def test_7_fallback_dummy_data_verification(self):
        """Test 7: Ensure no fallback dummy data is being used unless absolutely necessary"""
        print("\n" + "="*80)
        print("TEST 7: Fallback dummy data verification")
        print("="*80)
        
        # Test with completely empty persona (should use fallback)
        success, persona_data = self.make_request('POST', 'personas', {
            "starting_method": "demographics",
            "name": "Empty Data Persona"
        })
        
        if not success:
            self.log_test("7.1 Create empty persona", False, ["Failed to create persona"])
            return False
        
        persona_id = persona_data.get('id')
        self.log_test("7.1 Create empty persona", True, [f"Created persona ID: {persona_id}"])
        
        # Don't update with any data - generate with minimal info
        success, generated_persona = self.make_request('POST', f'personas/{persona_id}/generate')
        
        if not success:
            self.log_test("7.2 Generate with no data", False, ["Failed to generate persona"])
            return False
        
        # Check if fallback data was used appropriately
        fallback_indicators = []
        appropriate_fallback = []
        
        # Known fallback patterns from the code
        ai_insights = generated_persona.get('ai_insights', {})
        personality_traits = ai_insights.get('personality_traits', [])
        
        fallback_traits = ["Data-driven", "Research-oriented", "Platform-savvy", "Goal-focused"]
        for trait in personality_traits:
            if trait in fallback_traits:
                fallback_indicators.append(f"Fallback trait: {trait}")
        
        recommendations = generated_persona.get('recommendations', [])
        fallback_recs = ["Leverage data-driven marketing strategies", "Focus on platform-specific content optimization"]
        for rec in recommendations:
            if any(fallback in rec for fallback in fallback_recs):
                fallback_indicators.append(f"Fallback recommendation: {rec[:50]}...")
        
        pain_points = generated_persona.get('pain_points', [])
        fallback_pains = ["Information overload from multiple data sources", "Platform integration complexities"]
        for pain in pain_points:
            if any(fallback in pain for fallback in fallback_pains):
                fallback_indicators.append(f"Fallback pain point: {pain[:50]}...")
        
        # For empty data, fallback is appropriate
        fallback_appropriate = len(fallback_indicators) > 0
        
        details = []
        details.extend([f"✅ Appropriate fallback: {indicator}" for indicator in fallback_indicators])
        details.append(f"📊 Fallback indicators found: {len(fallback_indicators)}")
        
        if fallback_appropriate:
            details.append("✅ Fallback data used appropriately for empty persona")
        else:
            details.append("⚠️ No clear fallback patterns detected")
        
        self.log_test("7.2 Generate with no data", success, ["Successfully generated persona"])
        self.log_test("7.3 Appropriate fallback usage", fallback_appropriate, details)
        
        # Now test with some data - should NOT use fallback
        success, persona_data2 = self.make_request('POST', 'personas', {
            "starting_method": "demographics", 
            "name": "Some Data Persona"
        })
        
        if not success:
            self.log_test("7.4 Create persona with some data", False, ["Failed to create persona"])
            return False
        
        persona_id2 = persona_data2.get('id')
        
        # Update with some demographic data
        success, update_response = self.make_request('PUT', f'personas/{persona_id2}', {
            "demographics": {
                "age_range": "25-40",
                "gender": "Female",
                "occupation": "Teacher"
            },
            "completed_steps": [1]
        })
        
        if not success:
            self.log_test("7.5 Update with some data", False, ["Failed to update persona"])
            return False
        
        # Generate persona
        success, generated_persona2 = self.make_request('POST', f'personas/{persona_id2}/generate')
        
        if not success:
            self.log_test("7.6 Generate with some data", False, ["Failed to generate persona"])
            return False
        
        # Check that fallback was NOT used inappropriately
        fallback_indicators2 = []
        ai_insights2 = generated_persona2.get('ai_insights', {})
        personality_traits2 = ai_insights2.get('personality_traits', [])
        
        for trait in personality_traits2:
            if trait in fallback_traits:
                fallback_indicators2.append(f"Inappropriate fallback trait: {trait}")
        
        recommendations2 = generated_persona2.get('recommendations', [])
        for rec in recommendations2:
            if any(fallback in rec for fallback in fallback_recs):
                fallback_indicators2.append(f"Inappropriate fallback rec: {rec[:50]}...")
        
        no_inappropriate_fallback = len(fallback_indicators2) == 0
        
        details2 = []
        if no_inappropriate_fallback:
            details2.append("✅ No inappropriate fallback data used with available demographics")
        else:
            details2.extend([f"❌ {indicator}" for indicator in fallback_indicators2])
        
        # Check for age-appropriate content instead
        teacher_appropriate = False
        millennial_appropriate = False
        
        all_text2 = json.dumps(generated_persona2).lower()
        if "teacher" in all_text2 or "education" in all_text2 or "student" in all_text2:
            teacher_appropriate = True
            details2.append("✅ Teacher-specific content generated")
        
        if any(trait in ["Tech-savvy", "Value-conscious", "Experience-focused"] for trait in personality_traits2):
            millennial_appropriate = True
            details2.append("✅ Millennial-appropriate traits generated")
        
        contextual_generation = teacher_appropriate or millennial_appropriate
        
        self.log_test("7.4 Create persona with some data", True, [f"Created persona ID: {persona_id2}"])
        self.log_test("7.5 Update with some data", True, ["Updated with teacher demographics"])
        self.log_test("7.6 Generate with some data", success, ["Successfully generated persona"])
        self.log_test("7.7 No inappropriate fallback", no_inappropriate_fallback and contextual_generation, details2)
        
        return fallback_appropriate and no_inappropriate_fallback and contextual_generation
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 Starting Comprehensive BCM VentasAI Persona Generator Tests")
        print("Focus: Testing comprehensive fix for dummy data issue")
        print("="*80)
        
        test_results = []
        
        # Run all tests
        test_results.append(self.test_1_multi_source_with_uploaded_data())
        test_results.append(self.test_2_multi_source_demographics_only())
        test_results.append(self.test_3_regular_persona_good_demographics())
        test_results.append(self.test_4_regular_persona_limited_demographics())
        test_results.append(self.test_5_openai_integration_verification())
        test_results.append(self.test_6_contextual_insights_verification())
        test_results.append(self.test_7_fallback_dummy_data_verification())
        
        # Print summary
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("="*80)
        
        passed_tests = sum(1 for result in test_results if result)
        total_tests = len(test_results)
        
        print(f"Total Major Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests / total_tests * 100):.1f}%")
        
        print(f"\nDetailed Results:")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Overall Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        # Detailed breakdown
        print(f"\n📋 Test Breakdown:")
        for test_name, result in self.test_results.items():
            status = "✅" if result["success"] else "❌"
            print(f"{status} {test_name}")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    # Get backend URL
    backend_url = "https://28426961-bcbc-4f0c-9e2c-9ae3cc74eaf5.preview.emergentagent.com/api"
    
    # Run comprehensive tests
    tester = ComprehensivePersonaGeneratorTester(backend_url)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL COMPREHENSIVE TESTS PASSED!")
        print("✅ The comprehensive fix for dummy data issue is working correctly")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("❌ Issues detected with the dummy data fix implementation")
    
    exit(0 if success else 1)

import os
import sys
import tempfile
import pandas as pd
from typing import Dict, Any, List
import csv

# Add the backend directory to the path
sys.path.insert(0, '/app/backend')

# Import the file parser module
from external_integrations.file_parsers import ResonateFileParser

def create_test_csv_file():
    """Create a test CSV file with realistic demographic data"""
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, "demographics.csv")
    
    with open(csv_path, 'w') as f:
        f.write("Age Group,Gender,Household Income,Education Level,Location,Occupation\n")
        f.write("25-34,Female,\"$50,000-$75,000\",\"Bachelor's Degree\",New York,Marketing Manager\n")
        f.write("35-44,Male,\"$75,000-$100,000\",\"Master's Degree\",California,Software Engineer\n")
        f.write("18-24,Female,\"$25,000-$50,000\",Some College,Texas,Student\n")
        f.write("41-56,Male,\"$100,000-$150,000\",PhD,Illinois,Executive\n")
        f.write("57-75,Female,\"$150,000+\",\"Master's Degree\",Florida,Retired\n")
    
    return csv_path

def fix_parse_csv_method():
    """Fix the parse_csv method in the ResonateFileParser class"""
    def new_parse_csv(self, file_path: str) -> Dict[str, Any]:
        """Parse CSV file and extract demographic/behavioral data"""
        try:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = 'utf-8'  # Default to utf-8
                try:
                    import chardet
                    detected = chardet.detect(raw_data)
                    if detected and detected['encoding']:
                        encoding = detected['encoding']
                except:
                    pass
            
            # Read CSV with proper quoting to handle commas in values
            df = pd.read_csv(
                file_path, 
                encoding=encoding,
                quotechar='"',  # Use double quotes as quote character
                quoting=csv.QUOTE_MINIMAL  # Quote fields with special characters
            )
            
            # Print sample data for debugging
            print(f"DEBUG: CSV Sample Data:\n{df.head(2)}")
            
            # Extract insights based on common Resonate column patterns
            insights = self.extract_csv_insights(df)
            
            return {
                'type': 'csv_data',
                'source': os.path.basename(file_path),
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': df.columns.tolist(),
                'insights': insights,
                'sample_data': df.head(3).to_dict('records') if len(df) > 0 else []
            }
            
        except Exception as e:
            print(f"Error parsing CSV file {file_path}: {str(e)}")
            return {
                'type': 'csv_data',
                'source': os.path.basename(file_path),
                'error': str(e)
            }
    
    # Replace the original method with our fixed version
    ResonateFileParser.parse_csv = new_parse_csv
    
    print("✅ parse_csv method fixed")

def fix_extract_csv_insights_method():
    """Fix the extract_csv_insights method in the ResonateFileParser class"""
    def new_extract_csv_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract insights from CSV data based on column names and content"""
        insights = {
            'demographics': {},
            'psychographics': {},
            'media_consumption': {},
            'brand_affinity': {},
            'behavioral': {}
        }
        
        # Print column names for debugging
        print(f"DEBUG: CSV Columns: {df.columns.tolist()}")
        
        # Demographics extraction with improved column matching
        demo_fields = {
            'age': ['age', 'age group', 'age range', 'age_group', 'age_range'],
            'gender': ['gender', 'sex', 'gender identity', 'gender_identity'],
            'income': ['income', 'household income', 'household_income', 'hh income', 'hh_income', 'annual income', 'annual_income'],
            'education': ['education', 'education level', 'education_level', 'edu level', 'edu_level', 'highest education'],
            'location': ['location', 'city', 'state', 'region', 'zip', 'address'],
            'occupation': ['occupation', 'job', 'profession', 'employment', 'job title', 'job_title']
        }
        
        # Process each demographic field
        for demo_type, keywords in demo_fields.items():
            # Find matching columns
            matching_cols = []
            for col in df.columns:
                col_lower = col.lower()
                if any(keyword.lower() == col_lower or keyword.lower() in col_lower for keyword in keywords):
                    matching_cols.append(col)
            
            if matching_cols:
                col = matching_cols[0]  # Use the first matching column
                
                # Get value counts for this column
                try:
                    # Print sample values for debugging
                    sample_values = df[col].head(3).tolist()
                    print(f"DEBUG: Sample values for {col}: {sample_values}")
                    
                    value_counts = df[col].value_counts().head(5).to_dict()
                    
                    # Store the results
                    insights['demographics'][demo_type] = {
                        'source_column': col,
                        'top_values': value_counts
                    }
                except Exception as e:
                    print(f"Error processing column {col}: {e}")
        
        # Media consumption patterns - improved matching
        media_keywords = ['media', 'tv', 'social', 'digital', 'platform', 'channel', 'social media']
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword.lower() in col_lower for keyword in media_keywords):
                try:
                    if df[col].dtype in ['object', 'category'] or str(df[col].dtype).startswith('str'):
                        value_counts = df[col].value_counts().head(10).to_dict()
                        insights['media_consumption'][col] = value_counts
                except Exception as e:
                    print(f"Error processing media column {col}: {e}")
        
        # Brand affinity - improved matching
        brand_keywords = ['brand', 'product', 'company', 'preference', 'loyalty', 'purchase']
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword.lower() in col_lower for keyword in brand_keywords):
                try:
                    if df[col].dtype in ['object', 'category'] or str(df[col].dtype).startswith('str'):
                        value_counts = df[col].value_counts().head(10).to_dict()
                        insights['brand_affinity'][col] = value_counts
                except Exception as e:
                    print(f"Error processing brand column {col}: {e}")
        
        return insights
    
    # Replace the original method with our fixed version
    ResonateFileParser.extract_csv_insights = new_extract_csv_insights
    
    print("✅ extract_csv_insights method fixed")

def test_fixed_csv_parsing():
    """Test the fixed CSV parsing logic"""
    # Create a test CSV file
    csv_path = create_test_csv_file()
    
    print("\n🔍 Testing Fixed CSV Parsing...")
    print(f"   CSV file: {csv_path}")
    
    try:
        # Fix the CSV parsing methods
        fix_parse_csv_method()
        fix_extract_csv_insights_method()
        
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

def fix_server_mapping():
    """Fix the persona creation from Resonate data in server.py"""
    # This would modify the server.py file to correctly map the parsed data
    # For now, we'll just print instructions
    print("\n🔧 SERVER MAPPING FIX INSTRUCTIONS:")
    print("   1. In server.py, update the resonate-create endpoint to properly handle the parsed data")
    print("   2. Ensure gender values are properly extracted (e.g., 'Female', 'Male')")
    print("   3. Ensure income values include the full range (e.g., '$50,000-$75,000')")
    print("   4. Ensure age ranges are properly mapped to the AgeRange enum")
    print("   5. Restart the backend service after making these changes")

if __name__ == "__main__":
    test_fixed_csv_parsing()
    fix_server_mapping()

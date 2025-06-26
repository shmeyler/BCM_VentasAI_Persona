
import os
import sys
import tempfile
import zipfile
import pandas as pd
import csv

# Create a properly quoted CSV file
def create_quoted_csv():
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, "demographics.csv")
    
    with open(csv_path, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Age Group", "Gender", "Household Income", "Education Level", "Location", "Occupation"])
        writer.writerow(["25-34", "Female", "$50,000-$75,000", "Bachelor's Degree", "New York", "Marketing Manager"])
        writer.writerow(["35-44", "Male", "$75,000-$100,000", "Master's Degree", "California", "Software Engineer"])
        writer.writerow(["18-24", "Female", "$25,000-$50,000", "Some College", "Texas", "Student"])
        writer.writerow(["41-56", "Male", "$100,000-$150,000", "PhD", "Illinois", "Executive"])
        writer.writerow(["57-75", "Female", "$150,000+", "Master's Degree", "Florida", "Retired"])
    
    return csv_path, temp_dir

# Create a ZIP file with the CSV
def create_zip_with_csv(csv_path):
    zip_path = os.path.join(os.path.dirname(csv_path), "test_data.zip")
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        zip_file.write(csv_path, os.path.basename(csv_path))
    
    return zip_path

# Test uploading the ZIP file
def test_upload_zip(zip_path):
    import requests
    
    backend_url = "https://28426961-bcbc-4f0c-9e2c-9ae3cc74eaf5.preview.emergentagent.com/api"
    url = f"{backend_url}/personas/resonate-upload"
    
    files = {
        'file': ('test_data.zip', open(zip_path, 'rb'), 'application/zip')
    }
    
    print(f"Uploading ZIP file to {url}...")
    response = requests.post(url, files=files, timeout=30)
    
    if response.status_code == 200:
        print(f"✅ Upload successful - Status: {response.status_code}")
        result = response.json()
        
        if 'parsed_data' in result and 'demographics' in result['parsed_data']:
            demo_data = result['parsed_data']['demographics']
            print(f"\n📊 DEMOGRAPHICS DATA:")
            
            for field, data in demo_data.items():
                print(f"   {field.capitalize()}:")
                if isinstance(data, list) and len(data) > 0:
                    source = data[0].get('source', 'Unknown')
                    top_values = data[0].get('data', {}).get('top_values', {})
                    print(f"      Source: {source}")
                    print(f"      Values: {list(top_values.keys())[:3]}")
        
        return result
    else:
        print(f"❌ Upload failed - Status: {response.status_code}")
        try:
            print(f"   Error: {response.json()}")
        except:
            print(f"   Error: {response.text[:200]}")
        return None

# Main function
def main():
    print("🔍 Testing Resonate CSV Parsing with Properly Quoted CSV...")
    
    # Create CSV and ZIP files
    csv_path, temp_dir = create_quoted_csv()
    print(f"Created CSV file: {csv_path}")
    
    # Read the CSV with pandas to verify it's correct
    df = pd.read_csv(csv_path)
    print("\nCSV Content:")
    print(df.head())
    
    # Create ZIP file
    zip_path = create_zip_with_csv(csv_path)
    print(f"Created ZIP file: {zip_path}")
    
    # Test uploading the ZIP
    result = test_upload_zip(zip_path)
    
    # Clean up
    os.remove(zip_path)
    os.remove(csv_path)
    os.rmdir(temp_dir)
    
    print("\n✅ Test completed")

if __name__ == "__main__":
    main()

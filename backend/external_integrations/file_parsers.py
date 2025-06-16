"""
Real File Parsing Module for Resonate Data
Handles ZIP extraction and parsing of CSV, PDF, PNG, Excel files
"""

import os
import zipfile
import tempfile
import io
import csv
import json
import mimetypes
import chardet
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

import pandas as pd
import PyPDF2
from PIL import Image
from openpyxl import load_workbook


class ResonateFileParser:
    """Main class for parsing Resonate data files"""
    
    def __init__(self):
        self.supported_formats = {
            'csv': self.parse_csv,
            'xlsx': self.parse_excel,
            'xls': self.parse_excel,
            'pdf': self.parse_pdf,
            'png': self.parse_image,
            'jpg': self.parse_image,
            'jpeg': self.parse_image,
            'txt': self.parse_text
        }
    
    def extract_and_parse_zip(self, zip_file_path: str) -> Dict[str, Any]:
        """
        Extract ZIP file and parse all supported files within it
        Returns structured data suitable for persona generation
        """
        try:
            extracted_files = []
            parsed_data = {
                'demographics': {},
                'psychographics': {},
                'media_consumption': {},
                'brand_affinity': {},
                'behavioral_insights': {},
                'source_files': []
            }
            
            # Create temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract ZIP file
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Process all extracted files
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.startswith('.'):  # Skip hidden files
                            continue
                            
                        file_path = os.path.join(root, file)
                        file_info = self.get_file_info(file_path)
                        extracted_files.append(file_info)
                        
                        # Parse the file content
                        file_data = self.parse_file(file_path)
                        if file_data:
                            self.merge_parsed_data(parsed_data, file_data, file_info)
            
            return {
                'success': True,
                'extracted_files': extracted_files,
                'parsed_data': parsed_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'extracted_files': [],
                'parsed_data': {}
            }
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about a file"""
        try:
            file_stat = os.stat(file_path)
            file_name = os.path.basename(file_path)
            file_ext = Path(file_path).suffix.lower().lstrip('.')
            
            # Detect MIME type using mimetypes
            mime_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            
            return {
                'name': file_name,
                'size': file_stat.st_size,
                'type': self.get_file_type_description(file_ext, mime_type),
                'format': file_ext,
                'mime_type': mime_type,
                'parseable': file_ext in self.supported_formats
            }
        except Exception as e:
            return {
                'name': os.path.basename(file_path),
                'size': 0,
                'type': 'Unknown',
                'format': 'unknown',
                'mime_type': 'unknown',
                'parseable': False,
                'error': str(e)
            }
    
    def get_file_type_description(self, ext: str, mime_type: str) -> str:
        """Get human-readable file type description"""
        type_map = {
            'csv': 'CSV Data File',
            'xlsx': 'Excel Spreadsheet',
            'xls': 'Excel Spreadsheet (Legacy)',
            'pdf': 'PDF Document',
            'png': 'PNG Image',
            'jpg': 'JPEG Image',
            'jpeg': 'JPEG Image',
            'txt': 'Text Document'
        }
        return type_map.get(ext, f'Unknown ({mime_type})')
    
    def parse_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Parse a single file based on its extension"""
        try:
            file_ext = Path(file_path).suffix.lower().lstrip('.')
            parser_func = self.supported_formats.get(file_ext)
            
            if parser_func:
                return parser_func(file_path)
            else:
                return None
                
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return None
    
    def parse_csv(self, file_path: str) -> Dict[str, Any]:
        """Parse CSV file and extract demographic/behavioral data"""
        try:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
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
    
    def extract_csv_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract insights from Resonate CSV data based on actual Resonate export format"""
        insights = {
            'demographics': {},
            'psychographics': {},
            'media_consumption': {},
            'brand_affinity': {},
            'behavioral': {}
        }
        
        # Print column names for debugging
        print(f"DEBUG: Processing Resonate CSV with columns: {df.columns.tolist()}")
        
        # Handle Resonate-style data with Insight/Category structure
        if 'Insight' in df.columns and 'Insight Value' in df.columns:
            print("DEBUG: Found Resonate Insight format")
            self._process_resonate_insights(df, insights)
        
        # Handle Category-based data (like web behavior)
        elif 'Category' in df.columns:
            print("DEBUG: Found Category-based data")
            self._process_category_data(df, insights)
        
        # Handle Domain/Site data (web behavior)
        elif 'Domain Name' in df.columns:
            print("DEBUG: Found Domain/Site data")
            self._process_domain_data(df, insights)
        
        # Fallback to original demographic parsing for simple CSV files
        else:
            print("DEBUG: Using fallback demographic parsing")
            self._process_simple_demographics(df, insights)
        
        return insights
    
    def _process_resonate_insights(self, df: pd.DataFrame, insights: Dict[str, Any]):
        """Process Resonate data with Insight/Insight Value columns"""
        try:
            # Group by categories and subcategories
            for _, row in df.iterrows():
                insight = str(row.get('Insight', '')).lower()
                insight_value = row.get('Insight Value', '')
                category = row.get('Category', '')
                subcategory1 = row.get('Subcategory1', '')
                composition = row.get('Composition (%)', 0)
                
                # Demographics mapping
                if any(demo_term in insight for demo_term in ['age', 'gender', 'income', 'education', 'location', 'occupation']):
                    demo_type = self._categorize_demographic(insight)
                    if demo_type:
                        if demo_type not in insights['demographics']:
                            insights['demographics'][demo_type] = []
                        insights['demographics'][demo_type].append({
                            'source': 'Resonate Insights',
                            'data': {
                                'insight': insight,
                                'value': insight_value,
                                'composition': composition,
                                'category': category,
                                'subcategory': subcategory1
                            }
                        })
                
                # Media consumption mapping
                elif any(media_term in insight for media_term in ['social media', 'platform', 'streaming', 'tv', 'digital', 'mobile', 'device']):
                    if 'media_platforms' not in insights['media_consumption']:
                        insights['media_consumption']['media_platforms'] = []
                    insights['media_consumption']['media_platforms'].append({
                        'source': 'Resonate Insights',
                        'data': {
                            'insight': insight,
                            'value': insight_value,
                            'composition': composition
                        }
                    })
                
                # Brand/Shopping behavior
                elif any(brand_term in insight for brand_term in ['brand', 'shopping', 'purchase', 'retail', 'store']):
                    if 'shopping_behavior' not in insights['brand_affinity']:
                        insights['brand_affinity']['shopping_behavior'] = []
                    insights['brand_affinity']['shopping_behavior'].append({
                        'source': 'Resonate Insights',
                        'data': {
                            'insight': insight,
                            'value': insight_value,
                            'composition': composition
                        }
                    })
                
                # Psychographics/Values
                elif any(psycho_term in insight for psycho_term in ['value', 'lifestyle', 'interest', 'personality', 'attitude']):
                    if 'values_interests' not in insights['psychographics']:
                        insights['psychographics']['values_interests'] = []
                    insights['psychographics']['values_interests'].append({
                        'source': 'Resonate Insights',
                        'data': {
                            'insight': insight,
                            'value': insight_value,
                            'composition': composition
                        }
                    })
                
        except Exception as e:
            print(f"Error processing Resonate insights: {e}")
    
    def _process_category_data(self, df: pd.DataFrame, insights: Dict[str, Any]):
        """Process category-based data (web behavior, interests)"""
        try:
            for _, row in df.iterrows():
                category = row.get('Category', '')
                if 'Category Index' in df.columns:
                    index = row.get('Category Index', 0)
                    share = row.get('Category Share of Total Visits (if available)', 0)
                    
                    if 'web_behavior' not in insights['media_consumption']:
                        insights['media_consumption']['web_behavior'] = []
                    insights['media_consumption']['web_behavior'].append({
                        'source': 'Web Behavior Data',
                        'data': {
                            'category': category,
                            'index': index,
                            'share': share
                        }
                    })
        except Exception as e:
            print(f"Error processing category data: {e}")
    
    def _process_domain_data(self, df: pd.DataFrame, insights: Dict[str, Any]):
        """Process domain/site data"""
        try:
            for _, row in df.iterrows():
                domain = row.get('Domain Name', '')
                rating = row.get('Site Rating', 0)
                category = row.get('Category', '')
                
                if 'website_preferences' not in insights['media_consumption']:
                    insights['media_consumption']['website_preferences'] = []
                insights['media_consumption']['website_preferences'].append({
                    'source': 'Website Data',
                    'data': {
                        'domain': domain,
                        'rating': rating,
                        'category': category
                    }
                })
        except Exception as e:
            print(f"Error processing domain data: {e}")
    
    def _categorize_demographic(self, insight: str) -> str:
        """Categorize a Resonate insight into demographic type"""
        if any(term in insight for term in ['age', 'year', 'old']):
            return 'age'
        elif any(term in insight for term in ['gender', 'male', 'female', 'woman', 'man']):
            return 'gender'
        elif any(term in insight for term in ['income', 'salary', 'earn', 'household']):
            return 'income'
        elif any(term in insight for term in ['education', 'degree', 'college', 'university', 'school']):
            return 'education'
        elif any(term in insight for term in ['location', 'live', 'city', 'state', 'zip', 'area']):
            return 'location'
        elif any(term in insight for term in ['job', 'work', 'occupation', 'career', 'employed']):
            return 'occupation'
        return None
    
    def _process_simple_demographics(self, df: pd.DataFrame, insights: Dict[str, Any]):
        """Fallback processing for simple demographic CSV files"""
        # This is the original logic for simple CSV files
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
                    insights['demographics'][demo_type] = [{
                        'source': col,
                        'data': {
                            'top_values': value_counts
                        }
                    }]
                except Exception as e:
                    print(f"Error processing column {col}: {e}")
    
    def parse_excel(self, file_path: str) -> Dict[str, Any]:
        """Parse Excel file (both .xlsx and .xls)"""
        try:
            # Read all sheets
            xl_file = pd.ExcelFile(file_path)
            sheets_data = {}
            
            for sheet_name in xl_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Extract insights from each sheet
                insights = self.extract_csv_insights(df)  # Same logic as CSV
                
                sheets_data[sheet_name] = {
                    'row_count': len(df),
                    'column_count': len(df.columns),
                    'columns': df.columns.tolist(),
                    'insights': insights,
                    'sample_data': df.head(3).to_dict('records') if len(df) > 0 else []
                }
            
            return {
                'type': 'excel_data',
                'source': os.path.basename(file_path),
                'sheets': sheets_data,
                'sheet_names': xl_file.sheet_names
            }
            
        except Exception as e:
            return {
                'type': 'excel_data',
                'source': os.path.basename(file_path),
                'error': str(e)
            }
    
    def parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse PDF file and extract text content"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text()
            
            # Extract insights from text
            insights = self.extract_text_insights(text_content)
            
            return {
                'type': 'pdf_document',
                'source': os.path.basename(file_path),
                'page_count': len(pdf_reader.pages),
                'text_length': len(text_content),
                'insights': insights,
                'sample_text': text_content[:500] + "..." if len(text_content) > 500 else text_content
            }
            
        except Exception as e:
            return {
                'type': 'pdf_document',
                'source': os.path.basename(file_path),
                'error': str(e)
            }
    
    def parse_image(self, file_path: str) -> Dict[str, Any]:
        """Parse image file and extract metadata"""
        try:
            with Image.open(file_path) as img:
                # Basic image info
                width, height = img.size
                format_type = img.format
                mode = img.mode
                
                # Check if this might be a chart/graph (basic heuristic)
                is_chart = self.detect_chart_image(img)
                
                return {
                    'type': 'image_data',
                    'source': os.path.basename(file_path),
                    'dimensions': {'width': width, 'height': height},
                    'format': format_type,
                    'mode': mode,
                    'is_chart': is_chart,
                    'insights': {
                        'chart_type': 'data_visualization' if is_chart else 'general_image',
                        'potential_data': 'Brand affinity or demographic charts' if is_chart else 'Supporting visual'
                    }
                }
                
        except Exception as e:
            return {
                'type': 'image_data',
                'source': os.path.basename(file_path),
                'error': str(e)
            }
    
    def parse_text(self, file_path: str) -> Dict[str, Any]:
        """Parse text file"""
        try:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            
            # Read text content
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # Extract insights
            insights = self.extract_text_insights(content)
            
            return {
                'type': 'text_document',
                'source': os.path.basename(file_path),
                'length': len(content),
                'insights': insights,
                'sample_text': content[:500] + "..." if len(content) > 500 else content
            }
            
        except Exception as e:
            return {
                'type': 'text_document',
                'source': os.path.basename(file_path),
                'error': str(e)
            }
    
    def extract_text_insights(self, text: str) -> Dict[str, Any]:
        """Extract insights from text content"""
        text_lower = text.lower()
        
        # Keywords for different categories
        keywords = {
            'demographics': ['age', 'gender', 'income', 'education', 'location', 'occupation'],
            'psychographics': ['personality', 'values', 'attitudes', 'interests', 'lifestyle'],
            'media_consumption': ['social media', 'television', 'digital', 'streaming', 'podcast'],
            'brand_affinity': ['brand', 'product', 'purchase', 'loyalty', 'preference']
        }
        
        insights = {}
        for category, word_list in keywords.items():
            matches = [word for word in word_list if word in text_lower]
            if matches:
                insights[category] = {
                    'mentioned_concepts': matches,
                    'relevance_score': len(matches) / len(word_list)
                }
        
        return insights
    
    def detect_chart_image(self, img: Image.Image) -> bool:
        """Basic heuristic to detect if image might be a chart/graph"""
        try:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Simple heuristic: charts often have strong color contrasts and geometric patterns
            # This is a basic implementation - could be enhanced with ML
            width, height = img.size
            if width > 200 and height > 200:  # Reasonable size for a chart
                return True
            return False
        except:
            return False
    
    def merge_parsed_data(self, parsed_data: Dict[str, Any], file_data: Dict[str, Any], file_info: Dict[str, Any]):
        """Merge file data into the main parsed data structure"""
        if 'insights' in file_data:
            insights = file_data['insights']
            
            # Merge demographics
            if 'demographics' in insights:
                for key, value in insights['demographics'].items():
                    if key not in parsed_data['demographics']:
                        parsed_data['demographics'][key] = []
                    parsed_data['demographics'][key].append({
                        'source': file_info['name'],
                        'data': value
                    })
            
            # Merge psychographics
            if 'psychographics' in insights:
                for key, value in insights['psychographics'].items():
                    if key not in parsed_data['psychographics']:
                        parsed_data['psychographics'][key] = []
                    parsed_data['psychographics'][key].append({
                        'source': file_info['name'],
                        'data': value
                    })
            
            # Merge media consumption
            if 'media_consumption' in insights:
                for key, value in insights['media_consumption'].items():
                    if key not in parsed_data['media_consumption']:
                        parsed_data['media_consumption'][key] = []
                    parsed_data['media_consumption'][key].append({
                        'source': file_info['name'],
                        'data': value
                    })
            
            # Merge brand affinity
            if 'brand_affinity' in insights:
                for key, value in insights['brand_affinity'].items():
                    if key not in parsed_data['brand_affinity']:
                        parsed_data['brand_affinity'][key] = []
                    parsed_data['brand_affinity'][key].append({
                        'source': file_info['name'],
                        'data': value
                    })
        
        # Add source file info
        parsed_data['source_files'].append({
            'name': file_info['name'],
            'type': file_data.get('type', 'unknown'),
            'source': file_data.get('source', ''),
            'processed': 'insights' in file_data,
            'error': file_data.get('error')
        })


# Utility function for the API endpoint
def parse_resonate_zip(zip_file_path: str) -> Dict[str, Any]:
    """
    Main function to parse Resonate ZIP file
    Returns structured data for persona generation
    """
    parser = ResonateFileParser()
    return parser.extract_and_parse_zip(zip_file_path)
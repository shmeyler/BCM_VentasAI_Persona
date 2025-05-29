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
import magic
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
            
            # Detect MIME type
            mime_type = magic.from_file(file_path, mime=True)
            
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
            
            # Read CSV
            df = pd.read_csv(file_path, encoding=encoding)
            
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
            return {
                'type': 'csv_data',
                'source': os.path.basename(file_path),
                'error': str(e)
            }
    
    def extract_csv_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract insights from CSV data based on column names and content"""
        insights = {
            'demographics': {},
            'psychographics': {},
            'media_consumption': {},
            'brand_affinity': {},
            'behavioral': {}
        }
        
        columns_lower = [col.lower() for col in df.columns]
        
        # Demographics extraction
        demo_fields = {
            'age': ['age', 'age_group', 'age_range'],
            'gender': ['gender', 'sex'],
            'income': ['income', 'household_income', 'hh_income'],
            'education': ['education', 'edu_level', 'education_level'],
            'location': ['location', 'city', 'state', 'region', 'zip'],
            'occupation': ['occupation', 'job', 'profession', 'employment']
        }
        
        for demo_type, keywords in demo_fields.items():
            for keyword in keywords:
                matching_cols = [col for col in df.columns if keyword in col.lower()]
                if matching_cols:
                    col = matching_cols[0]
                    if col in df.columns:
                        value_counts = df[col].value_counts().head(5).to_dict()
                        insights['demographics'][demo_type] = {
                            'source_column': col,
                            'top_values': value_counts
                        }
        
        # Media consumption patterns
        media_keywords = ['media', 'tv', 'social', 'digital', 'platform', 'channel']
        for col in df.columns:
            if any(keyword in col.lower() for keyword in media_keywords):
                if df[col].dtype in ['object', 'category']:
                    value_counts = df[col].value_counts().head(10).to_dict()
                    insights['media_consumption'][col] = value_counts
        
        # Brand affinity
        brand_keywords = ['brand', 'product', 'company', 'preference']
        for col in df.columns:
            if any(keyword in col.lower() for keyword in brand_keywords):
                if df[col].dtype in ['object', 'category']:
                    value_counts = df[col].value_counts().head(10).to_dict()
                    insights['brand_affinity'][col] = value_counts
        
        return insights
    
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
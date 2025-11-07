Project Name: W-2 Parser & Insight Generator (Gemini AI)

Overview

This project extracts structured data and meaningful insights from a W-2 form (PDF or image) using Google Gemini AI and OCR.
It can identify key tax fields (like wages, state taxes, etc.) and provide human-readable insights such as missing data, address mismatches, or unusual tax rates.

Setup Instructions
Requirements

Make sure you have installed:

pip install google-generativeai pdf2image pytesseract pillow

Install Poppler (for PDF to image conversion)

Download Poppler for Windows:
https://github.com/oschwartz10612/poppler-windows/releases

Extract it somewhere (e.g., C:\Users\<you>\Downloads\poppler-25.07.0)

Copy the path to its Library\bin folder.
Example:

C:\Users\<you>\Downloads\poppler-25.07.0\Library\bin

et Your API Key

You must have a Google Gemini API Key.
Set it in your terminal before running the script:

set GEMINI_API_KEY=your_google_gemini_api_key

Run the Program
python process_w2.py


When prompted:

Enter W-2 file path: sample_w2.jpg

Output Example
{
  "fields": {
    "employee": {"name": "Jesan Rahaman", "address": "AK 8133", "ssn_last4": "5787"},
    "employer": {"name": "DesignNext", "ein_last4": "", "address": "AK 8133"},
    "state": [{"state_code": "AL", "state_wages": "80000.00", "state_tax": "3835.00"}]
  },
  "insights": [
    "Missing Federal Data",
    "Address mismatch (AK vs AL)",
    "Reasonable AL state tax"
  ],
  "quality": ["Extraction and insight generation successful."]
}

Test Mode

You can test locally without making Gemini API calls:

python process_w2.py
When prompted, it uses fake data if test_mode=True
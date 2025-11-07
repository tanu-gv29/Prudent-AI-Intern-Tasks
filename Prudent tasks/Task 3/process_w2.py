import os, json, pytesseract
from pdf2image import convert_from_path
from PIL import Image
import google.generativeai as genai

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\TANUSHRI\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"

def ocr_extract_text(file_path):
    
    POPPLER_PATH = r"C:\Users\TANUSHRI\Downloads\Release-25.07.0-0\poppler-25.07.0\Library\bin"
    print(f"Using Poppler path: {POPPLER_PATH}")

    if not os.path.exists(POPPLER_PATH):
        raise FileNotFoundError(f"Poppler path not found: {POPPLER_PATH}")

    if file_path.lower().endswith(".pdf"):
        pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
    else:
        text = pytesseract.image_to_string(Image.open(file_path))
    return text


def process_w2(file_path, test_mode=False):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    text = ocr_extract_text(file_path)
    if not text.strip():
        return {"error": "No readable text found"}

    with open("prompts/extraction_prompt.txt") as f:
        extract_prompt = f.read()
    with open("prompts/insight_prompt.txt") as f:
        insight_prompt = f.read()

    if test_mode:
        return {
            "fields": {"employee": {"name": "Test User", "ssn_last4": "1234"}},
            "insights": ["Test mode active – no network call."],
            "quality": ["Mock data only."]
        }

    model = genai.GenerativeModel("gemini-2.5-flash")
    extraction = model.generate_content([extract_prompt, text])
    print("Gemini raw output:\n", extraction.text)

    cleaned = extraction.text.strip()
    if cleaned.startswith("```"):
      cleaned = cleaned.strip("`")  # remove backticks
      cleaned = cleaned.replace("json", "", 1).strip()

    try:
      fields = json.loads(extraction.text)
    except Exception:
      print("Gemini did not return valid JSON. Showing raw text instead:")
      print(extraction.text)
      fields = {"error": "Invalid JSON", "raw_output": extraction.text}


    insight_input = json.dumps(fields)
    insights = model.generate_content([insight_prompt, insight_input])

    result = {
        "fields": fields,
        "insights": json.loads(insights.text) if insights.text.strip().startswith("[") else [insights.text],
        "quality": ["Extraction and insight generation successful."]
    }
    return result

if __name__ == "__main__":
    path = input("Enter W-2 file path: ")
    print(json.dumps(process_w2(path, test_mode=False), indent=2))

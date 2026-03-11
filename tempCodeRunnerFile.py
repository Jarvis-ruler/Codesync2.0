import google.generativeai as genai
import json
from PIL import Image
from yfinance import download

# 1. Put your actual API key here
genai.configure(api_key="AIzaSyDFFjqvk_XCCyyCimA7M3VGsFzNEFHzTtU")

def extract_lab_data(image_path):
    print("Loading image and waking up AI...")
    
    # Using Gemini 1.5 Flash - it's fast, free, and great at reading images
    model = genai.GenerativeModel('gemini-1.5-flash')
    img = Image.open(image_path)

    # 2. The Master Prompt
    prompt = """
    You are an expert code extractor for an engineering student's lab record system.
    Analyze this image containing a programming problem and code.
    1. Extract the 'question' (the problem statement or aim).
    2. Extract the 'code' (fix any obvious OCR typos, maintain proper indentation).
    Return the result strictly as a JSON object with exactly two keys: "question" and "code".
    """
    
    # 3. Call the API and force JSON output
    response = model.generate_content(
        [prompt, img],
        generation_config={"response_mime_type": "application/json"}
    )
    
    # 4. Parse and return the data
    try:
        lab_data = json.loads(response.text)
        return lab_data
    except Exception as e:
        print("Failed to parse AI response:", e)
        print("Raw response was:", response.text)
        return None

# --- Let's test it! ---
if __name__ == "__main__":
    # Change this to the name of a photo on your computer
    test_image = "sample_code.jpg" 
    
    try:
        result = extract_lab_data(download.j
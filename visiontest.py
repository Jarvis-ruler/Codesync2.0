import streamlit as st
import json
import time
from PIL import Image
from google import genai
from google.genai import types
from fpdf import FPDF

# --- PAGE SETUP ---
st.set_page_config(page_title="CodeSync Pro 2.0", page_icon="⚡", layout="centered")

st.title("⚡ CodeSync Pro 2.0")
st.markdown("### Powered by Gemini 2.5 Flash")

# --- AI EXTRACTION FUNCTION ---
def extract_lab_data(img, api_key, language):
    try:
        client = genai.Client(api_key=api_key)
        
        # TARGETING GEMINI 2.5 FLASH
        model_id = 'gemini-2.5-flash'
        
        prompt = f"""
        You are a senior {language} software engineer. 
        Analyze the provided image of a lab assignment.
        1. Extract the 'question' text precisely.
        2. Write production-grade, commented {language} 'code'.
        3. Provide the expected 'sample_output' in a clear console format.
        
        STRICT REQUIREMENT: Return a JSON ARRAY of objects with keys: "question", "code", "sample_output".
        """
        
        response = client.models.generate_content(
            model=model_id,
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1 # Low temperature for consistent JSON structure
            )
        )
        return json.loads(response.text)
    except Exception as e:
        if "429" in str(e):
            st.error("⏳ Quota Limit: Gemini 2.5 is busy. Please wait 30-60 seconds and try again.")
        else:
            st.error(f"System Error: {e}")
        return None

# --- PDF GENERATOR FUNCTION ---
def generate_pdf(lab_data, user_info, heading_prefix, output_filename="Lab_Record.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. FRONT COVER PAGE
    pdf.add_page()
    pdf.set_font("Arial", "B", 26)
    pdf.ln(50)
    pdf.cell(0, 20, "LABORATORY RECORD", ln=True, align='C')
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "Generated via CodeSync Pro", ln=True, align='C')
    pdf.ln(30)
    
    pdf.set_font("Arial", "", 14)
    details = [
        ("Name", user_info['name']),
        ("Class", user_info['class']),
        ("Section", user_info['sec']),
        ("Roll No", user_info['roll'])
    ]
    
    for key, value in details:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(40, 12, f"{key}:", ln=0)
        pdf.set_font("Arial", "", 14)
        pdf.cell(0, 12, f"{value}", ln=1)
        pdf.ln(2)

    # 2. EXPERIMENT PAGES
    for i, item in enumerate(lab_data, 1):
        pdf.add_page()
        
        # Heading
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"{heading_prefix} {i}", ln=True)
        pdf.ln(5)
        
        # Question
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, "QUESTION:", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, item.get('question', 'N/A'))
        pdf.ln(5)
        
        # Code
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, "SOURCE CODE:", ln=True)
        pdf.set_font("Courier", "", 9)
        # Using latin-1 to avoid PDF encoding crashes with special symbols
        code_body = item.get('code', '').encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 5, code_body, border=1)
        pdf.ln(5)
        
        # Output
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, "SAMPLE OUTPUT:", ln=True)
        pdf.set_font("Courier", "I", 9)
        pdf.set_fill_color(240, 240, 240) # Light grey background for output
        out_body = item.get('sample_output', '').encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 5, f"> {out_body}", fill=True)
        
    pdf.output(output_filename)
    return output_filename

# --- STREAMLIT UI ---
with st.sidebar:
    st.header("👤 Student Identity")
    u_name = st.text_input("Name", value="Md Faisal Hayat")
    u_class = st.text_input("Class/Year", placeholder="e.g. B.Tech ECE")
    u_sec = st.text_input("Section")
    u_roll = st.text_input("Roll Number")
    
    st.divider()
    st.header("🎨 PDF Customization")
    h_prefix = st.text_input("Heading (Experiment/Program)", value="Experiment")

user_key = st.text_input("Gemini API Key:", type="password")
lang = st.selectbox("Language:", ["C", "C++", "Python", "Java", "Auto-Detect"])
file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if st.button("🚀 Process & Generate"):
    if not (user_key and file and u_name):
        st.error("Please provide your name, API key, and an image!")
    else:
        with st.spinner("Analyzing with Gemini 2.5..."):
            img = Image.open(file)
            data = extract_lab_data(img, user_key, lang)
            
            if data:
                u_info = {"name": u_name, "class": u_class, "sec": u_sec, "roll": u_roll}
                pdf_path = generate_pdf(data, u_info, h_prefix)
                
                with open(pdf_path, "rb") as f:
                    st.download_button(f"📥 Download {u_name}_Lab.pdf", f, file_name=f"{u_name}_Lab_Record.pdf")
                st.success("PDF generated with Gemini 2.5 reasoning!")
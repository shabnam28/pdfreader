from google.cloud import documentai_v1 as documentai
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
import os, json, re, pandas as pd, glob

# ======================================================
# CONFIGURATION
# ======================================================
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cv-analyser-agent-c8418833717d.json"
project_id = os.environ["PROJECT_ID"]
docai_location = os.environ["LOCATION"] 
vertex_location = os.environ ["VERTEX_LOCATION"]    
processor_id = os.environ["PROCESSOR_ID"]
input_folder = os.environ["INPUT_FOLDER"]  
output_csv = os.environ["OUTPUT_CSV"]  

# Initialize Vertex AI
aiplatform.init(project=project_id, location=vertex_location)

# Prepare Gemini model
model = GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="You are an expert at text extraction and must only return a valid JSON object."
)
config = GenerationConfig(temperature=0)

# ======================================================
# PROMPT TEMPLATE
# ======================================================
def build_prompt(text):
    return f"""
You are an expert information extraction agent. Your task is to extract details for all individuals from the provided text and structure the output into a clean JSON array.

### Required JSON Structure:
[
  {{
    "full_name": "...",
    "first_name": "...",
    "last_name": "...",
    "title": "...",
    "telephone": "...",
    "mobile": "..."
  }}
]

Rules:
- Only include real people (ignore teams/departments)
- Remove prefixes (M., Mme, etc.)
- Split names correctly
- Normalize all phone numbers (keep + and digits)
- Return **only valid JSON** without explanations

TEXT:
{text}
"""

# ======================================================
# DOCUMENT AI FUNCTION
# ======================================================
def extract_text_from_pdf(file_path):
    """Processes a PDF file with Document AI and returns the extracted text."""
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{project_id}/locations/{docai_location}/processors/{processor_id}"

    with open(file_path, "rb") as f:
        raw_document = documentai.RawDocument(content=f.read(), mime_type="application/pdf")

    request = {"name": name, "raw_document": raw_document}
    result = client.process_document(request=request)
    return result.document.text.strip()

# ======================================================
# GEMINI FLASH FUNCTION
# ======================================================
def extract_json_from_text(text):
    """Uses Gemini Flash to extract structured info from text."""
    prompt = build_prompt(text)
    response = model.generate_content(contents=[prompt], generation_config=config)
    raw_output = response.text.strip()

    # Try direct JSON parsing
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        # Try to remove Markdown wrapper
        match = re.search(r'```json\s*(.*?)```', raw_output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except:
                return []
        return []

# ======================================================
# MAIN LOOP FOR MULTIPLE FILES
# ======================================================
all_records = []

pdf_files = glob.glob(os.path.join(input_folder, "*.pdf"))
print(f"Found {len(pdf_files)} PDF files to process...")

for pdf_file in pdf_files:
    print(f"\n🔍 Processing: {os.path.basename(pdf_file)}")

    try:
        text = extract_text_from_pdf(pdf_file)
        if not text:
            print("⚠️ No text found in this file, skipping.")
            continue

        records = extract_json_from_text(text)
        if isinstance(records, dict):  # Sometimes model returns a single dict instead of list
            records = [records]

        for r in records:
            r["filename"] = os.path.basename(pdf_file)

        all_records.extend(records)
        print(f"✅ Extracted {len(records)} records from {os.path.basename(pdf_file)}")

    except Exception as e:
        print(f" Error processing {pdf_file}: {e}")

# ======================================================
# SAVE ALL RECORDS TO CSV
# ======================================================
if all_records:
    df = pd.DataFrame(all_records)
    # Ensure all columns exist
    for col in ["full_name", "first_name", "last_name", "title", "telephone", "mobile", "filename"]:
        if col not in df.columns:
            df[col] = ""
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"\n Successfully saved {len(df)} rows to {output_csv}")
else:
    print("\n No data extracted from any file.")

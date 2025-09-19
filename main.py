import os
import sqlite3
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # loads .env automatically

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_MOCK = not OPENAI_API_KEY  # fallback if key is missing

if not USE_MOCK:
    client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(
    title="Financial Document Analyzer",
    version="0.1.0",
    description="Analyze financial documents with AI for insights, risks, and recommendations."
)

# SQLite setup
DB_PATH = "queries.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    input_text TEXT,
    result TEXT
)
""")
conn.commit()

class QueryRequest(BaseModel):
    query: str
    text: str

@app.get("/")
def root():
    return {"message": "Welcome to the Financial Document Analyzer API!"}

# --------------------------
# Helper function for AI call
# --------------------------
def get_ai_response(prompt: str):
    if USE_MOCK:
        return f"[MOCK RESPONSE] Analysis for: {prompt[:100]}..."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are an AI financial analyst."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception:
        return f"[MOCK RESPONSE] Analysis temporarily unavailable for: {prompt[:100]}..."

# --------------------------
# /query - Plain Text Analysis
# --------------------------
@app.post("/query")
def query_ai(request: QueryRequest):
    prompt = f"Query: {request.query}\n\nText: {request.text}"
    result = get_ai_response(prompt)

    cursor.execute(
        "INSERT INTO queries (query, input_text, result) VALUES (?, ?, ?)",
        (request.query, request.text[:1000], result)
    )
    conn.commit()
    return {"query": request.query, "result": result}

# --------------------------
# /analyze - PDF File Analysis
# --------------------------
@app.post("/analyze")
def analyze_file(file: UploadFile = File(...), query: str = Form(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_reader = PdfReader(file.file)
    text = "".join(page.extract_text() or "" for page in pdf_reader.pages)

    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found in PDF.")

    prompt = f"Query: {query}\n\nDocument: {text[:4000]}"
    result = get_ai_response(prompt)

    cursor.execute(
        "INSERT INTO queries (query, input_text, result) VALUES (?, ?, ?)",
        (query, text[:1000], result)
    )
    conn.commit()
    return {"query": query, "result": result}

# Financial Document Analyzer

Analyze financial documents using AI. This system processes corporate reports, financial statements, and investment documents to provide insights, risk assessments, and investment recommendations.

## Author
**Yogeswaran S**  
Email: yogeswaran00794@gmail.com

## Project Overview

- Upload financial documents (PDF format) or plain text.
- AI-powered financial analysis using OpenAI / CrewAI.
- Risk assessment and investment recommendations.
- Stores analysis results in a SQLite database.
- Mock responses available if OpenAI key is missing or quota exceeded.

---

## Bugs Fixed

| Issue |                         -                             | Fix |
1.Missing or invalid OpenAI API key - Added mock responses fallback so the app never crashes (`USE_MOCK`) 

2.PDF extraction errors - Checked for empty PDFs and non-existent files using PyPDF2 and PyPDFLoader 

3.Non-PDF file uploads - Added HTTPException validation in `/analyze` endpoint 

4.Large prompts causing AI errors - Trimmed input text to 4000 characters for AI calls; stored 1000 characters preview in DB

5.Unhandled exceptions in AI calls - Wrapped OpenAI API calls with try/except and fallback mock responses 

6.Async / task management - CrewAI tasks set up in `task.py` for modular AI processing

7.Database integrity  - SQLite tables auto-created and input safely committed;no crashes if database exists


📂 Project Structure
financial-document-analyzer-debug/
│   .env
│   agents.py
│   main.py
│   task.py
│   tools.py
│   analysis.db
│   queries.db
│   README.md
│   requirements.txt
│
├───data
│       sample.pdf
│
└───outputs


agents.py – AI agents for financial analysis, verification, investment advice, and risk assessment.
main.py – FastAPI app with /query and /analyze endpoints.
task.py – CrewAI tasks for AI processing.
tools.py – Custom tools for PDF extraction, investment, risk, and search.
analysis.db / queries.db – SQLite databases storing analysis results.
data/sample.pdf – Example financial document for testing.


🛠️ Setup Instructions
## Clone the repo:
git clone https://github.com/yogeswaran-94/financial-document-analyzer-debug.git
cd financial-document-analyzer-debug

## Create a .env file:
OPENAI_API_KEY=your_openai_api_key
USE_MOCK=false

If OPENAI_API_KEY is missing, the system will automatically use mock responses.

## Install dependencies:

pip install -r requirements.txt
Run the FastAPI server:
python main.py


Test API: Open http://127.0.0.1:8000/docs
 to access Swagger UI.

📡API Documentation
1. Analyze Plain Text
Endpoint: POST /query
Request Body (JSON):
{
  "query": "Summarize financial performance",
  "text": "Q2 2025 Tesla financial report text..."
}

Response:
{
  "query": "Summarize financial performance",
  "result": "[MOCK/AI RESPONSE] Analysis for: Summarize financial performance..."
}

2. Analyze PDF File
Endpoint: POST /analyze
Form-data Parameters:
1)file – PDF file
2)query – Text query

#Curl Example:
curl -X POST "http://127.0.0.1:8000/analyze" \
-F "file=@data/sample.pdf" \
-F "query=Summarize financial performance"

#Response:
{
  "query": "Summarize financial performance",
  "result": "[MOCK/AI RESPONSE] PDF analysis preview..."
}

#Error Handling:
Non-PDF file → 400 Only PDF files are supported.
Empty PDF → 400 No extractable text found in PDF.
Missing OpenAI key → Mock response returned automatically.

📄Sample Document
data/sample.pdf – placeholder financial report. Replace with any real financial document for testing.

⚡Key Features
1.AI agents for financial analysis, verification, investment advice, and risk assessment.
2.Plain text and PDF document support.
3.SQLite database stores queries, previews, and AI results.
4.Mock fallback ensures smooth testing without OpenAI key.
5.Safe PDF extraction and error handling.
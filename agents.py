import os
from dotenv import load_dotenv
from crewai import Agent
from tools import FinancialDocumentTool, InvestmentTool, RiskTool, search_tool

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OpenAI API key loaded:", OPENAI_API_KEY)

# LLM placeholder (CrewAI will auto-pick from env like OPENAI_API_KEY)
llm = None  

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Extract insights from financial documents and highlight key metrics.",
    verbose=True,
    memory=True,
    backstory="An expert in reading financial statements and extracting market insights.",
    tools=[FinancialDocumentTool()],   # ✅ create instance
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether a document is financial in nature.",
    verbose=True,
    memory=True,
    backstory="Trained to detect whether uploaded files are valid financial documents.",
    tools=[search_tool],   # ✅ this one is already a proper BaseTool
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide investment strategies and recommendations.",
    verbose=True,
    backstory="Provides suggestions on potential investment opportunities.",
    tools=[InvestmentTool()],   # ✅ instance
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessor",
    goal="Evaluate risk factors in financial documents.",
    verbose=True,
    backstory="Specialized in analyzing risk and volatility.",
    tools=[RiskTool()],   # ✅ instance
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

# task.py
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import FinancialDocumentTool, InvestmentTool, RiskTool

# Financial document analysis task
analyze_financial_document = Task(
    description="Analyze a financial document, extract key insights, assess risks, and provide recommendations.",
    expected_output="Comprehensive financial insights with investment advice and risk evaluation.",
    tools=[
        FinancialDocumentTool(),  # ✅ Pass instance, not a non-existent method
        InvestmentTool(),
        RiskTool(),
    ],
    agent=financial_analyst
)

# Document verification task
verify_document = Task(
    description="Verify whether an uploaded document is a valid financial document.",
    expected_output="Boolean result with a short explanation.",
    tools=[FinancialDocumentTool()],
    agent=verifier
)

# Investment advice task
give_investment_advice = Task(
    description="Provide potential investment opportunities based on financial document insights.",
    expected_output="List of investment strategies and recommendations.",
    tools=[InvestmentTool()],
    agent=investment_advisor
)

# Risk assessment task
assess_risk = Task(
    description="Evaluate risks, volatility, and uncertainties in the financial document.",
    expected_output="Risk factors and overall risk profile.",
    tools=[RiskTool()],
    agent=risk_assessor
)

from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader


# Search tool (already works as BaseTool)
search_tool = SerperDevTool()

# Custom PDF reader tool
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads and extracts text from financial PDF documents."

    def _run(self, path: str = "data/sample.pdf") -> str:
        try:
            loader = PyPDFLoader(path)
            docs = loader.load()

            full_report = ""
            for data in docs:
                content = data.page_content
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                full_report += content + "\n"

            return full_report.strip()
        except Exception as e:
            return f"Error reading PDF: {e}"

# Investment analysis tool
class InvestmentTool(BaseTool):
    name: str = "Investment Analysis Tool"
    description: str = "Analyzes financial document data and suggests investment insights."

    def _run(self, financial_document_data: str) -> str:
        if not financial_document_data:
            return "No data provided for investment analysis."
        return "Investment analysis completed (sample output)."

# Risk assessment tool
class RiskTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = "Performs risk assessment on financial document data."

    def _run(self, financial_document_data: str) -> str:
        if not financial_document_data:
            return "No data provided for risk assessment."
        return "Risk assessment completed (sample output)."

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sales_service import calculate_sales_summary

app = FastAPI(title="电商经营分析 Agent")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ecommerce-analysis-agent",
    }


class AnalysisRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.post("/analysis/query")
def submit_analysis(request: AnalysisRequest):
    return {
        "status": "received",
        "question": request.question,
    }


@app.get("/reports/sales-summary")
def sales_summary():
    return calculate_sales_summary()
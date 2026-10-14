from fastapi import FastAPI
from pydantic import BaseModel, Field
from decimal import Decimal
from sample_orders import ORDERS

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
    paid_order_count = 0
    total_sales = Decimal("0.00")

    for order in ORDERS:
        if order["status"] == "PAID":
            paid_order_count += 1
            total_sales += Decimal(order["amount"])

    return {
        "paid_order_count": paid_order_count,
        #str(total_sales) 将金额转成字符串返回，例如 "299.80"
        "total_sales": str(total_sales),
        "currency": "CNY",
        "data_source": "sample",
    }
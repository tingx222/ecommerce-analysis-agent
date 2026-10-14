from fastapi import FastAPI

app = FastAPI(title="电商经营分析 Agent")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ecommerce-analysis-agent",
    }
from fastapi import FastAPI

app = FastAPI(title="Fusion Backend API")

@app.get("/")
def root():
    return {
        "status": "Backend running",
        "framework": "FastAPI"
    }

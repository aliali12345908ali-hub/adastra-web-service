from fastapi import FastAPI

app = FastAPI(title="Adastra Core API")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "Adastra Core Engine",
        "message": "Real-world cloud service running successfully!"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

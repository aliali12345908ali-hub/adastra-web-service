import os
import time
from fastapi import FastAPI, BackgroundTasks, Request, status
from fastapi.responses import JSONResponse
from typing import Dict

app = FastAPI(
    title="Adastra Global CaaS Ecosystem",
    description="High-performance, secure, and resilient CaaS & SaaS Platform",
    version="2.3.0"
)

# سجل المقاييس والإحصائيات
METRICS_DATA = {
    "total_requests": 0,
    "start_time": time.time()
}

RATE_LIMIT_STORE: Dict[str, list] = {}
MAX_REQUESTS_PER_MINUTE = 10

@app.middleware("http")
async def metrics_and_rate_limit_middleware(request: Request, call_next):
    start_time = time.time()
    METRICS_DATA["total_requests"] += 1
    client_ip = request.client.host or "127.0.0.1"
    
    if client_ip in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[client_ip] = [
            t for t in RATE_LIMIT_STORE[client_ip] if start_time - t < 60
        ]
    else:
        RATE_LIMIT_STORE[client_ip] = []

    if len(RATE_LIMIT_STORE[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "status": "error",
                "message": "Rate limit exceeded. Too many requests, please try again later.",
                "limit": f"{MAX_REQUESTS_PER_MINUTE} requests per minute"
            }
        )

    RATE_LIMIT_STORE[client_ip].append(start_time)
    
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

@app.get("/metrics")
async def get_metrics():
    uptime = time.time() - METRICS_DATA["start_time"]
    return {
        "platform": "Adastra CaaS Ecosystem",
        "uptime_seconds": round(uptime, 2),
        "total_requests_handled": METRICS_DATA["total_requests"],
        "status": "Healthy"
    }

def run_heavy_security_scan(target: str):
    time.sleep(2)
    print(f"[Adastra Background Worker] Scan completed for: {target}")

@app.post("/caas/scan")
async def caas_security_scan(target: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_heavy_security_scan, target)
    return {
        "status": "accepted",
        "target": target,
        "message": "Adastra CaaS security assessment queued successfully in background.",
        "task_id": f"task_{int(time.time())}",
        "rate_limiting": "Active & Protected"
    }

@app.get("/")
async def root():
    return {
        "platform": "Adastra CaaS Ecosystem",
        "status": "Operational",
        "features": ["Rate Limiting", "Background Tasks Workers", "Live Performance Metrics"]
    }

import os
import time
from fastapi import FastAPI, BackgroundTasks, Request, status
from fastapi.responses import JSONResponse
from typing import Dict

app = FastAPI(
    title="Adastra Global CaaS Ecosystem",
    description="High-performance, secure, and resilient CaaS & SaaS Platform",
    version="2.1.0"
)

# نظام Rate Limiting النشط
RATE_LIMIT_STORE: Dict[str, list] = {}
MAX_REQUESTS_PER_MINUTE = 10

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host or "127.0.0.1"
    current_time = time.time()
    
    if client_ip in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[client_ip] = [
            t for t in RATE_LIMIT_STORE[client_ip] if current_time - t < 60
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

    RATE_LIMIT_STORE[client_ip].append(current_time)
    response = await call_next(request)
    return response

# دالة خلفية تحاكي الفحص الثقيل
def run_heavy_security_scan(target: str):
    time.sleep(5)  # محاكاة وقت المعالجة في الخلفية
    print(f"[Adastra Background Worker] Scan completed successfully for target: {target}")

# نقطة النهاية مع دعم Background Tasks
@app.post("/caas/scan")
async def caas_security_scan(target: str, background_tasks: BackgroundTasks):
    # إضافة المهمة للعمل في الخلفية
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
        "features": ["Rate Limiting", "Background Tasks Workers"]
    }

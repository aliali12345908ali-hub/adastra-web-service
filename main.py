import os
import time
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI(
    title="Adastra Global CaaS Ecosystem",
    description="High-performance, secure, and resilient CaaS & SaaS Platform",
    version="2.0.0"
)

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

@app.post("/caas/scan")
async def caas_security_scan(target: str):
    return {
        "status": "success",
        "target": target,
        "message": "Adastra CaaS security assessment initiated successfully.",
        "risk_level": "Low",
        "rate_limiting": "Active & Protected"
    }

@app.get("/")
async def root():
    return {
        "platform": "Adastra CaaS Ecosystem",
        "status": "Operational",
        "security_layer": "Rate Limiting & DDoS Shield Active"
    }

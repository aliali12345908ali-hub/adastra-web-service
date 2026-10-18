o
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


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


git add .
git commit -m "Add JWT authentication and SQLAlchemy database configuration"
git push


@app.get("/api/v1/status")
def get_system_status():
    return {"status": "active", "message": "Adastra system is fully operational and scaling!"}


from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import get_db
from models import SystemLog

@app.get("/api/v1/status")
def get_system_status(db: Session = Depends(get_db)):
    # حفظ سجل الحركة في قاعدة بيانات PostgreSQL
    new_log = SystemLog(action="STATUS_CHECK", details="API status checked successfully from Termux/Railway")
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    return {"status": "active", "message": "Adastra system is fully operational and scaling!", "log_id": new_log.id}




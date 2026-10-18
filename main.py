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



from pydantic import BaseModel
from models import User

class UserCreate(BaseModel):
    email: str
    password: str

@app.post("/api/v1/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # التحقق من عدم وجود المستخدم مسبقاً
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return {"status": "error", "message": "User already exists!"}
    
    # إنشاء المستخدم الجديد (ملاحظة: في الإنتاج الحقيقي يتم تشفير كلمة المرور)
    new_user = User(email=user.email, hashed_password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"status": "success", "message": "User registered successfully", "user_id": new_user.id}


from fastapi import HTTPException, status
from pydantic import BaseModel
from models import User, SystemLog

# نموذج تسجيل الدخول
class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/api/v1/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.hashed_password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return {
        "status": "success", 
        "message": "Login successful!", 
        "user_email": db_user.email, 
        "is_vip": db_user.is_vip
    }

# نموذج لوحة تحكم المشرفين لعرض الإحصائيات وسجلات النظام
@app.get("/api/v1/admin/dashboard")
def admin_dashboard(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_logs = db.query(SystemLog).count()
    recent_logs = db.query(SystemLog).order_by(SystemLog.id.desc()).limit(5).all()
    
    return {
        "platform": "Adastra Global SaaS",
        "total_registered_users": total_users,
        "total_system_logs": total_logs,
        "recent_activity": [{"id": log.id, "action": log.action, "details": log.details} for log in recent_logs]
    }

from fastapi import HTTPException, status
from pydantic import BaseModel
from models import User, SystemLog

# نموذج تسجيل الدخول
class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/api/v1/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or db_user.hashed_password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return {
        "status": "success", 
        "message": "Login successful!", 
        "user_email": db_user.email, 
        "is_vip": db_user.is_vip
    }

# نموذج لوحة تحكم المشرفين لعرض الإحصائيات وسجلات النظام
@app.get("/api/v1/admin/dashboard")
def admin_dashboard(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_logs = db.query(SystemLog).count()
    recent_logs = db.query(SystemLog).order_by(SystemLog.id.desc()).limit(5).all()
    
    return {
        "platform": "Adastra Global SaaS",
        "total_registered_users": total_users,
        "total_system_logs": total_logs,
        "recent_activity": [{"id": log.id, "action": log.action, "details": log.details} for log in recent_logs]
    }


import stripe
from fastapi import HTTPException

# مفتاح السكريت الخاص ببوابة Stripe (يتم وضعه لاحقاً كمتغير بيئي آمن في Railway)
stripe.api_key = "sk_test_your_stripe_secret_key"

@app.post("/api/v1/create-checkout-session")
def create_checkout_session(user_email: str):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Adastra VIP Global Subscription',
                    },
                    'unit_amount': 2900, # 29.00 دولار شهرياً
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="https://adastra.im/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://adastra.im/cancel",
            customer_email=user_email,
        )
        return {"status": "success", "checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

import stripe
from fastapi import HTTPException

# تفعيل مفتاح الدفع
stripe.api_key = "sk_test_your_stripe_secret_key"

@app.post("/api/v1/create-checkout-session")
def create_checkout_session(user_email: str):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Adastra VIP Global SaaS Subscription',
                    },
                    'unit_amount': 2900, # 29.00 دولار
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="https://adastra.im/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://adastra.im/cancel",
            customer_email=user_email,
        )
        return {"status": "success", "checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


cd ~/adastra_web_service
nano main.py





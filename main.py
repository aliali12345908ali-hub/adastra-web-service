from fastapi import FastAPI, Request, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
import stripe

app = FastAPI(title="Adastra CaaS", version="1.0.0")

stripe.api_key = "sk_test_..."
endpoint_secret = "whsec_..."

USER_DATABASE = {
    "adastra_vip_key_123": {"name": "Ali", "tier": "pro", "active": True},
    "adastra_pro_key_456": {"name": "Client X", "tier": "enterprise", "active": True}
}

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@app.get("/")
async def root():
    return {
        "platform": "Adastra CaaS",
        "status": "online",
        "message": "أهلاً بك في منصة الحاويات السحابية المدفوعة 🚀",
        "docs": "/docs"
    }

async def verify_api_key_advanced(api_key: str = Depends(api_key_header)):
    if not api_key or api_key not in USER_DATABASE:
        raise HTTPException(
            status_code=403, 
            detail="🔑 مفتاح الـ API غير صالح أو غير موجود"
        )
    user_info = USER_DATABASE[api_key]
    if not user_info["active"]:
        raise HTTPException(
            status_code=403, 
            detail="❌ هذا الحساب متوقف، يرجى تجديد الاشتراك عبر Stripe"
        )
    return user_info

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        print(f"🎉 تم تفعيل اشتراك جديد بنجاح للعميل: {customer_email}")

    return {"status": "success"}

@app.post("/caas/scan/pro")
async def protected_scan(target: str, user_info: dict = Depends(verify_api_key_advanced)):
    return {
        "status": "authorized",
        "tier": user_info["tier"],
        "target": target,
        "message": "جاري الفحص المتقدم للعميل المدفوع بنجاح 🚀"
    }

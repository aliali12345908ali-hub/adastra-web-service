from fastapi import FastAPI, Request, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
import stripe

app = FastAPI()

stripe.api_key = "sk_test_..."
endpoint_secret = "whsec_..."

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

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        print(f"💰 تم استلام المبلغ بنجاح: {payment_intent['amount']}")

    return {"status": "success"}

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
VALID_API_KEYS = {"adastra_vip_key_123", "adastra_pro_key_456"}

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=403, 
            detail="🔑 مفتاح الـ API غير صالح أو انتهى اشتراكك"
        )
    return api_key

@app.post("/caas/scan/pro")
async def protected_scan(target: str, key: str = Depends(verify_api_key)):
    return {
        "status": "authorized",
        "target": target,
        "message": "جاري الفحص المتقدم للعميل المدفوع 🚀"
    }

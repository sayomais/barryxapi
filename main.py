from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from gates import stripe_charge, stripe_auth, shopify

app = FastAPI()
AUTH_KEY = "VDX-SHA2X-NZ0RS-O7HAM"

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path != "/":
        auth_header = request.headers.get("Authorization")
        if auth_header != f"Bearer {AUTH_KEY}":
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)

@app.get("/")
def root():
    return {"status": "listening..."}

@app.post("/stripe_charge")
def stripe_charge_api():
    try:
        result = stripe_charge.run()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "declined", "message": str(e)}

@app.post("/stripe_auth")
def stripe_auth_api():
    try:
        result = stripe_auth.run()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "declined", "message": str(e)}

@app.post("/shopify")
async def shopify_api():
    try:
        await shopify.main()
        return {"status": "success", "message": "Shopify check completed"}
    except Exception as e:
        return {"status": "declined", "message": str(e)}

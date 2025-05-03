
from fastapi import FastAPI, Request
from gates.stripe_auth import stripe_auth
from gates.stripe_charge import stripe_charge
from gates.shopify import shopify_gate

app = FastAPI(title="BarryX API")

@app.post("/stripe-auth")
async def stripe_auth_gate(request: Request):
    data = await request.json()
    return await stripe_auth(data)

@app.post("/stripe-charge")
async def stripe_charge_gate(request: Request):
    data = await request.json()
    return await stripe_charge(data)

@app.post("/shopify")
async def shopify_gate_api(request: Request):
    data = await request.json()
    return await shopify_gate(data)

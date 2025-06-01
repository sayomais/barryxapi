from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from gates import stripe_auth, stripe_charge, shopify, str_auth, clover

app = FastAPI()
AUTH_KEY = "BRY-HEIQ7-KPWYR-DRU67"

@app.get("/")
def root():
    return {"status": "listening..."}

# GET endpoint for browser or testing
@app.get("/{gate_name}")
def run_gate_via_get(
    gate_name: str,
    key: str = Query(...),
    card: str = Query(...),
    proxy: str = Query(None)
):
    if key != AUTH_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    try:
        module = get_gate_module(gate_name)
        result = module.run(card, proxy) if hasattr(module, "run") else module.main(card, proxy)
        return result  # Direct result for bot compatibility
    except Exception as e:
        return {"status": "error", "message": str(e)}

# POST endpoint for programmatic use
@app.post("/{gate_name}")
async def run_gate_via_post(gate_name: str, request: Request):
    body = await request.json()
    key = body.get("key")
    card = body.get("card")
    proxy = body.get("proxy")

    if key != AUTH_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    try:
        module = get_gate_module(gate_name)
        result = module.run(card, proxy) if hasattr(module, "run") else await module.main(card, proxy)
        return result  # Direct result for bot compatibility
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Gate resolver
def get_gate_module(name: str):
    name = name.lower()
    if name == "stripe_auth":
        return stripe_auth
    elif name == "stripe_charge":
        return stripe_charge
    elif name == "shopify":
        return shopify
    elif name == "str_auth":
        return str_auth
    elif name == "clover":
        return clover
    else:
        raise Exception("Unknown gate")


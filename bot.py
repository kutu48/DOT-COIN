import requests
import json
import random
import time

# Function to get authorization token from the file
def get_auth_token():
    try:
        with open('authorization.txt', 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading authorization token: {e}")
        return None

# Function to get the payload data from the file
def get_payload_data():
    try:
        with open('data.txt', 'r') as file:
            return file.read().strip().split('\n')
    except Exception as e:
        print(f"Error reading payload data: {e}")
        return []

# Define common headers
def get_common_headers(auth_token):
    return {
        "origin": "https://dot.dapplab.xyz",
        "referer": "https://dot.dapplab.xyz/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "apikey": auth_token  # Add apikey to common headers
    }

def get_token(init_data, auth_token):
    url = "https://api.dotcoin.bot/functions/v1/getToken"
    headers = {
        **get_common_headers(auth_token),
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {auth_token}",  # Using Bearer token from authorization.txt
        "content-length": "335",
        "content-type": "application/json"
    }
    payload = {
        "initData": init_data
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_user_info(token):
    url = "https://api.dotcoin.bot/rest/v1/rpc/get_user_info"
    headers = {
        **get_common_headers(auth_token),
        "authorization": f"Bearer {token}",  # Using token from getToken response
        "x-client-info": "postgrest-js/0.0.0-automated"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_assets(token):
    url = "https://api.dotcoin.bot/rest/v1/rpc/get_assets"
    headers = {
        **get_common_headers(auth_token),
        "authorization": f"Bearer {token}",  # Using token from getToken response
        "x-client-info": "postgrest-js/0.0.0-automated"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")
        return None

def klik_url(token, coins):
    url = "https://api.dotcoin.bot/rest/v1/rpc/save_coins"
    headers = {
        **get_common_headers(auth_token),
        "authorization": f"Bearer {token}",  # Using token from getToken response
        "x-client-info": "postgrest-js/0.0.0-automated"
    }
    payload = {
        "coins": coins
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"success | nilai 'coins': {coins}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")

def gatcha_url(token, balance):
    url = "https://api.dotcoin.bot/rest/v1/rpc/try_your_luck"
    headers = {
        **get_common_headers(auth_token),
        "authorization": f"Bearer {token}",  # Using token from getToken response
        "x-client-info": "postgrest-js/0.0.0-automated"
    }
    coins = int(balance * 0.10)  # 10% of balance
    payload = {
        "coins": coins
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"success | nilai payload gatcha_url: {json.dumps(payload)}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")

# Main process wrapped in a while loop
while True:
    auth_token = get_auth_token()
    if not auth_token:
        print("Authorization token is missing. Exiting...")
        break

    payload_data = get_payload_data()
    if not payload_data:
        print("Payload data is missing. Exiting...")
        break

    for init_data in payload_data:
        token = get_token(init_data, auth_token)
        if token:
            user_info = get_user_info(token)
            if user_info:
                first_name = user_info.get("first_name")
                balance = user_info.get("balance")
                wallet = user_info.get("wallet")
                level = user_info.get("level")
                dtc_level = user_info.get("dtc_level")  # Added dtc_level
                group_title = user_info.get("group").get("title") if user_info.get("group") else "N/A"  # Handle None for group

                limit_attempts = user_info.get("limit_attempts")

                print(f"First Name: {first_name}")
                print(f"Balance: {balance}")
                print(f"Wallet: {wallet}")
                print(f"Level: {level}")
                print(f"Level: {dtc_level}")  # Print dtc_level
                print(f"Group Title: {group_title}")

                assets = get_assets(token)
                if assets:
                    for asset in assets:
                        print(f"Asset Name: {asset.get('name')}")
                        print(f"Asset Amount: {asset.get('amount')}")

                # Call gatcha_url function
                gatcha_url(token, balance)

                for _ in range(limit_attempts):
                    coins = random.randint(1000, 1500)  # Updated range of coins
                    klik_url(token, coins)
                    delay = random.randint(25, 60)
                    print(f"Waiting for {delay} seconds before next attempt...")
                    time.sleep(delay)

    # Wait 600 seconds (10 minutes) before repeating the process
    print("Waiting 10 minutes before the next iteration...")
    time.sleep(600)


import random
import string
import requests
import time

checked_names = set()

def generate_name():
    return ''.join(random.choices(string.ascii_lowercase, k=4))

def check_username(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"❌ {username} is taken.")
        elif response.status_code == 404:
            print(f"✅ {username} is available!")
            with open("available.txt", "a") as f:
                f.write(username + "\n")
        elif response.status_code == 429:
            print("⚠️ Rate limit hit, sleeping for 10 seconds...")
            time.sleep(10)
            return check_username(username)
        else:
            print(f"⚠️ {username}: Unexpected status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ {username}: Request failed: {e}")

print("🔍 starting random 4-letter name checks Press Ctrl+C to stop.")
try:
    while True:
        name = generate_name()
        if name in checked_names:
            continue
        checked_names.add(name)
        check_username(name)
        time.sleep(1.5)
except KeyboardInterrupt:
    print("\n⏹️ Stopped by user.")

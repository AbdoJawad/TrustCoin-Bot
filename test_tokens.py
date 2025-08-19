import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== Testing Bot Tokens ===")
print(f"BOT_TOKEN_ENG: {'✅ Found' if os.getenv('BOT_TOKEN_ENG') else '❌ Missing'}")
print(f"BOT_TOKEN_ARA: {'✅ Found' if os.getenv('BOT_TOKEN_ARA') else '❌ Missing'}")
print(f"BOT_TOKEN_FR: {'✅ Found' if os.getenv('BOT_TOKEN_FR') else '❌ Missing'}")

# Print actual tokens (first 10 characters only for security)
eng_token = os.getenv('BOT_TOKEN_ENG')
ara_token = os.getenv('BOT_TOKEN_ARA')
fr_token = os.getenv('BOT_TOKEN_FR')

if eng_token:
    print(f"English Token: {eng_token[:10]}...")
if ara_token:
    print(f"Arabic Token: {ara_token[:10]}...")
if fr_token:
    print(f"French Token: {fr_token[:10]}...")

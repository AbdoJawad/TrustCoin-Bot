#!/usr/bin/env python3
"""
Simple test script to check bot connectivity
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()

async def test_bot(token, name):
    """Test if a bot token is working"""
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"✅ {name} Bot: @{me.username} - {me.first_name}")
        return True
    except Exception as e:
        print(f"❌ {name} Bot Error: {e}")
        return False

async def main():
    print("=== Testing Bot Connections ===\n")
    
    tokens = {
        "English": os.getenv('BOT_TOKEN_ENG'),
        "Arabic": os.getenv('BOT_TOKEN_ARA'), 
        "French": os.getenv('BOT_TOKEN_FR')
    }
    
    for name, token in tokens.items():
        if token:
            await test_bot(token, name)
        else:
            print(f"❌ {name} Bot: Token not found")
        print()

if __name__ == "__main__":
    asyncio.run(main())

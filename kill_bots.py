import os
import sys
import requests
import time

# Bot tokens from .env file
ENGLISH_TOKEN = "7512597854:AAGSLTOQ-CkcKF7g6MI4SUzzDBIdHu89daE"
ARABIC_TOKEN = "8290216301:AAGjiN-MilQ3bjBrsJIwh3Fjh-QfBbaAc1c"
FRENCH_TOKEN = "8375639193:AAGkYT3TBzl195IK4d-GnP7Wpa38QLSdHtc"

def delete_webhook(token, bot_name):
    """Delete webhook for a bot"""
    try:
        url = f"https://api.telegram.org/bot{token}/deleteWebhook"
        response = requests.post(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {bot_name} webhook deleted successfully")
        else:
            print(f"❌ Failed to delete {bot_name} webhook: {response.text}")
    except Exception as e:
        print(f"❌ Error deleting {bot_name} webhook: {e}")

def get_updates_and_clear(token, bot_name):
    """Get updates with high offset to clear pending updates"""
    try:
        # Get current updates
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['result']:
                # Get the highest update_id
                highest_id = max(update['update_id'] for update in data['result'])
                # Clear all pending updates by setting offset to highest_id + 1
                clear_url = f"https://api.telegram.org/bot{token}/getUpdates?offset={highest_id + 1}"
                clear_response = requests.get(clear_url, timeout=10)
                if clear_response.status_code == 200:
                    print(f"✅ {bot_name} pending updates cleared")
                else:
                    print(f"❌ Failed to clear {bot_name} updates")
            else:
                print(f"✅ {bot_name} has no pending updates")
        else:
            print(f"❌ Failed to get {bot_name} updates: {response.text}")
    except Exception as e:
        print(f"❌ Error clearing {bot_name} updates: {e}")

def kill_python_processes():
    """Kill all Python processes that might be running bots"""
    try:
        import psutil
        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any('bot.py' in str(cmd) for cmd in cmdline):
                        print(f"🔪 Killing process {proc.info['pid']}: {' '.join(cmdline)}")
                        proc.kill()
                        killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if killed_count == 0:
            print("✅ No bot processes found running")
        else:
            print(f"✅ Killed {killed_count} bot processes")
            time.sleep(2)  # Wait for processes to fully terminate
            
    except ImportError:
        print("❌ psutil not installed. Install with: pip install psutil")
        return False
    except Exception as e:
        print(f"❌ Error killing processes: {e}")
        return False
    return True

def main():
    print("🤖 TrustCoin Bot Conflict Resolver")
    print("=" * 40)
    
    # Step 1: Kill running processes
    print("\n1. Killing running bot processes...")
    kill_python_processes()
    
    # Step 2: Delete webhooks
    print("\n2. Deleting webhooks...")
    bots = [
        (ENGLISH_TOKEN, "English Bot"),
        (ARABIC_TOKEN, "Arabic Bot"),
        (FRENCH_TOKEN, "French Bot")
    ]
    
    for token, name in bots:
        if token:  # Token is configured
            delete_webhook(token, name)
        else:
            print(f"⚠️  {name} token not configured")
    
    # Step 3: Clear pending updates
    print("\n3. Clearing pending updates...")
    for token, name in bots:
        if token:  # Token is configured
            get_updates_and_clear(token, name)
        else:
            print(f"⚠️  {name} token not configured")
    
    print("\n✅ Conflict resolution completed!")
    print("\n💡 If conflict persists:")
    print("   1. Check if bots are running on other servers/VPS")
    print("   2. Regenerate bot tokens from @BotFather")
    print("   3. Wait 5-10 minutes before restarting")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
TrustCoin Bot Setup Script
سكريبت الإعداد والتثبيت لبوتات TrustCoin
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Print setup header."""
    print("=" * 60)
    print("🚀 TrustCoin Bot Setup Script")
    print("=" * 60)
    print("مرحباً بك في سكريبت إعداد بوتات TrustCoin")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ يتطلب Python 3.8 أو أحدث")
        print(f"📍 الإصدار المتاح: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} متوافق")
    return True

def check_required_tools():
    """Check if required tools are available."""
    tools = {
        'pip': 'pip --version',
        'git': 'git --version'
    }
    
    missing_tools = []
    for tool, command in tools.items():
        try:
            subprocess.run(command.split(), capture_output=True, check=True)
            print(f"✅ {tool} متوفر")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {tool} غير متوفر")
            missing_tools.append(tool)
    
    return len(missing_tools) == 0

def install_requirements():
    """Install Python requirements."""
    print("\n📦 تثبيت المتطلبات...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ تم تثبيت جميع المتطلبات بنجاح")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل في تثبيت المتطلبات: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        print("✅ ملف .env موجود")
        return True
    
    if env_example.exists():
        print("📋 إنشاء ملف .env من المثال...")
        shutil.copy(env_example, env_file)
        print("✅ تم إنشاء ملف .env")
        print("⚠️ يرجى تحديث ملف .env بـ tokens البوتات الخاصة بك")
        return True
    else:
        print("❌ ملف .env.example غير موجود")
        return False

def validate_bot_tokens():
    """Validate bot tokens in .env file."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        tokens = {
            'BOT_TOKEN_ENG': os.getenv('BOT_TOKEN_ENG'),
            'BOT_TOKEN_ARA': os.getenv('BOT_TOKEN_ARA'),
            'BOT_TOKEN_FR': os.getenv('BOT_TOKEN_FR')
        }
        
        valid_tokens = 0
        for name, token in tokens.items():
            if token and token != f'your_{name.lower()}_here':
                print(f"✅ {name} configured")
                valid_tokens += 1
            else:
                print(f"⚠️ {name} غير مكوّن")
        
        if valid_tokens == 0:
            print("⚠️ لم يتم تكوين أي token. يرجى تحديث ملف .env")
            return False
        elif valid_tokens < 3:
            print(f"⚠️ تم تكوين {valid_tokens}/3 من البوتات فقط")
        else:
            print("✅ جميع البوتات مكوّنة")
        
        return True
        
    except ImportError:
        print("❌ لا يمكن تحميل python-dotenv")
        return False

def create_logs_directory():
    """Create logs directory."""
    logs_dir = Path('logs')
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("✅ تم إنشاء مجلد logs")
    else:
        print("✅ مجلد logs موجود")

def show_next_steps():
    """Show next steps to user."""
    print("\n" + "=" * 60)
    print("🎉 تم الإعداد بنجاح!")
    print("=" * 60)
    print("\n📋 الخطوات التالية:")
    print("1. تحديث ملف .env بـ tokens البوتات:")
    print("   - احصل على tokens من @BotFather في Telegram")
    print("   - ضع tokens في ملف .env")
    print()
    print("2. تشغيل البوتات:")
    print("   Windows: start_bots.bat")
    print("   Linux/Mac: ./start_bots.sh")
    print("   Docker: docker-compose up -d")
    print()
    print("3. في حالة مشاكل التضارب:")
    print("   python kill_bots.py")
    print()
    print("📖 لمزيد من المعلومات، راجع README.md")
    print("=" * 60)

def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check required tools
    print("\n🔍 فحص الأدوات المطلوبة...")
    if not check_required_tools():
        print("❌ يرجى تثبيت الأدوات المفقودة أولاً")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    print("\n🔧 إعداد متغيرات البيئة...")
    if not create_env_file():
        sys.exit(1)
    
    # Validate tokens
    print("\n🔑 فحص tokens البوتات...")
    validate_bot_tokens()
    
    # Create logs directory
    print("\n📁 إعداد مجلدات المشروع...")
    create_logs_directory()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ تم إلغاء الإعداد بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)

import os
import logging
import asyncio
import threading
from dotenv import load_dotenv
from flask import Flask, request
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.error import InvalidToken

# Load environment variables
load_dotenv()

# Get bot token from environment
BOT_TOKEN_ARA = os.getenv('BOT_TOKEN_ARA')

# Validate token
if not BOT_TOKEN_ARA:
    raise ValueError("❌ BOT_TOKEN_ARA not found in environment variables. Please check your .env file.")

# Main menu keyboard
def build_main_menu() -> InlineKeyboardMarkup:
    """Build the main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("📋 نظرة عامة والبدء", callback_data="overview")],
        [InlineKeyboardButton("⛏️ التعدين والنقاط", callback_data="points")],
        [InlineKeyboardButton("🎯 المهام والمكافآت", callback_data="missions")],
        [InlineKeyboardButton("👥 الإحالة والمجتمع", callback_data="referral")],
        [InlineKeyboardButton("🗺️ خارطة الطريق", callback_data="roadmap")],
        [InlineKeyboardButton("📱 تحميل التطبيق", callback_data="download")],
        [InlineKeyboardButton("🔒 الأمان ومكافحة الغش", callback_data="security")],
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data="faq")],
        [InlineKeyboardButton("🌐 الروابط الاجتماعية", callback_data="social")],
        [InlineKeyboardButton("🌍 مجموعات اللغات", callback_data="language_groups")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command by showing the main menu."""
    welcome_text = (
        "🚀 **أهلاً بك في TrustCoin (TBN)!** 🚀\n\n"
        "💎 **التعدين المحمول الثوري على Binance Smart Chain**\n\n"
        "🎁 **مكافأة الترحيب:** احصل على 1,000 نقطة فوراً عند التسجيل!\n"
        "⛏️ **التعدين:** اكسب حتى 1,000 نقطة كل 24 ساعة\n"
        "💰 **التحويل:** 1,000 نقطة = 1 رمز TBN\n"
        "🌟 **العرض الإجمالي:** 20 مليار رمز TBN\n\n"
        "📱 حمّل التطبيق الآن وابدأ رحلتك في عالم العملات المشفرة!\n\n"
        "👇 اختر قسماً لتعرف المزيد:"
    )
    
    # Send logo with welcome message
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'logo.png')
    
    try:
        with open(logo_path, 'rb') as logo_file:
            await update.message.reply_photo(
                photo=InputFile(logo_file, filename='logo.png'),
                caption=welcome_text,
                reply_markup=build_main_menu(),
                parse_mode="Markdown"
            )
    except FileNotFoundError:
        # Fallback to text message if logo not found
        await update.message.reply_text(
            welcome_text,
            reply_markup=build_main_menu(),
            parse_mode="Markdown"
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all callback queries from inline keyboards."""
    query = update.callback_query
    await query.answer()
    data = query.data

    def send_or_edit_message(text, reply_markup=None, parse_mode="Markdown"):
        """Helper function to send new message if photo exists, otherwise edit."""
        if query.message.photo:
            return query.message.reply_text(text=text, reply_markup=reply_markup, parse_mode=parse_mode)
        else:
            return query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=parse_mode)

    if data == "overview":
        text = (
            "📋 **نظرة عامة والبدء**\n\n"
            "🌟 TrustCoin (TBN) هو نظام مكافآت ثوري قائم على البلوك تشين على شبكة Binance الذكية.\n\n"
            "🚀 **كيفية البدء:**\n"
            "1️⃣ **حمّل تطبيق TrustCoin** لنظام iOS أو Android وأنشئ حسابك\n"
            "🎁 احصل على **مكافأة ترحيب 1,000 نقطة** فوراً!\n\n"
            "2️⃣ **ابدأ جلسات التعدين لمدة 24 ساعة** التي تستمر حتى عند إغلاق التطبيق\n"
            "💾 يتم حفظ التقدم تلقائياً كل ساعة\n\n"
            "3️⃣ **أكمل المهام وأدر عجلة الحظ** للحصول على نقاط إضافية\n"
            "🎯 طرق متعددة لكسب المكافآت يومياً\n\n"
            "4️⃣ **حوّل نقاطك إلى رموز TBN حقيقية** عبر العقد الذكي المؤتمت\n"
            "💰 **1,000 نقطة = 1 رمز TBN**\n\n"
            "📱 التطبيق متعدد المنصات (React Native) مع ميزات الدردشة والفريق\n"
            "🔒 TrustCoin يركز على الشفافية والتطوير المجتمعي والقيمة طويلة المدى"
        )
        await send_or_edit_message(text, build_main_menu())

    elif data == "back":
        await send_or_edit_message("القائمة الرئيسية:", build_main_menu())

    else:
        await send_or_edit_message("خيار غير صحيح. العودة للقائمة الرئيسية.", build_main_menu())

def main() -> None:
    """Initialize the bot with Flask webhook support for production or polling for development."""
    try:
        # Initialize the Telegram bot application
        app = ApplicationBuilder().token(BOT_TOKEN_ARA).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        
        # Check if we're running in webhook mode (production) or polling mode (development)
        webhook_url = os.getenv('WEBHOOK_URL')
        port = int(os.getenv('PORT', 5000))
        
        if webhook_url:
            # Production mode with webhook
            print(f"🚀 Starting Arabic bot in webhook mode on port {port}")
            
            # Initialize Flask app
            flask_app = Flask(__name__)
            
            @flask_app.route('/webhook', methods=['POST'])
            def webhook():
                """Handle incoming webhook requests from Telegram."""
                try:
                    update = Update.de_json(request.get_json(force=True), app.bot)
                    # Run the update handler in a separate thread to avoid blocking
                    def run_update():
                        asyncio.run(app.process_update(update))
                    threading.Thread(target=run_update).start()
                    return 'OK'
                except Exception as e:
                    logging.error(f"Error processing webhook: {e}")
                    return 'Error', 500
            
            @flask_app.route('/health', methods=['GET'])
            def health():
                """Health check endpoint."""
                return {'status': 'healthy', 'bot': 'arabic'}
            
            @flask_app.route('/', methods=['GET'])
            def home():
                """Home endpoint."""
                return {'message': 'TrustCoin Arabic Bot is running!', 'status': 'active'}
            
            # Set webhook
            asyncio.run(app.bot.set_webhook(url=f"{webhook_url}/webhook"))
            
            # Start Flask server
            flask_app.run(host='0.0.0.0', port=port, debug=False)
        else:
            # Development mode with polling
            print("🔄 Starting Arabic bot in polling mode (development)")
            app.run_polling(drop_pending_updates=True)
            
    except InvalidToken:
        print("❌ Invalid bot token. Please check your BOT_TOKEN_ARA in .env file.")
    except Exception as e:
        print(f"❌ Error starting Arabic bot: {e}")
        logging.error(f"Bot startup error: {e}")

if __name__ == "__main__":
    main()

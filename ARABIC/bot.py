import os
from dotenv import load_dotenv
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
    """Initialize the bot and start polling."""
    app = ApplicationBuilder().token(BOT_TOKEN_ARA).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()

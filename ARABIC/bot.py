import os
import logging
import asyncio
import threading
import signal
import sys
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

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global bot application instance
bot_app = None

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("🛑 Received shutdown signal. Stopping Arabic bot gracefully...")
    if bot_app:
        try:
            # Create health status file for Docker
            with open('/tmp/bot_healthy', 'w') as f:
                f.write('stopping')
        except:
            pass
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Get bot token from environment variables
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
            "🌟 **ما هو TrustCoin (TBN)?**\n"
            "TrustCoin هو مشروع تعدين محمول ثوري يعمل على شبكة Binance Smart Chain. "
            "يمكن للمستخدمين كسب العملة المشفرة من خلال التطبيق المحمول دون الحاجة إلى أجهزة تعدين باهظة الثمن.\n\n"
            
            "🎁 **كيفية البدء:**\n"
            "1️⃣ حمّل التطبيق من الرابط أدناه\n"
            "2️⃣ أنشئ حساباً جديداً\n"
            "3️⃣ احصل على 1,000 نقطة ترحيب فوراً\n"
            "4️⃣ ابدأ التعدين كل 24 ساعة\n"
            "5️⃣ ادع الأصدقاء واكسب المزيد!\n\n"
            
            "💎 **المزايا الأساسية:**\n"
            "• تعدين مجاني بدون استهلاك الطاقة\n"
            "• مكافآت يومية مضمونة\n"
            "• نظام إحالة ربحي\n"
            "• أمان عالي مع تشفير متقدم\n"
            "• فريق دعم متاح 24/7\n\n"
            
            "📱 **متطلبات النظام:**\n"
            "• Android 6.0+ أو iOS 12.0+\n"
            "• اتصال إنترنت مستقر\n"
            "• رقم هاتف صالح للتحقق"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "points":
        text = (
            "⛏️ **التعدين والنقاط**\n\n"
            "💰 **نظام النقاط:**\n"
            "• احصل على حتى 1,000 نقطة كل 24 ساعة\n"
            "• مكافأة تسجيل: 1,000 نقطة فوراً\n"
            "• التحويل: 1,000 نقطة = 1 رمز TBN\n\n"
            
            "⏰ **جدولة التعدين:**\n"
            "• دورة تعدين كل 24 ساعة\n"
            "• إشعارات تلقائية عند انتهاء الدورة\n"
            "• لا حاجة لبقاء التطبيق مفتوحاً\n\n"
            
            "🚀 **زيادة الأرباح:**\n"
            "• تسجيل دخول يومي: +10% مكافأة\n"
            "• مهام إضافية: حتى +50% مكافأة\n"
            "• عضوية VIP: مضاعفة المكافآت\n\n"
            
            "📊 **إحصائيات شخصية:**\n"
            "• تتبع رصيدك اليومي\n"
            "• تاريخ التعدين الكامل\n"
            "• توقعات الأرباح المستقبلية\n"
            "• مقارنة مع المستخدمين الآخرين"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "missions":
        text = (
            "🎯 **المهام والمكافآت**\n\n"
            "📋 **المهام اليومية:**\n"
            "• تسجيل دخول يومي: +100 نقطة\n"
            "• مشاهدة إعلان: +50 نقطة\n"
            "• دعوة صديق: +500 نقطة\n"
            "• متابعة حساباتنا: +200 نقطة\n\n"
            
            "🏆 **المهام الأسبوعية:**\n"
            "• التعدين 7 أيام متتالية: +1,000 نقطة\n"
            "• دعوة 5 أصدقاء: +2,500 نقطة\n"
            "• إكمال جميع المهام اليومية: +1,500 نقطة\n\n"
            
            "💎 **المهام الشهرية:**\n"
            "• التعدين 30 يوماً: +10,000 نقطة\n"
            "• بناء فريق من 50 مستخدم: +25,000 نقطة\n"
            "• الوصول للمستوى الذهبي: +50,000 نقطة\n\n"
            
            "🌟 **مهام خاصة:**\n"
            "• مشاركة التطبيق على وسائل التواصل\n"
            "• كتابة مراجعة في متجر التطبيقات\n"
            "• المشاركة في المسابقات الشهرية"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "referral":
        text = (
            "👥 **الإحالة والمجتمع**\n\n"
            "💰 **نظام الإحالة ثنائي المستوى:**\n"
            "🥇 **المستوى الأول:** 20% من أرباح المدعوين المباشرين\n"
            "🥈 **المستوى الثاني:** 5% من أرباح المدعوين غير المباشرين\n\n"
            
            "🎁 **مكافآت الدعوة:**\n"
            "• لكل مدعو جديد: +500 نقطة فوراً\n"
            "• عند وصول المدعو للمستوى 5: +1,000 نقطة\n"
            "• مكافآت شهرية حسب عدد الفريق\n\n"
            
            "🏆 **رتب القيادة:**\n"
            "🌟 **البرونزي** (10+ مدعوين): +10% مكافأة إضافية\n"
            "🥈 **الفضي** (50+ مدعوين): +25% مكافأة إضافية\n"
            "🥇 **الذهبي** (100+ مدعوين): +50% مكافأة إضافية\n"
            "💎 **الماسي** (500+ مدعوين): +100% مكافأة إضافية\n\n"
            
            "🌐 **انضم للمجتمع:**\n"
            "• مجموعات نقاش باللغات المختلفة\n"
            "• نصائح وحيل من الخبراء\n"
            "• إعلانات المسابقات والجوائز\n"
            "• دعم فني مباشر"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "roadmap":
        text = (
            "🗺️ **خارطة الطريق**\n\n"
            "📅 **المرحلة 1 - القاعدة (تمت):**\n"
            "✅ إطلاق التطبيق المحمول\n"
            "✅ نظام التعدين الأساسي\n"
            "✅ نظام الإحالة\n"
            "✅ واجهة متعددة اللغات\n\n"
            
            "📅 **المرحلة 2 - النمو (جارية):**\n"
            "🔄 تطوير نظام المكافآت\n"
            "🔄 إضافة مهام متقدمة\n"
            "🔄 تحسين الأمان\n"
            "🔄 توسيع المجتمع\n\n"
            
            "📅 **المرحلة 3 - التوسع (قريباً):**\n"
            "⏳ إطلاق الرمز على البلوك تشين\n"
            "⏳ نظام التداول الداخلي\n"
            "⏳ شراكات مع منصات التداول\n"
            "⏳ محفظة مدمجة\n\n"
            
            "📅 **المرحلة 4 - المستقبل:**\n"
            "🔮 نظام DeFi متكامل\n"
            "🔮 NFT وألعاب البلوك تشين\n"
            "🔮 منصة تعليمية\n"
            "🔮 توسع عالمي"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "download":
        text = (
            "📱 **تحميل التطبيق**\n\n"
            "🚀 **احصل على TrustCoin الآن!**\n\n"
            "📲 **روابط التحميل:**\n"
            "🤖 **Android:** [Google Play Store](https://play.google.com/store/apps/details?id=com.trustcoin.tbn)\n"
            "🍎 **iOS:** [App Store](https://apps.apple.com/app/trustcoin-tbn/id123456789)\n"
            "🌐 **موقع ويب:** [trustcoin.tbn](https://trustcoin.tbn)\n\n"
            
            "💾 **معلومات التطبيق:**\n"
            "• حجم التحميل: ~25 MB\n"
            "• آخر تحديث: نوفمبر 2024\n"
            "• التقييم: ⭐⭐⭐⭐⭐ (4.8/5)\n"
            "• التحميلات: +100,000\n\n"
            
            "🔒 **الأمان:**\n"
            "• التطبيق آمن 100% ومدقق\n"
            "• لا يطلب صلاحيات غير ضرورية\n"
            "• تشفير عالي المستوى\n"
            "• دعم فني 24/7\n\n"
            
            "🎁 **عرض خاص:** استخدم كود الدعوة عند التسجيل للحصول على مكافأة إضافية!"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "security":
        text = (
            "🔒 **الأمان ومكافحة الغش**\n\n"
            "🛡️ **تدابير الأمان:**\n"
            "• تشفير end-to-end لجميع البيانات\n"
            "• تحقق ثنائي العامل (2FA)\n"
            "• مراقبة النشاط المشبوه 24/7\n"
            "• نسخ احتياطية آمنة\n\n"
            
            "🚫 **مكافحة الغش:**\n"
            "• نظام ذكي لكشف الحسابات الوهمية\n"
            "• منع استخدام البوتات والأتمتة\n"
            "• تحديد الموقع الجغرافي\n"
            "• تحليل سلوك المستخدم\n\n"
            
            "⚖️ **السياسات:**\n"
            "• حساب واحد فقط لكل شخص\n"
            "• منع استخدام الشبكات الوهمية (VPN)\n"
            "• تعليق الحسابات المشبوهة\n"
            "• مراجعة دورية للأنشطة\n\n"
            
            "🚨 **الإبلاغ عن الانتهاكات:**\n"
            "إذا لاحظت أي نشاط مشبوه، تواصل معنا فوراً\n"
            "Email: security@trustcoin.tbn"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "faq":
        text = (
            "❓ **الأسئلة الشائعة**\n\n"
            "🔍 **س: هل التطبيق مجاني تماماً؟**\n"
            "ج: نعم! التحميل والاستخدام مجاني 100%\n\n"
            
            "🔍 **س: كم يمكنني أن أكسب يومياً؟**\n"
            "ج: حتى 1,000 نقطة يومياً + مكافآت الإحالة\n\n"
            
            "🔍 **س: متى سيتم إطلاق الرمز؟**\n"
            "ج: مخطط لإطلاقه في النصف الأول من 2025\n\n"
            
            "🔍 **س: هل يمكنني استخدام أكثر من حساب؟**\n"
            "ج: لا، حساب واحد فقط مسموح لكل شخص\n\n"
            
            "🔍 **س: كيف أحول النقاط إلى عملة؟**\n"
            "ج: سيكون متاحاً عند إطلاق الرمز الرسمي\n\n"
            
            "🔍 **س: هل البيانات آمنة؟**\n"
            "ج: نعم، نستخدم أعلى معايير الأمان والتشفير\n\n"
            
            "🔍 **س: كيف أتواصل مع الدعم؟**\n"
            "ج: عبر التطبيق أو البريد الإلكتروني أو التليجرام"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "social":
        text = (
            "🌐 **الروابط الاجتماعية**\n\n"
            "تابعنا على جميع المنصات للحصول على آخر الأخبار والتحديثات!\n\n"
            
            "📱 **وسائل التواصل الاجتماعي:**\n"
            "• [📘 Facebook](https://facebook.com/trustcointbn)\n"
            "• [🐦 Twitter/X](https://twitter.com/trustcointbn)\n"
            "• [📸 Instagram](https://instagram.com/trustcointbn)\n"
            "• [💼 LinkedIn](https://linkedin.com/company/trustcointbn)\n"
            "• [🎵 TikTok](https://tiktok.com/@trustcointbn)\n\n"
            
            "💬 **مجتمعات المحادثة:**\n"
            "• [📱 Telegram الرئيسي](https://t.me/trustcointbn)\n"
            "• [💬 Discord](https://discord.gg/trustcointbn)\n"
            "• [🗨️ Reddit](https://reddit.com/r/trustcointbn)\n\n"
            
            "🎥 **المحتوى التعليمي:**\n"
            "• [📺 YouTube](https://youtube.com/@trustcointbn)\n"
            "• [📖 Medium](https://medium.com/@trustcointbn)\n\n"
            
            "🌍 **الموقع الرسمي:**\n"
            "• [🌐 TrustCoin.tbn](https://trustcoin.tbn)"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "language_groups":
        text = (
            "🌍 **مجموعات اللغات**\n\n"
            "انضم إلى مجموعة لغتك المفضلة للحصول على دعم أفضل!\n\n"
            
            "🇸🇦 **العربية:**\n"
            "• [مجموعة عربية رئيسية](https://t.me/trustcointbn_arabic)\n"
            "• [دعم فني عربي](https://t.me/trustcointbn_arabic_support)\n\n"
            
            "🇺🇸 **English:**\n"
            "• [English Main Group](https://t.me/trustcointbn_english)\n"
            "• [English Support](https://t.me/trustcointbn_english_support)\n\n"
            
            "🇫🇷 **Français:**\n"
            "• [Groupe Principal Français](https://t.me/trustcointbn_french)\n"
            "• [Support Français](https://t.me/trustcointbn_french_support)\n\n"
            
            "🌐 **مجموعات أخرى:**\n"
            "• [🇪🇸 Español](https://t.me/trustcointbn_spanish)\n"
            "• [🇩🇪 Deutsch](https://t.me/trustcointbn_german)\n"
            "• [🇷🇺 Русский](https://t.me/trustcointbn_russian)\n"
            "• [🇨🇳 中文](https://t.me/trustcointbn_chinese)"
        )
        
        back_keyboard = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]]
        await send_or_edit_message(text, InlineKeyboardMarkup(back_keyboard))
        
    elif data == "main_menu":
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
        await query.edit_message_text(text=welcome_text, reply_markup=build_main_menu(), parse_mode="Markdown")
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

# Flask app for webhook
flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates."""
    try:
        update = Update.de_json(request.get_json(force=True), bot_app)
        asyncio.run(bot_app.process_update(update))
        return 'OK'
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return 'Error', 500

@flask_app.route('/health')
def health():
    """Health check endpoint."""
    return 'OK'

@flask_app.route('/')
def home():
    """Home endpoint."""
    return 'TrustCoin Bot Arabic is running!'

# Flask app for webhook support
flask_app = Flask(__name__)

@flask_app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle incoming webhook requests."""
    try:
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        await bot_app.update_queue.put(update)
        return 'OK'
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'ERROR', 500

@flask_app.route('/health')
def health_check():
    """Health check endpoint."""
    return {'status': 'healthy', 'bot': 'arabic'}, 200

@flask_app.route('/')
def home():
    """Home endpoint."""
    return {'message': 'TrustCoin Arabic Bot is running!', 'status': 'active'}, 200

def run_flask():
    """Run Flask app in a separate thread."""
    port = int(os.getenv('PORT', 8444))  # Different port for Arabic bot
    # Always run Flask server for render.com compatibility
    flask_app.run(host='0.0.0.0', port=port, debug=False)

def main() -> None:
    """Initialize the bot."""
    global bot_app
    
    try:
        # Create health check file for Docker
        with open('/tmp/bot_healthy', 'w') as f:
            f.write('starting')
            
        bot_app = ApplicationBuilder().token(BOT_TOKEN_ARA).build()
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(CallbackQueryHandler(button_handler))
        
        webhook_url = os.getenv('WEBHOOK_URL')
        
        # Always start Flask server for render.com compatibility
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logging.info("Flask server started on port " + str(os.getenv('PORT', 8444)))
        
        if webhook_url:
            # Production mode with webhook
            logging.info("Starting Arabic bot in webhook mode...")
            
            # Set webhook
            asyncio.run(bot_app.bot.set_webhook(url=webhook_url))
            
            # Update health status
            with open('/tmp/bot_healthy', 'w') as f:
                f.write('running')
            
            # Keep the main thread alive
            import time
            while True:
                time.sleep(1)
        else:
            # Development mode with polling
            logging.info("Starting Arabic bot in polling mode...")
            
            # Update health status
            with open('/tmp/bot_healthy', 'w') as f:
                f.write('running')
                
            bot_app.run_polling(drop_pending_updates=True)
            
    except InvalidToken:
        logging.error("❌ Invalid bot token. Please check your BOT_TOKEN_ARA.")
        # Remove health file on error
        try:
            os.remove('/tmp/bot_healthy')
        except:
            pass
        raise
    except Exception as e:
        logging.error(f"❌ Error starting Arabic bot: {e}")
        # Remove health file on error
        try:
            os.remove('/tmp/bot_healthy')
        except:
            pass
        raise

if __name__ == "__main__":
    main()

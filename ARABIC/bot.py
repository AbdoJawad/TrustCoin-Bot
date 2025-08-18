import os
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variables
BOT_TOKEN_ARA = os.getenv('BOT_TOKEN_ARA')

# Validate that the bot token is loaded
if not BOT_TOKEN_ARA:
    raise ValueError("❌ BOT_TOKEN_ARA not found in environment variables. Please check your .env file.")

# Main menu keyboard
def build_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📋 نظرة عامة والبدء", callback_data="overview")],
        [InlineKeyboardButton("⛏️ التعدين والنقاط", callback_data="points")],
        [InlineKeyboardButton("🎯 المهام والمكافآت", callback_data="missions")],
        [InlineKeyboardButton("👥 الإحالة والمجتمع", callback_data="referral")],
        [InlineKeyboardButton("📈 التوكينوميكس وخارطة الطريق", callback_data="roadmap")],
        [InlineKeyboardButton("📱 تحميل التطبيق", callback_data="download")],
        [InlineKeyboardButton("🔒 الأمان ومكافحة الغش", callback_data="security")],
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data="faq")],
        [InlineKeyboardButton("🌐 الروابط الاجتماعية", callback_data="social")],
        [InlineKeyboardButton("🌍 مجموعات اللغات", callback_data="language_groups")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Language group menu function removed - now using inline buttons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command by showing the main menu."""
    welcome_text = (
        "🚀 **مرحباً بك في TrustCoin (TBN)!** 🚀\n\n"
        "💎 **التعدين الثوري عبر الهاتف المحمول على شبكة Binance الذكية**\n\n"
        "🎁 **مكافأة الترحيب:** احصل على 1,000 نقطة فوراً عند التسجيل!\n"
        "⛏️ **التعدين:** اكسب حتى 1,000 نقطة كل 24 ساعة\n"
        "💰 **التحويل:** 1,000 نقطة = 1 رمز TBN\n"
        "🌟 **إجمالي المعروض:** 20 مليار رمز TBN\n\n"
        "📱 حمّل التطبيق الآن وابدأ رحلتك في عالم العملات المشفرة!\n\n"
        "👇 اختر قسماً لتعرف المزيد:"
    )
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
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "points":
        text = (
            "⛏️ **نظام التعدين والنقاط**\n\n"
            "🕐 **جلسات التعدين لمدة 24 ساعة:**\n"
            "• اكسب حتى **1,000 نقطة لكل دورة**\n"
            "• يتم حفظ التقدم تلقائياً كل ساعة\n"
            "• تستأنف الجلسات بعد إعادة تشغيل التطبيق\n\n"
            "📊 **معادلة المكافآت:**\n"
            "`(مدة الجلسة ÷ 86,400) × 1,000 نقطة`\n\n"
            "📺 **مكافآت الإعلانات:**\n"
            "• شاهد الإعلانات لفتح ضربات إضافية\n"
            "• احصل على مضاعفات للمكافآت الإضافية\n\n"
            "💎 **تحويل النقاط إلى TBN:**\n"
            "• **المعدل:** 1 TBN لكل 1,000 نقطة\n"
            "• **الحد الأدنى:** استرداد 1,000 نقطة\n"
            "• **الحد اليومي:** 100,000 نقطة كحد أقصى\n"
            "• **مثال:** 10,000 نقطة = 10 رموز TBN\n\n"
            "🔗 **ميزات العقد الذكي:**\n"
            "• التحويل المؤتمت على BSC\n"
            "• رسوم الغاز مغطاة من المشروع في البداية\n"
            "• **معدلات الحرق:** 1% للتحويلات، 0.5% للتحويلات، 2% للميزات المميزة"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "missions":
        text = (
            "🎯 **نظام المهام والمكافآت**\n\n"
            "🏆 **مهام الكؤوس (1-500 نقطة):**\n"
            "• إكمال أول جلسة تعدين\n"
            "• أيام الجمع المتتالية\n"
            "• إحالة مستخدمين جدد\n"
            "• سلاسل تسجيل الدخول اليومي\n\n"
            "💎 **مهام الأحجار الكريمة (1,000-5,000 نقطة):**\n"
            "• سلاسل تعدين لمدة 30 يوم\n"
            "• إنجازات الكفاءة العليا\n"
            "• إكمال جميع مهام الكؤوس\n\n"
            "🎁 **مهام الصناديق (2,000-10,000 نقطة):**\n"
            "• سلاسل متتالية لمدة 90 يوم\n"
            "• بناء فريق من 20+ إحالة\n"
            "• جمع 100,000+ نقطة إجمالية\n\n"
            "🪙 **مهام العملات (100-1,000 نقطة):**\n"
            "• المهام اليومية مثل مشاركة التطبيق\n"
            "• تحديث ملفك الشخصي\n"
            "• الانضمام لأحداث المجتمع\n\n"
            "🎰 **نظام عجلة الحظ:**\n"
            "• اربح **1-1,500 نقطة**\n"
            "• **3 ضربات لكل دورة**\n"
            "• **فترة انتظار 6 ساعات** بين الدورات\n"
            "• **الاحتماليات:** 50% (1-100)، 30% (101-200)، 15% (201-300)، 5% (301-500)\n"
            "• شاهد الإعلانات للحصول على دورات إضافية ومضاعفات!"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "referral":
        text = (
            "👥 **برنامج الإحالة والمجتمع**\n\n"
            "🔗 **نظام الإحالة ذو المستويين:**\n"
            "• **أكواد عامة** للجميع\n"
            "• **أكواد حصرية** لأفضل المُحيلين\n\n"
            "🎁 **مزايا المستخدم الجديد:**\n"
            "• **مكافأة ترحيب 1,000 نقطة** عند التسجيل\n"
            "• **500 نقطة إضافية** عند استخدام كود الدعوة\n"
            "• وصول فوري لجميع الميزات\n\n"
            "💰 **مكافآت المُحيل:**\n"
            "• **1,000 نقطة لكل إحالة ناجحة**\n"
            "• حصة من مكافآت تعدين المُحال\n"
            "• شارات التقدير والمكافآت\n"
            "• ترتيبات لوحة المتصدرين\n\n"
            "👨‍👩‍👧‍👦 **ميزات المجتمع:**\n"
            "• تشكيل فريق مع معدنين آخرين\n"
            "• الدردشة في المحادثات الجماعية\n"
            "• مشاركة استراتيجيات التعدين\n"
            "• التنافس في لوحات المتصدرين العالمية\n"
            "• المشاركة في أحداث المجتمع"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "roadmap":
        text = (
            "📈 **التوكينوميكس وخارطة الطريق**\n\n"
            "💰 **توزيع المعروض (20 مليار TBN إجمالي):**\n"
            "• 🏆 **12 مليار** - مجموعة مكافآت التعدين (60%)\n"
            "• 💧 **3 مليار** - احتياطي السيولة (15%)\n"
            "• 🛠️ **3 مليار** - صندوق التطوير (15%)\n"
            "• 👥 **2 مليار** - تخصيص الفريق (10%)\n\n"
            "🔥 **آليات الانكماش:**\n"
            "• **1%** حرق على جميع تحويلات الرموز\n"
            "• **0.5%** حرق على تحويلات النقاط\n"
            "• **2%** حرق على الميزات المميزة\n"
            "• **حرق متغير** لإنجازات المعالم\n\n"
            "🏛️ **الحوكمة والتخزين:**\n"
            "• خزن رموز TBN للحصول على مكافآت إضافية\n"
            "• نظام تصويت مرجح بالرموز\n"
            "• عائد سنوي متغير حسب مدة التخزين\n"
            "• فتح ميزات التطبيق المميزة\n\n"
            "🗺️ **خارطة طريق التطوير:**\n"
            "**2025:** الأساس والتحسين\n"
            "✅ أنظمة التعدين والمهام وعجلة الحظ\n"
            "✅ تكامل الإحالة والإعلانات\n\n"
            "**2025-2026:** الاختبار والإطلاق\n"
            "🔄 تدقيقات الأمان والتحسين\n"
            "🚀 إطلاق الشبكة الرئيسية على BSC\n"
            "🆔 أنظمة التحقق KYC/AI\n\n"
            "**2026-2027:** التوسع والابتكار\n"
            "📈 إدراج في البورصات الكبرى\n"
            "🏦 تكامل بروتوكول DeFi\n"
            "🌐 تطوير بلوك تشين Trust\n"
            "🏛️ تنفيذ حوكمة DAO\n"
            "🎨 إطلاق سوق NFT\n"
            "🌍 شراكات الميتافيرس\n"
            "🌉 تطوير جسر متعدد السلاسل\n"
            "💳 تكامل نظام الدفع العالمي"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "download":
        # Download app section with direct links
        download_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 تحميل لنظام iOS", url="https://apps.apple.com/app/trustcoin")],
            [InlineKeyboardButton("🤖 تحميل لنظام Android", url="https://play.google.com/store/apps/details?id=com.trustcoin")],
            [InlineKeyboardButton("🌐 زيارة الموقع الرسمي", url="https://www.trust-coin.site")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="back")],
        ])
        text = (
            "📱 **تحميل تطبيق TrustCoin**\n\n"
            "🚀 **ابدأ مع TrustCoin اليوم!**\n\n"
            "📲 **متاح على كلا المنصتين:**\n"
            "• متجر تطبيقات iOS\n"
            "• متجر Google Play\n\n"
            "🎁 **ما ستحصل عليه:**\n"
            "• **مكافأة ترحيب 1,000 نقطة**\n"
            "• **قدرة تعدين 24/7**\n"
            "• **توافق متعدد المنصات**\n"
            "• **ميزات الدردشة والفريق الفورية**\n"
            "• **تكامل آمن مع البلوك تشين**\n\n"
            "💡 **متطلبات النظام:**\n"
            "• iOS 12.0+ أو Android 6.0+\n"
            "• اتصال بالإنترنت\n"
            "• مساحة تخزين 50 ميجابايت\n\n"
            "🔗 انقر على الأزرار أدناه للتحميل:"
        )
        await query.edit_message_text(
            text, reply_markup=download_keyboard, parse_mode="Markdown"
        )

    elif data == "security":
        text = (
            "🔒 **الأمان ونظام مكافحة الغش**\n\n"
            "🛡️ **الأمان متعدد الطبقات:**\n"
            "• **بصمة الجهاز** لمنع إساءة استخدام الحسابات المتعددة\n"
            "• **التحقق من الجلسة في الوقت الفعلي** مع المصادقة الزمنية\n"
            "• **تحليل الأنماط بالذكاء الاصطناعي** لاكتشاف الأتمتة والغش\n"
            "• **فحوصات الاتساق الجغرافي** للسلوك الأصيل للمستخدم\n\n"
            "⚖️ **إنفاذ اللعب النظيف:**\n"
            "• سياسة **حساب واحد لكل شخص**\n"
            "• **متطلب الجهاز الحقيقي** - لا محاكيات\n"
            "• **لا أدوات أتمتة** مسموحة\n"
            "• **حظر دائم** للمخالفات\n\n"
            "🔐 **أمان البلوك تشين:**\n"
            "• **تدقيق العقود الذكية** من قبل شركات الأمان الرائدة\n"
            "• **آليات انكماشية** للقيمة الحقيقية\n"
            "• آليات **الحماية من الحيتان**\n"
            "• **عمليات شفافة على السلسلة**\n\n"
            "🚨 **منع الاحتيال:**\n"
            "• **تشفير متقدم** لجميع البيانات\n"
            "• خوارزميات **تحليل السلوك**\n"
            "• نظام **الإبلاغ المجتمعي**\n"
            "• بنية **مراقبة 24/7**\n\n"
            "✅ **سلامتك هي أولويتنا!**"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "faq":
        text = (
            "❓ **الأسئلة الشائعة**\n\n"
            "**س1: كيف أبدأ التعدين؟**\n"
            "ج: حمل التطبيق، سجل، واضغط على زر التعدين. الجلسات تعمل لمدة 24 ساعة تلقائياً.\n\n"
            "**س2: متى يمكنني سحب رموز TBN؟**\n"
            "ج: تحويل الرموز سيكون متاحاً بعد إطلاق الشبكة الرئيسية على BSC (2025-2026).\n\n"
            "**س3: هل TrustCoin مجاني الاستخدام؟**\n"
            "ج: نعم! التطبيق مجاني تماماً. تحتاج فقط اتصال بالإنترنت.\n\n"
            "**س4: كم حساباً يمكنني امتلاكه؟**\n"
            "ج: حساب واحد فقط لكل شخص. الحسابات المتعددة ستؤدي إلى حظر دائم.\n\n"
            "**س5: ما هو الحد الأدنى للسحب؟**\n"
            "ج: الحد الأدنى للتحويل هو 1,000 نقطة = 1 رمز TBN.\n\n"
            "**س6: هل يمكنني استخدام المحاكيات أو البوتات؟**\n"
            "ج: لا! الأجهزة الحقيقية فقط مسموحة. أدوات الأتمتة محظورة بشدة.\n\n"
            "**س7: كيف تعمل الإحالات؟**\n"
            "ج: شارك رمز الإحالة الخاص بك. تحصل على 1,000 نقطة لكل إحالة ناجحة.\n\n"
            "**س8: هل بياناتي آمنة؟**\n"
            "ج: نعم! نستخدم تشفيراً متقدماً وإجراءات أمنية لحماية بياناتك.\n\n"
            "**س9: متى سيتم إدراج TBN في البورصات؟**\n"
            "ج: إدراج البورصات الكبرى مخطط له في 2026-2027 بعد إطلاق الشبكة الرئيسية.\n\n"
            "**س10: كيف يمكنني التواصل مع الدعم؟**\n"
            "ج: انضم لمجموعة التليجرام أو زر موقعنا للحصول على الدعم."
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "social":
        # Social links as buttons
        social_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Website", url="https://www.trust-coin.site")],
            [InlineKeyboardButton("📘 Facebook ➡️", url="https://www.facebook.com/people/TrustCoin/61579302546502/")],
            [InlineKeyboardButton("✈️ Telegram Group ➡️", url="https://t.me/+djORe9HGRi45ZDdk")],
            [InlineKeyboardButton("🎵 TikTok ➡️", url="https://www.tiktok.com/@trusrcoin?_t=ZN-8yu1iUm1Wis&_r=1")],
            [InlineKeyboardButton("🐦 X/Twitter ➡️", url="https://x.com/TBNTrustCoin")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="back")],
        ])
        await query.edit_message_text(
            "اختر رابطاً لفتحه:", reply_markup=social_keyboard
        )

    elif data == "language_groups":
        # Language groups as direct buttons with flags
        language_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇺🇸 المجموعة الإنجليزية", url="https://t.me/tructcoin_bot")],
            [InlineKeyboardButton("🇸🇦 المجموعة العربية", url="https://t.me/trustcoin_arabic_bot")],
            [InlineKeyboardButton("🇫🇷 المجموعة الفرنسية", url="https://t.me/trustcoin_fr_bot")],
            [InlineKeyboardButton("⬅️ العودة للقائمة الرئيسية", callback_data="back")],
        ])
        await query.edit_message_text(
            "اختر مجموعة اللغة المفضلة لديك:",
            reply_markup=language_keyboard
        )

    # Language group handlers removed - now using direct URL buttons

    elif data == "back":
        await query.edit_message_text(
            "القائمة الرئيسية:", reply_markup=build_main_menu()
        )

    else:
        await query.edit_message_text(
            "خيار غير صحيح. العودة للقائمة الرئيسية.", reply_markup=build_main_menu()
        )

def main() -> None:
    """Initialize the bot and start polling."""
    app = ApplicationBuilder().token(BOT_TOKEN_ARA).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()

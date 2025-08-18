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

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variables
BOT_TOKEN_ENG = os.getenv('BOT_TOKEN_ENG')

# Validate that the bot token is loaded
if not BOT_TOKEN_ENG:
    raise ValueError("❌ BOT_TOKEN_ENG not found in environment variables. Please check your .env file.")

# Main menu keyboard
def build_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📋 Overview & Getting Started", callback_data="overview")],
        [InlineKeyboardButton("⛏️ Mining & Points", callback_data="points")],
        [InlineKeyboardButton("🎯 Missions & Rewards", callback_data="missions")],
        [InlineKeyboardButton("👥 Referral & Community", callback_data="referral")],
        [InlineKeyboardButton("📈 Tokenomics & Roadmap", callback_data="roadmap")],
        [InlineKeyboardButton("📱 Download App", callback_data="download")],
        [InlineKeyboardButton("🔒 Security & Anti-Cheat", callback_data="security")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🌐 Social Links", callback_data="social")],
        [InlineKeyboardButton("🌍 Language Groups", callback_data="language_groups")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Language group menu function removed - now using inline buttons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command by showing the main menu."""
    welcome_text = (
        "🚀 **Welcome to TrustCoin (TBN)!** 🚀\n\n"
        "💎 **Revolutionary Mobile Mining on Binance Smart Chain**\n\n"
        "🎁 **Welcome Bonus:** Get 1,000 points instantly upon registration!\n"
        "⛏️ **Mining:** Earn up to 1,000 points every 24 hours\n"
        "💰 **Conversion:** 1,000 points = 1 TBN token\n"
        "🌟 **Total Supply:** 20 Billion TBN tokens\n\n"
        "📱 Download the app now and start your cryptocurrency journey!\n\n"
        "👇 Choose a section to learn more:"
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

    if data == "overview":
        text = (
            "📋 **Overview & Getting Started**\n\n"
            "🌟 TrustCoin (TBN) is a revolutionary blockchain-based rewards ecosystem on Binance Smart Chain <mcreference link=\"https://www.trust-coin.site/\" index=\"0\">0</mcreference>.\n\n"
            "🚀 **How to Get Started:**\n"
            "1️⃣ **Download the TrustCoin app** for iOS or Android and create your account\n"
            "🎁 Receive a **1,000-point welcome bonus** instantly!\n\n"
            "2️⃣ **Start 24-hour mining sessions** that continue even when the app is closed\n"
            "💾 Progress saves automatically every hour\n\n"
            "3️⃣ **Complete missions & spin the Lucky Wheel** for extra points\n"
            "🎯 Multiple ways to earn rewards daily\n\n"
            "4️⃣ **Convert your points to real TBN tokens** via automated smart contract\n"
            "💰 **1,000 points = 1 TBN token**\n\n"
            "📱 The mobile app is cross-platform (React Native) with chat and team features\n"
            "🔒 TrustCoin emphasizes transparency, community-driven development, and long-term value"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "points":
        text = (
            "⛏️ **Mining & Points System**\n\n"
            "🕐 **24-Hour Mining Sessions:**\n"
            "• Earn up to **1,000 points per cycle**\n"
            "• Progress saves every hour automatically\n"
            "• Sessions resume after app restart\n\n"
            "📊 **Reward Formula:**\n"
            "`(session duration ÷ 86,400) × 1,000 points`\n\n"
            "📺 **Advertisement Rewards:**\n"
            "• Watch ads to unlock bonus strikes\n"
            "• Get multipliers for extra rewards\n\n"
            "💎 **Point-to-TBN Conversion:**\n"
            "• **Rate:** 1 TBN per 1,000 points\n"
            "• **Minimum:** 1,000 points redemption\n"
            "• **Daily Limit:** 100,000 points maximum\n"
            "• **Example:** 10,000 points = 10 TBN tokens\n\n"
            "🔗 **Smart Contract Features:**\n"
            "• Automated conversion on BSC\n"
            "• Gas fees initially covered by project\n"
            "• **Burn Rates:** 1% transfers, 0.5% conversions, 2% premium features"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "missions":
        text = (
            "🎯 **Missions & Rewards System**\n\n"
            "🏆 **Trophy Missions (1-500 points):**\n"
            "• First mining session completion\n"
            "• Consecutive collection days\n"
            "• Referring new users\n"
            "• Daily login streaks\n\n"
            "💎 **Gem Missions (1,000-5,000 points):**\n"
            "• 30-day mining streaks\n"
            "• Top efficiency achievements\n"
            "• Completing all trophy missions\n\n"
            "🎁 **Chest Missions (2,000-10,000 points):**\n"
            "• 90-day consecutive streaks\n"
            "• Building a team of 20+ referrals\n"
            "• Collecting 100,000+ total points\n\n"
            "🪙 **Coin Missions (100-1,000 points):**\n"
            "• Daily tasks like sharing the app\n"
            "• Updating your profile\n"
            "• Joining community events\n\n"
            "🎰 **Lucky Wheel System:**\n"
            "• Spin for **1-1,500 points**\n"
            "• **3 strikes per cycle**\n"
            "• **6-hour cooldown** between cycles\n"
            "• **Probabilities:** 50% (1-100), 30% (101-200), 15% (201-300), 5% (301-500)\n"
            "• Watch ads for additional spins and multipliers!"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "referral":
        text = (
            "👥 **Referral Program & Community**\n\n"
            "🔗 **Two-Tier Referral System:**\n"
            "• **Public codes** for everyone\n"
            "• **Exclusive codes** for top referrers\n\n"
            "🎁 **New User Benefits:**\n"
            "• **1,000-point welcome bonus** upon registration\n"
            "• **500 extra points** when using invitation code\n"
            "• Instant access to all features\n\n"
            "💰 **Referrer Rewards:**\n"
            "• **1,000 points per successful referral**\n"
            "• Share of referee's mining rewards\n"
            "• Recognition badges and bonuses\n"
            "• Leaderboard rankings\n\n"
            "👨‍👩‍👧‍👦 **Community Features:**\n"
            "• Team up with other miners\n"
            "• Chat in group conversations\n"
            "• Share mining strategies\n"
            "• Compete on global leaderboards\n"
            "• Participate in community events"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "roadmap":
        text = (
            "📈 **Tokenomics & Roadmap**\n\n"
            "💰 **Supply Distribution (20B TBN Total):**\n"
            "• 🏆 **12B** - Mining Rewards Pool (60%)\n"
            "• 💧 **3B** - Liquidity Reserve (15%)\n"
            "• 🛠️ **3B** - Development Fund (15%)\n"
            "• 👥 **2B** - Team Allocation (10%)\n\n"
            "🔥 **Deflationary Mechanics:**\n"
            "• **1%** burn on all token transfers\n"
            "• **0.5%** burn on point conversions\n"
            "• **2%** burn on premium features\n"
            "• **Variable burns** for milestone achievements\n\n"
            "🏛️ **Governance & Staking:**\n"
            "• Stake TBN tokens for additional rewards\n"
            "• Token-weighted voting system\n"
            "• Variable APY based on staking duration\n"
            "• Premium app features unlock\n\n"
            "🗺️ **Development Roadmap:**\n"
            "**2025:** Foundation & Enhancement\n"
            "✅ Mining, missions, lucky wheel systems\n"
            "✅ Referral and advertisement integration\n\n"
            "**2025-2026:** Testing & Launch\n"
            "🔄 Security audits and optimization\n"
            "🚀 Mainnet launch on BSC\n"
            "🆔 KYC/AI verification systems\n\n"
            "**2026-2027:** Expansion & Innovation\n"
            "📈 Major exchange listings\n"
            "🏦 DeFi protocol integration\n"
            "🌐 Trust blockchain development\n"
            "🏛️ DAO governance implementation\n"
            "🎨 NFT marketplace launch\n"
            "🌍 Metaverse partnerships\n"
            "🌉 Cross-chain bridge development\n"
            "💳 Global payment system integration"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "download":
        # Download app section with direct links
        download_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 Download for iOS", url="https://apps.apple.com/app/trustcoin")],
            [InlineKeyboardButton("🤖 Download for Android", url="https://play.google.com/store/apps/details?id=com.trustcoin")],
            [InlineKeyboardButton("🌐 Visit Official Website", url="https://www.trust-coin.site")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back")],
        ])
        text = (
            "📱 **Download TrustCoin App**\n\n"
            "🚀 **Get started with TrustCoin today!**\n\n"
            "📲 **Available on both platforms:**\n"
            "• iOS App Store\n"
            "• Google Play Store\n\n"
            "🎁 **What you get:**\n"
            "• **1,000 points welcome bonus**\n"
            "• **24/7 mining capability**\n"
            "• **Cross-platform compatibility**\n"
            "• **Real-time chat & team features**\n"
            "• **Secure blockchain integration**\n\n"
            "💡 **System Requirements:**\n"
            "• iOS 12.0+ or Android 6.0+\n"
            "• Internet connection\n"
            "• 50MB storage space\n\n"
            "🔗 Click the buttons below to download:"
        )
        await query.edit_message_text(
            text, reply_markup=download_keyboard, parse_mode="Markdown"
        )

    elif data == "security":
        text = (
            "🔒 **Security & Anti-Cheat System**\n\n"
            "🛡️ **Multi-Layer Security:**\n"
            "• **Device fingerprinting** to prevent multi-account abuse\n"
            "• **Real-time session validation** with time-based authentication\n"
            "• **AI-powered pattern analysis** to detect automation and cheating\n"
            "• **Geographic consistency checks** for authentic user behavior\n\n"
            "⚖️ **Fair Play Enforcement:**\n"
            "• **One account per person** policy\n"
            "• **Real device requirement** - no emulators\n"
            "• **No automation tools** allowed\n"
            "• **Permanent bans** for violations\n\n"
            "🔐 **Blockchain Security:**\n"
            "• **Smart contract audits** by leading security firms\n"
            "• **Deflationary mechanics** for real value\n"
            "• **Anti-whale protection** mechanisms\n"
            "• **Transparent on-chain operations**\n\n"
            "🚨 **Fraud Prevention:**\n"
            "• **Advanced encryption** for all data\n"
            "• **Behavioral analysis** algorithms\n"
            "• **Community reporting** system\n"
            "• **24/7 monitoring** infrastructure\n\n"
            "✅ **Your safety is our priority!**"
        )
        await query.edit_message_text(text=text, reply_markup=build_main_menu(), parse_mode="Markdown")

    elif data == "faq":
        text = (
            "❓ **Frequently Asked Questions**\n\n"
            "**Q1: How do I start mining?**\n"
            "A: Download the app, register, and tap the mining button. Sessions run for 24 hours automatically.\n\n"
            "**Q2: When can I withdraw my TBN tokens?**\n"
            "A: Token conversion will be available after mainnet launch on BSC (2025-2026).\n\n"
            "**Q3: Is TrustCoin free to use?**\n"
            "A: Yes! The app is completely free. You only need internet connection.\n\n"
            "**Q4: How many accounts can I have?**\n"
            "A: Only ONE account per person. Multiple accounts will result in permanent ban.\n\n"
            "**Q5: What's the minimum withdrawal?**\n"
            "A: Minimum conversion is 1,000 points = 1 TBN token.\n\n"
            "**Q6: Can I use emulators or bots?**\n"
            "A: No! Only real devices are allowed. Automation tools are strictly prohibited.\n\n"
            "**Q7: How do referrals work?**\n"
            "A: Share your referral code. You get 1,000 points per successful referral.\n\n"
            "**Q8: Is my data safe?**\n"
            "A: Yes! We use advanced encryption and security measures to protect your data.\n\n"
            "**Q9: When will TBN be listed on exchanges?**\n"
            "A: Major exchange listings are planned for 2026-2027 after mainnet launch.\n\n"
            "**Q10: How can I contact support?**\n"
            "A: Join our Telegram group or visit our website for support."
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
            [InlineKeyboardButton("Back to Main Menu", callback_data="back")],
        ])
        await query.edit_message_text(
            "Choose a link to open:", reply_markup=social_keyboard
        )

    elif data == "language_groups":
        # Language groups as direct buttons with flags
        language_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇺🇸 English Group", url="https://t.me/tructcoin_bot")],
            [InlineKeyboardButton("🇸🇦 Arabic Group", url="https://t.me/trustcoin_arabic_bot")],
            [InlineKeyboardButton("🇫🇷 French Group", url="https://t.me/trustcoin_fr_bot")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back")],
        ])
        await query.edit_message_text(
            "Choose your preferred language group:",
            reply_markup=language_keyboard
        )

    # Language group handlers removed - now using direct URL buttons

    elif data == "back":
        await query.edit_message_text(
            "Main menu:", reply_markup=build_main_menu()
        )

    else:
        await query.edit_message_text(
            "Invalid option. Returning to main menu.", reply_markup=build_main_menu()
        )

def main() -> None:
    """Initialize the bot and start polling."""
    app = ApplicationBuilder().token(BOT_TOKEN_ENG).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

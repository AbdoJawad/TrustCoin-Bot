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

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variables
BOT_TOKEN_FR = os.getenv('BOT_TOKEN_FR')

# Validate that the bot token is loaded
if not BOT_TOKEN_FR:
    raise ValueError("❌ BOT_TOKEN_FR not found in environment variables. Please check your .env file.")

# Main menu keyboard
def build_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📋 Aperçu & Commencer", callback_data="overview")],
        [InlineKeyboardButton("⛏️ Minage & Points", callback_data="points")],
        [InlineKeyboardButton("🎯 Missions & Récompenses", callback_data="missions")],
        [InlineKeyboardButton("👥 Parrainage & Communauté", callback_data="referral")],
        [InlineKeyboardButton("📈 Tokenomics & Feuille de Route", callback_data="roadmap")],
        [InlineKeyboardButton("📱 Télécharger l'App", callback_data="download")],
        [InlineKeyboardButton("🔒 Sécurité & Anti-Triche", callback_data="security")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🌐 Liens Sociaux", callback_data="social")],
        [InlineKeyboardButton("🌍 Groupes de Langues", callback_data="language_groups")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Language menu function removed - now handled inline

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command by showing the main menu."""
    welcome_text = (
        "🚀 **Bienvenue sur TrustCoin (TBN) !** 🚀\n\n"
        "💎 **Minage Mobile Révolutionnaire sur Binance Smart Chain**\n\n"
        "🎁 **Bonus de Bienvenue :** Obtenez 1 000 points instantanément lors de l'inscription !\n"
        "⛏️ **Minage :** Gagnez jusqu'à 1 000 points toutes les 24 heures\n"
        "💰 **Conversion :** 1 000 points = 1 jeton TBN\n"
        "🌟 **Offre Totale :** 20 milliards de jetons TBN\n\n"
        "📱 Téléchargez l'application maintenant et commencez votre voyage dans les cryptomonnaies !\n\n"
        "👇 Choisissez une section pour en savoir plus :"
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
            "📋 **Aperçu & Commencer**\n\n"
            "🌟 TrustCoin (TBN) est un écosystème de récompenses révolutionnaire basé sur la blockchain sur Binance Smart Chain.\n\n"
            "🚀 **Comment Commencer :**\n"
            "1️⃣ **Téléchargez l'application TrustCoin** pour iOS ou Android et créez votre compte\n"
            "🎁 Recevez un **bonus de bienvenue de 1 000 points** instantanément !\n\n"
            "2️⃣ **Démarrez des sessions de minage de 24 heures** qui continuent même lorsque l'application est fermée\n"
            "💾 Les progrès sont sauvegardés automatiquement toutes les heures\n\n"
            "3️⃣ **Complétez des missions et faites tourner la Roue de la Chance** pour des points supplémentaires\n"
            "🎯 Plusieurs façons de gagner des récompenses quotidiennement\n\n"
            "4️⃣ **Convertissez vos points en vrais jetons TBN** via un contrat intelligent automatisé\n"
            "💰 **1 000 points = 1 jeton TBN**\n\n"
            "📱 L'application mobile est multiplateforme (React Native) avec des fonctionnalités de chat et d'équipe\n"
            "🔒 TrustCoin met l'accent sur la transparence, le développement communautaire et la valeur à long terme"
        )
        await send_or_edit_message(text, build_main_menu())

    elif data == "points":
        text = (
            "⛏️ **Système de Minage & Points**\n\n"
            "🕐 **Sessions de Minage de 24 Heures :**\n"
            "• Gagnez jusqu'à **1 000 points par cycle**\n"
            "• Les progrès sont sauvegardés automatiquement toutes les heures\n"
            "• Les sessions reprennent après le redémarrage de l'application\n\n"
            "📊 **Formule de Récompense :**\n"
            "`(durée de session ÷ 86 400) × 1 000 points`\n\n"
            "📺 **Récompenses Publicitaires :**\n"
            "• Regardez des publicités pour débloquer des frappes bonus\n"
            "• Obtenez des multiplicateurs pour des récompenses supplémentaires\n\n"
            "💎 **Conversion Points vers TBN :**\n"
            "• **Taux :** 1 TBN pour 1 000 points\n"
            "• **Minimum :** Rachat de 1 000 points\n"
            "• **Limite Quotidienne :** Maximum 100 000 points\n"
            "• **Exemple :** 10 000 points = 10 jetons TBN\n\n"
            "🔗 **Fonctionnalités du Contrat Intelligent :**\n"
            "• Conversion automatisée sur BSC\n"
            "• Frais de gaz initialement couverts par le projet\n"
            "• **Taux de Brûlage :** 1% transferts, 0,5% conversions, 2% fonctionnalités premium"
        )
        await send_or_edit_message(text, build_main_menu())

    elif data == "missions":
        text = (
            "🎯 **Système de Missions & Récompenses**\n\n"
            "🏆 **Missions Trophée (1-500 points) :**\n"
            "• Complétion de la première session de minage\n"
            "• Jours de collecte consécutifs\n"
            "• Parrainage de nouveaux utilisateurs\n"
            "• Séries de connexion quotidienne\n\n"
            "💎 **Missions Gemme (1 000-5 000 points) :**\n"
            "• Séries de minage de 30 jours\n"
            "• Réalisations d'efficacité maximale\n"
            "• Complétion de toutes les missions trophée\n\n"
            "🎁 **Missions Coffre (2 000-10 000 points) :**\n"
            "• Séries consécutives de 90 jours\n"
            "• Construction d'une équipe de 20+ parrainages\n"
            "• Collecte de 100 000+ points au total\n\n"
            "🪙 **Missions Pièce (100-1 000 points) :**\n"
            "• Tâches quotidiennes comme partager l'application\n"
            "• Mise à jour de votre profil\n"
            "• Participation aux événements communautaires\n\n"
            "🎰 **Système de Roue de la Chance :**\n"
            "• Tournez pour **1-1 500 points**\n"
            "• **3 frappes par cycle**\n"
            "• **Temps de recharge de 6 heures** entre les cycles\n"
            "• **Probabilités :** 50% (1-100), 30% (101-200), 15% (201-300), 5% (301-500)\n"
            "• Regardez des publicités pour des tours supplémentaires et des multiplicateurs !"
        )
        await send_or_edit_message(text, build_main_menu())

    elif data == "referral":
        text = (
            "👥 **Programme de Parrainage & Communauté**\n\n"
            "🔗 **Système de Parrainage à Deux Niveaux :**\n"
            "• **Codes publics** pour tout le monde\n"
            "• **Codes exclusifs** pour les meilleurs parrains\n\n"
            "🎁 **Avantages pour les Nouveaux Utilisateurs :**\n"
            "• **Bonus de bienvenue de 1 000 points** lors de l'inscription\n"
            "• **500 points supplémentaires** lors de l'utilisation d'un code d'invitation\n"
            "• Accès instantané à toutes les fonctionnalités\n\n"
            "💰 **Récompenses pour les Parrains :**\n"
            "• **1 000 points par parrainage réussi**\n"
            "• Part des récompenses de minage du filleul\n"
            "• Badges de reconnaissance et bonus\n"
            "• Classements dans le tableau de bord\n\n"
            "👨‍👩‍👧‍👦 **Fonctionnalités Communautaires :**\n"
            "• Faire équipe avec d'autres mineurs\n"
            "• Discuter dans des conversations de groupe\n"
            "• Partager des stratégies de minage\n"
            "• Concourir sur les tableaux de bord mondiaux\n"
            "• Participer aux événements communautaires"
        )
        await send_or_edit_message(text, build_main_menu())

    elif data == "roadmap":
        text = (
            "🗺️ **Tokenomics & Feuille de Route**\n\n"
            "💎 **Tokenomics TBN :**\n"
            "• **Offre totale :** 1 milliard de tokens TBN\n"
            "• **Récompenses de minage :** 40% (400M TBN)\n"
            "• **Développement de l'écosystème :** 25% (250M TBN)\n"
            "• **Partenariats stratégiques :** 15% (150M TBN)\n"
            "• **Équipe & Conseillers :** 10% (100M TBN)\n"
            "• **Réserve de liquidité :** 10% (100M TBN)\n\n"
            "🔥 **Mécanismes Déflationnistes :**\n"
            "• Brûlage de tokens lors des transactions\n"
            "• Réduction des récompenses de minage au fil du temps\n"
            "• Mécanismes de rachat et de brûlage\n\n"
            "🏛️ **Gouvernance & Staking :**\n"
            "• Vote communautaire sur les propositions\n"
            "• Récompenses de staking pour les détenteurs\n"
            "• Gouvernance décentralisée progressive\n\n"
            "📅 **Feuille de Route de Développement :**\n\n"
            "**2025 T1 :**\n"
            "• Lancement de l'application mobile\n"
            "• Système de minage de base\n"
            "• Programme de parrainage\n\n"
            "**2025 T2 :**\n"
            "• Intégration de la blockchain\n"
            "• Lancement du token TBN\n"
            "• Fonctionnalités de staking\n\n"
            "**2025 T3 :**\n"
            "• Partenariats DeFi\n"
            "• Fonctionnalités de gouvernance\n"
            "• Expansion internationale\n\n"
            "**2026-2027 :**\n"
            "• Écosystème complet\n"
            "• Intégrations cross-chain\n"
            "• Adoption massive"
        )
        await send_or_edit_message(text, build_main_menu())

    elif data == "download":
        # Download app section with direct links
        download_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 Télécharger pour iOS", url="https://apps.apple.com/app/trustcoin")],
            [InlineKeyboardButton("🤖 Télécharger pour Android", url="https://play.google.com/store/apps/details?id=com.trustcoin")],
            [InlineKeyboardButton("🌐 Visiter le Site Officiel", url="https://www.trust-coin.site")],
            [InlineKeyboardButton("⬅️ Retour au Menu Principal", callback_data="back")],
        ])
        text = (
            "📱 **Téléchargement de l'Application TrustCoin**\n\n"
            "🚀 **Commencez avec TrustCoin aujourd'hui !**\n\n"
            "📲 **Disponible sur les deux plateformes :**\n"
            "• iOS App Store\n"
            "• Google Play Store\n\n"
            "🎁 **Ce que vous obtenez :**\n"
            "• **Bonus de bienvenue de 1 000 points**\n"
            "• **Capacité de minage 24/7**\n"
            "• **Compatibilité multiplateforme**\n"
            "• **Fonctionnalités de chat et d'équipe en temps réel**\n"
            "• **Intégration blockchain sécurisée**\n\n"
            "💡 **Configuration Système Requise :**\n"
            "• iOS 12.0+ ou Android 6.0+\n"
            "• Connexion Internet\n"
            "• 50 MB d'espace de stockage\n\n"
            "🔗 Cliquez sur les boutons ci-dessous pour télécharger :"
        )
        await send_or_edit_message(text, download_keyboard)

    elif data == "security":
        text = (
            "🔒 **Système de Sécurité & Anti-Triche**\n\n"
            "🛡️ **Sécurité Multi-Couches :**\n"
            "• **Empreinte d'appareil** pour empêcher l'abus de multi-comptes\n"
            "• **Validation de session en temps réel** avec authentification basée sur le temps\n"
            "• **Analyse de modèles alimentée par IA** pour détecter l'automatisation et la triche\n"
            "• **Vérifications de cohérence géographique** pour un comportement utilisateur authentique\n\n"
            "⚖️ **Application du Jeu Équitable :**\n"
            "• Politique **Un compte par personne**\n"
            "• **Exigence d'appareil réel** - pas d'émulateurs\n"
            "• **Aucun outil d'automatisation** autorisé\n"
            "• **Interdictions permanentes** pour les violations\n\n"
            "🔐 **Sécurité Blockchain :**\n"
            "• **Audits de contrats intelligents** par des entreprises de sécurité de premier plan\n"
            "• **Mécanismes déflationnistes** pour une valeur réelle\n"
            "• Mécanismes de **protection anti-baleine**\n"
            "• **Opérations transparentes sur la chaîne**\n\n"
            "🚨 **Prévention de la Fraude :**\n"
            "• **Chiffrement avancé** pour toutes les données\n"
            "• Algorithmes d'**analyse comportementale**\n"
            "• Système de **signalement communautaire**\n"
            "• Infrastructure de **surveillance 24/7**\n\n"
            "✅ **Votre sécurité est notre priorité !**"
        )
        await send_or_edit_message(text, build_main_menu())

    elif data == "faq":
        text = (
            "❓ **Questions Fréquemment Posées**\n\n"
            "**Q : Comment commencer à miner ?**\n"
            "R : Téléchargez l'app, inscrivez-vous, et appuyez sur 'Commencer le Minage'. C'est tout !\n\n"
            "**Q : Quand puis-je retirer mes tokens TBN ?**\n"
            "R : Les retraits seront disponibles après le lancement du mainnet en 2025 T2.\n\n"
            "**Q : Y a-t-il une limite au nombre de comptes ?**\n"
            "R : Oui, un seul compte par personne. Les multi-comptes entraînent une interdiction permanente.\n\n"
            "**Q : Puis-je utiliser des émulateurs ?**\n"
            "R : Non, seuls les appareils réels sont autorisés. Les émulateurs sont détectés et bannis.\n\n"
            "**Q : Qu'est-ce qui rend TBN unique ?**\n"
            "R : TBN combine le minage mobile, la gamification et la technologie blockchain pour une expérience unique.\n\n"
            "**Q : Mes données sont-elles sécurisées ?**\n"
            "R : Absolument ! Nous utilisons un chiffrement de niveau militaire et des audits de sécurité réguliers.\n\n"
            "**Q : Comment fonctionne le programme de parrainage ?**\n"
            "R : Partagez votre code, gagnez 1 000 points par parrainage réussi plus une part de leurs récompenses.\n\n"
            "**Q : Que se passe-t-il si je rate une session de minage ?**\n"
            "R : Pas de problème ! Redémarrez simplement quand vous êtes prêt. Aucune pénalité.\n\n"
            "**Q : Puis-je changer mon adresse de retrait ?**\n"
            "R : Oui, mais seulement avant le premier retrait pour des raisons de sécurité.\n\n"
            "**Q : TrustCoin est-il disponible dans le monde entier ?**\n"
            "R : Oui, TrustCoin est disponible mondialement avec support multilingue."
        )
        await send_or_edit_message(text, build_main_menu())

    elif data == "social":
        # Social links as buttons
        social_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Website", url="https://www.trust-coin.site")],
            [InlineKeyboardButton("📘 Facebook ➡️", url="https://www.facebook.com/people/TrustCoin/61579302546502/")],
            [InlineKeyboardButton("✈️ Telegram Group ➡️", url="https://t.me/+djORe9HGRi45ZDdk")],
            [InlineKeyboardButton("🎵 TikTok ➡️", url="https://www.tiktok.com/@trusrcoin?_t=ZN-8yu1iUm1Wis&_r=1")],
            [InlineKeyboardButton("🐦 X/Twitter ➡️", url="https://x.com/TBNTrustCoin")],
            [InlineKeyboardButton("⬅️ Retour au Menu Principal", callback_data="back")],
        ])
        await send_or_edit_message("Choisissez un lien à ouvrir :", social_keyboard)

    elif data == "language_groups":
        language_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇺🇸 Groupe Anglais", url="https://t.me/tructcoin_bot")],
            [InlineKeyboardButton("🇸🇦 Groupe Arabe", url="https://t.me/trustcoin_arabic_bot")],
            [InlineKeyboardButton("🇫🇷 Groupe Français", url="https://t.me/trustcoin_fr_bot")],
            [InlineKeyboardButton("⬅️ Retour au Menu Principal", callback_data="back")],
        ])
        text = (
            "🌍 **Choisissez Votre Groupe Linguistique**\n\n"
            "Sélectionnez votre langue préférée pour rejoindre le groupe Telegram correspondant :\n\n"
            "🇺🇸 **Groupe Anglais :** Discussions communautaires mondiales\n"
            "🇸🇦 **Groupe Arabe :** مجتمع عربي للنقاشات\n"
            "🇫🇷 **Groupe Français :** Communauté française pour les discussions\n\n"
            "Chaque groupe fournit :\n"
            "• 📢 Dernières mises à jour et annonces\n"
            "• 💬 Chat communautaire et support\n"
            "• 🎁 Événements exclusifs et cadeaux\n"
            "• 📚 Tutoriels et guides dans votre langue"
        )
        await send_or_edit_message(text, language_keyboard)

    # Language group handlers removed - now using direct URL buttons

    elif data == "back":
        await send_or_edit_message("Menu principal :", build_main_menu())

    else:
        await send_or_edit_message("Option invalide. Retour au menu principal.", build_main_menu())

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
    return 'TrustCoin Bot French is running!'

def run_flask():
    """Run Flask app in a separate thread."""
    port = int(os.getenv('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port, debug=False)

def main() -> None:
    """Initialize the bot."""
    global bot_app
    
    try:
        bot_app = ApplicationBuilder().token(BOT_TOKEN_FR).build()
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(CallbackQueryHandler(button_handler))
        
        webhook_url = os.getenv('WEBHOOK_URL')
        
        if webhook_url:
            # Production mode with webhook
            logging.info("Starting bot in webhook mode...")
            
            # Set webhook
            asyncio.run(bot_app.bot.set_webhook(url=webhook_url))
            
            # Start Flask server
            run_flask()
        else:
            # Development mode with polling
            logging.info("Starting bot in polling mode...")
            bot_app.run_polling(drop_pending_updates=True)
            
    except InvalidToken:
        logging.error("❌ Invalid bot token. Please check your BOT_TOKEN_FR.")
        raise
    except Exception as e:
        logging.error(f"❌ Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()

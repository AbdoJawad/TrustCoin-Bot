# 🚀 TrustCoin Bot - Multi-Language Telegram Bot

A comprehensive Telegram bot ecosystem for TrustCoin (TBN) - Revolutionary Mobile Mining on Binance Smart Chain.

## 🌟 Features

- **Multi-language Support**: English, Arabic, and French
- **Interactive Menu System**: User-friendly navigation
- **Comprehensive Information**: Complete TrustCoin ecosystem details
- **Mining & Rewards**: Real-time mining information and rewards tracking
- **Referral System**: Two-tier referral program details
- **Social Media Integration**: Direct links to all TrustCoin social platforms
- **Containerized Deployment**: Docker support for easy deployment
- **Auto-restart**: Built-in health checks and automatic recovery

## 📁 Project Structure

```
TrustCoinBot/
├── ENGLISH/
│   └── bot.py          # English language bot
├── ARABIC/
│   └── bot.py          # Arabic language bot
├── FRANCE/
│   └── bot.py          # French language bot
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Multi-container orchestration
├── start_bots.sh       # Linux/Mac startup script
├── start_bots.bat      # Windows startup script
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .dockerignore      # Docker ignore file
└── README.md          # This file
```

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**:
```bash
git clone <repository-url>
cd TrustCoinBot
```

2. **Create environment file**:
```bash
cp .env.example .env
# Edit .env with your bot tokens
```

3. **Start all bots**:
```bash
# Linux/Mac
chmod +x start_bots.sh
./start_bots.sh start

# Windows
start_bots.bat start
```

### Option 2: Manual Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Create `.env` file**:
```env
# Telegram Bot Tokens from @BotFather
BOT_TOKEN_ENG=your_english_bot_token_here
BOT_TOKEN_ARA=your_arabic_bot_token_here
BOT_TOKEN_FR=your_french_bot_token_here

# Optional Configuration
DEBUG=False
BOT_NAME=TrustCoin Bot
BOT_USERNAME=@trustcoin_bot
```

3. **Run individual bots**:
```bash
# Run all bots simultaneously
python ENGLISH/bot.py &
python ARABIC/bot.py &
python FRANCE/bot.py &
```

## 🐳 Docker Deployment

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

### Deployment Commands

```bash
# Start all bots
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all bots
docker-compose down

# Restart specific bot
docker-compose restart trustcoin-bot-english

# View status
docker-compose ps
```

### Management Scripts

Use the provided scripts for easy management:

```bash
# Linux/Mac
./start_bots.sh {start|stop|restart|logs|status}

# Windows
start_bots.bat {start|stop|restart|logs|status}
```

**Examples**:
```bash
./start_bots.sh start           # Start all bots
./start_bots.sh logs english    # View English bot logs
./start_bots.sh status          # Check all bots status
./start_bots.sh restart         # Restart all bots
```

## 🌐 Deployment Options

### 1. Heroku (Recommended)

1. **Install Heroku CLI**
2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku app**
```bash
heroku create your-trustcoin-bot
```

4. **Set environment variables**
```bash
heroku config:set BOT_TOKEN=your_bot_token_here
```

5. **Deploy**
```bash
git add .
git commit -m "Deploy TrustCoin Bot"
git push heroku main
```

### 2. Railway

1. Connect your GitHub repository to Railway
2. Set environment variable: `BOT_TOKEN`
3. Deploy automatically

### 3. Render

1. Connect your GitHub repository to Render
2. Set environment variable: `BOT_TOKEN`
3. Deploy as a Web Service

### 4. VPS Deployment

1. **Upload files to your VPS**
2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set environment variables**
```bash
export BOT_TOKEN=your_bot_token_here
```

4. **Run with PM2 (recommended)**
```bash
pm2 start bot.py --name trustcoin-bot
```

## 🔒 Security

- ✅ Environment variables for sensitive data
- ✅ .gitignore for protecting secrets
- ✅ Input validation and error handling
- ✅ Secure token management

## 📁 Project Structure

```
TrustCoinBot/
├── bot.py              # Main bot application
├── .env                # Environment variables (not in git)
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment config
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram Bot Token from @BotFather | ✅ |
| `DEBUG` | Enable debug mode (True/False) | ❌ |
| `WEBHOOK_URL` | Webhook URL for production | ❌ |
| `PORT` | Port for webhook (default: 8443) | ❌ |

## 📞 Support

For support and questions:
- Telegram: [@trustcoin_support](https://t.me/trustcoin_support)
- Website: [trust-coin.site](https://www.trust-coin.site/)

## 📄 License

This project is licensed under the MIT License.

---

**⚠️ Important Security Notes:**
- Never commit your `.env` file to version control
- Keep your bot token secure and private
- Use environment variables in production
- Regularly update dependencies for security patches
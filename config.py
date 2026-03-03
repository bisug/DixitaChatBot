from os import getenv
from dotenv import load_dotenv

# Load all environment variables defined in a .env file if it exists
load_dotenv()

# Essential Telegram API credentials
API_ID = int(getenv("API_ID", "24509589"))
API_HASH = getenv("API_HASH", "717cf21d94c4934bcbe1eaa1ad86ae75")

# Telegram Bot Token from @BotFather
BOT_TOKEN = getenv("BOT_TOKEN", "8568457723:AAFeCfdNRIi6wNYtlhfpO91WFNlG40fHEkc")

# Database connection URL for MongoDB Atlas or local MongoDB
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://vclub:vclub@vclub.hauilrr.mongodb.net/?retryWrites=true&w=majority")

# Numeric Telegram ID of the bot owner
OWNER_ID = int(getenv("OWNER_ID", "123456789"))

# Optional support group and update channel links
SUPPORT_GRP = getenv("SUPPORT_GRP", "none")
UPDATE_CHNL = getenv("UPDATE_CHNL", "none")

# Redis connection URL for caching chatbot responses
REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379")

# Toggle to start an internal web server for health monitoring (e.g., Render/Koyeb)
WEB_SERVICE = getenv("WEB_SERVICE", "False").lower() in ("true", "1", "t")

# Port to bind the web server if enabled
PORT = int(getenv("PORT", "8000"))

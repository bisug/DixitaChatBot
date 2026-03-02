from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", "24509589"))
API_HASH = getenv("API_HASH", "717cf21d94c4934bcbe1eaa1ad86ae75")
BOT_TOKEN = getenv("BOT_TOKEN", "8568457723:AAFeCfdNRIi6wNYtlhfpO91WFNlG40fHEkc")
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://vclub:vclub@vclub.hauilrr.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(getenv("OWNER_ID", "123456789"))
SUPPORT_GRP = getenv("SUPPORT_GRP", "none")
UPDATE_CHNL = getenv("UPDATE_CHNL", "none")
REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379")

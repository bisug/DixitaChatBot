import logging 
import time
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode

import redis
import config

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)
boot = time.time()
mongo = MongoCli(config.MONGO_URL)
db = mongo.Anonymous
try:
    redis_db = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)
except Exception as e:
    LOGGER.error(f"Failed to connect to Redis: {e}")
    redis_db = None
OWNER = config.OWNER_ID

class NexiChat(Client):
    def __init__(self):
        super().__init__(
            name="dixitabot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            lang_code="en",
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

    async def stop(self):
        await super().stop()


app = NexiChat()

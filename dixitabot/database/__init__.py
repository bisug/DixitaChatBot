from pymongo import MongoClient
import config

# Initialize a synchronous MongoClient for administrative/tracking operations
DAXXdb = MongoClient(config.MONGO_URL)

# Reference to the DAXX collection, used to track groups where the chatbot is disabled
DAXX = DAXXdb["DAXXDb"]["DAXX"]

# Import sub-modules for chat and user management
from .chats import *
from .users import *

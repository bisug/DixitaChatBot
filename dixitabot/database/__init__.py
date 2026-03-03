# Reuse the shared async Motor client from the main bot initializer
# This avoids opening a second MongoDB connection
from dixitabot import mongo

# Reference to the DAXX collection, used to track groups where the chatbot is disabled
DAXX = mongo["DAXXDb"]["DAXX"]

# Import sub-modules for chat and user management
from .chats import *
from .users import *

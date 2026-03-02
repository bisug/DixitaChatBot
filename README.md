<div align="center">
  <img src="https://ibb.co/B2ZNmfRg" alt="DixitaChatBot Logo" width="150" height="auto">
  <h1>DixitaChatBot</h1>
  <p><b>Next-Generation AI Chatbot for Telegram</b></p>

  [![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org)
  [![MongoDB](https://img.shields.io/badge/MongoDB-Database-green?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
  [![Redis](https://img.shields.io/badge/Redis-Cache-red?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)

  <br>
  <i>Powered by 210,000+ Real Conversations and Smart Response Caching</i>
</div>

---

## Authorship & Acknowledgements

**DixitaChatBot** is an updated and rebranded version of the original [NexiChat AI](https://github.com/DAXXTEAM/DAXXCHATBOT) repository, originally created by the [DAXXTEAM](https://github.com/DAXXTEAM).

This repository is maintained and modernized by **[Bisu G](https://github.com/bisug)**. The codebase was extensively refactored, debugged, and optimized for Python 3.13 and the Kurigram framework with the assistance of Artificial Intelligence tools including **Google Gemini** and **Anthropic Claude Sonnet**.

---

## Overview

DixitaChatBot is an advanced, high-performance Telegram Chatbot built on top of [Kurigram](https://github.com/KurimuzonAkuma/kurigram) (a modern Pyrogram fork optimized for Python 3.13) and backed by MongoDB and Redis.

Unlike simple rule-based bots, Dixita is pre-loaded with the Cornell Movie-Dialogs Corpus combined with custom conversational data, allowing it to provide surprisingly human-like, professional, and context-aware responses in multiple languages (English, Hindi, Hinglish).

It also features a self-learning mechanism where it observes group conversations and dynamically expands its vocabulary over time.

---

## Key Features

- **Pre-trained Intelligence:** 210,000+ real conversation pairs out of the box.
- **Ultra-Fast Caching:** Optional Redis integration (supports Upstash and standard Redis) ensures exact-match queries return in roughly `0.1ms`.
- **Auto-Learning:** Actively watches group chats and learns new dialect and slang patterns dynamically.
- **Trilingual Support:** Understands and replies seamlessly in English, Hindi, and Hinglish.
- **Interactive:** Uses intelligent context matching to send text, stickers, and reactions.
- **Admin Controls:** Granular control over bot states and permissions per group.
- **Asynchronous Core:** Built on Python 3.13's optimized `asyncio` for zero-blocking performance.

---

## Project Structure

```text
DixitaChatBot/
├── dixitabot/
│   ├── modules/
│   │   ├── helpers/       # UI keyboards, assets, and constants
│   │   ├── broadcast.py   # Owner broadcast logic
│   │   ├── callback.py    # Inline button handlers
│   │   ├── chatbot.py     # Core AI matching, learning, and response logic
│   │   ├── id.py          # Chat/User ID retrieval
│   │   ├── ping.py        # System latency and health metrics
│   │   ├── start.py       # Onboarding and start commands
│   │   └── stats.py       # Global database and conversation statistics
│   ├── database/          # Sync pymongo interface for basic chat/user tracking
│   ├── db/                # Async Motor interface for advanced AI data retrieval
│   ├── __init__.py        # Client initialization and MongoDB/Redis setup
│   └── __main__.py        # asyncio entry point and boot sequence
├── config.py              # Environment variable parser
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
└── sample.env             # Template for required environment variables
```

---

## Environment Variables Guide

To run DixitaChatBot, you will need to gather several credentials. Here is exactly how to get each one:

### 1. `API_ID` and `API_HASH`
These are your core Telegram developer credentials.
1. Go to [my.telegram.org](https://my.telegram.org).
2. Log in with your Telegram phone number.
3. Click on **API development tools**.
4. Create a new application (the details do not matter).
5. Copy the generated **App api_id** (`API_ID`) and **App api_hash** (`API_HASH`).

### 2. `BOT_TOKEN`
This is the unique token that controls your actual bot account.
1. Open Telegram and search for the verified [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts to name your bot and choose a username.
3. BotFather will provide you with a long HTTP API token. Copy this entirely; it is your `BOT_TOKEN`.

### 3. `MONGO_URL`
This is the connection string to your MongoDB database where all conversations and user data are stored forever.
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/) and create a free account.
2. Build a new free "Shared" cluster (M0 sandbox).
3. Create a Database User and remember the password.
4. Go to **Network Access** and add IP `0.0.0.0/0` (allow access from anywhere).
5. Go back to your cluster, click **Connect**, then **Connect your application**.
6. Copy the connection string. Replace `<password>` with the database user password you created. This full string is your `MONGO_URL`.

### 4. `OWNER_ID`
This designates you as the absolute admin of the bot.
1. Open Telegram and go to [@MissRose_bot](https://t.me/MissRose_bot) (or any ID bot).
2. Send `/id`.
3. Copy the numeric ID shown next to your name (e.g., `123456789`). This is your `OWNER_ID`.

### 5. `REDIS_URL` (Optional but Recommended)
Redis handles memory caching, making the bot significantly faster by avoiding constant database reads. If left completely blank in your `.env` file, the bot simply falls back directly to MongoDB for all queries.

If you want to use **Upstash** (an excellent serverless free option):
1. Go to [Upstash](https://upstash.com/) and create an account.
2. Create a new Redis database (Global or Regional).
3. Scroll down to the **Connect** section.
4. Select the **URL** connection format.
5. Copy the URL (it looks like `redis://default:YOUR_PASSWORD@endpoint.upstash.io:PORT`) and use it as your `REDIS_URL`.

---

## Deployment Methods

### Method 1: Deploy on a VPS (Linux / Ubuntu)

For maximum performance, deploying directly on a Virtual Private Server (VPS) is the best choice.

**1. Update system packages and install prerequisites:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git python3-pip tmux -y
```

**2. Clone the repository:**
```bash
git clone git@github.com:bisug/DixitaChatBot.git
cd DixitaChatBot
```

**3. Install Python dependencies:**
```bash
pip3 install -U pip
pip3 install -r requirements.txt
```

**4. Configure Environment Variables:**
Copy the template file to create your active configuration:
```bash
cp sample.env .env
nano .env
```
Fill in the credentials as gathered from the guide above:
```text
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MONGO_URL=your_mongodb_url
OWNER_ID=your_telegram_id
SUPPORT_GRP=your_support_group_username
UPDATE_CHNL=your_update_channel_username
REDIS_URL=your_redis_url  # Optional: Leave blank or remove entirely if not using Redis
```

**5. Start the bot persistently using tmux:**
```bash
tmux new -s dixitabot
python3 -m dixitabot
```
*(Press `Ctrl+B`, then `D` to detach and leave the bot running safely in the background).*

### Method 2: Deploy on Heroku

You can instantly deploy DixitaChatBot to Heroku using the button below. The `app.json` is configured to automatically provision a free Redis add-on (`rediscloud:30`) so caching works automatically without extra setup.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/bisug/DixitaChatBot)

### Method 3: Deploy on Railway

Railway is a fast PaaS that supports easy deployments via GitHub integration. Connect your repository and supply the environment variables defined above during the setup phase.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

---

## Commands Reference

| Command | Description | Required Privilege |
|---------|-------------|-------------------|
| `/start` | Start the bot and check if it is active. | Everyone |
| `/help` | Display the interactive help menu. | Everyone |
| `/id` | Get the current Chat ID or User ID. | Everyone |
| `/ping` | Check API latency and system resource usage. | Everyone |
| `/stats` | View global bot usage statistics. | Everyone |
| `/chatbot` | Open the interactive menu to enable/disable AI logic in the current group. | Admins Only |
| `/br` | Broadcast a copied message to all served chats. | Owner Only |
| `/an` | Forward a broadcast message to all users. | Owner Only |

---

## Contribution Guidelines

We welcome pull requests. If you would like to contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'feat: add a new feature'`).
4. Push the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

Please ensure your code follows `pep8` standards and utilizes Python 3.13 asynchronous programming patterns correctly.

---

## System Metrics

When testing locally on an average VPS (with Redis caching enabled):
- Response Phase 1 (Cache Hit): ~12ms
- Response Phase 2 (Database Fallback): ~300ms
- Typical RAM Usage: ~80-120 MB
- Base Dataset Size: ~50MB (MongoDB Document Storage)

---

## License

This project is distributed under the MIT License. See the `LICENSE` file for more information. Feel free to use, modify, and distribute the codebase.

<div align="center">
  <br>
  <i>Maintained by Bisu G. Originally forged by the DAXX Team.</i>
</div>

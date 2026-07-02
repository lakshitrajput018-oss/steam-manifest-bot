# Steam Manifest Bot

A Discord bot that generates and serves Lua and manifest files for Steam tools.

## Features
- `/gen <game_name>` - Generate and download Lua + manifest files for a game
- Database of games stored in the repository
- Automatic file serving via GitHub raw URLs

## Project Structure
```
steam-manifest-bot/
├── manifests/          # Game manifest files directory
│   ├── games_index.json    # Database of all games
│   └── [game_name]/         # Each game folder
│       ├── game_name.lua    # Lua configuration
│       └── game_name.manifest  # Manifest file
├── bot/                # Discord bot code
│   ├── bot.py         # Main bot file
│   ├── requirements.txt
│   └── config.py
└── README.md
```

## Setup Instructions

### 1. Create Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name it "Steam Manifest Bot"
4. Go to "Bot" tab → Click "Add Bot"
5. Copy the **TOKEN** (you'll need this)
6. Enable these Intents:
   - Message Content Intent
   - Server Members Intent

### 2. Set Bot Permissions
1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`, `applications.commands`
3. Select permissions:
   - Send Messages
   - Upload Files
   - Read Message History
4. Copy generated URL and open it to invite bot to your server

### 3. Clone & Setup
```bash
git clone https://github.com/lakshitrajput018-oss/steam-manifest-bot.git
cd steam-manifest-bot/bot
pip install -r requirements.txt
```

### 4. Environment Variables
Create `.env` file in `bot/` folder:
```
DISCORD_TOKEN=your_bot_token_here
GITHUB_REPO=lakshitrajput018-oss/steam-manifest-bot
GITHUB_RAW_URL=https://raw.githubusercontent.com/lakshitrajput018-oss/steam-manifest-bot/main
```

### 5. Run Bot
```bash
python bot.py
```

## Adding Games

1. Create new folder in `manifests/`: `manifests/game_name/`
2. Add files:
   - `game_name.lua` - Lua configuration
   - `game_name.manifest` - Manifest file
3. Update `manifests/games_index.json`:
```json
{
  "games": [
    {
      "name": "game_name",
      "display_name": "Game Display Name",
      "app_id": "12345"
    }
  ]
}
```

## Usage

In Discord:
```
/gen game_name
```

Bot will:
1. Check if game exists in database
2. If yes: Upload Lua + manifest files
3. If no: Show error message

## Support
For issues or questions, open an issue on GitHub.

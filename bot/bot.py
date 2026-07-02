import os
import json
import discord
from discord.ext import commands
from discord import app_commands
import requests
from dotenv import load_dotenv
import zipfile
import io

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
GITHUB_REPO = os.getenv("GITHUB_REPO", "lakshitrajput018-oss/steam-manifest-bot")
GITHUB_RAW_URL = os.getenv("GITHUB_RAW_URL", "https://raw.githubusercontent.com/lakshitrajput018-oss/steam-manifest-bot/main")

# Load games index
GAMES_INDEX_URL = f"{GITHUB_RAW_URL}/manifests/games_index.json"

def get_games_index():
    """Fetch the games index from GitHub"""
    try:
        response = requests.get(GAMES_INDEX_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"games": []}
    except Exception as e:
        print(f"Error fetching games index: {e}")
        return {"games": []}

def find_game(game_name):
    """Find a game in the database"""
    games_data = get_games_index()
    game_name_lower = game_name.lower()
    
    for game in games_data.get("games", []):
        if game.get("name", "").lower() == game_name_lower:
            return game
    return None

def create_zip_file(game_folder, lua_content, manifest_content):
    """Create a ZIP file with Lua and manifest files"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add Lua file
        zip_file.writestr(f"{game_folder}.lua", lua_content)
        
        # Add manifest file
        zip_file.writestr(f"{game_folder}.manifest", manifest_content)
    
    zip_buffer.seek(0)
    return zip_buffer

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

@bot.tree.command(name="gen", description="Generate and download ZIP file with Lua + manifest for a game")
@app_commands.describe(game_name="Name of the game to


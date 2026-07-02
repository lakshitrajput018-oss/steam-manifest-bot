import os
import json
import discord
from discord.ext import commands
from discord import app_commands
import requests
from dotenv import load_dotenv

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

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

@bot.tree.command(name="gen", description="Generate and download Lua + manifest files for a game")
@app_commands.describe(game_name="Name of the game to generate files for")
async def gen_command(interaction: discord.Interaction, game_name: str):
    """Generate Lua and manifest files for a game"""
    await interaction.response.defer()
    
    # Find game in database
    game = find_game(game_name)
    
    if not game:
        await interaction.followup.send(
            f"❌ Game **{game_name}** not found in database!\n\n"
            f"Available commands: `/gen <game_name>`"
        )
        return
    
    try:
        # Prepare file URLs
        game_folder = game.get("name", game_name)
        lua_url = f"{GITHUB_RAW_URL}/manifests/{game_folder}/{game_folder}.lua"
        manifest_url = f"{GITHUB_RAW_URL}/manifests/{game_folder}/{game_folder}.manifest"
        
        # Download files
        lua_response = requests.get(lua_url, timeout=10)
        manifest_response = requests.get(manifest_url, timeout=10)
        
        if lua_response.status_code != 200 or manifest_response.status_code != 200:
            await interaction.followup.send(
                f"❌ Error: Could not download files for **{game.get('display_name', game_name)}**"
            )
            return
        
        # Save files temporarily
        lua_filename = f"{game_folder}.lua"
        manifest_filename = f"{game_folder}.manifest"
        
        with open(lua_filename, "wb") as f:
            f.write(lua_response.content)
        
        with open(manifest_filename, "wb") as f:
            f.write(manifest_response.content)
        
        # Send files to Discord
        embed = discord.Embed(
            title=f"✅ Generated Files for {game.get('display_name', game_name)}",
            description=f"**Game:** {game.get('display_name', game_name)}\n**App ID:** {game.get('app_id', 'N/A')}",
            color=discord.Color.green()
        )
        
        with open(lua_filename, "rb") as lua_file, open(manifest_filename, "rb") as manifest_file:
            await interaction.followup.send(
                embed=embed,
                files=[
                    discord.File(lua_file, filename=lua_filename),
                    discord.File(manifest_file, filename=manifest_filename)
                ]
            )
        
        # Cleanup
        os.remove(lua_filename)
        os.remove(manifest_filename)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")
        print(f"Error in gen_command: {e}")

@bot.tree.command(name="games", description="List all available games")
async def games_command(interaction: discord.Interaction):
    """List all available games in the database"""
    await interaction.response.defer()
    
    try:
        games_data = get_games_index()
        games = games_data.get("games", [])
        
        if not games:
            await interaction.followup.send("❌ No games found in database!")
            return
        
        # Create embed with games list
        embed = discord.Embed(
            title="📚 Available Games",
            description=f"Total games: {len(games)}",
            color=discord.Color.blue()
        )
        
        game_list = "\n".join([
            f"• **{game.get('display_name', game.get('name'))}** (`{game.get('name')}`)"
            for game in games[:25]  # Limit to 25 to avoid embed size issues
        ])
        
        embed.add_field(name="Games", value=game_list or "No games available", inline=False)
        
        if len(games) > 25:
            embed.add_field(name="Note", value=f"Showing 25 of {len(games)} games", inline=False)
        
        embed.set_footer(text="Use /gen <game_name> to generate files")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="help", description="Get help on using the bot")
async def help_command(interaction: discord.Interaction):
    """Show help information"""
    embed = discord.Embed(
        title="📖 Steam Manifest Bot Help",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="/gen <game_name>",
        value="Generate and download Lua + manifest files for a game",
        inline=False
    )
    
    embed.add_field(
        name="/games",
        value="List all available games in the database",
        inline=False
    )
    
    embed.add_field(
        name="/help",
        value="Show this help message",
        inline=False
    )
    
    embed.add_field(
        name="Example Usage",
        value="`/gen valorant`\n`/games`",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in .env file")
        exit(1)
    bot.run(token)

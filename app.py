import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run("MTUyMzgxMzgyNjA3MDMxNTA2OQ.GZmel4.2omk7Cx_ym-aWmYivgWH1nsMnzGZK9W8EiK-zU")

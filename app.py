import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run("MTUyMzgxMzgyNjA3MDMxNTA2OQ.G7O9XQ.raS7Ytn2B0F_TvXGCF7iUlDtdwYaznAat-LFJY")

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run("MTUyNDAxNDk0MjU5OTExODg4OA.GFvygS.hmGRZLL2LwRixu6wjU2gT2flVU0Ze9UVIrtycQ")

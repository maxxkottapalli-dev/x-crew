import discord
from discord.ext import commands
from datetime import timedelta
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

warnings = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member} has been kicked.\nReason: {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"✅ {member} has been banned.\nReason: {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ Unbanned {user}")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="No reason"):
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"⏳ {member.mention} timed out for {minutes} minutes.")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ Removed timeout from {member.mention}")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if role is None:
        role = await ctx.guild.create_role(name="Muted")

    await member.add_roles(role)
    await ctx.send(f"🔇 {member.mention} muted.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if role:
        await member.remove_roles(role)

    await ctx.send(f"🔊 {member.mention} unmuted.")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("🔒 Channel locked.")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("🔓 Channel unlocked.")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑 Deleted {amount} messages.", delete_after=3)


@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    warnings.setdefault(member.id, [])
    warnings[member.id].append(reason)
    await ctx.send(
        f"⚠️ {member.mention} warned.\n"
        f"Total Warnings: {len(warnings[member.id])}"
    )


@bot.command()
async def warns(ctx, member: discord.Member):
    count = len(warnings.get(member.id, []))
    await ctx.send(f"{member.mention} has {count} warnings.")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"🐢 Slowmode set to {seconds} seconds.")


@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)
    await ctx.send(f"✏️ Nickname changed to {nickname}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    links = ["http://", "https://", "discord.gg"]

    if any(link in message.content.lower() for link in links):
        if not message.author.guild_permissions.manage_messages:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, links are not allowed.",
                delete_after=5
            )
            return

    await bot.process_commands(message)


bot.run(os.getenv("MTUyMzgxMzgyNjA3MDMxNTA2OQ.G9T8Ps.cYK8UzKCxcOeO7vrPFCxDqYbAAEHW6FBnzMlv8"))
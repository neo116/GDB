import discord
from discord.ext import commands


class Messaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _send_to_users(self, ctx, users, message):
        sent = 0
        failed = 0
        seen = set()

        for user in users:
            if user.bot or user.id in seen:
                continue
            seen.add(user.id)
            try:
                await user.send(message)
                sent += 1
            except (discord.Forbidden, discord.HTTPException):
                failed += 1

        result = f'Sent the message to {sent} user(s).'
        if failed:
            result += f' {failed} user(s) could not be messaged.'
        await ctx.send(result)

    @commands.command(name='everyone', aliases=['e'])
    @commands.guild_only()
    async def everyone(self, ctx, *, message):
        """DM EVERYONE LIKE A GOOD LITTLE BOT!"""
        users = (member for guild in self.bot.guilds for member in guild.members)
        await self._send_to_users(ctx, users, message)

    @commands.command(name='role', aliases=['r'])
    @commands.guild_only()
    async def role(self, ctx, role: discord.Role, *, message):
        """DM EVERYONE WITH A ROLE LIKE A GOOD LITTLE BOT!"""
        await self._send_to_users(ctx, role.members, message)

    @commands.command(name='person', aliases=['p'])
    async def person(self, ctx, user: discord.User, *, message):
        """DM A SPECIFIC USER LIKE A GOOD LITTLE BOT!"""
        await self._send_to_users(ctx, [user], message)


async def setup(bot):
    await bot.add_cog(Messaging(bot))
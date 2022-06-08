import discord

# DIRECT_MESSAGES
# GUILDS
# GUILD_MESSAGES
print(discord.Intents.VALID_FLAGS["guilds"])
print(discord.Intents.VALID_FLAGS["guild_messages"])
print(discord.Intents.VALID_FLAGS["dm_messages"])
#
# client = discord_bot.Client()
#
#
# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
#
# client.run('ODg2NDI2OTQ5MjE0NDE2OTc2.YT1bbQ.bBT_CIQre0SQOszFY4yqlH_MenI')
#
#
# class Test:
#     def __init__(self, bot):
#         self.bot = bot
#         pass
#
#     # @bot
#     def test(self):
#         pass

import discord

client = discord.Client()
@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    elif msg.content.startswith("hello"):
        await msg.channel.send("hey {}".format(msg.author))


client.run()

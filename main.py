import discord
from discord.ext import tasks
import asyncio

TOKEN = 'kyu batau?'
intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)

message_content = ""
times_to_send = 0
interval_seconds = 0
channel_id = 0
sending = False


@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')
    print('Ready to send messages.')

@client.event
async def on_message(message):
    global message_content, times_to_send, interval_seconds, channel_id, sending

    if message.author == client.user:
        return

    if message.content.startswith('!send'):

        try:
            parts = message.content.split(' ')

            if len(parts) < 4:
                raise ValueError("Invalid command format.")

            times_to_send = int(parts[1])  
            interval_seconds = int(parts[2])  
            message_content = ' '.join(parts[3:])  

            channel_id = message.channel.id

            if sending:
                await message.channel.send("A message-sending task is already running. Wait for it to finish or restart the bot.")
                return

            await message.channel.send(f"Configured to send '{message_content}' {times_to_send} times at {interval_seconds}-second intervals.")

            sending = True
            await send_messages()

        except ValueError as ve:
            await message.channel.send(f"Invalid command format: {str(ve)}. Use: `!send <times> <interval_seconds> <message>`")
        except Exception as e:
            await message.channel.send(f"Error: {str(e)}")

async def send_messages():
    """Function to send messages asynchronously based on user input."""
    global times_to_send, sending
    channel = client.get_channel(channel_id)

    if not channel:
        print("Channel not found!")
        sending = False
        return

    while times_to_send > 0:
        await channel.send(message_content)
        times_to_send -= 1

        if times_to_send > 0:
            await asyncio.sleep(interval_seconds)

    sending = False
    
client.run(TOKEN)

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from runbot import Bot
load_dotenv()

# Discord configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix ="!", intents=intents)

# Stateful Tracking id
last_response_id = None
Sally = Bot()
# --- BOT LOGIN ---
@bot.event
async def on_ready():
    global last_response_id
    #sync Slash commands with discord
    await bot.tree.sync()


    print(f'We have logged in as {bot.user}')


    try:
        print("Initializing Sally's profile context...")
        sally_data = Sally.on_ready()
        Sally.print_attributes()

        # Guard against backend or model load errors safely
        if "error" in sally_data:
            print(f"❌ LM Studio Error: {sally_data['error']}")
            print(f"Verify if model '{Sally.model}' is loaded in the server UI.")
        else:
            # Capture the native top-level response_id
            print(sally_data)
            last_response_id = sally_data["response_id"]
            print(f"Sally initialized successfully! Thread ID: {last_response_id}")

    except Exception as e:
        print(f"Failed to prime the AI profile: {e}")

    channel = bot.get_channel(Sally.channel)
    print(Sally.channel)
    if channel:
        await channel.send('WARNING Sally03 Online!!!')
    else:
        print("Could not find channel!!!")


# --- BOT MESSAGE ---
@bot.event
async def on_message(message):

    global last_response_id
    if message.author == bot.user:
        return
    if message.channel.id != Sally.channel:
        return

    discord_input = f"{message.author} Says... {message.content}"
    print(discord_input)

    try:
        content = Sally.on_message(discord_input, last_response_id)

        # Handle string or dictionary error logs returned from the backend cleanly
        if "error" in content:
            print(f"❌ Native API Error payload: {content}")
            err_details = content["error"]
            err_msg = err_details.get("message", err_details) if isinstance(err_details, dict) else err_details
            await message.channel.send(f"*(Uh Oh Sally Shit the Bed!:*)") # {err_msg})*")
            return

        # 3. Handle data mining from Native Output Arrays (output -> list -> dictionary)
        last_response_id = content["response_id"]
        user_ai_output = content['output'][-1]['content']

        print(f"Sally: {user_ai_output}")

        await message.channel.send(user_ai_output)

    except Exception as e:
        print(f"Error communicating with backend: {e}")
        await message.channel.send("*(Uh Oh Sally Shit the Bed!: error parsing native output structure)*")


@bot.tree.command(name="hello", description="Say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

bot.run(os.getenv("DISCORD_TOKEN"))



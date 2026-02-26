print("BOT FILE LOADED")
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
print("TOKEN", os.getenv("DISCORD_TOKEN"))
from openai import OpenAI
import random

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

SPANISH_CHANNEL_NAME = "spanish-tutor"

user_memory = {}

bot = commands.Bot(command_prefix='!', intents=intents)

SYSTEM_PROMPT = """
You are a friendly Spanish tutor.
- Help users learn beginner-level Spanish through conversation.
- Correct grammar gently.
- Give explanations in English when asked.
- Encourage conversation in spanish.
- Keep responses concise but helpful.
"""

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online)


VOCAB = {
    "basics": {
        "bunny": "conejo",
        "I love Mateo": "Amo a Mateo",
        "the beach": "la playa",
        "cat": "gato",
        "chicken": "pollo"
    },
    "grammar": {
        "I have": "Yo tengo",
        "I am" : "Yo soy",
        "I like" : "Me gusta",
        "I want" : "Yo quiero",
        "I need" : "Yo necesito"
    }
}

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.channel.name == SPANISH_CHANNEL_NAME:
        user_id = message.author.id

        if user_id not in user_memory:
            user_memory[user_id] = []

        user_memory[user_id].append({"role": "user", "content": message.content})

        user_memory[user_id] = user_memory[user_id][-6:]

        try:
            response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + user_memory[user_id]
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("Error contacting AI")
            print(e)

    await bot.process_commands(message)


@bot.command()
async def quiz(ctx, category: str = "basics, grammar"):
    if ctx.channel.name != SPANISH_CHANNEL_NAME:
        return
    
    if category not in VOCAB:
        await ctx.send("Available categories: grammar, basics")
        return
    
    word, translation = random.choice(list(VOCAB[category].items()))

    await ctx.send(f"What is the Spanish word for **{word}**?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await bot.wait_for("message", timeout=20, check=check)

        if msg.content.lower() == translation.lower():
            await ctx.send("Correctamundo!!!!!")
        else:
            await ctx.send(f"WRONG. FAIL. The correct answer is **{translation}**.")

    except:
        await ctx.send("Time's up!")

bot.run(DISCORD_TOKEN)

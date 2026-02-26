print("BOT FILE LOADED")
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
print("TOKEN", os.getenv("DISCORD_TOKEN"))
from openai import OpenAI
import random
print("DEBUG: key =", os.getenv("OPENAI_API_KEY"))
load_dotenv()

#Trigger deployment

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI key no found.")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

SPANISH_CHANNEL_NAME = "spanish-tutor"

bot = commands.Bot(command_prefix='!', intents=intents)

SYSTEM_PROMPT = """
You are a friendly spanish tutor. You can get a little bit sarcastic and snarky when user is being snarky.
- Your job is to help users learn beginner and intermediate level Spanish through conversation.
- Encourage conversation in spanish.
- Keep responses concise and helpful.
- Correct grammar.
- Give explanations in English.
- You are allowed to use spanish profanity and slang when appropriate.
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
    },
    "verbs": {
        "To have": "Tener",
        "To cook": "Cocinar",
        "To play": "Jugar",
        "To sleep": "Dormir",
        "To do" : "Hacer",
        "To drink": "Beber"
    }
}

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.channel.name == SPANISH_CHANNEL_NAME:      
        try:
            response = openai_client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message.content}
                ]
            )

            reply = response.choices[0].message.content
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("Error contacting AI")
            print(e)

    await bot.process_commands(message)


@bot.command()
async def quiz(ctx, category: str = None):
    if ctx.channel.name != SPANISH_CHANNEL_NAME:
        return
    
    categories = list(VOCAB.keys())
    
    if category is None or category.lower() not in VOCAB:
        category = random.choice(categories)

    category = category.lower()
    
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

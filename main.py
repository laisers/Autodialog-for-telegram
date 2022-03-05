import asyncio
import random
from telethon import TelegramClient, events, functions, types
import requests

API_ID = 17349
API_HASH = '344583e45741c457fe1862106095a5eb'
BLOCKUSER = 'stop'
UNBLOCKUSER = 'start'

uids = {}

what = ['Что?', 'не понял', 'Что такое?']
s = requests.session()


def return_answ(id, msg):
    try:
        uid = uids[id]
    except KeyError:
        uid = ''
        uids[id] = ''
    data = {
        "bot": 'Владик',
        "text": msg,
        "uid": uid
    }
    r = s.post('https://xu.su/api/send', data=data)
    answ = r.json()
    uids[id] = answ['uid']
    if answ:
        return answ['text']
    else:
        return random.choice(what)


def get_block_list():
    with open('block_list.txt') as f:
        return f.read().split('\n')


def add_block_list(user_id):
    with open('block_list.txt', 'a') as f:
        f.write(str(user_id) + '\n')


def del_block_list(user_id):
    with open('block_list.txt') as f:
        lst = f.read().split('\n')
    for en, i in enumerate(lst):
        if i == user_id:
            del lst[en]
    with open('block_list.txt', 'w') as f:
        f.write('\n'.join(lst))


async def main():
    async with TelegramClient('name', API_ID, API_HASH) as client:
        @client.on(events.NewMessage())
        async def handler(event):
            user_id = event.message.peer_id.user_id
            if event.message.peer_id == event.message.to_id:
                if event.message.text.lower() == BLOCKUSER:
                    add_block_list(user_id)
                if event.message.text.lower() == UNBLOCKUSER:
                    del_block_list(str(user_id))
                return
            if str(user_id) in get_block_list():
                return
            await asyncio.sleep(random.randint(1, 7))
            await client(functions.messages.SetTypingRequest(peer=event.message.peer_id,
                                                             action=types.SendMessageTypingAction()))
            await asyncio.sleep(random.randint(2, 5))
            answ = return_answ(user_id, event.message.text)
            await client.send_message(event.message.peer_id, message=answ)

        await client.run_until_disconnected()


asyncio.run(main())

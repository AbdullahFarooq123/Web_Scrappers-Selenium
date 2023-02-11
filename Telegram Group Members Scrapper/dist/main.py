# import datetime
#
# import pandas as pd
import asyncio
import datetime
import json
import time

from telethon import functions
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest



# https://youtu.be/aoJ-LhzqsdQ
app_id = 19578817
app_hash = '962f7bf6c0b0ac181bdb91d07eb04d83'

phone_number = '+923314058191'
client = TelegramClient(phone_number, app_id, app_hash)
client.connect()
print(client.is_connected())
print(client.is_user_authorized())
# chats = ['Byers']
#
# for chat in chats:
#     entity = client.get_entity(chat)
#     msg = client.get_messages(chat, limit=100)
#     post = client(GetHistoryRequest(
#         peer=entity,
#         limit=100,
#         offset_date=None,
#         offset_id=0,
#         max_id=0,
#         min_id=0,
#         add_offset=0,
#         hash=0
#     ))
#     print(msg)
#     print(post)
# for message in client.iter_messages(entity, offset_date=datetime.date.today()):
#     print(message)
#     data = {"group": chat, "sender": message.sender_id, "text": message.text, "date": message.date}

chats = ['python_fun']
data = []
for chat in chats:
    # client(JoinChannelRequest(chat))
    participants = client.get_participants(chat, aggressive=True)
    for user in participants:
        data.append({
            'id': user.id,
            'First Name': user.first_name,
            'Last Name': user.last_name,
            'User Name': user.username,
            'Phone': user.phone,
            'Access Hash': user.access_hash
        })
    print(f'Members : {len(data)}')

# with open('data.json', 'w') as participants_data:
#     participants_data.writelines(json.dumps(data, indent=4))
                                # send msgs to chats

chat = '+923170080348'
# client.action(chat, 'typing')
# time.sleep(2)
# msg_id = client.send_message(chat, 'Hello world! I type slow ^^').id
# print(msg_id)
                                #check if the msg has been read
# result = client(functions.messages.GetPeerDialogsRequest(peers=[chat]))
# print(result)
# print(result.dialogs[0].read_outbox_max_id)
# if result.dialogs[0].read_outbox_max_id >= 110:
#     print('Message has been read')
# else:
#     print('Not Read')
# PeerDialogs(dialogs=[Dialog(peer=PeerUser(user_id=2036681424), top_message=114, read_inbox_max_id=112, read_outbox_max_id=113, unread_count=1, unread_mentions_count=0, unread_reactions_count=0, notify_settings=PeerNotifySettings(show_previews=None, silent=None, mute_until=None, ios_sound=None, android_sound=None, other_sound=None), pinned=False, unread_mark=False, pts=None, draft=None, folder_id=None)], messages=[Message(id=114, peer_id=PeerUser(user_id=2036681424), date=datetime.datetime(2022, 9, 25, 8, 39, 10, tzinfo=datetime.timezone.utc), message='Niklo', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None)], chats=[], users=[User(id=2036681424, is_self=False, contact=True, mutual_contact=True, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, apply_min_photo=True, fake=False, bot_attach_menu=False, premium=False, attach_menu_enabled=False, access_hash=5746713491747429433, first_name='Zong', last_name=None, username=None, phone='923170080348', photo=None, status=UserStatusOnline(expires=datetime.datetime(2022, 9, 25, 8, 43, 54, tzinfo=datetime.timezone.utc)), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code=None), User(id=1883263738, is_self=True, contact=True, mutual_contact=False, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, apply_min_photo=True, fake=False, bot_attach_menu=False, premium=False, attach_menu_enabled=False, access_hash=-8471632598807832, first_name='Anonymous', last_name='shah', username=None, phone='923314058191', photo=None, status=UserStatusOffline(was_online=datetime.datetime(2022, 9, 25, 8, 34, 13, tzinfo=datetime.timezone.utc)), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code=None)], state=State(pts=196, qts=0, date=datetime.datetime(2022, 9, 25, 8, 39, 27, tzinfo=datetime.timezone.utc), seq=154, unread_count=16))
client.disconnect()

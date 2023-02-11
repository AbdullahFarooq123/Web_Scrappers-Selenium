import json
import sys
import time

from telethon.sync import TelegramClient, functions
from telethon.tl.functions.channels import JoinChannelRequest


class Bot:
    def __init__(self):
        self.api_id = 0
        self.api_hash = ''
        self.phone_number = ''
        self.client = None
        self.groups = []
        self.group_members = {}
        self.accounts = []
        self.message = ''
        self.messages_details = {}
        self.load_configurations()
        self.load_groups()
        self.load_message()

    def load_message(self):
        try:
            with open('message.txt', 'r') as message_file:
                lines = message_file.readlines()
                for line in lines:
                    self.message += line
                if len(self.message) == 0:
                    raise FileNotFoundError
        except FileNotFoundError:
            input('No Message typed\nPlease type any message in message.txt and rerun the script!')
            exit(1)

    def disconnect_client(self):
        if self.client is not None:
            self.client.disconnect()

    def save_configurations(self):
        self.api_id = int(input('Please enter you app id : '))
        self.api_hash = input('Please enter your api hash : ')
        self.phone_number = input('Please enter your phone no in the format +######## : ')
        with open('config.ini', 'w') as configuration_file:
            configuration_file.writelines(json.dumps({
                'api id': self.api_id,
                'api hash': self.api_hash,
                'phone no': self.phone_number
            }, indent=4))
        input('Data Saved successfully! Please rerun the script again\nPress enter to continue!')
        sys.exit(0)

    def load_configurations(self):
        try:
            with open('config.ini', 'r') as configuration_file:
                configurations = json.load(configuration_file)
                self.api_id = configurations['api id']
                self.api_hash = configurations['api hash']
                self.phone_number = configurations['phone no']
        except FileNotFoundError:
            self.save_configurations()

    def connect_client(self):
        self.client = TelegramClient(self.phone_number, self.api_id, self.api_hash)
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.phone_number)
            self.client.sign_in(self.phone_number, input('Enter code sent on your account : '))
            if not self.client.is_user_authorized():
                input('Code Error.\nPlease rerun the script')
                exit(1)
        print('Login successful')

    def load_groups(self):
        try:
            with open('groups.txt') as groups:
                data = groups.readlines()
                all_groups = ''
                for group in data:
                    all_groups += group
                self.groups = all_groups.split(',')
                if len(self.groups) == 0:
                    raise FileNotFoundError
                print('Groups loaded successfully!')
        except FileNotFoundError:
            input('No groups found in groups.txt\nPlease add some groups and rerun the script')
            exit(1)

    def scrape_members_from_group(self):
        members_data = {}
        for group in self.groups:
            self.client(JoinChannelRequest(group))
            participants = self.client.get_participants(group, aggressive=True)
            data = []
            for user in participants:
                if user.first_name is not None or user.last_name is not None or user.username is not None or user.phone is not None:
                    data.append({
                        'id': user.id,
                        'Name': user.first_name + (f' {user.last_name}' if user.last_name is not None else ''),
                        'User Name': user.username,
                        'Phone': user.phone,
                    })
            if not len(data) == 0:
                members_data[group] = data
            print(f'{group} members scraped successfully and saved in data.json!')
        self.group_members = members_data

    def save_members(self):
        with open('members.json', 'w') as members_file:
            members_file.writelines(json.dumps(self.group_members, indent=4))

    def load_persons(self):
        data = json.load(open('members.json'))
        for members in data.values():
            for member in members:
                member_name = member['Name']
                member_user_name = member['User Name']
                member_phone = member['Phone']
                if member_phone is not None:
                    self.accounts.append(f'+{member_phone}')
                elif member_user_name is not None:
                    self.accounts.append(member_user_name)
                elif member_name is not None:
                    self.accounts.append(member_name)

    def send_messages(self):
        print('Sending Messages')
        for account in self.accounts:
            self.client.action(account, 'typing')
            msg_id = self.client.send_message(account, self.message).id
            self.messages_details[account] = msg_id
            self.save_message_details()
            time.sleep(10)
        print('Messages successfully sent to all users')

    def save_message_details(self):
        previous_data = {}
        try:
            with open('message_details.json', 'r') as message_details_file:
                previous_data = json.load(message_details_file)
        except FileNotFoundError:
            pass
        previous_data.update(self.messages_details)
        with open('message_details.json', 'w') as message_details_file:
            message_details_file.writelines(json.dumps(previous_data, indent=4))

    def msg_status(self):
        with open('messages_status.json', 'w') as message_status:
            try:
                with open('message_details.json', 'r') as message_details:
                    data = json.load(message_details)
                    statuses = {}
                    for person in data:
                        result = self.client(functions.messages.GetPeerDialogsRequest(peers=[person]))
                        statuses[person] = (
                            'Read' if result.dialogs[0].read_outbox_max_id >= data[person] else 'Not Read')
            except FileNotFoundError:
                print('No messages sent')
                return
        message_status.writelines(json.dumps(statuses, indent=4))

    print('The message status has been saved in messages_status.json')


def run(self):
    while True:
        print('1.Send Msgs')
        print('2.Check Msg Status')
        print('3.Quit')
        option = input('Please select a number : ')
        self.connect_client()
        if option == '1':
            self.scrape_members_from_group()
            self.save_members()
            self.load_persons()
            self.send_messages()
        elif option == '2':
            self.msg_status()
        elif option == '3':
            break
        else:
            print('Wrong option')


Bot().run()

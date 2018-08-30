import time
import urllib
import re
import driver
from dbhelper import DBHelper

db = DBHelper()
TOKEN = "447451812:AAHk9KMBZdPJqguIZbi_Ooh97p0I3xXIES8"


class RPGBot(object):

    def __init__(self):
        db.setup()
        self.last_update_id = None
        self.updates = None
        self.will_stop = False
        self.nice_count = 0

        self.base_url = "https://api.telegram.org/bot{}/".format(TOKEN)
        # Dictionary that holds all the regular expressions the bot uses to process messages
        self.reglist = dict()
        self.reglist['addcharex'] = re.compile('^ */addchar')
        self.reglist['addcharform'] = re.compile('^ */addchar +(\w+) +(\w+) *$')
        self.reglist['delcharex'] = re.compile('^ */delchar')
        self.reglist['delcharform'] = re.compile('^ */delchar +(\w+) *$')
        self.reglist['hello'] = re.compile('^ *hello[, .]? ?(rover)?')
        self.reglist['noice'] = re.compile('^no?ice')

    def run(self):
        while not self.will_stop:
            self.updates = self.get_updates(self.last_update_id)
            if len(self.updates["result"]) > 0:
                self.last_update_id = self.get_last_update_id(self.updates) + 1
                self.echo_all(self.updates)
            time.sleep(0.5)

    ''' Sends a request to the URL to get any new messages.
        Offset is the numerical identifier of the first and earliest update that will be returned. A message is 
        considered confirmed as soon as getUpdates is called with an offset higher than its update_id.
        By default, update is unspecified. In this case, get_updates will return all unconfirmed updates,
        starting with the earliest.
    '''
    def get_updates(self, offset=None):
        url = self.base_url + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = driver.get_json_from_url(url)
        return js

    ''' Gets the update ID of the most recent update, to be used to confirm all previous messages. '''
    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    ''' Sends a the message given by the text param to the chat corresponding to chat_id
    '''
    def send_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        url = self.base_url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        driver.get_url(url)

    ''' Calls process text and sends the result to the chat the message came from.
        Updates is the JSON object representing the message that is being processed.
    '''
    def echo_all(self, updates):
        for update in updates["result"]:
            try:
                text = self.process_text(update)
                chat = update["message"]["chat"]["id"]
                self.send_message(text, chat)
            except Exception as e:
                print("Exception: ", e)

    ''' This method takes the message as a string, processes it, and returns the indicated response as a string. 
        To process, it reads the contents of the string and matches it against the set of keystrings.
        If there's a match, it performs the indicated operation and returns the resultant string.
                    #### In progress ####
    '''
    def process_text(self, update):
        original_message = update['message']['text']
        message = original_message.lower()

        # Just a hello
        if self.reglist['hello'].match(message):
            return 'Hello, I am a bot in testing.'

        # Add a player
        elif self.reglist['addcharex'].match(message):
            if self.reglist['addcharform'].match(message):
                match = message.split(' ')
                db.add_char(match[1], match[2])
                return 'Successfully added {} to game.'.format(match[1])
            return 'Error: incorrect format.\nUsage: \"/addchar <character> <player>\"'

        # Delete a player
        elif self.reglist['delcharform'].match(message):
            parsed_message = message.split(' ')
            if len(parsed_message) == 2:
                if db.delete_char(parsed_message[1]):
                    return 'Deleted {} from the game.'.format(parsed_message[1])
                else:
                    return 'Database Error: Could not delete character.'
            return 'Error: incorrect format. \nUsage: \"/delchar <character> <player>\"'

        # Nice
        elif self.reglist['noice'].match(message):
            self.nice_count += 1
            if self.nice_count < 5:
                return original_message
            else:
                self.nice_count = 0
                return original_message.replace('i', 'oi') if 'o' not in message else original_message
        else:
            return 'Default response'
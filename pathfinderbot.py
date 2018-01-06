import json, requests, time, urllib, sys, re
from dbhelper import DBHelper

db = DBHelper()
TOKEN = "447451812:AAHk9KMBZdPJqguIZbi_Ooh97p0I3xXIES8"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
niceCount = 0


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# @Deprecated
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = process_text(update)
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print("Exception: ",e)


def process_text(update):
    reglist = {}
    reglist["addcharex"] = re.compile("^ */addchar")
    reglist["addcharform"] = re.compile("^ */addchar +(\w+) +(\w+) *$")


    message = update["message"]["text"].lower()
    if message == "hello".lower():
        return "Hello, I am a bot in testing."
    elif reglist["addcharex"].match(message): #Add player case
        if (match = reglist["addcharform"].match(message)):
            db.add_char(match.group(1), match.group(2))
            return "Successfully added {} to game.".format(match.group(1))
        return "Error: incorrect format.\nUsage: \"/addchar <character> <player>\""
    elif message.startswith("/deletechar"): #Delete player case
        parsedMessage = message.split(" ")
        if len(parsedMessage) == 2:
            if db.delete_char(parsedMessage[1]):
                return "Deleted {} from the game.".format(parsedMessage[1])
            else:
                return "Database Error: Could not delete character."
        return "Error: incorrect format. \nUsage: \"/deletechar <character> <player>\""
    elif message.lower() == "nice":
        global niceCount
        niceCount += 1
        if niceCount - 1 < 5:
            return message
        else:
            return "Enough is enough"
    else:
        return message


def main():

    last_update_id = None
    while True:
        db.setup()
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

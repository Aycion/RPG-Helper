#### ADD IN REQUIRE STATEMENTS TO DEAL WITH ALL IMPORTS
### NEEDED: json, requests, time, urllib, sys, re
### ALSO NEED TO REDO DBHELPER IN RUBY

require 'httparty'
require 'json'
require'uri'

#db = DBHelper.new
TOKEN = "447451812:AAHk9KMBZdPJqguIZbi_Ooh97p0I3xXIES8"
URL = "https://api.telegram.org/bot#{TOKEN}/"


def get_url(url)
  HTTParty.get(url, format: :plain)
end

def get_json_from_url(url)
  content = get_url(url)
  JSON.parse(content, symbolize_names: true)
end

def get_updates(offset=nil)
  url = URL + "getUpdates?timeout=100"
  if offset
    url += "&offset=#{offset}"
  end
  js = get_json_from_url(url)
end

def get_last_update_id(updates)
  update_ids = []
  updates[:result].each{ |cur|
    update_ids.push(cur[:update_id])
  }
  update_ids.max
end

def send_message(text, chat_id)
   text = URI.parse(URI.encode(text))
   url = URL + "sendMessage?text=#{text}&chat_id=#{chat_id}"
   get_url(url)
end

def echo_all(updates)
   updates[:result].each { |cur|
      text = process_text(cur)
      chat = cur[:message][:chat][:id]
      send_message(text, chat)
   }
end

def process_text(update)
   reglist = {}
end



last_update_id = nil
loop do
   #db.setup()
   updates = get_updates(last_update_id)
   if updates[:result].length > 0
      last_update_id = get_last_update_id(updates) + 1
      echo_all(updates)
   end
   sleep(0.5)
end

#### ADD IN REQUIRE STATEMENTS TO DEAL WITH ALL IMPORTS
### NEEDED: json, requests, time, urllib, sys, re
### ALSO NEED TO REDO DBHELPER IN RUBY

require 'dbhelper.rb', 'httparty', 'json'

db = DBHelper.new
TOKEN = "447451812:AAHk9KMBZdPJqguIZbi_Ooh97p0I3xXIES8"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url)
  #need equivalent lib/functionality for requests.get
  HTTParty.get(url, format: :plain)
end

def get_json_from_url(url)
  content = get_url(url)
  JSON.parse response, symbolize_names: true

end

def get_updates(offset=None)
  url = URL + "getUpdates?timeout=100"
  if offset
    url += "&offset=#{offset}"
  end
  js = get_json_from_url(url)
end

def get_last_update_id(updates)
  update_ids = []
  updates["result"].each{ |cur|
    update_ids.push(cur.to_i)
  }
  update_ids.max
end

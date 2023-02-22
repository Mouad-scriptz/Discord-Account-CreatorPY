import requests, random, json, base64, pytz, yaml, threading
from datetime import datetime
from urllib.parse import urlencode

config = yaml.safe_load(open("config.yml"))
build_num = config["settings"]["discord_build_number"]
def get_username():
    names = requests.post(
        "https://www.spinxo.com/services/NameService.asmx/GetNames",
        json={"snr":{"category":0,"UserName":"","Hobbies":"playing","ThingsILike":"","Numbers": "1,2,6,9,,,!,$,|","WhatAreYouLike":"gaming","Words":"","Stub":"username","LanguageCode":"en","NamesLanguageID":"45","Rhyming":False,"OneWord":True,"UseExactWords":False,"ScreenNameStyleString":"Any","GenderAny":True,"GenderMale":False,"GenderFemale":False}}
    )
    return random.choice(names.json()["d"]["Names"])

def build_xsp(ua,fv):
    _json = json.dumps({
        "os":"Windows",
        "browser":"Chrome",
        "device":"",
        "system_locale":"en-US",
        "browser_user_agent":ua,
        "browser_version":fv,
        "os_version":"10",
        "referrer":"",
        "referring_domain":"",
        "referrer_current":"",
        "referring_domain_current":"",
        "release_channel":"stable",
        "client_build_number":build_num,
        "client_event_source":None,
        "design_id":0
    },separators=(",",":"))
    return base64.b64encode(_json.encode()).decode()

def build_xtrack(ua,fv):
    _json = json.dumps({
        "os":"Windows",
        "browser":"Chrome",
        "device":"",
        "system_locale":"en-US",
        "browser_user_agent":ua,
        "browser_version":fv,
        "os_version":"10",
        "referrer":"",
        "referring_domain":"",
        "referrer_current":"",
        "referring_domain_current":"",
        "release_channel":"stable",
        "client_build_number":9999,
        "client_event_source":None
    },separators=(",",":"))
    return base64.b64encode(_json.encode()).decode()
def build_oc():
    data = {
        'isIABGlobal': 'false',
        'datestamp': datetime.now(pytz.timezone('US/Eastern')).strftime('%a %b %d %Y %H:%M:%S GMT%z (%Z)'),
        'version': '6.33.0',
        'hosts': '',
        'landingPath': 'https://discord.com',
        'groups': 'C0001:1,C0002:1,C0003:1'
    }
    return urlencode(data)
open_lock = threading.Lock()
def save_token(token, isvalid):
    open_lock.acquire()
    if isvalid == True:
        valid_tokens = open("output/valid_tokens.txt","a+")
        valid_tokens.write(token+"\n")
        valid_tokens.close()
    else:
        locked_tokens = open("output/locked_tokens.txt","a+")
        locked_tokens.write(token+"\n")
        locked_tokens.close()
    open_lock.release()
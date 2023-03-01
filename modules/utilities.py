import requests, random, json, base64, pytz, yaml, threading, re
from datetime import datetime
from urllib.parse import urlencode
from modules.console import console

config = yaml.safe_load(open("config.yml"))


def requestBuildNumber():
    res = requests.get("https://discord.com/login")
    discord_login_page_exploration = res.text
    file_with_build_num = 'https://discord.com/assets/' + \
                            re.compile(r'assets/+([a-z0-9]+)\.js').findall(discord_login_page_exploration)[-2] + '.js'
    req_file_build = requests.get(file_with_build_num).text
    index_of_build_num = req_file_build.find('buildNumber') + 24
    discord_build_num = int(req_file_build[index_of_build_num:index_of_build_num + 6])

    return discord_build_num

if config["settings"]["discord_build_number"] == "": # automatically requests Discord's Build Number
    build_num = requestBuildNumber()
else:
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

def check_version():
    try:
        console.information("Checking generator version...")
        current_version = requests.get("https://raw.githubusercontent.com/Mouad-scriptz/Discord-Account-CreatorPY/main/version").text.split("\n")[0]
        local_version = open("version","r").read().splitlines()[0]
        if current_version == local_version:
            console.success("Using latest version",local_version)
        else:
            console.error(f"Using old version, current: {local_version} | latest: {current_version}")
            input("(@) Press ENTER to exit.")
    except:
        console.error("Failed to check version, skipped.")
import requests, yaml
from modules.console import console
config = yaml.safe_load(open("config.yml"))
key = config["captcha"]["key"]
service = config["captcha"]["provider"]
def get_balance():
    try:
        r = requests.post(f"https://api.{service}/getBalance",json={"clientKey":key})
        print(r.text)
        if r.json().get("balance"):
            return r.json()["balance"]
        else:
            console.failure("Failed to get captcha balance")
            return "0"
    except:
        console.failure("Failed to get captcha balance")
        return "0"
def get_captcha_key(ua,proxy):
    # Creating a task
    payload = {
        "clientKey":key,
        "task": {
            "websiteURL":"https://discord.com/",
            "websiteKey":config["captcha"]["site key"],
        }
    }
    if service == "capmonster.cloud":
        payload["task"]["type"] = "HCaptchaTask"
        payload["task"]["proxyType"] = "http"
        address = proxy.split("@")[1].split(":")[0]
        port = int(proxy.split("@")[1].split(":")[1])
        username = proxy.split(":")[0]
        password = proxy.split(":")[1].split("@")[0]
        payload["task"]["proxyAddress"] = address
        payload["task"]["proxyPort"] = port 
        payload["task"]["proxyLogin"] = username
        payload["task"]["proxyPassword"] = password
    elif service == "capsolver.com":
        payload["appId"] = "942A346E-6C5A-4AE8-B2DE-24E6F9444EA4"
        payload["task"]["type"] = "HCaptchaTurboTask"
        payload["task"]["proxy"] = proxy 
        payload["task"]["userAgent"] = ua
    r = requests.post(f"https://api.{service}/createTask",json=payload)
    try:
        if r.json().get("taskId"):
            taskid = r.json()["taskId"]
        else:
            console.failure("Couldn't retrieve captcha task id")
            return ""
    except:
        console.failure("Couldn't retrieve captcha task id")
        return ""
    # Waiting for results
    while True:
        try:
            r = requests.post(f"https://api.{service}/getTaskResult",json={"clientKey":key,"taskId":taskid})
            if r.json()["status"] == "ready":
                console.success("Solved captcha",r.json()["solution"]["gRecaptchaResponse"][:40])
                return r.json()["solution"]["gRecaptchaResponse"]
        except:
            console.failure("Failed to get captcha status.")
            return ""

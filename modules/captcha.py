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
        "task":
        {
            "websiteURL":"https://discord.com/",
            "websiteKey":config["captcha"]["site_key"],
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
    else:
        payload["task"]["type"] = "HCaptchaEnterpriseTask"
        payload["task"]["proxy"] = proxy 
        payload["userAgent"] = ua
    r = requests.post(f"https://api.{service}/createTask",json=payload)
    print(r.text)
    try:
        if r.json().get("taskId"):
            taskid = r.json()["taskId"]
        else:
            console.failure("Couldn't retrieve captcha task id")
            input("Press ENTER to exit.")
            exit(0)
    except:
        console.failure("Couldn't retrieve captcha task id")
        input("Press ENTER to exit.")
        exit(0)
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

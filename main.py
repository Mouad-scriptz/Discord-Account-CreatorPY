import yaml, threading, tls_client, requests
from modules.captcha import get_balance, get_captcha_key
from modules.utilities import get_username, build_xtrack, save_token, check_version
from modules.console import console

class Creator():
    def __init__(self):
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        self.chrome_v = 114
        self.full_chrome_v = "114.0.0.0"
        self.session = tls_client.Session( 
            f"chrome_{str(self.chrome_v)}",
            pseudo_header_order=[":authority",":method",":path",":scheme"],
            header_order=["accept","accept-encoding","accept-language","user-agent"],
            random_tls_extension_order=True
        )
        self.headers={
            'authority': "discord.com",
            'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "User-Agent": self.ua
        }
    def register(self, proxy=None):
        session = self.session
        if proxy is not None:
           session.proxies.update({
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            })
           
        # Getting cookies
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        r = session.get("https://discord.com/",headers=headers)
        cookies_dict = r.cookies.get_dict()

        # Getting fingerprint
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://discord.com/',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Track': build_xtrack(self.ua, self.full_chrome_v)
        }
        try:
            r = session.get("https://discord.com/api/v9/experiments",headers=headers,cookies=cookies_dict)
            fingerprint = r.json()["fingerprint"]
            console.success("Got fingerprint",fingerprint)
        except:
            console.failure("Failed to retrieve fingerprint.")
            Creator().register(proxy)

        # Register
        config = yaml.safe_load(open("config.yml"))
        if config["token"]["username"] != '':
            username = config["token"]["username"]
        else:
            username = get_username()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Fingerprint': fingerprint,
            'X-Track': build_xtrack(self.ua, self.full_chrome_v)
        }
        while True:
            captcha = get_captcha_key(self.ua, proxy)
            if captcha == '':
                console.failure("Failed to solve captcha, retrying...")
            else:
                break
        payload = {
            "captcha_key": captcha,
            "fingerprint": fingerprint,
            "consent": True,
            "username": username
        }
        try:
            r = session.post("https://discord.com/api/v9/auth/register",json=payload,headers=headers,cookies=cookies_dict)
            token = r.json()["token"]
        except:
            Creator().register(proxy)
        try:
            r = session.get("https://discord.com/api/v9/users/@me/affinities/users",headers={"authorization":token},cookies=cookies_dict)
        except:
            console.content("Generated UNKNOWN token",token)
            save_token(token, False)
        if r.status_code != 403:
            console.content("Generated UNLOCKED token",token)
            save_token(token, True)
        else:
            console.content("Generated LOCKED token",token)
            save_token(token, False)
        Creator().register(proxy)

def main():
    check_version
    console.information("Checking config...")
    config = yaml.safe_load(open("config.yml"))
    if config["captcha"]["key"] == '':
        console.error("No captcha key detected in config.yml")
        input("Press ENTER to exit.")
        exit(0)
    if not config["captcha"]["provider"] in ["capmonster.cloud", "capsolver.com", "anti-captcha.com"]:
        console.error("Unvalid captcha provider detected in config.yml (%s)".format(config["captcha"]["provider"]))
        input("Press ENTER to exit.")
        exit(0)
    if config["settings"]["rotating proxy"] == '':
        console.error("No proxy detected in config.yml")
        input("Press ENTER to exit.")
        exit(0)
    console.information("Checking proxy...")
    try:
        proxies = {
            "http": "http://"+config["settings"]["rotating proxy"],
            "https": "http://"+config["settings"]["rotating proxy"]
        }
        requests.get("https://www.google.com/",proxies=proxies,timeout=3)
        proxy = config["settings"]["rotating proxy"]
    except:
        console.error("Unvalid/Slow proxy")
        input("(E) Press ENTER to exit.")
        exit(0)
    console.information("Checking captcha key...")
    if not float(get_balance()) >= .1:
        console.error("Your captcha account has less then 0.1$, Please charge your funds then try again.")
        answer = input("(#) Continue anyway? (Y/N) >> ")
        if answer.lower() == "n":
            exit(0)
    console.clear()
    threads = console.input("Threads")
    try:
        if int(threads) > 0:
            threads = int(threads)
    except:
        console.error("Unvalid input.")
    console.clear()
    for _ in range(threads):
        threading.Thread(target=Creator().register,args=(proxy,)).start()
if __name__ == "__main__":
    main()

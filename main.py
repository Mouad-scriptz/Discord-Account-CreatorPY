# I know this can be better
import pkg_resources, os
installed = 0
uninstalled = 0
command = "pip install "
for lib in ['tls-client','requests','colorama','pytz','pyyaml','datetime']:
    try:
        dist = pkg_resources.get_distribution(lib)
        installed += 1
        command = command + lib + " "
    except pkg_resources.DistributionNotFound:
        uninstalled += 1
        command = command + lib + " "
command = command + " --upgrade"
print("(I) Installed libraries:",installed)
print("(I) Libraries to install:",uninstalled)
os.system(command)
print("(S) Installed all needed libraries, run main.py")

import yaml, threading, tls_client, requests, tls_client.exceptions, json, time, itertools
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
            'Authority': "discord.com",
            'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'User-Agent': self.ua
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
        try:
            r = session.get("https://discord.com/",headers=headers)
            cookies_dict = r.cookies.get_dict()
            console.success("Got cookies",len(cookies_dict))
        except tls_client.exceptions.TLSClientExeption:
            console.error("Failed to retrieve cookies, tls exception.")
            return
        except json.decoder.JSONDecodeError:
            console.error("Failed to retrieve cookies, invalid response.")
            return
        except:
            console.error("Failed to retrieve cookies, unknown error.")
            return
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
        except tls_client.exceptions.TLSClientExeption:
            console.error("Failed to retrieve fingerprint, tls exception.")
            return
        except json.decoder.JSONDecodeError:
            console.error("Failed to retrieve fingerprint, invalid response.")
            return
        except:
            console.error("Failed to retrieve fingerprint, unknown error.")
            return
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
        tries = 0
        while tries <= 3:
            captcha = get_captcha_key(self.ua, proxy)
            if captcha == '':
                tries += 1
                console.failure(f"Failed to solve captcha, retrying... ({tries})")
            else:
                break
        if tries == 3:
            return
        payload = {
            "captcha_key": captcha,
            "fingerprint": fingerprint,
            "consent": True,
            "username": username
        }
        try:
            r = session.post("https://discord.com/api/v9/auth/register",json=payload,headers=headers,cookies=cookies_dict)
            token = r.json()["token"]
        except tls_client.exceptions.TLSClientExeption:
            console.error("Failed to register, tls exception.")
            return
        except json.decoder.JSONDecodeError:
            console.error("Failed to register, invalid response.")
            return
        except:
            console.error("Failed to check token, unknown error.")
            return
        try:
            r = session.get("https://discord.com/api/v9/users/@me/affinities/users",headers={"authorization":token},cookies=cookies_dict)
        except tls_client.exceptions.TLSClientExeption:
            console.error("Failed to check token, tls exception.")
            save_token(token, True)
            return
        except json.decoder.JSONDecodeError:
            console.error("Failed to check token, invalid response.")
            save_token(token, True)
            return
        except:
            console.error("Failed to check token, unknown error.")
            save_token(token, True)
            return
        if r.status_code != 403:
            console.content("Generated UNLOCKED token",token)
            save_token(token, True)
        else:
            console.content("Generated LOCKED token",token)
            save_token(token, False)
        Creator().register(proxy)

def thread(proxies):
    while True:
        try:
            proxy = next(proxies)
            Creator().register(proxy)
        except:
            pass
def main():
    check_version()
    console.information("Checking config...")
    config = yaml.safe_load(open("config.yml"))
    if config["captcha"]["key"] == '':
        console.error("No captcha key detected in config.yml")
        input("Press ENTER to exit.")
        exit(0)
    if not config["captcha"]["provider"] in ["capmonster.cloud", "capsolver.com", "anti-captcha.com"]:
        console.error("Invalid captcha provider detected in config.yml ({config['captcha']['provider']})")
        input("Press ENTER to exit.")
        exit(0)
    proxies = open("proxies.txt").read().splitlines()
    if len(proxies) == 0:
        console.error("No proxies detected in proxies.txt")
        input("Press ENTER to exit.")
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
        if int(threads) > 0: threads = int(threads)
    except:
        console.error("Invalid input.")
        time.sleep(2)
        main()
    console.clear()
    proxies = itertools.cycle(proxies)
    for _ in range(threads):
        threading.Thread(target=thread,args=(proxies,)).start()
if __name__ == "__main__":
    main()

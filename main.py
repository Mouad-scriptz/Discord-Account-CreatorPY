import os, yaml, threading
try:
    import tls_client, requests, colorama, urllib
except:
    os.system("pip install tls-client requests colorama urllib")
from modules.captcha import get_balance, get_captcha_key
from modules.utilities import get_username, build_xtrack, save_token
from modules.better_print import console

class Creator():
    def __init__(self):
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        self.chrome_v = 110
        self.full_chrome_v = "110.0.0.0"
        self.session = tls_client.Session(
            f"chrome_{str(self.chrome_v)}",
            ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0",
            h2_settings={"HEADER_TABLE_SIZE": 65536,"MAX_CONCURRENT_STREAMS": 1000,"INITIAL_WINDOW_SIZE": 6291456,"MAX_HEADER_LIST_SIZE": 262144},
            h2_settings_order=["HEADER_TABLE_SIZE","MAX_CONCURRENT_STREAMS","INITIAL_WINDOW_SIZE","MAX_HEADER_LIST_SIZE"],
            supported_signature_algorithms=["ECDSAWithP256AndSHA256","PSSWithSHA256","PKCS1WithSHA256","ECDSAWithP384AndSHA384","PSSWithSHA384","PKCS1WithSHA384","PSSWithSHA512","PKCS1WithSHA512",],
            supported_versions=["GREASE", "1.3", "1.2"],
            key_share_curves=["GREASE", "X25519"],
            cert_compression_algo="brotli",
            pseudo_header_order=[":authority",":method",":path",":scheme"],
            connection_flow=15663105,
            header_order=["accept","user-agent","accept-encoding","accept-language"],
            random_tls_extension_order=True
        )

    def register(self, proxy=None):
        session = self.session
        if proxy:
           session.proxies.update({ # I dont know why i used update xD
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            })
        # Getting cookies
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "sec-ch-ua": f"\"Chromium\";v=\"{str(self.chrome_v)}\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"{str(self.chrome_v)}\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": self.ua
        }
        r = session.get("https://discord.com/",headers=headers)
        cookies_dict = r.cookies.get_dict()

        # Getting fingerprint
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "cookie": f'__dcfduid={cookies_dict["__dcfduid"]}; __sdcfduid={cookies_dict["__sdcfduid"]}; __cfruid={cookies_dict["__cfruid"]}; ',
            "referer": "https://discord.com/",
            "sec-ch-ua": f"\"Chromium\";v=\"{str(self.chrome_v)}\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"{str(self.chrome_v)}\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-track": build_xtrack(self.ua,self.full_chrome_v)
        }
        cookies = {"__dcfduid":cookies_dict["__dcfduid"],"__sdcfduid":cookies_dict["__sdcfduid"],"__cfruid":cookies_dict["__cfruid"]}
        r = session.get("https://discord.com/api/v9/experiments",headers=headers,cookies=cookies)
        try:
            fingerprint = r.json()["fingerprint"]
        except:
            console.failure("Failed to retrieve fingerprint.")
            Creator().register(proxy)

        # Register try 1
        config = yaml.safe_load(open("config.yml"))
        if config["token"]["username"] != '':
            username = config["token"]["username"]
        else:
            username = get_username()
        payload = {
            "consent": "true",
            "fingerprint": fingerprint,
            "username": username,
        }
        r = session.post("https://discord.com/api/v9/auth/register",json=payload,headers=headers,cookies=cookies)

        if r.status_code == 400:
            # Register try final
            payload = {
                "consent": "true",
                "fingerprint": fingerprint,
                "username": username,
                "captcha_key": get_captcha_key(self.ua,proxy)
            }

            r = session.post("https://discord.com/api/v9/auth/register",json=payload,headers=headers,cookies=cookies)
            try:
                token = r.json()["token"]
            except:
                Creator().register(proxy)
                
            try:
                r = session.get("https://discord.com/api/v9/users/@me/affinities/users",headers={"authorization":token},cookies=cookies)
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
        else:
            if r.json().get("token"):
                token = r.json()["token"]
                try:
                    r = session.get("https://discord.com/api/v9/users/@me/affinities/users",headers={"authorization":token},cookies=cookies)
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
            else:
                Creator().register(proxy)
def main():
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
    if config["settings"]["rotating-proxy"] == '':
        console.error("No proxy detected in config.yml")
        input("Press ENTER to exit.")
        exit(0)
    console.information("Checking proxy...")
    try:
        proxies = {
            "http": "http://"+config["settings"]["rotating-proxy"],
            "https": "http://"+config["settings"]["rotating-proxy"]
        }
        requests.get("https://www.google.com/",proxies=proxies,timeout=3)
        proxy = config["settings"]["rotating-proxy"]
    except:
        console.error("Unvalid proxy")
        input("Press ENTER to exit.")
        exit(0)
    console.information("Checking captcha key...")
    if not int(get_balance()) >= .1: # capsolver.com/getbalance currently down
        console.error("Your captcha account has less then 0.1$, Please charge your funds then try again.")
        answer = input("(#) Continue anyway? (Y/N) >> ")
        if answer.lower() == "n":
            exit(0)
    os.system("cls || clear")
    threads = console.input("Threads")
    try:
        if int(threads) > 0:
            threads = int(threads)
    except:
        console.error("Unvalid input.")
    for _ in range(threads):
        threading.Thread(target=Creator().register,args=(proxy,)).start()
main()

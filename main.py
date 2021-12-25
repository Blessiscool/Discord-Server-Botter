import threading
import requests,time,os
from threading import Thread
from itertools import cycle
def tokenjoiner(session,token,proxies,invite):
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    prox = {"http":f"socks5://{next(proxies)}"}
    resp = session.post(f"https://canary.discord.com/api/v8/invites/{invite}",headers=headers,proxies=prox)
    if resp.status_code == 200:
        print("Joined the guild")
    elif resp.status_code == 429:
        print("Rate limited exiting the script")
        time.sleep(1)
        os._exit(0)
    else:
        print("Invalid invite or token")
def checker(session,token,proxies):
    valid = open("tokens.txt","w")
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    proxy = {"http":f"socks5://{next(proxies)}"}
    resp = session.get("https://canary.discord.com/api/v8/users/@me",headers = headers,proxies = proxy)
    if resp.status_code == 200:
        valid.write(token + '\n')
        print("{0} valid ".format(token))
    elif resp.status_code == 429:
        print("Rate limited exiting code")
        os._exit(0)
    else:
        print("Invalid token")
def main():
    lock = threading.Lock()
    session = requests.Session()
    proxylist = open("proxies.txt","r").read().splitlines()
    proxies = cycle(proxylist)
    choice = input(" [1] Token Checker\n [2] Token Joiner\n [3] Exit\nChoice: ")
    if choice == "1":
        for user in open("tokens.txt","r").read().splitlines():
            lock.acquire()
            Thread(target=checker,args=(session,user,proxies)).start()
            lock.release()
        main()
    elif choice == "2":
        invite = input("Invite Code:  ")
        for user in open("tokens.txt","r").read().splitlines():
            try:
                lock.acquire()
                Thread(target=tokenjoiner,args=(session,user,proxies,invite)).start()
                lock.release()
            except Exception as e:
                print(e)
        main()
    else:
        os._exit(1)
if __name__ == "__main__":
    main()

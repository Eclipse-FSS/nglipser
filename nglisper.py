import random
import time
import requests
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import threading
import win32console

os.system('cls' if os.name == 'nt' else 'clear')

win32console.SetConsoleTitle("NGLipser V1")

sent, errored = 0, 0

class Console:
    @staticmethod
    def get_time() -> str:
        return time.strftime("%H:%M:%S", time.gmtime())

    @staticmethod
    def logger(*content: tuple, status: str) -> None:
        lock = threading.Lock()
        current_time = Console.get_time()

        colors = {
            "g": "\033[92m",  # Green
            "r": "\033[91m",  # Red
            "y": "\033[93m",  # Yellow
            "cyan": "\033[96m",  # Cyan
            "reset": "\033[0m"
        }
        with lock:
            if status == "g":
                sys.stdout.write(
                    f'{colors["y"]}[{current_time}]{colors["reset"]}{colors["g"]}{" ".join(content)}{colors["reset"]}\n'
                )
            elif status == "r":
                sys.stdout.write(
                    f'{colors["y"]}[{current_time}]{colors["reset"]}{colors["r"]}{" ".join(content)}{colors["reset"]}\n'
                )
            elif status == "y":
                sys.stdout.write(
                    f'{colors["y"]}[{current_time}]{colors["reset"]}{colors["y"]}{" ".join(content)}{colors["reset"]}\n'
                )

    @staticmethod
    def clear() -> None:
        os.system("cls" if os.name == "nt" else "clear")


def main(username, message, deviceid):
    global errored
    global sent

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
    }

    try:
        postresp = requests.post(
            "https://ngl.link/api/submit",
            headers=headers,
            data={
                "username": username,
                "question": message,
                "deviceId": deviceid,
            }
        )
        if postresp.status_code == 200:
            sent += 1
            Console.logger(
                f"Sent {message} to victim, Message Number: {sent}, {errored} blocked messages",
                status="g",
            )
        elif postresp.status_code == 404:
            Console.logger(f"User {username} does not exist", status="r")
            exit()
        elif postresp.status_code == 429:
            Console.logger(f"User {username} is rate limited", status="r")
        else:
            Console.logger(postresp.status_code, status="r")
    except Exception as e:
        errored += 1
        Console.logger(f"Error: {e}", status="y")


def messages():
    randomQuestions = ["Hello", "How are you?", "What's up?"]  
    return random.choice(randomQuestions)


def deviceid():
    return "".join(
        random.choice("0123456789abcdefghijklmnopqrstuvwxyz-") for _ in range(36)
    )


def center_text(text: str) -> str:
    terminal_width = os.get_terminal_size().columns
    centered_lines = [line.center(terminal_width) for line in text.split('\n')]
    return '\n'.join(centered_lines)


def handler():
    ascii_art = """
_____   __       __________                            
___  | / /______ ___  /__(_)___________________________
__   |/ /__  __ `/_  /__  /___  __ \\_  ___/  _ \\_  ___/
_  /|  / _  /_/ /_  / _  / __  /_/ /(__  )/  __/  /    
/_/ |_/  _\\__, / /_/  /_/  _  .___//____/ \\___//_/     
         /____/            /_/                         
dsc.gg/wearentdevs
    """

    cyan = "\033[96m"
    reset = "\033[0m"

    centered_art = center_text(ascii_art)
    print(f"{cyan}{centered_art}{reset}")
    
    username = str(input("Enter username (/...): "))
    threadcount = int(input("Enter message count: "))

    delay = 0.05
    messagestatus = input("Send random messages (y/n)? ").strip().lower() == "y"

    if messagestatus:
        with ThreadPoolExecutor(max_workers=threadcount) as executor:
            for _ in range(threadcount):
                executor.submit(
                    main, username, messages(), deviceid()
                )
    else:
        message = str(input("Enter message: "))
        with ThreadPoolExecutor(max_workers=threadcount) as executor:
            futures = [executor.submit(
                main, username, message, deviceid()
            ) for _ in range(threadcount)]
            for future in futures:
                future.result()  
                time.sleep(delay)

    Console.logger(f"Successfully, sents messages to {username}.", status="g")


if __name__ == "__main__":
    handler()

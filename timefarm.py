import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone
import argparse
import urllib.parse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='TimeFarm BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], help='Claim Task (y/n)')
    parser.add_argument('--upgrade', type=str, choices=['y', 'n'], help='Auto Upgrade (y/n)')
    parser.add_argument('--proxy', type=str, help='SOCKS5 proxy (format: socks5://user:pass@host:port)')
    args = parser.parse_args()

    if args.task is None:
        task_input = input("Apakah Anda ingin auto claim task? (y/n, default n): ").strip().lower()
        args.task = task_input if task_input in ['y', 'n'] else 'n'
    
    if args.upgrade is None:
        upgrade_input = input("Apakah Anda ingin auto upgrade clock? (y/n, default n): ").strip().lower()
        args.upgrade = upgrade_input if upgrade_input in ['y', 'n'] else 'n'

    return args

args = parse_arguments()
cek_task_enable = args.task
cek_upgrade_enable = args.upgrade
proxy = args.proxy

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://tg-tap-miniapp.laborx.io',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tg-tap-miniapp.laborx.io/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

def get_proxies():
    return {"http": proxy, "https": proxy} if proxy else None

def cek_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/info'
    headers['authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=headers, proxies=get_proxies())
    return response.json()

def start_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/start'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={}, proxies=get_proxies())
    return response.json()

def finish_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/finish'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={}, proxies=get_proxies())
    return response.json()

def cek_task(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/tasks'
    headers['authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=headers, proxies=get_proxies())
    return response.json()

def submit_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={}, proxies=get_proxies())
    return response.json()

def claim_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={}, proxies=get_proxies())
    return response.json()

def upgrade_level(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/me/level/upgrade'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, proxies=get_proxies())
    return response.json()

def auto_upgrade(token):
    while True:
        response = upgrade_level(token)
        if 'error' in response:
            if response['error']['message'] == "Not enough balance":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Tidak memiliki cukup saldo untuk upgrade.", flush=True)
                break
            elif response['error']['message'] == "Forbidden":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Error upgrade.", flush=True)
            elif response['error']['message'] == "Max level reached":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Sudah mencapai level maksimal.", flush=True)
                break
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Error upgrade. {response['error']['message']}", flush=True)
                break
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade ] : Upgrade berhasil, next..", flush=True)

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rMenunggu waktu claim berikutnya {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\rMenunggu waktu claim berikutnya selesai.                            ", flush=True)     

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "TimeFarm BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearman/timefarm")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")

def main():
    while True:
        print_welcome_message()
     
        if os.path.exists('tokens.txt'):
            with open('tokens.txt', 'r') as file:
                tokens = [line.strip() for line in file.readlines()]
      
        for token in tokens:
            try:
                balance_info = cek_farming(token)
    
                print(Fore.CYAN + Style.BRIGHT + f"\n===== [ Akun {tokens.index(token) + 1} ] =====")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Balance ] : {int(float(balance_info['balance'])):,}".replace(',', '.'))
                if cek_upgrade_enable == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Upgrade ] : Upgrading Clock..", end="", flush=True)
                    auto_upgrade(token)
                if cek_task_enable == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Task ] : Checking ...", end="", flush=True)
                    tasks = cek_task(token)
      
                    if tasks:
                        for task in tasks:
                            if task.get('submission', {}).get('status') == 'CLAIMED':
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : {task['title']} | Claimed                                               ", flush=True)
                            elif task.get('submission', {}).get('status') == 'COMPLETED':
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Claiming {task['title']}", flush=True)
                                response = claim_task(token, task['id'])
                                if response is not None:
                                    if 'error' in response:
                                        if response['error']['message'] == "Failed to claim reward":
                                            print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : Claim task: {task['title']} | Already claimed", end="", flush=True)
                                    else:
                                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Claim task: {task['title']} | Claimed", flush=True)    
                            
                            else:
                                print(f"\r[ Task ] : Submit task: {task['title']}", end="", flush=True)
                                if task.get('submission', {}).get('status') == 'SUBMITTED':
                                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Task ] : {task['title']} | Submitted", flush=True)
                                elif task.get('submission', {}).get('status') == 'REJECTED':
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : {task['title']} | Rejected", flush=True)
                                elif task.get('submission', {}).get('status') == 'APPROVED':
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : {task['title']} | Approved", flush=True)
                                elif task.get('submission', {}).get('status') == 'NONE':
                                    response = submit_task(token, task['id'])
                                    if response is not None:
                                        if 'error' in response:
                                            if response['error']['message'] == "Failed to submit":
                                                print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : Submit task: {task['title']} | Failed", flush=True)
                                        else:
                                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Submit task: {task['title']} | Submitted", flush=True) 
                    else:
                        print(Fore.YELLOW + Style.BRIGHT + "\r[ Task ] : No tasks available")
                farming_info = cek_farming(token)
                if farming_info.get('state') == 'FARMING':
                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Sedang farming.. - Target: {int(farming_info['target']) - int(farming_info['elapsed'])} detik")
                    wait_time = int(farming_info['target']) - int(farming_info['elapsed'])
                    animated_loading(wait_time)
                    response = finish_farming(token)
                    if response is not None:
                        if 'error' in response:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Finish farming: Gagal - {response['error']['message']}")
                        else:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Finish farming: Berhasil")
                elif farming_info.get('state') == 'IDLE':
                    print(Fore.YELLOW + Style.BRIGHT + "\r[ Farming ] : Mulai farming..")
                    response = start_farming(token)
                    if response is not None:
                        if 'error' in response:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Gagal memulai farming - {response['error']['message']}")
                        else:
                            print(Fore.GREEN + Style.BRIGHT + "\r[ Farming ] : Berhasil memulai farming")
            except Exception as e:
                print(Fore.RED + Style.BRIGHT + f"\n[ Error ] : Error pada akun {tokens.index(token) + 1} - {str(e)}", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    main()

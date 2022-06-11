import discord, json, asyncio,  base64, os, requests, ctypes, io, time, subprocess, sys, webbrowser
from discord.ext import commands
from discord.ext import tasks
from discord import Message
from discord import DMChannel
from requests.structures import CaseInsensitiveDict
from colorama import Fore, Back, Style
from colorama import init
init()


def check_config():
    try:
        with open("config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        with open("config.json", "w") as f: 
            config = { 
                "userdata": {
                    "token": "null",
                    "hours": "null",
                    "message": "null",
                    "channelids": "null"
                }
            }
            json.dump(config, f)
    return config

def slow_type(text, speed, newLine = True):
    for i in text:
        print(i, end = "", flush = True)
        time.sleep(speed)
    if newLine: 
        print() 

clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
          
intro = f"""
{Fore.MAGENTA}═════════════════════════════════════════════════════════════════════════════════════{Fore.RESET}
 ____ ____ ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ ____ 
||S |||h |||i |||l |||l |||i |||f |||y |||       |||D |||i |||s |||c |||o |||r |||d ||
||__|||__|||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|
{Fore.MAGENTA}═════════════════════════════════════════════════════════════════════════════════════{Fore.RESET}
"""

sCount=0

def rsCount():
    sCount=0

logs = f""" 
{Fore.MAGENTA}╭───────────────╮{Fore.RESET}
│ Shillify Logs │  
{Fore.MAGENTA}╰───────────────╯{Fore.RESET}
"""
check_config()
with open('config.json', "rb") as infile:
    config = json.load(infile)
    token = config["userdata"].get('token')
    channelids = config["userdata"].get('channelids')
    hours = config["userdata"].get('hours')


os.system(f"title Shillify Discord - Starting...")

if token == "null":
    clear()
    unset = True
    os.system(f"title Shillify Discord - Checking config files...")
    while unset == True:
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + "No settings found! Creating config!", 0.01)
        os.system(f"title Shillify Discord - No settings found.")
        clear()
        slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "Please enter your token: ", 0.01)
        os.system(f"title Shillify Discord - Input your token...")
        token = input()
        url = "https://canary.discord.com/api/v9/users/@me"

        headers = CaseInsensitiveDict()
        headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        headers["authorization"] = token

        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            while unset == True:
                try:
                    clear()
                    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "Please enter the delay between advertisements in hours: ", 0.01)
                    os.system(f"title Shillify Discord - Input delay between advertisements in hours.")
                    hours = int(input())
                    oldmessagevalue = config["userdata"].get('message')
                    oldchannelidsvalue = config["userdata"].get('channelids')
                    update = {"userdata": {"token": token,"hours": hours,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
                    config.update(update)
                    with open('config.json', "w") as jsfile:
                        json.dump(config, jsfile)
                        jsfile.close()
                    unset = False
                except:
                    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + "Must be a number!", 0.01)
                    os.system(f"title Shillify Discord - Must be a number!")
        else:
            slow_type(Fore.RED + "Error: " + Style.RESET_ALL + "Invalid token!", 0.01)
            os.system(f"title Shillify Discord - Invalid token!")
else:
    pass

client = commands.Bot(command_prefix = ".", self_bot=True, loop=None, intents=discord.Intents.default())

@client.event
async def on_ready():
    clear()
    slow_type(intro + Style.RESET_ALL, 0.001)
    slow_type('Logged in as ' + Fore.GREEN + f'{client.user.name}#{client.user.discriminator}' + Style.RESET_ALL, 0.001)
    slow_type(Fore.YELLOW + "\nTip: " + Style.RESET_ALL + f" Take a look at the commands typing .h in any chat!", 0.001)
    slow_type(logs + Style.RESET_ALL, 0.001)
    os.system(f"title Shillify Discord - Ready!")
    time.sleep(1)
    rsCount()
    advertise.start()

decodedmsg = base64.b64decode(config["userdata"].get('message'))
@tasks.loop(hours=int(hours))
async def advertise():
    with open('config.json', "rb") as infile:
        config = json.load(infile)
        channelstosend = config["userdata"].get('channelids')
    if "null" in channelstosend:
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" You didn't add any channels!", 0.01)
        os.system(f"title Shillify Discord - You didn't add channels!")
    else:
        sCount=0
        for i in channelstosend:
            try:
                await client.get_channel(int(i)).send(decodedmsg.decode('utf-8'))
                slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + f" Successfully sent advertisment to channel id '{i}'!", 0.01)
                sCount += 1
                os.system(f"title Shillify Discord - Working... - {sCount} message(s) sent this session.")
            except:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Could not send to channel id '{i}', removing from list...", 0.01)
                with open('config.json', "rb") as infile:
                    config = json.load(infile)
                oldtokenvalue = config["userdata"].get('token')
                oldmessagevalue = config["userdata"].get('message')
                oldchannelidsvalue = config["userdata"].get('channelids')
                oldhoursvalue = config["userdata"].get('hours')
                oldchannelidsvalue.remove(i)
                update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
                config.update(update)
                with open('config.json', "w") as jsfile:
                    json.dump(config, jsfile)
                    jsfile.close()
    slow_type(Fore.YELLOW + "Sleep: " + Style.RESET_ALL + f" Finished task, sleeping for {hours} hour(s).", 0.02)

@client.command()
async def h(ctx):
    await ctx.message.delete()
    help_all = slow_type(Fore.BLUE + "\nHelp: " + Style.RESET_ALL + f" Shillify discord help commands ", 0.01)
    slow_type(f"\n {Fore.YELLOW}.add <channelid>{Fore.RESET} Add a channel to advertise.\n {Fore.YELLOW}.rem <channelid>{Fore.RESET} Remove a channel from the list.\n {Fore.YELLOW}.cm <message>{Fore.RESET} Set/change the message to be sent and restart.\n {Fore.YELLOW}.ct <newtoken>{Fore.RESET} Change actual token and restart.\n {Fore.YELLOW}.cd <newdelay>{Fore.RESET} Change actual delay and restart.\n {Fore.YELLOW}.rt{Fore.RESET} Delete the actual config and choose what to do in terminal.\n {Fore.YELLOW}.s{Fore.RESET} Shows the actual settings/config.\n {Fore.YELLOW}.r{Fore.RESET} Restart the tool.\n {Fore.YELLOW}.dc{Fore.RESET} Discord.", 0.01)
    message = ".add <channelid> - Add a channel to advertise.\n.rem <channelid> - Remove a channel from advertise.\n.cm <message> - Set/change the message to be sent and restart.\n.ct <newtoken> - Change actual token and restart.\n.cd <newdelay> - Change actual delay and restart.\n.rt - Delete the actual config and choose what to do in terminal.\n.s - Shows the actual settings/config.\n.r - Restart the tool.\n.dc - Discord."
    await ctx.send(message, delete_after=20)
    


@client.command()
async def rem(ctx, *, id):
    await ctx.message.delete()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldmessagevalue = config["userdata"].get('message')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldhoursvalue = config["userdata"].get('hours')
    oldchannelidsvalue.remove(id)
    update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + "Removed channel!", 0.01)

@client.command()
async def add(ctx, *, id):
    await ctx.message.delete()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldmessagevalue = config["userdata"].get('message')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldhoursvalue = config["userdata"].get('hours')
    if oldchannelidsvalue == "null":
        update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": [id]}}
        config.update(update)
        with open('config.json', "w") as jsfile:
            json.dump(config, jsfile)
            jsfile.close()
    else:
        oldchannelidsvalue.append(id)
        update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
        config.update(update)
        with open('config.json', "w") as jsfile:
            json.dump(config, jsfile)
            jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + "Added channel! Type .r in any chat or restart the tool for it to take effect.", 0.01)

@client.command()
async def cm(ctx, *, msg):
    await ctx.message.delete()
    encodedmsg = str(base64.b64encode(bytes(msg, 'utf-8')))[2:-1]
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldhoursvalue = config["userdata"].get('hours')
    update = {"userdata": {"token": oldtokenvalue,"hours": oldhoursvalue,"message": encodedmsg,"channelids": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + "Changed the message!", 0.01)
    slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task! If it doesn't work, do it manually", 0.01)
    time.sleep(2)
    subprocess.call([sys.executable, os.path.realpath(__file__)]+ sys.argv[1:])

@client.command()
async def cd(ctx):
    await ctx.message.delete()
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "Enter new delay in hours: ", 0.01)
    newdelay = input()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldhoursvalue = config["userdata"].get('hours')
    oldmessagevalue = config["userdata"].get('message')
    update = {"userdata": {"token": oldtokenvalue,"hours": newdelay,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + f"Changed the delay to {newdelay} hours!", 0.01)
    slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task! If it doesn't work, do it manually", 0.01)
    time.sleep(2)
    subprocess.call([sys.executable, os.path.realpath(__file__)]+ sys.argv[1:])

@client.command()
async def ct(ctx):
    await ctx.message.delete()
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "Enter new token: ", 0.01)
    newtoken = input()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldchannelidsvalue = config["userdata"].get('channelids')
    oldhoursvalue = config["userdata"].get('hours')
    oldmessagevalue = config["userdata"].get('message')
    update = {"userdata": {"token": newtoken,"hours": oldhoursvalue,"message": oldmessagevalue,"channelids": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + f"Changed the delay to {newtoken}!", 0.01)
    slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task! If it doesn't work, do it manually", 0.01)
    time.sleep(2)
    subprocess.call([sys.executable, os.path.realpath(__file__)]+ sys.argv[1:])


@client.command()
async def rt(ctx):
    await ctx.message.delete()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
        update = {"userdata": {"token": "null", "hours": "null", "message": "null", "channelids": "null"}}
        config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + "Config reseted!", 0.01)
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "What to do now? (restart/keep): ", 0.01)
    decission = input()
    if decission == "restart":
        slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task! If it doesn't work, do it manually", 0.01)
        time.sleep(2)
        subprocess.call([sys.executable, os.path.realpath(__file__)]+ sys.argv[1:])
    else:
        pass

@client.command()
async def r(ctx):
    await ctx.message.delete()
    slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task! If it doesn't work, do it manually", 0.01)
    time.sleep(2)
    subprocess.call([sys.executable, os.path.realpath(__file__)]+ sys.argv[1:])

@client.command()
async def s(ctx):
    await ctx.message.delete()
    with open('config.json', "rb") as infile:
        sConfig = json.load(infile)
    sToken = config["userdata"].get('token')
    sChannelids = config["userdata"].get('channelids')
    sMsg = config["userdata"].get('message')
    sHours = config["userdata"].get('hours')
    if sHours == "null":
        sHours = "empty"
    if sToken == "null":
        sToken = "empty"
    if sChannelids == "null":
        sChannelids = "empty"
    if sMsg == "null":
        sMsg = "empty"
    else:
        sMsg = decodedmsg.decode('utf-8')
    slow_type(Fore.BLUE + "\nSettings:\n " + Style.RESET_ALL + f"Token: {sToken}\n Delay: {sHours}\n Channel IDs: {sChannelids}\n Message: {sMsg}\n", 0.01)

@client.command()
async def dc(ctx):
    await ctx.message.delete()
    webbrowser.open('http://discord.gg/kws')
    slow_type(Fore.MAGENTA + "Success: " + Style.RESET_ALL + "Opening discord.gg/kws in browser!", 0.01)

client.run(token, bot=False)
input()
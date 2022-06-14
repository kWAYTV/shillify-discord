import discord, json, asyncio, base64, os, requests, ctypes, io, time, subprocess, sys, webbrowser
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
                    "seconds": "null",
                    "message": "null",
                    "channels": {"null": "null"}
                }
            }
            json.dump(config, f)
    return config

def slow_type(text, speed, newLine=True):
    for i in text:
        print(i, end="", flush=True)
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

sCount = 0

def rsCount():
    sCount = 0


logs = f""" 
{Fore.MAGENTA}╭───────────────╮{Fore.RESET}
│ Shillify Logs │  
{Fore.MAGENTA}╰───────────────╯{Fore.RESET}
"""
check_config()
with open('config.json', "rb") as infile:
    config = json.load(infile)
    token = config["userdata"].get('token')
    channelids = config["userdata"].get('channels')
    seconds = 0

with open('config.json', "rb") as infile:
    temp_config = json.load(infile)

os.system(f"title Shillify Discord - Starting... - discord.gg/kws")

if token == "null":
    clear()
    unset = True
    while unset == True:
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + "No settings found! Creating config!", 0.01)
        os.system(f"title Shillify Discord - Creating config. - discord.gg/kws")
        time.sleep(1)
        clear()
        slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "Please enter your token: ", 0.01)
        os.system(f"title Shillify Discord - Input your token...  - discord.gg/kws")
        token = input()
        url = "https://canary.discord.com/api/v9/users/@me"

        headers = CaseInsensitiveDict()
        headers[
            "user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        headers["authorization"] = token

        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            while unset == True:
                try:
                    clear()
                    slow_type(
                        Fore.BLUE + "Input: " + Style.RESET_ALL + "Please enter the delay between advertisements in seconds: ",
                        0.01)
                    seconds = int(input())
                    oldmessagevalue = config["userdata"].get('message')
                    oldchannelidsvalue = config["userdata"].get('channels')
                    update = {"userdata": {"token": token, "seconds": seconds, "message": oldmessagevalue,
                                           "channels": oldchannelidsvalue}}
                    config.update(update)
                    with open('config.json', "w") as jsfile:
                        json.dump(config, jsfile)
                        jsfile.close()
                    unset = False
                except:
                    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + "Must be a number!", 0.01)
        else:
            slow_type(Fore.RED + "Error: " + Style.RESET_ALL + "Invalid token!", 0.01)
else:
    pass

client = commands.Bot(command_prefix=".", self_bot=True, loop=None, intents=discord.Intents.default())

@client.event
async def on_ready():
    clear()
    slow_type(intro + Style.RESET_ALL, 0.001)
    slow_type('Logged in as ' + Fore.GREEN + f'{client.user.name}#{client.user.discriminator}' + Style.RESET_ALL, 0.001)
    slow_type(logs + Style.RESET_ALL, 0.001)
    os.system(f"title Shillify Discord - Ready! - discord.gg/kws")
    time.sleep(1)
    rsCount()
    advertise.start()

decodedmsg = base64.b64decode(config["userdata"].get('message'))

@tasks.loop(seconds=int(seconds))
async def advertise():
    with open('config.json', "rb") as infile:
        config = json.load(infile)
        channels_config = config["userdata"].get('channels')
        temp_channels_config = temp_config["userdata"].get('channels')
        decodedmsg = base64.b64decode(config["userdata"].get('message'))

        if "null" in channels_config or len(channels_config) == 0:

            if advertise.seconds is 0:
                seconds = int(config["userdata"].get('seconds'))
                advertise.change_interval(seconds=seconds)
                return

            slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" You didn't add any channels!", 0.01)

            seconds = config["userdata"].get('seconds')
            advertise.change_interval(seconds=seconds)

            slow_type(Fore.YELLOW + "Sleep: " + Style.RESET_ALL + f" Finished task, sleeping for {seconds} second(s).",
                      0.02)
            return

        channels_to_send = list()

        for id_e, delay_e in temp_channels_config.items():
            if delay_e == "null":
                delay_e = config["userdata"].get('seconds')
            if delay_e <= advertise.seconds:
                channels_to_send.append(id_e)
                temp_channels_config[id_e] = delay_e - advertise.seconds
            else:
                temp_channels_config[id_e] = delay_e - advertise.seconds

        counter = 0

        for channel_id in channels_to_send:
            await client.get_channel(int(channel_id)).send(str(decodedmsg)[2:-1])
            slow_type(
                Fore.GREEN + f"Success: " + Style.RESET_ALL + f" Successfully sent advertisment to channel id '{channel_id}'!", 0.01)
            counter += 1

            os.system(f"title Shillify Discord - Working... - {counter} message(s) sent this session. - discord.gg/kws")

        seconds = 999999999999999

        for id_e, delay_e in temp_channels_config.items():
            if delay_e <= 0:
                temp_channels_config[id_e] = channels_config[id_e]

        for delay_e in temp_channels_config.values():
            if delay_e < seconds:
                seconds = delay_e

        advertise.change_interval(seconds=seconds)

@client.command()
async def h(ctx):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Loading help... - discord.gg/kws")
    help_all = slow_type(Fore.BLUE + "\nHelp: " + Style.RESET_ALL + f" Shillify discord help commands ", 0.01)
    slow_type(
        f"\n {Fore.YELLOW}.add <channelID> <delay/empty for default>{Fore.RESET} Add a channel to advertise.\n {Fore.YELLOW}.rem <channelID>{Fore.RESET} Remove a channel from the list.\n {Fore.YELLOW}.cm <message>{Fore.RESET} Set/change the message to be sent and restart.\n {Fore.YELLOW}.ct <newtoken>{Fore.RESET} Change actual token and restart.\n {Fore.YELLOW}.cd <newdelay>{Fore.RESET} Change actual delay and restart.\n {Fore.YELLOW}.rt{Fore.RESET} Delete the actual config and choose what to do in terminal.\n {Fore.YELLOW}.s{Fore.RESET} Shows the actual settings/config.\n {Fore.YELLOW}.r{Fore.RESET} Restart the tool.\n {Fore.YELLOW}.dc{Fore.RESET} Discord.",
        0.01)
    os.system(f"title Shillify Discord - Help loaded! - discord.gg/kws")


@client.command()
async def rem(ctx, *, id):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Removing channel... - discord.gg/kws")
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldmessagevalue = config["userdata"].get('message')
    oldchannelidsvalue = config["userdata"].get('channels')
    oldhoursvalue = config["userdata"].get('seconds')
    del oldchannelidsvalue[id]
    update = {"userdata": {"token": oldtokenvalue, "seconds": oldhoursvalue, "message": oldmessagevalue,
                           "channels": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + "Removed channel!", 0.01)
    os.system(f"title Shillify Discord - Channel removed! - discord.gg/kws")


@client.command()
async def add(ctx, id, delay):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Adding channel... - discord.gg/kws")
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldmessagevalue = config["userdata"].get('message')
    oldchannelidsvalue = config["userdata"].get('channels')
    oldhoursvalue = config["userdata"].get('seconds')
    try:
        delay = int(delay)
    except ValueError:
        delay = int(oldhoursvalue)
    if oldchannelidsvalue == "null":
        update = {"userdata": {"token": oldtokenvalue, "seconds": oldhoursvalue, "message": oldmessagevalue,
                               "channels": {id: delay}}}
        config.update(update)
        temp_config.update(update)
        with open('config.json', "w") as jsfile:
            json.dump(config, jsfile)
            jsfile.close()
    else:
        if 'null' in oldchannelidsvalue.keys():
            del oldchannelidsvalue['null']

        oldchannelidsvalue.update({id: delay})
        update = {"userdata": {"token": oldtokenvalue, "seconds": oldhoursvalue, "message": oldmessagevalue,
                               "channels": oldchannelidsvalue}}
        config.update(update)
        temp_config.update(update)
        with open('config.json', "w") as jsfile:
            json.dump(config, jsfile)
            jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + "Added channel!", 0.01)
    os.system(f"title Shillify Discord - Added channel! - discord.gg/kws")


@client.command()
async def cm(ctx, *, msg):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Changing message... - discord.gg/kws")
    encodedmsg = str(base64.b64encode(bytes(msg, 'utf-8')))[2:-1]
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldchannelidsvalue = config["userdata"].get('channels')
    oldhoursvalue = config["userdata"].get('seconds')
    update = {"userdata": {"token": oldtokenvalue, "seconds": oldhoursvalue, "message": encodedmsg,
                           "channels": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + "Changed the message!", 0.01)
    slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task! If it doesn't work, do it manually",
              0.01)
    time.sleep(2)
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    os.system(f"title Shillify Discord - Message changed! Restarting... - discord.gg/kws")


@client.command()
async def cd(ctx):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Changing delay... - discord.gg/kws")
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "Enter new delay in seconds: ", 0.01)
    newdelay = int(input())
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldchannelidsvalue = config["userdata"].get('channels')
    oldhoursvalue = config["userdata"].get('seconds')
    oldmessagevalue = config["userdata"].get('message')
    update = {"userdata": {"token": oldtokenvalue, "seconds": newdelay, "message": oldmessagevalue,
                           "channels": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + f"Changed the delay to {newdelay} seconds!", 0.01)
    slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task! If it doesn't work, do it manually",
              0.01)
    time.sleep(2)
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    os.system(f"title Shillify Discord - Delay changed! Restarting... - discord.gg/kws")


@client.command()
async def ct(ctx):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Changing token... - discord.gg/kws")
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "Enter new token: ", 0.01)
    newtoken = input()
    with open('config.json', "rb") as infile:
        config = json.load(infile)
    oldtokenvalue = config["userdata"].get('token')
    oldchannelidsvalue = config["userdata"].get('channels')
    oldhoursvalue = config["userdata"].get('seconds')
    oldmessagevalue = config["userdata"].get('message')
    update = {"userdata": {"token": newtoken, "seconds": oldhoursvalue, "message": oldmessagevalue,
                           "channels": oldchannelidsvalue}}
    config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + f"Changed the delay to {newtoken}!", 0.01)
    slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task! If it doesn't work, do it manually",
              0.01)
    time.sleep(2)
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    os.system(f"title Shillify Discord - Token changed! Restarting... - discord.gg/kws")


@client.command()
async def rt(ctx):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Resetting config... - discord.gg/kws")
    with open('config.json', "rb") as infile:
        config = json.load(infile)
        update = {"userdata": {"token": "null", "seconds": "null", "message": "null", "channels": {"null": "null"}}}
        config.update(update)
    with open('config.json', "w") as jsfile:
        json.dump(config, jsfile)
        jsfile.close()
    slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + "Config reseted!", 0.01)
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + "What to do now? (restart/keep): ", 0.01)
    decission = input()
    if decission == "restart":
        slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task!", 0.01)
        time.sleep(2)
        subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    else:
        pass
    os.system(f"title Shillify Discord - Config reseted! - discord.gg/kws")


@client.command()
async def r(ctx):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Restarting... - discord.gg/kws")
    slow_type(Fore.CYAN + "Restart: " + Style.RESET_ALL + "Trying to restart task!", 0.01)
    time.sleep(2)
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    os.system(f"title Shillify Discord - Restarted! - discord.gg/kws")


@client.command()
async def s(ctx):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Loading settings command... - discord.gg/kws")
    with open('config.json', "rb") as infile:
        sConfig = json.load(infile)
    sToken = config["userdata"].get('token')
    sChannelids = config["userdata"]['channels']
    sMsg = config["userdata"].get('message')
    sHours = config["userdata"].get('seconds')
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
    slow_type(
        Fore.BLUE + "\nSettings:\n " + Style.RESET_ALL + f"Token: {sToken}\n Delay: {sHours}\n Channels: {sChannelids}\n Message: {sMsg}\n",
        0.01)
    os.system(f"title Shillify Discord - Settings command loaded! - discord.gg/kws")


@client.command()
async def dc(ctx):
    await ctx.message.delete()
    os.system(f"title Shillify Discord - Opening website... - discord.gg/kws")
    webbrowser.open('http://discord.gg/kws')
    slow_type(Fore.MAGENTA + "Success: " + Style.RESET_ALL + "Opening discord.gg/kws in browser!", 0.01)
    os.system(f"title Shillify Discord - Website opened! - discord.gg/kws")

client.run(token, bot=False)
input()

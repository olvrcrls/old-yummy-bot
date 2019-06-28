#!/usr/bin/env python3

import discord, asyncio, random, requests, json, time, os, subprocess, sys, traceback, threading
import pytz
from pytz import timezone 
from datetime import datetime, timedelta
from yummy_token import token, novaUsername, novaPassword
from discord.ext import commands
from discord.ext.commands import Bot
from pyquery import PyQuery
from lxml import html
from bs4 import BeautifulSoup
from urllib.parse import quote

prefix=["$", "-", "!"]
description="A bot intended for Yummy Yummy Dumplings in NovaRO. Created by Andie."
bot = commands.Bot(command_prefix=prefix, description=description)
localToken = token
bot.remove_command('help')
session_requests = requests.session()

yyd_recruit_channel = "428463114120462336"
yyd_bg_channel = "461214457427787781"
yyd_summer_fest_channel = "466274296386551818"
yyd_main_chat = "428465462096166918"
yyd_server = "428458200174428160"

den_notif_channel = "470852311325999104"
den_server = "419101228467879937"
midnight_snacks_server = "473910000205561858"
elephants = "506332548247584778" # korea's and oli's woe guild
interval = False
timeInterval = 3600 # 1 hour


network_server = "532466596644651008" # Creative's Discord server
network_bot_channel = "532477151035916299" # creative's event time server

def setInterval(func, time):
  e = threading.Event()
  while not e.wait(time):
    func()

def toggleInterval():
  interval = not interval

@bot.event
async def on_ready():
 print(bot.user.name + " is ready.")
 member_count = 0
 total_members = bot.get_all_members()
 for member in total_members:
  member_count += 1
 await bot.change_presence(game=discord.Game(name="with %s members| use %shelp or %shelp" % (str(member_count), prefix[0], prefix[1]))) #str(len(bot.servers)),
 # await bot.send_message(ctx.message.channel, "Automated Event Notification commenced!")
 print("Automated Event Notification commenced!")
 print("Elephants attendance system also initiated.")
 format = "%H:%M:%S"
 for server in bot.servers:
  if server.id == yyd_server:
   yyd = server
   continue
  if server.id == den_server:
   den = server
   continue
  if server.id == network_server:
      network = server
      continue

 for channel in den.channels:
  if channel.id == den_notif_channel:
   den_notif = channel
   break
 for channel in network.channels:
     if channel.id == network_bot_channel:
         network_notif = channel
 for channel in yyd.channels:
  if channel.id == yyd_recruit_channel:
   recruit_channel = channel
   continue
  # if channel.id == yyd_bg_channel:
  #  bg_channel = channel
  #  continue
  if channel.id == yyd_summer_fest_channel:
   summer_fest_channel = channel
   continue
  if channel.id == yyd_main_chat:
   main_chat = channel
   continue

 while True:
  ph_time = timezone('Asia/Manila')
  ph_location = ph_time.normalize(ph_time.localize(datetime.now() + timedelta(hours=8)))
  ph_time_now = ph_location.strftime(format)
  await asyncio.sleep(1)
  # Summer event Notification ##
  # if ph_time_now == "06:55:00" or ph_time_now == "10:55:00" or ph_time_now == "14:55:00" or ph_time_now == "18:55:00" or ph_time_now == "22:55:00" or ph_time_now == "2:55:00":
  #  await bot.send_message(summer_fest_channel, "**Summer Festival** is about to start in **5 minutes**.\n\n `@go 0` and speak to the ferry man on the left to enter the event.")
  #  await bot.send_message(den_notif, "@here **Summer Festival** is about to start in **5 minutes**")
  #  print("---------- SUMMER FEST ------------")
  #  continue

  ## DECEMBER EVENT Snowball Fight ##
  if ph_time_now == "09:25:00" or ph_time_now == "15:25:00" or ph_time_now == "21:25:00" or ph_time_now == "03:25:00":
   snowball = await bot.send_message(main_chat, "**SNOWBALL FIGHT** in 5 minutes. :snowflake:")
   den_snowball = await bot.send_message(den_notif, "@here **SNOWBALL FIGHT** in 5 minutes. :snowflake:")
   network_snowball = await bot.send_message(network_notif, "@here **SNOWBALL FIGHT** in 5 minutes. :snowflake:")
   print("---------- BG HH notif ------------")
   continue

  ## start of the snowball fight
  if ph_time_now == "09:30:00" or ph_time_now == "15:30:00" or ph_time_now == "21:30:00" or ph_time_now == "03:30:00":
   await bot.edit_message(snowball, "**SNOWBALL FIGHT :snowflake:** is starting now!!") # edits the initial snowbll announcement message.
   await bot.edit_message(den_snowball, "**SNOWBALL FIGHT :snowflake:** is starting now!!") # edits the initial snowball announcement message.
   await bot.edit_message(network_snowball, "**SNOWBALL FIGHT :snowflake:** is starting now!!") # edits the initial snowball announcement message.
   print("---------- DECEMBER SNOWBALL FIGHT notif ------------")
   continue

  ## Battlegrounds HH Notification ##
  if ph_time_now == "10:00:00" or ph_time_now == "17:00:00" or ph_time_now == "22:00:00" or ph_time_now == "04:00:00":
   await bot.send_message(main_chat, "**Battlegrounds :crossed_swords:** has increased valor badge rewards.")
   await bot.send_message(den_notif, "@here **Battlegrounds :crossed_swords: increased rewards** is starting now.")
   await bot.send_message(network_notif, "@here **Battlegrounds :crossed_swords: increased rewards** is starting now.")
   print("---------- BG HH notif ------------")
   continue
  ## Monster Hunter HH Notification ##
  if ph_time_now == "07:55:00" or ph_time_now == "12:55:00" or ph_time_now == "18:55:00" or ph_time_now == "00:55:00":
   await bot.send_message(recruit_channel, "**Monster Hunter Happy Hour** is about to start in **5 minutes**.\nDon't forget to try the command of `-mh <type>`")
   await bot.send_message(den_notif, "@here **Monster Hunter Happy Hour** is about to start in **5 minutes**")
   await bot.send_message(network_notif, "@here **Monster Hunter Happy Hour** is about to start in **5 minutes**")
   print("---------- MH HH notif ------------")
   continue
  ## Slot Machine Notification ##
  if ph_time_now == "21:00:00" or ph_time_now == "09:00:00" or ph_time_now == "03:00:00" or ph_time_now == "15:00:00":
   before_slot = await bot.send_message(recruit_channel, "**Slot Machine :slot_machine:** is about to spawn in **5 minutes** at **Prontera (@go 0)**.\nSee list of rewards here: https://www.novaragnarok.com/wiki/Automated_Events")
   den_before_slot = await bot.send_message(den_notif, "@here **Slot Machine :slot_machine:** is about to spawn in **5 minutes** at **Prontera (@go 0)**")
   network_before_slot = await bot.send_message(network_notif, "@here **Slot Machine :slot_machine:** is about to spawn in **5 minutes** at **Prontera (@go 0)**")
   print("--------- BEFORE SLOT MACHINE notif ----------")
   continue

  if ph_time_now == "21:06:00" or ph_time_now == "09:06:00" or ph_time_now == "03:06:00" or ph_time_now == "15:06:00":
   await bot.edit_message(before_slot, "**Slot Machine :slot_machine:** has spawned in **Prontera (@go 0 )**.") # edits the initial slot machine announcement message.
   await bot.edit_message(den_before_slot, "**Slot Machine :slot_machine:** has spawned in **Prontera (@go 0 )**.") # edits the initial slot machine announcement message.
   await bot.edit_message(network_before_slot, "**Slot Machine :slot_machine:** has spawned in **Prontera (@go 0 )**.") # edits the initial slot machine announcement message.
   print("--------- SLOT MACHINE notif ----------")
   continue

@bot.event
async def on_member_remove(member):
    server = member.server
    yyd_server = "428458200174428160"
    ravaj_server = "377666970809794565"
    test_server = "430531932355559436"
    if server.id == yyd_server:
        # yyd_chat_archive = "456273106164514828"
        yyd_welcome_channel = "428458200174428162"
        for channel in server.channels:
            if yyd_welcome_channel == channel.id:
                await bot.send_message(channel, "**%s** has left Yummy Yummy Dumplings :sob:" % (member.name))
                break
    elif server.id == ravaj_server:
        ravaj_welcome_channel = "377668128487768065"
        for channel in server.channels:
            if ravaj_welcome_channel == channel.id:
                await bot.send_message(channel, "**%s** has left Ravage Discord :eyes:" % (member.name))
                break
    elif server.id == test_server:
        test_server_welcome = "431846217220227096"
        for channel in server.channels:
            if test_server_welcome == channel.id:
                await bot.send_message(channel, "**%s** has left the discord server :sob:" % (member.name))
                break

# when a new member joined.
@bot.event
async def on_member_join(member):
    print(member)
    server = member.server
    print("Server:"+server.id)
    yyd_server = "428458200174428160"
    test_server = "430531932355559436"
    if(server.id == yyd_server):
        yyd_welcome_channel = "428458200174428162"
        introduction_channel = "428469891289317377"
        roaches_id = "&450501364905148417"
        for channel in server.channels:
            if yyd_welcome_channel == channel.id:
                welcome_channel = channel
                for channel in server.channels:
                    if introduction_channel == channel.id:
                        intro_channel = channel
                        await bot.send_message(welcome_channel, "Hey <@%s>!\n<@%s> has joined our humble guild! Please set his/her role accordingly" % (roaches_id, member.id)) # replace andie with roaches_id
                        await bot.send_message(member, "Welcome to **Yummy Yummy Dumplings!**\n\n Please fill out a brief description about yourself in [introduction channel in YYD], your role will be added soon:tm: and also please add your name on our meme page here to help us know you and your guild members more!\n\n https://docs.google.com/document/d/1mtNN0FQDO7xTEVay5E-tYHjcwttt1Sb1RA5t4SykMOs/edit \n\n **Note:** \n ```Remember to type $yyd on #main```")
                        break
                break
    elif(server.id == test_server):
        test_server_welcome = "431846217220227096"
        guest_role = "431845670035521537"
        for channel in server.channels:
            print("Channels: %s" + channel.name)
            if test_server_welcome == channel.id:
                await bot.send_message(channel, "Our new recruit <@%s> has come! Calling <@%s>. Please set this lad's appropriate role while I enable him to Social." % (member.id, andie))
                break
        for role in server.roles:
            print("Roles:" + role.name)
            if guest_role == role.id:
                await bot.add_roles(member, role)
                await bot.send_message(member, "Hi")
                break
            # else:
            #     bot.send_message(test_server_welcome, "I can't set his/her role because your default role doesn't exist!")
    elif(server.id == elephants):
      hhe_welcome = "506340146929467404"
      for channel in server.channels:
        if hhe_welcome == channel.id:
          await bot.send_message(channel, "<@%s> has joined :elephant: group. Please wait for your role to be assigned :ok_hand:" % (member.id))
          break

    else:
        server_owner = server.owner
        server_name = server.name
        await bot.send_message(member, "Hi! We're glad you came! Please enjoy your stay to **%s**. Try to mention <@%s> from the server so the owner knows you're here. Thank you :smile:" % (server_name, server_owner.id))


@bot.event
async def on_message(message):
    if not message.author.bot:
        if message.content.startswith("eyyy"):
            await bot.send_message(message.channel, "Ayyyy!")
        elif message.content.startswith("ayyy"):
            await bot.send_message(message.channel, "Eyyy!")
        elif message.content.startswith("ayy"):
            await bot.send_message(message.channel, "Eyyy!")
        elif message.content.startswith("eyy"):
            await bot.send_message(message.channel, "Ayyy!")
        elif message.content.startswith(":j0y:"):
            await bot.send_message(message.channel, ":j0y:")
    
    await bot.process_commands(message)

    if message.content.lower() == "hi" or message.content.lower() == "hello" or message.content.lower() == "ola" or message.content.lower() == "halo" or message.content.lower() == "hola":
        await bot.send_message(message.channel, "Greetings to you too!")
    if message.content.lower() == "i love you":
        await bot.send_message(message.channel, "<@%s>, I love you too!" % (message.author.id))

@bot.event
async def on_message_delete(message):
    server = message.author.server
    member = message.author
    if not message.author.bot:
        yyd_server = "428458200174428160"
        ravaj_server = "377666970809794565"
        test_server = "430531932355559436"
        if server.id == test_server:
            audit_channel = "431846217220227096"
            for channel in server.channels:
                if channel.id == audit_channel:
                    await bot.send_message(channel, "**%s** deleted a chat from **%s** channel at **%s**:\n**Message:**\n%s" % (member.name, message.channel.name, message.timestamp.strftime("%B %d, %Y | %A"), message.content))
                    if len(message.attachments) > 0:
                        print(message.attachments)
                        await bot.send_message(channel, "\n\n```Attachments:```\n")
                        attachments = message.attachments
                        for attachment in attachments:
                            await bot.send_message(channel, "File name: %s | Size: %s bytes" % (attachment['filename'], attachment['size']))
                            await bot.send_message(channel, "Attachment from %s's message:\n" % (member.name))
                            await bot.send_message(channel, attachment['proxy_url'])
                            await bot.send_message(channel, "\n If this is a nude, ples delet.")
                            # embed = discord.Embed(title="Attachment from %s's message" % (member.name))
                            # embed.set_image(url=attachment['url'])
                            # embed.set_footer(text="If this is a nude, ples delet.")
                            # await bot.send_message(channel, embed=embed)
                    break
        elif server.id == yyd_server:
            audit_channel = "456273106164514828"
            for channel in server.channels:
                if channel.id == audit_channel:
                    await bot.send_message(channel, "**%s** deleted a chat from **%s** channel at **%s**:\n**Message:**\n%s" % (member.name, message.channel.name, message.timestamp.strftime("%B %d, %Y | %A"), message.content))
                    if len(message.attachments) > 0:
                        print(message.attachments)
                        await bot.send_message(channel, "\n\n```Attachments:```\n")
                        attachments = message.attachments
                        for attachment in attachments:
                            await bot.send_message(channel, "File name: %s | Size: %s bytes" % (attachment['filename'], attachment['size']))
                            await bot.send_message(channel, "Attachment from %s's message:\n" % (member.name))
                            await bot.send_message(channel, attachment['proxy_url'])
                            await bot.send_message(channel, "\n If this is a nude, ples delet.")
                            # embed = discord.Embed(title="Attachment from %s's message" % (member.name))
                            # embed.set_image(url=attachment['url'])
                            # embed.set_footer(text="If this is a nude, ples delet.")
                            # await bot.send_message(channel, embed=embed)
                    break

@bot.event
async def on_message_edit(before, after):
    message = before
    server = before.author.server
    member = before.author
    if not message.author.bot:
        yyd_server = "428458200174428160"
        ravaj_server = "377666970809794565"
        test_server = "430531932355559436"
        if server.id == test_server:
            audit_channel = "431846217220227096"
            for channel in server.channels:
                if channel.id == audit_channel:
                    await bot.send_message(channel, "**%s** edited a chat from **%s** channel at **%s**:\n**Original Message:**\n%s \n\n **Edited Message:**\n%s" % (member.name, message.channel.name, message.timestamp.strftime("%B %d, %Y | %A"), before.content, after.content))
                    if len(message.attachments) > 0:
                        print(message.attachments)
                        await bot.send_message(channel, "\n\n```Attachments:```\n")
                        attachments = message.attachments
                        for attachment in attachments:
                            await bot.send_message(channel, "File name: %s | Size: %s bytes" % (attachment['filename'], attachment['size']))
                            await bot.send_message(channel, "Attachment from %s's message:\n" % (member.name))
                            await bot.send_message(channel, attachment['proxy_url'])
                            await bot.send_message(channel, "\n If this is a nude, ples delet.")
                            # embed = discord.Embed(title="Attachment from %s's message" % (member.name))
                            # embed.set_image(url=attachment['url'])
                            # embed.set_footer(text="If this is a nude, ples delet.")
                            # await bot.send_message(channel, embed=embed)
                    break
        elif server.id == yyd_server:
            audit_channel = "456273106164514828"
            for channel in server.channels:
                if channel.id == audit_channel:
                    await bot.send_message(channel, "**%s** edited a chat from **%s** channel at **%s**:\n**Original Message:**\n%s \n\n **Edited Message:**\n%s" % (member.name, message.channel.name, message.timestamp.strftime("%B %d, %Y | %A"), before.content, after.content))
                    if len(message.attachments) > 0:
                        print(message.attachments)
                        await bot.send_message(channel, "\n\n```Attachments:```\n")
                        attachments = message.attachments
                        for attachment in attachments:
                            await bot.send_message(channel, "File name: %s | Size: %s bytes" % (attachment['filename'], attachment['size']))
                            await bot.send_message(channel, "Attachment from %s's message:\n" % (member.name))
                            await bot.send_message(channel, attachment['proxy_url'])
                            await bot.send_message(channel, "\n If this is a nude, ples delet.")
                            # embed = discord.Embed(title="Attachment from %s's message" % (member.name))
                            # embed.set_image(url=attachment['url'])
                            # embed.set_footer(text="If this is a nude, ples delet.")
                            # await bot.send_message(channel, embed=embed)
                    break

@bot.event
async def on_member_update(before, after):
    member = after
    server = member.server
    game = member.game
    chat_channel = "428465462096166918"
    yyd_server = "428458200174428160"
    elephants = "506332548247584778" # korea's and oli's woe guild
    elephants_stream = "506344690765922314"
    if game:
     if game.type == 1 and not member.bot:
         if server.id == yyd_server:
             for channel in server.channels:
                 if (channel.id == chat_channel and not interval):
                     await bot.send_message(channel, "```STREAM ALERT:```\n**%s** is streaming **%s** now at %s\n\n*Don't forget to follow though* :smirk:" % (member.name, game.name, game.url))
                     setInterval(toggleInterval, timeInterval)
                     break

         if server.id == elephants:
             for channel in server.channels:
                 if channel.id == elephants_stream and not interval:
                     await bot.send_message(channel, "```STREAM ALERT:```\n**%s** is streaming **%s** now at %s\n\n*Don't forget to follow and add to your friends server!* :wink:" % (member.name, game.name, game.url))
                     setInterval(toggleInterval, timeInterval)
                     break

init_extensions = ["misc", "member", "familyfriendly"]
if __name__ == "__main__":
 for extension in init_extensions:
  try:
   bot.load_extension(extension)
  except Exception as e:
   print("Failed to load extension {extension}.", file=sys.stderr)
   traceback.print_exc()


# @bot.command(pass_context=True)
# async def events(ctx):
#  await bot.send_message(ctx.message.channel, "Automated Event Notification commenced!")
#  format = "%H:%M:%S"
#  for server in bot.servers:
#   if server.id == yyd_server:
#    yyd = server
#    break
#  for channel in yyd.channels:
#   if channel.id == yyd_recruit_channel:
#    recruit_channel = channel
#    continue
#   if channel.id == yyd_bg_channel:
#    bg_channel = channel
#    continue
#   if channel.id == yyd_summer_fest_channel:
#    summer_fest_channel = channel
#    continue

#  while True:
#   ph_time = timezone('Asia/Manila')
#   ph_location = ph_time.normalize(ph_time.localize(datetime.now() + timedelta(hours=8)))
#   ph_time_now = ph_location.strftime(format)
#   await asyncio.sleep(1)
#   # Summer event Notification ##
#   if ph_time_now == "06:55:00" or ph_time_now == "10:55:00" or ph_time_now == "14:55:00" or ph_time_now == "18:55:00" or ph_time_now == "22:55:00" or ph_time_now == "2:55:00":
#    await bot.send_message(summer_fest_channel, "@here **Summer Festival** is about to start in **5 minutes**.\n*If you don't wanna be notified you can supress the notification on the server's settings or ask the Leaders to remove you from notifs.*")
#    print("---------- SUMMER FEST ------------")
#    continue
#   ## Battlegrounds HH Notification ##
#   if ph_time_now == "09:00:00" or ph_time_now == "16:00:00" or ph_time_now == "21:00:00" or ph_time_now == "03:00:00":
#    await bot.send_message(bg_channel, "@here **Battlegrounds Happy Hour** is starting now, bitches.\n*If you don't wanna be notified you can supress the notification on the server's settings or ask the Leaders to remove you from notifs.*")
#    print("---------- BG HH notif ------------")
#    continue
#   ## Monster Hunter HH Notification ##
#   if ph_time_now == "06:55:00" or ph_time_now == "12:55:00" or ph_time_now == "17:55:00" or ph_time_now == "23:55:00":
#    await bot.send_message(recruit_channel, "@here **Monster Hunter Happy Hour** is about to start in **5 minutes**.\n*If you don't wanna be notified you can supress the notification on the server's settings or ask the Leaders to remove you from notifs.*")
#    print("---------- MH HH notif ------------")
#    continue
#   # print(ph_time_now)



bot.run(localToken, bot=True, reconnect=True) # danger zone
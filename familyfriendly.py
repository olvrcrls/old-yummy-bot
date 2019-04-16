import discord, asyncio, random, requests, json, time, os, subprocess
from discord.ext import commands
from discord.ext.commands import Bot
# dedicated to Family Friendly : SERVER ID : 428458200174428160
# spreadsheet things
from oauth2client import file as oauth_file, client, tools
from apiclient.discovery import build
from httplib2 import Http
from yummy_token import friendly_spreadsheet_id, friendly_woe_spreadsheet


yyd_server = "428458200174428160"
woe_channel = "537027193834831887"

# Constants
name_range = 'B2:B50'
class_range = 'C2:C50'
attendance_range = 'D2:D50'
spreadsheet_range = 'A2:D50'
value_input_option = 'USER_ENTERED'
sanoshi = "130186870742056960"
andie = "291146480927113218"
azn = "135908154692206595"

spreadsheetId = friendly_spreadsheet_id
store = oauth_file.Storage('token.json')
credentials = store.get()
read_credentials = credentials
READ_SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly' # for read
SCOPES = 'https://www.googleapis.com/auth/spreadsheets' # for other purposes
CREDENTIAL_FILE = "friendly.json"

if not credentials or credentials.invalid:
 flow = client.flow_from_clientsecrets(CREDENTIAL_FILE, SCOPES)
 credentials = tools.run_flow(flow, store)

 read_flow = client.flow_from_clientsecrets(CREDENTIAL_FILE, READ_SCOPES)
 read_credentials = tools.run_flow(flow, store)

service = build('sheets', 'v4', http=credentials.authorize(Http()))
read_service = build('sheets', 'v4', http=read_credentials.authorize(Http()))


class FriendlyCog:
 def __init__(self, bot):
  self.bot = bot

 # set attendance without putting your name.
 @commands.command(pass_context=True)
 async def att(self, ctx, *, response : str):
   sender = ctx.message.author
   response = response.lower()
   user = sender.name
   nickname = sender.display_name

   if(ctx.message.channel.id == woe_channel):
    if (response == 'yes' or response == 'no' or response == 'maybe' or response == '50/50'):
     names = self.result_name_spreadsheet(name_range)
     # attendance cell : cell_name + cell_number
     cell_name = "D"
     cell_number = 2
     finding_msg = await self.bot.send_message(ctx.message.channel, "Finding...")
     found = False
     for name in names:
      if ((user.lower() == name[0].lower()) or (nickname.lower() == name[0].lower())):
       print("Cell:" + str(cell_number))
       found = True
       break
      else:
       cell_number += 1
       print(cell_number)
     if (found):
      await self.bot.delete_message(finding_msg)
      thumbs_up_msg = await self.bot.send_message(ctx.message.channel, ":+1:")
      cell = cell_name + str(cell_number)
      values = {
       "values" : [[response.capitalize()]]
      }
      try:
       service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=cell, valueInputOption=value_input_option, body=values).execute()
       await self.bot.delete_message(thumbs_up_msg)
       await self.bot.send_message(ctx.message.channel, "<@%s>, **%s** your attendance has been successfully updated." % (sender.id, user))
      except Exception as e:
       print(e)
       await self.bot.send_message(ctx.message.channel, "Failed to update attendance. <@%s>" % (andie))
     else:
      await self.bot.send_message(ctx.message.channel, '<@%s>, %s is not found. Try to check if it matches his/her discord name or nickname on this server.' % (sender.id, user))

    else:
     await self.bot.send_message(ctx.message.channel, "<@%s>, bitch, your response is not correct. Only yes or no or maybe." % (sender.id))
   else:
    await self.bot.send_message(ctx.message.channel, "Unauthorized Channel. Exclusive for FamILY FrieNDLy WoE memebers.")

  # set attendance.
 @commands.command(pass_context=True)
 async def setatt(self, ctx, user : str, response : str):
   sender = ctx.message.author
   response = response.lower()
   found = False
   if not user.strip():
    user = sender.name
   if(ctx.message.channel.id == woe_channel):
    if (response == 'yes' or response == 'no' or response == 'maybe' or response == '50/50'):
     names = self.result_name_spreadsheet(name_range)
     # attendance cell : cell_name + cell_number
     cell_name = "D"
     cell_number = 2
     finding_msg = await self.bot.send_message(ctx.message.channel, "Finding...")
     for name in names:
      if (user.lower() == name[0].lower()):
       print("Cell:" + str(cell_number))
       found = True
       break
      else:
       cell_number += 1
       print(cell_number)
     if (found):
      await self.bot.delete_message(finding_msg)
      thumbs_up_msg = await self.bot.send_message(ctx.message.channel, ":+1:")
      cell = cell_name + str(cell_number)
      values = {
       "values" : [[response.capitalize()]]
      }
      try:
       service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=cell, valueInputOption=value_input_option, body=values).execute()
       await self.bot.delete_message(thumbs_up_msg)
       await self.bot.send_message(ctx.message.channel, "<@%s>, **%s**'s attendance has been successfully updated." % (sender.id, user))
      except Exception as e:
       print(e)
       await self.bot.send_message(ctx.message.channel, "Failed to update attendance. <@%s>" % (andie))
     else:
      await self.bot.send_message(ctx.message.channel, '<@%s>, **%s** is not found.  Try to check if it matches his/her discord name or nickname on this server.' % (sender.id, user))

    else:
     await self.bot.send_message(ctx.message.channel, "<@%s> bitch your response is not correct. Only yes or no or maybe." % (sender.id))
   else:
    await self.bot.send_message(ctx.message.channel, "Unauthorized Channel. Exclusively for FamILY FrieNDLy WoE memebers.")

  # reset attendance
 @commands.command(pass_context=True)
 async def reset(self, ctx):
   sender = ctx.message.author
   channel = ctx.message.channel
   if channel.id == woe_channel:
    if sender.id == sanoshi or sender.id == andie or sender.id == azn:
     counter = 0
     total = 26
     values = { "values" : [[""]] }
     try:
      reset_msg = await self.bot.send_message(channel, "Resetting attendance...")
      number = 2 # starting range
      cell = "D"
      while counter < total:
       cell_number = cell + str(number)
       result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=cell_number, valueInputOption=value_input_option, body=values).execute()
       counter += 1
       number += 1
      await self.bot.send_message(channel, "Successful reset. Please chill out for like 5 minutes, I'm pooped on sniffing your excel sheet.")
     except Exception as e:
      print(e)
      await self.bot.send_message(channel, "Failed to reset attendance. <@%s>" % (andie))
     finally:
      await self.bot.delete_message(reset_msg)
    else:
     await self.bot.send_message(channel, "Unauthorized! Only for Sanoshi, Azn, and Andie")
   else:
    await self.bot.send_message(ctx.message.channel, "Unauthorized Channel. Exclusive only for FamILY FrieNDLy WoE memebers.")

 # set job without putting your name.
 @commands.command(pass_context=True)
 async def job(self, ctx, *, response : str):
   sender = ctx.message.author
   response = response.capitalize()
   user = sender.name
   nickname = sender.display_name

   if(ctx.message.channel.id == woe_channel):
     names = self.result_name_spreadsheet(name_range)
     # attendance cell : cell_name + cell_number
     cell_name = "B"
     cell_number = 21
     finding_msg = await self.bot.send_message(ctx.message.channel, "Finding...")
     for name in names:
      if ((user.lower() == name[0].lower()) or (nickname.lower() == name[0].lower())):
       print("Cell:" + str(cell_number))
       found = True
       break
      else:
       cell_number += 1
       print(cell_number)
     if (found):
      await self.bot.delete_message(finding_msg)
      thumbs_up_msg = await self.bot.send_message(ctx.message.channel, ":+1:")
      cell = cell_name + str(cell_number)
      values = {
       "values" : [[response.capitalize()]]
      }
      try:
       service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=cell, valueInputOption=value_input_option, body=values).execute()
       await self.bot.delete_message(thumbs_up_msg)
       await self.bot.send_message(ctx.message.channel, "<@%s>, **%s** your class job has been successfully updated." % (sender.id, user))
      except Exception as e:
       print(e)
       await self.bot.send_message(ctx.message.channel, "Failed to update. <@%s>" % (andie))
     else:
      await self.bot.send_message(ctx.message.channel, '<@%s>, %s is not found. Try to check if it matches his/her discord name or nickname on this server.' % (sender.id, user))
   else:
    await self.bot.send_message(ctx.message.channel, "Unauthorized Channel. Exclusive for FamILY FrieNDLy WoE memebers.")


  # set job.
 @commands.command(pass_context=True)
 async def setjob(self, ctx, user : str, response : str):
   sender = ctx.message.author
   response = response.capitalize()
   found = False
   if not user.strip():
    user = sender.name
   if(ctx.message.channel.id == woe_channel):
     names = self.result_name_spreadsheet(name_range)
     # attendance cell : cell_name + cell_number
     cell_name = "C"
     cell_number = 2
     finding_msg = await self.bot.send_message(ctx.message.channel, "Finding...")
     for name in names:
      if (user.lower() == name[0].lower()):
       print("Cell:" + str(cell_number))
       found = True
       break
      else:
       cell_number += 1
       print(cell_number)
     if (found):
      await self.bot.delete_message(finding_msg)
      thumbs_up_msg = await self.bot.send_message(ctx.message.channel, ":+1:")
      cell = cell_name + str(cell_number)
      
      values = {
       "values" : [[response.capitalize()]]
      }
      try:
       service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=cell, valueInputOption=value_input_option, body=values).execute()
       await self.bot.delete_message(thumbs_up_msg)
       await self.bot.send_message(ctx.message.channel, "<@%s>, **%s**'s class job has been successfully updated." % (sender.id, user))
      except Exception as e:
       print(e)
       await self.bot.send_message(ctx.message.channel, "Failed to update attendance. <@%s>" % (andie))
     else:
      await self.bot.send_message(ctx.message.channel, '<@%s>, **%s** is not found.  Try to check if it matches his/her discord name or nickname on this server.' % (sender.id, user))
   else:
    await self.bot.send_message(ctx.message.channel, "Unauthorized Channel. Exclusively for FamILY FrieNDLy WoE memebers.")


  # added private methods
 def result_name_spreadsheet(self, val : str):
   result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=val).execute()
   return result.get('values', [])
   # return result

 def result_spreadsheet(self):
   result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=spreadsheet_range).execute()
   # return result
   return result.get('values', [])


def setup(bot):
 bot.add_cog(FriendlyCog(bot))
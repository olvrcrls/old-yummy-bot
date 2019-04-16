import discord, asyncio, random, requests, json, time, os, subprocess
from discord.ext import commands
from discord.ext.commands import Bot
from pyquery import PyQuery
from lxml import html
from bs4 import BeautifulSoup
from urllib.parse import quote
from yummy_token import novaUsername, novaPassword, translate_token

andie = "291146480927113218" # in case people will abuse me. shit cunts.
session_requests = requests.session()
class MemberCog:
 def __init__(self, bot):
  self.bot = bot

 async def on_ready(self):
  payload = {"username": novaUsername, "password": novaPassword,"server":"NovaRO"}
  url = "https://www.novaragnarok.com/?module=account&action=login&return_url="
  result = session_requests.get(url)
  tree = html.fromstring(result.text)
  authenticity_token = list(set(tree.xpath("//input[@name='server']/@value")))[0]
  result = session_requests.post(url, data = payload, headers = dict(referer=url))
     # print(result.status_code, result.reason) # checking if NovaRO website is on
  if(result.status_code == 200):
   print("STATUS 200: NovaRO Website is ON")
  else:
   print("NovaRO Website is DOWN")
  url = "https://www.novaragnarok.com/?module=vending"
  result = session_requests.get(url, headers = dict(referer = url))
     # print(result.status_code, result.reason) # checking if the NovaRO market page is on.
  if(result.status_code == 200):
   print("STATUS 200: NovaRO Market's Website is ON")
  else:
   print("NovaRO Market's Website is DOWN")
 @commands.command(pass_context=True)
 async def hi(self, ctx):
  sender = ctx.message.author
  await self.bot.say("Hi %s" % (sender.name))

 @commands.command(pass_context=True)
 async def gay(self, ctx, *, member: discord.Member):
  message = ctx.message
  if member.id == andie:
   await self.bot.say("No! <@%s> you are the gay one :joy: \n\n Also this guy: \n https://media.discordapp.net/attachments/428465462096166918/445218800867213312/Screenshot_20170406-065024.jpg" % (ctx.message.author.id))
  else:
   await self.bot.delete_message(message)
   await self.bot.say("<@%s> is gay :peach: :wave: :joy:"  % (member.id))

 # NovaRO Character card.
 @commands.command(pass_context=True)
 async def sig(self, ctx, *, name: str):
     sender = ctx.message.author
     urlName = quote(name)
     background = random.randint(1,11)
     pose = random.randint(0,14)
     url = "https://www.novaragnarok.com/ROChargenPHP/newsig/%s/%d/%d" % (urlName, background, pose)
     thumbnail_url = "https://www.novaragnarok.com/themes/nova/img/img/logo_new_.png"
     embed = discord.Embed(title="NovaRO Character", description="%s's Character Card." % (name.title()))
     embed.set_thumbnail(url=thumbnail_url)
     embed.set_image(url=url)
     await self.bot.send_message(ctx.message.channel, "<@%s>" % sender.id, embed=embed)

 # NovaRO character head.
 @commands.command(pass_context=True)
 async def charhead(self, ctx, *, name: str):
     sender = ctx.message.author
     urlName = quote(name)
     url = "https://www.novaragnarok.com/ROChargenPHP/characterhead/%s" % (urlName)
     thumbnail_url = "https://www.novaragnarok.com/themes/nova/img/img/logo_new_.png"
     embed = discord.Embed(title="NovaRO Character", description="%s's Character Head." % (name))
     embed.set_thumbnail(url=thumbnail_url)
     embed.set_image(url=url)
     await self.bot.send_message(ctx.message.channel, "<@%s>" % sender.id, embed=embed)

 # NovaRO character sprite.
 @commands.command(pass_context=True)
 async def char(self, ctx, *, name: str):
     sender = ctx.message.author
     urlName = quote(name)
     url = "https://www.novaragnarok.com/ROChargenPHP/character/"
     thumbnail_url = "https://www.novaragnarok.com/themes/nova/img/img/logo_new_.png"
     urlStand = url+"%s/0/1" % (urlName)
     embed = discord.Embed(title="NovaRO Character", description="%s's Character Sprite." % (name))
     embed.set_thumbnail(url=thumbnail_url)
     embed.set_image(url=urlStand)
     await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)


 # RNG choose on provided options/choices
 @commands.command(pass_context=True)
 async def choose(self, ctx, *choices: str):
     sender = ctx.message.author
     try:
         await self.bot.say("<@%s>, I choose **%s** for you :thumbsup:" % (sender.id, random.choice(choices)))
     except Exception as e:
         print(e)
         await self.bot.say("<@%s> please enter some choices that I can choose from!" % (sender.id))
 
 # Ping/poke someone without knowing it's you.
 @commands.command(pass_context=True)
 async def poke(self, ctx, *, member: discord.User):
     message = ctx.message
     if member.id == andie:
         await self.bot.delete_message(ctx.message)
         await self.bot.say("You can't ping this person, duck :yum:")
     else:
         await self.bot.delete_message(ctx.message)
         await self.bot.say("<@%s>! Someone has poked you :yum:" % (member.id))

 # dice game.
 @commands.command(pass_context=True)
 async def dice(self, ctx):
     values = [1,2,3,4,5,6,6,5,4,3,2,1]
     rolledValue = random.choice(values)
     embed = discord.Embed(title="You rolled **%d** :game_die:" % (rolledValue))
     await self.bot.send_message(ctx.message.channel, embed=embed)

 # NovaRO RMS
 @commands.command(pass_context=True)
 async def rms(self, ctx):
     sender = ctx.message.author
     rmsImageURL = "https://images-ext-2.discordapp.net/external/SPJMmbZtazzssxwqT4WD8vbKDCJNSOpvH91ZfGadrqk/https/www.novaragnarok.com/images/rms2.png?width=540&height=309"
     embed = discord.Embed(description="Remember to review us on RMS and invite your friends to the server! Click here: http://ratemyserver.net/index.php?page=writereview&serid=17776&url_sname=NovaRO")
     embed.set_image(url=rmsImageURL)
     await self.bot.send_message(ctx.message.channel, embed=embed)

 # Asking the self.bot a question and returns a random answer to the question.
 @commands.command(pass_context=True)
 async def ask(self, ctx):
     sender = ctx.message.author

     # questions if the user didn't ask anything.
     questions = ["What's up?", "Waddup, fam?", "Ask away!", "Anything you want to know?", "Ask something",
                 "Dude, ask something. I don't have all time.", "What? Yes, Ash is gay.", "???", "What?",
                 "Hello. Can I help you?", "Nani?", "rAvAj", "?!", "Hi.", "Yes?", "What is it?", "Do you need help on something?",
                 "Try following up the command with a question :sweat_smile:", "Hello Sir/Ma'am"
                 ]

     # responses if there is a question being asked by the user.
     responses = ["Might be.", "Yes, of course", "There is certainty to that", "I don't know about that, maybe?",
                  "Of course, no :joy:", "I think that's the case", "Haha, yes it is. If you know what I mean :smirk:",
                  "Ask me again about this, please :sweat_smile:", "Probably, not", "Probably, yes", "Try again.",
                  "Absolutely", "I think yes, what you think?", "I think no, what you think?", "Follow your heart :heart:",
                  "Whatever your guts is saying", "Stop. Let me think and ask again.", "It's you.", "Maybe it's them.", "Oh no, I don't know. Sorry!",
                  "Yes", "No", "Yeah", "Nah", "Maybe", "I don't think so.", "It's not possible", "That's quite not right, I think no.",
                  "Nothing's impossible, yes!", "I think so too."
                 ]
     if ctx.message.content == "$ask":
         answer = random.choice(questions)
         await self.bot.say("<@%s> %s" % (sender.id, answer))
     else:
         answer = random.choice(responses)
         await self.bot.say("<@%s> %s" % (sender.id, answer))


 @commands.command(pass_context=True)
 async def market(self, ctx, *, item=""):
     sender = ctx.message.author
     title = ""
     param = "DP"
     if item.startswith('dp'.upper()) or item.startswith('ap'.upper()) or item.startswith('dr'.upper()) or item.startswith('ar'.upper()):
      param = item[:2]
      item = item[3:]

     if (param.upper() == "AP" or param.upper() == "DP" or param.upper() == "AR" or param.upper() == "DR" or param.upper() == "" or param.upper() == None):
         await self.bot.send_message(ctx.message.channel, "`This command has known bugs. I will fix it when free.` - **Andie#4170**")
         if param.upper() == "AP":
             param = "&price_order=asc"
             title = " - Ascending Price"
         if param.upper() == "DP":
             param = "&price_order=desc"
             title = " - Descending Price"
         if param.upper() == "AR":
             param = "&price_order=none&refine_order=asc"
             title = " - Ascending Refinement"
         if param.upper() == "DR":
             param = "&price_order=none&refine_order=desc"
             title = " - Descending Refinement"
         itemURL = item.replace(" ", "+")
         url = "https://www.novaragnarok.com/?module=item&action=index&name="+itemURL+"&type=-1"
         kroItemURL = "https://www.novaragnarok.com/data/kRO/inventory/"
         result = session_requests.get(url, headers = dict(referer = url))
         content = result.text
         bSoup = BeautifulSoup(content, 'lxml')
         table = bSoup.find("table", attrs={"class":"nova-table"})
         itemIDs = []
         ctr = 1
         flag = 0
         flag_counter = 1
         if table is None:
             embed = discord.Embed(title="NovaRO Market Error", description="Item **%s** is not found" % (item.capitalize()))
             await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)
         else:
             for row in table.find_all("tr"):
                 for column in table.find_all("td"):
                     dataset = column.get_text()
                     if ctr == 1:
                         for flag in dataset.split():
                             if flag.isdigit():
                                 if len(itemIDs) > 0:
                                     if flag != itemIDs[flag_counter - 1]:
                                         itemIDs.append(flag)
                                 elif len(itemIDs) == 0:
                                     itemIDs.append(flag)
                                 flag_counter += 1
                         ctr += 1
                 ctr = 1
                 flag_counter = 1
             vendingURL = "https://www.novaragnarok.com/?module=vending&action=item&id="
             for itemID in itemIDs:
                 result = session_requests.get(vendingURL+itemID+param, headers = dict(referer = vendingURL+itemID+param))
                 content = result.text
                 contentLow = content.lower()
                 itemLower = item.lower()
                 start_range = contentLow.find(itemLower)
                 end_range = 0
                 for index in range(start_range, len(content)):
                     if content[index] == "<":
                         end_range = index
                         break
                 for index2 in range(start_range, 0, -1):
                     if content[index2] == ">":
                         start_range = index2+1
                         break
                 objName = content[start_range:end_range]
                 marketHist1 = ""
                 marketHist2 = ""
                 marketHist3 = ""
                 marketHist4 = ""
                 marketHist5 = ""
                 marketHist6 = ""
                 marketLive1 = ""
                 marketLive2 = ""
                 marketLive3 = ""
                 marketLive4 = "" #vending location
                 sold = True
                 selling = True
                 sellingObj = False
                 bSoup = BeautifulSoup(content, 'lxml')
                 table_list = []
                 table_list = bSoup.find_all("table", attrs={"class":"nova-table"})
                 if len(table_list) > 0:
                     item_counter = 1
                     for row in table_list[0].find_all("tr")[1:]:
                         item_counter_str = "**["+str(item_counter)+"]**" + " "
                         columns = row.find_all("td")
                         if len(columns) == 4:
                             sellingObj = True
                             marketLive1 = marketLive1 + item_counter_str + columns[0].get_text().strip() + "\n"
                             marketLive2 = marketLive2 + columns[1].get_text().strip() + "\n"
                             if (len(columns[2].get_text()) > 25):
                                 columns[2] = (columns[2][:25].get_text() + "...")
                             marketLive3 = marketLive3 + item_counter_str + columns[2].get_text().strip() + "\n"
                            
                         else:
                             if len(columns) == 5:
                                 sellingObj = True
                                 marketLive1 = marketLive1 + item_counter_str + columns[1].get_text().strip() + "\n"
                                 marketLive2 = marketLive2 + columns[2].get_text().strip() + "\n"
                                 if (len(columns[2].get_text()) > 25):
                                     columns[2] = (columns[2][:25].get_text() + "...")
                                 marketLive3 = marketLive3 + item_counter_str + columns[3].get_text().strip() + "\n"
                                 
                             else:
                                 marketHist1 = marketHist1 + columns[0].get_text().strip() + "\n"
                                 marketHist2 = marketHist2 + columns[1].get_text().strip() + "\n"
                                 marketHist3 = marketHist3 + columns[2].get_text().strip() + "\n"
                                 marketHist4 = marketHist4 + columns[3].get_text().strip() + "\n"
                                 marketHist5 = marketHist5 + columns[4].get_text().strip() + "\n"
                                 marketHist6 = marketHist6 + columns[5].get_text().strip() + "\n"
                         item_counter += 1

                     if len(table_list) > 1:
                         item_counter = 1
                         for row in table_list[1].find_all("tr")[1:]:
                             item_counter_str = "**["+str(item_counter)+"]**" + " "
                             columns2 = row.find_all("td")
                             if len(columns2) == 3:
                                 marketLive1 = marketLive1 + item_counter_str + columns2[0].get_text().strip() + "\n"
                                 marketLive2 = marketLive2 + columns2[1].get_text().strip() + "\n"
                                 marketLive4 = marketLive4 + item_counter_str + columns2[2].get_text().strip() + "\n"

                             elif len(columns2) == 4:
                                 marketLive1 = marketLive1 + item_counter_str + columns2[0].get_text().strip() + "\n"
                                 marketLive2 = marketLive2 + columns2[1].get_text().strip() + "\n"
                                 if (len(columns[2].get_text()) > 25):
                                     columns[2] = (columns[2][:25].get_text() + "...")
                                 marketLive3 = marketLive3 + item_counter_str + columns2[2].get_text().strip() + "\n"
                                 marketLive4 = marketLive4 + item_counter_str + columns2[3].get_text().strip() + "\n"

                             elif len(columns2) == 5:
                                 marketLive1 = marketLive1 + columns2[1].get_text().strip() + "\n"
                                 marketLive2 = marketLive2 + columns2[2].get_text().strip() + "\n"
                                 if (len(columns[2].get_text()) > 25):
                                     columns[2] = (columns[2][:25].get_text() + "...")
                                 marketLive3 = marketLive3 + item_counter_str + columns2[3].get_text().strip() + "\n"
                             item_counter += 1

                     else:
                         if not sellingObj:
                             selling = False
                 else:
                     sold = False;
                 if sold:
                  print(len(marketLive1+marketLive2+marketLive3+marketLive4))
                 if not sellingObj:
                     embed = discord.Embed(title="NovaRO Market History " + title, descripton=objName + " - ID: %s" % (itemID))
                     embed.set_thumbnail(url=kroItemURL+"%s.png" % (itemID))
                     embed.add_field(name="/", value=marketHist1, inline=True)
                     embed.add_field(name="#", value=marketHist2, inline=True)
                     embed.add_field(name="MIN", value=marketHist3, inline=True)
                     embed.add_field(name="MAX", value=marketHist4, inline=True)
                     embed.add_field(name="AVG.", value=marketHist5, inline=True)
                     embed.add_field(name="Std. Deviation", value=marketHist6, inline=True)
                     await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)

                 else:
                     embed = discord.Embed(title="NovaRO Market History " + title, descripton=objName + " - ID: %s" %(itemID))
                     embed.set_thumbnail(url=kroItemURL+"%s.png" % (itemID))
                     embed.add_field(name="The item has no market history", value="_", inline=True)
                     await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)

                 if selling:
                     if marketLive3 != "":
                             embed2 = discord.Embed(title="NovaRO Live Market " + title, descripton=objName + " - ID: %s" %(itemID))
                             embed2.set_thumbnail(url=kroItemURL+"%s.png" % (itemID))
                             embed2.add_field(name="Price", value=marketLive1, inline=True)
                             embed2.add_field(name="Refine", value=marketLive2, inline=True)
                             embed2.add_field(name="Additional Properties", value=marketLive3, inline=True)
                             embed2.add_field(name="Vending Area", value=marketLive4, inline=True)
                             await self.bot.send_message(ctx.message.channel, embed=embed2)
                         
                     else:
                         embed2 = discord.Embed(title="NovaRO Live Market " + title, descripton=objName + " - ID: %s" % (itemID))
                         embed2.set_thumbnail(url=kroItemURL+"%s.png" % (itemID))
                         embed2.add_field(name="Price", value=marketLive1, inline=True)
                         embed2.add_field(name="Qty.", value=marketLive2, inline=True)
                         embed2.add_field(name="Vending Area", value=marketLive4, inline=True)
                         await self.bot.send_message(ctx.message.channel, embed=embed2)
                         
                 else:
                     embed2 = discord.Embed(title="NovaRO Live Market " + title, descripton=objName + " - ID: %s" %(itemID))
                     embed2.set_thumbnail(url=kroItemURL+"%s.png" % (itemID))
                     embed2.add_field(name="No one's selling this right now", value="_", inline=True)
                     await self.bot.send_message(ctx.message.channel, embed=embed2)
             else:
                 embed = discord.Embed(title="NovaRO History Market " + title, descripton=objName + " - ID: %s" %(itemID))
                 embed.set_thumbnail(url=kroItemURL+"%s.png" % (itemID))
                 embed.add_field(name="The item has never been sold, yet.", value="_", inline=True)
                 await self.bot.send_message(ctx.message.channel, embed=embed)

     else: # if a wrong parameter has been provided by the user.
         embed = discord.Embed(title="NovaRO Market", description="Incorrect Parameter. Try the following:")
         embed.add_field(name="AP", value="Ascending Price", inline=True)
         embed.add_field(name="DP", value="Descending Price", inline=False)
         embed.add_field(name="AR", value="Ascending Refinement", inline=False)
         embed.add_field(name="DR", value="Descending Refinement", inline=False)
         await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)
         await self.bot.send_message(ctx.message.channel, "The command is changed. Try: `<AP/DP/AR/DR> <itemname>` like `DR heroic backpack`" % (sender.id))

 @commands.command(pass_context=True)
 async def memes(self, ctx, param=""):
     sender = ctx.message.author
     memeImages = ["https://imgur.com/a/pkfSw", "https://imgur.com/a/R22W2", "https://imgur.com/FqIi4XD",
                "https://imgur.com/SJgLl4p", "https://imgur.com/d7jAH3f", "https://imgur.com/yH0Khtx",
                "https://imgur.com/sWNKCrY", "https://imgur.com/kxmpPJW", "https://imgur.com/YKjlKZY",
                "https://gyazo.com/20f19c365ad2c264706c032dea559bdf.gif", "https://imgur.com/Bxy4usz",
                "https://imgur.com/78ttCEG", "https://imgur.com/7uRLfjN", "https://imgur.com/Cb4XZvB",
                "https://imgur.com/G0f3Bmg", "https://imgur.com/tTgcYpc", "https://imgur.com/FSF42Zj",
                "https://imgur.com/2MZxr1d", "https://imgur.com/WQX7Kd2", "https://imgur.com/0sykhjb",
                "https://imgur.com/VW0mYL3", "https://imgur.com/XL6Ik9o", "https://media.discordapp.net/attachments/431947714511634432/431947966052433940/aot.PNG?width=330&height=500",
                "https://media.discordapp.net/attachments/431947714511634432/431974743319511050/unknown.png",
                "https://media.discordapp.net/attachments/435744130623340545/435748581702369280/unknown.png?width=442&height=485",
                "https://media.discordapp.net/attachments/431947714511634432/432031226392608768/shirtimage-13.png",
                "https://media.discordapp.net/attachments/431947714511634432/432031243933188097/unknown.png",
                "https://media.discordapp.net/attachments/431947714511634432/432033436526444544/unknown.png",
                "https://media.discordapp.net/attachments/431947714511634432/432385005537329153/unknown.png",
                "https://media.discordapp.net/attachments/431947714511634432/432391290034847744/unknown.png",
                "https://clips.twitch.tv/JollySecretiveMooseHotPokket \n https://puu.sh/zO9PJ/462f30987b.png",
                "https://imgur.com/a/Q8rIR", "https://imgur.com/a/8oULW",
                "https://cdn.discordapp.com/attachments/428465462096166918/432004530138513411/unknown.png?width=341&height=421",
                "https://cdn.discordapp.com/attachments/431947714511634432/432391552988479488/unknown.png",
                "https://cdn.discordapp.com/attachments/431947714511634432/432392065092026378/unknown.png",
                "https://imgur.com/V1q6ICY", "https://imgur.com/K4jye2T", "https://imgur.com/8FFw5nq", "https://imgur.com/xYipZQk",
                "https://imgur.com/iaV5FV0", "`Asura with Runaway Magic proc` \n http://i.imgur.com/vC3cSJT.gif",
                "`How converge e-call` :joy: \n https://clips.twitch.tv/AgitatedPoisedDugongPanicBasket \n\n `Don't dirty converge on this. This is ravage.`",
                "`Ravej Forever.` \n https://cdn.discordapp.com/attachments/377669073380835328/437666653983997952/screenNovaRO682.jpg",
                "`Don't forget who feed you on WoE, Fluffs` :joy: \n\n https://imgur.com/yDK1w6m",
                "`The weeb himself.` \n https://imgur.com/fYf9Pul", "`Champagnepapi` \n https://imgur.com/SAcaZPN",
                "https://imgur.com/LkJFf4d", "https://imgur.com/Davjalx", "`Warrage practicing for PvP tourney.` \n https://imgur.com/27AjprP", "https://imgur.com/PWY3igV",
                "https://imgur.com/YK4Epib", "`ef cee pee pls paparampam` - *Infuriate* :joy: \n https://clips.twitch.tv/ImportantFunnyBottleKeepo", "`el pucking pee plz` - *Midnight* :joy: https://clips.twitch.tv/GrotesqueAgitatedFerretDogFace",
                "https://imgur.com/b1fgbfe", "`how to be a chad.` \n https://imgur.com/tsa2PSV", "`he's not wrong.` :thinking: \n https://imgur.com/5UAymSx",
                "https://media.discordapp.net/attachments/428465462096166918/443420586568318976/unknown.png \n\n `this is why you don't do drugs, bois`",
                "`when your DM slide goes wrong.` \n\n https://media.discordapp.net/attachments/428465462096166918/443587720833400843/unknown.png?width=243&height=122",
                "`OK sir. OK.` \n\n https://media.discordapp.net/attachments/258430730756030474/442374255653552138/unknown.png?width=512&height=268",
                "`Xaide's love for Shally` \n\n https://cdn.discordapp.com/attachments/428465462096166918/443885601607909376/unknown.png",
                "`This guy left ravaj woe. Unacceptable. His reason?` \n\n https://i.imgur.com/b4FIOrP.png?width=270&height=192",
                "`Zento` \n\n https://cdn.discordapp.com/attachments/258430730756030474/440327586128855050/unknown.png",
                "`While developing this bot... Too much boi lul` \n\n https://cdn.discordapp.com/attachments/435744130623340545/444797728766296064/unknown.png",
                "`NovaRO May 2018 Tournament in a nutshell.` \n\n https://gyazo.com/abf71be9cff93bd4dd05d2aa1f9bff7d.gif",
                "`NovaRO Infinity Ban Movie` \n\n https://images-ext-1.discordapp.net/external/AshAIn6Ul-jKPMlaWpmpwkCwlkdb6pCo1KCtBA8JgS4/%3Fwidth%3D695%26height%3D499/https/media.discordapp.net/attachments/428465462096166918/444680404230995988/INFINITYBAN.png?width=674&height=484",
                "`WE WILL NEVER BE SLAVES!` \n\n https://cdn.discordapp.com/attachments/428465462096166918/444677152026132498/free_azn_combo.webm",
                "`Traps are not gay, Tokei` \n\n https://images-ext-1.discordapp.net/external/VkWwgWoIU0ZcANYNvLqW5a6Lev8TNgoXQy8V6q6tm4Y/https/images-ext-2.discordapp.net/external/XcGpUCuzY9VrjnEdUnvTo4-djvyxKJzeLGUIIMuGDn8/https/cdn.discordapp.com/attachments/428465462096166918/444676076942262303/unknown.png",
                "`Hang on there friendo, I was confused!! Ask me again!` <@120471942745554944> \n\n https://images-ext-1.discordapp.net/external/jvs49gCb8Sy7beHTbCfEPDmQSbqGLTulaTKESlZgEMQ/https/i.imgur.com/je4Wft2.png",
                "`Of course, you don't` :smirk: \n\n https://media.discordapp.net/attachments/435744130623340545/444499036125528065/unknown.png",
                "`Creepy` \n\n https://media.discordapp.net/attachments/428465462096166918/444466485449195522/NovaRO_2018-05-11_13-29-26.png",
                "`Oh god. Stop meme-ing` \n\n https://images-ext-1.discordapp.net/external/mhri25bPbQ4VHeyiFJi_sm1pkQaYR4y86SBgbyNveBk/https/media.discordapp.net/attachments/393802116294115329/444492522874732564/image.jpg",
                "`It's over bois. JK` :smirk: \n\n https://cdn.discordapp.com/attachments/435744130623340545/440511553268351006/unknown.png",
                "`NovaRO May 2018 Tournament Aftermath` \n\n https://images-ext-2.discordapp.net/external/LuPyn5VQ5Ub9sqLV3wePiLDyZqjK91oJ0lUgU6Sftf8/%3Fwidth%3D887%26height%3D499/https/media.discordapp.net/attachments/428465462096166918/444675080430288906/unknown.png?width=860&height=484",
                "`Quality content, sirs` \n\n https://media.discordapp.net/attachments/428465462096166918/445413303905419274/unknown.png?width=417&height=499",
                "https://media.discordapp.net/attachments/428465462096166918/445831291607187456/gabi-love-conquest.png?width=176&height=192",
                "https://media.discordapp.net/attachments/428465462096166918/445830596548100116/alliance.png?width=647&height=234",
                "https://media.discordapp.net/attachments/428465462096166918/445830713485557760/Arcadios.png?width=495&height=420",
                "https://cdn.discordapp.com/attachments/428465462096166918/445831625670918155/kellysuggestap.PNG?width=546&height=75",
                "https://cdn.discordapp.com/attachments/428465462096166918/445831751458095104/congythrottle.PNG?width=396&height=81",
                "https://images-ext-2.discordapp.net/external/tPMhlV2XSqeobKiTaNqP6idbIlN45nAY-oZrQnuVnss/https/cdn.discordapp.com/attachments/377669073380835328/414678957997293568/LUL.jpg?width=308&height=435",
                "https://media.discordapp.net/attachments/428465462096166918/447467279530196993/Capture.PNG?width=401&height=83",
                "https://media.discordapp.net/attachments/428465462096166918/447917682822479873/unknown.png",
                "https://media.discordapp.net/attachments/428465462096166918/448323523887235082/unknown.png?width=468&height=144",
                "https://media.discordapp.net/attachments/393802116294115329/444895235550609409/SCshoUt.png?width=679&height=356",
                "https://media.discordapp.net/attachments/428465462096166918/450593137933549570/AV.JPG?width=408&height=117",
                "https://media.discordapp.net/attachments/428465462096166918/450417152017825814/Saldar_How_Pathatic.png",
                "https://media.discordapp.net/attachments/428465462096166918/450416667156021250/dedbrain.png",
                "https://media.discordapp.net/attachments/428465462096166918/450147398409519112/unknown.png",
                "https://media.discordapp.net/attachments/428465462096166918/449808202998218752/unknown.png",
                "https://puu.sh/vyhhW.gif",
                "https://images-ext-2.discordapp.net/external/6Etw4zHXb0QymuRnddoyDW1Tqb9OM8xceT9US4s-9NE/%3Fwidth%3D307%26height%3D499/https/images-ext-1.discordapp.net/external/64hW4DosEH2UVhi5THpMCjTCvjM-uUaBbORJZyP-smA/%253Fwidth%253D432%2526height%253D702/https/media.discordapp.net/attachments/258430730756030474/429298648019632129/Screenshot_190.png?width=277&height=450",
                "https://media.discordapp.net/attachments/431947714511634432/449405826487156736/unknown.png?width=366&height=499",
                "https://cdn.discordapp.com/attachments/397709077955870735/449090785296646145/unknown.png",
                "https://media.discordapp.net/attachments/428465462096166918/449032669993500675/unknown.png?width=213&height=195",
                "https://media.discordapp.net/attachments/428465462096166918/451869116496609290/unknown.png",
                "https://images-ext-2.discordapp.net/external/MoEbRpJ0cHwtc3XLVkl0e8ZN-zyTMDml1A2r71KAK34/https/images-ext-2.discordapp.net/external/16FSr3j1uVZCKGJr9gC0s0Py_1bqCC7Bl5XvOr_F61I/https/media.discordapp.net/attachments/428465462096166918/451039060304330753/Capture.PNG?width=669&height=163",
                "https://cdn.discordapp.com/attachments/428465462096166918/438448451756359700/unknown.png?width=484&height=484",
                "https://images-ext-2.discordapp.net/external/t5gjrMcz2XmojKkulsmf48HWwWXBCYslVLsYtPvunU8/%3Fwidth%3D981%26height%3D499/https/images-ext-2.discordapp.net/external/RG5N585XAOuru8Nr4KO32pulXDknPF8VrfpR3kNN8co/https/i.gyazo.com/df5a0743cfbbb66ec6e5634133061fea.png?width=883&height=450",
                "https://media.discordapp.net/attachments/428465462096166918/453015232470712331/unknown.png?width=226&height=97",
                "https://media.discordapp.net/attachments/292965480254275587/460298974595776513/sitar.jpg",
                "https://media.discordapp.net/attachments/342779946000711683/425778090871095296/ihsanyamcha.png?width=463&height=481",
                "https://cdn.discordapp.com/attachments/428465462096166918/459360915142213645/unknown.png",
                "https://media.discordapp.net/attachments/428465462096166918/455503698953764864/unknown.png?width=424&height=29",
                "https://cdn.discordapp.com/attachments/448319388630777877/463027460339007488/unknown.png",
                "https://cdn.discordapp.com/attachments/292965480254275587/462025395059949570/cringe.png",
                "https://cdn.discordapp.com/attachments/448319388630777877/467702048046186519/unknown.png",
                "https://media.discordapp.net/attachments/448319388630777877/467702048046186519/unknown.png?width=213&height=54",
                "https://images-ext-1.discordapp.net/external/OuE7F3472W9FQ1qY5gRp3KCwR0O16B0iRVnYKeBtPpU/https/s7.postimg.cc/fugb8i2jv/Isah.gif?width=360&height=119",
                "https://images-ext-1.discordapp.net/external/aHRjD86ZlqEq8mebWcRVU5eSG1TFzS-KsmxErH-vUJM/https/cdn.discordapp.com/attachments/342779946000711683/461833302463217665/unknown.png?width=325&height=270",
                "https://media.discordapp.net/attachments/448319388630777877/508934236590571521/basic_egirl_package.png?width=505&height=281",
                ]
     if not param:
         chosenMeme = random.choice(memeImages)
         await self.bot.say("%s \n `Total of %d meme images` \n\n **DISCLAIMER:** \n`The memes generated are not mine.`" % (chosenMeme, len(memeImages)))
     else:
         index = int(param)
         try:
             chosenMeme = memeImages[index-1]
             await self.bot.say("%s \n `%s of %d meme images` \n\n **DISCLAIMER:** \n`The memes generated are not mine.`" % (chosenMeme, param, len(memeImages)))
         except Exception as e:
             print(e)
             await self.bot.say("There are %d of total meme images. Choose within that number :wink:" %(len(memeImages)))


 @commands.command(pass_context=True)
 async def incant(self, ctx):
     sender = ctx.message.author
     den_emoji = "https://cdn.discordapp.com/emojis/377918156460654593.png?v=1"
     images = ["https://media.discordapp.net/attachments/401524127841648652/435745879819943936/riiGZqd.png",
              "https://media.discordapp.net/attachments/401524127841648652/435746545686675466/l2rChoe.png",
             ]
     chosenImage = random.choice(images)
     embed = discord.Embed(title="The Incantation Samurai Card Broken Promise", description="Proofs of expectations.")
     embed.set_thumbnail(url=den_emoji)
     embed.set_image(url=chosenImage)
     embed.set_footer(text="Den is waiting, Deegs. Anytime now.")
     await self.bot.send_message(ctx.message.channel, embed=embed)

 @commands.command(pass_context=True)
 async def dogs(self, ctx):
     sender = ctx.message.author
     apiUrl = "https://dog.ceo/api/breeds/image/random" # the api host of dog images.
     response = requests.get(apiUrl)
     if response.status_code == 200:
         dog = json.loads(response.content.decode('utf-8'))
         image = dog['message']
         embed = discord.Embed(title="Random Dog Pictures", description="Brought to you by http://dog.ceo/dog-api/documentation/ :dog:")
         embed.set_image(url=image)
         await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)
     else:
         await self.bot.say("<@%s>, there's something wrong with the dog's server :dog:" % sender.id)

 @commands.command(pass_context=True)
 async def cats(self, ctx):
     sender = ctx.message.author
     catUrl = "https://thecatapi.com/api/images/get?format=xml"
     result = session_requests.get(catUrl, headers = dict(referer= catUrl))
     content = result.text
     bSoup = BeautifulSoup(content, 'xml')
     url = bSoup.find("url").get_text()
     embed = discord.Embed(title="Random Cat Pictures", description="Brought to you by http://thecatapi.com/ :cat:")
     embed.set_image(url=url)
     await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)

 # bot command for item information on Ragnarok Online.
 # source : http://ratemyserver.net
 @commands.command(pass_context=True)
 async def ii(self, ctx, *, search: str):
  sender = ctx.message.author
  item = search.replace(" ", "+")
  dpride_search_url = "https://www.divine-pride.net/database/item/jellopy?Name=%s&function=&find=Search" % (item)
  dpride_domain = "https://www.divine-pride.net"
  result = session_requests.get(dpride_search_url, headers = dict(referer = dpride_search_url))
  content = result.text
  bSoup = BeautifulSoup(content, 'lxml')
  search_result_table = bSoup.find("tbody")
  item_url = ""
  item_id = ""
  item_sell = ""
  item_weight = ""
  item_type = ""
  item_subtype = ""
  item_description = ""
  item_image = ""
  scripts = ""
  await self.bot.say("`This command is still in beta.`")
  wait_message = await self.bot.send_message(ctx.message.channel, "Searching Divine Pride's database...")
     # checking if there is an item existing in the database
  if len(search_result_table.find_all("tr")) == 0:
   await self.bot.send_message(ctx.message.channel, "There is no such **%s** item in the Divine-Pride database." % (search.capitalize()))
  else:
   await asyncio.sleep(0.2)
   slots = ["[1]", "[2]", "[3]", "[4]"]
   for row in search_result_table.find_all("tr"):
    column = row.find_all("td")[0]
    data = column.get_text().strip()
    # cleaning the items that have slots on their names to match the search parameter.
    for slot in slots:
     if not data.find(slot) == -1:
      data = data.replace(slot, "")
      break
             # print(search.title())
             # print(data)
    if search.title() == data.strip():
     link = column.find_all("a", href=True)[0]
     item_url = link['href']
   item_url = dpride_domain+item_url
   result = session_requests.get(item_url, headers = dict(referer = item_url))
   content = result.text
   bSoup = BeautifulSoup(content, 'lxml')
   item_description_table = bSoup.find('table', attrs={"class":"mon_table"})
   item_data_table = bSoup.find('table', attrs={"class" : "table table-bordered table-striped table-condensed table-full table-small-text"})
   script_table = bSoup.find('ul', attrs={"style" : "list-style: disc;"})
   for row in item_description_table.find_all("tr"):
    column = row.find_all("td")
    img = column[0].find('img')['src']
    item_image = img
    item_description = column[1].get_text().strip()
         # table beside
   row = item_data_table.find_all("tr")
   column_item_id = row[0].find_all("td")
   column_item_sell = row[1].find_all("td")
   column_item_weight = row[2].find_all("td")
   column_item_type = row[3].find_all("td")
   column_item_subtype = row[4].find_all("td")

   item_id = column_item_id[0].get_text().strip()
   item_sell = column_item_sell[0].get_text().strip()
   item_weight = column_item_weight[0].get_text().strip()
   item_type = column_item_type[0].get_text().strip()
   item_subtype = column_item_subtype[0].get_text().strip()
   await asyncio.sleep(0.25)
   if not script_table == None:
    for unlist in script_table.find_all("li"):
     scripts += unlist.get_text().strip() + "\n"
   else:
    scripts = ""
   thumbnail_url = item_image.replace("collection", "item")
   if item_type == "Card":
    item_image = "/images/items/cards/%s.png" % (item_id)
   embed = discord.Embed(title="%s" % (data.strip()), description="Divine Pride reference")
   embed.set_thumbnail(url="%s" % (dpride_domain + thumbnail_url))
   embed.set_image(url="%s" % (dpride_domain + item_image))
         # embed.add_field(name="Item Name", value="%s" % (data.strip()), inline=False)  
   embed.add_field(name="ID", value="%s" % (item_id), inline=True)
   embed.add_field(name="Sell", value="%s" % (item_sell), inline=True)
   embed.add_field(name="Weight", value="%s" % (item_weight), inline=True)
   embed.add_field(name="Type", value="%s" % (item_type), inline=True)
   embed.add_field(name="Sub-type", value="%s" % (item_subtype), inline=True)
   embed.add_field(name="Description", value="```%s```" % (item_description), inline=False)
   embed.add_field(name="Scripts", value="```css\n%s```" % (scripts) if len(scripts) > 0 else "No script.", inline=False)
   print(len(item_description) + len(scripts))
   try:
    await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)
   except Exception as e:
    print(e)
    await self.bot.send_message(ctx.message.channel, "Error encountered")
  await self.bot.delete_message(wait_message)

 # bot command for monster information on Ragnarok Online
 # source : http://ratemyserver.net
 # @bot.command(pass_context=True)
 # async def mi(ctx, monster: str):
             

 # ree
 @commands.command(pass_context=True)
 async def ree(self, ctx):
     ree_img = "./images/ree.gif"
     await self.bot.send_file(ctx.message.channel, ree_img)


 # let ravaj say something for you.
 @commands.command(pass_context=True)
 async def say(self, ctx, *, message=""):
  if "$say" in message:
      message = ctx.message.content.replace("$say", "")
  if "-say" in message:
   message = ctx.message.content.replace("$say", "")
  await self.bot.delete_message(ctx.message)
  await self.bot.say(message)


 # bot command for QOP memes.
 @commands.command(pass_context=True)
 async def qop(self, ctx, param=""):
     sender = ctx.message.author
     image_urls = ["https://media.discordapp.net/attachments/352246546353356810/442376705705771008/unknown.png",
                     "https://media.discordapp.net/attachments/352246546353356810/442383885637124096/unknown.png?width=165&height=132",
                     "https://media.discordapp.net/attachments/393802116294115329/450830788469194753/unknown-27.png?width=528&height=408",
                     "https://media.discordapp.net/attachments/448319388630777877/470740877577420800/image.png?width=235&height=271",]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/kingofpain"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Great Ravaj Warlock", description="There are a total of %d image(s)." % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         if chosenImage == "https://media.discordapp.net/attachments/393802116294115329/450830788469194753/unknown-27.png?width=528&height=408":
             embed.set_footer(text="You just jealous. I kill Alliance in 300ms :pepehi:")
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Great Ravaj Warlock - QOP", description="%s of %d images." % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 # bot command for Fluffs memes.
 @commands.command(pass_context=True)
 async def fluffs(self, ctx, params=""):
     sender = ctx.message.author
     image_urls = ["https://media.discordapp.net/attachments/431947714511634432/437498547328385034/fluffsfood.jpg?width=450&height=450",
         "https://gyazo.com/03742683cc4071078da4f526f1e0f7fe",
         "https://images-ext-1.discordapp.net/external/F39lOX3JmTY2Vy2XJPWhnoJah-ghdohhIxAZVXYyIb0/https/cdn.discordapp.com/attachments/428465462096166918/468317104941039626/unknown.png",
         "https://images-ext-1.discordapp.net/external/F39lOX3JmTY2Vy2XJPWhnoJah-ghdohhIxAZVXYyIb0/https/cdn.discordapp.com/attachments/428465462096166918/468317104941039626/unknown.png?width=360&height=154",
                     ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/Fluffs"
     if not params:
         chosenImage = random.choice(image_urls)
         if not "gyazo" in chosenImage:
          embed = discord.Embed(title="Greatest Shadow Chaser next to Kobe. - Fluffs", description="There are a total of %d image(s)." % (len(image_urls)))
          embed.set_image(url=chosenImage)
          embed.set_thumbnail(url=thumbnail)
          await self.bot.send_message(ctx.message.channel, embed=embed)
         else:
          await self.bot.send_message(ctx.message.channel, "%s" % (chosenImage))
     else:
         index = int(params)
         try:
             chosenImage = image_urls[index-1]
             if not "gyazo" in chosenImage:
              embed = discord.Embed(title="Greatest Shadow Chaser next to Kobe. - Fluffs", description="%s of %d images." % (param, len(image_urls)))
              embed.set_thumbnail(url=thumbnail)
              embed.set_image(url=chosenImage)
              await self.bot.send_message(ctx.message.channel, embed=embed)
             else:
              await self.bot.send_message(ctx.message.channel, "%s" % (chosenImage))
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 # bot command for Den memes.
 @commands.command(pass_context=True)
 async def den(self, ctx, param=""):
     sender = ctx.message.author
     image_urls = ["https://media.discordapp.net/attachments/428465462096166918/447815068126543872/cats-on-leashes.jpg?width=563&height=376",
                 "https://cdn.discordapp.com/attachments/428465462096166918/440862965814525953/iconicduo.png",
                 "https://images-ext-1.discordapp.net/external/bDpbuqqTp5P5S9k_S_Piza8TZvM3NmEwQmL0un3Z4Sc/https/jet.s-ul.eu/97D0XZg3?width=445&height=60",
                 "https://media.discordapp.net/attachments/428465462096166918/444905949686267914/unknown.png?width=409&height=149",
                 "https://media.discordapp.net/attachments/448319388630777877/451246999669440522/unknown.png?width=286&height=63",
                 "https://images-ext-1.discordapp.net/external/D4MTtAA2pT7s-euwVY91epI-WZgUN1vi5bKa4d2NRwM/https/cdn.discordapp.com/attachments/258430730756030474/470277549948272660/Capture.PNG?width=360&height=73",
                 ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/Denkins"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Den - Den", description="There are a total of %d image(s)" % (len(image_urls)))
         embed.set_thumbnail(url=thumbnail)
         embed.set_image(url=chosenImage)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Den - Den", description="%s of %d images." % (param, len(image_urls)))
             embed.set_thumbnail(url=thumbnail)
             embed.set_image(url=chosenImage)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 # bot command for Xaide memes.
 @commands.command(pass_context=True)
 async def xaide(self, ctx, param=""):
     sender = ctx.message.author
     image_urls = ["https://media.discordapp.net/attachments/428465462096166918/447685910830645249/unknown.png",
                "https://media.discordapp.net/attachments/428465462096166918/447686108353134592/unknown.png",
                "https://media.discordapp.net/attachments/428465462096166918/448123775184142338/Untitled.png",
                "https://media.discordapp.net/attachments/428465462096166918/448319312336388116/unknown.png?width=269&height=284",
                "https://media.discordapp.net/attachments/428465462096166918/448319312336388116/unknown.png?width=269&height=284",
                "https://media.discordapp.net/attachments/428465462096166918/448320771849322497/unknown-32.png?width=338&height=135",
                "https://media.discordapp.net/attachments/428465462096166918/460560374035513344/unknown.png",
                "https://media.discordapp.net/attachments/428465462096166918/459906742403465216/unknown.png",
                ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/xaide"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Agik BG Player - Xaide", description="There are a total of %d image(s)" % (len(image_urls)))
         embed.set_thumbnail(url=thumbnail)
         embed.set_image(url=chosenImage)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Agik BG Player - Xaide", description="%s of %d images." % (param, len(image_urls)))
             embed.set_thumbnail(url=thumbnail)
             embed.set_image(url=chosenImage)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 # bot command for Deegs memes.
 @commands.command(pass_context=True)
 async def deegs(self, ctx, param=""):
     sender = ctx.message.author
     image_urls = ["https://cdn.discordapp.com/attachments/378800013767344128/439579452108832788/unknown.png", 
                "https://media.discordapp.net/attachments/352246546353356810/442392864773636106/unknown.png",
                "https://media.discordapp.net/attachments/352246546353356810/442381167183003656/Screenshot_2018-05-05-14-44-41.png?width=890&height=205",
                "https://cdn.discordapp.com/attachments/352246546353356810/442727402913792011/unknown.png",
                "https://images-ext-2.discordapp.net/external/AabhdwSlwv0sTuKz2nlYxitdYztTYD0UihIOTKbYQgg/https/i.imgur.com/MBDYPTo.png?width=355&height=499",
                "https://cdn.discordapp.com/attachments/352246546353356810/442732473672269825/unknown.png?width=1026&height=459",
                "https://media.discordapp.net/attachments/428465462096166918/447762827021647882/unknown.png?width=288&height=170",
                "https://media.discordapp.net/attachments/352246546353356810/419528829002973216/unknown.png",
                "https://cdn.discordapp.com/attachments/448319388630777877/463027460339007488/unknown.png",
                "https://cdn.discordapp.com/attachments/428465462096166918/465002527696617472/unknown.png",
                ]
     thumbnail = "https://images-ext-1.discordapp.net/external/0NAaQKw0w3L5bAZuxkCGSUWUs6jAzH8Z-eOetSXjY_s/https/www.novaragnarok.com/ROChargenPHP/characterhead/More%2520Life"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Great Ravej Leader - Deegs", description="There are a total of %d image(s)" % (len(image_urls)))
         embed.set_thumbnail(url=thumbnail)
         embed.set_image(url=chosenImage)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Great Ravej Leader - Deegs", description="%s of %d images." % (param, len(image_urls)))
             embed.set_thumbnail(url=thumbnail)
             embed.set_image(url=chosenImage)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))
             
 #bot command for Yummy yummy dumplings.
 @commands.command(pass_context=True)
 async def yyd(self, ctx):
     thumbnail = "https://images-ext-1.discordapp.net/external/APyDQ5Zo5oB4e5IBnOAK8mYddEEq6nI2xjP3kvpxKSo/%3Fmodule%3Dguild%26action%3Demblem%26login%3DNovaRO%26charmap%3DNovaRO%26id%3D8091/https/www.novaragnarok.com/"
     image = "https://cdn.discordapp.com/attachments/430532948266319872/444793430728638464/unknown.png"
     embed = discord.Embed(title="First PvX Guild", description="Like, Share, and Subscribe by the way ;)")
     embed.set_image(url=image)
     embed.set_thumbnail(url=thumbnail)
     await self.bot.send_message(ctx.message.channel, embed=embed)
     await self.bot.say("Let me show you a tale of how the `Yummy Yummy Dumplings` is formed. \n https://www.youtube.com/watch?v=6derHHu0Xt0&feature=youtu.be")

 @commands.command(pass_context=True)
 async def egirls(self, ctx):
    image = "https://media.discordapp.net/attachments/448319388630777877/508934236590571521/basic_egirl_package.png?width=505&height=281"
    embed = discord.Embed(title="Basic RO E-Girl Starter Pack", description="Gabi, you're still the best though ;)")
    embed.set_image(url=image)
    await self.bot.send_message(ctx.message.channel, embed=embed)
 #bot command for Russian Squad.
 @commands.command(pass_context=True)
 async def rs(self, ctx, param=""):
     image_urls = ["https://cdn.discordapp.com/attachments/428465462096166918/443792460938739722/unknown.png",
                 "https://media.discordapp.net/attachments/352246546353356810/442386388990820372/unknown.png?width=549&height=368",
                 "https://media.discordapp.net/attachments/352246546353356810/442387982843117598/shittard.png?width=809&height=484",
                 "https://cdn.discordapp.com/attachments/428465462096166918/448495714033598464/unknown-17.png",
                 "https://media.discordapp.net/attachments/448319388630777877/470280698398244874/unknown.png?width=360&height=253",
                 ]
     thumbnail = "https://cdn.discordapp.com/attachments/430532948266319872/444803756022824960/unknown.png"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Best WoE Guild in NovaRO", description="There are a total of %d image/meme(s)" % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Best WoE Guild in NovaRO.", description="%s of %d image(s)." % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 #bot command for NeonSeeker.
 @commands.command(pass_context=True)
 async def neon(self, ctx, param=""):
     image_urls = ["https://cdn.discordapp.com/attachments/428465462096166918/450417690994147338/splindedsplash1.png",
                    "https://cdn.discordapp.com/attachments/428465462096166918/450418679428153344/neoncockcomplete.png",
                    "https://cdn.discordapp.com/attachments/428465462096166918/450418805097627679/neonspearpart2.png",
                    "https://cdn.discordapp.com/attachments/428465462096166918/450418706816958474/neondicc.png",
                    "https://media.discordapp.net/attachments/428465462096166918/459548369765924884/neonkaintae.png?width=123&height=16",
                    "https://images-ext-2.discordapp.net/external/fxg1AIX9E9UovApwU3MaRViOm9ZzN8D1I5j1tKjJVqE/%3Fwidth%3D199%26height%3D450/https/media.discordapp.net/attachments/428465462096166918/458114585627590656/unknown.png?width=180&height=405",
                    "https://cdn.discordapp.com/attachments/428465462096166918/458114232601411585/unknown.png",
                    "https://media.discordapp.net/attachments/428465462096166918/458113961284599808/unknown.png?width=226&height=56",
                    "https://media.discordapp.net/attachments/428465462096166918/458111375391064064/unknown.png?width=173&height=69",
                    "https://media.discordapp.net/attachments/428465462096166918/458109133489700874/unknown.png?width=182&height=68",
                ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/neonseeker"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Yack Strike - NeonSeeker", description="There are a total of %d image/meme(s)" % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Yack Strike - NeonSeeker", description="%s of %d image(s)." % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 # bot command for shalltear
 @commands.command(pass_context=True)
 async def shally(self, ctx, param=""):
     image_urls = ["https://media.discordapp.net/attachments/428465462096166918/443791102445748224/unknown.png",
                   "https://www.youtube.com/watch?v=hyhwHsqy4fY",
                   "https://cdn.discordapp.com/attachments/430532948266319872/444803516582592524/unknown.png",
                   "https://cdn.discordapp.com/attachments/428465462096166918/453723526470565908/unknown.png",
                   "https://images-ext-2.discordapp.net/external/8UPBjt_OtClxyoWi_B64K2n9nldEjQfs3C3b4v44Jrs/https/media.discordapp.net/attachments/428465462096166918/456836153543229444/shalltear-family.png?width=756&height=370",
               ]
     thumbnail = "https://images-ext-1.discordapp.net/external/rHH50TYM7OqKi6pLEQeryEMBmeEmZahZLnwmXTRHhrE/https/www.novaragnarok.com/ROChargenPHP/characterhead/Shalltear"
     if not param:
         chosenImage = random.choice(image_urls)
         if "youtube" in chosenImage:
             await self.bot.send_message(ctx.message.channel, "`Bwing out bois!` \n %s" % (chosenImage))
         else:
             embed = discord.Embed(title="Tao Gonker / Great Alliance Leader", description="There are a total of %d image/meme(s)" % (len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             if "youtube" in chosenImage:
                 await self.bot.send_message(ctx.message.channel, "`Bwing out bois!` \n %s" % (chosenImage))
             else:
                 embed = discord.Embed(title="Tao Gonker / Great Alliance Leader", description="%s of %d image/meme(s)" % (param, len(image_urls)))
                 embed.set_image(url=chosenImage)
                 embed.set_thumbnail(url=thumbnail)
                 await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))


 # bot command for clear boks
 @commands.command(pass_context=True)
 async def box(self, ctx, param=""):
     image_urls = ["https://cdn.discordapp.com/attachments/428465462096166918/443962495170904065/unknown.png?width=273&height=323",
                   "https://media.discordapp.net/attachments/292965480254275587/443956822257303563/aura.png?width=259&height=374",
                   "https://media0.giphy.com/media/8TCb91n9U59TWODUZX/giphy.mp4",
                   "https://cdn.discordapp.com/attachments/342779946000711683/427983919418310666/unknown.png",
                   "https://cdn.discordapp.com/attachments/214065718449274882/282892609297317888/unknown.png",
                   "https://images-ext-2.discordapp.net/external/oAnvfljgrCEmquW0ZQwoT5iFlYy7HSbLSdlk3ztVfvU/https/i.gyazo.com/thumb/1200/0dec42515430e691e2fcdf941df29ff0-png.jpg?width=530&height=83",
                   "https://cdn.discordapp.com/attachments/397709077955870735/448126261680668682/unknown.png",
                   "https://cdn.discordapp.com/attachments/448319388630777877/470282322047008768/unknown.png",
                   ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/clear%20box"

     if not param:
         chosenImage = random.choice(image_urls)
         if "giphy" in chosenImage:
             await self.bot.send_message(ctx.message.channel, "%s :joy: :DEN:" % (chosenImage))
         else:
             embed = discord.Embed(title="[Almost There] Boks kun - Clear Box", description="There are a total of %d image/meme(s)" % (len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             if "giphy" in chosenImage:
                 await self.bot.send_message(ctx.message.channel, "%s :joy: :DEN:" % (chosenImage))
             else:
                 embed = discord.Embed(title="[Almost There] Boks kun - Clear Box", description="%s of %d image/meme(s)" % (param, len(image_urls)))
                 embed.set_image(url=chosenImage)
                 embed.set_thumbnail(url=thumbnail)
                 await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 @commands.command(pass_context=True)
 async def von(self, ctx, param=""):
     image_urls = ["https://media.discordapp.net/attachments/393802116294115329/444494065023582218/image.jpg",
                   "https://youtu.be/QOW3UbWbP6o",
                  ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/von%20henheim"

     if not param:
         chosenImage = random.choice(image_urls)
         if "youtu" in chosenImage:
             await self.bot.send_message(ctx.message.channel, "%s :joy: :DEN:" % (chosenImage))
         else:
             embed = discord.Embed(title="Rich Maricon", description="There are a total of %d image/meme(s)" % (len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             if "youtu" in chosenImage:
                 await self.bot.send_message(ctx.message.channel, "%s :joy: :DEN:" % (chosenImage))
             else:
                 embed = discord.Embed(title="Rich Maricon", description="%s of %d image/meme(s)" % (param, len(image_urls)))
                 embed.set_image(url=chosenImage)
                 embed.set_thumbnail(url=thumbnail)
                 await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 @commands.command(pass_context=True)
 async def azn(self, ctx, param=""):
     image_urls = ["https://media.discordapp.net/attachments/428465462096166918/444676241757437952/dontfeelssogood.png",
                  "https://cdn.discordapp.com/attachments/428465462096166918/444667219712933888/unknown.png",
                  "https://media.discordapp.net/attachments/428465462096166918/444684170917183489/unknown.png",
                  "https://media.discordapp.net/attachments/428465462096166918/444698930731548678/unknown.png",
                  "https://media.discordapp.net/attachments/428465462096166918/444703812473585664/unknown.png",
                  "https://media.discordapp.net/attachments/430532948266319872/444810575395160064/unknown.png",
                  "https:///cdn.discordapp.com/attachments/428465462096166918/444667219712933888/unknown.png?width=378&height=19",
                  "https://images-ext-1.discordapp.net/external/3n2qzrp-sPX9IZKT-5eCMh940KU8XQDZcUpQtSbrkZk/https/media.discordapp.net/attachments/428465462096166918/463165217195556885/unknown.png?width=524&height=161",
                  ]
     thumbnail = "https://cdn.discordapp.com/emojis/416051244029706241.png?v=1"

     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Best Sura in NovaRO", description="There are a total of %d image/meme(s)" % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Best Sura in NovaRO", description="%s of %d image/meme(s)" % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))


 @commands.command(pass_context=True)
 async def jet(self, ctx, param=""):
     image_urls = ["https://media.discordapp.net/attachments/428465462096166918/445279403216207872/ur_retarded.png",
                  "https://media.discordapp.net/attachments/428465462096166918/445279395482042378/imretarded.png?width=380&height=499",
                  "https://media.discordapp.net/attachments/428465462096166918/445278627521626137/jetmilifuk.PNG",
                 ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/Milly"
     names = ["Billy", "Milly", "Jet", "Jett"]
     chosenName = random.choice(names)
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="One of the Unreliable Casuals Leaders - %s" % (chosenName), description="There are a total of %d image/meme(s)" % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="One of the Unreliable Casuals Leaders - %s" % (chosenName), description="%s of %d image/meme(s)" % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 @commands.command(pass_context=True)
 async def sano(self, ctx, param: str = ""):
     image_urls = ["https://cdn.discordapp.com/attachments/428465462096166918/455203936190857217/unknown.png",
                     "https://cdn.discordapp.com/attachments/428465462096166918/455204482406416394/unknown.png",
                     "https://cdn.discordapp.com/attachments/428465462096166918/438448451756359700/unknown.png?width=484&height=484",
                 ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/Sanoshi"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="All around Player | YYD's founder | Enya's Lover - Sanoshi", description="There are a total of %d image/meme(s)" % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="All around Player | YYD's founder | Enya's Lover - Sanoshi", description="%s of %d image/meme(s)" % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 @commands.command(pass_context=True)
 async def nova(self, ctx, param: str = ""):
     image_urls = ["https://cdn.discordapp.com/attachments/428465462096166918/454793705333719050/unknown.png",
                  "https://cdn.discordapp.com/attachments/428465462096166918/454788220907945994/unknown.png",
                  "https://media.discordapp.net/attachments/428465462096166918/445413303905419274/unknown.png?width=417&height=499",
                  "https://media.discordapp.net/attachments/428465462096166918/458173932760203274/unknown.png?width=91&height=28",
                  "https://media.discordapp.net/attachments/428465462096166918/457686191467266049/unknown.png",
                  "https://images-ext-1.discordapp.net/external/VDiotR0OX6gxBv0y050ULNEQUQIS-LIssRHNG-C673g/https/i.gyazo.com/thumb/1200/3f449ebf3468f260f976aa9fe99d0ab6-png.jpg",
                ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/%5Bgm%5D%20nova"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Best GM | Moderator | Content Provider | You name it - [GM] Nova", description="There are a total of %d image/meme(s)" % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Best GM | Moderator | Content Provider | You name it - [GM] Nova", description="%s of %d image/meme(s)" % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 @commands.command(pass_context=True)
 async def kagami(self, ctx, param: str = ""):
     image_urls = ["https://images-ext-1.discordapp.net/external/BDTW4JK1EsUUCiBcyYIBzPdkBJxmq5M_HOtaxJy-YGI/https/cdn.discordapp.com/attachments/443955138227601418/453630402771288075/unknown.png",
                   "https://cdn.discordapp.com/attachments/448319388630777877/460344622875541506/unknown.png",
                   "https://cdn.discordapp.com/attachments/448319388630777877/460344804669259786/unknown.png",
                   "https://media.discordapp.net/attachments/448319388630777877/465706313494691870/unknown.png",
                   "https://images-ext-2.discordapp.net/external/W2P9TI1SC5aJNxa5FpZnJIGRw3qz1_zZ2ggXUFUnQe8/http/clip2net.com/clip/m552035/thumb800/bc0b8-clip-7kb.png",
                   "https://media.discordapp.net/attachments/328839519531040769/467627963245133824/unknown.png?width=887&height=499",
                   "https://media.discordapp.net/attachments/428465462096166918/467511610135674890/unknown.png",
                   "https://cdn.discordapp.com/attachments/448319388630777877/465706313494691870/unknown.png",]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/akashi%20z"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="NovaRO's Habibi - Kagamii", description="There are a total of %d image/meme(s)" % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="NovaRO's Habibi - Kagamii", description="%s of %d image/meme(s)" % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 @commands.command(pass_context=True)
 async def infu(self, ctx, param: str = ""):
     image_urls = ["https://images-ext-2.discordapp.net/external/hBgfYd30Wc0-0NsEtxSph2b9VuBv6ujTHtJjhdcTNzI/https/i.imgur.com/7e4ZBop.png",
          "https://media.discordapp.net/attachments/352246546353356810/465564796083896325/unknown.png",
          "https://media.discordapp.net/attachments/352246546353356810/465564890313261059/unknown.png",]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/lnfuriate"
     if not param:
         chosenImage = random.choice(image_urls)
         embed = discord.Embed(title="Infuriated Russian - Infuriate", description="There are a total of %d image/meme(s)" % (len(image_urls)))
         embed.set_image(url=chosenImage)
         embed.set_thumbnail(url=thumbnail)
         await self.bot.send_message(ctx.message.channel, embed=embed)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             embed = discord.Embed(title="Infuriated Russian - Infuriate", description="%s of %d image/meme(s)" % (param, len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 @commands.command(pass_context=True)
 async def fu(self, ctx, param: str = ""):
     image_urls = ["Ｐｌｅａｓｅ，　ｓｔｏｐ　ｃｒｙｉｎｇ．　Ｉｆ　ｙｏｕ＇ｒｅ　ｒｅａｌｌｙ　ｇｏｏｄ　ａｔ　ｕｓｉｎｇ　Ｓｕｒａ，　ｙｏｕ　ｗｏｎ＇ｔ　ｈａｖｅ　ａ　ｐｒｏｂｌｅｍ　ｂｙ　ｓｔｉｌｌ　ｕｓｉｎｇ　ｉｔ　ｗｈｅｎ　Ｓｎａｐ　ｇｅｔｓ　ｒｅｍｏｖｅｄ．　Ａ　ｊｏｂ　ｄｏｅｓｎ＇ｔ　ｄｉｅ　ｂｅｃａｕｓｅ　ｏｆ　ａ　ｓｉｎｇｌｅ　ｓｋｉｌｌ　ｔｈａｔ　ｂｒｅａｋｓ　ｔｈｅ　ｇａｍｅ．　Ｓｕｒａ＇ｓ　ｉｄｅｎｔｉｔｙ　ｇｏｅｓ　ｍｕｃｈ　ｆｕｒｔｈｅｒ　ｔｈａｎ　ｔｈａｔ．　Ｉｎ　ｔｈｅ　ｌｏｒｅ，　ｔｈｅｙ＇ｒｅ　Ｍｏｎｋｓ　ｔｈａｔ　ｌｅａｒｎｅｄ　ｔｏ　ｄｏｍｉｎａｔｅ　ｔｈｅ　Ｄｅｍｏｎ＇ｓ　Ｐｏｗｅｒ．　Ｓｏ，　ｐｒｏｐｅｒｌｙ　ｔａｌｋｉｎｇ，　ｔｈｅｉｒ　ｍａｉｎ　ｓｋｉｌｌ　ｓｈｏｕｌｄ　ｂｅ　ｃｏｎｓｉｄｅｒｅｄ　Ｇａｔｅｓ　ｏｆ　Ｈｅｌｌ\n\n- **Balde of Wind | Legendary folklore - Fu - Blade of Wind**",
                 "https://cdn.discordapp.com/attachments/214065718449274882/450675670784278538/fu_wind.JPG",
                  "https://cdn.discordapp.com/attachments/342779946000711683/450686562057846804/fu_wind_2.JPG",
                  "https://media.discordapp.net/attachments/342779946000711683/457313132654755841/unknown.png",
                  "https://media.discordapp.net/attachments/342779946000711683/456925411746512919/unknown.png?width=577&height=499",
                  "https://media.discordapp.net/attachments/258430730756030474/461728492544065556/Screenshot_Discord_20180627-23025801.png?width=972&height=360"
                  ]
     thumbnail = "https://www.novaragnarok.com/ROChargenPHP/characterhead/fu%20wind"
     if not param:
         chosenImage = random.choice(image_urls)
         if "http" in chosenImage:
             embed = discord.Embed(title="Balde of Wind | Legendary folklore - Fu - Blade of Wind", description="There are a total of %d image/meme(s)" % (len(image_urls)))
             embed.set_image(url=chosenImage)
             embed.set_thumbnail(url=thumbnail)
             await self.bot.send_message(ctx.message.channel, embed=embed)
         else:
             await self.bot.send_message(ctx.message.channel, "%s" % chosenImage)
     else:
         index = int(param)
         try:
             chosenImage = image_urls[index-1]
             if "http" in chosenImage:
                 embed = discord.Embed(title="Balde of Wind | Legendary folklore - Fu - Blade of Wind", description="%s of %d image/meme(s)" % (param, len(image_urls)))
                 embed.set_image(url=chosenImage)
                 embed.set_thumbnail(url=thumbnail)
                 await self.bot.send_message(ctx.message.channel, embed=embed)
             else:
                 await self.bot.send_message(ctx.message.channel, "%s" % chosenImage)
         except Exception as e:
             print(e)
             await self.bot.say("The image is only from 1 to %d. Choose a number between those :wink:" % (len(image_urls)))

 # bot command to know who has their own personalized commands.
 @commands.command(pass_context=True)
 async def who(self, ctx):
     sender = ctx.message.author
     embed = discord.Embed(title="Hall of Famers", description="The following are commands to witness the evidence(s) of their greatness.")
     embed.add_field(name="$rs", value="Best WoE Guild in NovaRO", inline=False)
     embed.add_field(name="$yyd", value="The first PvX Guild in NovaRO", inline=False)
     embed.add_field(name="$shally", value="Tao Gonker and Glorious Alliance leader.", inline=False)
     embed.add_field(name="$deegs", value="Great Ravaj Leader", inline=False)
     embed.add_field(name="$qop", value="Great Ravaj Warlock", inline=False)
     embed.add_field(name="$fluffs", value="Greatest Shadow Chaser next to Kobe.", inline=False)
     embed.add_field(name="$box", value="[Almost There] Boks kun.", inline=False)
     embed.add_field(name="$azn", value="Best Sura in NovaRO", inline=False)
     embed.add_field(name="$von", value="Rich Maricon", inline=False)
     embed.add_field(name="$jet", value="One of the Unreliable Casuals Leaders", inline=False)
     embed.add_field(name="$den", value="Den", inline=False)
     embed.add_field(name="$xaide", value="Agik BG Player", inline=False)
     embed.add_field(name="$neon", value="Yack Strike. Goat CS RK", inline=False)
     embed.add_field(name="$sano", value="All around player | YYD Leader | Enya's Lover", inline=False)
     embed.add_field(name="$kagami", value="NovaRO's Habibi", inline=False)
     embed.add_field(name="$fu", value="Balde of Wind | Legendary folklore", inline=False)
     embed.add_field(name="$infu", value="Infuriated Russian", inline=False)
     embed.add_field(name="$nova", value="Best GM | Moderator | Content Provider | You name it", inline=False)
     embed.set_footer(text="Want your own command? Gib 2m. Jk, just pm Andie and gib a great image of your own.")

     await self.bot.send_message(ctx.message.channel, embed=embed)

 # shows random bird pics
 @commands.command(pass_context=True)
 async def birds(self, ctx):
     sender = ctx.message.author
     apiUrl = "https://random.birb.pw/tweet.json" # the api host of dog images.
     displayUrl = "https://random.birb.pw/img/"
     response = requests.get(apiUrl)
     if response.status_code == 200:
         bird = json.loads(response.content.decode('utf-8'))
         image = displayUrl+bird['file']
         embed = discord.Embed(title="Random Bird Pictures", description="Brought to you by https://random.birb.pw/ :bird:")
         embed.set_image(url=image)
         await self.bot.send_message(ctx.message.channel, "<@%s>" % (sender.id), embed=embed)
     else:
         await self.bot.say("<@%s>, there's something wrong with the bird's server :bird:" % sender.id)

 # bot gives random advice.
 @commands.command(pass_context=True)
 async def advice(self, ctx):
     sender = ctx.message.author
     adviceUrl = "http://api.adviceslip.com/advice"
     memeAdvices = ["Don't let Deegs be captain on draft.", "Should tell QueenOfPaiN to use Demi-human reducts.",
                     "Let Shalltear lend his Tao Gunka to Ravage.", "Give Clear Box his aura. Consolation for trying hard.",
                     "Release Den from the leash, Deegs.", "Guys, just quit this server or game.", "Nova should provide a quality content. Not qUaLiTy ConTiNeNt.",
                     "How about donating to Andie for making this bot ;)", "Russians should stop abusing things that are bugged. Report it.",
                     "Munbalanced should stop commenting about PvP related forums suggestion posts.", "Fu Wind should get out of the server.",
                     "Unban the old players."]
     fate = random.randint(0,10)
     if not fate == 3:    
         response = requests.get(adviceUrl)
         if response.status_code == 200:
             advice = json.loads(response.content.decode('utf-8'))['slip']['advice']
             await self.bot.say('<@%s>, `%s`' % (sender.id, advice))
         else:
             await self.bot.say("<@%s>, there's something wrong with the advice's API server" % sender.id)
     else:
         advice = random.choice(memeAdvices)
         await self.bot.say('<@%s>, `%s`' % (sender.id, advice))
     
 # urban dictionary meaning of a word.
 @commands.command(pass_context=True)
 async def urban(self, ctx, *, term: str):
     sender = ctx.message.author
     if term:
         # urbanURL = "https://www.urbandictionary.com/define.php?term=%s" % (term)
         urbanURL = "http://api.urbandictionary.com/v0/define?term=%s" % (term)
         response = requests.get(urbanURL)
         if response.status_code == 200:
             meaning = json.loads(response.content.decode('utf-8'))
             # print(meaning['list']) # definitions
             # meaning[list][0]['definition'] # definition one on index 0
             if len(meaning['list']) == 0:
                 await self.bot.send_message(ctx.message.channel, "There's no urban meaning for this word: `%s`" %(term))
             else:
                 tags = ""
                 for tag in meaning['tags']:
                     tags += tag + " | "

                 counter = 0
                 for definition in meaning['list']:
                     embed = discord.Embed(title=definition['word'], description="Urban Dictionary", colour=0x32CD32)
                     embed.add_field(name="Tags:", value=tags, inline=False)
                     embed.add_field(name="Author:", value=definition['author'], inline=False)
                     embed.add_field(name="Likes :thumbsup:", value=definition['thumbs_up'], inline=True)
                     embed.add_field(name="Dislikes :thumbsdown:", value=definition['thumbs_down'], inline=True)
                     embed.add_field(name="Definition:", value="```"+definition['definition']+"```", inline=False)
                     embed.add_field(name="Example:", value="`"+definition['example']+"`" if definition['example'] else "", inline=False)
                     embed.set_footer(text="All definitions based on urbandictionary.com")
                     await self.bot.send_message(ctx.message.channel, embed=embed)
                     counter += 1
                     if counter >= 3:
                      break
         else:
             await self.bot.send_message(ctx.message.channel, "Urban dictionary's API service is not available.")

     elif term == None:
         await self.bot.send_message(ctx.message.channel, "Please give me a term to look for...")


 # gives an instruction for soft ether vpn.
 @commands.command(pass_context=True)
 async def vpn(self, ctx):
     sender = ctx.message.author
     author = sender.mention
     embed = discord.Embed(title="", description="%s If you're unable to connect to the server or patch, and have reason to believe your Internet Service Provider might be at fault (Especially if you live in the Philippines), follow these instructions: \n http://www.vpngate.net/en/howto_softether.aspx" % (author))
     await self.bot.send_message(ctx.message.channel, embed=embed)

 # gives the url for NovaRO wiki
 @commands.command(pass_context=True)
 async def wiki(self, ctx):
     sender = ctx.message.author
     author = sender.mention
     embed = discord.Embed(title="", description="%s You can find the NovaRO wiki here!:\nhttps://novaragnarok.com/wiki/index.php?title=Main_Page" % (author))
     await self.bot.send_message(ctx.message.channel, embed=embed)

 # views the user's avatar
 @commands.command(pass_context=True)
 async def avatar(self, ctx, *,person: str = None):
  sender = ctx.message.author
  print(person)
  if person:
   server = ctx.message.server
   members = server.members
   for member in members:
    if member.name.lower() == person.lower() or person.lower() == member.display_name.lower() or person.lower() in member.name.lower():
     avatarLink = member.avatar_url
     embed = discord.Embed(title="%s's Avatar" %(member.name))
     embed.set_image(url=avatarLink)
     await self.bot.send_message(ctx.message.channel, embed=embed)
     break
    elif "<@" in person or "<@!" in person:
     user_id = person.strip('<@!>')
     if member.id == user_id:
      avatarLink = member.avatar_url
      embed = discord.Embed(title="%s's Avatar" %(member.name))
      embed.set_image(url=avatarLink)
      await self.bot.send_message(ctx.message.channel, embed=embed)
      break

  elif person == None:
   avatarLink = sender.avatar_url
   embed = discord.Embed(title="%s's Avatar" %(sender.name))
   embed.set_image(url=avatarLink)
   await self.bot.send_message(ctx.message.channel, embed=embed)

 # translates words from a foreign language into an english one.
 @commands.command(pass_context=True)
 async def translate(self, ctx, term: str, f: str):
     # f - from
     url_term = quote(term) # making the term URL friendly.
     sender = ctx.message.author
     translateURL = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&text=%s&lang=%s-en" % (translate_token, url_term, f)
     translating_msg = await self.bot.send_message(ctx.message.channel, "Transalating the word: **%s** from **%s** to en (English)." % (term, f))
     response = requests.get(translateURL)
     if response.status_code == 200:
         translation = json.loads(response.content.decode('utf-8'))
         await self.bot.delete_message(translating_msg)
         await self.bot.send_message(ctx.message.channel, "Translation [format: %s-en] of **%s** to its english meaning is: `%s`" % (f, term, translation['text'][0]))        
     else:
         await self.bot.delete_message(translating_msg)

 @commands.command(pass_context=True)
 async def quotes(self, ctx):
     quoteURL = "http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1"
     response = requests.get(quoteURL)
     if response.status_code == 200:
       quote = json.loads(response.content.decode('utf-8'))[0]
       quote_content = BeautifulSoup(quote['content'], "lxml").text
       await self.bot.send_message(ctx.message.channel, "```%s```\n - **%s**" % (quote_content, quote['title']))
     else:
         await self.bot.say("The quotes API site is currently down.")

 # retrieves the latest news from the forums
 @commands.command(pass_context=True)
 async def news(self, ctx, number: int = 0):
  sender = ctx.message.author
  waiting_message = await self.bot.send_message(ctx.message.channel, "**%s**, I'm fetching the NovaRO news...." % (sender.name))
  forum_news_url = "https://www.novaragnarok.com/forum/news/"
  result = session_requests.get(forum_news_url, headers = dict(referer = forum_news_url))
  content = result.text
  bSoup = BeautifulSoup(content, 'lxml')
  news_result_table = bSoup.find_all("span", attrs={"class":"ipsContained ipsType_break"})
  if not len(news_result_table) > 0:
   await self.bot.send_message(ctx.message.channel, "The forums is currently down. Can't find any news.")
  else:
   embed = discord.Embed(title="NovaRO News", description="All fresh from the forums.")
   if number == 0:
    counter = 0
    for news in news_result_table:
     counter += 1
     url = news.find('a', href=True)
     embed.add_field(name="%s. " % (str(counter)) + url.get_text().strip(), value="%s" % (url['href']), inline=False)
    await self.bot.send_message(ctx.message.channel, embed=embed)
   else:
    index = number - 1
    try:
     url = news_result_table[index].find('a', href=True)
     embed.add_field(name=url.get_text().strip(), value="%s" % (url['href']), inline=False)
     await self.bot.send_message(ctx.message.channel, embed=embed)
    except Exception as e:
     print(e)
     news_count = len(news_result_table)
     await self.bot.delete_message(waiting_message)
     await self.bot.send_message(ctx.message.channel, "The news is only %d at max number." % (news_count))
  await self.bot.delete_message(waiting_message)

 @commands.command(pass_context=True)
 async def number(self, ctx, number: int):
  sender = ctx.message.author
  number_trivia_url = "http://numbersapi.com/%d" % (number)
  response = requests.get(number_trivia_url)
  if response.status_code == 200:
   content = response.text
   await self.bot.send_message(ctx.message.channel, "%s, `%s`" % (sender.name, content))
  else:
   await self.bot.say("My number trivia brain is dead. Please tell Andie.")

# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MemberCog(bot))
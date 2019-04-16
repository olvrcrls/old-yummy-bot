import discord, asyncio, random, requests, json, time, os, subprocess
from discord.ext import commands
from discord.ext.commands import Bot
from pyquery import PyQuery
from lxml import html
from bs4 import BeautifulSoup
from yummy_token import novaUsername, novaPassword
from urllib.parse import quote
session_requests = requests.session()
class MiscCog:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def help(self, ctx):
		await self.bot.say("```Server member commands```\n" +
                  "`$sig` - **See your NovaRO character's signature. No need for the quotes inside your name if there are spaces!**\n" +
                  "`$charhead` - **Displays a NovaRO character's head.\n**" +
                  "`$char` - **Displays a NovaRO character sprite. Provide 'sit', 'back', 'sit back' for parameters.\n**" +
                  "`$ii` - **Get Item Information. Source is divine-pride.net**\n" +
                  "`$who` - **See the Hall of Famers.**\n" +
                  "`$choose` - **Yummy Bot will choose on the set of your choices provided.**\n" +
				  "`$gay` - **Tell someone that he/she is gay.**\n" +
                  "`$poke` - **Poke someone to annoy them with that ping without knowing it's you.\n**" +
                  "`$rms` - **The iconic !rms of NovaRO discord.\n**" +
                  "`$ask` - **Ask me about anything and I'll respond.\n**" +
                  "`$market` - **Looking up for the price/details on the NovaRO market on a specified item. Thanks to **Kyou** on this module.\n**" +
                  "`$dice` - **Rolls a die and gives out the value.\n**" +
                  "`$memes` - **Display random NovaRO related memes. Yummy might post it repeatedly though!\n**" +
                  "`$incant` - **DEN's promised incant!\n**" +
                  "`$say` - **Want to say something shady but you don't want anyone wanna know it's you. Use this\n**" +
                  "`$dogs` - **Displays random picture of a dog(s)\n**" +
                  "`$cats` - **Displays random picture of a cat(s)\n**" +
                  "`$birds` - **Displays random picture of a bird(s)\n**" +
                  "`$advice` - **I give a random advice for you. Might be memey.\n**" +
                  "`$urban` - **Look up for the urban meaning of a word.\n**" +
                  "`$news` - **Retrieves NovaRO's recent news from the forums.\n**" +
                  "`$number` - **I will tell you a trivia from the number you will give me.\n**" +
                  "`$vpn` - **NovaRO's soft ether instructions.\n**" +
                  "`$avatar` - **View a user's avatar.\n**" +
                  "`$calc` - **Simple calculator that can perform addition, subtraction, multiplication, and division.**\n" + 
                  "`$quotes` - **Gives out quotes from famous people.\n**" +
                  "`$summer` - **Summer Festival Schedule.\n**" +
                  "`$mh` - **Follow up the command with the set you want to see. E.g. $mh agi.\n**" +
                  "`$invite` - **I give you an invite link for me to come to your own server.\n**")
		await self.bot.say('\n\n\n**REMINDER**\n\n If your parameter has spaces on it. Please use `"text here"` for example: `$market "Abusive Robe"`')

	# gives the invite link for Yummy bot.    
	@commands.command(pass_context=True)
	async def invite(self, ctx):
	    sender = ctx.message.author
	    inviteURL = "https://discordapp.com/api/oauth2/authorize?client_id=456334689196834838&permissions=8&redirect_uri=https%3A%2F%2Fdiscordapp.com%2Foauth2%2Fauthorize%3Fclient_id%3D456334689196834838%26scope%3Dbot&response_type=code&scope=bot%20identify%20guilds%20guilds.join%20rpc.notifications.read%20messages.read%20connections"
	    await self.bot.say("Hey <@%s>, invite me to your own server or share me with your friends. \n**Here's my invite link:**\n %s" % (sender.id, inviteURL))

	# shows check response
	@commands.command(pass_context=True)
	async def check(self, ctx):
	    await self.bot.say("I'm online.")
      
	@commands.command(pass_context=True)
	async def resetmarket(self, ctx):
		waiting_message = await self.bot.send_message(ctx.message.channel, "Resetting the market connection....")
		payload = {"username": novaUsername, "password": novaPassword,"server":"NovaRO"}
		url = "https://www.novaragnarok.com/?module=account&action=login&return_url="
		result = session_requests.get(url)
		tree = html.fromstring(result.text)
		authenticity_token = list(set(tree.xpath("//input[@name='server']/@value")))[0]
		result = session_requests.post(url, data = payload, headers = dict(referer=url))
		if(result.status_code == 200):
			print("STATUS 200: NovaRO Website is ON")
		else:
			print("NovaRO Website is DOWN")
		url = "https://www.novaragnarok.com/?module=vending"
		result = session_requests.get(url, headers = dict(referer = url))
		if(result.status_code == 200):
			print("STATUS 200: NovaRO Market's Website is ON")
			await self.bot.send_message(ctx.message.channel, "Successfully reset the market functionality.")
		else:
			print("NovaRO Market's Website is DOWN")
			await self.bot.send_message(ctx.message.channel, "Failed to reset the market functionality. There's something wrong with the NovaRO website.")
		await self.bot.delete_message(waiting_message)

	@commands.group(pass_context=True)
	async def calc(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.send_message(ctx.message.channel, "Please provide an operation to be used...\nExample: `$calc or -calc <add, sub, mult, div> num1 num2`")

	@calc.command(pass_context=True)
	async def add(self, ctx, number1 : float = None, number2: float = None):
		sender = ctx.message.author
		if number1 != None and number2 != None:
			total = number1 + number2
			await self.bot.send_message(ctx.message.channel, "I added all the numbers you provided. It's **%d**." % (total))
		else:
			await self.bot.send_message(ctx.message.channel, "%s, Please provide two numbers to be added..." % (sender.name))

	@calc.command(pass_context=True)
	async def sub(self, ctx, number1 : float = None, number2: float = None):
		sender = ctx.message.author
		if number1 != None and number2 != None:
			total = number1 - number2
			await self.bot.send_message(ctx.message.channel, "I subtracted all the numbers you provided. It's **%d**." % (total))
		else:
			await self.bot.send_message(ctx.message.channel, "%s, Please provide two numbers to be in subtraction..." % (sender.name))

	@calc.command(pass_context=True)
	async def mult(self, ctx, number1 : float = None, number2: float = None):
		sender = ctx.message.author
		if number1 != None and number2 != None:
			total = number1 * number2
			await self.bot.send_message(ctx.message.channel, "I multiplied all the numbers you provided. It's **%d**." % (total))
		else:
			await self.bot.send_message(ctx.message.channel, "%s, Please provide two numbers to be multiplied..." % (sender.name))

	@calc.command(pass_context=True)
	async def div(self, ctx, number1 : float = None, number2: float = None):
		sender = ctx.message.author
		if number1 != None and number2 != None:
			try:
				total = number1 / number2
				await self.bot.send_message(ctx.message.channel, "I divided all the numbers you provided. It's **%d**." % (total))
			except Exception as e:
				print(e)
				await self.bot.send_message(ctx.message.channel, "That violates the law of Mathematics!")
		else:
			await self.bot.send_message(ctx.message.channel, "%s, Please provide two numbers to be divided..." % (sender.name))

	@commands.command(pass_context=True)
	async def summer(self, ctx):
		sender = ctx.message.author
		image_url = "https://media.discordapp.net/attachments/428465462096166918/463513492884946944/unknown.png?width=266&height=166"
		embed = discord.Embed(title="Summer Festival Schedule")
		embed.set_image(url=image_url)
		await self.bot.send_message(ctx.message.channel, embed=embed)

	@commands.group(pass_context=True)
	async def mh(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.send_message(ctx.message.channel, "Please provide the type of set which is currently available. E.g. `$mh agi`")

	@mh.command(pass_context=True)
	async def str(self, ctx):
		image_url = "https://cdn.discordapp.com/attachments/448319388630777877/463521281174798337/unknown.png"
		embed = discord.Embed(title="STR Shadow Set")
		embed.set_image(url=image_url)
		await self.bot.send_message(ctx.message.channel, embed=embed)

	@mh.command(pass_context=True)
	async def agi(self, ctx):
		image_url = "https://cdn.discordapp.com/attachments/448319388630777877/463521341966909440/unknown.png"
		embed = discord.Embed(title="AGI Shadow Set")
		embed.set_image(url=image_url)
		await self.bot.send_message(ctx.message.channel, embed=embed)

	@mh.command(pass_context=True)
	async def vit(self, ctx):
		image_url = "https://cdn.discordapp.com/attachments/448319388630777877/463521400523849760/unknown.png"
		embed = discord.Embed(title="VIT Shadow Set")
		embed.set_image(url=image_url)
		await self.bot.send_message(ctx.message.channel, embed=embed)

	@mh.command(pass_context=True)
	async def int(self, ctx):
		image_url = "https://cdn.discordapp.com/attachments/448319388630777877/509201499168178188/unknown.png"
		embed = discord.Embed(title="INT Shadow Set")
		embed.set_image(url=image_url)
		await self.bot.send_message(ctx.message.channel, embed=embed)

	@mh.command(pass_context=True)
	async def dex(self, ctx):
		image_url = "https://cdn.discordapp.com/attachments/448319388630777877/463521515229413396/unknown.png"
		embed = discord.Embed(title="DEX Shadow Set")
		embed.set_image(url=image_url)
		await self.bot.send_message(ctx.message.channel, embed=embed)

def setup(bot):
	bot.add_cog(MiscCog(bot))
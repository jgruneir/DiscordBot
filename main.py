import os
import discord
from dotenv import load_dotenv
import boto3
from cleverchat import cleverchat
from crosstext import crosstext
from handwriting import handwriting
from reactions import reactions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

allCopy = False
selfConvoCount = 0

dynamodb = boto3.resource('dynamodb', 'us-east-2')
table = dynamodb.Table('discord-react')

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')
	allCopy = False

@client.event
async def on_message(message):
	global allCopy

	if message.author == client.user:
		return

	#Turns on/off mode where all incoming messages are replaced with handwritten image versions.
	if message.content == "copy messages":
		allCopy = not allCopy
		if allCopy:
			await message.channel.send("copying")
		else:
			await message.channel.send("no longer copying")

	#Responds to messages targetted at the bot.
	elif '814903859683262474' in message.content and len(message.content.split(" ", 1)) > 1:
		chatText = message.content.split(" ", 1)[1]
		responseText = cleverchat.cleverChat(chatText)
		handwriting.createTextPicture(responseText)
		await message.channel.send(file=discord.File("out.jpg"))
		os.remove("out.jpg")

	elif "reset bot history" in message.content.lower():
		cleverchat.wipeConversation()
		await message.channel.send("conversation reset")

	elif message.content.lower().startswith("ctext down "):
		crosstext.handleDownCtext(message)
		await message.channel.send(file=discord.File("out.jpg"))
		os.remove("out.jpg")

	elif message.content.lower().startswith("ctext cross "):
		await crosstext.handleCrossCtext(message)
		await message.channel.send(file=discord.File("out.jpg"))
		os.remove("out.jpg")

	elif message.content.lower().startswith("ctext "):
		crosstext.handleNormalCtext(message)
		await message.channel.send(file=discord.File("out.jpg"))
		os.remove("out.jpg")

	elif message.content.lower().startswith("htext ") or allCopy:
		handwriting.createTextPicture(message.content.lower())
		await message.channel.send(file=discord.File("out.jpg"))
		os.remove("out.jpg")
		if allCopy:
			await message.delete()

	#Bot will converse with itself for given # of messages.
	elif message.content.lower().startswith("talk to self "):
		split = message.content.lower().split(" ")
		if len(split) != 4:
			await message.channel.send("give a #")
		elif split[3].isnumeric():
			selfConvoCount = int(split[3])
			await cleverchat.talkToSelf("starting", message, selfConvoCount)

	#Adds reaction.
	elif message.content.lower().startswith(".lacr "):
		split = message.content.lower().split(" ")
		if len(split) != 3:
			await message.channel.send(".lacr -text <response>")
		elif split[1][0] == '-':
			await reactions.addReact(split[1], split[2], message, table)

	#Deletes reaction.
	elif message.content.lower().startswith(".ldcr "):
		split = message.content.lower().split(" ")
		if len(split) != 2:
			await message.channel.send(".ldcr -text")
		elif split[1][0] == '-':
			await reactions.delReact(split[1], message, table)
			
	#Checks if input message is a trigger, if so, provides the response.
	try:
		reactLink = table.get_item(
			Key={
				'id': message.content
			}
		)['Item']['react']
		await message.channel.send(str(reactLink))
	except Exception as e:
		return

client.run(TOKEN)
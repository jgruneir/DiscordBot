import os
import requests
import discord
from dotenv import load_dotenv
from handwriting import handwriting

load_dotenv()
CLEVERBOT_APIKEY = os.getenv('CLEVERBOT_TOKEN')
currentConvo = ""


def cleverChat(chatText):
	'''Takes in text to send to bot, returns response. Uses chat history to frame answer.'''
	global currentConvo
	baseUrl = "https://www.cleverbot.com/getreply?key=" + CLEVERBOT_APIKEY
	baseUrl = baseUrl + "&input=" + chatText
	if currentConvo is not None and len(currentConvo) > 0:
		baseUrl = baseUrl + "&cs=" + currentConvo
	baseUrl = baseUrl + "&cb_settings_tweak3=0"
	response = requests.get(baseUrl)
	currentConvo = response.json()['cs']
	return response.json()['output']

async def talkToSelf(text, message, count):
	'''Takes in text to send to bot, and number of times to converse.
	Returns nothing, but posts messages in the chat talking to itself the given number of times.'''
	global currentConvo
	responseText = cleverChat(text)
	handwriting.createTextPicture(responseText)
	await message.channel.send(file=discord.File("out.jpg"))
	os.remove("out.jpg")
	count = count - 1
	if count > 0:
		await talkToSelf(responseText, message, count)

def wipeConversation():
	'''Resets the current chat history state of the bot.
	Useful when it gets itself into some weird rut or another language.'''
	global currentConvo
	currentConvo = ""
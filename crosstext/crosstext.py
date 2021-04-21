import math
from PIL import Image

recognizedChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890? _.-,:\""

def handleNormalCtext(message):
	'''Takes in a message, generates an image of that message in crossword form.'''
	files = []

	if message.content.lower().startswith("ctext "):
		msg = message.content[6:]

	for char in msg:
		if char in recognizedChars:
			if char == "_":
				files.append("resources/ctext/blank.jpg")
			elif char.isalpha():
				files.append("resources/ctext/" + char.lower() + ".jpg")

	images = [Image.open(x) for x in files]

	widths, heights = zip(*(i.size for i in images))
	max_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (max_width, max_height), (229, 224, 218))

	x_offset = 0
	rowNum = 0
	currHeight = 0

	for im in images:
		new_im.paste(im, (x_offset, max_height - im.height))
		x_offset += im.size[0]

	new_im.save('out.jpg')

async def handleCrossCtext(message):
	'''Takes in a message with 2 words, generates an image of that message crossed with the other.'''
	dim = Image.open("resources/ctext/blank.jpg")
	tileWidth = dim.width
	tileHeight = dim.height

	if message.content.lower().startswith("ctext cross "):
		msg = message.content[12:]

	split = msg.split()
	if len(split) != 2:
		await message.channel.send("Provide 2 words")
		return
	word1 = split[0]
	word2 = split[1]

	coord1, coord2 = findCross(word1, word2)
	if coord1 == "ERROR":
		await message.channel.send("No cross")
		return

	filesWord1 = []
	filesWord2 = []
	for char in word1:
		if char in recognizedChars:
			if char == "_":
				filesWord1.append("resources/ctext/blank.jpg")
			elif char.isalpha():
				filesWord1.append("resources/ctext/" + char.lower() + ".jpg")
	for char in word2:
		if char in recognizedChars:
			if char == "_":
				filesWord2.append("resources/ctext/blank.jpg")
			elif char.isalpha():
				filesWord2.append("resources/ctext/" + char.lower() + ".jpg")

	files = [[Image.open("resources/ctext/dBlank.jpg") for i in range(len(filesWord1))] for j in range(len(filesWord2))]

	for i in range(len(filesWord1)):
		files[coord2][i] = Image.open(filesWord1[i])
	for i in range(len(filesWord2)):
		files[i][coord1] = Image.open(filesWord2[i])

	max_width = tileWidth * len(filesWord1)
	max_height = tileHeight * len(filesWord2)

	new_im = Image.new('RGB', (max_width, max_height), (229, 224, 218))

	x_offset = 0
	rowNum = 0

	for row in files:
		for im in row:
			new_im.paste(im, (x_offset, rowNum * tileHeight))
			x_offset += im.width
		x_offset = 0
		rowNum = rowNum + 1

	new_im.save('out.jpg')

def handleDownCtext(message):
	'''Takes in a message, generates an image of that message in crossword form going down rather than across.'''
	files = []

	if message.content.lower().startswith("ctext down "):
		msg = message.content[11:]

	for char in msg:
		if char in recognizedChars:
			if char == "_":
				files.append("resources/ctext/blank.jpg")
			elif char.isalpha():
				files.append("resources/ctext/" + char.lower() + ".jpg")

	images = [Image.open(x) for x in files]

	widths, heights = zip(*(i.size for i in images))
	max_width = max(widths)
	max_height = sum(heights)

	new_im = Image.new('RGB', (max_width, max_height), (229, 224, 218))

	y_offset = -1 * (images[0].height)

	for im in images:
		new_im.paste(im, (0, y_offset + im.height))
		y_offset += im.height

	new_im.save('out.jpg')

def findCross(word1, word2):
	'''Given two words, finds the first location (in indices of each word) where they intersect on a letter.'''
	i1 = 0
	i2 = 0
	for c1 in word1:
		for c2 in word2:	
			if c1 == c2:
				return i1, i2
			else:
				i2 = i2 + 1
		i1 = i1 + 1
		i2 = 0
	return "ERROR", "ERROR"
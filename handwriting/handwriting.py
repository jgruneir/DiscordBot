import math
from PIL import Image

recognizedChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890? _.-,:\""

def createTextPicture(msg):
	'''Given a text message, generates an image of that text in handwritten form.'''
	files = []
	add = 0
	if msg.startswith("htext "):
		msg = msg[6:]
	if "g" in msg or "q" in msg or "y" in msg:
		add = 25
	for char in msg:
		if char in recognizedChars:
			if char == " ":
				files.append("resources/ltext/space.jpg")
			elif char == ".":
				files.append("resources/ltext/dot.jpg")
			elif char == "-":
				files.append("resources/ltext/dash.jpg")
			elif char == ",":
				files.append("resources/ltext/comma.jpg")
			elif char == ":":
				files.append("resources/ltext/colon.jpg")
			elif char == "?":
				files.append("resources/ltext/qmark.jpg")
			elif char == "\"":
				files.append("resources/ltext/quote.jpg")
			elif char.isalpha():
				files.append("resources/ltext/" + char.lower() + ".jpg")
			elif char.isnumeric():
				files.append("resources/ltext/" + char + ".jpg")

	images = [Image.open(x) for x in files]
	perRow = 15
	numRows = math.ceil(len(images) / perRow)
	rows = []
	for i in range(0, numRows):
		rows.append([])
	curr = 0

	imgCount = 0

	curRow = 0
	for image in images:
		if imgCount < perRow:
			rows[curRow].append(image)
			imgCount = imgCount + 1
		elif image.filename == "resources/ltext/space.jpg":
			curRow = curRow + 1
			imgCount = 0
		else:
			rows[curRow].append(image)
			imgCount = imgCount + 1

	rowsTemp = []
	for row in rows:
		if len(row) > 0:
			rowsTemp.append(row)
	rows = rowsTemp

	widths, heights = zip(*(i.size for i in images))
	total_width = sum(widths)
	max_height = max(heights)
	max_width = 0
	row_heights = []

	for row in rows:
		widths, heights = zip(*(i.size for i in row))
		total_width = sum(widths)
		max_height = max(heights)
		max_width = max(max_width, total_width)
		row_heights.append(max_height)

	new_im = Image.new('RGB', (max_width, sum(row_heights) + add), (229, 224, 218))

	x_offset = 0
	rowNum = 0
	currHeight = 0

	for row in rows:
		for im in row:
			if im.filename in ("resources/ltext/g.jpg", "resources/ltext/q.jpg", "resources/ltext/y.jpg"):
				new_im.paste(im, (x_offset, currHeight + row_heights[rowNum] - im.height + 25))
			else:
				new_im.paste(im, (x_offset, currHeight + row_heights[rowNum] - im.height))
			x_offset += im.size[0]
		x_offset = 0
		currHeight = currHeight + row_heights[rowNum]
		rowNum = rowNum + 1

	new_im.save('out.jpg')
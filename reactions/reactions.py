async def addReact(trigger, reaction, message, table):
	'''Takes a trigger and reaction and stores in the DB.
	After added, the bot will respond to the trigger with the reaction.'''
	table.put_item(
		Item={
			'id': trigger,
			'react': reaction
		}
	)
	await message.channel.send("added")

async def delReact(trigger, message, table):
	'''Takes a trigger and deletes that entry from the table.'''
	table.delete_item(
		Key={
			'id': trigger,
		}
	)
	await message.channel.send("deleted " + trigger)
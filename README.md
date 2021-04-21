## Personal Discord Bot

Don't expect anything too fancy, features generated on a want-to-have basis.

- Generate a message in handwritten text - YOU supply the PNGs for any character to be included as an option
	- Yes, I did photoshop 36+ letters/numbers/symbols from a handwriting sample
- Toggle the bot into a mode where it replaces EVERY incoming message in the server with a handwritten version
	- This is absolutely destructive
- Generate a message using crossword-style characters, either up or down
- Generate a message out of 2 words using crossword-style characters, one crossing the other
- Communicate with the bot via a cleverbot conversation
	- Have the bot have a conversation with itself for X number of messages
- Add a reaction for the bot to respond to a specific input with a specific output
	- The bot will respond to a trigger after it's added
	- Can delete these reactions as well

### Usage

If you really want this to work, you'll need the following:

1. Set up a Discord bot via their portal, provide the DISCORD_TOKEN in a .env file
2. For handwriting, you'll need image files for each letter, number, and character you want to work, in the location indicated in handwriting.py, all similar sizes, named a.jpg, b.jpg, etc
3. For crossword text, you'll need image files for each letter in a crossword box, similar to above
4. For cleverbot to work, you'll need to pay for some sort of subscription through the cleverbot portal, and provide the CLEVERBOT_TOKEN in the .env file 
5. For reactions, you'll need to setup a dynamoDB AWS instance and connect it, or use your own DB solution

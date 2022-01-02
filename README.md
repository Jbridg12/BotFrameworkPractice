# Volbot
Volbot is an implementation of a bot framework that uses a waterfall stack method to implement dialog.
The Volbot framework allows the user to create a bot by simply writing a dictionary and calling the 
Volbot constructor to start to start an instance. The Volbot has an internal HTTP server and a dialog manager 
that processes the user input and creates a response based on the dialog that the specific bot specifies.

The bot handles reactive messaging for when the user instantiates the conversation and creates a response accordingly,
as well as, proactive reminders. This means that if the user creates a bot, such as ReminderBot in the examples, that prompts
for a reminder, the bot will remind the user to perform the task specified in the time specified. These reminders must follow
the format "Remind me to [TASK] in [TIME] seconds."


# Dependencies
Volbot does not use any other external dependencies for it to work properly.


# How do I use the Volbots Framework?
In order to use the Volbots you need to first make a bot. To start you need create your bot 
file in the server directory and then make sure to include the volbot file at the top like so: 

	import lib.volbot as vb  

from here you just need to create the dictionary of the dialogs. The proper format for the dialogs
is as follows
	
	dialogs = {
		'[NAME]': {
			'type': 'reactive',
			'default': True | False,
			'waterfall': [
				String 1,
				String 2,
				String 3
			], 
		},
		
		...
	}
	
Make sure there is only one default dialog option and that if you want the name to match the user input
that you have the proper case sensitivity in the [NAME]. At the bottom of your bot just call the Volbot constructor 
in order to create a working bot.

In order to run the bot you will need Open two terminal windows. In one window navigate to the 
location of your bot and run "python [bot_name].py".In the other terminal window, navigate to 
the client folder and run "python html_server.py". You should now be capable of opening the Volbot 
interface by navigating to http://localhost:8080/ in your browser. From the Volbot browser page 
there are two user options provided for you. They do not change how the bots interact, just the 
user ID that the bot recieves. In the dialog box you can communicate with the bot as either of 
the users. The enter key does not work to submit the text so remember to click the send icon, and 
the text does not autoscroll, so if the text doesn't appear for you try scrolling down.


# Submission Info
- Joshua Bridges
- jbridg12
- 04/2/2021

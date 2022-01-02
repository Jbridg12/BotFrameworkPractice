#   file:   ReminderBot.py
#   name:   Josh Bridges
#   description:
#       this file implements a Volbot specification for a bot designed for 
#       reminding the user to do certain events.

import lib.volbot as vb

# Dialog for prompting and then scheduling user events.
# The dialog response to the first line is checked however,
# The second line assumes that the response to the first is always a reminder

dialogs = {
    'capture': {
        'type': 'reactive',
        'default': True,
        'waterfall': [
            "Hi! I\'m ReminderBot! What would you like me to remind you about?",
            "Got it. I\'ll remind you later."
        ]
    },
}

# create a new VolBot
ReminderBot = vb.VolBot('ReminderBot', dialogs)

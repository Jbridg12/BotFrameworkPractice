#   file:   comcastbot.py
#   description:
#       this file implements a Volbot specification for a bot designed for 
#       Comcast tech support.

import lib.volbot as vb

# The following is the dialog specification format that the VolBot framework should support.
# The keys, values, and types of this dictionary reflect the *correct* format. You should 
# use this dialog structure as inspiration for your other VolBot use-cases in Part 3.

dialogs = {
    'introduction': {
        'type': 'reactive',
        'default': True,
        'waterfall': [
            "Hi! My name is ComcastBot! What's your name?",
            "You said your name is: $lastMessage$"
        ], 
    },
    'help': {
        'type': 'reactive',
        'default': False,
        'waterfall': [
            "Hi! It sounds like you need help. What can I help you with?.",
            "Hmm. I don't think I know how to help with that. Please call our help line at 1-888-293-2910",
        ]
    },
}

# create a new VolBot
comcastBot = vb.VolBot('comcastBot', dialogs) 
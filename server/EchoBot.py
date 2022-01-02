#   file:   EchoBot.py
#   name:   Josh Bridges
#   description:
#       this file implements a Volbot specification for a bot designed for 
#       echoing user response.

import lib.volbot as vb


# Dialog for echoing back the user response as an "echoBot"
# Just one line is repeated over and over for each input
dialogs = {
    'echo': {
        'type': 'reactive',
        'default': True,
        'waterfall': [
            "You said: $lastMessage$"
        ]
    },
}

# create a new VolBot
EchoBot = vb.VolBot('EchoBot', dialogs) 

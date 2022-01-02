#   file:   volbot.py
#   name:   Josh Bridges
#   description:
#       this file implements a Volbot class structure to instantiate the bot designs.
#       It contains the constructor which takes the name, dictionary of dialogs and optionally
#       the hostname and port; and a validate_dialogs fuction that checks to make sure the dialogs are okay

import sys
from http.server import HTTPServer

import lib.server
import lib.manager

class VolBot():

    # Constructor
    def __init__(self, name, dialogs, hostname='localhost', port=9738):
        
        #assign passed dictionary to member variable
        self.dialogs = dialogs
        
        #Check if the dialog is in proper format, otherwise exit
        if self.validate_dialogs() == False:
            print('Invalid Dialog')
            exit()
        
        #create a member variable to instantiate a new dialog manager based on the bot's dictionary
        self.manager = lib.manager.DialogManager(dialogs)
        
        #Assign name
        self.name = name
        
        #Create a wrapper to alter the server constructor to allow it to pass a dialog manager as well as the hostname and port
        def serverWrapper(*args):
            lib.server.BotServer(self.manager, *args)
        
        # instantiate and start serving an HTTP server
        self.server = HTTPServer((hostname, port), serverWrapper)
        print("[SERVING] BotServer : http://%s:%s" % (hostname, port))

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass

        # close the server after we've hit a keyboard interrupt
        self.server.server_close()
        print("Server stopped.")
    
    #Instance function to validate the dialog dictionary
    def validate_dialogs(self):
    
        #copy member dialog to local variable
        dls = self.dialogs
        
        #Loop over the names of the dialog options
        for name in dls:
            
            #Save the contents of each name's values to local variable
            ele = dls[name]
            
            #Check that the type is eaither reactive or proactive
            if ele['type'] != 'reactive' and ele['type'] != 'proactive':
                return False
            
            #Check if the default value is a boolean
            elif not isinstance(ele['default'], bool):
                return False
            
            #Check if the waterfall is a list
            if isinstance(ele['waterfall'], list):
                
                #make sure it isn't empty
                if len(ele['waterfall']) < 1:
                    return False
                
                #check that each element in the list is a string
                for st in ele['waterfall']:
                    if isinstance(st, str):
                        continue
                        
                    else:
                        return False
                        
            else:
                return False
                
        #If they all succeed then it is a valid dialog        
        return True 
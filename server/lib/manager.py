#   file:   manager.py
#   name:   Josh Bridges
#   description:
#       this file implements a dialog manager to take user input and decide the appropriate
#       actions based on the dialog passed to the constructor


class DialogManager():

    # Constructor
    def __init__(self, dialogs):
    
        # Set dialog dictionary to member variable
        self.dialogs = dialogs
        
        # Stack implementation of message state and the related index to the message in a corresponding list
        self.state = []
        self.state_ind = []
        
        # List of reminders and the times assocaited with each one
        self.reminder = []
        self.reminder_time = []
        
    # Function to generate a response to a Post call.
    # Takes all the parameters of the message and an optional boolean for
    # if the message is a reminder
    def generate_response(self, user, type, msg, reminder=False):
        
        # Reponse to reactive messages
        if type == 'reactive':
            
            #If it is a reminder setting message, handle it
            if reminder:
                
                # Split the task and the time from the rest of the message string
                mp = msg.partition('to')[2]
                mpr = mp.rpartition('in')
                task = mpr[0]
                time = mpr[2].split()[0]
        
                # Append the proper format and time to the reminder array so that the indexes line update
                self.reminder.append('Hey! Here\'s your reminder to ' + task)
                self.reminder_time.append(int(time))
            
            # If the message is the name of a dialog option in the dictionary
            if msg in self.dialogs:
                
                # If the list is not empty then make sure the last message will get repeated
                if self.state:
                    self.state_ind[-1] -= 1
                
                # Get the message list and append it to the stack
                # Then append the starting index (0) to the index list for tracking
                key_name = self.dialogs[msg]
                self.state.append(key_name['waterfall'])
                self.state_ind.append(0)
                
                # Check if there is a certain format in the strings for echoing
                # and replace it with the last user message
                rm = self.state[-1][self.state_ind[-1]]
                if rm.find('$lastMessage$') > -1:
                    rm = rm.replace('$lastMessage$', msg)
                
                # Create the reponse message in JSON format
                response = {
                    'user' : user,
                    'msg' : rm
                }
                
                # Check if the waterfall list will be empty after this message and pop it if so
                if (self.state_ind[-1]+1) > (len(self.state[-1]) - 1):
                    self.state.pop()
                    self.state_ind.pop()
                    
            # If the stack is empty then handle that    
            elif not self.state:
                
                # Search the dialog to find the default waterfall
                for name in self.dialogs:
                    ele = self.dialogs[name]
                    if ele['default']:
                    
                        # And append it 
                        self.state.append(ele['waterfall'])
                        self.state_ind.append(0)
                
                # Check if there is a certain format in the strings for echoing
                # and replace it with the last user message
                rm = self.state[-1][self.state_ind[-1]]
                if rm.find('$lastMessage$') > -1:
                    rm = rm.replace('$lastMessage$', msg)
                
                # Create the reponse message in JSON format
                response = {
                    'user' : user,
                    'msg' : rm
                }
                
                # Check if the waterfall list will be empty after this message and pop it if so
                if (self.state_ind[-1]+1) > (len(self.state[-1]) - 1):
                    self.state.pop()
                    self.state_ind.pop()
                
            # Otherwise there is still dialog on the stack    
            else:
                
                # Increment the index since we are revisiting the list
                self.state_ind[-1] += 1
                
                # Check if there is a certain format in the strings for echoing
                # and replace it with the last user message
                rm = self.state[-1][self.state_ind[-1]]
                if rm.find('$lastMessage$') > -1:
                    rm = rm.replace('$lastMessage$', msg)
                
                # Create the reponse message in JSON format
                response = {
                    'user' : user,
                    'msg' : rm
                }
                
                # Check if the waterfall list will be empty after this message and pop it if so
                if (self.state_ind[-1]+1) > (len(self.state[-1]) - 1):
                    self.state.pop()
                    self.state_ind.pop()
            
            # Return the full dialog response
            return response
        
        # In this case the Post call is a proactive call
        else:
            
            # Decrement all time counters of the reminders by 1 second
            self.reminder_time = [item - 1 for item in self.reminder_time]
            
            # Find the index of a timestamp with 0 time left
            for i, j in enumerate(self.reminder_time):
                if j <= 0:
                    
                    # And return the reminder at the proper time 
                    response = {
                        'user' : user,
                        'msg' : self.reminder[i]
                    }
                    
                    # Then remove the reminder and its timestamp from the list
                    self.reminder.pop(i)
                    self.reminder_time.pop(i)
                    return response
            
            # If there are no reminders to trigger at the time, then return an empty response
            response = {
                'user' : user,
                'msg': '' # An empty 'msg' string tells the client UI that there are no proactive messages to handle.
            }
            return response
    
    # Function to determine if a user input is going to be a reminder 
    def parse_msg(self, msg):
    
        # Return true if the identifying substring, ignoring cases, is found
        if msg.lower().find('remind me to') > -1:
            return True
            
        # Otherwise return False    
        return False
#   file:   server.py
#   name:   Josh Bridges
#   description:
#       this file implements a Bot server designed to handle the post requests 
#       and interact with the dialog manager to fetch responses to user input.

from http.server import BaseHTTPRequestHandler
import socketserver
import time
import os
import urllib
import json
import codecs
import pprint

class BotServer(BaseHTTPRequestHandler):
    
    #New Constructor to augment BaseHTTPRequestHandler call
    def __init__(self, DialogManager, *args):
        
        #set dialog manager to a member variable
        self.DialogManager = DialogManager
        
        #pass the hostname and port to the http handler
        BaseHTTPRequestHandler.__init__(self, *args)
        
    def _set_headers(self):
        # WARNING: DO NOT TOUCH THIS CODE!
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()
        
    def do_HEAD(self):
        # WARNING: DO NOT TOUCH THIS CODE!
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()

        # A dummy list of recommendations and similarity scores.
        self.wfile.write(bytes(json.dumps({'hello': 'world', 'received': 'ok'}), 'utf-8'))
    
    # POST echoes the message adding a JSON field
    def do_POST(self):
        # read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        message = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)

        # Print out what we've received.
        print('-: "NEW MESSAGE :-')
        t = message[b'type'][0].decode('utf-8')
        u = message[b'user'][0].decode('utf-8')
        
        if t == 'reactive': # Reactive messages are chat messages.
            print('msg: ' + message[b'msg'][0].decode('utf-8'))
            
            # Get the actual message part
            m = message[b'msg'][0].decode('utf-8')
            
            # If the dialog is a reminder flag the call, otherwise pass it normally
            if self.DialogManager.parse_msg(m):
                respMsg = self.DialogManager.generate_response(u, t, m, True)
                
            else:    
                respMsg = self.DialogManager.generate_response(u, t, m)
            
        else:
            # Note: Proactive "messages" have no msg component, and we therefore have nothing to print.
            
            # msg is empty because proactives have no content
            respMsg = self.DialogManager.generate_response(u, t, '')
        
        # send the message back
        self._set_headers()
        self.wfile.write(bytes(json.dumps(respMsg), 'utf-8'))
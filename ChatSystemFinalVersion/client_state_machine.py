"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import aes

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.temp = ''
        self.key = ''
        self.storage = ''

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        elif response['status'] == 'refused':
            self.out_msg += 'You are refused to join the group'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    msg = json.dumps({"action":"connect", "target":peer})
                    mysend(self.s, msg)
                    self.out_msg += "Please wait while %s is confirming your request!\n"%peer

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    if peer_msg["status"] == "request":
                        self.peer = peer_msg["from"]
                        self.out_msg += 'You are connected with ' + self.peer
                        self.out_msg += '. Chat away!\n\n'
                        self.out_msg += '------------------------------------\n'
                        self.state = S_CHATTING
                        self.key = str(aes.AES_decrypt(peer_msg["key"],"ChatSystem"))
                    if peer_msg["status"] == "reject":
                        self.out_msg += "So bad! %s don't want to chat with you.\n"%peer_msg["from"]
                    if peer_msg["status"] == "busy":
                        self.out_msg += "%s is now busy, please try again later!\n"%peer_msg["from"]
                    if peer_msg["status"] == "self":
                        self.out_msg += "Can't connect to yourself!\n"
                    if peer_msg["status"] == "no-user":
                        self.out_msg += "No such user!\n"
                elif peer_msg["action"] == "confirm":
                    self.out_msg += peer_msg["from"] + " wants to connect with you. Please response 'y' or 'n'" 
                    self.temp = peer_msg["from"]
                    self.state = S_connecting_from_login

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:       # my stuff going out、
                my_msg1 = aes.AES_encrypt(my_msg,self.key)
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg1}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
        
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "confirm":
                    self.temp = peer_msg["from"]
                    self.out_msg += peer_msg["from"]+"wants to join your chatting. Type 'y' for accept, 'n' for reject:\n"
                    self.state = S_AMFROMCHATTING
                else:
                    peer_msg["message"] = str(aes.AES_decrypt(peer_msg["message"],self.key))
                    self.out_msg += peer_msg["from"] + peer_msg["message"]


            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
                
                
        elif self.state == S_connecting_from_login:
            if len(my_msg) > 0:
                if my_msg == 'y':
                    mysend(self.s, json.dumps({"action":"confirm", "status":"yes", "who":self.temp}))
                    self.temp = ''
                    self.state = S_LOGGEDIN
                elif my_msg == 'n':
                    mysend(self.s, json.dumps({"action":"confirm", "status":"no","who":self.temp}))
                    self.temp = ''
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += 'Invalid response. Please type "y" or "n"'
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    if peer_msg["status"] == "request":
                        self.peer = peer_msg["from"]
                        self.out_msg += 'You are connected with ' + self.peer
                        self.out_msg += '. Chat away!\n\n'
                        self.out_msg += '------------------------------------\n'
                        self.state = S_CHATTING
                        self.key = str(aes.AES_decrypt(peer_msg["key"],"ChatSystem"))
                    if peer_msg["status"] == "reject":
                        self.out_msg += "So bad! %s don't want to chat with you.\n"%peer_msg["from"]
                    if peer_msg["status"] == "busy":
                        self.out_msg += "%s is now busy, please try again later!\n"%peer_msg["from"]
                if peer_msg["action"] == "confirm":
                    mysend(self.s, json.dumps({"action":"confirm", "status":"busy", "who":peer_msg["from"]}))

        elif self.state == S_AMFROMCHATTING:
            
            if len(my_msg) > 0:
                if my_msg == "y":
                    mysend(self.s, json.dumps({"action":"confirm", "status":"yes", "who":self.temp}))
                    self.temp = ''
                    self.state = S_CHATTING
                    self.out_msg += self.storage
                    self.storage = ''
                elif my_msg == "n":
                    mysend(self.s, json.dumps({"action":"confirm", "status":"no","who":self.temp}))
                    self.temp = ''
                    self.state = S_CHATTING
                    self.out_msg += self.storage
                    self.storage = ''
                else:
                    self.out_msg += "Invalid input!\n"
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "confirm":
                    mysend(self.s, json.dumps({"action":"confirm", "status":"busy", "who":peer_msg["from"]}))
                elif peer_msg["action"] == "disconnect":
                    mysend(self.s, json.dumps({"action":"confirm", "status":"busy", "who":peer_msg["from"]}))
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                else:
                    peer_msg["message"] = str(aes.AES_decrypt(peer_msg["message"],self.key))
                    self.storage += peer_msg["from"] + peer_msg["message"] + "\n"

#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg

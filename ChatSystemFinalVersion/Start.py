# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox
from chat_client_class import *
import argparse
import threading
import json
import random
import game_new
import aes

class ChatSystem:
    
    def __init__(self,window):
        
        self.client = Client(args)
        self.client.init_chat()
        
        self.loggedin = False
        self.user_name = ''

        #init window
        self.window = window
        self.window.title("Billy, Sophia and Wendy's Chat System")
        self.window.geometry("1000x600+%d+%d"%(self.get_window_positon(1000, 600)))
        self.window.resizable(False, False)
        
        #init pages
        self.image_logo = tk.PhotoImage(file = '1575619342912.gif')
        self.initPage()
        
    def get_window_positon(self,width,height):
        
        return (self.window.winfo_screenwidth()-width)/2,(self.window.winfo_screenheight()-height)/2-30
    
    def getLoginStatus(self):
        return self.loggedin
    
    def getUserName(self):
        return self.user_name

    def initPage(self):  #
        
        #init login page
        self.var_usr_name= tk.StringVar()
        self.loginPage = tk.Frame(self.window,height=600,width=1000)
        
        #init main page
        self.mainPage = tk.Frame(self.window,height=600,width=1000)
        self.mainPageBarFrame = tk.Frame(self.mainPage,height=40,width=1000,background='#0E4F7B', highlightbackground = '#DDDDDD',highlightthickness=1)
        self.mainPageChatFrame = tk.Frame(self.mainPage,height=560,width=600,background='#EEEEEE',highlightbackground = '#DDDDDD',highlightthickness=1,highlightcolor='#DDDDDD')
        self.mainPageFunctionFrame = tk.Frame(self.mainPage,height=560,width=400,background='#FFFFFF',highlightbackground = '#DDDDDD',highlightthickness=1,)
        self.mainPageFunctionFrame_1 = tk.Frame(self.mainPageFunctionFrame,height=30,width=400,background='#FFFFFF',highlightbackground = '#DDDDDD',highlightthickness=1)
        self.mainPageFunctionFrame_2 = tk.Frame(self.mainPageFunctionFrame,height=486,width=400,background='#FFFFFF',highlightbackground = '#DDDDDD',highlightthickness=1)
        self.mainPageFunctionFrame_3 = tk.Frame(self.mainPageFunctionFrame,height=44,width=400,background='#FFFFFF',highlightbackground = '#DDDDDD',highlightthickness=1)
        self.mainPageChatFrame_1 = tk.Frame(self.mainPageChatFrame,height=30,width=600,background='#F7F7F7',highlightbackground = '#DDDDDD',highlightthickness=1)
        self.mainPageChatFrame_2 = tk.Frame(self.mainPageChatFrame,height=380,width=600,background='#F7F7F7',highlightbackground = '#DDDDDD',highlightthickness=1,bg="#EEEEEE")
        self.canvasTool = tk.Canvas(self.mainPageChatFrame_2,width=600,height=1380,background='#F7F7F7',highlightbackground = '#DDDDDD',highlightthickness=1,bg="#EEEEEE",scrollregion=(0,0,600,1380))

        
        self.userFrame = []
        self.userFrameName = []
        self.userFrameButton = []
        self.userFrameNameStr = []
        
        
        #start login page
        self.startLoginPage()

    def startLoginPage(self):  #
        
        #load frame
        self.loginPage.pack_propagate(0)
        self.loginPage.pack()
               
        #load logo
        canvas = tk.Canvas(self.loginPage,height=500,width=400)
        image = canvas.create_image(10,0,anchor = 'nw',image = self.image_logo)
        canvas.pack()
        
        #load label and entry
        l1 = tk.Label(self.loginPage,text = "Welcome to Billy, Sophia and Wendy's Chat System",font=("Arial",20)).place(x=300,y=370)
        l2 = tk.Label(self.loginPage,text = "User name:",font=("Hei",16)).place(x=360,y=450)
        self.entry_username = tk.Entry(self.loginPage,textvariable= self.var_usr_name)
        self.entry_username.place(x=460,y=450)
        self.entry_username.bind("<Return>",self.user_login_by_enter)
        self.entry_username.focus()
        
        #load login button
        btn_login = tk.Button(self.loginPage,text="Login",command = self.user_login,font=("Hei",16),height=2,width=8)
        btn_login.place(x=490,y=520)
        
    def user_login_by_enter(self,event):
        
        self.user_login()

    def user_login(self):  #

        user_name = self.var_usr_name.get()
        if user_name != '':
            if self.client.login(user_name) == True:
                self.user_name = user_name
                self.loginPage.destroy()
                self.startMainPage()
                self.loggedin = True
            elif self.client.system_msg == "Duplicate username, try again":
                
                a = tkinter.messagebox.askokcancel(title='Error username',message='This username has already been taken, you can take this suggestion: %s'%user_name+"1")
                    
        
    def user_logout(self):  #
        
        logout = tkinter.messagebox.askokcancel("Confirm","Are you sure to logout？")
        if logout == True:
            self.stopFreshWhoThread = True
            self.stopReceiveServerMessageThread == True
            self.user_name = ''
            self.restart()
            self.loggedin = False

    def startMainPage(self):  #
        
        #load frame
        self.mainPage.pack_propagate(0)
        self.mainPage.pack()
        self.mainPageBarFrame.pack_propagate(0)
        self.mainPageBarFrame.pack(side='top')
        self.mainPageChatFrame.pack_propagate(0)
        self.mainPageChatFrame.pack(side='left')
        self.mainPageFunctionFrame.pack_propagate(0)
        self.mainPageFunctionFrame.pack(side='right')
        self.mainPageFunctionFrame_1.pack_propagate(0)
        self.mainPageFunctionFrame_1.pack(side='top')
        self.mainPageFunctionFrame_3.pack_propagate(0)
        self.mainPageFunctionFrame_3.pack(side='bottom')
        self.mainPageFunctionFrame_2.pack_propagate(0)
        self.mainPageFunctionFrame_2.pack(side='left')
        
        #load labels and buttons
        l1 = tk.Label(self.mainPageBarFrame,text = "Chat System",font=("Nanum Gothic",24),background='#0E4F7B',fg='#FFFFFF').pack(side="left")
        btn_logout = tk.Button(self.mainPageBarFrame,text="Logout",command = self.user_logout,font=("Hei",16),height=1,width=8,background = '#D1EAFA',fg='#0E4F7B').place(x=910,y=8)
        l2 = tk.Label(self.mainPageBarFrame,text = "Welcome, %s"%self.user_name,font=("Arial",18),background='#0E4F7B',fg='#FFFFFF').place(x=805-len(self.user_name)*7,y=6)
        self.l3 = tk.Label(self.mainPageChatFrame,text = "Please connect somebody to start a chat or a group discussion",font=("Arial",16),background='#EEEEEE',fg="#AAAAAA")
        self.l3.place(x=100,y=200)
        l6 = tk.Label(self.mainPageFunctionFrame_1,background='#FFFFFF',text='Chat Space',font=("Arial",16),fg='#0E4F7B').pack(side='top')
        btn_logout = tk.Button(self.mainPageFunctionFrame_3,text="What time is it?",command = self.time,font=("Hei",16),height=2,width=14,background = '#FFFFFF',fg='#0E4F7B').pack(side='left')
        btn_logout = tk.Button(self.mainPageFunctionFrame_3,text="Read a poem",command = self.poem,font=("Hei",16),height=2,width=14,background = '#FFFFFF',fg='#0E4F7B').pack(side='right')
        btn_logout = tk.Button(self.mainPageFunctionFrame_3,text="Retro Snaker",command = self.game,font=("Hei",16),height=2,width=14,background = '#FFFFFF',fg='#0E4F7B').pack()
        
        self.stopFreshWhoThread = False
        self.startFreshingWho()
        self.stopReceiveServerMessageThread = False
        self.startReceivingServerMessage()
        
        self.state = "alone"
        self.peer = ""
           
    def addUser(self,user_name):  #
        
        self.userFrame.append(tk.Frame(self.mainPageFunctionFrame_2,height=40,width=400,background='#FFFFFF',highlightbackground = '#DDDDDD',highlightthickness=1))
        
        self.userFrame[-1].pack_propagate(0)
        self.userFrame[-1].pack(side="top")
        self.userFrameName.append(tk.Label(self.userFrame[-1],background='#FFFFFF',text=user_name,font=("Arial",16),fg='#0E4F7B'))
        self.userFrameNameStr.append(user_name)
        self.userFrameName[-1].pack(side='left')
        name = self.userFrameNameStr[-1]
        self.userFrameButton.append(tk.Button(self.userFrame[-1],text="connect",command = lambda: self.connect(name,1),font=("Hei",16),height=1,width=8,background = '#FFFFFF',fg='#0E4F7B'))
        self.userFrameButton[-1].pack(side='right')
        if user_name[0:5] == "Group":
            groupName = user_name[7:]
            if self.user_name in groupName.split(","):
                self.userFrameButton[-1].config(text="disconnect",command = lambda: self.disconnect(self.peer,1),width = 10,fg="#0E4F7B")
        if user_name == self.peer:
            self.userFrameButton[-1].config(text="disconnect",command = lambda: self.disconnect(self.peer,1),width = 10,fg="#0E4F7B")
        print("add:",user_name)
                   
        
    def delUser(self,user_name):
        
        index = self.userFrameNameStr.index(user_name)
        self.userFrame[index].destroy()
        for i in range(index+1,len(self.userFrame)):
            self.userFrame[i].pack_forget()
            self.userFrame[i].pack(side="top")
        del self.userFrame[index]
        del self.userFrameName[index]
        del self.userFrameNameStr[index]
        del self.userFrameButton[index]
        print("del:",user_name)
        
        
    def handleMsg(self):  #
        
        peer_msg = json.loads(self.serverMessage)
        if peer_msg["action"] == "connect":
            if self.state == "alone":
                self.connect(peer_msg["from"],2)
            elif self.state == "chatting":
                self.connect(peer_msg["from"],3)
        elif peer_msg["action"] == "confirm":
            self.confirm(peer_msg["from"])
        elif peer_msg["action"] == "exchange":
            self.receive(peer_msg["message"],peer_msg["from"])
        elif peer_msg["action"] == "disconnect":
            self.disconnect("",2)
        elif peer_msg["action"] == "list":
            self.fresh()
        elif peer_msg["action"] == "sb_disconnect":
            self.sbDisconnect(peer_msg["who"])
       

    def lockChat(self):  #
        
        self.text.destroy()
        self.mainPageChatFrame.config(background='#EEEEEE')
        self.mainPageChatFrame_2.pack_forget()
        self.mainPageChatFrame_1.pack_forget()
        self.chatRoomName.destroy()
        self.l3.place(x=100,y=200)
        for i in self.messageFrameList:
            i.pack_forget()
            i.destroy()
        self.messageFrameList.clear()
    
    def unlockChat(self,name):  #
        
        self.l3.place_forget()
        self.mainPageChatFrame.config(background='#EEEEEE')
        self.text = tk.Text(self.mainPageChatFrame,height=6,width=650,highlightcolor='#DDDDDD',background='#F7F7F7',highlightbackground='#DDDDDD',font=("黑体",16),padx=12,pady=12)
        self.text.pack(side='bottom')
        self.mainPageChatFrame_1.pack_propagate(0)
        self.mainPageChatFrame_1.pack(side='top')
        self.chatRoomName = tk.Label(self.mainPageChatFrame_1,text = "Chat Room: %s"%(self.user_name+','+name),font=("Arial",16),background='#F7F7F7',fg="#0E4F7B")
        self.chatRoomName.pack(side='top')
        self.text.bind("<Return>",self.send)
        self.mainPageChatFrame_2.pack_propagate(0)
        self.mainPageChatFrame_2.pack(side = "left")
        self.messageFrameList = []
        '''
        vbar = tk.Scrollbar(self.canvasTool,orient="vertical")
        vbar.pack(side="right",fill="y")
        vbar.config(command=self.canvasTool.yview)
        self.canvasTool.config(yscrollcommand=vbar.set)
        self.canvasTool.pack_propagate(0)
        self.canvasTool.pack()
        '''
    
    def startFreshingWho(self): #
        
        thread_who = threading.Thread(target=self.freshWho)
        thread_who.daemon = True
        thread_who.start()

    def freshWho(self):

        while self.stopFreshWhoThread == False:
            self.client.send(json.dumps({"action":"list"}))
            time.sleep(2)    
        
    def fresh(self):
        
        try:
            logged_in = json.loads(self.serverMessage)["results"]
            list_temp = logged_in.split("\n")
            member = eval(list_temp[1])
            group = eval(list_temp[3])
            single = []
            groupList = []
            groupListStr = []
            print("member:",member)
            print("group:",group)
            print("peer:",self.peer)
            for i in member.keys():
                if member[i] == 0 and i != self.user_name :
                    single.append(i)
                if member[i] != 0 and i == self.peer:
                    single.append(i)
            print("single:",single)
            for i in group.values():
                groupList.append(i)
            for i in groupList:
                if len(i) == 2:
                    if self.user_name in i:
                        groupList.remove(i)
                if len(i) > 2:
                    if self.user_name in i:
                        single.remove(self.peer)
            for i in groupList:
                groupStr=  "Group: "
                for j in range(0,len(i)-1):
                    groupStr += i[j] + ","
                groupStr += i[-1]
                groupListStr.append(groupStr)
            for i in single:
                print("loop")
                if i not in self.userFrameNameStr:
                    self.addUser(i)
                    print("added")
            print("userFrameNameStr:",self.userFrameNameStr)
            for i in groupListStr:
                if i not in self.userFrameNameStr:
                    self.addUser(i)
            for i in self.userFrameNameStr:
                if i not in single and i not in groupListStr:
                    self.delUser(i)     
        except Exception as e:
            print(e)
            
            
    def startReceivingServerMessage(self):  #
        
        thread_receive = threading.Thread(target=self.ReceiveServerMessage)
        thread_receive.daemon = True
        thread_receive.start()
        
    def ReceiveServerMessage(self):
        
        while self.stopReceiveServerMessageThread == False:
            self.serverMessage = self.client.get_msgs()
            time.sleep(0.2)
            if len(self.serverMessage) > 0:
                self.handleMsg()
        
    def connect(self,name,step):  #
        
        if step == 1:
            if name[0:5] == "Group":
                name1 = name[7:]
                nameList = name1.split(",")
                msg = json.dumps({"action":"connect", "target":nameList[0]})
                self.client.send(msg)
                index = self.userFrameNameStr.index(name)
                self.userFrameButton[index].config(text="waiting",command = self._pass,fg="#CCCCCC")    
            else:
                msg = json.dumps({"action":"connect", "target":name})
                self.client.send(msg)
                index = self.userFrameNameStr.index(name)
                self.userFrameButton[index].config(text="waiting",command = self._pass,fg="#CCCCCC")
            
        if step == 2:
            peer_msg = json.loads(self.serverMessage)
            try:
                index = self.userFrameNameStr.index(name)
            except:
                
                j = 0
                for i in self.userFrameNameStr:
                    groupName = i[7:]
                    if name in groupName.split(","):
                        groupName1 = groupName
                        index = j
                        break
                    j += 1
            if peer_msg["status"] == "request":
                self.peer = peer_msg["from"]
                try:
                    self.unlockChat(groupName1)
                except:
                    self.unlockChat(self.peer)
                self.userFrameButton[index].config(text="disconnect",command = lambda: self.disconnect(self.userFrameNameStr[index],1),width = 10,fg="#0E4F7B")
                tkinter.messagebox.showinfo(title='',message="Connected with %s, Chat away!"%self.peer)
                self.key = str(aes.AES_decrypt(peer_msg["key"],"ChatSystem"))
                self.state = "chatting"
            if peer_msg["status"] == "reject":
                tkinter.messagebox.showinfo(title='',message="So bad! %s don't want to chat with you.\n"%peer_msg["from"])
                self.userFrameButton[index].config(text="connect",fg="#0E4F7B",command = lambda: self.connect(self.userFrameNameStr[index],1))
            if peer_msg["status"] == "busy":
                tkinter.messagebox.showinfo(title='',message="%s is now busy, please try again later!\n"%peer_msg["from"])
                self.userFrameButton[index].config(text="connect",fg="#0E4F7B",command = lambda: self.connect(self.userFrameNameStr[index],1))
            if peer_msg["status"] == "self":
                tkinter.messagebox.showinfo(title='',message="Can't connect to yourself!\n")
            if peer_msg["status"] == "no-user":
                tkinter.messagebox.showinfo(title='',message="No such user!\n")
                      
        if step == 3:
            peer_msg = json.loads(self.serverMessage)
            tkinter.messagebox.showinfo(title='',message="%s joined your chatting"%name)
            index = self.userFrameNameStr.index(name)
            self.userFrameButton[index].config(text="disconnect",fg="#0E4F7B",width=10,command = lambda: self.disconnect("",1))
            self.chatRoomName.config(text=self.chatRoomName["text"]+",%s"%name)
            
                
    def confirm(self,from_):
        
        accept = tkinter.messagebox.askyesno("","%s wants to chat with you Accept?"%from_)
        if accept == True:
            self.client.send(json.dumps({"action":"confirm", "status":"yes", "who":from_}))
        if accept == False:
            self.client.send(json.dumps({"action":"confirm", "status":"no", "who":from_}))
         
    def disconnect(self,name,step):  #
        
        if step == 1:
            msg = json.dumps({"action":"disconnect"})
            self.client.send(msg)
            try:
                index = self.userFrameNameStr.index(self.peer)
            except:
                j = 0
                for i in self.userFrameNameStr:
                    groupName = i[7:]
                    if name in groupName.split(","):
                        groupName1 = groupName
                        index = j
                        break
                    j += 1
            self.userFrameButton[index].config(text="connect",command = lambda: self.connect(self.userFrameNameStr[index],1),width = 8,fg="#0E4F7B")
            self.peer = ""
            self.lockChat()
            tkinter.messagebox.showinfo(title='',message="You are disconnected with your peer")
            self.state = "alone"
        if step ==2:
            index = self.userFrameNameStr.index(self.peer)
            self.userFrameButton[index].config(text="connect",command = lambda: self.connect(self.userFrameNameStr[index],1),width = 8,fg="#0E4F7B")
            self.peer = ""
            self.lockChat()
            tkinter.messagebox.showinfo(title='',message="You are disconnected with your peer")
            self.state = "alone"
            
    def sbDisconnect(self,who):
        
        tkinter.messagebox.showinfo(title='',message="%s left your chat room"%who)
        text = self.chatRoomName["text"][11:]
        textList = text.split(",")
        textList.remove(who)
        newText = "Chat Room: "
        for i in range(0,len(textList)-1):
            newText += textList[i] + ","
        newText += textList[-1]
        self.chatRoomName.config(text=newText)
            
            
    def send(self,event):  #
        
        msg = self.text.get(0.0,'end')
        msg = msg[:-1]
        msg1 = aes.AES_encrypt(msg,self.key)
        self.text.delete(0.0,'end')
        self.text.mark_set("here", "0.0")
        self.client.send(json.dumps({"action":"exchange", "from":"[" + self.user_name + "]", "message":msg1}))
        if len(self.messageFrameList)*40 > 340:
            for i in self.messageFrameList:
                i.pack_forget()
                i.destroy()
            self.messageFrameList.clear()
        self.messageFrameList.append(tk.Frame(self.mainPageChatFrame_2,height=40,width=600,bg="#EEEEEE"))
        self.messageFrameList[-1].pack_propagate(0)
        self.messageFrameList[-1].pack(side="top")
        l = tk.Label(self.messageFrameList[-1],text=msg,font=("黑体",16),background='#1DC01D',fg='#FFFFFF').pack(side="right",padx=10)
        
    def receive(self,msg,from_name):  #
        
        msg1 = str(aes.AES_decrypt(msg,self.key))
        if len(self.messageFrameList)*40 > 340:
            for i in self.messageFrameList:
                i.pack_forget()
                i.destroy()
            self.messageFrameList.clear()
        self.messageFrameList.append(tk.Frame(self.mainPageChatFrame_2,height=40,width=600,bg="#EEEEEE"))
        self.messageFrameList[-1].pack_propagate(0)
        self.messageFrameList[-1].pack(side="top")
        l1 = tk.Label(self.messageFrameList[-1],text=from_name+":",font=("Arial",16),background='#EEEEEE',fg='#AAAAAA',highlightbackground = '#DDDDDD',highlightthickness=1,anchor="s").pack(side="left")
        l2 = tk.Label(self.messageFrameList[-1],text=msg1,font=("Arial",16),background='#FFFFFF',fg='#000000',highlightbackground = '#DDDDDD',highlightthickness=1,anchor="s").pack(side="left")

    def restart(self):
        
        #destroy all pages
        self.loginPage.destroy()
        self.mainPage.destroy()
        self.client.quit()
        
        #init
        self.client = Client(args)
        self.client.init_chat()
        self.initPage()
        
    def poem(self):
        
        poem_idx = str(int(random.random()*100))
        self.client.send(json.dumps({"action":"poem", "target":poem_idx}))
        poem = json.loads(self.client.recv())["results"]
        tkinter.messagebox.showinfo(title='poem',message=poem)
        
    def game(self):
        
        game_new.game()
        
    def time(self):
        
        self.client.send(json.dumps({"action":"time"}))
        time_in = json.loads(self.client.recv())["results"]
        time_in = str(time_in)
        time_in = time_in.split(",")
        tkinter.messagebox.showinfo(title='time',message="Today is %s\nTime is %s"%(time_in[0],time_in[1]))
        
    def _pass(self):
        
        pass
        
if __name__ == '__main__':  
    
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    window = tk.Tk()
    chatsystem = ChatSystem(window)
    window.mainloop()
    
    
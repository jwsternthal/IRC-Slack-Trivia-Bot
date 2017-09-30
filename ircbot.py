#!/usr/bin/python3
import socket

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net" # Server
channel = "#penguinhackers" # Channel
botnick = "YPH-Trivia-Test" # Bot's Nick
adminname = "EvilSon" # Your IRC User Name
exitcode = "bye " + botnick

ircsock.connect((server, 6667)) #Connect to server using 6667
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) #Filling Form out
ircsock.send(bytes("NICK "+botnick +"\n", "UTF-8")) #Assigning Nick to bot

def joinchan(chan): #join channels
    ircsock.send(bytes("JOIN " + chan +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") ==-1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping(): #Respond to Server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel): #sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ target +" :" + msg +"\n", "UTF-8"))

def main():
    joinchan(channel)
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
        if len(name) < 17:
            if message.find('Hi ' + botnick) != -1:
                sendmsg("Hello " + name + "!")
            if message[:5].find('.tell') != -1:
                target = message.split(' ',1)[1]
                if target.find(' ')!= -1:
                    message = target.split(' ')[1]
                    target = target.split(' ')[0]
                else:
                    target = name
                    message = "Could not parse. The message should be in the format of '.tell [target] [message]' to work properly."
                sendmsg(message, target)
            if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                sendmsg("oh... ok. :-()")
                ircsock.send(bytes("QUIT \n", "UTF-8"))
                return
        else:
            if ircmsg.find("PING :") !=-1:
                ping()

main()

#!/usr/bin/python3
import socket
import datetime

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "irc.freenode.net" # Server
channel = "#penguinhackers" # Channel
botnick = "TestBot-YPH" # Bot's Nick
adminname = "EvilSon" # Your IRC User Name
exitcode = "!die " + botnick

ircsock.connect((server, 6667)) #Connect to server using 6667
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) #Filling Form out
ircsock.send(bytes("NICK "+botnick +"\n", "UTF-8")) #Assigning Nick to bot
ircfile = ircsock.makefile()

def idx(lst, index, default=None):
    try:
        return lst[index]
    except IndexError:
        return default

def send_raw(msg):
    print("SEND: " + msg)
    ircsock.send(bytes(msg + "\r\n", "UTF-*"))

def joinchan(chan): #join channels
    send_raw("JOIN " + chan)

def ping(ping_ts): #Respond to Server Pings.
    send_raw("PONG " + ping_ts)

def sendmsg(msg, target=channel): #sends messages to the target.
    send_raw("PRIVMSG " + target + " :" + msg)

def main():
    ircmsg = ircfile.readline()
    awaiting_join = False
    while ircmsg != '':
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg.split(' '))
        event = idx(ircmsg.split(' '), 1, '')
        if event == '001':
            awaiting_join = True
            joinchan(channel)
        if event == '366' and awaiting_join:
            # Then you know the join was successful.
            awaiting_join = False
            sendmsg('Hey ' + adminname + 'I have arrived!')
        elif event == "PRIVMSG":
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
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
                sendmsg("Goodbye cruel world...")
                ircsock.send(bytes("QUIT \n", "UTF-8"))
                return
        elif event == "PING":
            ping_ts = idx(ircmsg.split(' '), 2, '')
            ping(ping_ts)
        ircmsg = ircfile.readline()

main()

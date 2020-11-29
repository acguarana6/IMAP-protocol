#IMAP Server
#Alexandra Chin and Wabil Asjad

from socket import *
import json
import sys
from _thread import *
import threading

# print_lock = threading.Lock()

#Load mail server data 
with open('/Users/alexandrachin/Desktop/inboxes.json') as f:
  inboxes = json.load(f)
    

def threaded(c):
    '''Given a connection as input, this function handles the interaction between a 
    client and the server.'''
    listening = True 
    while listening:
        message, address = c.recvfrom(1024)
        #A0001 USER command receive
        #Client says hello and sends username and password
        #USER_cmd = 'A0001 USER "' + username + '" "' + password + '"\r\n'

        USER_info = str(message.decode())
        #confirm that command is A0001 USER
        info = USER_info.split()
        command = str(info[0])+ " " + str(info[1])
        if command == "A0001 USER":
            #authenticate user
            username = info[2]
            username = username[1:len(username)-1]
            if username not in inboxes:
                c.send('User not registered'.encode())
                c.close()
                break
            else: 
                c.send('200 OK for username'.encode())
                #CHECK 200 or 220
        else:
            c.send('Invalid command for A0001.'.encode())

        #A0002 SELECT INBOX receive
        message, addr = c.recvfrom(1024)
        INBOX_info = str(message.decode())
        info = INBOX_info.split()
        
        #confirm that command is A0002 SELECT INBOX
        command = info[0]+ " " + info[1] + " " +info[2]
        if command == "A0002 SELECT INBOX":
            #get information about user's inbox
            num_msgs = len(inboxes[username])
            emailsExist = str(num_msgs) + ' EXISTS'

            #calculating number of unread messages
            unread = 0
            for msg in range(num_msgs):
                if inboxes[username][msg][4] ==0:
                    unread+=1
            
            unreadMsgIndex = 0 
            #get index of first unread message
            for msg in range(num_msgs):
                if inboxes[username][msg][4] ==0:
                    unreadMsgIndex = msg
                    break

            emailsRecent = str(unread) + ' RECENT'
            sendingInformation = emailsExist + "\n" + emailsRecent
            fullsend = "200 OK \n" + sendingInformation
            c.send(fullsend.encode())
        else:
            c.send('Invalid command for A0002.'.encode())

        #A0003 FETCH 1 RFC822.SIZE
        message, addr = c.recvfrom(1024)
        FETCH_info = str(message.decode())
        if FETCH_info == 'No mail':
            #confirm that command is A0006 LOGOUT
            info = FETCH_info.split()
            command = info[0]+ " " + info[1]
            if command == "No mail":
                print('Logging out...')
                print("BYE "+ str(username)+ "@mymailserver IMAP4rev1 server terminating connection")
                c.send('200 OK'.encode())
                c.close()
                break
            else:
                c.send('Invalid command for Logout.'.encode())
        
        else:
            #A0003 FETCH 1 RFC822.SIZE continue as normal
            FETCH_info = str(message.decode())
            FETCH_info = FETCH_info.strip()
            FETCH_info = FETCH_info.split()
            FETCH_info = ' '.join(FETCH_info)
            print(FETCH_info)
            if FETCH_info == "A0003 FETCH 1 RFC822.SIZE":
                #get size of both header and body in bytes
                emailsize = sys.getsizeof(inboxes[username][msg][2]) + sys.getsizeof(inboxes[username][msg][3])
                print("1 FETCH RFC822.SIZE ("+ str(emailsize) +")")
                c.send('200 OK'.encode())
            else:
                c.send(FETCH_info.encode())
                c.send('Invalid command for A0003.'.encode())


            #A0004 FETCH 1 BODY[HEADER]
            message, addr = c.recvfrom(1024)
            HEADER_info = str(message.decode())
            HEADER_info = HEADER_info.strip()
            HEADER_info = HEADER_info.split()
            HEADER_info = ' '.join(HEADER_info)
            if HEADER_info == "A0004 FETCH 1 BODY[HEADER]":
                #get size of both header in bytes
                headersize = sys.getsizeof(inboxes[username][unreadMsgIndex][2])
                header = inboxes[username][unreadMsgIndex][2]
                print("1 FETCH RFC822.SIZE HEADER ("+ str(headersize) +")")
                c.send(header.encode())
            else:
                c.send('Invalid command for A0004.'.encode())

            
            #A0005 FETCH 1 BODY[TEXT]
            message, addr = c.recvfrom(1024)
            TEXT_info = str(message.decode())
            TEXT_info = TEXT_info.strip()
            TEXT_info = TEXT_info.split()
            TEXT_info = ' '.join(TEXT_info)
            #confirm that command is A0005 FETCH 1 BODY[TEXT]
            if TEXT_info == "A0005 FETCH 1 BODY[TEXT]":
                #get size of both header in bytes
                
                textsize = sys.getsizeof(inboxes[username][unreadMsgIndex][3])
                text = inboxes[username][msg][3]
                print("1 FETCH RFC822.SIZE ("+ str(textsize) +")")
                c.send(text.encode())

                #mark email as read
                inboxes[username][unreadMsgIndex][4] = 1 

                #commit data to official json file
                a_file = open("/Users/alexandrachin/Desktop/inboxes.json", "w")
                json.dump(inboxes, a_file)
                a_file.close()
            else:
                c.send('Invalid command for A0005.'.encode())


            #A0006 LOGOUT
            message, addr = c.recvfrom(1024)
            LOGOUT_info = str(message.decode())
            LOGOUT_info = LOGOUT_info.strip()
            LOGOUT_info = LOGOUT_info.split()
            LOGOUT_info = ' '.join(LOGOUT_info)
            if LOGOUT_info == "A0006 LOGOUT":
                print("BYE "+ str(username)+ "@mymailserver IMAP4rev1 server terminating connection")
                c.send('200 OK'.encode())
                listening = False
                break
            else:
                c.send('Invalid command for A0006.'.encode())

    c.close()

    

def Main(): 
    '''After creating a socket for the TCP connection, this function creates as many
    threads as necessary that will then handle the interaction with the client.'''

    #c is the socket that we are receving from now
    #need to update the recvfrom sockets to c.recvfrom(1024)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('192.168.1.3', 1055))
    serverSocket.listen(1)
    print('listening')

    threads = []

    socket_is_open = True 
    threadCounter = 0 
    thread_collection = [] 

    while True:
        #establish connect with client
        c, addr = serverSocket.accept()

        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # start a new thread and return its identifier
        print("STARTING NEW THREAD")
        
        start_new_thread(threaded, (c,))
    serverSocket.close()


if __name__ == '__main__':
    Main()
    print("You are done with checking your email!")
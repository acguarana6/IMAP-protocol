#IMAP Client
#Alexandra Chin and Wabil Asjad

from socket import *
import sys 

#what should the mail server be? 
mailserver = "192.168.1.3"
username = "hannah@mymailserver.com"
password = ""

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver,1055))
print('Connected to mymailserver.com')

#Get username from user
getting_username = True
while getting_username:
    username = input("Please enter your username: ")
    getting_username = False
    print("Authenticating...")


#Say hello and identify user
USER_cmd = 'A0001 USER "' + username + '" "' + password + '"\r\n'
clientSocket.send(USER_cmd.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] == "200":
    print("Welcome, " + username + "!")

elif recv[:3] != "200":
    print("200 reply not received from server.")

else:
    clientSocket.close()
    sys.exit('You are not registered with @mymailserver. Goodbye.')


# Ask for information

INBOX_cmd = "A0002 SELECT INBOX\r\n"
clientSocket.send(INBOX_cmd.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != "200":
    print("200 reply not received from server.")



#if user has no email then proceed to logout
if "0 EXISTS" in recv:
    print("You have no mail.")
    NOMAIL = 'No mail'
    clientSocket.send(NOMAIL.encode())
    print('Logging out...')               
    if recv[:3] != "200":
        print("200 reply not received from server.")
    #logout
    print("See you next time, "+ str(username)+ "!")
    clientSocket.close()

else:

    #A0003 FETCH 1 RFC822.SIZ
    # Ask for information, provide answers
    FETCH_cmd = "A0003 FETCH 1 RFC822.SIZE\r\n"
    clientSocket.send(FETCH_cmd.encode())
    print("sending command 3 ")
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != "200":
        print("200 reply not received from server.")


    #Ask for email header information
    FETCH_head = "A0004 FETCH 1 BODY[HEADER]\r\n"
    clientSocket.send(FETCH_head.encode())
    recv = clientSocket.recv(1024).decode()
    print('HEADER:')
    print(recv)

    #Ask for email body information
    FETCH_body = "A0005 FETCH 1 BODY[TEXT]\r\n"
    clientSocket.send(FETCH_body.encode())
    recv = clientSocket.recv(1024).decode()
    print('BODY:')
    print(recv)
    #wait until user says ok to continue so they can read the email
    isRunning = True
    while isRunning:
        user_input = input("Are you done reading this email? Enter 'Q' if you are finished. ")
        if user_input == 'q' or user_input == 'Q':
            print('Continuing to logout...')
            isRunning = False
        else:
            print("Please enter 'Q' if you are finished.")


#Logout of account
LOGOUT_cmd = "A0006 LOGOUT\r\n"
clientSocket.send(LOGOUT_cmd.encode())
recv = clientSocket.recv(1024).decode()
print("Logging out...")
print(recv)
if recv[:3] != "200":
    print("200 reply not received from server.")

print("See you next time, "+ str(username)+ "!")

clientSocket.close()


        

    
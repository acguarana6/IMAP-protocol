# imap-protocol
* Wellesley College CS242 Computer Networking - Final Project
* Authors: Alexandra Chin & Wabil Asjad
* VERSION: v1.0 October 17, 2020

Implement both SMTP and IMAP and allow for multiple clients to be users on the same mail server. Multiple clients can access their email accounts and see the read and unread mail sent to them. They can also send mail to other clients that have addresses in the same mail server.

## Installation
Either use git clone, or download the files as a zip.

```cd``` to wherever this local repository is.

## Usage

* Please make sure to change the IP address to your IP address in the server file, and write the correct path to wherever you’ve downloaded the inboxes.json file!
* Run all the files in different terminals.
* As the IMAP client, run the commands that allow you to authenticate (A0001 USER) with your username (alex@mymailserver.com, wabil@mymailserver.com),
* Get information from your inbox (A0002 SELECT INBOX), if there are any unread emails you can use (A0003 FETCH 1 RFC822.SIZE) to get the size of the email, as well as (A0004 FETCH 1 BODY[HEADER]) and (A0005 FETCH 1 BODY[TEXT]) to see the header and the actual text in the body of the email.
* Finally, to log out you can use A0006 LOGOUT.

## Limitations and Improvements
* Establish a database for user emails and passwords.
* Using password hashing for security.

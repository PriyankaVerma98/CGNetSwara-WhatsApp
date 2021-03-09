#connects and interacts with database
import email, getpass, imaplib, os, sys
import datetime,quopri

from database import *
from utilities import *
from email.header import decode_header

detach_dir = './audio' 
config=ConfigParser.ConfigParser()
config.read("../tools/swara2.conf")
USERNAME = config.get("System","inboundgmail")
PASSWORD = config.get("System","inboundgmailpw")
SERVERNAME = config.get("System","servername")
NUMBER = config.get("System","phonenum")
user = USERNAME
pwd = PASSWORD

db = Database()	 

if __name__ == '__main__':
	user="UNKNOWN"
	location="UNKNOWN"
	timestamp="UNKNOWN"
	state = 1 

	auth=db.getAuthDetails(user)
	if auth == 0:
		auth=db.addAuthor(user)
	print(auth)
	# postid = db.addCommentToChannel(user, auth,'12345')
	getLatestPost()


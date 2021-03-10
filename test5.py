
#open incoming email, download file from link, add to database
# works for images and audios

import email, getpass, imaplib, os, sys
import datetime,quopri
from email.header import decode_header
from database import *
import re
import requests
import shutil
try:
	import urllib.request
except ImportError:
	import urllib2 


config=ConfigParser.ConfigParser()
config.read("./swara2.conf")
USERNAME = config.get("System","inboundgmail")
PASSWORD = config.get("System","inboundgmailpw")
emailuser = USERNAME
emailpwd = PASSWORD

db = Database()	 

if __name__ == '__main__':
	user="UNKNOWN"
	location="UNKNOWN"
	timestamp="UNKNOWN"
	state = 1 

	mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
	mail.login(emailuser,emailpwd)
	print("Logged in")

	mail.select("INBOX") 
	date = (datetime.date.today() - datetime.timedelta(int(sys.argv[1]))).strftime("%d-%b-%Y")

	searchstring = '(SINCE "'+ date+'" FROM "cgnet.sendgrid@gmail.com")'
	typ, data = mail.search('utf-8' , searchstring)
	id_list = data[0].split()

	for num in id_list:
		typ, data = mail.fetch(num, '(RFC822)' ) #"`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
		raw_email = data[0][1] # getting the mail content/ email body
		# converts byte literal to string removing b''
		raw_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(raw_email_string)

		subject=email_message["Subject"]
		print("Subject: " + subject)

		for part in email_message.walk():
			auth=db.getAuthDetails(user)
			if auth == 0:
				auth=db.addAuthor(user)
			postid = db.addCommentToChannel(user, auth,'12345')

			if part.get_content_type() == 'text/plain':
				text = (part.get_payload()) # prints the raw text
				index = text.find('https://')
				if(index == -1 ):
					continue
				url = text[index:]
				#the url was getting read with extra characters
				url = url.replace("\n","")
				url = url.replace("\r", "")
				url = url.replace("=","")
				print("url=" + url)
				filedata = urllib2.urlopen(url.encode("UTF-8"))
				datatowrite = filedata.read()
				#media = requests.get(url, stream = True) #bytes : does not work
				#media.raw.decode_content = True
				# print(media.headers.get('content-type')) #gives application/xml in all media formats

				if(subject == "Image"):
					extension = ".jpg"
					filename = str(postid)+extension
					#urllib2.urlretrieve(url, filename) # works only in python3
					
					#with open(filename, 'wb') as file: #not works
				   		# file.write(media.content)
					#	shutil.copyfileobj(media.raw, file)
					#file.close()

				elif(subject == "Audio"):
					extension = ".ogg"
					filename= str(postid) + extension
					
				else:
					print("don't have video link")
					extension = ".mpeg"
					continue
					#videoUrl wrong from IMI
				# with open("video1.mpeg", 'wb') as f:  
				# 	for chunk in media.iter_content(chunk_size = 1024*1024):  
				# 		if chunk:  
				# 			f.write(chunk) 
				
				with open(filename, 'wb') as f:
					f.write(datatowrite)








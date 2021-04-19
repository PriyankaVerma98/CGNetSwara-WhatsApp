#download all media while being in audiowiki directory 

#open incoming email and download file from link

import email, getpass, imaplib, os, sys
#os.chdir('/home/priyanka')
import datetime,quopri
from email.header import decode_header
from database import *
from utilities import *
import re
import ConfigParser
import requests
import shutil
try:
	import urllib.request
except ImportError:
	import urllib2 


config=ConfigParser.ConfigParser()
config.read("/etc/swara.conf")
USERNAME = config.get("WA","inboundgmail")
PASSWORD = config.get("WA","inboundgmailpw")
SERVERNAME = 'main'
emailuser = USERNAME
emailpwd = PASSWORD
down_dir = '/home/swara/audiowiki'
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
	#date = (datetime.date.today() - datetime.timedelta(int(sys.argv[1]))).strftime("%d-%b-%Y")

	searchstring = '(UNSEEN FROM "cgnet.sendgrid@gmail.com")'
	typ, data = mail.search('utf-8' , searchstring)
	id_list = data[0].split()
	print(id_list)
	for num in id_list:
		typ, data = mail.fetch(num, '(RFC822)' ) #"`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
		raw_email = data[0][1] # getting the mail content/ email body
		# converts byte literal to string removing b''
		raw_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(raw_email_string)

		#fromaddr=email_message["From"]
		subject=email_message["Subject"]
		#print("FROM: " + fromaddr)
		print("Subject: " + subject)
		print(num)
		user = subject.split('|')[1]
		user = user[3:]	
		# user = "9887777406"
		for part in email_message.walk():
			auth=db.getAuthDetails(user)
			if auth == 0:
				auth=db.addAuthor(user)
			#print("auth= ")
			print(auth)

			if part.get_content_type() == 'text/plain':
				text = (part.get_payload()) # prints the raw text
				#print("email text: "+ text)
				index = text.find('https://')
				if(index == -1 ):
					continue
				url = text[index:]
				url = url.replace("\n","")
				url = url.replace("\r", "")
				url = url.replace("=","")
				print("url=" + url)

				if(subject == "Image"):
					print("have not worked out images properly")
					print("thanks for patience")
					# postid = db.addCommentToChannel(user, auth,'12345', SERVERNAME, 1)
					# extension = ".jpg"
					# filedata = urllib2.urlopen(url.encode("UTF-8"))
					# datatowrite = filedata.read()
					# #media.raw.decode_content = True
					# filename = str(postid)+extension
					# filename = os.path.join(down_dir, filename)
					# with open(filename, 'wb') as f:
					# 	f.write(datatowrite)

				elif(subject.find("Audio") != -1):
					postid = db.addCommentToChannel(user, auth,'12345',SERVERNAME,1)
					indexx = url.rindex('.')
					extension = url[indexx:]
					filename= str(postid) + extension
					filename = os.path.join(down_dir, filename)
					filedata = urllib2.urlopen(url.encode("UTF-8"))
					datatowrite = filedata.read()
					with open(filename, 'wb') as f:
						f.write(datatowrite)
					nfilename= str(postid)+ ".wav"
					os.system("ffmpeg -i %s %s" %(filename, nfilename))
					os.system("ffmpeg -i %s %s.mp3" %(filename, str(postid)))
        				#os.system("rm %s" %(file))
					os.system("mv %s /home/swara/audiowiki/web/sounds" %(nfilename))
					os.system("mv %s.mp3 /home/swara/audiowiki/web/audio" %(str(postid)))
					os.system("mv %s audios" %(filename))
				
				else:	
					postid = db.addVideoCommentToChannel(user, auth,'12345', 'main', 1)
					print(postid)
					video_data = requests.get(url)
					filename = str(postid) +".mp4"
					with open(filename,'wb') as f:
						f.write(video_data.content)
					os.system("ffmpeg -i %s -map 0:a %s.mp3" %(filename,postid))
					print("conversion to audio succesful!")
					os.system("cp %s web/sounds/%s.mp4" %(filename,postid))
					os.system("cp %s.mp3 web/sounds/%s.mp3" %(postid, postid))
 					os.system("mv %s web/audio/%s.mp4" %(filename, postid))
					os.system("mv %s.mp3 web/audio" %(postid))

			mail.store(num, '+FLAGS', '\Seen')






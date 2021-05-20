#download all media while being in audiowiki directory 

#open incoming email and download file from link

# add features for moderator on mode : his number in interviewee

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
#	print("Logged in")

	mail.select("INBOX") 
	searchstring = '(UNSEEN FROM "cgnet.sendgrid@gmail.com")'
	typ, data = mail.search('utf-8' , searchstring)
	id_list = data[0].split()
	for num in id_list:
		typ, data = mail.fetch(num, '(RFC822)' ) #"`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
		raw_email = data[0][1] # getting the mail content/ email body
		# converts byte literal to string removing b''
		raw_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(raw_email_string)

		#fromaddr=email_message["From"]
		subject=email_message["Subject"]
		#print("FROM: " + fromaddr)
		#print("Subject: " + subject)
		#print(num)
		user = subject.split('|')[-1]
		user = user[3:]	
		
		#user is not entered properly
		for part in email_message.walk():
			auth=db.getAuthDetails(user)
			if auth == 0:
				auth=db.addAuthor(user)
			#print("auth= ")
		#	print(auth)

			if part.get_content_type() == 'text/plain':
				text = (part.get_payload()) # prints the raw text
				start_search =  0
				postid = 0
				text = text.replace("=","") #clean, else the url is read wrong
				text = text.replace("\n","")
				text = text.replace("\r", "")
				#print("email text: "+ text)
				
				if(subject.find("Image") != -1 ):
					# print("working on image")
					postid = db.addCommentToChannel(user, auth,'12345', SERVERNAME,0, 1) #adds audio entry
					#add the image_file in db
					extension = ".jpg"
				
					index = text.find('https')
					index_end = text.find('.jpg')
					url = text[index:index_end+4]
					
					start_search = index +1 ; #for associated video / audio

					filedata = urllib2.urlopen(url.encode("UTF-8"))
					datatowrite = filedata.read()

					filename = str(postid)+ extension
					# print("Image file= %s " %(filename))
					filename = os.path.join(down_dir, filename)
					filetype = "image/jpeg"
					with open(filename, 'wb') as f:
						f.write(datatowrite)
					filesize = os.stat(filename).st_size

					db.setImageFilename(postid, str(postid)+ ".jpg", filesize, filetype) #adds image entry in db
					os.system("cp %s /home/swara/audiowiki/web/audio" %(filename))
					os.system("mv %s /home/swara/audiowiki/web/sounds" %(filename))

				if(subject.find("Audio") != -1):
					index = text.find('https://',start_search ) #start_search is > 0 of image exists, else 0
					if(index == -1 ):
						continue
					url = text[index:]
					# print("Audio url=" + url)
					if(start_search == 0):
						postid = db.addCommentToChannel(user, auth,'12345',SERVERNAME,0, 1)
					#else postid came from image 
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
				
				elif(subject.find("Video") != -1):	
					index = text.find('https://', start_search)
					if(index == -1 ):
						continue
					url = text[index:]
					url = url.replace("\n","")
					url = url.replace("\r", "")
					url = url.replace("=","")
					# print("Video url=" + url)
					if(start_search == 0):
						postid = db.addVideoCommentToChannel(user, auth,'12345', 'main', 1)
					else:
						db.setVideoFilename(str(postid)+".mp4",postid) #adds image entry
					
					# print(postid)
					video_data = requests.get(url)
					filename = str(postid) +".mp4"
					filename = os.path.join(down_dir, filename)
					audio_filename = str(postid)+ ".mp3"
					audio_filename = os.path.join(down_dir, audio_filename)
					with open(filename,'wb') as f:
						f.write(video_data.content)
					os.system("ffmpeg -i %s -map 0:a %s" %(filename,audio_filename))
					#print("conversion to audio succesful!")
					os.system("cp %s /home/swara/audiowiki/web/sounds/%s.mp4" %(filename,postid))
					os.system("cp %s /home/swara/audiowiki/web/sounds/%s.mp3" %(audio_filename, postid))
 					os.system("mv %s /home/swara/audiowiki/web/audio/%s.mp4" %(filename, postid))
					os.system("mv %s /home/swara/audiowiki/web/audio" %(audio_filename))

			mail.store(num, '+FLAGS', '\Seen')






# open incoming email and download file from link

import email, getpass, imaplib, os, sys
import datetime,quopri
from email.header import decode_header
import re
import requests
import shutil

ach_dir = '/Users/PV/Desktop/Acads 5-2/codes/audio' 
user = "wacgnet76@gmail.com"	
pwd = "...." # put the actual one!

if __name__ == '__main__':
	mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
	mail.login(user,pwd)
	print("Logged in")

	mail.select("INBOX") 
	searchstring = '(FROM "ananya.saxena9716@gmail.com" SUBJECT "Fwd: Video")'
	typ, data = mail.search('utf-8' , searchstring)
	id_list = data[0].split()

	for num in id_list:
		typ, data = mail.fetch(num, '(RFC822)' ) #"`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
		raw_email = data[0][1] # getting the mail content/ email body
		# converts byte literal to string removing b''
		raw_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(raw_email_string)

		fromaddr=email_message["From"]
		subject=email_message["Subject"]
		print("FROM: " + fromaddr)
		print("Subject: " + subject)

		for part in email_message.walk():
			if part.get_content_type() == 'text/plain':
				text = (part.get_payload()) # prints the raw text
				print("email text: "+ text)
				index = text.find('https://')
				url = text[index:]
				print ("url= " +url)

				media = requests.get(url, stream = True) #bytes
				print(media.headers.get('content-type'))

				#for  images
				# media.raw.decode_content = True
				# with open('wa_image.jpg', 'wb') as file:
			 #   		# file.write(media.content)
				# 	shutil.copyfileobj(media.raw, file)
				# file.close()

				audio
				with open('wa_audio.ogg', 'wb') as file:
			   		file.write(media.content)
				# file.close()

				#videoUrl wrong from IMI
				# with open("video1.mpeg", 'wb') as f:  
				# 	for chunk in media.iter_content(chunk_size = 1024*1024):  
				# 		if chunk:  
				# 			f.write(chunk) 








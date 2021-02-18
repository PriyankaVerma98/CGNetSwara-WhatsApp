#connect to gmail server from my terminal 
# downloads one attachment from the selected email
# code source: https://medium.com/@sdoshi579/to-read-emails-and-download-attachments-in-python-6d7d6b60269


import email, getpass, imaplib, os, sys
import datetime,quopri
from email.header import decode_header

user = "vpriyanka0492@gmail.com"	
pwd = "fukutsu54321"

ach_dir = '/Users/PV/Desktop' 
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

mail.login(user,pwd)
print ("Logged in")
print (mail.list())
mail.select("INBOX")

searchstring='(SUBJECT "Fwd: Saikat <> Devansh")'


print (searchstring
)

typ, data = mail.search('utf-8' , searchstring)
mail_ids = data[0]
id_list = mail_ids.split()


# resp, items = mail.search('utf-8'	, searchstring) # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
# items = items[0].split() # getting the mails id
# print (items)

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
# converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
# downloading attachments
for part in email_message.walk():
    # this part comes from the snipped I don't understand yet... 
    if part.get_content_maintype() == 'multipart':
        continue
    if part.get('Content-Disposition') is None:
        continue
    fileName = part.get_filename()
    if bool(fileName):
        filePath = os.path.join('/Users/PV/Desktop' , fileName)
        if not os.path.isfile(filePath) :
            fp = open(filePath, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
        subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
        # print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=latest_email_uid.decode('utf-8')))


from finder import *
import pickle
import os.path
import requests
from hidden import SECRET
from sparkpost import SparkPost
from datetime import date
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid
class Sender:

    def __init__(self):
        self.finder = Finder()
        self.finder.get_list_of_cards_to_fetch()
        self.to_send = self.finder.get_cards_to_send()

    def send(self):
        body='<html>'
        print(len(self.to_send))
        # for k,v in self.to_send.items():
        #     body+=f'<img src="data:{k}/jpg;base64, {v}" />'
        # body+='</html>'
        


        try:
            server = smtplib.SMTP('smtp.gmail.com')
            server.ehlo()
            server.starttls()
            gmail_user = "alan.berman.92@gmail.com"
            gmail_password = SECRET
            server.login(gmail_user,gmail_password)
            sent_from = gmail_user
            to = gmail_user
            msg = MIMEMultipart()
            msg['Subject']= f'Spoilers for {date.today()}'
            msg['From']= gmail_user
            msg['To'] = gmail_user
            alt = "<html><body>"

            count = 0
            for k,v in self.to_send.items():
                alt+=f'<img src="{k}"><br/>'
                count+=1
            alt+="</body></html>"
     
            msg.attach(MIMEText(alt,'html','utf-8'))
            server.sendmail(sent_from,to,msg.as_string())
            server.close()
        except Exception(e):
            print("eish")
        
def main():
    sender = Sender()
    sender.send()

if __name__=='__main__':
    main()

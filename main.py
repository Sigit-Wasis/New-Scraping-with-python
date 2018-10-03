import requests 
from bs4 import BeautifulSoup
import mysql.connector
import scrapper
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url = "http://lpse.acehbaratkab.go.id/eproc/"

soup = scrapper.get(url)

# database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "123",
    database = "scrape"
)

mycursor = mydb.cursor()

find_title = soup.find('title').text
title = find_title.split(":")
tags = soup.find_all('a')

href = []

for t in tags:

    if "rumah sakit" in t.text.lower():
        href.append(url + "".join(t.attrs['href']))
    else:
        False

if len(href) > 0: 

    for links in href:
        mycursor.execute("SELECT link FROM link WHERE link = '%s'" % links)
        myresult = mycursor.fetchall()
    
    if mycursor.rowcount > 0:

        False

    else:

        sql = "INSERT INTO link (name, link) VALUES(%s, %s)"

        for link in href:
            val = [(title[0], link)]
            mycursor.executemany(sql, val)
            mydb.commit()


        fromaddr = "sigitghoticmetal2001@gmail.com" # email pengirim
        toaddr = "sigitwasisqodr2018@gmail.com" # email tujuan
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = title[0] # judul pesan

        for link in href:
            body = link+"\n"
            msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "jaringan") # password pengirim
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
else:

    False
from flask import Flask, request, render_template, send_file
from cryptography.fernet import Fernet
import sqlite3
import smtplib
import random
import string
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from binascii import a2b_base64
def getRandID(stringLength = 8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def initializeDatabase():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    sql_command = """
    CREATE TABLE requests_table (  
    requestID VARCHAR(40), 
    email VARCHAR(40),
    int1 INTEGER,
    int2 INTEGER
    );"""
    cursor.execute(sql_command)
    connection.commit()
    
def printTableContents():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    sql_command = """
    SELECT * FROM requests_table """
    cursor.execute(sql_command)
    print(cursor.fetchall())
# set up the SMTP server
smtpConnection = smtplib.SMTP(host='smtp.gmail.com', port=587)
smtpConnection.starttls()
smtpConnection.login('ejaybennett@gmail.com', '17Jaguars!6917046EB')
DB_NAME = "C:/Users/ejayb/ReallyYou/ReallyYou/requests.db"
#initializeDatabase()

#token = f.encrypt(b"A really secret message. Not for prying eyes.")

app = Flask(__name__)

@app.route('/',methods=['GET'])
def render_index():
    #s = open('index.html')
    #return s.read()
    if request.method == 'GET':
        print(render_template('index.html'))
        return render_template('index.html')
    #elif request.method == 'POST':
    #    return str(request.data)+str(request.args)+str(request.form)

@app.route('/getlink',methods=['GET'])
def give_link():
    emailAddress = str(request.args['email_input'])
    if(isEmail(emailAddress)):
        #uniqueID = ''
        #print('this method got called!')
        requestID = getRandID()#getRandRequestID()
        address = 'really-you.net/'+requestID
        int1 = int(1+ 5*random.random())
        int2 = int(1+ 5*random.random())
        #initializeDatabase()
        processRequest(emailAddress,requestID,int1,int2)
        return render_template('getlink.html', generatedLink = address)
    else:
        return render_template('index.html')
    
@app.route(
    '/favicon.ico',methods=['GET'])
def favicon():
    return send_file('static/favicon.ico')
@app.route('/<sendID>',methods=['GET'])
def acceptImagePage(sendID):
    print(sendID)
    printTableContents()
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    command = """SELECT int1, int2 FROM requests_table
    WHERE requestID = '{}'""".format(sendID)
    cursor.execute(command)
    int1,int2 = cursor.fetchone()
    print(int1)
    return render_template('verifyIdentity.html',sendID = sendID,
                           rightInt = int1, leftInt = int2)

@app.route('/<sendID>',methods=['POST'])
def acceptImage(sendID):
    f = open('C:/Users/ejayb/ReallyYou/ReallyYou/'+'{}.png'.format(sendID), 'wb')
    #f.write(a2b_base64(request.form['img'].split('a2b_base64')))
    header = 'data:image/png;base64,'
    if request.form['img'][0:len(header)] == header:
        f.write(a2b_base64(request.form['img'][len(header):]))
    f.close()
    processImageRecieve(sendID)
    return 'ok'

def processRequest(email,requestID,int1,int2):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    command = '''INSERT INTO requests_table
    VALUES ('{}', '{}', {}, {})'''.format(requestID,email,int1,int2)
    cursor.execute(command)
    connection.commit()


def processImageRecieve(requestID):
    print('processing image recieve')
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    command = """
    SELECT email, int1, int2 FROM requests_table
    WHERE requestID = '{}'""".format(requestID)
    cursor.execute(command)
    (address,int1,int2) = cursor.fetchone()
    sendSuccess = sendEmail(address,requestID, int1, int2)
    
    if(sendSuccess):
        command = """DELETE FROM requests_table
        WHERE requestID = {}""".format(requestID)
        cursor.execute(command)
        connection.commit()
    
    #remove from table here

def sendEmail(address,requestID, leftInt, rightInt):

    ownEmail = 'ejaybennett@gmail.com'
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'ReallyYou verification'
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = ownEmail
    msg['To'] = address
    htmlFile = open('C:/Users/ejayb/ReallyYou/ReallyYou/email.html','r')
    htmlTxt = htmlFile.read().format(rightInt,leftInt)
    msg.attach(MIMEText(htmlTxt,'html'))
    fp = open('C:/Users/ejayb/ReallyYou/ReallyYou/'+requestID+'.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    # Send the email via our own SMTP server.
    smtpConnection.sendmail(ownEmail, address, msg.as_string())
    return True

def isEmail(s):
    try:
        assert(s.count('@') == 1)
        a = s.split('@')
        name = a[0]
        addr = a[1]
        assert  3<=len(addr)<= 253
        assert 1<=len(name)<253
        assert(s.count('.')>=1)
        assert(not(' ' in addr) and not(' ') in name)
        return True
    except:
        return False

if __name__ == "__main__":
    app.run()

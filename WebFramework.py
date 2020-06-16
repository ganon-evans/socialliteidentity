from flask import Flask, request, render_template
from sql import *
from sql.aggregate import *
from sql.conditionals import *
from cryptography.fernet import Fernet
import sqlite3

# Put this somewhere safe!
key = b'Pk9Hx2eGaXe6pr_F4JcGQS50D8qBFykcNPFfDSchLO0='
f = Fernet(key)
#token = f.encrypt(b"A really secret message. Not for prying eyes.")

app = Flask(__name__)

@app.route('/',methods=['GET'])
def render_index():
    #s = open('index.html')
    #return s.read()
    if request.method == 'GET':
        return render_template('index.html')
    #elif request.method == 'POST':
    #    return str(request.data)+str(request.args)+str(request.form)

@app.route('/getlink',methods=['GET'])
def give_link():
    emailAddress = str(request.args['email_input'])
    #uniqueID = ''
    #print('this method got called!')
    address = 'really-you.net/'+emailAddress
    return render_template('getlink.html', generatedLink = address)
 
def processRequest(email,requestID):
    command = '''INSERT INTO requests_table
    VALUES ('%s', '%s')'''.format(email.requestID)
    cursor.execute(command)
    connection.commit()

def processEmailRecieve(requestID,img):
    command = """
    SELECT FROM requests_table
    WHERE requestID = %s"""

def initializeDatabase():
    connection = sqlite3.connect("requests.db")
    cursor = connection.cursor()
    sql_command = """
    CREATE TABLE requests_table (  
    requestID VARCHAR(40), 
    email VARCHAR(40),
    );"""
    cursor.execute(sql_command)
    connection.commit()

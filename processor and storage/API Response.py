from flask import Flask, send_file
import os

#returning a file from api request

#api setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretRandomKey' #validate api with a secret (string) key

#responding to the api sent from the GUI
@app.route('/log',  methods = ['GET', 'POST'])
def response():
    try: 
        os.system("python3 'Postgres to JSON.py'")
        return send_file('APIRequest.json', attachment_filename = 'APIRequest.json')
    except Exception as e:
        return str(e)
    
    #removing files to avoid duplicates and confusion
    os.remove('APIRequest.json')
    os.remove('send_to_arno')

if __name__ == '__main__':
    while True:
        app.run()
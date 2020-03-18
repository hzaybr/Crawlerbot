import json
import re
import ssl
import os
import sqlite3
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from gevent.pywsgi import WSGIServer
from crawler import crawler

app = Flask(__name__)

with open('config.json','r')as f:
    j = json.load(f)
line_bot_api = LineBotApi(j['access_token']) # Channel Access Token
handler = WebhookHandler(j['secret']) # Channel Secret

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] # get X-Line-Signature header value
    body = request.get_data(as_text=True) # get request body as text
    app.logger.info("Request body: " + body) # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Input = event.message.text
    try:
        url = re.search(r'(https?\:\/\/[\w\.\@\#\%\&\?]*\s?)', Input).group()
        title, content,  keywords = crawler(url.strip(), toFile=False)
        message = TextSendMessage(text=title+'\n---\n'+content+ '\n---\n'+' '.join([keyword for keyword in keywords]))
        line_bot_api.reply_message(event.reply_token, message)
        conn = sqlite3.connect('crawler.db')
        c = conn.cursor()
        c.execute("insert into CRAWLER (title, content, keywords) values (?, ?, ?)",
                  (title, content,' '.join([keyword for keyword in keywords])))
        conn.commit()
        conn.close()
    except:
        pass

if __name__ == "__main__":
    http_server = WSGIServer(('merry.ee.ncku.edu.tw', 1095), app, keyfile='../ssl/private.key', certfile='../ssl/certificate.crt', ca_certs='../ssl/ca_bundle.crt')
    http_server.serve_forever()

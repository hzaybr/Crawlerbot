import re
import ssl
import os
import json
import requests
import sqlite3
from datetime import datetime
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from flask import Flask, request, abort
from crawler import crawler
import ipynb_importer
from statisticsplot import gen_plot

app = Flask(__name__)

with open('config.json','r')as f:
    j = json.load(f)
line_bot_api = LineBotApi(j['access_token'])
handler = WebhookHandler(j['secret'])

@app.route('/bpitt', methods=['GET'])
def bpitt():
    event = request.args.get('event').replace('AaNnDd', '&')
    event = json.loads(event)

    userId = event['source']['userId']
    if event['source']['type'] == 'group':
        groupId = event['source']['groupId']
    else:
        groupId = userId
    profile = line_bot_api.get_profile(userId)
    displayName = profile.display_name
    if event['message']['type'] == 'text':
        text = event['message']['text']
    else:
        messageId = event['message']['id']
        get_file(messageId)
        text = messageId
    time = datetime.now()
    print(f"{displayName}\n{text}\n{time}")

    if text == 'image':
        conn = sqlite3.connect('crawler.db')
        cursor = conn.cursor()
        imagelink, deletehash = gen_plot(cursor)
        print(imagelink)
        replytype = 'image'
        replymessage = imagelink
    else:
        replytype = 'text'
        replymessage = '!!'
    replytoken = event['replyToken']
    r = requests.get(f"https://bpitt.herokuapp.com/reply?replytype={replytype}&replymessage={replymessage}&replytoken={replytoken}")

    to_database(displayName, text, time, groupId)
    return "ok"

def to_database(user, text, time, groupId):
    conn = sqlite3.connect('crawler.db')
    c = conn.cursor()
    source = ''
    try:
        url = re.search(r'(https?\:\/\/[\w\.\@\#\%\&\?\=\/]*\s?)', text)
        if not url:
            print("No url need to saved")
        else:
            url = url.group()
            url_raw = requests.get(url).text
            title, content,  keywords, source = crawler(url.strip(), toFile=False)
            c.execute("insert into CRAWLER (title, content, keywords, rawdata, time) values (?, ?, ?, ?, ?)",
                      (title, content,' '.join([keyword for keyword in keywords]), url_raw, time))
            conn.commit()
            print(f"data {title} saved")
    except Exception as e:
        print(e)
    c.execute("insert into raw_data (user, message, time, groupId, source) values (?, ?, ?, ?, ?)",
              (user, text, time, groupId, source))
    conn.commit()
    conn.close()
    print("raw data saved")

def get_file(messageId):
    message_content = line_bot_api.get_message_content(messageId)
    with open('file', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

if __name__ == "__main__":
    port = 1095
    app.run(host='merry.ee.ncku.edu.tw', port=port, ssl_context=('./ssl/server.crt', './ssl/private.key'))
    # http_server = WSGIServer(('merry.ee.ncku.edu.tw', port), app, keyfile='../../ssl/private.key', certfile='../../ssl/certificate.crt', ca_certs='../../ssl/ca_bundle.crt')
    print(f"listen on port {port}")
    # http_server.serve_forever()

# -*- encoding: utf-8 -*-

import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

from .load_data import load_data, load_access_token
from .getCalenderInformation import get_schedule

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = load_access_token
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is a bot api.")


def callback(request):
    reply = ""
    #  requestの情報をdic形式で取得
    request_json = json.loads(request.body.decode('utf-8'))
    for e in request_json['events']:
        # 返信先のトークンの取得
        reply_token = e['replyToken']
        # typeの取得
        message_type = e['message']['type']

        if message_type == 'text':
            # 受信メッセージの取得
            text = e['message']['text']
            # Lineにセリフを返す
            reply += reply_text(reply_token, text)

    return HttpResponse(reply)


def reply_text(reply_token, text):
    reply = ""
    if text.find('追加') > -1 or text.find('ついか') > -1:
        m_data = 'd';
    elif text.find('予定') > -1 or text.find('よてい') > -1:
        m_data = get_schedule()
        if not m_data:
            reply = '直近のイベントが見つかりませんでした。'
        else:
            for i in m_data:
                reply += '{}\n{}がありますよ！\n頑張ってください！\n'.format(i[0], i[1])
    elif text == '言語ガチャ':
        reply = random.choice(load_data)
    else:
        reply = 'まだ実装してないよ。'
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": reply
            }
        ]
    }

    # Lineにデータを送信
    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload))
    return reply

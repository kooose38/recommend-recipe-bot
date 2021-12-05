from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn
)
import os
import pandas as pd 
import numpy as np 

from search import find_similar_recipe
from db import request_post_user 

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 入力された単語を取得
    kwd = event.message.text 
    df, conf = find_similar_recipe(kwd)
    request_post_user(kwd)
    
    # テンプレートメッセージの作成
    notes = []
    for nrow in range(df.shape[0]):
        cols = CarouselColumn(thumbnail_image_url=df.iloc[nrow]["foodImageUrl"], 
                             title=df.iloc[nrow]["recipeTitle"], 
                             text=df.iloc[nrow]["recipeDescription"][:59],
                             actions=[{
                                 "type": "message",
                                 "label": "詳しく見る",
                                 "text": df.iloc[nrow]["recipeUrl"]                         
                             }])
        notes.append(cols)
        
    messages = TemplateSendMessage(
        alt_text="template",
        template=CarouselTemplate(columns=notes),
    )        
    line_bot_api.reply_message(
        event.reply_token,
        messages=messages)


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
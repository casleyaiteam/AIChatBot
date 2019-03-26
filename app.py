import os
import re

# Python Web framework
from flask import Flask, request, abort

# LINE API
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

# インスタンス化
app = Flask(__name__)

channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
channel_secret       = os.environ['LINE_CHANNEL_SECRET']
line_bot_api         = LineBotApi(channel_access_token)
handler              = WebhookHandler(channel_secret)

# LINEからPOSTリクエストが届いたときの処理
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = event.message.text)
    )
    return

if __name__ == "__main__":
    app.run()

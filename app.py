from flask import Flask, request, abort

from events.basic import *
from events.service import *
from line_bot_api import *



app = Flask(__name__)

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()

    if message_text == '@關於我們':
        about_us_event(event)

    elif message_text == '@營業據點':
        location_event(event)
    elif message_text == '@預約服務':
        service_category_event(event)


@handler.add(FollowEvent)        
def handle_follow(event):
    welcome_msg= """您好 ! 歡迎使用找屋DII, 找好屋都在這。
-想找優質乾淨的居住環境嗎?
-想找便宜低價的租屋嗎?  
-!!!!!這裡都有!!!!! 
-幫我留下姓名電話跟地點按下【預約服務】
-就會有專人聯繫你了喔!"""
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)
        
if __name__ == "__main__":
    app.run()

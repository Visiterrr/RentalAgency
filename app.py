from flask import Flask, request, abort
from events.basic import *
from events.service import *
from line_bot_api import *
from extensions import db, migrate
from models.user import User
from events.admin import *

import os


app = Flask(__name__)#admin: !QAZ2wsx資料庫的帳號和密碼
#讓程式自己去判斷如果是測試端就會使用APP_SETTINGS
app.config.from_object(os.environ.get('APP_SETTINGS','config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://userr:7tZfyeK42j5bvpkRUVqghp54EgHNgyjK@dpg-cjhm5rl1a6cs73955a80-a.singapore-postgres.render.com/reokroke'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app,db)

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


@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):

    message_text = str(event.message.text).lower()
    user = User.query.filter(User.line_id == event.source.user_id).first()#取得user的第一筆資料
    #如果沒有user的資料時,才會透過api去取得
    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)#line API中說明get_profile可以取得的資料
        print(profile.display_name)
        print(profile.user_id)#相同的好友會因為不同的profile而有不同的user_id
        print(profile.picture_url)

        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    print(user.id)
    print(user.line_id)
    print(user.display_name)


    if message_text == '@關於我們':
        about_us_event(event)

    elif message_text == '@營業據點':
        location_event(event)
    elif message_text == '@預約服務':
        service_category_event(event)
    #管理者的line id 可以去資料庫中取
    #開頭是*代表是管理者
    elif message_text.startswith('*'):
        if event.source.user_id not in ['']:
            return
        if message_text in ['*data','*d']:
            list_reservation_event(event)

#接收postback的訊息
#parse_qsl解析data中的資料
@handler.add(PostbackEvent)
def handle_postback(event):
    #把傳進來的event儲存在postback.data中再利用parse_qsl解析data中的資料然漚轉換成dict
    data = dict(parse_qsl(event.postback.data))
    #建立好def service_event(event) function後要來這裡加上判斷式
    #直接呼叫service_event(event)

    if data.get('action') == 'service':
        service_event(event)
    elif data.get('action') == 'select_date':
        service_select_date_event(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
    elif data.get('action') == 'confirm':
        service_confirm_event(event)
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event)

    #用get()來取得data中的資料，好處是如果備有data時會顯示None，而不會出線錯物


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
        
if __name__ == '__main__':
    app.run()

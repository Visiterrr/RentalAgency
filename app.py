from flask import Flask, request, abort
from events.basic import *
from events.service import *
from line_bot_api import *
from extensions import db, migrate
from models.user import User
from events.admin import *
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,StickerSendMessage,FollowEvent,UnfollowEvent
   )
from product import Products
from linebot.models import *
from models.user import Users
from database import db_session, init_db
from models.cart import Cart
from models.order import Orders
from models.item import Items
from config import Config
from models.linepay import LinePay
from urllib.parse import parse_qsl
import uuid

import os


app = Flask(__name__)#admin: !QAZ2wsx資料庫的帳號和密碼
#讓程式自己去判斷如果是測試端就會使用APP_SETTINGS
app.config.from_object(os.environ.get('APP_SETTINGS','config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://userr:zQIqLBm4Sy6MZl75YsPR5BgCXFwVQ0nr@dpg-ck2bpg821fec73akon3g-a/td_a4bv'
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
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id

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
    message_text = str(event.message.text).lower()
    cart = Cart(user_id= event.source.user_id)
    message = None

    print(user.id)
    print(user.line_id)
    print(user.display_name)


    if message_text == '@關於我們':
        about_us_event(event)

    elif message_text == '@營業據點':
        location_event(event)
    elif message_text == '@預約服務':
        service_category_event(event)
    elif message_text == '@我想重新預約':
        service_category_event(event)
    if message_text == '@使用說明':
        about_us_event(event)
    elif message_text in ['我想訂購商品', "add"]:
        message = Products.list_all()
    #當user要訂購時就會執行這段程式
    elif "i'd like to have" in message_text:
             
            product_name = message_text.split(',')[0] #利用split(',')拆解並取得第[0]個位置的值
            #例如COFFEE,I'D LIKE TO HAVE經過SPLIT(',')拆解並取得第[0]後位置就是COFFEE
            num_item = message_text.rsplit(':')[1]#同理產品就用(':')拆解取得第[1]位置的值
            #資料庫搜尋是否有這產品名稱
            product = db_session.query(Products).filter(Products.name.ilike(product_name)).first()
             #如果有這項產品就會加入
            if product:
                cart.add(product=product_name, num=num_item)
                #然後利用confirm_template的格式詢問用戶是否還要加入？
                confirm_template = ConfirmTemplate(
                    text='Sure, {} {}, anything else?'.format(num_item, product_name),
                    actions=[
                        MessageAction(label='Add', text='add'),
                        MessageAction(label="That's it", text="That's it")
                    ])
                message = TemplateSendMessage(alt_text='anything else?', template=confirm_template)
            else:
                #如果沒有找到產品名稱就會回給用戶沒有這個產品
                message = TextSendMessage(text="Sorry, We don't have{}.".format(product_name))
            
            print(cart.bucket())
    elif message_text in ['my cart','cart',"that's it"]:#當出現'my cart','cart',"that's it"時
        if cart.bucket():
            message = cart.display()
        else:
            message = TextSendMessage(text='Your cart is empty now.')
    if message:
        line_bot_api.reply_message(
        event.reply_token,
        message)

    #管理者的line id 可以去資料庫中取
    #開頭是*代表是管理者
    elif message_text.startswith('*'):
        if event.source.user_id not in ['U2aa57b9878cd6c1ced5aa3b82251dfae']:
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
    elif data.get('action') == 'cancel':
        service_cancel_event(event)
    #用get()來取得data中的資料，好處是如果備有data時會顯示None，而不會出現錯誤

    #print('action:',data.get('action'))
    #print('category:',data.get('category'))
    #print('service_id:', data.get('service_id'))
    #print('date:', data.get('date'))
    #print('time:', data.get('time'))








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
@handler.add(PostbackEvent)
def handle_postback(event):
    data = dict(parse_qsl(event.postback.data))#先將postback中的資料轉成字典
    action = data.get('action')#再get action裡面的值
    if action == 'checkout':#如果action裡面的值是checkout的話才會執行結帳的動作
        user_id = event.source.user_id#取得user_id
        cart = Cart(user_id=user_id)#透過user_id取得購物車
        if not cart.bucket():#判斷購物車裡面有沒有資料，沒有就回傳購物車是空的
            message = TextSendMessage(text='Your cart is empty now.')
            line_bot_api.reply_message(event.reply_token, [message])
            return 'OK'
        order_id = uuid.uuid4().hex#如果有訂單的話就會使用uuid的套件來建立，因為它可以建立獨一無二的值
        total = 0 #總金額
        items = [] #暫存訂單項目
        for product_name, num in cart.bucket().items():#透過迴圈把項目轉成訂單項目物件
            #透過產品名稱搜尋產品是不是存在
            product = db_session.query(Products).filter(Products.name.ilike(product_name)).first()
            #接著產生訂單項目的物件
            item = Items(product_id=product.id,
                         product_name=product.name,
                         product_price=product.price,
                         order_id=order_id,
                         quantity=num)
            items.append(item)
            total += product.price * int(num)#訂單價格 * 訂購數量
        #訂單項目物件都建立後就會清空購物車
        cart.reset()
        #建立LinePay的物件
        line_pay = LinePay()
        #再使用line_pay.pay的方法，最後就會回覆像postman的格式
        info = line_pay.pay(product_name='LSTORE',
                            amount=total,
                            order_id=order_id,
                            product_image_url=Config.STORE_IMAGE_URL)
        #取得付款連結和transactionId後
        pay_web_url = info['paymentUrl']['web']
        transaction_id = info['transactionId']
        #接著就會產生訂單
        order = Orders(id=order_id,
                       transaction_id=transaction_id,
                       is_pay=False,
                       amount=total,
                       user_id=user_id)
        #接著把訂單和訂單項目加入資料庫中
        db_session.add(order)
        for item in items:
            db_session.add(item)
        db_session.commit()
        #最後告知用戶並提醒付款
        message = TemplateSendMessage(
            alt_text='Thank you, please go ahead to the payment.',
            template=ButtonsTemplate(
                text='Thank you, please go ahead to the payment.',
                actions=[
                    URIAction(label='Pay NT${}'.format(order.amount),
                              uri=pay_web_url)
                ]))
        line_bot_api.reply_message(event.reply_token, [message])
    return 'OK'
@app.route("/confirm")
def confirm():
    transaction_id = request.args.get('transactionId')
    order = db_session.query(Orders).filter(Orders.transaction_id == transaction_id).first()
    if order:
        line_pay = LinePay()
        line_pay.confirm(transaction_id=transaction_id, amount=order.amount)
        order.is_pay = True#確認收款無誤時就會改成已付款
        db_session.commit()
        
        #傳收據給用戶
        message = order.display_receipt()
        line_bot_api.push_message(to=order.user_id, messages=message)
        return '<h1>Your payment is successful. thanks for your purchase.</h1>'
#初始化產品資訊
@app.before_first_request
def init_products():
    # init db
    result = init_db()#先判斷資料庫有沒有建立，如果還沒建立就會進行下面的動作初始化產品
    if result:
        init_data = [Products(name='Coffee',
                              product_image_url='https://i.imgur.com/DKzbk3l.jpg',
                              price=170,
                              description='nascetur ridiculus mus. Donec quam felis, ultricies'),
                     Products(name='Tea',
                              product_image_url='https://i.imgur.com/PRTxyhq.jpg',
                              price=150,
                              description='adipiscing elit. Aenean commodo ligula eget dolor'),
                     Products(name='Cake',
                              price=100,
                              product_image_url='https://i.imgur.com/PRm22i8.jpg',
                              description='Aenean massa. Cum sociis natoque penatibus')]
        db_session.bulk_save_objects(init_data)#透過這個方法一次儲存list中的產品
        db_session.commit()#最後commit()才會存進資料庫
        #記得要from models.product import Products在app.py

        
if __name__ == '__main__':
    init_products()
    app.run()

from line_bot_api import *
from urllib.parse import parse_qsl


services={
    1:{
        'category':'租屋',
        'img_url':  'https://i.imgur.com/ZLEUIqH.png',
        'title': '租屋(短期/長期)',
        'duration':'1hr',
        'description':'不用擔心找不到短期或長期的房子,這邊應有盡有',
        'price':5000,
        'post_url':'https://www.google.com.tw/?hl=zh_TW',
    },
    2:{
        'category':'買屋',
        'img_url': 'https://i.imgur.com/ZLEUIqH.png',
        'title': '買屋',
        'duration':'1hr',
        'description':'想買房嗎?給你最優惠的價格包你滿意!',
        'price':5000,
        'post_url':'https://www.google.com.tw/?hl=zh_TW',
    },
    3:{
        'category':'賞屋',
        'img_url': 'https://i.imgur.com/ZLEUIqH.png',
        'title': '賞屋',
        'duration':'1hr',
        'description':'還在猶豫嗎?那不如先來看房子吧!',
        'price':5000,
        'post_url':'https://www.google.com.tw/?hl=zh_TW',
    }
}
def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='請選擇想要的服務',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/ZLEUIqH.png',
                    action=PostbackAction(
                        label='租屋',
                        display_text='想租屋',
                        data='action=service&category=租屋'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/ZLEUIqH.png',
                    action=PostbackAction(
                        label='買屋',
                        display_text='想買屋',
                        data='action=service&category=買屋'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/ZLEUIqH.png',
                    action=PostbackAction(
                        label='賞屋',
                        display_text='想賞屋',
                        data='action=service&category=賞屋'
                    )
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [image_carousel_template_message])

def service_event(event):
    #底下三個要等上面的service建立後才寫,主要是跑service的服務
    #data=dict(parse_qsl)(event.postback.data)
    #bubbles=[]
    #for service_id in services:
    data=dict(parse_qsl(event.postback.data))

    bubbles = []

    for service_id in services:
        if services[service_id]['category'] == data['category']:
            service = services[service_id]
            bubble = {
              "type": "bubble",
              "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": service['img_url']
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": service['title'],
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                  },
                  {
                    "type": "text",
                    "text": service['duration'],
                    "size": "md",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "text": service['description'],
                    "margin": "lg",
                    "wrap": True
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": f"NT$ {service['price']}",
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "flex": 0
                      }
                    ],
                    "margin": "xl"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "action": {
                      "type": "postback",
                      "label": "預約",
                      "data": f"action=select_date&service_id={service_id}",
                      "displayText": f"我想預約【{service['title']} {service['duration']}】"
                    },
                    "color": "#b28530"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "了解詳情",
                      "uri": service['post_url']
                    }
                  }
                ]
              }
            }

            bubbles.append(bubble)

    flex_message =FlexSendMessage(
        alt_text='請選擇預約項目',
        content={
         "type":"carousel",
         "contents": bubbles

        })
    
    line_bot_api.reply_message(
        event.reply_token,
        [flex_message])
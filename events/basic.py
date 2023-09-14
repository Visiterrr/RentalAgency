from line_bot_api import *


def about_us_event(event):
    emoji = [
        {
            "index": 0,
            "productId": "5ac21184040ab15980c9b43a",
            "emojiId": "225"
        },
        {
            "index": 6,
            "productId": "5ac21184040ab15980c9b43a",
            "emojiId": "225"
        }
    ]

    text_message = TextSendMessage (text='''$ DII $
-全網最新：放上去的一定是最新圖片。

-搜尋方便：簡化操作介面，使用上一定很好理解。

-種類齊全：想找的房屋類型種類這裡都會有!

-隨約隨看：預約成功即可依日期時間賞屋!
                                    
-如有其他問題可以詢問工作人員(意見接受，態度照舊)''', emojis=emoji)
    
    sticker_message = StickerSendMessage(
        package_id='11538',
        sticker_id='51626517'
    )

    about_us_img = 'https://i.imgur.com/57FI7lK_d.jpg?maxwidth=520&shape=thumb&fidelity=high'

    image_message = ImageSendMessage(
        original_content_url=about_us_img,
        preview_image_url=about_us_img
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message, image_message])

def location_event(event):

    location_message = LocationSendMessage(
        title='DII',
        address='高雄市三民區三民路三民街三十三號',
        latitude=48.858001, 
        longitude=2.294812 )
    

    line_bot_api.reply_message(
        event.reply_token,
        location_message)
    



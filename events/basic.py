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

-嚴格把關：所有用品皆未消毒且是二手。

-設備齊全：內附10kg陶土設備不夠自己捏。

-獨立空間：四個人獨立一個空間!。''', emojis=emoji)
    
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
    



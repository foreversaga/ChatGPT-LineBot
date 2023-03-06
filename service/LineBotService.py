from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os, ChatGPTService as gptService

lineBotApi = LineBotApi(os.environ['LINE_BOT_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_BOT_CHANNEL_SECRET'])


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    print('Line message: ' + message)
    if '貓貓告訴我' in message:
        try:
            response = gptService.callDavinci(message.replace('貓貓告訴我', ''))
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text=response))
        except Exception as e:
            print(e)
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text='貓貓壞了，請稍後再試。'))
    elif '貓貓幫我' in message:
        try:
            response = gptService.callGTPTurbo(message.replace('貓貓幫我', ''))
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text=response))
        except Exception as e:
            print(e)
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text='貓貓壞了，請稍後再試。'))
    elif '貓貓畫' in message:
        try:
            imageUrl = gptService.callImage(message.replace('貓貓畫', ''))
            lineBotApi.reply_message(event.reply_token, ImageSendMessage(original_content_url=imageUrl, preview_image_url=imageUrl))
        except Exception as e:  
            print(e)
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text='貓貓壞了，請稍後再試。'))



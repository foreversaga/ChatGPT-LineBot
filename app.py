from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai, os

app = Flask(__name__)

# openai.api_key = os.environ['CHATGPT_API_KEY']
# lineBotApi = LineBotApi(os.environ['LINE_BOT_ACCESS_TOKEN'])
# handler = WebhookHandler(os.environ['LINE_BOT_CHANNEL_SECRET'])

# @app.route('/callback', methods=['POST'])
# def callback():
    
#     signature = request.headers['X-Line-Signature']
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     message = event.message.text
#     response = callChatGPT(message)
#     lineBotApi.reply_message(event.reply_token, TextSendMessage(text=response))

# def callChatGPT(message):
#     response = openai.Completion.create(
#     engine="text-davinci-003",
#     prompt=message,
#     temperature=0.7,
#     max_tokens=1024)

#     return response.choices[0].text

@app.route('/')
def hello():
    return "Hello World!"

app.run()
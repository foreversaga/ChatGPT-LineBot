from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai, os, json

app = Flask(__name__)

openai.api_key = os.environ['CHATGPT_API_KEY']
lineBotApi = LineBotApi(os.environ['LINE_BOT_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_BOT_CHANNEL_SECRET'])

@app.route('/callback', methods=['POST'])
def callback():
    
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print('Line request: ' + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    print('Line message: ' + message)
    if '貓貓告訴我' in message:
        try:
            response = callDavinci(message.replace('貓貓告訴我', ''))
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text=response))
        except Exception as e:
            print(e)
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text='貓貓壞了，請稍後再試。'))
    elif '貓貓幫我' in message:
        try:
            response = callGTPTurbo(message.replace('貓貓幫我', ''))
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text=response))
        except Exception as e:
            print(e)
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text='貓貓壞了，請稍後再試。'))

def callDavinci(message):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=message,
    temperature=0.7,
    max_tokens=1024)

    print('ChatGPT response: ' + response)
    return response.choices[0].text

def callGTPTurbo(message):
    messages = [{
        'content': message,
        'role': 'system'
    }]

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,
    max_tokens=1024)

    messageJson = json.dumps(response.choices)

    contents = map(lambda item: item['message']['content'], json.loads(messageJson))
    if len(contents) > 0:
        print('ChatGPT response: ' + messageJson)
        return '\n'.join(contents)
    else:
        return '這件事貓貓沒辦法幫你。'

@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/test', methods=['GET'])
def testChatGPT():
    
    message = request.args.get('message')
    response = callGTPTurbo(message)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 80))
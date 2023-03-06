from flask import Flask, request, abort
import os, service.ChatGPTService as gptService
import service.LineBotService as lineBotService

app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def callback():
    
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print('Line request: ' + body)
    try:
        lineBotService.handler.handle(body, signature)
    except lineBotService.InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/test', methods=['GET'])
def testChatGPT():
    
    message = request.args.get('message')
    response = gptService.callGTPTurbo(message)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 80))
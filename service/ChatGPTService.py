import openai, os, json

openai.api_key = os.environ['CHATGPT_API_KEY']

def callDavinci(message):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=message,
    temperature=0.7,
    max_tokens=1024)

    print('ChatGPT response: ' + json.dumps(response))
    aiMessage = response['choices'][0]['text'].split('\n\n')
    if len(aiMessage) > 1:
        return aiMessage[1]
    else:
        return aiMessage[0]

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

    contents = list(map(lambda item: item['message']['content'], json.loads(messageJson)))
    print(contents)
    if len(contents) > 0:
        print('ChatGPT response: ' + messageJson)
        return '\n'.join(contents)
    else:
        return '這件事貓貓沒辦法幫你。'

def callImage(prompt):
   response = openai.Image.create(
   prompt=prompt,
   n=1,
   size="1024x1024")
   image_url = response['data'][0]['url']
   print('Image response: ' + json.dumps(response))
   return image_url

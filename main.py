from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkApi
import os
from dotenv import load_dotenv
import requests
import json
import random

load_dotenv()

# ваш токен страницы ВК
vk_token = os.getenv('VK_TOKEN')
gpt_token = os.getenv('GPT_TOKEN')
url = "https://api.openai.com/v1/chat/completions"
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {gpt_token}'
}

vk_session = VkApi(token=vk_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        message = event.text
        print(f'{user_id} прислал сообщение\n {message}')

        data = {
            'model': 'gpt-3.5-turbo',  # или другая доступная модель
            'messages': [
                {
                    'role': 'system',
                    'content': 'Вы:'
                },
                {
                    'role': 'user',
                    'content': message
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            completion = response.json()
            for choice in completion['choices']:
                message_for_vk = choice['message']['content']
                print(message_for_vk)
                vk.messages.send(
                    user_id=user_id,
                    message=message_for_vk,
                    random_id=random.randint(1, 1000))
        else:
            print("Ошибка при отправке запроса: ", response.text)

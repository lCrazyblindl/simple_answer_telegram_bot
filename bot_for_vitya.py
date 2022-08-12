import random
import telebot
import requests as r


with open('apitoken.txt') as file:
    token = file.readline()

# получил токен от BotFather
bot = telebot.TeleBot(token)


def send_message():
    answers = ['Вот это да!', 'Ну ты дал!', 'Да, это жестко', 'Ты нормальный вообще?', 'Витя, осади',
               'Похоже, что ты снова победил меня', 'А как тебе такое?', 'Сам такой', 'Вот и поговорили',
               'Ты уверен?', 'Загадай число', 'Неверно', 'А ты хорош', 'Ты думаешь, что можешь тягаться со мной?',
               'И не говори', 'Ну и зачем?', 'Не делай так', 'Возможно ты и прав... но это не доказано'
               ]
    text = random.choice(answers)
    chat_id = -1001108188910
    params = dict(text=text, chat_id=chat_id)
    r.post(f'https://api.telegram.org/bot{token}/sendMessage', params=params)


def answer_vitya(used_message_id):
    updates = r.get(f'https://api.telegram.org/bot{token}/getUpdates')
    json_answer = updates.json()
    last_message_user_id = json_answer['result'][-1]['message']['from']['id']
    last_message_id = json_answer['result'][-1]['message']['message_id']
    if last_message_user_id == 345420795:
        send_message()
    return last_message_id


def main():
    params_for_clean = dict(drop_pending_updates=True)
    r.post(f'https://api.telegram.org/bot{token}/setWebhook', params=params_for_clean)
    updates = r.get(f'https://api.telegram.org/bot{token}/getUpdates')
    message_found = False
    while True:
        if not updates.json()['result']:
            updates = r.get(f'https://api.telegram.org/bot{token}/getUpdates')
        else:
            used_message_id = updates.json()['result'][-1]['message']['message_id']
            message_found = True
        if message_found:
            while True:
                used_message_id = answer_vitya(used_message_id)
                params_for_clean = dict(drop_pending_updates=True)
                r.post(f'https://api.telegram.org/bot{token}/setWebhook', params=params_for_clean)
                updates = r.get(f'https://api.telegram.org/bot{token}/getUpdates')
                message_found = False
                break


if __name__ == '__main__':
    main()

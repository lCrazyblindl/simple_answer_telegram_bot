import random
import telebot
import requests as r


with open('apitoken.txt') as file:
    token = file.readline()


# получил токен от BotFather
bot = telebot.TeleBot(token)


def get_bot():
    my_bot = r.get(f'https://api.telegram.org/bot{token}/getMe')
    return my_bot


def send_message():
    answers = ['Вот это да!', 'Ну ты дал!', 'Да, это жестко', 'Ты нормальный вообще?']
    text = random.choice(answers)
    chat_id = -1001108188910
    params = dict(text=text, chat_id=chat_id)
    r.post(f'https://api.telegram.org/bot{token}/sendMessage', params=params)


def answer_vitya(used_message_id):
    updates = r.get(f'https://api.telegram.org/bot{token}/getUpdates')
    json_answer = updates.json()
    last_message_user_id = json_answer['result'][-1]['message']['from']['id']
    last_message_id = json_answer['result'][-1]['message']['message_id']
    if last_message_user_id == 345420795 and last_message_id != used_message_id:
        send_message()
    return last_message_id


def main():
    updates = r.get(f'https://api.telegram.org/bot{token}/getUpdates')
    used_message_id = updates.json()['result'][-1]['message']['message_id']
    while True:
        used_message_id = answer_vitya(used_message_id)


if __name__ == '__main__':
    main()

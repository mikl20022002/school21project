import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from nlp_api import *

bot = telebot.TeleBot('7015330412:AAGOd6G_X0JVdHzahxA6yRxHznZ8FcYMVFI')

def get_balance(message):
    bot.send_message(message.chat.id, 'Ваш баланс 100100101')


def get_week_spent(message):
    bot.send_message(message.chat.id, 'Ваши траты за прошедшую неделю 1001100101')


def get_month_spent(message):
    bot.send_message(message.chat.id, 'Ваши траты за прошедший месяц 10001011')


def card_recreate(message):
    bot.send_message(message.chat.id, 'Отправил ваш запрос на перевыпуск карты в обработку. Сообщу вам как только карта будет готова.')


def top_up_account(message):
    bot.send_message(message.chat.id, '(перенаправление на окно пополнения счета)')


def unblock_card(message):
    bot.send_message(message.chat.id, 'Для разблокировки карты посетите отделение банка')


def get_statement(message):
    bot.send_message(message.chat.id, 'Я пришлю вам выписку как только она будет готова')


def set_up_notifications(message):
    bot.send_message(message.chat.id, '(перенаправление в окно настроек уведомлений)')


def find_nearest_atm_step1(message):
    bot.send_message(message.chat.id, "Отправьте вашу геолокацию, пожалуйста")
    bot.register_next_step_handler(message, find_nearest_atm_step2)

def find_nearest_atm_step2(message):

    # user_location = message.location
    # lat = user_location.latitude
    # lon = user_location.longitude
    #

    # url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1'
    # response = requests.get(url)
    # data = json.loads(response.text)

    # для реальной геолокации требуется найти APIшник, предоставляющий локацию банкоматов сбера
    atm_lat = 59.9390
    atm_lon = 30.3158

    bot.send_location(message.chat.id, atm_lat, atm_lon)




# region block card
def block_card_step1(message):
    markup = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton('ЗАБЛОКИРОВАТЬ', callback_data='block')
    markup.add(b1)

    bot.send_message(message.chat.id,
                     'Разблокировка будет доступна только при личном посещении отделения банка.\nВы действительно хотите заблокировать карту? ',
                     reply_markup=markup)

def block_card_step2(message):
    bot.send_message(message.chat.id, 'Карта заблокирована.')
# endregion


# region change card limit
def change_card_limit_step1(message):
    bot.send_message(message.chat.id, 'Какой лимит вы хотите установить?')
    bot.register_next_step_handler(message, change_card_limit_step2)

def change_card_limit_step2(message):
    bot.send_message(message.chat.id, 'Лимит установлен')
# endregion


# region card apply
def card_apply_step1(message):
    bot.send_message(message.chat.id, 'Пожалуйста, введите... (информация для карты №1)')
    bot.register_next_step_handler(message, card_apply_step2)


def card_apply_step2(message):
    bot.send_message(message.chat.id, 'Пожалуйста, введите... (информация для карты №2)')
    bot.register_next_step_handler(message, card_apply_step3)


def card_apply_step3(message):
    bot.send_message(message.chat.id, 'Спасибо! \nЯ отправил ваш запрос в обработку. \nНапишу вам как карта будет готова.')
# endregion


# region message handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '''Привет!\nЯ виртуальный ассистент, помогу тебе разобраться с любыми вопросами касательно твоего счета.\nЯ могу показать тебе траты за неделю или месяц, помочь настроить уведомления, произвести операции с картой такие как блокировка, пополнение счета или изменение лимитов. А можем просто поболтать (правда пока я не запоминаю истории сообщений)''')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    act_class = int(classify(message.text))
    if act_class == 10:
        get_balance(message)
    elif act_class == 11:
        get_week_spent(message)
    elif act_class == 12:
        get_month_spent(message)
    elif act_class == 13:
        card_apply_step1(message)
    elif act_class == 14:
        card_recreate(message)
    elif act_class == 15:
        top_up_account(message)
    elif act_class == 16:
        change_card_limit_step1(message)
    elif act_class == 17:
        block_card_step1(message)
    elif act_class == 18:
        unblock_card(message)
    elif act_class == 19:
        get_statement(message)
    elif act_class == 20:
        set_up_notifications(message)
    elif act_class == 21:
        find_nearest_atm_step1(message)
    elif act_class == 22:
        answer = talk(message.text)
        bot.send_message(message.chat.id, answer)

# endregion


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    text = call.data

    if text == 'block':
        block_card_step2(call.message)



bot.infinity_polling()
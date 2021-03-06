import telebot
from config import keys, TOKEN
from extensions import APIException, ExchangeRates

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])  # Ответ на сообщение /start
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> \
    <в какую валюты перевести> \
    <кол-во переводимой валюты>\nсписок всех доступных валют /values'
    bot.reply_to(message, f'{message.chat.username}, {text}')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')  # убираем заглавные буквы

        if len(values) == 1:  # возможность ввода только amount
            amount = values[0]
            values = []
            values.append('доллар')
            values.append('рубль')
            values.append(amount)

        if len(values) != 3:
            raise APIException("Слишком много параметров")

        quote, base, amount = values
        total_base = ExchangeRates.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)  # none stop

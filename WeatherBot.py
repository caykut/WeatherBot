from telegram.ext import Updater

import logging

from telegram.ext import CommandHandler ,InlineQueryHandler

import pprint

import datetime

import googlemaps

import requests
import time
import schedule


my_location_chatid_dict = {} 
my_location_based_user_dict = {
    "Istanbul":[]
}




updater = Updater(token='yourtoken', use_context=True)
URL = "your api"

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                     level=logging.INFO)



def  start ( update , context ):

    context.bot.send_message ( chat_id = update.effective_chat.id, text = " Merhaba bu bot size anlık hava duramu bilgisi desteği sağlar! " ) 

start_handler =  CommandHandler('start', start)

dispatcher.add_handler(start_handler)

updater.start_polling()



def kelvinToCelcius(degree):

    return degree - 273.15



def getWeather(cityname):

    weather_str = "your api"

    

    r = requests.get(weather_str.format(cityname))

    current_degree_kelvin = r.json()["main"]["temp"]

    current_degree_celcius = kelvinToCelcius(current_degree_kelvin)

    return current_degree_celcius

    

def weather ( update , context ):



    last_sentence = update.message.text



    last_sentence_splitted = last_sentence.split(" ")



    try:

    
    
        my_location_chatid_dict[update.effective_chat.id] = last_sentence_splitted[1]
        
        print("Dict şu an :{}".format(my_location_chatid_dict))


        context.bot.send_message ( chat_id = update.effective_chat.id,text=getWeather(last_sentence_splitted[1]))
    except:
         context.bot.send_message ( chat_id = update.effective_chat.id,text="şehir adını giriniz")



weather_handler =  CommandHandler('weather', weather) 

dispatcher.add_handler(weather_handler)

def caps(update, context):

    text_caps = ' '.join(context.args).upper()

    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)




def echo(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Tam olarak istediğinizi anlamadım")



from telegram.ext import MessageHandler, Filters

echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(echo_handler)



caps_handler = CommandHandler('caps', caps)

dispatcher.add_handler(caps_handler)

from telegram import InlineQueryResultArticle, InputTextMessageContent

import requests


 
def telegram_bot_sendtext(bot_message):
    
    for bot_chatID in list(my_location_chatid_dict.keys()):
        
        bot_token = 'your token'
        #bot_chatID = '1016539557'
        current_message = "Şu an hava durumun:{}".format(str(getWeather(my_location_chatid_dict[bot_chatID])))
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(bot_chatID) + '&parse_mode=Markdown&text=' +current_message

        response = requests.get(send_text)

    return response.json()
    

def report():
    my_balance = 10   ## Replace this number with an API call to fetch your account balance
    my_message = "Günaydın bugün şehrinizde hava"  ## Customize your message
    telegram_bot_sendtext(my_message)


    
schedule.every().day.at("10:30").do(report)

while True:
    schedule.run_pending()
    time.sleep(1)

def inline_caps(update, context):

    query = update.inline_query.query

    if not query:

        return

    results = list()

    results.append(

        InlineQueryResultArticle(

            id=query.upper(),

            title='Caps',

            input_message_content=InputTextMessageContent(query.upper())

        )

    )

    context.bot.answer_inline_query(update.inline_query.id, results)



inline_caps_handler = InlineQueryHandler(inline_caps)

dispatcher.add_handler(inline_caps_handler)





inline_caps_handler = InlineQueryHandler(inline_caps)

dispatcher.add_handler(inline_caps_handler)

def unknown(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="İstediğiniz Komutu anlamadım ")



unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(unknown_handler)



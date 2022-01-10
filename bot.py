from pycoingecko import CoinGeckoAPI
from flask import Flask
from flask_sslify import SSLify
from flask import request
from flask import jsonify
import re
import time
import random
from keys_and_addr import telegram_bot_token,API_key,url_weather,url_currency
import json
app=Flask(__name__)
sslify=SSLify(app)
import requests

URL=f'https://api.telegram.org/bot{telegram_bot_token}/'

"""Заготовка под ML"""
# domen='https://coronavirus-monitor.ru/coronavirus-v-rossii/'
# resp_for_pars=req.get(domen)
# resp_for_pars.encoding = 'utf8'
# pars=BeautifulSoup(resp_for_pars.text,'lxml')
# date=pars.find('time').get_text()
# conf_rus=pars.find('div', class_="info-block disease").find('i').get_text()
# conf_daily_rus=pars.find('div', class_="info-block disease").find('span').get_text()
# rec_rus=pars.find('div', class_="info-block healed").find('i').get_text()
# rec_daily_rus=pars.find('div', class_="info-block healed").find('span').get_text()
# died_rus=pars.find('div', class_="info-block deaths").find('i').get_text()
# died_daily_rus=pars.find('div', class_="info-block deaths").find('span').get_text()

# domen_tat='https://coronavirus-monitor.ru/coronavirus-v-tatarstane/'
# resp_for_pars_tat=req.get(domen_tat)
# resp_for_pars_tat.encoding = 'utf8'
# pars_tat=BeautifulSoup(resp_for_pars_tat.text,'lxml')
# date_tat=pars_tat.find('time').get_text()
# conf_tat=pars_tat.find('div', class_="info-block disease").find('i').get_text()
# conf_daily_tat=pars_tat.find('div', class_="info-block disease").find('span').get_text()
# rec_tat=pars_tat.find('div', class_="info-block healed").find('i').get_text()
# rec_daily_tat=pars_tat.find('div', class_="info-block healed").find('span').get_text()
# died_tat=pars_tat.find('div', class_="info-block deaths").find('i').get_text()
# # died_daily_tat=pars_tat.find('div', class_="info-block deaths").find('span').get_text()

# domen_all='https://www.worldometers.info/coronavirus/'
# resp_for_pars_all=req.get(domen_all)
# resp_for_pars_all.encoding = 'utf8'
# pars_all=BeautifulSoup(resp_for_pars_all.text,'lxml')
# # date_all=pars_all.find('div', class_='amount small').get_text()
# conf_all=pars_all.find('h1', text=re.compile('Coronavirus Cases:')).next_sibling.next_sibling.get_text()
# died_all=pars_all.find('h1', text=re.compile('Deaths:')).next_sibling.next_sibling.get_text()
# rec_all=pars_all.find('h1', text=re.compile('Recovered:')).next_sibling.next_sibling.get_text()
"""END Заготовка под ML"""
def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_updates():
    url=URL+'getUpdates'
    r=requests.get(url)
    return r.json()


def send_message(chat_id,text='meow meow meow'):

    url=URL+'sendMessage'
    answer={'chat_id':chat_id,
            'text':text}
    r=requests.post(url,json=answer)
    return r.json()

def send_dice(chat_id, emoji="🎲"):

    url=URL+'sendDice'
    answer={'chat_id':chat_id,
            'emoji':emoji}
    r=requests.post(url,json=answer)
    return r.json()

def parse_url1(city):
    ma=str(url_weather.format(city=city,API_key=API_key))
    req=requests.get(ma)
    req_json=req.json()
    pressure=req_json['main']['pressure']
    temperature=req_json['main']['temp']
    humid = req_json['main']['humidity']
    name=req_json['name']
    wind=req_json['wind']['speed']
    weather=req_json['weather'][0]['description']
    visibility=req_json['visibility']
    return visibility , pressure,humid,name,temperature,wind,weather


def parse_text1(text):
    pattern=re.compile(r'\w+')
    city=pattern.findall(text)[1]
    return city

def replika(chat_id,text='Я - шерсть этой земли!'):

    repliks_list=['Я - МЯВК этой земли!','Я - пылающий хвост правосудия!','Склонитесь перед клыком и когтем!','Моя миска бесконечно полна молоком!','Моя миска накормит голодного!',
    'Одного флакона валерьяны мне будет мало!','Чую, ты затеял неладное!','Энергия мявка питает эту землю!','Да поможет мне великое Мя!','Не стоит дергать меня за хвост!','Запарил ты меня, смертный!',
    'Не оскверняй это место своим текстом!','Чем ты тут, черт возьми, занимаешься?','Если не оставишь меня в покое, я превращу тебя в комок шерсти','Хммм... Странно.. я вроде не накладывал на тебя чары слабоумия..',
    'Великий Мя создал человека на 80% из жидкости... Неоторые состоят из тормозной ','В последний раз говорю!... Я Бог, а не наркобарон!','Выход есть всегда...даже когда вас съели у вас есть парочка',
    'Берегите природу, вашу мать!','Земля содрогнется от моих лап!','Да поглотит тебя Мя!','Я ненавижу тебя каждой клеточкой своего тела -_-',]

    send_message(chat_id, text=repliks_list[random.randint( 0,len(repliks_list))])

def main():
    """заготовка под ML"""
    # r=get_updates()
    # chat_id=r['result'][-1]['message']['chat']['id']
    # send_message(chat_id)
    pass


def parse_text(text):
    pattern=r'/\w+'
    crypto=re.search(pattern,text).group()
    return crypto[1:]

def get_price(curr):
    try:
        cg = CoinGeckoAPI()
        r = cg.get_price(ids=curr, vs_currencies='usd')
        price = r[str(curr)]["usd"]
    except Exception:
        try:
            curr_upp=curr.upper()
            req = requests.get(url_currency)
            req_json = req.json()
            value=req_json['Valute'][str(curr_upp)]['Value']
            name_value=req_json['Valute'][str(curr_upp)]['Name']
            return ('Курс ' + str(name_value)+' в рублях ='+str(value))
        except Exception:
            cg = CoinGeckoAPI()
            r = cg.get_price(ids="bitcoin", vs_currencies='usd')
            price = str(r["bitcoin"]["usd"])
            return ('Не знаю что ты хочешь, но вот держи стоимость биткойна ' + str(price))

    return ('Стоимость  ' + str(curr) + '=' + str(price))

def send_sticker(chat_id,sticker):

    url=URL+'sendSticker'
    answer={'chat_id':chat_id,
            'sticker':sticker}
    r=requests.post(url,json=answer)
    return r.json()

def trier(r):
    global message
    global message1
    try:
        message=r['message']['text']
        message1=r['message']
        message=message.lower()
        return message
    except Exception:
        try:
            message=r['message']['dice']['emoji']
            return message
        except Exception:
            try:
                message=r['edited_message']['text']
                message=message.lower()
                return message
            except Exception:
                try:
                    message=r['edited_message']['dice']['emoji']
                    return message
                except Exception:
                    message=r['message']['sticker']['file_id']
                    message1=r['message']
                    return message , message1

spisok_igr=["⚽️", "🏀", "🎯",  "🎲", "🎰"]

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        r=request.get_json()
        try:
            chat_id = r['message']['chat']['id']
        except Exception:
            chat_id = r['edited_message']['chat']['id']

        trier(r)
        pattern = r'/\w+'
        try:
            if re.search(pattern, message):
                price = get_price(parse_text(message))
                send_message(chat_id, text=price)
            # elif 'Сколько заболевших ковид в мире?' in message:
            #     send_message(chat_id, text=conf_all)
            # elif 'сколько заболевших ковид в мире?' in message:
            #     send_message(chat_id, text=conf_all)
            # elif 'Сколько заболевших ковид в России?' in message:
            #     send_message(chat_id, text=conf_rus)
            # elif 'сколько заболевших ковид в России?' in message:
            #     send_message(chat_id, text=conf_rus)
            # elif 'прирост заболевших ковид в России?' in message:
            #     send_message(chat_id, text=conf_daily_rus)
            # elif 'Прирост заболевших ковид в России?' in message:
            #     send_message(chat_id, text=conf_daily_rus)
            # elif 'Сколько заболевших ковид в Татарстане?' in message:
            #     send_message(chat_id, text=conf_tat)
            # elif 'сколько заболевших ковид в Татарстане?' in message:
            #     send_message(chat_id, text=conf_tat)
            # elif 'Прирост заболевших ковид в Татарстане?' in message:
            #     send_message(chat_id, text=conf_daily_tat)
            # elif 'прирост заболевших ковид в Татарстане?' in message:
            #     send_message(chat_id, text=conf_daily_tat)
            # elif 'Сколько умерших от ковид в мире?' in message:
            #     send_message(chat_id, text=died_all)
            # elif 'сколько умерших от ковид в мире?' in message:
            #     send_message(chat_id, text=died_all)
            # elif 'Сколько умерших от ковид в России?' in message:
            #     send_message(chat_id, text=died_rus)
            # elif 'сколько умерших от ковид в России?' in message:
            #     send_message(chat_id, text=died_rus)
            # elif 'Прирост умерших от ковид в России?' in message:
            #     send_message(chat_id, text=died_daily_rus)
            # elif 'прирост умерших от ковид в России?' in message:
            #     send_message(chat_id, text=died_daily_rus)
            # elif 'Сколько умерших от ковид в Татарстане?' in message:
            #     send_message(chat_id, text=died_tat)
            # elif 'сколько умерших от ковид в Татарстане?' in message:
            #     send_message(chat_id, text=died_tat)
            # elif 'Сколько выздоровевших от ковид в мире?' in message:
            #     send_message(chat_id, text=rec_all)
            # elif 'cколько выздоровевших от ковид в мире?' in message:
            #     send_message(chat_id, text=rec_all)
            # elif 'Сколько выздоровевших от ковид в России?' in message:
            #     send_message(chat_id, text=rec_rus)
            # elif 'cколько выздоровевших от ковид в России' in message:
            #     send_message(chat_id, text=rec_rus)
            # elif 'Прирост выздоровевших от ковид в России?' in message:
            #     send_message(chat_id, text=rec_daily_rus)
            # elif 'прирост выздоровевших от ковид в России' in message:
            #     send_message(chat_id, text=rec_daily_rus)
            # elif 'Сколько выздоровевших от ковид в Татарстане?' in message:
            #     send_message(chat_id, text=rec_tat)
            # elif 'cколько выздоровевших от ковид в Татарстане?' in message:
            #     send_message(chat_id, text=rec_tat)
            # elif 'Прирост выздоровевших от ковид в Татарстане?' in message:
            #     send_message(chat_id, text=rec_daily_tat)
            # elif 'прирост выздоровевших от ковид в Татарстане?' in message:
            #     send_message(chat_id, text=rec_daily_tat)
            elif 'слот машина' in message:
                send_dice(chat_id, emoji='🎰')
            elif message in spisok_igr:
                send_dice(chat_id, emoji=message)

            elif 'дартс' in message:
                send_dice(chat_id, emoji='🎯')

            elif 'футбол' in message:
                send_dice(chat_id, emoji='⚽️')

            elif 'баскетбол' in message:
                send_dice(chat_id, emoji='🏀')

            elif 'кубик' in message:
                send_dice(chat_id, emoji='🎲')


            elif 'мне плохо' in message:
                send_message(chat_id, text='попробуй музыку послушать, посмотреть кино, погулять или сыграть в любимую игру')
            elif 'как дела?' in message:
                send_message(chat_id, text='у меня все хорошо, а у тебя?')

            elif 'sticker' in message1:
                send_sticker(chat_id, sticker= message)


            elif 'погод' in message:
                visibility , pressure,humid,name,temperature,wind,weather=parse_url1(parse_text1(message))
                send_message(chat_id, text='Температура в городе '+str(name)+' на сегодня: '+str(temperature)
                +' \nпогода: '+str(weather)+'.'+
                '\nВлажность: '+str(humid)+'%.'+
                '\nДавление: '+str(pressure)+'hPa.'+
                '\nСкорость ветра : '+str(wind)+' м/с.'+
                '\nВидимость: '+str(visibility)+'метров.')



            # Мявк - великий и могучий
            elif 'мявк' in message:
                replika(chat_id)



            elif 'хай' in message:
                send_message(chat_id, text='Здравствуй, послушник Мя')
            elif 'hi' in message:
                send_message(chat_id, text='Здравствуй, послушник Мя')
            elif 'hello' in message:
                send_message(chat_id, text='Здравствуй, послушник Мя')
            elif 'здравствуй' in message:
                send_message(chat_id, text='Здравствуй, послушник Мя')
            elif 'приветствую' in message:
                send_message(chat_id, text='Здравствуй, послушник Мя')
            elif 'привет' in message:
                send_message(chat_id, text='Здравствуй, послушник Мя')
            elif 'пошел на' in message:
                send_message(chat_id, text='Сам/сама иди')
            elif 'иди на' in message:
                send_message(chat_id, text='Сам/сама иди')
            elif 'у меня проблема' in message:
                send_message(chat_id, text='Попробуй подумать и разобраться, если не получится, обратись к тому кто знает и спроси у него совет. Многие современные проблемы можно найти в интернете')
            elif 'кто ты' in message:
                send_message(chat_id, text='Я  - бог Мявк! Покровитель пушистых, карающая лапа виновных, \n уничтожитель несправедливости и теплая шерсть для замерзших! \n Склонись предо мной и я исполню твою мявочную волю!')
            elif 'как тебя зовут' in message:
                send_message(chat_id, text='Я  - бог Мявк! Покровитель пушистых, карающая лапа виновных, \n уничтожитель несправедливости и теплая шерсть для замерзших! \n Склонись предо мной и я исполню твою мявочную волю!')
                time.sleep(2)
                send_message(chat_id, text='а как тебя?')
                time.sleep(9)
                if request.method!='POST':
                    r=request.get_json()
                    try:
                        chat_id = r['message']['chat']['id']
                    except Exception:
                        chat_id = r['edited_message']['chat']['id']

                    trier(r)
                    if 'меня зовут Тони' in message:
                        send_message(chat_id, text='Fuck you, Tony')
                    else:
                        time.sleep(5)
                        send_message(chat_id, text='Можно звать тебя Джимми?')
                        time.sleep(3)
                        send_message(chat_id, text='Окей, Джим')

            else:
                replika(chat_id)
        except:
            replika(chat_id)

        return jsonify(r)
    return '<h1>Hello bot</h1>'


if __name__ == '__main__':\
    app.run()
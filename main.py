import telebot
from telebot import types
import wikipedia
from googletrans import Translator
import time
import requests

#token va modullarni cahqirish
admin_id='-1001261577807'
apikey='-jgjTI4nQgb-UebbeCNF3unEFqaMyOAkDi_ZMBmlQIA'
TOKEN="1546844166:AAF77WzEduNI6hIu-TgHkHYz8fBW-V83Vu8"
bot = telebot.TeleBot(TOKEN, parse_mode='HTML') # parse mode Html uchun ham o'tishi mumkin
translator = Translator()

#telegram keyboard uchun
markup_inline=types.InlineKeyboardMarkup()
item_uz=types.InlineKeyboardButton(text='Uzbekcha 🇺🇿',callback_data='uz')
item_ru=types.InlineKeyboardButton(text='русский 🇷🇺',callback_data='ru')
item_report_problem=types.InlineKeyboardButton(text='❌Report❌',callback_data='report_problem')
markup_inline.add(item_uz,item_ru,item_report_problem)

#report problem uchun buttonlar
markup_inline2=types.InlineKeyboardMarkup()
item_1=types.InlineKeyboardButton(text="Xato ma'lumot",callback_data='report1')
item_2=types.InlineKeyboardButton(text="Error 404",callback_data='report2')
item_3=types.InlineKeyboardButton(text="Rasm error",callback_data='report3')
markup_inline2.add(item_1,item_2,item_3)

#botni boshlash funksiyasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global name
    global id
    name = message.from_user.first_name
    id=message.from_user.id
    print(name, id)
    bot.reply_to(message, '''Salom {}, bizning wikipedia_uz botiga xush kelibsiz. 
     Wikipedia so'rovlarini jo'natishingiz mumkin.
     Masalan: Apple/Warsaw/Uzbekistan
    '''.format(name))
    bot.send_message(chat_id=admin_id,text='{} -botga kirdi!'.format(name))
    #reklama uchun funksiya 15 minut va 50 soatda jonatadi
    #bu funskiya xozir ishlamayapti 
    #reklama jonatish funksiyasi

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id,'''
             Botimiz xaqida:
Masalan:
✅ Yangilangan sanasi- 08/02/2021
✅ Dasturchi- @husanboy_us
✅ Xamkorlik uchun - @husanboy_us
✅ Bizning kanalimiz https://t.me/artofitt
             ''' )

#asosiy funksiya yoki funskiyalar
@bot.message_handler(func=lambda message: True)
def main_func(message):
    global get_wiki
    try:
        msg=message.text
        get_wiki=wikipedia.summary(msg, sentences=7)
        get_wiki_pics=wikipedia.page(msg).images[0]
        bot.send_message(message.chat.id,get_wiki,reply_markup=markup_inline )
        bot.send_photo(message.chat.id, photo=get_wiki_pics)
    except Exception  :
        bot.send_message(message.chat.id, text="Nimadur xatolik yuz berdi. Aniq javob olshingiz uchun aniq so'rov kiriting 👇👇👇")
        bot.send_message(message.chat.id,'''
             So'rovni Ingliz Tilida yozishni yoki tekshirishni unutmang!
Masalan:
Trump-❌❌❌ Donald Trump-✅✅✅
             ''' )
                
#function gets inline data and translates to the given languages
@bot.callback_query_handler(func=lambda call: True)
def query_text(call):
    global name
    global id
    if call.data=='uz':
        translation = translator.translate(get_wiki, dest='uz',)
        data_uz=translation.text
        bot.send_message(call.message.chat.id, data_uz)        
    elif call.data=='ru':
        translation = translator.translate(get_wiki, dest='ru',)
        data_ru=translation.text
        bot.send_message(call.message.chat.id,data_ru)
    elif call.data=='report_problem':
        bot.send_message(call.message.chat.id, text='  🔻🔻🔻   Xato turini tanlang! 🔻🔻🔻   ',reply_markup=markup_inline2)
    elif call.data=='report1':
        global name
        global id
        print('hello report 1')
        bot.send_message(call.message.chat.id,text='Xatolik Botimiz Adminiga yetib bordi! Tez orada kamchilik tuzatiladi!')
        bot.send_message(chat_id=admin_id,text=" Name: {}  ID: {} -Reported code 1".format(name,id))
      
    elif call.data=='report2':
        print('hello report 2')
        bot.send_message(call.message.chat.id,text='Xatolik Botimiz Adminiga yetib bordi! Tez orada kamchilik tuzatiladi!')
        bot.send_message(chat_id=admin_id,text=" Name: {}  ID: {} -Reported code 2".format(name,id))
     
        bot.send_message(call.message.chat.id,text='Xatolik Botimiz Adminiga yetib bordi! Tez orada kamchilik tuzatiladi!')
    elif call.data=='report3':
        print('hello report 3')
        bot.send_message(call.message.chat.id,text='Xatolik Botimiz Adminiga yetib bordi! Tez orada kamchilik tuzatiladi!')
        bot.send_message(chat_id=admin_id,text=" Name: {}  ID: {} -Reported code 3".format(name,id))
       
    else:
        print('Not working query_text funskiyasida')


bot.polling()    
#translation = translator.translate(result, dest='uz',)
#bot.reply_to(message,translation,parse_mode=None)

import config
import telebot
import sqlite3
bot = telebot.TeleBot(config.token)
chatid=None

@bot.message_handler(commands=["start"])
def start(commands):
    global chatid
    chatid = commands.chat.id
    user_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    first_button = telebot.types.InlineKeyboardButton(text="Магазин", callback_data="shop")
    second_button = telebot.types.InlineKeyboardButton(text="О нас", callback_data="about")
    third_button = telebot.types.InlineKeyboardButton(text="Профиль", callback_data="prof")
    fourth_button=telebot.types.InlineKeyboardButton(text="Корзина", callback_data="sale")
    user_markup.add( first_button, second_button,third_button,fourth_button )
    bot.send_message( commands.chat.id, "Выберите категорию ",reply_markup=user_markup )

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == "mainmenu":
        user_markup = telebot.types.InlineKeyboardMarkup( row_width=2 )
        first_button = telebot.types.InlineKeyboardButton( text="Магазин", callback_data="shop" )
        second_button = telebot.types.InlineKeyboardButton( text="О нас", callback_data="about" )
        third_button = telebot.types.InlineKeyboardButton( text="Профиль", callback_data="prof" )
        fourth_button = telebot.types.InlineKeyboardButton( text="Корзина", callback_data="sale" )
        user_markup.add( first_button, second_button, third_button, fourth_button )
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id, text="Меню",reply_markup=user_markup )

    if call.data == "shop":
        shopboard=telebot.types.InlineKeyboardMarkup(row_width=3)
        cat1 = telebot.types.InlineKeyboardButton( text="Формы", callback_data="1" )
        cat2 = telebot.types.InlineKeyboardButton( text="Жидкий силикон", callback_data="2" )
        cat3 = telebot.types.InlineKeyboardButton( text="Краски", callback_data="3" )
        cat4 = telebot.types.InlineKeyboardButton( text="Блёстки", callback_data="4" )
        cat5 = telebot.types.InlineKeyboardButton( text="Шприцы", callback_data="5" )
        cat6 = telebot.types.InlineKeyboardButton( text="Аттрактанты", callback_data="6" )
        cat7 = telebot.types.InlineKeyboardButton( text="Приманки", callback_data="7" )
        cat8 = telebot.types.InlineKeyboardButton( text="Лодки", callback_data="8" )
        cat9 = telebot.types.InlineKeyboardButton( text="Одежда", callback_data="9" )
        backbutton = telebot.types.InlineKeyboardButton( text="В меню", callback_data="mainmenu" )
        shopboard.add(cat1,cat2,cat3,cat4,cat5,cat6,cat7,cat8,cat9,backbutton)
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите категорию",reply_markup=shopboard )

    elif call.data=="about":
        adoutboard=telebot.types.InlineKeyboardMarkup(row_width=2)
        backbutton = telebot.types.InlineKeyboardButton( text="В меню", callback_data="mainmenu" )
        adoutboard.add(backbutton)
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id,text="Раздел 'О нас' в работе", reply_markup=adoutboard )

    elif call.data=="prof":
        profboard=telebot.types.InlineKeyboardMarkup(row_width=2)
        backbutton = telebot.types.InlineKeyboardButton( text="В меню", callback_data="mainmenu" )
        profboard.add(backbutton)
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id,text="Раздел 'Профиль' в работе", reply_markup=profboard )

    elif call.data == "sale":
        saleboard = telebot.types.InlineKeyboardMarkup( row_width=2 )
        backbutton = telebot.types.InlineKeyboardButton( text="В меню", callback_data="mainmenu" )
        saleboard.add( backbutton )
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id,text="Раздел 'Корзина' в работе", reply_markup=saleboard )
    if call.data == "1":
        #bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id,text="Раздел 'Корзина' в работе", reply_markup="" )
        global chatid
        with sqlite3.connect("picbd.db") as pic:
            cur=pic.cursor()
            result=cur.execute("SELECT price,path,name FROM form").fetchall()
        pic.close()
        for i in result:
            bot.send_photo( chatid, open( i[1], "rb" ),caption="Цена: "+str(i[0])+" грн."+"\n"+"Название: "+i[2] )
        else:
            saleboard = telebot.types.InlineKeyboardMarkup( row_width=2 )
            backbutton = telebot.types.InlineKeyboardButton( text="В меню", callback_data="mainmenu" )
            saleboard.add( backbutton )
            bot.send_message( chat_id=call.message.chat.id,text="Раздел 'Корзина' в работе", reply_markup=saleboard )
        return saleboard


bot.infinity_polling()
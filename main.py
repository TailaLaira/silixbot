import config
import telebot
import sqlite3
bot = telebot.TeleBot(config.token)

user_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
first_button = telebot.types.InlineKeyboardButton(text="Магазин", callback_data="shop")
second_button = telebot.types.InlineKeyboardButton(text="О нас", callback_data="about")
third_button = telebot.types.InlineKeyboardButton(text="Профиль", callback_data="prof_users")
fourth_button=telebot.types.InlineKeyboardButton(text="Корзина", callback_data="sale")
user_markup.add( first_button, second_button,third_button,fourth_button )
backboard = telebot.types.InlineKeyboardMarkup( row_width=2 )
backbutton = telebot.types.InlineKeyboardButton( text="В меню", callback_data="mainmenu" )
menubutton = telebot.types.InlineKeyboardButton( text="Вернутся к категориям", callback_data="shop" )
backboard.add( backbutton, menubutton )

user_markup = telebot.types.InlineKeyboardMarkup( row_width=2 )
user_markup.add( first_button, second_button, third_button, fourth_button )

shopboard = telebot.types.InlineKeyboardMarkup( row_width=3 )
cat1 = telebot.types.InlineKeyboardButton( text="Формы", callback_data="category_form" )
cat2 = telebot.types.InlineKeyboardButton( text="Жидкий силикон", callback_data="category_silic" )
cat3 = telebot.types.InlineKeyboardButton( text="Краски", callback_data="category_kras" )
cat4 = telebot.types.InlineKeyboardButton( text="Блёстки", callback_data="category_bles" )
cat5 = telebot.types.InlineKeyboardButton( text="Шприцы", callback_data="category_shpritc" )
cat6 = telebot.types.InlineKeyboardButton( text="Аттрактанты", callback_data="category_att" )
cat7 = telebot.types.InlineKeyboardButton( text="Приманки", callback_data="category_sp" )
cat8 = telebot.types.InlineKeyboardButton( text="Лодки", callback_data="category_ship" )
cat9 = telebot.types.InlineKeyboardButton( text="Одежда", callback_data="category_odej" )
shopboard.add( cat1, cat2, cat3, cat4, cat5, cat6, cat7, cat8, cat9, backbutton )

adoutboard = telebot.types.InlineKeyboardMarkup( row_width=2 )
adoutboard.add( backbutton )

profboard = telebot.types.InlineKeyboardMarkup( row_width=2 )
profboard.add( backbutton )

saleboard = telebot.types.InlineKeyboardMarkup( row_width=2 )
saleboard.add( backbutton )

def regist(call):
    reg = []
    def inputsurname(message):
        text = message.text
        reg.append( text )
        msg = bot.send_message( message.chat.id, 'Введите Фамилию:' )
        bot.register_next_step_handler( msg, inputphone )

    def inputphone(message):
        text = message.text
        reg.append( text )
        msg = bot.send_message( message.chat.id, 'Введите телефон:' )
        bot.register_next_step_handler( msg, inputadress )

    def inputadress(message):
        text = message.text
        reg.append( text )
        msg = bot.send_message( message.chat.id, 'Введите адрес:' )
        bot.register_next_step_handler( msg, allreg )

    def allreg(message):
        text = message.text
        reg.append( text )
        bot.send_message( message.chat.id, 'Регистрация завершена!' )
        with sqlite3.connect( "picbd.db") as pic:
            cur = pic.cursor()
            cur.execute("INSERT INTO users  (id, name, surname, phone, adress) VALUES (?, ?, ?, ?, ?)",(message.chat.id,reg[0],reg[1],reg[2],reg[3]))
            pic.commit()
            cur.close()
        bot.send_message( chat_id=call.message.chat.id, text="Выберите действие", reply_markup=backboard )
    msg = bot.send_message(call.message.chat.id, 'Введите имя' )
    bot.register_next_step_handler( msg, inputsurname)

def sendphoto(bdname,call):
    media=[]
    with sqlite3.connect( "picbd.db" ) as pic:
        cur = pic.cursor()
        result = cur.execute( "SELECT price,path,name FROM "+bdname ).fetchall()
    pic.close()
    for i in result:
        media.append(telebot.types.InputMediaPhoto(open( i[1], "rb" ),"Цена: " + str( i[0] ) + " грн." + "\n" + "Название: " + i[2]))
    else:
        bot.send_media_group( call.message.chat.id, media )

def profile(bdname,call):

    with sqlite3.connect( "picbd.db" ) as pic:
        cur = pic.cursor()
        info = cur.execute("SELECT * FROM "+bdname+" WHERE id=?", (call.message.chat.id,))
        if info.fetchone() is None:
            cur.close()
            regist(call)
        else:
            info = cur.execute( "SELECT * FROM users WHERE id=?", (call.message.chat.id,))
            data=info.fetchone()
            cur.close()
            bot.send_message( call.message.chat.id,"Имя: "+data[1]+"\nФамилия: "+data[2]+"\nТелефон: "+data[3]+"\nАдрес доставки: "+data[4])
            bot.send_message( chat_id=call.message.chat.id, text="Выберите действие", reply_markup=backboard )



@bot.message_handler(commands=["start"])
def start(commands):
    bot.send_message( commands.chat.id, "Выберите категорию ",reply_markup=user_markup )

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):

    if call.data == "mainmenu":
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id, text="Меню",reply_markup=user_markup )

    if call.data == "shop":
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите категорию",reply_markup=shopboard )

    elif call.data=="about":
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id,text="Раздел 'О нас' в работе", reply_markup=adoutboard )

    elif call.data == "sale":
        bot.edit_message_text( chat_id=call.message.chat.id, message_id=call.message.message_id,text="Раздел 'Корзина' в работе", reply_markup=saleboard )

    if call.data.split("_")[0]=="category":
        sendphoto(call.data.split("_")[1],call)
        bot.send_message( chat_id=call.message.chat.id, text="Выберите действие", reply_markup=backboard )
    if call.data.split("_")[0]=="prof":
        profile(call.data.split("_")[1],call)



bot.infinity_polling()
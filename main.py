import telebot 
from config import token
from random import randint
from logic import Pokemon, Wizard, Fighter
from telebot import types

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1,3)

        if chance == 1:
            pokemon = Pokemon(message.from_user.username)

        elif chance == 2:
            pokemon = Wizard(message.from_user.username)

        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, open(pokemon.show_img(), "rb"))
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'])
def attack(message):
    if message.reply_to_message:
        sender_username = Pokemon.pokemons[message.from_user.username]
        receiver_username = Pokemon.pokemons[message.reply_to_message.from_user.username]
        if message.from_user.username in Pokemon.pokemons.keys():
            if message.reply_to_message.from_user.username in Pokemon.pokemons.keys():
                result = sender_username.attack(receiver_username)
                bot.send_message(message.chat.id, result)
            else:
                bot.send_message(message.chat.id, "У противника нет покемона❌")
        else:
            bot.send_message(message.chat.id, "У тебя нет покемона❌, напиши /go что бы его получить!")

@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        username = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, username.info())
        bot.send_photo(message.chat.id, open(username.show_img(), "rb"))
    else:
        bot.send_message(message.chat.id, "У тебя нет покемона❌, напиши /go что бы его получить!")



@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, """
Помощь по командам в этом боте:\n
/go - Призвать себе покемона\n
/attack - атаковать игрок на чье сообщение вы отвечаете\n
/info - узнать информацию о своем покемоне\n
/heal - излечить своего покемона на 20hp\n
/pokeinfo - информация про покемонов\n
/help - вызвать это меню\n
""")
    
@bot.message_handler(commands=['pokeinfo'])
def pokeinfo(message):
        bot.send_message(message.chat.id, """
Покемон - имеет от 50 до 100 здоровья, его сила колеблится от 20 до 40, излечением он востанавливает 20 здоровья\n
Покемон-волшебник - имеет от 80 до 110 здоровья, его сила колеблится от 20 до 40, излечением он востанавливает 40 здоровья\n
Покемон-боец - имеет от 50 до 100 здоровья, его сила колеблится от 40 до 50, излечением он востанавливает 20 здоровья\n
                         """)
@bot.message_handler(commands=['heal'])
def heal(message):
    username = Pokemon.pokemons[message.from_user.username]
    bot.send_message(message.chat.id, username.heal())




bot.infinity_polling(none_stop=True)


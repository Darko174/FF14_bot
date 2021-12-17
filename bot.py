import telebot
import requests
import time
from bs4 import BeautifulSoup

botToken = "987921289:AAFRwmrcAFZbUwiHWeU0ZIn9gsW2x8dG3qs"
bot = telebot.TeleBot(botToken)

targetSiteUrl = "https://na.finalfantasyxiv.com/lodestone/worldstatus/"
status = "123"
numberOfTry = 0


def CheckServer():
    response = requests.get(targetSiteUrl)
    soup = BeautifulSoup(response.text, 'lxml')
    listOfServers = soup.findAll('li', class_='item-list')

    global numberOfTry
    numberOfTry +=1
    print(numberOfTry)

    for i in listOfServers:
        s = str(i)
        if "Cerberus" in s and "Available" in s:
            return "Регистрация снова открыта"
        elif "Cerberus" in s and "Unavailable" in s:
            return "Регистрация закрыта"

    return "Ошибка, сервер не найден"

def SendMessage(m):
    result = CheckServer()
    global status

    if status != result:
        bot.send_message(m.chat.id, result)
        status = result
    
    time.sleep(1800)
    SendMessage(m)

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Начинаю отслеживание сервера Cerberus")
    SendMessage(m)
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
# Запускаем бота
bot.polling(none_stop=True, interval=0)
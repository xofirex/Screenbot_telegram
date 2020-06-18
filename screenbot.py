import telebot
import configparser
import requests
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options


config = configparser.ConfigParser()
config.read("config.ini")
bot = telebot.TeleBot(config["DEFAULT"]["Token"])



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет, если нужен скриншот кидай ссылку")


@bot.message_handler(func=lambda m: True)
def send_screen(message):
    uid = message.chat.id
    umsg = message.text
    try:
        response = requests.get(umsg)
        DRIVER = 'chromedriver'
        driver = webdriver.Chrome(executable_path=r"C:\Users\xofir\Downloads\chromedriver_win32\chromedriver.exe")
        driver.get(umsg)
        time.sleep(3)
        # get scroll Height
        height = driver.execute_script(
            "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
        print(height)
        # close browser
        driver.close()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--window-size=1920,{height}")
        chrome_options.add_argument("--hide-scrollbars")
        driver = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\xofir\Downloads\chromedriver_win32\chromedriver.exe")
        driver.get(umsg)
        screenshot = driver.save_screenshot('my_screenshot.png')
        driver.quit()
        photo = open('my_screenshot.png', 'rb')
        bot.send_photo(uid, photo)
    except requests.ConnectionError as exception:
        bot.send_message(uid, "URL invalid")
    except requests.exceptions.MissingSchema as exception:
        bot.send_message(uid, "URL invalid")




bot.polling()
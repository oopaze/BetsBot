import os, time
import subprocess

from selenium import webdriver

from bot.bets.bot import Bot
from bot.src.settings import BASE_URL, CHROME_APP_CONFIG


def run():
    bot_options = webdriver.ChromeOptions()
    bot_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    bot_options.add_argument("start-maximized")
    bot_options.add_argument("--auto-open-devtools-for-tabs")

    bot = Bot(options=bot_options)
    bot.watch_api()
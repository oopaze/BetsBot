import time

from decouple import config
import requests as r

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from bot.src.settings import USERNAME, PASSWORD, BASE_URL, API_ENDPOINTS
from .selectors import *


class Bot(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        self.base_delay = kwargs.pop('delay', 5)
        super().__init__(*args, **kwargs)

        self.get(BASE_URL)
        self.perform_login()


    def get_widget(self, selector, type_selector=By.CSS_SELECTOR):
        return WebDriverWait(self, self.base_delay).until(
            EC.presence_of_element_located((type_selector, selector))
        )


    def perform_login(self):
        login_css_selector = ".hm-MainHeaderRHSLoggedOutWide .hm-MainHeaderRHSLoggedOutWide_Login "
        login_button = self.get_widget(login_css_selector)
        login_button.click()

        username_input = self.get_widget(".lms-StandardLogin_Username")
        password_input = self.get_widget(".lms-StandardLogin_Password")

        time.sleep(1)

        username_input.clear()
        username_input.send_keys(USERNAME)

        if not(password_input.get_attribute("value") == PASSWORD):
            password_input.clear()
            password_input.send_keys(PASSWORD)

        login_button = self.get_widget(".lms-StandardLogin_LoginButtonText").click()
        self.dispenser_messages_document_verification()


    def dispenser_messages_document_verification(self):
        try:
            self.get_widget("iframe[name='messageWindow']")
            self.switch_to.frame(0)
            self.get_widget("#remindLater").click()
        except:
            pass

        self.switch_to.default_content()

        try:
            self.get_widget(CLOSE_MESSAGES).click()
        except:
            pass


    def watch_api(self):
        while True:
            count_time = time.time()
            
            response = r.get(API_ENDPOINTS['get_entradas']["URL"])
            entradas = response.json()

            if entradas:
                self.perform_entrada(entradas)
    
            if (count_time - time.time()) < 5:
                time.sleep(5 - (count_time - time.time()))


    def update_entradas(self, ids):
        r.put(API_ENDPOINTS['bet_entradas']['URL'], json={"ids": ids})


    def make_entrada(self, div_input, input, valor):
        self.get_widget(div_input).click()
        input_1 = self.get_widget(input)
        input_1.send_keys(f"{valor}")


    def perform_entrada(self, entradas):
        ids = []

        for entrada in entradas:
            url = entrada['link']
            valor = entrada['valor'] * (30 / 100)
            self.get(url)

            self.dispenser_messages_document_verification()
            
            self.get_widget(TIME_ONE).click()
            self.get_widget(TIME_TWO).click()
            self.get_widget(CARDENETA).click()

            self.make_entrada(DIV_INPUT_ONE, INPUT_ONE, valor)
            self.make_entrada(DIV_INPUT_TWO, INPUT_TWO, valor)

            self.get_widget(FAZER_APOSTA).click()

            ids.append(entrada['id'])

        self.update_entradas(ids)

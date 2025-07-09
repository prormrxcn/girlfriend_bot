# whatsapp_bot.py

from deep_translator import GoogleTranslator
from main_chat_bot import DeepanshiChatbot
from threading import Thread
from time import sleep
import datetime

# For WhatsApp Automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class WhatsAppBot:
    def __init__(self):
        self.chatbot = DeepanshiChatbot()
        self.last_seen = ""
        self.group_name = "Deepanshi Group 💬"
        self.my_name = "Daksh"
        self.driver = self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument("--user-data-dir=./User_Data")
        driver = webdriver.Chrome(options=options)
        driver.get("https://web.whatsapp.com")
        input("\n📱 Scan the QR code and press ENTER to continue...")
        return driver

    def find_chat(self, name):
        try:
            chat = self.driver.find_element(By.XPATH, f"//span[@title='{name}']")
            chat.click()
            return True
        except:
            return False

    def send_message(self, message):
        try:
            input_box = self.driver.find_element(By.XPATH, "//div[@title='Type a message']")
            input_box.click()
            input_box.send_keys(message)
            send_button = self.driver.find_element(By.XPATH, "//button[@data-testid='compose-btn-send']")
            send_button.click()
        except Exception as e:
            print(f"❌ Error sending message: {e}")

    def get_last_message(self):
        try:
            messages = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]//div[@class='_21Ahp']")
            if messages:
                return messages[-1].text
        except:
            pass
        return None

    def run_group_listener(self):
        print(f"💬 Listening in group: {self.group_name}")
        if not self.find_chat(self.group_name):
            print("❌ Group not found!")
            return

        while True:
            sleep(2)
            last_msg = self.get_last_message()
            if last_msg and last_msg != self.last_seen and self.my_name.lower() in last_msg.lower():
                print(f"📥 Mentioned in group: {last_msg}")
                self.last_seen = last_msg
                clean_input = last_msg.replace(self.my_name, "").strip()
                reply = self.chatbot.get_response(clean_input)
                self.send_message(f"@{self.my_name} {reply}")

    def run_direct_chat(self):
        print(f"💌 Waiting for direct message from {self.my_name}...")
        if not self.find_chat(self.my_name):
            print("❌ Chat not found!")
            return

        while True:
            sleep(2)
            last_msg = self.get_last_message()
            if last_msg and last_msg != self.last_seen:
                self.last_seen = last_msg
                reply = self.chatbot.get_response(last_msg)
                self.send_message(reply)

if __name__ == "__main__":
    bot = WhatsAppBot()

    # Choose one mode:
    Thread(target=bot.run_group_listener).start()
    # Thread(target=bot.run_direct_chat).start()

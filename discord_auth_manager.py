import json
import time
import random
from sys import stderr
from typing import List, Dict, Optional

from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# --- КОНФИГУРАЦИЯ ЛОГГЕРА ---
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{message}</level>")

class DiscordBot:
    def __init__(self, headless: bool = False):
        self.options = self._get_chrome_options(headless)
        self.service = Service(ChromeDriverManager().install())
        self.driver = None
        self.wait = None

    def _get_chrome_options(self, headless: bool) -> Options:
        options = webdriver.ChromeOptions()
        # options.add_extension("Anti.crx") # Раскомментируй, если есть файл
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-gpu')
        options.add_argument("--mute-audio")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        if headless:
            options.add_argument("--headless")
        return options

    def start_driver(self):
        """Запуск браузера"""
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def close_driver(self):
        """Закрытие браузера"""
        if self.driver:
            self.driver.quit()

    def login(self, email: str, password: str) -> bool:
        """Логин в аккаунт"""
        try:
            logger.info(f"Вход в аккаунт: {email}")
            self.driver.get('https://discord.com/login')
            
            # Ждем появления полей ввода
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            pass_field = self.driver.find_element(By.NAME, "password")
            
            email_field.send_keys(email)
            pass_field.send_keys(password)
            
            # Жмем кнопку входа
            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            
            # Проверка на успешный вход (ждем появления URL каналов или кнопки настроек)
            # Тут можно добавить проверку на капчу или вериф
            time.sleep(5) # Небольшая пауза для прогрузки JS
            
            if "login" not in self.driver.current_url:
                logger.success(f"Успешный вход: {email}")
                return True
            else:
                logger.warning(f"Не удалось войти (возможно капча/вериф): {email}")
                return False
                
        except TimeoutException:
            logger.error(f"Такой элемент не найден или сайт лагает: {email}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при входе: {e}")
            return False

    def get_token(self) -> Optional[str]:
        """Достаем токен через JS инъекцию (Webpack)"""
        try:
            # JS код
            script = """
            let webpack = (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m);
            let module = webpack.find(m=>m?.exports?.default?.getToken!==void 0);
            return module.exports.default.getToken();
            """
            token = self.driver.execute_script(script)
            if token:
                logger.success(f"Токен получен: {token[:20]}...") # Скрываем часть токена в логах
                return token
            return None
        except Exception as e:
            logger.error(f"Ошибка получения токена: {e}")
            return None

def change_password(self, old_pass: str, new_pass: str):
        """Смена пароля (Полная логика)"""
        try:
            logger.info("Открываем настройки пользователя...")
            # 1. Жмем на шестеренку (Настройки)
            # Используем универсальный поиск по aria-label 
            settings_btn = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='User Settings'], button[aria-label='Настройки пользователя']")
            ))
            settings_btn.click()
            time.sleep(1) # Ждем анимацию

            logger.info("Переходим к смене пароля...")
            # 2. Ищем кнопку "Изменить пароль"
            # Логика: ищем блок, где написано "Password", и берем кнопку внутри этого блока
            # Это надежнее, чем искать по кривым ID
            change_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'Password') or contains(text(), 'Пароль')]/parent::div//button")
            ))
            change_btn.click()

            # 3. Заполняем поля (Старый, Новый, Повтор)
            logger.info("Вводим новые данные...")
            # Ждем появления полей ввода пароля (обычно их 3 штуки)
            inputs = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='password']")))
            
            if len(inputs) >= 2: # Иногда просит 2, иногда 3 поля
                inputs[0].send_keys(old_pass)      # Первое поле - Текущий пароль
                inputs[1].send_keys(new_pass)      # Второе поле - Новый пароль
                if len(inputs) > 2:
                    inputs[2].send_keys(new_pass)  # Третье поле - Подтверждение (если есть)
                
                # 4. Жмем кнопку "Готово" (Done/Save)
                save_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                save_btn.click()
                
                logger.success(f"Пароль изменен на {new_pass}")
                time.sleep(2) # Ждем сохранения
            else:
                logger.warning("Не удалось найти поля ввода пароля")

        except Exception as e:
            logger.error(f"Не удалось сменить пароль (возможно, изменилась верстка): {e}")

def main():
    # Загрузка аккаунтов
    try:
        with open('accs.json', 'r') as file:
            accounts = json.load(file)
    except FileNotFoundError:
        logger.error("Файл accs.json не найден!")
        return

    bot = DiscordBot(headless=False)

    for acc in accounts:
        bot.start_driver()
        email = acc.get("mail")
        password = acc.get("password")

        if bot.login(email, password):
            token = bot.get_token()
            if token:
                # Сохраняем результат
                with open('valid_tokens.txt', 'a') as f:
                    f.write(f"{email}:{password}:{token}\n")
        
        bot.close_driver()
        time.sleep(2) # Пауза между аккаунтами

if __name__ == "__main__":
    main()
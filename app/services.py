import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import app


def get_driver():
    """Cоздание драйвера хром"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-site-isolation-trials')
    driver = webdriver.Chrome('../driver/chromedriver', options=chrome_options)
    return driver


def get_screen(url: str):
    """Создает скриншот страницы и возвращает путь до файла"""

    driver = get_driver()

    try:
        driver.set_window_size(1600, 900)

        driver.get(url)

        width = driver.execute_script("return document.body.offsetWidth")
        height = driver.execute_script('return document.body.scrollHeight')

        driver.set_window_size(width, height)
        driver.refresh()
        time.sleep(1)

        filename = f'{str(datetime.utcnow())}.png'

        filepath = os.path.join(app.Configuration.MEDIA_DIR, filename)

        driver.save_screenshot(filepath)

        return filename

    except Exception as e:
        print(f'Exception: {e}')

    finally:
        driver.quit()


if __name__ == '__main__':
    get_screen('https://leroymerlin.ru/')
    get_screen('https://flask.palletsprojects.com/')
    get_screen('https://www.e1.ru')
    get_screen('https://docs.sqlalchemy.org/')



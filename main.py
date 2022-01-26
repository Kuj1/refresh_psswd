import random
import os
import time
from datetime import datetime
from multiprocessing import Pool

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from auth import old_pass


# Constants
UA = UserAgent(verify_ssl=False)
URLS = ['https://account.battle.net/', 'https://vk.com/']

# Options
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'--user-agent={UA.opera}')
options.add_argument('start-maximized')
options.add_argument('--headless')
options.add_argument('--enable-javascript')


# Directory 'fresh_passwd.txt'
file_pass = f'{os.getcwd()}/fresh_passwd.txt'


def gen_pass():
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = random.randint(25, 35)
    new_password = ''
    for i in range(length):
        new_password += random.choice(chars)

    return new_password


def refresh_password(url):

    # Driver initial
    s = Service(f'{os.getcwd()}/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)

    username = ''
    passwd = ''
    if url == 'https://account.battle.net/':
        for key in old_pass.keys():
            if key == 'battle':
                username = ''
                passwd = ''

                username += old_pass[key]['username']
                passwd += old_pass[key]['passwd']
        try:
            driver.get(url)
            time.sleep(random.randint(5, 10))
            enter_login = driver.find_element(By.ID, 'accountName')
            enter_login.send_keys(username, Keys.ENTER)
            enter_password = driver.find_element(By.ID, 'password')
            enter_password.send_keys(passwd, Keys.ENTER)
            time.sleep(10)

            security = BeautifulSoup(driver.page_source, 'html.parser')
            m_to_refresh = security.find('div', class_='side-navigation desktop').find('ul', class_='nav').find_all('li')[4].find('a').get('href')
            sec_page = f'https://account.battle.net{m_to_refresh}'
            driver.get(sec_page)
            time.sleep(random.randint(5, 10))

            driver.execute_script("document.getElementsByClassName('card-header-link float-md-right')[0].click()")

            enter_old_passwd = driver.find_element(By.ID, 'old-password')
            enter_old_passwd.send_keys(passwd, Keys.ENTER)
            new_passwd = gen_pass()
            enter_new_passwd = driver.find_element(By.ID, 'new-password')
            enter_new_passwd.send_keys(new_passwd, Keys.ENTER)
            conf_new_passwd = driver.find_element(By.ID, 'confirm-password')
            conf_new_passwd.send_keys(new_passwd, Keys.ENTER)

            current_datetime = datetime.now()
            fresh_pass = f'Battle.net: {new_passwd} - {current_datetime}'
            if not file_pass:
                with open(f'{os.getcwd()}/fresh_passwd.txt', 'w') as file:
                    file.write(f'{fresh_pass}')
            else:
                with open(f'{os.getcwd()}/fresh_passwd.txt', 'a') as file:
                    file.write(f'\n{fresh_pass}')

        except Exception as ex:
            print(f'[ERROR]: {ex}')

        finally:
            driver.close()
            driver.quit()

    if url == 'https://vk.com/':
        for key in old_pass.keys():
            if key == 'vk':
                username = ''
                passwd = ''

                username += old_pass[key]['username']
                passwd += old_pass[key]['passwd']
        try:
            driver.get(url)
            enter_login = driver.find_element(By.ID, 'index_email')
            enter_login.send_keys(username, Keys.ENTER)
            enter_password = driver.find_element(By.ID, 'index_pass')
            enter_password.send_keys(passwd, Keys.ENTER)
            time.sleep(random.randint(5, 10))

            change_page = f'https://m.vk.com/settings?act=change_password'
            driver.get(change_page)
            time.sleep(random.randint(5, 10))

            enter_old_passwd = driver.find_element(By.XPATH, '//input[@name="old_password"]')
            enter_old_passwd.send_keys(passwd)
            new_passwd = gen_pass()
            enter_new_passwd = driver.find_element(By.XPATH, '//input[@name="new_password"]')
            enter_new_passwd.send_keys(new_passwd)
            conf_new_passwd = driver.find_element(By.XPATH, '//input[@name="confirm_password"]')
            conf_new_passwd.send_keys(new_passwd, Keys.ENTER)

            current_datetime = datetime.now()
            fresh_pass = f'Vk.com: {new_passwd} - {current_datetime}'

            if not file_pass:
                with open(f'{os.getcwd()}/fresh_passwd.txt', 'w') as file:
                    file.write(f'{fresh_pass}')
            else:
                with open(f'{os.getcwd()}/fresh_passwd.txt', 'a') as file:
                    file.write(f'\n{fresh_pass}')

        except Exception as ex:
            print(f'[ERROR]: {ex}')

        finally:
            print('[INFO]: All password are refreshed')
            driver.close()
            driver.quit()


if __name__ == '__main__':
    p = Pool(processes=2)
    p.map(refresh_password, URLS)

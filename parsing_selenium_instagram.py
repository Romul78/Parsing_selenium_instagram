#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import os
import wget
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.headers = True
options.add_argument(
    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 '
    'Safari/537.36')
driver = webdriver.Chrome(options=options)


def get_url(url):
    return driver.get(url)


def get_name():
    name = input('Enter your nickname: ')
    url1 = f'https://www.instagram.com/{name}/'
    driver.get(url1)


def get_login(login):
    if True:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Only allow "
                                                                              "essential cookies')]"))).click()

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='_9nyy2']")))

    login = driver.find_element(By.XPATH, "//input[@name='username']")
    password = driver.find_element(By.XPATH, "//input[@name='password']")

    log_enter = input('Enter login and phone: ')
    pass_enter = input('Enter password: ')

    login.clear()
    login.send_keys(log_enter)

    password.clear()
    password.send_keys(pass_enter)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()


# Screen scroll down function
def scroll(end_scroll):
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
    i = 0

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))

        i += 1
        time.sleep(2)

        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")

        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break


def get_img():
    # Folder where the downloaded files will be located
    keyword = 'img_insta'

    driver.find_elements(By.XPATH, "//div[@class='vNnq7C weEfm']")
    time.sleep(5)

    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
    i = 0
    links = []

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))

        time.sleep(5)
        images = driver.find_elements(By.TAG_NAME, 'img')
        images = [image.get_attribute('src') for image in images]
        time.sleep(10)
        images = images[3:-2]

        for j in images:
            links.append(j)

        # print('Number of scraped images: ', len(links))

        i += 1
        time.sleep(10)

        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")

        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if screen_height * i > scroll_height:
            break

    print(links)
    print('Number of scraped images: ', len(links))

    path = os.getcwd()
    path = os.path.join(path, keyword)
    if os.path.exists(path):
        counter = 0
        for image in tqdm(list(set(links))):
            save_as = os.path.join(path, keyword + str(counter) + '.jpg')
            wget.download(image, save_as)
            time.sleep(2)
            counter += 1
    else:
        os.mkdir(keyword)
        counter = 0
        for image in tqdm(list(set(links))):
            save_as = os.path.join(path, keyword + str(counter) + '.jpg')
            wget.download(image, save_as)
            time.sleep(2)
            counter += 1



def main():
    url = 'https://www.instagram.com/'
   
    get_login(get_url(url))
    scroll(get_name())
    get_img()
    driver.quit()
    driver.close()


if __name__ == '__main__':
    main()

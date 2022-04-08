from pathlib import Path
import time

import requests
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

BASE_DIR = Path(__file__).resolve(strict=True).parent


def get_driver(headless):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")

    # initialize driver
    driver = webdriver.Chrome(chrome_options=options, executable_path="C:\\chromedriver\\chromedriver")
    return driver


def connect_to_base(browser, search_request):
    base_url = "https://www.wildberries.ru/"
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(base_url)
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "adaptive"))
            )
            search_block = browser.find_element_by_class_name("nav-element__search")
            search_block.click()
            time.sleep(1)
            search_allowed = browser.find_element_by_id("mobileSearchInput")
            search_allowed.send_keys(search_request)
            time.sleep(1)
            search_allowed.send_keys(Keys.ENTER)
            time.sleep(1)
            not_found = browser.find_element_by_class_name("catalog-page__text").text
            if not_found == "По Вашему запросу ничего не найдено.":
                return not_found
            else:
                break
        except selenium.common.exceptions.NoSuchElementException:
            try:
                card = browser.find_element_by_class_name("product-detail")
                if card:
                    print(f"По запросу найдена ({search_request}) только 1 нм")
            except Exception as err:
                print(f"Запрос {search_request} - ошибка!")
                not_found = browser.find_element_by_class_name("catalog-page__text").text
                # if not_found == "По Вашему запросу ничего не найдено.":
                #     return not_found
                # else:
                break
        except Exception as e:
            print(f"Запрос {search_request} - ошибка!")
            print(e)
            connection_attempts += 1
            print(f"Error connecting to {base_url}.")
            print(f"Attempt #{connection_attempts}.")
    return False


# def parse_html(html):
#     # create soup object
#     soup = BeautifulSoup(html, "html.parser")
#     # parse soup object to get wikipedia article url, title, and last modified date
#     not_found = soup.find("p", {"class": "catalog-page__text"}).text
#     if not_found == "По Вашему запросу ничего не найдено.":
#         return True
#     else:
#         return False


def get_load_time(search_url):
    try:
        # set headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        # make get request to article_url
        response = requests.get(
            search_url, headers=headers, stream=True, timeout=3.000
        )
        # get page load time
        load_time = response.elapsed.total_seconds()
    except Exception as e:
        print(e)
        load_time = "Loading Error"
    return load_time


def write_to_file(output_list, filename):
    for row in output_list:
        with open(Path(BASE_DIR).joinpath(filename), "a") as file:
            file.write(str(row) + "\n")

#encoding=utf-8
import time
import json
import random
import platform
import logging
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)

"""
使用selenium 4版本 浏览器驱动Webdriver的初始化方式与之前版本有所不同
"""

# 指定抓取单个collection
COLLECTION_ID = None


def get_selenium_webservice():
    platform_str = platform.system()
    if platform_str == "Windows":
        service = Service(executable_path="C:\driver\chromedriver.exe")
    elif platform_str == "Darwin":
        service = Service(executable_path="/Users/zhaopengfei/work/chrome-driver/chromedriver")
    else:
        service = Service(executable_path="/data/driver/chromedriver")

    return service


def get_slugs_by_chain(chain=None):
    """
    从接口获取collection names
    """
    chain_name = chain if chain else "eth"
    url = f"https://webapi.nftscan.com/category/getSlug?chain={chain_name}"
    try:
        rt = requests.get(url)
        result = rt.json()
    except Exception as e:
        return []
    res_code = result.get("code", 0)
    if not result or (str(res_code) != "200"):
        return []
    slugs = result.get("data", [])

    return slugs


def crawler(driver, chain=None):
    """
    crawler category from opensea
    """
    if not chain:
        return None
    collections = get_slugs_by_chain(chain=chain)
    for collection in collections:
        url = f"https://opensea.io/collection/{collection}"
        logging.info(url)
        driver.get(url)
        try:
            elements = driver.find_element(By.XPATH, '//span[@data-testid="collection-description-metadata-category"]')
            result = elements.text
            content = result.split("\n")
            cate = content[-1]
            msg = f"content: {content}, cate: {cate}"
            logging.info(msg)
            data = {
                "chain": chain,
                "slug": collection,
                "category": cate,
            }
            logging.info(data)
            post = "https://webapi.nftscan.com/category/modifyCategory"
            res = requests.post(post, json=data)
            logging.info(res.status_code)
        except selenium.common.exceptions.NoSuchElementException as e:
            logging.info("NoSuchElementException")
        except Exception as e:
            logging.info(e)
            continue
        time.sleep(0.2)


def main():
    chains = ["eth"]
    for chain in chains:
        start(chain)


def start(chain):
    service = get_selenium_webservice()
    driver = webdriver.Chrome(service=service)
    while 1:
        crawler(driver, chain=chain)
        time.sleep(5)
    driver.quit()
    driver.close()


if __name__ == "__main__":
    # get_slugs_by_chain()
    # crawler()
    main()

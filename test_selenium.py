#encoding=utf-8
import time
import json
import random
import platform
import logging
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)

"""
使用selenium 4版本 浏览器驱动Webdriver的初始化方式与之前版本有所不同
"""

HOST = ""
USER = "root"
PASSWD = ""

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


def main():
    """
    crawler by collection
    """
    collections = get_collections(collection_id=COLLECTION_ID)
    
    conn = connect_mysql(host=HOST, user=USER, passwd=PASSWD, db="sol_data")
    
    service = get_selenium_webservice()
    driver = webdriver.Chrome(service=service)
    
    col_index = 1
    for col_id, col_value in collections.items():
        collection = str(col_value).strip()
        if not collection:
            continue
        msg = f"--------------------process: {col_index} col: {collection}"
        logging.info(msg)
        offset = 0
        index = 0
        collections_total_nft_count = 0
        collections_total_nft = []
        while True:
            payload = {"$match":{"collectionSymbol":collection},"$sort":{"createdAt":-1},"$skip":offset,"$limit":150,"status":["all"]}

            query = urllib.parse.quote_plus(json.dumps(payload))
            params = str(query).replace("+", "")

            url = f"https://api-mainnet.magiceden.io/rpc/getListedNFTsByQueryLite?q={params}"
            logging.info(url)

            driver.get(url)

            count = random.randint(1, 3)
            time.sleep(count)
            elements = driver.find_element(By.TAG_NAME, 'body')
            content = elements.text
            json_data = json.loads(content)
            nft_list = json_data.get("results", [])
            nft_list_count = len(nft_list)
            msg = f"index:{index} offset:{offset} count:{nft_list_count}"
            logging.info(msg)

            collections_total_nft_count += nft_list_count
            collections_total_nft.extend(nft_list)
            if (nft_list_count < 150) or (not nft_list):
                break
            index += 1
            offset += 150

        data = {"result": collections_total_nft}
        save = save_data_to_file(collection, data)
        # 若保存失败,则跳出
        if not save:
            break
        msg = f"{collection} total count:{collections_total_nft_count}"
        logging.info(msg)

        conn.ping()
        cur = conn.cursor()
        sql = f"update sol_data.magic_collection set synced=1, count={collections_total_nft_count} where id={col_id}"
        cur.execute(sql)
        conn.commit()
        col_index += 1
        time.sleep(random.randint(2, 5))
    
    conn.close()
    driver.close()
    driver.quit()


def save_data_to_file(collection, data):
    """
    保存数据到文件
    """
    file_name = get_file_name(collection)
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        logging.info(e)
        return False
    return True


def get_file_name(collection):
    """
    生成文件路径和文件名
    """
    platform_str = platform.system()
    if platform_str == "Windows":
        file_name = f"C:\crawler_data\{collection}.json"
    elif platform_str == "Darwin":
        file_name = f"/Users/zhaopengfei/work/crawler/{collection}.json"
    else:
        file_name = f"/Users/zhaopengfei/work/crawler/{collection}.json"
    return file_name


def test_crawler():
    """
    抓取测试
    """
    collection = 'mongomons'

    service = get_selenium_webservice()
    driver = webdriver.Chrome(service=service)

    offset = 0
    index = 0
    collections_total_nft_count = 0
    collections_total_nft = []
    while True:
        payload = {"$match":{"collectionSymbol":collection},"$sort":{"createdAt":-1},"$skip":offset,"$limit":150,"status":["all"]}

        query = urllib.parse.quote_plus(json.dumps(payload))
        params = str(query).replace("+", "")

        url = f"https://api-mainnet.magiceden.io/rpc/getListedNFTsByQueryLite?q={params}"
        logging.info(url)

        driver.get(url)

        count = random.randint(3, 6)
        time.sleep(count)
        elements = driver.find_element(By.TAG_NAME, 'body')
        content = elements.text
        json_data = json.loads(content)
        nft_list = json_data.get("results", [])
        nft_list_count = len(nft_list)
        msg = f"index:{index} offset:{offset} count:{nft_list_count}"
        logging.info(msg)

        collections_total_nft_count += nft_list_count
        collections_total_nft.extend(nft_list)
        if (nft_list_count < 150) or (not nft_list):
            break
        index += 1
        offset += 150

    data = {"result": collections_total_nft}
    save = save_data_to_file(collection, data)
    # 若保存失败,则跳出
    msg = f"{collection} total count:{collections_total_nft_count}"
    logging.info(msg)


def test_visit():
    """
    访问测试
    """
    service = get_selenium_webservice()
    driver = webdriver.Chrome(service=service)

    url = "https://magiceden.io/popular-collections"
    logging.info(url)

    driver.get(url)
    time.sleep(10)



if __name__ == "__main__":
    # test_crawler()
    test_visit()
    # main()

#encoding=utf-8
from cgitb import handler
import time
import json
import random
import platform
import logging
import urllib.parse
import pymysql
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
        service = Service(executable_path="C:\crawler\chromedriver.exe")
    elif platform_str == "Darwin":
        service = Service(executable_path="/Users/zhaopengfei/work/driver/chromedriver.exe")
    else:
        service = Service(executable_path="/data/driver/chromedriver.exe")

    return service


def connect_mysql(host='127.0.0.1', user=None, passwd=None, db=None):
    """
    连接mysql
    """
    conn = pymysql.connect(host=host, user=user, password=passwd, db=db)
    return conn


def get_collections(collection_id=None):
    """
    查询所有的collection
    """
    conn = connect_mysql(host=HOST, user=USER, passwd=PASSWD, db="sol_data")
    cur = conn.cursor()
    if collection_id:
        sql = f"SELECT id, symbol FROM sol_data.magic_collection where id={collection_id}"
    else:
        sql = "SELECT id, symbol FROM sol_data.magic_collection where synced=0 order by id desc limit 100"
    cur.execute(sql)
    symbols = cur.fetchall()
    conn.close()

    all_symbols = {}
    symbols_set = set()
    for i in symbols:
        symbol_id = i[0]
        symbol_name = i[1]
        if not symbol_name:
            continue
        col_name = str(symbol_name).strip()
        if col_name not in symbols_set:
            all_symbols[symbol_id] = col_name
            symbols_set.add(col_name)

    return all_symbols


def main():
    """
    crawler by collection
    """
    collections = get_collections(collection_id=COLLECTION_ID)
    
    conn = connect_mysql()
    
    service = get_selenium_webservice()
    driver = webdriver.Chrome(service=service)
    
    col_index = 1
    for col_id, col_value in collections.items():
        collection = str(col_value).lower().strip()
        if not collection:
            continue
        msg = f"--------------------process: {col_index} col: {collection}"
        logging.info(msg)
        offset = 0
        index = 0
        collections_total_nft_count = 0
        collections_total_nft = []
        while True:
            payload = {"$match":{"collectionSymbol":collection},"$sort":{"takerAmount":1},"$skip":offset,"$limit":150,"status":["all"]}

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
        file_name = f"/Users/zhaopengfei/work/collection_data/{collection}.json"
    else:
        file_name = f"/Users/zhaopengfei/work/collection_data/{collection}.json"
    return file_name


def test_collections():
    collections = get_collections()
    for col_id, col_value in collections.items():
        col_name = str(col_value).strip()
        msg = f"{col_id} {col_name}"
        logging.info(msg)


if __name__ == "__main__":
    # main()
    test_collections()

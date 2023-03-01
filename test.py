#encoding=utf-8
import time
import json
import random
import platform
import logging
from collections import defaultdict

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)


def test():
    """
    test by collection
    """
    # collection = 'bbcf_new'
    collection = 'mongomons'
    result = read_data_from_file(collection)
    data_list = result.get("result", [])
    titles = set()
    count = defaultdict(int)
    for data in data_list:
        title = data.get("title")
        count[title] += 1
        if not title:
            continue
        titles.add(title)
    print("data count: ", len(data_list))
    print("title count: ", len(titles))
    # print(count)
    
    
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


def read_data_from_file(collection):
    """
    读数据
    """
    file_name = get_file_name(collection)
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
    except Exception as e:
        logging.info(e)
        return None
    return data


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


if __name__ == "__main__":
    test()

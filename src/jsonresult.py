import csv
import datetime
import json
import os
import time


# def JsonWrite(name,item):
#     if not os.path.exists('output'):
#             os.mkdir('output')
#
#     """
#     处理item
#     """
#     now = datetime.datetime.now()
#     file_name = name + '.jsonl'
#     file = open(f'output/{file_name}', 'at', encoding='utf-8')
#     item['crawl_time'] = int(time.time())
#     line = json.dumps(dict(item), ensure_ascii=False) + "\n"
#     file.write(line)
#     file.flush()

def JsonWrite(name, item):
    if not os.path.exists('output'):
        os.mkdir('output')

    now = datetime.datetime.now()
    file_name = name + '.csv'
    file_path = f'output/{file_name}'

    # 检查文件是否存在，以确定是写入头部还是追加内容
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=item.keys())

        if not file_exists:
            # 如果文件不存在，写入头部
            writer.writeheader()

        # 添加时间戳并写入数据
        item['crawl_time'] = int(time.time())
        writer.writerow(item)
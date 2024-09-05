import json
import multiprocessing

import time
from datetime import datetime

from fastapi import APIRouter, Request, WebSocket

from fastapi.encoders import jsonable_encoder

from tortoise.contrib.pydantic import PydanticModel


from src.douyinspider import DouyinspiderSpider
from src.video import VideoSpider
from src.weibospider import WeibospiderSpider
from src.weitoutiao import WeitoutiaoSpider
from src.xiaoshipin import XiaoshipinSpider
from src.zonghe import ToutiaospiderSpider

router = APIRouter()


class key(PydanticModel):
    key: str
    st: str
    et: str


@router.post("/search")
async def run(request: Request, data: key):
    clear()
    s_time = time.time()
    pool = multiprocessing.Pool(6)
    pool.apply_async(WeibospiderSpider, args=(data.key,data.st,data.et))
    pool.apply_async(DouyinspiderSpider, args=(data.key,))
    pool.apply_async(WeitoutiaoSpider, args=(data.key,))
    pool.apply_async(XiaoshipinSpider, args=(data.key,data.st,data.et))  # 在进程池中异步执行请求处理函数
    pool.apply_async(VideoSpider, args=(data.key,data.st,data.et))  # 在进程池中异步执行请求处理函数
    pool.apply_async(ToutiaospiderSpider, args=(data.key,data.st,data.et))

    pool.close()
    pool.join()  # 等待所有进程结束
    # 初始化一个空列表，用来存储解析后的数据
    data_list = []

    # 打开文件并逐行读取
    with open('output/抖音.jsonl', 'r', encoding='utf-8') as file:
        for line in file:

            data = json.loads(line)


            data_list.append(data)
    with open('output/微博.jsonl', 'r', encoding='utf-8') as file:
        for line in file:

            data = json.loads(line)


            data_list.append(data)
    with open('output/今日头条小视频.jsonl', 'r', encoding='utf-8') as file:
        for line in file:

            data = json.loads(line)

            data_list.append(data)
    with open('output/今日头条微头条.jsonl', 'r', encoding='utf-8') as file:
        for line in file:

            data = json.loads(line)


            data_list.append(data)
    with open('output/今日头条资讯.jsonl', 'r', encoding='utf-8') as file:
        for line in file:

            data = json.loads(line)

            data_list.append(data)
    with open('output/今日头条视频.jsonl', 'r', encoding='utf-8') as file:
        for line in file:

            data = json.loads(line)

            data_list.append(data)
    # 根据日期时间对数据进行排序
    sorted_data_list = sorted(data_list, key=lambda x: x['timestamp'])

    # 计算条目总数
    total_count = len(sorted_data_list)

    # 打印排序后的数据和条目总数
    for item in sorted_data_list:
        print(item)
    print(f"Total count: {total_count}")

    e_time = time.time()
    run_time = e_time - s_time
    print(f"程序运行时间为：{run_time}秒")
    return {"message": "请求处理完成"}



def clear():
    with open('output/今日头条小视频.jsonl', 'w') as file:
        pass
    with open('output/今日头条微头条.jsonl', 'w') as file:
        pass
    with open('output/今日头条视频.jsonl', 'w') as file:
        pass

    with open('output/今日头条资讯.jsonl', 'w') as file:
        pass

    with open('output/微博.jsonl', 'w') as file:
        pass
    with open('output/抖音.jsonl', 'w') as file:
        pass

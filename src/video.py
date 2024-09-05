import requests


import time

import datetime

import json
import re

from src.jsonresult import JsonWrite


def date_timestamp(day):
    if day.count('-') == 0:
        timeArray = time.strptime(day.strip(), "%Y")
    elif day.count('-') == 1:
        timeArray = time.strptime(day.strip(), "%Y-%m")
    elif day.count('-') == 2:
        timeArray = time.strptime(day.strip(), "%Y-%m-%d")
    else:
        raise ValueError('日期格式错误')
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def VideoSpider(key, startTime, endTime):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie': 'tt_webid=7353547544990041615; _S_DPR=1.25; _S_IPAD=0; s_v_web_id=verify_lxvi2fst_eCxwlsaA_g4OB_4mQA_AH0O_t9xjmyqJFMBq; notRedShot=1; WIN_WH=2000_1038; PIXIEL_RATIO=1.25; FRM=new; passport_csrf_token=5b5eb6bdaf871d44d9bc959b8f19d692; passport_csrf_token_default=5b5eb6bdaf871d44d9bc959b8f19d692; _ga=GA1.1.1821336777.1712131223; _ga_1Y7TBPV8DE=GS1.1.1719826734.1.1.1719826791.0.0.0; _tea_utm_cache_4916=undefined; __ac_nonce=066ab28be00efd9a6ac38; __ac_signature=_02B4Z6wo00f01RR3AlAAAIDBI1PGDfTSXh0UVwbAACO5c1; __ac_referer=__ac_blank; ttwid=1%7CSMkGnVMLymjgsCqv6eopWSv9qX5sfEQDPFGZ5MySNvM%7C1722493221%7C8a07560684008301cad201617ca6e5f9ab61be9ee03a015ef49efe753cd88aaf; _ga_QEHZPBE5HH=GS1.1.1722492686.52.1.1722493224.0.0.0; _S_WIN_WH=2000_1036'}

    # with open('cookie_video', 'r') as file:
    #     for cookie in file.readlines():
    #         cookie_read = cookie.strip()
    # cookie = {
    #     'Cookie': cookie_read
    # }
    # print(cookie['Cookie'])

    # 方式一: 在init方法中获取参数
    keywords = key
    print('keywords: ', keywords)
    page = 0
    start_time = startTime
    end_time = endTime
    if start_time:
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
    else:
        start_time = None
    if end_time:
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
    else:
        end_time = None

    """
    爬虫入口
    """
    if not start_time:
        start_time = datetime.datetime(year=2024, month=6, day=23)
    else:
        start_time = start_time
    if not end_time:
        end_time = datetime.datetime(year=2024, month=6, day=24)
    else:
        end_time = end_time

    keyword = keywords
    min_time = int(datetime.datetime.timestamp(start_time))
    max_time = int(datetime.datetime.timestamp(end_time))
    # print(min_time, max_time)
    if keywords:
        # cmd = 'node - e "require(\" %s\").init()"' %('./ norm')
        # pipeline = os.popen(cmd)
        # signature = pipeline.read()
        # print(signature)

        url = f"https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={keyword}&pd=video&action_type=search_subtab_switch&from=video&cur_tab_title=video&page_num=0&search_id=&min_time={min_time}&max_time={max_time}"
        print(url)
        response = requests.get(url, headers=headers)

    """
    网页解析
    """
    # Cookie = response.cookies
    # if Cookie:
    #     Cookie = Cookie.decode('utf-8')
    #     # print(Cookie)
    #     with open('cookie_video', 'w') as file:
    #         file.write(str(Cookie))

    keywords = keywords
    html = response.text

    # print(html)
    LoadMore = r'/*# sourceMappingURL=LoadMore(.*)?<script nonce='
    LoadMore = re.findall(LoadMore, html, re.S | re.M)
    # print(LoadMore)
    rawdata = re.findall('"rawData":(.*?)</script>', str(LoadMore))

    res_id = r'\"group_id\":\"(.*?)\"'
    ids = re.findall(res_id, str(rawdata[0]), re.S | re.M)
    id_list = []
    for item in ids:
        if item not in id_list:
            id_list.append(item)

    # print(1)
    # print(id_list)
    # 点赞
    res_like = r'\"digg_count\":(\d+)'
    likes = re.findall(res_like, str(rawdata[0]), re.S | re.M)
    # print("点赞:",likes)
    # 评论
    res_comment = r'\"comment_count\":(\d+)'
    comment = re.findall(res_comment, str(rawdata[0]), re.S | re.M)
    # print("评论:",comment)
    # 时间
    res_time = r'\"datetime\":"(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})'
    time = re.findall(res_time, str(rawdata[0]), re.S | re.M)
    # print("时间:",time)
    # 播放量
    res_read = r'\"play_count\":(\d+)'
    reads = re.findall(res_read, str(rawdata[0]), re.S | re.M)
    # 作者
    res_name = r'\"media_name\":\"(.*?)\"'
    author_name = re.findall(res_name, str(rawdata[0]), re.S | re.M)
    # url
    res_url = r'\"source_url\":\"(.*?)\"'
    source_url = re.findall(res_url, str(rawdata[0]), re.S | re.M)
    # print("播放量:",reads)
    # 内容
    res_text = r'\"summary\":"([\u4e00-\u9fa5a-zA-Z\d# \\⚡️🍵/.，。？！?!‼️⁉️]*)'
    texts = re.findall(res_text, str(rawdata[0]), re.S | re.M)
    text_list = texts[::2]
    # for item in texts:
    #     if item not in text_list:
    #         text_list.append(item)
    # print("标题:",text_list)
    # print(rawdata[0])
    # ids = list(set(ids))
    # # print(1)
    # print(ids)

    # with open('./video_ids.txt', 'a') as file:
    #     for item in id_list:
    #         file.write(str(item) + '\n')

    video_list = []
    for i in range(len(id_list)):
        res_dict = {}
        res_dict['id'] = id_list[i]
        res_dict['title'] = text_list[i][0:16]
        res_dict['media_type'] = '视频'
        res_dict['date'] = time[i]
        res_dict['url'] = source_url[i]
        res_dict['text'] = text_list[i]
        res_dict['keyword'] = keywords
        res_dict['like'] = likes[i]
        res_dict['comment'] = comment[i]
        res_dict['read'] = reads[i]
        res_dict['author_name'] = author_name[i]
        date_time = datetime.datetime.strptime(time[i], '%Y-%m-%d %H:%M')

        # 将datetime对象转换为UNIX时间戳
        res_dict['timestamp'] = int(datetime.datetime.timestamp(date_time))
        video_list.append(res_dict)
        # print(res_dict)
    for item in video_list:
        JsonWrite('今日头条视频',item)

if __name__ == '__main__':
    VideoSpider('奥运会','2024-7-30','2024-7-31')

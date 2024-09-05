import os

import time

import datetime

import json
import re

import requests

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


def ToutiaospiderSpider(key, start_date, end_date):
    name = "今日头条资讯"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie': 'tt_webid=7353547544990041615; _S_DPR=1.25; _S_IPAD=0; s_v_web_id=verify_lxvi2fst_eCxwlsaA_g4OB_4mQA_AH0O_t9xjmyqJFMBq; notRedShot=1; WIN_WH=2000_1038; PIXIEL_RATIO=1.25; FRM=new; passport_csrf_token=5b5eb6bdaf871d44d9bc959b8f19d692; passport_csrf_token_default=5b5eb6bdaf871d44d9bc959b8f19d692; _ga=GA1.1.1821336777.1712131223; _ga_1Y7TBPV8DE=GS1.1.1719826734.1.1.1719826791.0.0.0; _tea_utm_cache_4916=undefined; __ac_nonce=066ab28be00efd9a6ac38; __ac_signature=_02B4Z6wo00f01RR3AlAAAIDBI1PGDfTSXh0UVwbAACO5c1; __ac_referer=__ac_blank; ttwid=1%7CSMkGnVMLymjgsCqv6eopWSv9qX5sfEQDPFGZ5MySNvM%7C1722493221%7C8a07560684008301cad201617ca6e5f9ab61be9ee03a015ef49efe753cd88aaf; _ga_QEHZPBE5HH=GS1.1.1722492686.52.1.1722493224.0.0.0; _S_WIN_WH=2000_1036'}

    # with open('./cookie', 'r') as file:
    #     for cookie in file.readlines():
    #         cookie_read = cookie.strip()
    # cookie = {
    #     'Cookie': cookie_read
    # }

    # 方式一: 在init方法中获取参数
    keywords = key
    print('keywords: ', keywords)
    page = 0
    start_time = start_date
    end_time = end_date
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

    keywords = keywords
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
        url = f"https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={keyword}&pd=information&action_type=search_subtab_switch&search_id=&from=news&cur_tab_title=news&min_time={min_time}&max_time={max_time}&page_num=0"
        # print(url)
        response = requests.get(url, headers=headers)

    # Cookie = response.request.headers.get('Cookie')
    # Cookie = Cookie.decode('utf-8')
    # # print(Cookie)
    # with open('./cookie', 'w') as file:
    #     file.write(str(Cookie))

    keywords = keywords
    html = response.text
    # print(html)
    res_id = r'\"group_id\":\"(.*?)\"'
    ids = re.findall(res_id, html, re.S | re.M)
    ids = list(set(ids))
    # print(1)
    # print(ids)
    with open('./keyword.txt', 'w') as file:
        file.write(str(keywords) + '\n')
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
    # comment = comment[::2]
    # print("评论:",comment)
    # 时间
    res_time = r'\"create_time\":"(\d+)'
    time_list = re.findall(res_time, str(rawdata[0]), re.S | re.M)
    # time_list = time_list[::2]
    for i in range(len(time_list)):
        tmp = time.localtime(int(time_list[i]))
        time_list[i] = time.strftime("%Y-%m-%d %H:%M", tmp)

    # print("时间:",time)
    # 播放量
    res_read = r'\"read_count\":(\d+)'
    reads = re.findall(res_read, str(rawdata[0]), re.S | re.M)
    # reads = reads[::2]

    # 作者
    res_name = r'\"media_name\":\"(.*?)\"'
    author_name = re.findall(res_name, str(rawdata[0]), re.S | re.M)
    # name_list = author_name[::]
    # url
    res_url = r'\"share_url\":\"(.*?)\"'
    source_url = re.findall(res_url, str(rawdata[0]), re.S | re.M)
    url_list = source_url
    # print("播放量:",reads)
    # 内容
    res_text = r'\"title\":\"(.*?)\"'
    texts = re.findall(res_text, str(rawdata[0]), re.S | re.M)
    texts = texts[::3]
    # print(rawdata[0])
    # texts = re.findall(r'\"title\":(.*)","des', str(texts), re.S | re.M)
    # text_list = texts[::2]

    # for item in texts:
    #     if item not in text_list:
    #         text_list.append(item)
    # print("标题:",text_list)
    # print(rawdata[0])
    # ids = list(set(ids))
    # # print(1)
    # print(ids)

    video_list = []
    for i in range(len(id_list)):
        res_dict = {}
        res_dict['id'] = id_list[i]
        res_dict['title'] = texts[i]
        res_dict['media_type'] = '短视频'
        res_dict['date'] = time_list[i]
        res_dict['url'] = url_list[i]
        res_dict['text'] = texts[i]
        res_dict['keyword'] = keywords
        res_dict['like'] = likes[i]
        res_dict['comment'] = comment[i]
        # res_dict['transpond'] = share[i]
        res_dict['read'] = reads[i]
        res_dict['author_name'] = author_name[i]
        video_list.append(res_dict)
        # 假设你有一个日期字符串
        # 将字符串转换为datetime对象
        date_time = datetime.datetime.strptime(time_list[i], '%Y-%m-%d %H:%M')

        # 将datetime对象转换为UNIX时间戳
        res_dict['timestamp'] = int(datetime.datetime.timestamp(date_time))
        # print(res_dict)
        JsonWrite(name, res_dict)

if __name__ == '__main__':
    ToutiaospiderSpider('奥运', '2024-7-30', '2024-7-31')
    # if len(ids)==10:
    #     keyword = keywords
    #     min_time = int(datetime.datetime.timestamp(start_time))
    #     max_time = int(datetime.datetime.timestamp(end_time))
    #
    #     # print(page)
    #
    #     page += 1
    #     url = f"https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={keyword}&pd=information&action_type=search_subtab_switch&search_id=&from=news&cur_tab_title=news&min_time={min_time}&max_time={max_time}&page_num={page}"
    #     yield Request(url, callback=parse, meta={'keyword': keyword,'id': id, 'min_time':min_time, 'max_time':max_time})
    # else:
    #     pass

    # for id in ids:
    #     execute('scrapy crawl article -a key={} -a id={}'.format(str(keywords), str(id)).split())

    # if '<p>抱歉，未找到相关结果。</p>' in html:
    #     logger.info(f'no search result. url: {response.url}')
    #     return
    # tweets_infos = re.findall('<div class="from"\s+>(.*?)</div>', html, re.DOTALL)
    # for tweets_info in tweets_infos:
    #     tweet_ids = re.findall(r'weibo\.com/\d+/(.+?)\?refer_flag=1001030103_" ', tweets_info)
    #     for tweet_id in tweet_ids:
    #         url = f"https://weibo.com/ajax/statuses/show?id={tweet_id}"
    #         yield Request(url, callback=parse_tweet, meta=response.meta, priority=10)
    # next_page = re.search('<a href="(.*?)" class="next">下一页</a>', html)
    # if next_page:
    #     url = "https://s.weibo.com" + next_page.group(1)
    #     yield Request(url, callback=parse, meta=response.meta)

# @staticmethod
# def parse_tweet(response):
#     """
#     解析推文
#     """
#     data = json.loads(response.text)
#     item = common.parse_tweet_info(data)
#     item['keyword'] = response.meta['keyword']
#     if item['isLongText']:
#         url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
#         yield Request(url, callback=common.parse_long_tweet, meta={'item': item}, priority=20)
#     else:
#         yield item

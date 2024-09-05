import datetime

import json
import re

import requests

import common
from src.jsonresult import JsonWrite

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': 'SINAGLOBAL=8722282712197.711.1711795521101; UOR=,,cn.bing.com; _s_tentry=-; Apache=9180041998542.354.1722480007866; ULV=1722480007897:6:1:2:9180041998542.354.1722480007866:1722305457565; XSRF-TOKEN=7L7GTtO8P20xYxygmaDH886v; SCF=AnexzcPsBUFUc1UFYOjzuQNMlLPezBKz1-VEUDq2qMoQ434aiFsvHG-Y1RqipmYb12islKrfg3kawAVnoD5yzqU.; SUB=_2A25Lr2u3DeRhGeFJ4lMT-CjJzTuIHXVoxeF_rDV8PUNbmtB-LVrMkW9NfsI0UFEo6z-CkD-urCN0iwjE6gU4ljN_; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5pHYsWn7k58fcQYPgMxdgG5JpX5KzhUgL.FoMN1K2E1hqfSoM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNS0.peoncSKqN; ALF=02_1725081832; WBPSESS=c_qEkUFwjhlStXswyQ4PAn00_m-xZ8QJsWAl1WQjcR6YETnYviXOeDDVRudm95u37td3UJAlWwobXrBbAxfZi1yPPH9OT68UlUGz1_SVcw2skXe1VQoLEh5bvomR6wbH'
}

name = "微博"
def WeibospiderSpider(key, start_date, end_date):


    keywords = key
    print('keywords: ', keywords)
    start_time = start_date
    end_time = end_date
    if start_time:
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
    else:
        start_time = None
    if end_time:
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
        end_time -= datetime.timedelta(days=1)
    else:
        end_time = None

    """
    爬虫入口
    """
    if not start_time:
        start_time = datetime.datetime(year=2024, month=6, day=24, hour=0)
    else:
        start_time = start_time
    if not end_time:
        end_time = datetime.datetime(year=2024, month=6, day=24, hour=23)
    else:
        end_time = end_time
    # 是否按照小时进行切分，数据量更大; 对于非热门关键词**不需要**按照小时切分
    is_split_by_hour = False
    keyword = keywords
    if keywords:
        if not is_split_by_hour:
            _start_time = start_time.strftime("%Y-%m-%d")+'-0'
            _end_time = end_time.strftime("%Y-%m-%d")+'-23'
            url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom%3A{_start_time}%3A{_end_time}&page=1"
            print(url)
            response = requests.get(url, headers=headers)
            parse(response, keywords, headers)
            # print(response.text)
            # return 0
            # yield Request(url, callback=parse, meta={'keyword': keyword}, headers=headers)
        else:
            time_cur = start_time
            while time_cur < end_time:
                _start_time = time_cur.strftime("%Y-%m-%d")
                _end_time = (time_cur + datetime.timedelta(hours=1)).strftime("%Y-%m-%d")
                url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom%3A{_start_time}%3A{_end_time}&page=1"
                # print(url)
                response = requests.get(url, headers=headers)
                parse(response, keywords, headers)
                # yield Request(url, callback=parse, meta={'keyword': keyword}, headers=headers)
                time_cur = time_cur + datetime.timedelta(hours=1)


def parse(response, keywords, headers):
    """
    网页解析
    """
    html = response.text
    # print(html)
    if '<p>抱歉，未找到相关结果。</p>' in html:
        print(f'no search result. url: {response.url}')
        return
    tweets_infos = re.findall('<div class="from"\s+>(.*?)</div>', html, re.DOTALL)
    for tweets_info in tweets_infos:
        tweet_ids = re.findall(r'weibo\.com/\d+/(.+?)\?refer_flag=1001030103_" ', tweets_info)
        for tweet_id in tweet_ids:
            url = f"https://weibo.com/ajax/statuses/show?id={tweet_id}"
            # print(url)
            response = requests.get(url, headers=headers)
            parse_tweet(response, keywords, headers)
            # yield Request(url, callback=parse_tweet, meta=response.meta, priority=10, headers=headers)
    next_page = re.search('<a href="(.*?)" class="next">下一页</a>', html)
    # if next_page:
    #     url = "https://s.weibo.com" + next_page.group(1)
    #     print(url)
    #     response = requests.get(url, headers=headers)
    #     parse(response, keywords, headers)
    #     # yield Request(url, callback=parse, meta=response.meta, headers=headers)


@staticmethod
def parse_tweet(response,keywords, headers):
    """
    解析推文
    """
    data = json.loads(response.text)
    item = common.parse_tweet_info(data)
    item['keyword'] = keywords
    if item['isLongText']:
        url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
        # print(url)
        response = requests.get(url, headers=headers)
        common.parse_long_tweet(response, item, headers)
        # yield Request(url, callback=common.parse_long_tweet, meta={'item': item}, priority=20, headers=headers)
    else:
        JsonWrite(name,item)

        # yield item


if __name__ == '__main__':
    WeibospiderSpider('奥运', '2024-7-30', '2024-7-31')

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


def XiaoshipinSpider(key, startTime, endTime):
    name = "今日头条小视频"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie': 'tt_webid=7353547443977913871; _ga=GA1.1.1236590485.1712131199; _tea_utm_cache_4916=undefined; _S_DPR=1.25; _S_IPAD=0; s_v_web_id=verify_ly2qj6gj_IVG1AEbe_VnJq_4Ds8_BEW7_IPF2VFOmViom; msToken=Y-1vYEqW6HOWdP_RzOk_3wIq4tc3K2ruOJI51-pv4XRIgPWRdVuOErgaWWj-MWhOVYKAJZyCrYADEuxTCxiP1bblNCIjTY8kGmWhAWw=; notRedShot=1; _S_WIN_WH=1172_1010; __ac_nonce=06683b7ce00b3d61ad357; __ac_signature=_02B4Z6wo00f019os4zwAAIDCDerORZatWqfaDeeAAJAR59; __ac_referer=__ac_blank; _ga_QEHZPBE5HH=GS1.1.1719908305.5.1.1719909159.0.0.0; ttwid=1%7Ck2XvQYt6A_wovcniQDHxFuxE6B_tgj-1cQ5mHOx5ZoA%7C1719909160%7Ca3e5f8cdf97fef1ce9bafb3e143c24156389813242b62335d8c4699d08782314'}

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

        url = f"https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={keyword}&pd=xiaoshipin&action_type=search_subtab_switch&from=xiaoshipin&cur_tab_title=video&page_num=0&search_id=&min_time={min_time}&max_time={max_time}"
        # print(url)
        response = requests.get(url, headers=headers)
        """
        网页解析
        """
        # Cookie = response.request.headers.get('Cookie')
        # Cookie = Cookie.decode('utf-8')
        # print(Cookie)
        # with open('./cookie_video', 'w') as file:
        #     file.write(str(Cookie))

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
        comment = comment[::2]
        # print("评论:",comment)
        # 时间
        res_time = r'\"create_time\":(\d+)'
        time_liat = re.findall(res_time, str(rawdata[0]), re.S | re.M)
        time_list = time_liat[::2]
        for i in range(len(time_list)):
            tmp = time.localtime(int(time_list[i]))
            time_list[i] = time.strftime("%Y-%m-%d %H:%M", tmp)

        # print("时间:",time)
        # 播放量
        res_read = r'\"play_count\":(\d+)'
        reads = re.findall(res_read, str(rawdata[0]), re.S | re.M)
        reads = reads[::2]
        # 转发
        res_share = r'\"share_count\":(\d+)'
        share = re.findall(res_share, str(rawdata[0]), re.S | re.M)

        # 作者
        res_name = r'\"user_nickname\":\"(.*?)\"'
        author_name = re.findall(res_name, str(rawdata[0]), re.S | re.M)
        # name_list = author_name[::]
        # url
        res_url = r'\"share_url\":\"(.*?)\"'
        source_url = re.findall(res_url, str(rawdata[0]), re.S | re.M)
        url_list = source_url[::2]
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

        # with open('./xiaoshipin_ids.txt', 'a') as file:
        #     for item in id_list:
        #         file.write(str(item) + '\n')

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
            res_dict['transpond'] = share[i]
            res_dict['read'] = reads[i]
            res_dict['author_name'] = author_name[i]
            date_time = datetime.datetime.strptime(time_list[i], '%Y-%m-%d %H:%M')

            # 将datetime对象转换为UNIX时间戳
            res_dict['timestamp'] = int(datetime.datetime.timestamp(date_time))
            video_list.append(res_dict)
            # print(res_dict)
        for item in video_list:
            # print(item)
            JsonWrite(name, item)

if __name__ == '__main__':
    XiaoshipinSpider('奥运','2024-7-30','2024-7-31')

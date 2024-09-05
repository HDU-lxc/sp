import time
import datetime

import json
import re

import requests

from src.jsonresult import JsonWrite

name = "今日头条微头条"
def WeitoutiaoSpider(key):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie': 'tt_webid=7353547544990041615; _S_DPR=1.25; _S_IPAD=0; s_v_web_id=verify_lxvi2fst_eCxwlsaA_g4OB_4mQA_AH0O_t9xjmyqJFMBq; notRedShot=1; WIN_WH=2000_1038; PIXIEL_RATIO=1.25; FRM=new; passport_csrf_token=5b5eb6bdaf871d44d9bc959b8f19d692; passport_csrf_token_default=5b5eb6bdaf871d44d9bc959b8f19d692; _ga=GA1.1.1821336777.1712131223; _ga_1Y7TBPV8DE=GS1.1.1719826734.1.1.1719826791.0.0.0; _tea_utm_cache_4916=undefined; __ac_nonce=066ab28be00efd9a6ac38; __ac_signature=_02B4Z6wo00f01RR3AlAAAIDBI1PGDfTSXh0UVwbAACO5c1; __ac_referer=__ac_blank; ttwid=1%7CSMkGnVMLymjgsCqv6eopWSv9qX5sfEQDPFGZ5MySNvM%7C1722493221%7C8a07560684008301cad201617ca6e5f9ab61be9ee03a015ef49efe753cd88aaf; _ga_QEHZPBE5HH=GS1.1.1722492686.52.1.1722493224.0.0.0; _S_WIN_WH=2000_1036'}

    cookie = {
        'Cookie': 'tt_webid=7353547544990041615; _S_DPR=1.25; _S_IPAD=0; s_v_web_id=verify_lxvi2fst_eCxwlsaA_g4OB_4mQA_AH0O_t9xjmyqJFMBq; notRedShot=1; WIN_WH=2000_1038; PIXIEL_RATIO=1.25; FRM=new; passport_csrf_token=5b5eb6bdaf871d44d9bc959b8f19d692; passport_csrf_token_default=5b5eb6bdaf871d44d9bc959b8f19d692; _ga=GA1.1.1821336777.1712131223; _ga_1Y7TBPV8DE=GS1.1.1719826734.1.1.1719826791.0.0.0; _tea_utm_cache_4916=undefined; _S_WIN_WH=2000_1038; __ac_nonce=066878bec002c72397fef; __ac_signature=_02B4Z6wo00f010x3QuQAAIDDe1OGuIXcasdMV0ZAALWl06; __ac_referer=https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword=%E7%8E%8B%E8%80%81%E5%90%89&pd=weitoutiao&action_type=search_subtab_switch&page_num=0&search_id=&from=weitoutiao&cur_tab_title=weitoutiao; msToken=t26Aru2kNnHSg44IyaaZI3zYKJtHKKrOR1TRGeoXnnOmu9gz8bQJDZ1eP9Js7x3-n_uWF2d_cAo3l-C4zFHEeyuR71KuGXFHfKlell-C; _ga_QEHZPBE5HH=GS1.1.1720157995.33.1.1720159646.0.0.0; ttwid=1%7CSMkGnVMLymjgsCqv6eopWSv9qX5sfEQDPFGZ5MySNvM%7C1720159647%7C516ce5ec98e6b67cf385dcb79806774504d6fc428785df3bc24045fc83c64c31'
    }

    keywords = key
    # print('keywords: ', .keywords)
    page = 0
    keyword = keywords

    if keywords:
        url = f"https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={keyword}&pd=weitoutiao&action_type=search_subtab_switch&from=weitoutiao&cur_tab_title=weitoutiao&page_num={page}&search_id="
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            parse(response,page,keywords,headers)



def parse(response, page, keywords, headers):
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

    res_id = r'"fw_id":(\d+)'
    ids = re.findall(res_id, str(rawdata[0]), re.S | re.M)
    id_list = []
    for item in ids:
        if item not in id_list:
            id_list.append(item)

    # # print(1)
    # # print(id_list)
    # 点赞
    res_like = r'\"digg_count\":(\d+)'
    likes = re.findall(res_like, str(rawdata[0]), re.S | re.M)
    likes = likes[::3]
    # print("点赞:",likes)
    # 评论
    res_comment = r'\"comment_count\":(\d+)'
    comment = re.findall(res_comment, str(rawdata[0]), re.S | re.M)
    comment = comment[::3]
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
    res_read = r'\"read_count\":(\d+)'
    reads = re.findall(res_read, str(rawdata[0]), re.S | re.M)
    # reads = reads[::2]
    # 转发
    res_share = r'\"share_count\":(\d+)'
    share = re.findall(res_share, str(rawdata[0]), re.S | re.M)

    # 作者
    res_name = r'\"media_name\":\"(.*?)\"'
    author_name = re.findall(res_name, str(rawdata[0]), re.S | re.M)
    # name_list = author_name[::]
    # url
    res_url = r'\"share_url\":\"(.*?)/\?'
    source_url = re.findall(res_url, str(rawdata[0]), re.S | re.M)
    url_list = source_url[::4]
    # print("播放量:",reads)
    # 内容
    res_text = r'\"content\":\"(.*?)\"'
    texts = re.findall(res_text, str(rawdata[0]), re.S | re.M)
    texts = texts[::2]

    # with open('./weitoutiao_ids.txt', 'a') as file:
    #     for item in id_list:
    #         file.write(str(item) + '\n')

    _list = []
    for i in range(len(id_list)):
        res_dict = {}
        res_dict['id'] = id_list[i]
        res_dict['title'] = texts[i]
        res_dict['media_type'] = '新闻'
        res_dict['date'] = time_list[i][0:16]
        res_dict['url'] = url_list[i]
        res_dict['text'] = texts[i]
        res_dict['keyword'] = keywords
        res_dict['like'] = likes[i]
        res_dict['comment'] = comment[i]
        res_dict['transpond'] = share[i]
        res_dict['read'] = reads[i]
        res_dict['author_name'] = author_name[i]
        date_time = datetime.datetime.strptime(time_list[i][0:16], '%Y-%m-%d %H:%M')

        # 将datetime对象转换为UNIX时间戳
        res_dict['timestamp'] = int(datetime.datetime.timestamp(date_time))
        _list.append(res_dict)
        # print(res_dict)

    for item in _list:
        JsonWrite(name,item)

    # if len(_list) == 10:
    #     keyword = keywords
    #
    #     page += 1
    #     url = f"https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={keyword}&pd=weitoutiao&action_type=search_subtab_switch&from=weitoutiao&cur_tab_title=weitoutiao&page_num={page}&search_id="
    #     response = requests.get(url, headers=headers)
    #     if response.status_code == 200:
    #         parse(response,page,keywords,headers)
    # else:
    #     pass
if __name__ == '__main__':
    WeitoutiaoSpider('奥运')

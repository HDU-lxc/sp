import time
import json
from datetime import datetime

import requests
import subprocess
from functools import partial

from src.jsonresult import JsonWrite

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')  #这三行代码需要放在导入execjs之前
import execjs
import urllib.parse

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


def DouyinspiderSpider(key):


        keywords = key
        print('keywords: ', keywords)

        """
        爬虫入口
        """
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': 's_v_web_id=verify_lx4a2dyz_KTWJMVQL_FM2X_44A8_A68a_tirDF0LhXRqF; passport_csrf_token=1753f449f5a74aa3fe7e3cddb33c534e; passport_csrf_token_default=1753f449f5a74aa3fe7e3cddb33c534e; bd_ticket_guard_client_web_domain=2; ttwid=1%7CmxQVC99jhxqhE5stlEBhBkpG4e3Xa4LPwemStfGd580%7C1719802225%7Cc0ff52838927929a084872c0a75b14061bc8c55391b41fd146faa11b2d8d6179; UIFID_TEMP=c4683e1a43ffa6bc6852097c712d14b81f04bc9b5ca6d30214b0e66b4e3852801b612978422ca0c438d6e0bf9e8bc8ed533e940d80dc4a763eaf9e445f7f235d803cc24e8d4dce08553d0c6f3af75ac6; dy_swidth=2048; dy_sheight=1152; fpk1=U2FsdGVkX19Rq9uSLgk1sXt/OyeoTr8i9VyBSQzLwrfX6zPX+28fnIia8KNaD00sa6WSqAse3gubYv20gfSNBQ==; fpk2=5f4591689f71924dbd1e95e47aec4ed7; UIFID=c4683e1a43ffa6bc6852097c712d14b81f04bc9b5ca6d30214b0e66b4e3852804dc072b7f9e7c454a0716441f3c7ee9f1679d81333dedffcb8aefa1847541c7fc4eed5460b3d5726ad261afe8f0a4b7d14cf61e49b7e4a95a4dc8c7764cf1a312c5af6277dc154b6213ad2ebf1ab32ec8457ec5c87a8f46b3ed3246c351ffae66294ec06af87a73804259afe39d147672bc738c435c0d1bdb890ea3dba11b08b; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2048%2C%5C%22screen_height%5C%22%3A1152%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; strategyABtestKey=%221720661243.385%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; xgplayer_user_id=63192188309; SEARCH_RESULT_LIST_TYPE=%22single%22; csrf_session_id=75d93a963e0ee5598d04df8037ee1d54; douyin.com; device_web_cpu_core=8; device_web_memory_size=8; architecture=amd64; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; xg_device_score=7.632684371023287; download_guide=%223%2F20240711%2F1%22; pwa2=%220%7C0%7C3%7C1%22; d_ticket=cbc5046c541314d67ba544bff87f0aa6e42bb; passport_assist_user=CkHI6Iw4Ysap-tdVQXGdEzf8UNNcBtt1bWdN_OYGlw6nDDKBPZ-SDEKKx1aXSeGc9h66AhcOlY4WvZY_2dFuTEnatBpKCjw-tZZqsfaA3VoZbgRd5OlxDI8cHwJcQfr0qWUSYEHs92dYuF2PQxoFLZY6gL56QD0ahQhiFDZv98muTDcQ-azWDRiJr9ZUIAEiAQN2-b7s; n_mh=sLXHKy0uxjF1kukfdJfiJwYKXJGC-ap4p8SnDnE0RqQ; sso_auth_status=51700c2557720caf80902e644d18cf97; sso_auth_status_ss=51700c2557720caf80902e644d18cf97; sso_uid_tt=e88241123121a9e3453e7032a75c9b81; sso_uid_tt_ss=e88241123121a9e3453e7032a75c9b81; toutiao_sso_user=b21096a2b08236ce3fe07bb03b1a7210; toutiao_sso_user_ss=b21096a2b08236ce3fe07bb03b1a7210; sid_ucp_sso_v1=1.0.0-KDRiNTczNmY3MjZkYTc2OWZiZjYwYzkxZWIyOTc2Njg4MzllMDM4MmQKIQiNh5Dq6YzbAhDxjr20BhjvMSAMMJCpp5sGOAJA8QdIBhoCbHEiIGIyMTA5NmEyYjA4MjM2Y2UzZmUwN2JiMDNiMWE3MjEw; ssid_ucp_sso_v1=1.0.0-KDRiNTczNmY3MjZkYTc2OWZiZjYwYzkxZWIyOTc2Njg4MzllMDM4MmQKIQiNh5Dq6YzbAhDxjr20BhjvMSAMMJCpp5sGOAJA8QdIBhoCbHEiIGIyMTA5NmEyYjA4MjM2Y2UzZmUwN2JiMDNiMWE3MjEw; passport_auth_status=ac5050636d943fe3b85b04303526605f%2C47a2036dfe8cde827698808f760613e0; passport_auth_status_ss=ac5050636d943fe3b85b04303526605f%2C47a2036dfe8cde827698808f760613e0; uid_tt=a59b9f4bc0053f4f36faaf0491d46e37; uid_tt_ss=a59b9f4bc0053f4f36faaf0491d46e37; sid_tt=5592f8b535da6787eab46355f1d18057; sessionid=5592f8b535da6787eab46355f1d18057; sessionid_ss=5592f8b535da6787eab46355f1d18057; publish_badge_show_info=%220%2C0%2C0%2C1720665975979%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=c5050d69654d7e27f61473d2adcb2e03; __security_server_data_status=1; sid_guard=5592f8b535da6787eab46355f1d18057%7C1720665983%7C5183989%7CMon%2C+09-Sep-2024+02%3A46%3A12+GMT; sid_ucp_v1=1.0.0-KDNhZjlkNGI3ZGIyOTY1MTgyNjZiZmE4MDAzNDkwODQzMDRiNWExNWYKGwiNh5Dq6YzbAhD_jr20BhjvMSAMOAJA8QdIBBoCbHEiIDU1OTJmOGI1MzVkYTY3ODdlYWI0NjM1NWYxZDE4MDU3; ssid_ucp_v1=1.0.0-KDNhZjlkNGI3ZGIyOTY1MTgyNjZiZmE4MDAzNDkwODQzMDRiNWExNWYKGwiNh5Dq6YzbAhD_jr20BhjvMSAMOAJA8QdIBBoCbHEiIDU1OTJmOGI1MzVkYTY3ODdlYWI0NjM1NWYxZDE4MDU3; biz_trace_id=2237289b; store-region=cn-zj; store-region-src=uid; passport_fe_beating_status=true; WallpaperGuide=%7B%22showTime%22%3A1720661633447%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A93%2C%22cursor2%22%3A0%2C%22hoverTime%22%3A1720665582671%7D; __ac_nonce=0669097cb00e5a185ba5d; __ac_signature=_02B4Z6wo00f012tRgmQAAIDDXHVGOOOZ0FNrcYbAALxQ6d; IsDouyinActive=true; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTWsvWWt2SVkzbkpUN292blJxeGxzUTJUT1hUYldFRC9tZFA0enJ2UWVJSk5kdTlZenh5WkdObEpJMlZXT3BPWENmbDhQSFVaSm44VEU4b0k5dWMxRVU9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; odin_tt=e35d8c8c469e6e10ed3f438ee0d0a2f16bd294807e775fb40af6cce33a9c1ae9fd6f1754c4acb0d30b74511d43f18487',
            'priority': 'u=1, i',
            'referer': 'https://www.douyin.com/search/%E5%86%9C%E5%A4%AB%E5%B1%B1%E6%B3%89?aid=3124ed1b-a3c7-48b4-80d4-fe620094706d&type=general',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'channel': 'channel_pc_web',
            'search_channel': 'aweme_general',
            'enable_history': '1',
            'filter_selected': '{"sort_type":"0","publish_time":"1"}',
            'keyword': keywords,
            'search_source': 'tab_search',
            'query_correct_type': '1',
            'is_filter_search': '1',
            'from_group_id': '',
            'offset': '0',
            'count': '30',
            'need_filter_settings': '1',
            'list_type': 'multi',
            'update_version_code': '170400',
            'pc_client_type': '1',
            'version_code': '190600',
            'version_name': '19.6.0',
            'cookie_enabled': 'true',
            'screen_width': '2048',
            'screen_height': '1152',
            'browser_language': 'zh-CN',
            'browser_platform': 'Win32',
            'browser_name': 'Edge',
            'browser_version': '126.0.0.0',
            'browser_online': 'true',
            'engine_name': 'Blink',
            'engine_version': '126.0.0.0',
            'os_name': 'Windows',
            'os_version': '10',
            'cpu_core_num': '8',
            'device_memory': '8',
            'platform': 'PC',
            'downlink': '3.4',
            'effective_type': '4g',
            'round_trip_time': '50',
            'webid': '7353547291875739146',
            'msToken': 'KW-NIPek2X3wbmBZVIuC2BwdWfhgzFBBjV_0iWn8S3CzcJ7LvJdRGWDvLkRAWAH5sJFc3wfrq2YKOaZgfwotm2Bw0gcWie-QI1rjlnFO9z-5SB1Lflk9enVs7eHJwKw=',
            # 'a_bogus': 'DJmZ/QggdD6ikfy65VdLfY3q6Ve3Y8Kx0CPYMD2fQxVTC639HMT49exE8bTv8UfjNs/DIeEjy4hjTpNME55rM1w3H8vO/2C2m6h0t-P2so0j53iJey8DE0hx-vj3Sla/RXNAEchMy7cbF8RDA9xamhK4bfebY7Y6i6trHf==',
        }
        # js = """
        # require('./env')
        # require('./source')
        #
        # function get_ab(params) {
        #     arguments = [0,
        #         1,
        #         8,
        #         params,
        #         ''
        #         , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0']
        #     var r = window.lxc._v;
        #     return (0,
        #         window.lxc._u)(r[0], arguments, r[1], r[2], this)
        # }
        #
        # """
        params_url = urllib.parse.urlencode(params)
        # print(params_url)
        with open("douyin.js", 'r') as file:
            result = file.read()
        a_bogus = execjs.compile(result).call('get_ab', params_url)
        # print(a_bogus)
        params['a_bogus'] = a_bogus
        url = 'https://www.douyin.com/aweme/v1/web/general/search/single?'+ urllib.parse.urlencode(params)

        response = requests.get(url,  headers=headers)

        with open('keyword.txt', 'w') as file:
            file.write(str(keywords) + '\n')
        status = response.text
        # print(status)
        status = json.loads(status)
        data = status['data']
        for item in data:
            if item['type'] == 1:
                res_dict = {}
                res_dict['id'] = item['aweme_info']['group_id']
                try:
                    res_dict['title'] = item['aweme_info']['share_info']['share_title']
                except KeyError:
                    res_dict['title'] = item['aweme_info']['desc']

                media_flag = item['aweme_info']['aweme_type']
                if media_flag == 0:
                    res_dict['media_type'] = '视频'
                elif media_flag == 68:
                    res_dict['media_type'] = '笔记'
                res_dict['source'] = '抖音'
                s_l = time.localtime(item['aweme_info']['create_time'])
                res_dict['date'] = time.strftime("%Y-%m-%d %H:%M:%S", s_l)
                res_dict['url'] = 'https://www.douyin.com/video/' + item['aweme_info']['group_id']
                res_dict['description'] = item['aweme_info']['desc']
                res_dict['keyword'] = keywords
                res_dict['likes'] = item['aweme_info']['statistics']['digg_count']
                res_dict['comment'] = item['aweme_info']['statistics']['comment_count']
                res_dict['transpond'] = item['aweme_info']['statistics']['share_count']
                # extra = json.loads(item['aweme_info']['anchor_info']['extra'])
                # print(type(extra))
                # res_dict['address'] = extra['address_info']['city']
                # ['address_info']['city']
                res_dict['author'] = item['aweme_info']['author']['nickname']
                date_time = datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", s_l), '%Y-%m-%d %H:%M:%S')

                # 将datetime对象转换为UNIX时间戳
                res_dict['timestamp'] = int(datetime.timestamp(date_time))
                # with open ('id.txt', 'a') as file:
                #     file.write(str(res_dict['id']) + '\n')
                # print(res_dict)
                JsonWrite('抖音', res_dict)
        # if len(data) == 30:
        #     headers = response.meta['headers']
        #     params = response.meta['params']
        #     params['offset'] = '45'
        #     # params['offset'] = str(int(params['offset'])+45)
        #     url = 'https://www.douyin.com/aweme/v1/web/general/search/single?' + urllib.parse.urlencode(params)
        #     yield Request(url, callback=parse, headers=headers,
        #                 meta={'keyword': keywords, 'headers':headers, 'params':params})


if __name__ == '__main__':
    DouyinspiderSpider('奥运会')




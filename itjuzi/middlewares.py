from itjuzi.settings import USER_AGENTS
import random
import time
# import requests
# import base64


# User-Agetn 下载中间件
class RandomUserAgent(object):
    def process_request(self, request, spider):
        # 这句话用于随机选择user-agent
        user_agent = random.choice(USER_AGENTS)
        date = time.strftime(u"%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        request.headers.setdefault('User-Agent', user_agent)
        request.cookies = {
            'Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89': '1510147146',
            'Hm_lvt_1c587ad486cdb6b962e94fc2002edf89': '1510147122',
            '_ga': 'GA1.2.1005162620.1510147122',
            '_gat': '1',
            '_gid': 'GA1.2.896314216.1510147122',
            'acw_tc': 'AQAAAOyEy0o3Mg8AkqHYPSaYL+d9YCwO',
            'gr_session_id_eee5a46c52000d401f969f4535bdaa78': '890e406b-822a-408b-a0f8-e803f81cda65',
            'gr_user_id': '659244f8-882f-4474-937a-4a540739470b',
            'identity': '18655118785%40test.com',
            'remember_code': 'DK7mTAbu%2Fa',
            'session': 'a4f49cb63dee56d72b30dbcf27bfed19184d9b83',
            'unique_token': '465991',
        }


class RandomProxy(object):
    def __init__(self):
        self.proxy_list = [
            '106.39.160.135:8888',
            '140.210.6.190:80',
            '58.83.183.139:80',
            '42.202.130.246:3128',
            '122.224.227.202:3128',
            '183.2.208.35:80',
            '116.199.115.79:80',
            '116.199.115.78:80',
            '116.199.2.209:80',
            '61.136.163.245:8103',
            '116.199.2.209:80',
            '116.199.2.210:80',
            '183.136.218.253:80',
            '106.14.51.145:8118',
            '58.56.128.84:9001',
            '183.62.196.10:3128',
            '111.155.116.208:8123'
        ]

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = "http://" + proxy
        print(proxy)

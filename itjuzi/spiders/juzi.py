# coding:utf-8

import scrapy
# from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from scrapy_redis.spiders import RedisCrawlSpider
from itjuzi.items import CompanyItem


#class ITjuziSpider(RedisCrawlSpider):
class ITjuziSpider(RedisCrawlSpider):
    name = 'itjuzi'
    allowed_domains = ['www.itjuzi.com']
    #start_urls = ['http://www.itjuzi.com/company?page=1/']
    redis_key = 'itjuzispider:start_urls'

    headers = {
        "Host": "www.itjuzi.com",
        "Connection": "keep-alive",
        #"Upgrade-Insecure-Requests" : "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        #"Referer": "http://www.itjuzi.com/company",
        "Cookie": "gr_user_id=b609a4a5-8b03-4078-85b5-0bb0e617daf5; _hp2_id.2147584538=%7B%22userId%22%3A%225361264262655533%22%2C%22pageviewId%22%3A%222812157498870176%22%2C%22sessionId%22%3A%221376560908636027%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%223.0%22%7D; identity=123636274%40qq.com; remember_code=3zB55lODqf; acw_tc=AQAAAMOWGBUfUwgAU3Awtjx04lI+Gr0e; acw_sc=589c0d25fa257c17aedfa3127a7c3a0eac145db7; session=4f1aec94fd99840a562f39488480a9b2798824f9; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1486565620,1486575689,1486603765,1486603844; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1486624109; ",
        #"If-Modified-Since": "Thu, 09 Feb 2017 03:35:25 GMT"

    }
    cookies = {
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
        'unique_token': '465991'
    }
    rules = [
        # 获取每一页的链接
        Rule(link_extractor=LinkExtractor(allow=('/company\?page=\d+'))),
        Rule(link_extractor=LinkExtractor(allow=('/company/foreign\?page=\d+'))),
        # 获取每一个公司的详情
        Rule(link_extractor=LinkExtractor(allow=('/company/\d+')), callback='parse_item')
    ]

    def start_requests(self):
        print('==================')
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=self.cookies, callback=self.make_requests_from_url, dont_filter=True)

    def make_requests_from_url(self, url):
        print('make_request_from_url---------------------------------------')
        return scrapy.FormRequest(url, headers=self.headers, cookies=self.cookies, dont_filter=True)

    def parse_item(self, response):
        print('=====================|||||||||||||||||||||||||')
        print(response.request.headers.getlist('cookie'))
        print("======================" + response.url)
        # soup = BeautifulSoup(response.body, 'lxml')

        # 开头部分： //div[@class="infoheadrow-v2 ugc-block-item"]
        # cpy1 = soup.find('div', class_='infoheadrow-v2')
        cpy1 = response.xpath('//div[@class="on-edit-hide"]')
        if cpy1:
            company_name = cpy1.xpath('//h1[@class="seo-important-title"]//text()').extract_first().strip()
        #
        #     # 口号： //div[@class="info-line"]/p
            slogan = cpy1.xpath('//h2[@class="seo-slogan"]/text()').extract_first()
        #
        #     # 分类：子分类//span[@class="scope c-gray-aset"]/a[1]
            scope = cpy1.xpath('//span[@class="scope c-gray-aset"]/a[1]/text()').extract_first()
        #     scope_a = cpy1.find(class_='scope c-gray-aset').find_all('a')
        #     # 分类：//span[@class="scope c-gray-aset"]/a[1]
            sub_scope = cpy1.xpath('//span[@class="scope c-gray-aset"]/a[2]/text()').extract_first()
        #     scope = scope_a[0].get_text().strip() if len(scope_a) > 0 else 'NULL'
        #     # 子分类：# //span[@class="scope c-gray-aset"]/a[2]
        #     sub_scope = scope_a[1].get_text().strip() if len(scope_a) > 1 else 'NULL'
        #
        #     # 城市+区域：//span[@class="loca c-gray-aset"]/a
        #     city_a = ':'.join(cpy1.xpath('//span[@class="loca c-gray-aset"]/a/text()').extract())
        #     city_a = cpy1.find(class_='loca c-gray-aset').find_all('a')
        #     # 城市：//span[@class="loca c-gray-aset"]/a[1]
            city = cpy1.xpath('//span[@class="loca c-gray-aset"]/a[1]/text()').extract_first()
        #     city = city_a[0].get_text().strip() if len(city_a) > 0 else 'NULL'
        #     # 区域：//span[@class="loca c-gray-aset"]/a[2]
            area = cpy1.xpath('//span[@class="loca c-gray-aset"]/a[2]/text()').extract_first()
        #     area = city_a[1].get_text().strip() if len(city_a) > 1 else 'NULL'
        #
        #     # 主页：//a[@class="weblink"]/@href
        #     home_page = cpy1.find(class_='weblink')['href']
            home_page = cpy1.xpath('//a[@class="weblink"]/@href').extract_first()
        #     # 标签：//div[@class="tagset dbi c-gray-aset"]/a
            tags = set(cpy1.xpath('//div[@class="tagset dbi c-gray-aset"]/a/span/text()').extract())
        #     tags = cpy1.find(class_='tagset dbi c-gray-aset').get_text().strip().strip().replace('\n', ',')
        #
        # #基本信息：//div[@class="block-inc-info on-edit-hide"]
        # cpy2 = soup.find('div', class_='block-inc-info on-edit-hide')
        cpy2 = response.xpath('//div[@class="block-inc-info on-edit-hide"]')
        if cpy2:
            company_intro = ''.join(cpy2.xpath('//div[@class="block-inc-info on-edit-hide"]//div/text()').extract()).split(' hello@itjuzi.com')[-1].split()[0]

        #
        #     # 公司全称：成立时间：公司规模：运行状态：//div[@class="des-more"]
            cpy2_content = cpy2.xpath('//div[@class="des-more"]//h2/text()').extract()
        #     cpy2_content = cpy2.find(class_='des-more').contents
        #
        #     # 公司全称：//div[@class="des-more"]/div[1]
        #     company_full_name = cpy2_content[1].get_text().strip()[len('公司全称：'):] if cpy2_content[1] else 'NULL'
        #     company_full_name = cpy2.xpath('//h2[@class="seo-second-title"]/text()').extract_first().split('：')[-1]
            company_full_name = cpy2_content[0].split('：')[-1]
        #     # 成立时间：//div[@class="des-more"]/div[2]/span[1]
        #     found_time = cpy2_content[3].contents[1].get_text().strip()[len('成立时间：'):] if cpy2_content[1] else 'NULL'
        #     found_time = cpy2.xpath('//h2[@class="seo-second-title"][2]/text()').extract()
            found_time = cpy2_content[1].split('：')[-1]
        #     # 公司规模：//div[@class="des-more"]/div[2]/span[2]
        #     company_size = cpy2_content[3].contents[3].get_text().strip()[len('公司规模：'):] if cpy2_content[1] else 'NULL'
            company_size = cpy2_content[2].strip().split('：')[-1]
        #     #运营状态：//div[@class="des-more"]/div[3]/span
        #     company_status = cpy2_content[5].get_text().strip() if cpy2_content[3] else 'NULL'
            company_status = cpy2.xpath('//div[@class="des-more"]/div[3]/span/text()').extract_first()
        # 主体信息：
        # main = soup.find('div', class_='main')

        # 投资情况：//table[@class="list-round-v2 jzblur need2login"]
        # 投资情况，包含获投时间、融资阶段、融资金额、投资公司
        # tz = response.xpath('/html/body/div[3]/div[5]/div[2]/div[2]/div[2]/div/div[2]/table')
        tz = response.xpath('//table[@class="list-round-v2"]')
        # print(tz)
        # tz = main.find('table', 'list-round-v2')
        tz_list = []
        if tz:
        # 找出投资情况下所有的tr
            all_tr = tz.xpath('.//tr')
            # print(all_tr)
            for tr in all_tr:
                tz_dict = {}
                all_td = tr.xpath('.//td')
                # print(all_td)
                # # 投资时间
                # tz_dict['tz_time'] = all_td[0].span.get_text().strip()
                tz_dict['tz_time'] = all_td[0].xpath('./span/text()').extract_first().strip()

                # # 融资阶段
                # tz_dict['tz_round'] = all_td[1].get_text().strip()
                tz_dict['tz_round'] = all_td[1].xpath('./span/a/text()').extract_first().strip()
                # # 融资金额
                # tz_dict['tz_finades'] = all_td[2].get_text().strip()
                tz_dict['tz_finades'] = all_td[2].xpath('./span/a/text()').extract_first().strip()
                # # 投资公司
                # tz_dict['tz_capital'] = all_td[3].get_text().strip().replace('\n', ',')

                tz_dict['tz_capital'] = all_td[3].xpath('./span//text() | .//a/text()').extract_first().strip().replace('\n', ',')

                tz_list.append(tz_dict)

        tz_list = []
        # 团队信息：成员姓名、成员职称、成员介绍
        # tm = main.find('ul', class_='list-prodcase limited-itemnum')
        tm = response.xpath('//ul[@class="list-prodcase limited-itemnum"]')
        tm_list = []
        if tm:
            # for li in tm.find_all('li'):
            for li in tm.xpath('.//li'):
                tm_dict = {}
                # 成员姓名
        #         tm_dict['tm_m_name'] = li.find('span', class_='c').get_text().strip()
                tm_dict['tm_m_name'] = li.xpath('.//span[@class="c"]/text()').extract_first()
                #成员职称
        #         tm_dict['tm_m_title'] = li.find('span', class_='c-gray').get_text().strip()
                tm_dict['tm_m_title'] = li.xpath('.//span[@class="c-gray"]/text()').extract_first()
                # 成员信息
        #         tm_dict['tm_m_intro'] = li.find('p', class_='mart10 person-des').get_text().strip()
                tm_dict['tm_m_intro'] = li.xpath('.//p[@class="mart10 person-des"]/text()').extract_first().strip()
                # print(tm_dict)
                tm_list.append(tm_dict)

        # # 产品信息：产品名称、产品类型、产品介绍
        # pdt = main.find('ul', class_='list-prod limited-itemnum')
        pdt = response.xpath('//ul[@class="list-prod limited-itemnum"]')
        pdt_list = []
        if pdt:
        #     for li in pdt.find_all('li'):
            for li in pdt.xpath('.//li'):
                pdt_dict = {}
        #         pdt_dict['pdt_name'] = li.find('h4').b.get_text().strip()
                pdt_dict['pdt_name'] = li.xpath('./h4/b/text()').extract_first()
        #         pdt_dict['pdt_type'] = li.find('span', class_='tag yellow').get_text().strip()
                pdt_dict['pdt_type'] = li.xpath('./span[@class="tag yellow"]/text()').extract_first()
        #         pdt_dict['pdt_intro'] = li.find(class_='on-edit-hide').p.get_text().strip()
                pdt_dict['pdt_intro'] = li.xpath('./div[@class="on-edit-hide"]/p/text()').extract_first()
                pdt_list.append(pdt_dict)
                # print(pdt_dict)

        item = CompanyItem()
        #取出后面的数字编号
        item['info_id'] = response.url.split('/')[-1:][0]
        item['company_name'] = company_name
        item['slogan'] = slogan
        item['scope'] = scope
        item['sub_scope'] = sub_scope
        item['city'] = city
        item['area'] = area
        item['home_page'] = home_page
        item['tags'] = tags
        item['company_intro'] = company_intro
        item['company_full_name'] = company_full_name
        item['found_time'] = found_time
        item['company_size'] = company_size
        item['company_status'] = company_status
        item['tz_info'] = tz_list
        item['tm_info'] = tm_list
        item['pdt_info'] = pdt_list

        yield item

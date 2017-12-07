import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
import time

from scrapy_redis.spiders import RedisCrawlSpider


class Bookspider(RedisCrawlSpider):
    name = 'book'
    redis_key = 'bookspider:start_urls'

    # 编写连接提取器规则
    book_link = LinkExtractor(allow=r'.quanwenyuedu.io$', deny='big5')
    text_link = LinkExtractor(allow=r'/(\d+).html$', deny='big5')

    rules = (
        # 生成 Rule 对象，注意： callback 的函数为 字符串
        Rule(book_link, callback='get_book', follow=True),
        Rule(text_link, callback='get_ajax_info', follow=True),
    )

    def get_book(self, response):
        print('get_book ===== ', response.url)
        book_name = response.url.split('.')[0].split('/')[-1]
        book_info = '\n'.join(response.xpath("//div[@class='top']/p//text()").extract())
        # print(book_name)
        # print(book_info)

        with open('/home/python/Desktop/spider/files/' + book_name + '.txt', 'a') as f:
            f.write(book_info + '\n\n\n')
        time.sleep(1)

    def get_ajax_info(self, response):
        form_data = {
            'c': 'book',
            'a': 'ajax',
        }

        zz = re.compile(r'setTimeout.*')
        js = zz.search(response.text)
        js_list = js.group().split("','")

        form_data['id'] = js_list[3]
        form_data['sky'] = js_list[5]
        form_data['t'] = js_list[7].split("'")[0]
        form_data['rndval'] = str(int(time.time() * 1000))

        print(form_data)

        url_str = ''.join(response.url.split('io/')[:-1]) + 'io/index.php?c=book&a=ajax'
        print(url_str)
        print("===========================")

        yield scrapy.FormRequest(
            url=url_str,
            formdata=form_data,
            callback=self.get_text
        )

    def get_text(self, response):
        print('get_text =====', response.url)
        book_name = response.url.split('.')[0].split('/')[-1]

        text_info = '\n'.join(response.xpath("//text()").extract())
        # print('text_info =====', text_info)
        time.sleep(2)

        with open('/home/python/Desktop/spider/files/' + book_name + 'txt', 'a') as f:
            f.write(text_info + '\n\n=====================================\n')
        time.sleep(2)
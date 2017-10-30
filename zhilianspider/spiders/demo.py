# -*- coding: utf-8 -*-

import os
import time
import scrapy
from scrapy.selector import Selector
from zhilianspider..items import ZhilianspiderItem

# 构造url；
def create_url():
    jl = "深圳"
    kw = "python"
    first_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl="
    for p in xrange(1,21):
        my_url = first_url + jl + "&kw=" + kw + "&p=" + str(p)
        yield my_url


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['sou.zhaopin.com']
    # start_urls = list(create_url())
    start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=python&p=1']

    # 找到网页中公司的链接，并返回公司主页的url继续爬取；
    def parse(self, response):
        # 把爬取到的网页实例存储成html文件，方便检查是否匹配正确；
        # fname = 'parse.html'
        # with open(fname, 'wb') as f:
        #     f.write(response.body)

        # 提取网页中的公司主页的url;
        main_html = response.xpath('.//*[@id="newlist_list_content_table"]/table').extract()
        try:
            for job in main_html[1:]:
                job_href = Selector(text=job).xpath("//td[@class='zwmc']//a/@href").extract()[0]
                print job_href
                print '-------------------------------'
                yield scrapy.Request(job_href, callback=self.parse_stock, dont_filter=True)
        except:
            pass


    def parse_stock(self, response):
        print response.status
        item = ZhilianspiderItem()
        item['title'] = response.xpath('//title').extract()
        yield item
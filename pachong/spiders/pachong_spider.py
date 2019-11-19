import scrapy



class itemSpider(scrapy.Spider):
    # scrapy.Spider 是一个简单的爬虫类型。
    # 它只是提供了一个默认start_requests()实现。
    # 它从start_urlsspider属性发送请求，并parse 为每个结果响应调用spider的方法。
    page = 1
    name = "pachong"
    # 定义此爬虫名称的字符串。
    # 它必须是唯一的。
    base_urls = 'http://lab.scrapyd.cn/page/'

    # start_urls = list(base_urls + str(page))
    start_urls = ['http://lab.scrapyd.cn/page/1']

    print(start_urls)
    # 爬虫抓取自己需要的网址列表--可以有多个
    def parse(self, response):
        # 定义一个parse规则，用来爬取自己需要的网站信息。
        pachong = response.css('div.quote')
        # 用变量pachong来保存获取网站的部分内容。
        for v in pachong:
            text = v.css('.text::text').extract_first()
            author = v.css('.author::text').extract_first()

            # 循环提取所有的标题、作者和标签内容。
            fileName = u'%s-语录.txt' % author
            with open(fileName, 'a+')as f:
                f.write(text)
                f.close()
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            # 查看存在不存在下一页的链接，如果存在下一页，把下一页的内容提交给parse然后继续爬取,直到不存在为止

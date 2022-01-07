# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from collections import OrderedDict
import random, time, csv, json
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

class discord_sneakerSpider(Spider):
    name = "discord_sneaker"

    start_urls = []
    url_list = []
    # --------------- Get list of proxy-----------------------#
    proxy_text = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt').text
    list_proxy_temp = proxy_text.split('\n')
    use_selenium = True
    # file = open("proxies.txt", "r")
    # # lines =
    # list_proxy = []
    # for key in file.readlines():
    #     list_proxy.append(key.strip())

    list_proxy = []
    # for line in list_proxy_temp:
    #     if line.strip() !='' and (line.strip()[-1] == '+' or line.strip()[-1] == '-'):
    #         ip = line.strip().split(':')[0].replace(' ', '')
    #         port = line.split(':')[-1].split(' ')[0]
    #         list_proxy.append('http://'+ip+':'+port)
    #
    # # datas = []
    links_file = open('links.csv')

    csv_items = csv.DictReader(links_file)

    for i, row in enumerate(csv_items):
        url_list.append(row['url'])


    def start_requests(self):
        # webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/534454925334151185/M00ryaTldlPr92HiCssKxIQR91G4YekX3PWGwwvDo2eXaKQjUNuMVTUbR4ZcBMF2C6jX')
        #
        # # create embed object for webhook
        # embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)
        #
        # # add embed object to webhook
        # webhook.add_embed(embed)
        #
        # webhook.execute()


        for url in self.url_list:
            # proxy = random.choice(self.list_proxy)
            # yield Request(url, callback=self.parse, meta={'proxy': proxy}, errback=self.errCall)
            yield Request(url, callback=self.parse)

        ##test
        # yield Request(self.start_urls[0], callback=self.parse)
    def parse(self, response):

        pass
        # title = response.xpath('//span[@class="productname"]/text()').extract_first()
        # price = response.xpath('//meta[@itemprop="price"]/@content').extract_first()
        # title_to_send = '{} is priced at €{}.'.format(title, price)
        #
        # sku = response.xpath('//meta[@itemprop="sku"]/@content').extract_first()
        # gtin14 = response.xpath('//meta[@itemprop="gtin14"]/@content').extract_first()
        #
        # selectVariants_tags = response.xpath('//div[@class="selectVariants clear"]//select[@class="customSelectBox"]/option')
        # availability_list = {}
        # for i, selectVariants_tag in enumerate(selectVariants_tags):
        #     if i == 0:
        #         continue
        #     temp = selectVariants_tag.xpath('./text()').re(r'[\d.,]+')
        #     if selectVariants_tag.xpath('./@class').extract_first() == "":
        #         if temp:
        #             val = selectVariants_tag.xpath('./@value').extract_first()
        #
        #             data = {'chosen_attribute_value': val,
        #                     'returnHtmlSnippets[partials][0][module]': 'product',
        #                     'returnHtmlSnippets[partials][0][path]': '_productDetail',
        #                     'returnHtmlSnippets[partials][0][partialName]': 'buybox'}
        #             payload = {
        #                         "cache-control": "no-cache",
        #                 # ":authority": "www.bstn.com",
        #                 # ":method": "POST",
        #                 # ":path": "/p/nike-air-monarch-iv-martine-rose-at3147-100-115062",
        #                 # ":scheme": "https",
        #                 "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ko;q=0.6",
        #                         # "Connection": "keep-alive",
        #                         "content-length": '218',
        #                         "pragma": "no-cache",
        #                         "content-type": "application/json",
        #                         "accept": "*/*",
        #                         "accept-encoding": "gzip,deflate,br",
        #                         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        #                         "x-requested-with": "XMLHttpRequest",
        #                         "Cookie": "__cfduid=dbe87014f86275fd413ab6942f2ac59cb1547490417; _ga=GA1.2.1578699562.1547489942; _gid=GA1.2.879335533.1547489942; trbo_usr=ff8f36dca86690355d8921799a7502e5; 3mo_ebusiness_shop_v3=a8ipb1rmbd7qqpfcq89ga5cek2; cto_lwid=17602c49-3516-4ce5-97df-dd64db0b7397; bstnhome=men; x-tracking_referer=https://www.freelancer.com/projects/php/page-url-monitor-with-Cloudflare/?w=f; cf_clearance=798f993c76ad6c18cc03b6d96b4048581b2ac279-1547542599-14400-250; trbo_usr=ff8f36dca86690355d8921799a7502e5; trbo_us_ff8f36dca86690355d8921799a7502e5=%7B%22saleCount%22%3A0%2C%22sessionCount%22%3A7%2C%22brandSessionCount%22%3A3%2C%22pageViewCountTotal%22%3A17%2C%22sessionDurationTotal%22%3A942%2C%22externalUserId%22%3A%22%22%2C%22userCreateTime%22%3A1547489944%7D; _fbp=fb.1.1547553413323.127650898; trbo_us_ff8f36dca86690355d8921799a7502e5=%7B%22saleCount%22%3A0%2C%22sessionCount%22%3A8%2C%22brandSessionCount%22%3A3%2C%22pageViewCountTotal%22%3A20%2C%22sessionDurationTotal%22%3A1752%2C%22externalUserId%22%3A%22%22%2C%22userCreateTime%22%3A1547489944%7D"
        #                     }
        #             headers = {}
        #             r = requests.post(response.url, json=data, headers=payload)
        #
        #
        #             availability_list[temp[0]] = selectVariants_tag.xpath('./@value').extract()
        #
        # detail_url = response.url
        # image_url = response.urljoin(response.xpath('//ul[@class="thumbnails"]/li/div/img/@src').extract_first())
        #
        # webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/534454925334151185/M00ryaTldlPr92HiCssKxIQR91G4YekX3PWGwwvDo2eXaKQjUNuMVTUbR4ZcBMF2C6jX')
        #
        # # create embed object for webhook
        # embed = DiscordEmbed(title=title_to_send, description='', color=242424)
        #
        # # set author
        # embed.set_author(name=title, url=detail_url, icon_url='')
        #
        # # set image
        # # embed.set_image(url=image_url)
        #
        # # set thumbnail
        # embed.set_thumbnail(url=image_url)
        #
        # # set footer
        # embed.set_footer(text='easycopeu', icon_url='https://images-ext-1.discordapp.net/external/6wgec4zOzXdH3Ro4BuF81VzZpOvyYOZS6KGLh3ZEUA0/https/i.imgur.com/jTYyIYX.png')
        #
        # # set timestamp (default is now)
        # # embed.set_timestamp()
        #
        # # add fields to embed
        # embed.add_embed_field(name='Availability', value='\n'.join(availability_list.keys()), inline=True)
        # embed.add_embed_field(name='URL', value=detail_url)
        #
        # # add embed object to webhook
        # webhook.add_embed(embed)
        #
        # webhook.execute()


    def errCall(self, response):
        ban_proxy = response.request.meta['proxy']
        if '154.16.' in ban_proxy:
            ban_proxy = ban_proxy.replace('http://', 'http://eolivr4:bntlyy3@')
        if ban_proxy in self.list_proxy:
            self.list_proxy.remove(ban_proxy)
        if len(self.list_proxy) < 1:
            proxy_text = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt').text
            list_proxy_temp = proxy_text.split('\n')
            self.list_proxy = []
            for line in list_proxy_temp:
                if line.strip() !='' and (line.strip()[-1] == '+' or line.strip()[-1] == '-'):
                    ip = line.strip().split(':')[0].replace(' ', '')
                    port = line.split(':')[-1].split(' ')[0]
                    self.list_proxy.append('http://'+ip+':'+port)

        proxy = random.choice(self.list_proxy)
        # response.request.meta['proxy'] = proxy
        print ('err proxy: ' + proxy)
        if not 'errpg' in response.request.url :
            yield Request(response.request.url,
                          callback=self.parse,
                          meta={'proxy': proxy},
                          dont_filter=True,
                          errback=self.errCall)



    def removeSeveralSpace(self, strContent):
        strContent = strContent.replace('\n', '')
        array = []
        for s in strContent.split(' '):
            if s:
                array.append(s)

        return ' '.join(array)

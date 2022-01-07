from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from scrapy.http import TextResponse
from scrapy.exceptions import CloseSpider
from scrapy import signals
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import date
import json
import time

class SeleniumMiddleware(object):

    def __init__(self, s):
        # self.exec_path = s.get('PHANTOMJS_PATH', './chromedriver.exe')
        self.exec_path = 'E:/chromedriver.exe'

###########################################################

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)

        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(obj.spider_closed,
                                signal=signals.spider_closed)
        return obj

###########################################################

    def spider_opened(self, spider):
        try:
            self.d = init_driver(self.exec_path)
        except TimeoutException:
            CloseSpider('PhantomJS Timeout Error!!!')

###########################################################

    def spider_closed(self, spider):
        self.d.quit()
###########################################################
    
    def process_request(self, request, spider):
        if spider.use_selenium:
            print("############################ Received url request from scrapy #####")

            try:
                self.d.get(request.url)
                

            except TimeoutException as e:            
                raise CloseSpider('TIMEOUT ERROR')
            
            # lastHeight = self.d.execute_script("return document.body.scrollHeight")
            # print "*** Last Height = ", lastHeight
            # while True:
            #     self.d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #     time.sleep(5)
            #     newHeight = self.d.execute_script("return document.body.scrollHeight")
            #     if newHeight == lastHeight:
            #         break
            #     lastHeight = newHeight

            # time.sleep(5)

            selector = None
            city = None
            button = None

            # if not "categories" in spider.name:
            #
            #
            #
            #     resultData = ""
            #     next_count = 0
            #     while True:
            #
            #         resp = TextResponse(url=self.d.current_url,
            #                     body=self.d.page_source,
            #                     encoding='utf-8')
            #         resp.request = request.copy()
            #
            #         products = resp.xpath('//*[@class="product_listing_container"]/ul/li')
            #
            #         print(len(products))
            #         print("###########")
            #         # print response.url
            #
            #         if not products: return
            #
            #         for i in products:
            #             item = {}
            #
            #             item['Vendedor'] = 447
            #             item['ID'] = i.xpath('.//*[@class="product_image"]/@id').extract_first().split('_')[-1]
            #             item['Title'] = i.xpath('.//*[@class="product_name"]/a/text()').extract_first().strip()
            #             #item['Description'] = ''
            #
            #             price = i.xpath('.//*[contains(@id, "offerPrice_")]/text()').re(r'[\d.,]+')
            #             item['Price'] = ''
            #
            #             if price:
            #                 price[0] = price[0].replace('.', '').replace(',', '')
            #                 # price[0] = price[0].replace(',', '.')
            #                 # if price[0].count('.') == 2:
            #                 #     price[0] = price[0].replace('.', '', 1)
            #                 item['Price'] = price[0]
            #                 item['Currency'] = 'CLP'
            #             else:
            #                 continue
            #
            #             item['Category URL'] = request.meta['CatURL']
            #             item['Details URL'] = resp.urljoin(i.xpath('.//*[@class="product_name"]/a/@href').extract_first().strip())
            #             item['Date'] = str(date.today())
            #
            #             resultData = resultData + json.dumps(item) + '+++++'
            #
            #         # count = len(response.xpath('//ul[@class="pagination"]/li'))
            #         next00 = resp.xpath('//*[@class="right_arrow "]')
            #
            #
            #         if next00:
            #             selector = self.d.find_element_by_xpath('//*[@class="right_arrow "]')
            #             selector.click()
            #             time.sleep(1)
            #             continue
            #         break
            #     resp0 = TextResponse(url=self.d.current_url,
            #                         body=resultData, #self.d.page_source,
            #                         encoding='utf-8')
            #     resp0.request = request.copy()
            #
            #     return resp0

            response = TextResponse(url=self.d.current_url,
                                body=self.d.page_source,
                                encoding='utf-8')

            while True:
                response = TextResponse(url=self.d.current_url,
                                body=self.d.page_source,
                                encoding='utf-8')
                if response.xpath('//div[@class="message"]/div/h1/text()').extract_first() == 'Relax ':
                    time.sleep(3)
                    continue
                break

            response.request = request.copy()
            self.d.find_element_by_xpath('//a[@class="close-reveal-modal close-geo-switch"]').click()
            time.sleep(0.5)
            self.d.find_element_by_xpath('//div[@class="selectVariants clear"]').click()
            self.d.find_element_by_xpath('//div[@class="selectVariants clear"]').click()

            title = response.xpath('//span[@class="productname"]/text()').extract_first()
            price = response.xpath('//meta[@itemprop="price"]/@content').extract_first()
            title_to_send = '{} is priced at €{}.'.format(title, price)

            sku = response.xpath('//meta[@itemprop="sku"]/@content').extract_first()
            gtin14 = response.xpath('//meta[@itemprop="gtin14"]/@content').extract_first()

            selectVariants_tags = response.xpath('//div[@class="selectVariants clear"]//select[@class="customSelectBox"]/option')
            availability_list = {}
            for i, selectVariants_tag in enumerate(selectVariants_tags):
                if i == 0:
                    continue
                temp = selectVariants_tag.xpath('./text()').re(r'[\d.,]+')
                if selectVariants_tag.xpath('./@class').extract_first() == "":
                    if temp:
                        val = selectVariants_tag.xpath('./@value').extract_first()
                        availability_list[temp[0]] = selectVariants_tag.xpath('./@value').extract()

            detail_url = response.url
            image_url = response.urljoin(response.xpath('//ul[@class="thumbnails"]/li/div/img/@src').extract_first())

            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/534454925334151185/M00ryaTldlPr92HiCssKxIQR91G4YekX3PWGwwvDo2eXaKQjUNuMVTUbR4ZcBMF2C6jX')

            # create embed object for webhook
            embed = DiscordEmbed(title=title_to_send, description='', color=242424)

            # set author
            embed.set_author(name=title, url=detail_url, icon_url='')

            # set image
            # embed.set_image(url=image_url)

            # set thumbnail
            embed.set_thumbnail(url=image_url)

            # set footer
            embed.set_footer(text='easycopeu', icon_url='https://images-ext-1.discordapp.net/external/6wgec4zOzXdH3Ro4BuF81VzZpOvyYOZS6KGLh3ZEUA0/https/i.imgur.com/jTYyIYX.png')

            # set timestamp (default is now)
            # embed.set_timestamp()

            # add fields to embed
            embed.add_embed_field(name='Availability', value='\n'.join(availability_list.keys()), inline=True)
            embed.add_embed_field(name='URL', value=detail_url)

            # add embed object to webhook
            webhook.add_embed(embed)

            webhook.execute()



            
            return response

###########################################################
###########################################################

def init_driver(path):

    chrome_options = Options()
    # chrome_options.add_argument("window-size=1,1")
    # chrome_options.add_argument("window-position=-3000,0")
    d = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    d.set_page_load_timeout(30)

    return d
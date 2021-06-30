import logging
import re
import pathlib
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from user_agents import headers

path = pathlib.Path('exports').mkdir(parents=True, exist_ok=True)

export_json = pathlib.Path(
    'exports', 'kindle_bestsellers_ebooks-%(time)s.json')
export_csv = pathlib.Path('exports', 'kindle_bestsellers_ebooks-%(time)s.csv')


def clean_data(item_names, item_values):
    name_list = []
    value_list = []
    for item_name, item_value in zip(item_names, item_values):
        item_name = item_name.replace(":", "")
        item_name = item_name.strip()
        item_value = item_value.strip()
        name_list.append(item_name)
        value_list.append(item_value)
    return name_list, value_list


class AmazonKindleSpider(scrapy.Spider):
    name = 'amazon_kindle'

    cate_input = input("Enter your category: ")
    subcate_input = input("Enter your subcategory: ")

    COUNT_MAX = 1000
    FEEDS = {
        export_json: {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': ['Title', 'Author'],
            'indent': 4,
            # 'item_export_kwargs': {
            #     'export_empty_fields': True,
            # },
        },
        export_csv: {
            'format': 'csv',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': ['Title', 'Author'],
        },
    }
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'DOWNLOAD_DELAY': 1.5,
        'COOKIES_ENABLED': False,
        # 'FEED_URI': 'kindle_bestsellers_ebooks.json',
        # 'FEED_FORMAT': 'json',
        # 'FEED_URI': 'kindle_bestsellers_ebooks.csv',
        # 'FEED_FORMAT': 'csv'
        'FEEDS': FEEDS,
        'CLOSESPIDER_PAGECOUNT': COUNT_MAX
    }
    headers = headers()
    url = "https://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/154606011/ref=zg_bs_nav_kstore_1_kstore"

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.category_parse)

    def category_parse(self, response):
        category_names = response.xpath(
            '//*[@id="zg_browseRoot"]/ul/ul/li/a/text()').getall()
        category_urls = response.xpath(
            '//*[@id="zg_browseRoot"]/ul/ul/li/a/@href').getall()
        for category_url, category_name in zip(category_urls, category_names):
            # yield scrapy.Request(url=category_url, headers=self.headers, callback=self.subcategory_parse)
            if self.cate_input.lower() == category_name.lower():
                yield scrapy.Request(url=category_url, headers=self.headers, callback=self.subcategory_parse)
            if self.cate_input.lower() == "all":
                yield scrapy.Request(url=category_url, headers=self.headers, callback=self.subcategory_parse)

    def subcategory_parse(self, response):
        subcategory_names = response.xpath(
            '//*[@id="zg_browseRoot"]/ul/ul/ul/li/a/text()').getall()
        subcategory_urls = response.xpath(
            '//*[@id="zg_browseRoot"]/ul/ul/ul/li/a/@href').getall()
        for subcategory_url, subcategory_name in zip(subcategory_urls, subcategory_names):
            # yield scrapy.Request(url=subcategory_url, headers=self.headers, callback=self.books_parse)
            if self.subcate_input.lower() == subcategory_name.lower():
                # previously used yield
                return scrapy.Request(url=subcategory_url, headers=self.headers, callback=self.books_parse)
            if self.subcate_input.lower() == "all":
                # previously used yield
                return scrapy.Request(url=subcategory_url, headers=self.headers, callback=self.books_parse)

    def books_parse(self, response):
        books_urls = response.xpath(
            '//*[@id="zg-ordered-list"]/li/span/div/span/a[1]/@href').getall()
        for book_url in books_urls:
            absolute_url = f"https://www.amazon.com{book_url}"
            yield scrapy.Request(url=absolute_url, headers=self.headers,
                                 callback=self.books_details_parse)

        next_page_url = response.xpath(
            '//*[@id="zg-center-div"]/div[2]/div/ul/li[4]/a/@href').get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, headers=self.headers, callback=self.books_parse)

    def books_details_parse(self, response):
        raw_title = response.xpath(
            '//*[@id="productTitle"]/text()').get()
        title = re.sub(r'\n', '', str(raw_title))

        author_single = response.xpath(
            '//*[@id="bylineInfo"]/span[1]/a/text()').get()
        author_multiple = response.xpath(
            '//*[@id="bylineInfo"]/span/a/text()').getall()
        authors = []
        raw_author = ""
        if len(author_multiple) < 1:
            raw_author = author_single
            
        if len(author_multiple) > 1:
            for author_multi in author_multiple:
                authors.append(author_multi)
            raw_author = ", ".join(authors)

        author = re.sub(r'\n', '', str(raw_author))

        item_names = response.xpath(
            '//*[@id="detailBullets_feature_div"]/ul/li/span/span[1]/text()').getall()
        item_values = response.xpath(
            '//*[@id="detailBullets_feature_div"]/ul/li/span/span[2]/text()').getall()
        item_names, item_values = clean_data(item_names, item_values)
        item_dict = {}
        book_features = ['ASIN', 'Publisher', 'Publication date', 'Language', 'File size',
                         'Text-to-Speech', 'Enhanced typesetting', 'X-Ray', 'Word Wise', 'Print length', 'Lending']
        for feature in book_features:
            if feature not in item_names:
                item_names.append(feature)
                item_values.append("")

        for item_name, item_value in zip(item_names, item_values):
            item_dict[item_name] = item_value

        best_sellers_ranks_no = response.xpath(
            '//*[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/ul/li/span/text()').getall()
        best_sellers_rank_titles = response.xpath(
            '//*[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/ul/li/span/a/text()').getall()
        best_sellers_ranks_urls = response.xpath(
            '//*[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/ul/li/span/a/@href').getall()

        best_sellers_rank_lst = []

        for best_sellers_rank_no, best_sellers_ranks_url, best_sellers_rank_title in zip(best_sellers_ranks_no, best_sellers_ranks_urls, best_sellers_rank_titles):
            best_sellers_absolute_url = f"https://www.amazon.com{best_sellers_ranks_url}"
            best_sellers_rank = f"{best_sellers_rank_no}{best_sellers_rank_title}({best_sellers_absolute_url})"
            best_sellers_rank_lst.append(best_sellers_rank.strip())

        review = response.xpath(
            '//*[@id="acrPopover"]/span[1]/a/i[1]/span[1]/text()').get()
        rating = response.xpath(
            '//*[@id="acrCustomerReviewText"][1]/text()').get()
        customer_reviews = f"{review}, {rating}"

        items_details = {
            'Title': title,
            'Author': author,
            'ASIN': item_dict['ASIN'],
            'Publisher': item_dict['Publisher'],
            'Publication date': item_dict['Publication date'],
            'Language': item_dict['Language'],
            'File size': item_dict['File size'],
            'Text-to-Speech': item_dict['Text-to-Speech'],
            'Enhanced typesetting': item_dict['Enhanced typesetting'],
            'X-Ray': item_dict['X-Ray'],
            'Word Wise': item_dict['Word Wise'],
            'Print length': item_dict['Print length'],
            'Lending': item_dict['Lending'],
            'Best Sellers Rank': ", ".join(best_sellers_rank_lst),
            'Customer Reviews': customer_reviews,
        }

        # audible = response.xpath(
        #     '//*[@id="a-autoid-6-announce"]/span[1]/span/span[2]/span/text()').get()
        # if audible == 'Audiobook':

        audible_url = response.xpath(
            '//*[@id="a-autoid-6-announce"]/@href').get()
        if audible_url:
            return scrapy.Request(
                url=audible_url, headers=self.headers, callback=self.audible_details_parse, meta={
                    'items_details': items_details
                })
        else:
            return items_details

    def audible_details_parse(self, response):
        narrator = response.xpath(
            '//*[@id="detailsnarrator"]/td/a/text()').get()
        listening_length = response.xpath(
            '//*[@id="detailsListeningLength"]/td/span/text()').get()
        whispersync_for_voice = response.xpath(
            '//*[@id="aud_product_details"]/text()').get()
        program_type = response.xpath(
            '//*[@id="detailsProgramType"]/td/span/text()').get()
        version = response.xpath(
            '//*[@id="detailsVersion"]/td/span/text()').get()
        audible_release_date = response.xpath(
            '//*[@id="detailsReleaseDate"]/td/span/text()').get()

        audible_details = {
            'Title': response.meta['items_details']['Title'],
            'Author': response.meta['items_details']['Author'],
            'ASIN': response.meta['items_details']['ASIN'],
            'Publisher': response.meta['items_details']['Publisher'],
            'Publication date': response.meta['items_details']['Publication date'],
            'Language': response.meta['items_details']['Language'],
            'File size': response.meta['items_details']['File size'],
            'Text-to-Speech': response.meta['items_details']['Text-to-Speech'],
            'Enhanced typesetting': response.meta['items_details']['Enhanced typesetting'],
            'X-Ray': response.meta['items_details']['X-Ray'],
            'Word Wise': response.meta['items_details']['Word Wise'],
            'Print length': response.meta['items_details']['Print length'],
            'Lending': response.meta['items_details']['Lending'],
            'Best Sellers Rank': response.meta['items_details']['Best Sellers Rank'],
            'Customer Reviews': response.meta['items_details']['Customer Reviews'],
            'Narrator': narrator,
            'Listening Length': listening_length,
            'Whispersync for Voice': whispersync_for_voice,
            'Program Type': program_type,
            'Version': version,
            'Audible Release Date': audible_release_date,
        }

        return audible_details


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(AmazonKindleSpider)
    process.start()
    # CloseSpider() #close spider manually

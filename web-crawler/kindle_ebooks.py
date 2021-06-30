import re
import time
import datetime
from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
from user_agents import headers

 
def selected_fields():
    choice = input(
        "\nWould you like to choose the fields? If yes, please press y else any other key: ")[0]
    field_names = ['Title', 'Author', 'ASIN', 'Publisher', 'Publication date', 'Language', 'File size', 'Text-to-Speech', 'Enhanced typesetting', 'X-Ray', 'Word Wise',
                   'Print length', 'Lending', 'Best Sellers Rank', 'Customer Reviews', 'Narrator', 'Listening Length', 'Whispersync for Voice', 'Program Type', 'Version', 'Audible Release Date']
    fields = []
    if choice.lower() == 'y':
        print("Please press s for select a field otherwise any other key.")
        for field in field_names:
            print(field, end=': ')
            select = input()[0]
            if select.lower() == "s":
                fields.append(field)
        return fields
    else:
        return field_names

class KindleEbooksSpider(scrapy.Spider):
    name = 'kindle_ebooks'

    _start_year = 0
    _start_month = 0
    _start_date = 0
    _start_hour = 0
    _start_minute = 0
    _start_second = 0

    COUNT_MAX = 10000

    path = Path('exports').mkdir(parents=True, exist_ok=True)
    export_json = Path(
        'exports', 'kindle_ebooks-%(time)s.json')
    export_csv = Path('exports', 'kindle_ebooks-%(time)s.csv')

    def clean_data(self, item_names, item_values):
        name_list = []
        value_list = []
        for item_name, item_value in zip(item_names, item_values):
            item_name = item_name.replace(":", "")
            item_name = item_name.strip()
            item_value = item_value.strip()
            name_list.append(item_name)
            value_list.append(item_value)
        return name_list, value_list

    def selected_categorical(self, field_names, field_urls):
        choice = input(
            '\nWould you like to choose the categories? If yes, please press y else any other key: ')[0]
        names = []
        urls = []
        if choice.lower() == 'y':
            print("Please press s for select a category otherwise any other key.")
            for field_name, field_url in zip(field_names, field_urls):
                print(field_name, end=': ')
                select = input()[0]
                if select.lower() == "s":
                    names.append(field_name)
                    urls.append(field_url)
            return names, urls
        else:
            return field_names, field_urls

    def start_scheduler(self):
        print("::::Starting Time::::")
        self._start_year = int(input("Year: "))
        self._start_month = int(input("Month: "))
        self._start_date = int(input("Date: "))
        self._start_hour = int(input("Hour: "))
        self._start_minute = int(input("Minute: "))
        self._start_second = 0
        then = datetime.datetime(self._start_year, self._start_month, self._start_date,
                                 self._start_hour, self._start_minute, self._start_second)
        now = datetime.datetime.now()
        duration = (then-now)
        duration_in_s = duration.total_seconds()
        print(
            f'\nYou\'ve perfectly scheduled your job. Wait until {then} for start crawling...\n')
        time.sleep(abs(duration_in_s))

    _fields = selected_fields()

    FEEDS = {
        export_json: {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': _fields,
            'indent': 4,
        },
        export_csv: {
            'format': 'csv',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': _fields,
        },
    }

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'DOWNLOAD_DELAY': 1.5,
        'COOKIES_ENABLED': False,
        'FEEDS': FEEDS,
        'CLOSESPIDER_PAGECOUNT': COUNT_MAX,
        'LOG_LEVEL': 'INFO',
    }

    headers = headers()
    url = "https://www.amazon.com/Kindle-eBooks-Audible-Narration-Store/s?i=digital-text&bbn=133141011&rh=n%3A133140011%2Cn%3A154606011%2Cp_n_feature_three_browse-bin%3A6577679011&dc&qid=1612445710&rnid=133141011&ref=sr_nr_n_1"

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.category_parse)

    def category_parse(self, response):
        category_names = response.xpath(
            '//*[@id="departments"]/ul/li/span/a/span/text()').getall()
        category_names = category_names[1:]
        category_urls = response.xpath(
            '//*[@id="departments"]/ul/li/span/a/@href').getall()
        category_urls = category_urls[1:]
        # select category to crawl data
        category_names, category_urls = self.selected_categorical(
            category_names, category_urls)

        choice = input(
            "\nWould you like to schedule your job? If yes, please press y else any other key: ")[0]
        # start scheduler to crawl data
        if choice == "y":
            self.start_scheduler()

        print('\nCralwer is running...\n')

        for category_url, category_name in zip(category_urls, category_names):
            absolute_url = f"https://www.amazon.com{category_url}"
            yield scrapy.Request(url=absolute_url, headers=self.headers, callback=self.subcategory_parse)

    def subcategory_parse(self, response):

        subcategory_names = response.xpath(
            '//*[@id="departments"]/ul/li/span/a/span/text()').getall()
        subcategory_names = subcategory_names[2:]
        subcategory_urls = response.xpath(
            '//*[@id="departments"]/ul/li/span/a/@href').getall()
        subcategory_urls = subcategory_urls[2:]
        # select subcategory to crawl data
        for subcategory_url in subcategory_urls:
            absolute_url = f"https://www.amazon.com{subcategory_url}"
            yield scrapy.Request(url=absolute_url, headers=self.headers, callback=self.books_parse)

    def books_parse(self, response):

        books_urls = response.xpath(
            '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a/@href').getall()
        for book_url in books_urls:
            absolute_url = f"https://www.amazon.com{book_url}"
            yield scrapy.Request(url=absolute_url, headers=self.headers,
                                 callback=self.books_details_parse)

        next_page_url = response.xpath(
            '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[17]/span/div/div/ul/li[7]/a/@href').get()
        if next_page_url:
            next_page_absolute_url = f"https://www.amazon.com{next_page_url}"
            yield scrapy.Request(url=next_page_absolute_url, headers=self.headers, callback=self.books_parse)

    def books_details_parse(self, response):

        raw_title = response.xpath(
            '//*[@id="productTitle"]/text()').get()
        title = re.sub(r'\n', '', str(raw_title))

        author_single = response.xpath(
            '//*[@id="bylineInfo"]/span[1]/span[1]/a[1]/text()').get()
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
        item_names, item_values = self.clean_data(item_names, item_values)
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
            '//*[@id="acrPopover"]/span[1]/a/i[1]/span[1]/text()').extract_first()
        rating = response.xpath(
            '//*[@id="acrCustomerReviewText"][1]/text()').extract_first()
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

        audible_url = response.xpath(
            '//*[@id="tmmSwatches"]/ul/li[2]/span/span[1]/span/a/@href').get()
        if audible_url:
            absolute_url = f"https://www.amazon.com{audible_url}"
            return scrapy.Request(
                url=absolute_url, headers=self.headers, callback=self.audible_details_parse, meta={
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
    process.crawl(KindleEbooksSpider)
    process.start()

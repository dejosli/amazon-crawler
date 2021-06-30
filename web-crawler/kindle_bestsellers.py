import re
from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
from user_agents import headers

path = Path('exports').mkdir(parents=True, exist_ok=True)
export_json = Path(
    'exports', 'kindle_bestsellers_ebooks-%(time)s.json')
export_csv = Path('exports', 'kindle_bestsellers_ebooks-%(time)s.csv')


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


class BestSellersSpider(scrapy.Spider):
    name = 'kindle_bestsellers'

    COUNT_MAX = 1000
    FEEDS = {
        export_json: {
            'format': 'json',
            'encoding': 'utf-8',
            'store_empty': False,
            'indent': 4,

        },
        export_csv: {
            'format': 'csv',
            'encoding': 'utf-8',
            'store_empty': False,
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
    url = "https://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/154606011/ref=zg_bs_nav_kstore_1_kstore"

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.category_parse)

    def category_parse(self, response):
        category_names = response.xpath(
            '//*[@id="zg_browseRoot"]/ul/ul/ul/li/a/text()').getall()
        category_urls = response.xpath(
            '//*[@id="zg_browseRoot"]/ul/ul/ul/li/a/@href').getall()
        for category_url, category_name in zip(category_urls, category_names):
            yield scrapy.Request(url=category_url, headers=self.headers, callback=self.subcategory_parse)

    def subcategory_parse(self, response):
        subcategory_names = response.xpath(
            '//*[@id="zg_browseRoot"]/ul/ul/ul/ul/li/a/text()').getall()
        subcategory_urls = response.xpath(
            '//*[@id="zg_browseRoot"]/ul/ul/ul/ul/li/a/@href').getall()
        for subcategory_url, subcategory_name in zip(subcategory_urls, subcategory_names):
            yield scrapy.Request(url=subcategory_url, headers=self.headers, callback=self.books_parse)

    def books_parse(self, response):
        books_urls = {}
        no_of_books = response.xpath(
            '//*[@id="zg-ordered-list"]/li/span/div/span/a[1]/@href').getall()
        for i in range(1, len(no_of_books)+1):
            partial_url = response.xpath(
                f'//*[@id="zg-ordered-list"]/li[{i}]/span/div/span/a/@href').get()
            books_urls.update({
                i: partial_url
            })

        for index, book_url in books_urls.items():
            absolute_url = f"https://www.amazon.com{book_url}"
            yield scrapy.Request(url=absolute_url, headers=self.headers,
                                 callback=self.books_details_parse,
                                 meta={'index': index})

        next_page_url = response.xpath(
            '//*[@id="zg-center-div"]/div[3]/div/ul/li[4]/a/@href').get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, headers=self.headers, callback=self.books_parse)

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

        response_info = response.meta['items_details']
        audible_details = {
            'Title': response_info['Title'],
            'Author': response_info['Author'],
            'ASIN': response_info['ASIN'],
            'Publisher': response_info['Publisher'],
            'Publication date': response_info['Publication date'],
            'Language': response_info['Language'],
            'File size': response_info['File size'],
            'Text-to-Speech': response_info['Text-to-Speech'],
            'Enhanced typesetting': response_info['Enhanced typesetting'],
            'X-Ray': response_info['X-Ray'],
            'Word Wise': response_info['Word Wise'],
            'Print length': response_info['Print length'],
            'Lending': response_info['Lending'],
            'Best Sellers Rank': response_info['Best Sellers Rank'],
            'Customer Reviews': response_info['Customer Reviews'],
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
    process.crawl(BestSellersSpider)
    process.start()

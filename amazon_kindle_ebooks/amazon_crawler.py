from scrapy.crawler import CrawlerProcess
from kindle_bestsellers import BestSellersSpider
from kindle_ebooks import EbookSpider
from kindle_audible import AudibleSpider


if __name__ == '__main__':
    choice = input("Run the following Crawler:")[0]
    process = CrawlerProcess()
    if choice == 'e':
        process.crawl(EbookSpider)
        process.start()
    elif choice == 'a':
        process.crawl(AudibleSpider)
        process.start()
    elif choice == 'b':
        process.crawl(BestSellersSpider)
        process.start()
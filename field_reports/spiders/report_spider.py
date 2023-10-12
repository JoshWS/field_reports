import scrapy
from scrapy.loader import ItemLoader
from field_reports.items import ReportItem
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from field_reports.items import ReportItem
from datetime import datetime
import csv


class ReportSpider(scrapy.Spider):
    name = "report_spider"

    def start_requests(self):
        yield scrapy.Request(
            "https://www.freeburmarangers.org/category/reports/",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod(
                        "wait_for_load_state",
                        "domcontentloaded",
                    )
                ],
                errback=self.errback,
            ),
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        # follow pagination links
        for pagination in range(2, 118):
            # Follow links to articles
            html = await page.content()
            loaded_articles = Selector(text=html)
            article_selector = loaded_articles.xpath(
                "//div[@class='neta-query-results']/article/a/@href"
            )
            for article in article_selector:
                yield response.follow(article, self.parse_article)
            if loaded_articles.xpath(
                f"//div[@id='divPagination']/a[text()='{pagination}']"
            ):
                await page.click(f"//div[@id='divPagination']/a[text()='{pagination}']")
                await page.wait_for_selector(
                    f"//div[@id='divPagination']/a[@class='paginate-button current'][text()='{pagination}']"
                )
        # Follow links to articles
        html = await page.content()
        loaded_articles = Selector(text=html)
        article_selector = loaded_articles.xpath(
            "//div[@class='neta-query-results']/article/a/@href"
        )
        for article in article_selector:
            yield response.follow(article, self.parse_article)

    def parse_article(self, response):
        l = ItemLoader(item=ReportItem(), response=response)

        # Created.
        l.add_value("created", datetime.now())

        # Slug.
        slug_raw = l.get_xpath("//header//div[@class='col-md-12']/h1//text()")
        slug = slug_raw[0].replace(" ", "-")
        l.add_value("slug", slug)

        # Sapphire url.
        sapphire_url = f"/reports/articles/{slug}"
        l.add_value("sapphire_url", sapphire_url)

        # Description.
        l.add_xpath("description", "//div[@id='main-content-wrap']//p")

        # Article date.
        l.add_xpath("article_date", "//time[@class='published']/text()")

        # Source url.
        l.add_value("source_url", response.url)

        # Author.
        l.add_value("author", "freeburmarangers")

        # Posted by.
        l.add_value("posted_by", "Joshua Westphal Da Silva")

        # Countries.
        l.add_xpath("countries", "Myanmar")

        # Attachment.
        l.add_xpath(
            "attachment", "//div[@id='main-content-wrap']//a[text()='Download']/@href"
        )

        # Images.
        l.add_xpath("images", "//div[@id='main-content-wrap']//figure/a/@href")

        return l.load_item()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

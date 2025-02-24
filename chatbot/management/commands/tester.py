from django.core.management.base import BaseCommand
import logging
from ...helpers import scrap_from_url_helper as helper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This is a utility management command for testing purpose'

    def handle(self, *args, **options):

        url = "https://en.m.wikipedia.org/wiki/%C4%80j%C4%ABvika"
        # 1. Scraping all the text within all the <p> tags:
        paragraphs = helper.scrape_content(url, "p", attribute="text")
        if paragraphs is not None:
            if paragraphs:
                for p in paragraphs:
                    print(p)
            else:
                print("No paragraphs found.")

        # 2. Scraping all the links (href attributes of <a> tags):
        links = helper.scrape_content(url, "a", attribute="href")
        if links is not None:
            if links:
                for link in links:
                    print(link)
            else:
                print("No links found.")

        # 3. Scraping the HTML content of a specific div:
        div_content = helper.scrape_content(url, "#some-specific-div")
        if div_content is not None:
            if div_content:
                for div in div_content:
                    print(div)
            else:
                print("No divs found.")

        # 4. Scraping the text within a specific class:
        class_content = helper.scrape_content(url, ".some-class", attribute="text")
        if class_content is not None:
            if class_content:
                for content in class_content:
                    print(content)
            else:
                print("No content found.")
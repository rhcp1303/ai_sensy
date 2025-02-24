import time
from django.core.management.base import BaseCommand
import logging
from ...helpers import scrape_content_from_url_helper as helper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape all visible text from a list of web urls for langchain query'

    def add_arguments(self, parser):
        parser.add_argument('--list_of_urls', nargs='+', type=str,
                            help='List of URLs of the web pages to be queried through RAG', required=True)

    def handle(self, *args, **options):
        urls = options['list_of_urls']
        for url in urls:
            scraped_data = helper.scrape_all_visible_text(url)
            if scraped_data:
                with open("temp.txt", "w") as file:
                    file.write(helper.wrap_text(scraped_data))
            else:
                print(f"Scraping failed for {url}")
            time.sleep(1)

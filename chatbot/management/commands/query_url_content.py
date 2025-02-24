import time
from django.core.management.base import BaseCommand
import logging
from ...helpers import scrape_content_from_url_helper as scrape_helper, create_embeddings_helper as embeddings_helper, \
    query_url_content_helper as query_helper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run RAG query over content scraped from a list of urls'

    def add_arguments(self, parser):
        parser.add_argument('--list_of_urls', nargs='+', type=str,
                            help='List of URLs of the web pages to be queried through RAG', required=True)

    def handle(self, *args, **options):
        urls = options['list_of_urls']
        for url in urls:
            scraped_content = scrape_helper.scrape_all_visible_text(url)
            if scraped_content:
                with open("temp.txt", "w") as file:
                    file.write(scrape_helper.wrap_text(scraped_content))
            else:
                print(f"Scraping failed for {url}")
            time.sleep(1)
        embeddings_helper.create_embeddings(scraped_content)

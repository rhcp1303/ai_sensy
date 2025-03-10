import time
from django.core.management.base import BaseCommand
import logging
from ...helpers import scrape_content_from_url_helper as helper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrape all visible text from a list of web urls for langchain query'

    """
        Scrapes all visible text from a list of web URLs for LangChain query.
    """

    def add_arguments(self, parser):

        """
                Adds command-line arguments.
        """

        parser.add_argument('--list_of_urls', nargs='+', type=str,
                            help='List of URLs of the web pages to be queried through RAG', required=True)

    def handle(self, *args, **options):

        """
                Handles the command execution.
        """

        urls = options['list_of_urls']
        total_scraped_content = []
        for url in urls:
            scraped_content = helper.scrape_all_visible_text(url)
            if scraped_content:
                total_scraped_content.append(scraped_content)
            else:
                logger.info(f"Scraping failed for {url}")
            time.sleep(1)
        combined_text = "\n\n".join(total_scraped_content)
        with open("temp/scraped_content.txt", "w") as file:
            file.write(helper.wrap_text(combined_text))

from django.core.management.base import BaseCommand
import logging
from ...helpers import create_embeddings_helper as helper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create embeddings (faiss folders) for a text file for use in langchain retrieval'

    """
    Creates embeddings (faiss folders) for a text file for use in langchain retrieval
    """

    def add_arguments(self, parser):
        """
        Adds command-line arguments.
        """

        parser.add_argument('--text_file_path', type=str,
                            help='path to the text file containing scraped content from url', required=True)

    def handle(self, *args, **options):
        """
        Handles the command execution.
        """

        text_file_path = options['text_file_path']
        with open(text_file_path, "r") as file:
            text = file.read()
        helper.create_embeddings(text, chunk_size=500, chunk_overlap=50)

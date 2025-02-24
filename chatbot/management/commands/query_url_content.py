from django.core.management.base import BaseCommand
import logging
from ...helpers import query_url_content_helper as query_helper
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run RAG query over content scraped from a list of urls'

    """
        Runs a Retrieval Augmented Generation (RAG) query.

        This command takes a list of URLs and a user query as input. It loads a pre-existing
        FAISS vector store, uses it to retrieve relevant information based on the user's
        query, and then answers the query using the retrieved context.
    """

    def add_arguments(self, parser):
        """
                Adds command-line arguments.

                Args:
                    parser (argparse.ArgumentParser): The argument parser object.
        """
        parser.add_argument('--list_of_urls', nargs='+', type=str,
                            help='List of URLs of the web pages to be queried through RAG', required=True)
        parser.add_argument('--user_query', type=str,
                            help='user query to be answered through RAG on scraped content', required=True)

    def handle(self, *args, **options):
        """
                Handles the command execution.

                This method retrieves the user query and list of URLs from the command-line options.
                It loads the FAISS vector store, calls the `answer_question` helper function to
                perform the RAG query, and prints the answer to the console.

                Args:
                    *args: Additional positional arguments (not used).
                    **options: Keyword arguments containing the command-line options.
        """
        user_query = options['user_query']
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
        vectorstore = FAISS.load_local(
            "temp/vectorstore_faiss",
            embeddings=embeddings,
            allow_dangerous_deserialization=True)
        answer = query_helper.answer_question(query=user_query, vectorstore=vectorstore)
        logger.info(answer)

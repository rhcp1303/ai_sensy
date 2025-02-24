from django.core.management.base import BaseCommand
import logging
from ...helpers import query_url_content_helper as query_helper
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run RAG query over content scraped from a list of urls'

    def add_arguments(self, parser):
        parser.add_argument('--list_of_urls', nargs='+', type=str,
                            help='List of URLs of the web pages to be queried through RAG', required=True)
        parser.add_argument('--user_query', type=str,
                            help='user query to be answered through RAG on scraped content', required=True)

    def handle(self, *args, **options):
        user_query = options['user_query']
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
        vectorstore = FAISS.load_local(
            "temp/vectorstore_faiss",
            embeddings=embeddings,
            allow_dangerous_deserialization=True)
        answer = query_helper.answer_question(query=user_query, vectorstore=vectorstore)
        print("---------------------------------------\n\n")
        print(answer)
        print("\n\n---------------------------------------")

from django.core.management.base import BaseCommand
import logging
from ...helpers import query_url_content_helper as query_helper
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import gradio as gr
import re
import os

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


def perform_qna(urls_str, user_query):
    try:
        urls = re.findall(
            r'(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))',
            urls_str)
        if not urls:
            return "No valid URLs found.", ""
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
        vectorstore_path = "temp/vectorstore_faiss"
        if not os.path.exists(vectorstore_path):
            return "Please create the vectorstore first by running the Django command.", ""
        vectorstore = FAISS.load_local(
            vectorstore_path,
            embeddings=embeddings,
            allow_dangerous_deserialization=True)
        answer = query_helper.answer_question(query=user_query, vectorstore=vectorstore)
        return answer
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return f"An error occurred: {e}", ""


with gr.Blocks() as demo:
    url_input = gr.Textbox(label="Enter URLs (one or more, separated by spaces or newlines)",
                           placeholder="https://www.example.com https://www.wikipedia.org\nhttps://www.anothersite.com")
    query_input = gr.Textbox(label="Enter your query")
    answer_output = gr.Textbox(label="Answer")
    submit_btn = gr.Button("Submit Query")

    submit_btn.click(
        fn=perform_qna,
        inputs=[url_input, query_input],
        outputs=[answer_output],
    )

demo.launch()

import logging
from .helpers import scrape_content_from_url_helper as scraping_helper, query_url_content_helper as querying_helper, \
    create_embeddings_helper as embedding_helper
import gradio as gr
import re
import time

logger = logging.getLogger(__name__)


def perform_qna(urls_str, user_query):
    try:
        urls = re.findall(
            r'(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))',
            urls_str)
        if not urls:
            return "No valid URLs found.", ""
        total_scraped_content = []
        for url in urls:
            scraped_content = scraping_helper.scrape_all_visible_text(url)
            if scraped_content:
                total_scraped_content.append(scraped_content)
            else:
                print(f"Scraping failed for {url}")
            time.sleep(1)
        combined_text = "\n\n".join(total_scraped_content)
        vectorstore = embedding_helper.create_embeddings(combined_text)
        answer = querying_helper.answer_question(query=user_query, vectorstore=vectorstore)
        return answer
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return f"An error occurred: {e}", ""


with gr.Blocks() as demo:
    url_input = gr.Textbox(label="Enter URLs (one or more, separated by commas)",
                           placeholder="https://www.example.com, https://www.wikipedia.org, https://www.anothersite.com")
    query_input = gr.Textbox(label="Enter your query")
    answer_output = gr.Textbox(label="Answer")
    submit_btn = gr.Button("Submit Query")

    submit_btn.click(
        fn=perform_qna,
        inputs=[url_input, query_input],
        outputs=[answer_output],
    )

demo.launch()

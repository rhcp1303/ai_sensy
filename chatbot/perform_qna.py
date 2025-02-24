import logging
from .helpers import scrape_content_from_url_helper as scraping_helper, query_url_content_helper as querying_helper, \
    create_embeddings_helper as embedding_helper
import gradio as gr
import re
import time

logger = logging.getLogger(__name__)

# Global variables to store the vectorstore and ingestion status
vectorstore = None
ingestion_done = False


def ingest_data(urls_str):
    global vectorstore, ingestion_done
    try:
        urls = re.findall(
            r'(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))',
            urls_str)
        if not urls:
            return "No valid URLs found."
        total_scraped_content = []
        for url in urls:
            scraped_content = scraping_helper.scrape_all_visible_text(url)
            if scraped_content:
                total_scraped_content.append(scraped_content)
            else:
                logger.log(f"Scraping failed for {url}")
            time.sleep(1)
        combined_text = "\n\n".join(total_scraped_content)
        vectorstore = embedding_helper.create_embeddings(combined_text)
        ingestion_done = True
        return "Data Ingestion Complete!!!"

    except Exception as e:
        logger.exception(f"An error occurred during ingestion: {e}")
        return f"An Error Occurred During Ingestion!!!"


def perform_qna(user_query):
    global vectorstore, ingestion_done
    if not ingestion_done:
        return "Please Ingest Data First!!!", ""
    if vectorstore is None:
        return "No Vectorstore Available. Ingestion Might Have Failed!!!", ""
    try:
        answer = querying_helper.answer_question(query=user_query, vectorstore=vectorstore)
        return answer
    except Exception as e:
        logger.exception(f"An error occurred during Q&A: {e}")
        return f"An Error Occurred During Q&A!!!", ""


with gr.Blocks() as demo:
    url_input = gr.Textbox(label="Enter URLs   ( One Or More, Separated By Commas )",
                           placeholder="https://www.example.com, https://www.wikipedia.org, https://www.anothersite.com")
    ingest_button = gr.Button("Ingest Data")
    ingest_status = gr.Textbox(label="Ingestion Status", value="")
    query_input = gr.Textbox(label="Enter Question")
    answer_output = gr.Textbox(label="Answer", lines=10)
    submit_btn = gr.Button("Ask Question")
    ingest_button.click(
        fn=ingest_data,
        inputs=[url_input],
        outputs=[ingest_status]
    ).then(
        lambda: gr.update(placeholder="Enter your question here"),
        None,
        query_input
    )
    submit_btn.click(
        fn=perform_qna,
        inputs=[query_input],
        outputs=[answer_output],
    )

demo.launch()

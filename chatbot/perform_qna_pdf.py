"""
Module: main_app  (or whatever the name of your module/file is)

This module defines a Gradio-based web application for performing question answering
over content extracted from PDFs. It uses helper functions for PDF extraction, embedding,
and querying.
"""

import logging
from .helpers import extract_text_from_pdf_helper as pdf_helper, query_url_content_helper as querying_helper, \
    create_embeddings_helper as embedding_helper
import gradio as gr
import os

logger = logging.getLogger(__name__)

vectorstore = None
ingestion_done = False


def ingest_pdf_data_from_paths(pdf_paths):
    """
        Ingests data from PDF files specified by their paths.

        This function takes a list of PDF file paths, extracts the text
        from each PDF, creates embeddings for the combined text, and stores the embeddings
        in a vector database.

        Args:
            pdf_paths (list): A list of paths to PDF files.

        Returns:
            str: A message indicating the status of the data ingestion process.
        """

    global vectorstore, ingestion_done
    try:
        if not pdf_paths:
            return "No PDF file paths provided."
        total_extracted_content = []
        for pdf_path in pdf_paths:
            try:
                if not os.path.exists(pdf_path):
                    logger.error(f"PDF file not found: {pdf_path}")
                    return f"PDF file not found: {pdf_path}"

                extracted_content = pdf_helper.extract_text(pdf_path)
                if extracted_content:
                    total_extracted_content.append(extracted_content)
                    logger.info(f"Extraction successful for {pdf_path}")
                else:
                    logger.info(f"Extraction failed for {pdf_path}")
            except Exception as pdf_err:
                logger.error(f"Error processing PDF {pdf_path}: {pdf_err}")
                return f"Error processing PDF {pdf_path}: {pdf_err}"

        combined_text = "\n\n".join(total_extracted_content)
        print("-------" + combined_text)
        vectorstore = embedding_helper.create_embeddings(combined_text)
        ingestion_done = True
        return "PDF Data Ingestion Complete!!!"

    except Exception as e:
        logger.exception(f"An error occurred during PDF ingestion: {e}")
        return f"An Error Occurred During PDF Ingestion!!!"


def perform_qna_pdf(user_query):
    """
        Performs question answering using the ingested PDF data.

        This function takes a user query, retrieves relevant information from the vector
        database, and returns the answer.

        Args:
            user_query (str): The user's question.

        Returns:
            answer (str): The answer returned from the semantic search on vector database
        """

    global vectorstore, ingestion_done
    if not ingestion_done:
        return "Please Ingest PDF Data First!!!", ""
    if vectorstore is None:
        return "No Vectorstore Available. Ingestion Might Have Failed!!!", ""
    try:
        answer = querying_helper.answer_question(query=user_query, vectorstore=vectorstore)
        return answer
    except Exception as e:
        logger.exception(f"An error occurred during PDF Q&A: {e}")
        return f"An Error Occurred During PDF Q&A!!!", ""


with gr.Blocks() as demo:
    """
       Defines the Gradio interface for PDF processing.

       This block creates the Gradio interface with text input for PDF paths, ingestion status,
       user query, and answer output. It also includes buttons to trigger data ingestion and
       question answering.
       """

    pdf_paths_input = gr.Textbox(label="Enter PDF File Paths (comma-separated)", placeholder="path1.pdf, path2.pdf")
    ingest_button = gr.Button("Ingest PDF Data")
    ingest_status = gr.Textbox(label="Ingestion Status", value="")
    query_input = gr.Textbox(label="Enter Question")
    answer_output = gr.Textbox(label="Answer", lines=10)
    submit_btn = gr.Button("Ask Question")
    ingest_button.click(
        fn=lambda paths: ingest_pdf_data_from_paths([p.strip() for p in paths.split(',')]),
        inputs=[pdf_paths_input],
        outputs=[ingest_status]
    ).then(
        lambda: gr.update(placeholder="Enter your question here"),
        None,
        query_input
    )
    submit_btn.click(
        fn=perform_qna_pdf,
        inputs=[query_input],
        outputs=[answer_output],
    )

demo.launch()
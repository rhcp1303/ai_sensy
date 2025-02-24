# My Awesome Q&A Web App

This web application allows you to ask questions about content scraped from URLs. It uses Retrieval Augmented Generation (RAG) to provide answers based on the ingested data.

## Installation

1. Clone the repository:

        git clone https://github.com/rhcp1303/ai_sensy.git

2. Create a virtual environment (recommended):

        python3 -m venv .venv  # Or virtualenv .venv
        source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install the dependencies:

            pip install -r requirements.txt

4. Install the specific Langchain package versions:

         pip install langchain==0.0.245
         pip install langchain_huggingface==0.0.3
         pip install langchain_community==0.0.2
5. Create the temp directory for storing the temporary files in the root project directory:

         mkdir temp


6. Run the following command from the root directory of the django project:

         python -m chatbot.perform_qna.py

7. Open your web browser and go to the URL provided by Gradio

         http://127.0.0.1:7860





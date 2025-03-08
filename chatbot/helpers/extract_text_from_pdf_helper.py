import os
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import pdfplumber
import google.generativeai as genai
import time
import pytesseract

def extract_page_text(pdf_file_path, page_number):
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            page = pdf.pages[page_number]
            extracted_text = page.extract_text()
            if extracted_text is None:
                return ""
            print(extracted_text)
            return extracted_text
    except Exception as e:
        raise


def extract_text(pdf_file_path):
    try:
        number_of_pages = len(pdfplumber.open(pdf_file_path).pages)
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(
                executor.map(extract_page_text, [pdf_file_path] * number_of_pages, range(number_of_pages)))
            return "\n".join(results)
    except Exception as e:
        print(f"Error processing digital single-column PDF: {e}")

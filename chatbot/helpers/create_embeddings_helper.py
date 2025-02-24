from langchain.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter


def create_embeddings(text, chunk_size, chunk_overlap):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator=".")
    pdf_chunks = text_splitter.split_text(text)
    print(f"number of pdf chunks created: {len(pdf_chunks)}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    vectorstore = FAISS.from_texts(pdf_chunks, embeddings)
    return vectorstore

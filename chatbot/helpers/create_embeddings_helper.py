from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS


def create_embeddings(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator=".")
    text_chunks = text_splitter.split_text(text)
    print(f"number of text chunks created: {len(text_chunks)}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    vectorstore.save_local("temp/vectorstore_faiss")
    return vectorstore

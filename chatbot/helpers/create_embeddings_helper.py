import logging

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)


def create_embeddings(text, chunk_size=1000, chunk_overlap=200):
    """Creates and saves a FAISS vectorstore from input text.

        This function takes a string of text, splits it into chunks, generates
        embeddings for each chunk using a Hugging Face model, and then creates and
        saves a FAISS vectorstore to disk.

        Args:
            text (str): The input text to be used for creating the vectorstore.
            chunk_size (int, optional): The size of each text chunk. Defaults to 1000.
            chunk_overlap (int, optional): The number of overlapping characters
                between chunks. Defaults to 200.

        Returns:
            FAISS: The created FAISS vectorstore object.

        Raises:
            Exception: If any error occurs during the process (text splitting,
                       embedding generation, or vectorstore creation/saving).

        Example:
            >>> text = "This is a long text to be embedded."
            >>> vectorstore = create_embeddings(text)
            >>> print(type(vectorstore))
            <class 'langchain_community.vectorstores.faiss.FAISS'>

            >>> # To load the vectorstore later:
            >>> embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
            >>> loaded_vectorstore = FAISS.load_local("temp/vectorstore_faiss", embeddings)
        """
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator=".")
    text_chunks = text_splitter.split_text(text)
    logger.info(f"number of text chunks created: {len(text_chunks)}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    vectorstore.save_local("temp/vectorstore_faiss")
    return vectorstore

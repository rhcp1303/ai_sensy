from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

api_key = "AIzaSyBq2_GdMf0KhowSVSb0hn4Z_8B81kBewXY"
os.environ["GOOGLE_API_KEY"] = api_key


def answer_question(query, vectorstore):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        retriever = vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                               return_source_documents=True)
        template = """Use the following pieces of context to answer the question at the end. If the answer is not in the context, say "I don't know".

        {context}

        Question: {question}
        Helpful Answer:"""
        prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )
        qa_chain.combine_documents_chain.llm_chain.prompt = prompt
        result = qa_chain({"query": query})
        answer = result['result']
        return answer

    except Exception as e:
        print(f"An error occurred during question answering: {e}")
        return "An error occurred.", []

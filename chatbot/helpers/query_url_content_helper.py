from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from ..helpers.prompt_helper import prompt_template

api_key = "AIzaSyBq2_GdMf0KhowSVSb0hn4Z_8B81kBewXY"
os.environ["GOOGLE_API_KEY"] = api_key


def answer_question(query, vectorstore):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        retriever = vectorstore.as_retriever(k=10)
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                               return_source_documents=True)
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        qa_chain.combine_documents_chain.llm_chain.prompt = prompt
        result = qa_chain({"query": query})
        answer = result['result']
        return answer

    except Exception as e:
        print(f"An error occurred during question answering: {e}")
        return "An error occurred.", []

from flask import Flask, request, jsonify
import openai
import requests
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import openai
import tiktoken
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# Set up the Flask application
app = Flask(__name__)

# Set up the OpenAI API key
openai.api_key = "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"


# Define the Flask endpoint for answering questions
@app.route("/wa_answer", methods=["POST"])
def answer_wa_question():
    # Get the question from the request
    question = request.json["question"]
    answer = loadData(question)

    # Return the answer
    response = {
        "question": question,
        "answer": answer
    }
    return jsonify(response)
def loadData(question):
    loader = PyPDFLoader("/Users/himavadlamani/Desktop/ai project/WA_handbook.pdf")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    
    #api constants
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '3ad26d4d-dc27-4f87-9919-70909e0ae9d1')
    PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'us-central1-gcp')
    
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(
    api_key = PINECONE_API_KEY,  # find at app.pinecone.io
    environment = PINECONE_API_ENV# next to api key in console
    )
    index_name = "westfordacademy"
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY) #temperature = randomness and creativity
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = docsearch.similarity_search(question)
    response = chain.run(input_documents=docs, question=question)
    return response


# Start the Flask application
if __name__ == "__main__":
    app.run(port=8000,debug=True)


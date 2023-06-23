from flask import Flask, render_template, request, jsonify
#Create Embeddings of your documents to get ready for semantic search 
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import pinecone 
import os

app = Flask(__name__)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '0b0244fc-fee8-43c0-8f6a-ec6bad3b2dcc')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'northamerica-northeast1-gcp') 
docsearch = None


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gpt")
def gpt():
    print("Hit GPT route..")
    return render_template("gpt.html")

@app.route("/mosiac")
def mosiac():
    print("Hit the mosiac route")
    return render_template("mosiac.html")

@app.route("/files/", methods=["POST"])
def create_file():
    print("Created the files....")
    file = request.files["file"]
    if file:
        file.save(f"uploads/{file.filename}")
        # return {"filename": file.filename}
        return render_template("index.html")
    return {"error": "No file provided."}

@app.route("/chatbot", methods=["POST"])
def chatbot_endpoint():
    global docsearch
    user_message = request.json.get("message")
    if user_message:
        # Process the user message and generate a bot response
        # Replace the code below with your chatbot logic
        # bot_message = f"Bot: You said '{user_message}'"
        # query = "What are examples of good data science teams ?"
            #Load your data
        loader = UnstructuredPDFLoader(os.path.join(os.getcwd(), 'uploads', "field-guide-to-data-science.pdf"))
        print("Done with loading the pdf file...")

        data = loader.load()

        print(f'You have {len(data)} documents in your data')
        print(f'There are  {len(data[0].page_content)} characters in your documents')

        # Chunk your data up into smaller documents 
        text_spliter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=0)
        texts = text_spliter.split_documents(data)

        print(f'Now you have {len(texts)} documents')


        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
        PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '0b0244fc-fee8-43c0-8f6a-ec6bad3b2dcc')
        PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'northamerica-northeast1-gcp')

        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        pinecone.init(
            api_key = PINECONE_API_KEY,
            environment=PINECONE_API_ENV
        )
        index_name = "datascience-book"

        docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

        query = user_message
        print(f"Query:{query}")
        docs = docsearch.similarity_search(query)

        # Here's an example of the first document that was returned 
        # print(docs[0].page_content[:450])

        #Query those docs to get your answer back 
        llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
        chain = load_qa_chain(llm, chain_type="stuff")

        query= "What is the Impact of Data Science?"
        docs = docsearch.similarity_search(query)
        answer = chain.run(input_documents=docs, question=query)
        print(f"Answer:{answer}")
        return {"message": answer}
    return {"error": "No message provided."}


@app.route("/train-function", methods=["POST"])
def my_function():
    global docsearch
    # Implement your function logic here
    # Access any data passed from JavaScript using request.json
    # Perform any necessary computations or actions
    # Return a response, if needed

    # For example, you can return a JSON response
    print("This is button click")
    #Load your data
    loader = UnstructuredPDFLoader(os.path.join(os.getcwd(), 'uploads', "field-guide-to-data-science.pdf"))
    print("Done with loading the pdf file...")

    data = loader.load()

    print(f'You have {len(data)} documents in your data')
    print(f'There are  {len(data[0].page_content)} characters in your documents')

    # Chunk your data up into smaller documents 
    text_spliter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=0)
    texts = text_spliter.split_documents(data)

    print(f'Now you have {len(texts)} documents')


    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '0b0244fc-fee8-43c0-8f6a-ec6bad3b2dcc')
    PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'northamerica-northeast1-gcp')

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    pinecone.init(
        api_key = PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
    index_name = "datascience-book"

    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

    response = {"message": "Function called successfully"}
    return jsonify(response)

@app.route("/voice")
def voice():
    return render_template("voice.html")

@app.route("/github_links")
def github_links():
    return render_template("github_links.html")

if __name__ == "__main__":
    app.run(debug=True)

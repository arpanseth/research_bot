from flask import Flask, request, render_template, session
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import openai
from utils import *

#MODEL_NAME = "gpt-3.5-turbo-16k" 
MODEL_NAME = "ft:gpt-3.5-turbo-1106:personal:ignacio:9hfPEnGH"

# Create flask app
app = Flask(__name__)
app.secret_key = '12345'  # Replace with a real secret key

# Set up OpenAI API key here instead of environment variable
#os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Initialize ChatOpenAI
llm = ChatOpenAI(temperature=1.0, model=MODEL_NAME)

# Initialize embeddings model using OpenaAI
embeddings = OpenAIEmbeddings()

# Initialize Chroma as the vectorstore to point at the chroma_db folder
vectorstore = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")


# Main endpoint for the flask app
@app.route("/")
def home():
    session.clear()
    return render_template("home.html")

# Chat route 
@app.route("/chat", methods=["POST"])
def chat():
    # Get user request from post
    user_message = request.form["message"]
    
    # Initialize or retrieve conversation memory for the session
    if 'conversation_memory' not in session:
        session['conversation_memory'] = []
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        human_prefix="Human",
        ai_prefix="AI",
        output_key='answer'
    )
    
    for message_dict in session['conversation_memory']:
        memory.chat_memory.add_message(deserialize_message(message_dict))
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    
    # Define a custom prompt with system message
    system_message = open('system_message.txt', 'r').read()
    template = system_message + """

    {context}

    Question: {question}
    Answer:"""

    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )
    #print(f"Number of documents in Chroma: {vectorstore._collection.count()}")
    

    # Set up the conversational chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever = retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )
    
    # Get the response from the model
    try:
        response = qa.invoke({"question": user_message})
        ai_message = response['answer']
    except openai.OpenAIError as e:
        return f"OpenAI API error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
    
    # Print retrieved documents to see how good the RAG is
    # print("Retrieved documents:")
    # for doc in response['source_documents']:
    #     print(f"Content: {doc.page_content}")
    #     print(f"Metadata: {doc.metadata}")
    #     print("---")

    # Update the conversation memory
    memory.chat_memory.add_user_message(user_message)
    memory.chat_memory.add_ai_message(ai_message)
    
    # Save the updated memory to the session
    session['conversation_memory'] = [serialize_message(msg) for msg in memory.chat_memory.messages]
    print(session['conversation_memory'])
    return ai_message

if __name__ == "__main__":
    app.run(debug=True)
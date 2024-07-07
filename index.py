# index_new_pdfs_with_chroma.py

import os
import json
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
#from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os


def load_indexed_pdfs(metadata_file):
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            return json.load(f)
    return []

def save_indexed_pdfs(metadata_file, indexed_pdfs):
    with open(metadata_file, 'w') as f:
        json.dump(indexed_pdfs, f)

def index_pdf(pdf_directory, chroma_db_path="./chroma_db", chunk_size=500, chunk_overlap=100, metadata_file="indexed_pdfs.json"):

    # Initialize embeddings
    embeddings = OpenAIEmbeddings()

    # Initialize Chroma database
    chroma = Chroma(persist_directory=chroma_db_path, embedding_function=embeddings)

    # Load indexed PDFs metadata
    indexed_pdfs = load_indexed_pdfs(metadata_file)

    # Get the list of PDF files in the specified directory
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

    # Filter out PDFs that have already been indexed
    new_pdfs = [pdf for pdf in pdf_files if pdf not in indexed_pdfs]

    if not new_pdfs:
        print("No new PDFs to index.")
        return

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    #text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    for filename in new_pdfs:
        loader = PyPDFLoader(os.path.join(pdf_directory, filename))
        documents = loader.load()
        docs = text_splitter.split_documents(documents)
        # Add documents to the vectorstore
        chroma.add_documents(docs)
        indexed_pdfs.append(filename)
    
    save_indexed_pdfs(metadata_file, indexed_pdfs)

    print(f"Indexed {len(new_pdfs)} new PDFs.")

if __name__ == '__main__':
    pdf_directory = "pdfs"
    index_pdf(pdf_directory)

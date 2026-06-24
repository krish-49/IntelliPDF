# python.exe -m pip install --upgrade pip
import streamlit as st
from dotenv import load_dotenv  
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def get_pdf_text(pdf_docs):   # get raw text from pdfs
    text = "" 
    for pdf in pdf_docs:      # loop each pdf
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages: # loop each page + append text 
            text += page.extract_text() 
    
    return text

def get_text_chunks(text):   # splitting text into smaller chunks
    text_splitter = CharacterTextSplitter( # just by using one function
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def getvectorstore(text_chunks):   # create vector store from text chunks
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def main():
    load_dotenv()  # Load env var from .env

    st.set_page_config(page_title="Ask multiple PDFs", page_icon=":books:", layout="wide")

    st.header("Ask multiple PDFs :books:")

    st.text_input("Ask your question here:")

    with st.sidebar:
        st.subheader("Upload your PDFs / Documents")

        pdf_docs = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

        if st.button("Process PDFs"):
            with st.spinner("Processing..."):

                # Get text from pdfs
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)

                # get text chunks(converting raw text)
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)

                # get vector store
                vectorstore = get_vectorstore(text_chunks)


if __name__ == "__main__":
    main()
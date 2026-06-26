# python.exe -m pip install --upgrade pip
import streamlit as st
from dotenv import load_dotenv  
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from htmlTemplates import css, bot_template, user_template

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

def get_vectorstore(text_chunks):   # create vector store from text chunks
    # embeddings = OpenAIEmbeddings()
    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2"
)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):   # create a conversation chain
    # llm = ChatOpenAI()
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userQue(user_que):
    response = st.session_state.conversation({'question' : user_que})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()  # Load env var from .env

    st.set_page_config(page_title="Ask multiple PDFs", page_icon=":books:", layout="wide")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Ask multiple PDFs :books:")

    user_que = st.text_input("Ask your question here:")

    if user_que:
        handle_userQue(user_que)

    st.write(user_template.replace("{{MSG}}", "Hello robot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello dear"), unsafe_allow_html=True)

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

                # create a conversation chain(a system)
                st.session_state.conversation = get_conversation_chain(vectorstore)
    
    
if __name__ == "__main__":
    main()
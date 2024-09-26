import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')

# Initialize the Chat model Gemini-pro Model
model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

#PDF Text Extraction from the Pdf ,Function
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

#Function to load FAISS index
def load_faiss_index():
    embeddings = GoogleGenerativeAIEmbeddings(api_key=google_api_key, model="models/embedding-001")
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

#Title
st.title("AI-Enhanced Q&A and MCQ Content Generator")

#Sider bar for the PDF Uploader
with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Upload your PDF file:", type=["pdf"])
    if uploaded_file is not None:
        # Extract text from uploaded PDF
        extracted_text = get_pdf_text([uploaded_file])
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splitter.split_text(extracted_text)
        
        # Create and save FAISS index
        embeddings = GoogleGenerativeAIEmbeddings(api_key=google_api_key, model="models/embedding-001")
        vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
        
        st.success("PDF processed and FAISS index created!")

# Main content - User inputs for MCQ Generation and Chat with PDF
if uploaded_file:
    # MCQ Generation Input
    st.header("Generate Multiple Choice Questions (MCQs)")
    mcq_batch_size = st.number_input("How many MCQs would you like to generate?", min_value=1, max_value=20, value=5)
    mcq_topic = st.text_input("What topic would you like the MCQs to focus on?")

    if st.button("Generate MCQs"):
        if mcq_topic:
            new_db = load_faiss_index()
            docs = new_db.similarity_search(mcq_topic)
            context = " ".join([doc.page_content for doc in docs])

            #prompt Template for the MCQ generation 
            mcq_prompt_template = """
            You are an expert question paper creator specializing in technical subjects.
            Generate {batch_size} unique multiple-choice questions (MCQs) based on the provided context extracted from the PDF.
            Ensure that the questions are completely original and free from plagiarism.
            Each question should be accompanied by four answer choices labeled 
            (A)\n
            (B)\n
            (C)\n
            (D).\n
            Context: {context}
            """
            prompt = PromptTemplate(template=mcq_prompt_template, input_variables=["batch_size", "context"])
            chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
            
            # Generate MCQs
            response = chain({"input_documents": docs, "context": context, "batch_size": mcq_batch_size}, return_only_outputs=True)
            st.write("Generated MCQs:", response.get("output_text", "No output generated."))
        else:
            st.warning("Please specify a topic for the MCQs.")
    
    # Chat with PDF Input
    st.header("Chat with PDF")
    user_question = st.text_input("Ask a question based on the PDF content:")
    
    if st.button("Get Answer"):
        if user_question:
            new_db = load_faiss_index()
            docs = new_db.similarity_search(user_question)
            context = " ".join([doc.page_content for doc in docs])

            # Prompt Template For the  Q&A.
            qa_prompt_template = """Answer the Question as Detailed as possible from the provided context,
                                    make sure to provide all the details. If the answer is not in the provided context, just say "The answer is not available in the provided PDF."
                                    Context: \n{context}\n
                                    Question: \n{question}\n
                                    Answer:"""
            prompt = PromptTemplate(template=qa_prompt_template, input_variables=["context", "question"])
            chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
            
            # Generate response
            response = chain({"input_documents": docs, "context": context, "question": user_question}, return_only_outputs=True)
            st.write("Answer:", response.get("output_text", "No output generated."))

else:
    st.warning("Please upload a PDF file to proceed.")

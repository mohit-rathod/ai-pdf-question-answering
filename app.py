import streamlit as st
import os
import warnings
warnings.filterwarnings("ignore")
from db_connectorr import store_raptor_dict_in_postgres, document_exists
from raptor import recursive_embed_cluster_summarize
from doc_retriever import return_docs
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import get_llm
import tempfile
from pdf_texts import load_pdf_text

import nest_asyncio

nest_asyncio.apply()


os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize LLM model
model = get_llm()

# Streamlit UI
st.title("PDF Document Question Answering")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
question = st.text_input("Enter your question:")

if uploaded_file and question:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load text from PDF
        doc_texts = load_pdf_text(file_path)
        
        # Check if document already exists in database
        if document_exists(doc_texts):
            st.write("Document already exists in the database. Fetching relevant information...")
        else:
            # Process document if it doesn't exist
            results = recursive_embed_cluster_summarize([doc_texts], level=1, n_levels=5)
            
            # Store results in Postgres
            store_raptor_dict_in_postgres(results)
        
        # Retrieve relevant documents
        retrieved_docs_text = return_docs(question, 5)
        
        # Define prompt
        template = """You are an expert information retrieval assistant. Your task is to answer the following question using only the information provided in the documents below. Do not incorporate any external knowledge or assumptions. If the answer is not explicitly present in the documents, respond with \"I don't know.\" and do not mention anything else apart from I don't know. Provide a concise and accurate answer that is directly supported by the context.

        Documents:
        {context}

        Question:
        {question}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model | StrOutputParser()
        
        # Generate answer
        answer = chain.invoke({"context": retrieved_docs_text, "question": question})
        
        st.subheader("Answer:")
        st.write(answer)
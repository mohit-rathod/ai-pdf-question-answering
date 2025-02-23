# AI-Powered PDF Question Answering System

## Overview
This project is an AI-powered application that enables users to:

- Upload PDF documents.
- Extract text from the uploaded PDFs.
- Store and retrieve document embeddings in a PostgreSQL database using PgVector for efficient querying.
- Ask questions based on the stored documents and receive relevant answers.
- Interact with the system through a Streamlit-based user interface.

## Features
- **Backend (AI/ML & Database)**
  - Extract text from PDFs using LangChain.
  - Generate embeddings using a SentenceTransformers model.
  - Store embeddings in PostgreSQL for fast vector retrieval.
  - Perform document retrieval using PgVector.
- **Frontend (Streamlit UI)**
  - Upload PDF documents.
  - Query the system with questions.
  - Display retrieved responses dynamically.

## Tech Stack
- **Programming Language:** Python
- **Frontend:** Streamlit
- **Backend:** PostgreSQL with PgVector extension
- **ML/NLP:** LangChain, Hugging Face SentenceTransformers
- **Vector Storage:** PostgreSQL with PgVector

## Installation & Setup

### Prerequisites
- Install Python (>=3.8)
- Install PostgreSQL and ensure the PgVector extension is enabled.

### Step 1: Clone the Repository
```sh
git clone https://github.com/mohit-rathod/ai-pdf-question-answering
cd ai-pdf-question-answering
```

### Step 2: Set Up Environment Variables
Create a `.env` file and set up your PostgreSQL credentials:
```env
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=yourpassword
PG_DBNAME=yourdbname
```

### Step 3: Run Database Migrations
Ensure your PostgreSQL database is running and execute:
```sh
python -c 'from db_connector import create_table_if_not_exists; create_table_if_not_exists()'
```

### Step 4: Run the Application
```sh
streamlit run app.py
```

## Application Flow
1. **Uploading PDFs**
   - Users upload a PDF document via the Streamlit UI.
   - The system extracts text using `PyMuPDFLoader`.
   - If the document does not exist in the database, embeddings are generated and stored.

2. **Processing and Storing Data**
   - The extracted text is embedded using `Hugging Face Embeddings`.
   - Clustering and summarization are performed using Gaussian Mixture Models and UMAP.
   - The embeddings are stored in PostgreSQL with PgVector.

3. **Querying the System**
   - Users enter questions in the Streamlit UI.
   - The system retrieves the most relevant documents using vector search.
   - A language model (LLM) processes the retrieved data and generates an answer.

## Key Components

### `app.py`
Handles the Streamlit UI, document upload, processing, and querying.

### `db_connector.py`
Manages PostgreSQL connections, document insertion, and retrieval.

### `raptor.py`
Performs text embedding, clustering, and summarization using Gaussian Mixture Models and UMAP.

### `doc_retriever.py`
Retrieves relevant documents based on user queries using vector search.

### `llm.py`
Handles language model inference for answering user queries.

### `pdf_texts.py`
Extracts text from PDFs using `PyMuPDFLoader`.

## Architectural Decisions & Trade-offs
- **PgVector for Vector Search:**
  - Allows efficient document retrieval but requires additional setup.
- **LangChain for Text Processing:**
  - Provides modular NLP functionality but adds dependencies.
- **Streamlit for UI:**
  - Quick to build and deploy but may not be as customizable as React or Vue.

## Future Improvements
- **Support for Multiple LLMs:** Extend to support OpenAI, Gemini, or other LLMs.
- **Enhanced Retrieval Methods:** Implement hybrid search combining keyword and vector search.
- **Caching Mechanism:** Improve query performance with caching layers.



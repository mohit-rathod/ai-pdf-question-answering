import os
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf_texts_from_folder(folder_path: str):
    """
    Reads all .pdf files in the specified folder using PyMuPDFLoader 
    and returns their page contents as a list of strings (doc_texts).
    """
    doc_texts = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            
            # Load the PDF, returns a list of Document objects
            loader = PyMuPDFLoader(pdf_path)
            docs = loader.load()
            
            # Extract text from each page in the PDF
            for doc in docs:
                doc_texts.append(doc.page_content)

    return doc_texts


def load_pdf_text(pdf_path: str) -> str:
    """
    Reads a single PDF file using PyMuPDFLoader and returns its combined page contents as a single string.
    
    Parameters:
      pdf_path (str): The file path to the PDF.
      
    Returns:
      A string containing the combined text of all pages in the PDF.
    """
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    # Combine all page texts with newlines in between.
    full_text = "\n\n".join(doc.page_content for doc in docs)
    return full_text
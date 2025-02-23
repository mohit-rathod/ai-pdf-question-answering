from langchain_ollama import OllamaLLM 

def generate_response(context: str, question: str, temperature: float = 0.0) -> str:
    prompt = (
        f"Answer the following question based on the context provided.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    llm = OllamaLLM(model="llama3.2", temperature=temperature)
    response = llm(prompt)
    return response


def get_llm():
    return OllamaLLM(model="llama3.2")
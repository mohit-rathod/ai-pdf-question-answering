from langchain_community.vectorstores import PGVector
from db_connectorr import get_connection, get_connection_string
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
embd = HuggingFaceEmbeddings(model_name=embedding_model)


def return_docs(question, n):
    """
    Converts the question into an embedding, then queries the PostgreSQL database 
    to retrieve the top-n nearest documents based on Euclidean distance.
    """
    # Convert the question to an embedding vector.
    query_embedding = embd.embed_query(question)
    
    # Convert to list if necessary.
    if hasattr(query_embedding, "tolist"):
        query_vector = query_embedding.tolist()
    else:
        query_vector = query_embedding

    # Convert the list to a string in the format "[x,y,z,...]"
    query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"

    conn = get_connection()
    cur = conn.cursor()
    
    # Use the <-> operator to compute Euclidean distance between vectors.
    # Cast the parameter to the vector type.
    sql = """
    SELECT id, content 
    FROM documents
    ORDER BY embedding <-> %s::vector
    LIMIT %s;
    """
    cur.execute(sql, (query_vector_str, n))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results



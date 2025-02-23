import psycopg2
import os


def get_connection():
    """
    Create and return a new PostgreSQL connection.
    Adjust host/user/password/dbname as needed.
    """
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5432"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD", ""),
        dbname=os.getenv("PG_DBNAME", "")
    )
    return conn

import os

def get_connection_string():
    host = os.getenv("PG_HOST", "localhost")
    port = os.getenv("PG_PORT", "5432")
    user = os.getenv("PG_USER", "postgres")
    password = os.getenv("PG_PASSWORD", "")
    dbname = os.getenv("PG_DBNAME", "")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"


def create_table_if_not_exists():
    """
    Creates the 'documents' table (if it doesn’t exist) 
    with a vector column for embeddings, and a generated column for the MD5 hash of content.
    A unique index is then created on the hash to enforce uniqueness.
    """
    conn = get_connection()
    cur = conn.cursor()
    # Create the table with an extra generated column "content_md5"
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384),
        content_md5 TEXT GENERATED ALWAYS AS (md5(content)) STORED
    );
    """
    cur.execute(create_table_sql)
    conn.commit()
    # Create a unique index on the generated column
    create_index_sql = """
    CREATE UNIQUE INDEX IF NOT EXISTS documents_content_md5_idx
    ON documents (content_md5);
    """
    cur.execute(create_index_sql)
    conn.commit()
    cur.close()
    conn.close()



def insert_document(content, embedding):
    """
    Inserts a new row into the 'documents' table with the text content and embedding.
    If an entry with the same content already exists (based on its MD5 hash), do not insert a duplicate;
    instead, return the existing row's id.
    """
    # Convert numpy array to list if necessary.
    if hasattr(embedding, "tolist"):
        embedding = embedding.tolist()
    
    conn = get_connection()
    cur = conn.cursor()
    
    insert_sql = """
    INSERT INTO documents (content, embedding) 
    VALUES (%s, %s)
    ON CONFLICT (content_md5) DO NOTHING
    RETURNING id;
    """
    cur.execute(insert_sql, (content, embedding))
    result = cur.fetchone()
    
    if result is None:
        # Entry already exists. Retrieve its id.
        cur.execute("SELECT id FROM documents WHERE content_md5 = md5(%s);", (content,))
        result = cur.fetchone()
    
    new_id = result[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id



def store_raptor_dict_in_postgres(raptor_dict):
    """
    Iterates through each level in the raptor_dict, 
    inserts rows from df_clusters & df_summary into the 'documents' table.
    """
    # Ensure the documents table is created
    create_table_if_not_exists()

    for level, (df_clusters, df_summary) in raptor_dict.items():
        print(f"\n--- Processing level {level} ---")

        # 1) Insert df_clusters rows
        for idx, row in df_clusters.iterrows():
            text_content = row["text"]
            embedding = row["embd"]  

            # Insert into db
            new_id = insert_document(text_content, embedding)
            print(f"Inserted df_clusters row {idx} -> ID {new_id}")

        # 2) Insert df_summary rows
        for idx, row in df_summary.iterrows():
            text_content = row["summaries"]
            # If you have no summary embedding, use a placeholder or re-embed
            # For now, let's just do zeros:
            embedding_zeros = [0.0]*384  # if table is vector(1536)
            # Or if your table is vector(384): embedding_zeros = [0.0]*384

            new_id = insert_document(text_content, embedding_zeros)
            print(f"Inserted df_summary row {idx} -> ID {new_id}")


def empty_documents_table():
    """
    Empties the 'documents' table by truncating it, which removes all rows and resets any identity columns.
    """
    conn = get_connection()
    cur = conn.cursor()
    # TRUNCATE is faster than DELETE and resets the serial ID counter
    cur.execute("TRUNCATE TABLE documents RESTART IDENTITY;")
    conn.commit()
    cur.close()
    conn.close()
    print("The 'documents' table has been emptied.")
    

def document_exists(content):
    """
    Check if a document already exists in the database based on its MD5 hash.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM documents WHERE content_md5 = md5(%s);", (content,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count > 0
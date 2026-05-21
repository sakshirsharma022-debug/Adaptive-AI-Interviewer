from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_embedding():

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    return embedding_model

def create_vector_store(chunks):

    embedding_model = load_embedding()
    vector_store = FAISS.from_texts(chunks, embedding_model)
    return vector_store

def retrieve_relevant_context(
        vectore_store,
        query
):
    
    docs = vectore_store.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    return context
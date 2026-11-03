from pathlib import Path

from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma

from document_loader import load_documents
from text_splitter import split_documents


MODEL_NAME = "all-MiniLM-L6-v2"

VECTOR_PATH = Path(__file__).parent / "knowledge_base" / "vector_store"


class SentenceTransformerEmbeddings(Embeddings):

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_documents(self, texts):
        vectors = self.model.encode(
            texts,
            convert_to_numpy=True
        )
        return vectors.tolist()

    def embed_query(self, text):
        vector = self.model.encode(
            text,
            convert_to_numpy=True
        )
        return vector.tolist()


def create_vector_database():

    print("Loading policy documents...")

    documents = load_documents()

    print("Splitting documents...")

    chunks = split_documents(documents)

    print("Loading embedding model...")

    embeddings = SentenceTransformerEmbeddings()

    print("Creating ChromaDB vector database...")

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTOR_PATH),
        collection_name="resolveai_knowledge"
    )

    print("\nVector database created successfully!")
    print("Total chunks stored:", vector_db._collection.count())

    return vector_db


def search_knowledge_base(query, k=3):

    embeddings = SentenceTransformerEmbeddings()

    vector_db = Chroma(
        persist_directory=str(VECTOR_PATH),
        embedding_function=embeddings,
        collection_name="resolveai_knowledge"
    )

    results = vector_db.similarity_search(
        query,
        k=k
    )

    return results


if __name__ == "__main__":

    create_vector_database()

    print("\nTesting semantic search...")

    results = search_knowledge_base(
        "What is the refund period?"
    )

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("Source:", result.metadata.get("source"))
        print("Content:", result.page_content)

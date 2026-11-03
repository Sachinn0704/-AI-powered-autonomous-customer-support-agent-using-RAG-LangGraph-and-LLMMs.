from sentence_transformers import SentenceTransformer

from text_splitter import split_documents
from document_loader import load_documents


MODEL_NAME = "all-MiniLM-L6-v2"


def generate_embeddings():

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    documents = load_documents()
    chunks = split_documents(documents)

    texts = [chunk.page_content for chunk in chunks]

    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    print("\nEmbedding generation completed!")
    print("Total chunks:", len(chunks))
    print("Embedding dimensions:", vectors.shape)

    return chunks, vectors, model


if __name__ == "__main__":

    chunks, vectors, model = generate_embeddings()

    print("\nFirst embedding:")
    print(vectors[0][:10])
